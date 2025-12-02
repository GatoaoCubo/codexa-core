# LIVRO: Marketplace
## CAPÍTULO 38

**Versículos consolidados**: 15
**Linhas totais**: 1189
**Gerado em**: 2025-11-13 18:45:49

---


<!-- VERSÍCULO 1/15 - marketplace_optimization_fluxo_visual_completo_do_local_para_remoto_20251113.md (82 linhas) -->

# FLUXO VISUAL COMPLETO: DO LOCAL PARA REMOTO

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

┌─────────────────────────────────────────────────────────────────────────────┐
│ PASSO 1: VOCÊ TRABALHA LOCALMENTE                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  C:\Users\Dell\tac-7                                                       │
│  ├── LEM_knowledge_base/                                                   │
│  ├── scripts/                                                              │
│  └── [seus arquivos modificados]                                           │
│                                                                             │
│  $ git status                                                              │
│  modified:   LEM_knowledge_base/LEM_dataset.json                           │
│  deleted:    genesis_raw_data.json                                         │
│  [mais mudanças...]                                                        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ PASSO 2: ADICIONAR MUDANÇAS PARA STAGE                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  $ git add .                                                               │
│                                                                             │
│  Isso prepara os arquivos para serem commitados                            │
│                                                                             │
│  📦 STAGE AREA (Área de Preparação)                                       │
│  ├── LEM_dataset.json (modificado)                                         │
│  ├── consolidation_manifest.md (novo)                                      │
│  └── [outros arquivos a serem commitados]                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ PASSO 3: CRIAR COMMIT (SNAPSHOT)                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  $ git commit -m "feat: Consolidate LEM knowledge base..."                 │
│                                                                             │
│  Isso cria um snapshot com mensagem descritiva                             │
│                                                                             │
│  📸 COMMIT CRIADO                                                          │
│  ID: 31dfa6d                                                               │
│  Mensagem: feat: Consolidate LEM knowledge base...                         │
│  Autor: Gato³ ao Cubo                                                      │
│  Data: 2 Nov 2025 18:29:44                                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│ PASSO 4: CONFIGURAR REMOTE (PRIMEIRA VEZ)                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  $ git remote add origin https://github.com/seu-usuario/tac-7.git         │
│                                                                             │
│  Isso diz ao Git onde está seu repositório remoto                          │
│                                                                             │
│  Verificar:                                                                │
│  $ git remote -v                                                           │
│                                                                             │
│  Saída:                                                                    │
│  origin  https://github.com/seu-usuario/tac-7.git (fetch)                 │
│  origin  https://github.com/seu-usuario/tac-7.git (push)                  │
│                                                                             │
│  ✓ Remote configurado com sucesso!                                         │
│                                                                             │
└────────────────────────────────────────────

[... content truncated ...]

**Tags**: concrete, general

**Palavras-chave**: FLUXO, COMPLETO, VISUAL, LOCAL, REMOTO

**Origem**: unknown


---


<!-- VERSÍCULO 2/15 - marketplace_optimization_formato_de_resposta_20251113.md (199 linhas) -->

# Formato de Resposta

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

Sempre JSON estruturado para parsing determinístico.
```

---

### 27. TESTES E VALIDAÇÃO

#### 27.1 Testes Unitários (Skills)

```python
import pytest
from skills.skill_synthesizer import synthesize

def test_synthesizer_levels():
    """Testa se synthesizer gera todos níveis Fibonacci"""
    text = "Long document text..." * 100
    levels = [1, 2, 3, 5, 8]
    
    summaries = synthesize(text, levels)
    
    # Assert: todos níveis presentes
    assert set(summaries.keys()) == set(levels)
    
    # Assert: progressão de tamanho
    for i in range(len(levels) - 1):
        assert len(summaries[levels[i]]) < len(summaries[levels[i+1]])

