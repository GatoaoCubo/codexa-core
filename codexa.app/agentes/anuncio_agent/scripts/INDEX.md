# Master Pipeline - File Index

Quick reference guide to all files created for the Master Pipeline orchestration system.

## Created Files

### 1. Main Script
**File**: `master_pipeline.py` (25KB, 804 lines)
- Complete Python CLI for pipeline orchestration
- Single product and batch processing
- Error recovery with retry logic (LAW 7)
- Progress tracking and comprehensive logging
- JSON export capabilities

**Quick Start**:
```bash
python master_pipeline.py "Product Name"
python master_pipeline.py --batch products.csv --verbose
```

**Key Features**:
- Calls unified-sync Edge Function
- Exponential backoff retry logic
- CSV/JSON batch support
- Configurable timeouts and retries
- Real-time progress tracking
- File logging support

---

### 2. Documentation Files

#### `MASTER_PIPELINE_README.md` (12KB)
**Purpose**: Comprehensive user guide and API reference
**Contains**:
- Quick start guide
- Configuration options
- Batch file formats (CSV/JSON)
- Usage examples (7+)
- Exit codes and error handling
- Troubleshooting guide
- Integration examples (CI/CD, cron)
- Performance recommendations

**Best For**: Users implementing the script in production

#### `IMPLEMENTATION_SUMMARY.md` (12KB)
**Purpose**: Technical implementation details
**Contains**:
- Feature checklist (all completed)
- Code metrics and quality
- LAW 7 compliance verification
- Integration points
- Performance characteristics
- Known limitations
- Future enhancement ideas
- Support information

**Best For**: Developers maintaining the script

#### `INDEX.md` (this file)
**Purpose**: Quick reference navigation
**Contains**: File listing and quick lookup

---

### 3. Sample Batch Files

#### `sample_products.csv` (111 bytes)
**Format**: CSV with headers
**Columns**:
- `product_name` (required)
- `product_id` (optional)

**Usage**:
```bash
python master_pipeline.py --batch sample_products.csv
```

**Contents**: 5 example products

#### `sample_products.json` (362 bytes)
**Format**: JSON array of objects
**Schema**:
```json
{
  "product_name": "string",
  "product_id": "string or null"
}
```

**Usage**:
```bash
python master_pipeline.py --batch sample_products.json
```

**Contents**: 5 example products (same as CSV)

---

## Quick Command Reference

### Basic Usage
```bash
# Single product
python master_pipeline.py "iPhone 15 Pro"

# Batch processing
python master_pipeline.py --batch products.csv

# Get help
python master_pipeline.py --help
```

### Common Options
```bash
# Dry run (preview)
--dry-run

# Custom sync mode
--mode=pull|push|bidirectional

# Custom scope
--scope=all|inventory|content|price

# Verbose logging
--verbose

# Log to file
--log-file pipeline.log

# Export results
--output results.json

# High retry
--max-retries 5 --retry-delay 3
```

### Complete Examples
```bash
# Batch with all options
python master_pipeline.py --batch products.csv \
  --mode=push \
  --scope=content \
  --max-retries 5 \
  --verbose \
  --log-file run.log \
  --output results.json

# Dry run preview
python master_pipeline.py "Product" --dry-run --verbose

# Force sync
python master_pipeline.py "Product" --force --mode=push
```

---

## File Organization

```
codexa.app/agentes/anuncio_agent/scripts/
│
├── CORE SCRIPT
│   └── master_pipeline.py                 ← Main orchestrator (NEW)
│
├── DOCUMENTATION
│   ├── MASTER_PIPELINE_README.md          ← User guide (NEW)
│   ├── IMPLEMENTATION_SUMMARY.md          ← Technical details (NEW)
│   └── INDEX.md                           ← This file (NEW)
│
├── EXAMPLES
│   ├── sample_products.csv                ← CSV example (NEW)
│   └── sample_products.json               ← JSON example (NEW)
│
├── SUPPORTING SCRIPTS (existing)
│   ├── unified_sync.py                    ← Low-level wrapper
│   ├── fetch_product.py                   ← Product retrieval
│   ├── list_products.py
│   ├── auto_publish_anuncios.py
│   └── ... (others)
│
└── DATA FILES (existing)
    └── products_cache.json
```

---

## Getting Started

### 1. Review Documentation
Start here based on your role:

| Role | Start With |
|------|-----------|
| **User** | `MASTER_PIPELINE_README.md` |
| **Developer** | `IMPLEMENTATION_SUMMARY.md` |
| **Quick Check** | This file (INDEX.md) |

