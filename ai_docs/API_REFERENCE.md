# API Reference | ECOMLM.CODEXA

> **Status**: Documentation in progress
> **Last Updated**: 2025-11-14
> **Version**: 1.0.0

---

## 🎯 Overview

This document provides API reference documentation for the ECOMLM.CODEXA system, including both the FastAPI backend and agent interfaces.

---

## 🌐 FastAPI Backend (app/server)

### Base Information

- **Title**: Natural Language SQL Interface
- **Description**: Convert natural language to SQL queries
- **Version**: 1.0.0
- **Base URL**: `http://localhost:8000` (development)

### Core Modules

#### 1. Data Models (`core/data_models.py`)

**Request Models**:
- `QueryRequest` - Natural language query input
- `InsightsRequest` - Data insights generation
- `ExportRequest` - Data export configuration
- `QueryExportRequest` - Query-based export
- `ProductCreate` - Product creation
- `ProductUpdate` - Product update

**Response Models**:
- `FileUploadResponse` - File upload status
- `QueryResponse` - SQL query results
- `DatabaseSchemaResponse` - Database schema info
- `InsightsResponse` - Generated insights
- `HealthCheckResponse` - API health status
- `RandomQueryResponse` - Random query generation
- `ProductListResponse` - Product listing
- `ProductResponse` - Single product response

**Data Models**:
- `Product` - Product entity
- `TableSchema` - Database table structure
- `ColumnInfo` - Column metadata

#### 2. File Processing (`core/async_file_processor.py`)

**Functions**:
```python
async convert_csv_to_sqlite_async(file: UploadFile) -> str
async convert_json_to_sqlite_async(file: UploadFile) -> str
async convert_jsonl_to_sqlite_async(file: UploadFile) -> str
```

**Purpose**: Convert uploaded files to SQLite tables asynchronously

#### 3. LLM Processing (`core/llm_processor.py`)

**Functions**:
```python
generate_sql(query: str, schema: dict) -> str
generate_random_query(schema: dict) -> str
```

**Purpose**: Generate SQL queries from natural language using LLMs

#### 4. SQL Processing (`core/sql_processor.py`)

**Functions**:
```python
execute_sql_safely(sql: str, db_path: str) -> list
get_database_schema(db_path: str) -> dict
```

**Purpose**: Execute SQL queries safely with validation

#### 5. Security (`core/sql_security.py`)

**Functions**:
```python
execute_query_safely(sql: str, db_path: str) -> tuple
validate_identifier(identifier: str) -> bool
check_table_exists(table_name: str, db_path: str) -> bool
```

**Classes**:
- `SQLSecurityError` - SQL security exception

**Purpose**: SQL injection prevention and query validation

#### 6. Insights (`core/insights.py`)

**Functions**:
```python
generate_insights(data: list, query: str) -> dict
```

**Purpose**: Generate AI-powered insights from query results

#### 7. Export Utils (`core/export_utils.py`)

**Functions**:
```python
generate_csv_from_data(data: list, headers: list) -> str
generate_csv_from_table(table_name: str, db_path: str) -> str
```

**Purpose**: Export data to CSV format

#### 8. Product Database (`core/product_db.py`)

**Functions**:
```python
init_products_table(db_path: str) -> None
create_product(product: ProductCreate, db_path: str) -> Product
get_product_by_id(product_id: int, db_path: str) -> Optional[Product]
get_all_products(db_path: str, skip: int, limit: int) -> list
update_product(product_id: int, product: ProductUpdate, db_path: str) -> Optional[Product]
delete_product(product_id: int, db_path: str) -> bool
search_products(query: str, db_path: str) -> list
```

**Purpose**: Product CRUD operations

#### 9. Database Pool (`core/db_pool.py`)

**Functions**:
```python
initialize_pool(max_connections: int) -> None
shutdown_pool() -> None
get_db_connection() -> sqlite3.Connection
```

**Purpose**: Connection pooling for performance

#### 10. Caching (`core/llm_cache.py`, `core/schema_cache.py`)

