"""
Async File Processor for TAC-7

Non-blocking file processing to prevent event loop blocking.

Performance Impact:
- Before: 100MB CSV blocks event loop for 2-5 seconds
- After: Non-blocking async processing
- Expected improvement: Server remains responsive under load

This module wraps CPU-intensive pandas operations in ThreadPoolExecutor
to prevent blocking the FastAPI async event loop.
"""

import asyncio
import io
import json
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, List, Optional
import pandas as pd
from pathlib import Path

from core.db_pool import get_db_connection
from core.sql_security import validate_identifier


# Global thread pool for CPU-intensive operations
executor = ThreadPoolExecutor(max_workers=4)


async def convert_csv_to_sqlite_async(
    csv_content: bytes,
    table_name: str,
    db_path: str = "db/database.db"
) -> Dict[str, Any]:
    """
    Convert CSV to SQLite asynchronously.

    Wraps pandas CSV reading in executor to avoid blocking event loop.

    Args:
        csv_content: Raw CSV file content
        table_name: Name for the target table
        db_path: Path to SQLite database

    Returns:
        Dict with table_name, table_schema, row_count, sample_data

    Raises:
        ValueError: If CSV is invalid or table name is unsafe
    """
    # Validate table name for SQL injection prevention
    validate_identifier(table_name, "table")

    # Run CPU-intensive pandas operations in thread pool
    loop = asyncio.get_event_loop()

    def _process_csv():
        """Sync function to run in executor"""
        # Read CSV
        df = pd.read_csv(io.BytesIO(csv_content))

        # Normalize column names
        df.columns = [
            col.strip().lower().replace(' ', '_').replace('-', '_')
            for col in df.columns
        ]

        # Get schema and sample data before writing to DB
        schema = {col: str(dtype) for col, dtype in df.dtypes.items()}
        sample_data = df.head(5).to_dict('records')
        row_count = len(df)

        # Write to database
        with get_db_connection() as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)

        return schema, sample_data, row_count

    # Execute in thread pool
    schema, sample_data, row_count = await loop.run_in_executor(
        executor,
        _process_csv
    )

    return {
        "table_name": table_name,
        "table_schema": schema,
        "row_count": row_count,
        "sample_data": sample_data
    }


async def convert_json_to_sqlite_async(
    json_content: bytes,
    table_name: str,
    db_path: str = "db/database.db"
) -> Dict[str, Any]:
    """
    Convert JSON to SQLite asynchronously.

    Handles both JSON arrays and single objects.

    Args:
        json_content: Raw JSON file content
        table_name: Name for the target table
        db_path: Path to SQLite database

    Returns:
        Dict with table_name, table_schema, row_count, sample_data

    Raises:
        ValueError: If JSON is invalid or table name is unsafe
    """
    validate_identifier(table_name, "table")

    loop = asyncio.get_event_loop()

    def _process_json():
        """Sync function to run in executor"""
        # Parse JSON
        data = json.loads(json_content.decode('utf-8'))

        # Normalize to list
        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            raise ValueError("JSON must be an object or array")

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Normalize column names
        df.columns = [
            col.strip().lower().replace(' ', '_').replace('-', '_')
            for col in df.columns
        ]

        # Get schema and sample
        schema = {col: str(dtype) for col, dtype in df.dtypes.items()}
        sample_data = df.head(5).to_dict('records')
        row_count = len(df)

        # Write to database
        with get_db_connection() as conn:
            df.to_sql(table_name, conn, if_exists='replace', index=False)

        return schema, sample_data, row_count

    schema, sample_data, row_count = await loop.run_in_executor(
        executor,
        _process_json
    )

    return {
        "table_name": table_name,
        "table_schema": schema,
        "row_count": row_count,
        "sample_data": sample_data
    }


