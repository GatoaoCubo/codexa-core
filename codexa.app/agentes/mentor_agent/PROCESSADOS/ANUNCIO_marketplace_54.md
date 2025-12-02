# LIVRO: Marketplace
## CAPÍTULO 54

**Versículos consolidados**: 18
**Linhas totais**: 1200
**Gerado em**: 2025-11-13 18:45:49

---


<!-- VERSÍCULO 1/18 - marketplace_optimization_recommended_workflows_20251113.md (122 linhas) -->

# Recommended Workflows

**Categoria**: marketplace_optimization
**Qualidade**: 0.95/1.00
**Data**: 20251113

## Conteúdo

### Workflow 1: Starting a New Feature

```bash
# 1. Create specification
cat > specs/issue-feature-myfeature.md << EOF
# Feature: My Feature
Description...
EOF

# 2. Create GitHub issue from spec
gh issue create --title "Feature: My Feature" --body-file specs/issue-feature-myfeature.md

# 3. Let ADW process it
cd adws
uv run adw_sdlc_iso.py <issue-number> <new-worktree-id>

# 4. Review PR created by ADW
gh pr view <pr-number>

# 5. Merge when ready
gh pr merge <pr-number>
```

### Workflow 2: Adding New Knowledge to KB

```bash
# 1. Create knowledge source
cat > new_knowledge.md << EOF
# New Knowledge
Content...
EOF

# 2. Run enrichment script
python scripts/enrich_with_custom_knowledge.py --input new_knowledge.md

# 3. Validate output
python -c "import json; print(json.load(open('RAW_LEM_v1.1/ENRICHMENT_REPORT.json')))"

# 4. Commit changes
git add RAW_LEM_v1.1/
git commit -m "feat: add new knowledge to KB"
```

### Workflow 3: Integrating PaddleOCR Knowledge

```bash
# 1. Run distillation
python scripts/distill_paddleocr_knowledge.py

# 2. Review output
cat RAW_LEM_v1.1_PADDLEOCR/DISTILLATION_SUMMARY.json

# 3. Deduplicate
python scripts/select_master_files.py RAW_LEM_v1.1_PADDLEOCR/duplicates_report.json

# 4. Generate training pairs
python scripts/generate_training_pairs.py RAW_LEM_v1.1_PADDLEOCR

# 5. Integrate with main KB
cp RAW_LEM_v1.1_PADDLEOCR/semantic_map.json RAW_LEM_v1.1/knowledge_base/
cat RAW_LEM_v1/knowledge_base/training_data.jsonl \
    training_pairs_paddleocr.jsonl \
    > RAW_LEM_v1.1/knowledge_base/training_data_combined.jsonl

# 6. Commit integration
git add RAW_LEM_v1.1/
git commit -m "feat: integrate PaddleOCR knowledge into KB"
```

### Workflow 4: Deploying Web Application

```bash
# 1. Setup environment
cd app/server
cp .env.sample .env
# Edit .env with API keys

# 2. Install dependencies
cd app/server && uv sync --all-extras
cd app/client && bun install

# 3. Run tests
cd app/server && uv run pytest

# 4. Start services
./scripts/start.sh

# 5. Verify
curl http://localhost:8000/api/health
curl http://localhost:5173
```

### Workflow 5: Creating Documentation

```bash
# 1. Identify documentation need
# Example: New feature needs guide

# 2. Create in appropriate location
# - Root: High-level guides (INTEGRATION_GUIDE.md)
# - ai_docs: AI-specific
# - app_docs: Application-specific
# - specs: Specifications

# 3. Follow template structure
cat > NEW_GUIDE.md << EOF
# GUIDE NAME

**Tags**: ecommerce, concrete

**Palavras-chave**: Recommended, Workflows

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 2/18 - marketplace_optimization_references_20251113.md (185 linhas) -->

# References

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

- [Paper relevante](link)
- [Tutorial externo](link)
- [Código-fonte](github-link)
```

### 3.2 JSON Schema para Structured Data

**Quando usar JSON em vez de Markdown:**
- ✅ Dados estruturados precisos (APIs, configs)
- ✅ Validação automática necessária
- ✅ Parsing programático frequente
- ✅ Schema evolution tracking

**Exemplo: Documentação de API como JSON Schema**