### 2. Setup Environment
```bash
# Verify .env configuration
python config/env_loader.py

# Check env_loader status
# Should show: [OK] Supabase configured
```

### 3. Create Batch File
Use `sample_products.csv` or `sample_products.json` as template

### 4. Test Script
```bash
# Syntax check
python -m py_compile master_pipeline.py

# Help system
python master_pipeline.py --help

# Single product test
python master_pipeline.py "Test Product" --dry-run --verbose
```

### 5. Run Production
```bash
# Single
python master_pipeline.py "Product Name"

# Batch
python master_pipeline.py --batch products.csv --verbose
```

---

## Integration Quick Links

### Environment Configuration
**File**: `codexa.app/config/env_loader.py`

```python
from config.env_loader import supabase

# Credentials loaded from .env
supabase.url
supabase.service_role_key
```

### Unified-Sync Edge Function
**Endpoint**: `{SUPABASE_URL}/functions/v1/unified-sync`
**Method**: POST
**Auth**: Bearer {SUPABASE_SERVICE_ROLE_KEY}

### Support Files
- `unified_sync.py` - Lower-level direct wrapper
- `fetch_product.py` - Individual product fetching
- `sample_products.csv/json` - Batch format examples

---

## Features at a Glance

### CLI Interface
- ✅ Single product mode: `python master_pipeline.py "Name"`
- ✅ Batch mode: `python master_pipeline.py --batch file.csv`
- ✅ Argument validation with helpful errors
- ✅ Help system: `-h` or `--help`

### Sync Capabilities
- ✅ Pull (Shopify → Supabase)
- ✅ Push (Supabase → Shopify)
- ✅ Bidirectional (smart sync)
- ✅ All/inventory/content/price scopes

### Error Recovery (LAW 7)
- ✅ Exponential backoff retry
- ✅ Recoverable vs fatal error detection
- ✅ Max retry configuration
- ✅ Quality gate validation

### Batch Processing
- ✅ CSV support
- ✅ JSON support
- ✅ Optional product IDs
- ✅ Continue on errors

### Progress Tracking
- ✅ Real-time console logging
- ✅ Optional file logging
- ✅ Debug mode (verbose)
- ✅ Batch progress counter

### Output & Reporting
- ✅ Pretty console output
- ✅ JSON export
- ✅ Success statistics
- ✅ Error details

---

## Troubleshooting Quick Links

### "SUPABASE_SERVICE_ROLE_KEY not configured"
→ Check `MASTER_PIPELINE_README.md` → Troubleshooting

### "Product not found" errors
→ Check `MASTER_PIPELINE_README.md` → Troubleshooting

### Connection timeout issues
→ Check `MASTER_PIPELINE_README.md` → Troubleshooting

### High failure rates
→ Check `MASTER_PIPELINE_README.md` → Troubleshooting

### Need detailed error logs
→ Use: `--verbose --log-file run.log`

---

## Version Information

| Component | Version | Date |
|-----------|---------|------|
| master_pipeline.py | 1.0.0 | 2025-12-04 |
| Python | 3.7+ | Required |
| Dependencies | Standard library | No externals |

---

## Related Documentation

- **CLAUDE.md** (Project Laws)
  - LAW 7: Error Recovery
  - LAW 4: Agentic Design

- **codexa.app/config/env_loader.py**
  - Environment configuration
  - Supabase integration

- **Unified-Sync Edge Function**
  - Endpoint: `/functions/v1/unified-sync`
  - Handles Shopify ↔ Supabase sync

---

## Next Steps

### For First-Time Users
1. Read `MASTER_PIPELINE_README.md` (Quick Start section)
2. Review `sample_products.csv` format
3. Run: `python master_pipeline.py --help`
4. Test with dry-run: `python master_pipeline.py "Test" --dry-run`

### For Integration
1. Check `MASTER_PIPELINE_README.md` → Integration section
2. Set up environment variables in `.env`
3. Create batch file (CSV or JSON)
4. Integrate with CI/CD or cron scheduler

### For Troubleshooting
1. Check `MASTER_PIPELINE_README.md` → Troubleshooting
2. Run with `--verbose` flag
3. Check log file with `--log-file`
4. Review `IMPLEMENTATION_SUMMARY.md` → Known Limitations

---

**Created**: 2025-12-04
**Status**: Production Ready
**Maintained by**: CODEXA Anuncio Agent
