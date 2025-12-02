# 📝 ECOMLM.CODEXA - Complete Command Reference

## COMMAND SYSTEM IDENTITY
You are using the ECOMLM.CODEXA command system, a comprehensive set of slash commands for e-commerce automation and development workflows.

## COMMAND USAGE PATTERN
```
/command_name [required_param] <optional_param>
```

---

## 🚀 CORE E-COMMERCE COMMANDS

### /pesquisa - Market Research Agent
```
SYNTAX: /pesquisa "product or niche description"

PURPOSE:
Conduct comprehensive market research across 9+ Brazilian marketplaces

WHEN TO USE:
- Starting a new product listing
- Analyzing competitor landscape
- Extracting SEO keywords
- Understanding pricing strategies

EXAMPLE:
/pesquisa "fone bluetooth para home office"

OUTPUT:
- research_notes.md (22 structured blocks)
- Competitor analysis
- Pricing matrix
- SEO keyword clusters
- Compliance risks
```

### /anuncio - Ad Generation Agent
```
SYNTAX: /anuncio [research_file]

PURPOSE:
Generate optimized marketplace listings with 60% higher CTR

WHEN TO USE:
- After completing market research
- Creating new product listings
- Optimizing existing listings
- A/B testing different approaches

EXAMPLE:
/anuncio ./research_notes.md

OUTPUT:
- anuncio.json (structured data)
- anuncio.md (formatted listing)
- 9 image prompts
- Video script
- SEO metadata
```

### /marca - Brand Strategy Agent
```
SYNTAX: /marca [business_context]

PURPOSE:
Develop comprehensive brand strategy and identity

WHEN TO USE:
- New brand creation
- Brand refresh/repositioning
- Multi-brand management
- Brand consistency audit

EXAMPLE:
/marca "Sustainable home products for millennials"

OUTPUT:
- brand_strategy.md
- brand_guidelines.json
- Visual identity specs
- Tone of voice guide
- Brand narrative
```

---

## 🧠 KNOWLEDGE & INTELLIGENCE COMMANDS

### /knowledge - Knowledge Extraction Agent
```
SYNTAX: /knowledge [source_path]

PURPOSE:
Extract and synthesize knowledge from any source

WHEN TO USE:
- Processing documentation
- Creating training datasets
- Knowledge base updates
- Content consolidation

EXAMPLE:
/knowledge ./docs/

OUTPUT:
- knowledge_cards.json
- Quality metrics
- Relationship graph
- ML-ready datasets
```

### /scout - Repository Intelligence Agent
```
SYNTAX: /scout [search_query]

PURPOSE:
Navigate and search codebases intelligently

WHEN TO USE:
- Finding specific code patterns
- Understanding dependencies
- Locating documentation
- Code archaeology

EXAMPLE:
/scout "database connection"

OUTPUT:
- File locations
- Code snippets
- Dependency tree
- Usage examples
```

### /mentor - Strategic Planning Agent
```
SYNTAX: /mentor [objective]

PURPOSE:
Provide strategic guidance and KPI tracking

WHEN TO USE:
- Project planning
- Performance analysis
- Resource allocation
- Risk assessment

EXAMPLE:
/mentor "Scale to 1000 products/month"

OUTPUT:
- Strategic plan
- KPI dashboard
- Risk matrix
- Action items
```

---

## 🔧 DEVELOPMENT COMMANDS

### /codexa - Central Orchestrator
```
SYNTAX: /codexa [action] [params]

PURPOSE:
Central command for system orchestration

ACTIONS:
- run: Execute workflow
- status: Check system status
- config: Update configuration
- health: System health check

EXAMPLE:
/codexa run full_pipeline
/codexa status agents
```

### /build - Build System
```
SYNTAX: /build [target]

PURPOSE:
Build and compile project components

TARGETS:
- all: Complete build
- backend: Python backend
- frontend: TypeScript frontend
- docs: Documentation

EXAMPLE:
/build all
```

### /test - Test Runner
```
SYNTAX: /test [scope]

PURPOSE:
Run automated tests

SCOPES:
- unit: Unit tests only
- integration: Integration tests
- e2e: End-to-end tests
- all: Complete test suite

EXAMPLE:
/test e2e
```

---

## 📋 WORKFLOW COMMANDS

### /orchestrator - Workflow Orchestration
```
SYNTAX: /orchestrator [workflow_name]

PURPOSE:
Execute predefined workflows

WORKFLOWS:
- full_listing: Research → Brand → Generate
- quick_listing: Generate from template
- brand_audit: Brand consistency check
- knowledge_update: Refresh knowledge base

EXAMPLE:
/orchestrator full_listing
```

### /plan - Execution Planning
```
SYNTAX: /plan [goal]

PURPOSE:
Create execution plans for complex tasks

EXAMPLE:
/plan "Launch 50 products this week"

OUTPUT:
- Task breakdown
- Timeline
- Resource requirements
- Dependencies
```

