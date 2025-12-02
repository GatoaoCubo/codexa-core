# Brand Alignment para Vídeo

**Sistema de Tradução** - Da marca para linguagem visual de vídeo

---

## Conceito

Assim como o `photo_agent` traduz marca para prompts de imagem, o `video_agent` traduz elementos de marca para linguagem cinematográfica.

```
Brand Profile → Video Language Translation → Prompts Alinhados
```

---

## Elementos de Marca → Vídeo

### 1. Cores da Marca → Color Grading

| Elemento da Marca | Tradução para Vídeo |
|-------------------|---------------------|
| Cor primária | Cor dominante na iluminação/ambiente |
| Cor secundária | Acentos de luz, detalhes |
| Cor de contraste | Highlights, rim lights |

**Exemplo CODEXA**:
```
Marca: Dourado + Azul escuro
→ Vídeo: "golden accent lighting on dark navy background, warm highlights"
```

**Template**:
```
"[primary color] as dominant lighting, [secondary color] accents, [contrast color] rim highlights"
```

### 2. Tom de Voz → Ritmo de Edição

| Tom da Marca | Pacing | Cuts/min | Transições |
|--------------|--------|----------|------------|
| Energético | Fast | 15-20 | Quick cuts, whip pans |
| Calmo | Slow | 6-8 | Dissolves, fades |
| Profissional | Measured | 10-12 | Clean cuts |
| Premium | Deliberate | 8-10 | Elegant transitions |
| Jovem | Dynamic | 12-15 | Jump cuts, zooms |

### 3. Personalidade → Movimento de Câmera

| Personalidade | Camera Style |
|---------------|--------------|
| Confiante | Steady, deliberate dolly |
| Inovador | Dynamic tracking, FPV |
| Tradicional | Static, classical framing |
| Ousado | Dutch angles, dramatic moves |
| Acessível | Handheld, organic |
| Premium | Smooth crane, orbit |

### 4. Valores → Iluminação e Atmosfera

| Valor | Tradução Visual |
|-------|-----------------|
| Transparência | Bright, clean, high-key |
| Confiança | Warm, golden, stable |
| Inovação | Cool tech, neon accents |
| Tradição | Natural, warm, soft |
| Exclusividade | Low-key, dramatic shadows |
| Sustentabilidade | Natural light, green tones |

---

## Sistema de Tradução

### Input: Brand Profile
```json
{
  "nome": "CODEXA",
  "cores": {
    "primaria": "#D4AF37",
    "secundaria": "#1a1a2e",
    "acento": "#ffffff"
  },
  "tom": "profissional, inovador, premium",
  "valores": ["automação", "eficiência", "tecnologia"],
  "personalidade": "confiante, futurista, acessível"
}
```

### Output: Video Style Guide
```json
{
  "color_grading": {
    "dominant": "golden warm tones",
    "shadows": "deep navy blue",
    "highlights": "clean white accents"
  },
  "lighting": {
    "key": "warm golden from side",
    "fill": "subtle cool blue",
    "rim": "strong golden edge light",
    "mood": "premium tech"
  },
  "camera": {
    "movement": "smooth deliberate",
    "style": "professional with innovation touches",
    "angles": "eye level, occasional low angle for power"
  },
  "pacing": {
    "tempo": "measured but modern",
    "cuts_per_minute": 10,
    "transitions": "clean cuts, occasional smooth zooms"
  },
  "atmosphere": {
    "mood": "confident, futuristic, accessible",
    "environment": "modern tech, clean lines",
    "energy": "controlled dynamism"
  }
}
```

---

## Templates por Arquétipo de Marca

### Tech/Inovação
```
Camera: Smooth tracking with FPV elements
Lighting: Cool blue base with neon accents, high-tech glow
Color: Blue-purple spectrum, clean whites
Pacing: Modern, dynamic but controlled
Transitions: Smooth zooms, digital transitions
Keywords: "futuristic tech aesthetic, holographic elements, neon accent lighting, clean modern lines, 4K quality"
```

### Premium/Luxo
```
Camera: Deliberate crane movements, slow orbit
Lighting: Low-key dramatic, golden accents, strong rim
Color: Gold, black, subtle contrasts
Pacing: Slow, deliberate, elegant
Transitions: Smooth dissolves, elegant fades
Keywords: "luxury aesthetic, dramatic low-key lighting, golden accents on dark, premium quality, sophisticated atmosphere"
```

