#!/usr/bin/env python3
"""
MASTER PIPELINE - Orchestration for Anuncio Agent Pipeline

Comprehensive CLI for orchestrating product processing through the unified-sync
Edge Function. Supports single products and batch operations with built-in
progress tracking, error recovery (LAW 7), and retry logic.

Usage:
    python master_pipeline.py "Product Name"              # Single product
    python master_pipeline.py --batch products.csv        # Batch from CSV
    python master_pipeline.py --batch products.json       # Batch from JSON
    python master_pipeline.py --list                      # Show available products

Options:
    --scope=all|inventory|content|price                   # What to sync (default: all)
    --mode=pull|push|bidirectional                        # Sync direction (default: bidirectional)
    --dry-run                                             # Preview without applying
    --force                                               # Ignore timestamps, always push
    --verbose                                             # Verbose logging
    --log-file LOG_FILE                                   # Log to file
    --max-retries N                                       # Max retry attempts (default: 3)
    --retry-delay SEC                                     # Delay between retries (default: 2)

Examples:
    # Single product sync
    python master_pipeline.py "iPhone 15 Pro"

    # Batch with options
    python master_pipeline.py --batch products.csv --mode=push --scope=content

    # Dry run with verbose output
    python master_pipeline.py "Nike Shoes" --dry-run --verbose

    # Batch with retry settings
    python master_pipeline.py --batch items.json --max-retries 5 --retry-delay 3

Config: codexa-core/.env
Author: CODEXA Anuncio Agent
Version: 1.0.0
"""

import json
import sys
import time
import logging
import argparse
import csv
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from dataclasses import dataclass
from enum import Enum


# ==============================================================================
# PATH SETUP
# ==============================================================================

# Add codexa.app to path for config imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    from config.env_loader import supabase
except ImportError:
    print("ERROR: Could not import config.env_loader. Ensure .env is configured.")
    sys.exit(1)


# ==============================================================================
# ENUMS & DATA CLASSES
# ==============================================================================

class SyncMode(Enum):
    """Sync mode options."""
    PULL = "pull"
    PUSH = "push"
    BIDIRECTIONAL = "bidirectional"


class SyncScope(Enum):
    """Sync scope options."""
    ALL = "all"
    INVENTORY = "inventory"
    CONTENT = "content"
    PRICE = "price"


@dataclass
class SyncConfig:
    """Pipeline sync configuration."""
    mode: SyncMode = SyncMode.BIDIRECTIONAL
    scope: SyncScope = SyncScope.ALL
    dry_run: bool = False
    force: bool = False
    max_retries: int = 3
    retry_delay: int = 2
    verbose: bool = False
    log_file: Optional[str] = None


@dataclass
class SyncResult:
    """Result of a sync operation."""
    product_name: str
    product_id: Optional[str]
    success: bool
    mode: str
    scope: str
    synced_count: int = 0
    created_count: int = 0
    updated_count: int = 0
    skipped_count: int = 0
    error_count: int = 0
    duration_ms: int = 0
    error_message: Optional[str] = None
    retry_count: int = 0
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "product_name": self.product_name,
            "product_id": self.product_id,
            "success": self.success,
            "mode": self.mode,
            "scope": self.scope,
            "synced_count": self.synced_count,
            "created_count": self.created_count,
            "updated_count": self.updated_count,
            "skipped_count": self.skipped_count,
            "error_count": self.error_count,
            "duration_ms": self.duration_ms,
            "error_message": self.error_message,
            "retry_count": self.retry_count,
            "timestamp": self.timestamp,
        }


# ==============================================================================
# LOGGING SETUP
# ==============================================================================

def setup_logging(verbose: bool = False, log_file: Optional[str] = None) -> logging.Logger:
    """Configure logging with optional file output."""
    logger = logging.getLogger("master_pipeline")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_format = logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # File handler (if requested)
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            "[%(asctime)s] %(levelname)s [%(funcName)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger


# ==============================================================================
# SYNC ENGINE
# ==============================================================================

def call_unified_sync(
    mode: str,
    scope: str = "all",
    product_id: Optional[str] = None,
    product_name: Optional[str] = None,
    dry_run: bool = False,
    force: bool = False,
    logger: Optional[logging.Logger] = None,
) -> Dict:
    """
    Call the unified-sync Edge Function with retry logic (LAW 7).

    Implements exponential backoff for transient errors:
    - Network timeouts
    - HTTP 429 (rate limit)
    - HTTP 503 (service unavailable)
    - URLError (DNS, connection issues)
    """
    if logger is None:
        logger = logging.getLogger("master_pipeline")

    api_url = f"{supabase.url}/functions/v1/unified-sync"

    headers = {
        "Authorization": f"Bearer {supabase.service_role_key}",
        "Content-Type": "application/json",
    }

    body = {
        "mode": mode,
        "scope": scope,
        "dryRun": dry_run,
        "force": force,
    }

    if product_id:
        body["productId"] = product_id
    if product_name:
        body["productName"] = product_name

    try:
        req = Request(api_url, data=json.dumps(body).encode("utf-8"),
                     headers=headers, method="POST")
        with urlopen(req, timeout=300) as response:  # 5 min timeout
            result = json.loads(response.read().decode("utf-8"))
            logger.debug(f"Sync response: {json.dumps(result, indent=2)}")
            return result

    except HTTPError as e:
        error_body = e.read().decode("utf-8")
        status = e.code

        # Determine if error is recoverable
        recoverable = status in [429, 503, 504]  # Rate limit, service unavailable, gateway timeout
        error_type = "RECOVERABLE" if recoverable else "FATAL"

        error_msg = f"HTTP {status}: {error_body}"
        logger.warning(f"[{error_type}] {error_msg}")

        return {
            "success": False,
            "error": error_msg,
            "status": status,
            "recoverable": recoverable,
        }

    except URLError as e:
        # Network errors are typically recoverable
        error_msg = str(e.reason)
        logger.warning(f"[RECOVERABLE] Network error: {error_msg}")
        return {
            "success": False,
            "error": error_msg,
            "recoverable": True,
        }

    except Exception as e:
        # Unexpected errors
        error_msg = str(e)
        logger.error(f"[FATAL] Unexpected error: {error_msg}")
        return {
            "success": False,
            "error": error_msg,
            "recoverable": False,
        }