**Functions**:
```python
initialize_cache() -> None
shutdown_cache() -> None
initialize_schema_cache() -> None
shutdown_schema_cache() -> None
```

**Purpose**: LLM response and schema caching

#### 11. Database Indexes (`core/db_indexes.py`)

**Functions**:
```python
create_all_indexes(db_path: str) -> None
```

**Purpose**: Optimize database performance with indexes

---

## 🤖 Agent API (codexa.app/agentes/)

### Agent Registry

All agents are registered in `codexa.app/51_AGENT_REGISTRY.json`

#### 1. Anuncio Agent (Product Listings)

**Entry Command**: `/anuncio [research_file]`
**Version**: 1.2.1
**Purpose**: Generate optimized product listings

**Input**:
- `research_notes.md` - Market research data (22 blocks)
- `brand_strategy.md` - Brand guidelines (optional)

**Output**:
- `anuncio.json` - Structured listing data
- `marketplace_listings/` - Platform-specific listings (9 marketplaces)

**Capabilities**:
- SEO optimization (9-10 keyword density)
- 100% compliance validation
- Multi-marketplace support

#### 2. Pesquisa Agent (Market Research)

**Entry Command**: `/pesquisa "produto ou nicho"`
**Version**: 2.1.0
**Purpose**: Conduct market research and competitive analysis

**Input**:
- Natural language product description

**Output**:
- `research_notes.md` - 22-block structured research

**Capabilities**:
- 9+ marketplace coverage
- Competitor analysis
- Keyword extraction
- Trend identification

#### 3. Marca Agent (Brand Strategy)

**Entry Command**: `/marca`
**Version**: 1.0.0
**Purpose**: Develop brand strategy and identity

**Input**:
- Business context (interactive)

**Output**:
- `brand_strategy.md` - Strategy document
- `brand_guidelines.json` - Brand rules

**Status**: Beta (In Development)

#### 4. Mentor Agent (Strategic Planning)

**Entry Command**: `/mentor`
**Version**: 2.0.0
**Purpose**: Strategic guidance and planning

**Capabilities**:
- Strategic planning
- KPI definition
- Process optimization
- Mentoring workflows

#### 5. Scout Agent (Code Navigation)

**Entry Command**: `/scout [query]`
**Version**: 1.0.0
**Purpose**: Navigate and discover codebase patterns

**Capabilities**:
- Repository navigation
- Code pattern discovery
- File and function search
- Dependency analysis

#### 6. Conhecimento Agent (Knowledge & ML)

**Entry Command**: `/knowledge`
**Version**: 1.1.0
**Purpose**: Extract knowledge and generate ML datasets

**Capabilities**:
- Knowledge card generation
- ML training data extraction
- Knowledge base management
- Dataset versioning

#### 7. Codexa Agent (Meta-Constructor)

**Entry Commands**:
- `/codexa-build_agent` - Create new agent
- `/codexa-build_prompt` - Create HOP module
- `/codexa-build_command` - Create slash command
- `/codexa-orchestrate` - Multi-phase workflow

**Version**: 1.2.0
**Purpose**: Self-building agent that constructs and validates other agents

**Capabilities**:
- 5-phase agent construction
- HOP generation (TAC-7)
- Slash command creation
- Workflow orchestration
- Documentation sync
- Self-improvement

---

## 📋 Common Workflows

### Workflow 1: E-commerce Listing Creation

```bash
# Step 1: Research
/prime-pesquisa
/pesquisa "fone bluetooth para home office"
# Output: research_notes.md

# Step 2: Generate Listing
/prime-anuncio
/anuncio research_notes.md
# Output: anuncio.json + marketplace_listings/
```

### Workflow 2: Create New Agent

```bash
# Step 1: Load meta-construction context
/prime-codexa

# Step 2: Build agent
/codexa-build_agent
# Follow 5-phase workflow
# Output: Complete agent in agents/{name}/
```

### Workflow 3: Natural Language SQL Query

```bash
# Use FastAPI endpoint
POST /query
{
  "query": "Show me top 10 products by sales",
  "database": "products.db"
}

# Response: SQL query + results
```

