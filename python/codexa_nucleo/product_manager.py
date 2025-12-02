"""
CODEXA Product Manager Module

Comprehensive CRUD operations for e-commerce product catalogs.
Supports product data management, bulk operations, and search.

Part of CODEXA HOP-001 E-commerce suite.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from hop_orchestrator import BaseModule
from modules.utils.logger import get_logger
from modules.utils.file_ops import FileOperationsSkill
from modules.utils.git_helper import GitHelper

logger = get_logger("codexa.product")


class ProductStatus(str, Enum):
    """Product status options."""
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"
    OUT_OF_STOCK = "out_of_stock"
    DISCONTINUED = "discontinued"


class Product(BaseModel):
    """Product data model."""

    id: str = Field(description="Unique product ID")
    name: str = Field(description="Product name")
    description: str = Field(description="Product description")
    price: float = Field(description="Product price")
    currency: str = Field(default="BRL", description="Currency code")
    category: str = Field(description="Product category")
    keywords: List[str] = Field(default_factory=list, description="Search keywords")
    competitors: List[str] = Field(default_factory=list, description="Competitor product IDs")
    status: ProductStatus = Field(default=ProductStatus.DRAFT)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Optional fields
    sku: Optional[str] = None
    stock_quantity: Optional[int] = None
    images: List[str] = Field(default_factory=list)
    specifications: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ProductManager(BaseModule):
    """Product management module."""

    def __init__(self, working_dir: Optional[str] = None):
        super().__init__(
            name="product_manager",
            description="E-commerce product catalog management with CRUD operations"
        )

        self.working_dir = Path(working_dir or os.getcwd())
        self.products_dir = self.working_dir / "data" / "products"
        self.products_dir.mkdir(parents=True, exist_ok=True)

        self.file_ops = FileOperationsSkill(str(self.working_dir))
        self.git = GitHelper(str(self.working_dir))

        # Register operations
        self._register_operations()

        logger.info(f"Product Manager initialized at: {self.products_dir}")

    def _register_operations(self):
        """Register all product operations."""
        self.register_operation(
            "create",
            self.create_product,
            "Create a new product"
        )
        self.register_operation(
            "read",
            self.read_product,
            "Read product by ID"
        )
        self.register_operation(
            "update",
            self.update_product,
            "Update existing product"
        )
        self.register_operation(
            "delete",
            self.delete_product,
            "Delete a product"
        )
        self.register_operation(
            "list",
            self.list_products,
            "List all products"
        )
        self.register_operation(
            "search",
            self.search_products,
            "Search products by keyword"
        )
        self.register_operation(
            "bulk_import",
            self.bulk_import,
            "Import multiple products from JSON"
        )
        self.register_operation(
            "bulk_export",
            self.bulk_export,
            "Export all products to JSON"
        )

    def list_operations(self) -> List[str]:
        """List all operations this module supports."""
        return list(self.operations.keys())

    def get_operation_info(self, operation: str) -> Dict[str, Any]:
        """Get detailed information about an operation."""
        if operation not in self.operations:
            return {}

        op_data = self.operations[operation]

        params_map = {
            "create": ["name", "description", "price", "category", "keywords"],
            "read": ["product_id"],
            "update": ["product_id", "data"],
            "delete": ["product_id"],
            "list": ["status", "category"],
            "search": ["keyword", "category"],
            "bulk_import": ["file_path"],
            "bulk_export": ["output_path"],
        }

        return {
            "description": op_data["description"],
            "parameters": params_map.get(operation, []),
        }

    def execute(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Execute a product operation."""
        if operation not in self.operations:
            return {
                "success": False,
                "error": f"Unknown operation: {operation}"
            }

        try:
            func = self.operations[operation]["func"]
            result = func(**kwargs)
            return result
        except Exception as e:
            logger.error(f"Product operation '{operation}' failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def _generate_product_id(self, name: str) -> str:
        """Generate a product ID from name."""
        # Simple ID generation - in production, use UUID or more robust method
        base_id = name.lower().replace(" ", "-")[:30]
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{base_id}-{timestamp}"

    def _get_product_path(self, product_id: str) -> Path:
        """Get file path for a product."""
        return self.products_dir / f"{product_id}.json"

    def create_product(
        self,
        name: str,
        description: str,
        price: float,
        category: str,
        keywords: Optional[List[str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a new product.

        Args:
            name: Product name
            description: Product description
            price: Product price
            category: Product category
            keywords: Search keywords
            **kwargs: Additional product fields

        Returns:
            Result dictionary with product data
        """
        try:
            # Generate product ID
            product_id = self._generate_product_id(name)

            # Check if product already exists
            product_path = self._get_product_path(product_id)
            if product_path.exists():
                return {
                    "success": False,
                    "error": f"Product already exists: {product_id}"
                }

            # Create product object
            product = Product(
                id=product_id,
                name=name,
                description=description,
                price=price,
                category=category,
                keywords=keywords or [],
                **kwargs
            )

            # Save to file
            product_data = json.loads(product.model_dump_json())
            success = self.file_ops.write_json(str(product_path), product_data)

            if not success:
                return {
                    "success": False,
                    "error": "Failed to save product"
                }

            # Auto-commit
            if self.git.is_git_repo():
                self.git.auto_commit_data(str(product_path), "product")

            logger.operation("Product Create", "success", f"{product_id} - {name}")

            return {
                "success": True,
                "product_id": product_id,
                "product": product_data,
                "file_path": str(product_path)
            }

        except Exception as e:
            logger.operation("Product Create", "fail", str(e))
            return {
                "success": False,
                "error": str(e)
            }

    def read_product(self, product_id: str) -> Dict[str, Any]:
        """
        Read product by ID.

        Args:
            product_id: Product ID

        Returns:
            Result dictionary with product data
        """
        try:
            product_path = self._get_product_path(product_id)

            if not product_path.exists():
                return {
                    "success": False,
                    "error": f"Product not found: {product_id}"
                }

            # Read product data
            product_data = self.file_ops.read_json(str(product_path))

            if product_data is None:
                return {
                    "success": False,
                    "error": "Failed to read product"
                }

            # Validate with Pydantic model
            product = Product(**product_data)

            logger.operation("Product Read", "success", product_id)

            return {
                "success": True,
                "product_id": product_id,
                "product": json.loads(product.model_dump_json())
            }

        except Exception as e:
            logger.operation("Product Read", "fail", str(e))
            return {
                "success": False,
                "error": str(e)
            }

    def update_product(
        self,
        product_id: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update existing product.

        Args:
            product_id: Product ID
            data: Updated fields

        Returns:
            Result dictionary
        """
        try:
            # Read existing product
            read_result = self.read_product(product_id)
            if not read_result["success"]:
                return read_result

            # Update fields
            product_data = read_result["product"]
            product_data.update(data)
            product_data["updated_at"] = datetime.now().isoformat()

            # Validate with Pydantic
            product = Product(**product_data)

            # Save updated product
            product_path = self._get_product_path(product_id)
            success = self.file_ops.write_json(
                str(product_path),
                json.loads(product.model_dump_json()),
                force=True
            )

            if not success:
                return {
                    "success": False,
                    "error": "Failed to save updated product"
                }

            # Auto-commit
            if self.git.is_git_repo():
                self.git.auto_commit_data(str(product_path), "product")

            logger.operation("Product Update", "success", product_id)

            return {
                "success": True,
                "product_id": product_id,
                "product": json.loads(product.model_dump_json())
            }

        except Exception as e:
            logger.operation("Product Update", "fail", str(e))
            return {
                "success": False,
                "error": str(e)
            }

    def delete_product(
        self,
        product_id: str,
        force: bool = False
    ) -> Dict[str, Any]:
        """
        Delete a product.

        Args:
            product_id: Product ID
            force: Force deletion

        Returns:
            Result dictionary
        """
        try:
            product_path = self._get_product_path(product_id)

            if not product_path.exists():
                return {
                    "success": False,
                    "error": f"Product not found: {product_id}"
                }

            # Delete (backup handled by file_ops)
            success = self.file_ops.delete_file(str(product_path), force=True)

            if not success:
                return {
                    "success": False,
                    "error": "Failed to delete product"
                }

            logger.operation("Product Delete", "success", product_id)

            return {
                "success": True,
                "product_id": product_id,
                "message": f"Product deleted: {product_id}"
            }

        except Exception as e:
            logger.operation("Product Delete", "fail", str(e))
            return {
                "success": False,
                "error": str(e)
            }

    def list_products(
        self,
        status: Optional[str] = None,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List all products (with optional filters).

        Args:
            status: Filter by status
            category: Filter by category

        Returns:
            Result dictionary with product list
        """
        try:
            # Get all product files
            product_files = list(self.products_dir.glob("*.json"))

            products = []
            for product_file in product_files:
                product_data = self.file_ops.read_json(str(product_file))
                if product_data:
                    # Apply filters
                    if status and product_data.get("status") != status:
                        continue
                    if category and product_data.get("category") != category:
                        continue

                    products.append(product_data)

            logger.operation("Product List", "success", f"Found {len(products)} products")

            return {
                "success": True,
                "count": len(products),
                "products": products,
                "filters": {
                    "status": status,
                    "category": category
                }
            }

        except Exception as e:
            logger.operation("Product List", "fail", str(e))
            return {
                "success": False,
                "error": str(e)
            }

    def search_products(
        self,
        keyword: str,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search products by keyword.

        Args:
            keyword: Search keyword
            category: Optional category filter

        Returns:
            Result dictionary with matching products
        """
        try:
            # Get all products
            list_result = self.list_products(category=category)
            if not list_result["success"]:
                return list_result

            # Search in name, description, and keywords
            keyword_lower = keyword.lower()
            matches = []

            for product in list_result["products"]:
                if (keyword_lower in product.get("name", "").lower() or
                    keyword_lower in product.get("description", "").lower() or
                    any(keyword_lower in kw.lower() for kw in product.get("keywords", []))):
                    matches.append(product)

            logger.operation("Product Search", "success", f"Found {len(matches)} matches for '{keyword}'")

            return {
                "success": True,
                "keyword": keyword,
                "count": len(matches),
                "matches": matches
            }

        except Exception as e:
            logger.operation("Product Search", "fail", str(e))
            return {
                "success": False,
                "error": str(e)
            }

    def bulk_import(self, file_path: str) -> Dict[str, Any]:
        """Bulk import products from JSON file."""
        try:
            data = self.file_ops.read_json(file_path)
            if data is None:
                return {
                    "success": False,
                    "error": "Failed to read import file"
                }

            products = data if isinstance(data, list) else [data]
            imported = 0
            errors = []

            for product_data in products:
                try:
                    result = self.create_product(**product_data)
                    if result["success"]:
                        imported += 1
                    else:
                        errors.append(f"{product_data.get('name', 'unknown')}: {result['error']}")
                except Exception as e:
                    errors.append(f"{product_data.get('name', 'unknown')}: {str(e)}")

            return {
                "success": True,
                "imported": imported,
                "errors": errors,
                "total": len(products)
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def bulk_export(self, output_path: Optional[str] = None) -> Dict[str, Any]:
        """Bulk export all products to JSON file."""
        try:
            if output_path is None:
                output_path = str(self.products_dir / f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

            # Get all products
            list_result = self.list_products()
            if not list_result["success"]:
                return list_result

            # Write to file
            success = self.file_ops.write_json(output_path, list_result["products"])

            if not success:
                return {
                    "success": False,
                    "error": "Failed to write export file"
                }

            return {
                "success": True,
                "exported": list_result["count"],
                "output_path": output_path
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_usage_examples(self) -> List[str]:
        """Get usage examples for this module."""
        return [
            "python cli.py ecom products create --name 'Smartwatch X' --price 299.99 --category 'Electronics'",
            "python cli.py ecom products read <product_id>",
            "python cli.py ecom products update <product_id> --price 279.99",
            "python cli.py ecom products delete <product_id>",
            "python cli.py ecom products list --category 'Electronics'",
            "python cli.py ecom products search --keyword 'smart'",
        ]
