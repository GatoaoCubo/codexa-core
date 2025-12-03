# 🎬 DIREÇÃO VISUAL: {{BRAND_NAME}} {{PRODUCT_TYPE}} - Linguagem Natural

**Versão**: 1.0.0 | **Duração**: 8-11 minutos
**Referência**: `VIDEO_LP_{{PRODUCT_TYPE}}.md`
**Tipo**: Visual Bible (Biblia Visual para Produção de Vídeo)
**Objetivo**: Guia completo de direção visual, câmera, iluminação e estilo

---

## 📋 ÍNDICE

1. [Camera Movements por Seção](#camera-movements-por-seção)
2. [Arco de Iluminação](#arco-de-iluminação)
3. [Breakdown Detalhado com Timecodes](#breakdown-detalhado-com-timecodes)
4. [Regras de Ouro para Câmera](#regras-de-ouro-para-câmera)
5. [Style Preset](#style-preset)
6. [Paleta de Cores](#paleta-de-cores)
7. [Notas Específicas para Plataformas](#notas-específicas-para-plataformas)

---

## 🎥 CAMERA MOVEMENTS POR SEÇÃO

### Tabela de Referência Rápida

| Seção | Tempo | Movimento Principal | Movimento Secundário | Mood Visual |
|-------|-------|---------------------|----------------------|-------------|
| **HOOK** | 00:00-00:40 | `slow zoom in` | Static holds | Impacto, prova imediata |
| **PROBLEMA** | 00:45-02:30 | `handheld shake` | `slow pan` | Caos, frustração, fragmentação |
| **SOLUÇÃO** | 02:30-04:30 | `dolly in` | `zoom out` | Clareza, alívio, simplicidade |
| **DEMO** | 04:30-07:00 | `slow pan down` | Static frames | Transparência, processo |
| **ESPECIALISTAS** | 07:00-08:30 | `orbit` | `dolly in` | Expertise, destilação |
| **DIFERENCIAL** | 08:30-10:00 | `handheld` → `static` | Transition | Dor → Alívio |
| **{{EASTER_EGG_NAME}}** | 09:45-10:00 | `medium shot, casual` | Cozy handheld | Humor, quebra de tom |
| **CTA** | 10:00-11:00 | `slow zoom in` | Static hold | Ação imediata, urgência |

### Descrição dos Movimentos

#### **Slow Zoom In**
- **Velocidade**: 10-15% por segundo
- **Uso**: Foco, atenção, dramatização
- **Quando**: Hook, outputs importantes, CTA

#### **Handheld Shake**
- **Intensidade**: Moderada (2-4% drift)
- **Uso**: Desconforto, caos, problema
- **Quando**: Problema, antes de "{{BRAND_NAME}} quebra"

#### **Dolly In**
- **Velocidade**: Suave (20-30% ao longo de 15s)
- **Uso**: Aproximação confiante
- **Quando**: Solução, especialistas

#### **Slow Pan**
- **Direção**: Esquerda → Direita (leitura natural)
- **Velocidade**: 5-10 segundos para varrer tela
- **Uso**: Exploração, listas, processo
- **Quando**: Demo, checklists

#### **Orbit**
- **Ângulo**: 45-90 graus ao redor do objeto
- **Velocidade**: 15-20 segundos para ciclo completo
- **Uso**: Visão holística, conexões
- **Quando**: Diagrama de agentes, especialistas

#### **Static Hold**
- **Duração**: 3-10 segundos
- **Uso**: Deixar mensagem respirar
- **Quando**: Frases de impacto, pausa dramática

---

## 💡 ARCO DE ILUMINAÇÃO

### Progressão Cromática

```
COLD BLUE           WARM NEUTRAL         GOLDEN
(Problema)      →   (Solução)        →   (CTA)
───────────────────────────────────────────────────
 {{PROBLEM_COLOR}}   {{NEUTRAL_COLOR}}    {{SUCCESS_COLOR}}
 harsh, high         soft, balanced       success glow
 contrast                                  warm, inviting
```

### Detalhamento por Fase

#### **FASE 1: COLD (00:00-02:30)**
- **Hook + Problema**
- **Temperatura**: 5500K-6500K (azul frio)
- **Contraste**: Alto (sombras duras)
- **Intensidade**: Média-baixa (opressivo)
- **Objetivo**: Desconforto, fragmentação
- **Referência visual**: Tela de computador tarde da noite, luz azul

#### **FASE 2: WARM (02:30-08:30)**
- **Solução + Demo + Especialistas**
- **Temperatura**: 4000K-5000K (branco neutro)
- **Contraste**: Médio (sombras suaves)
- **Intensidade**: Média-alta (clareza)
- **Objetivo**: Alívio, confiança, transparência
- **Referência visual**: Escritório iluminado naturalmente, manhã

#### **FASE 3: GOLDEN (08:30-11:00)**
- **Diferencial + CTA**
- **Temperatura**: 3000K-3500K (dourado quente)
- **Contraste**: Baixo (difusão suave)
- **Intensidade**: Alta (glow, aura)
- **Objetivo**: Sucesso, liberdade, ação
- **Referência visual**: Golden hour, pôr do sol, sensação de vitória

### Transições de Iluminação

| Transição | Timecode | Duração | Técnica |
|-----------|----------|---------|---------|
| COLD → WARM | 02:25-02:35 | 10s | Crossfade gradual |
| WARM → GOLDEN | 08:25-08:35 | 10s | Fade + color grade shift |
| GOLDEN → BLACK | 10:45-10:55 | 10s | Fade out com mantém rim light |

---

## 🎬 BREAKDOWN DETALHADO COM TIMECODES

### [00:00-00:40] HOOK - Uma Frase, Tudo Pronto

#### **00:00-00:05** Tela Preta, Cursor
```
VISUAL: Tela completamente preta
CAMERA: Static
LIGHTING: Low key, apenas cursor visível
COLOR: Monocromático (#000000 bg, #FFFFFF cursor)
AUDIO: Silêncio, depois som de teclado
```

#### **00:05-00:10** Texto Letra por Letra
```
VISUAL: "{{USER_INPUT_EXAMPLE}}"
CAMERA: Static, close-up no texto
LIGHTING: Spotlight no texto, background escuro
COLOR: #FFFFFF texto, #0A0A0A background
ANIMATION: Typing effect (0.1s por caractere)
AUDIO: Som de teclado mecânico
```

#### **00:10-00:20** Split: Input → Output
```
VISUAL: Tela dividida - esquerda input, direita progress bar
CAMERA: Static, balanced split screen
LIGHTING: Neutral, clean, sem sombras
COLOR: {{BG_LIGHT}} background, {{PRIMARY_COLOR}} progress bar
ANIMATION: Progress bar 0% → 100% (3s)
AUDIO: Som de processamento (sutil, sci-fi)
```

#### **00:20-00:30** Checkmarks Aparecendo
```
VISUAL: Lista de outputs com checkmarks surgindo
CAMERA: Slow zoom in (10% em 10s)
LIGHTING: Warm, soft spotlight
COLOR: {{SUCCESS_COLOR}} checkmarks, {{TEXT_PRIMARY}} texto
ANIMATION: Checkmarks surgem um por vez (0.8s interval)
AUDIO: "Ding" sutil a cada checkmark
```

#### **00:30-00:40** "{{TIME_SAVED}} / {{INPUT_SIMPLICITY}}"
```
VISUAL: Texto bold centralizado
CAMERA: Static hold
LIGHTING: High contrast, dramatic
COLOR: {{ACCENT_COLOR}} "{{TIME_SAVED}}", #FFFFFF "{{INPUT_SIMPLICITY}}"
ANIMATION: Fade in + scale pulse (1x → 1.05x → 1x)
AUDIO: Pausa silenciosa (deixa mensagem respirar)
```

---

### [00:45-02:30] PROBLEMA - Ferramentas Fragmentadas

#### **00:45-01:00** 8 Abas Navegador
```
VISUAL: Screenshot de navegador com 8 abas abertas
CAMERA: Slow pan right (esquerda → direita, 15s)
LIGHTING: Cold blue ({{PROBLEM_COLOR}}), harsh
COLOR: Desaturado (-20%), azul dominante
ANIMATION: Abas piscando (notificações falsas)
AUDIO: Clicks, notificações, caos sonoro
```

#### **01:00-01:20** Ícones Girando
```
VISUAL: Ícones de ferramentas ({{COMPETITOR_TOOLS}})
CAMERA: Handheld shake (intensidade 3/10)
LIGHTING: Flickering (simulação de instabilidade)
COLOR: {{PROBLEM_COLOR}} (frio), low saturation
ANIMATION: Ícones giram caoticamente, direções aleatórias
AUDIO: Whoosh sounds, caos
```

#### **01:20-01:40** Copiar/Colar
```
VISUAL: Animação de copiar texto → colar em outro app
CAMERA: Medium shot, alternando entre apps
LIGHTING: Cold, desaturado
COLOR: {{GRAY_MEDIUM}} (cinza dominante)
ANIMATION: Copy → Paste loop (3x em 20s)
AUDIO: Ctrl+C, Ctrl+V sounds
```

#### **01:40-02:00** Relógio Acelerando
```
VISUAL: Relógio digital acelerando (horas passando)
CAMERA: Zoom out (mostra mais contexto)
LIGHTING: Red warning light ({{ERROR_COLOR}})
COLOR: Vermelho dominante, alerta
ANIMATION: Time-lapse (1s = 1h no vídeo)
AUDIO: Ticking acelerado, tensão
```

#### **02:00-02:30** "{{PAIN_POINT_PHRASE}}"
```
VISUAL: Texto bold sobre background escuro
CAMERA: Static, centered
LIGHTING: Dark, dramatic, spotlight no texto
COLOR: {{ERROR_COLOR}} "{{PAIN_KEYWORD}}", #FFFFFF resto
ANIMATION: Fade in lento (2s)
AUDIO: Pausa dramática, silêncio após frase
```

---

### [02:30-04:30] SOLUÇÃO - O {{PRODUCT_TYPE}} em Linguagem Natural

#### **02:30-02:45** Interface Limpa
```
VISUAL: Interface do {{BRAND_NAME}} aparecendo
CAMERA: Slow dolly in (aproximação confiante)
LIGHTING: Transição COLD → WARM (10s fade)
COLOR: {{BG_LIGHT}} background, {{TEXT_PRIMARY}} texto
ANIMATION: Fade in + soft glow
AUDIO: Som de "reveal" positivo
```

#### **02:45-03:30** 4 Cards (Um a Um)
```
VISUAL: Menu de {{NUM_OPTIONS}} armas, surgindo uma por vez
CAMERA: Static, each card gets spotlight
LIGHTING: Soft highlight em cada card quando surge
COLOR:
  - {{OPTION_1_NAME}}: {{OPTION_1_COLOR}}
  - {{OPTION_2_NAME}}: {{OPTION_2_COLOR}}
  - {{OPTION_3_NAME}}: {{OPTION_3_COLOR}}
  - {{OPTION_4_NAME}}: {{OPTION_4_COLOR}}
ANIMATION: Cards surgem com slide up + fade in (1.5s cada)
AUDIO: "Pop" sutil a cada card
```

#### **03:30-03:45** Cursor Digitando
```
VISUAL: Close-up em input field, cursor digitando
CAMERA: Close-up, macro shot
LIGHTING: Warm, soft
COLOR: #FFFFFF input, {{PRIMARY_COLOR}} cursor piscando
ANIMATION: Typing effect realista (variação de velocidade)
AUDIO: Teclado mecânico, ritmo natural
```

#### **03:45-04:30** 4 Cards Lado a Lado
```
VISUAL: Visão completa dos {{NUM_OPTIONS}} comandos
CAMERA: Slow zoom out (reveal do todo)
LIGHTING: Balanced, uniform
COLOR: Accent colors mantidos, background neutro
ANIMATION: Subtle hover effects (cards ligeiramente elevam)
AUDIO: Música de fundo entra suave (uplifting)
```

---

### [04:30-07:00] DEMO - Demonstração Real

#### **04:30-05:00** Screencast Real
```
VISUAL: Gravação de tela do sistema executando
CAMERA: Static, fullscreen ou com frame sutil
LIGHTING: Neutral, clean
COLOR: UI original do sistema (não alterar)
ANIMATION: Real-time screen recording
AUDIO: Narração + sons do sistema
```

#### **05:00-05:40** Fases 1-2 Executando
```
VISUAL: Listas de tarefas sendo completadas (checkmarks)
CAMERA: Slow pan down (acompanha lista)
LIGHTING: Soft, neutral
COLOR: {{SUCCESS_COLOR}} checkmarks, {{SUCCESS_LIGHT}} progress bars
ANIMATION: Checkmarks surgem progressivamente
AUDIO: "Ding" a cada tarefa completa
```

#### **05:40-06:00** Bridge (Seta Conectando)
```
VISUAL: Seta conectando {{AGENT_1}} → {{AGENT_2}}
CAMERA: Zoom on arrow (foco no momento crítico)
LIGHTING: Accent light na seta
COLOR: {{COMBO_COLOR}} seta, pulse effect
ANIMATION: Arrow animates (draw + glow pulse)
AUDIO: "Whoosh" + conexão estabelecida
```

#### **06:00-06:40** Fases 4-5 Executando
```
VISUAL: Checklist de {{NUM_PHASES}} fases do {{AGENT_2}}
CAMERA: Slow pan down
LIGHTING: Soft green progress light
COLOR: {{SUCCESS_COLOR}} checkmarks, {{PRIMARY_COLOR}} current task highlight
ANIMATION: Progress bars + checkmarks
AUDIO: Continuation of "ding" sounds
```

#### **06:40-07:00** Score {{QUALITY_SCORE}}
```
VISUAL: Score de qualidade em destaque
CAMERA: Slow zoom in (emphasis)
LIGHTING: Golden glow ao redor do score
COLOR: {{ACCENT_COLOR}} score, {{SUCCESS_COLOR}} "{{READY_STATUS}}"
ANIMATION: Number count-up (0.00 → {{QUALITY_SCORE}} em 2s)
AUDIO: Success chime
```

---

### [07:00-08:30] ESPECIALISTAS - Conhecimento Destilado

#### **07:00-07:15** Diagrama Orbital
```
VISUAL: {{BRAND_NAME}} no centro, agentes orbitando
CAMERA: Slow orbit (45° em 15s)
LIGHTING: Warm, spotlight central
COLOR: {{BG_DARK}} background, {{PRIMARY_COLOR}} conexões
ANIMATION: Agentes orbitam (slow rotation)
AUDIO: Ambient, espacial
```

#### **07:15-07:30** Ícones Conhecimento
```
VISUAL: Ícones de {{KNOWLEDGE_SOURCES}}
CAMERA: Pan across (esquerda → direita)
LIGHTING: Soft spotlights em cada ícone
COLOR: Variado (cada ícone tem cor própria)
ANIMATION: Icons float in + subtle glow
AUDIO: "Chime" sutil a cada ícone
```

#### **07:30-07:45** Funil de Destilação
```
VISUAL: Funil gráfico (conhecimento → agentes)
CAMERA: Slow dolly in (aproximação do funil)
LIGHTING: Gradient light (topo frio → base quente)
COLOR: Gradient {{PRIMARY_COLOR}} → {{COMBO_COLOR}} → {{SUCCESS_COLOR}}
ANIMATION: Particle flow (conhecimento fluindo)
AUDIO: Flow sound effect
```

#### **07:45-08:15** 3 Cards Agentes
```
VISUAL: Três cards lado a lado ({{AGENT_1}}, {{AGENT_2}}, {{AGENT_3}})
CAMERA: Static, balanced composition
LIGHTING: Individual spotlights em cada card
COLOR:
  - {{AGENT_1}}: {{OPTION_1_COLOR}}
  - {{AGENT_2}}: {{OPTION_2_COLOR}}
  - {{AGENT_3}}: {{OPTION_4_COLOR}}
ANIMATION: Cards reveal (stagger 0.5s cada)
AUDIO: "Pop" a cada card
```

#### **08:15-08:30** "Você no Centro"
```
VISUAL: User silhouette no centro, agentes ao redor
CAMERA: Slow zoom out (revela contexto completo)
LIGHTING: Spotlight no user, soft light nos agentes
COLOR: {{ACCENT_COLOR}} user (destaque), {{GRAY_MEDIUM}} agentes
ANIMATION: Conexões pulsam (user → agentes)
AUDIO: Uplifting, empowering
```

---

### [08:30-10:00] DIFERENCIAL - Escale Sem Risco

#### **08:30-08:45** Treinando Funcionário
```
VISUAL: Pessoa treinando outra, frustração visível
CAMERA: Handheld (instabilidade)
LIGHTING: Harsh, cold ({{PROBLEM_COLOR}})
COLOR: Desaturado, cinza dominante
ANIMATION: Subtle shake
AUDIO: Background noise, frustração
```

#### **08:45-09:00** Reclamação + $
```
VISUAL: Notificação de reclamação, $ sumindo
CAMERA: Close-up (emphasis na dor)
LIGHTING: Red warning ({{ERROR_COLOR}})
COLOR: Vermelho alerta
ANIMATION: Notificação pop-up, $ desaparece
AUDIO: Alert sound, negativo
```

#### **09:00-09:15** Ciclo Vicioso
```
VISUAL: Diagrama circular (contratar → treinar → sair)
CAMERA: Slow orbit (seguindo o ciclo)
LIGHTING: Cold, desaturado
COLOR: {{GRAY_MEDIUM}} (cinza, sem esperança)
ANIMATION: Arrows animam em loop
AUDIO: Loop repetitivo (reforça ciclo)
```

#### **09:15-09:30** "{{BRAND_NAME}} Quebra o Ciclo"
```
VISUAL: Texto bold, ciclo se quebrando
CAMERA: Static, centered
LIGHTING: Transição WARM → GOLDEN (começa aqui)
COLOR: {{ACCENT_COLOR}} "{{BRAND_NAME}}", {{ERROR_COLOR}} "quebra" (ação)
ANIMATION: Ciclo se parte (break effect)
AUDIO: "Break" sound, dramático
```

#### **09:30-09:45** {{TARGET_AUDIENCE}} Usando
```
VISUAL: Grupo de pessoas usando {{BRAND_NAME}}, felizes
CAMERA: Wide shot (mostra contexto social)
LIGHTING: Golden, happy ({{ACCENT_COLOR}} dominant)
COLOR: Saturado, quente, acolhedor
ANIMATION: Subtle movements (pessoas interagindo)
AUDIO: Uplifting, light background music
```

#### **09:45-10:00** {{EASTER_EGG_NAME}}
```
VISUAL: {{EASTER_EGG_SCENE}}
CAMERA: Medium casual (cozy handheld, leve)
LIGHTING: Cozy warm, soft ({{WARNING_COLOR}})
COLOR: Tons quentes, ambiente aconchegante
ANIMATION: {{EASTER_EGG_ANIMATION}}
AUDIO: {{EASTER_EGG_AUDIO}}
EASTER EGG: Nome "{{EASTER_EGG_DETAIL}}" aparece sutil na tela
```

---

### [10:00-11:00] CTA - Comece Agora

#### **10:00-10:15** 4 Comandos Recap
```
VISUAL: Recap dos {{NUM_OPTIONS}} comandos, limpo e direto
CAMERA: Static, centered
LIGHTING: Clean bright (#FFFFFF)
COLOR: Accent colors mantidos ({{OPTION_1_COLOR}}, {{OPTION_2_COLOR}}, {{OPTION_3_COLOR}}, {{OPTION_4_COLOR}})
ANIMATION: Cards surgem rapidamente (0.3s cada)
AUDIO: Quick "pop" sounds
```

#### **10:15-10:30** Botão Pulsando
```
VISUAL: Botão "{{CTA_TEXT}}" em destaque
CAMERA: Slow zoom in (foco total)
LIGHTING: CTA green glow ({{SUCCESS_COLOR}})
COLOR: {{SUCCESS_COLOR}} botão, #FFFFFF texto
ANIMATION: Pulse (1x → 1.1x → 1x, loop 2s)
AUDIO: Urgência sutil (não agressivo)
```

#### **10:30-10:45** "{{CTA_BENEFIT}}"
```
VISUAL: Texto de benefícios abaixo do botão
CAMERA: Static hold
LIGHTING: Trust blue ({{PRIMARY_COLOR}})
COLOR: {{PRIMARY_COLOR}} "{{CTA_BENEFIT}}", {{GRAY_MEDIUM}} "{{CTA_DETAIL}}"
ANIMATION: Fade in suave
AUDIO: Música de fundo continua
```

#### **10:45-10:55** Fade to Black
```
VISUAL: Fade gradual para preto
CAMERA: Static, mantém composição
LIGHTING: Dim out gradual
COLOR: Fade to #000000
ANIMATION: 10s fade out
AUDIO: Música diminui volume gradualmente
```

#### **10:55-11:00** Logo + Tagline
```
VISUAL: Logo {{BRAND_NAME}} centralizado, tagline abaixo
CAMERA: Static, centered
LIGHTING: Subtle golden rim light (aura)
COLOR: #FFFFFF logo, {{ACCENT_COLOR}} rim light
ANIMATION: Logo soft glow pulse
AUDIO: Final chord (resolution)
EASTER EGG: Tagline {{TAGLINE_REFERENCE}} sutil
```

---

## 📐 REGRAS DE OURO PARA CÂMERA

### Princípios de Movimento

1. **Um Movimento Principal por Shot**
   - Nunca combine zoom + pan no mesmo take
   - Se precisar de dois movimentos, faça em shots separados
   - Exceção: Transições entre seções

2. **Velocidade = Qualidade**
   - Movimentos lentos = maior qualidade percebida
   - Regra: 10-15 segundos mínimo para completar movimento
   - Fast motion apenas para humor ou caos intencional

3. **Direção de Leitura**
   - Pan sempre esquerda → direita (leitura natural)
   - Exceção: Quando mostrando "retrocesso" ou "erro"

4. **Static Holds Estratégicos**
   - Toda frase de impacto precisa de 3-5s de hold
   - Permite audiência processar informação
   - Não tenha medo do silêncio/pausa

5. **Transições Invisíveis**
   - Crossfade entre seções: 1-2s
   - Cut direto apenas para impacto dramático
   - Match cut quando possível (elementos visuais conectam)

### Composição por Tipo de Conteúdo

#### **Texto/Legenda**
```
RULE: Lower third ou central (nunca top)
CAMERA: Static (deixa texto ser o movimento)
TIMING: 1s por cada 3 palavras + 1s buffer
```

#### **Interface/Screencast**
```
RULE: Fullscreen ou frame sutil (não distrair)
CAMERA: Slow pan/zoom apenas para guiar atenção
TIMING: Real-time ou 1.2x speed (nunca > 1.5x)
```

#### **Diagrams/Infográficos**
```
RULE: Reveal progressivo (não mostrar tudo de uma vez)
CAMERA: Orbit ou dolly in para visão 360°
TIMING: 2-3s por elemento visual
```

#### **People/Characters**
```
RULE: Rule of thirds (não centralizar sempre)
CAMERA: Medium shot (MS) como padrão
TIMING: Natural (não acelerar)
```

### Anti-Patterns (Evitar)

❌ **Zoom excessivo**: > 50% em um shot
❌ **Handheld sem propósito**: Usar apenas para desconforto intencional
❌ **Pan rápido**: < 5s para atravessar tela (causa desconforto)
❌ **Movimentos simultâneos**: Zoom + Pan + Dolly = nauseante
❌ **Static em ação**: Se há movimento no conteúdo, câmera pode/deve acompanhar

---

## 🎨 STYLE PRESET

### Tone & Pacing

**Tone Progression**:
```
PROBLEMA (Serious)  →  SOLUÇÃO (Confident)  →  DIFERENCIAL (Playful)  →  CTA (Urgent)
     Dark, tense          Bright, clear           Warm, human           Energetic
```

**Pacing**:
```
00:00-00:40  HOOK          → FAST (grab attention)
00:45-02:30  PROBLEMA      → MEDIUM (build tension)
02:30-04:30  SOLUÇÃO       → SLOW (explain clearly)
04:30-07:00  DEMO          → MEDIUM (show process)
07:00-08:30  ESPECIALISTAS → SLOW (establish authority)
08:30-10:00  DIFERENCIAL   → MEDIUM-FAST (excitement)
10:00-11:00  CTA           → FAST (urgency)
```

### Music Arc

**Track Layers**:

1. **Layer 1: Ambient Base** (sempre presente)
   - Drone sutil, low frequency
   - 00:00-11:00 continuous

2. **Layer 2: Melody** (varia por seção)
   - 00:00-00:40: Minimal, sparse
   - 00:45-02:30: Tense, minor key
   - 02:30-04:30: Uplifting, major key
   - 04:30-07:00: Neutral, productive
   - 07:00-08:30: Epic, authoritative
   - 08:30-10:00: Warm, playful ({{EASTER_EGG_NAME}}!)
   - 10:00-11:00: Energetic, call to action

3. **Layer 3: Percussion** (adiciona energia)
   - 00:00-02:30: Ausente
   - 02:30-04:30: Light, subtle
   - 04:30-07:00: Steady, building
   - 07:00-08:30: Epic drums
   - 08:30-11:00: Full rhythm

**Music References**:
- Problema: "Anxious" by Incompetech
- Solução: "Inspired" by Incompetech
- Demo: "Cipher" by Incompetech
- Especialistas: "Armada" by Incompetech
- Diferencial: "Wallpaper" by Incompetech
- CTA: "Laser Groove" by Incompetech

### Audio Mix Guidelines

```
NARRATION: -3dB (sempre prioridade)
MUSIC:     -12dB (background)
SFX:       -6dB (pontual, não constante)
SILENCE:   Strategic (pausa dramática)
```

**Dynamic Range**:
- Compress narration: 3:1 ratio
- Limit peaks: -1dB ceiling
- Normalize: -16 LUFS (YouTube standard)

---

## 🎨 PALETA DE CORES

### Color Progression Timeline

```
00:00-02:30  COLD PHASE    {{PROBLEM_COLOR}} → {{GRAY_MEDIUM}}
02:30-08:30  WARM PHASE    {{NEUTRAL_COLOR}} → {{BG_LIGHT}}
08:30-11:00  GOLDEN PHASE  {{ACCENT_COLOR}} → {{WARNING_COLOR}}
```

### Paleta Completa por Elemento

#### **Background Colors**
```css
--bg-cold:    #0A0A0A;  /* Problema */
--bg-warm:    {{BG_LIGHT}};  /* Solução */
--bg-golden:  {{BG_GOLDEN}};  /* CTA */
--bg-black:   #000000;  /* Hook/Fade */
```

#### **Accent Colors (Agents)**
```css
--agent-1:  {{OPTION_1_COLOR}};  /* {{OPTION_1_NAME}} */
--agent-2:  {{OPTION_2_COLOR}};  /* {{OPTION_2_NAME}} */
--agent-3:  {{OPTION_3_COLOR}};  /* {{OPTION_3_NAME}} */
--agent-4:  {{OPTION_4_COLOR}};  /* {{OPTION_4_NAME}} */
```

#### **Semantic Colors**
```css
--success:   {{SUCCESS_COLOR}};  /* Checkmarks, scores */
--warning:   {{WARNING_COLOR}};  /* Alerts, attention */
--error:     {{ERROR_COLOR}};  /* Problems, pain points */
--info:      {{PRIMARY_COLOR}};  /* Information, neutral */
```

#### **Text Colors**
```css
--text-primary:    {{TEXT_PRIMARY}};  /* Main text */
--text-secondary:  {{GRAY_MEDIUM}};  /* Supporting text */
--text-inverse:    #FFFFFF;  /* On dark bg */
--text-emphasis:   {{ACCENT_COLOR}};  /* Highlights */
```

### Color Grading Presets

#### **Preset 1: COLD (Problema)**
```
Temperature:  6500K (cool)
Tint:         +5 (magenta)
Saturation:   -20% (desaturado)
Contrast:     +15 (harsh)
Highlights:   -10
Shadows:      +5 (lift blacks slightly)
```

#### **Preset 2: WARM (Solução)**
```
Temperature:  4500K (neutral warm)
Tint:         0 (balanced)
Saturation:   0% (natural)
Contrast:     0 (balanced)
Highlights:   0
Shadows:      0
```

#### **Preset 3: GOLDEN (CTA)**
```
Temperature:  3200K (warm)
Tint:         -3 (green)
Saturation:   +10% (vibrant)
Contrast:     -5 (soft)
Highlights:   +10 (glow)
Shadows:      +10 (lift, open)
```

### Gradient Usage

#### **Background Gradients**
```css
/* Transição Problema → Solução */
.transition-cold-warm {
  background: linear-gradient(
    180deg,
    {{PROBLEM_COLOR}} 0%,    /* Cold blue */
    {{NEUTRAL_COLOR}} 100%   /* Warm neutral */
  );
}

/* Transição Solução → CTA */
.transition-warm-golden {
  background: linear-gradient(
    180deg,
    {{BG_LIGHT}} 0%,    /* Warm light */
    {{BG_GOLDEN}} 100%   /* Golden */
  );
}

/* Funil de Destilação (Especialistas) */
.distillation-funnel {
  background: linear-gradient(
    90deg,
    {{PRIMARY_COLOR}} 0%,    /* Blue (knowledge) */
    {{COMBO_COLOR}} 50%,   /* Purple (process) */
    {{SUCCESS_COLOR}} 100%   /* Green (agents) */
  );
}
```

---

## 🤖 NOTAS ESPECÍFICAS PARA PLATAFORMAS

### Se Usando Runway Gen-3 / Pika Labs

#### **Prompt Structure**
```
[Camera movement], [subject], [lighting], [style]
cinematic, 4K, professional, [mood]
```

#### **Exemplos por Seção**

**HOOK (00:00-00:40)**:
```
Slow zoom in, computer screen with code output,
soft spotlight, clean modern UI, cinematic, 4K,
professional, impactful
```

**PROBLEMA (00:45-02:30)**:
```
Handheld shake, multiple browser tabs chaos,
harsh blue lighting, desaturated, cinematic, 4K,
professional, tense frustration
```

**SOLUÇÃO (02:30-04:30)**:
```
Dolly in, clean interface with {{NUM_OPTIONS}} option cards,
soft warm lighting, bright balanced, cinematic, 4K,
professional, confident clarity
```

**{{EASTER_EGG_NAME}} (09:45-10:00)**:
```
Medium shot casual, {{EASTER_EGG_SCENE}},
cozy warm lighting, soft golden, cinematic, 4K,
natural, playful humorous
```

#### **Settings Recomendadas**
- **Resolution**: 1920x1080 (4K se disponível)
- **Frame Rate**: 24fps (cinematic) ou 30fps (smooth)
- **Duration**: 5-10s clips (montar depois)
- **Seed**: Fixar para consistência entre clips relacionados
- **Motion**: 3-5 (slow) para movimentos suaves

### Se Usando After Effects / Premiere

#### **Project Settings**
```
Resolution:   1920x1080 (Full HD)
Frame Rate:   24fps ou 30fps
Color Space:  Rec. 709 (YouTube standard)
Audio:        48kHz, 16-bit stereo
```

#### **Plugins Recomendados**
- **Color Grading**: Lumetri Color / FilmConvert
- **Camera Movement**: 3D Camera Tracker
- **Text Animation**: TypeMonkey / TextEvo
- **Particles**: Particular (funil de destilação)
- **Glow Effects**: Optical Flares / Saber

#### **Render Settings**
```
Format:     H.264
Preset:     YouTube 1080p Full HD
Bitrate:    CBR 16 Mbps
Audio:      AAC, 320 kbps
```

### Se Usando Figma + Rive (Motion Graphics)

#### **Workflow**
1. Design all screens in Figma
2. Export assets (SVG para vetores, PNG para rasters)
3. Import para Rive
4. Animate com state machines
5. Export video ou embed

#### **Animation Timing**
```javascript
// Exemplo: Card reveal
{
  ease: "easeOutCubic",
  duration: 1.5,  // seconds
  delay: 0.3      // stagger
}
```

### Screencast (Demo Real)

#### **Software Recomendado**
- **Windows**: OBS Studio (grátis)
- **macOS**: ScreenFlow ou Camtasia

#### **Settings**
```
Resolution:  1920x1080 (match output)
FPS:         30fps (smoother para UI)
Cursor:      Show with highlight
Audio:       Capture system + mic
```

#### **Post-Processing**
- Crop para aspect ratio 16:9
- Add subtle zoom/pan em pós (não durante gravação)
- Speed up 1.2x se demo muito longa
- Add callouts (arrows, highlights) em momentos-chave

---

## 📋 CHECKLIST FINAL (PRÉ-PRODUÇÃO)

### Camera
- [ ] Camera movements definidos por seção
- [ ] Transições entre seções planejadas
- [ ] Static holds identificados (frases de impacto)
- [ ] Composição respeitando rule of thirds

### Lighting
- [ ] Arco COLD → WARM → GOLDEN implementado
- [ ] Transições de temperatura de cor suaves (10s)
- [ ] Lighting keys definidos por timecode
- [ ] Color grading presets preparados

### Color
- [ ] Paleta de cores por fase verificada
- [ ] Accent colors por agente consistentes
- [ ] Gradientes preparados (funil, transições)
- [ ] Semantic colors aplicados (success, error, etc)

### Audio
- [ ] Music arc com 3 layers definido
- [ ] SFX marcados por timecode
- [ ] Mix levels planejados (-3dB narração, -12dB música)
- [ ] Pausa dramática identificadas (silêncio estratégico)

### Style
- [ ] Tone progression confirmada (Serious → Playful → Urgent)
- [ ] Pacing ajustado por seção (Fast → Medium → Slow)
- [ ] Easter eggs posicionados ({{EASTER_EGG_NAME}}, {{TAGLINE_REFERENCE}})
- [ ] Humor balance checado (não excessivo)

### Platform-Specific
- [ ] Prompts para AI video gerados (se aplicável)
- [ ] Project settings configurados (AE/Premiere)
- [ ] Screencast software testado
- [ ] Export settings verificados (YouTube 1080p)

---

## 🔗 REFERÊNCIAS

### Documentos Relacionados
- **Roteiro Completo**: `VIDEO_LP_{{PRODUCT_TYPE}}.md`
- **Trinity Pattern**: `.claude/commands/prime.md`
- **Direção de Agentes**: `{{AGENT_PRIME_PATH}}`

### Inspirações Visuais
- **Apple Keynotes**: Camera work suave, iluminação impecável
- **Stripe Marketing Videos**: Minimal, clean, color grading top
- **Linear App Videos**: Smooth UI animations, fast-paced
- **Notion Product Demos**: Clear, friendly, não intimidador

### Style References
- **COLD Phase**: "Blade Runner 2049" color palette
- **WARM Phase**: "Her" (Spike Jonze) soft naturals
- **GOLDEN Phase**: "La La Land" golden hour glow
- **{{EASTER_EGG_NAME}}**: "Studio Ghibli" cozy warmth

---

## 📝 PLACEHOLDER REFERENCE

### Required Placeholders

**Brand & Product**:
- `{{BRAND_NAME}}` - Nome da marca
- `{{BRAND_URL}}` - URL da marca
- `{{PRODUCT_TYPE}}` - Tipo de produto (ex: "Roteador", "Platform", "Tool")

**Colors**:
- `{{PRIMARY_COLOR}}` - Cor primária da marca (ex: #3B82F6)
- `{{SECONDARY_COLOR}}` - Cor secundária
- `{{ACCENT_COLOR}}` - Cor de destaque/CTA (ex: #FBBF24)
- `{{SUCCESS_COLOR}}` - Cor de sucesso (ex: #10B981)
- `{{SUCCESS_LIGHT}}` - Versão clara do success (ex: #22C55E)
- `{{ERROR_COLOR}}` - Cor de erro/problema (ex: #DC2626)
- `{{WARNING_COLOR}}` - Cor de aviso (ex: #F59E0B)
- `{{PROBLEM_COLOR}}` - Cor da fase problema (ex: #1E3A8A)
- `{{NEUTRAL_COLOR}}` - Cor neutra/transição (ex: #78716C)
- `{{COMBO_COLOR}}` - Cor de combinação (ex: #8B5CF6)
- `{{BG_LIGHT}}` - Background claro (ex: #F9FAFB)
- `{{BG_GOLDEN}}` - Background dourado (ex: #FEF3C7)
- `{{BG_DARK}}` - Background escuro (ex: #111827)
- `{{TEXT_PRIMARY}}` - Cor texto primário (ex: #111827)
- `{{GRAY_MEDIUM}}` - Cinza médio (ex: #6B7280)

**Content**:
- `{{USER_INPUT_EXAMPLE}}` - Exemplo de input do usuário
- `{{TIME_SAVED}}` - Tempo economizado (ex: "50 minutos")
- `{{INPUT_SIMPLICITY}}` - Simplicidade do input (ex: "1 frase")
- `{{PAIN_POINT_PHRASE}}` - Frase do ponto de dor
- `{{PAIN_KEYWORD}}` - Palavra-chave da dor (ex: "escravidão")
- `{{NUM_OPTIONS}}` - Número de opções (ex: "4")
- `{{OPTION_1_NAME}}` - Nome da opção 1 (ex: "PESQUISA")
- `{{OPTION_1_COLOR}}` - Cor da opção 1
- `{{OPTION_2_NAME}}` - Nome da opção 2
- `{{OPTION_2_COLOR}}` - Cor da opção 2
- `{{OPTION_3_NAME}}` - Nome da opção 3
- `{{OPTION_3_COLOR}}` - Cor da opção 3
- `{{OPTION_4_NAME}}` - Nome da opção 4
- `{{OPTION_4_COLOR}}` - Cor da opção 4

**Agents**:
- `{{AGENT_1}}` - Nome do agente 1 (ex: "pesquisa_agent")
- `{{AGENT_2}}` - Nome do agente 2 (ex: "anuncio_agent")
- `{{AGENT_3}}` - Nome do agente 3 (ex: "photo_agent")
- `{{NUM_PHASES}}` - Número de fases (ex: "7")
- `{{QUALITY_SCORE}}` - Score de qualidade (ex: "0.87")
- `{{READY_STATUS}}` - Status de prontidão (ex: "Pronto pra publicar")
- `{{KNOWLEDGE_SOURCES}}` - Fontes de conhecimento (ex: "cursos, mentorias, estratégias")
- `{{AGENT_PRIME_PATH}}` - Caminho para PRIME do agente

**CTA & Easter Eggs**:
- `{{TARGET_AUDIENCE}}` - Público-alvo (ex: "Família")
- `{{CTA_TEXT}}` - Texto do CTA (ex: "COMEÇAR AGORA")
- `{{CTA_BENEFIT}}` - Benefício do CTA (ex: "Teste Grátis")
- `{{CTA_DETAIL}}` - Detalhe do CTA (ex: "Sem cartão")
- `{{EASTER_EGG_NAME}}` - Nome do easter egg (ex: "CAT CODING")
- `{{EASTER_EGG_SCENE}}` - Cena do easter egg
- `{{EASTER_EGG_ANIMATION}}` - Animação do easter egg
- `{{EASTER_EGG_AUDIO}}` - Áudio do easter egg
- `{{EASTER_EGG_DETAIL}}` - Detalhe do easter egg (ex: "Pirulita")
- `{{TAGLINE_REFERENCE}}` - Referência da tagline (ex: "LOTR sutil")

**Competitor**:
- `{{COMPETITOR_TOOLS}}` - Ferramentas concorrentes (ex: "ChatGPT, Canva, etc")

---

## 📝 CHANGELOG

### v1.0.0 (Template Version)
- ✅ Distilled from CODEXA-specific version
- ✅ All brand elements replaced with {{PLACEHOLDERS}}
- ✅ Universal camera movements preserved
- ✅ Lighting arc maintained (COLD → WARM → GOLDEN)
- ✅ All timecodes kept as-is
- ✅ Platform-specific notes retained
- ✅ Comprehensive placeholder reference added

---

**Status**: ✅ TEMPLATE READY
**Usage**: Replace all {{PLACEHOLDERS}} with brand-specific values
**Original Source**: `DIRECAO_VISUAL_LP_ROTEADOR.md` v1.0.0

**Universal Visual Bible Template.** 🎬
