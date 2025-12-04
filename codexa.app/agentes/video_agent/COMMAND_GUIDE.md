# COMMAND GUIDE: Video Creation

**Como comandar o video_agent** | v1.0.0 | 2025-12-04

---

## Visão Geral

Dois modos de operação: **LLM** (Claude executa autonomamente) e **Humano** (você comanda passo a passo).

```
PIPELINE COMPLETO (Fases 1-6.5)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1] Concept → [2] Script → [3] Visual → [4] Render → [5] Edit
                                                          ↓
[6+] Title → [6++] Description → [6+++] Tags → [6++++] Thumbnail → [6.5] Chapters
```

---

## LLM: Execução Autônoma

### Comando Único (Full Pipeline)

```
/prime-video

Crie um vídeo de 30s para [PRODUTO] no formato 9:16.
Tom: [energético/calmo/dramático]
Objetivo: [benefício principal]
Incluir: otimização YouTube completa (title, description, tags, thumbnail, chapters)
```

**O que o LLM faz sozinho:**
1. Valida brief e escolhe execution_plan
2. Gera storyboard (6-8 shots)
3. Escreve script com timing
4. Cria prompts Runway/Pika
5. Orquestra geração de clips
6. Monta vídeo final (FFmpeg)
7. Gera metadados YouTube (6 otimizadores)
8. Entrega Trinity output (.mp4, .llm.json, .meta.json)

### Comando Parcial (Só Metadados YouTube)

```
/prime-video

Tenho um vídeo pronto sobre [TEMA].
Gere apenas os metadados YouTube:
- Título otimizado (5 variantes)
- Descrição SEO (5 seções)
- Tags (30-50, max 500 chars)
- Texto thumbnail (3-5 variantes)
- Chapters (se vídeo >= 3min)

Contexto: [descreva o conteúdo do vídeo]
Duração: [X minutos]
Público-alvo: [quem vai assistir]
```

### Comando Batch (Múltiplos Vídeos)

```
/prime-video

Gere 5 vídeos em batch:

1. Produto: Tênis Nike Air Max | 30s | Tom: energético
2. Produto: Bolsa Louis Vuitton | 20s | Tom: luxo
3. Produto: iPhone 15 Pro | 30s | Tom: tech
4. Produto: Perfume Chanel | 25s | Tom: elegante
5. Produto: Relógio Rolex | 30s | Tom: premium

Formato: 9:16 (Reels/TikTok)
Incluir: metadados YouTube para cada
```

---

## Humano: Comandos Passo a Passo

### Fase 1: Conceito

```bash
# Opção A: Brief mínimo
/youtube-video --produto "Tênis Nike" --duracao 30 --tom energético

# Opção B: Brief detalhado
/youtube-video \
  --produto "Tênis Nike Air Max 2024" \
  --duracao 30 \
  --formato "9:16" \
  --tom "energético, jovem, urbano" \
  --objetivo "destacar amortecimento Air e design moderno" \
  --publico "18-35, atletas amadores" \
  --cta "Compre agora com 20% OFF"
```

### Fase 2-5: Produção

```bash
# Executar pipeline completo
/video-run --all

# Ou fase por fase
/video-run --phase 1  # Concept
/video-run --phase 2  # Script
/video-run --phase 3  # Visual prompts
/video-run --phase 4  # Render clips
/video-run --phase 5  # Edit/assemble
```

### Fase 6+: YouTube Title

```bash
# Standalone (sem vídeo anterior)
/youtube-title \
  --topic "Como ganhar massa muscular em 30 dias" \
  --target-audience "homens 25-40, fitness iniciante" \
  --content-type "tutorial"

# Encadeado (após vídeo)
/youtube-title --from-video outputs/tenis_nike_30s.mp4
```

**Output esperado:**
```
TÍTULOS GERADOS (5 variantes):

1. [QUESTION] Como Ganhar 5kg de Músculo em 30 Dias? (Score: 8.7)
2. [NUMBER] 7 Exercícios Para Ganhar Massa em 1 Mês (Score: 9.1) ⭐ RECOMENDADO
3. [SOCIAL] +10.000 Pessoas Ganharam Músculo Com Isso (Score: 8.2)
4. [HOW-TO] Como Iniciantes Ganham Massa Rápido (Score: 8.5)
5. [COMPARISON] Whey vs Creatina: Qual Dá Mais Resultado? (Score: 8.4)
```

