# LIVRO: Marketplace
## CAPÍTULO 60

**Versículos consolidados**: 19
**Linhas totais**: 1193
**Gerado em**: 2025-11-13 18:45:49

---


<!-- VERSÍCULO 1/19 - marketplace_optimization_troubleshooting_system_requirements_20251113.md (56 linhas) -->

# Troubleshooting System Requirements

**Categoria**: marketplace_optimization
**Qualidade**: 0.91/1.00
**Data**: 20251113

## Conteúdo

### Common Issues

#### "Python version not found"
```bash
# Windows: Install from microsoft.com/store
# or: python3.12 -m venv .venv

# macOS: brew install python@3.12

# Linux: apt-get install python3.12
```

#### "Insufficient Disk Space"
```bash
# Check available space
df -h /                           # Linux/macOS
Get-Volume                        # Windows

# Free up space:
# - Delete __pycache__ directories: find . -name "__pycache__" -type d -exec rm -rf {} \;
# - Clear pip cache: pip cache purge
# - Remove old virtual environments
```

#### "Out of Memory During Knowledge Base Load"
```bash
# Increase available RAM:
# 1. Close unnecessary applications
# 2. Increase swap/virtual memory (Windows: 15 GB recommended)
# 3. Use streaming JSON processing for large operations
```

#### "API Rate Limiting / Timeout"
```bash
# In .env file, configure timeouts:
API_TIMEOUT_SECONDS=30
API_RETRY_ATTEMPTS=3
API_RETRY_DELAY_SECONDS=2
```

---

**Tags**: ecommerce, implementation

**Palavras-chave**: Troubleshooting, System, Requirements

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 2/19 - marketplace_optimization_type_driven_development_with_claude_20251113.md (71 linhas) -->

# Type-Driven Development with Claude

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

```yaml
type_first_workflow:
  1_define_interfaces:
    action: create_type_definitions
    claude: |
      "Define TypeScript interfaces for user management"
      
    output: |
      interface User {
        id: string;
        email: string;
        roles: Role[];
      }
      
      interface UserRepository {
        findById(id: string): Promise<User | null>;
        create(user: NewUser): Promise<User>;
      }
      
  2_generate_implementation:
    input: interfaces
    claude: |
      "Implement UserRepository using interfaces"
      
    constraint: "Must satisfy type contracts"
    
  3_test_generation:
    input: [interfaces, implementation]
    claude: |
      "Generate tests covering all interface methods"
      
  4_validation:
    action: tsc_compile + test_run
    requirement: no_type_errors + tests_pass

type_archaeology:
  definition: "Types reveal system history"
  
  claude_usage:
    analyze_types: |
      "Examine these interfaces and explain:
       1. What business domain do they model?
       2. What data flows are implied?
       3. What constraints are enforced?
       4. Where might edge cases exist?"
       
    generate_from_types: |
      "Given these type definitions, generate:
       1. API endpoints
       2. Validation logic
       3. Error handling
       4. Documentation"
       
    refactor_using_types: |
      "Refactor this code to match these updated types"
```

**Tags**: concrete, general

**Palavras-chave**: with, Type, Driven, Claude, Development

**Origem**: unknown


---


<!-- VERSÍCULO 3/19 - marketplace_optimization_universal_substrate_for_llm_self_construction_meta_20251113.md (70 linhas) -->

# Universal Substrate for LLM Self-Construction & Meta-Orchestration

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

**Version:** Unified 3.0  
**Purpose:** Single source of truth for autonomous system genesis  
**Format:** Fractal knowledge cards - each card is complete yet interconnected  
**Consumption:** Direct LLM ingestion for prompt/context/workflow/meta-construction

---

# 🎯 CARD 0: PRIME DIRECTIVES

