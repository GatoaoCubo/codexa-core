# SPEC: Landing Page CODEXA.APP + Video Promo

**Version**: 2.0.0 | **Date**: 2025-11-30
**Task**: Criar LP completa + video promo + video 10min via Lovable
**Executor**: codexa_agent
**Status**: REFINADO

---

## OBJETIVO

Criar uma landing page **DISRUPTIVA e ELEGANTE** para o **codexa.app** - um E-com Language Model que combina 3 agentes de IA para sellers de marketplace escalarem com vantagem competitiva.

### Posicionamento (da Brand Strategy)
> "Meta-Construction AI for E-commerce" - Não somos mais uma ferramenta de IA. Somos a camada de inteligência especializada que se pluga em qualquer LLM (GPT, Claude, Gemini) e a eleva ao nível de expertise máxima em e-commerce brasileiro.

### Diferencial Visual Obrigatorio
**NAO PODE PARECER**: Sites tech/vibe coding Lovable genericos
**DEVE PARECER**: Elegancia tecnologica com profundidade, categoria propria

---

## PATHS MAPEADOS

### 1. LOVABLE - Comandos e Prompts

| Path | Descricao | Uso |
|------|-----------|-----|
| `FONTES/ai_tools_prompts/lovable/Agent Prompt.txt` | System prompt do Lovable | Entender como o Lovable funciona, guidelines, workflow |
| `FONTES/ai_tools_prompts/lovable/Agent Tools.json` | Tools disponiveis no Lovable | Lista de ferramentas: lov-write, lov-line-replace, imagegen, websearch |

**Tools Lovable Disponiveis**:
- `lov-write` - Criar/sobrescrever arquivos
- `lov-line-replace` - Editar linhas especificas
- `lov-search-files` - Buscar no codebase
- `lov-fetch-website` - Capturar conteudo web
- `lov-download-to-repo` - Baixar assets
- `imagegen--generate_image` - Gerar imagens (flux.schnell, flux.dev)
- `websearch--web_search` - Pesquisa web

---

### 2. CURSO_AGENT - Templates e Argumentos para LP

| Path | Descricao | Uso |
|------|-----------|-----|
| `codexa.app/agentes/curso_agent/prompts/HOP_LANDING_PAGE.md` | HOP para gerar landing pages | Template de estrutura |
| `codexa.app/agentes/curso_agent/outputs/sales/LANDING_PAGE_FREEMIUM.md` | **LP Freemium completa** | REFERENCIA PRINCIPAL - estrutura, copy, specs |
| `codexa.app/agentes/curso_agent/outputs/sales/LANDING_PAGE_HOTMART.md` | LP Hotmart | Referencia de copy |
| `codexa.app/agentes/curso_agent/outputs/sales/LANDING_PAGE.md` | LP base | Estrutura base |
| `codexa.app/agentes/curso_agent/prompts/HOP_VIDEO_SCRIPT.md` | HOP para video scripts | Template para videos |
| `codexa.app/agentes/curso_agent/templates/TEMPLATE_VIDEO_SCRIPT.md` | Template video | Estrutura de roteiro |
| `codexa.app/agentes/curso_agent/context/PRODUCAO_VIDEO_M0.md` | Producao video M0 | Guidelines producao |
| `codexa.app/agentes/curso_agent/builders/02_video_script_builder.py` | Builder de video | Referencia de geracao |

---

### 3. MARCA_AGENT - Branding e-Commerce

| Path | Descricao | Uso |
|------|-----------|-----|
| `codexa.app/agentes/marca_agent/outputs/brand_strategy/brand_strategy_codexa_v2.md` | **Brand Strategy CODEXA** | CORE - voz, tom, posicionamento |
| `codexa.app/agentes/marca_agent/outputs/consolidated/brand_book_executive_summary.md` | Brand Book resumo | Guidelines visuais |
| `codexa.app/agentes/marca_agent/iso_vectorstore/15_brand_archetypes.md` | Arquetipos de marca | Personalidade |
| `codexa.app/agentes/marca_agent/iso_vectorstore/10_brand_rules.json` | Regras de marca | Consistencia |
| `codexa.app/agentes/marca_agent/prompts/01_brand_identity_HOP.md` | HOP identidade | Guidelines criacao |

---

### 4. MENTOR_AGENT - Conhecimento e-Commerce