---

## 🔐 Authentication

**Current Status**: No authentication (development mode)

**Planned**:
- API key authentication
- OAuth integration
- Rate limiting
- User roles and permissions

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- Claude/OpenAI API keys

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/codexa.git
cd codexa

# Backend setup
cd app/server
uv sync
cp .env.sample .env
# Edit .env with API keys

# Start backend
uv run python server.py

# Frontend setup (new terminal)
cd app/client
npm install
npm run dev
```

### Testing API

```bash
# Health check
curl http://localhost:8000/health

# Upload CSV
curl -X POST -F "file=@data.csv" http://localhost:8000/upload

# Query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show all products", "database": "data.db"}'
```

---

## 📖 Detailed API Examples

This section provides comprehensive examples for all major endpoints with request/response patterns, error handling, and client implementations.

### Example 1: Health Check

**Purpose**: Verify API availability and database connectivity

**cURL Command**:
```bash
curl -X GET http://localhost:8000/api/health
```

**Python Client** (using `httpx`):
```python
import httpx

response = httpx.get("http://localhost:8000/api/health")
data = response.json()

print(f"Status: {data['status']}")
print(f"Database Connected: {data['database_connected']}")
print(f"Tables Count: {data['tables_count']}")
print(f"Uptime: {data['uptime_seconds']}s")
```

**Success Response** (200 OK):
```json
{
  "status": "ok",
  "database_connected": true,
  "tables_count": 5,
  "uptime_seconds": 3600.45
}
```

**Error Response** (500 Internal Server Error):
```json
{
  "status": "error",
  "database_connected": false,
  "tables_count": 0,
  "uptime_seconds": 0
}
```

**Error Handling**:
```python
try:
    response = httpx.get("http://localhost:8000/api/health", timeout=5.0)
    response.raise_for_status()
    data = response.json()

    if data['status'] != 'ok':
        print(f"API unhealthy: {data}")
except httpx.TimeoutException:
    print("Health check timed out")
except httpx.HTTPStatusError as e:
    print(f"HTTP error: {e.response.status_code}")
```

---

### Example 2: File Upload (CSV/JSON/JSONL)

**Purpose**: Upload data files and convert to SQLite tables

**cURL Command** (CSV):
```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@products.csv" \
  -H "Accept: application/json"
```

**Python Client** (with validation):
```python
import httpx
from pathlib import Path

def upload_file(file_path: str) -> dict:
    """Upload CSV/JSON/JSONL file to API"""
    file_path = Path(file_path)

    # Validate file type
    if file_path.suffix not in ['.csv', '.json', '.jsonl']:
        raise ValueError("Only .csv, .json, .jsonl supported")

    # Upload file
    with open(file_path, 'rb') as f:
        files = {'file': (file_path.name, f, 'application/octet-stream')}
        response = httpx.post(
            "http://localhost:8000/api/upload",
            files=files,
            timeout=30.0
        )

    response.raise_for_status()
    return response.json()

# Usage
result = upload_file("products.csv")
print(f"Table created: {result['table_name']}")
print(f"Rows imported: {result['row_count']}")
print(f"Schema: {result['table_schema']}")
```

**Success Response** (200 OK):
```json
{
  "table_name": "products",
  "table_schema": {
    "id": "INTEGER",
    "name": "TEXT",
    "price": "REAL",
    "category": "TEXT"
  },
  "row_count": 1250,
  "sample_data": [
    {"id": 1, "name": "Wireless Mouse", "price": 29.99, "category": "Electronics"},
    {"id": 2, "name": "USB Cable", "price": 9.99, "category": "Accessories"}
  ]
}
```

**Error Response** (400 Bad Request):
```json
{
  "table_name": "",
  "table_schema": {},
  "row_count": 0,
  "sample_data": [],
  "error": "Only .csv, .json, and .jsonl files are supported"
}
```

---

### Example 3: Natural Language Query

**Purpose**: Convert natural language to SQL and execute queries

**cURL Command**:
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Show me the top 10 products by price in the Electronics category",
    "database": "products"
  }'
```

