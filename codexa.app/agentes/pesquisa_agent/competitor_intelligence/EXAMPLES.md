# Competitor Intelligence - Usage Examples

Real-world examples of how to use the system effectively.

---

## Example 1: Monitor Competitor Pricing Changes

**Scenario**: You want to track if any AI course platforms change their pricing.

### Step 1: Check Current Pricing

```bash
# View all current prices
jq '.platforms | to_entries[] | {
  name: .value.name,
  price: .value.metrics.price_brl,
  tier: .value.tier
}' sources/ai_courses_platforms.json
```

**Output**:
```json
{
  "name": "Sebrae - IA na Prática",
  "price": 0,
  "tier": "free"
}
{
  "name": "RD University (TOTVS)",
  "price": 1997,
  "tier": "paid"
}
{
  "name": "G4 Educação",
  "price": 2997,
  "tier": "premium"
}
...
```

### Step 2: Set Up Daily Monitoring

```bash
# Run daily check
./scripts/monitor_changes.sh --daily
```

### Step 3: Review Changes

```bash
# Check today's report
cat snapshots/$(date +%Y-%m-%d)/change_report_*.md
```

### Step 4: Update Prices if Changed

If you detect a change:
1. Edit `sources/ai_courses_platforms.json`
2. Update the `price_brl` field
3. Add note in `monitoring` section
4. Re-run fetch to document the change

---

## Example 2: Track New AI Tools from Marketplaces

**Scenario**: Monitor when marketplaces launch new AI-powered features.

### Step 1: List Current AI Tools Being Tracked

```bash
# Check TikTok Shop AI tools
jq '.marketplaces.tiktok_shop.key_topics' sources/marketplaces_docs.json
```

**Output**:
```json
[
  "gmv_max",
  "search_ads",
  "creative_ai",
  "live_commerce",
  "social_commerce",
  "seller_education",
  "tiktok_world_brasil"
]
```

### Step 2: Fetch Latest Documentation

```bash
/update_competitor_docs --category marketplaces_docs --priority high
```

### Step 3: Review for New Features

```bash
# Read latest TikTok Shop documentation
cat docs/marketplaces_docs/tiktok_shop/latest.md

# Check for mentions of new AI tools
grep -i "ai\|artificial intelligence\|automation" docs/marketplaces_docs/tiktok_shop/latest.md
```

### Step 4: Update Tracking if Needed

If you find a new AI tool:
1. Add to `key_topics` in `sources/marketplaces_docs.json`
2. Update monitoring parameters
3. Document in competitive analysis

---

## Example 3: Compliance Alert - New LGPD Regulation

**Scenario**: Check for new data protection regulations affecting AI course content.

### Step 1: Monitor Compliance Sources

```bash
# Fetch latest LGPD documentation
/update_competitor_docs --category compliance_sources
```

### Step 2: Check ANPD Updates

```bash
# Read latest ANPD documentation
cat docs/compliance_sources/anpd/latest.md

# Search for AI-specific guidance
grep -i "inteligência artificial\|ia generativa\|ai" docs/compliance_sources/anpd/latest.md
```

### Step 3: Cross-Reference with Course Content

```bash
# Check implications for AI courses
jq '.data_protection.lgpd_official.implications_for_ai[]' sources/compliance_sources.json
```

**Output**:
```json
"prompt_data_handling"
"training_data_consent"
"automated_decisions"
"profiling_transparency"
"data_retention_policies"
```

### Step 4: Update Course Compliance Guidelines

If new regulations found:
1. Document in `docs/compliance_sources/`
2. Update `implications_for_ai` in source JSON
3. Alert course development team
4. Update course content as needed

---

## Example 4: Competitive Analysis Report

**Scenario**: Generate a competitive positioning report for your AI course.

### Step 1: Fetch All Competitor Data

```bash
python scripts/fetch_docs.py --category ai_courses_platforms --force-refresh --verbose
```

### Step 2: Extract Key Metrics

```bash
# Create comparison table
echo "# Competitive Analysis - AI Courses"
echo ""
echo "| Platform | Price (BRL) | Duration (h) | Tier | Rating |"
echo "|----------|-------------|--------------|------|--------|"

jq -r '.platforms | to_entries[] |
  "| \(.value.name) | \(.value.metrics.price_brl // 0) | \(.value.metrics.duration_hours // "N/A") | \(.value.tier) | \(.value.metrics.rating_reclameaqui // "N/A") |"' \
  sources/ai_courses_platforms.json
```