```json
{
  "api": "SFTTrainer",
  "version": "2.0",
  "type": "class",
  "description": "Trainer para Supervised Fine-Tuning de LLMs",
  
  "constructor": {
    "signature": "SFTTrainer(model, args, train_dataset, eval_dataset, tokenizer)",
    "parameters": [
      {
        "name": "model",
        "type": "PreTrainedModel",
        "required": true,
        "description": "Modelo base a ser fine-tunado",
        "example": "AutoModelForCausalLM.from_pretrained('gpt2')"
      },
      {
        "name": "args",
        "type": "TrainingArguments",
        "required": true,
        "description": "Configurações de treinamento",
        "default_example": {
          "output_dir": "./results",
          "num_train_epochs": 3,
          "per_device_train_batch_size": 4,
          "learning_rate": 2e-5
        },
        "reference": "#TrainingArguments"
      }
    ]
  },
  
  "methods": [
    {
      "name": "train",
      "signature": "train() -> TrainOutput",
      "description": "Executa loop de treinamento",
      "returns": {
        "type": "TrainOutput",
        "fields": {
          "global_step": "int - Número total de steps",
          "training_loss": "float - Loss médio final",
          "metrics": "dict - Métricas adicionais"
        }
      },
      "example": "output = trainer.train()",
      "complexity": {
        "time": "O(epochs * dataset_size / batch_size)",
        "space": "O(model_size + batch_size * seq_length)"
      }
    }
  ],
  
  "usage_patterns": [
    {
      "name": "Basic Training",
      "scenario": "Fine-tune modelo em dataset simples",
      "code": "trainer = SFTTrainer(model, args, dataset)\ntrainer.train()",
      "when_to_use": "Dataset pequeno (<10k samples), única GPU"
    },
    {
      "name": "Distributed Training",
      "scenario": "Treinar em múltiplas GPUs",
      "code": "# Usar com accelerate launch\ntrainer = SFTTrainer(...)\ntrainer.train()",
      "when_to_use": "Dataset grande, múltiplas GPUs disponíveis"
    }
  ],
  
  "related_components": [
    {"name": "TrainingArguments", "type": "config", "relationship": "dependency"},
    {"name": "DPOTrainer", "type": "class", "relationship": "alternative"},
    {"name": "Trainer", "type": "class", "relationship": "parent"}
  ]
}
```

**Vantagens para LLMs:**

1. **Parsing determinístico**: JSON é não-ambíguo
2. **Schema validation**: Garante estrutura consistente
3. **Queryability**: Fácil extrair campos específicos
4. **Composability**: JSONs podem referenciar outros via IDs

### 3.3 Código Auto-Documentado

**Princípio:** Código bem escrito É documentação

**Exemplo de Código que Documenta a Si Mesmo:**

