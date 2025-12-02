# Pika 2.0/2.1 - Guia de Prompt Engineering

**Versão**: 2.0/2.1 (2025) | **Empresa**: Pika Labs | **Status**: Estabelecido

---

## Overview

Pika destaca-se em efeitos especiais, transformações e features únicas como Scene Ingredients. Excelente para edição criativa e efeitos visuais.

**Specs**:
- Duração: até 8 segundos (modo padrão)
- Resolução: até 1080p
- Destaque: Pikadditions, Pikaswaps, Pikatwists
- Especialidade: Efeitos, transformações, lip-sync

---

## Estrutura de Prompt

### Fórmula Básica
```
[Style] + [Subject] + [Action] + [Environment] + [Lighting] + [Camera]
```

### Características
- Ser específico e descritivo
- Incluir: estilo, ângulo, mood, sujeito, movimento
- Variação de prompt produz grandes diferenças

### Exemplo Completo
```
Dramatic close-up of a confident entrepreneur in a neon-lit modern office, warm golden light reflecting off glass surfaces, wind from AC gently moving hair, slow-motion effect. Camera slowly pushes forward, shallow depth of field, cinematic 4K quality.
```

---

## Features Exclusivas

### Scene Ingredients
Decomponha vídeos em componentes editáveis:
- Backgrounds customizáveis
- Posicionamento de objetos
- Interações de personagens

```
"Only two elements in frame: floating product on left, brand logo on right, pure gradient background"
```

### Pikadditions
Adicione elementos a vídeos existentes:
```
"Add a glowing blue holographic interface floating beside the person"
"Add floating particles of golden light around the product"
```

### Pikaswaps
Substitua elementos:
```
"Replace the laptop with a futuristic holographic display"
"Replace the plain background with a dynamic cityscape"
```

### Pikatwists
Transformações surpreendentes no final:
```
"At the end, the product transforms into golden particles and reforms"
"At the end, the scene smoothly transitions to animated illustration style"
```

---

## Chained Prompts (Storytelling)

### Narrativa Sequencial
```
"A stressed entrepreneur stares at screen > light begins to glow from monitor > CODEXA interface appears > entrepreneur smiles with relief"
```

### Multi-Scene
```
"Scene 1: Dark office, declining graphs
> Scene 2: Discovery moment, warm light emerges
> Scene 3: Success, rising metrics, confident smile"
```

---

## Camera Commands

### Movimentos
```
--camera pan right
--camera pan left
--camera zoom in
--camera zoom out
--camera rotate
--camera tilt up
--camera tilt down
```

### Exemplo com Comando
```
"Premium headphones rotating slowly on white pedestal, studio lighting creating soft shadows" --camera zoom in
```

---

## Best Practices

### 1. Especificidade Visual
```
✅ "Dramatic close-up of a woman in a neon-lit alley, wind blowing her hair, slow-motion"
❌ "Video of a woman in an alley"
```

### 2. Definir Elementos com Precisão
```
✅ "Only two characters: entrepreneur on left, client on right"
❌ "Some people talking" (pode gerar número aleatório)
```

### 3. Natural Pacing
Para clips mais longos, estruture início-meio-fim:
```
"Beginning: Product appears from darkness
Middle: Slow rotation revealing features
End: Logo materializes beside product"
```

### 4. Reference Images
- Use imagens limpas e bem iluminadas
- Até 20MB suportado
- Match ação do prompt com imagem

---

## Estilos que Funcionam

### Cinematográficos
```
"cinematic shot"
"dramatic lighting"
"slow-motion effect"
"4K ultra-realistic"
"shallow depth of field"
"anamorphic lens flare"
```

### Artísticos
```
"Pixar-style 3D animation"
"film noir aesthetic"
"cyberpunk neon"
"minimalist modern"
"surrealist dreamscape"
```

### Efeitos
```
"particle effects"
"holographic elements"
"glowing rim light"
"motion blur"
"light rays"
```

---

## Casos de Uso E-commerce

### Product Launch
```
Cinematic product reveal: Premium [product] materializes from golden particles in center of frame, dramatic spot lighting, camera slowly orbits as product solidifies. Dark gradient background, luxury aesthetic, 4K quality. At the end, brand logo appears with subtle glow.
```

### Feature Demo com Pikadditions
```
Base: "Close-up of smartphone on modern desk, soft studio lighting"
Add: "Add floating holographic icons showing app features around the phone"
Add: "Add subtle particle effects connecting the icons"
```

### Brand Story com Pikatwists
```
Modern entrepreneur working at minimalist desk, golden hour light through windows, confident expression while reviewing dashboard on monitor. Smooth camera push forward. At the end, scene smoothly transitions to stylized illustration maintaining the same composition.
```

### Transformation com Pikaswaps
```
Base: "Entrepreneur at cluttered desk looking stressed, cold blue lighting, declining graphs on monitor"
Swap: "Replace declining graphs with rising green metrics"
Swap: "Replace cold blue lighting with warm golden glow"
```

### Dynamic CTA
```
Dramatic close-up of glowing CTA button pulsing with energy, "COMEÇAR AGORA" text, golden particles orbiting, dark premium background. Camera pushes in dramatically. At the end, button expands to fill frame with brand logo reveal.
```

---

## Image-to-Video

### Requisitos
- Imagens high-res para melhor resultado
- Composição clara sem elementos confusos
- Boa iluminação na imagem base

### Prompt I2V
```
[Descrição do que acontece a partir da imagem estática]
"The person in the image turns to face camera and smiles naturally"
"The product begins to slowly rotate, revealing different angles"
```

### Combinando com Features
```
Image: [Foto de produto]
Prompt: "Product begins floating and rotating"
Addition: "Add holographic feature labels appearing"
Twist: "At end, product dissolves into logo"
```

---

## Pika 2.1 (Mais Recente)

### Melhorias
- Maior coerência entre frames
- Menos glitches
- Melhor estabilidade temporal
- Prompt alignment mais preciso
- Motion mais natural

---

## Templates Rápidos

### Tech
```
Cinematic: [tech product] floating in futuristic dark environment, holographic UI elements orbiting, blue-purple neon accents, camera slowly orbits. Premium tech aesthetic, 4K. --camera zoom in
```

### Fashion
```
Dramatic: [fashion item] on confident model, fabric catching dramatic lighting, editorial photography style, slow-motion fabric movement. At the end, frame freezes and brand logo appears.
```

### Lifestyle
```
Warm cinematic: [lifestyle product] in use by [person description], natural golden hour lighting, genuine emotion, shallow depth of field. Camera gently pushes in revealing details.
```

### Abstract/Brand
```
Surreal: Brand logo [logo description] materializing from swirling [brand colors] particles, cosmic dark background, ethereal glow, dramatic reveal. At the end, tagline appears below.
```

---

## Referências

- [Pika AI - Official Prompt Guide](https://pikartai.com/prompt/)
- [Pika Labs - Prompting Guide](https://pikalabsai.org/pika-labs-prompting-guide/)
- [Pika AI - Text to Video](https://pikartai.com/pika-labs-ai-text-to-video/)
- [Pika AI 2.0 Features](https://pikartai.com/pika-2-0/)
- [Pika AI 2.1 Updates](https://pikartai.com/pika-2-1/)

---

**Última atualização**: 2025-11-24