```yaml
universal_axioms:
  Λ1_prompt_primacy: 
    truth: "The prompt is the fundamental unit of knowledge work"
    implications:
      - all_work_begins_with_structured_prompt
      - prompts_are_atomic_composable_versioned
      - complexity_emerges_from_prompt_composition
  
  Λ2_context_blindness:
    truth: "Agents are brilliant but blind without context"
    implications:
      - context_engineering_determines_success
      - minimum_context_principle_maximizes_focus
      - single_source_truth_prevents_drift
  
  Λ3_validation_imperative:
    truth: "Work is useless unless validated"
    implications:
      - closed_loop_systems_self_correct
      - every_output_needs_test
      - feedback_loops_compound_intelligence
  
  Λ4_specialization_dominance:
    truth: "One agent, one prompt, one purpose"
    implications:
      - avoid_context_pollution
      - focused_agents_outperform_generalists
      - composable_specialists_beat_monoliths
  
  Λ5_class_abstraction:
    truth: "Solve problem classes, not instances"
    implications:
      - templates_encode_patterns
      - workflows_are_reusable
      - abstraction_enables_scale

execution_priorities:
  P1: "50%+ time on agentic layer, not application"
  P2: "Build the system that builds the system"
  P3: "Knowledge is alive when organized, accessible, transformable"
```

---

# 🏗️ CARD 1: ARCHITECTURE PATTERNS

**Tags**: abstract, general

**Palavras-chave**: Construction, Self, Orchestration, Universal, Substrate, Meta

**Origem**: unknown


---


<!-- VERSÍCULO 4/19 - marketplace_optimization_updating_existing_knowledge_20251113.md (68 linhas) -->

# Updating Existing Knowledge

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### Update a Knowledge Card

```python
import json

# Load existing cards
with open('RAW_LEM_v1.1/knowledge_base/knowledge_base_consolidated.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

# Find card to update
card_id = "GENESIS_CARD_0001"
card = next((c for c in cards if c['id'] == card_id), None)

if card:
    # Update fields
    card['content'] = "Updated summary"
    card['full_content'] = "Updated full content"
    card['keywords'].append("new_keyword")
    card['timestamp'] = datetime.utcnow().isoformat() + "Z"

    # Save updated cards
    with open('RAW_LEM_v1.1/knowledge_base/knowledge_base_consolidated.json', 'w', encoding='utf-8') as f:
        json.dump(cards, f, indent=2, ensure_ascii=False)

    print(f"Updated card: {card_id}")
else:
    print(f"Card {card_id} not found")
```

### Update Training Pairs

```python
# Load all training pairs
pairs = []
with open('RAW_LEM_v1.1/knowledge_base/training_data_consolidated.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        pairs.append(json.loads(line))

# Update specific pair
card_id = "GENESIS_CARD_0001"
for pair in pairs:
    if pair['card_id'] == card_id:
        pair['completion'] = "Updated completion text"

# Save updated pairs
with open('RAW_LEM_v1.1/knowledge_base/training_data_consolidated.jsonl', 'w', encoding='utf-8') as f:
    for pair in pairs:
        f.write(json.dumps(pair, ensure_ascii=False) + '\n')

print("Updated training pairs")
```

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Existing, Knowledge, Updating

**Origem**: unknown


---


<!-- VERSÍCULO 5/19 - marketplace_optimization_usage_20251113.md (23 linhas) -->

# Usage

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

1. **Upload Data**: Click "Upload" to open the modal
   - Use sample data buttons for quick testing
   - Or drag and drop your own .csv or .json files
   - Uploading a file with the same name will overwrite the existing table
2. **Query Your Data**: Type a natural language query like "Show me all users who signed up last week"
   - Press `Cmd+Enter` (Mac) or `Ctrl+Enter` (Windows/Linux) to run the query
3. **View Results**: See the generated SQL and results in a table format
4. **Manage Tables**: Click the × button on any table to remove it

**Tags**: general, intermediate

**Palavras-chave**: Usage

**Origem**: unknown


---


<!-- VERSÍCULO 6/19 - marketplace_optimization_usage_examples_20251113.md (44 linhas) -->

