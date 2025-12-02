"""
CODEXA Competitor Scout Module

Monitors and analyzes competitor products, pricing, and strategies in the e-commerce space.

Core Capabilities:
- Competitor tracking and monitoring
- Price comparison and analysis
- Market positioning insights
- Competitive intelligence gathering
- Trend detection and alerts
"""

from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

from ..utils.logger import get_logger
from ..crud_ops import get_crud_ops, CRUDOperations

logger = get_logger()


class CompetitorStatus(str, Enum):
    """Competitor monitoring status."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"


class ThreatLevel(str, Enum):
    """Competitive threat assessment."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CompetitorProduct(BaseModel):
    """Competitor product data model."""

    id: str = Field(..., description="Unique identifier")
    competitor_id: str = Field(..., description="Competitor identifier")
    product_name: str = Field(..., description="Product name")
    category: str = Field(..., description="Product category")

    # Pricing data
    current_price: float = Field(..., description="Current price")
    previous_price: Optional[float] = Field(None, description="Previous price")
    price_history: List[Dict[str, Any]] = Field(
        default_factory=list, description="Historical prices"
    )

    # Market data
    marketplace_rank: Optional[int] = Field(None, description="Marketplace ranking")
    rating: Optional[float] = Field(None, description="Product rating")
    review_count: int = Field(default=0, description="Number of reviews")
    sales_estimate: Optional[int] = Field(None, description="Estimated monthly sales")

    # Analysis
    threat_level: ThreatLevel = Field(default=ThreatLevel.MEDIUM)
    competitive_advantages: List[str] = Field(
        default_factory=list, description="Identified advantages"
    )
    weaknesses: List[str] = Field(
        default_factory=list, description="Identified weaknesses"
    )

    # Tracking
    url: Optional[str] = Field(None, description="Product URL")
    last_scraped: Optional[str] = Field(None, description="Last data collection")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    def add_price_snapshot(self, price: float):
        """Add a price snapshot to history."""
        self.price_history.append(
            {"price": price, "timestamp": datetime.now().isoformat()}
        )
        self.previous_price = self.current_price
        self.current_price = price
        self.updated_at = datetime.now().isoformat()

    def calculate_price_change_percentage(self) -> float:
        """Calculate price change percentage."""
        if self.previous_price and self.previous_price > 0:
            return ((self.current_price - self.previous_price) / self.previous_price) * 100
        return 0.0


