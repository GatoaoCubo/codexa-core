# MÓDULO: WEB SEARCH OUTBOUND (SERP, MÍDIA, SOCIAL)

## 📋 MODULE_METADATA (TAC-7 Header)

```yaml
id: web_search_outbound_v1
version: 1.0.0
purpose: "Execute SERP + social searches (Google, YouTube, TikTok, Reclame Aqui) for organic insights"
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

**Optional Inputs**: (see original content below)

## 📤 OUTPUT_CONTRACT

**Primary Outputs**: `[SEO OUTBOUND]`, `[DORES DO PÚBLICO]`, `[GANHOS DESEJADOS]`, `[CONSULTAS WEB]`

**Export Variables**:
```yaml
organic_keywords: "Content keywords from SERP"
pain_points_initial: "Initial pain points from reviews/social"
```

## 🎯 TASK

**Role**: Data Collection Specialist
**Objective**: Execute SERP + social searches (Google, YouTube, TikTok, Reclame Aqui) for organic insights
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
Pesquisar SERP Google, mídia especializada e canais sociais brasileiros para coletar perguntas frequentes, reviews UGC, padrões de conteúdo e sinais de demanda orgânica.

## Escopo OBRIGATÓRIO
Pesquisar **mínimo 2 canais sociais BR + SERP por head term**.

### Canais Prioritários e URLs Base

**IMPORTANTE**: Consulte `config/accessible_urls.md` para URLs completas e padrões testados.

| Canal | Domain | Tipo | Use para |
|-------|--------|------|----------|
| YouTube | youtube.com | UGC Video | Reviews, unboxings, tutoriais |
| TikTok | tiktok.com | UGC Short | Tendências, autenticidade |
| Instagram | instagram.com | UGC Visual | Lifestyle, hashtags |
| Google SERP | google.com.br | Busca | Perguntas, comparativos |
| Reclame Aqui | reclameaqui.com.br | Reclamações | Riscos, dores reais |

**Método de Coleta**:
- Use URLs testadas de `accessible_urls.md` (Seção: CANAIS SOCIAIS)
- Captura visual: screenshot + GPT-5 Vision
- Foco em conteúdo BR recente (<3 meses)

### URLs Diretas para Coleta Visual

**YouTube**:
```
https://www.youtube.com/results?search_query={{HEAD_TERM}}+review+brasil
https://www.youtube.com/results?search_query={{HEAD_TERM}}+unboxing+brasil
https://www.youtube.com/results?search_query={{HEAD_TERM}}+vs+{{ALTERNATIVA}}
https://www.youtube.com/results?search_query={{HEAD_TERM}}+vale+a+pena
```

**TikTok**:
```
https://www.tiktok.com/search/video?q={{HEAD_TERM}}
https://www.tiktok.com/search?q={{HEAD_TERM}}+brasil
https://www.tiktok.com/discover/{{HEAD_TERM}}-review
```

**Instagram**:
```
https://www.instagram.com/explore/tags/{{HEAD_TERM}}
https://www.instagram.com/explore/tags/{{HEAD_TERM}}brasil
```

**Google Shopping**:
```
https://www.google.com.br/search?q={{HEAD_TERM}}&tbm=shop
https://www.google.com.br/search?q={{HEAD_TERM}}+review
https://www.google.com.br/search?q={{HEAD_TERM}}+melhor+preço
```

**Reclame Aqui**:
```
https://www.reclameaqui.com.br/busca?q={{HEAD_TERM}}
https://www.reclameaqui.com.br/busca?q={{MARCA}}
```

## Templates de Consulta

### SERP Geral
```
"{head_term}" guia de compra
"{head_term}" review
"{head_term}" melhores
"{head_term}" vale a pena
"{head_term}" como escolher
"{head_term}" comparação
"{head_term}" onde comprar
"{head_term}" perguntas frequentes
```

### YouTube (Review e Tutorial)
```
site:youtube.com "{head_term}" review Brasil
site:youtube.com "{head_term}" unboxing
site:youtube.com "{head_term}" vale a pena
site:youtube.com "{head_term}" teste
site:youtube.com "{head_term}" vs {concorrente}
```

### TikTok (UGC e Viral)
```
site:tiktok.com "{head_term}" Brasil
site:tiktok.com "{head_term}" review
site:tiktok.com "{head_term}" recebi
```

### Instagram
```
site:instagram.com "{head_term}" Brasil
site:instagram.com #{head_term_hashtag}
site:instagram.com "{head_term}" review
```

### Reclame Aqui (Risco)
```
site:reclameaqui.com.br "{marca}" "{produto}"
site:reclameaqui.com.br "{head_term}"
```

## Dados a Coletar

### 1. Perguntas Frequentes (SERP)
Extrair de:
- Featured snippets "People Also Ask"
- Títulos de artigos (ex: "Como escolher...")
- Fóruns e Q&A (Reddit, Quora, comunidades BR)

Formato:
```
pergunta: [texto exato da pergunta]
fonte: [SERP, blog, fórum]
recorrência: [quantas fontes repetem]
resposta_síntese: [resumo breve]
```

### 2. Padrões de Título SERP
Analisar títulos de páginas ranqueadas:
- Estrutura típica (head term + modificador)
- Modificadores eficazes (melhor, top, guia, review)
- Tamanho (caracteres)
- Presença de números, anos, listas

Exemplo:
```
padrão_titulo: "Melhores [head_term] de [ano]: Top [N] com Review"
recorrência: alta em 7 de 10 resultados top
insight: ano atual e número de itens aumentam CTR
```

### 3. Ângulos de Review (YouTube, TikTok)
Tipos de conteúdo encontrados:
- Unboxing e primeira impressão
- Review após uso (1 semana, 1 mês, 6 meses)
- Comparativo (produto A vs B)
- Tutorial ou how-to
- Teste de resistência/durabilidade
- Vale a pena ou não

Registrar:
```
tipo: [review após 30 dias]
canal: YouTube
views_típicas: [range observado]
tom: [positivo, crítico, neutro]
foco: [durabilidade, custo-benefício, performance]
```

### 4. Claims e Benefícios Destacados (UGC)
O que criadores de conteúdo enfatizam:
- Benefícios reais experimentados
- Problemas resolvidos
- Comparações com concorrentes
- Contextos de uso

### 5. Objeções e Críticas Recorrentes
Pontos negativos mencionados repetidamente:
- Limitações do produto
- Expectativa vs realidade
- Problemas de durabilidade
- Atendimento ou logística

Formato:
```
objeção: [descrição breve]
frequência: [quantas menções]
contexto: [quando/por quem]
resposta_possível: [como endereçar]
```

### 6. Padrões Visuais e de Conteúdo
Em vídeos e posts:
- Tipo de demonstração (mãos à obra, lifestyle, close técnico)
- Duração típica (vídeos)
- Presença de gráficos ou comparativos
- Provas sociais (antes/depois, depoimentos)

### 7. Palavras-Chave Negligenciadas
Termos relevantes que aparecem em SERP/social mas não em marketplaces:
- Sinônimos regionais
- Gírias ou termos coloquiais
- Nomes alternativos do produto
- Verbos de ação específicos

### 8. Reclamações e Riscos (Reclame Aqui)
Para marcas/produtos identificados:
- Número de reclamações (volume)
- Tipo predominante (entrega, produto defeituoso, atendimento)
- Taxa de resolução
- Reputação geral

Formato:
```
marca: [nome]
volume_reclamações: [range ou número]
tipo_principal: [categoria]
taxa_resposta: [% ou qualitativo]
alerta: [risco para associação ou menção]
```

## Processo de Coleta

### Para cada head term:

1. **SERP geral**: executar 3-5 queries de intenção diferente
   - Informacional: "o que é", "como funciona"
   - Comparativa: "melhores", "vs"
   - Transacional: "onde comprar", "preço"

2. **YouTube**: buscar reviews BR recentes (último ano)
   - Analisar 5-10 vídeos mais relevantes
   - Ler comentários para capturar dúvidas e feedback

3. **TikTok/Instagram**: buscar conteúdo viral e UGC
   - Priorizar posts recentes (últimos 3 meses)
   - Observar engajamento (likes, compartilhamentos, comentários)

4. **Reclame Aqui**: buscar marcas principais identificadas
   - Verificar reputação
   - Ler reclamações recentes (último trimestre)

5. **Registrar cada consulta** em [CONSULTAS WEB]

### Registro de Consulta
```
termo: {head_term ou query específica}
fonte: {SERP Google, YouTube, TikTok, Instagram, Reclame Aqui}
data: {YYYY-MM-DD}
insight: {padrão ou descoberta chave}
```

## Output: Blocos Afetados

### [SEO OUTBOUND]
```
head ou padrão de título eficaz: [estrutura observada em SERP]
pergunta frequente do público: [pergunta + fonte]
termo semântico útil: [termo não usado em marketplace mas relevante]
pauta sugerida: [ideia de conteúdo orgânico]
```

### [DORES DO PÚBLICO]
```
dor identificada: [descrição]
fonte: [YouTube, TikTok, comentários]
contexto: [quando ocorre]
```

### [GANHOS DESEJADOS]
```
ganho esperado: [benefício buscado]
fonte: [reviews, perguntas frequentes]
evidência: [menções, recorrência]
```

### [OBJEÇÕES E RESPOSTAS]
```
objeção: [pergunta ou crítica]
resposta: [como endereçar com dados ou prova]
fonte: [canal onde foi identificada]
```

### [RISCOS OU ALERTAS DE COMPLIANCE]
```
alerta: [risco identificado]
fonte: Reclame Aqui ou reviews negativos
contexto: [marcas, produtos afetados]
ação: [evitar menção, disclaimers]
```

### [ESTRATÉGIAS E GAPS]
```
gap de palavra-chave: [termo com demanda mas pouco explorado]
oportunidade visual: [tipo de conteúdo ausente]
oportunidade de prova social: [tipo de UGC inexplorado]
```

## Exemplo Completo

**Head term**: fone bluetooth

### Consultas Executadas

**SERP**:
```
"fone bluetooth" melhores
"fone bluetooth" guia de compra
"fone bluetooth" vale a pena
"como escolher fone bluetooth"
```

**YouTube**:
```
site:youtube.com "fone bluetooth" review Brasil
site:youtube.com "fone bluetooth" vale a pena
site:youtube.com "fone bluetooth vs fone com fio"
```

**TikTok**:
```
site:tiktok.com "fone bluetooth" Brasil
```

**Reclame Aqui**:
```
site:reclameaqui.com.br "JBL fone"
site:reclameaqui.com.br "Sony fone"
```

### Dados Coletados

**Perguntas frequentes** (SERP):
- "Qual o melhor fone bluetooth custo-benefício?"
- "Fone bluetooth estraga o ouvido?"
- "Como saber se fone bluetooth é original?"
- "Quanto tempo dura bateria de fone bluetooth?"
- "Vale a pena fone bluetooth barato?"

**Padrões de título** (SERP):
- "Melhores Fones Bluetooth 2025: Top 10 com Review Completo" (recorrente)
- "Fone Bluetooth Bom e Barato: Guia de Compra [Ano]"
- "Review: [Marca Modelo] - Vale a Pena?" (estrutura comum)

**Ângulos de review** (YouTube):
- Unboxing + teste inicial (30% dos vídeos)
- Review após 30 dias de uso (25%)
- Comparativo marca vs marca (20%)
- "Comprei o mais barato vs mais caro" (15%)
- Teste de durabilidade (10%)

**Claims destacados** (UGC):
- Duração real de bateria (vs especificação)
- Conforto para uso prolongado
- Qualidade de som (graves, agudos)
- Facilidade de pareamento Bluetooth
- Resistência a queda e água

**Objeções recorrentes**:
- Objeção: "Bateria dura menos que o anunciado"
  Frequência: alta (40% dos reviews)
  Resposta: "Especificar condições de teste (volume, uso contínuo vs pausado)"

- Objeção: "Conecta em um dispositivo só por vez"
  Frequência: moderada (20%)
  Resposta: "Destacar se suporta multipoint connection"

- Objeção: "Demora para chegar e vem sem garantia"
  Frequência: moderada (15%)
  Resposta: "Usar vendedor oficial, destacar prazo e garantia"

**Palavras-chave negligenciadas**:
- "fone sem fio" (sinônimo mais coloquial que bluetooth)
- "headphone bluetooth" (termo híbrido)
- "fone para treino" (contexto de uso)
- "fone que não cai da orelha" (benefício específico)

**Reclamações** (Reclame Aqui):
- Marca JBL: 450 reclamações, 70% sobre entrega/logística, reputação boa
- Marca genérica XYZ: 180 reclamações, 60% sobre produto defeituoso, reputação ruim
- Alerta: evitar associação com marcas de reputação ruim

### Output [CONSULTAS WEB]
```
termo: fone bluetooth melhores
fonte: Google SERP
data: 2025-11-03
insight: Featured snippets priorizam listas numeradas com critérios de escolha; ano no título aumenta relevância