async def convert_jsonl_to_sqlite_async(
    jsonl_content: bytes,
    table_name: str,
    db_path: str = "db/database.db",
    chunk_size: int = 10000
) -> Dict[str, Any]:
    """
    Convert JSONL to SQLite asynchronously with chunked processing.

    Processes large JSONL files in chunks to limit memory usage.

    Args:
        jsonl_content: Raw JSONL file content
        table_name: Name for the target table
        db_path: Path to SQLite database
        chunk_size: Number of records per chunk (default: 10000)

    Returns:
        Dict with table_name, table_schema, row_count, sample_data

    Raises:
        ValueError: If JSONL is invalid or table name is unsafe
    """
    validate_identifier(table_name, "table")

    loop = asyncio.get_event_loop()

    def _process_jsonl():
        """Sync function to run in executor"""
        # First pass: discover all fields (streaming)
        buffer = io.BytesIO(jsonl_content)
        all_fields = set()

        for line in buffer:
            if line.strip():
                try:
                    obj = json.loads(line.decode('utf-8'))
                    all_fields.update(obj.keys())
                except json.JSONDecodeError:
                    continue

        # Normalize field names
        all_fields = {
            field.strip().lower().replace(' ', '_').replace('-', '_')
            for field in all_fields
        }

        # Second pass: insert in chunks
        buffer.seek(0)
        records_chunk = []
        total_rows = 0
        sample_data = []
        first_chunk = True

        with get_db_connection() as conn:
            for line in buffer:
                if line.strip():
                    try:
                        obj = json.loads(line.decode('utf-8'))

                        # Normalize keys
                        normalized = {
                            k.strip().lower().replace(' ', '_').replace('-', '_'): v
                            for k, v in obj.items()
                        }

                        # Ensure all fields present
                        record = {field: normalized.get(field) for field in all_fields}
                        records_chunk.append(record)

                        # Store sample from first chunk
                        if first_chunk and len(sample_data) < 5:
                            sample_data.append(record)

                        # Write chunk when full
                        if len(records_chunk) >= chunk_size:
                            df = pd.DataFrame(records_chunk)
                            if_exists = 'replace' if first_chunk else 'append'
                            df.to_sql(table_name, conn, if_exists=if_exists, index=False)

                            total_rows += len(records_chunk)
                            records_chunk = []
                            first_chunk = False

                    except json.JSONDecodeError:
                        continue

            # Write remaining records
            if records_chunk:
                df = pd.DataFrame(records_chunk)
                if_exists = 'replace' if first_chunk else 'append'
                df.to_sql(table_name, conn, if_exists=if_exists, index=False)
                total_rows += len(records_chunk)

        # Get schema from final DataFrame
        if records_chunk or total_rows > 0:
            # Re-read to get accurate schema
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                schema = {col[1]: col[2] for col in columns}
        else:
            schema = {field: "TEXT" for field in all_fields}

        return schema, sample_data, total_rows

    schema, sample_data, row_count = await loop.run_in_executor(
        executor,
        _process_jsonl
    )

    return {
        "table_name": table_name,
        "table_schema": schema,
        "row_count": row_count,
        "sample_data": sample_data
    }


async def process_file_upload_async(
    file_content: bytes,
    filename: str,
    table_name: str,
    db_path: str = "db/database.db"
) -> Dict[str, Any]:
    """
    Process uploaded file asynchronously based on file type.

    Routes to appropriate async processor based on file extension.

    Args:
        file_content: Raw file content
        filename: Original filename (for extension detection)
        table_name: Name for the target table
        db_path: Path to SQLite database

    Returns:
        Dict with processing results

    Raises:
        ValueError: If file type is unsupported
    """
    file_ext = Path(filename).suffix.lower()

    if file_ext == '.csv':
        return await convert_csv_to_sqlite_async(file_content, table_name, db_path)
    elif file_ext == '.json':
        return await convert_json_to_sqlite_async(file_content, table_name, db_path)
    elif file_ext == '.jsonl':
        return await convert_jsonl_to_sqlite_async(file_content, table_name, db_path)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")


def shutdown_executor():
    """
    Shutdown the thread pool executor.

    Call this during application shutdown.
    """
    executor.shutdown(wait=True)
