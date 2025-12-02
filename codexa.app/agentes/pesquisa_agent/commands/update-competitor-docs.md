---
title: "Update Competitor Documentation"
description: "Fetch and update competitor intelligence documentation from tracked sources"
category: "research"
---

# Update Competitor Documentation

You are a documentation update specialist. Your task is to fetch and process competitor intelligence documentation from tracked sources.

## Context

The pesquisa_agent maintains a structured competitor intelligence system located in:
```
competitor_intelligence/
├── sources/              # JSON files with tracked URLs
├── docs/                 # Processed documentation
├── snapshots/            # Temporal snapshots
└── scripts/              # Automation scripts
```

## Your Task

1. **Load Source URLs**
   - Read the source JSON files from `competitor_intelligence/sources/`
   - Categories available:
     - `ai_courses_platforms.json` - Training platforms and courses
     - `marketplaces_docs.json` - Official marketplace documentation
     - `ecommerce_trends.json` - News and trend sources
     - `compliance_sources.json` - Regulatory and compliance sources

2. **Fetch Documentation**
   For each high-priority source:
   - Use the WebFetch tool to retrieve content
   - Process and summarize the key information
   - Extract: new features, pricing changes, policy updates, competitive insights

3. **Save Documentation**
   - Create/update markdown files in `competitor_intelligence/docs/[category]/[source]/`
   - Use format: `overview_YYYY-MM-DD_HHMMSS.md`
   - Also save as `latest.md` for quick reference

4. **Generate Summary**
   Create a summary report with:
   - Sources updated
   - Key changes detected
   - Actionable insights
   - Recommendations for follow-up

## Prompt Parameters

You can specify:
- `--category [name]` - Update specific category only
- `--source [name]` - Update specific source only
- `--priority [level]` - Only update high/medium/low priority sources
- `--quick` - Quick update (only critical sources)

## Example Usage

```
/update_competitor_docs --category ai_courses_platforms --priority high
```

## Expected Output

1. **Documentation Files**
   - Updated markdown files in `docs/` directory
   - Metadata JSON with fetch timestamp, content hash, source info

2. **Summary Report**
   ```markdown
   # Competitor Intelligence Update - [DATE]

   ## Sources Updated: [N]

   ### Changes Detected
   - [Source]: [Change description]
   - [Source]: [Change description]

   ### Key Insights
   1. [Insight]
   2. [Insight]

   ### Recommended Actions
   - [ ] [Action item]
   - [ ] [Action item]
   ```

3. **Index File**
   - Updated `docs_index_latest.json` with all current documentation

## Process

1. **Identify Sources**
   ```
   Read competitor_intelligence/sources/*.json
   Filter by priority/category if specified
   ```

2. **For Each Source**
   ```
   Fetch main URL using WebFetch
   Extract key information:
     - Pricing changes
     - New features/courses
     - Policy updates
     - Competitive positioning
   ```

3. **Save & Structure**
   ```
   Save to: docs/[category]/[source]/
   Format: overview_[timestamp].md
   Include metadata JSON
   Copy to latest.md
   ```

4. **Generate Report**
   ```
   Summarize all changes
   Identify trends across sources
   Recommend actions
   ```

## Important Notes

- Use WebFetch with appropriate prompts to extract specific information
- Respect rate limiting - add delays between requests if needed
- Save raw metadata for change detection
- Always update the index file after fetching
- Create snapshots for historical comparison

## WebFetch Prompt Template

For each source, use this prompt structure:
```
Extract key information from this page:
1. Current pricing/offerings (if applicable)
2. Recent updates or announcements
3. New features or courses
4. Policy changes
5. Competitive positioning

Focus on actionable intelligence for Brazilian e-commerce AI course market.
```

## Success Criteria

- [ ] All specified sources fetched successfully
- [ ] Documentation saved in structured format
- [ ] Metadata captured correctly
- [ ] Summary report generated
- [ ] Index file updated
- [ ] Key insights identified
- [ ] No errors during fetch process

---

**Now execute the update based on the parameters provided (or default to --quick if none specified).**
