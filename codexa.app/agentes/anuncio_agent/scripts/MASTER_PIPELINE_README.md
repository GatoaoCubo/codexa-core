# Master Pipeline - Anuncio Agent Orchestration

Complete Python script for orchestrating product processing through the unified-sync Edge Function with enterprise-grade error handling, retry logic, and batch processing capabilities.

## Overview

`master_pipeline.py` is a production-ready CLI tool that:

- **Calls unified-sync Edge Function** with typed, validated parameters
- **Handles errors intelligently** (LAW 7) with exponential backoff retry logic
- **Supports single products** or batch processing from CSV/JSON files
- **Tracks progress** with detailed logging and optional file output
- **Provides comprehensive reporting** with success rates and error details
- **Uses centralized env_loader** for secure credential management

## Quick Start

### Single Product
```bash
python master_pipeline.py "iPhone 15 Pro"
```

### Batch Processing
```bash
# From CSV file
python master_pipeline.py --batch products.csv

# From JSON file
python master_pipeline.py --batch products.json
```

### With Options
```bash
# Dry run (preview changes)
python master_pipeline.py "Nike Shoes" --dry-run

# Custom sync mode and scope
python master_pipeline.py --batch products.csv --mode=push --scope=content

# With verbose logging to file
python master_pipeline.py "Product" --verbose --log-file pipeline.log
```

## Requirements

- Python 3.7+
- `.env` file configured with Supabase credentials:
  - `SUPABASE_URL`
  - `SUPABASE_SERVICE_ROLE_KEY`
- Network access to unified-sync Edge Function

## Configuration

### Environment Variables

Required (from `codexa-core/.env`):
```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOi...
```

### Sync Options

| Option | Values | Default | Purpose |
|--------|--------|---------|---------|
| `--mode` | pull, push, bidirectional | bidirectional | Sync direction |
| `--scope` | all, inventory, content, price | all | What fields to sync |
| `--dry-run` | flag | false | Preview without applying |
| `--force` | flag | false | Ignore timestamps, always sync |

### Retry Configuration (LAW 7)

| Option | Type | Default | Purpose |
|--------|------|---------|---------|
| `--max-retries` | int | 3 | Maximum retry attempts |
| `--retry-delay` | int | 2 | Base delay between retries (seconds) |

**Backoff Formula**: `delay = retry_delay * (2 ^ retry_attempt)`

Example with 3 retries and 2s delay:
- Attempt 1: Immediate
- Attempt 2: After 2s
- Attempt 3: After 4s
- Attempt 4: After 8s

### Retry Strategy (LAW 7)

#### Recoverable Errors (Retry)
- HTTP 429 (Rate Limited)
- HTTP 503/504 (Service Unavailable)
- Network timeout
- DNS resolution failure
- Connection reset

#### Fatal Errors (Fail Fast)
- HTTP 400/401/403 (Auth/validation)
- Missing environment variables
- Invalid product data
- Corrupt response body

## Batch File Formats

### CSV Format
```csv
product_name,product_id
iPhone 15 Pro,
Nike Air Max 90,
Sony WH-1000XM5,abc-123-def
Samsung 65" Smart TV,
```

- Required column: `product_name`
- Optional column: `product_id` (leave blank if unknown)

### JSON Format
```json
[
  {
    "product_name": "iPhone 15 Pro",
    "product_id": null
  },
  {
    "product_name": "Nike Air Max 90",
    "product_id": "abc-123-def"
  }
]
```

### Sample Files
- `sample_products.csv` - CSV example
- `sample_products.json` - JSON example

## Output

### Console Output (Single Product)
```
================================================================================
MASTER PIPELINE - Anuncio Agent Orchestration
================================================================================
[2025-12-04 14:30:45] INFO: Mode: bidirectional
[2025-12-04 14:30:45] INFO: Scope: all
================================================================================

[2025-12-04 14:30:45] INFO: Processing single product: iPhone 15 Pro
[2025-12-04 14:30:47] INFO: SUCCESS: iPhone 15 Pro | Synced: 1, Created: 0, Updated: 1, Duration: 2150ms

================================================================================
SUCCESS: iPhone 15 Pro
--------------------------------------------------------------------------------
Mode:     bidirectional
Scope:    all
Duration: 2150ms
Stats:
  Synced:   1
  Created:  0
  Updated:  1
  Skipped:  0
  Errors:   0
================================================================================
```