### Fase 6++: YouTube Description

```bash
/youtube-description \
  --title "7 Exercícios Para Ganhar Massa em 1 Mês" \
  --topic "treino hipertrofia iniciantes" \
  --duration 12  # minutos
  --links "https://loja.com/whey, https://app.com/treino"
```

**Output esperado:**
```
DESCRIÇÃO GERADA (5 seções):

[HOOK] (147 chars)
Quer ganhar massa muscular rapidamente? Estes 7 exercícios transformaram
milhares de iniciantes - e vão transformar você também.

[VALUE PROP] (234 chars)
Neste vídeo você aprende:
- Os 7 exercícios essenciais para hipertrofia
- Quantas séries e repetições fazer
- Erros que travam seu ganho de massa
- Plano de 30 dias para resultados visíveis

[TIMESTAMPS]
00:00 Introdução
01:23 Exercício 1: Supino
02:45 Exercício 2: Agachamento
...

[LINKS/CTA]
🛒 Whey Protein: https://loja.com/whey
📱 App de Treino: https://app.com/treino

[HASHTAGS]
#Hipertrofia #GanharMassa #Musculação #Treino #Fitness
```

### Fase 6+++: YouTube Tags

```bash
/youtube-tags \
  --title "7 Exercícios Para Ganhar Massa em 1 Mês" \
  --description-keywords "hipertrofia, massa muscular, treino" \
  --niche "fitness"
```

**Output esperado:**
```
TAGS GERADAS (42 tags, 487/500 chars):

[PRIMARY] 5 tags, 67 chars
ganhar massa muscular, hipertrofia, treino musculação, exercícios massa,
musculação iniciante

[SECONDARY] 10 tags, 156 chars
como ganhar massa, treino hipertrofia, exercícios para massa, ganho muscular,
treino para iniciantes, massa muscular rápido, academia iniciante,
treino completo, série de exercícios, rotina musculação

[LONG-TAIL] 18 tags, 198 chars
como ganhar massa muscular em 30 dias, exercícios para ganhar massa em casa,
treino de hipertrofia para iniciantes, melhores exercícios para massa muscular,
...

[SEMANTIC] 6 tags, 66 chars
fitness, bodybuilding, gym, workout, muscle building, strength training
```

### Fase 6++++: Thumbnail Text

```bash
/youtube-thumbnail-text \
  --title "7 Exercícios Para Ganhar Massa em 1 Mês" \
  --angle benefit  # ou: hook, curiosity, urgency, transformation
```

**Output esperado:**
```
TEXTOS THUMBNAIL (5 variantes):

[A] HOOK: "Segredo Revelado" (Score: 7.8)
    Case: ALL_CAPS | Posição: Top | CTR: 1.18x

[B] BENEFIT: "+5kg em 30 Dias" (Score: 9.2) ⭐ RECOMENDADO
    Case: Mixed | Posição: Center | CTR: 1.32x

[C] CURIOSITY: "Você Fazia Errado" (Score: 8.1)
    Case: Title Case | Posição: Bottom | CTR: 1.25x

[D] URGENCY: "Só Funciona Assim" (Score: 7.5)
    Case: ALL_CAPS | Posição: Top | CTR: 1.20x

[E] TRANSFORMATION: "Magro → Forte" (Score: 8.6)
    Case: Mixed + Symbol | Posição: Center | CTR: 1.28x
```

### Fase 6.5: Chapters

```bash
/youtube-chapters \
  --input-mode script  # ou: transcript, outline
  --duration 12  # minutos
  --script-file outputs/tenis_nike_script.json
```

**Output esperado:**
```
CHAPTERS GERADOS (7 capítulos):

00:00 Introdução e Visão Geral
01:23 Preparando o Ambiente de Treino
02:45 Dominando o Supino Correto
04:12 Executando Agachamento Perfeito
06:30 Implementando Remada Curvada
08:45 Otimizando Desenvolvimento de Ombros
10:30 Conclusão e Próximos Passos

Score: 8.7/10 | Cobertura: 95% | Timing: OK
```

---

## Comparativo: LLM vs Humano

| Aspecto | LLM (Autônomo) | Humano (Passo a Passo) |
|---------|----------------|------------------------|
| **Velocidade** | ~5 min (pipeline completo) | ~15-30 min (com revisões) |
| **Controle** | Baixo (confia no agente) | Alto (aprova cada fase) |
| **Personalização** | Média (ajustes no brief) | Alta (edita outputs) |
| **Consistência** | Alta (mesmo padrão) | Variável (depende do operador) |
| **Ideal para** | Batch, escala, prototipagem | Campanhas premium, ajuste fino |

