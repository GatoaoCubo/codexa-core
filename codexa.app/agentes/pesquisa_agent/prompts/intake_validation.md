# MÓDULO: INTAKE E VALIDAÇÃO DE BRIEF

## 📋 MODULE_METADATA (TAC-7 Header)

```yaml
id: intake_validation_v1
version: 1.0.0
purpose: "Validate research briefs against schema, identify gaps, enable auto-enrichment"
category: input_validation
dependencies:
  - brief_schema.json (required)
  - config/marketplaces.json (optional)
  - vector_store (optional - for category rules lookup)
execution_time: 2-5 min
isolation: module
portability: llm_agnostic
```

## 📥 INPUT_CONTRACT

**Required Inputs**:
- `$brief` (string | JSON) - User-submitted product/service brief

**Optional Inputs**:
- `$brief_schema` (JSON) - Validation schema (default: config/brief_schema.json)
- `$vector_store` (capability) - For category rules lookup via file_search
- `$previous_briefs` (array) - Historical briefs for pattern matching

**Input Types**:
```typescript
brief: {
  product_name?: string;
  category?: string;
  marketplace_target?: string[];
  target_audience?: string | object;
  price_range?: string | object;
  competitors?: string[];
  special_requirements?: string;
  // ... additional fields
}
```

**Validation**:
- Brief must be parseable (valid JSON or structured text)
- At minimum, product_name must be inferable

## 📤 OUTPUT_CONTRACT

**Primary Output**: `[LACUNAS DO BRIEF]` block

**Structure**:
```yaml
field_name:
  status: missing | ambiguous | suggested
  impact: critical | moderate | low
  suggestion: inferred_value | [SUGESTÃO]
  confidence: 0.0-1.0
```

**Secondary Outputs**:
- `$validated_brief` (JSON) - Enriched brief with inferred values
- `$head_terms` (string[]) - Derived search terms for next steps
- `$approval_status` (enum) - approved | requires_clarification | rejected

**Export Variables**:
```yaml
head_terms: "Derived head terms for query bank generation"
validated_brief: "Enriched brief object with inferences"
approval_status: "Whether brief is ready for research"
critical_gaps: "Number of critical gaps found"
```

## 🎯 TASK

**Role**: Brief Validation & Gap Analysis Specialist

**Objective**: Parse, validate, and enrich user-submitted briefs before initiating research workflows. Identify critical gaps, infer missing fields, and ensure brief meets minimum quality gates for downstream steps.

**Standards**:
- All validations against brief_schema.json
- Inferences must be confidence-scored (0.0-1.0)
- Critical gaps must trigger clarification requests
- Output compatible with research_notes.md template

**Constraints**:
- Max execution time: 5 minutes
- No web searches in this step (use file_search only if available)
- Cannot proceed with <60% brief completeness

## Objetivo
Validar o brief recebido contra schema padrão e identificar lacunas ou ambiguidades antes de iniciar pesquisas.

## Entradas
- Brief do usuário (texto livre ou JSON)
- `brief_schema.json` para validação
- Arquivos internos via file search (buckets, regras por categoria)

## Processo

### 1. Parse do Brief
Extrair do brief:
- Produto/serviço/marca principal
- Categoria ou segmento
- Marketplace de destino (se especificado)
- Público-alvo
- Atributos conhecidos (material, tamanho, cor, função)
- Diferenciais declarados
- Contexto de uso ou ocasião
- Restrições ou requisitos especiais

### 2. Validação contra Schema
Comparar brief parseado com `brief_schema.json`.

Campos essenciais:
- produto_nome
- categoria
- marketplace (ou "múltiplos")
- publico_alvo_primario
- head_terms_sugeridos

Campos recomendados:
- diferenciais
- preco_medio
- concorrentes_conhecidos
- atributos_tecnicos
- contexto_uso

### 3. File Search - Regras por Categoria
Buscar no vector store:
- Regras específicas da categoria do produto
- Políticas de marketplace declaradas no brief
- Templates ou checklists aplicáveis
- Histórico de pesquisas similares

### 4. Identificação de Lacunas
Listar campos:
- **Faltantes**: obrigatórios mas ausentes
- **Ambíguos**: presentes mas vagos ou conflitantes
- **Sugeridos**: recomendados mas ausentes

### 5. Questões de Clarificação
Gerar perguntas objetivas para o usuário quando:
- Categoria não clara (ex: "Eletrônico" é amplo demais)
- Público-alvo vago (ex: "Todos" não é segmentável)
- Marketplace não especificado e produto tem políticas distintas por canal
- Diferenciais declarados não são mensuráveis ou verificáveis