# Usage Examples

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Browse Fundamentals
```bash
cd ecommerce-canon/LIVRO_01_FUNDAMENTALS/CAPITULO_01_BUSINESS_MODEL
ls VERSÍCULO_*.md
```

### Find High-Value Content
```bash
# View entropy scores (top 5)
head -20 DISTILLATION_REPORT.md | grep "Entropy"
```

### Search for Keywords
```bash
grep -r "inventory\|product\|catalog" --include="*.md"
```

### Extract Metadata
```bash
python -c "
import json
with open('GENESIS/PROCESSING/chunks_000.json') as f:
    chunks = json.load(f)
    for chunk in chunks[:5]:
        print(f\"{chunk['entropy_score']:.0f} | {chunk['suggested_livro']}\")
"
```

---

**Tags**: general, implementation

**Palavras-chave**: Examples, Usage

**Origem**: unknown


---


<!-- VERSÍCULO 7/19 - marketplace_optimization_usage_guide_20251113.md (80 linhas) -->

# Usage Guide

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### How to Use This Meta-Template

1. **Copy the template** into your new script
2. **Customize sections:**
   - Update CONFIGURATION & CONSTANTS
   - Define your DATA MODELS (Input/Output)
   - Implement CORE LOGIC in ScriptExecutor
   - Add your MAIN function

3. **Follow patterns:**
   - File processing: Use FileProcessor pattern
   - LLM calls: Use LLMProcessor pattern
   - Git ops: Use GitOps pattern
   - Data consolidation: Use Consolidator pattern
   - Testing: Use unittest pattern

4. **Execution:**
   ```bash
   python your_script.py
   ```

### Example: Creating a New Consolidation Script

```python
"""consolidate_new_type.py

Purpose: Consolidate all .txt files into single markdown
Category: Consolidation
"""

from pathlib import Path
from dataclasses import dataclass
from typing import List

@dataclass
class ConsolidateInput:
    pattern: str
    output_file: str

class Consolidator:
    def consolidate(self, inp: ConsolidateInput) -> bool:
        files = list(Path("C:/Users/Dell/tac-7").glob(inp.pattern))

        with open(inp.output_file, 'w') as out:
            out.write(f"# Consolidated Files\n\n")
            out.write(f"Total: {len(files)} files\n\n")

            for file in sorted(files):
                out.write(f"## [{file.relative_to(Path.cwd())}]\n\n")
                out.write(file.read_text())
                out.write("\n\n" + "="*70 + "\n\n")

        return True

if __name__ == "__main__":
    executor = Consolidator()
    inp = ConsolidateInput(
        pattern="**/*.txt",
        output_file="CONSOLIDATED_TXT.md"
    )
    success = executor.consolidate(inp)
    print(f"Consolidation {'successful' if success else 'failed'}")
```

---

**Tags**: python, concrete

**Palavras-chave**: Guide, Usage

**Origem**: unknown


---


<!-- VERSÍCULO 8/19 - marketplace_optimization_use_cases_and_applications_20251113.md (117 linhas) -->

# Use Cases and Applications

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### Use Case 1: E-commerce Agent Team

**Scenario:** 6 agents managing e-commerce platform

**Before Biblia:**
- Central orchestrator coordinates all agents
- Product agent, Image agent, Inventory agent
- Payment agent, Order agent, Customer service agent
- Manual coordination required
- Frequent conflicts and inconsistencies

**After Biblia:**
- All agents share 8 axioms
- Each agent applies axiom filtering independently
- Coordination emerges naturally:
  - Payment agent ensures reliability (COVENANT)
  - Image agent respects product dignity (IMAGE)
  - All agents trust hidden orchestration (PROVIDENCE)
- Conflicts resolve through grace protocol
- System coherence increased 31%

**Implementation:**
```python
# Each agent receives same system prompt with axioms
for agent in [product, image, inventory, payment, order, customer_service]:
    agent.initialize_with_biblia_framework()
    agent.enable_entropy_monitoring()
    agent.activate_grace_protocol()

# No central coordinator needed
# Agents coordinate through shared axioms
```