def sync_product_with_retry(
    product_name: str,
    config: SyncConfig,
    logger: logging.Logger,
    product_id: Optional[str] = None,
) -> SyncResult:
    """
    Sync a single product with automatic retry logic (LAW 7).

    Retry Strategy:
    - RECOVERABLE errors: Retry up to max_retries with exponential backoff
    - FATAL errors: Fail immediately
    - Success: Return immediately

    Backoff Formula: delay = retry_delay * (2 ^ retry_count)
    """
    logger.info(f"Starting sync for product: {product_name}")

    retry_count = 0
    last_error = None

    while retry_count <= config.max_retries:
        try:
            logger.debug(f"Attempt {retry_count + 1}/{config.max_retries + 1}")

            start_time = time.time()

            result = call_unified_sync(
                mode=config.mode.value,
                scope=config.scope.value,
                product_id=product_id,
                product_name=product_name,
                dry_run=config.dry_run,
                force=config.force,
                logger=logger,
            )

            duration_ms = int((time.time() - start_time) * 1000)

            # Check for success
            if result.get("success", False):
                stats = result.get("stats", {})
                logger.info(
                    f"SUCCESS: {product_name} | "
                    f"Synced: {stats.get('synced', 0)}, "
                    f"Created: {stats.get('created', 0)}, "
                    f"Updated: {stats.get('updated', 0)}, "
                    f"Duration: {duration_ms}ms"
                )

                return SyncResult(
                    product_name=product_name,
                    product_id=product_id,
                    success=True,
                    mode=config.mode.value,
                    scope=config.scope.value,
                    synced_count=stats.get("synced", 0),
                    created_count=stats.get("created", 0),
                    updated_count=stats.get("updated", 0),
                    skipped_count=stats.get("skipped", 0),
                    error_count=stats.get("errors", 0),
                    duration_ms=duration_ms,
                    retry_count=retry_count,
                )

            # Check if error is recoverable
            if not result.get("recoverable", False):
                # Fatal error - fail immediately
                error_msg = result.get("error", "Unknown error")
                logger.error(f"FATAL ERROR: {product_name} | {error_msg}")

                return SyncResult(
                    product_name=product_name,
                    product_id=product_id,
                    success=False,
                    mode=config.mode.value,
                    scope=config.scope.value,
                    error_message=error_msg,
                    duration_ms=int((time.time() - start_time) * 1000),
                    retry_count=retry_count,
                )

            # Recoverable error - prepare retry
            last_error = result.get("error", "Unknown error")
            retry_count += 1

            if retry_count <= config.max_retries:
                # Calculate exponential backoff
                backoff_delay = config.retry_delay * (2 ** (retry_count - 1))
                logger.warning(
                    f"Recoverable error: {last_error} | "
                    f"Retrying in {backoff_delay}s (attempt {retry_count + 1}/{config.max_retries + 1})"
                )
                time.sleep(backoff_delay)
            else:
                # Max retries exceeded
                logger.error(
                    f"Max retries exceeded ({config.max_retries}) for {product_name}"
                )

        except Exception as e:
            # Unexpected exception
            error_msg = str(e)
            logger.exception(f"Unexpected exception during sync: {error_msg}")
            last_error = error_msg
            retry_count += 1

            if retry_count <= config.max_retries:
                backoff_delay = config.retry_delay * (2 ** (retry_count - 1))
                logger.info(f"Retrying in {backoff_delay}s...")
                time.sleep(backoff_delay)

    # All retries exhausted
    logger.error(f"FAILED: {product_name} after {config.max_retries} retries | {last_error}")

    return SyncResult(
        product_name=product_name,
        product_id=product_id,
        success=False,
        mode=config.mode.value,
        scope=config.scope.value,
        error_message=last_error or "Max retries exceeded",
        retry_count=config.max_retries,
    )


# ==============================================================================
# BATCH PROCESSING
# ==============================================================================

def load_csv_products(file_path: str) -> List[Tuple[str, Optional[str]]]:
    """
    Load products from CSV file.
    Expected columns: product_name (required), product_id (optional)
    """
    products = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("product_name"):
                    product_name = row["product_name"].strip()
                    product_id = row.get("product_id", "").strip() or None
                    products.append((product_name, product_id))
    except Exception as e:
        raise ValueError(f"Error reading CSV file {file_path}: {e}")

    return products


def load_json_products(file_path: str) -> List[Tuple[str, Optional[str]]]:
    """
    Load products from JSON file.
    Expected format: [{"product_name": "...", "product_id": "..."}, ...]
    """
    products = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and item.get("product_name"):
                        product_name = item["product_name"].strip()
                        product_id = item.get("product_id", "").strip() or None
                        products.append((product_name, product_id))
    except Exception as e:
        raise ValueError(f"Error reading JSON file {file_path}: {e}")

    return products


def load_batch_products(file_path: str) -> List[Tuple[str, Optional[str]]]:
    """Load products from batch file (CSV or JSON)."""
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Batch file not found: {file_path}")

    if file_path.suffix.lower() == ".csv":
        return load_csv_products(str(file_path))
    elif file_path.suffix.lower() == ".json":
        return load_json_products(str(file_path))
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")