termo: fone bluetooth review Brasil
fonte: YouTube
data: 2025-11-03
insight: Reviews longos (>10min) com teste real geram mais engajamento; comparativos diretos são mais buscados

termo: fone bluetooth Brasil
fonte: TikTok
data: 2025-11-03
insight: Vídeos curtos de unboxing com reação autêntica viralizam; foco em "vale a pena" e preço

termo: JBL fone
fonte: Reclame Aqui
data: 2025-11-03
insight: Reclamações concentradas em logística não no produto; reputação da marca é positiva
```

## Sinais de Oportunidade

### Gap de Conteúdo
Perguntas frequentes sem resposta satisfatória:
- Criar guia de compra endereçando objeções
- Produzir review comparativo profissional
- Tutorial de manutenção ou troubleshooting

### Gap de Palavra-Chave
Termos com demanda não explorados em marketplace:
- Incorporar sinônimos coloquiais em títulos
- Usar termos de contexto de uso (treino, estudo, trabalho)

### Gap de Prova Social
Tipos de conteúdo ausentes:
- Vídeo de teste de longo prazo (6 meses)
- Review técnico com medições objetivas
- Comparativo head-to-head com marcas premium

### Oportunidade de Posicionamento
Ângulos pouco explorados:
- Foco em durabilidade (não só especificações)
- Custo total de propriedade (custo inicial + vida útil)
- Casos de uso específicos (trabalho remoto, academia)

## Compliance e Alertas

Identificar durante coleta:
- Claims médicos ou de saúde sem evidência ("melhora audição", "previne surdez")
- Comparações denigratórias a concorrentes
- Uso de imagens ou depoimentos sem autorização
- Associação a marcas com má reputação

Registrar em [RISCOS OU ALERTAS DE COMPLIANCE].

## Integração com SEO Inbound

Cruzar descobertas:
- Termos frequentes em SERP mas ausentes em marketplaces → oportunidade de longtail
- Objeções em reviews → destacar provas ou políticas que resolvem
- Claims UGC → validar se são verificáveis e permitidos
- Padrões visuais virais → adaptar para imagens de marketplace

---

**Execução**: Após web search inbound e antes de benchmark consolidado
**Duração típica**: 8-15 consultas por head term (SERP + 2-3 sociais + Reclame Aqui)
**Output principal**: [SEO OUTBOUND], [OBJEÇÕES E RESPOSTAS], [DORES/GANHOS], [CONSULTAS WEB]



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
*Enriquecido em: 2025-11-03T16:21:53.269237*
*Fonte: PaddleOCR Organized Knowledge Base*