```python
from dataclasses import dataclass
from typing import Optional, List
from enum import Enum

class OptimizerType(Enum):
    """Tipos de otimizadores suportados"""
    ADAM = "adam"
    ADAMW = "adamw"
    SGD = "sgd"

@dataclass
class TrainingConfig:
    """
    Configuração para treinamento de LLM.
    
    Attributes:
        learning_rate: Taxa de aprendizado inicial. Valores típicos: 1e-5 a 1e-4
        batch_size: Tamanho do batch por dispositivo. Maior = mais rápido mas mais memória
        num_epochs: Número de épocas de treinamento. Típico: 3-5 para fine-tuning
        optimizer: Tipo de otimizador. AdamW recomendado para a maioria dos casos
        warmup_steps: Steps de warmup linear. Recomendado: 10% do total de steps
        
    Example:
        >>> config = TrainingConfig(
        ...     learning_rate=2e-5,
        ...     batch_size=8,
        ...     num_epochs=3
        ... )
    """
    learning_rate: float = 2e-5
    batch_size: int = 8
    num_epochs: int = 3
    optimizer: OptimizerType = OptimizerType.ADAMW
    warmup_steps: Optional[int] = None
    
    def __post_init__(self):
        """Validação e ajustes automáticos"""
        if self.warmup_steps is None:
            # Heurística: 10% de warmup é um bom padrão
            total_steps = self.estimate_total_steps()
            self.warmup_steps = int(0.1 * total_steps)
    
    def estimate_total_steps(self) -> int:
        """
        Estima número total de steps de treinamento.
        
        Returns:
            int: Número estimado de gradient updates
            
        Note:
            Assume dataset de 10k samples. Para dataset real,
            calcular como: len(dataset) * num_epochs / batch_size
        """
        ASSUMED_DATASET_SIZE = 10_000
        return (ASSUMED_DATASET_SIZE * self.num_epochs) // self.batch_size


class Trainer:
    """
    Trainer para Supervised Fine-Tuning de LLMs.
    
    Este trainer implementa o loop de treinament

[... content truncated ...]

**Tags**: concrete, general

**Palavras-chave**: References

**Origem**: unknown


---


<!-- VERSÍCULO 3/18 - marketplace_optimization_referência_rápida_20251113.md (27 linhas) -->

# Referência Rápida

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

| Comando | O que faz |
|---------|-----------|
| `git push origin main` | Envia branch main para remoto |
| `git push -u origin main` | Envia e configura tracking |
| `git push origin --all` | Envia todas as branches |
| `git push origin --delete branch` | Deleta branch remota |
| `git push origin main --force` | ⚠️ Sobrescreve remoto |
| `git push --tags` | Envia todas as tags |
| `git fetch origin` | Baixa atualizações sem fazer merge |
| `git pull origin main` | Fetch + merge em um comando |

---

**Tags**: general, intermediate

**Palavras-chave**: Referência, Rápida

**Origem**: unknown


---


<!-- VERSÍCULO 4/18 - marketplace_optimization_regras_de_otimização_20251113.md (22 linhas) -->

# Regras de Otimização

**Categoria**: marketplace_optimization
**Qualidade**: 0.87/1.00
**Data**: 20251113

## Conteúdo

- Marca entre 115 e 120 caracteres (densidade máxima de keywords)
- Modelo entre 115 e 120 caracteres (foco absoluto em conversão)
- Títulos ≤ 60 caracteres cada (3 versões A/B)
- ZERO stop words em títulos - apenas keywords que convertem
- Mínimo 8 keywords relevantes por campo
- Keywords são enriquecidas automaticamente com a pesquisa SEO
- Estrutura StoryBrand obrigatória na descrição

**Tags**: ecommerce, intermediate

**Palavras-chave**: Regras, Otimização

**Origem**: _CONSOLIDATED_ECOMMERCE_RAW_FROM_GIT.md


---


<!-- VERSÍCULO 5/18 - marketplace_optimization_related_documents_20251113.md (24 linhas) -->

# Related Documents

**Categoria**: marketplace_optimization
**Qualidade**: 0.87/1.00
**Data**: 20251113

## Conteúdo

- **BIBLIA_FRAMEWORK.md** - 8 axioms and computational theology
- **KNOWLEDGE_BASE_GUIDE.md** - KB structure and usage
- **REPOSITORY_STRUCTURE.md** - Directory organization
- **README.md** - Project overview
- **START_HERE.md** - Quick start guide
- **compose_prompts.md** - 5-chunk prompt composition framework
- **TROUBLESHOOTING.md** - Common issues and solutions (see for next steps)

---

**Tags**: ecommerce, abstract

**Palavras-chave**: Related, Documents

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 6/18 - marketplace_optimization_related_files_20251113.md (29 linhas) -->

# Related Files

**Categoria**: marketplace_optimization
**Qualidade**: 0.87/1.00
**Data**: 20251113

## Conteúdo

- `ecommerce-canon/` - Root directory
- `ecommerce-canon/DISTILLATION_REPORT.md` - Detailed analysis
- `ecommerce-canon/AGENTS/distiller.py` - Distillation engine
- `ecommerce-canon/create_versiculos.py` - Chunk processor
- `ecommerce-canon/GENESIS/` - Source and processed knowledge
- `ecommerce-canon/LIVRO_*/` - Organized knowledge units

---

**Last Updated:** 2025-11-02
**Maintained by:** LEM CANON System


======================================================================

**Tags**: ecommerce, implementation

**Palavras-chave**: Related, Files

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 7/18 - marketplace_optimization_relevant_files_20251113.md (44 linhas) -->

# Relevant Files

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### Directories to Analyze & Organize
- `RAW_LEM_v1.1/` - 168 MB (contains duplicates in deployment_artifacts/)
- `RAW_LEM_v1.1_PADDLEOCR/` - 80 MB (potential version duplication)
- `RAW_LEM_v1/` - 177 KB (old version)
- `RAW_LEM_v1_OPTIMIZED/` - 192 KB (variant version)
- `LEM_knowledge_base/` - 133 KB (unclear if current)
- `knowledge_artifacts_v1/` - 4.5 MB (potential consolidation)
- `INTEGRATION_REPORT/` - 100 KB (overlaps with docs)
- `RAW_BIBLE_v1/` - 172 KB (theological framework)
- `app/` - 203 MB (application code - needs minor cleanup)
- `app/server/db/` - Database and backup files
- `README.md` - Root documentation

### Key Documentation Files to Consolidate (50+ files)
- Multiple START_HERE variants (7 files)
- Multiple final project completion reports (15+ files)
- Multiple integration guides (6 files)
- Multiple knowledge base guides (5 files)
- Multiple PaddleOCR documentation (5 files)
- Multiple Biblia framework docs (5 files)

### New Files to Create
- `START_HERE.md` - Single entry point for new developers
- `PROJECT_COMPLETION_SUMMARY.md` - Unified final summary
- `INTEGRATION_GUIDE.md` - Unified integration documentation
- `KNOWLEDGE_BASE_GUIDE.md` - Unified KB usage guide
- `PADDLEOCR_GUIDE.md` - Unified PaddleOCR documentation
- `REPOSITORY_STRUCTURE.md` - Clear directory structure guide
- `VERSIONS_STATUS.md` - Version status and deprecation info

**Tags**: abstract, general

**Palavras-chave**: Files, Relevant

**Origem**: unknown


---


<!-- VERSÍCULO 8/18 - marketplace_optimization_remaining_high_priority_improvements_20251113.md (174 linhas) -->

# Remaining High-Priority Improvements

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### PRIORITY 1: Consolidate Getting Started Documentation

**Current State:**
- START_HERE.md (86/100 quality)
- 00_LEIA_PRIMEIRO_RESUMO.txt (63/100 quality)
- 00_GENESIS_ENRICHMENT_COMECE_AQUI.md (82/100 quality)
- 3 docs covering overlapping content

**Recommended Action:**
Create unified `GETTING_STARTED.md` serving all audiences:

```
GETTING_STARTED.md (Plan)
├─ Section 1: Choose Your Path (3-5 minutes)
│  ├─ Path A: Familiar with Python/Git? → Fast track
│  ├─ Path B: New to development? → Guided setup
│  └─ Path C: Only need specific component? → Component guide
│
├─ Section 2: Prerequisites Check
│  └─ SYSTEM_REQUIREMENTS.md checklist (link)
│
├─ Section 3: Step-by-Step Installation
│  └─ Clone → Setup venv → Install → Configure → Validate
│
├─ Section 4: Verify Setup Success
│  └─ Links to validation scripts
│
├─ Section 5: What's Next?
│  └─ First tasks by role (Developer, Researcher, Operator)
│
└─ Section 6: Help & Support
   └─ TROUBLESHOOTING.md link + FAQ
