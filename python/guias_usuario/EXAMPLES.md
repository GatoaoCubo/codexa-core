# CODEXA Usage Examples

**Version**: 1.0.0
**Last Updated**: 2025-11-11

---

## Quick Start

### Installation

```bash
cd codexa/
pip install -r requirements.txt
```

### Verify Installation

```bash
python cli.py status
```

**Expected Output**:
```
🤖 CODEXA System Status
───────────────────────────────────
Working Directory    | C:\Users\...\tac-7\codexa
Modules Registered   | 6
README Exists        | ✅
Git Repository       | ✅
Git Branch           | main

Registered Modules:
  • crud
  • scout
  • product_manager
  • strategy_mentor
  • competitor_scout
  • knowledge_base
```

---

## Example 1: Documentation Management (CRUD)

### Scenario
Create and manage project documentation with automatic git commits.

### Commands

```bash
# Create a new documentation file
python cli.py crud create docs/getting-started.md \
  --content "# Getting Started\n\nWelcome to CODEXA!" \
  --type document

# Read the documentation
python cli.py crud read docs/getting-started.md --type document

# Update the documentation
python cli.py crud update docs/getting-started.md \
  --content "# Getting Started\n\n## Installation\n..." \
  --type document

# List all documentation
python cli.py crud list --type document --pattern "docs/*.md"

# Search documentation
python cli.py crud search --keyword "getting" --type document
```

### Expected Behavior

- ✅ Files created with automatic backup
- ✅ Git auto-commit: `docs: create getting-started.md`
- ✅ Backup saved to `.codexa_backups/`
- ✅ Safe overwrite protection for critical files

---

## Example 2: Repository Organization (Scout)

### Scenario
Scan a repository, understand its structure, and find files efficiently.

### Commands

```bash
# Scan repository (creates .scout_cache.json)
python cli.py scout scan --target . --cache

# Find all Python files
python cli.py scout find --extension py

# Find files matching pattern
python cli.py scout find --pattern "test_*.py"

# Get repository statistics
python cli.py scout stats

# Query organization
python cli.py scout query "Where should I put API endpoint tests?"
```

### Expected Output (scout stats)

```
Repository Statistics
─────────────────────
Files: 150
Directories: 25
Annotations: 12
```

### Use Case: Onboarding New Developers

```bash
# New developer explores codebase
python cli.py scout scan --target ../tac-7

# Find all agent implementations
python cli.py scout find --pattern "adws/*agent*.py"

# Understand where to add new code
python cli.py scout query "Where should I add a new e-commerce agent?"
```

---

## Example 3: Product Catalog Management

### Scenario
Manage an e-commerce product catalog with full CRUD operations.

### Commands

```bash
# Create a new product
python cli.py ecom products create \
  --name "Smartwatch Pro X" \
  --description "Advanced fitness tracker with GPS" \
  --price 299.99 \
  --category "Electronics" \
  --keywords '["smartwatch", "fitness", "GPS"]'

# Read product
python cli.py ecom products read <product_id>

# Update product price
python cli.py ecom products update <product_id> \
  --price 279.99

# List all products
python cli.py ecom products list

# List products by category
python cli.py ecom products list --category "Electronics"

# Search products
python cli.py ecom products search --keyword "smart"
```

### Bulk Operations

```bash
# Export all products to JSON
python cli.py ecom products bulk-export --output products_backup.json

# Import products from JSON
python cli.py ecom products bulk-import --file products_new.json
```

---

## Example 4: Strategic Planning & KPIs

### Scenario
Create a strategic plan for Q4 sales growth and track KPIs.

### Step 1: Create Strategic Plan

```bash
python cli.py ecom strategy create-plan \
  --title "Q4 2025 Sales Growth" \
  --objective "Increase monthly revenue by 30% through product line expansion" \
  --kpis '[
    {"name": "Revenue", "target": 150000, "unit": "BRL"},
    {"name": "New Products", "target": 10, "unit": "items"},
    {"name": "Customer Acquisition", "target": 500, "unit": "customers"}
  ]' \
  --priority high
```

### Step 2: Track Progress

