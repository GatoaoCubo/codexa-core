# MÓDULO: WEB SEARCH INBOUND (MARKETPLACES)

## 📋 MODULE_METADATA (TAC-7 Header)

```yaml
id: web_search_inbound_v1
version: 1.0.0
purpose: "Execute marketplace searches (BR platforms) to extract SEO patterns, competitors, pricing"
category: data_collection
dependencies:
  - config/accessible_urls.md (relevant sections)
  - web_search capability (required for most modules)
execution_time: 8-10 min
isolation: module
portability: llm_agnostic
```

## 📥 INPUT_CONTRACT

**Required Inputs**:
- `$query_list` - Input parameter
- `$validated_brief.marketplace_target` - Input parameter

**Optional Inputs**: (see original content below)

## 📤 OUTPUT_CONTRACT

**Primary Outputs**: `[SEO INBOUND]`, `[PADRÕES DE LINGUAGEM]`, `[CONSULTAS WEB]`

**Export Variables**:
```yaml
competitors: "Competitor products found in marketplaces"
marketplace_patterns: "Title and messaging patterns"
```

## 🎯 TASK

**Role**: Data Collection Specialist
**Objective**: Execute marketplace searches (BR platforms) to extract SEO patterns, competitors, pricing
**Standards**: (see original content below)
**Constraints**: Max execution time: 8-10 min, All queries logged

## ✅ VALIDATION (Quality Gates)

(See original content for specific validation criteria)

## 🔗 CONTEXT (Usage & Integration)

**Upstream Dependencies**: Previous steps in execution plan
**Downstream Consumers**: Subsequent steps + output blocks
**Data Flow**: (see original content)

---



## Objetivo
Pesquisar sistematicamente marketplaces brasileiros para coletar padrões de anúncios, claims, provas, preços e estratégias competitivas.

## Escopo OBRIGATÓRIO
Pesquisar **mínimo 3 marketplaces BR por head term**.

### Marketplaces Prioritários e URLs Base

**IMPORTANTE**: Consulte `config/accessible_urls.md` para URLs completas e padrões testados.

| Marketplace | Domain | Prioridade | Use para |
|-------------|--------|------------|----------|
| Mercado Livre | mercadolivre.com.br | 1 | Todas as categorias |
| Shopee | shopee.com.br | 2 | Preço competitivo, promoções |
| Magazine Luiza | magazineluiza.com.br | 3 | Eletrônicos, casa |
| Amazon BR | amazon.com.br | 4 | Premium, reviews |
| Americanas | americanas.com.br | 5 | Varejo tradicional |
| Casas Bahia | casasbahia.com.br | 6 | Eletrodomésticos, móveis |
| TikTok Shop | shop.tiktok.com | 7 | Moda, beleza, viral |
| Shein | br.shein.com | 8 | Fast fashion |
| Submarino | submarino.com.br | 9 | Livros, eletrônicos |

**Método de Coleta**:
- Use URLs testadas de `accessible_urls.md` (Seção: URLS BASE E PADRÕES)
- Captura visual: screenshot + GPT-5 Vision
- Sem APIs diretas (anti-scraping ready)

Adaptação por categoria:
- Moda: incluir Shein, Shopee, TikTok Shop
- Eletrônicos: priorizar ML, Amazon, Magalu
- Casa e decoração: Magalu, Casas Bahia, ML
- Beleza: Shopee, Amazon, Americanas

## Templates de Consulta

**FONTE**: `config/accessible_urls.md` (Seção: PADRÕES DE QUERY)

### Consulta Base (Google Search)
```
site:{marketplace} "{head_term}"
```

### URLs Diretas (Preferencial - Uso Visual)

**Mercado Livre**:
```
https://www.mercadolivre.com.br/jm/search?as_word={{HEAD_TERM}}
https://www.mercadolivre.com.br/jm/search?as_word={{HEAD_TERM}}&sort=price_asc
https://www.mercadolivre.com.br/jm/search?as_word={{HEAD_TERM}}&sort=relevance
```

**Shopee**:
```
https://www.shopee.com.br/search?keyword={{HEAD_TERM}}
https://www.shopee.com.br/search?keyword={{HEAD_TERM}}&sort=sales
https://www.shopee.com.br/search?keyword={{HEAD_TERM}}&sort=price
```

**Amazon BR**:
```
https://www.amazon.com.br/s?k={{HEAD_TERM}}
https://www.amazon.com.br/s?k={{HEAD_TERM}}&sort=price-asc-rank
https://www.amazon.com.br/s?k={{HEAD_TERM}}&sort=review-rank
```

**Magazine Luiza**:
```
https://www.magazineluiza.com.br/busca/{{HEAD_TERM}}/
```