```

**Benefits:**
- Single source of truth for new users
- Reduced cognitive load
- Easier to maintain and update
- Better SEO/discoverability

**Estimated Effort:** 3 hours
**Priority:** HIGH
**Expected Quality Improvement:** +12 points (getting started avg 77 → 89)

**Action:** Consolidate into single document, deprecate old 3 docs

---

### PRIORITY 2: Consolidate Git Documentation

**Current State:**
- GIT_PUSH_GUIA.md (73/100 quality)
- GUIA_GIT_COMMITS.md (71/100 quality)
- 75% content overlap
- Language mixing (Portuguese + English)

**Recommended Action:**
Create single `GIT_WORKFLOW_GUIDE.md`:

```
GIT_WORKFLOW_GUIDE.md (Unified)
├─ Part 1: Quick Reference (1 page)
│  └─ Common commands table
│
├─ Part 2: Complete Git Workflow
│  ├─ Commit workflow
│  ├─ Push workflow
│  ├─ Branching strategy
│  └─ Pull request process
│
├─ Part 3: Best Practices
│  ├─ Commit message conventions
│  ├─ Code review standards
│  └─ Conflict resolution
│
├─ Part 4: Error Handling
│  ├─ Undo commits
│  ├─ Fix push mistakes
│  └─ Restore deleted files
│
└─ Part 5: Advanced (Worktrees, rebasing, etc.)
```

**Benefits:**
- Eliminates duplication
- Clearer workflow progression
- Easier to keep in sync
- Reduces maintenance burden

**Estimated Effort:** 2 hours
**Priority:** HIGH
**Expected Quality Improvement:** +10 points (Git avg 72 → 82)

**Action:** Merge into single doc; deprecate GIT_PUSH_GUIA.md and GUIA_GIT_COMMITS.md

---

### PRIORITY 3: Add Code Block Standardization

**Current State:**
- Code blocks inconsistently labeled
- Mix of bash, python, json, pseudo-code
- No syntax highlighting guidance
- Confusion about which language

**Recommended Action:**
Establish markdown code block standard:

```markdown
# ✅ CORRECT - Clear language label
\`\`\`bash
python3 --version
git status
\`\`\`

# ✗ WRONG - No language specified
\`\`\`
python3 --version
\`\`\`

# ✅ CORRECT - With output
\`\`\`bash
$ python3 --version
Python 3.12.0
\`\`\`

# ✅ CORRECT - With explanation
\`\`\`python
# Check API connection
client = Anthropic()
response = client.messages.create(...)
\`\`\`
```

**Scope of Work:**
1. Audit all 44 root docs for code block compliance
2. Standardize formatting across docs
3. Add language labels to unlabeled blocks
4. Add output examples where helpful

**Estimated Effort:** 3 hours
**Priority:** MEDIUM
**Expected Quality Improvement:** +5 points (readability)

**Action:** Create MARKDOWN_STYLE_GUIDE.md, apply to all docs

---

### PRIORITY 4: Add Validation Checklists to Core Docs

**Current State:**
- Documentation explains WHAT to do
- Missing: "How do I verify it worked?"
- Users unsure if setup successful

**Recommended Action:**
Add "Verify Your Setup" section to each major doc:

