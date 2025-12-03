# PROMPT: Redesenhar CLAUDE.md v2.0

**Objetivo**: Criar CLAUDE.md v2.0 com baixa entropia, meta-construído, que dê autonomia para LLMs executarem sem supervisão.

---

## CONTEXTO COLETADO (10 Scouts)

### Scout 1: Agent Structures
- 11 agentes encontrados
- Fractal compliance: 55-90%
- Gaps comuns: context/, validators/, builders/
- Padrão consistente: PRIME.md + INSTRUCTIONS.md + README.md

### Scout 2: Workflow Patterns
- 27 ADWs descobertos
- 150+ fases totais
- Pattern dominante: LINEAR (70%)
- Quality gates: ≥7.0/10.0 padrão
- Dual-layer architecture: ADW ↔ HOP

### Scout 3: Template Patterns
- 1,978 placeholders encontrados
- 3 sintaxes diferentes:
  - {UPPERCASE_NAME} (80%)
  - [OPEN_VARIABLE: NAME] (15%)
  - {$variable} (4%)
- {{MUSTACHE}} compliance: 0% (CLAUDE.md define mas ninguém usa!)

### Scout 4: Slash Commands
- 43 comandos totais
- 28 global, 15 agent-specific
- Categorias: navigation, workflow, build, utility, orchestration
- Pattern: /prime-* (navigation), /codexa-* (meta-construction)

### Scout 5: MCP Integration
- 4 MCPs funcionando: scout, browser, codexa-commands, voice
- 1 configurado mas não buildado: playwright
- Gap: CLAUDE.md só menciona Scout, faltam os outros 3

### Scout 6: Documentation Patterns
- Score geral: 7.8/10
- Mix de idiomas: 60% EN / 40% PT
- Redundância: README ↔ PRIME overlap
- Best documented: anuncio_agent, codexa_agent
- Worst documented: database schema, deployment

### Scout 7: Error Patterns
- 7+ gaps críticos (subprocess sem check, webhook loops)
- 150+ try/except blocks
- Retry logic sofisticado em apenas 1 arquivo (agent.py)
- Falta: Error Recovery LAW

### Scout 8: Dependencies Map
- 15+ integrações externas
- Custo estimado: R$260-735/mês
- Críticas: Anthropic API, Supabase, Shopify
- Opcionais: ElevenLabs, Runway, Pika

### Scout 9: Brand Context
- 248+ violações hardcoded
- Principais: "codexa", "gatoaocubo", hex colors
- CLAUDE.md linha 20-22 viola sua própria LAW 1!
- qa_gato3_agent: 35+ violações

### Scout 10: Meta-Patterns
- 12 padrões implícitos descobertos:
  1. Fractal Directory Architecture
  2. Ordinal Sequencing (numbered files)
  3. Mustache Placeholder Convention
  4. Trinity Output Format (.md + .llm.json + .meta.json)
  5. HOP Framework (Higher-Order Prompts)
  6. ADW Layer (AI Developer Workflows)
  7. Path Registry as Single Source of Truth
  8. Command Naming Convention
  9. ISO_VECTORSTORE (knowledge base pattern)
  10. Execution Plans as Data (JSON workflows)
  11. Quality Gates and Validation Layers
  12. Agentic Architecture for LLM Composition

---

## PROBLEMAS IDENTIFICADOS NO CLAUDE.md ATUAL

### Entropia Alta (45% eficiência)
1. LAW 1 muito verbosa (82 linhas, tabela inline)
2. LAW 2 muito curta (14 linhas, sem exemplos)
3. LAW 4 superficial (define "o quê" não "como")
4. LAW 5 NÃO É LAW (é workflow específico com hardcoded)

### Contradições
1. LAW 5 ↔ LAW 1: LAW 5 tem "gatoaocubo" hardcoded
2. LAW 6 ↔ NEVER: "Run .py files directly" vs `python script.py`
3. CLAUDE.md linha 20-22 viola sua própria LAW 1

### Gaps
1. Error Handling não documentado
2. Ordinal Sequencing (padrão de numeração) implícito
3. Trinity Output não mencionado
4. HOP Framework não referenciado
5. 4 MCPs existem, só 1 documentado