### Consulta com Longtail
```
site:{marketplace} "{head_term} {atributo}"
```
Atributos: material, cor, tamanho, voltagem, compatibilidade

### Consulta Comparativa
```
site:{marketplace} "{head_term}" melhor avaliado
site:{marketplace} "{head_term}" mais vendido
site:{marketplace} "{head_term}" lançamento
```

### Consulta de Faixa de Preço
```
site:{marketplace} "{head_term}" até {valor}
site:{marketplace} "{head_term}" a partir de {valor}
```

### Método de Coleta Visual

Para cada URL:
1. **Capture screenshot** da página de resultados (SERP)
2. **Identifique top 3-5 produtos** mais relevantes
3. **Capture screenshot** de 1-2 páginas de detalhes
4. **Analise com GPT-5 Vision** extraindo:
   - Título estruturado
   - Preço (único, faixa, ou com desconto)
   - Rating e volume de avaliações
   - Atributos visíveis (cor, tamanho, marca)
   - Badges e selos (frete grátis, certificação)
   - Imagens (quantidade e tipo)
   - Claims na descrição
5. **Registre em [CONSULTAS WEB]**:
   ```
   termo: {{head_term}}
   fonte: {{nome_marketplace}}
   data: {{YYYY-MM-DD}}
   URL: {{url_usada}}
   insight: {{padrão_observado_max_140_chars}}
   ```

## Dados a Coletar

### 1. Padrões de Título
Estrutura observada:
- Ordem de elementos (marca > produto > atributo > benefício)
- Tamanho típico (caracteres)
- Uso de números e símbolos
- Presença de claims (original lacrado garantia)
- Presença de especificações técnicas

Exemplo de registro:
```
marketplace: Mercado Livre
padrão: [Marca] [Produto] [Especificação] [Benefício] [Diferencial]
exemplo: "Fone JBL Tune 510BT Bluetooth Sem Fio 40h Bateria Original"
caracteres: 45-65 típico
```

### 2. Atributos Destacados
Registrar atributos mais presentes em títulos e descrições:
- Técnicos (medidas, capacidades, materiais)
- Benefícios (economia, durabilidade, praticidade)
- Provas (certificações, garantias, selos)
- Diferenciais (exclusivo, lançamento, edição limitada)

### 3. Claims Recorrentes
Claims encontrados em múltiplos anúncios:
- Produto original
- Garantia estendida
- Frete grátis
- Entrega rápida
- Certificação (Anatel, Inmetro, etc)
- Satisfação garantida

Validar se claim é:
- **Verificável**: com prova ou selo visível
- **Genérico**: presente em muitos concorrentes
- **Diferenciador**: raro e relevante

### 4. Faixa de Preços
Por head term e principais variações:
- Preço mínimo observado
- Preço máximo observado
- Preço modal (mais frequente)
- Média ponderada (se possível inferir)

Registrar contexto:
```
head_term: fone bluetooth
marketplace: Mercado Livre
faixa: 50-800 BRL
modal: 120-180 BRL
nota: preços >500 são modelos premium com cancelamento ruído
```

### 5. Provas Sociais
- Número de avaliações (range observado)
- Rating médio (range observado)
- Perguntas respondidas (presença/ausência)
- Medalhas/selos do marketplace (vendedor pro, full, plus)
- Volume de vendas (quando exibido)

### 6. Imagens e Recursos Visuais
Padrões observados:
- Fundo branco vs lifestyle vs detalhes técnicos
- Número de imagens (range)
- Presença de vídeo
- Infográficos ou comparativos
- Imagens de embalagem/certificação

### 7. Políticas e Operações
- Prazo de envio típico
- Opções de frete (grátis, expresso, retirada)
- Política de devolução (dias, condições)
- Formas de pagamento destacadas
- Parcelamento típico

### 8. Selos e Certificações
- Selos de marketplace (produto oficial, importado autorizado)
- Certificações técnicas (Anatel, Inmetro, CE, FCC)
- Garantias (fabricante, vendedor, estendida)
- Programas especiais (fidelidade, cashback)

## Processo de Coleta

### Para cada head term:

1. **Executar consulta base** em cada marketplace prioritário
2. **Analisar primeiros 10-15 resultados** (primeira página)
3. **Registrar padrões** em cada categoria de dados
4. **Identificar outliers** (anúncios muito diferentes)
5. **Coletar concorrentes** relevantes para benchmark posterior
6. **Registrar consulta** em [CONSULTAS WEB]

### Registro de Consulta
Formato obrigatório:
```
termo: {head_term}
fonte: {nome_marketplace}
data: {YYYY-MM-DD}
insight: {padrão_chave_observado}
```

Exemplo:
```
termo: fone bluetooth
fonte: Mercado Livre
data: 2025-11-03
insight: 80% dos títulos incluem duração de bateria; claim "original" em 60% dos anúncios top
```