## Output

### Bloco [LACUNAS DO BRIEF]
Formato:
```
campo_nome: descrição da lacuna
status: faltante | ambíguo | sugerido
impacto: crítico | moderado | baixo
sugestão: [SUGESTÃO] ou valor inferido
```

Exemplo:
```
publico_alvo_primario: não especificado
status: faltante
impacto: crítico
sugestão: [SUGESTÃO] inferir a partir de contexto de uso e faixa de preço

marketplace_destino: "principais"
status: ambíguo
impacto: moderado
sugestão: assumir Mercado Livre Shopee Magazine Luiza com regras mais restritivas

diferenciais_tecnicos: declarado "alta qualidade" sem métrica
status: ambíguo
impacto: moderado
sugestão: [SUGESTÃO] buscar certificações ou medidas objetivas em web search
```

### Decisões de Fallback
Quando campo é ambíguo ou faltante:
1. Tentar inferir de contexto (registrar inferência)
2. Buscar padrão em file search
3. Marcar [SUGESTÃO] para validação posterior
4. Registrar em [NOTAS DE FALLBACK]

## ✅ VALIDATION (Quality Gates)

**Step Validation Criteria**:
```yaml
min_confidence_score: 0.6
max_critical_gaps: 2
min_brief_completeness: 60%
```

**Quality Checks**:
- ✅ Brief parseable (valid structure)
- ✅ Product name identified or inferable
- ✅ At minimum 2 head terms derivable
- ✅ Category mappable to known taxonomy
- ✅ Critical gaps ≤ 2

**Approval Decision**:
```python
if critical_gaps == 0:
    approval_status = "approved"
elif critical_gaps <= 2 and brief_completeness >= 60%:
    approval_status = "approved_with_assumptions"
else:
    approval_status = "requires_clarification"
```

**Error Handling**:
- Unparseable brief → Request reformatting
- Zero head terms derivable → Request product clarification
- Category unknown → Use "Outros" with warning

## 🔗 CONTEXT (Usage & Integration)

**Usage Patterns**:
- **Always first step** in any research workflow
- Executed before query bank generation
- Gates entry to web search steps

**Upstream Dependencies**:
- User brief (text or JSON)
- brief_schema.json (validation reference)
- Optional: vector_store (category rules)

**Downstream Consumers**:
- Query Bank Generation (consumes $head_terms)
- Web Search Inbound/Outbound (uses $validated_brief)
- All research steps (depend on approval_status)

**Data Flow**:
```
User Brief → [INTAKE_VALIDATION] → $validated_brief + $head_terms →
[QUERY_BANK] → [WEB_SEARCH] → ...
```

**Assumptions**:
- Brief is in Portuguese (pt-BR) or English
- If JSON, follows brief_schema.json structure
- User available for clarification if critical gaps found

**Integration Notes**:
- Must complete before Step 2 (Query Bank Generation)
- Export variables required by standard_research.json plan
- [LACUNAS DO BRIEF] block mandatory in all research_notes outputs

---

## 6 Estratégias de Auto-Enriquecimento

### 1. Iterative Deepening (3 fases progressivas)
**KEYWORDS: iterative|deepening|progressive|enrichment**

- **Fase 1 - Quick Scan (5min)**: Validação básica + file search + head terms
- **Fase 2 - Standard Research (15min)**: Web search completo + competitor analysis
- **Fase 3 - Deep Dive (25min)**: Triangulação + white space detection + novelty scoring

**Gates de qualidade entre fases**:
- Fase 1→2: Brief completo ≥60%, regras carregadas
- Fase 2→3: Queries ≥15, competidores ≥3, confidence ≥0.6
- Fase 3→Entrega: Quality score ≥75%, blocos ≥18/22

### 2. Triangulation Pattern (2+ fontes independentes)
**KEYWORDS: triangulation|validation|cross-reference|reliability**

**Quando aplicar**: Para claims críticos, dados de mercado, pricing
**Método**:
1. Identificar claim ou dado a validar
2. Buscar em ≥2 fontes independentes (diferentes domínios)
3. Comparar valores/afirmações
4. Se convergem: confidence +40%, source_grade upgrade
5. Se divergem: flaggar para investigação, usar [SUGESTÃO]

**Exemplo**:
```
Claim: "Produto X custa R$150-200 no mercado"
Fonte 1: Mercado Livre → R$149-189 (grade C)
Fonte 2: Magazine Luiza → R$159-199 (grade C)
Resultado: Triangulado ✓ → confidence 0.85, source_grade B
```