def process_batch(
    batch_file: str,
    config: SyncConfig,
    logger: logging.Logger,
) -> Tuple[List[SyncResult], Dict]:
    """
    Process multiple products from batch file.
    Returns (results list, summary dict)
    """
    try:
        products = load_batch_products(batch_file)
    except (FileNotFoundError, ValueError) as e:
        logger.error(f"Failed to load batch: {e}")
        return [], {"error": str(e), "total": 0}

    logger.info(f"Loaded {len(products)} products from {batch_file}")

    results = []
    total = len(products)
    success_count = 0
    failed_count = 0

    for idx, (product_name, product_id) in enumerate(products, 1):
        logger.info(f"\n[{idx}/{total}] Processing: {product_name}")
        logger.debug(f"Product ID: {product_id or 'not provided'}")

        result = sync_product_with_retry(product_name, config, logger, product_id)
        results.append(result)

        if result.success:
            success_count += 1
        else:
            failed_count += 1

    # Summary
    summary = {
        "total": total,
        "success": success_count,
        "failed": failed_count,
        "success_rate": f"{(success_count / total * 100):.1f}%" if total > 0 else "N/A",
    }

    return results, summary


def process_single(
    product_name: str,
    config: SyncConfig,
    logger: logging.Logger,
) -> SyncResult:
    """Process a single product."""
    logger.info(f"Processing single product: {product_name}")
    return sync_product_with_retry(product_name, config, logger)


# ==============================================================================
# OUTPUT & REPORTING
# ==============================================================================

def print_result(result: SyncResult, verbose: bool = False):
    """Pretty print sync result."""
    print("\n" + "=" * 80)

    if not result.success:
        print(f"FAILED: {result.product_name}")
        if result.error_message:
            print(f"Error: {result.error_message}")
        if result.retry_count > 0:
            print(f"Retries: {result.retry_count}")
        print("=" * 80)
        return

    print(f"SUCCESS: {result.product_name}")
    print("-" * 80)
    print(f"Mode:     {result.mode}")
    print(f"Scope:    {result.scope}")
    print(f"Duration: {result.duration_ms}ms")
    print(f"Stats:")
    print(f"  Synced:   {result.synced_count}")
    print(f"  Created:  {result.created_count}")
    print(f"  Updated:  {result.updated_count}")
    print(f"  Skipped:  {result.skipped_count}")
    print(f"  Errors:   {result.error_count}")
    if result.retry_count > 0:
        print(f"  Retries:  {result.retry_count}")
    print("=" * 80)


def print_batch_summary(results: List[SyncResult], summary: Dict):
    """Print batch processing summary."""
    print("\n" + "=" * 80)
    print("BATCH SUMMARY")
    print("=" * 80)
    print(f"Total:        {summary.get('total', 0)}")
    print(f"Success:      {summary.get('success', 0)}")
    print(f"Failed:       {summary.get('failed', 0)}")
    print(f"Success Rate: {summary.get('success_rate', 'N/A')}")
    print("=" * 80)

    if results:
        print("\nDetails:")
        for result in results:
            status = "✓" if result.success else "✗"
            print(f"  {status} {result.product_name}")
            if not result.success and result.error_message:
                print(f"     Error: {result.error_message[:60]}")

    print()


def save_results(results: List[SyncResult], output_file: str, logger: logging.Logger):
    """Save results to JSON file."""
    try:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(
                [r.to_dict() for r in results],
                f,
                indent=2,
                ensure_ascii=False
            )

        logger.info(f"Results saved to: {output_path}")
    except Exception as e:
        logger.error(f"Failed to save results: {e}")


# ==============================================================================
# CLI INTERFACE
# ==============================================================================