```markdown

**Tags**: concrete, general

**Palavras-chave**: Improvements, High, Priority, Remaining

**Origem**: unknown


---


<!-- VERSÍCULO 9/18 - marketplace_optimization_reorder_points_and_automated_replenishment_20251113.md (37 linhas) -->

# Reorder Points and Automated Replenishment

**Categoria**: marketplace_optimization
**Qualidade**: 0.91/1.00
**Data**: 20251113

## Conteúdo

A reorder point (ROP) is the inventory level that triggers a purchase order.

**ROP Formula:**
ROP = (Average Daily Usage × Lead Time) + Safety Stock

Using our previous example:
ROP = (50 × 14) + 700 = 1,400 units

When inventory drops below 1,400 units, the system automatically creates a purchase order.

### Reorder Quantity (EOQ)

Economic Order Quantity optimizes order size to minimize total inventory costs:

**EOQ = √(2 × D × S / H)**

Where:
- D = annual demand
- S = cost per order
- H = holding cost per unit

Larger orders reduce ordering frequency but increase holding costs. Smaller orders reduce holding costs but increase ordering frequency. EOQ finds the sweet spot.

**Tags**: ecommerce, concrete

**Palavras-chave**: Reorder, Points, Automated, Replenishment

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 10/18 - marketplace_optimization_reports_documentation_20251113.md (32 linhas) -->

# Reports & Documentation

**Categoria**: marketplace_optimization
**Qualidade**: 0.87/1.00
**Data**: 20251113

## Conteúdo

### DISTILLATION_REPORT.md
Complete analysis of the knowledge distillation process:
- Document processing summary
- Entropy distribution analysis
- Coverage by LIVRO
- Quality metrics
- Processing pipeline details
- Deus-vs-Todo analysis

### create_versiculos.py
Python script that transforms chunks into VERSÍCULOS:
- Chunk filtering by entropy
- Metadata extraction
- Hierarchical file organization
- Versículo generation

---

**Tags**: ecommerce, concrete

**Palavras-chave**: Reports, Documentation

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 11/18 - marketplace_optimization_repository_overview_20251113.md (32 linhas) -->

# Repository Overview

**Categoria**: marketplace_optimization
**Qualidade**: 0.91/1.00
**Data**: 20251113

## Conteúdo

### Project Name
**TAC-7**: Natural Language SQL Interface with AI-Powered Knowledge Distillation and Agent Orchestration

### Primary Components
1. **Web Application** (Natural Language → SQL)
2. **Knowledge Bases** (LEM, Genesis, Biblia, PaddleOCR)
3. **ADW System** (AI Developer Workflow for GitHub automation)
4. **Agent Orchestration** (Multi-agent systems)
5. **Documentation** (Comprehensive guides)

### Repository Stats
- **Total Directories:** 50+
- **Primary Languages:** Python, TypeScript, Markdown
- **Main Frameworks:** FastAPI, Vite, PaddlePaddle
- **Documentation:** 100+ MD files

---

**Tags**: ecommerce, abstract

**Palavras-chave**: Repository, Overview

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 12/18 - marketplace_optimization_repository_structure_20251113.md (37 linhas) -->

# Repository Structure

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

```
ecommerce-canon/
├── GENESIS/
│   ├── RAW/              [36 source documents]
│   └── PROCESSING/       [chunks_000.json - 29 chunks]
├── LIVRO_01_FUNDAMENTALS/
│   └── CAPITULO_01/      [23 VERSÍCULOS]
├── LIVRO_02_PRODUCT_MANAGEMENT/
│   └── CAPITULO_01/      [2 VERSÍCULOS]
├── LIVRO_03_OPERATIONS/
│   └── CAPITULO_01/      [2 VERSÍCULOS]
├── LIVRO_04_TECHNOLOGY/
│   └── CAPITULO_01/      [2 VERSÍCULOS]
├── AGENTS/
│   └── distiller.py      [v2.1.0]
├── create_versiculos.py  [v1.0.0]
├── INDEX.md              [Navigation guide]
├── DISTILLATION_REPORT.md [Complete analysis]
└── QUICK_START.md        [Getting started]
```

---

**Tags**: general, implementation

**Palavras-chave**: Structure, Repository

**Origem**: unknown


---


<!-- VERSÍCULO 13/18 - marketplace_optimization_research_framework_20251113.md (209 linhas) -->

# Research Framework

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### CARD-010: Framework de Pesquisa Tática (7 Fases)
**KEYWORDS:** `research|methodology|marketplace|workflow`

**Estrutura das 7 Fases Obrigatórias:**

```
FASE 1: INTAKE & VALIDAÇÃO
├─ Validação de brief contra schema
├─ Identificação de lacunas
└─ Contextualização de marketplace

FASE 2: GERAÇÃO DE TAXONOMIA
├─ Head terms (conceitos centrais)
├─ Longtails (atributos + benefícios)
├─ Sinônimos e variações morfológicas
└─ Ocasião, contexto, persona

