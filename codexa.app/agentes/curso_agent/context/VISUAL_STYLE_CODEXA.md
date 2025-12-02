# CODEXA Visual Style Guide

**Versão**: 1.0.0 | **Data**: 2025-11-29
**Tipo**: Brand Visual Identity + Video Production Style

---

## CONCEITO CENTRAL

### A Metáfora Visual

```
CODEXA = O Arquiteto na Camada 3

Você não está NO sistema.
Você está ACIMA do sistema, construindo-o.

Visual: Perspectiva elevada, como um arquiteto olhando a planta de cima.
```

### Mood Board Conceitual

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   NÃO É:                          É:                            │
│   ─────                           ──                            │
│   Tech bro arrogante              Mentor acessível              │
│   Frio e robótico                 Humano e tecnológico          │
│   Complexo e intimidador          Sofisticado mas claro         │
│   Hype de startup                 Autoridade silenciosa         │
│   Neon cyberpunk                  Azul profundo + ouro          │
│   Flat e genérico                 Profundidade e camadas        │
│                                                                 │
│   SENTIMENTO: "Encontrei alguém que sabe o que está fazendo"    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 1. PALETA DE CORES

### 1.1 Cores Primárias

```yaml
DEEP_OCEAN:
  hex: "#0A1628"
  rgb: "10, 22, 40"
  uso: "Background principal, base de credibilidade"
  sensacao: "Profundidade, conhecimento, confiança"

ELECTRIC_SAPPHIRE:
  hex: "#2563EB"
  rgb: "37, 99, 235"
  uso: "CTAs, highlights, elementos interativos"
  sensacao: "Tecnologia, inteligência, ação"

KNOWLEDGE_GOLD:
  hex: "#F59E0B"
  rgb: "245, 158, 11"
  uso: "Destaques premium, achievements, valor"
  sensacao: "Valor, conquista, conhecimento precioso"
```

### 1.2 Cores Secundárias

```yaml
SOFT_WHITE:
  hex: "#F8FAFC"
  rgb: "248, 250, 252"
  uso: "Texto principal, respiro visual"
  sensacao: "Clareza, legibilidade, ar"

STEEL_GRAY:
  hex: "#64748B"
  rgb: "100, 116, 139"
  uso: "Texto secundário, bordas sutis"
  sensacao: "Profissionalismo, neutralidade"

MINT_SUCCESS:
  hex: "#10B981"
  rgb: "16, 185, 129"
  uso: "Confirmações, progresso, XP ganho"
  sensacao: "Sucesso, crescimento, validação"

CORAL_ALERT:
  hex: "#F43F5E"
  rgb: "244, 63, 94"
  uso: "Alertas, dores, problemas (antes)"
  sensacao: "Urgência suave, atenção"
```

### 1.3 Gradientes Signature

```yaml
GRADIENT_DEPTH:
  from: "#0A1628"
  via: "#1E3A5F"
  to: "#2563EB"
  direcao: "180deg (top to bottom)"
  uso: "Backgrounds de seção, cards premium"

GRADIENT_KNOWLEDGE:
  from: "#2563EB"
  to: "#F59E0B"
  direcao: "135deg (diagonal)"
  uso: "Elementos de destaque, badges, highlights"

GRADIENT_GLOW:
  from: "#2563EB40"
  to: "#2563EB00"
  tipo: "Radial"
  uso: "Efeito de brilho atrás de elementos importantes"
```

### 1.4 Aplicação de Cores

```
┌─────────────────────────────────────────────────────────────────┐
│  HIERARQUIA VISUAL                                              │
│                                                                 │
│  ████████████████████████████████████ DEEP_OCEAN (60%)         │
│  Background, base, fundação                                     │
│                                                                 │
│  ██████████████████ ELECTRIC_SAPPHIRE (25%)                    │
│  CTAs, links, destaques primários                              │
│                                                                 │
│  ████████ KNOWLEDGE_GOLD (10%)                                 │
│  Achievements, valor, premium                                   │
│                                                                 │
│  ████ ACCENT COLORS (5%)                                       │
│  Success, alerts, variação                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. TIPOGRAFIA

### 2.1 Font Stack

```yaml
HEADLINES:
  font: "Inter"
  fallback: "SF Pro Display, -apple-system, sans-serif"
  weights: [700, 800]
  caracteristica: "Geométrica, moderna, authoritative"

