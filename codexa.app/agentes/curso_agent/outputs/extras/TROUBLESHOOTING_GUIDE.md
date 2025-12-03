# Guia de Troubleshooting CODEXA

**O que fazer quando as coisas não saem como esperado**

---

## ÍNDICE

1. [Problemas Gerais](#1-problemas-gerais)
2. [Anuncio Agent](#2-anuncio-agent)
3. [Pesquisa Agent](#3-pesquisa-agent)
4. [Marca Agent](#4-marca-agent)
5. [Photo Agent](#5-photo-agent)
6. [CODEXA Agent](#6-codexa_agent)
7. [Quando Pedir Ajuda ao Mentor](#7-quando-pedir-ajuda-ao-mentor)

---

## 1. PROBLEMAS GERAIS

### 1.1 Output genérico/superficial

**SINTOMA:** O agente responde mas o conteúdo parece ChatGPT genérico

**CAUSA:** Contexto insuficiente ou vago demais

**SOLUÇÃO:**
```
❌ RUIM: "Cria um anúncio de tênis"

✅ BOM: "Cria um anúncio para Mercado Livre:
- Produto: Tênis Nike Air Max 90
- Tamanho: 38-44
- Cores: Preto, Branco, Azul
- Preço: R$ 599,90
- Diferencial: Original com NF, entrega em 24h
- Público: Homens 25-35 anos que praticam esportes"
```

**REGRA:** Quanto mais contexto, melhor o output.

---

### 1.2 Agente não entende o pedido

**SINTOMA:** Resposta completamente fora do esperado

**CAUSA:** Ambiguidade no prompt ou contexto errado carregado

**SOLUÇÃO:**
```
1. Verifique se carregou o agente certo:
   - Anúncios? → /prime-anuncio
   - Pesquisa? → /prime-pesquisa
   - Marca? → /prime-marca

2. Seja explícito sobre o que quer:
   "Quero EXATAMENTE:
   1. Título de 60 caracteres
   2. 5 bullet points
   3. Descrição de 500 palavras
   NÃO quero: explicações, teoria, opções"
```

---

### 1.3 Output muito longo/curto

**SINTOMA:** Recebe 3 páginas quando queria 3 linhas (ou vice-versa)

**CAUSA:** Não especificou tamanho/formato

**SOLUÇÃO:**
```
ESPECIFIQUE SEMPRE:
- "Título CURTO (máx 60 caracteres)"
- "Descrição MÉDIA (300-500 palavras)"
- "Análise COMPLETA (mínimo 1000 palavras)"
- "Resposta DIRETA, sem explicações"
- "Lista com EXATAMENTE 5 itens"
```

---

### 1.4 Resposta em inglês

**SINTOMA:** Output vem em inglês em vez de português

**CAUSA:** Alguns prompts técnicos trigam resposta em inglês

**SOLUÇÃO:**
```
Adicione no início ou final do prompt:
"Responda SEMPRE em português brasileiro."

Ou seja específico:
"[IDIOMA: PT-BR, tom informal, expressões brasileiras]"
```

---

## 2. ANUNCIO AGENT

### 2.1 Título passa do limite de caracteres

**SINTOMA:** Título com 75 caracteres quando ML aceita 60

**SOLUÇÃO:**
```
"O título ficou com X caracteres.
Preciso MÁXIMO 60 caracteres para Mercado Livre.
Encurta mantendo:
1. Keyword principal
2. Tamanho/cor se relevante
3. Benefício principal"
```

---

### 2.2 Compliance não mencionado

**SINTOMA:** Anúncio não fala sobre ANVISA/INMETRO

**SOLUÇÃO:**
```
"Esse produto precisa de compliance?
Verifica:
- É alimento/suplemento? → ANVISA
- É eletrônico/brinquedo? → INMETRO
- É cosmético? → ANVISA
Me dá o checklist completo de obrigatoriedades."
```

---

### 2.3 Copy genérico/sem persuasão

**SINTOMA:** Texto descritivo mas não vende

**SOLUÇÃO:**
```
"A copy ficou informativa mas não persuasiva.
Reescreve usando framework PAS:
- PROBLEMA: Que dor o cliente tem?
- AGITAÇÃO: Por que isso é urgente resolver?
- SOLUÇÃO: Como meu produto resolve?

Adiciona pelo menos 2 gatilhos mentais:
escassez, prova social, autoridade, garantia"
```

---

### 2.4 Keywords erradas/insuficientes

**SINTOMA:** SEO fraco, produto não aparece nas buscas

**SOLUÇÃO:**
```
"Quais são as TOP 10 keywords que clientes usam
para buscar esse tipo de produto no Mercado Livre?

Organiza em:
- 3 keywords principais (volume alto)
- 4 keywords secundárias (intenção de compra)
- 3 long-tail (conversão alta)

Depois ajusta o título e descrição para incluir todas."
```

---

## 3. PESQUISA AGENT

### 3.1 Dados parecem desatualizados

**SINTOMA:** Informações que não batem com a realidade

**SOLUÇÃO:**
```
"Esses dados parecem desatualizados.
Consegue fazer busca em tempo real nos marketplaces?

Se não conseguir acessar dados ao vivo, me indica:
1. Quais fontes você está usando
2. De quando são esses dados
3. Como eu posso validar manualmente"
```

---

### 3.2 Análise superficial

**SINTOMA:** Quick research quando você queria comprehensive

**SOLUÇÃO:**
```
"Preciso de análise COMPREHENSIVE, não quick.
Inclui obrigatoriamente:
- Mínimo 10 concorrentes analisados
- Faixa de preço com min/med/max
- Análise de reviews (o que elogiam/reclamam)
- Gaps de mercado (mín 5 oportunidades)
- Sazonalidade se aplicável"
```

---

### 3.3 Recomendação de preço sem justificativa

**SINTOMA:** "Sugiro R$ 99" sem explicar por quê

**SOLUÇÃO:**
```
"Preço sugerido de R$ X.
Justifica essa recomendação:
1. Como cheguei nesse número?
2. Quanto a concorrência cobra?
3. Qual margem terei com custo de R$ Y?
4. É premium, médio ou econômico?
5. Que argumentos uso pra justificar esse preço?"
```

---

## 4. MARCA AGENT

### 4.1 Arquétipo não parece certo

**SINTOMA:** Sugeriu arquétipo que não combina

**SOLUÇÃO:**
```
"Arquétipo sugerido não combina com meu negócio.
Minha marca é [descreva com 3 adjetivos].

Reavalia considerando:
- Quem é meu cliente ideal?
- Que emoção quero despertar?
- Quais marcas admiro e por quê?

Me dá 3 opções de arquétipo com prós/contras de cada."
```

---

### 4.2 Cores genéricas

**SINTOMA:** Azul/verde/branco que toda marca usa

**SOLUÇÃO:**
```
"Cores ficaram muito comuns.
Quero paleta mais distintiva.

Referências que gosto:
- [cite marcas ou estilos: ex. "minimalismo japonês", "Aesop"]

Cria paleta que seja:
1. Reconhecível (não genérica)
2. Funcional (contraste bom)
3. Alinhada com meu arquétipo [X]"
```

---

### 4.3 Tom de voz inconsistente

**SINTOMA:** Às vezes formal, às vezes casual

**SOLUÇÃO:**
```
"Tom de voz está inconsistente.
Define claramente:
- Escala 1-10 em cada dimensão
- 10 palavras que SEMPRE uso
- 10 palavras que NUNCA uso
- 3 exemplos de frase certa
- 3 exemplos de frase errada"
```

---

## 5. PHOTO AGENT

### 5.1 Imagens não parecem profissionais

**SINTOMA:** Resultado parece amador/stock photo

**SOLUÇÃO:**
```
"Imagem ficou genérica.
Adiciona esses elementos profissionais:
- Iluminação específica: [softbox, natural, dramática]
- Câmera específica: Canon R5, Sony A7III
- Lente específica: 85mm f/1.8
- Detalhes de textura visíveis
- Profundidade de campo (bokeh)
- Contexto único (não estúdio branco genérico)"
```

---

### 5.2 Cores não batem com a marca

**SINTOMA:** Cenário com cores que conflitam com brand

**SOLUÇÃO:**
```
"Cores do ambiente não combinam com minha marca.
Minha paleta é:
- Primária: #XXXXXX
- Secundária: #XXXXXX

Ajusta o prompt para:
- Cenário em tons que complementam
- Props nas cores da marca
- Iluminação que favorece minha paleta"
```

---

### 5.3 Resolução insuficiente

**SINTOMA:** Imagem pixelada ou pequena

**SOLUÇÃO:**
```
"Preciso de resolução específica para marketplace:
- Mercado Livre: mínimo 1200x1200px
- Amazon: mínimo 1000x1000px, ideal 2000x2000px
- Shopee: mínimo 800x800px

Regenera especificando:
--ar 1:1 --quality 2 --upscale
(ou parâmetros equivalentes da sua ferramenta)"
```

---

## 6. CODEXA AGENT

### 6.1 Agente criado não funciona

**SINTOMA:** Novo agente não responde corretamente

**SOLUÇÃO:**
```
"O agente [nome] não está funcionando.
Checa:
1. PRIME.md existe e está completo?
2. iso_vectorstore/ tem os arquivos necessários?
3. Comando /prime-[nome] está configurado?
4. Context está sendo carregado?

Me dá diagnóstico e correção."
```

---

### 6.2 Estrutura diferente do padrão

**SINTOMA:** Agente criado não segue padrão CODEXA

**SOLUÇÃO:**
```
"Estrutura não está no padrão fractal CODEXA.
Reorganiza seguindo:
agente_nome/
├── PRIME.md
├── README.md
├── iso_vectorstore/
├── prompts/
├── validators/
└── workflows/

Cada arquivo deve seguir template dos outros agentes."
```

---

## 7. QUANDO PEDIR AJUDA AO MENTOR

Use `/prime-mentor` quando:

| Situação | Exemplo |
|----------|---------|
| Não sabe qual agente usar | "Quero fazer X, qual agente?" |
| Output repetidamente ruim | "Tentei 3x e não funciona" |
| Dúvida conceitual | "Não entendi o que é HOP" |
| Quer aprender mais | "Me ensina sobre copywriting" |
| Validar trabalho | "Esse anúncio está bom?" |

**COMANDO:**
```
/prime-mentor

"Estou tendo problema com [agente].
Tentei [o que você fez].
O resultado foi [o que aconteceu].
Esperava [o que queria].
Me ajuda a entender o que está errado?"
```

---

## REGRA DE OURO DO TROUBLESHOOTING

```
┌──────────────────────────────────────────────────┐
│                                                  │
│  SE O OUTPUT NÃO ESTÁ BOM:                       │
│                                                  │
│  1. Adicione mais CONTEXTO                       │
│  2. Seja mais ESPECÍFICO                         │
│  3. Peça EXATAMENTE o formato que quer           │
│  4. Mostre EXEMPLO do que espera                 │
│  5. Itere: refine, não recomece do zero          │
│                                                  │
│  LEMBRE: Agente não lê mentes.                   │
│  Quanto mais você explica, melhor o resultado.   │
│                                                  │
└──────────────────────────────────────────────────┘
```

---

**Arquivo**: `outputs/extras/TROUBLESHOOTING_GUIDE.md`
**Criado**: 2025-11-25
**Versão**: 1.0.0
**Para incluir em**: Todos os workbooks como anexo
