<!-- TEMPLATE: Requires hydration with brand values -->
<!-- Placeholders: {{BRAND_NAME}}, {{BRAND_URL}}, {{PRIMARY_COLOR}}, {{SECONDARY_COLOR}} -->

# ANUNCIO AGENT | Direção Visual para Video Tutorial

**Proposito**: Guia de estilo visual para video NotebookLM
**Agente**: anuncio_agent v2.5.0
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

### Cores do Anuncio Agent
```
LARANJA CONVERSAO: #F97316 (urgencia, CTA)
ROXO CRIATIVO: #8B5CF6 (copy, criatividade)
VERDE VALIDACAO: #10B981 (aprovado, compliant)
VERMELHO ALERTA: #EF4444 (erro, rejeicao)
```

---

## ELEMENTOS VISUAIS DO WORKFLOW

### Icones por Fase

| Fase | Icone Sugerido | Cor |
|------|---------------|-----|
| Input/Brief | Inbox/Import | Teal |
| Parse | Code/Extract | Roxo |
| Generate | Pencil/Write | Laranja |
| Validate | Shield/Check | Verde |
| Output | Export/Copy | Teal |

### Representacao dos Elementos do Anuncio

```
Stack vertical estilizado:

+---------------------------+
| TITULO                    | → 58-60 chars
| ========================= |
+---------------------------+
| KEYWORDS                  | → 115-120 termos x2
| ========================= |
+---------------------------+
| BULLETS (10)              | → 250-299 chars cada
| • Bullet 1               |
| • Bullet 2               |
| • ...                    |
+---------------------------+
| DESCRICAO                 | → ≥3.300 chars
| ========================= |
+---------------------------+
```

---

## ESTRUTURA VISUAL DO VIDEO

### Cena 1: Abertura (0:00-0:15)
- Fundo: Gradiente branco → laranja suave
- Texto central: "ANUNCIO AGENT"
- Subtitulo: "Copy que Converte em 10 Minutos"
- Logo {{BRAND_NAME}} discreto no canto

### Cena 2: O Problema (0:15-0:30)
- Split screen: Anuncio amador | Anuncio sem cliques
- Texto overlay: "Copy sem estrategia = vendas perdidas"
- Transicao: Fade para solucao

### Cena 3: O Input (0:30-0:50)
- Terminal/Chat interface estilizado
- Animacao de digitacao: `"Quero anunciar garrafa termica 500ml"`
- Opcional: research_notes.md entrando como contexto
- Highlight verde quando completo

### Cena 4: O Workflow (0:50-2:00)
- **Timeline vertical** mostrando 6 fases
- Cada fase:
  - Icone aparece
  - Barra de progresso
  - Preview do que esta sendo gerado
  - Transicao fluida

### Cena 5: Geracao em Tempo Real (2:00-3:00)
- **Split screen animado**:
  - Esquerda: Codigo/processo
  - Direita: Output aparecendo

```
Sequencia:
1. Titulos aparecem (3x) - typewriter
2. Keywords fluem (como tags)
3. Bullets surgem (1 por 1)
4. Descricao preenche (scroll)
```

### Cena 6: Validacao (3:00-3:30)
- Checklist animado dos 11 criterios
- Cada item recebe check verde
- Contador: "11/11 PASS"
- Badge de qualidade aparece

### Cena 7: Output Final (3:30-4:00)
- Documento anuncio.md completo
- Botao "Copiar" com efeito de clique
- Mockup de marketplace recebendo o conteudo
- Texto: "Pronto para publicar"

### Cena 8: CTA (4:00-4:30)
- Logo {{BRAND_NAME}} centralizado
- Texto: "Crie seu anuncio agora"
- URL: {{BRAND_URL}}
- Gradiente {{PRIMARY_COLOR}} de fundo

---

## ANIMACOES RECOMENDADAS

### Efeito Typewriter para Titulos
```
Garrafa Termica Inox 500ml Quente Frio 24h BPA Free Premium
         ^
         cursor piscando enquanto digita
```

### Efeito Flow para Keywords
```
Tags aparecendo e flutuando para posicao:
[garrafa termica] [squeeze inox] [500ml] [bpa free]...
```