```bash
# List all strategic plans
python cli.py ecom strategy list-plans

# Read specific plan
python cli.py ecom strategy read-plan plan-20251111133000

# Update KPI progress
python cli.py ecom strategy update-kpi \
  plan-20251111133000 \
  "Revenue" \
  95000

# Check overall achievement
python cli.py ecom strategy read-plan plan-20251111133000
```

### Expected Output

```json
{
  "success": true,
  "plan_id": "plan-20251111133000",
  "plan": {
    "title": "Q4 2025 Sales Growth",
    "status": "active",
    "kpis": [
      {
        "name": "Revenue",
        "target": 150000,
        "current": 95000,
        "unit": "BRL",
        "achievement": 63.3
      },
      ...
    ]
  },
  "overall_achievement": 45.8
}
```

---

## Example 5: Competitor Analysis

### Scenario
Track competitor products and compare pricing/features.

### Commands

```bash
# Add competitor product
python cli.py ecom competitor add \
  --name "SmartWatch Elite" \
  --competitor-name "Competitor X" \
  --price 249.99 \
  --url "https://competitor.com/product/elite" \
  --features '["GPS", "Heart Rate", "5-day battery"]'

# List all competitors
python cli.py ecom competitor list

# Compare our product with competitor
python cli.py ecom competitor compare \
  our-product-123 \
  comp-20251111133000
```

### Use Case: Pricing Strategy

```bash
# Analyze competitor pricing
python cli.py ecom competitor list | grep price

# Update our pricing based on analysis
python cli.py ecom products update our-product-123 --price 269.99
```

---

## Example 6: Knowledge Base Management

### Scenario
Organize internal documentation and best practices.

### Commands

```bash
# Add knowledge entry
python cli.py ecom knowledge add \
  --title "Product Description Best Practices" \
  --content "1. Focus on benefits not features...\n2. Use action words..." \
  --category "guidelines" \
  --tags '["copywriting", "products", "seo"]'

# Search knowledge base
python cli.py ecom knowledge search --keyword "product description"

# List all entries by category
python cli.py ecom knowledge list --category "guidelines"
```

### Use Case: Onboarding Documentation

```bash
# Create onboarding guide
python cli.py ecom knowledge add \
  --title "New Product Manager Onboarding" \
  --content "Welcome! This guide covers..." \
  --category "onboarding" \
  --tags '["training", "getting-started"]'

# Team member searches for info
python cli.py ecom knowledge search --keyword "onboarding"
```

---

## Example 7: Self-Updating README

### Scenario
Keep README documentation synchronized with actual system capabilities.

### Commands

```bash
# Update README with current system introspection
python cli.py readme update

# Verify README content
cat README.md
```

### Expected Behavior

1. **Introspection**: System scans all registered modules
2. **Generation**: Creates comprehensive README with:
   - Module descriptions
   - Available operations
   - Usage examples
   - System statistics
3. **Auto-commit**: Git commit: `docs: auto-update README with new capabilities`

### When to Use

- After adding new modules
- After updating operation descriptions
- Before sharing project with team
- As part of CI/CD pipeline

---

## Example 8: Complete E-commerce Workflow

### Scenario
Launch a new product line with full strategic planning.

### Step 1: Create Products

```bash
# Create product 1
python cli.py ecom products create \
  --name "Smartwatch Pro" \
  --price 299.99 \
  --category "Wearables"

# Create product 2
python cli.py ecom products create \
  --name "Smartwatch Elite" \
  --price 449.99 \
  --category "Wearables"
```

### Step 2: Analyze Competitors

```bash
# Add competitor data
python cli.py ecom competitor add \
  --name "FitBand X" \
  --competitor-name "Competitor A" \
  --price 279.99
```

### Step 3: Create Strategic Plan

```bash
python cli.py ecom strategy create-plan \
  --title "Wearables Launch 2025" \
  --objective "Establish market presence in wearables segment" \
  --kpis '[
    {"name": "Units Sold", "target": 1000, "unit": "units"},
    {"name": "Revenue", "target": 350000, "unit": "BRL"},
    {"name": "Market Share", "target": 5, "unit": "%"}
  ]'
```

### Step 4: Document Knowledge