BODY:
  font: "Inter"
  fallback: "SF Pro Text, -apple-system, sans-serif"
  weights: [400, 500, 600]
  caracteristica: "Alta legibilidade, clean"

CODE:
  font: "JetBrains Mono"
  fallback: "Fira Code, Consolas, monospace"
  weights: [400, 500]
  caracteristica: "Ligatures, tech feel"

ACCENT:
  font: "Space Grotesk"
  fallback: "Inter, sans-serif"
  weights: [500, 700]
  caracteristica: "Distintiva, para números e badges"
```

### 2.2 Escala Tipográfica

```yaml
# Desktop
h1: "48px / 56px line-height / -0.02em tracking"
h2: "36px / 44px / -0.01em"
h3: "24px / 32px / 0"
h4: "20px / 28px / 0"
body: "16px / 24px / 0"
small: "14px / 20px / 0.01em"
caption: "12px / 16px / 0.02em"

# Mobile
h1: "32px / 40px"
h2: "28px / 36px"
h3: "20px / 28px"
body: "16px / 24px"
```

### 2.3 Tratamento de Texto

```yaml
headlines:
  - Sempre em Sentence case (não ALL CAPS)
  - Máximo 2 linhas
  - Contraste mínimo 7:1 no background

body:
  - Linha máxima: 65-75 caracteres
  - Parágrafo máximo: 4 linhas antes de quebra
  - Espaçamento entre parágrafos: 1.5x line-height

destaques:
  - Keywords em KNOWLEDGE_GOLD
  - Termos técnicos em `monospace`
  - Números grandes em Space Grotesk
```

---

## 3. ELEMENTOS VISUAIS

### 3.1 Camadas e Profundidade

```
O visual CODEXA usa CAMADAS literais para representar
os 3 níveis de uso de IA (Usuário → Automação → Meta)

┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   LAYER 3 (mais acima, mais visível)                           │
│   ┌─────────────────────────────────┐                          │
│   │  Elementos interativos          │  shadow-xl               │
│   │  CTAs, modais, cards flutuantes │  blur backdrop           │
│   └─────────────────────────────────┘                          │
│                                                                 │
│   LAYER 2 (meio)                                                │
│   ┌─────────────────────────────────┐                          │
│   │  Conteúdo principal             │  shadow-md               │
│   │  Cards, seções, diagramas       │  border sutil            │
│   └─────────────────────────────────┘                          │
│                                                                 │
│   LAYER 1 (base)                                                │
│   ┌─────────────────────────────────┐                          │
│   │  Background, grid, texturas     │  flat                    │
│   │  Elementos de suporte           │  low contrast            │
│   └─────────────────────────────────┘                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Cards e Containers

```yaml
card_padrao:
  background: "rgba(30, 58, 95, 0.5)"  # DEEP_OCEAN com transparência
  border: "1px solid rgba(37, 99, 235, 0.2)"  # SAPPHIRE sutil
  border_radius: "16px"
  padding: "24px"
  shadow: "0 4px 24px rgba(0, 0, 0, 0.3)"
  backdrop_filter: "blur(12px)"

card_hover:
  border: "1px solid rgba(37, 99, 235, 0.5)"
  shadow: "0 8px 32px rgba(37, 99, 235, 0.15)"
  transform: "translateY(-2px)"
  transition: "all 0.3s ease"

card_premium:
  border: "1px solid rgba(245, 158, 11, 0.3)"  # GOLD border
  background: "linear-gradient(135deg, rgba(30, 58, 95, 0.8), rgba(10, 22, 40, 0.9))"
```

### 3.3 Ícones e Ilustrações

