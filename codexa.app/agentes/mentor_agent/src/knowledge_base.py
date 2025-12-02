"""
CODEXA Knowledge Base Module

Manages organizational knowledge, insights, best practices, and learnings from
e-commerce operations.

Core Capabilities:
- Knowledge article management
- Insight capture and categorization
- Best practices documentation
- Lessons learned tracking
- Cross-module knowledge integration
- Search and retrieval
"""

from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

from ..utils.logger import get_logger
from ..crud_ops import get_crud_ops, CRUDOperations

logger = get_logger()


class KnowledgeType(str, Enum):
    """Type of knowledge article."""

    INSIGHT = "insight"  # Competitive or market insight
    BEST_PRACTICE = "best_practice"  # Proven best practice
    LESSON_LEARNED = "lesson_learned"  # Learning from experience
    STRATEGY = "strategy"  # Strategic guidance
    PROCESS = "process"  # Process documentation
    REFERENCE = "reference"  # Reference material


class KnowledgeStatus(str, Enum):
    """Knowledge article status."""

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"


class Relevance(str, Enum):
    """Knowledge relevance level."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class KnowledgeArticle(BaseModel):
    """Knowledge base article."""

    id: str = Field(..., description="Unique article ID")
    title: str = Field(..., description="Article title")
    content: str = Field(..., description="Article content (markdown)")
    summary: Optional[str] = Field(None, description="Brief summary")

    # Classification
    knowledge_type: KnowledgeType = Field(..., description="Type of knowledge")
    category: str = Field(..., description="Category (e.g., 'pricing', 'marketing')")
    tags: List[str] = Field(default_factory=list, description="Search tags")

    # Source and context
    source: Optional[str] = Field(
        None, description="Source (e.g., 'competitor_analysis', 'product_launch')"
    )
    source_module: Optional[str] = Field(
        None, description="Originating module (e.g., 'competitor_scout')"
    )
    related_entities: List[str] = Field(
        default_factory=list,
        description="Related IDs (product_id, competitor_id, plan_id)",
    )

    # Metadata
    status: KnowledgeStatus = Field(default=KnowledgeStatus.DRAFT)
    relevance: Relevance = Field(default=Relevance.MEDIUM)
    author: Optional[str] = Field(None, description="Article author")
    views: int = Field(default=0, description="View count")
    usefulness_score: float = Field(
        default=0.0, description="Usefulness rating (0-10)"
    )

    # Timestamps
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    published_at: Optional[str] = Field(None, description="Publication timestamp")


class KnowledgeInsight(BaseModel):
    """Quick insight or observation."""

    id: str = Field(..., description="Unique insight ID")
    insight: str = Field(..., description="The insight text")
    category: str = Field(..., description="Insight category")
    source: str = Field(..., description="Source of insight")
    confidence: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Confidence level (0-1)"
    )
    actionable: bool = Field(default=False, description="Is this actionable?")
    action_taken: bool = Field(default=False, description="Was action taken?")
    tags: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class KnowledgeBase:
    """
    Knowledge base management system.

    Capabilities:
    - Create and manage knowledge articles
    - Capture insights from operations
    - Organize and categorize knowledge
    - Search and retrieve relevant information
    - Track knowledge usage and effectiveness
    """

    def __init__(
        self,
        data_dir: Path = Path("./knowledge"),
        auto_backup: bool = True,
        auto_git: bool = True,
        dry_run: bool = False,
    ):
        """
        Initialize Knowledge Base.

        Args:
            data_dir: Directory for knowledge storage
            auto_backup: Enable automatic backups
            auto_git: Enable automatic git commits
            dry_run: Preview mode
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories for organization
        (self.data_dir / "articles").mkdir(exist_ok=True)
        (self.data_dir / "insights").mkdir(exist_ok=True)

        self.crud = get_crud_ops(
            auto_backup=auto_backup, auto_git=auto_git, dry_run=dry_run
        )
        self.dry_run = dry_run

        logger.module_loaded(
            "KnowledgeBase",
            capabilities=[
                "article_management",
                "insight_capture",
                "knowledge_search",
                "cross_module_integration",
            ],
        )

    # ==================== ARTICLE MANAGEMENT ====================

    def create_article(self, article: KnowledgeArticle) -> Tuple[bool, str]:
        """
        Create a new knowledge article.

        Args:
            article: KnowledgeArticle object

        Returns:
            Tuple of (success, article_id_or_error)
        """
        logger.operation_start("create_article", title=article.title)

        try:
            # Save as markdown document
            article_path = (
                self.data_dir / "articles" / f"{article.id}_{article.title[:30]}.md"
            )

            metadata = {
                "id": article.id,
                "type": article.knowledge_type.value,
                "category": article.category,
                "status": article.status.value,
                "tags": ", ".join(article.tags),
            }

            # Create markdown content
            content = f"# {article.title}\n\n"
            if article.summary:
                content += f"**Summary**: {article.summary}\n\n"
            content += article.content

            success, message = self.crud.create_document(
                path=article_path,
                content=content,
                doc_type="markdown",
                metadata=metadata,
            )

            if not success:
                return False, message

            # Also save as structured data
            success, result = self.crud.create_data_record(
                collection="knowledge_articles",
                record=article.model_dump(),
                record_id=article.id,
                data_dir=self.data_dir,
            )

            if success:
                logger.operation_success("create_article", id=article.id)
                return True, article.id
            else:
                logger.operation_failure("create_article", result, title=article.title)
                return False, result

        except Exception as e:
            logger.operation_failure("create_article", str(e), title=article.title)
            return False, str(e)

    def get_article(
        self, article_id: str
    ) -> Tuple[bool, Union[KnowledgeArticle, str]]:
        """
        Retrieve a knowledge article.

        Args:
            article_id: Article ID

        Returns:
            Tuple of (success, article_or_error)
        """
        logger.operation_start("get_article", id=article_id)

        try:
            success, result = self.crud.read_data_record(
                collection="knowledge_articles",
                record_id=article_id,
                data_dir=self.data_dir,
            )

            if success:
                article = KnowledgeArticle(**result)

                # Increment view count
                article.views += 1
                self.crud.update_data_record(
                    collection="knowledge_articles",
                    record_id=article_id,
                    updates={"views": article.views},
                    data_dir=self.data_dir,
                )

                logger.operation_success("get_article", id=article_id)
                return True, article
            else:
                logger.operation_failure("get_article", result, id=article_id)
                return False, result

        except Exception as e:
            logger.operation_failure("get_article", str(e), id=article_id)
            return False, str(e)

    def update_article(
        self, article_id: str, updates: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """
        Update a knowledge article.

        Args:
            article_id: Article ID
            updates: Dictionary of updates

        Returns:
            Tuple of (success, message)
        """
        logger.operation_start("update_article", id=article_id)

        try:
            updates["updated_at"] = datetime.now().isoformat()

            success, result = self.crud.update_data_record(
                collection="knowledge_articles",
                record_id=article_id,
                updates=updates,
                data_dir=self.data_dir,
            )

            if success:
                logger.operation_success("update_article", id=article_id)
            else:
                logger.operation_failure("update_article", result, id=article_id)

            return success, result

        except Exception as e:
            logger.operation_failure("update_article", str(e), id=article_id)
            return False, str(e)

    def publish_article(self, article_id: str) -> Tuple[bool, str]:
        """
        Publish an article (change status to published).

        Args:
            article_id: Article ID

        Returns:
            Tuple of (success, message)
        """
        logger.operation_start("publish_article", id=article_id)

        updates = {
            "status": KnowledgeStatus.PUBLISHED.value,
            "published_at": datetime.now().isoformat(),
        }

        return self.update_article(article_id, updates)

    def list_articles(
        self,
        knowledge_type: Optional[KnowledgeType] = None,
        category: Optional[str] = None,
        status: Optional[KnowledgeStatus] = None,
    ) -> Tuple[bool, Union[List[KnowledgeArticle], str]]:
        """
        List knowledge articles with optional filters.

        Args:
            knowledge_type: Filter by type
            category: Filter by category
            status: Filter by status

        Returns:
            Tuple of (success, articles_or_error)
        """
        logger.operation_start(
            "list_articles", type=knowledge_type, category=category, status=status
        )

        try:
            success, result = self.crud.list_data_records(
                collection="knowledge_articles", data_dir=self.data_dir
            )

            if not success:
                return False, result

            articles = [KnowledgeArticle(**record) for record in result]

            # Apply filters
            if knowledge_type:
                articles = [a for a in articles if a.knowledge_type == knowledge_type]
            if category:
                articles = [a for a in articles if a.category == category]
            if status:
                articles = [a for a in articles if a.status == status]

            # Sort by relevance and creation date
            relevance_order = {
                Relevance.CRITICAL: 0,
                Relevance.HIGH: 1,
                Relevance.MEDIUM: 2,
                Relevance.LOW: 3,
            }
            articles.sort(
                key=lambda a: (relevance_order.get(a.relevance, 99), a.created_at),
                reverse=True,
            )

            logger.operation_success("list_articles", count=len(articles))
            return True, articles

        except Exception as e:
            logger.operation_failure("list_articles", str(e))
            return False, str(e)

    # ==================== INSIGHT MANAGEMENT ====================

    def capture_insight(self, insight: KnowledgeInsight) -> Tuple[bool, str]:
        """
        Capture a quick insight.

        Args:
            insight: KnowledgeInsight object

        Returns:
            Tuple of (success, insight_id_or_error)
        """
        logger.operation_start("capture_insight", source=insight.source)

        try:
            success, result = self.crud.create_data_record(
                collection="insights",
                record=insight.model_dump(),
                record_id=insight.id,
                data_dir=self.data_dir,
            )

            if success:
                logger.operation_success("capture_insight", id=insight.id)
            else:
                logger.operation_failure("capture_insight", result, source=insight.source)

            return success, result

        except Exception as e:
            logger.operation_failure("capture_insight", str(e), source=insight.source)
            return False, str(e)

    def get_insights(
        self,
        category: Optional[str] = None,
        actionable_only: bool = False,
        limit: int = 50,
    ) -> Tuple[bool, Union[List[KnowledgeInsight], str]]:
        """
        Retrieve insights with optional filters.

        Args:
            category: Filter by category
            actionable_only: Only return actionable insights
            limit: Maximum number of insights to return

        Returns:
            Tuple of (success, insights_or_error)
        """
        logger.operation_start("get_insights", category=category)

        try:
            success, result = self.crud.list_data_records(
                collection="insights", data_dir=self.data_dir
            )

            if not success:
                return False, result

            insights = [KnowledgeInsight(**record) for record in result]

            # Apply filters
            if category:
                insights = [i for i in insights if i.category == category]
            if actionable_only:
                insights = [i for i in insights if i.actionable and not i.action_taken]

            # Sort by confidence and recency
            insights.sort(key=lambda i: (i.confidence, i.created_at), reverse=True)

            # Limit results
            insights = insights[:limit]

            logger.operation_success("get_insights", count=len(insights))
            return True, insights

        except Exception as e:
            logger.operation_failure("get_insights", str(e))
            return False, str(e)

    # ==================== SEARCH & DISCOVERY ====================

    def search_articles(
        self, query: str, limit: int = 10
    ) -> Tuple[bool, Union[List[KnowledgeArticle], str]]:
        """
        Search knowledge articles by query string.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            Tuple of (success, articles_or_error)
        """
        logger.operation_start("search_articles", query=query)

        try:
            success, articles = self.list_articles(status=KnowledgeStatus.PUBLISHED)
            if not success:
                return False, articles

            query_lower = query.lower()

            # Simple text search (can be enhanced with better search algorithms)
            matches = []
            for article in articles:
                score = 0
                if query_lower in article.title.lower():
                    score += 10
                if query_lower in article.content.lower():
                    score += 5
                if article.summary and query_lower in article.summary.lower():
                    score += 7
                for tag in article.tags:
                    if query_lower in tag.lower():
                        score += 3

                if score > 0:
                    matches.append((score, article))

            # Sort by score
            matches.sort(key=lambda x: x[0], reverse=True)
            results = [article for _, article in matches[:limit]]

            logger.operation_success("search_articles", query=query, results=len(results))
            return True, results

        except Exception as e:
            logger.operation_failure("search_articles", str(e), query=query)
            return False, str(e)

    def get_related_knowledge(
        self, entity_id: str
    ) -> Tuple[bool, Union[Dict[str, List], str]]:
        """
        Get all knowledge related to a specific entity (product, competitor, plan).

        Args:
            entity_id: Entity ID to find related knowledge for

        Returns:
            Tuple of (success, related_knowledge_dict_or_error)
        """
        logger.operation_start("get_related_knowledge", entity=entity_id)

        try:
            # Get articles
            success, articles = self.list_articles()
            if not success:
                return False, articles

            related_articles = [
                a for a in articles if entity_id in a.related_entities
            ]

            # Get insights
            success, insights = self.get_insights()
            if not success:
                insights = []

            related = {
                "articles": related_articles,
                "insights": insights,  # Could filter by tags/entity
                "entity_id": entity_id,
                "total_items": len(related_articles) + len(insights),
            }

            logger.operation_success(
                "get_related_knowledge", entity=entity_id, items=related["total_items"]
            )
            return True, related

        except Exception as e:
            logger.operation_failure("get_related_knowledge", str(e), entity=entity_id)
            return False, str(e)

    def get_capabilities(self) -> List[str]:
        """Get list of available capabilities."""
        return [
            "create_article",
            "get_article",
            "update_article",
            "publish_article",
            "list_articles",
            "capture_insight",
            "get_insights",
            "search_articles",
            "get_related_knowledge",
        ]


# Global Knowledge Base instance
_global_knowledge_base: Optional[KnowledgeBase] = None


def get_knowledge_base(
    data_dir: Path = Path("./knowledge"),
    auto_backup: bool = True,
    auto_git: bool = True,
    dry_run: bool = False,
) -> KnowledgeBase:
    """
    Get or create the global Knowledge Base instance.

    Args:
        data_dir: Directory for knowledge storage
        auto_backup: Enable automatic backups
        auto_git: Enable automatic git commits
        dry_run: Preview mode

    Returns:
        KnowledgeBase instance
    """
    global _global_knowledge_base

    if _global_knowledge_base is None:
        _global_knowledge_base = KnowledgeBase(
            data_dir=data_dir,
            auto_backup=auto_backup,
            auto_git=auto_git,
            dry_run=dry_run,
        )

    return _global_knowledge_base