class Competitor(BaseModel):
    """Competitor entity data model."""

    id: str = Field(..., description="Unique competitor identifier")
    name: str = Field(..., description="Competitor name/brand")
    description: Optional[str] = Field(None, description="Competitor description")

    # Business data
    store_url: Optional[str] = Field(None, description="Store/marketplace URL")
    categories: List[str] = Field(
        default_factory=list, description="Product categories they compete in"
    )

    # Market position
    market_share_estimate: Optional[float] = Field(
        None, description="Estimated market share %"
    )
    threat_level: ThreatLevel = Field(default=ThreatLevel.MEDIUM)

    # Tracking
    status: CompetitorStatus = Field(default=CompetitorStatus.ACTIVE)
    product_count: int = Field(default=0, description="Number of tracked products")
    last_analyzed: Optional[str] = Field(None, description="Last analysis timestamp")

    # Intelligence
    strengths: List[str] = Field(
        default_factory=list, description="Competitive strengths"
    )
    weaknesses: List[str] = Field(
        default_factory=list, description="Competitive weaknesses"
    )
    strategies: List[str] = Field(
        default_factory=list, description="Observed strategies"
    )

    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class CompetitorScout:
    """
    Competitor intelligence and monitoring system.

    Capabilities:
    - Track competitors and their products
    - Monitor pricing and market positioning
    - Generate competitive insights
    - Alert on competitive threats
    """

    def __init__(
        self,
        data_dir: Path = Path("./data"),
        auto_backup: bool = True,
        auto_git: bool = True,
        dry_run: bool = False,
    ):
        """
        Initialize Competitor Scout.

        Args:
            data_dir: Directory for competitor data
            auto_backup: Enable automatic backups
            auto_git: Enable automatic git commits
            dry_run: Preview mode
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.crud = get_crud_ops(
            auto_backup=auto_backup, auto_git=auto_git, dry_run=dry_run
        )
        self.dry_run = dry_run

        logger.module_loaded(
            "CompetitorScout",
            capabilities=[
                "competitor_tracking",
                "price_monitoring",
                "threat_assessment",
                "competitive_intelligence",
            ],
        )

    # ==================== COMPETITOR MANAGEMENT ====================

    def add_competitor(self, competitor: Competitor) -> Tuple[bool, str]:
        """
        Add a new competitor to track.

        Args:
            competitor: Competitor object

        Returns:
            Tuple of (success, competitor_id_or_error)
        """
        logger.operation_start("add_competitor", name=competitor.name)

        try:
            success, result = self.crud.create_data_record(
                collection="competitors",
                record=competitor.model_dump(),
                record_id=competitor.id,
                data_dir=self.data_dir,
            )

            if success:
                logger.operation_success("add_competitor", id=competitor.id)
            else:
                logger.operation_failure("add_competitor", result, name=competitor.name)

            return success, result

        except Exception as e:
            logger.operation_failure("add_competitor", str(e), name=competitor.name)
            return False, str(e)

    def get_competitor(
        self, competitor_id: str
    ) -> Tuple[bool, Union[Competitor, str]]:
        """
        Retrieve competitor information.

        Args:
            competitor_id: Competitor ID

        Returns:
            Tuple of (success, competitor_or_error)
        """
        logger.operation_start("get_competitor", id=competitor_id)

        try:
            success, result = self.crud.read_data_record(
                collection="competitors",
                record_id=competitor_id,
                data_dir=self.data_dir,
            )

            if success:
                competitor = Competitor(**result)
                logger.operation_success("get_competitor", id=competitor_id)
                return True, competitor
            else:
                logger.operation_failure("get_competitor", result, id=competitor_id)
                return False, result

        except Exception as e:
            logger.operation_failure("get_competitor", str(e), id=competitor_id)
            return False, str(e)

    def list_competitors(
        self, status: Optional[CompetitorStatus] = None
    ) -> Tuple[bool, Union[List[Competitor], str]]:
        """
        List all tracked competitors.

        Args:
            status: Filter by status

        Returns:
            Tuple of (success, competitors_or_error)
        """
        logger.operation_start("list_competitors", status=status)

        try:
            success, result = self.crud.list_data_records(
                collection="competitors", data_dir=self.data_dir
            )

            if not success:
                return False, result

            competitors = [Competitor(**record) for record in result]

            if status:
                competitors = [c for c in competitors if c.status == status]

            logger.operation_success("list_competitors", count=len(competitors))
            return True, competitors

        except Exception as e:
            logger.operation_failure("list_competitors", str(e))
            return False, str(e)

    # ==================== PRODUCT TRACKING ====================

    def track_competitor_product(
        self, product: CompetitorProduct
    ) -> Tuple[bool, str]:
        """
        Add a competitor product to tracking.

        Args:
            product: CompetitorProduct object

        Returns:
            Tuple of (success, product_id_or_error)
        """
        logger.operation_start(
            "track_competitor_product",
            competitor=product.competitor_id,
            product=product.product_name,
        )

        try:
            success, result = self.crud.create_data_record(
                collection="competitor_products",
                record=product.model_dump(),
                record_id=product.id,
                data_dir=self.data_dir,
            )

            if success:
                # Update competitor's product count
                comp_success, competitor = self.get_competitor(product.competitor_id)
                if comp_success:
                    self.crud.update_data_record(
                        collection="competitors",
                        record_id=product.competitor_id,
                        updates={"product_count": competitor.product_count + 1},
                        data_dir=self.data_dir,
                    )

                logger.operation_success("track_competitor_product", id=product.id)
            else:
                logger.operation_failure(
                    "track_competitor_product", result, product=product.product_name
                )

            return success, result

        except Exception as e:
            logger.operation_failure(
                "track_competitor_product", str(e), product=product.product_name
            )
            return False, str(e)

    def update_product_price(
        self, product_id: str, new_price: float
    ) -> Tuple[bool, str]:
        """
        Update competitor product price and add to history.

        Args:
            product_id: Product ID
            new_price: New price observed

        Returns:
            Tuple of (success, message)
        """
        logger.operation_start("update_product_price", id=product_id, price=new_price)

        try:
            # Get current product
            success, result = self.crud.read_data_record(
                collection="competitor_products",
                record_id=product_id,
                data_dir=self.data_dir,
            )

            if not success:
                return False, result

            product = CompetitorProduct(**result)
            product.add_price_snapshot(new_price)

            # Update record
            success, result = self.crud.update_data_record(
                collection="competitor_products",
                record_id=product_id,
                updates=product.model_dump(),
                data_dir=self.data_dir,
            )

            if success:
                price_change = product.calculate_price_change_percentage()
                logger.operation_success(
                    "update_product_price",
                    id=product_id,
                    change_pct=f"{price_change:.2f}%",
                )

            return success, result

        except Exception as e:
            logger.operation_failure("update_product_price", str(e), id=product_id)
            return False, str(e)

    def get_competitor_products(
        self, competitor_id: str
    ) -> Tuple[bool, Union[List[CompetitorProduct], str]]:
        """
        Get all products for a specific competitor.

        Args:
            competitor_id: Competitor ID

        Returns:
            Tuple of (success, products_or_error)
        """
        logger.operation_start("get_competitor_products", competitor=competitor_id)

        try:
            success, result = self.crud.list_data_records(
                collection="competitor_products", data_dir=self.data_dir
            )

            if not success:
                return False, result

            products = [
                CompetitorProduct(**record)
                for record in result
                if record.get("competitor_id") == competitor_id
            ]

            logger.operation_success(
                "get_competitor_products", competitor=competitor_id, count=len(products)
            )
            return True, products

        except Exception as e:
            logger.operation_failure(
                "get_competitor_products", str(e), competitor=competitor_id
            )
            return False, str(e)

    # ==================== ANALYTICS & INSIGHTS ====================

    def get_price_comparison(
        self, category: str
    ) -> Tuple[bool, Union[Dict[str, Any], str]]:
        """
        Get price comparison for a category across all competitors.

        Args:
            category: Product category

        Returns:
            Tuple of (success, comparison_data_or_error)
        """
        logger.operation_start("get_price_comparison", category=category)

        try:
            success, result = self.crud.list_data_records(
                collection="competitor_products", data_dir=self.data_dir
            )

            if not success:
                return False, result

            # Filter by category
            products = [
                CompetitorProduct(**record)
                for record in result
                if record.get("category") == category
            ]

            if not products:
                return True, {
                    "category": category,
                    "products": 0,
                    "avg_price": 0,
                    "min_price": 0,
                    "max_price": 0,
                }

            prices = [p.current_price for p in products]

            comparison = {
                "category": category,
                "products": len(products),
                "avg_price": sum(prices) / len(prices),
                "min_price": min(prices),
                "max_price": max(prices),
                "price_range": max(prices) - min(prices),
                "products_by_competitor": {},
            }

            # Group by competitor
            for product in products:
                comp_id = product.competitor_id
                if comp_id not in comparison["products_by_competitor"]:
                    comparison["products_by_competitor"][comp_id] = {
                        "count": 0,
                        "avg_price": 0,
                        "products": [],
                    }
                comparison["products_by_competitor"][comp_id]["count"] += 1
                comparison["products_by_competitor"][comp_id]["products"].append(
                    {
                        "name": product.product_name,
                        "price": product.current_price,
                        "rank": product.marketplace_rank,
                    }
                )

            # Calculate average prices per competitor
            for comp_id, data in comparison["products_by_competitor"].items():
                comp_prices = [p["price"] for p in data["products"]]
                data["avg_price"] = sum(comp_prices) / len(comp_prices)

            logger.operation_success("get_price_comparison", category=category)
            return True, comparison

        except Exception as e:
            logger.operation_failure("get_price_comparison", str(e), category=category)
            return False, str(e)

    def identify_threats(self) -> Tuple[bool, Union[List[Dict[str, Any]], str]]:
        """
        Identify high-threat competitors and products.

        Returns:
            Tuple of (success, threats_or_error)
        """
        logger.operation_start("identify_threats")

        try:
            # Get all competitors
            success, competitors = self.list_competitors(status=CompetitorStatus.ACTIVE)
            if not success:
                return False, competitors

            threats = []

            for competitor in competitors:
                if competitor.threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
                    # Get their products
                    prod_success, products = self.get_competitor_products(competitor.id)

                    threat_data = {
                        "competitor_id": competitor.id,
                        "competitor_name": competitor.name,
                        "threat_level": competitor.threat_level.value,
                        "product_count": competitor.product_count,
                        "strengths": competitor.strengths,
                        "strategies": competitor.strategies,
                        "products": [],
                    }

                    if prod_success:
                        # Add high-threat products
                        high_threat_products = [
                            {
                                "name": p.product_name,
                                "price": p.current_price,
                                "rank": p.marketplace_rank,
                                "threat_level": p.threat_level.value,
                            }
                            for p in products
                            if p.threat_level
                            in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]
                        ]
                        threat_data["products"] = high_threat_products

                    threats.append(threat_data)

            logger.operation_success("identify_threats", count=len(threats))
            return True, threats

        except Exception as e:
            logger.operation_failure("identify_threats", str(e))
            return False, str(e)

    def get_capabilities(self) -> List[str]:
        """Get list of available capabilities."""
        return [
            "add_competitor",
            "get_competitor",
            "list_competitors",
            "track_competitor_product",
            "update_product_price",
            "get_competitor_products",
            "get_price_comparison",
            "identify_threats",
        ]


# Global Competitor Scout instance
_global_competitor_scout: Optional[CompetitorScout] = None


def get_competitor_scout(
    data_dir: Path = Path("./data"),
    auto_backup: bool = True,
    auto_git: bool = True,
    dry_run: bool = False,
) -> CompetitorScout:
    """
    Get or create the global Competitor Scout instance.

    Args:
        data_dir: Directory for competitor data
        auto_backup: Enable automatic backups
        auto_git: Enable automatic git commits
        dry_run: Preview mode

    Returns:
        CompetitorScout instance
    """
    global _global_competitor_scout

    if _global_competitor_scout is None:
        _global_competitor_scout = CompetitorScout(
            data_dir=data_dir,
            auto_backup=auto_backup,
            auto_git=auto_git,
            dry_run=dry_run,
        )

    return _global_competitor_scout
