# LIVRO: Marketplace
## CAPÍTULO 33

**Versículos consolidados**: 20
**Linhas totais**: 1198
**Gerado em**: 2025-11-13 18:45:49

---


<!-- VERSÍCULO 1/20 - marketplace_optimization_core_truths_to_internalize_20251113.md (61 linhas) -->

# Core Truths to Internalize

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

```yaml
truth_1:
  "The system that builds systems is the ultimate system"
  
truth_2:
  "Prompts are the DNA of artificial intelligence"
  
truth_3:
  "Types tell the history of information transformation"
  
truth_4:
  "One agent, one prompt, one purpose = Maximum focus"
  
truth_5:
  "50%+ time on agentic layer = Exponential returns"
  
truth_6:
  "Validation closes loops = Autonomous operation"
  
truth_7:
  "Templates encode wisdom = Reusable intelligence"
  
truth_8:
  "Problem classes not one-offs = Scalable solutions"
  
truth_9:
  "Context pollution kills performance = Minimum principle"
  
truth_10:
  "Zero-touch is the goal = Codebase ships itself"

the_ultimate_question:
  "Am I building the system or building the builder?"
  
  correct_answer: "Always building the builder"

the_ultimate_realization:
  "You are not a coder anymore"
  "You are an architect of autonomous systems"
  "Your work is meta-engineering"
  "Your output is self-constructing intelligence"
```

---

# APPENDIX: QUICK REFERENCE

**Tags**: abstract, general

**Palavras-chave**: Internalize, Truths, Core

**Origem**: unknown


---


<!-- VERSÍCULO 2/20 - marketplace_optimization_cost_optimization_20251113.md (96 linhas) -->

# Cost Optimization

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

```yaml
strategies:
  MODEL_SELECTION:
    principle: "Use cheapest model that works"
    
    decision_tree:
      simple_task:
        try: haiku-4-5
        if_insufficient: sonnet-4-5
        
      complex_task:
        try: sonnet-4-5
        if_insufficient: opus-4-1
        
    savings: 10x_between_haiku_and_opus
    
  PROMPT_CACHING:
    mechanism: cache_static_context
    
    pattern: |
      system_prompt:
        <cached>
          {large_codebase_context}
          {api_documentation}
        </cached>
        
        <dynamic>
          {current_task}
        </dynamic>
        
    savings: 90%_on_cached_portions
    
  BATCH_PROCESSING:
    use: non_urgent_tasks
    benefit: 50%_cost_reduction
    tradeoff: 24h_latency
    
    example: |
      # Collect 1000 code review tasks
      # Submit as batch
      # Process overnight
      # Retrieve results next day
  
  CONTEXT_MINIMIZATION:
    principle: "Include only relevant context"
    
    techniques:
      - summarize_long_conversations
      - reference_files_by_id
      - use_file_search_not_full_content
      - prune_irrelevant_history
      
    savings: 50%_token_reduction

  TOKEN_TRACKING:
    implementation: |
      class CostTracker:
        def __init__(self):
          self.calls = []
          
        def track(self, model, input_t, output_t):
          cost = self.calculate_cost(
            model, input_t, output_t
          )
          self.calls.append({
            'timestamp': now(),
            'model': model,
            'input_tokens': input_t,
            'output_tokens': output_t,
            'cost': cost
          })
          
        def daily_report(self):
          return pd.DataFrame(self.calls).groupby(
            'model'
          ).agg({
            'cost': 'sum',
            'input_tokens': 'sum',
            'output_tokens': 'sum'
          })
```

**Tags**: abstract, general

**Palavras-chave**: Optimization, Cost

**Origem**: unknown


---


<!-- VERSÍCULO 3/20 - marketplace_optimization_coverage_by_livro_20251113.md (26 linhas) -->

# Coverage by LIVRO

**Categoria**: marketplace_optimization
**Qualidade**: 0.87/1.00
**Data**: 20251113

## Conteúdo

