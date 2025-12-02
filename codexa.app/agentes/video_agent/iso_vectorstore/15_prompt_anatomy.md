# Anatomia do Prompt de Vídeo AI

**Guia Universal** - Estrutura que funciona em todas as plataformas

---

## Fórmula Universal

```
[Camera + Movement] + [Subject + Description] + [Action] + [Environment] + [Lighting] + [Style] + [Audio]*
```

*Audio apenas para plataformas com suporte nativo (Veo3, Sora2)

---

## Os 7 Elementos Essenciais

### 1. CAMERA (Como vemos)
Define perspectiva e movimento visual.

```
Ângulo: low angle, high angle, eye level, overhead, dutch angle
Movimento: dolly in/out, pan left/right, tracking, crane, static
Lens: wide angle, close-up, macro, telephoto
Framing: wide shot, medium shot, close-up, extreme close-up
```

**Exemplo**:
```
"Low angle dolly forward, 35mm lens, medium shot"
```

### 2. SUBJECT (Quem/O que)
O foco principal da cena.

```
Pessoa: descrição física, roupas, expressão, idade
Produto: nome, características, material, cor
Objeto: descrição detalhada
```

**Exemplo**:
```
"A confident Brazilian entrepreneur, 30s, wearing navy blazer and white shirt"
"Premium wireless earbuds in matte black finish"
```

### 3. ACTION (O que acontece)
O movimento ou ação do sujeito.

```
Movimento: walking, rotating, floating, gesturing
Transição: appearing, transforming, dissolving
Interação: typing, speaking, demonstrating
```

**Exemplo**:
```
"slowly rotating 360 degrees"
"gestures confidently toward holographic dashboard"
"transforms from stressed to confident expression"
```

### 4. ENVIRONMENT (Onde)
O contexto espacial da cena.

```
Local: office, studio, outdoor, abstract
Elementos: furniture, props, background
Atmosfera: clean, busy, minimalist, futuristic
```

**Exemplo**:
```
"modern glass-walled office with city skyline visible"
"pure white studio environment"
"futuristic tech lab with holographic displays"
```

### 5. LIGHTING (Como ilumina)
Define mood e qualidade visual.

```
Tipo: natural, studio, dramatic, soft
Direção: front, back, rim, side
Temperatura: warm (golden), cool (blue), neutral
Mood: bright, moody, high-key, low-key
```

**Exemplo**:
```
"warm golden hour light streaming through windows"
"dramatic rim lighting on dark background"
"soft studio lighting with subtle shadows"
```

### 6. STYLE (Estética)
Qualificadores de qualidade e estilo.

```
Qualidade: 4K, cinematic, professional, high-end
Estética: minimal, luxury, tech, editorial
Efeitos: shallow depth of field, motion blur, lens flare
Referência: shot on 35mm, Pixar-style, film noir
```

**Exemplo**:
```
"cinematic 4K quality, shallow depth of field"
"luxury editorial aesthetic, anamorphic lens"
"Pixar-style 3D animation, vibrant colors"
```

### 7. AUDIO (O que ouvimos) *
*Apenas Veo3 e Sora2

```
Dialogue: Character says: "[text]"
SFX: specific sound effects
Ambient: background atmosphere
Music: style and mood of score
```

**Exemplo**:
```
"Character says: 'Automatize seu negócio' (no subtitles)"
"Sound effects: satisfying click, subtle whoosh"
"Ambient: quiet office atmosphere with distant traffic"
```

---

## Estruturas por Plataforma

### Veo 3 (Google)
```
[Camera movement]: [Establishing scene]. [Subject description]. [Action]. [Lighting]. [Style]. [Audio].
```

### Sora 2 (OpenAI)
```
LOOK: [visual style, color grade]
CAMERA: [lens, movement, angle]
LIGHTING: [key, fill, mood]
SOUNDSCAPE: [ambient, sfx, music]
ACTION: [subject movement, timing]
```

### Kling 1.6
```
[Subject], [subject description], [subject movement], [scene]. [Scene description]. [Camera, lighting, atmosphere].
```

### Hailuo/MiniMax
```
[Camera Shot + Motion] + [Subject + Description] + [Action] + [Scene + Description] + [Lighting] + [Style/Mood]
```

### Runway Gen-3
```
[camera movement]: [establishing scene]. [additional details].
```

### Pika 2.0
```
[Style] + [Subject] + [Action] + [Environment] + [Lighting] + [Camera]
```

---

## Ordem de Prioridade

A maioria das AIs prioriza elementos no **início** do prompt:

```
1º - O mais importante (camera ou subject principal)
2º - Ação principal
3º - Contexto/ambiente
4º - Iluminação e estilo
5º - Detalhes adicionais
```

**Regra**: Coloque o elemento mais crítico primeiro.

---

## Níveis de Detalhe

### Básico (iniciante)
```
A product rotating on white background, studio lighting, 4K quality.
```

### Intermediário
```
Slow orbit shot: A premium wireless headphone floating and rotating slowly against pure white background, soft studio lighting creating subtle shadows, shallow depth of field, 4K cinematic quality.
```

### Avançado
```
Smooth 360 orbit, 85mm telephoto lens: Premium wireless headphone in matte black finish floating at eye level, rotating slowly revealing design details from all angles. Pure white seamless studio background. Soft key light from upper left, subtle fill from right, creating dimensional shadows. Motion blur enabled for smooth rotation. Cinematic 4K quality, shallow depth of field isolating product.
```

---

## Templates Universais

### Product Showcase
```
[Camera: slow orbit/push in]: [Product name] in [finish/color] [floating/displayed] against [background]. [Lighting setup] creating [shadow/highlight effect]. [Quality qualifiers], [depth of field].
```

### Person/Brand Story
```
[Camera movement], [lens]: [Person description] in [environment]. [Action/expression]. [Lighting description], [mood]. [Style qualifiers].
```

### Transformation/Before-After
```
[Transition type]: [Initial state description]. [Transformation action]. [Final state description]. [Lighting transition]. [Style].
```

### CTA/Urgency
```
[Dynamic camera]: [CTA element description], [animation/pulsing effect]. [Text content]. [Background]. [Accent lighting]. [Energy level].
```

---

## Checklist de Prompt

Antes de submeter, verifique:

- [ ] Camera definida (movimento + ângulo)
- [ ] Sujeito claramente descrito
- [ ] Ação específica (não vaga)
- [ ] Ambiente/contexto
- [ ] Iluminação especificada
- [ ] Estilo/qualidade incluídos
- [ ] Prompt em inglês
- [ ] Comprimento adequado (20-500 chars por plataforma)
- [ ] Sem negações ("don't", "no X")
- [ ] Um movimento principal de câmera

---

## Anti-Patterns (O que evitar)

```
❌ "A nice video of a product"
❌ "The camera doesn't move"
❌ "Someone doing something"
❌ "Beautiful lighting"
❌ "High quality"

✅ "Slow dolly forward: Premium sneaker rotating..."
✅ "Static locked shot on tripod"
✅ "Confident entrepreneur gestures toward dashboard"
✅ "Warm golden hour rim lighting from behind"
✅ "Cinematic 4K, shallow depth of field, 35mm film look"
```

---

**Última atualização**: 2025-11-24
