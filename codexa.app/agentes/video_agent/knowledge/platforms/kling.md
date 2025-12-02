# Kling AI 1.6 - Guia de Prompt Engineering

**Versão**: 1.6 (Dezembro 2024) | **Empresa**: Kuaishou | **Status**: Mainstream

---

## Overview

Kling 1.6 oferece excelente custo-benefício com 195% de melhoria sobre v1.5. Destaca-se em aderência a prompts, física realista e movimentos naturais.

**Specs**:
- Duração: 5 segundos (padrão), extensível
- Resolução: até 1080p
- FPS: 30 ou 60
- Aspect Ratios: 16:9, 9:16, 1:1
- Modos: Standard, Professional

---

## Estrutura de Prompt

### Fórmula Oficial
```
[Subject], [subject description], [subject movement], [scene]. [Scene description]. [Camera language, lighting, atmosphere].
```

### Três Elementos Essenciais
1. **Descrições claras** - O que está na cena
2. **Detalhes exatos** - Especificidades visuais
3. **Estrutura adequada** - Ordem lógica

### Exemplo
```
A confident Brazilian entrepreneur, wearing a navy blazer and white shirt, gestures toward a holographic dashboard, modern glass office. Sunset light streams through floor-to-ceiling windows creating warm rim lighting. Camera slowly dollies forward, shallow depth of field.
```

---

## Parâmetros Disponíveis

| Parâmetro | Valores | Descrição |
|-----------|---------|-----------|
| `prompt` | texto | Descrição do vídeo |
| `negative_prompt` | texto | O que evitar |
| `aspect_ratio` | 16:9, 9:16, 1:1 | Formato |
| `start_image` | imagem | Frame inicial (opcional) |
| `cfg_scale` | 0-1 | Aderência ao prompt |

### Configurações Recomendadas
```
fps: 60 (movimento fluido)
cfg_scale: 0.7-0.8 (balanço criatividade/controle)
aspect_ratio: 9:16 (social media vertical)
```

---

## Camera Keywords

### Taxa de Sucesso por Movimento

| Movimento | Sucesso | Notas |
|-----------|---------|-------|
| `Camera slowly zooms in` | 9/10 | Muito confiável |
| `Slow pan left/right` | 8/10 | Confiável |
| `Static shot` | 9/10 | Máxima estabilidade |
| `Tracking shot` | 7/10 | Bom para seguir sujeito |
| `Fast rotation 360` | 2/10 | Evitar - causa artefatos |
| `Rapid zoom` | 3/10 | Distorção e stuttering |

### Regra de Ouro
```
✅ Movimentos lentos e suaves = Alta qualidade
❌ Movimentos extremos e rápidos = Artefatos
```

---

## Magic Words para Qualidade

### Movimento Natural
```
"motion blur enabled"
"natural movement"
"fluid motion"
"smooth transition"
```

### Cores e Iluminação
```
"cobalt blue" (específico > "blue")
"forest green" (específico > "green")
"natural color grading"
"warm sunlight"
"cool LED lights"
"golden hour lighting"
```

### Qualidade Visual
```
"4K quality"
"cinematic"
"professional lighting"
"shallow depth of field"
```

---

## Forças do Kling 1.6

### 1. Animação de Personagens
```
A young woman with long black hair smiling and waving at the camera, standing in a sunny park, natural and friendly expression, gentle breeze moving her hair slightly.
```

### 2. Expressões Faciais
```
Close-up of a man's face transitioning from worried to relieved expression, subtle eye movement, natural skin texture, soft studio lighting.
```

### 3. Movimentos Sequenciais
```
A mechanical wolf rises slowly, spreading its limbs smoothly. The camera moves upward as its blue eyes narrow slightly. Neon lights flicker in background, mysterious futuristic atmosphere.
```

---

## Limitações e Soluções

### O que Evitar
| Problema | Motivo | Solução |
|----------|--------|---------|
| Números específicos | AI inconsistente | "multiple" ou "several" |
| Movimentos físicos complexos | Trajetórias difíceis | Simplificar movimento |
| Rotações rápidas | Artefatos | Movimentos lentos |
| Split-screen implícito | Confuso | Especificar ângulos |

### Negative Prompts Úteis
```
blurry, distorted, low quality, artifacts, glitches, unnatural movement, cartoon style, anime, watermark, text overlay
```

---

## Casos de Uso E-commerce

### Product Showcase
```
A premium wireless headphone floating and slowly rotating against pure white background, studio lighting creating soft shadows, product reflects ambient light, camera slowly zooms in. 4K quality, shallow depth of field, motion blur enabled.

Negative: cartoon, low quality, harsh shadows, cluttered background
```

### Testimonial Style
```
A confident Brazilian seller, 30s, sitting at modern desk with laptop showing analytics, speaking directly to camera with genuine smile, natural hand gestures, warm office lighting from window.

Negative: exaggerated expressions, unnatural movement, poor lighting
```

### Before/After Transformation
```
Split composition: left side shows stressed entrepreneur in blue cold lighting with declining graphs, right side shows same person relaxed with warm golden lighting and rising metrics, smooth visual transition between states.

Negative: harsh transition, inconsistent person, cartoon style
```

---

## Image-to-Video Tips

Quando usar imagem inicial:

1. **Imagem alta qualidade** (até 20MB)
2. **Match prompt com imagem** - ação deve ser factível
3. **Movimentos alinhados** - não pedir ações impossíveis dada a pose inicial
4. **Câmera clara** - especificar movimento desejado

### Exemplo
```
Image: [Foto de produto estático]
Prompt: The product slowly rotates revealing different angles, soft studio lighting remains consistent, camera orbits smoothly. Shallow depth of field, 4K quality.
```

---

## Templates por Categoria

### Tech/Gadgets
```
[Product name] hovering and slowly rotating in futuristic environment, holographic UI elements appearing around it, blue-purple neon accent lighting, camera slowly orbits. Cinematic 4K, shallow depth of field, motion blur enabled.
```

### Fashion
```
[Clothing item] worn by confident model walking toward camera, fabric flowing naturally with movement, professional runway lighting, camera tracks backward. Fashion photography style, natural color grading.
```

### Food
```
[Food item] in appetizing presentation, steam rising naturally, warm restaurant ambient lighting, camera slowly pushes in revealing texture details. Food photography style, shallow depth of field.
```

---

## Referências

- [RunDiffusion - Kling Prompt Guide](https://learn.rundiffusion.com/text-to-video-prompt-guide-how-to-prompt-with-kling/)
- [Tom's Guide - Kling 1.6 Test](https://www.tomsguide.com/ai/ai-image-video/i-put-kling-1-6-to-the-test-7-prompts-to-make-compelling-ai-videos)
- [Pollo AI - Kling Video Prompts](https://pollo.ai/hub/kling-ai-video-prompts)
- [Segmind - Kling Best Prompts](https://blog.segmind.com/best-text-to-video-prompts-for-kling-ai-with-examples/)

---

**Última atualização**: 2025-11-24