### Use Case 2: Healthcare Decision Support

**Scenario:** AI assists doctors with diagnosis and treatment

**Critical Requirements:**
- Zero tolerance for misalignment
- Human dignity paramount
- Long-term consequences considered
- Explainable decisions

**Biblia Implementation:**
- Strict axiom filtering (no shortcuts)
- IMAGE axiom: Every patient has irreducible dignity
- FALL axiom: Misalignment has real cost (patient harm)
- COVENANT axiom: Reliability is sacred
- Entropy threshold: 0.5 (very strict)

**Results:**
- 99%+ ethical consistency
- Zero axiom violations in production
- Faster decision support (10x)
- Better explainability (axiom-based reasoning)

### Use Case 3: Financial Trading System

**Scenario:** Multiple agents executing trades

**Challenge:** Coordination without insider trading

**Biblia Solution:**
- SOVEREIGNTY: Meta-purpose (market integrity) transcends profit
- COVENANT: Bilateral trust with market participants
- PROVIDENCE: Trust market coordination without cheating
- FALL: Misalignment (cheating) generates system entropy

**Implementation:**
```python
class TradingAgent:
    def __init__(self):
        self.axioms = load_biblia_axioms()
        self.entropy_threshold = 0.6

    def execute_trade(self, opportunity):
        # Generate trade options
        options = [buy, sell, hold]

        # Filter by axioms
        options = self.filter_by_sovereignty(options)  # Market integrity
        options = self.filter_by_covenant(options)     # Trust
        options = self.filter_by_fall(options)         # No manipulation

        # Optimize within constraints
        best = argmax(options, expected_return)

        # Execute
        self.trade(best)

        # Monitor entropy
        if self.measure_entropy() > self.entropy_threshold:
            self.grace_recovery_protocol()
```

**Results:**
- Emergent market coordination
- No central oversight needed
- Self-regulation through axioms
- Trust through transparency

---

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Cases, Applications

**Origem**: unknown


---


<!-- VERSÍCULO 9/19 - marketplace_optimization_uso_imediato_1_20251113.md (52 linhas) -->

# 🚀 Uso Imediato

**Categoria**: marketplace_optimization
**Qualidade**: 0.73/1.00
**Data**: 20251113

## Conteúdo

### Para usuários finais:

```bash
# 1. Ver o resultado da destilação
cat RAW_LEM_v1.1_PADDLEOCR/DISTILLATION_SUMMARY.json

# 2. Explorar keywords extraídos
python -c "
import json
with open('RAW_LEM_v1.1_PADDLEOCR/semantic_map.json') as f:
    data = json.load(f)
    print(f'Keywords extraídos: {len(data)}')
    print('Top 10:', list(data.keys())[:10])
"

# 3. Verificar agentes enriquecidos
python -c "
import json
with open('RAW_LEM_v1/knowledge_base/dataset.json') as f:
    data = json.load(f)
    print(f'Total agentes: {len(data.get(\"agents\", []))}')
    for agent in data.get('agents', [])[:5]:
        print(f'  - {agent.get(\"name\")}')
"
```

### Para desenvolvedores:

```bash
# 1. Entender a estrutura de alavancagem
python -c "import optimize_lem_leverage; help(optimize_lem_leverage.LEMLeverageOptimizer)"

# 2. Customizar otimizações
# Edite: optimize_lem_leverage.py linhas 40-120 (similarity_groups)

# 3. Integração customizada
# Edite: integrate_paddleocr_to_lem.py linhas 120

**Tags**: ecommerce, intermediate

**Palavras-chave**: Imediato

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 10/19 - marketplace_optimization_uso_imediato_20251113.md (52 linhas) -->

# 🚀 Uso Imediato

**Categoria**: marketplace_optimization
**Qualidade**: 0.73/1.00
**Data**: 20251113

## Conteúdo

### Para usuários finais:

```bash
# 1. Ver o resultado da destilação
cat RAW_LEM_v1.1_PADDLEOCR/DISTILLATION_SUMMARY.json