## Output: Blocos Afetados

### [SEO INBOUND]
```
padrão de título eficaz: [estrutura observada]
atributo que melhora ranqueamento: [atributo + contexto]
combinação longtail com benefício: [exemplo]
sinal de prova que diferencia: [tipo de prova + impacto]
```

### [ANÁLISE DE CONCORRENTES]
Para cada concorrente relevante:
```
nome: [marca ou produto]
forças: [claims, provas, diferenciais]
preço médio: [valor ou faixa]
```

### [BENCHMARK DE CONCORRENTES]
```
faixa de preço predominante: [range por marketplace]
taxa de avaliações média: [rating de X.X]
padrão visual: [fundo branco, lifestyle, etc]
claims mais frequentes: [lista]
políticas recorrentes: [prazo, devolução, etc]
```

### [PADRÕES DE LINGUAGEM EFICAZ]
```
estrutura de título de alta conversão: [padrão]
atributos priorizados: [lista ordenada]
provas típicas: [certificações, garantias]
```

## Exemplo Completo

**Head term**: fone bluetooth
**Marketplaces**: Mercado Livre, Shopee, Magazine Luiza

### Consultas
```
site:mercadolivre.com.br "fone bluetooth"
site:shopee.com.br "fone bluetooth"
site:magazineluiza.com "fone bluetooth"
```

### Dados Coletados

**Padrões de título**:
- ML: [Marca] Fone [Modelo] Bluetooth [Característica] [Duração Bateria]
- Shopee: Fone Bluetooth [Benefício] [Característica] [Preço Atrativo]
- Magalu: [Marca] Fone [Modelo] Bluetooth com [Benefício]

**Atributos destacados**:
- Duração bateria (40h, 50h, 60h)
- Tipo conectividade (Bluetooth 5.0, 5.3)
- Cancelamento ruído (ativo, passivo)
- Dobrável/compacto
- Certificação Anatel

**Claims recorrentes**:
- Original/Lacrado (65% dos anúncios)
- Garantia (90% especifica prazo)
- Frete grátis (50% no ML, 80% na Shopee)
- Bateria longa duração (70%)

**Faixa de preços**:
- ML: 60-600 BRL, modal 120-180 BRL
- Shopee: 40-400 BRL, modal 80-120 BRL
- Magalu: 100-800 BRL, modal 150-250 BRL

**Provas sociais**:
- Avaliações: 50-5000 por produto
- Rating: 4.2-4.8 predominante
- Perguntas: 10-200 por anúncio popular

**Padrão visual**:
- 70% fundo branco + detalhe produto
- 40% incluem lifestyle
- 20% incluem vídeo
- 6-10 imagens típico

**Políticas**:
- Envio: 5-15 dias (econômico), 1-3 dias (expresso)
- Devolução: 7-30 dias, maioria 7 dias
- Parcelamento: 6x-12x sem juros típico

### Output [CONSULTAS WEB]
```
termo: fone bluetooth
fonte: Mercado Livre
data: 2025-11-03
insight: Duração bateria é atributo #1 em títulos; rating >4.5 essencial para primeiras posições

termo: fone bluetooth
fonte: Shopee
data: 2025-11-03
insight: Preço é driver primário; ofertas relâmpago dominam destaques; imagens lifestyle convertem mais

termo: fone bluetooth
fonte: Magazine Luiza
data: 2025-11-03
insight: Marcas consolidadas dominam; parcelamento destacado; certificação Anatel obrigatória em descrição
```

## Sinais de Oportunidade

Identificar durante coleta:
- **Gap de atributo**: atributo relevante pouco explorado em títulos
- **Gap de prova**: tipo de prova social ausente (ex: vídeos de review)
- **Gap de preço**: faixa de preço sub-representada
- **Gap de claim**: benefício verdadeiro não explorado
- **Gap de visual**: padrão de imagem diferenciador ausente

Registrar em [ESTRATÉGIAS E GAPS].

## Compliance e Alertas

Durante coleta, observar:
- Claims suspeitos (médicos, absolutos sem prova)
- Uso de termos bloqueados
- Produtos importados sem certificação aparente
- Preços muito abaixo da média (risco de falsificação)

Registrar em [RISCOS OU ALERTAS DE COMPLIANCE].

---

**Execução**: Após validação de brief e antes de web search outbound
**Duração típica**: 10-20 consultas por head term (3-5 marketplaces × 2-4 variações)
**Output principal**: [SEO INBOUND], [BENCHMARK DE CONCORRENTES], [CONSULTAS WEB]



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
*Enriquecido em: 2025-11-03T16:21:53.285768*
*Fonte: PaddleOCR Organized Knowledge Base*
