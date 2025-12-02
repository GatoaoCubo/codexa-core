# 🚀 Quick Start - ADW Workflows

Guia rápido para executar workflows ADW (Agentic Developer Workflow) no CODEXA.

## 📋 Comandos Disponíveis

### 1. Listar Workflows Disponíveis

```bash
/adw-list
```

Mostra todos os 5 workflows ADW com especificações completas.

---

### 2. Executar Workflow Completo

```bash
/prime {agent_name} [input]
```

**Agentes disponíveis**:
- `pesquisa` - Pesquisa de mercado
- `anuncio` - Geração de anúncios
- `mentor` - Mentoria para vendedores
- `marca` - Estratégia de marca
- `photo` - Prompts de fotografia AI

---

## 🎯 Exemplos de Uso

### Pesquisa de Mercado (20-30min)

```bash
/prime pesquisa Product: Garrafa térmica de aço inox, Category: Casa e Cozinha, Audience: 25-45 anos fitness, Price: R$ 80-250
```

**Output**:
- `user_research/garrafa_termica_research_notes.md` (22 blocos)
- `user_research/garrafa_termica_metadata.json`
- `user_research/garrafa_termica_queries.json`

**Quality Gates**: Score ≥0.75, Completeness ≥75%, Queries ≥15

---

### Geração de Anúncios (23-38min)

```bash
/prime anuncio USER_DOCS/produtos/research/garrafa_termica_research_notes.md
```

**Output**:
- `USER_DOCS/anuncios/garrafa_termica/garrafa_termica_ad_copy.md`
- `USER_DOCS/anuncios/garrafa_termica/garrafa_termica_ad_copy.llm.json`
- `USER_DOCS/anuncios/garrafa_termica/garrafa_termica_ad_copy.meta.json`

**Quality Gates**: Score ≥0.85, Keyword density 0.70-0.80

---

### Mentoria para Vendedores (16-31min)

```bash
/prime mentor Como otimizar títulos de produtos no Mercado Livre sem violar regras de compliance?
```

**Output**:
- Resposta de mentoria estruturada (Summary + Action Plan + Resources + Next Steps)

**Quality Gates**: Score ≥0.87, Skill gaps ≥2, Resources ≥3

---

### Estratégia de Marca (21-36min)

```bash
/prime marca Business: Garrafas térmicas sustentáveis premium, Mission: Reduzir plástico descartável através de produtos duráveis e design atraente, Vision: Ser referência em sustentabilidade no Brasil, Values: Sustentabilidade, Qualidade, Design, Target: Millennials urbanos eco-conscientes 25-40 anos
```

**Output**:
- `USER_DOCS/marcas/garrafa_sustentavel/brand_strategy.md` (30+ blocos)
- `USER_DOCS/marcas/garrafa_sustentavel/validation_report.txt`
- Brand consistency score

**Quality Gates**: Consistency ≥0.85, Values 3-5, Positioning ≤2 sentences

---

### AI Photography Prompts (15-30min)

```bash
/prime photo subject=Garrafa térmica de aço inox, style=minimalist
```

**Output**:
- `USER_DOCS/photos/garrafa_termica/photo_prompts.md` (9 prompts individuais + 1 batch)
- `USER_DOCS/photos/garrafa_termica/photo_prompts.llm.json`
- `USER_DOCS/photos/garrafa_termica/photo_prompts.meta.json`

**Quality Gates**: Score ≥7.0/10, All prompts ≥80 words, 9 scenes validated

---

## 🏗️ Como Funciona (Arquitetura Dual-Layer)

### Layer 1: ADW (Orchestration)
Define **O QUE** fazer e **QUANDO** fazer.

```
agentes/{agent}_agent/workflows/100_ADW_RUN_{AGENT}.md
```

**Contém**:
- Fases numeradas (5-9 fases por workflow)
- Objetivos de cada fase
- Critérios de validação
- Gates de qualidade
- Error handling

### Layer 2: HOP (Execution)
Define **COMO** fazer em detalhes.

```
agentes/{agent}_agent/prompts/{module}_HOP.md
```

**Contém**:
- Instruções passo-a-passo
- Exemplos completos
- Templates
- Checklists de validação
- Soluções de erro

---

## 📊 Fluxo de Execução