FASE 3: COLETA INTELIGENTE (Web Search)
├─ INBOUND: Mercados nativos BR (7 marketplaces)
├─ OUTBOUND: SERP geral + UGC + Sociais
├─ Concorrência: Análise comparativa estruturada
└─ Compliance: ReclameAqui + políticas

FASE 4: ANÁLISE & CONSOLIDAÇÃO
├─ Benchmark de concorrentes
├─ Padrões de linguagem eficaz
├─ SEO Inbound vs Outbound
└─ Estratégias vencedoras + gaps

FASE 5: OUTPUT ESTRUTURADO
└─ research_notes (17 blocos determinísticos)

FASE 6: VALIDAÇÃO & QUALIDADE
├─ Confidence scoring
├─ Gap detection
└─ Quality assessment

FASE 7: ITERAÇÃO & REFINAMENTO
├─ Feedback loop
├─ A/B testing de estratégias
└─ Continuous improvement
```

**Como Aplicar:**
1. **Nunca pular fases** - cada fase depende da anterior
2. Usar templates de consulta padronizados
3. Documentar tudo em research_notes (17 blocos)
4. Aplicar confidence scores em cada seção

**Confidence:** 96% | **Weight:** 5 | **Source:** RESEARCH_FRAMEWORK_ANALYSIS.md

---

### CARD-011: Heurísticas de Priorização de Research
**KEYWORDS:** `research|scoring|prioritization`

**Critérios de Scoring (0-100):**

| Critério | Peso | Descrição |
|----------|------|-----------|
| Presença no brief e regras internas | 35% | Alinhamento com objetivos |
| Clareza da intenção de compra | 25% | Buyer intent detectado |
| Potencial de variação longtail | 20% | Expansão de keywords |
| Aderência às políticas | 15% | Compliance e segurança |
| Volume + recorrência observados | 5% | Validação por dados |

**Fórmula de Scoring:**
```
score_total = (
    brief_alignment * 0.35 +
    buyer_intent * 0.25 +
    longtail_potential * 0.20 +
    compliance * 0.15 +
    volume_frequency * 0.05
)
```

**Como Aplicar:**
1. Classificar cada head term com score 0-100
2. Priorizar pesquisa pelos termos de maior score
3. Alocar tempo proporcionalmente ao score

**Confidence:** 92% | **Weight:** 4 | **Source:** RESEARCH_FRAMEWORK_ANALYSIS.md

---

### CARD-012: Cobertura Obrigatória de Fontes (7 Marketplaces BR)
**KEYWORDS:** `research|marketplaces|web-search|brasil`

**INBOUND - Mercados Nativos BR (7 obrigatórios):**
1. `site:mercadolivre.com.br`
2. `site:shopee.com.br`
3. `site:magazineluiza.com`
4. `site:amazon.com.br`
5. `site:americanas.com.br`
6. `site:casasbahia.com.br`
7. `site:shop.tiktok.com`

**OUTBOUND - Canais de Descoberta:**
- **SERP Geral:** Google search (sem site operator)
- **UGC Social Obrigatório:**
  - `site:youtube.com` (reviews + demos)
  - `site:tiktok.com` (trend analysis + unboxings)
  - `site:instagram.com` (lifestyle + UGC)

**ANÁLISE DE RISCO:**
- `site:reclameaqui.com.br` (reclamações, pós-venda, claims falsos)

**Padrão de Consulta:**
```
site:[marketplace] "[head_term]"
site:[marketplace] "[longtail]"
```

**Templates de Consulta:**
```
# Outbound/SERP + Mídia
{{head_term}} guia de compra
{{head_term}} review
{{head_term}} melhores
{{head_term}} perguntas frequentes
{{head_term}} vs {{alternativa}}

# Inbound Marketplaces
site:mercadolivre.com.br "{{head_term}}"
site:shopee.com.br "{{head_term}}"

# Sociais + UGC
site:youtube.com "{{head_term}}" review Brasil
site:tiktok.com "{{head_term}}" Brasil
```

**Como Aplicar:**
1. Sempre pesquisar nos 7 marketplaces obrigatórios
2. Usar padrão de consulta com site operator
3. Documentar source de cada insight
4. Validar compliance no ReclameAqui

**Confidence:** 98% | **Weight:** 5 | **Source:** RESEARCH_FRAMEWORK_ANALYSIS.md

---

### CARD-013: Estrutura de research_notes (17 Blocos)
**KEYWORDS:** `research|output|template|structure`

**Formato Determinístico - 17 Blocos Obrigatórios:**

```markdown
[LACUNAS DO BRIEF]
campo_faltante ... Não informado ou [SUGESTÃO]

[HEAD TERMS PRIORITÁRIOS]
termo_1 (score: 95)
termo_2 (score: 88)