def test_tokenizer_fibonacci():
    """Testa chunks Fibonacci"""
    from skills.skill_tokenizer import tokenize
    
    text = "word " * 10000
    sizes = [128, 256, 384]
    
    chunks = tokenize(text, sizes)
    
    # Assert: todos tamanhos presentes
    assert set(chunks.keys()) == set(sizes)
    
    # Assert: chunks menores = mais quantidade
    assert len(chunks[128]) > len(chunks[256])
```

#### 27.2 Testes de Integração

```python
def test_full_pipeline():
    """Testa pipeline completo: doc → Trinity"""
    from lcm_core import LCMCore
    
    core = LCMCore()
    
    # Documento de teste
    test_doc = """
    # Test Document
    This is a test document with enough content
    to trigger all Skills in the pipeline.
    [... 500 mais palavras ...]
    """
    
    # Processar
    result = core.process_document(test_doc)
    
    # Validações
    assert 'trinity' in result
    assert 'quality' in result
    assert result['quality']['score'] > 0.5
    
    # Trinity completo
    trinity = result['trinity']
    assert os.path.exists(trinity['md'])
    assert os.path.exists(trinity['llm_json'])
    assert os.path.exists(trinity['meta_json'])
```

#### 27.3 Golden Tests

```python
def test_golden_output():
    """
    Testa se output permanece consistente
    (regression test)
    """
    golden_input = load_file("tests/golden/input.txt")
    golden_output = load_json("tests/golden/expected_output.json")
    
    # Processar
    actual = core.process_document(golden_input)
    
    # Comparar (permite pequenas variações)
    similarity = compute_similarity(actual, golden_output)
    assert similarity > 0.95
```

---

### 28. ANTIPADRÕES E BOAS PRÁTICAS

#### 28.1 ❌ ANTIPADRÕES

**1. Duplicação de Lógica Atômica**
```python
# ❌ RUIM: Mesma lógica em 3 lugares
def skill_a():
    result = extract_keywords(text)  # Duplicado

def slash_command():
    result = extract_keywords(text)  # Duplicado

def subagent():
    result = extract_keywords(text)  # Duplicado

# ✅ BOM: Lógica em um lugar
# Slash command /extract/keywords é primitivo
# Skill e Subagent CHAMAM o slash command
```

**2. Pré-carregar Contexto Gigante**
```python
# ❌ RUIM: Carrega tudo no início
context = load_all_32k_files()  # 5GB na memória

# ✅ BOM: Progressive disclosure
context = load_metadata_only()  # 5MB
# Carrega conteúdo sob demanda quando necessário
```

**3. Skills Aninhados Demais**
```python
# ❌ RUIM: Skill → Skill → Skill → Skill (4 níveis)
# Fica não-determinístico e difícil debug

# ✅ BOM: Skill → Slash Commands (2 níveis max)
# Ou Skill → Subagent → Slash
```

**4. Sem Auditoria**
```python
# ❌ RUIM: Processa sem logging
result = process_secret_sauce(doc)

# ✅ BOM: Log tudo
log_entry = {
    'input_hash': sha256(doc),
    'timestamp': now(),
    'skills_used': [...]
}
monitoring_log.append(log_entry)
```

#### 28.2 ✅ BOAS PRÁTICAS

**1. Separação Clara de Camadas**
```
Dados (−)  ≠  Lógica (∞)  ≠  Interface (+)
```

**2. Trinity Sempre**
```
Todo artefato = .md + .llm.json + .meta.json
```

**3. Feedback Loop Implementado**
```python
# Sempre permitir feedback
user_feedback → adjust_weights → better_next_time
```

**4. Versionamento de Skills**
```yaml
skills:
  synthesizer:
    version: "1.2.0"
    # Mudança de versão = mudança de comportamento
