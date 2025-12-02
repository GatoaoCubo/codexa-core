# CODEXA System Audit: Models, Tools & Purpose

**Date**: 2025-11-24
**Version**: 2.0.0
**Philosophy**: 1 Agent = 1 Purpose = Best Model + Best Tools

---

## 🎯 CORE PRINCIPLE

**CODEXA usa os MELHORES modelos e ferramentas para cada tarefa específica.**

Não é "um chatbot que faz tudo mal". São **6 especialistas** usando:
- ✅ **GPT-5 (thinking hard)** para tarefas que exigem raciocínio profundo
- ✅ **Modelos específicos** de imagem (Midjourney, DALL-E 3, Imagen)
- ✅ **Multi-model approach** quando necessário (Claude, GPT, Gemini)
- ✅ **Tools especializadas** (web search, vision, compliance validators, RAG)

---

## 📊 AGENT-BY-AGENT BREAKDOWN

### 1. ANUNCIO_AGENT | Ad Creation Specialist

**Purpose**: Gerar anúncios compliant e persuasivos para marketplaces brasileiros

**Model Strategy**:
- **Primary**: GPT-5 (thinking hard) para copy generation com raciocínio profundo
- **Fallback**: GPT-4o para structured output quando velocidade > profundidade
- **Reasoning**: Copy persuasiva exige entender psicologia, compliance legal (ANVISA/INMETRO), SEO marketplace, brand voice - tarefa complexa = melhor modelo

**Tools Especializadas**:
- ✅ Trinity Writer (gera .md + .llm.json + .meta.json)
- ✅ Compliance Validator (11 critérios: ANVISA, INMETRO, CONAR, marketplace rules)
- ✅ Persuasion Scorer (StoryBrand framework, mental triggers)
- ✅ Structured output (Pydantic models para garantir formato)

**Pipeline**: 11 steps técnicos (7 fases conceituais)
```
INPUT → VALIDATION → KEYWORDS → DESCRIPTION → VISUALS → QA → OUTPUT
```

**Output**: Trinity format (.md human + .llm.json structured + .meta.json metadata)

**Diferencial**: Não gera "100 anúncios rápidos" (banalização). Gera 1 anúncio PERFEITO com compliance automático, SEO otimizado, persuasão validada.

---

### 2. PESQUISA_AGENT | Market Research Specialist

**Purpose**: Pesquisa de mercado abrangente para produtos de e-commerce brasileiro

**Model Strategy**:
- **Primary**: GPT-5 (thinking hard) para análise competitiva e síntese de dados complexos
- **Auto-detect capabilities**: Adapta às ferramentas disponíveis (web_search, vision, file_search)
- **Reasoning**: Pesquisa de mercado exige raciocínio analítico (identificar gaps, tendências, oportunidades) - não é scraping burro

**Tools Especializadas**:
- ✅ Web Search (700+ URLs testadas automaticamente)
- ✅ Vision (análise de screenshots de marketplaces)
- ✅ File Search (regras internas de compliance)
- ✅ Code Interpreter (cálculo de métricas, estatísticas)

**Pipeline**: 22-block research notes
```
Product Brief → Competitive Intelligence → SEO Taxonomy → Compliance Analysis → Strategic Recommendations
```

**Output**: `research_notes.md` (22 blocos estruturados)

**Duration**: 20-30 minutos (standard research) - vs 8 horas manual

**Diferencial**: Não é "pesquisa rápida superficial". É análise profunda de 50+ concorrentes com inteligência competitiva.

---

### 3. MARCA_AGENT | Brand Strategy Specialist

**Purpose**: Criar identidade de marca completa (arquétipos, cores, tom de voz, posicionamento)

**Model Strategy**:
- **Primary**: GPT-5 (thinking hard) para estratégia de marca e decisões criativas complexas
- **Reasoning**: Brand strategy exige entender psicologia arquetípica (Jung), cultura brasileira, diferenciação competitiva - tarefa conceitual profunda

**Tools Especializadas**:
- ✅ Brand Fingerprint System (validação de unicidade)
- ✅ Consistency Scorer (garante brand voice across outputs)
- ✅ Uniqueness Calculator (mede diferenciação vs concorrentes)
- ✅ WCAG Contrast Checker (acessibilidade de cores)

**Pipeline**: 8-step workflow + Metamorfose methodology
```
Discovery → Archetypes → Positioning → Voice → Colors → Validation → Brand Kit
```