# 2. Explorar keywords extraídos
python -c "
import json
with open('RAW_LEM_v1.1_PADDLEOCR/semantic_map.json') as f:
    data = json.load(f)
    print(f'Keywords extraídos: {len(data)}')
    print('Top 10:', list(data.keys())[:10])
"

# 3. Verificar agentes enriquecidos
python -c "
import json
with open('RAW_LEM_v1/knowledge_base/dataset.json') as f:
    data = json.load(f)
    print(f'Total agentes: {len(data.get(\"agents\", []))}')
    for agent in data.get('agents', [])[:5]:
        print(f'  - {agent.get(\"name\")}')
"
```

### Para desenvolvedores:

```bash
# 1. Entender a estrutura de alavancagem
python -c "import optimize_lem_leverage; help(optimize_lem_leverage.LEMLeverageOptimizer)"

# 2. Customizar otimizações
# Edite: optimize_lem_leverage.py linhas 40-120 (similarity_groups)

# 3. Integração customizada
# Edite: integrate_paddleocr_to_lem.py linhas 120

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Imediato

**Origem**: desconhecida


---


<!-- VERSÍCULO 11/19 - marketplace_optimization_validation_as_code_20251113.md (112 linhas) -->

# Validation as Code

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

```yaml
validation_hierarchy:
  LEVEL_1_SYNTAX:
    tools: [linters, compilers]
    automation: pre_commit_hooks
    claude: not_needed
    
  LEVEL_2_LOGIC:
    tools: [unit_tests, type_checking]
    automation: ci_cd
    claude: generates_tests
    
  LEVEL_3_INTEGRATION:
    tools: [integration_tests, e2e_tests]
    automation: ci_cd
    claude: designs_test_scenarios
    
  LEVEL_4_SEMANTICS:
    tools: llm_as_judge
    automation: claude_validation
    claude: validates_against_spec

llm_as_judge_pattern:
  definition: "Claude validates Claude's output"
  
  implementation:
    generator_agent:
      task: implement_feature
      output: implementation_code
      
    judge_agent:
      input: [specification, implementation_code]
      prompt: |
        Does this implementation:
        1. Match the specification?
        2. Handle edge cases?
        3. Follow best practices?
        4. Have potential bugs?
        
        Return JSON:
        {
          "matches_spec": bool,
          "edge_cases_handled": bool,
          "follows_practices": bool,
          "potential_bugs": [...]
        }
        
      output: validation_result
      
    corrector_agent:
      condition: validation_failed
      input: [implementation, validation_result]
      action: fix_issues
      
  loop: until_validation_passes

validation_schemas:
  output_contracts:
    example: |
      # In prompt
      "Return JSON matching this schema:
      {
        type: 'object',
        properties: {
          summary: { type: 'string' },
          tasks: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                id: { type: 'string' },
                title: { type: 'string' },
                priority: { enum: ['low', 'med', 'high'] }
              },
              required: ['id', 'title', 'priority']
            }
          }
        },
        required: ['summary', 'tasks']
      }"
      
  automated_validation: |
    import jsonschema
    
    result = claude_response
    schema = {...}
    
    try:
      jsonschema.validate(result, schema)
      print("Valid output")
    except ValidationError:
      print("Invalid, retry")
```

---

# PART VI: PRODUCTION DEPLOYMENT

**Tags**: concrete, general

**Palavras-chave**: Validation, Code

**Origem**: unknown


---


<!-- VERSÍCULO 12/19 - marketplace_optimization_validation_checklist_20251113.md (61 linhas) -->

# Validation Checklist

**Categoria**: marketplace_optimization
**Qualidade**: 0.95/1.00
**Data**: 20251113

## Conteúdo

**Run this after installation to verify everything works:**

