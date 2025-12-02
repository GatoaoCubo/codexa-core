from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from datetime import datetime
from typing import Optional
import os
import sqlite3
import traceback
from dotenv import load_dotenv
import logging
import sys

from core.data_models import (
    FileUploadResponse,
    QueryRequest,
    QueryResponse,
    DatabaseSchemaResponse,
    InsightsRequest,
    InsightsResponse,
    HealthCheckResponse,
    TableSchema,
    ColumnInfo,
    RandomQueryResponse,
    ExportRequest,
    QueryExportRequest,
    Product,
    ProductCreate,
    ProductUpdate,
    ProductListResponse,
    ProductResponse
)
from core.async_file_processor import (
    convert_csv_to_sqlite_async,
    convert_json_to_sqlite_async,
    convert_jsonl_to_sqlite_async
)
from core.llm_processor import generate_sql, generate_random_query
from core.sql_processor import execute_sql_safely, get_database_schema
from core.insights import generate_insights
from core.sql_security import (
    execute_query_safely,
    validate_identifier,
    check_table_exists,
    SQLSecurityError
)
from core.export_utils import generate_csv_from_data, generate_csv_from_table
from core.product_db import (
    init_products_table,
    create_product,
    get_product_by_id,
    get_all_products,
    update_product,
    delete_product,
    search_products
)
from core.db_pool import initialize_pool, shutdown_pool, get_db_connection
from core.llm_cache import initialize_cache, shutdown_cache
from core.schema_cache import initialize_schema_cache, shutdown_schema_cache
from core.db_indexes import create_all_indexes

# Load .env file from server directory
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Create logger for this module
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Natural Language SQL Interface",
    description="Convert natural language to SQL queries",
    version="1.0.0"
)