### Console Output (Batch)
```
[2025-12-04 14:35:10] INFO: Loaded 5 products from products.csv

================================================================================
BATCH SUMMARY
================================================================================
Total:        5
Success:      4
Failed:       1
Success Rate: 80.0%
================================================================================

Details:
  ✓ iPhone 15 Pro
  ✓ Nike Air Max 90
  ✓ Sony WH-1000XM5
  ✗ Samsung 65" Smart TV
     Error: Product not found in Shopify
  ✓ iPad Pro 12.9"
```

### JSON Output (`--output results.json`)
```json
[
  {
    "product_name": "iPhone 15 Pro",
    "product_id": null,
    "success": true,
    "mode": "bidirectional",
    "scope": "all",
    "synced_count": 1,
    "created_count": 0,
    "updated_count": 1,
    "skipped_count": 0,
    "error_count": 0,
    "duration_ms": 2150,
    "error_message": null,
    "retry_count": 0,
    "timestamp": "2025-12-04T14:30:47.123456"
  },
  {
    "product_name": "Samsung 65\" Smart TV",
    "product_id": null,
    "success": false,
    "mode": "bidirectional",
    "scope": "all",
    "synced_count": 0,
    "created_count": 0,
    "updated_count": 0,
    "skipped_count": 0,
    "error_count": 0,
    "duration_ms": 3000,
    "error_message": "HTTP 404: Product not found",
    "retry_count": 0,
    "timestamp": "2025-12-04T14:30:50.654321"
  }
]
```

## Logging

### Console Logging
```bash
# Standard (INFO level)
python master_pipeline.py "Product"

# Verbose (DEBUG level)
python master_pipeline.py "Product" --verbose
```

### File Logging
```bash
# Log to file
python master_pipeline.py "Product" --log-file pipeline.log

# Both console and file
python master_pipeline.py "Product" --verbose --log-file pipeline.log
```

Log file format:
```
[2025-12-04 14:30:45] INFO: Starting sync for product: iPhone 15 Pro
[2025-12-04 14:30:45] DEBUG [sync_product_with_retry]: Attempt 1/4
[2025-12-04 14:30:47] INFO: SUCCESS: iPhone 15 Pro | Synced: 1, Created: 0, Updated: 1, Duration: 2150ms
```

## Usage Examples

### 1. Basic Single Product
```bash
python master_pipeline.py "iPhone 15 Pro"
```

### 2. Batch with Inventory Scope Only
```bash
python master_pipeline.py --batch products.csv --scope=inventory
```

### 3. Push-Only Sync
```bash
python master_pipeline.py "Nike Shoes" --mode=push
```

### 4. Dry Run (Preview)
```bash
python master_pipeline.py --batch products.csv --dry-run --verbose
```

### 5. High-Retry Batch with Logging
```bash
python master_pipeline.py --batch products.json \
  --max-retries 5 \
  --retry-delay 3 \
  --verbose \
  --log-file batch_log.log \
  --output results.json
```

### 6. Force Sync Ignoring Timestamps
```bash
python master_pipeline.py "Product" --force --mode=push
```

