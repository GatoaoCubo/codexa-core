"""
Pydantic data models for the Natural Language SQL Interface API.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any, List, Optional
from datetime import datetime


# ============================================================================
# File Upload Models
# ============================================================================

class FileUploadResponse(BaseModel):
    """Response for file upload endpoint"""
    table_name: str
    table_schema: Dict[str, Any]
    row_count: int
    sample_data: List[Dict[str, Any]]
    error: Optional[str] = None


# ============================================================================
# Query Models
# ============================================================================

class QueryRequest(BaseModel):
    """Request for natural language query"""
    query: str
    table_name: Optional[str] = None
    model: Optional[str] = "gpt-4"  # Default model


class QueryResponse(BaseModel):
    """Response for query execution"""
    sql: str
    results: List[Dict[str, Any]]
    columns: List[str]
    row_count: int
    execution_time_ms: float
    error: Optional[str] = None


class RandomQueryResponse(BaseModel):
    """Response for random query generation"""
    query: str
    table_name: str
    error: Optional[str] = None


# ============================================================================
# Schema Models
# ============================================================================

class ColumnInfo(BaseModel):
    """Information about a database column"""
    name: str
    type: str
    nullable: bool = True
    primary_key: bool = False


class TableSchema(BaseModel):
    """Schema information for a database table"""
    name: str
    columns: List[ColumnInfo]
    row_count: int = 0
    created_at: Optional[datetime] = None


class DatabaseSchemaResponse(BaseModel):
    """Response for database schema endpoint"""
    tables: List[TableSchema]
    total_tables: int
    error: Optional[str] = None


# ============================================================================
# Insights Models
# ============================================================================

class ColumnInsight(BaseModel):
    """Statistical insight for a column"""
    column_name: str
    data_type: str
    null_count: int = 0
    unique_count: int = 0
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    avg_value: Optional[float] = None
    sample_values: List[Any] = Field(default_factory=list)


class InsightsRequest(BaseModel):
    """Request for generating insights"""
    table_name: str
    column_names: Optional[List[str]] = None


class InsightsResponse(BaseModel):
    """Response for insights generation"""
    table_name: str
    insights: List[ColumnInsight]
    generated_at: datetime
    error: Optional[str] = None


# ============================================================================
# Export Models
# ============================================================================

class ExportRequest(BaseModel):
    """Request for exporting table data"""
    table_name: str
    format: str = "csv"  # csv, json, xlsx


class QueryExportRequest(BaseModel):
    """Request for exporting query results"""
    sql: str
    format: str = "csv"  # csv, json, xlsx


# ============================================================================
# Health Check Models
# ============================================================================

class HealthCheckResponse(BaseModel):
    """Response for health check endpoint"""
    status: str = "healthy"
    version: str = "1.0.0"
    uptime_seconds: float = 0
    database_connected: bool = True
    error: Optional[str] = None


# ============================================================================
# Product Models (for product database)
# ============================================================================

class ProductBase(BaseModel):
    """Base product model with common fields"""
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    sku: Optional[str] = None
    stock_quantity: int = 0


class ProductCreate(ProductBase):
    """Model for creating a new product"""
    pass


class ProductUpdate(BaseModel):
    """Model for updating a product (all fields optional)"""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    sku: Optional[str] = None
    stock_quantity: Optional[int] = None


class Product(ProductBase):
    """Full product model with ID and timestamps"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ProductResponse(BaseModel):
    """Response for single product operations"""
    product: Optional[Product] = None
    error: Optional[str] = None


class ProductListResponse(BaseModel):
    """Response for product list operations"""
    products: List[Product]
    total_count: int
    error: Optional[str] = None