```yaml
estilo_icones:
  tipo: "Outline com fill seletivo"
  stroke: "2px"
  corners: "Rounded (match border-radius)"
  tamanhos: [16, 20, 24, 32, 48]

principios:
  - Simplicidade geométrica
  - Consistência de peso visual
  - Área de toque mínima 44x44px
  - Cor única (SAPPHIRE ou WHITE)

icones_signature:
  - Cérebro com conexões (Meta-Construção)
  - Camadas empilhadas (3 Layers)
  - Gota destilando (Knowledge Distillation)
  - 4 quadrantes (Os 4 CORES)
  - Coroa simples (Meta-God badge)

ilustracoes:
  estilo: "Isométrico simplificado"
  cores: "Paleta CODEXA (máximo 4 cores)"
  detalhes: "Minimal, sem gradientes complexos"
  uso: "Diagramas conceituais, não decoração"
```

---

## 4. MOTION DESIGN

### 4.1 Princípios de Animação

```yaml
filosofia: "Movimento com propósito, não decoração"

principios:
  - Guiar atenção, não distrair
  - Revelar hierarquia através de sequência
  - Feedback imediato em interações
  - Transições suaves entre estados

timing_function: "cubic-bezier(0.4, 0, 0.2, 1)"  # Material easing
```

### 4.2 Durações Padrão

```yaml
micro: "150ms"
# Hover states, toggles, pequenos feedbacks

short: "250ms"
# Transições de cor, opacity changes

medium: "400ms"
# Modais entrando, cards expandindo

long: "600ms"
# Transições de página, reveals complexos

extra_long: "1000ms"
# Animações de loading, progress bars
```

### 4.3 Animações Signature

```yaml
LAYER_REVEAL:
  descricao: "Elementos emergem de baixo para cima, em camadas"
  aplicacao: "Entrada de seções, listas, cards"
  sequencia:
    - "Layer 1 aparece primeiro (0ms)"
    - "Layer 2 aparece depois (150ms delay)"
    - "Layer 3 aparece por último (300ms delay)"
  easing: "ease-out"
  duracao: "400ms cada"

KNOWLEDGE_GLOW:
  descricao: "Pulse suave em elementos de valor"
  aplicacao: "Achievements desbloqueados, XP ganho"
  efeito: "Box-shadow GOLD pulsando"
  duracao: "2s loop"

DEPTH_SHIFT:
  descricao: "Zoom sutil para dar sensação de profundidade"
  aplicacao: "Transição entre conceitos/camadas"
  scale: "1.0 → 1.02 → 1.0"
  blur: "Background blur durante transição"

TEXT_REVEAL:
  descricao: "Texto aparece caractere por caractere ou palavra por palavra"
  aplicacao: "Headlines importantes, citações"
  velocidade: "30ms por caractere"
  cursor: "Blink no final (como terminal)"
```

---

## 5. VIDEO PRODUCTION STYLE

### 5.1 Estilo de Câmera

```yaml
enquadramento:
  tipo: "Medium close-up (do peito para cima)"
  regra_dos_tercos: "Olhos no terço superior"
  look_room: "Espaço para o lado que olha"
  head_room: "Mínimo acima da cabeça"

movimento:
  principal: "Estático com micro-movimentos"
  zoom: "Lento, 5% máximo, para ênfase"
  pan: "Raramente, apenas para revelar"

posicao:
  angulo: "Levemente acima do nível dos olhos"
  justificativa: "Transmite autoridade sem arrogância"
  distancia: "Íntima mas profissional"
```

### 5.2 Iluminação

```yaml
estilo: "Soft key com rim light"

key_light:
  posicao: "45° à frente e acima"
  intensidade: "Principal, define o rosto"
  qualidade: "Soft (difusor grande)"
  temperatura: "5000-5500K (daylight)"

fill_light:
  posicao: "Oposta ao key, mais baixa"
  intensidade: "30-40% do key"
  funcao: "Suavizar sombras sem eliminar"

rim_light:
  posicao: "Atrás, oposto ao key"
  intensidade: "Destaque nas bordas"
  cor: "Levemente azulada (#2563EB tint)"
  funcao: "Separar do background, criar profundidade"

background_light:
  intensidade: "Gradiente, mais escuro nas bordas"
  cor: "DEEP_OCEAN com variação"
  efeito: "Vinheta natural"
```