```
1. LOAD CONTEXT
   ├─ Read PRIME.md (agent instructions)
   ├─ Read 100_ADW_RUN_{AGENT}.md (workflow orchestration)
   └─ Read config/*.json (domain knowledge)

2. EXECUTE PHASES (1 → 2 → ... → N)
   For each phase:
   ├─ Announce: "🔄 Phase {N}: {Phase Name}"
   ├─ Load HOP prompt (detailed instructions)
   ├─ Execute HOP steps
   ├─ Validate outputs (quality gates)
   └─ Report: "✅ Phase {N} completed"

3. GENERATE OUTPUT
   ├─ Assemble final deliverables
   ├─ Trinity format (.md + .llm.json + .meta.json) OR
   └─ Agent-specific format

4. REPORT COMPLETION
   ├─ Duration: {actual}min (target: {min}-{max}min)
   ├─ Quality score: {score}/1.0
   ├─ Files saved: {paths}
   └─ Next steps: {recommendations}
```

---

## ✅ Validation & Quality Gates

Todos os workflows aplicam gates de qualidade:

| Agent | Quality Threshold | Key Metrics |
|-------|-------------------|-------------|
| pesquisa | ≥0.75 | Completeness ≥75%, Queries ≥15 |
| anuncio | ≥0.85 | Keyword density 0.70-0.80 |
| mentor | ≥0.87 | Skill gaps ≥2, Resources ≥3 |
| marca | ≥0.85 | Brand consistency, Values 3-5 |
| photo | ≥7.0/10 | Prompts ≥80 words, 9 scenes |

**Se validação falhar**:
- **WARN** (0.70-0.84): Reporta issues, pergunta se deve continuar
- **FAIL** (<0.70): HALT workflow, reporta erros específicos
- **RETRY**: Aplica solução sugerida e re-executa fase

---

## 📚 Documentação Completa

### Relatório Técnico
`ADW_TEST_REVIEW_REPORT.md` - Review completo com:
- Análise estrutural de todos os 5 workflows
- Inventário de arquivos (37 HOP prompts, 17 configs)
- Padrões arquiteturais (Micro-Modular, Monolítico, Balanceado)
- Status funcional (5/5 agents PRODUCTION-READY)

### Comandos
`.claude/commands/` - Slash commands disponíveis:
- `prime.md` - Comando /prime (executor principal)
- `adw-list.md` - Comando /adw-list (listar workflows)
- `README.md` - Documentação de comandos

### Workflows
`agentes/*/workflows/100_ADW_RUN_*.md` - Orquestradores ADW:
- pesquisa_agent (9 fases, 12 HOP prompts)
- anuncio_agent (7 fases, 10 HOP prompts)
- mentor_agent (6 fases, 8 HOP prompts)
- marca_agent (7 fases, 2 HOP prompts)
- photo_agent (5 fases, 5 HOP prompts)

---

## 🎓 Workflow Chain Example

Exemplo de cadeia completa (pesquisa → anuncio → photo):

### Step 1: Market Research
```bash
/prime pesquisa Product: Smartwatch fitness, Category: Eletrônicos, Audience: 20-35 anos fitness, Price: R$ 300-800
```
**Output**: `user_research/smartwatch_research_notes.md`

### Step 2: Ad Generation
```bash
/prime anuncio user_research/smartwatch_research_notes.md
```
**Output**: `USER_DOCS/anuncios/smartwatch/smartwatch_ad_copy.*`

### Step 3: Photography Prompts
```bash
/prime photo subject=Smartwatch fitness, style=lifestyle
```
**Output**: `USER_DOCS/photos/smartwatch/photo_prompts.*`

**Total Duration**: ~60-100min
**Complete Deliverables**: Research + Ad copy + Photo prompts

---

## 🚦 Status

**Production Status**: ✅ **READY**

- 5/5 agents funcionais
- 34 fases totais
- 37 HOP prompts (~982KB knowledge base)
- 17 config files (all valid JSON)
- Modo conversacional (Phase A) pronto
- Python automation (Phase B) planejado

---

## 🆘 Troubleshooting

### "Quality score below threshold"
→ Workflow pausará e reportará issues específicos
→ Revise input ou aceite qualidade reduzida (se score ≥0.70)

### "Missing config files"
→ Verifique que agente tem todos os arquivos em `config/`
→ Execute validação: todos os 17 configs testados como JSON válido

### "HOP prompt not found"
→ Verifique path: `agentes/{agent}_agent/prompts/{module}.md`
→ Todos os 37 HOP prompts estão presentes e validados

### "Phase validation failed"
→ Leia error message específico
→ Aplique correção sugerida
→ Workflow tentará RETRY automaticamente

---

## 📞 Support

**Issues**: Report em `ADW_TEST_REVIEW_REPORT.md` seção "Issues & Recommendations"
**Documentation**: Consulte `.claude/commands/README.md`
**Workflow Specs**: Leia `agentes/*/workflows/100_ADW_RUN_*.md`

---

**Version**: 1.0.0
**Last Updated**: 2025-11-24
**Maintainer**: CODEXA Meta-Constructor
