"""
Product database operations module
Handles all CRUD operations for products table
"""
import sqlite3
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

DB_PATH = "db/database.db"

def init_products_table() -> None:
    """Initialize products table if it doesn't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT,
            marketplace TEXT,
            sku TEXT,
            stock_quantity INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Create indexes for common queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_products_name
        ON products(name)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_products_category
        ON products(category)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_products_marketplace
        ON products(marketplace)
    """)

    conn.commit()
    conn.close()
    logger.info("[SUCCESS] Products table initialized")

def create_product(product_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new product"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO products (
            name, description, price, category, marketplace,
            sku, stock_quantity, is_active, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        product_data['name'],
        product_data.get('description'),
        product_data['price'],
        product_data.get('category'),
        product_data.get('marketplace'),
        product_data.get('sku'),
        product_data.get('stock_quantity', 0),
        1 if product_data.get('is_active', True) else 0,
        now,
        now
    ))

    product_id = cursor.lastrowid
    conn.commit()
    conn.close()

    logger.info(f"[SUCCESS] Product created: id={product_id}, name={product_data['name']}")
    return get_product_by_id(product_id)

def get_product_by_id(product_id: int) -> Optional[Dict[str, Any]]:
    """Get a product by ID"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return dict(row)
    return None

def get_all_products() -> List[Dict[str, Any]]:
    """Get all products"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM products
        ORDER BY created_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def update_product(product_id: int, update_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update a product"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Build dynamic update query based on provided fields
    update_fields = []
    values = []

    for field in ['name', 'description', 'price', 'category', 'marketplace', 'sku', 'stock_quantity']:
        if field in update_data and update_data[field] is not None:
            update_fields.append(f"{field} = ?")
            values.append(update_data[field])

    if 'is_active' in update_data and update_data['is_active'] is not None:
        update_fields.append("is_active = ?")
        values.append(1 if update_data['is_active'] else 0)

    if not update_fields:
        conn.close()
        return get_product_by_id(product_id)

    # Add updated_at
    update_fields.append("updated_at = ?")
    values.append(datetime.now().isoformat())

    # Add product_id for WHERE clause
    values.append(product_id)

    query = f"""
        UPDATE products
        SET {', '.join(update_fields)}
        WHERE id = ?
    """

    cursor.execute(query, values)
    conn.commit()
    conn.close()

    logger.info(f"[SUCCESS] Product updated: id={product_id}")
    return get_product_by_id(product_id)

def delete_product(product_id: int) -> bool:
    """Delete a product"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    deleted = cursor.rowcount > 0

    conn.commit()
    conn.close()

    if deleted:
        logger.info(f"[SUCCESS] Product deleted: id={product_id}")
    else:
        logger.warning(f"[WARNING] Product not found for deletion: id={product_id}")

    return deleted

def search_products(
    name: Optional[str] = None,
    category: Optional[str] = None,
    marketplace: Optional[str] = None,
    is_active: Optional[bool] = None
) -> List[Dict[str, Any]]:
    """Search products with filters"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT * FROM products WHERE 1=1"
    params = []

    if name:
        query += " AND name LIKE ?"
        params.append(f"%{name}%")

    if category:
        query += " AND category = ?"
        params.append(category)

    if marketplace:
        query += " AND marketplace = ?"
        params.append(marketplace)

    if is_active is not None:
        query += " AND is_active = ?"
        params.append(1 if is_active else 0)

    query += " ORDER BY created_at DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]