### Lifestyle/Bem-estar
```
Camera: Organic handheld, gentle movements
Lighting: Natural daylight, warm golden hour
Color: Warm naturals, soft pastels
Pacing: Relaxed, breathing room
Transitions: Soft dissolves, gentle fades
Keywords: "natural warm lighting, organic atmosphere, golden hour, soft diffused light, welcoming mood"
```

### Corporativo/Profissional
```
Camera: Steady, professional framing
Lighting: Clean, even, professional
Color: Neutral with brand accent
Pacing: Measured, confident
Transitions: Clean cuts
Keywords: "professional corporate lighting, clean modern office, confident atmosphere, balanced composition"
```

### Esportivo/Energia
```
Camera: Dynamic tracking, action shots
Lighting: High contrast, dramatic
Color: Bold, high saturation
Pacing: Fast, energetic
Transitions: Quick cuts, impact zooms
Keywords: "dynamic high-energy, dramatic contrast lighting, bold colors, action cinematography, intense atmosphere"
```

---

## Processo de Alinhamento

### Passo 1: Extrair Elementos da Marca
```
1. Identificar cores (hex → nome descritivo)
2. Identificar tom de voz
3. Identificar valores principais
4. Identificar personalidade
```

### Passo 2: Traduzir para Linguagem de Vídeo
```
1. Cores → Color grading description
2. Tom → Pacing e ritmo
3. Valores → Atmosfera e mood
4. Personalidade → Movimento de câmera
```

### Passo 3: Gerar Style Guide
```
1. Compilar lighting setup
2. Definir camera style
3. Estabelecer pacing
4. Listar keywords obrigatórios
```

### Passo 4: Aplicar aos Prompts
```
1. Injetar color grading em cada prompt
2. Aplicar lighting style consistente
3. Manter camera style definido
4. Incluir brand keywords
```

---

## Exemplo Completo: CODEXA

### Brand Profile
```
Nome: CODEXA
Tagline: "Cérebro IA para Sellers"
Cores: Dourado (#D4AF37), Navy (#1a1a2e), Branco
Tom: Profissional, Inovador, Acessível
Valores: Automação, Eficiência, Tecnologia
Personalidade: Confiante, Futurista, Premium mas Acessível
```

### Video Style Guide Gerado
```
COLOR GRADING:
- Dominant: "warm golden tones"
- Shadows: "deep navy blue"
- Highlights: "clean white"
- Transition: "from cold blue (problem) to warm gold (solution)"

LIGHTING:
- Key: "golden warm light, usually from side/back"
- Fill: "subtle cool ambient"
- Rim: "strong golden edge defining contours"
- Mood: "premium tech, confident, inviting"

CAMERA:
- Movement: "smooth confident dolly, occasional orbit"
- Style: "professional cinematography with modern touches"
- Angles: "eye level for connection, low angle for power moments"

PACING:
- Tempo: "measured but engaging"
- Cuts: 10-12 per minute
- Transitions: "clean cuts, smooth zooms for emphasis"

KEYWORDS OBRIGATÓRIOS:
"golden accent lighting", "premium tech aesthetic", "dark navy background",
"confident atmosphere", "modern professional", "warm optimistic mood"
```

### Prompt Alinhado
```
Slow dolly forward: Confident Brazilian entrepreneur at modern standing desk, reviewing holographic CODEXA dashboard with rising metrics. Dark navy office environment with warm golden accent lighting creating rim light on figure. Golden particles float subtly in air. Premium tech aesthetic, cinematic 4K quality, shallow depth of field. Warm optimistic atmosphere, professional but innovative mood.
```

---

## Checklist de Brand Alignment

Antes de finalizar prompts, verificar:

- [ ] Cores da marca presentes (lighting/grading)
- [ ] Tom refletido no pacing
- [ ] Valores expressos na atmosfera
- [ ] Personalidade no movimento de câmera
- [ ] Keywords de marca incluídos
- [ ] Consistência entre todos os shots
- [ ] Transição narrativa alinhada (problema→solução)

---

## Anti-Patterns

```
❌ Ignorar cores da marca
❌ Pacing inconsistente com tom
❌ Iluminação genérica sem personalidade
❌ Misturar estilos conflitantes
❌ Esquecer keywords de marca

✅ Cada shot reflete a marca
✅ Cores consistentes em toda narrativa
✅ Atmosfera alinhada com valores
✅ Camera style coerente
✅ Keywords de marca em todos os prompts
```

---

**Última atualização**: 2025-11-24
