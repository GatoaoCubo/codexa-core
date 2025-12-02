# Hailuo AI (MiniMax) - Guia de Prompt Engineering

**Versão**: 2.3 (2025) | **Empresa**: MiniMax | **Status**: Emergente/Competitivo

---

## Overview

Hailuo (MiniMax) oferece uma das gerações mais rápidas do mercado com excelente física humana e efeitos visuais. Ideal para movimentos dinâmicos e estilização.

**Specs**:
- Duração: 6 segundos
- Resolução: 768p (expandindo)
- Tempo de geração: ~55 segundos
- Especialidade: Física humana, VFX, estilização

---

## Fórmula de Prompt

### Estrutura Otimizada
```
[Camera Shot + Motion] + [Subject + Description] + [Action] + [Scene + Description] + [Lighting] + [Style/Mood]
```

### Mecanismo de Atenção
O AI prioriza elementos no **início** do prompt. Coloque o mais importante primeiro.

```
✅ CORRETO: "A glowing golden orb, floating in dark space, emitting particles..."
❌ ERRADO: "In a dark space, there is something that looks like an orb that glows..."
```

---

## Melhores Práticas

### 1. Elemento-Chave Primeiro
```
✅ "A premium sneaker rotating slowly, white background, studio lighting..."
❌ "There is a white background with studio lighting where a sneaker rotates..."
```

### 2. Movimento Específico
```
✅ "The person slowly raises their right arm, hand open reaching toward light, hair gently sways in breeze"
❌ "The person moves"
```

### 3. Instruções de Câmera Claras
```
"camera tracks behind"
"dolly forward"
"slow zoom in"
"smooth pan right"
"static centered shot"
```

### 4. Marcadores de Ênfase
Use parênteses duplos para priorizar:
```
"A confident woman, ((wearing a red blazer)), standing in modern office"
```

---

## Camera Keywords

### Movimentos Confiáveis
| Movimento | Sintaxe | Uso |
|-----------|---------|-----|
| Tracking | `camera tracks behind subject` | Seguir personagem |
| Dolly | `dolly forward slowly` | Aproximação emotiva |
| Pan | `smooth pan left to right` | Revelar ambiente |
| Zoom | `slow zoom into face` | Foco em detalhe |
| Orbit | `camera orbits around product` | 360° de objeto |
| Static | `static centered shot` | Estabilidade |

### Combinações Efetivas
```
"Tracking shot, camera follows from behind as..."
"Slow dolly forward while subject..."
"Static wide shot with subtle zoom..."
```

---

## Estilos e Estilização

### Estilos Artísticos
```
"Pixar-style 3D animation"
"film noir aesthetic"
"cyberpunk neon"
"surrealist dreamscape"
"minimalist modern"
```

### Paletas de Cor
```
"muted tones"
"vibrant saturated colors"
"black and white"
"golden warm palette"
"cool blue-silver tones"
```

### Efeitos
```
"slow-motion effect"
"time-lapse"
"dramatic lighting"
"lens flare"
"bokeh background"
```

---

## Forças do Hailuo

### 1. Física Humana Excepcional
```
A dancer performing fluid contemporary movements, arms extending gracefully, fabric of dress flowing with momentum, natural weight transfer between poses, professional stage lighting.
```

### 2. Movimentos Dinâmicos
```
An athlete executing a perfect backflip, body rotating with natural physics, landing with slight knee bend absorbing impact, outdoor training ground, golden hour lighting.
```

### 3. VFX e Efeitos
```
Magical particles swirling around a floating crystal, each particle emitting soft blue glow, crystalline reflections, dark ethereal background, cinematic fantasy lighting.
```

### 4. Transformações de Estilo
```
Portrait of a woman transforming from realistic photography into Pixar-style 3D animation, smooth transition maintaining facial features, studio lighting throughout.
```

---

## Image-to-Video

### Requisitos
- Imagem alta qualidade (até 20MB)
- Alta resolução para detalhes
- Composição clara

### Boas Práticas
```
1. Match imagem + prompt (ação factível dada a imagem)
2. Movimentos simples a partir da pose inicial
3. Câmera clara e específica
4. Não pedir ações impossíveis
```

### Exemplo
```
Image: [Retrato de empresário sentado]
Prompt: The man leans forward with confident expression, gestures with right hand while speaking, subtle head movement, warm office lighting, camera slowly pushes in, professional corporate video style.
```

---

## Features Especiais

### Scene Ingredients
Decomponha vídeos em componentes customizáveis:
- Backgrounds separados
- Posicionamento de objetos
- Interações de personagens

```
"Two characters only: businessman on left, client on right, modern conference room background, natural daylight from window"
```

### Chained Prompts (Storytelling)
```
"A robot wakes up in a desert > walks toward a distant city > gets scanned by hovering drones"
```

---

## Casos de Uso E-commerce

### Product Hero Shot
```
((Premium wireless earbuds)), floating and slowly rotating against gradient dark background, soft blue accent lighting creating rim light, particles of light floating around product, camera slowly orbits, cinematic product photography, 4K quality.
```

### Brand Story
```
Dolly forward: Entrepreneur sits at modern desk, multiple monitors showing analytics, ((confident smile)), leans back in chair with satisfaction. Warm golden hour light through windows, modern office environment, corporate success aesthetic.
```

### Dynamic Showcase
```
((Athletic sneaker)) in dramatic slow-motion, water droplets splashing around as it lands, dynamic lighting with rim light highlighting contours, dark background, sports advertisement style, high energy.
```

### Transformation Narrative
```
Split composition morphing: Left shows stressed seller in cold blue lighting with declining graphs, smoothly transforms to right side showing same person confident in warm golden lighting with rising metrics. Professional corporate video style.
```

---

## Templates Rápidos

### Tech Product
```
((Product name)) hovering in dark tech environment, holographic UI elements orbiting around it, blue-purple neon accent lighting, slow camera orbit, futuristic aesthetic, premium quality.
```

### Fashion Item
```
((Clothing item)) worn by model in confident pose, fabric catching light naturally, smooth slow-motion movement, professional fashion photography lighting, editorial style.
```

### Food/Beverage
```
((Food/drink item)) in appetizing hero presentation, ((steam rising naturally)), warm inviting lighting, slow zoom revealing textures, food photography excellence.
```

---

## Hailuo 2.3 (Mais Recente)

### Novidades
- Parceria com VEED
- Física humana ainda melhor
- VFX capabilities expandidos
- Estilização mais precisa
- Geração ~55s para 6s de vídeo

### Acesso
- VEED AI Playground
- API MiniMax

---

## Referências

- [Curious Refuge - 5 Tips for Cinematic Video with MiniMax](https://curiousrefuge.com/blog/5-tips-for-using-minimax-ai-video-generator-by-hailuo-ai)
- [Flux AI - Ultimate Guide to Hailuo 02](https://flux-ai.io/blog/detail/The-Ultimate-Guide-to-Hailuo-02-MiniMax-s-Cinematic-AI-Video-Model-e128c65d7401/)
- [Segmind - Hailuo Minimax Prompt Guide](https://blog.segmind.com/hailuo-minimax-ai-video-prompt-guide/)
- [GetImg - Guide to MiniMax Hailuo Models](https://getimg.ai/blog/the-ultimate-guide-to-minimax-hailuo-ai-video-models)
- [MiniMax News - Hailuo 2.3 Launch](https://www.minimax.io/news/minimax-and-veed-hailuo-23-for-pro-level-ai-video)

---

**Última atualização**: 2025-11-24