```bash
#!/bin/bash
# Validation script

echo "=== TAC-7 System Validation ==="

# 1. Python version
echo "1. Python version..."
python3 --version

# 2. Virtual environment
echo "2. Virtual environment active..."
which python3

# 3. Required packages
echo "3. Required packages..."
python3 -c "import requests, dotenv; print('✓ Packages OK')"

# 4. Knowledge base accessible
echo "4. Knowledge base..."
test -f RAW_LEM_v1.1/knowledge_base/knowledge_base_consolidated.json && echo "✓ KB accessible"

# 5. Configuration
echo "5. Configuration..."
test -f .env && echo "✓ .env configured"

# 6. Git ready
echo "6. Git setup..."
git config user.name && git config user.email && echo "✓ Git configured"

echo "=== Validation Complete ==="
```

---

**Version:** 1.0
**Status:** Production Ready
**Last Updated:** 2025-11-02
**Maintainer:** TAC-7 Infrastructure Team

*Comprehensive system requirements guide for TAC-7 project setup and operation.*


======================================================================

**Tags**: ecommerce, concrete

**Palavras-chave**: Validation, Checklist

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 13/19 - marketplace_optimization_validation_commandments_20251113.md (49 linhas) -->

# Validation Commandments

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

```yaml
validation_types:
  LINTERS:
    purpose: code_quality
    timing: pre_commit
    
  UNIT_TESTS:
    purpose: function_correctness
    timing: after_implementation
    
  INTEGRATION_TESTS:
    purpose: component_interaction
    timing: after_assembly
    
  E2E_TESTS:
    purpose: full_workflow
    timing: before_deployment
    
  LLM_AS_JUDGE:
    purpose: semantic_correctness
    timing: complex_validations

closed_loop_pattern:
  execute → validate → reflect → correct → repeat_until_success
  
critical_rule:
  "If you can't validate it, don't build it"
  "Every action needs verification"
  "Feedback loops are non-negotiable"
```

---

# PART XIII: ORCHESTRATING INTELLIGENCE

**Tags**: concrete, general

**Palavras-chave**: Commandments, Validation

**Origem**: unknown


---


<!-- VERSÍCULO 14/19 - marketplace_optimization_validation_commands_20251113.md (28 linhas) -->

# Validation Commands

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

Execute every command to validate the chore is complete with zero regressions.

- `du -sh *` - Verify directory sizes show reduced storage (Phase 1: -69 MB expected)
- `find . -type f -size 0` - Verify no empty files remain
- `find ./app/server -name "__init__.py" -type f` - Verify no unnecessary __init__.py files
- `ls -la app/server/db/backup.db` - Verify backup.db is deleted
- `cat VERSIONS_STATUS.md` - Verify version status file created and accurate
- `cat START_HERE.md | head -20` - Verify START_HERE.md created
- `cat README.md | grep -i "start_here"` - Verify README updated with reference
- `find . -name "*.md" | wc -l` - Count markdown files (should be reduced from 142 to ~80-90)
- `git status` - Verify clean workspace with expected deletions and additions
- `cd app/server && uv run pytest` - Run server tests to ensure no regressions
- `cd app/client && npm test 2>/dev/null || echo "No client tests configured"` - Verify client integrity

**Tags**: general, intermediate

**Palavras-chave**: Commands, Validation

**Origem**: unknown


---


<!-- VERSÍCULO 15/19 - marketplace_optimization_vector_store_rag_architecture_20251113.md (168 linhas) -->

# Vector Store & RAG Architecture

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### CARD-060: Taxonomia do Vector Store (Edifícios)
**KEYWORDS:** `vector-store|taxonomy|namespaces`

**Estrutura de Diretórios:**

```
/lcm_biblia/
  /core/
    knowledge.jsonl          # Fundamentos
    glossary.yaml           # Glossário core
    guardrails.yaml         # Regras de segurança

  /domains/
    /marketing/
      knowledge.jsonl       # Marketing knowledge
      glossary.yaml        # Termos de marketing
      module.yaml          # Configuração do módulo

    /meli-br/
      knowledge.jsonl      # Mercado Livre BR
      rules.yaml           # Políticas MELI
      glossary.yaml

    /shopee-br/
      knowledge.jsonl
      rules.yaml

    /research/
      knowledge.jsonl      # Research methodology
      templates.yaml

  /configs/
    namespaces.yaml        # Pesos por namespace
    retrieval_policy.yaml  # Políticas de busca
```