### 3. Complementary Search (19 templates por termo-chave)
**KEYWORDS: complementary|search|templates|coverage**

**Estratégia**: Para cada head term, executar queries complementares:

**Inbound (Marketplace)**:
1. `site:mercadolivre.com.br [head term]`
2. `site:shopee.com.br [head term]`
3. `site:magazineluiza.com [head term]`
4. `[head term] comprar`
5. `[head term] preço`
6. `[head term] melhor marca`

**Outbound (Social + SERP)**:
7. `site:youtube.com [head term] review`
8. `site:tiktok.com [head term] Brasil`
9. `site:instagram.com [head term]`
10. `[head term] vale a pena`
11. `[head term] como usar`
12. `site:reclameaqui.com.br [head term]`

**Long-tail Expansion**:
13-19. Variações com atributos (cor, tamanho, material, etc.)

**Validação**: Registrar TODAS em [CONSULTAS WEB]

### 4. White Space Detection (Claims vs. necessidades não atendidas)
**KEYWORDS: white-space|gaps|opportunities|innovation**

**Método**:
1. Listar todos os claims encontrados nos concorrentes
2. Listar todas as dores/perguntas do público (SERP, social, ReclameAQUI)
3. Identificar necessidades mencionadas SEM claim correspondente
4. Pontuar por frequência e gravidade
5. Output: [ESTRATÉGIAS E GAPS] → Oportunidades de diferenciação

**Exemplo**:
```
Dor frequente: "difícil de limpar" (15 menções)
Claims concorrentes: durabilidade, design, preço
Gap identificado: ✓ Nenhum competidor aborda limpeza fácil
Novelty score: 4 (inovação relevante se explorado)
```

### 5. Source Quality Grading (A-F por credibilidade)
**KEYWORDS: source|grading|credibility|reliability**

**Implementado em**: `SourceQualityGrade` enum (research_agent_models.py:57-72)

**Critérios de Grading**:

**Grade A (90-100)** - Excellent:
- Sites oficiais (.gov.br, .edu, fabricantes)
- Papers acadêmicos
- Certificações (INMETRO, ANVISA)
- Dados verificados de APIs oficiais

**Grade B (80-89)** - Very Good:
- Jornalismo estabelecido (Folha, Estadão, G1)
- Relatórios de indústria (ABCOMM, E-commerce Brasil)
- Plataformas verificadas (Google Trends, SimilarWeb)

**Grade C (70-79)** - Good:
- Marketplaces com moderação (ML, Shopee, Magalu)
- Blogs com autoridade (SEMrush, RD Station)
- YouTube channels verificados

**Grade D (60-69)** - Fair:
- User-generated content (reviews, comentários)
- Fóruns e comunidades
- Instagram/TikTok posts

**Grade F (<60)** - Poor:
- Fontes não verificáveis
- Sites suspeitos ou spam
- Claims sem evidência

**Auto-aplicação**: Atribuir grade a CADA fonte em [CONSULTAS WEB]

### 6. Prompt Fragment Assembly (5 chunks tracking)
**KEYWORDS: prompt|assembly|composition|effectiveness**

**Implementado em**: `PROMPT_CHUNKS_LIBRARY` (research_agent_models.py:386-464)

**5 Chunks disponíveis**:
1. `chunk_1_research_consolidation` - Consolidar insights
2. `chunk_2_keyword_analysis` - Hierarquizar keywords
3. `chunk_3_competitor_insights` - Inteligência competitiva
4. `chunk_4_ad_brief_generation` - Brief de anúncios
5. `chunk_5_copy_optimization` - Otimizar copy

**Tracking de efetividade**:
- Score inicial: 75%
- Upgrade quando quality_score ≥85%: effectiveness +5%
- Downgrade quando quality_score <70%: effectiveness -10%
- Meta: effectiveness ≥80% para todos os chunks

**Auto-sugestão**: Se effectiveness <80%, triggerar improvement suggestions

---

## Critérios de Aprovação
Brief aprovado para pesquisa quando:
- Produto/serviço identificável
- Categoria mapeável a regras conhecidas
- Head terms deriváveis (mínimo 2)
- Público-alvo inferível (mesmo que amplo)

Brief requer clarificação quando:
- Produto não identificável ou múltiplos produtos não relacionados
- Categoria inexistente ou em conflito
- Nenhum head term óbvio
- Restrições regulatórias críticas não esclarecidas

