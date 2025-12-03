# CODEXA API Keys Reference

> Complete guide to all API keys, where they're stored, and how they're used

---

## Quick Summary

| Priority | Key | Required? | Used By |
|----------|-----|-----------|---------|
| **Critical** | `ANTHROPIC_API_KEY` | At least 1 | All agents, Claude Code |
| **Critical** | `OPENAI_API_KEY` | At least 1 | Alternative LLM |
| **Critical** | `GOOGLE_API_KEY` | At least 1 | Gemini, Imagen |
| Optional | `ELEVENLABS_API_KEY` | No | voice, video_agent |
| Optional | `SUPABASE_URL` | No | anuncio_agent |
| Optional | `SUPABASE_SERVICE_ROLE_KEY` | No | anuncio_agent |
| Optional | `RUNWAY_API_KEY` | No | video_agent |
| Optional | `PIKA_API_KEY` | No | video_agent |
| Optional | `GITHUB_PAT` | No | ADW workflows |

---

## 1. LLM Providers (Required: at least one)

### Anthropic Claude

```
Key: ANTHROPIC_API_KEY
Format: sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Get at: https://console.anthropic.com
Used by: All agents, primary LLM
```

### OpenAI GPT

```
Key: OPENAI_API_KEY
Format: sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Get at: https://platform.openai.com/api-keys
Used by: Alternative LLM, embeddings
```

### Google Gemini/Imagen

```
Key: GOOGLE_API_KEY
Format: AIzaSy... (39 chars)
Get at: https://aistudio.google.com/app/apikey
Used by: photo_agent (Imagen), Gemini LLM
```

**Related Settings:**
```env
GOOGLE_IMAGEN_MODEL=imagen-3.0-generate-001
GOOGLE_GEMINI_MODEL=gemini-2.0-flash-exp
GOOGLE_API_TIMEOUT=30
MAX_IMAGE_SIZE_MB=10
```

---

## 2. Voice & Audio (Optional)

### ElevenLabs

```
Key: ELEVENLABS_API_KEY
Format: el_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Get at: https://elevenlabs.io
Used by: voice server, video_agent TTS
Fallback: Local pyttsx3 (free, lower quality)
```

**Related Settings:**
```env
ELEVENLABS_DEFAULT_VOICE_ID=pMsXgVXv3BLzUgSXRplE
ELEVENLABS_MODEL_ID=eleven_multilingual_v2
VOICE_PORT=5000
VOICE_LANGUAGE=pt-BR
```

---

## 3. Video Generation (Optional)

### Runway

```
Key: RUNWAY_API_KEY
Format: rw_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Get at: https://runwayml.com
Used by: video_agent (primary)
```

### Pika

```
Key: PIKA_API_KEY
Format: pk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Get at: https://pika.art
Used by: video_agent (fallback)
```

**Related Settings:**
```env
VIDEO_AGENT_DEBUG=false
VIDEO_AGENT_LOG_LEVEL=INFO
VIDEO_AGENT_MAX_COST_PER_VIDEO=5.00
VIDEO_AGENT_DAILY_COST_LIMIT=50.00
```

---

## 4. Database (Optional)

### Supabase

```
Key: SUPABASE_URL
Format: https://xxxxx.supabase.co
Get at: https://supabase.com/dashboard
Used by: anuncio_agent (product database)

Key: SUPABASE_SERVICE_ROLE_KEY
Format: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Get at: Project Settings > API
Used by: anuncio_agent (admin writes)

Key: SUPABASE_ANON_KEY
Format: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Get at: Project Settings > API
Used by: Public read access
```

---

## 5. Cloud Storage (Optional)

### AWS S3

```
Key: AWS_ACCESS_KEY_ID
Format: AKIAXXXXXXXXXXXX
Get at: AWS IAM Console
Used by: video_agent (output storage)

Key: AWS_SECRET_ACCESS_KEY
Format: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Get at: AWS IAM Console

Key: AWS_S3_BUCKET
Default: video-agent-outputs

Key: AWS_REGION
Default: us-east-1
```

---

## 6. Development & Automation (Optional)

### GitHub

```
Key: GITHUB_PAT
Format: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Get at: https://github.com/settings/tokens
Used by: ADW workflows, CI/CD automation
Scopes needed: repo, workflow
```

### E2B (Code Sandbox)

```
Key: E2B_API_KEY
Format: e2b_xxxxxxxxxxxxxxxxxxxxx
Get at: https://e2b.dev
Used by: Code execution sandbox
```

---

## Storage Locations

### Primary (Recommended)

```
~/.codexa/
├── config.json          # Global settings
└── credentials.json     # API keys (persistent)
```

### Project-Level

```
codexa-core/
├── codexa.app/.env      # Project environment (gitignored)
└── app/server/.env      # Backend environment (gitignored)
```

### Templates (Reference Only)

```
codexa.app/.env.example
codexa.app/agentes/video_agent/.env.example
codexa.app/agentes/pesquisa_agent/.env.example
app/server/.env.sample
```

---

## How to Configure

### Method 1: Interactive Setup (Recommended)

```bash
node setup-codexa.js --apis
```

### Method 2: Environment Variables

**PowerShell (Session):**
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

**PowerShell (Permanent):**
```powershell
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-...", "User")
```

**Bash:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Method 3: .env File

```bash
# Copy template
cp codexa.app/.env.example codexa.app/.env

# Edit with your keys
notepad codexa.app/.env
```

---

## Loading Priority

Keys are loaded in this order (first found wins):

1. **Environment variables** (system-level)
2. **~/.codexa/credentials.json** (user-level)
3. **Project .env files** (project-level)
4. **Defaults** (if applicable)

---

## Verification

### Check via Setup Script

```bash
node setup-codexa.js --check
```

### Check via Claude Code

```
/codexa-init --apis
```

### Check via Python

```python
python codexa.app/config/secrets.py
```

---

## Security Best Practices

### DO

- Store keys in `~/.codexa/credentials.json` (not in project)
- Use environment variables for CI/CD
- Rotate keys periodically
- Use different keys for dev/prod

### DON'T

- Commit `.env` files to git
- Share keys in chat or docs
- Log actual key values
- Use production keys for testing

---

## Troubleshooting

### "No LLM key configured"

```bash
# Set at least one
export ANTHROPIC_API_KEY="sk-ant-..."
# or
node setup-codexa.js --apis
```

### "Invalid API key"

- Check for extra spaces or quotes
- Verify key hasn't expired
- Confirm correct key format

### "Voice not working"

```bash
# Falls back to local TTS if no ElevenLabs key
# This is normal - premium voices require the key
```

### "Database connection failed"

```bash
# Verify Supabase URL and keys
echo $SUPABASE_URL
echo $SUPABASE_SERVICE_ROLE_KEY
```

---

## Cost Estimates

| Service | Free Tier | Typical Usage |
|---------|-----------|---------------|
| Anthropic Claude | $5 credit | ~R$ 50-100/month |
| OpenAI | $5 credit | ~R$ 30-80/month |
| Google AI | Free tier | ~R$ 0-20/month |
| ElevenLabs | Limited free | ~R$ 25-50/month |
| Supabase | 500MB free | R$ 0 (hobby) |

---

**Version**: 1.0.0 | **Updated**: 2025-12-02
