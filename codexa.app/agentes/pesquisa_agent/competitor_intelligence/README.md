# Competitor Intelligence System

**Version**: 1.0.0
**Status**: Active
**Last Updated**: 2025-11-23

---

## 🎯 Purpose

Automated system for tracking, fetching, and analyzing competitor documentation and market intelligence for Brazilian AI courses and e-commerce markets.

**Key Capabilities:**
- Track 40+ sources across 4 categories
- Automated documentation fetching
- Change detection and monitoring
- Historical snapshots
- Compliance tracking
- Competitive analysis

---

## 📂 Structure

```
competitor_intelligence/
├── sources/                     # Source URL databases (JSON)
│   ├── ai_courses_platforms.json      # 10 training platforms
│   ├── marketplaces_docs.json         # 9 marketplace docs
│   ├── ecommerce_trends.json          # 12 news/trend sources
│   └── compliance_sources.json        # 8 regulatory sources
│
├── docs/                        # Fetched documentation
│   ├── ai_courses_platforms/
│   │   ├── sebrae/
│   │   │   ├── overview_2025-11-23.md
│   │   │   ├── latest.md
│   │   │   └── metadata_2025-11-23.json
│   │   └── [other sources...]
│   ├── marketplaces_docs/
│   ├── ecommerce_trends/
│   └── compliance_sources/
│
├── snapshots/                   # Historical snapshots
│   ├── 2025-11-23/
│   │   ├── ai_courses_platforms.json
│   │   ├── change_report_2025-11-23.md
│   │   └── [snapshot files...]
│   └── [other dates...]
│
├── scripts/                     # Automation tools
│   ├── fetch_docs.py           # Documentation fetcher
│   └── monitor_changes.sh      # Change monitor
│
├── docs_index_latest.json      # Current documentation index
└── README.md                   # This file
```

---

## 🚀 Quick Start

### 1. Update All Documentation

Using slash command (recommended):
```bash
/update_competitor_docs --priority high
```

Using Python script:
```bash
cd competitor_intelligence/scripts
python fetch_docs.py --all --verbose
```

Using bash script:
```bash
cd competitor_intelligence/scripts
./monitor_changes.sh --daily
```

### 2. Update Specific Category

```bash
/update_competitor_docs --category ai_courses_platforms
```

Or:
```bash
python scripts/fetch_docs.py --category ai_courses_platforms --verbose
```

### 3. Monitor Changes

```bash
./scripts/monitor_changes.sh --compare
```

---

## 📊 Source Categories

### 1. AI Courses Platforms (10 sources)

**Purpose**: Track competitor training programs, pricing, content updates

**Key Sources**:
- Sebrae - Free institutional courses
- RD University - Paid B2B platform
- G4 Educação - Premium programs
- Ecommerce na Prática - Membership model
- Live University/ML Ensina - Marketplace-specific
- DMI Brasil - International certification
- Senac - Regional institutional
- Niara - Specialized e-commerce AI
- Microsoft/ENAP - Free corporate
- AWS AI Ready - Free technical

**Monitoring**:
- Price changes (threshold: 15%)
- New course launches
- Reputation scores (Reclame Aqui)
- Certification updates
- Partnership announcements

### 2. Marketplaces Documentation (9 sources)

**Purpose**: Track platform policies, AI tools, educational content

**Key Sources**:
- Mercado Livre (Priority 1)
- Shopee (Priority 2)
- Magazine Luiza (Priority 3)
- Amazon BR (Priority 4)
- TikTok Shop (Priority 5)
- Shopify (Priority 6)
- Americanas, Casas Bahia, Shein (Priority 7-9)

**Monitoring**:
- Policy changes (images, descriptions, ads)
- New AI tools (GMV Max, Shopify Magic)
- Educational programs
- API updates
- Live commerce features

### 3. E-commerce Trends (12 sources)

**Purpose**: Market intelligence, news, research reports

**Key Sources**:
- B9 - Tech/business news
- Mercado & Consumo - Retail news
- IT Forum - Enterprise tech
- Money Report - Business news
- PwC Brasil - Market research
- Ebit Nielsen - E-commerce metrics
- ABComm - Industry association
- Udemy Brasil - Training trends
- Alura - Tech education
- TikTok Newsroom - Platform updates
- Meta Business - Social commerce
- Reclame Aqui - Reputation monitoring