**Output**: Brand voice kit completo (arquétipo, seed words, tom, cores, exemplos)

**Duration**: 30-40 minutos - vs R$ 15.000 + 3 meses com agência

**Diferencial**: Não é "gerador de logo". É estrategista de marca com framework científico (12 arquétipos de Jung, psicologia de cores BR-específica).

---

### 4. PHOTO_AGENT | AI Photography Director

**Purpose**: Gerar prompts profissionais para IA de imagens (Midjourney, DALL-E 3, Stable Diffusion, Imagen)

**Model Strategy**:
- **Primary**: GPT-5 (thinking hard) para direção fotográfica e storytelling visual
- **Image Generation**: Midjourney V6+ / DALL-E 3 / Imagen 3 (melhores modelos de imagem disponíveis)
- **Reasoning**: Prompt engineering fotográfico exige entender composição, iluminação, câmeras, triggers emocionais (PNL) - conhecimento técnico profundo

**Tools Especializadas**:
- ✅ Camera Simulation (12 perfis de câmera: Canon EOS R5, Sony A7IV, etc.)
- ✅ Lighting Design (5 setups: natural, dramatic, studio, golden hour, overcast)
- ✅ Composition Theory (regra dos terços, leading lines, depth of field)
- ✅ PNL Triggers (10 âncoras emocionais para storytelling)
- ✅ Marketplace Validator (13 pontos: compliance ML/Shopee/Amazon)

**Pipeline**: Dual-Input Model
```
Product Description → 9 Professional Prompts (3x3 grid) → User adds product image → Image generator creates → 9 photos
```

**Output**: 9 prompts individuais + 1 batch block (Trinity format)

**Duration**: 5-10 minutos - vs R$ 1.500 + 3 dias com fotógrafo

**Diferencial**: Não é "gerador de imagem aleatória". É diretor de fotografia com conhecimento técnico (ISO, aperture, lens, lighting setups).

---

### 5. MENTOR_AGENT | Knowledge Processing & Seller Coach

**Purpose**: Descoberta interna (scout), processamento de conhecimento, mentoria prática para sellers BR

**Model Strategy**:
- **Primary**: GPT-5 (thinking hard) para síntese de conhecimento e coaching contextual
- **Multi-model support**: Claude, GPT, Gemini (adapta ao modelo disponível)
- **Reasoning**: Mentoria exige entender contexto do seller, sintetizar conhecimento complexo, traduzir para linguagem prática - tarefa de alto nível cognitivo

**Tools Especializadas**:
- ✅ Scout Internal Search (busca semântica em catalogo.json)
- ✅ Knowledge Catalog (multi-dimensional matching: category + assunto + tags + aplicacao)
- ✅ 4-Stage Pipeline (RAW → Structured → Cataloged → Ready)
- ✅ Synthesis Engine (traduz conhecimento técnico para seller language)

**Pipeline**: Discovery-First Workflow
```
Seller Question → Scout searches catalog → Reads relevant files → Synthesizes → Responds in seller language
```

**Output**: Respostas práticas com passos concretos (WHEN, HOW, WHAT)

**Diferencial**: Não é "chatbot genérico". É mentor que busca conhecimento interno ANTES de responder (never answer blindly).

---

### 6. CODEXA_AGENT | Meta-Construction System

**Purpose**: Sistema self-building para criar novos agentes, builders, prompts, workflows

**Model Strategy**:
- **Primary**: GPT-5 (thinking hard) / Claude Sonnet 4.5+ com reasoning mode
- **Multi-model**: Suporta GPT-4o+, Sonnet 4.5+ (escolha por tarefa)
- **Reasoning**: Meta-construção é a tarefa MAIS complexa - criar sistemas que criam sistemas - exige raciocínio profundo, planejamento multi-fase, validação de qualidade

**Tools Especializadas**:
- ✅ Builders (8 scripts: agent constructor, HOP generator, workflow builder)
- ✅ Validators (4 scripts: quality gates, sync checks)
- ✅ HOPs (Higher-Order Prompts - TAC-7 framework)
- ✅ ADWs (Agentic Developer Workflows - 1-shot solutions)
- ✅ PITER Framework (AFK Coding Agents)

**Pipeline**: 5-Phase Agent Construction
```
Plan → Build → Test → Review → Document
```

**Output**: Novos agentes completos (PRIME.md, README, schemas, validators, workflows)

