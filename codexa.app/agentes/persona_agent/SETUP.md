# Persona Agent | SETUP

> Configuration and deployment guide for {{PERSONA_NAME}} AI assistant

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     {{BRAND_NAME}} Frontend              │
│  {{PERSONA_NICKNAME}}Chat.tsx -> use{{PERSONA_NAME}}.ts -> voice.ts │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  Supabase Edge Functions                 │
│  {{persona_id}}-chat -> {{persona_id}}-recommendations -> TTS │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                     External APIs                        │
│  Gemini (AI) -> E-commerce (Products) -> OpenAI (TTS)   │
└─────────────────────────────────────────────────────────┘
```

---

## Prerequisites

- Supabase account with Edge Functions enabled
- Google AI API key (Gemini)
- OpenAI API key (TTS)
- E-commerce store with products

---

## Environment Variables

### Supabase Edge Functions

Set in Supabase Dashboard > Edge Functions > Secrets:

```env
# AI
GOOGLE_AI_API_KEY=xxx
OPENAI_API_KEY=xxx

# E-commerce
ECOMMERCE_STORE_URL={{ECOMMERCE_URL}}
ECOMMERCE_ACCESS_TOKEN=xxx

# Optional
ELEVENLABS_API_KEY=xxx
```

---

## Frontend Setup

### 1. Chat Component

Located at: `src/components/{{PERSONA_NICKNAME}}Chat.tsx`

Key props:
```typescript
interface {{PERSONA_NICKNAME}}ChatProps {
  isOpen: boolean;
  onClose: () => void;
  initialMessage?: string;
}
```

### 2. Hook Configuration

Located at: `src/hooks/use{{PERSONA_NAME}}.ts`

```typescript
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL;
const SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY;
```

### 3. Voice Setup

Located at: `src/lib/voice.ts`

Requires browser permissions for microphone access.

---

## Backend Setup

### Edge Functions

Located at: `supabase/functions/`

| Function | Purpose | Endpoint |
|----------|---------|----------|
| `{{persona_id}}-chat` | Main conversation | POST /{{persona_id}}-chat |
| `{{persona_id}}-recommendations` | Product matching | POST /{{persona_id}}-recommendations |
| `{{persona_id}}-tts` | Text-to-speech | POST /{{persona_id}}-tts |

### Deploy Functions

```bash
# Deploy all
supabase functions deploy

# Deploy specific
supabase functions deploy {{persona_id}}-chat
```

---

## Knowledge Base

### Structure

```
persona_agent/
├── knowledge/
│   ├── core/
│   │   └── identidade.md    # Fixed identity
│   └── issues/              # Issue-specific knowledge
│       ├── issue_1.md
│       ├── issue_2.md
│       └── ...
│
└── templates/
    └── variaveis.md         # Variable system
```

### Adding Knowledge

1. Create new file in `knowledge/` directory
2. Follow naming convention: `categoria_topico.md`
3. Include keywords for matching

---

## Testing

### Local Testing

```bash
# Test chat endpoint
curl -X POST \
  'https://your-project.supabase.co/functions/v1/{{persona_id}}-chat' \
  -H 'Authorization: Bearer YOUR_ANON_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"message": "{{EXAMPLE_USER_MESSAGE}}"}'
```

### In Claude Code

```bash
/prime-persona
/{{persona_cmd}}-test "{{EXAMPLE_USER_MESSAGE}}"
```

---

## Monitoring

### Logs

View in Supabase Dashboard > Edge Functions > Logs

### Metrics to Track

- Response time (target: <3s)
- Issue detection accuracy
- Product recommendation CTR
- Red flag triggers

---

## Updating Persona

### Tone Adjustments

Edit: `persona_agent/knowledge/core/identidade.md`

### Adding New Issues

1. Add keywords to detection system
2. Map to product category
3. Create response templates

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Chat not responding | Check Edge Function logs |
| Wrong products | Verify E-commerce integration |
| TTS not working | Check OpenAI API key |
| Voice not recording | Check browser permissions |

---

## Security Notes

- Never expose API keys in frontend
- Use Supabase RLS for data access
- Validate all user inputs
- Rate limit chat endpoints

---

**Version**: 1.0.0
**Last Updated**: {{CURRENT_DATE}}
