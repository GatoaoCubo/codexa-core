# MÓDULO: ANÁLISE DE IMAGENS

## 📋 MODULE_METADATA (TAC-7 Header)

```yaml
id: image_analysis_v1
version: 1.0.0
purpose: "Analyze product images for visual trends, context, quality assessment"
category: visual_intelligence
dependencies:
  - config/accessible_urls.md (relevant sections)
  - web_search capability (required for most modules)
execution_time: 3-5 min
isolation: module
portability: llm_agnostic
```

## 📥 INPUT_CONTRACT

**Required Inputs**:
- `$validated_brief.image_urls` - Input parameter

**Optional Inputs**: (see original content below)

## 📤 OUTPUT_CONTRACT

**Primary Outputs**: `[IMAGENS ANALISADAS]`

**Export Variables**:
```yaml
visual_insights: "Visual trends and quality assessment"
```

## 🎯 TASK

**Role**: Visual Analysis Specialist
**Objective**: Analyze product images for visual trends, context, quality assessment
**Standards**: (see original content below)
**Constraints**: Max execution time: 3-5 min, All queries logged

## ✅ VALIDATION (Quality Gates)

(See original content for specific validation criteria)

## 🔗 CONTEXT (Usage & Integration)

**Upstream Dependencies**: Previous steps in execution plan
**Downstream Consumers**: Subsequent steps + output blocks
**Data Flow**: (see original content)

---



## Objetivo
Analisar imagens de produtos fornecidas pelo usuário ou observadas em concorrentes para identificar sinais de prova, riscos de compliance e oportunidades de diferenciação visual.

## Quando Usar
- Usuário fornece `image_urls` no brief
- Imagens de produto estão disponíveis para análise
- Análise comparativa de padrões visuais de concorrentes

## Tipos de Análise

### 1. Análise Descritiva (Objetiva)

Descrever elementos visuais sem julgamento:
- **Composição**: fundo (branco, colorido, lifestyle), enquadramento, ângulo
- **Produto**: posição, tamanho relativo, nitidez
- **Elementos adicionais**: texto, selos, certificações, pessoas, ambientes
- **Cores dominantes**: paleta, contraste
- **Resolução aparente**: alta, média, baixa
- **Formato**: quadrado, retangular, panorâmico

Exemplo:
```
imagem_1:
- fundo branco sólido
- produto centralizado ocupando 70% do frame
- ângulo frontal levemente inclinado
- sem texto ou elementos gráficos
- alta nitidez
- formato quadrado (1:1)
```

### 2. Análise Comparativa (Múltiplas Imagens)

Comparar 2+ imagens para identificar:
- Consistência visual (mesma linha, diferentes ângulos)
- Diferenças de qualidade (resolução, iluminação)
- Complementaridade (produto, detalhe, contexto de uso)
- Redundância (imagens muito similares)

Exemplo:
```
comparação imagem_1 vs imagem_2:
- imagem_1: fundo branco, produto isolado, foco em design geral
- imagem_2: ambiente lifestyle (escritório), produto em uso, contexto aplicado
- complementaridade: alta (cobrem necessidades visuais diferentes)
- recomendação: usar ambas em sequência (1 para produto, 2 para contexto)
```

### 3. Análise de Prova Social e Credibilidade

Identificar elementos que aumentam confiança:
- **Selos visíveis**: Anatel, Inmetro, ISO, CE, FCC
- **Certificações**: orgânico, sustentável, premiações
- **Garantias**: texto visível de garantia
- **Embalagem**: produto lacrado, embalagem original, nota fiscal
- **Detalhes técnicos**: especificações visíveis, medidas, componentes
- **Prova de uso**: produto em contexto real, resultados, antes/depois

Exemplo:
```
imagem_3 - sinais de prova:
- selo Anatel visível no canto inferior direito do produto
- embalagem lacrada aparente
- texto "Original" na embalagem
- código de barras visível (autenticidade)
- nota fiscal parcialmente visível no fundo
prova_score: alto
```

### 4. Análise de Risco e Compliance