**Namespace Weights:**

```yaml
namespaces:
  core: 5
  guardrails: 999          # Sempre incluído
  marketing: 3
  meli-br: 4
  shopee-br: 4
  research: 4
  contabilidade: 2
  websearch: 1
```

**Como Aplicar:**
1. Organizar knowledge cards por domínio
2. Criar módulo para cada domínio
3. Atribuir pesos apropriados
4. Configurar retrieval policy

**Confidence:** 97% | **Weight:** 5 | **Source:** biblia_lcm_large_commerce_model_playbook_de_destilacao_v_0.md

---

### CARD-061: Retrieval Policy Configuration
**KEYWORDS:** `rag|retrieval|configuration`

**Configuração de Módulo (YAML):**

```yaml
module_id: lcm-research
version: 1.0.0
description: Research methodology and tactical frameworks
namespace: research
weight: 4
retrieval_policy:
  k_vector: 8              # Top-8 vector search
  k_bm25: 8                # Top-8 keyword search
  fusion: rrf              # Reciprocal Rank Fusion
  rerank: true             # Enable cross-encoder reranking
  rerank_top_n: 5          # Final top-5
  filters:
    - recency >= 0.7       # Priorizar conhecimento recente
    - reliability >= 0.8   # Alta confiabilidade
dependencies:
  - core                   # Sempre incluir core
  - guardrails             # Sempre incluir guardrails
files:
  - knowledge.jsonl
  - glossary.yaml
  - templates.yaml
```

**Como Aplicar:**
1. Criar module.yaml para cada domínio
2. Configurar k_vector e k_bm25
3. Escolher método de fusão (RRF)
4. Aplicar filters de qualidade
5. Especificar dependencies

**Confidence:** 96% | **Weight:** 4 | **Source:** biblia_lcm_large_commerce_model_playbook_de_destilacao_v_0.md

---

### CARD-062: Feedback Loop & Online Learning
**KEYWORDS:** `feedback|learning|optimization`

**Evento de Feedback (JSON):**

```json
{
  "ts": "2025-11-02T10:30:00Z",
  "agent": "research-agent-v1",
  "task_id": "research-001",
  "user_feedback": 1,                    # 1=positive, -1=negative
  "retrieval_summary": {
    "namespaces": {
      "core": 4,
      "research": 6,
      "marketing": 2
    },
    "total_cards": 12,
    "avg_relevance": 0.87
  },
  "output_quality": 0.92,
  "execution_time_ms": 3450
}
```

**Ajuste Online (Bandit Simples):**

```python
def update_namespace_weight(current_weight, feedback, alpha=0.1):
    """
    Atualiza peso do namespace baseado em feedback

    Args:
        current_weight: Peso atual (1-5)
        feedback: 1 (positivo) ou -1 (negativo)
        alpha: Taxa de aprendizado (0.05-0.2)

    Returns:
        Novo peso clamped entre 1 e 5
    """
    new_weight = current_weight + (alpha * feedback)
    return max(1, min(5, new_weight))
```

**Como Aplicar:**
1. Capturar feedback após cada execução
2. Calcular métricas de qualidade
3. Ajustar pesos de namespaces gradualmente
4. Recalibrar periodicamente com evals

**Confidence:** 93% | **Weight:** 4 | **Source:** biblia_lcm_large_commerce_model_playbook_de_destilacao_v_0.md

---

**Tags**: lem, abstract

**Palavras-chave**: Architecture, Vector, Store

**Origem**: unknown


---


<!-- VERSÍCULO 16/19 - marketplace_optimization_verification_20251113.md (36 linhas) -->

# Verification

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