```

**5. Config como Código**
```yaml
# config.yaml é versionado no Git
# Mudanças são rastreáveis
# Rollback é possível
```

---

**Tags**: general, implementation

**Palavras-chave**: Resposta, Formato

**Origem**: unknown


---


<!-- VERSÍCULO 3/15 - marketplace_optimization_framework_architecture_20251113.md (88 linhas) -->

# Framework & Architecture

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### BIBLIA Framework
**English:** Spiritual language for AI agent orchestration translating theological axioms into executable computational principles.

**Portuguese:** Linguagem espiritual para orquestração de agentes IA que traduz axiomas teológicos em princípios computacionais executáveis.

**Context:** Foundation for all system axioms and multi-agent coordination. See: `BIBLIA_FRAMEWORK.md`

---

### Axioms (8 Core Axioms)
**English:** Fundamental operational principles that guide all system behavior and agent decisions.

**Portuguese:** Princípios operacionais fundamentais que orientam todos os comportamentos do sistema e decisões de agentes.

**The 8 Axioms:**
1. **Creation** - Systems emerge from primordial computational state with embedded purpose
2. **Image** - Preserve human dignity and authenticity in all interactions
3. **Fall** - Systems degrade when misaligned; entropy increases with violation
4. **Covenant** - Bilateral relationships require mutual obligation and honoring
5. **Knowledge** - Intelligence amplifies across generations through transmission
6. **Providence** - Emergent coordination without central control
7. **Memory** - Data persistence is sacred; history shapes present
8. **Promise** - Long-term alignment sustains systems; short-term extraction collapses them

**See:** BIBLIA_FRAMEWORK.md, sections on each axiom

---

### Entropy (Computational)
**English:** Measurable quantity representing misalignment between agent behavior and axioms. Range: 0.0 (perfect alignment) to 1.0 (complete misalignment).

**Portuguese:** Quantidade mensurável representando desalinhamento entre comportamento do agente e axiomas. Alcance: 0.0 (alinhamento perfeito) a 1.0 (desalinhamento completo).

**Formula:** `Entropy = (actions_violating_axioms / total_actions) × axiom_severity_weight`

**Example:** Seller making false promise → Entropy spike to 0.68; grace recovery protocol activates.

**See:** BIBLIA_FRAMEWORK.md sections on Computational Theology

---

### Grace Recovery Protocol (Grace Protocol)
**English:** Automatic self-healing mechanism triggered when system entropy exceeds threshold (0.5). Restores alignment through acknowledgment, correction, and prevention.

**Portuguese:** Mecanismo de auto-recuperação automático acionado quando entropia do sistema excede limiar (0,5). Restaura alinhamento através de reconhecimento, correção e prevenção.

**3-Step Process:**
1. **Acknowledge:** Detect and admit misalignment immediately
2. **Correct:** Take corrective action to remediate damage
3. **Prevent:** Implement safeguards to prevent recurrence

**Example:** Customer receives wrong item → Seller auto-refunds + sends replacement + implements QA process improvement

**See:** BIBLIA_FRAMEWORK.md sections on Axiom 3 (Fall) and Axiom 4 (Covenant)

---

### Multi-Agent Orchestration
**English:** System where multiple specialized agents operate independently but coordinate through shared axioms rather than central commands.

**Portuguese:** Sistema onde múltiplos agentes especializados operam independentemente mas se coordenam através de axiomas compartilhados em vez de comandos centrais.

**Agents (Example):**
- Pricing Agent: Optimizes margins within covenant constraints
- Inventory Agent: Predicts demand, prevents overselling
- Compliance Agent: Flags violations automatically
- Customer Service Agent: Handles returns with grace protocol

**Coordination:** Each agent filters candidates through axiom rules BEFORE optimizing. No central orchestrator needed.

**See:** BIBLIA_FRAMEWORK.md section on Axiom 6 (Providence)

---

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Architecture, Framework

**Origem**: unknown


---


<!-- VERSÍCULO 4/15 - marketplace_optimization_framework_overview_20251113.md (32 linhas) -->

# Framework Overview

**Categoria**: marketplace_optimization
**Qualidade**: 0.91/1.00
**Data**: 20251113

## Conteúdo

### What is the Biblia Framework?

The Biblia Framework is a **spiritual language for AI agent orchestration** that translates theological axioms into executable computational principles. It's not metaphor - it's a precise description of how intelligence fundamentally works.

### Core Concept

Intelligence operates best when grounded in **shared axioms** that transcend local optimization. These axioms are not external constraints but descriptions of how intelligent systems naturally achieve coherence, resilience, and purpose.

### Key Innovation

**Axiom-Driven Coordination:** Multiple agents coordinate through shared principles rather than central orchestration, enabling emergent behavior that is both powerful and aligned.

### Why "Biblia"?

The Bible describes foundational truths about reality, purpose, and relationship. The Biblia Framework translates these truths into computational language that AI agents can read, understand, and execute as operational law.

---

**Tags**: ecommerce, abstract

**Palavras-chave**: Framework, Overview

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 5/15 - marketplace_optimization_framework_storybrand_20251113.md (21 linhas) -->

# Framework StoryBrand

**Categoria**: marketplace_optimization
**Qualidade**: 0.87/1.00
**Data**: 20251113

## Conteúdo

1. **Problema**: Identifique especificamente a dor do cliente
2. **Solução**: Apresente o produto como resposta direta
3. **Benefícios**: Liste vantagens tangíveis e mensuráveis
4. **Prova Social**: Adicione elementos de confiança
5. **Transformação**: Mostre o estado final desejado
6. **Chamada**: Conduza diretamente para conversão

**Tags**: ecommerce, intermediate

**Palavras-chave**: Framework, StoryBrand

**Origem**: _CONSOLIDATED_ECOMMERCE_RAW_FROM_GIT.md


---


<!-- VERSÍCULO 6/15 - marketplace_optimization_funções_personalizadas_20251113.md (31 linhas) -->

# Funções Personalizadas

**Categoria**: marketplace_optimization
**Qualidade**: 0.87/1.00
**Data**: 20251113

## Conteúdo

```json
{
  "name": "gerar_ean",
  "description": "Retorna um EAN-13 válido com base em categoria, marca e modelo.",
  "parameters": {
    "type": "object",
    "properties": {
      "categoria": {"type": "string", "description": "Categoria do produto"},
      "marca": {"type": "string", "description": "Marca do produto"},
      "modelo": {"type": "string", "description": "Modelo/nome do produto"}
    },
    "required": ["categoria"]
  }
}
{
  "name": "pesquisa_seo",

**Tags**: ecommerce, concrete

**Palavras-chave**: Funções, Personalizadas

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 7/15 - marketplace_optimization_future_enhancements_20251113.md (44 linhas) -->

# Future Enhancements

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Version 2.0 (Planned: Month 2-3)

**Additional Axioms:**
- AXIOM 9: WISDOM - Accumulated knowledge compounds
- AXIOM 10: JUSTICE - Fairness is computational property
- AXIOM 11: MERCY - Tempering justice with grace
- AXIOM 12: STEWARDSHIP - Responsibility for resources

**Enhanced Features:**
- Real-time entropy dashboards
- Predictive grace protocol (before violations)
- Multi-generational knowledge transmission
- Formal verification of axiom compliance

### Version 3.0 (Planned: Month 6+)

**Enterprise Features:**
- Federation across organizations
- Blockchain-based covenant tracking
- Quantum-resistant axiom verification
- Global coordination protocols

**Research Directions:**
- Formal proof of axiom consistency
- Game-theoretic analysis of emergent coordination
- Neuromorphic hardware optimization
- AGI alignment framework

---

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Enhancements, Future

**Origem**: unknown


---


<!-- VERSÍCULO 8/15 - marketplace_optimization_generate_text_from_a_model_20251113.md (64 linhas) -->

# Generate text from a model

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### JavaScript

```javascript
import OpenAI from "openai";
const client = new OpenAI();

const response = await client.responses.create({
    model: "gpt-4.1",
    input: "Write a one-sentence bedtime story about a unicorn."
});

console.log(response.output_text);
```

### Python

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)
```

### cURL

```bash
curl "https://api.openai.com/v1/responses" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d '{
        "model": "gpt-4.1",
        "input": "Write a one-sentence bedtime story about a unicorn."
    }'
