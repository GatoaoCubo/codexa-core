<!-- TEMPLATE: Requires hydration with brand values -->
<!-- Placeholders: {{BRAND_NAME}}, {{BRAND_URL}}, {{PRIMARY_COLOR}}, {{SECONDARY_COLOR}} -->

# PESQUISA AGENT | Direção Visual para Video Tutorial

**Proposito**: Guia de estilo visual para video NotebookLM
**Agente**: pesquisa_agent v3.1.0
**Alinhamento**: {{BRAND_NAME}} Brand + Landing Page

---

## PALETA DE CORES

### Cores Primarias ({{BRAND_NAME}} Brand)
```
PRIMARY: {{PRIMARY_COLOR}} (destaque, CTAs)
SECONDARY: {{SECONDARY_COLOR}} (hover, secundario)
BRANCO: #FFFFFF (fundo principal)
CINZA ESCURO: #1F2937 (texto principal)
CINZA MEDIO: #6B7280 (texto secundario)
```

### Cores do Pesquisa Agent
```
AZUL INTEL: #3B82F6 (inteligencia, dados)
VERDE SUCESSO: #10B981 (validacao, completo)
AMARELO ALERTA: #F59E0B (atencao, lacunas)
```

---

## ELEMENTOS VISUAIS DO WORKFLOW

### Icones por Fase

| Fase | Icone Sugerido | Cor |
|------|---------------|-----|
| Brief Input | Documento/Clipboard | Teal |
| Query Generation | Lupa/Search | Azul |
| Marketplace Scan | Carrinho/Store | Teal |
| SERP Analysis | Globe/Web | Azul |
| Competitor Analysis | Chart/Graph | Verde |
| Compliance Check | Shield/Check | Verde |
| Output Assembly | File/Export | Teal |

### Representacao dos 9 Marketplaces

```
Grid 3x3 com logos estilizados:

[ML]  [SHP] [MAG]
[AMZ] [AME] [CB]
[SUB] [TIK] [SHE]

Cores dos badges:
- Mercado Livre: #FFE600 (amarelo)
- Shopee: #EE4D2D (laranja)
- Magazine Luiza: #0086FF (azul)
- Amazon: #FF9900 (laranja)
- Americanas: #E60014 (vermelho)
- Casas Bahia: #0046C0 (azul)
- Submarino: #00AEEF (azul claro)
- TikTok Shop: #000000 (preto)
- Shein: #000000 (preto)
```

---

## ESTRUTURA VISUAL DO VIDEO

### Cena 1: Abertura (0:00-0:15)
- Fundo: Gradiente branco → cinza claro
- Texto central: "PESQUISA AGENT"
- Subtitulo: "Inteligencia Competitiva em 20 Minutos"
- Logo {{BRAND_NAME}} discreto no canto

### Cena 2: O Problema (0:15-0:30)
- Split screen: Pessoa frustrada | Planilhas confusas
- Texto overlay: "4-8 horas de pesquisa manual"
- Transicao: Fade para solucao

### Cena 3: O Input (0:30-0:50)
- Terminal/Chat interface estilizado
- Animacao de digitacao: `"Quero pesquisar garrafa termica"`
- Highlight verde quando completo

### Cena 4: O Workflow (0:50-2:30)
- **Timeline horizontal** mostrando 9 passos
- Cada passo:
  - Icone animado aparece
  - Barra de progresso preenche
  - Texto breve do que esta acontecendo
  - Fade para proximo passo

### Cena 5: Os 22 Blocos (2:30-3:30)
- Grid animado 4x6 (22 blocos + 2 vazios)
- Cada bloco aparece com efeito de "check"
- Highlight nos blocos mais importantes:
  - Resumo Executivo (ouro)
  - Gaps Competitivos (verde)
  - Oportunidades (teal)

### Cena 6: Output Final (3:30-4:00)
- Documento research_notes.md aparecendo
- Zoom em secoes chave
- Texto: "Pronto para o Anuncio Agent"

### Cena 7: CTA (4:00-4:30)
- Logo {{BRAND_NAME}} centralizado
- Texto: "Comece sua pesquisa agora"
- URL: {{BRAND_URL}}
- Gradiente {{PRIMARY_COLOR}} de fundo

---

## ANIMACOES RECOMENDADAS

### Transicoes
```
Entre secoes: Slide horizontal suave (0.5s)
Entre passos: Fade + Scale (0.3s)
Highlights: Pulse glow (2s loop)
```

### Elementos Animados
```
Barra de progresso: Fill linear (duracao proporcional)
Icones: Bounce on appear (0.2s)
Numeros: Count up animation
Texto: Typewriter effect para inputs
```

---

## TIPOGRAFIA

### Fontes Sugeridas
```
Titulos: Inter Bold / Montserrat Bold
Corpo: Inter Regular
Codigo/Terminal: JetBrains Mono / Fira Code
```

### Tamanhos
```
Titulo principal: 48-64px
Subtitulos: 32-40px
Corpo: 18-24px
Labels: 14-16px
```

---

## MOOD E TOM

### Palavras-Chave Visuais
- Profissional
- Eficiente
- Confiavel
- Inteligente
- Moderno

### O que EVITAR
- Cores neon agressivas
- Animacoes exageradas
- Muitos elementos na tela
- Fontes decorativas
- Imagens stock genericas

### O que PRIORIZAR
- Espaco em branco
- Hierarquia clara
- Movimento sutil
- Dados visiveis
- Fluxo logico

---

## EXEMPLOS DE COMPOSICAO

### Tela de Workflow
```
+------------------------------------------+
|  PESQUISA AGENT                    [logo]|
+------------------------------------------+
|                                          |
|  [===========------------] 45%           |
|                                          |
|  Passo 3 de 9: Pesquisa Inbound         |
|                                          |
|  +------+  +------+  +------+           |
|  | [ML] |  | [SHP]|  | [MAG]|           |
|  |  OK  |  |  OK  |  | ...  |           |
|  +------+  +------+  +------+           |
|                                          |
|  Keywords encontradas: 47               |
|  Concorrentes mapeados: 12              |
|                                          |
+------------------------------------------+
```

### Tela de Output
```
+------------------------------------------+
|  research_notes.md              [export] |
+------------------------------------------+
|                                          |
|  # RESUMO EXECUTIVO                     |
|  Mercado em expansao. Gap identificado. |
|                                          |
|  # HEAD TERMS                           |
|  garrafa termica, squeeze inox...       |
|                                          |
|  # OPORTUNIDADES ★                      |
|  1. Posicionamento premium              |
|  2. Foco em home office                 |
|                                          |
+------------------------------------------+
```

---

## ASSETS NECESSARIOS

1. Logo {{BRAND_NAME}} (SVG)
2. Icones do workflow (9 icones)
3. Logos dos marketplaces (9 logos)
4. Background gradients (3 variacoes)
5. Animacao de loading/progress
6. Mockup de terminal/chat
7. Mockup de documento markdown

---

**Versao**: 1.0.0
**Data**: 2025-12-01