### Estruturais
1. TOOLS no meio das LAWs (quebra fluxo)
2. Mix PT/EN inconsistente
3. NEVER/ALWAYS redundante com LAW 1

---

## REQUISITOS PARA CLAUDE.md v2.0

### Princípios
1. **Baixa entropia**: Máxima informação em mínimo espaço
2. **Meta-construído**: Segue suas próprias regras
3. **Autonomia-first**: LLM deve poder executar sem perguntar
4. **Sem contradições**: Todas as LAWs devem ser compatíveis
5. **Referências externas**: Tabelas grandes vão para docs/

### Estrutura Proposta

```markdown
# CLAUDE.md - Project Laws

## IDENTITY
[Nome, versão, propósito em 3 linhas]

## CORE LAWS

### LAW 1: DISTILLATION
[Compacta: princípio + trigger + validação]
[Tabela de placeholders → referência externa]

### LAW 2: FRACTAL NAVIGATION
[Expandida: princípio + estrutura + exemplo visual]

### LAW 3: META-CONSTRUCTION
[Mantém: 4 princípios concisos]

### LAW 4: AGENTIC DESIGN
[Expandida: estrutura + comportamento + composição]

### LAW 5: ORDINAL SEQUENCING (NOVA)
[Padrão de numeração de arquivos]
[00-09 foundation, 10-90 execution, 100+ workflows]

### LAW 6: EXECUTION INTELLIGENCE
[Corrigida: remover contradição com NEVER]

### LAW 7: ERROR RECOVERY (NOVA)
[Padrões de erro, retry, fallback]

## TOOLS
[Seção separada das LAWs]

### Navigation
- /prime, /prime-*

### Meta-Construction
- /codexa-build-*, /codexa-orchestrate

### MCP Servers
- scout (discover, smart_context, search)
- browser (screenshot, extract, marketplace_search)
- codexa-commands (list, get, execute)
- voice (listen, speak)

## CONSTRAINTS

### NEVER
[Lista consolidada, sem redundância]

### ALWAYS
[Lista consolidada, sem redundância]

## REFERENCES
- docs/PLACEHOLDERS.md (tabela completa)
- docs/WORKFLOWS.md (27 ADWs)
- docs/API_KEYS_REFERENCE.md

## METADATA
Version: 2.0.0
Updated: 2025-12-03
Type: Project Laws (Auto-loaded)
```

---

## TAREFAS PARA EXECUTAR

1. **Criar docs/PLACEHOLDERS.md**
   - Mover tabela de 12 placeholders do LAW 1 atual
   - Adicionar placeholders descobertos pelos scouts
   - Total: ~25 placeholders padronizados

2. **Criar docs/WORKFLOWS.md**
   - Listar 27 ADWs descobertos
   - Formato: nome, path, fases, trigger

3. **Reescrever CLAUDE.md**
   - Seguir estrutura proposta acima
   - Máximo 200 linhas (atual tem 302)
   - Idioma: EN (consistente)
   - Sem hardcoded brand content

4. **Validar**
   - Nenhuma contradição entre LAWs
   - Todas as referências existem
   - Próprio arquivo segue LAW 1 (distillation)

---

## OUTPUT ESPERADO

1. `docs/PLACEHOLDERS.md` - Tabela completa de placeholders
2. `docs/WORKFLOWS.md` - Referência de ADWs
3. `CLAUDE.md` v2.0 - Arquivo principal redesenhado
4. Relatório de validação

---

## CRITÉRIOS DE SUCESSO

- [ ] Entropia < 30% (vs 45% atual)
- [ ] Zero contradições entre LAWs
- [ ] Zero hardcoded brand content
- [ ] Todas as 7 LAWs acionáveis
- [ ] LLM consegue executar autonomamente lendo apenas CLAUDE.md
- [ ] Máximo 200 linhas

---

**Executor**: Claude Code (novo terminal)
**Modelo recomendado**: Opus (tarefa complexa de redesign)
**Tempo estimado**: 30-45 minutos