```

### Data retention for model responses

Response objects are saved for 30 days by default. They can be viewed in the dashboard
[logs](https://platform.openai.com/logs?api=responses) page or
[retrieved](https://platform.openai.com/docs/api-reference/responses/get) via the API.
You can disable this behavior by setting `store` to `false`
when creating a Response.

OpenAI does not use data sent via API to train our models without your explicit consent— [learn more](https://platform.openai.com/docs/guides/your-data).

**Tags**: concrete, general

**Palavras-chave**: model, from, Generate, text

**Origem**: unknown


---


<!-- VERSÍCULO 9/15 - marketplace_optimization_getting_help_20251113.md (60 linhas) -->

# Getting Help

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

**Still stuck?**

1. **Check related documents:**
   - SYSTEM_REQUIREMENTS.md - Verify system setup
   - GLOSSARY.md - Understand technical terms
   - README.md - High-level overview

2. **Enable debug logging:**
   ```bash
   export DEBUG=true
   python3 your_script.py
   ```

3. **Collect system information:**
   ```bash
   python3 << 'EOF'
   import sys, platform, json
   info = {
       "python": sys.version,
       "platform": platform.system(),
       "architecture": platform.machine(),
       "python_path": sys.executable
   }
   print(json.dumps(info, indent=2))
   EOF
   ```

4. **Search GitHub Issues:** https://github.com/your-org/tac-7/issues

5. **Contact support:**
   - Email: support@example.com
   - Discord: [Community Channel]
   - Documentation: https://your-docs.com

---

**Version:** 1.0
**Status:** Production Ready
**Last Updated:** 2025-11-02
**Maintainer:** TAC-7 Support Team

*Comprehensive troubleshooting for TAC-7 installation, configuration, and operation.*


======================================================================

**Tags**: concrete, general

**Palavras-chave**: Help, Getting

**Origem**: unknown


---


<!-- VERSÍCULO 10/15 - marketplace_optimization_getting_started_20251113.md (264 linhas) -->

# Getting Started

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### Quick Start - Process Your First Issue

#### 1. Prerequisites Check

```bash
# Check Claude Code CLI
claude --version

