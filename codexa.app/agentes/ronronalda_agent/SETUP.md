# Ronronalda Agent | SETUP

> Configuration and deployment guide for Ronronalda AI assistant

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     GATO3 Frontend                       │
│  RoChat.tsx → useRonronalda.ts → voice.ts               │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  Supabase Edge Functions                 │
│  ronronalda-chat → ronronalda-recommendations → TTS     │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                     External APIs                        │
│  Gemini (AI) → Shopify (Products) → OpenAI (TTS)        │
└─────────────────────────────────────────────────────────┘
```

---

## Prerequisites

- Supabase account with Edge Functions enabled
- Google AI API key (Gemini)
- OpenAI API key (TTS)
- Shopify store with products

---

## Environment Variables

### Supabase Edge Functions

Set in Supabase Dashboard > Edge Functions > Secrets:

```env
# AI
GOOGLE_AI_API_KEY=xxx
OPENAI_API_KEY=xxx

# Shopify
SHOPIFY_STORE_URL=gatoaocubo.myshopify.com
SHOPIFY_ACCESS_TOKEN=xxx

# Optional
ELEVENLABS_API_KEY=xxx
```

---

## Frontend Setup

### 1. Chat Component

Located at: `src/components/RoChat.tsx`

Key props:
```typescript
interface RoChatProps {
  isOpen: boolean;
  onClose: () => void;
  initialMessage?: string;
}
```

### 2. Hook Configuration

Located at: `src/hooks/useRonronalda.ts`

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
| `ronronalda-chat` | Main conversation | POST /ronronalda-chat |
| `ronronalda-recommendations` | Product matching | POST /ronronalda-recommendations |
| `ronronalda-tts` | Text-to-speech | POST /ronronalda-tts |

### Deploy Functions

```bash
# Deploy all
supabase functions deploy

# Deploy specific
supabase functions deploy ronronalda-chat
```

---

## Knowledge Base

### Structure

```
ronronalda_agent/
├── knowledge/
│   └── core/
│       └── identidade.md    # Fixed identity
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
  'https://your-project.supabase.co/functions/v1/ronronalda-chat' \
  -H 'Authorization: Bearer YOUR_ANON_KEY' \
  -H 'Content-Type: application/json' \
  -d '{"message": "Meu gato arranha o sofa"}'
```

### In Claude Code

```bash
/prime-ronronalda
/ro-test "Meu gato arranha o sofa"
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

Edit: `ronronalda_agent/knowledge/core/identidade.md`

### Adding New Issues

1. Add keywords to detection system
2. Map to product category
3. Create response templates

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Chat not responding | Check Edge Function logs |
| Wrong products | Verify Shopify integration |
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
**Last Updated**: 2025-11-29
