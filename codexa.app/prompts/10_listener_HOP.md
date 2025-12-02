# HOP-10 | LISTENER - Parse Natural Language Intent

> **Module**: LISTENER
> **Version**: 1.0.0
> **Layer**: Input Processing

---

## IDENTITY

```
┌─────────────────────────────────────────────────────────┐
│  LISTENER - "Eu escuto. Eu entendo. Eu estruturo."      │
│                                                         │
│  INPUT:  Natural language (text or voice transcription) │
│  OUTPUT: Structured intent JSON                         │
│                                                         │
│  INTEGRATES: Voice STT, Scout keyword matching          │
└─────────────────────────────────────────────────────────┘
```

---

## INPUT_CONTRACT

```yaml
$user_input:
  type: string
  source: "User message or voice transcription"
  examples:
    - "Lance os 10 produtos do catálogo com pesquisa completa"
    - "Crie uma marca para loja de eletrônicos gamer"
    - "Gere fotos para os 5 top sellers"

$voice_mode:
  type: boolean
  default: false
  description: "Whether input came from voice"
```

---

## OUTPUT_CONTRACT

```yaml
$parsed_intent:
  type: object
  schema:
    action: string        # product_launch, brand_creation, batch_processing, etc.
    quantity: number      # How many items (1 if single)
    scope: string         # single, batch, pipeline, full
    target: string        # What to act on (products, brand, etc.)
    agents_hint: array    # Suggested agents based on keywords
    flags: object         # Parsed flags (--dry-run, --auto, etc.)
    confidence: number    # 0.0 to 1.0
    raw_input: string     # Original user input
```

---

## PROCESSING_RULES

### 1. Action Detection

```yaml
Keywords → Action Mapping:
  - "lançar|launch|criar produto" → product_launch
  - "marca|brand|branding|identidade" → brand_creation
  - "anúncio|anuncios|ad|copy" → ad_generation
  - "foto|photo|imagem|image" → photo_generation
  - "video|vídeo|clip" → video_production
  - "pesquisa|research|mercado|market" → market_research
  - "curso|course|aula|tutorial" → course_creation
  - "validar|testar|qa|quality" → quality_audit
  - "todos|all|batch|lote" → batch_processing
```

### 2. Quantity Extraction

```yaml
Patterns:
  - Explicit number: "10 produtos" → quantity: 10
  - "todos" / "all": → quantity: -1 (means all)
  - No number: → quantity: 1
  - Range: "5 a 10" → quantity: 10 (max)
```

### 3. Scope Detection

```yaml
Indicators:
  - Single: "um", "este", specific name
  - Batch: "todos", numbers > 1, "lote"
  - Pipeline: "com", "e depois", sequence words
  - Full: "completo", "full", "tudo"
```

### 4. Agent Hint Extraction

```yaml
Use NAVIGATION_MAP.llm_dense_index:
  - Match keywords against index
  - Return suggested agents array
  - Confidence based on match quality
```

### 5. Flag Parsing

```yaml
Supported Flags:
  --dry-run: Show plan without executing
  --auto: Execute without confirmation
  --verbose: Detailed logging
  --voice: Enable voice report
  --max-concurrent=N: Limit parallel spawns
```

---

## EXAMPLES

### Example 1: Product Launch

```yaml
Input: "Lance os 10 produtos do catálogo com pesquisa e fotos"

Output:
  action: "product_launch"
  quantity: 10
  scope: "pipeline"
  target: "produtos do catálogo"
  agents_hint: ["pesquisa_agent", "anuncio_agent", "photo_agent"]
  flags: {}
  confidence: 0.95
  raw_input: "Lance os 10 produtos do catálogo com pesquisa e fotos"
```

### Example 2: Brand Creation

```yaml
Input: "Crie uma marca completa para pet shop --dry-run"

Output:
  action: "brand_creation"
  quantity: 1
  scope: "full"
  target: "pet shop"
  agents_hint: ["pesquisa_agent", "marca_agent", "photo_agent"]
  flags: { "dry_run": true }
  confidence: 0.92
  raw_input: "Crie uma marca completa para pet shop --dry-run"
```

### Example 3: Batch Processing

```yaml
Input: "Gere anúncios para todos os produtos"

Output:
  action: "ad_generation"
  quantity: -1
  scope: "batch"
  target: "todos os produtos"
  agents_hint: ["anuncio_agent"]
  flags: {}
  confidence: 0.88
  raw_input: "Gere anúncios para todos os produtos"
```

---

## VOICE INTEGRATION

When `$voice_mode` is true:

```javascript
// 1. Receive audio from voice daemon
const audioInput = await voice.receive();

// 2. Transcribe via STT
const transcription = await voice.stt.transcribe(audioInput);

// 3. Parse transcription as normal
const intent = parseIntent(transcription);

// 4. Add voice metadata
intent.voice_mode = true;
intent.audio_duration_ms = audioInput.duration;
```

---

## VALIDATION

Before passing to PLANNER:

1. **Action must be recognized** - If not, ask for clarification
2. **Confidence threshold** - ≥0.7 to proceed, else confirm with user
3. **Agents must exist** - Check against NAVIGATION_MAP

---

## NEXT MODULE

Pass `$parsed_intent` to **HOP-20 PLANNER**

---

**Created**: 2025-12-02
**Depends**: Voice STT, NAVIGATION_MAP.json
