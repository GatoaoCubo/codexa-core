/**
 * Product Management Module
 * Handles all CRUD operations for products
 */

import { api } from './api/client';

// State management
let currentEditingProduct: Product | null = null;

/**
 * Initialize product management
 */
export function initializeProducts() {
  loadProducts();
  initializeProductModal();
  initializeAddProductButton();
}

/**
 * Load and display all products
 */
async function loadProducts() {
  const productsList = document.getElementById('products-list');
  if (!productsList) return;

  try {
    productsList.innerHTML = '<p class="loading-products">Loading products...</p>';

    const response = await api.getAllProducts();

    if (response.error) {
      throw new Error(response.error);
    }

    if (response.products.length === 0) {
      productsList.innerHTML = '<p class="no-products">No products yet. Click "+ Add Product" to create one.</p>';
      return;
    }

    // Render products
    productsList.innerHTML = response.products.map(product => renderProductCard(product)).join('');

    // Attach event listeners
    attachProductEventListeners();

  } catch (error) {
    console.error('Failed to load products:', error);
    productsList.innerHTML = `<p class="error-message">Failed to load products: ${error instanceof Error ? error.message : 'Unknown error'}</p>`;
  }
}

/**
 * Render a single product card
 */
function renderProductCard(product: Product): string {
  const statusClass = product.is_active ? 'status-active' : 'status-inactive';
  const statusText = product.is_active ? 'Active' : 'Inactive';
  const price = formatCurrency(product.price);
  const createdDate = product.created_at ? new Date(product.created_at).toLocaleDateString('pt-BR') : 'N/A';

  return `
    <div class="product-card" data-product-id="${product.id}">
      <div class="product-header">
        <h4 class="product-name">${escapeHtml(product.name)}</h4>
        <span class="product-status ${statusClass}">${statusText}</span>
      </div>

      ${product.description ? `<p class="product-description">${escapeHtml(product.description)}</p>` : ''}

      <div class="product-details">
        <div class="product-detail">
          <span class="detail-label">Price:</span>
          <span class="detail-value price">${price}</span>
        </div>

        <div class="product-detail">
          <span class="detail-label">Stock:</span>
          <span class="detail-value">${product.stock_quantity} units</span>
        </div>

        ${product.category ? `
        <div class="product-detail">
          <span class="detail-label">Category:</span>
          <span class="detail-value">${escapeHtml(product.category)}</span>
        </div>
        ` : ''}

        ${product.marketplace ? `
        <div class="product-detail">
          <span class="detail-label">Marketplace:</span>
          <span class="detail-value">${escapeHtml(product.marketplace)}</span>
        </div>
        ` : ''}

        ${product.sku ? `
        <div class="product-detail">
          <span class="detail-label">SKU:</span>
          <span class="detail-value">${escapeHtml(product.sku)}</span>
        </div>
        ` : ''}

        <div class="product-detail">
          <span class="detail-label">Created:</span>
          <span class="detail-value">${createdDate}</span>
        </div>
      </div>

      <div class="product-actions">
        <button class="action-button edit-product" data-product-id="${product.id}">
          ✏️ Edit
        </button>
        <button class="action-button delete-product" data-product-id="${product.id}">
          🗑️ Delete
        </button>
      </div>
    </div>
  `;
}

/**
 * Attach event listeners to product cards
 */
function attachProductEventListeners() {
  // Edit buttons
  document.querySelectorAll('.edit-product').forEach(button => {
    button.addEventListener('click', handleEditProduct);
  });

  // Delete buttons
  document.querySelectorAll('.delete-product').forEach(button => {
    button.addEventListener('click', handleDeleteProduct);
  });
}

/**
 * Initialize "Add Product" button
 */
function initializeAddProductButton() {
  const addButton = document.getElementById('add-product-button');
  if (!addButton) return;

  addButton.addEventListener('click', () => {
    currentEditingProduct = null;
    openProductModal();
  });
}

/**
 * Initialize product modal
 */
function initializeProductModal() {
  const modal = document.getElementById('product-modal');
  const form = document.getElementById('product-form') as HTMLFormElement;
  const closeButtons = modal?.querySelectorAll('.close-modal, .cancel-product');

  if (!modal || !form) return;

  // Close modal handlers
  closeButtons?.forEach(button => {
    button.addEventListener('click', () => closeProductModal());
  });

  // Close on outside click
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      closeProductModal();
    }
  });

  // Form submission
  form.addEventListener('submit', handleProductFormSubmit);
}

/**
 * Open product modal
 */