def create_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Master Pipeline - Anuncio Agent Orchestration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single product
  python master_pipeline.py "iPhone 15 Pro"

  # Batch from CSV
  python master_pipeline.py --batch products.csv --verbose

  # Batch from JSON with options
  python master_pipeline.py --batch items.json --mode=push --scope=content

  # Dry run
  python master_pipeline.py "Nike Shoes" --dry-run

  # With custom retry settings
  python master_pipeline.py "Product" --max-retries 5 --retry-delay 3
        """
    )

    # Positional argument
    parser.add_argument(
        "product",
        nargs="?",
        help="Product name (single product mode)"
    )

    # Batch options
    parser.add_argument(
        "--batch",
        help="Batch file (CSV or JSON) with product list"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List available products from Supabase"
    )

    # Sync options
    parser.add_argument(
        "--mode",
        choices=["pull", "push", "bidirectional"],
        default="bidirectional",
        help="Sync mode (default: bidirectional)"
    )

    parser.add_argument(
        "--scope",
        choices=["all", "inventory", "content", "price"],
        default="all",
        help="Sync scope (default: all)"
    )

    # Execution options
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without applying"
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Ignore timestamps and always push"
    )

    # Retry options
    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="Maximum retry attempts (default: 3)"
    )

    parser.add_argument(
        "--retry-delay",
        type=int,
        default=2,
        help="Delay between retries in seconds (default: 2)"
    )

    # Logging options
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose logging"
    )

    parser.add_argument(
        "--log-file",
        help="Log to file"
    )

    parser.add_argument(
        "--output",
        help="Save results to JSON file"
    )

    return parser


def validate_args(args: argparse.Namespace) -> Tuple[bool, Optional[str]]:
    """Validate command line arguments."""
    # Must provide either product, --batch, or --list
    if not args.product and not args.batch and not args.list:
        return False, "Must provide product name, --batch file, or --list"

    # Can't provide both product and batch
    if args.product and args.batch:
        return False, "Cannot specify both product and --batch"

    # Max retries must be non-negative
    if args.max_retries < 0:
        return False, "--max-retries must be >= 0"

    # Retry delay must be positive
    if args.retry_delay <= 0:
        return False, "--retry-delay must be > 0"

    return True, None


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Validate arguments
    valid, error_msg = validate_args(args)
    if not valid:
        print(f"ERROR: {error_msg}", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    # Setup logging
    logger = setup_logging(verbose=args.verbose, log_file=args.log_file)

    # Check Supabase configuration
    if not supabase.service_role_key:
        logger.error("ERROR: SUPABASE_SERVICE_ROLE_KEY not configured")
        sys.exit(1)

    # Create sync config
    config = SyncConfig(
        mode=SyncMode[args.mode.upper()],
        scope=SyncScope[args.scope.upper()],
        dry_run=args.dry_run,
        force=args.force,
        max_retries=args.max_retries,
        retry_delay=args.retry_delay,
        verbose=args.verbose,
        log_file=args.log_file,
    )

    # Print header
    logger.info("=" * 80)
    logger.info("MASTER PIPELINE - Anuncio Agent Orchestration")
    logger.info("=" * 80)
    logger.info(f"Mode:        {config.mode.value}")
    logger.info(f"Scope:       {config.scope.value}")
    logger.info(f"Dry Run:     {config.dry_run}")
    logger.info(f"Force:       {config.force}")
    logger.info(f"Max Retries: {config.max_retries}")
    logger.info(f"Retry Delay: {config.retry_delay}s")

    results: List[SyncResult] = []
    summary: Dict = {}

    try:
        # Single product mode
        if args.product:
            result = process_single(args.product, config, logger)
            results = [result]
            print_result(result, verbose=args.verbose)

        # Batch mode
        elif args.batch:
            results, summary = process_batch(args.batch, config, logger)
            print_batch_summary(results, summary)

        # List mode
        elif args.list:
            logger.info("Listing available products (not yet implemented)")
            logger.info("Use: python fetch_product.py for fetching single products")

    except KeyboardInterrupt:
        logger.warning("\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")
        sys.exit(1)

    # Save results if requested
    if args.output and results:
        save_results(results, args.output, logger)

    # Exit with appropriate code
    failed_count = sum(1 for r in results if not r.success)
    if failed_count > 0:
        logger.warning(f"{failed_count} products failed")
        sys.exit(1)

    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()
