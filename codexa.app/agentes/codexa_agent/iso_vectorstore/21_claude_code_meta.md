# Claude Code Meta-Construction Guide | codexa_agent

Otimizações de Claude Code para meta-construction e desenvolvimento agentic.

**Version**: 1.0.0 | **Created**: 2025-11-29
**Purpose**: Maximizar produtividade em workflows de meta-construction
**Context**: CODEXA builders, validators, ADW workflows

---

## 1. Memory Settings (Persistent Context)

### Why Memory Matters

- Sem memory: Repetir instruções de estilo/linguagem toda sessão
- Com memory: Claude já sabe seu contexto CODEXA

### Configuração Recomendada

```markdown
# .claude/memory.md (local ao projeto)

## CODEXA Context
- Agent: codexa_agent (meta-construction)
- Framework: ADW (5 phases), HOP (TAC-7), Trinity Output
- Language: Python 3.11+, TypeScript quando necessário
- Style: Information-dense, keywords not sentences, MAX 1000 LINES

## Meta-Construction Principles
- Build builders, not instances
- OPOP: One Prompt, One Purpose
- Always validate with quality gates
- $arguments chaining between phases

## Output Standards
- .md for humans
- .llm.json for LLM parsing
- .meta.json for metadata (version, quality score)
```

### Como Configurar

1. Pressione `#` no prompt
2. Adicione snippet de contexto
3. Escolha escopo: Local (projeto) ou Global (todas sessões)
4. Edite `.claude/memory.md` diretamente para ajustes

---

## 2. Comandos Personalizados para Meta-Construction

### Estrutura de Comandos

```
.claude/commands/
├── build/
│   ├── agent.md        # Build new agent (5 phases)
│   ├── hop.md          # Build HOP prompt (TAC-7)
│   ├── command.md      # Build slash command
│   └── validator.md    # Build validator
├── validate/
│   ├── hop-sync.md     # Validate HOP compliance
│   ├── doc-sync.md     # Validate documentation
│   └── quality.md      # Validate code quality
└── workflow/
    ├── doc-sync.md     # ADW-100 documentation sync
    └── upgrade.md      # System upgrade workflow
```

### Exemplos de Comandos

**build/agent.md**:
```markdown
Build a new agent following ADW 5-phase workflow:

Agent description: $ARGUMENTS

Execute:
1. PHASE 1 (Plan): Read existing agents, extract patterns
2. PHASE 2 (Build): Generate 8 artifacts
3. PHASE 3 (Test): Run validators
4. PHASE 4 (Review): Check quality gates
5. PHASE 5 (Document): Update registry

Output: Complete agent in agentes/{name}_agent/
```

**validate/hop-sync.md**:
```markdown
Validate HOP file against TAC-7 standard:

File: $ARGUMENTS

Check:
- [ ] MODULE_METADATA complete
- [ ] INPUT_CONTRACT has all required fields
- [ ] OUTPUT_CONTRACT specifies formats
- [ ] TASK has role + objective
- [ ] STEPS numbered (3-7 steps)
- [ ] VALIDATION has quality gates
- [ ] CONTEXT has $arguments chaining

Report: ##report format (JSON + summary)
```

---

## 3. MCP Servers para Meta-Construction

### Servers Recomendados

| Server | Uso | Comando de Ativação |
|--------|-----|---------------------|
| **Context 7** | Docs atualizados de libs | "use context 7" |
| **Scout** | File discovery no projeto | `mcp__scout__discover` |
| **Filesystem** | Operações em arquivos | built-in |

### Context 7 para Frameworks

```markdown
# Quando usar:
- Documentação de libraries que atualizam frequentemente
- APIs de terceiros (Anthropic, OpenAI, etc.)
- Frameworks (FastAPI, Pydantic, etc.)

# Como usar:
"use context 7 para documentação do Pydantic v2"
"use context 7 para Claude API reference"
```

### Scout MCP para Discovery

```python
# Descoberta de arquivos relevantes
mcp__scout__discover(query="create product listing")

# Busca por padrão
mcp__scout__search(pattern="**/*_HOP.md")

# Contexto completo de um agent
mcp__scout__agent_context(agent="codexa_agent")
```

---

## 4. Sub-agentes: TASKS not ROLES

### Princípio Fundamental

**ERRO**: Atribuir papéis ("você é um UX designer")
**CERTO**: Atribuir tarefas específicas ("revise acessibilidade deste form")

### Por que Tasks > Roles

| Roles (Ruim) | Tasks (Bom) |
|--------------|-------------|
| Ambíguo: "seja um expert" | Específico: "valide X contra Y" |
| Context pollution | Context isolation |
| Resultados inconsistentes | Output previsível |
| Difícil de validar | Mensurável |

### Configuração de Sub-agentes