### Efeito Bullet por Bullet
```
• MANTÉM BEBIDA GELADA 24H - Tecnologia...
  [fade in + slide right]

• MATERIAL PREMIUM INOX 304 - Aço inoxidável...
  [fade in + slide right, 0.3s delay]
```

---

## VISUALIZACAO DOS GATILHOS MENTAIS

### Icones de Gatilho
```
ESCASSEZ: ⏰ Relogio
PROVA SOCIAL: 👥 Pessoas
AUTORIDADE: 🏆 Trofeu
URGENCIA: ⚡ Raio
GARANTIA: 🛡️ Escudo
```

### Highlight nos Bullets
```
+-----------------------------------------------+
| • MANTÉM BEBIDA GELADA 24H - Tecnologia de   |
|   dupla parede [ESCASSEZ] preserva temperatura|
|                    ↑                          |
|              badge animado                    |
+-----------------------------------------------+
```

---

## TIPOGRAFIA

### Fontes Sugeridas
```
Titulos: Inter Bold / Montserrat Bold
Copy preview: Inter Regular
Codigo/Terminal: JetBrains Mono
```

### Hierarquia Visual
```
TITULO DO ANUNCIO: 32px, Bold, Cinza Escuro
Keywords: 14px, Regular, Tags com fundo cinza
Bullets: 18px, Regular, Icone + Texto
Descricao: 16px, Regular, Paragrafo justificado
```

---

## MOOD E TOM

### Palavras-Chave Visuais
- Persuasivo
- Profissional
- Confiavel
- Conversao
- Estrategico

### O que EVITAR
- Cores de "vendas agressivas" (vermelho piscante)
- Textos longos demais na tela
- Muitos elementos simultaneos
- Comparacoes negativas
- Claims exagerados

### O que PRIORIZAR
- Antes/Depois sutil
- Metricas de qualidade
- Processo visivel
- Output limpo
- Compliance destacado

---

## EXEMPLOS DE COMPOSICAO

### Tela de Geracao
```
+------------------------------------------+
|  ANUNCIO AGENT                    [logo] |
+------------------------------------------+
|                                          |
|  Gerando Titulos...                      |
|                                          |
|  TITULO 1:                               |
|  Garrafa Termica Inox 500ml Quente Frio  |
|  24h BPA Free Premium                    |
|  [58 chars] ✓                            |
|                                          |
|  TITULO 2:                               |
|  ████████████░░░░░░░░                    |
|                                          |
+------------------------------------------+
```

### Tela de Validacao
```
+------------------------------------------+
|  VALIDACAO DE QUALIDADE           [100%] |
+------------------------------------------+
|                                          |
|  Copy                                    |
|  [✓] Titulos: 3x 58-60 chars            |
|  [✓] Keywords: 2x 115-120 termos        |
|  [✓] Bullets: 10x 250-299 chars         |
|  [✓] Descricao: 3.847 chars             |
|                                          |
|  Compliance                              |
|  [✓] Sem HTML/CSS                       |
|  [✓] Sem claims proibidos               |
|  [✓] ANVISA OK                          |
|                                          |
|  STATUS: PASS ✓                         |
|                                          |
+------------------------------------------+
```

---

## FRAMEWORK STORYBRAND VISUAL

### Os 7 Elementos (para animacao)
```
1. HEROI      → Icone de pessoa
2. PROBLEMA   → Icone de obstaculo
3. GUIA       → Icone de produto/estrela
4. PLANO      → Icone de mapa/steps
5. ACAO       → Icone de botao/CTA
6. FRACASSO   → Icone de X vermelho
7. SUCESSO    → Icone de check verde

Animacao: Timeline horizontal com cada elemento
aparecendo em sequencia, conectados por linha
```

---

## ASSETS NECESSARIOS

1. Logo {{BRAND_NAME}} (SVG)
2. Icones das fases (6 icones)
3. Icones de gatilhos mentais (5 icones)
4. Mockup de marketplace (ML, Shopee)
5. Animacao de typewriter
6. Badges de validacao
7. Background gradients

---

**Versao**: 1.0.0
**Data**: 2025-12-01