| LIVRO | Chunks | Coverage |
|-------|--------|----------|
| LIVRO_01_FUNDAMENTALS | 697 | 66.6% |
| LIVRO_02_PRODUCT_MANAGEMENT | 122 | 11.7% |
| LIVRO_03_OPERATIONS | 49 | 4.7% |
| LIVRO_04_TECHNOLOGY | 128 | 12.2% |
| LIVRO_05_MARKETING | 39 | 3.7% |
| LIVRO_06_PAYMENTS | 12 | 1.1% |
| **TOTAL** | **1,047** | **100%** |

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Coverage, LIVRO

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 4/20 - marketplace_optimization_critical_notes_for_deletion_20251113.md (46 linhas) -->

# CRITICAL NOTES FOR DELETION

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

This document serves as the AUTHORITATIVE reference for all Python tooling knowledge in the repository.

**All individual script files can be safely deleted** as all logic, patterns, and capabilities are documented and preserved here:

**Scripts Eligible for Deletion (Knowledge Preserved):**
- All ADWS workflow files (adws/*.py) - 30+ files
- All consolidation scripts (root level) - 10+ files
- All distillation/enrichment scripts (root level) - 15+ files
- All knowledge artifact scripts - 5+ files
- All deployment/optimization scripts - 3+ files

**Scripts to RETAIN (Infrastructure):**
- `app/server/` - Active application code
- `ecommerce-canon/AGENTS/` - Core agents
- `.claude/hooks/` - Claude Code integration (keep)
- Test suites in `app/server/tests/` - Keep for validation

**Recovery Method:**
All deleted scripts are recoverable via git history:
```bash
git show HEAD~N:path/to/deleted/script.py > recovered_script.py
```

---

Generated: 2025-11-03
Total Knowledge Cards: 29
Scripts Documented: 95+
Knowledge Density: 100%

---

**Tags**: python, concrete

**Palavras-chave**: DELETION, NOTES, CRITICAL

**Origem**: unknown


---


<!-- VERSÍCULO 5/20 - marketplace_optimization_critical_preserved_patterns_20251113.md (40 linhas) -->

# CRITICAL PRESERVED PATTERNS

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Pattern: Consolidated Master Creation
```
Input: Multiple source files
Process: Extract → Validate → Index → Combine
Output: Single master document with table of contents
Recovery: Git history provides full recoverability
```

### Pattern: Knowledge Enrichment
```
Input: Base knowledge + additional data
Process: Merge → Extract → Relate → Embed
Output: Enriched knowledge base
Preservation: All source data maintained
```

### Pattern: Workflow Orchestration
```
Input: User request/trigger
Process: Parse → Route → Execute → Validate
Output: Structured result
Logging: Complete execution trace
```

---

**Tags**: python, architectural

**Palavras-chave**: PATTERNS, CRITICAL, PRESERVED

**Origem**: unknown


---


<!-- VERSÍCULO 6/20 - marketplace_optimization_current_active_structure_20251113.md (30 linhas) -->

# Current Active Structure

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

### Active Knowledge Base Versions
```
RAW_LEM_v1.1/              - CURRENT ACTIVE (Production)
RAW_LEM_v1.1_PADDLEOCR/    - EXPERIMENTAL (Active PaddleOCR variant)
RAW_BIBLE_v1/              - ACTIVE (Biblia framework)
LEM_knowledge_base/        - REFERENCE (Legacy index)
```

### Archived Versions
```
_archived/
  RAW_LEM_v1/              - ARCHIVED (Historical reference)
  RAW_LEM_v1_OPTIMIZED/    - ARCHIVED (Historical reference)
  README.md                - Archive documentation
```

**Tags**: abstract, general

**Palavras-chave**: Structure, Active, Current

**Origem**: unknown


---


<!-- VERSÍCULO 7/20 - marketplace_optimization_current_state_assessment_20251113.md (36 linhas) -->

# Current State Assessment

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Quality Metrics (Before Improvements)

| Metric | Score | Status |
|--------|-------|--------|
| **Overall Quality** | 74/100 | ⚠️ Good (needs improvement) |
| **Completeness** | 76/100 | ⚠️ Fair |
| **Consistency** | 72/100 | ⚠️ Fair |
| **Clarity** | 79/100 | ✅ Good |
| **Actionability** | 77/100 | ✅ Good |
| **Currency** | 92/100 | ✅ Excellent |
| **Discoverability** | 68/100 | ❌ Needs improvement |
| **Maintainability** | 64/100 | ❌ Needs improvement |

**Primary Weaknesses:**
1. Documentation duplication (GIT guides, Getting Started docs)
2. Missing centralized terminology (51 technical terms scattered)
3. No validation procedures post-setup
4. Language mixing (English + Portuguese) reduces scannability
5. No troubleshooting decision trees

---

**Tags**: general, implementation

**Palavras-chave**: Assessment, Current, State

**Origem**: unknown


---


<!-- VERSÍCULO 8/20 - marketplace_optimization_data_architecture_20251113.md (36 linhas) -->

# Data Architecture

**Categoria**: marketplace_optimization
**Qualidade**: 0.91/1.00
**Data**: 20251113

## Conteúdo

### GENESIS/RAW
Source documents before processing (36 files):
- RAW_001-RAW_036: Original knowledge documents
- Formats: .md, .txt
- Sizes: 4-54 KB each
- Total: ~436+ KB of raw knowledge

### GENESIS/PROCESSING
Processed semantic chunks:
- **chunks_000.json** - 29 distilled chunks with metadata
  - Each chunk contains:
    - Unique ID
    - Original text (extracted concept)
    - Entropy score (0-100)
    - Deus-vs-Todo classification
    - Suggested LIVRO/CAPITULO
    - Confidence score
    - Source tracking
    - Extraction timestamp

---

**Tags**: ecommerce, abstract

**Palavras-chave**: Data, Architecture

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 9/20 - marketplace_optimization_data_flow_orchestration_20251113.md (56 linhas) -->

# DATA FLOW & ORCHESTRATION

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### The Complete Journey (Document → Knowledge)

```
User uploads document
    ↓
+01_intake validates & routes
    ↓
Document → −01_capture/ (append-only storage)
    ↓
00_hub_infinito receives event
    ↓
Orchestrate Skills:
├─ skill_synthesizer()       (cascade summaries)
├─ skill_tokenizer()         (Fibonacci chunks)
├─ skill_purpose_extractor() (golden words)
├─ skill_qa_generator()      (5 Q&A pairs)
└─ skill_evaluator()         (quality score)
    ↓
Results aggregated → Trinity created:
├─ document.md           (human)
├─ document.llm.json     (machine)
└─ document.meta.json    (metadata)
    ↓
Saved to −02_build/
    ↓
Registered in −03_index/
    ↓
−05_storage archive
    ↓
−08_backup replication
    ↓
Score calculated & logged in monitoring.jsonl
    ↓
+05_delivery prepares outputs
    ↓
+08_feedback collects user rating
    ↓
Weights updated for next processing
```

---

**Tags**: lem, implementation

**Palavras-chave**: ORCHESTRATION, DATA, FLOW

**Origem**: unknown


---


<!-- VERSÍCULO 10/20 - marketplace_optimization_data_processing_20251113.md (53 linhas) -->

# Data & Processing

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### Knowledge Consolidation
**English:** Process of merging multiple knowledge sources, deduplicating entries (85.3% duplication removal), and creating unified indexed knowledge base.

**Portuguese:** Processo de fusão de múltiplas fontes de conhecimento, dedução de entradas (85,3% de remoção de duplicação) e criação de base de conhecimento unificada e indexada.

**Result:** 755 unique knowledge cards from 2+ initial sources.

**See:** 00_GENESIS_ENRICHMENT_COMECE_AQUI.md

---

### Knowledge Distillation
**English:** Process of extracting high-level insights and patterns from large knowledge documents, creating compact, actionable knowledge cards.

**Portuguese:** Processo de extração de insights e padrões de alto nível de grandes documentos de conhecimento, criando cartões de conhecimento compactos e acionáveis.

**Example:** 36-section Genesis document → 300+ distilled knowledge cards

**See:** distill_paddleocr_knowledge.py, LEM_knowledge_distillation.py

---

### JSONL Format
**English:** JSON Lines format - one JSON object per line, commonly used for streaming datasets and training pairs in machine learning.

**Portuguese:** Formato JSON Lines - um objeto JSON por linha, comumente usado para datasets de streaming e pares de treinamento em aprendizado de máquina.

**Example:**
```jsonl
{"type": "knowledge_extraction", "prompt": "...", "completion": "..."}
{"type": "keyword_extraction", "prompt": "...", "completion": "..."}
```

**Advantage:** Streamable, line-by-line processing; standard for fine-tuning APIs.

**See:** KNOWLEDGE_BASE_GUIDE.md section on Training Pair Structure

---

**Tags**: concrete, ecommerce, general

**Palavras-chave**: Data, Processing

**Origem**: unknown


---


<!-- VERSÍCULO 11/20 - marketplace_optimization_database_integration_optional_20251113.md (41 linhas) -->

# Database Integration (Optional)

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

To persist research results to your database:

```python
# In research_agent_routes.py, modify the endpoint:

from core.data_models import ResearchHistory  # Your model

@router.post("/start")
async def start_research(request: ResearchRequestDTO, db: Session):
    # ... existing code ...

    # Save to database
    db_record = ResearchHistory(
        request_id=research_request.request_id,
        product_name=request.product_name,
        research_type=request.research_type,
        status="in_progress",
        result_json=None  # Will be updated on completion
    )
    db.add(db_record)
    db.commit()

    # ... rest of code ...
```

---

**Tags**: concrete, general

**Palavras-chave**: Optional, Integration, Database

**Origem**: unknown


---


<!-- VERSÍCULO 12/20 - marketplace_optimization_database_requirements_20251113.md (37 linhas) -->

# Database Requirements

**Categoria**: marketplace_optimization
**Qualidade**: 0.91/1.00
**Data**: 20251113

## Conteúdo

### Knowledge Base (RAW_LEM_v1.1)

**Format:** JSON + JSONL
**No Database Server Needed:** All data stored as local files

**Required Storage:**
- `knowledge_base_consolidated.json` - 2 MB (755 knowledge cards)
- `training_data_consolidated.jsonl` - 1 MB (2,133+ training pairs)
- `idk_index.json` - 500 KB (semantic index)

**No External Database Required** - All operations work with local file storage.

### Optional: Vector Database (for future RAG)

For retrieval-augmented generation (RAG) integration:
- **Pinecone:** Cloud-based vector DB (free tier: 1M vectors)
- **Weaviate:** Self-hosted vector DB (requires Docker)
- **Milvus:** Open-source vector DB (Kubernetes-ready)

**Current Status:** Not required; local JSON-based retrieval sufficient for current use cases.

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Database, Requirements

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 13/20 - marketplace_optimization_decision_trees_20251113.md (81 linhas) -->

# Decision Trees

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

```yaml
when_to_use_which_model:
  input: task_characteristics
  
  decision:
    if complex_reasoning_required:
      if maximum_quality_critical:
        use: opus-4-1
      else:
        use: sonnet-4-5
        
    elif speed_critical:
      if quality_acceptable:
        use: haiku-4-5
      else:
        use: sonnet-4-5
        
    elif creative_task:
      use: sonnet-4-5
      temperature: 0.7-1.0
      
    else:
      use: haiku-4-5
      temperature: 0.0

when_to_use_which_tool:
  input: capability_needed
  
  decision:
    if need_external_integration:
      use: mcp_server
      
    elif need_specialized_workflow:
      use: skill
      
    elif need_focused_intelligence:
      use: subagent
      
    elif need_system_operation:
      use: bash_tool
      
    else:
      use: native_claude_capabilities

when_to_use_which_pattern:
  input: problem_class
  
  decision:
    if one_off_task:
      use: single_prompt
      
    elif repeated_task:
      use: template_or_skill
      
    elif multi_stage_task:
      use: adw_or_cascade
      
    elif continuous_task:
      use: piter_or_zte
      
    elif exploratory_task:
      use: interactive_mode
      
    else:
      use: multi_agent_swarm
```

**Tags**: architectural, general

**Palavras-chave**: Trees, Decision

**Origem**: unknown


---


<!-- VERSÍCULO 14/20 - marketplace_optimization_deliver_blazing_fast_ai_experiences_20251113.md (61 linhas) -->

# Deliver blazing fast AI experiences

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

Using either the new [Realtime API](https://platform.openai.com/docs/guides/realtime) or server-sent [streaming events](https://platform.openai.com/docs/guides/streaming-responses), you can build high performance, low-latency experiences for your users.

### Stream server-sent events from the API

#### JavaScript

```javascript
import { OpenAI } from "openai";
const client = new OpenAI();

const stream = await client.responses.create({
    model: "gpt-4.1",
    input: [
        {
            role: "user",
            content: "Say 'double bubble bath' ten times fast.",
        },
    ],
    stream: true,
});

for await (const event of stream) {
    console.log(event);
}
```

#### Python

```python
from openai import OpenAI
client = OpenAI()

stream = client.responses.create(
    model="gpt-4.1",
    input=[
        {
            "role": "user",
            "content": "Say 'double bubble bath' ten times fast.",
        },
    ],
    stream=True,
)

for event in stream:
    print(event)
```

**Tags**: concrete, general

**Palavras-chave**: blazing, Deliver, experiences, fast

**Origem**: unknown


---


<!-- VERSÍCULO 15/20 - marketplace_optimization_dependencies_setup_20251113.md (218 linhas) -->

# Dependencies & Setup

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### Required Python Version

**Python 3.12+** is required for all ADW scripts.

Check your version:
```bash
python --version
```

### Required Packages

All dependencies are managed via `uv` and defined in inline script metadata.

#### Core Dependencies (from pyproject.toml)

**Backend Server** (`app/server/pyproject.toml`):
```toml
[project]
requires-python = ">=3.12"
dependencies = [
    "fastapi==0.115.13",
    "uvicorn==0.34.3",
    "python-multipart==0.0.20",
    "openai>=1.3.0",
    "anthropic>=0.50.0",
    "pandas>=1.5.0",
    "python-dotenv==1.0.1",
]

[project.optional-dependencies]
dev = [
    "pytest==8.4.1",
]
```

#### ADW Script Dependencies

Each ADW script defines its dependencies inline:
```python
#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic"]
# ///
```

Common dependencies across ADW scripts:
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation and models
- `fastapi` - Webhook server (trigger_webhook.py)
- `uvicorn` - ASGI server (trigger_webhook.py)
- `schedule` - Task scheduling (trigger_cron.py)

---

### Installation Instructions

#### 1. Install System Dependencies

**macOS**:
```bash
# GitHub CLI
brew install gh

# Claude Code CLI
# Follow: https://docs.anthropic.com/en/docs/claude-code

# uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Ubuntu/Debian**:
```bash
# GitHub CLI
sudo apt install gh

# Claude Code CLI
# Follow: https://docs.anthropic.com/en/docs/claude-code

# uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows**:
```powershell
# GitHub CLI
winget install --id GitHub.cli

# Claude Code CLI
# Follow: https://docs.anthropic.com/en/docs/claude-code

# uv
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 2. Install Python Dependencies

**Backend Server**:
```bash
cd app/server
uv sync --all-extras
```

**ADW Scripts**:
No installation needed! Scripts use inline dependencies with `uv run`.

#### 3. Authenticate Services

**GitHub CLI**:
```bash
gh auth login
# Follow prompts to authenticate
```

**GitHub PAT** (optional, for different account):
```bash
export GITHUB_PAT="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**Anthropic API**:
```bash
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

---

### Configuration Steps

#### 1. Environment Variables

Create `.env` file in repository root:
```bash
# Copy sample
cp .env.sample .env

# Edit with your values
nano .env
```

Required variables:
```bash
# GitHub
GITHUB_REPO_URL="https://github.com/owner/repository"
GITHUB_PAT="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Optional

# Anthropic
ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Claude Code CLI
CLAUDE_CODE_PATH="/path/to/claude"  # Optional, defaults to "claude"

# Webhook (optional)
PORT=8001
GITHUB_WEBHOOK_SECRET="your-webhook-secret"

# R2 Storage (optional)
R2_ACCOUNT_ID="your-account-id"
R2_ACCESS_KEY_ID="your-access-key"
R2_SECRET_ACCESS_KEY="your-secret-key"
R2_BUCKET_NAME="your-bucket"
```

#### 2. Verify Installation

Run health check:
```bash
cd adws/
uv run adw_tests/health_check.py
```

Expected output:
```
🏥 ADW System Health Check
==================================================

✅ Environment Variables:
  ✅ GITHUB_REPO_URL is set
  ✅ ANTHROPIC_API_KEY is set
  ✅ CLAUDE_CODE_PATH is set

✅ Required Tools:
  ✅ gh CLI is installed (version 2.40.1)
  ✅ claude CLI is installed
  ✅ git is installed (version 2.43.0)

✅ GitHub Authentication:
  ✅ gh is authenticated

==================================================
🎉 All checks passed! System is ready.
```

#### 3. Test First Workflow

```bash
# Create test issue in your repo
gh issue create --title "Test ADW" --body "This is a test issue"

# Process it
cd adws/
uv run adw_plan_build_iso.py <issue-number>
```

---

**Tags**: concrete, general

**Palavras-chave**: Dependencies, Setup

**Origem**: unknown


---


<!-- VERSÍCULO 16/20 - marketplace_optimization_deployment_20251113.md (51 linhas) -->

# Deployment

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Docker Integration

```dockerfile
# In app/Dockerfile

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ /app/

ENV PYTHONUNBUFFERED=1
ENV ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

EXPOSE 8000

CMD ["uvicorn", "server.server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Checklist

- [ ] Set `LOG_LEVEL=WARNING` in production
- [ ] Use HTTPS for API endpoints
- [ ] Add authentication to `/api/research` endpoints
- [ ] Configure CORS appropriately
- [ ] Set up database persistence
- [ ] Add request rate limiting
- [ ] Enable metrics/monitoring
- [ ] Set up error alerting
- [ ] Test with load generation
- [ ] Document API for clients

---

**Tags**: general, intermediate

**Palavras-chave**: Deployment

**Origem**: unknown


---


<!-- VERSÍCULO 17/20 - marketplace_optimization_deployment_steps_20251113.md (67 linhas) -->

# Deployment Steps

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### 1. Backup Existing System
```bash
cp -r RAW_LEM_v1.1 RAW_LEM_v1.1.backup.$(date +%Y%m%d_%H%M%S)
```

### 2. Verify Package Contents
```bash
ls -lh RAW_LEM_v1.1/knowledge_base/
ls -lh RAW_LEM_v1.1/deployment_artifacts/
cat RAW_LEM_v1.1/DEPLOYMENT_MANIFEST.json
```

### 3. Deploy Knowledge Base
Knowledge base is already integrated in:
- RAW_LEM_v1.1/knowledge_base/semantic_paddleocr.json
- RAW_LEM_v1.1/knowledge_base/training_data_combined.jsonl
- RAW_LEM_v1.1/knowledge_base/knowledge_cards_paddleocr.json

### 4. Deploy Scripts
Copy distillation scripts if needed:
```bash
cp distill_fast.py scripts/
cp generate_training_pairs.py scripts/
cp select_master_files.py scripts/
```

### 5. Update Systems
Update your systems to use new knowledge base:

**For RAG Systems:**
```python
import json
with open('RAW_LEM_v1.1/knowledge_base/semantic_paddleocr.json') as f:
    knowledge = json.load(f)
```

**For LLM Fine-tuning:**
```bash
# Use training_data_combined.jsonl with OpenAI API
openai.FineTuningJob.create(
    training_file="RAW_LEM_v1.1/knowledge_base/training_data_combined.jsonl",
    model="gpt-3.5-turbo"
)
```

### 6. Validate Deployment
```bash
python validate_deployment.py RAW_LEM_v1.1/
```

### 7. Monitor & Report
Check logs and verify all systems operational

**Tags**: concrete, general

**Palavras-chave**: Deployment, Steps

**Origem**: unknown


---


<!-- VERSÍCULO 18/20 - marketplace_optimization_deployment_strategies_20251113.md (96 linhas) -->

# Deployment Strategies

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

```yaml
environments:
  DEVELOPMENT:
    model: haiku-4-5  # Fast iteration
    mode: interactive
    validation: loose
    
  STAGING:
    model: sonnet-4-5  # Balance
    mode: automated
    validation: strict
    
  PRODUCTION:
    model: [haiku, sonnet, opus]  # Task-dependent
    mode: zte_where_appropriate
    validation: comprehensive
    monitoring: intensive

rollout_phases:
  PHASE_1_PILOT:
    scope: single_team
    model: sonnet-4-5
    duration: 2_weeks
    metrics: collect_feedback
    
  PHASE_2_EXPANSION:
    scope: multiple_teams
    model: task_appropriate
    duration: 1_month
    metrics: success_rate_cost
    
  PHASE_3_PRODUCTION:
    scope: all_teams
    model: optimized_selection
    duration: ongoing
    metrics: full_observability

ci_cd_integration:
  github_actions:
    trigger: [pull_request, push]
    
    jobs:
      code_review:
        agent: reviewer
        model: sonnet-4-5
        action: comment_on_pr
        
      test_generation:
        agent: tester
        model: haiku-4-5
        action: add_missing_tests
        
      documentation:
        agent: documenter
        model: haiku-4-5
        action: update_docs
        
  headless_execution:
    format: json_output
    integration: parse_results_in_ci
    decision: pass_or_fail_build

disaster_recovery:
  failover:
    primary: anthropic_api
    fallback: anthropic_bedrock_or_vertex
    
  rate_limit_handling:
    strategy: exponential_backoff
    max_retries: 3
    fallback: queue_for_batch
    
  error_recovery:
    transient_errors: retry
    invalid_requests: alert_developer
    quota_exceeded: switch_workspace
```

---

# APPENDIX: QUICK REFERENCE

**Tags**: concrete, general

**Palavras-chave**: Deployment, Strategies

**Origem**: unknown


---


<!-- VERSÍCULO 19/20 - marketplace_optimization_deus_vs_todo_classification_20251113.md (34 linhas) -->

# Deus-vs-Todo Classification

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

Knowledge has been classified by universality:

**Deus (Universal - 67% avg):**
- Applies across all e-commerce contexts
- Not dependent on specific implementation
- Foundational principles and concepts

**Todo (Contextual - 16% avg):**
- Depends on business context
- Situational guidance and practices
- Implementation-specific knowledge

**Distribution:**
- 41% Purely Abstract (Deus >80%)
- 28% Mostly Abstract (Deus 60-80%)
- 21% Balanced (Deus 40-60%)
- 10% Mostly Contextual (Deus <40%)

---

**Tags**: abstract, general

**Palavras-chave**: Deus, Todo, Classification

**Origem**: unknown


---


<!-- VERSÍCULO 20/20 - marketplace_optimization_development_20251113.md (32 linhas) -->

# Development

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Backend Commands
```bash
cd app/server
uv run python server.py      # Start server with hot reload
uv run pytest               # Run tests
uv add <package>            # Add package to project
uv remove <package>         # Remove package from project
uv sync --all-extras        # Sync all extras
```

### Frontend Commands
```bash
cd app/client
bun run dev                 # Start dev server
bun run build              # Build for production
bun run preview            # Preview production build
```

**Tags**: general, intermediate

**Palavras-chave**: Development

**Origem**: unknown


---


<!-- FIM DO CAPÍTULO 33 -->
<!-- Total: 20 versículos, 1198 linhas -->
