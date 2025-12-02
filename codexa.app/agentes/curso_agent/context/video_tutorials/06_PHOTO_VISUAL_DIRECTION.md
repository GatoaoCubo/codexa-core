<!-- TEMPLATE: Requires hydration with brand values -->
<!-- Placeholders: {{BRAND_NAME}}, {{BRAND_URL}}, {{PRIMARY_COLOR}}, {{SECONDARY_COLOR}} -->

# PHOTO AGENT | Direção Visual para Video Tutorial

**Proposito**: Guia de estilo visual para video NotebookLM
**Agente**: photo_agent v2.5.0
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

### Cores do Photo Agent
```
MAGENTA CRIATIVO: #EC4899 (fotografia, arte)
AZUL TECNICO: #3B82F6 (camera, specs)
AMARELO LUZ: #FBBF24 (iluminacao)
BRANCO PURO: #FFFFFF (fundo de produto)
```

---

## ELEMENTOS VISUAIS DO WORKFLOW

### Icones por Fase

| Fase | Icone Sugerido | Cor |
|------|---------------|-----|
| Scene Planning | Storyboard/Grid | Magenta |
| Technical Setup | Camera/Settings | Azul |
| Prompt Generation | Code/Text | Teal |
| Brand Validation | Palette/Check | Magenta |
| Output Assembly | Export/Layers | Teal |

### Representacao do Grid 3x3

```
+-------+-------+-------+
|   1   |   2   |   3   |
| Pack  | Hero  |Detail |
+-------+-------+-------+
|   4   |   5   |   6   |
|Scale  | Life  |Context|
+-------+-------+-------+
|   7   |   8   |   9   |
| Flat  |Group  |Clean  |
+-------+-------+-------+

Bordas: Teal para cenas 1 e 9 (marketplace compliant)
```

---

## ESTRUTURA VISUAL DO VIDEO

### Cena 1: Abertura (0:00-0:15)
- Fundo: Gradiente branco → magenta suave
- Texto central: "PHOTO AGENT"
- Subtitulo: "Diretor de Fotografia de E-commerce"
- Logo {{BRAND_NAME}} discreto no canto

### Cena 2: O Problema (0:15-0:30)
- Split screen: Foto amadora | Foto profissional
- Texto overlay: "Fotos vendem. Fotos ruins repelem."
- Transicao: Morph entre as duas fotos

### Cena 3: O Input (0:30-0:50)
- Terminal/Chat interface estilizado
- Animacao de digitacao: `"Quero foto de garrafa termica inox preta 500ml"`
- Highlight verde quando completo

### Cena 4: Scene Planning (0:50-1:30)
- Grid 3x3 aparecendo celula por celula
- Cada celula:
  - Numero aparece
  - Nome da cena
  - Thumbnail representativo
  - Icone de camera

### Cena 5: Technical Setup (1:30-2:15)
- **Dashboard de camera**:
```
+----------------------------------+
|  CAMERA PROFILE: STUDIO          |
|  ================================|
|  Lens: 85mm                      |
|  Aperture: f/2.8                 |
|  ISO: 100                        |
|  Shutter: 1/125s                 |
+----------------------------------+
|  LIGHTING: SOFTBOX               |
|  ================================|
|  Position: 45° left              |
|  Intensity: 80%                  |
|  Diffusion: High                 |
+----------------------------------+
```

### Cena 6: Prompt Generation (2:15-3:15)
- Split screen:
  - Esquerda: Cena selecionada (ex: Lifestyle)
  - Direita: Prompt sendo gerado

- Animacao typewriter mostrando estrutura:
```
{user_image} {seed:42}

Professional product photography...
Camera: Canon EOS R5, 50mm f/1.8...
Lighting: Natural window light...
Composition: Rule of thirds...
```

### Cena 7: Output Final (3:15-3:45)
- Dois blocos aparecendo:
  1. "PROMPT 1: Grid 3x3 Master"
  2. "PROMPT 2: 9 Prompts Individuais"
- Mockup de IA gerando imagem (Midjourney style)
- Antes/Depois: Prompt → Foto gerada

### Cena 8: CTA (3:45-4:15)
- Logo {{BRAND_NAME}} centralizado
- Texto: "Transforme seus produtos em arte"
- URL: {{BRAND_URL}}
- Gradiente {{PRIMARY_COLOR}} de fundo

---

## ANIMACOES RECOMENDADAS

### Grid 3x3 Animation
```
Sequencia de aparicao:
1 → 2 → 3
↓
4 → 5 → 6
↓
7 → 8 → 9

Cada celula: Scale 0→1 + Fade in (0.2s cada)
Delay entre celulas: 0.15s
Total: ~1.8s para grid completo
```

### Camera Settings Animation
```
Dial girando para valor:
ISO: 100 ← 400 ← 800 (spin animation)
Aperture: f/1.8 → f/2.8 → f/5.6 (step animation)
```