# CORS configuration for frontend
frontend_port = os.environ.get("FRONTEND_PORT", "5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"http://localhost:{frontend_port}"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global app state
app_start_time = datetime.now()

# Ensure database directory exists
os.makedirs("db", exist_ok=True)
os.makedirs("cache", exist_ok=True)

@app.on_event("startup")
async def startup():
    """Initialize connection pool, caches, and database on startup"""
    logger.info("[*] Initializing TAC-7 system...")

    # Initialize database connection pool
    initialize_pool("db/database.db")
    logger.info("[+] Database connection pool initialized")

    # Initialize LLM cache with 1-hour TTL and persistence
    initialize_cache(ttl_seconds=3600, persist_path="cache/llm_cache.pkl")
    logger.info("[+] LLM cache initialized (TTL: 1 hour)")

    # Initialize schema cache with 5-minute TTL
    initialize_schema_cache(ttl_seconds=300)
    logger.info("[+] Schema cache initialized (TTL: 5 minutes)")

    # Initialize products table
    init_products_table()
    logger.info("[+] Products table initialized")

    # Create database indexes for performance
    try:
        create_all_indexes()
        logger.info("[+] Database indexes created/verified")
    except Exception as e:
        logger.warning(f"[-] Index creation warning: {e}")

    logger.info("[+] TAC-7 system ready!")

@app.on_event("shutdown")
async def shutdown():
    """Cleanup resources on shutdown"""
    logger.info("[*] Shutting down TAC-7 system...")

    # Shutdown connection pool
    shutdown_pool()
    logger.info("[+] Database connection pool closed")

    # Shutdown LLM cache (persists to disk)
    shutdown_cache()
    logger.info("[+] LLM cache persisted and closed")

    # Shutdown schema cache
    shutdown_schema_cache()
    logger.info("[+] Schema cache cleared")

    logger.info("[+] TAC-7 system shutdown complete")

@app.post("/api/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)) -> FileUploadResponse:
    """Upload and convert .json, .jsonl or .csv file to SQLite table (non-blocking)"""
    try:
        # Validate file type
        if not file.filename.endswith(('.csv', '.json', '.jsonl')):
            raise HTTPException(400, "Only .csv, .json, and .jsonl files are supported")

        # Generate table name from filename
        table_name = file.filename.rsplit('.', 1)[0].lower().replace(' ', '_')

        # Read file content
        content = await file.read()

        # Convert to SQLite based on file type (using async processors)
        if file.filename.endswith('.csv'):
            result = await convert_csv_to_sqlite_async(content, table_name)
        elif file.filename.endswith('.jsonl'):
            result = await convert_jsonl_to_sqlite_async(content, table_name)
        else:
            result = await convert_json_to_sqlite_async(content, table_name)

        response = FileUploadResponse(
            table_name=result['table_name'],
            table_schema=result['table_schema'],
            row_count=result['row_count'],
            sample_data=result['sample_data']
        )
        logger.info(f"[SUCCESS] File upload (async): {response.table_name}, {response.row_count} rows")
        return response
    except Exception as e:
        logger.error(f"[ERROR] File upload failed: {str(e)}")
        logger.error(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
        return FileUploadResponse(
            table_name="",
            table_schema={},
            row_count=0,
            sample_data=[],
            error=str(e)
        )

@app.post("/api/query", response_model=QueryResponse)
async def process_natural_language_query(request: QueryRequest) -> QueryResponse:
    """Process natural language query and return SQL results"""
    try:
        # Get database schema
        schema_info = get_database_schema()
        
        # Generate SQL using routing logic
        sql = generate_sql(request, schema_info)
        
        # Execute SQL query
        start_time = datetime.now()
        result = execute_sql_safely(sql)
        execution_time = (datetime.now() - start_time).total_seconds() * 1000
        
        if result['error']:
            raise Exception(result['error'])
        
        response = QueryResponse(
            sql=sql,
            results=result['results'],
            columns=result['columns'],
            row_count=len(result['results']),
            execution_time_ms=execution_time
        )
        logger.info(f"[SUCCESS] Query processed: SQL={sql}, rows={len(result['results'])}, time={execution_time}ms")
        return response
    except Exception as e:
        logger.error(f"[ERROR] Query processing failed: {str(e)}")
        logger.error(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
        return QueryResponse(
            sql="",
            results=[],
            columns=[],
            row_count=0,
            execution_time_ms=0,
            error=str(e)
        )

@app.get("/api/schema", response_model=DatabaseSchemaResponse)
async def get_database_schema_endpoint() -> DatabaseSchemaResponse:
    """Get current database schema and table information"""
    try:
        schema = get_database_schema()
        tables = []
        
        for table_name, table_info in schema['tables'].items():
            columns = []
            for col_name, col_type in table_info['columns'].items():
                columns.append(ColumnInfo(
                    name=col_name,
                    type=col_type,
                    nullable=True,
                    primary_key=False
                ))
            
            tables.append(TableSchema(
                name=table_name,
                columns=columns,
                row_count=table_info.get('row_count', 0),
                created_at=datetime.now()  # Simplified for v1
            ))
        
        response = DatabaseSchemaResponse(
            tables=tables,
            total_tables=len(tables)
        )
        logger.info(f"[SUCCESS] Schema retrieved: {len(tables)} tables")
        return response
    except Exception as e:
        logger.error(f"[ERROR] Schema retrieval failed: {str(e)}")
        logger.error(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
        return DatabaseSchemaResponse(
            tables=[],
            total_tables=0,
            error=str(e)
        )

@app.post("/api/insights", response_model=InsightsResponse)
async def generate_insights_endpoint(request: InsightsRequest) -> InsightsResponse:
    """Generate statistical insights for table columns"""
    try:
        insights = generate_insights(request.table_name, request.column_names)
        response = InsightsResponse(
            table_name=request.table_name,
            insights=insights,
            generated_at=datetime.now()
        )
        logger.info(f"[SUCCESS] Insights generated for table: {request.table_name}, insights count: {len(insights)}")
        return response
    except Exception as e:
        logger.error(f"[ERROR] Insights generation failed: {str(e)}")
        logger.error(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
        return InsightsResponse(
            table_name=request.table_name,
            insights=[],
            generated_at=datetime.now(),
            error=str(e)
        )

@app.get("/api/generate-random-query", response_model=RandomQueryResponse)
async def generate_random_query_endpoint() -> RandomQueryResponse:
    """Generate a random natural language query based on database schema"""
    try:
        # Get database schema
        schema_info = get_database_schema()
        
        # Check if there are any tables
        if not schema_info.get('tables'):
            return RandomQueryResponse(
                query="Please upload some data first to generate queries.",
                error="No tables found in database"
            )
        
        # Generate random query using LLM
        random_query = generate_random_query(schema_info)
        
        response = RandomQueryResponse(query=random_query)
        logger.info(f"[SUCCESS] Random query generated: {random_query}")
        return response
    except Exception as e:
        logger.error(f"[ERROR] Random query generation failed: {str(e)}")
        logger.error(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
        return RandomQueryResponse(
            query="Could not generate a random query. Please try again.",
            error=str(e)
        )

@app.get("/api/health", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """Health check endpoint with database status"""
    try:
        # Check database connection
        conn = sqlite3.connect("db/database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()
        
        uptime = (datetime.now() - app_start_time).total_seconds()
        
        response = HealthCheckResponse(
            status="ok",
            database_connected=True,
            tables_count=len(tables),
            uptime_seconds=uptime
        )
        logger.info(f"[SUCCESS] Health check: OK, {len(tables)} tables, uptime: {uptime}s")
        return response
    except Exception as e:
        logger.error(f"[ERROR] Health check failed: {str(e)}")
        logger.error(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
        return HealthCheckResponse(
            status="error",
            database_connected=False,
            tables_count=0,
            uptime_seconds=0
        )

@app.delete("/api/table/{table_name}")
async def delete_table(table_name: str):
    """Delete a table from the database"""
    try:
        # Validate table name using security module
        try:
            validate_identifier(table_name, "table")
        except SQLSecurityError as e:
            raise HTTPException(400, str(e))
        
        conn = sqlite3.connect("db/database.db")
        
        # Check if table exists using secure method
        if not check_table_exists(conn, table_name):
            conn.close()
            raise HTTPException(404, f"Table '{table_name}' not found")
        
        # Drop the table using safe query execution with DDL permission
        execute_query_safely(
            conn,
            "DROP TABLE IF EXISTS {table}",
            identifier_params={'table': table_name},
            allow_ddl=True
        )
        conn.commit()
        conn.close()
        
        response = {"message": f"Table '{table_name}' deleted successfully"}
        logger.info(f"[SUCCESS] Table deleted: {table_name}")
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[ERROR] Table deletion failed: {str(e)}")
        logger.error(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
        raise HTTPException(500, f"Error deleting table: {str(e)}")

@app.post("/api/export/table")
async def export_table(request: ExportRequest) -> Response:
    """Export a table as CSV file"""
    try:
        # Validate table name
        validate_identifier(request.table_name, "table")
        
        # Connect to database
        conn = sqlite3.connect("db/database.db")
        
        # Check if table exists
        if not check_table_exists(conn, request.table_name):
            conn.close()
            raise HTTPException(404, f"Table '{request.table_name}' not found")
        
        # Generate CSV
        csv_data = generate_csv_from_table(conn, request.table_name)
        conn.close()
        
        # Return CSV response
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={
                "Content-Disposition": f'attachment; filename="{request.table_name}_export.csv"'
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[ERROR] Table export failed: {str(e)}")
        logger.error(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
        raise HTTPException(500, f"Error exporting table: {str(e)}")

@app.post("/api/export/query")
async def export_query_results(request: QueryExportRequest) -> Response:
    """Export query results as CSV file"""
    try:
        # Generate CSV from query results
        csv_data = generate_csv_from_data(request.data, request.columns)

        # Return CSV response
        return Response(
            content=csv_data,
            media_type="text/csv",
            headers={
                "Content-Disposition": 'attachment; filename="query_results.csv"'
            }
        )
    except Exception as e:
        logger.error(f"[ERROR] Query export failed: {str(e)}")
        logger.error(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
        raise HTTPException(500, f"Error exporting query results: {str(e)}")

# ========== PRODUCT CRUD ENDPOINTS ==========

@app.post("/api/products", response_model=ProductResponse)
async def create_product_endpoint(product: ProductCreate) -> ProductResponse:
    """Create a new product"""
    try:
        created_product = create_product(product.model_dump())

        # Convert is_active from integer to boolean
        if created_product:
            created_product['is_active'] = bool(created_product['is_active'])

        response = ProductResponse(product=Product(**created_product))
        logger.info(f"[SUCCESS] Product created via API: id={created_product['id']}, name={created_product['name']}")
        return response
    except Exception as e:
        logger.error(f"[ERROR] Product creation failed: {str(e)}")
        logger.error(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
        return ProductResponse(error=str(e))

@app.get("/api/products", response_model=ProductListResponse)
async def get_all_products_endpoint(
    name: Optional[str] = None,
    category: Optional[str] = None,
    marketplace: Optional[str] = None,
    is_active: Optional[bool] = None
) -> ProductListResponse:
    """Get all products with optional filters"""
    try:
        # Use search if any filters provided, otherwise get all
        if any([name, category, marketplace, is_active is not None]):
            products = search_products(
                name=name,
                category=category,
                marketplace=marketplace,
                is_active=is_active
            )
        else:
            products = get_all_products()

        # Convert is_active from integer to boolean
        for product in products:
            product['is_active'] = bool(product['is_active'])

        response = ProductListResponse(
            products=[Product(**p) for p in products],
            total=len(products)
        )
        logger.info(f"[SUCCESS] Products retrieved: count={len(products)}")
        return response
    except Exception as e:
        logger.error(f"[ERROR] Products retrieval failed: {str(e)}")
        logger.error(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
        return ProductListResponse(products=[], total=0, error=str(e))

@app.get("/api/products/{product_id}", response_model=ProductResponse)
async def get_product_endpoint(product_id: int) -> ProductResponse:
    """Get a product by ID"""
    try:
        product = get_product_by_id(product_id)

        if not product:
            raise HTTPException(404, f"Product with id={product_id} not found")

        # Convert is_active from integer to boolean
        product['is_active'] = bool(product['is_active'])

        response = ProductResponse(product=Product(**product))
        logger.info(f"[SUCCESS] Product retrieved: id={product_id}")
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[ERROR] Product retrieval failed: {str(e)}")
        logger.error(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
        return ProductResponse(error=str(e))

@app.put("/api/products/{product_id}", response_model=ProductResponse)
async def update_product_endpoint(product_id: int, product: ProductUpdate) -> ProductResponse:
    """Update a product"""
    try:
        # Check if product exists
        existing = get_product_by_id(product_id)
        if not existing:
            raise HTTPException(404, f"Product with id={product_id} not found")

        # Update product
        update_data = product.model_dump(exclude_unset=True)
        updated_product = update_product(product_id, update_data)

        if not updated_product:
            raise Exception("Failed to update product")

        # Convert is_active from integer to boolean
        updated_product['is_active'] = bool(updated_product['is_active'])

        response = ProductResponse(product=Product(**updated_product))
        logger.info(f"[SUCCESS] Product updated: id={product_id}")
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[ERROR] Product update failed: {str(e)}")
        logger.error(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
        return ProductResponse(error=str(e))

@app.delete("/api/products/{product_id}")
async def delete_product_endpoint(product_id: int):
    """Delete a product"""
    try:
        # Check if product exists
        existing = get_product_by_id(product_id)
        if not existing:
            raise HTTPException(404, f"Product with id={product_id} not found")

        # Delete product
        success = delete_product(product_id)

        if not success:
            raise Exception("Failed to delete product")

        response = {"message": f"Product {product_id} deleted successfully"}
        logger.info(f"[SUCCESS] Product deleted: id={product_id}")
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[ERROR] Product deletion failed: {str(e)}")
        logger.error(f"[ERROR] Full traceback:\n{traceback.format_exc()}")
        raise HTTPException(500, f"Error deleting product: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=int(os.environ.get("BACKEND_PORT", "8000")), reload=True)