**Monitoring**:
- AI adoption trends
- Market size/growth
- New platform launches
- Training demand
- Reputation changes

### 4. Compliance Sources (8 sources)

**Purpose**: Legal/regulatory tracking for AI and e-commerce

**Key Sources**:
- LGPD Official - Data protection law
- ANPD - Data protection authority
- CONAR - Advertising regulation
- Procon - Consumer protection
- CDC - Consumer defense code
- E-commerce Decree - Online commerce rules
- Copyright Law - IP protection
- Reuters Fact Check - Deepfake/fraud monitoring

**Monitoring**:
- New regulations
- Enforcement actions
- AI-specific guidance
- Jurisprudence changes
- Penalty cases

---

## 🔧 Tools & Scripts

### 1. fetch_docs.py

**Purpose**: Fetch and save documentation from tracked sources

**Usage**:
```bash
# Fetch all sources
python fetch_docs.py --all --verbose

# Fetch specific category
python fetch_docs.py --category ai_courses_platforms

# Force refresh
python fetch_docs.py --all --force-refresh

# Generate index only
python fetch_docs.py --generate-index
```

**Features**:
- Fetches content from URLs
- Saves to structured directories
- Creates metadata JSON
- Generates content hashes
- Creates snapshots
- Updates index

### 2. monitor_changes.sh

**Purpose**: Monitor sources for changes and generate reports

**Usage**:
```bash
# Daily monitoring run
./monitor_changes.sh --daily

# Compare with previous snapshot
./monitor_changes.sh --compare

# Send alerts for changes
./monitor_changes.sh --alert

# Fetch updates only
./monitor_changes.sh --fetch
```

**Features**:
- Compares with previous snapshots
- Detects changes in source files
- Generates change reports
- Triggers documentation updates
- (Placeholder for alerts)

### 3. /update_competitor_docs (Slash Command)

**Purpose**: Claude Code slash command for documentation updates

**Usage**:
```bash
# Quick update (high priority only)
/update_competitor_docs --quick

# Update specific category
/update_competitor_docs --category ai_courses_platforms

# Update specific source
/update_competitor_docs --source sebrae

# Update by priority
/update_competitor_docs --priority high
```

**Features**:
- Integrated with Claude Code
- Uses WebFetch tool
- Generates summaries
- Extracts actionable insights
- Updates index automatically

---

## 📋 Workflows

### Daily Workflow

1. **Monitor Changes** (Automated)
   ```bash
   ./scripts/monitor_changes.sh --daily
   ```
   - Detects source file changes
   - Generates change report
   - Triggers updates if needed

2. **Review Reports**
   - Check `snapshots/[date]/change_report_*.md`
   - Identify significant changes
   - Prioritize follow-up actions

3. **Update Documentation** (If changes detected)
   ```bash
   /update_competitor_docs --priority high
   ```

### Weekly Workflow

1. **Full Documentation Refresh**
   ```bash
   python scripts/fetch_docs.py --all --force-refresh --verbose
   ```

2. **Competitive Analysis**
   - Review all latest.md files
   - Compare pricing across platforms
   - Identify new features/trends
   - Update competitive positioning

3. **Compliance Check**
   - Review compliance_sources docs
   - Check for new regulations
   - Update internal policies if needed

### Monthly Workflow

1. **Comprehensive Review**
   - Analyze trends across all categories
   - Generate executive summary
   - Update strategic recommendations

2. **Archive Management**
   - Archive old snapshots (keep last 90 days)
   - Compress historical docs
   - Clean up redundant files

3. **Source List Update**
   - Review source priorities
   - Add new competitors/sources
   - Remove inactive sources
   - Update monitoring parameters

---

## 📊 Metrics & KPIs

### Tracking Metrics

**Source Coverage**:
- Total sources tracked: 40+
- High priority: 15
- Active monitoring: 32

**Update Frequency**:
- Daily: 8 sources (marketplaces, news)
- Weekly: 18 sources (platforms, trends)
- Monthly: 14 sources (compliance, research)

**Change Detection**:
- Average changes/week: [To be measured]
- Critical changes/month: [To be measured]
- False positive rate: [To be measured]

### Success Metrics

- [ ] 95% source availability
- [ ] <24h update latency for critical sources
- [ ] 100% compliance tracking coverage
- [ ] <5% documentation gaps

