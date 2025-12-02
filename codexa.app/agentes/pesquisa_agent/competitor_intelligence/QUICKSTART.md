# Competitor Intelligence - Quick Start Guide

**Get started in 5 minutes** ⚡

---

## 1️⃣ Understand What You Have

You now have a complete competitor intelligence system tracking:

- **10 AI Course Platforms** (Sebrae, G4, RD University, etc.)
- **9 Marketplace Docs** (Mercado Livre, Shopee, TikTok Shop, etc.)
- **12 Trend Sources** (B9, PwC, Ebit Nielsen, Reclame Aqui, etc.)
- **8 Compliance Sources** (LGPD, CONAR, CDC, etc.)

**Total**: 40+ sources with structured URLs and monitoring parameters.

---

## 2️⃣ First Run - Update Documentation

### Option A: Using Slash Command (Easiest)

```bash
/update_competitor_docs --priority high
```

This will:
1. Fetch documentation from high-priority sources
2. Save structured markdown files
3. Generate a summary report
4. Update the index

### Option B: Using Python Script

```bash
cd competitor_intelligence/scripts
python fetch_docs.py --all --verbose
```

### Option C: Using Bash Script

```bash
cd competitor_intelligence/scripts
./monitor_changes.sh --daily
```

---

## 3️⃣ View Results

### Check Documentation

```bash
# Navigate to docs directory
cd competitor_intelligence/docs

# View latest docs for a source
cat ai_courses_platforms/sebrae/latest.md
cat marketplaces_docs/mercado_livre/latest.md
```

### Check Index

```bash
# View complete documentation index
cat competitor_intelligence/docs_index_latest.json
```

### Check Snapshots

```bash
# View today's snapshot and change report
ls competitor_intelligence/snapshots/$(date +%Y-%m-%d)/
cat competitor_intelligence/snapshots/$(date +%Y-%m-%d)/change_report_*.md
```

---

## 4️⃣ Explore Sources

All source URLs are organized in JSON files:

```bash
cd competitor_intelligence/sources

# View AI course platforms
cat ai_courses_platforms.json | jq '.platforms'

# View marketplace docs
cat marketplaces_docs.json | jq '.marketplaces'

# View compliance sources
cat compliance_sources.json | jq '.data_protection'
```

**Each source includes**:
- Name and URLs
- Priority level
- Monitoring parameters
- Metrics (price, duration, reputation)
- Key topics to track

---

## 5️⃣ Common Tasks

### Update Specific Category

```bash
/update_competitor_docs --category ai_courses_platforms
```

### Check for Changes

```bash
./scripts/monitor_changes.sh --compare
```

### Add New Source

1. Open relevant JSON file in `sources/`
2. Add new source with required fields:
   ```json
   "source_name": {
     "name": "Display Name",
     "priority": "high",
     "urls": {
       "main": "https://..."
     },
     "monitoring": {
       "price_changes": true
     }
   }
   ```
3. Run update to fetch new source

### Generate Fresh Index

```bash
python scripts/fetch_docs.py --generate-index
```

---

## 6️⃣ Automation Setup (Optional)

### Daily Auto-Update (Cron)

Add to crontab:
```cron
# Run daily at 9 AM
0 9 * * * cd /path/to/competitor_intelligence/scripts && ./monitor_changes.sh --daily
```

### Weekly Full Refresh (Cron)

```cron
# Run every Monday at 6 AM
0 6 * * 1 cd /path/to/competitor_intelligence/scripts && python fetch_docs.py --all
```

---

## 🎯 Key Files to Know

| File | Purpose |
|------|---------|
| `sources/*.json` | Source URL databases (edit these to add/modify sources) |
| `docs/[category]/[source]/latest.md` | Most recent documentation for each source |
| `docs_index_latest.json` | Complete index of all documentation |
| `snapshots/[date]/change_report_*.md` | Daily change detection reports |
| `scripts/fetch_docs.py` | Main documentation fetcher |
| `scripts/monitor_changes.sh` | Change monitoring script |
| `/update_competitor_docs` | Claude Code slash command |

---

## 🔥 Power User Tips

### 1. Quick Competitive Analysis

```bash
# Compare pricing across platforms
jq '.platforms | to_entries[] | {name: .value.name, price: .value.metrics.price_brl}' \
  sources/ai_courses_platforms.json
```

### 2. Monitor Reputation Scores

```bash
# Check Reclame Aqui ratings
jq '.platforms | to_entries[] | select(.value.metrics.rating_reclameaqui != null) | {name: .value.name, rating: .value.metrics.rating_reclameaqui}' \
  sources/ai_courses_platforms.json
```

### 3. Track High-Priority Sources

```bash
# List all high-priority sources
jq '.. | objects | select(.priority == "high") | .name' sources/*.json
```

### 4. Check Update Schedule

```bash
# View update frequency for all sources
jq '.metadata.update_frequency' sources/*.json
```

---

## 📚 Next Steps

1. **Customize Sources**
   - Review `sources/*.json` files
   - Adjust priorities based on your needs
   - Add specific competitors to track

2. **Set Up Alerts**
   - Edit `scripts/monitor_changes.sh`
   - Configure notification method (Slack, email, etc.)
   - Test alert flow

3. **Integrate with Workflow**
   - Schedule regular updates
   - Create competitive analysis reports
   - Feed insights to other agents (anuncio, marca, curso)

4. **Extend System**
   - Add new source categories
   - Implement advanced analytics
   - Create visualization dashboards

---

## 🆘 Need Help?

**Common Issues**:

1. **Script won't run**
   - Check file permissions: `chmod +x scripts/*.sh`
   - Verify Python installed: `python --version`

2. **No sources found**
   - Verify you're in correct directory
   - Check JSON syntax: `jq . sources/[file].json`

3. **WebFetch not working**
   - Ensure running in Claude Code environment
   - Check internet connectivity
   - Verify URLs are accessible

**Full Documentation**: See `README.md` in this directory

**Support**: Check troubleshooting section in main README

---

## ✅ Success Checklist

After setup, you should have:

- [x] Source JSON files with 40+ tracked sources
- [x] Documentation fetcher script working
- [x] Change monitoring script working
- [x] Slash command available in Claude Code
- [x] First documentation fetch completed
- [x] Index file generated
- [x] Understand where to find docs
- [x] Know how to add new sources
- [x] Know how to run updates

**You're all set!** 🚀

Start exploring competitor intelligence in `docs/` directory.

---

**Quick Command Reference**:

```bash
# Update all
/update_competitor_docs --all

# Update category
/update_competitor_docs --category [name]

# Monitor changes
./scripts/monitor_changes.sh --compare

# Full refresh
python scripts/fetch_docs.py --all --force-refresh

# Generate index
python scripts/fetch_docs.py --generate-index
```

**Happy intelligence gathering!** 🔍