### 5.3 Cenário/Background

```yaml
opcao_1_fisico:
  cor: "Parede em tom escuro (cinza grafite ou azul marinho)"
  elementos:
    - "Prateleira minimalista com livros (3-5)"
    - "Luz LED strip SAPPHIRE (sutil, fora de foco)"
    - "Planta pequena (humaniza)"
    - "Nada no centro (área limpa atrás da cabeça)"
  profundidade: "2-3 metros do apresentador (blur natural)"

opcao_2_virtual:
  tipo: "Abstract depth background"
  elementos:
    - "Gradiente DEEP_OCEAN → SAPPHIRE"
    - "Partículas flutuantes (sutis, lentas)"
    - "Grid geométrico (baixa opacidade)"
    - "Glow points (simulando bokeh)"
  movimento: "Drift lento (5-10px por segundo)"

elementos_graficos_overlay:
  - "Lower third com nome/cargo"
  - "Palavras-chave aparecendo ao lado"
  - "Diagramas entrando quando mencionados"
  - "Progress bar do vídeo (sutil no topo)"
```

### 5.4 Composição de Tela

```yaml
apresentador_camera:
  layout: "Regra dos terços, apresentador à esquerda"
  espaco_livre: "⅓ direito para overlays/gráficos"

  ┌─────────────────────────────────────────────┐
  │        │           │                        │
  │        │  [ROSTO]  │    [ÁREA PARA          │
  │        │           │     GRÁFICOS]          │
  │        │           │                        │
  └─────────────────────────────────────────────┘

screencast:
  layout: "Tela cheia com facecam pequena"
  facecam: "Canto inferior direito, 15-20% da tela"
  borda_facecam: "2px SAPPHIRE, rounded"

  ┌─────────────────────────────────────────────┐
  │                                             │
  │            [SCREENCAST]                     │
  │                                             │
  │                               ┌───────┐     │
  │                               │ FACE  │     │
  │                               │  CAM  │     │
  └───────────────────────────────┴───────┴─────┘

diagrama_fullscreen:
  layout: "Gráfico centralizado, background DEEP_OCEAN"
  animacao: "Build-up progressivo dos elementos"
  presenter: "Voz over, sem facecam"
```

### 5.5 Text Overlays

```yaml
lower_third:
  posicao: "Inferior esquerdo, margem 5%"
  background: "rgba(10, 22, 40, 0.85)"
  borda: "Left border 4px SAPPHIRE"
  padding: "16px 24px"
  animacao: "Slide in from left, 400ms"

  estrutura:
    nome: "Space Grotesk Bold 20px WHITE"
    cargo: "Inter Regular 14px STEEL_GRAY"

keyword_popup:
  posicao: "Ao lado do apresentador"
  background: "rgba(37, 99, 235, 0.15)"
  borda: "1px SAPPHIRE"
  font: "JetBrains Mono 16px"
  animacao: "Fade in + subtle scale"
  duracao_tela: "3-5 segundos"

quote_fullscreen:
  font: "Inter Bold 32px"
  cor: "WHITE com GOLD em palavras-chave"
  background: "GRADIENT_DEPTH"
  aspas: "Decorativas em SAPPHIRE (30% opacity)"
  animacao: "Word by word reveal"
```

---

## 6. THUMBNAIL STYLE

### 6.1 Estrutura

```yaml
dimensoes: "1280x720px (16:9)"

layout:
  ┌─────────────────────────────────────────────┐
  │                                             │
  │  [ROSTO]              [TEXTO PRINCIPAL]     │
  │  expressivo            grande, bold         │
  │  40% da largura        60% da largura       │
  │                                             │
  │              [ELEMENTO VISUAL]              │
  │              (diagrama/ícone/contraste)     │
  │                                             │
  └─────────────────────────────────────────────┘

zonas:
  esquerda: "Rosto com expressão (curiosidade, surpresa, confiança)"
  direita: "Texto principal + elemento visual de suporte"
  inferior: "Área livre para UI do YouTube (título, progress)"
```

