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

> **IMPORTANT**: Voice features work WITHOUT any API keys!
>
> The system uses:
> - **TTS**: Edge TTS (FREE) → ElevenLabs (premium) → pyttsx3 (offline)
> - **STT**: Local Whisper model (FREE, offline)
>
> Leave `ELEVENLABS_API_KEY` empty to use FREE Edge TTS + Whisper.

### ElevenLabs (Optional Premium TTS)

```
Key: ELEVENLABS_API_KEY
Format: el_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Get at: https://elevenlabs.io/app/settings/api-keys
Used by: voice server, video_agent TTS (optional)
Required: NO - system falls back to Edge TTS (free, online) or pyttsx3 (offline)
```

**TTS Fallback Chain:**
1. **Edge TTS** (FREE, online, good quality) - tried first
2. **ElevenLabs** (premium, optional) - only if API key configured
3. **pyttsx3** (FREE, offline, basic) - final fallback

**Related Settings:**
```env
# ElevenLabs (optional)
ELEVENLABS_API_KEY={YOUR_KEY_HERE}
ELEVENLABS_VOICE_ID=pMsXgVXv3BLzUgSXRplE
ELEVENLABS_MODEL_ID=eleven_multilingual_v2

# Voice server
VOICE_PORT=5000
VOICE_LANGUAGE=pt-BR

# TTS provider override (optional)
TTS_PROVIDER=auto  # auto, edge, elevenlabs, pyttsx3

# Edge TTS voice (free alternative)
EDGE_VOICE=pt-BR-FranciscaNeural
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

### Centralized Configuration (NEW)

All environment variables are now managed from a **single location**:

```
codexa-core/
├── .env.example         # Master template (ALL variables documented)
├── .env                 # Your actual config (gitignored)
└── codexa.app/config/
    └── env_loader.py    # Centralized loader module
```

### User-Level (Optional)

```
~/.codexa/
├── config.json          # Global settings
└── credentials.json     # API keys (persistent across projects)
```

### Python Usage

```python
# Import the centralized config
from config.env_loader import env, supabase, llm, voice

# Access LLM keys
api_key = llm.anthropic_key

# Access Supabase config
url = supabase.url
headers = supabase.get_headers(admin=True)

# Check configuration status
env.print_status()
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

### Method 3: .env File (Recommended)

```bash
# Copy the master template from project root
cp .env.example .env

# Edit with your keys
notepad .env    # Windows
# or
code .env       # VS Code
# or
nano .env       # Linux/WSL
```

**Important**: The `.env` file should be in the project root (`codexa-core/`), NOT inside `codexa.app/`.

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

### Check via Python (Recommended)

```bash
# Run the env_loader status check
python -c "from codexa.app.config.env_loader import env; env.print_status()"

# Or run directly
python codexa.app/config/env_loader.py
```

### Check via Claude Code

```
/codexa-init --apis
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

**Version**: 2.0.0 | **Updated**: 2025-12-03

---

## Changelog

- **v2.0.0** (2025-12-03): Centralized all config in single `.env.example` at project root. Added `env_loader.py` module. Removed individual agent .env files.
- **v1.0.0** (2025-12-02): Initial documentation
