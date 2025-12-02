# PROMPT_ENGINEERING Knowledge Base

> Conhecimento extraído de 106 system prompts de ferramentas AI

## Quick Start

```bash
# 1. Listar ferramentas disponíveis
python scripts/pipeline_extract.py --mode list

# 2. Processar todas (requer ANTHROPIC_API_KEY)
export ANTHROPIC_API_KEY=sk-ant-xxx
python scripts/pipeline_extract.py --mode full

# 3. Ou processar sem LLM (extração básica)
python scripts/pipeline_extract.py --mode full --no-llm

# 4. Gerar knowledge cards
python scripts/pipeline_synthesize.py --mode all

# 5. Verificar estatísticas
python scripts/pipeline_extract.py --mode stats
```

## Estrutura

```
PROMPT_ENGINEERING/
├── README.md                   # Este arquivo
├── extraction_schema.json      # Schema de extração
├── catalogo_prompts.json       # Índice master
│
├── raw_extractions/            # Stage 1: JSONs por ferramenta
│   ├── cursor_Agent_Prompt_2.0.json
│   ├── claude_code_system_prompt.json
│   └── ...
│
├── patterns/                   # Stage 3a: Knowledge cards de padrões
│   ├── pattern_tool_calling_YYYYMMDD.md
│   ├── pattern_agent_loop_YYYYMMDD.md
│   └── ...
│
├── techniques/                 # Stage 3b: Knowledge cards de técnicas
│   ├── technique_xml_structure_YYYYMMDD.md
│   └── ...
│
├── comparisons/                # Stage 3c: Análises comparativas
│   ├── compare_coding_ide_YYYYMMDD.md
│   └── ...
│
├── playbook_prompt_engineering_YYYYMMDD.md  # Stage 4: Guia consolidado
│
└── scripts/
    ├── pipeline_extract.py     # Extração (Stage 1)
    └── pipeline_synthesize.py  # Síntese (Stage 3-4)
```

## Pipeline de 4 Estágios

### Stage 1: Extração
```
FONTES/ai_tools_prompts/ → raw_extractions/*.json
```
- Lê prompts originais (106 arquivos)
- Extrai estrutura, patterns, técnicas via Claude API
- Fallback para extração regex se API indisponível

### Stage 2: Análise (automático)
```
raw_extractions/*.json → catalogo_prompts.json
```
- Indexa patterns por frequência
- Agrupa técnicas cross-platform
- Identifica padrões universais vs específicos

### Stage 3: Síntese
```
catalogo_prompts.json → patterns/ + techniques/ + comparisons/
```
- Gera knowledge cards por tema (não por ferramenta)
- Consolida implementações de múltiplas fontes
- Extrai best practices

### Stage 4: Consolidação
```
Tudo → playbook_prompt_engineering.md
```
- Guia definitivo para devs CODEXA
- Checklist de implementação
- Rankings de ferramentas

## Ferramentas Processadas

### Coding IDEs (6)
- Cursor, Windsurf, Augment Code, VS Code Agent, Xcode, Trae

### AI Agents (7)
- Devin, Manus, Lovable, Same.dev, Junie, Kiro, Emergent

### Open Source (6)
- Cline, Bolt, RooCode, Codex CLI, Gemini CLI, Lumo

### Platforms (7)
- Claude Code, Anthropic, Replit, v0, Perplexity, Notion AI, Gemini

### Enterprise (14)
- Cluely, CodeBuddy, Comet Assistant, AMP, Qoder, Orchids, Leap, Poke, Warp, Dia, Traycer, Zai Code

## Patterns Rastreados

| Pattern | Descrição |
|---------|-----------|
| `tool_calling` | Como ferramentas são definidas e chamadas |
| `agent_loop` | Ciclo de execução (think → act → observe) |
| `error_handling` | Tratamento de erros e retry |
| `context_management` | Gerenciamento de contexto/memória |
| `code_generation` | Geração de código novo |
| `code_editing` | Edição de código existente |
| `search_strategy` | Busca em codebase |
| `task_management` | Gerenciamento de tarefas (todos) |
| `memory_persistence` | Persistência de conhecimento |
| `security_constraints` | Restrições de segurança |
| `communication_style` | Tom e estilo de comunicação |
| `planning_mode` | Modo de planejamento |

## Schema de Extração

Cada extração contém:

```json
{
  "metadata": {
    "ferramenta": "cursor",
    "versao": "Agent Prompt 2.0",
    "categoria": "coding_ide",
    "modelo_base": "gpt-4.1",
    "tokens_original": 4500
  },
  "estrutura": {
    "secoes_detectadas": [...],
    "formatacao": {
      "usa_xml_tags": true,
      "usa_markdown": true,
      "usa_json_schemas": true
    }
  },
  "patterns": [...],
  "techniques": [...],
  "insights_codexa": [...],
  "metricas": {
    "clareza": 0.85,
    "completude": 0.80,
    "reusabilidade": 0.75,
    "inovacao": 0.70
  }
}
```

## Como Usar o Conhecimento

### Para Desenvolvedores CODEXA

1. **Consultar playbook**: `playbook_prompt_engineering_*.md`
2. **Estudar patterns específicos**: `patterns/pattern_*.md`
3. **Ver implementações de referência**: `raw_extractions/*.json`

### Para Novos Agentes

1. Verificar checklist no playbook
2. Implementar patterns universais primeiro
3. Adicionar técnicas específicas conforme necessidade

### Para Debugging

1. Comparar com `comparisons/compare_*.md`
2. Verificar se patterns críticos estão implementados
3. Consultar exemplos de ferramentas similares

## Métricas de Qualidade

| Dimensão | Descrição | Target |
|----------|-----------|--------|
| Clareza | Quão claro é o prompt | > 0.85 |
| Completude | Cobre todos os casos | > 0.80 |
| Reusabilidade | Fácil de adaptar | > 0.75 |
| Inovação | Técnicas diferenciadas | > 0.70 |

## Dependências

```bash
pip install anthropic  # Para extração com LLM
# Stdlib: json, pathlib, datetime, argparse, re, collections
```

## Contribuindo

1. Adicionar novos prompts em `FONTES/ai_tools_prompts/`
2. Executar `pipeline_extract.py --mode single --tool <nome>`
3. Regenerar síntese: `pipeline_synthesize.py --mode all`

---

**Versão**: 1.0.0
**Criado**: 2025-12-01
**Mantido por**: CODEXA Team