---

## 🔔 Alerts & Notifications

### Alert Triggers

**Critical** (Immediate action):
- Major policy change (marketplace)
- New regulation (LGPD/CONAR)
- Competitor price drop >20%
- Reputation crisis (RA score drop >1.0)

**High** (Same day):
- New competitor entry
- Feature launch (AI tools)
- Training program update
- Enforcement action

**Medium** (Weekly review):
- Price change 10-20%
- Content update
- Partnership announcement
- Research report release

**Low** (Monthly review):
- Minor updates
- Blog posts
- General news

### Alert Configuration

Currently placeholder in `monitor_changes.sh`.

**To configure**:
1. Choose notification method (email, Slack, Discord, GitHub Issues)
2. Set webhook URLs or API credentials
3. Update `send_alerts()` function in `monitor_changes.sh`
4. Test alert flow

---

## 🛠️ Maintenance

### Regular Tasks

**Daily**:
- [ ] Run change monitor
- [ ] Review high-priority changes
- [ ] Update critical source docs

**Weekly**:
- [ ] Full documentation refresh
- [ ] Review all categories
- [ ] Update competitive analysis
- [ ] Clean up failed fetches

**Monthly**:
- [ ] Archive old snapshots
- [ ] Review source priorities
- [ ] Update monitoring parameters
- [ ] Generate trend report

### Troubleshooting

**Issue**: Fetch fails for source
- Check if URL is still valid
- Verify source is accessible
- Check rate limiting
- Update URL in source JSON

**Issue**: No changes detected (but expected)
- Verify snapshot comparison logic
- Check file timestamps
- Review diff output manually

**Issue**: Index not updating
- Run `python fetch_docs.py --generate-index`
- Check file permissions
- Verify JSON syntax

---

## 🔐 Security & Privacy

### Data Handling

- **Public Data Only**: All tracked sources are publicly accessible
- **No Credentials**: No authentication or private APIs used
- **Respect robots.txt**: Follow site crawling policies
- **Rate Limiting**: Implement delays between requests
- **Cache Responses**: Avoid redundant fetches

### Compliance

- **LGPD**: No personal data collection or processing
- **Copyright**: Fair use for competitive intelligence only
- **Attribution**: Source URLs maintained in all docs
- **Retention**: 90-day snapshot retention policy

---

## 📈 Future Enhancements

### Planned Features

1. **Automated Alerts**
   - Email notifications
   - Slack/Discord webhooks
   - GitHub issue creation

2. **Enhanced Analytics**
   - Trend visualization
   - Competitive dashboards
   - Price tracking charts

3. **AI-Powered Analysis**
   - Automatic insight extraction
   - Sentiment analysis
   - Anomaly detection

4. **API Integration**
   - Direct marketplace API access
   - Real-time data feeds
   - Automated compliance checks

5. **Scheduling**
   - Cron job setup
   - GitHub Actions integration
   - Cloud function deployment

---

## 🤝 Contributing

### Adding New Sources

1. **Identify Source**
   - Confirm it's public and relevant
   - Determine category and priority
   - Collect all relevant URLs

2. **Update Source JSON**
   ```json
   "new_source": {
     "name": "Source Name",
     "tier": "paid|free|premium",
     "priority": "high|medium|low",
     "urls": {
       "main": "https://...",
       "docs": "https://..."
     },
     "monitoring": {
       "price_changes": true,
       "new_features": true
     },
     "metrics": {
       "price_brl": 0
     }
   }
   ```

3. **Test Fetch**
   ```bash
   python scripts/fetch_docs.py --category [category] --verbose
   ```

4. **Update Documentation**
   - Add to README source list
   - Update total counts
   - Document monitoring criteria

### Updating Monitoring Logic

1. Edit `scripts/fetch_docs.py` or `monitor_changes.sh`
2. Test changes locally
3. Document new parameters/options
4. Update this README

---

## 📞 Support

**Questions or Issues?**

1. Check troubleshooting section above
2. Review script help: `python fetch_docs.py --help`
3. Check logs in `snapshots/[date]/`
4. Contact maintainer

---

## 📄 License

Internal use only - CODEXA Project

---

**Last Updated**: 2025-11-23
**Maintainer**: CODEXA Research Team
**System Status**: ✅ Active