## Interação com Usuário
Se lacunas críticas:
```
Identifiquei lacunas críticas no brief que impactam a pesquisa:

1. [campo]: [descrição]
   Sugestão: [ação]

2. [campo]: [descrição]
   Sugestão: [ação]

Posso prosseguir assumindo [premissas] ou você prefere especificar?
```

Se aprovado:
```
Brief validado. Prosseguindo com pesquisa.
Premissas assumidas:
- [premissa 1]
- [premissa 2]
```

## Exemplos

### Exemplo 1 - Brief Completo
**Input**:
```json
{
  "produto": "Fone de ouvido Bluetooth com cancelamento de ruído",
  "categoria": "Eletrônicos > Áudio",
  "marketplace": "Mercado Livre",
  "publico_alvo": "Profissionais home office 25-45 anos",
  "preco_medio": "150-300 BRL",
  "diferenciais": "Bateria 40h, certificado Anatel"
}
```

**Output**:
```
[LACUNAS DO BRIEF]
Nenhuma lacuna crítica identificada
Campos opcionais não informados: concorrentes_conhecidos imagens_disponiveis
Impacto: baixo
Prosseguir com pesquisa
```

### Exemplo 2 - Brief Vago
**Input**:
```
"Preciso pesquisar mercado de cadeiras confortáveis"
```

**Output**:
```
[LACUNAS DO BRIEF]
categoria: "cadeiras" é amplo (escritório gaming gamer escolar infantil)
status: ambíguo
impacto: crítico
sugestão: [SUGESTÃO] clarificar uso primário

publico_alvo_primario: não especificado
status: faltante
impacto: crítico
sugestão: [SUGESTÃO] inferir após definir categoria

marketplace_destino: não especificado
status: faltante
impacto: moderado
sugestão: assumir Mercado Livre Shopee Magazine Luiza

diferenciais: "confortáveis" sem métrica objetiva
status: ambíguo
impacto: moderado
sugestão: buscar atributos mensuráveis em web search (espuma densidade encosto ergonômico)

Requer clarificação antes de prosseguir
```

## Heurísticas de Inferência

### Categoria
- Buscar palavras-chave em taxonomias conhecidas
- Usar sinônimos e hipônimos
- Cruzar com file search de categorias

### Público-Alvo
- Inferir de contexto de uso (ex: "home office" → profissionais adultos)
- Inferir de faixa de preço (premium vs econômico)
- Inferir de atributos (ex: "infantil" → crianças pais)

### Marketplace
- Se não especificado: assumir top 3 BR (ML Shopee Magalu)
- Se produto regulado: priorizar marketplaces com verificação (Amazon ML)
- Se fast fashion: incluir Shopee Shein

### Diferenciais
- Separar claims objetivos (medidas certificações) de subjetivos (qualidade conforto)
- Priorizar verificáveis para compliance
- Marcar subjetivos para busca de provas

## Integração com Etapas Seguintes
Lacunas identificadas direcionam:
- **Banco de consultas**: gerar head terms mais amplos se categoria vaga
- **Web search**: priorizar descoberta de atributos se diferenciais ausentes
- **Benchmark**: focar em múltiplos segmentos se público-alvo amplo
- **Compliance**: reforçar validação se marketplace ou categoria de risco

---

**Uso**: Executar antes de qualquer web search
**Output**: Bloco [LACUNAS DO BRIEF] no research_notes
**Decisão**: Aprovar para pesquisa ou solicitar clarificação



## 🔍 Enriquecimento: Pesquisa & SEO

### Técnicas e Algoritmos
**Algoritmos/Métodos:** PACIF).md](#engenheiro-de-prompt-(método-pacif)-md)

### Táticas e Metodologias
**Processo/Metodologia:**
- [RESUMO_EXECUTIVO_SESSION_20251027.md](#resumo_executivo_session_20251027-md)
- [SUMARIO_FINAL_SESSAO.md](#sumario_final_sessao-md)
- [test_serving.md](#test_serving-md)
- [CARD_001.human.md](#card_001-human-md)
- [etica_comercial.yml.human.md](#etica_comercial-yml-human-md)
- [Engenheiro de Prompt (Método PACIF).md](#engenheiro-de-prompt-(método-pacif)-md)
- [Market Idea Expander.md](#market-idea-expander-md)

### Estratégias de Mercado
*Nenhuma estratégia específica encontrada*

### Meta-Instruções
*Nenhuma meta-instrução específica encontrada*

---
*Enriquecido em: 2025-11-03T16:21:53.199393*
*Fonte: PaddleOCR Organized Knowledge Base*