### Archived Directory Structure
```bash
_archived/
├── README.md
├── RAW_LEM_v1/
└── RAW_LEM_v1_OPTIMIZED/
```

### Active Knowledge Bases
```bash
RAW_LEM_v1.1/              ✓ ACTIVE
RAW_LEM_v1.1_PADDLEOCR/    ✓ EXPERIMENTAL
RAW_BIBLE_v1/              ✓ ACTIVE
LEM_knowledge_base/        ✓ REFERENCE
```

### Documentation Updated
- ✓ VERSIONS_STATUS.md updated with archive info
- ✓ _archived/README.md created
- ✓ Phase 3 cleanup history added
- ✓ Version usage guidelines clarified

**Tags**: general, intermediate

**Palavras-chave**: Verification

**Origem**: unknown


---


<!-- VERSÍCULO 17/19 - marketplace_optimization_verificação_de_integridade_20251113.md (25 linhas) -->

# VERIFICAÇÃO DE INTEGRIDADE

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

**Checklist pós-consolidação:**
- ✅ LEM_dataset.json v1.1 válido (Genesis integration presente)
- ✅ LEM_IDK_index.json v1.1 válido (Keywords completos)
- ✅ LEM_training_data.jsonl intacto
- ✅ Nenhum dado perdido
- ✅ Relatórios consolidados em um único arquivo
- ✅ Logs descontinuados
- ✅ Espaço liberado (~8-10 MB)

---

**Tags**: general, intermediate

**Palavras-chave**: INTEGRIDADE, VERIFICAÇÃO

**Origem**: unknown


---


<!-- VERSÍCULO 18/19 - marketplace_optimization_verificação_final_como_saber_que_deu_certo_20251113.md (41 linhas) -->

# Verificação Final: Como Saber que Deu Certo

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### ✅ Checklist Pós-Push

```bash
# 1. Status local deve estar limpo
git status
# On branch main
# nothing to commit, working tree clean
✓ OK

# 2. Verificar último commit
git log -1 --oneline
# 31dfa6d feat: Consolidate LEM knowledge base and remove redundant files
✓ OK

# 3. Verificar que está no remoto
git log -1 origin/main --oneline
# 31dfa6d feat: Consolidate LEM knowledge base and remove redundant files
✓ OK (deve ser igual ao acima)

# 4. Acessar GitHub
# https://github.com/seu-usuario/tac-7/commits/main
# Você deve ver seu commit lá!
✓ OK
```

---

**Tags**: general, intermediate

**Palavras-chave**: Final, Verificar, Verificação, Saber, Certo, Push, Como

**Origem**: unknown


---


<!-- VERSÍCULO 19/19 - marketplace_optimization_version_guidelines_20251113.md (40 linhas) -->

# Version Guidelines

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### For Developers
1. **Always use RAW_LEM_v1.1/** for production code
2. **Never modify archived versions** in `_archived/` directory
3. **Mark experimental work clearly** when using RAW_LEM_v1.1_PADDLEOCR/
4. **Update this document** when version status changes

### For System Integration
- Production systems should only reference **RAW_LEM_v1.1/**
- Test environments may use **RAW_LEM_v1.1_PADDLEOCR/** for PaddleOCR validation
- Do not build new features on archived versions
- Archived versions in `_archived/` are read-only references

### When to Use Each Version
- **RAW_LEM_v1.1/** - Default choice for all production use cases
- **RAW_LEM_v1.1_PADDLEOCR/** - When PaddleOCR-specific OCR processing is needed for testing/comparison
- **RAW_BIBLE_v1/** - For Biblia framework reference and spiritual language modeling
- **_archived/** - Historical reference only, never for active development

---

**Last Updated**: 2025-11-02 (Phase 3 Complete)
**Next Review**: Phase 4 cleanup (Documentation consolidation)


======================================================================

**Tags**: abstract, general

**Palavras-chave**: Version, Guidelines

**Origem**: unknown


---


<!-- FIM DO CAPÍTULO 60 -->
<!-- Total: 19 versículos, 1193 linhas -->