### Lighting Diagram
```
        [SOFTBOX]
            ↓
      45°  |
           |
    [PRODUTO] ←→ [CAMERA]
           |
           |
      [REFLETOR]

Animacao: Raios de luz emanando da softbox
```

---

## VISUALIZACAO DAS 9 CENAS

### Cards de Cena
```
+---------------------------+
|  [THUMBNAIL]              |
|                           |
|  CENA 5: LIFESTYLE        |
|  -------------------------|
|  Proposito: Uso real      |
|  Background: Ambiente     |
|  Gatilho: Pertencimento   |
|                           |
|  Camera: 50mm f/1.8       |
|  Lighting: Natural        |
+---------------------------+
```

### Gatilhos PNL Visual
```
| Cena | Icone | Emocao |
|------|-------|--------|
| Pack Shot | 📦 | Confianca |
| Hero Shot | ⭐ | Aspiracao |
| Detail | 🔍 | Seguranca |
| Scale | 📏 | Racional |
| Lifestyle | 🏃 | Social |
| In-Context | 🏠 | Imaginacao |
| Flat Lay | 📐 | Controle |
| Group | 🎨 | Liberdade |
| Clean | ✅ | Credibilidade |
```

---

## TIPOGRAFIA

### Fontes Sugeridas
```
Titulos: Inter Bold / Montserrat Bold
Specs tecnicas: JetBrains Mono
Prompts: Fira Code (monoespace)
```

### Hierarquia Visual
```
NOME DA CENA: 28px, Bold, Cor da categoria
Specs: 14px, Mono, Azul tecnico
Prompt preview: 12px, Mono, Cinza escuro
Labels: 12px, Regular, Cinza medio
```

---

## MOOD E TOM

### Palavras-Chave Visuais
- Artistico
- Tecnico
- Profissional
- Criativo
- Premium

### O que EVITAR
- Filtros exagerados nas fotos exemplo
- UI muito complexa
- Termos tecnicos sem explicacao
- Comparacoes de "antes feio/depois bonito"
- Promessas de resultados magicos

### O que PRIORIZAR
- Processo tecnico visivel
- Specs de camera claras
- Grid organizado
- Prompt legivel
- Flexibilidade (funciona em qualquer IA)

---

## EXEMPLOS DE COMPOSICAO

### Tela de Scene Planning
```
+------------------------------------------+
|  PHOTO AGENT                      [logo] |
+------------------------------------------+
|                                          |
|  Planejando 9 Cenas para:               |
|  "Garrafa Termica Inox Preta 500ml"     |
|                                          |
|  +------+ +------+ +------+             |
|  |PACK  | |HERO  | |DETAIL|             |
|  | ✓    | | ✓    | | ...  |             |
|  +------+ +------+ +------+             |
|  +------+ +------+ +------+             |
|  |SCALE | |LIFE  | |CONTXT|             |
|  |      | |      | |      |             |
|  +------+ +------+ +------+             |
|                                          |
+------------------------------------------+
```

### Tela de Prompt Output
```
+------------------------------------------+
|  PROMPT GERADO - CENA 5: LIFESTYLE       |
+------------------------------------------+
|                                          |
|  {user_image} {seed:42}                  |
|                                          |
|  Professional product photography of     |
|  black stainless steel thermal bottle    |
|  500ml in lifestyle setting.             |
|                                          |
|  Camera: Canon EOS R5, 50mm f/1.8 lens   |
|  Lighting: Natural window light          |
|  Composition: Rule of thirds             |
|  Background: [MINIMALIST_INTERIOR]       |
|  Mood: Aspirational, healthy lifestyle   |
|                                          |
|  [COPIAR] [PROXIMO]                      |
+------------------------------------------+
```

---

## MOCKUP DE IA DE IMAGEM

### Estilo Midjourney
```
+------------------------------------------+
|  /imagine prompt: {user_image} {seed:42} |
|  Professional product photography...      |
+------------------------------------------+
|                                          |
|  [████████████████] 78%                  |
|                                          |
|  +--------+  +--------+                  |
|  |        |  |        |                  |
|  | FOTO 1 |  | FOTO 2 |                  |
|  |        |  |        |                  |
|  +--------+  +--------+                  |
|  +--------+  +--------+                  |
|  |        |  |        |                  |
|  | FOTO 3 |  | FOTO 4 |                  |
|  |        |  |        |                  |
|  +--------+  +--------+                  |
|                                          |
+------------------------------------------+
```

---

## ASSETS NECESSARIOS

1. Logo {{BRAND_NAME}} (SVG)
2. Icones das 9 cenas
3. Diagrama de lighting setups
4. Mockup de camera/lens
5. Grid 3x3 template
6. Mockup de Midjourney/DALL-E
7. Thumbnails exemplo das cenas
8. Icones de gatilhos PNL

---

**Versao**: 1.0.0
**Data**: 2025-12-01