```bash
python cli.py ecom knowledge add \
  --title "Wearables Product Guidelines" \
  --content "Key features to highlight: battery life, accuracy, design..." \
  --category "product-guidelines"
```

### Step 5: Track Progress

```bash
# Weekly KPI update
python cli.py ecom strategy update-kpi <plan_id> "Units Sold" 250

# Check overall progress
python cli.py ecom strategy read-plan <plan_id>
```

---

## Example 9: Scripting & Automation

### Python Script Integration

```python
#!/usr/bin/env python3
"""
Automated product sync script
"""

import subprocess
import json

def create_product(name, price, category):
    """Create product via CLI."""
    result = subprocess.run([
        "python", "cli.py", "ecom", "products", "create",
        "--name", name,
        "--price", str(price),
        "--category", category
    ], capture_output=True, text=True)

    return "success" in result.stdout

# Batch product creation
products = [
    ("Watch A", 199.99, "Wearables"),
    ("Watch B", 299.99, "Wearables"),
    ("Watch C", 399.99, "Wearables"),
]

for name, price, category in products:
    if create_product(name, price, category):
        print(f"✅ Created: {name}")
    else:
        print(f"❌ Failed: {name}")
```

### Bash Automation

```bash
#!/bin/bash
# Daily repository health check

echo "🔍 Running daily health check..."

# Scan repository
python cli.py scout scan --cache

# Get stats
python cli.py scout stats

# Update README
python cli.py readme update

echo "✅ Health check complete!"
```

---

## Example 10: CI/CD Integration

### GitHub Actions Workflow

```yaml
name: CODEXA Documentation Update

on:
  push:
    paths:
      - 'codexa/**/*.py'

jobs:
  update-readme:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          cd codexa
          pip install -r requirements.txt

      - name: Update README
        run: |
          cd codexa
          python cli.py readme update

      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add codexa/README.md
          git commit -m "docs: auto-update README [skip ci]" || echo "No changes"
          git push
```

---

## Troubleshooting Common Issues

### Issue: ModuleNotFoundError

```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### Issue: Permission Denied

```bash
# Solution: Adjust file permissions
chmod +x cli.py
```

### Issue: Unicode Errors (Windows)

```bash
# Solution: Set encoding
set PYTHONIOENCODING=utf-8
python cli.py status
```

---

## Best Practices

### 1. Use Version Control

```bash
# Always work in git repository
git init
git add .
git commit -m "Initial CODEXA setup"

# Let CODEXA auto-commit changes
python cli.py crud create doc.md --content "..."
# Auto-creates commit: "docs: create doc.md"
```

### 2. Regular README Updates

```bash
# After adding modules/changing operations
python cli.py readme update
```

### 3. Use Scout Cache

```bash
# First scan (slow, builds cache)
python cli.py scout scan --cache

# Subsequent scans (fast, uses cache)
python cli.py scout find --pattern "*.py"
```

### 4. Backup Important Data

```bash
# Export products before major changes
python cli.py ecom products bulk-export --output backup.json

# Backups are automatic, but explicit exports are safer
```

---

## Advanced Usage

### Custom Module Development

See `hop_orchestrator.py` for `BaseModule` interface.

```python
from hop_orchestrator import BaseModule

class MyCustomModule(BaseModule):
    def __init__(self):
        super().__init__(
            name="my_module",
            description="My custom functionality"
        )
        self._register_operations()

    # Implement required methods...
```

### Direct Python API

```python
from hop_orchestrator import get_orchestrator

# Initialize
orchestrator = get_orchestrator("./codexa")

# Execute operations
result = orchestrator.route_operation(
    "crud",
    "create",
    path="test.md",
    content="# Test"
)

print(result)
```

---

## Next Steps

1. **Explore the CLI**: `python cli.py --help`
2. **Read the README**: `cat README.md`
3. **Check system status**: `python cli.py status`
4. **Try examples**: Start with Example 1 (Documentation Management)
5. **Read MIGRATION.md**: Understand consolidation decisions

---

**Happy CODEXAing!** 🚀

Generated by CODEXA HOP-001 Meta-Agent
Part of TAC-7 (Tactical Agentic Commerce) Project