### 6.2 Tratamento de Imagem

```yaml
rosto:
  recorte: "Contorno limpo, sem background"
  borda: "3px SAPPHIRE ou GOLD (opcional)"
  sombra: "Drop shadow para separar do fundo"
  expressao: "Autêntica, não forçada"
  olhar: "Para o texto ou para câmera"

background:
  tipo: "GRADIENT_DEPTH ou solid DEEP_OCEAN"
  elementos: "Formas geométricas sutis (15% opacity)"
  glow: "Atrás do rosto (SAPPHIRE radial)"

texto:
  fonte: "Inter Black ou Space Grotesk Bold"
  tamanho: "Mínimo 72px para legibilidade"
  cor: "WHITE com 1 palavra em GOLD"
  shadow: "2px 2px 4px rgba(0,0,0,0.5)"
  max_palavras: "5-7 palavras"
```

### 6.3 Exemplos de Composição

```yaml
estilo_contraste:
  titulo: "De 2 HORAS para 5 MINUTOS"
  visual: "2h em vermelho riscado, 5min em GOLD"
  rosto: "Expressão de alívio/realização"

estilo_revelacao:
  titulo: "O ERRO que 99% comete"
  visual: "Ícone de alerta ou X grande"
  rosto: "Expressão de seriedade/conhecimento"

estilo_framework:
  titulo: "Os 4 CORES da IA"
  visual: "Mini-diagrama dos 4 elementos"
  rosto: "Expressão de explicação/clareza"

estilo_antes_depois:
  titulo: "Você está na Camada ERRADA"
  visual: "Pirâmide com camada 1 em vermelho"
  rosto: "Apontando para o visual"
```

---

## 7. AUDIO DESIGN

### 7.1 Música de Fundo

```yaml
genero: "Ambient Electronic / Lo-fi Tech"
bpm: "70-90 (calm, não agitado)"
elementos:
  - "Pads suaves e prolongados"
  - "Arpejos discretos"
  - "Sem batidas marcantes"
  - "Espacial, com reverb"

volume: "-20dB abaixo da voz"
ducking: "Automático quando apresentador fala"

momentos_especiais:
  hook: "Ligeiro build-up nos primeiros 5s"
  transicoes: "Swell suave entre seções"
  cta: "Resolução musical (sensação de chegada)"
```

### 7.2 Sound Effects

```yaml
transicoes:
  tipo: "Whoosh suave, não agressivo"
  volume: "-15dB"
  uso: "Entre seções principais"

destaques:
  tipo: "Soft chime / notification sound"
  volume: "-12dB"
  uso: "Quando keyword aparece"

achievements:
  tipo: "Ascending tone + sparkle"
  volume: "-10dB"
  uso: "XP ganho, badge desbloqueado"

typing:
  tipo: "Soft keyboard clicks"
  volume: "-18dB"
  uso: "Durante text reveals"
```

### 7.3 Voz

```yaml
tratamento:
  eq: "High-pass 80Hz, presence boost 2-4kHz"
  compressao: "Leve, ratio 2:1"
  de_essing: "Sim, frequências 5-8kHz"
  volume: "Consistente, peaks em -6dB"

ambiente:
  reverb: "Room pequeno, sutil"
  noise_gate: "Threshold baixo"

tom:
  registro: "Médio-grave (autoridade sem intimidação)"
  ritmo: "Pausado, não apressado"
  enfase: "Em keywords e números"
```

---

## 8. APLICAÇÃO POR CONTEXTO

### 8.1 Video Promo (30-60s)

```yaml
ritmo: "Rápido, cortes a cada 2-3s"
musica: "Mais energética, build-up"
texto: "Bold, grande, impacto imediato"
cor_dominante: "SAPPHIRE + GOLD"
cta: "Forte, urgência visual"
```

### 8.2 Video LP (2-3 min)

```yaml
ritmo: "Moderado, cortes a cada 4-5s"
musica: "Equilibrada, inspira confiança"
texto: "Destaques pontuais"
cor_dominante: "DEEP_OCEAN + SAPPHIRE"
cta: "Convite, não pressão"
```