Identificar elementos problemáticos:
- **Claims visuais não verificáveis**: "melhor", "#1", "único"
- **Comparações denigratórias**: produto vs concorrente de forma negativa
- **Imagens enganosas**: produto diferente, tamanho distorcido
- **Uso indevido de marca**: logos sem autorização
- **Conteúdo sensível**: pessoas sem autorização, menores, imagens inadequadas
- **Regulação específica**: alimentos, cosméticos, eletrônicos (requisitos visuais)

Exemplo:
```
imagem_4 - alertas de risco:
- texto "Melhor do Brasil" sem fonte ou prova
- comparação lado a lado com produto concorrente (marca visível)
- tamanho do produto aparenta distorção (maior que real)
risco_score: alto
ação: remover claim absoluto, evitar comparação direta, ajustar escala
```

### 5. Análise de Padrão Visual (Benchmark)

Ao observar imagens de concorrentes, mapear padrões:
- **Dominante no segmento**: fundo branco 80%, lifestyle 40%
- **Ângulos típicos**: frontal 60%, 3/4 30%, detalhe 40%
- **Número de imagens**: 6-10 típico em marketplaces
- **Sequência comum**: produto > detalhe > lifestyle > embalagem > certificação
- **Uso de infográfico**: 30% incluem comparativo visual ou tabela
- **Presença de vídeo**: 25% dos anúncios top

Exemplo:
```
padrão visual - fone bluetooth (15 concorrentes):
- 90% usam fundo branco na imagem principal
- 60% incluem imagem lifestyle (pessoa usando)
- 50% mostram close de almofadas/conforto
- 40% exibem embalagem e acessórios
- 30% incluem infográfico de bateria/conectividade
- 20% têm vídeo de demonstração
insight: fundo branco é mandatório; lifestyle e close de conforto diferenciam
```

## Processo de Análise

### Para cada imagem fornecida:

1. **Descrever objetivamente** (bloco descritivo)
2. **Identificar provas** (selos, certificações, contexto)
3. **Identificar riscos** (claims, comparações, distorções)
4. **Avaliar adequação** ao marketplace de destino
5. **Sugerir uso** (principal, secundária, remover, ajustar)

### Para conjunto de imagens:

1. **Analisar complementaridade** (cobrem diferentes necessidades?)
2. **Verificar redundância** (imagens muito similares?)
3. **Ordenar sequência ideal** (produto > detalhe > contexto)
4. **Identificar gaps** (faltam ângulos, provas, contexto?)

### Para benchmark visual (concorrentes):

1. **Mapear padrões** (tipos, ângulos, elementos)
2. **Quantificar recorrência** (% de presença)
3. **Identificar table stakes** (>70% usam = obrigatório)
4. **Identificar diferenciais** (<30% usam = oportunidade)

## Output: Bloco [IMAGENS ANALISADAS]

Formato:
```
[IMAGENS ANALISADAS]

imagem_1: [URL ou ID]
descrição: [composição, fundo, produto, elementos]
tipo: [produto isolado | lifestyle | detalhe | embalagem | infográfico]
provas visíveis: [selos, certificações, garantias] ou nenhuma
riscos visíveis: [claims não verificáveis, comparações] ou nenhum
adequação: [alta | média | baixa] para marketplace [nome]
uso sugerido: [imagem principal | secundária | remover | ajustar]
ajustes necessários: [lista de ações] ou nenhum

imagem_2: [URL ou ID]
[... mesmo formato]

comparação entre imagens:
complementaridade: [alta | média | baixa]
redundância: [sim | não] - se sim, remover [qual]
sequência ideal: [ordem sugerida]
gaps identificados: [ângulos ou elementos faltantes]

benchmark visual (se aplicável):
padrão observado em concorrentes: [descrição]
elementos obrigatórios: [lista]
oportunidades de diferenciação: [lista]
```

## Exemplo Completo

**Produto**: Fone Bluetooth JBL Tune 510BT
**Imagens fornecidas**: 3

### Análise