**Output**:
```markdown
# Competitive Analysis - AI Courses

| Platform | Price (BRL) | Duration (h) | Tier | Rating |
|----------|-------------|--------------|------|--------|
| Sebrae - IA na Prática | 0 | 3 | free | institutional |
| RD University (TOTVS) | 1997 | 1 | paid | 6.9 |
| G4 Educação | 2997 | N/A | premium | 8.9 |
| Ecommerce na Prática | 990 | 250+ | membership | 9.0 |
...
```

### Step 3: Identify Gaps & Opportunities

```bash
# High prices without high ratings
jq '.platforms | to_entries[] |
  select(.value.metrics.price_brl > 1500 and
         (.value.metrics.rating_reclameaqui // 10) < 8) |
  {name: .value.name, price: .value.metrics.price_brl, rating: .value.metrics.rating_reclameaqui}' \
  sources/ai_courses_platforms.json
```

### Step 4: Generate Recommendations

Based on analysis:
- **Price Gap**: Most courses are R$1,000-R$3,000
- **Duration Sweet Spot**: 8-20 hours
- **Rating Benchmark**: Target >8.5 on RA
- **Opportunity**: Marketplace-specific AI tracks (underserved)

---

## Example 5: Reputation Monitoring

**Scenario**: Track competitor reputation scores on Reclame Aqui.

### Step 1: Set Up Reputation Tracking

```bash
# List all platforms with RA tracking
jq '.platforms | to_entries[] |
  select(.value.urls.reputation != null) |
  {name: .value.name, reputation_url: .value.urls.reputation, current_rating: .value.metrics.rating_reclameaqui}' \
  sources/ai_courses_platforms.json
```

### Step 2: Fetch Latest Reputation Data

```bash
# Note: This would require WebFetch in Claude Code or web scraping
/update_competitor_docs --source rd_university
/update_competitor_docs --source g4_educacao
/update_competitor_docs --source ecommerce_na_pratica
```

### Step 3: Compare Ratings Over Time

```bash
# Check historical snapshots
for snapshot in snapshots/*/ai_courses_platforms.json; do
  date=$(basename $(dirname $snapshot))
  rating=$(jq -r '.platforms.g4_educacao.metrics.rating_reclameaqui' $snapshot 2>/dev/null || echo "N/A")
  echo "$date: G4 Rating = $rating"
done
```

### Step 4: Alert on Significant Changes

```bash
# Set up alert for rating drop >0.5
# Add to monitor_changes.sh or implement custom script
```

---

## Example 6: Marketplace Policy Updates

**Scenario**: Check if Mercado Livre updated their image usage policies.

### Step 1: Fetch Current Policy

```bash
/update_competitor_docs --source mercado_livre
```

### Step 2: Review Image Policy Documentation

```bash
cat docs/marketplaces_docs/mercado_livre/latest.md | grep -A 10 -i "image\|imagem\|foto"
```

### Step 3: Compare with Previous Version

```bash
# Find previous versions
ls -lt docs/marketplaces_docs/mercado_livre/overview_*.md | head -5

# Compare latest with previous
diff docs/marketplaces_docs/mercado_livre/overview_2025-11-22*.md \
     docs/marketplaces_docs/mercado_livre/overview_2025-11-23*.md
```

### Step 4: Update Course Content if Needed

If policies changed:
1. Document the change
2. Update course module on marketplace compliance
3. Notify students/users
4. Update best practices guide

---

## Example 7: Trend Analysis - AI Adoption

**Scenario**: Analyze trends in AI adoption for e-commerce based on news sources.

### Step 1: Fetch News Sources

```bash
python scripts/fetch_docs.py --category ecommerce_trends --verbose
```

### Step 2: Search for AI Adoption Trends

```bash
# Search across all trend docs
grep -r -i "adoção\|crescimento\|demanda\|mercado.*ia" docs/ecommerce_trends/ | \
  grep -v ".json" | head -20
```

### Step 3: Extract Key Statistics

```bash
# Look for specific stats (from PwC, Udemy, etc.)
cat docs/ecommerce_trends/pwc_brasil/latest.md | grep -E "[0-9]+%|quadruplic|crescimento"
cat docs/ecommerce_trends/udemy_brasil/latest.md | grep -E "[0-9]+%|aumento|demanda"
```