| Path | Descricao | Uso |
|------|-----------|-----|
| `codexa.app/agentes/mentor_agent/PRIME.md` | PRIME Mentor | Orquestracao |
| `codexa.app/agentes/mentor_agent/PROCESSADOS/MARCA_branding_*.md` (01-03) | Conhecimento branding | Estrategia marca |
| `codexa.app/agentes/mentor_agent/PROCESSADOS/MARCA_visual_*.md` (01-10) | Conhecimento visual | Design guidelines |
| `codexa.app/agentes/mentor_agent/PROCESSADOS/ANUNCIO_marketplace_*.md` (01-62) | Conhecimento marketplace | Best practices |
| `codexa.app/agentes/mentor_agent/PROCESSADOS/ANUNCIO_copywriting_*.md` (01-04) | Conhecimento copy | Tecnicas escrita |
| `codexa.app/agentes/mentor_agent/PROCESSADOS/LIVRO_marketplace_INDEX.md` | Index marketplace | Navegacao conteudo |

---

### 5. CORE AGENTS (O Produto codexa.app)

| Path | Descricao | Uso |
|------|-----------|-----|
| `codexa.app/agentes/pesquisa_agent/PRIME.md` | **PRIME Pesquisa** | Features pesquisa mercado |
| `codexa.app/agentes/pesquisa_agent/INSTRUCTIONS.md` | Instructions pesquisa | Capacidades |
| `codexa.app/agentes/anuncio_agent/PRIME.md` | **PRIME Anuncio** | Features geracao anuncios |
| `codexa.app/agentes/anuncio_agent/INSTRUCTIONS.md` | Instructions anuncio | Capacidades |
| `codexa.app/agentes/photo_agent/PRIME.md` | **PRIME Photo** | Features geracao fotos |
| `codexa.app/agentes/photo_agent/INSTRUCTIONS.md` | Instructions photo | Capacidades |

---

## DELIVERABLES

### 1. Landing Page (Lovable)

**Sections obrigatorias** (baseado em LANDING_PAGE_FREEMIUM.md):
1. Hero - Headline + CTA
2. Problema - 3 pain points do seller
3. Solucao - Diagrama 3 camadas
4. Features - Os 3 agentes combinados
5. Video embed - Video promo
6. Transformacao - Antes/Depois
7. Social Proof - Depoimentos
8. CTA Final - Captura
9. Footer

**Tech Stack Lovable**:
- React + Vite + TypeScript
- Tailwind CSS
- shadcn/ui components

**Cores** (do brand):
```css
--primary: #10B981;    /* Verde CTA */
--secondary: #3B82F6;  /* Azul info */
--warning: #F59E0B;    /* Amarelo */
--premium: #8B5CF6;    /* Roxo premium */
```

### 2. Video Promo (30-60s)

**Objetivo**: Apresentar o codexa.app de forma impactante

**Estrutura sugerida**:
- 0-5s: Hook visual + problema
- 5-15s: Apresenta solucao (3 agentes)
- 15-25s: Demo rapida das features
- 25-30s: CTA

### 3. Video 10 Minutos (Educacional)

**Conteudo** (baseado em LANDING_PAGE_FREEMIUM.md):
- 00:00 - Problema comum do seller
- 02:00 - O que e o codexa.app
- 04:00 - Os 3 agentes explicados
- 06:00 - Demo pratica
- 08:00 - Resultados esperados
- 09:30 - Como comecar

---

## PROMPT PARA LOVABLE

```
Crie uma landing page moderna e responsiva para o codexa.app - uma plataforma que combina 3 agentes de IA para sellers de marketplace:

1. PESQUISA AGENT - Pesquisa de mercado automatizada
2. ANUNCIO AGENT - Geracao de anuncios otimizados
3. PHOTO AGENT - Geracao de prompts para fotos profissionais

Use as seguintes guidelines:
- Design system com cores: Verde #10B981 (CTA), Azul #3B82F6 (info), Roxo #8B5CF6 (premium)
- Font: Inter para headings e body
- Estilo: Clean, profissional, tech-forward
- Mobile-first responsive

Sections:
[Inserir estrutura da LANDING_PAGE_FREEMIUM.md]

Gere imagens hero usando flux.dev para elementos visuais.
```

---

## ORDEM DE EXECUCAO RECOMENDADA

