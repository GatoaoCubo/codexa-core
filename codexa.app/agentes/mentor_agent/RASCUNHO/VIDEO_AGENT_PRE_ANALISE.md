# VIDEO_AGENT: Análise Pré-Construção

## 1. Comparação com Photo_Agent

### Similaridades (Reutilizar)
- ✅ Workflow: Brief → Research → Concept → Generation
- ✅ Tools: file_search, web_search, image_gen (adaptar para video_gen)
- ✅ Validação: Quality checks, compliance, brand alignment
- ✅ Output format: Structured JSON + media files

### Diferenças (Adaptar)
- 🎬 **Temporal dimension**: Video tem duração, sequência, transições
- 🎬 **Audio layer**: Música, narração, sound effects
- 🎬 **Editing workflow**: Múltiplos shots → timeline → render
- 🎬 **Tools diferentes**: Runway, Pika, Stable Video vs Midjourney/DALL-E

---

## 2. Arquitetura Recomendada

### Pattern: Sequential Pipeline (como Research → Copy → Visual)

```
VIDEO_AGENT Pipeline:

INPUT: Brief do usuário
├─ produto: "Shampoo X"
├─ objetivo: "video 30s para Instagram Reels"
├─ tom: "energético, jovem"
└─ specs: "vertical 9:16, música upbeat"

        ↓

STAGE 1: CONCEPT_AGENT (5-10s)
├─ Analisa brief + brand guidelines
├─ Define storyline (começo, meio, fim)
├─ Cria storyboard (6-8 shots)
└─ OUTPUT: concept.json

        ↓

STAGE 2: SCRIPT_AGENT (3-5s)
├─ Escreve narração/texto overlay
├─ Define timing de cada shot
├─ Escolhe música/sfx
└─ OUTPUT: script.json

        ↓

STAGE 3: VISUAL_AGENT (30-60s)
├─ Gera prompts para cada shot (Runway/Pika)
├─ Define transições entre shots
├─ Valida consistência visual
└─ OUTPUT: shotlist.json

        ↓

STAGE 4: PRODUCTION_AGENT (background, 2-5min)
├─ Chama APIs de video generation
├─ Aguarda renders (async)
├─ Baixa clips gerados
└─ OUTPUT: raw_clips/

        ↓

STAGE 5: EDITING_AGENT (10-20s)
├─ Monta timeline (clips + audio + text)
├─ Aplica transições e efeitos
├─ Exporta video final
└─ OUTPUT: final_video.mp4
```

---

## 3. Decisões de Arquitetura

### Opção A: 5 Sub-Agents (Recomendado) ✅
**Prós**:
- Especialização clara (cada agent faz 1 coisa bem)
- Fácil debugar (sabe exatamente onde falhou)
- Modular (substituir VISUAL_AGENT sem quebrar resto)

**Contras**:
- Mais complexo de orquestrar
- Latência maior (5 etapas sequenciais)

### Opção B: 1 Monolithic Agent ❌
**Prós**:
- Simples de implementar inicialmente
- Latência menor (1 chamada LLM)

**Contras**:
- Difícil debugar (tudo misturado)
- Qualidade inferior (generalista vs especialistas)

**Recomendação**: Opção A (5 sub-agents) para qualidade superior.

---

## 4. Stack Tecnológico

### LLM Orchestrator
- **Claude Sonnet 4**: Concept + Script agents
- **Claude Haiku**: Validações rápidas

### Video Generation APIs
- **Runway Gen-3**: Realismo alto, $0.05/segundo
- **Pika 1.5**: Melhor para produtos, $0.03/segundo
- **Stable Video Diffusion**: Open-source, self-hosted

### Video Editing
- **FFmpeg**: CLI para timeline assembly (free)
- **MoviePy**: Python library (free, flexível)
- **Remotion**: React-based (programmatic editing)

### Storage
- **AWS S3**: Armazenar clips + final videos
- **CloudFlare R2**: Alternativa mais barata

---

## 5. Estimativa de Custos

### Por Video (30s, 6 shots)

**LLM Calls**:
- Concept Agent: $0.02
- Script Agent: $0.01
- Visual Agent: $0.03
- Editing Agent: $0.01
- **Total LLM**: $0.07

**Video Generation** (Pika):
- 6 shots × 5s cada = 30s total
- $0.03/s × 30s = $0.90
- **Total Video Gen**: $0.90

**Storage** (S3):
- 50 MB final video × $0.023/GB = $0.001
- **Total Storage**: negligível

**TOTAL POR VIDEO**: ~$1.00

**Escala** (100 videos/mês):
- Custo mensal: $100
- Vs contratar editor: $2.000-5.000/mês
- **ROI**: 20-50x

---

## 6. Riscos e Mitigações

### Risco 1: Latência Alta (2-5 min/video)
**Mitigação**:
- Rodar PRODUCTION_AGENT em background (async)
- Mostrar preview para usuário enquanto render acontece
- Queue system (processar múltiplos em paralelo)

### Risco 2: Qualidade Inconsistente
**Mitigação**:
- VALIDATION_AGENT dedicado (checa cada shot)
- Retry automático se quality < threshold
- Fallback para templates pré-aprovados

### Risco 3: Custo de API
**Mitigação**:
- Cache de shots similares (reutilizar)
- Tier pricing (primeiros 50 videos grátis, depois cobrar)
- Option para self-hosted (Stable Video Diffusion)

---

## 7. Próximos Passos

### Semana 1: Prototype
- [ ] Implementar CONCEPT_AGENT (gera storyboard)
- [ ] Testar com 5 briefs reais
- [ ] Validar output quality

### Semana 2: Integration
- [ ] Integrar Runway/Pika API
- [ ] Implementar PRODUCTION_AGENT (async)
- [ ] Testar geração de 1 video completo

### Semana 3: Editing Pipeline
- [ ] Implementar EDITING_AGENT (FFmpeg/MoviePy)
- [ ] Montar timeline automático
- [ ] Exportar video final

### Semana 4: Polish & Deploy
- [ ] Adicionar validations
- [ ] Error handling + retries
- [ ] Deploy beta para 10 usuários teste

---

**Decisão Final**: Prosseguir com arquitetura de 5 sub-agents usando Runway para geração e FFmpeg para edição.
