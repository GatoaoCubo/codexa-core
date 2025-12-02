<!-- TEMPLATE: Requires hydration with brand values -->
<!-- Placeholders: {{BRAND_NAME}}, {{BRAND_URL}} -->

# PROMPT PARA NOTEBOOKLM VIDEO | ANUNCIO AGENT

**Usar com**: NotebookLM Video Generation
**Objetivo**: Video tutorial de 3-5 minutos simulando execucao do agente
**Tom**: Didatico, profissional, direto

---

## PROMPT

```
Crie um video tutorial explicativo sobre o ANUNCIO AGENT do {{BRAND_URL}}.

CONTEXTO:
O Anuncio Agent e um copywriter de IA especializado em e-commerce brasileiro. Ele transforma pesquisa de mercado ou brief de produto em anuncios completos prontos para colar em marketplaces (Mercado Livre, Shopee, Magazine Luiza, Amazon BR).

ESTRUTURA DO VIDEO (3-5 minutos):

ABERTURA (15 segundos):
- Apresente o Anuncio Agent como "seu copywriter que entende SEO de marketplace"
- Mencione: "Anuncios que convertem em 10-15 minutos"

O PROBLEMA (30 segundos):
- Explique a dor: escrever copy que vende e dificil e demorado
- Destaque: titulos sem keywords, descricoes fracas, bullets sem gatilhos
- O resultado: anuncios que nao aparecem nas buscas e nao convertem
- Transicao: "O Anuncio Agent resolve isso com copy estrategica"

O INPUT (30 segundos):
- Mostre como o usuario inicia: basta digitar uma frase
- Exemplo: "Quero anunciar garrafa termica 500ml inox"
- Opcao avancada: pode colar research_notes.md do Pesquisa Agent
- Enfatize: "NAO e uma conversa. E execucao automatica do workflow completo."

O QUE ELE ENTREGA (90 segundos):

1. TITULOS (3 variacoes):
   - 58-60 caracteres cada (limite de marketplace)
   - 8-10 keywords por titulo
   - ZERO conectores (de, para, com, e)
   - Exemplo: "Garrafa Termica Inox 500ml Quente Frio 24h BPA Free Premium"

2. KEYWORDS (2 blocos):
   - Bloco 1: 115-120 termos
   - Bloco 2: 115-120 termos (sem duplicatas)
   - Prontos para colar no campo de tags

3. BULLETS (10 pontos):
   - 250-299 caracteres cada
   - Gatilhos mentais integrados (escassez, prova social, autoridade)
   - Estrutura: EMOJI + GANCHO + BENEFICIO + PROVA

4. DESCRICAO LONGA:
   - Minimo 3.300 caracteres
   - Framework StoryBrand (7 elementos narrativos)
   - Gatilhos PNL integrados
   - Compliance automatico

O WORKFLOW - 6 FASES (45 segundos):
1. INPUT - Recebe brief ou research_notes
2. PARSE - Extrai informacoes estruturadas
3. GENERATE - Gera titulos, keywords, bullets, descricao
4. VALIDATE - Verifica 11 criterios de qualidade
5. OUTPUT - Formata em bloco copiavel
6. OPCIONAL - Prompts de imagem, roteiro de video

OS 11 CRITERIOS DE QUALIDADE (30 segundos):
- Copy: titulos, keywords, bullets, descricao, legibilidade
- Compliance: sem HTML, sem emojis proibidos, sem claims falsos
- Status final: PASS (100%) | PARTIAL (90-99%) | FAIL (<90%)
- "Voce so recebe o anuncio quando passa na validacao"

FRAMEWORK STORYBRAND (30 segundos):
- Explique brevemente os 7 elementos:
  1. Heroi (seu cliente)
  2. Problema (a dor)
  3. Guia (seu produto)
  4. Plano (como funciona)
  5. Chamada a acao
  6. Evitar fracasso
  7. Sucesso (transformacao)
- "Cada descricao conta uma historia persuasiva"

CONEXAO COM OUTROS AGENTES (20 segundos):
- Recebe dados do Pesquisa Agent (opcional)
- Alimenta o Photo Agent com context de copy
- Fluxo: Pesquisa → Anuncio → Foto

CTA (15 segundos):
- "Crie seu anuncio agora em {{BRAND_URL}}"
- "Copy que converte, compliance automatico"

TOM E ESTILO:
- Fale como um copywriter senior explicando sua metodologia
- Use exemplos concretos de titulos e bullets
- Mostre o valor: conversao + economia de tempo
- Evite ser vendedor demais - deixe os resultados falarem

MENSAGEM CHAVE A REPETIR:
"O Anuncio Agent transforma seu produto em copy que converte. Titulos com 8-10 keywords, bullets com gatilhos mentais, descricao com storytelling persuasivo. Tudo com compliance automatico. Voce digita uma frase, ele entrega um anuncio pronto para colar no marketplace."

DADOS NUMERICOS A MENCIONAR:
- 3 titulos de 58-60 caracteres
- 240 keywords (2 blocos de 120)
- 10 bullets de 250-299 caracteres
- Descricao de 3.300+ caracteres
- 11 criterios de validacao
- 10-15 minutos de execucao

NAO FAZER:
- Nao fale como chatbot
- Nao mostre exemplos muito longos (corta o ritmo)
- Nao seja tecnico demais - foque em resultados
- Nao prometa "vender mais" - prometa copy melhor
```

---

## CHECKLIST DE QUALIDADE

- [ ] Video entre 3-5 minutos
- [ ] Mostra input simples do usuario
- [ ] Explica os 4 outputs principais
- [ ] Mostra exemplo de titulo e bullet
- [ ] Menciona StoryBrand
- [ ] Destaca compliance automatico
- [ ] Conecta com Pesquisa e Photo Agent
- [ ] CTA para {{BRAND_URL}}
- [ ] Tom profissional, nao vendedor

---

**Versao**: 1.0.0
**Data**: 2025-12-01
