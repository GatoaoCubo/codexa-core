# Template Padrão de Estrutura de Agente CODEXA

> **Versão**: 1.0.0 | **Data**: 2025-11-30

## Estrutura Mínima Obrigatória

```
{agent_name}/
├── PRIME.md              # Entry point - identidade e propósito
├── INSTRUCTIONS.md       # Instruções detalhadas para LLM
├── README.md             # Documentação para humanos
├── SETUP.md              # Guia de configuração
└── iso_vectorstore/      # Knowledge base isolado
    └── 01_QUICK_START.md # Quick start do agente
```

## Estrutura Recomendada (Agente Maduro)

```
{agent_name}/
├── PRIME.md
├── INSTRUCTIONS.md
├── README.md
├── SETUP.md
├── CHANGELOG.md          # Histórico de versões
├── ARCHITECTURE.md       # Arquitetura técnica (opcional)
│
├── iso_vectorstore/      # ⭐ Knowledge Base Isolado
│   ├── 01_QUICK_START.md
│   ├── 02_PRIME.md
│   ├── 03_INSTRUCTIONS.md
│   ├── 04_README.md
│   ├── 05_ARCHITECTURE.md
│   ├── 06_input_schema.json
│   ├── 07_output_template.md
│   ├── 08-10_*.json      # Configs específicas
│   ├── 11_ADW_orchestrator.md
│   ├── 12_execution_plans.json
│   ├── 13-19_HOP_*.md    # HOPs consolidados
│   └── 20_CHANGELOG.md
│
├── config/               # Configurações
│   ├── paths.py
│   └── *.json
│
├── prompts/              # HOPs (Higher-Order Prompts)
│   ├── 10_main_agent_HOP.md
│   ├── 20_*.md
│   └── ...
│
├── workflows/            # ADWs (Agentic Developer Workflows)
│   └── 100_ADW_RUN_{AGENT}.md
│
├── builders/             # Scripts de construção (opcional)
│   └── *.py
│
├── validators/           # Scripts de validação (opcional)
│   └── *.py
│
├── templates/            # Templates de output (opcional)
│   └── *.md
│
├── examples/             # Exemplos de uso (opcional)
│   └── *.md
│
└── outputs/              # Outputs gerados (opcional)
    └── *.md
```

## Campos Obrigatórios por Arquivo

### PRIME.md
```markdown
# {Agent Name}

> **Versão**: X.Y.Z | **Última Atualização**: YYYY-MM-DD

## Identidade
- **Nome**: {agent_name}
- **Tipo**: {Production|Infrastructure|Companion}
- **Domínio**: {descrição do domínio}

## Propósito
{Uma frase clara sobre o que o agente faz}

## Capacidades Principais
1. {Capacidade 1}
2. {Capacidade 2}
3. {Capacidade 3}

## Dependências
- {dependency_1}
- {dependency_2}

## Quick Start
{Como usar em 3 passos}
```

### INSTRUCTIONS.md
```markdown
# Instruções: {Agent Name}

## Contexto
{Contexto para o LLM}

## Regras de Operação
1. {Regra 1}
2. {Regra 2}

## Workflow Principal
{Passo a passo}

## Output Esperado
{Formato do output}
```

### iso_vectorstore/01_QUICK_START.md
```markdown
# Quick Start: {Agent Name}

## O que este agente faz?
{Explicação em 2-3 frases}

## Comando Rápido
{Exemplo de uso}

## Inputs Necessários
- {input_1}
- {input_2}

## Output Gerado
{Descrição do output}
```

## Checklist de Padronização

- [ ] PRIME.md existe e tem identidade clara
- [ ] INSTRUCTIONS.md existe e tem regras completas
- [ ] README.md existe e é útil para humanos
- [ ] SETUP.md existe e tem passos de configuração
- [ ] iso_vectorstore/ existe com pelo menos 01_QUICK_START.md
- [ ] Pelo menos 1 HOP definido em prompts/ ou iso_vectorstore/
- [ ] Pelo menos 1 ADW definido em workflows/ ou iso_vectorstore/
- [ ] CHANGELOG.md para tracking de versões

## Numeração Padrão

### iso_vectorstore/
| Range | Conteúdo |
|-------|----------|
| 01-05 | Docs core (QUICK_START, PRIME, INSTRUCTIONS, README, ARCHITECTURE) |
| 06-07 | Schemas (input, output) |
| 08-10 | Configs específicas do domínio |
| 11-12 | ADWs e execution plans |
| 13-19 | HOPs consolidados |
| 20 | CHANGELOG |

### prompts/
| Range | Conteúdo |
|-------|----------|
| 10 | main_agent_HOP.md |
| 20-90 | HOPs específicos por fase |

### workflows/
| Range | Conteúdo |
|-------|----------|
| 100 | ADW_RUN_{AGENT}.md (workflow principal) |
| 101+ | ADWs adicionais |

---

**Criado por**: CODEXA Meta-Constructor
**Uso**: Template para criação e padronização de agentes