1. **Ler** `LANDING_PAGE_FREEMIUM.md` - entender estrutura completa
2. **Ler** `brand_strategy_codexa_v2.md` - capturar voz/tom
3. **Ler** PRIMEs dos 3 agents - entender features
4. **Criar** prompt detalhado para Lovable
5. **Executar** no Lovable com iteracoes
6. **Gerar** assets visuais (flux.dev)
7. **Criar** roteiro video promo
8. **Criar** roteiro video 10min

---

## ARQUIVOS CRITICOS PARA CONTEXTO LOVABLE

Prioridade de leitura para ultrathink:

```
MUST READ:
├── FONTES/ai_tools_prompts/lovable/Agent Prompt.txt
├── codexa.app/agentes/curso_agent/outputs/sales/LANDING_PAGE_FREEMIUM.md
├── codexa.app/agentes/marca_agent/outputs/brand_strategy/brand_strategy_codexa_v2.md
├── codexa.app/agentes/pesquisa_agent/PRIME.md
├── codexa.app/agentes/anuncio_agent/PRIME.md
└── codexa.app/agentes/photo_agent/PRIME.md

SHOULD READ:
├── codexa.app/agentes/curso_agent/prompts/HOP_LANDING_PAGE.md
├── codexa.app/agentes/curso_agent/prompts/HOP_VIDEO_SCRIPT.md
├── codexa.app/agentes/marca_agent/outputs/consolidated/brand_book_executive_summary.md
└── codexa.app/agentes/mentor_agent/PROCESSADOS/LIVRO_marketplace_INDEX.md

NICE TO HAVE:
├── codexa.app/agentes/mentor_agent/PROCESSADOS/MARCA_branding_01.md
├── codexa.app/agentes/mentor_agent/PROCESSADOS/ANUNCIO_copywriting_01.md
└── codexa.app/agentes/curso_agent/context/PRODUCAO_VIDEO_M0.md
```

---

## REFINAMENTOS VALIDADOS

### 1. Publico-Alvo
**Sellers de TODOS os niveis** que precisam de um E-com Language Model para escalar com vantagem sobre concorrentes.

### 2. CTA Principal
**Conteudo educacional gratuito + Quick Wins**
- Baseado no Modulo 0 do curso_agent
- Quick Wins ja estao prontos em `curso_agent/context/01_MODULO_INTRODUCAO.md`

**Quick Wins a destacar**:
1. META-PROMPT - "Voce e um construtor de prompts..."
2. PLAN - "Cria um plano para [X]. Me mostra antes de executar."
3. IMPLEMENT - "Aprovo. Entrega em formato portatil."

### 3. Backend
**Apenas frontend** - LP estatica, CTA para conteudo externo

### 4. Design Guidelines (CRITICO)

**TOM DE VOZ**: Disruptivo-Sofisticado
```
Formal ──────────●───── Casual (60% formal)
Sério ───────●────────── Divertido (70% sério)
Técnico ●──────────────── Simples (90% técnico)
Establishment ────────────● Anti-establishment (80% anti)
```

**ARQUETIPOS**:
- **Primario**: CRIADOR - "Construimos o que nunca existiu"
- **Secundario**: SABIO - "Conhecimento e poder, protege-lo e sabedoria"
- **Terciario**: REBELDE (elegante) - "Chega de vender sua alma para IA generica"

**PERSONALIDADE (SOMOS)**:
- Arquitetos de Inteligencia
- Anti-Vendedores (nao vendemos curso/template)
- Future-Proof Fanatics
- Guardioes de Conhecimento
- Elegantemente Superiores
- Tecnicamente Brutais

**PERSONALIDADE (NAO SOMOS)**:
- Genericos
- Vendedores de Sonho
- Barulhentos
- Prompts-as-a-Service

**TAGLINES APROVADAS**:
- "O cerebro que transforma LLMs genericas em especialistas da SUA marca"
- "Camada acima das LLMs. Categoria propria. Zero competicao."
- "Pare de entregar seu conhecimento de bandeja. Construa seu cerebro proprietario."
- "CODEXA = Novo BTC do conhecimento"

---

**Created**: 2025-11-30
**Author**: Claude (path mapping)
**Next**: codexa_agent executa com Lovable

---

> "Os 3 agentes em harmonia: pesquisa informa, anuncio converte, foto encanta."
