"""
Database Index Management for TAC-7

Creates and manages database indexes for optimal query performance.

Performance Impact:
- Without indexes: Full table scans (50-100ms on 10K rows)
- With indexes: Index lookups (<5ms on 10K rows)
- Expected improvement: 10-20x faster filtered queries
"""

import sqlite3
from typing import List, Dict, Any
from core.db_pool import get_db_connection


def create_products_indexes() -> None:
    """
    Create indexes for products table.

    Indexes created:
    - idx_products_is_active: For filtering active products
    - idx_products_category: For category filtering
    - idx_products_marketplace: For marketplace filtering
    - idx_products_category_active: Composite for category + active filters
    - idx_products_name: For name searches
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Single column indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_products_is_active
            ON products(is_active)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_products_category
            ON products(category)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_products_marketplace
            ON products(marketplace)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_products_name
            ON products(name)
        """)

        # Composite indexes for common query patterns
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_products_category_active
            ON products(category, is_active)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_products_marketplace_active
            ON products(marketplace, is_active)
        """)

        print("[+] Created products table indexes")


def create_repository_indexes() -> None:
    """
    Create indexes for repository scan tables (ml-knowledge-agent).

    Indexes for files table:
    - idx_files_llm_context: For context filtering
    - idx_files_keywords: For keyword searches
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Check if files table exists
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='files'
        """)

        if cursor.fetchone():
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_files_llm_context
                ON files(llm_context)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_files_keywords
                ON files(keywords)
            """)

            print("[+] Created repository scan indexes")


def create_processed_files_indexes() -> None:
    """
    Create indexes for processed_files table (ml-knowledge-agent).

    Indexes:
    - idx_processed_status: For status filtering
    - idx_processed_domain: For domain filtering
    - idx_processed_quality: For quality score filtering
    - idx_processed_status_domain: Composite for status + domain
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Check if processed_files table exists
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='processed_files'
        """)

        if cursor.fetchone():
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_processed_status
                ON processed_files(status)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_processed_domain
                ON processed_files(domain)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_processed_quality
                ON processed_files(quality_score)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_processed_status_domain
                ON processed_files(status, domain)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_processed_card_id
                ON processed_files(card_id)
            """)

            print("[+] Created processed_files indexes")


def create_all_indexes() -> None:
    """
    Create all recommended indexes for the database.

    Call this during application startup or after schema changes.
    """
    print("[*] Creating database indexes...")

    try:
        create_products_indexes()
    except Exception as e:
        print(f"[-] Error creating products indexes: {e}")

    try:
        create_repository_indexes()
    except Exception as e:
        print(f"[-] Error creating repository indexes: {e}")

    try:
        create_processed_files_indexes()
    except Exception as e:
        print(f"[-] Error creating processed_files indexes: {e}")

    print("[+] Index creation complete")


def analyze_table_indexes(table_name: str) -> List[Dict[str, Any]]:
    """
    Analyze indexes for a specific table.

    Args:
        table_name: Name of table to analyze

    Returns:
        List of index information dictionaries
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Get all indexes for table
        cursor.execute(f"""
            SELECT name, sql FROM sqlite_master
            WHERE type='index' AND tbl_name=?
        """, (table_name,))

        indexes = []
        for row in cursor.fetchall():
            indexes.append({
                "name": row[0],
                "sql": row[1]
            })

        return indexes


def get_index_usage_stats() -> List[Dict[str, Any]]:
    """
    Get statistics about index usage (requires SQLite 3.30+).

    Returns:
        List of index usage statistics

    Note: This uses PRAGMA statements that may not be available
    in older SQLite versions.
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """)

        tables = [row[0] for row in cursor.fetchall()]

        stats = []
        for table in tables:
            indexes = analyze_table_indexes(table)
            stats.append({
                "table": table,
                "index_count": len(indexes),
                "indexes": indexes
            })

        return stats


def optimize_database() -> None:
    """
    Run database optimization commands.

    - ANALYZE: Update statistics for query planner
    - VACUUM: Reclaim unused space and defragment
    - WAL checkpoint: Ensure WAL mode changes are written
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()

        print("[*] Running ANALYZE...")
        cursor.execute("ANALYZE")

        print("[*] Running VACUUM...")
        cursor.execute("VACUUM")

        print("[*] WAL checkpoint...")
        try:
            cursor.execute("PRAGMA wal_checkpoint(FULL)")
        except sqlite3.OperationalError:
            # WAL mode may not be enabled
            pass

        print("[+] Database optimization complete")


if __name__ == "__main__":
    # Run when executed directly
    print("TAC-7 Database Index Manager\n")

    create_all_indexes()
    print()

    print("Index Usage Statistics:")
    stats = get_index_usage_stats()
    for stat in stats:
        print(f"\nTable: {stat['table']}")
        print(f"  Indexes: {stat['index_count']}")
        for idx in stat['indexes']:
            print(f"    - {idx['name']}")

    print("\nRunning database optimization...")
    optimize_database()

    print("\n[+] All operations complete!")