function openProductModal(product?: Product) {
  const modal = document.getElementById('product-modal');
  const modalTitle = document.getElementById('product-modal-title');
  const form = document.getElementById('product-form') as HTMLFormElement;

  if (!modal || !form) return;

  // Set modal title
  if (modalTitle) {
    modalTitle.textContent = product ? 'Edit Product' : 'Add Product';
  }

  // Reset form
  form.reset();

  // Populate form if editing
  if (product) {
    (document.getElementById('product-name') as HTMLInputElement).value = product.name;
    (document.getElementById('product-description') as HTMLTextAreaElement).value = product.description || '';
    (document.getElementById('product-price') as HTMLInputElement).value = product.price.toString();
    (document.getElementById('product-stock') as HTMLInputElement).value = product.stock_quantity.toString();
    (document.getElementById('product-category') as HTMLInputElement).value = product.category || '';
    (document.getElementById('product-marketplace') as HTMLSelectElement).value = product.marketplace || '';
    (document.getElementById('product-sku') as HTMLInputElement).value = product.sku || '';
    (document.getElementById('product-active') as HTMLInputElement).checked = product.is_active;

    currentEditingProduct = product;
  } else {
    currentEditingProduct = null;
  }

  // Show modal
  modal.style.display = 'flex';
}

/**
 * Close product modal
 */
function closeProductModal() {
  const modal = document.getElementById('product-modal');
  if (modal) {
    modal.style.display = 'none';
  }
  currentEditingProduct = null;
}

/**
 * Handle product form submission
 */
async function handleProductFormSubmit(e: Event) {
  e.preventDefault();

  const form = e.target as HTMLFormElement;
  const submitButton = form.querySelector('button[type="submit"]') as HTMLButtonElement;
  const originalText = submitButton.textContent;

  try {
    // Disable submit button
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="loading"></span>';

    // Collect form data
    const formData = {
      name: (document.getElementById('product-name') as HTMLInputElement).value.trim(),
      description: (document.getElementById('product-description') as HTMLTextAreaElement).value.trim() || undefined,
      price: parseFloat((document.getElementById('product-price') as HTMLInputElement).value),
      stock_quantity: parseInt((document.getElementById('product-stock') as HTMLInputElement).value),
      category: (document.getElementById('product-category') as HTMLInputElement).value.trim() || undefined,
      marketplace: (document.getElementById('product-marketplace') as HTMLSelectElement).value || undefined,
      sku: (document.getElementById('product-sku') as HTMLInputElement).value.trim() || undefined,
      is_active: (document.getElementById('product-active') as HTMLInputElement).checked
    };

    // Create or update product
    if (currentEditingProduct?.id) {
      const response = await api.updateProduct(currentEditingProduct.id, formData);
      if (response.error) {
        throw new Error(response.error);
      }
      showNotification('Product updated successfully!', 'success');
    } else {
      const response = await api.createProduct(formData as ProductCreate);
      if (response.error) {
        throw new Error(response.error);
      }
      showNotification('Product created successfully!', 'success');
    }

    // Close modal and reload products
    closeProductModal();
    await loadProducts();

  } catch (error) {
    console.error('Failed to save product:', error);
    showNotification(
      `Failed to save product: ${error instanceof Error ? error.message : 'Unknown error'}`,
      'error'
    );
  } finally {
    // Re-enable submit button
    submitButton.disabled = false;
    submitButton.textContent = originalText || 'Save Product';
  }
}

/**
 * Handle edit product
 */
async function handleEditProduct(e: Event) {
  const button = e.currentTarget as HTMLButtonElement;
  const productId = parseInt(button.dataset.productId || '0');

  if (!productId) return;

  try {
    const response = await api.getProduct(productId);
    if (response.error || !response.product) {
      throw new Error(response.error || 'Product not found');
    }

    openProductModal(response.product);
  } catch (error) {
    console.error('Failed to load product:', error);
    showNotification(
      `Failed to load product: ${error instanceof Error ? error.message : 'Unknown error'}`,
      'error'
    );
  }
}

/**
 * Handle delete product
 */
async function handleDeleteProduct(e: Event) {
  const button = e.currentTarget as HTMLButtonElement;
  const productId = parseInt(button.dataset.productId || '0');

  if (!productId) return;

  if (!confirm('Are you sure you want to delete this product? This action cannot be undone.')) {
    return;
  }

  try {
    // Find product card and show loading state
    const productCard = button.closest('.product-card');
    if (productCard) {
      productCard.classList.add('deleting');
    }

    await api.deleteProduct(productId);
    showNotification('Product deleted successfully!', 'success');

    // Reload products
    await loadProducts();
  } catch (error) {
    console.error('Failed to delete product:', error);
    showNotification(
      `Failed to delete product: ${error instanceof Error ? error.message : 'Unknown error'}`,
      'error'
    );

    // Remove loading state
    const productCard = button.closest('.product-card');
    if (productCard) {
      productCard.classList.remove('deleting');
    }
  }
}

/**
 * Show notification toast
 */
function showNotification(message: string, type: 'success' | 'error') {
  // Remove existing notifications
  const existing = document.querySelector('.notification-toast');
  if (existing) {
    existing.remove();
  }

  // Create notification
  const notification = document.createElement('div');
  notification.className = `notification-toast notification-${type}`;
  notification.textContent = message;

  // Add to page
  document.body.appendChild(notification);

  // Animate in
  setTimeout(() => notification.classList.add('show'), 10);

  // Remove after 3 seconds
  setTimeout(() => {
    notification.classList.remove('show');
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

/**
 * Format currency
 */
function formatCurrency(value: number): string {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value);
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text: string): string {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