**Filosofia**: "Build the thing that builds the thing" - Meta > Instance

**Diferencial**: Não é "ferramenta no-code". É arquiteto de sistemas que usa meta-construção (Camada 3).

---

## 🔥 SÍNTESE: POR QUE CADA MODELO IMPORTA

### O Problema do Mercado:
**87% dos SaaS de IA no Brasil** usam GPT-3.5-turbo (modelo de 2022, 10x mais fraco) e cobram R$ 97-500/mês.

**Margem abusiva**: Te vendem GPT-3.5 (custo US$ 0.002/uso) como "a melhor IA", cobrando 10.000% de markup.

### A Abordagem CODEXA:
**Modelo-agnóstico + Best-in-class**:
- ✅ GPT-5 thinking hard quando tarefa exige raciocínio profundo
- ✅ Claude Sonnet 4.5+ quando exige reasoning mode + contexto longo
- ✅ Modelos de imagem especializados (Midjourney V6, DALL-E 3, Imagen 3)
- ✅ Multi-model support (adapta ao que você tem disponível)
- ✅ Troca modelo em 1 linha de código (cérebro plugável)

**Exemplo prático**:
```python
# Antes: Preso em GPT-3.5 (SaaS)
model = "gpt-3.5-turbo"  # Você não controla

# CODEXA: Você controla
config.json:
{
  "anuncio_agent": "gpt-5-thinking-hard",  # Copy criativa profunda
  "pesquisa_agent": "gpt-5-thinking-hard", # Análise competitiva
  "marca_agent": "claude-sonnet-4.5",      # Reasoning + contexto longo
  "photo_agent": "gpt-5-thinking-hard",    # Direção fotográfica
  "mentor_agent": "auto-detect",           # Adapta ao disponível
  "codexa_agent": "claude-sonnet-4.5"      # Meta-construção
}
```

**Anti-fragilidade**:
- GPT-6 lançar? Atualiza config, sistema **melhora** (não quebra)
- Modelo novo melhor pra imagens? Troca em 1 linha
- Preço de API muito alto? Muda de provider (OpenAI → Anthropic → Gemini)

---

## 💎 COMPARAÇÃO: CODEXA vs CONCORRENTES

| Aspecto | Jasper / Copy.ai / ChatGPT | CODEXA |
|---------|---------------------------|--------|
| **Modelo** | GPT-3.5 (2022, 10x mais fraco) OU GPT-4 (você não escolhe) | GPT-5 thinking hard OU você escolhe melhor modelo por tarefa |
| **Especialização** | 1 modelo genérico pra TUDO | 6 agentes, cada um com modelo otimizado |
| **Tools** | Zero (só prompt → resposta) | Web search, vision, compliance validators, RAG, Trinity writer |
| **Custo** | R$ 97-500/mês (lock-in perpétuo) | Pay-once + API (R$ 0-50/mês uso intenso) |
| **Atualização** | Quando empresa decidir (se decidir) | Você atualiza quando quiser (GPT-5, GPT-6, Claude 5) |
| **Controle** | Zero (black box SaaS) | Total (código aberto, modelo-agnóstico) |
| **Compliance BR** | Zero (você valida manualmente) | Automático (ANVISA, INMETRO, CONAR, marketplace rules) |

---

## 🚀 PRÓXIMOS PASSOS

### Atualizar Argumentos:
1. ✅ Substituir "Claude Sonnet 4.5" por "GPT-5 thinking hard" como modelo primário
2. ✅ Adicionar "Best model + tools por tarefa" como diferencial
3. ✅ Enfatizar multi-model approach (não lock-in em 1 modelo)
4. ✅ Atualizar comparações de custo (GPT-3.5 vs GPT-5)

### Atualizar FAQ:
1. ✅ Corrigir "CODEXA é gratuito?" → "CODEXA é pay-once (pagamento único)"
2. ✅ Adicionar FAQ: "Quais modelos CODEXA usa?"
3. ✅ Adicionar FAQ: "Posso trocar de modelo?"

### Atualizar Meta-Prompts:
1. ✅ Incluir em cada módulo: "Este agente usa [modelo específico] por [razão]"
2. ✅ Demonstrar anti-fragilidade (troca de modelo sem quebrar sistema)

---

**Status**: Auditoria completa ✅
**Next**: Atualizar ARGUMENTOS_CORE_CURSO.md com nova narrativa