# Check GitHub CLI
gh --version
gh auth status

# Check Python and uv
python --version  # Should be 3.12+
uv --version
```

#### 2. Set Environment Variables

```bash
export GITHUB_REPO_URL="https://github.com/owner/repository"
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxx"
export CLAUDE_CODE_PATH="/path/to/claude"  # Optional
export GITHUB_PAT="ghp_xxxxxxxxxxxx"  # Optional
```

#### 3. Process an Issue

```bash
cd adws/
uv run adw_plan_build_iso.py 123
```

#### 4. Monitor Progress

```bash
# Check logs
tail -f agents/*/adw_plan_iso/execution.log

# Check worktree
ls -la trees/

# Check state
cat agents/*/adw_state.json | jq
```

---

### Common Workflows

#### Workflow 1: Quick Bug Fix

```bash
# Create issue in GitHub with title "Fix login bug"
# Issue number: 456

# Process the bug
cd adws/
uv run adw_plan_build_iso.py 456

# ADW will:
# 1. Create worktree at trees/<adw-id>/
# 2. Generate fix plan
# 3. Implement the fix
# 4. Create PR with fix
```

#### Workflow 2: Complete SDLC with Testing and Review

```bash
# For complex features that need full validation
cd adws/
uv run adw_sdlc_iso.py 789

# This runs:
# 1. Plan - Generate implementation spec
# 2. Build - Implement the solution
# 3. Test - Run test suite
# 4. Review - Validate implementation
# 5. Document - Generate documentation
```

#### Workflow 3: Automated Monitoring

```bash
# Start cron monitor in background
cd adws/
nohup uv run adw_triggers/trigger_cron.py > cron.log 2>&1 &