[LONGTAILS]
head + atributo_1
head + atributo_2

[SINÔNIMOS E VARIAÇÕES MORFOLÓGICAS]
variação_1
variação_2

[TERMO CONTEXTUAL E OCASIÃO]
ocasião | contexto | público_alvo | ambiente | frequência | estilo

[DORES DO PÚBLICO]
dor_1 (fonte: site:youtube.com reviews)
dor_2 (fonte: site:reclameaqui.com.br)

[GANHOS DESEJADOS]
ganho_1 (evidência: XX% mencionam)
ganho_2

[OBJEÇÕES E RESPOSTAS]
P: pergunta_curta
R: resposta_curta

[PROVAS E EVIDÊNCIAS DISPONÍVEIS]
tipo_prova | descrição ou [SUGESTÃO]

[DIFERENCIAIS COMPETITIVOS]
diferencial_real_sustentável ou [SUGESTÃO]

[RISCOS OU ALERTAS DE COMPLIANCE]
termo_proibido | claim_bloqueado | política_sensível | checklist_categoria

[ANÁLISE DE CONCORRENTES]
nome | forças | fraquezas | preço_médio | oportunidade | novelty (1-5)

[BENCHMARK DE CONCORRENTES]
Tabela comparativa: Característica | C

[... content truncated ...]

**Tags**: lem, abstract

**Palavras-chave**: Framework, Research

**Origem**: unknown


---


<!-- VERSÍCULO 14/18 - marketplace_optimization_research_notes_ecomlm_20251113.md (58 linhas) -->

# Research Notes Ecomlm | marketplace_optimization

## CONCEITOS-CHAVE

• **Fundamentos**: Este conhecimento aborda conceitos essenciais para vendedores que querem crescer no e-commerce brasileiro
• **Aplicação Prática**: Técnicas e estratégias que você pode aplicar hoje mesmo nos seus produtos
• **Resultados Mensuráveis**: Foco em ações que geram impacto direto nas suas vendas
• **Marketplaces**: Conhecimento aplicável ao Mercado Livre, Shopee, Magalu e outros canais

## POR QUE IMPORTA

Se você vende online no Brasil, sabe que a concorrência está cada vez maior. Este conhecimento foi criado para te ajudar a se destacar da multidão e vender mais.

No cenário atual dos marketplaces brasileiros, quem domina as técnicas certas consegue resultados até 3x melhores que a média. Seja otimizando títulos para o algoritmo do Mercado Livre, criando descrições que convencem, ou automatizando processos repetitivos - cada detalhe conta.

## COMO FAZER

1. **Comece pelo básico**: Analise sua situação atual e identifique onde você pode melhorar
2. **Aplique as técnicas**: Implemente as estratégias de forma gradual, começando pelos produtos mais importantes
3. **Teste e ajuste**: Monitore os resultados e faça ajustes conforme necessário
4. **Escale o que funciona**: Quando encontrar uma estratégia vencedora, replique para todos os produtos
5. **Automatize processos**: Use ferramentas e scripts para economizar tempo nas tarefas repetitivas
6. **Acompanhe métricas**: Fique de olho em conversão, visualizações e posição nos resultados de busca
7. **Mantenha-se atualizado**: Os marketplaces mudam constantemente - adapte suas estratégias

## EXEMPLO REAL

**Antes**: Vendedor com 50 produtos no Mercado Livre, títulos genéricos, fotos padrão do fornecedor, descrições copiadas. Taxa de conversão: 1.2%, aparecendo na 5ª página de resultados.

**Depois**: Após aplicar as técnicas de otimização - títulos com palavras-chave estratégicas, fotos profissionais com fundo branco, descrições persuasivas com gatilhos mentais, uso de ferramentas de automação para atualizar preços.

**Resultado**: Taxa de conversão subiu para 3.8% (+217%), produtos aparecendo na primeira página, vendas aumentaram de 15 para 42 unidades/mês por produto (+180%). Tempo gasto em gestão reduziu de 4h para 1h por dia graças à automação.

## BOAS PRÁTICAS

• **Seja consistente**: Aplique as técnicas em todos os seus produtos, não apenas em alguns
• **Teste sempre**: O que funciona para um vendedor pode não funcionar para outro - teste e descubra o que dá certo no seu nicho
• **Foque no cliente**: Pense sempre em como facilitar a decisão de compra do seu cliente
• **Use dados**: Baseie suas decisões em números reais, não em achismos
• **Automatize o repetitivo**: Use ferramentas para economizar tempo e focar no estratégico

## PRÓXIMOS PASSOS

Depois de dominar este conteúdo, explore:
• Técnicas avançadas de SEO para marketplaces
• Estratégias de precificação dinâmica
• Automação de processos com Python
• Análise de concorrência e benchmarking
• Gatilhos mentais aplicados ao e-commerce