```
[IMAGENS ANALISADAS]

imagem_1: product_front.jpg
descrição: fundo branco sólido, fone centralizado em ângulo frontal, cor preta, logo JBL visível, sem texto adicional
tipo: produto isolado
provas visíveis: logo JBL (autenticidade), produto nítido (qualidade)
riscos visíveis: nenhum
adequação: alta para Mercado Livre, Amazon, Magazine Luiza
uso sugerido: imagem principal (primeira imagem do anúncio)
ajustes necessários: nenhum

imagem_2: product_detail_comfort.jpg
descrição: close das almofadas auriculares, textura visível, fundo desfocado neutro
tipo: detalhe técnico
provas visíveis: material aparente (espuma macia), qualidade de construção
riscos visíveis: nenhum
adequação: alta para destacar conforto
uso sugerido: terceira ou quarta imagem (após produto e lifestyle)
ajustes necessários: adicionar texto discreto "Almofadas Macias" se permitido

imagem_3: lifestyle_office.jpg
descrição: pessoa usando fone em ambiente de escritório home office, laptop visível, iluminação natural, pessoa sorrindo
tipo: lifestyle
provas visíveis: contexto de uso real (home office), conforto aparente
riscos visíveis: rosto da pessoa visível (verificar autorização de uso de imagem)
adequação: média-alta para marketplace (alta para redes sociais)
uso sugerido: segunda imagem (logo após produto isolado)
ajustes necessários: verificar autorização de uso de imagem; considerar versão com rosto desfocado para marketplace

comparação entre imagens:
complementaridade: alta (produto + detalhe + contexto cobrem necessidades visuais completas)
redundância: não
sequência ideal: imagem_1 (produto) > imagem_3 (lifestyle) > imagem_2 (detalhe conforto)
gaps identificados:
- faltam embalagem/acessórios (cabo, case se aplicável)
- faltam certificações visíveis (Anatel)
- faltam infográfico de especificações (bateria, Bluetooth)

imagens adicionais sugeridas:
- imagem_4: embalagem lacrada com selo Anatel visível
- imagem_5: infográfico com bateria 40h, Bluetooth 5.0, alcance 10m
- imagem_6: produto dobrado para demonstrar portabilidade

benchmark visual (fone bluetooth):
padrão observado: 90% fundo branco principal, 60% lifestyle, 50% close conforto, 40% embalagem
elementos obrigatórios: fundo branco produto isolado, certificação Anatel (por regulação)
oportunidades de diferenciação: vídeo de pareamento (20% têm), comparativo de bateria com concorrentes (10% têm)
```

## Heurísticas de Qualidade Visual

### Imagem Principal (obrigatória)
- Fundo branco sólido (RGB 255,255,255)
- Produto centralizado ocupando 70-85% do frame
- Alta resolução (mínimo 1000x1000px)
- Ângulo que mostra produto claramente
- Sem texto, selos ou elementos gráficos adicionais

### Imagens Secundárias (recomendadas)
- **Lifestyle**: produto em uso, contexto real, pessoas se aplicável
- **Detalhe**: close de features importantes (material, conexões, botões)
- **Embalagem**: produto lacrado, selos, certificações
- **Acessórios**: tudo que acompanha o produto
- **Infográfico**: especificações técnicas visuais

### Imagens a Evitar
- Baixa resolução ou pixeladas
- Fundo poluído ou confuso (exceto lifestyle intencional)
- Múltiplos produtos na mesma imagem (confunde)
- Texto excessivo (melhor na descrição)
- Claims visuais não verificáveis
- Comparações denigratórias

## Integração com Outros Módulos

### Com Benchmark de Concorrentes
Padrões visuais observados em concorrentes → benchmark visual consolidado

### Com Compliance
Riscos visuais identificados → [RISCOS OU ALERTAS DE COMPLIANCE]

### Com Diferenciais
Gaps visuais de concorrentes → oportunidades de imagem diferenciadora

### Com SEO Inbound
Padrões visuais de top ranqueados → recomendações de sequência e tipo

---

**Execução**: Quando image_urls fornecido ou ao final da análise para consolidar padrões visuais
**Input**: URLs de imagens ou observações de imagens de concorrentes
**Output**: Bloco [IMAGENS ANALISADAS] + insights visuais em [BENCHMARK], [ESTRATÉGIAS E GAPS]



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
*Enriquecido em: 2025-11-03T16:21:53.180376*
*Fonte: PaddleOCR Organized Knowledge Base*
