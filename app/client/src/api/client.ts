// API client configuration

// Base URL configuration - works in both dev and production
const API_BASE_URL = import.meta.env.DEV 
  ? '/api'  // Proxy to backend in development
  : (import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000') + '/api';  // Direct backend in production

// Generic API request function
async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
      }
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

// API methods
export const api = {
  // Upload file
  async uploadFile(file: File): Promise<FileUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    
    return apiRequest<FileUploadResponse>('/upload', {
      method: 'POST',
      body: formData
    });
  },
  
  // Process query
  async processQuery(request: QueryRequest): Promise<QueryResponse> {
    return apiRequest<QueryResponse>('/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request)
    });
  },
  
  // Get database schema
  async getSchema(): Promise<DatabaseSchemaResponse> {
    return apiRequest<DatabaseSchemaResponse>('/schema');
  },
  
  // Generate insights
  async generateInsights(request: InsightsRequest): Promise<InsightsResponse> {
    return apiRequest<InsightsResponse>('/insights', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request)
    });
  },
  
  // Health check
  async healthCheck(): Promise<HealthCheckResponse> {
    return apiRequest<HealthCheckResponse>('/health');
  },
  
  // Generate random query
  async generateRandomQuery(): Promise<RandomQueryResponse> {
    return apiRequest<RandomQueryResponse>('/generate-random-query');
  },
  
  // Export table as CSV
  async exportTable(tableName: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/export/table`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ table_name: tableName })
    });
    
    if (!response.ok) {
      throw new Error(`Export failed: ${response.status}`);
    }
    
    // Get the filename from Content-Disposition header
    const contentDisposition = response.headers.get('Content-Disposition');
    const filenameMatch = contentDisposition?.match(/filename="(.+)"/);
    const filename = filenameMatch ? filenameMatch[1] : `${tableName}_export.csv`;
    
    // Download the file
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  },
  
  // Export query results as CSV
  async exportQueryResults(data: any[], columns: string[]): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/export/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ data, columns })
    });

    if (!response.ok) {
      throw new Error(`Export failed: ${response.status}`);
    }

    // Download the file
    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'query_results.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  },

  // ========== PRODUCT CRUD METHODS ==========

  // Create product
  async createProduct(product: ProductCreate): Promise<ProductResponse> {
    return apiRequest<ProductResponse>('/products', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(product)
    });
  },

  // Get all products with optional filters
  async getAllProducts(filters?: {
    name?: string;
    category?: string;
    marketplace?: string;
    is_active?: boolean;
  }): Promise<ProductListResponse> {
    const params = new URLSearchParams();
    if (filters?.name) params.append('name', filters.name);
    if (filters?.category) params.append('category', filters.category);
    if (filters?.marketplace) params.append('marketplace', filters.marketplace);
    if (filters?.is_active !== undefined) params.append('is_active', String(filters.is_active));

    const query = params.toString() ? `?${params.toString()}` : '';
    return apiRequest<ProductListResponse>(`/products${query}`);
  },

  // Get product by ID
  async getProduct(productId: number): Promise<ProductResponse> {
    return apiRequest<ProductResponse>(`/products/${productId}`);
  },

  // Update product
  async updateProduct(productId: number, product: ProductUpdate): Promise<ProductResponse> {
    return apiRequest<ProductResponse>(`/products/${productId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(product)
    });
  },

  // Delete product
  async deleteProduct(productId: number): Promise<{ message: string }> {
    return apiRequest<{ message: string }>(`/products/${productId}`, {
      method: 'DELETE'
    });
  }
};