---
**Categoria**: marketplace_optimization
**Nível**: básico
**Tags**: mercadolivre, shopee, magalu, seo, automacao
**Aplicação**: quando_criar_anuncios
**Fonte**: RASCUNHO/research_notes_ecomlm.md
**Processado**: 20251113


---


<!-- VERSÍCULO 15/18 - marketplace_optimization_research_phases_8_phases_20251113.md (62 linhas) -->

# Research Phases (8 Phases)

**Categoria**: marketplace_optimization
**Qualidade**: 0.95/1.00
**Data**: 20251113

## Conteúdo

```
1. PLANNING
   ↓
2. MARKET_RESEARCH → MarketResearchAgent
   ├─ Market size & growth trends
   ├─ Customer pain points
   ├─ Seasonal patterns
   └─ Market insights
   ↓
3. COMPETITIVE_ANALYSIS → CompetitorAnalystAgent
   ├─ Competitor analysis
   ├─ Market gaps
   ├─ Differentiation opportunities
   └─ Messaging insights
   ↓
4. KEYWORD_EXTRACTION → KeywordExtractionAgent
   ├─ Core keywords (primary)
   ├─ Variant keywords (variations)
   ├─ Buyer intent keywords
   └─ Long-tail keywords
   ↓
5. FAQ_COLLECTION → FAQCollectionAgent
   ├─ Common FAQs
   ├─ Objections
   └─ Objection counters
   ↓
6. DATA_VALIDATION → DataValidatorAgent
   ├─ Completeness check
   ├─ Consistency validation
   ├─ Quality scoring
   └─ Error identification
   ↓
7. PROMPT_COMPOSITION → PromptComposerAgent
   ├─ Chunk 1: Research consolidation
   ├─ Chunk 2: Keyword analysis
   ├─ Chunk 3: Competitor insights
   ├─ Chunk 4: Ad brief generation
   └─ Chunk 5: Copy optimization
   ↓
8. REPORT_GENERATION
   ├─ Final scoring
   ├─ Recommendations
   ├─ Next steps
   └─ COMPLETE
```

---

**Tags**: ecommerce, architectural

**Palavras-chave**: Research, Phases

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 16/18 - marketplace_optimization_research_workflow_5_types_20251113.md (46 linhas) -->

# Research Workflow: 5 Types

**Categoria**: marketplace_optimization
**Qualidade**: 0.91/1.00
**Data**: 20251113

## Conteúdo

### 1. Quick Research (45-60 minutes)
- Market research
- Keyword extraction
- Prompt composition
- **Best for**: Fast turnaround needed

### 2. Deep Research (3-4 hours)
- All phases
- Comprehensive analysis
- Full AI prompt composition
- **Best for**: Strategic decisions

### 3. Keywords Only (20-30 minutes)
- Keyword extraction only
- 4-level hierarchy
- Long-tail generation
- **Best for**: SEO optimization

### 4. Competitors (90 minutes)
- Competitive analysis
- Market positioning
- Differentiation strategy
- **Best for**: Competitive moves

### 5. AI-Assisted (15-30 minutes)
- AI-optimized workflow
- Claude-powered analysis
- Fast turnaround
- **Best for**: Quick decisions with AI help

---

**Tags**: ecommerce, architectural

**Palavras-chave**: Research, Workflow, Types

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 17/18 - marketplace_optimization_resources_20251113.md (24 linhas) -->

# Resources

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

- **Documentation**: https://www.e2b.dev/docs
- **GitHub**: https://github.com/e2b-dev
- **Discord Community**: https://discord.com/invite/U7KEcGErtQ
- **Dashboard**: https://www.e2b.dev/dashboard
- **Cookbook Examples**: https://github.com/e2b-dev/e2b-cookbook

E2B makes it easy to run AI-generated code safely and efficiently. Start building your AI applications with secure, scalable sandbox execution today!

======================================================================

**Tags**: concrete, general

**Palavras-chave**: Resources

**Origem**: unknown


---


<!-- VERSÍCULO 18/18 - marketplace_optimization_response_format_20251113.md (36 linhas) -->

# Response Format

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

Tipo: JSON Schema

```json
{
  "name": "produto_otimizado_seo",
  "strict": true,
  "schema": {
    "type": "object",
    "properties": {
      "marca_modelo": {
        "type": "object",
        "properties": {
          "marca": {
            "type": "string",
            "minLength": 115,
            "maxLength": 120,
            "description": "Nome da marca otimizado para SEO"
          },
          "modelo": {
            "type": "string",
            "minLength": 115,

**Tags**: ecommerce, concrete

**Palavras-chave**: Response, Format

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- FIM DO CAPÍTULO 54 -->
<!-- Total: 18 versículos, 1200 linhas -->
