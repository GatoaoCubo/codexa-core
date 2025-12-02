# PESQUISA AGENT | Documento de Referencia para Video Tutorial

**Proposito**: Fonte de conhecimento para NotebookLM gerar video tutorial
**Agente**: pesquisa_agent v3.1.0
**Duracao do Video**: 3-5 minutos

---

## O QUE E O PESQUISA AGENT

O Pesquisa Agent e um especialista em inteligencia competitiva para e-commerce brasileiro. Ele analisa 9 marketplaces (Mercado Livre, Shopee, Magazine Luiza, Amazon BR, Americanas, Casas Bahia, Submarino, TikTok Shop, Shein) e entrega um relatorio estruturado com 22 blocos de informacao.

**Transformacao**: Brief do produto → Relatorio de pesquisa de 22 blocos
**Duracao da execucao**: 20-30 minutos
**Output**: research_notes.md

---

## COMO O USUARIO INICIA

O usuario digita uma frase simples:

```
"Quero pesquisar [URL do produto]"
```

ou

```
"Quero pesquisar garrafa de agua reutilizavel ecologica"
```

O agente NAO conversa. Ele EXECUTA o workflow completo automaticamente.

---

## O WORKFLOW COMPLETO (9 Passos)

### Passo 1: Validacao do Brief (2 min)
- Agente analisa o que foi pedido
- Identifica lacunas (preco? categoria? publico?)
- Gera suposicoes para dados faltantes
- Output: Bloco [LACUNAS DO BRIEF]

### Passo 2: Geracao de Queries (3 min)
- Extrai head terms (1-3 palavras, alta intencao)
- Deriva longtails (head + atributo/beneficio)
- Mapeia sinonimos e variacoes regionais
- Output: 10-15 head terms + 30-50 longtails

### Passo 3: Pesquisa INBOUND - Marketplaces (8 min)
- Busca em 9 marketplaces brasileiros
- Para cada termo: minimo 3 buscas
- Extrai: titulos, precos, avaliacoes, badges, reputacao
- Captura screenshots dos top listings
- Output: Padroes de SEO inbound

### Passo 4: Pesquisa OUTBOUND - SERP e Social (8 min)
- Google SERP (reviews, comparacoes, blogs)
- YouTube (reviews, unboxing, tutoriais)
- TikTok (demos, conteudo de usuario)
- Instagram (tendencias visuais, influencers)
- Reclame Aqui (reclamacoes, analise de risco) - OBRIGATORIO
- Output: Dores, ganhos, objecoes do publico

### Passo 5: Analise de Concorrentes (6 min)
- Analise profunda dos top 3-5 concorrentes
- Benchmark agregado: preco medio, rating, volume de reviews
- Identificacao de gaps: features nao atendidas, mensagens fracas
- Output: Perfis de concorrentes + oportunidades

### Passo 6: Taxonomia SEO (4 min)
- Consolida dados de SEO
- Separa inbound (marketplace) vs outbound (conteudo organico)
- Identifica posicionamento de categoria
- Output: Keywords clusterizadas

### Passo 7: Compliance e Riscos (3 min)
- Verifica regras ANVISA (saude, cosmeticos, suplementos)
- Verifica regras INMETRO (brinquedos, eletronicos, texteis)
- Verifica regras CONAR (publicidade, claims)
- Output: Alertas e restricoes

### Passo 8: Sintese e Insights (3 min)
- Consolida todos os achados
- Prioriza oportunidades (alto impacto, baixa complexidade)
- Cria decisoes iniciais de copy
- Output: Oportunidades acionaveis + argumentos de venda

### Passo 9: Montagem do Output (2 min)
- Preenche template de 22 blocos
- Gera arquivos: research_notes.md + metadata.json + queries.json
- Valida qualidade (minimo 75% completude)
- Output: Relatorio final pronto para uso

---

## OS 22 BLOCOS DO RELATORIO

1. Resumo Executivo
2. Lacunas do Brief
3. Head Terms Prioritarios
4. Longtails
5. Sinonimos e Variacoes
6. SEO Inbound
7. SEO Outbound
8. Padroes de Linguagem Eficaz
9. Analise de Concorrentes
10. Benchmark Agregado
11. Gaps Competitivos
12. Diferenciais Competitivos
13. Dores do Publico
14. Ganhos Desejados
15. Objecoes e Respostas
16. Taxonomia de Categorias
17. Riscos e Alertas
18. Regras Criticas de Marketplace
19. Oportunidades Acionaveis
20. Argumentos de Venda
21. Gatilhos Mentais
22. Consultas Web (rastreabilidade)

---

## EXEMPLO DE INPUT E OUTPUT

**Input do usuario**:
```
Quero pesquisar garrafa de agua reutilizavel ecologica
Categoria: Casa e Jardim > Cozinha
Publico: Profissionais home office, 25-45 anos
Faixa de preco: R$ 89 - R$ 129
Marketplace: Mercado Livre (principal)
```

**Output resumido (Bloco 1 - Resumo Executivo)**:
```
Mercado de garrafas reutilizaveis em expansao no Brasil.
Gap identificado: poucos concorrentes focam em home office.
Oportunidade: posicionamento "produtividade + sustentabilidade".
Preco medio concorrencia: R$ 79. Margem para premium existe.
Recomendacao: enfatizar design minimalista + BPA-free + 24h termico.
```

---

## POR QUE USAR O PESQUISA AGENT

1. **Economia de tempo**: 20-30 min vs 4-8 horas manual
2. **Rastreabilidade total**: Cada query logada com URL e fonte
3. **Compliance**: Verifica ANVISA, INMETRO, CONAR automaticamente
4. **Dados quantitativos**: Precos, ratings, volumes em BRL e %
5. **Pronto para uso**: Output alimenta diretamente o Anuncio Agent

---

## CONEXAO COM OUTROS AGENTES

```
PESQUISA AGENT
     |
     | research_notes.md
     v
ANUNCIO AGENT → Gera copy de anuncio
     |
     | anuncio.md
     v
PHOTO AGENT → Gera prompts de foto
```

O Pesquisa Agent e o PRIMEIRO passo do pipeline. Ele coleta a inteligencia que alimenta os outros agentes.

---

## METRICAS DE QUALIDADE

| Metrica | Minimo | Ideal |
|---------|--------|-------|
| Blocos preenchidos | 17/22 (75%) | 22/22 (100%) |
| Concorrentes analisados | 3 | 5+ |
| Queries logadas | 15 | 30+ |
| Placeholders [SUGESTAO] | ≤10% | 0% |
| Score de confianca | 0.75 | 0.90+ |

---

## MENSAGEM CHAVE PARA O VIDEO

"O Pesquisa Agent transforma horas de trabalho manual em minutos. Voce digita uma frase, ele entrega um relatorio completo de 22 blocos com inteligencia competitiva, SEO, compliance e oportunidades acionaveis. E tudo rastreavel - cada dado tem fonte e URL."

---

**Arquivo fonte**: agentes/pesquisa_agent/PRIME.md
**Versao**: 3.1.0