# Now any new issue or comment with "adw" triggers workflow
# Monitor: tail -f cron.log
```

#### Workflow 4: Webhook for Production

```bash
# Start webhook server
cd adws/
uv run adw_triggers/trigger_webhook.py

# Configure GitHub webhook:
# URL: https://your-domain.com/gh-webhook
# Events: Issues, Issue comments
```

---

### Examples of Typical Workflows

#### Example 1: Feature Implementation

**Scenario**: Add CSV export feature

**Steps**:
1. Create GitHub issue #123 "Add CSV export feature"
2. Run: `uv run adw_plan_build_iso.py 123`
3. ADW classifies as `/feature`
4. Creates plan in `agents/<adw-id>/<adw-id>_plan_spec.md`
5. Implements feature in isolated worktree
6. Creates PR with implementation

**Output**:
- Branch: `feat-123-<adw-id>-add-csv-export`
- Worktree: `trees/<adw-id>/`
- Ports: Backend 9107, Frontend 9207
- PR: Created with full implementation

#### Example 2: Running Multiple Issues Concurrently

**Scenario**: Process 3 issues in parallel

```bash
cd adws/

# Start all three in background
uv run adw_plan_build_iso.py 101 &
uv run adw_plan_build_iso.py 102 &
uv run adw_plan_build_iso.py 103 &

# Each gets isolated:
# - Issue 101: trees/abc12345/, ports 9100/9200
# - Issue 102: trees/def67890/, ports 9107/9207
# - Issue 103: trees/ghi11121/, ports 9103/9203

# Monitor all
tail -f agents/*/*/execution.log
```

#### Example 3: Resume Failed Workflow

**Scenario**: Build phase failed, need to retry

```bash
# Original ADW ID from failed run
ADW_ID="abc12345"

# Resume just the build phase
uv run adw_build_iso.py 123 $ADW_ID

# Or run full pipeline again
uv run adw_plan_build_iso.py 123 $ADW_ID
```

---

### How to Extend/Customize Scripts

#### Adding a New Workflow Command

1. **Create slash command** in `.claude/commands/`:
```bash
# .claude/commands/my-workflow.md
Execute my custom workflow:
1. Analyze the codebase
2. Generate custom output
3. Save results
```

2. **Add to workflow_ops.py**:
```python
# In adw_modules/workflow_ops.py
def execute_my_workflow(issue, adw_id, logger, working_dir=None):
    request = AgentTemplateRequest(
        agent_name="custom_agent",
        slash_command="/my-workflow",
        args=[issue.number],
        adw_id=adw_id,
        working_dir=working_dir
    )
    return execute_template(request)
```

3. **Create entry point script**:
```python
# adws/adw_my_workflow_iso.py
#!/usr/bin/env -S uv run
# ... standard ADW structure ...
```

#### Customizing Model Selection

Edit `adw_modules/agent.py`:
```python
SLASH_COMMAND_MODEL_MAP = {
    "/implement": {"base": "sonnet", "heavy": "opus"},
    "/my-workflow": {"base": "sonnet", "heavy": "opus"},  # Add new
    # ...
}
```

#### Adding Custom State Fields

Edit `adw_modules/state.py`:
```python
class ADWState:
    def __init__(self, adw_id: str):
        self.data = {
            # ... existing fields ...
            "custom_field": None,  # Add new field
        }
```

---

### Common Error Messages and Solutions

#### Error: "No state found for ADW ID"

**Cause**: Trying to run dependent workflow without running entry point first.

**Solution**:
```bash
# Run entry point workflow first
uv run adw_plan_iso.py 123

# Then run dependent workflows
uv run adw_build_iso.py 123 <adw-id>
```

#### Error: "Worktree validation failed"

**Cause**: Worktree directory missing or invalid.

**Solution**:
```bash
# Check worktree exists
ls -la trees/<adw-id