**Python Client** (with retry logic):
```python
import httpx
from typing import Optional
import time

def execute_nl_query(query: str, database: str = "database", max_retries: int = 3) -> dict:
    """Execute natural language query with retry logic"""
    url = "http://localhost:8000/api/query"
    payload = {"query": query, "database": database}

    for attempt in range(max_retries):
        try:
            response = httpx.post(url, json=payload, timeout=30.0)
            response.raise_for_status()
            data = response.json()

            if data.get('error'):
                raise ValueError(f"Query failed: {data['error']}")

            return data
        except httpx.HTTPStatusError as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff

# Usage
result = execute_nl_query("Find products cheaper than $50")
print(f"Generated SQL: {result['sql']}")
print(f"Rows returned: {result['row_count']}")
print(f"Execution time: {result['execution_time_ms']}ms")

for row in result['results'][:5]:
    print(row)
```

**Success Response** (200 OK):
```json
{
  "sql": "SELECT * FROM products WHERE category = 'Electronics' ORDER BY price DESC LIMIT 10",
  "results": [
    {"id": 45, "name": "Gaming Laptop", "price": 1299.99, "category": "Electronics"},
    {"id": 78, "name": "4K Monitor", "price": 599.99, "category": "Electronics"}
  ],
  "columns": ["id", "name", "price", "category"],
  "row_count": 10,
  "execution_time_ms": 45.23
}
```

**Error Response** (500 Internal Server Error):
```json
{
  "sql": "",
  "results": [],
  "columns": [],
  "row_count": 0,
  "execution_time_ms": 0,
  "error": "Table 'products' does not exist"
}
```

---

### Example 4: Get Database Schema

**Purpose**: Retrieve all tables and their column definitions

**cURL Command**:
```bash
curl -X GET http://localhost:8000/api/schema \
  -H "Accept: application/json"
```

**Python Client**:
```python
import httpx
from datetime import datetime

def get_schema() -> dict:
    """Get complete database schema"""
    response = httpx.get("http://localhost:8000/api/schema")
    response.raise_for_status()
    return response.json()

# Usage
schema = get_schema()
print(f"Total tables: {schema['total_tables']}\n")

for table in schema['tables']:
    print(f"Table: {table['name']} ({table['row_count']} rows)")
    print(f"Created: {table['created_at']}")
    print("Columns:")
    for col in table['columns']:
        nullable = "NULL" if col['nullable'] else "NOT NULL"
        pk = "PRIMARY KEY" if col['primary_key'] else ""
        print(f"  - {col['name']}: {col['type']} {nullable} {pk}")
    print()
```

**Success Response** (200 OK):
```json
{
  "tables": [
    {
      "name": "products",
      "columns": [
        {"name": "id", "type": "INTEGER", "nullable": false, "primary_key": true},
        {"name": "name", "type": "TEXT", "nullable": true, "primary_key": false},
        {"name": "price", "type": "REAL", "nullable": true, "primary_key": false}
      ],
      "row_count": 1250,
      "created_at": "2025-11-14T10:30:00"
    }
  ],
  "total_tables": 1
}
```

---

### Example 5: Product CRUD Operations

**Purpose**: Create, read, update, and delete products

**Create Product**:

```bash
# cURL
curl -X POST http://localhost:8000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Wireless Keyboard",
    "description": "Ergonomic wireless keyboard with backlight",
    "price": 79.99,
    "category": "Electronics",
    "marketplace": "mercadolivre",
    "is_active": true
  }'
```

```python
# Python Client
import httpx

def create_product(product_data: dict) -> dict:
    response = httpx.post(
        "http://localhost:8000/api/products",
        json=product_data
    )
    response.raise_for_status()
    return response.json()

# Usage
new_product = {
    "name": "Wireless Keyboard",
    "description": "Ergonomic wireless keyboard",
    "price": 79.99,
    "category": "Electronics",
    "marketplace": "mercadolivre",
    "is_active": True
}

result = create_product(new_product)
product_id = result['product']['id']
print(f"Product created with ID: {product_id}")
```