### Step 4: Create Trend Summary

Create file: `docs/trends_summary_$(date +%Y-%m-%d).md`

```markdown
# AI Adoption Trends - E-commerce Brasil

**Date**: 2025-11-23

## Key Findings

1. **Job Market** (PwC):
   - AI skills demand quadrupled (2021-2024)
   - 47% salary premium for AI-skilled professionals

2. **Training Demand** (Udemy):
   - 24% increase in AI course consumption
   - Corporate training leading growth

3. **Marketplace Adoption**:
   - TikTok Shop launching full AI suite (GMV Max, Search Ads)
   - Shopify Magic/Sidekick rolling out in BR
   - ML, Shopee enhancing AI moderation

## Strategic Implications

- Strong market validation for AI training
- Focus on marketplace-specific AI applications
- Emphasize ROI and practical outcomes
- Highlight compliance (LGPD) as differentiator
```

---

## Example 8: Automated Weekly Report

**Scenario**: Create a weekly summary of all changes and updates.

### Step 1: Set Up Weekly Automation

Create file: `scripts/weekly_report.sh`

```bash
#!/bin/bash
# Weekly competitive intelligence report

REPORT_DATE=$(date +%Y-%m-%d)
REPORT_FILE="reports/weekly_report_$REPORT_DATE.md"

mkdir -p reports

echo "# Weekly Competitor Intelligence Report" > $REPORT_FILE
echo "**Week Ending**: $REPORT_DATE" >> $REPORT_FILE
echo "" >> $REPORT_FILE

# Run full update
python scripts/fetch_docs.py --all --force-refresh

# Compare with last week
echo "## Changes Detected" >> $REPORT_FILE
./scripts/monitor_changes.sh --compare >> $REPORT_FILE

# Price changes
echo "" >> $REPORT_FILE
echo "## Pricing Updates" >> $REPORT_FILE
# ... add pricing comparison logic

# New features/courses
echo "" >> $REPORT_FILE
echo "## New Launches" >> $REPORT_FILE
# ... add new feature detection logic

# Compliance updates
echo "" >> $REPORT_FILE
echo "## Compliance & Regulatory" >> $REPORT_FILE
# ... add compliance check logic

echo "Report generated: $REPORT_FILE"
```

### Step 2: Schedule Weekly Run

Add to crontab:
```cron
# Every Monday at 6 AM
0 6 * * 1 /path/to/competitor_intelligence/scripts/weekly_report.sh
```

---

## Tips & Best Practices

### 1. Efficient Source Checking

```bash
# Check only high-priority sources
jq '.platforms | to_entries[] | select(.value.priority == "high") | .value.name' \
  sources/ai_courses_platforms.json
```

### 2. Quick Content Verification

```bash
# Verify all latest.md files exist
find docs/ -name "latest.md" -type f | wc -l
# Should match total number of sources
```

### 3. Search Across All Documentation

```bash
# Find mentions of specific topic across all docs
grep -r "shopify magic\|gmv max\|ia generativa" docs/ --include="latest.md"
```

### 4. Export for Analysis

```bash
# Export all metadata to CSV for Excel analysis
find docs/ -name "metadata_*.json" -exec cat {} \; | \
  jq -r '[.source_name, .category, .fetched_at, .content_hash] | @csv'
```

### 5. Backup Critical Data

```bash
# Create weekly backup
tar -czf backups/competitor_intelligence_$(date +%Y-%m-%d).tar.gz \
  sources/ docs/ snapshots/ config.json
```

---

## Troubleshooting Examples

### Issue: Source Fetch Failed

```bash
# Check which sources failed
grep -r "ERROR\|FAILED" logs/ snapshots/

# Manually test URL
curl -I "https://example.com/source-url"

# Update URL if changed
# Edit sources/[category].json and update URL
```

### Issue: Outdated Documentation

```bash
# Find docs older than 7 days
find docs/ -name "latest.md" -mtime +7

# Force refresh old docs
python scripts/fetch_docs.py --all --force-refresh
```

### Issue: Missing Metadata

```bash
# Find docs without metadata
for doc in docs/*/*/latest.md; do
  dir=$(dirname $doc)
  if [ ! -f "$dir/metadata_"*.json ]; then
    echo "Missing metadata: $dir"
  fi
done
```

---

**More examples available in the full documentation (README.md)**