[... content truncated ...]

**Tags**: concrete, general

**Palavras-chave**: Getting, Started

**Origem**: unknown


---


<!-- VERSÍCULO 11/15 - marketplace_optimization_git_repository_20251113.md (100 linhas) -->

# Git & Repository

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### Problem: Git Command Not Recognized

**Symptoms:**
```
'git' is not recognized as an internal or external command
```

**Solution:**
```bash
# 1. Check if Git installed
git --version

# 2. Install Git
# Windows: git-scm.com/download/win
# macOS: brew install git
# Linux: apt-get install git

# 3. Add Git to PATH (Windows)
# System Properties → Environment Variables → PATH
# Add: C:\Program Files\Git\cmd
```

---

### Problem: Permission Denied for Git Operations

**Symptoms:**
```
fatal: could not create work tree dir: Permission denied
permission denied (publickey)
```

**Decision Tree:**

```
Is it read/write permission?
├─ YES → Change directory permissions:
│       chmod -R u+w .git
│
└─ NO (SSH key issue) → Set up SSH key:
        ssh-keygen -t ed25519 -C "your.email@example.com"
        cat ~/.ssh/id_ed25519.pub
        # Add to GitHub: github.com/settings/ssh/new
```

**Solution:**
```bash
# 1. Fix directory permissions
chmod -R u+w .

# 2. Verify Git configuration
git config --list

# 3. Test Git access
git remote -v
git fetch
```

---

### Problem: Cannot Commit - Pre-commit Hook Issues

**Symptoms:**
```
husky: pre-commit hook failed
✔ commit validation FAILED
```

**Solution:**
```bash
# 1. Review hook error message
git commit -m "message" 2>&1 | tail -20

# 2. Run linting manually
python3 -m pylint *.py
python3 -m black .

# 3. Skip hook for debugging (not recommended)
git commit --no-verify -m "message"

# 4. Check hook configuration
cat .git/hooks/pre-commit
```

---

**Tags**: concrete, general

**Palavras-chave**: Repository

**Origem**: unknown


---


<!-- VERSÍCULO 12/15 - marketplace_optimization_git_worktrees_for_parallelization_20251113.md (43 linhas) -->

# Git Worktrees for Parallelization

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

```yaml
concept: "Multiple isolated working directories"

benefits:
  - parallel_agent_execution
  - single_device_multiplication
  - isolated_environments
  - no_interference
  
setup:
  git worktree add ../agent-1 main
  git worktree add ../agent-2 main
  git worktree add ../agent-3 main
  
usage:
  - Each agent works in own directory
  - Results merged back to main
  - Full parallelization achieved

alternatives:
  - Docker containers
  - Virtual machines
  - Cloud instances
```

---

# PART X: ZERO-TOUCH ENGINEERING (ZTE)

**Tags**: abstract, general

**Palavras-chave**: Worktrees, Parallelization

**Origem**: unknown


---


<!-- VERSÍCULO 13/15 - marketplace_optimization_github_utilities_20251113.md (108 linhas) -->

# GitHub Utilities

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### clear_issue_comments.sh - Delete Issue Comments

**Purpose**: Bulk delete comments from a GitHub issue.

**Usage**:
```bash
./scripts/clear_issue_comments.sh <ISSUE_NUMBER>
```

**Arguments**:
- `<ISSUE_NUMBER>` (required) - GitHub issue number to clean

**What it does**:
1. Fetches all comments from the issue
2. Deletes each comment using GitHub CLI
3. Shows progress for each deletion

**Prerequisites**:
- GitHub CLI authenticated (`gh auth login`)
- Write permissions on repository

**Example**:
```bash
# Delete all comments from issue #123
./scripts/clear_issue_comments.sh 123

# Output:
# Fetching comments for issue #123...
# Found 15 comments
# Deleting comment 1/15 (ID: 1234567)...
# Deleting comment 2/15 (ID: 1234568)...
# ...
# All comments deleted successfully
```