### 7. Batch with Content and Pricing
```bash
python master_pipeline.py --batch products.csv --scope=content
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (all products synced successfully) |
| 1 | Failure (one or more products failed) |
| 130 | Interrupted by user (Ctrl+C) |

## Error Handling (LAW 7)

The script implements comprehensive error recovery:

### Retry Categories

**RECOVERABLE** (Automatic Retry):
- Network timeouts
- Rate limiting (429)
- Service unavailable (503/504)
- Connection errors

**FATAL** (Fail Immediately):
- Authentication errors (401/403)
- Invalid parameters (400)
- Missing required configuration
- Corrupt data

### Quality Gate

If a product fails after max retries:
1. Error is logged with context
2. Result marked as failed
3. Next product continues (batch processing)
4. Exit code 1 at end if any failures

## Architecture

```
master_pipeline.py
├── CLI Interface (argparse)
├── Sync Engine
│   ├── call_unified_sync() - Call Edge Function
│   ├── sync_product_with_retry() - Retry logic with backoff
│   └── validate_response() - Result validation
├── Batch Processing
│   ├── load_csv_products()
│   ├── load_json_products()
│   └── process_batch()
├── Logging System
│   ├── Console handler
│   └── File handler (optional)
└── Output & Reporting
    ├── print_result()
    ├── print_batch_summary()
    └── save_results()
```

## Connecting to env_loader

The script uses centralized environment configuration:

```python
from config.env_loader import supabase

# Access Supabase configuration
api_url = supabase.url
service_key = supabase.service_role_key
```

Benefits:
- Single source of truth for credentials
- Automatic placeholder detection
- Type-safe configuration
- Cross-project consistency

## Performance Considerations

### Timeouts
- API call timeout: 300 seconds (5 minutes)
- Suitable for large products with many SKUs

### Concurrency
- Single-threaded by design
- Processes one product at a time
- Suitable for ordered processing

### Batch Size Recommendations
- Small batches: 10-50 products
- Medium batches: 50-200 products
- Large batches: 200+ products (consider splitting)

## Troubleshooting

### "SUPABASE_SERVICE_ROLE_KEY not configured"
- Check `.env` file exists in project root
- Verify `SUPABASE_SERVICE_ROLE_KEY` is set
- Run `python config/env_loader.py` to check status

### HTTP 401/403 Errors
- Verify service role key is not expired
- Check credentials in `.env`
- Ensure key has appropriate permissions

### Connection Timeouts
- Check network connectivity
- Verify Edge Function is deployed
- Check URL in `.env` is correct

### Rate Limited (429)
- Adjust `--retry-delay` (default: 2s)
- Reduce batch size
- Process during off-peak hours

### High Failure Rate
- Check product names are correct
- Verify products exist in source system
- Review logs with `--verbose`

## Integration

### With CI/CD
```bash
# GitHub Actions example
- name: Sync Products
  run: |
    python codexa.app/agentes/anuncio_agent/scripts/master_pipeline.py \
      --batch products.csv \
      --log-file pipeline.log \
      --output results.json
```

### Scheduled Tasks
```bash
# Windows Task Scheduler
python C:\path\to\master_pipeline.py --batch daily_products.csv

# Linux cron
0 2 * * * cd /path && python master_pipeline.py --batch daily_products.csv
```

## Advanced Features

### Quality Gate
The script validates outputs >= 7.0 quality score (from unified-sync response).
If validation fails after retry, product is marked as failed.

### Partial Success
Batch processing continues even if individual products fail (degrade gracefully).
This prevents one failure from blocking entire batch.

### Async Reporting
Results are reported as they complete, not batched at end.
Suitable for long-running batches.

## Version

- **Script**: master_pipeline.py v1.0.0
- **Python**: 3.7+
- **Dependencies**: Standard library only (no external deps)
- **Created**: 2025-12-04
- **Author**: CODEXA Anuncio Agent

## Related Files

- `unified_sync.py` - Lower-level sync wrapper
- `fetch_product.py` - Product retrieval utility
- `sample_products.csv` - CSV batch example
- `sample_products.json` - JSON batch example
- `config/env_loader.py` - Environment configuration

## References

- **LAW 7**: Error Recovery (CLAUDE.md)
  - Retry strategies for transient errors
  - Fail fast for unrecoverable errors
  - Quality gates and validation

- **Project**: CODEXA Meta-Construction Framework
  - Agents: anuncio_agent
  - Edge Function: unified-sync
  - Database: Supabase