### 8.3 Módulo 0 (10 min)

```yaml
ritmo: "Educacional, cortes a cada 8-10s"
musica: "Sutil, quase imperceptível"
texto: "Estrutural (títulos de seção)"
cor_dominante: "DEEP_OCEAN + WHITE"
cta: "Suave, 'vai estar aqui quando decidir'"
```

### 8.4 Curso Completo (15-30 min/módulo)

```yaml
ritmo: "Didático, variado conforme conteúdo"
musica: "Apenas em transições"
texto: "Checkpoints, resumos, frameworks"
cor_dominante: "Paleta completa equilibrada"
cta: "Próximo módulo, exercício"
```

---

## 9. CONSISTÊNCIA DE MARCA

### 9.1 Do's

```markdown
✅ Usar paleta de cores consistentemente
✅ Manter tipografia padronizada
✅ Aplicar motion com propósito
✅ Respeitar hierarquia de camadas
✅ Priorizar legibilidade
✅ Ser minimalista com elementos
✅ Manter espaço negativo
✅ Usar glow e gradientes com moderação
```

### 9.2 Don'ts

```markdown
❌ Misturar fontes além do sistema definido
❌ Usar cores fora da paleta
❌ Animar tudo (motion sem propósito)
❌ Sobrecarregar com elementos visuais
❌ Usar stock photos genéricas
❌ Aplicar efeitos datados (lens flare, 3D bevel)
❌ Ignorar contraste de acessibilidade
❌ Copiar estética de outras marcas tech
```

---

## 10. ASSETS PARA PRODUÇÃO

### 10.1 Checklist de Preparação

```markdown
GRÁFICOS ESTÁTICOS:
- [ ] Thumbnail templates (3 variações)
- [ ] Lower third template
- [ ] Card de CTA final
- [ ] Diagrama "Os 4 CORES"
- [ ] Diagrama "3 Camadas"
- [ ] Ícones dos 6 agentes

MOTION GRAPHICS:
- [ ] Intro animada (3-5s)
- [ ] Transição entre seções
- [ ] Text reveal animation
- [ ] XP/Achievement animation
- [ ] Subscriber/Like reminder
- [ ] End screen template

ÁUDIO:
- [ ] Background music (loop)
- [ ] Transition whoosh
- [ ] Highlight chime
- [ ] Achievement sound
```

### 10.2 Especificações de Export

```yaml
video:
  codec: "H.264"
  resolucao: "1920x1080 (4K se possível)"
  fps: "30 (fala) ou 60 (screencast)"
  bitrate: "15-20 Mbps"

audio:
  codec: "AAC"
  sample_rate: "48kHz"
  bitrate: "320kbps"

graficos:
  formato: "PNG (transparência) ou SVG"
  resolucao: "2x para retina"

cores:
  perfil: "sRGB para web"
```

---

## RESUMO VISUAL

```
┌─────────────────────────────────────────────────────────────────┐
│                     CODEXA VISUAL IDENTITY                      │
│                                                                 │
│  CORES:    Deep Ocean │ Electric Sapphire │ Knowledge Gold     │
│            #0A1628    │ #2563EB           │ #F59E0B            │
│                                                                 │
│  FONTES:   Inter (body) │ Space Grotesk (accent) │ JetBrains   │
│                                                                 │
│  MOOD:     Sofisticado + Acessível + Tecnológico + Humano      │
│                                                                 │
│  MOTION:   Proposital + Em Camadas + Suave + Revelador         │
│                                                                 │
│  VIDEO:    Calmo + Autoridade + Profundidade + Intimidade      │
│                                                                 │
│  SOM:      Ambient + Sutil + Espacial + Confiante              │
│                                                                 │
│  MANTRA:   "O Arquiteto na Camada 3"                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

**Versão**: 1.0.0
**Data**: 2025-11-29
**Autor**: Curso Agent + Brand Guidelines
**Uso**: Video Production, Thumbnails, Course Materials, Marketing Assets