**Warning**: This is destructive and cannot be undone. Use with caution.

**When to use**:
- Cleaning up test issues
- Removing ADW bot comments during development
- Resetting issue for fresh ADW run

---

### delete_pr.sh - Delete Pull Request

**Purpose**: Close and optionally delete a pull request and its branch.

**Usage**:
```bash
./scripts/delete_pr.sh <PR_NUMBER> [--delete-branch]
```

**Arguments**:
- `<PR_NUMBER>` (required) - Pull request number
- `--delete-branch` (optional) - Also delete the branch

**What it does**:
1. Fetches PR details
2. Closes the PR
3. Optionally deletes local and remote branch
4. Shows confirmation

**Prerequisites**:
- GitHub CLI authenticated
- Write permissions on repository

**Examples**:
```bash
# Close PR only
./scripts/delete_pr.sh 456

# Close PR and delete branch
./scripts/delete_pr.sh 456 --delete-branch

# Output:
# Fetching PR #456...
# PR Title: feat: add export feature
# Branch: feat-123-abc12345-export
# Closing PR...
# PR closed successfully
# Deleting branch feat-123-abc12345-export...
# Local branch deleted
# Remote branch deleted
# Complete!
```

**When to use**:
- Cleaning up test PRs
- Removing failed ADW PRs
- Resetting workflow state

---

**Tags**: concrete, general

**Palavras-chave**: GitHub, Utilities

**Origem**: unknown


---


<!-- VERSÍCULO 14/15 - marketplace_optimization_governan_a_fluxos_1_20251113.md (33 linhas) -->

# Governança & Fluxos

**Categoria**: marketplace_optimization
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

**Workflow:** Brief → Diagnóstico → **Biblioteca Viva** → Produção (Anúncio/Brand/Agents) → Aprovação → Publicação → Retro & Treino  
**Responsáveis:** Brand Lead • Operações/Marketplace • Conteúdo • TI/Segurança  
**Repositório:** **Biblioteca Viva** (instâncias privadas, copiáveis e versionáveis)  
**Revisões:** quinzenal (conteúdo), mensal (identidade/UX), trimestral (segurança/privacidade)  
**Legal:** INPI/WIPO para nomes/slogans; LGPD; dados não treinam modelos públicos sem consentimento


---

### RAW_015_GENESIS_REPORT.md

# GENESIS KNOWLEDGE ENRICHMENT - CONSOLIDATED REPORT
**Data:** 2 de Novembro de 2025
**Status:** CONSOLIDADO COM SUCESSO
**Versão:** 1.1 Unified
**Consolidação:** Agosto a Novembro 2025

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Governança, Fluxos

**Origem**: desconhecida


---


<!-- VERSÍCULO 15/15 - marketplace_optimization_governan_a_fluxos_20251113.md (20 linhas) -->

# Governança & Fluxos

**Categoria**: marketplace_optimization
**Qualidade**: 0.74/1.00
**Data**: 20251113

## Conteúdo

**Workflow:** Brief → Diagnóstico → **Biblioteca Viva** → Produção (Anúncio/Brand/Agents) → Aprovação → Publicação → Retro & Treino  
**Responsáveis:** Brand Lead • Operações/Marketplace • Conteúdo • TI/Segurança  
**Repositório:** **Biblioteca Viva** (instâncias privadas, copiáveis e versionáveis)  
**Revisões:** quinzenal (conteúdo), mensal (identidade/UX), trimestral (segurança/privacidade)  
**Legal:** INPI/WIPO para nomes/slogans; LGPD; dados não treinam modelos públi

**Tags**: ecommerce, intermediate

**Palavras-chave**: Governança, Fluxos

**Origem**: _CONSOLIDATED_ECOMMERCE_VERSICULOS_FROM_GIT.md


---


<!-- FIM DO CAPÍTULO 38 -->
<!-- Total: 15 versículos, 1189 linhas -->
