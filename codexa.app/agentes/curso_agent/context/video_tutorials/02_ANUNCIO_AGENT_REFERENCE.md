# ANUNCIO AGENT | Documento de Referencia para Video Tutorial

**Proposito**: Fonte de conhecimento para NotebookLM gerar video tutorial
**Agente**: anuncio_agent v2.5.0
**Duracao do Video**: 3-5 minutos

---

## O QUE E O ANUNCIO AGENT

O Anuncio Agent e um copywriter especializado em e-commerce brasileiro. Ele transforma pesquisa de mercado ou brief de produto em anuncios completos para marketplaces (Mercado Livre, Shopee, Magazine Luiza, Amazon BR).

**Transformacao**: Research notes / Brief → Anuncio completo para marketplace
**Duracao da execucao**: 10-15 minutos (full) / 2-3 minutos (quick)
**Output**: Bloco unico copiavel para marketplace

---

## COMO O USUARIO INICIA

O usuario digita uma frase simples:

```
"Quero anunciar [URL do produto]"
```

ou

```
"Quero anunciar garrafa termica 500ml inox"
```

Se o Pesquisa Agent ja foi executado, o usuario pode colar o research_notes.md como contexto.

O agente NAO conversa. Ele EXECUTA o workflow completo automaticamente.

---

## O QUE O AGENTE ENTREGA

### 1. Titulos (3 variacoes)
- 58-60 caracteres cada
- ZERO conectores ("de", "para", "com", "e")
- 8-10 keywords por titulo
- Otimizado para SEO de marketplace

**Exemplo**:
```
Garrafa Termica Inox 500ml Quente Frio 24h BPA Free Premium
```

### 2. Keywords (2 blocos)
- Bloco 1: 115-120 termos
- Bloco 2: 115-120 termos (sem duplicatas)
- Separados por virgula
- Prontos para colar no campo de tags

### 3. Bullets (10 pontos)
- 250-299 caracteres cada
- Gatilhos mentais (escassez, prova social, autoridade)
- Beneficios > Features
- Estrutura: EMOJI + GANCHO + BENEFICIO + PROVA

**Exemplo**:
```
MANTÉM BEBIDA GELADA 24H - Tecnologia de dupla parede a vácuo preserva temperatura por até 24 horas frias ou 12 horas quentes, ideal para o dia todo no escritório ou academia
```

### 4. Descricao Longa (≥3.300 caracteres)
- Framework StoryBrand (7 elementos)
- Estrutura narrativa persuasiva
- Gatilhos PNL integrados
- Compliance ANVISA/INMETRO automatico

**Os 7 Elementos StoryBrand**:
1. Heroi (cliente)
2. Problema (dor)
3. Guia (produto)
4. Plano (como funciona)
5. Chamada a acao
6. Evitar fracasso (o que perde se nao comprar)
7. Sucesso (transformacao)

---

## O WORKFLOW COMPLETO (6 Fases)

### Fase 1: INPUT
- Recebe research_notes.md ou brief do produto
- Identifica: head terms, diferenciais, dores, ganhos

### Fase 2: PARSE
- Extrai informacoes estruturadas
- Mapeia keywords prioritarias
- Identifica compliance necessario

### Fase 3: GENERATE
- Gera 3 titulos (HOP 14)
- Gera 2 blocos de keywords (HOP 15)
- Gera 10 bullets (HOP 16)
- Gera descricao longa (HOP 17)

### Fase 4: VALIDATE
- Verifica 11 criterios de qualidade
- Checa compliance ANVISA/INMETRO
- Valida limites de caracteres

### Fase 5: OUTPUT
- Formata em bloco unico copiavel
- Pronto para colar no marketplace

### Fase 6: OPCIONAL
- Prompts de imagem (9 cenas)
- Roteiro de video
- Metadata SEO
- Variacoes A/B

---

## OS 11 CRITERIOS DE QUALIDADE

**Copy (6 pontos)**:
1. Titulos: 3 x 58-60 chars, ZERO conectores
2. Keywords Bloco 1: 115-120 termos
3. Keywords Bloco 2: 115-120 termos (sem duplicatas)
4. Bullets: 10 x 250-299 chars
5. Descricao: ≥3.300 chars
6. Legibilidade: Flesch >60

**Compliance (5 pontos)**:
7. Sem tags HTML/CSS
8. Sem emojis/Unicode decorativos (exceto bullets)
9. Sem claims proibidos ("#1", "melhor do Brasil")
10. Sem claims terapeuticos (ANVISA)
11. Sem links externos

**Status**: PASS (100%) | PARTIAL (90-99%) | FAIL (<90%)

---

## EXEMPLO DE OUTPUT

**Input**:
```
Quero anunciar garrafa termica 500ml inox
- Mantem temperatura 24h
- BPA free
- Tampa anti-vazamento
- Publico: profissionais urbanos
```

**Output (resumido)**:

```
=== TITULO 1 ===
Garrafa Termica Inox 500ml Quente Frio 24h BPA Free Premium

=== TITULO 2 ===
Garrafa Agua Termica 500ml Inox Academia Escritorio 24 Horas

=== TITULO 3 ===
Squeeze Termico Inox 500ml BPA Free Quente Frio Tampa Segura

=== KEYWORDS BLOCO 1 ===
garrafa termica, garrafa inox, squeeze termico, 500ml, bpa free...
[115-120 termos]

=== KEYWORDS BLOCO 2 ===
garrafa agua quente, garrafa fria 24h, tampa anti vazamento...
[115-120 termos sem duplicatas]

=== BULLET 1 ===
MANTÉM BEBIDA GELADA 24H - Tecnologia de dupla parede...

[... 10 bullets ...]

=== DESCRICAO ===
[Narrativa StoryBrand com ≥3.300 caracteres]
```

---

## POR QUE USAR O ANUNCIO AGENT

1. **Economia de tempo**: 10-15 min vs 2+ horas manual
2. **SEO otimizado**: Keywords baseadas em dados reais de mercado
3. **Compliance automatico**: ANVISA, INMETRO, CONAR integrado
4. **Conversao comprovada**: StoryBrand + gatilhos PNL
5. **Multi-marketplace**: ML, Shopee, Magalu, Amazon BR

---

## CONEXAO COM OUTROS AGENTES

```
PESQUISA AGENT
     |
     | research_notes.md (opcional)
     v
ANUNCIO AGENT ← Voce esta aqui
     |
     | anuncio.md
     v
PHOTO AGENT → Prompts de foto alinhados
```

O Anuncio Agent pode funcionar sozinho (com brief) ou usar dados do Pesquisa Agent para resultados superiores.

---

## MODOS DE EXECUCAO

| Modo | Duracao | Completude | Quando usar |
|------|---------|------------|-------------|
| **Full** | 10-15min | 100% | Lancamento de produto |
| **Quick** | 2-3min | 75% | Iteracao rapida |
| **Visual** | 15-20min | 100%+ | Pacote completo com fotos |

---

## MENSAGEM CHAVE PARA O VIDEO

"O Anuncio Agent transforma seu produto em copy que converte. Titulos com 8-10 keywords, bullets com gatilhos mentais, descricao com storytelling persuasivo. Tudo com compliance automatico. Voce digita uma frase, ele entrega um anuncio pronto para colar no marketplace."

---

**Arquivo fonte**: agentes/anuncio_agent/PRIME.md
**Versao**: 2.5.0