---

## Atalhos Rápidos

### Vídeo Completo + YouTube
```
/prime-video
Vídeo 30s para [PRODUTO]. Tom [X]. Formato 9:16.
Incluir todos os metadados YouTube.
```

### Só Metadados YouTube (Vídeo Existente)
```
/prime-video
Metadados YouTube para vídeo sobre [TEMA].
Duração: [X] min. Público: [Y].
```

### Só Título (Rápido)
```
/youtube-title --topic "[TEMA]" --type "[tutorial/review/vlog]"
```

### Só Tags (Rápido)
```
/youtube-tags --title "[TÍTULO FINAL]" --niche "[NICHO]"
```

### Pipeline YouTube Completo
```
/youtube-title → /youtube-description → /youtube-tags → /youtube-thumbnail-text → /youtube-chapters
```

---

## Checklist de Aprovação Humana

Antes de publicar, o humano DEVE validar:

### Vídeo (Fases 1-5)
- [ ] Storyboard conta história coerente (6-8 shots)
- [ ] Script timing viável (palavras/segundo OK)
- [ ] Clips sem artefatos ou glitches
- [ ] Áudio sincronizado (narração + música)
- [ ] Texto legível (contraste, tamanho)
- [ ] Brand voice consistente
- [ ] Aspect ratio correto para plataforma

### YouTube Metadata (Fases 6+)
- [ ] Título não é clickbait enganoso
- [ ] Descrição tem timestamps corretos
- [ ] Tags relevantes (não keyword stuffing)
- [ ] Thumbnail text complementa (não duplica) título
- [ ] Chapters alinhados com conteúdo real

---

## Output Consolidado

O pipeline gera 2 arquivos finais prontos para uso:

### YOUTUBE_READY.json (Para APIs/Automação)
```json
{
  "youtube_metadata": {
    "title": "...",
    "description": "...",
    "tags": "...",
    "thumbnail_text": "..."
  },
  "score": 8.92,
  "generated": "2025-12-04"
}
```

### YOUTUBE_READY.md (Para Copy-Paste)
```markdown
## TÍTULO
22 Anúncios em 18 Minutos: Conheça o Codexa

## THUMBNAIL TEXT
10x Mais Rápido

## DESCRIÇÃO
[texto completo pronto para colar]

## TAGS
[tags separadas por vírgula]
```

### Estrutura de Arquivos
```
outputs/
├── YOUTUBE_READY.json    ← Consolidado (use este)
├── YOUTUBE_READY.md      ← Copy-paste humano
└── detailed/             ← Análises detalhadas (opcional)
    ├── 01_title_output.json
    ├── 02_description_output.json
    ├── 03_tags_output.json
    ├── 04_thumbnail_output.json
    └── 05_chapters_output.json
```

---

## Troubleshooting

| Problema | Comando |
|----------|---------|
| Título muito genérico | `/youtube-title --angle number --specificity high` |
| Descrição sem keywords | `/youtube-description --keyword-density 2.5` |
| Tags estourando 500 chars | `/youtube-tags --max-chars 480 --prioritize primary` |
| Thumbnail ilegível | `/youtube-thumbnail-text --max-words 3 --case CAPS` |
| Chapters muito curtos | `/youtube-chapters --min-gap 60` |

---

## Fluxos Recomendados

### Fluxo 1: Vídeo Novo (LLM Full)
```
1. /prime-video [brief completo]
2. LLM executa Fases 1-6.5
3. Humano revisa checklist
4. Publicar
```

### Fluxo 2: Vídeo Existente (Metadata Only)
```
1. /youtube-title --topic [X]
2. /youtube-description --title [resultado anterior]
3. /youtube-tags --title [X] --description-keywords [Y]
4. /youtube-thumbnail-text --title [X]
5. /youtube-chapters --transcript [arquivo]
6. Humano revisa e publica
```

### Fluxo 3: Batch (Escala)
```
1. Preparar products.json com N briefs
2. /prime-video --batch products.json
3. LLM processa N vídeos em paralelo
4. Humano revisa amostra (20%)
5. Publicar batch
```

---

**Created by**: video_agent v2.8.0
**Purpose**: Guia de comandos LLM vs Humano para criação de vídeo
