# Outputs | curso_agent

**Purpose**: Generated course content and artifacts

## Directory Structure

```
outputs/
├── video_scripts/       # Generated video scripts (.md + .llm.json + .meta.json)
├── workbooks/           # Generated workbooks (PDF-ready .md)
├── exercises/           # Hands-on exercises with solutions
├── sales/              # Sales collateral (landing pages, emails, ads)
├── packages/           # Hotmart-ready packages
└── reports/            # Validation reports and quality scores
```

## Trinity Output Format

All builders generate 3 files:
- **.md** - Human-readable content
- **.llm.json** - Structured data for LLM consumption
- **.meta.json** - Metadata (version, timestamp, quality_score, [OPEN_VARIABLES] used)

## Example

```
outputs/video_scripts/
├── 01_introducao_codexa.md
├── 01_introducao_codexa.llm.json
└── 01_introducao_codexa.meta.json
```

## Gitignore

Outputs are typically excluded from git (add to .gitignore):
```
outputs/**/*.md
outputs/**/*.json
!outputs/README.md
```

## Status

- **Sprint 1**: Directory created
- **Sprint 2**: Builders populate this directory
- **Sprint 5**: Trinity Output implemented