**Success Response** (200 OK):
```json
{
  "product": {
    "id": 123,
    "name": "Wireless Keyboard",
    "description": "Ergonomic wireless keyboard with backlight",
    "price": 79.99,
    "category": "Electronics",
    "marketplace": "mercadolivre",
    "is_active": true,
    "created_at": "2025-11-14T10:30:00",
    "updated_at": "2025-11-14T10:30:00"
  }
}
```

**Get Product by ID**:

```python
def get_product(product_id: int) -> dict:
    response = httpx.get(f"http://localhost:8000/api/products/{product_id}")

    if response.status_code == 404:
        raise ValueError(f"Product {product_id} not found")

    response.raise_for_status()
    return response.json()

# Usage
product = get_product(123)
print(f"Product: {product['product']['name']}")
```

**List Products with Filters**:

```python
def list_products(name: str = None, category: str = None, is_active: bool = None) -> list:
    params = {}
    if name:
        params['name'] = name
    if category:
        params['category'] = category
    if is_active is not None:
        params['is_active'] = is_active

    response = httpx.get("http://localhost:8000/api/products", params=params)
    response.raise_for_status()
    return response.json()

# Usage
electronics = list_products(category="Electronics", is_active=True)
print(f"Found {electronics['total']} active electronics")
```

**Update Product**:

```python
def update_product(product_id: int, updates: dict) -> dict:
    response = httpx.put(
        f"http://localhost:8000/api/products/{product_id}",
        json=updates
    )
    response.raise_for_status()
    return response.json()

# Usage
updates = {"price": 69.99, "is_active": False}
result = update_product(123, updates)
print(f"Product updated: {result['product']['name']}")
```

**Delete Product**:

```python
def delete_product(product_id: int) -> dict:
    response = httpx.delete(f"http://localhost:8000/api/products/{product_id}")
    response.raise_for_status()
    return response.json()

# Usage
result = delete_product(123)
print(result['message'])
```

---

### Example 6: Export Data to CSV

**Purpose**: Export table data or query results to CSV files

**Export Table**:

```bash
# cURL
curl -X POST http://localhost:8000/api/export/table \
  -H "Content-Type: application/json" \
  -d '{"table_name": "products"}' \
  --output products_export.csv
```

```python
# Python Client
def export_table(table_name: str, output_file: str):
    response = httpx.post(
        "http://localhost:8000/api/export/table",
        json={"table_name": table_name}
    )
    response.raise_for_status()

    with open(output_file, 'wb') as f:
        f.write(response.content)

    print(f"Exported to {output_file}")

# Usage
export_table("products", "products_export.csv")
```

**Export Query Results**:

```python
def export_query_results(data: list, columns: list, output_file: str):
    response = httpx.post(
        "http://localhost:8000/api/export/query",
        json={"data": data, "columns": columns}
    )
    response.raise_for_status()

    with open(output_file, 'wb') as f:
        f.write(response.content)

# Usage
query_result = execute_nl_query("SELECT * FROM products WHERE price < 50")
export_query_results(
    data=query_result['results'],
    columns=query_result['columns'],
    output_file="filtered_products.csv"
)
```

---

### Example 7: Generate AI Insights

**Purpose**: Get statistical insights for table columns

**cURL Command**:
```bash
curl -X POST http://localhost:8000/api/insights \
  -H "Content-Type: application/json" \
  -d '{
    "table_name": "products",
    "column_names": ["price", "category"]
  }'
```

**Python Client**:
```python
def generate_insights(table_name: str, columns: list) -> dict:
    response = httpx.post(
        "http://localhost:8000/api/insights",
        json={"table_name": table_name, "column_names": columns}
    )
    response.raise_for_status()
    return response.json()

# Usage
insights = generate_insights("products", ["price", "category"])
print(f"Insights for {insights['table_name']}:")
for insight in insights['insights']:
    print(f"- {insight}")
```