```yaml
# ❌ Nunca faça isso
sub_agents:
  - name: architect
    prompt: "You are a senior software architect"
  - name: reviewer
    prompt: "You are a code reviewer with 10 years experience"

# ✅ Sempre faça isso
sub_agents:
  - name: hop_validator
    task: "Validate HOP against TAC-7 checklist"
    input: $hop_file
    output: validation_report (JSON)
    success_criteria: score >= 0.85

  - name: doc_generator
    task: "Generate README from agent config"
    input: $agent_config
    output: README.md
    template: templates/README_TEMPLATE.md
```

### Quando Usar Sub-agentes

- Tarefas paralelas independentes
- Context window muito grande
- Validação especializada
- Geração de artefatos separados

### Como Invocar

```bash
# Via comando
/agents

# Via @mention no prompt
@hop_validator validate prompts/91_meta_build_agent_HOP.md

# Via Task tool
Task(subagent_type="validator", prompt="...")
```

---

## 5. Mentalidade para Meta-Construction

### Princípio 1: Garbage In, Garbage Out

**Realidade**: Qualidade do output = Qualidade do prompt

**Diagnóstico**:
- Output ruim? → Revise seu prompt primeiro
- Claude "não entende"? → Você não foi claro o suficiente
- Resultados inconsistentes? → Instrução ambígua

**Prática**:
```markdown
# ❌ Prompt vago
"Crie um agent bom"

# ✅ Prompt específico
"Crie um agent seguindo ADW 5-phase workflow:
- Nome: sentiment_agent
- Propósito: Análise de sentimento de reviews
- Input: texto (string), max 5000 chars
- Output: sentiment (positive/neutral/negative), score (0-1)
- Validação: Accuracy >= 0.85 no dataset de teste
- Artefatos: README, INSTRUCTIONS, config.json, tests/"
```

**Use Plan Mode** quando a ideia ainda está vaga:
- Claude faz perguntas de esclarecimento
- Você refina antes de executar
- Menos retrabalho

### Princípio 2: AI Gera, Humano é Dono

**Responsabilidade**: Código vai para produção com SUA assinatura

**Checklist antes de commit**:
```markdown
- [ ] Security: Sem secrets hardcoded, input validado
- [ ] Performance: Sem gargalos óbvios, queries otimizadas
- [ ] Error handling: Casos de falha tratados
- [ ] Tests: Cobertura adequada para código novo
- [ ] Documentation: APIs públicas documentadas
```

**Hábito**:
- Nova sessão → revisar código tocado recentemente
- Antes de merge → validar segurança e performance
- Deploy → você é responsável, não a IA

### Princípio 3: Context is Everything

**Problema comum**: Claude "esquece" contexto ao longo da conversa

**Solução**:
```markdown
# Início de sessão longa
"Contexto atual:
- Trabalhando em: codexa_agent/builders/
- Objetivo: Criar novo validator
- Arquivos relevantes: validators/07_hop_sync_validator.py (referência)
- Padrões: ##report output, score >= 0.85"

# Ao mudar de tarefa
"Mudando contexto:
- De: validator
- Para: HOP prompt
- Novo objetivo: ..."
```

---

## 6. Fluxo de Trabalho Recomendado

### Setup Inicial (Uma Vez)

```
1. Configure Memory
   └── .claude/memory.md com contexto CODEXA

2. Instale Comandos
   └── .claude/commands/ com builders/validators

3. Configure MCP
   └── Context 7 para docs atualizadas
```

### Desenvolvimento (Por Feature)

```
1. Discovery
   ├── mcp__scout__discover para encontrar arquivos relevantes
   └── Ler padrões existentes antes de criar

2. Planning
   ├── Plan mode se ideia vaga
   └── /build/agent para scaffolding

3. Execution
   ├── Sub-agentes para tarefas paralelas
   └── "use context 7" para docs atualizadas

4. Validation
   ├── /validate/hop-sync para HOPs
   └── /validate/quality para código

5. Review
   ├── Human review checklist
   └── Nova sessão → revisar arquivos modificados
```

### Antes de Commit

```
1. Security check
2. Performance check
3. Test coverage
4. Documentation updated
5. Human approval ✓
```

---

## Quick Reference

| Situação | Ação |
|----------|------|
| Repetindo instruções | Configure Memory |
| Docs desatualizadas | "use context 7" |
| Tasks paralelas | Sub-agentes (TASKS not ROLES) |
| Output inconsistente | Melhore o prompt (Garbage In/Out) |
| Antes de deploy | Human review checklist |
| Context pollution | OPOP - um propósito por agent |

---

**Version**: 1.0.0
**Source**: 800+ hours Claude Code usage + CODEXA patterns
**Status**: Production Ready
**Maintainer**: CODEXA Team