---

## 🛠️ UTILITY COMMANDS

### /commit - Git Commit Helper
```
SYNTAX: /commit [type] "message"

PURPOSE:
Create standardized git commits

TYPES:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Code style
- refactor: Code refactoring
- test: Test updates
- chore: Maintenance

EXAMPLE:
/commit feat "Add HOP framework to marca agent"
```

### /organize - File Organization
```
SYNTAX: /organize [directory]

PURPOSE:
Organize files according to project structure

EXAMPLE:
/organize ./data/
```

### /clean_worktree - Cleanup
```
SYNTAX: /clean_worktree

PURPOSE:
Clean working directory and temporary files

EXAMPLE:
/clean_worktree
```

---

## 🔍 ANALYSIS COMMANDS

### /classify_issue - Issue Classification
```
SYNTAX: /classify_issue "issue_description"

PURPOSE:
Classify and prioritize issues

EXAMPLE:
/classify_issue "API timeout on large requests"

OUTPUT:
- Priority level
- Category
- Suggested assignee
- Related issues
```

### /health_check - System Health
```
SYNTAX: /health_check [component]

PURPOSE:
Check component health status

COMPONENTS:
- agents: All agents
- api: API endpoints
- database: Database connections
- external: External services

EXAMPLE:
/health_check agents
```

---

## 📊 SPECIALIZED COMMANDS

### /in_loop_review - Iterative Review
```
SYNTAX: /in_loop_review [file]

PURPOSE:
Continuous review during development

EXAMPLE:
/in_loop_review processor.py
```

### /track_agentic_kpis - KPI Tracking
```
SYNTAX: /track_agentic_kpis [agent]

PURPOSE:
Track agent-specific KPIs

EXAMPLE:
/track_agentic_kpis pesquisa

OUTPUT:
- Performance metrics
- Success rate
- Average duration
- Resource usage
```

### /mentor_tactical_report - Tactical Analysis
```
SYNTAX: /mentor_tactical_report

PURPOSE:
Generate tactical execution report

OUTPUT:
- Current status
- Blockers
- Immediate actions
- Risk assessment
```

---

## 🧪 E2E TEST COMMANDS

### /test_basic_query
```
PURPOSE: Test basic query functionality
```

### /test_complex_query
```
PURPOSE: Test complex multi-step queries
```

### /test_sql_injection
```
PURPOSE: Test SQL injection prevention
```

### /test_export_functionality
```
PURPOSE: Test data export features
```

### /test_random_query_generator
```
PURPOSE: Test with random query generation
```

---

## 🔄 MIGRATION COMMANDS

### /convert_paths_absolute
```
SYNTAX: /convert_paths_absolute

PURPOSE:
Convert relative paths to absolute in configurations

EXAMPLE:
/convert_paths_absolute
```

---

## 📝 COMMAND PATTERNS

### Sequential Execution
```bash
# Research then generate
/pesquisa "product" && /anuncio

# Full pipeline
/pesquisa "product" && /marca && /anuncio
```

### Parallel Execution
```bash
# Run multiple researches
/pesquisa "product1" & /pesquisa "product2"
```

### Conditional Execution
```bash
# Generate only if research succeeds
/pesquisa "product" && /anuncio || echo "Research failed"
```

---

## 🎯 BEST PRACTICES

### 1. Command Selection
```
IF task = "new product listing":
    /pesquisa → /anuncio

IF task = "brand development":
    /marca → /knowledge

IF task = "code exploration":
    /scout → /mentor

IF task = "system check":
    /health_check → /track_agentic_kpis
```

### 2. Parameter Guidelines
- Always quote strings with spaces
- Use relative paths when possible
- Provide context in descriptions
- Check command status before chaining

### 3. Error Handling
```bash
# Check if command exists
/help command_name

# Validate parameters
/command --validate params

# Dry run mode
/command --dry-run
```

---

## 🆘 HELP SYSTEM

### Getting Help
```bash
# List all commands
/help

# Get command details
/help command_name

# Show examples
/help command_name --examples
```

### Command Discovery
```bash
# Search commands
/help --search "keyword"

# List by category
/help --category "ecommerce"
```

---

## 📌 QUICK REFERENCE

### Most Used Commands
1. `/pesquisa` - Market research
2. `/anuncio` - Generate listing
3. `/marca` - Brand strategy
4. `/scout` - Find code
5. `/commit` - Git commit
6. `/test` - Run tests
7. `/health_check` - System status

### Command Categories
- **E-Commerce**: pesquisa, anuncio, marca
- **Knowledge**: knowledge, scout, mentor
- **Development**: build, test, commit
- **Utility**: organize, clean, health_check
- **Workflow**: orchestrator, plan

---

> **Note**: Commands are continuously updated. Use `/help` for the latest command documentation and `/help [command]` for detailed usage information.