**Success Response** (200 OK):
```json
{
  "table_name": "products",
  "insights": [
    "Average price: $89.45",
    "Most common category: Electronics (45%)",
    "Price range: $9.99 - $1,299.99",
    "Total products: 1,250"
  ],
  "generated_at": "2025-11-14T10:30:00"
}
```

---

### Complete Python Client Example

**Full-featured client with error handling, retries, and logging**:

```python
import httpx
import logging
from typing import Optional, Dict, List
from pathlib import Path
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CodexaAPIClient:
    """Complete client for ECOMLM.CODEXA API"""

    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 30.0):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.client = httpx.Client(base_url=self.base_url, timeout=self.timeout)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    def health_check(self) -> Dict:
        """Check API health"""
        response = self.client.get("/api/health")
        response.raise_for_status()
        return response.json()

    def upload_file(self, file_path: str) -> Dict:
        """Upload CSV/JSON/JSONL file"""
        file_path = Path(file_path)

        with open(file_path, 'rb') as f:
            files = {'file': (file_path.name, f)}
            response = self.client.post("/api/upload", files=files)

        response.raise_for_status()
        return response.json()

    def query(self, natural_language: str, database: str = "database") -> Dict:
        """Execute natural language query"""
        payload = {"query": natural_language, "database": database}
        response = self.client.post("/api/query", json=payload)
        response.raise_for_status()

        data = response.json()
        if data.get('error'):
            raise ValueError(f"Query error: {data['error']}")

        return data

    def get_schema(self) -> Dict:
        """Get database schema"""
        response = self.client.get("/api/schema")
        response.raise_for_status()
        return response.json()

    def create_product(self, product: Dict) -> Dict:
        """Create new product"""
        response = self.client.post("/api/products", json=product)
        response.raise_for_status()
        return response.json()

    def get_product(self, product_id: int) -> Dict:
        """Get product by ID"""
        response = self.client.get(f"/api/products/{product_id}")
        response.raise_for_status()
        return response.json()

    def list_products(self, **filters) -> Dict:
        """List products with optional filters"""
        response = self.client.get("/api/products", params=filters)
        response.raise_for_status()
        return response.json()

    def update_product(self, product_id: int, updates: Dict) -> Dict:
        """Update product"""
        response = self.client.put(f"/api/products/{product_id}", json=updates)
        response.raise_for_status()
        return response.json()

    def delete_product(self, product_id: int) -> Dict:
        """Delete product"""
        response = self.client.delete(f"/api/products/{product_id}")
        response.raise_for_status()
        return response.json()

    def export_table(self, table_name: str, output_file: str):
        """Export table to CSV"""
        response = self.client.post("/api/export/table", json={"table_name": table_name})
        response.raise_for_status()

        with open(output_file, 'wb') as f:
            f.write(response.content)

        logger.info(f"Exported {table_name} to {output_file}")

# Usage Example
if __name__ == "__main__":
    with CodexaAPIClient() as client:
        # Health check
        health = client.health_check()
        print(f"API Status: {health['status']}")

        # Upload data
        result = client.upload_file("products.csv")
        print(f"Uploaded {result['row_count']} rows to {result['table_name']}")

        # Query data
        query_result = client.query("Show top 10 products by price")
        print(f"Query returned {query_result['row_count']} rows")

        # Create product
        new_product = {
            "name": "USB Cable",
            "price": 9.99,
            "category": "Accessories",
            "marketplace": "mercadolivre"
        }
        created = client.create_product(new_product)
        print(f"Created product: {created['product']['id']}")
```

---

## 📚 Additional Documentation

- **HOP Framework**: See `codexa.app/42_HOP_FRAMEWORK.md`
- **Agent Specs**: See `codexa.app/51_AGENT_REGISTRY.json`
- **Meta-Construction**: See `codexa.app/docs_consolidados/43_META_CONSTRUCTION_INDEX.md`

---

## 🔄 Versioning

This API follows [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes

**Current Version**: 1.0.0

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/codexa/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/codexa/discussions)

---

**Note**: This is a living document. API endpoints and agent interfaces are continuously improved. Always refer to the latest version.

**Last Updated**: 2025-11-14
**Status**: In Development
