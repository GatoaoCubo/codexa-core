# CODEXA Setup Guide

## Quick Start (TL;DR)

```bash
# 1. Clone
git clone https://github.com/GatoaoCubo/codexa-core.git
cd codexa-core

# 2. Setup (instala tudo)
node setup-codexa.js

# 3. Start Claude Code
claude
```

---

## Full Setup for New PC

### Step 1: Install Prerequisites

#### Windows (PowerShell as Admin)
```powershell
winget install OpenJS.NodeJS.LTS
winget install Python.Python.3.12
winget install Git.Git
pip install uv
```

#### macOS
```bash
brew install node python@3.12 git
pip install uv
```

#### Linux (Ubuntu/Debian)
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs python3.12 git
pip install uv
```

### Step 2: Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

First time login:
```bash
claude
# Opens browser for authentication
```

### Step 3: Clone Project

```bash
git clone https://github.com/GatoaoCubo/codexa-core.git
cd codexa-core
```

### Step 4: Run Smart Installer

```bash
node setup-codexa.js
```

This will:
1. Check all prerequisites (Node.js, Python, uv, Git, FFmpeg)
2. Install NPM packages for all MCP servers
3. Install Python packages (voice, agents)
4. Configure `.claude/settings.json`
5. Prompt for API keys (stored in `~/.codexa/credentials.json`)

### Step 5: Start Claude Code

```bash
claude
```

All 4 MCP servers should load:
- `scout` - File discovery
- `codexa-commands` - Slash commands
- `browser` - Web automation
- `voice` - Speech-to-text/Text-to-speech

### Step 6: Verify Inside Claude Code

```
/codexa-init
```

---

## Setup Commands Reference

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `node setup-codexa.js` | Full interactive setup | New PC or new user |
| `node setup-codexa.js --check` | Health check only | Verify status |
| `node setup-codexa.js --repair` | Fix issues automatically | After errors |
| `node setup-codexa.js --apis` | Configure API keys only | Add/change keys |
| `node setup-codexa.js --help` | Show help | Reference |

---

## Running Claude Code

### Standard Mode (Recommended for Development)
```bash
claude
```
- Asks for permission before dangerous operations
- Safe for learning and experimenting

### Autonomous Mode (For Experienced Users)
```bash
claude --dangerously-skip-permissions
```
- Skips all permission prompts
- Faster for repetitive tasks
- **Use only if you trust the codebase**

### When to Use Each Mode

| Mode | Use Case | Risk Level |
|------|----------|------------|
| Standard | Development, debugging, learning | Low |
| `--dangerously-skip-permissions` | Automation, CI/CD, trusted scripts | Medium |

---

## Configuration Files

### User-Level (Persistent across projects)
```
~/.codexa/
├── config.json         # Global settings
└── credentials.json    # API keys (ANTHROPIC, OPENAI, etc.)
```

### Project-Level
```
codexa-core/
├── .claude/settings.json    # MCP servers config
├── .claude/commands/        # Slash commands
├── .claude/hooks/           # Pre/post tool hooks
└── codexa.app/.env          # Environment variables
```

---

## API Keys

### Required (at least one)
| Key | Service | Get it at |
|-----|---------|-----------|
| `ANTHROPIC_API_KEY` | Claude API | https://console.anthropic.com |
| `OPENAI_API_KEY` | OpenAI API | https://platform.openai.com |
| `GOOGLE_API_KEY` | Gemini API | https://aistudio.google.com |

### Optional (for specific features)
| Key | Feature | Get it at |
|-----|---------|-----------|
| `ELEVENLABS_API_KEY` | Premium voice | https://elevenlabs.io |
| `SUPABASE_URL` | Database publishing | https://supabase.com |
| `SUPABASE_SERVICE_ROLE_KEY` | Database admin | https://supabase.com |
| `RUNWAY_API_KEY` | Video generation | https://runwayml.com |

---

## Troubleshooting

### "1 MCP server failed"
```bash
node setup-codexa.js --repair
# Then restart Claude Code
```

### "scout-mcp not loading"
```bash
cd codexa.app/mcp-servers/scout-mcp
rm -rf node_modules
npm install
```

### "No LLM responses"
Configure at least one API key:
```bash
node setup-codexa.js --apis
```

### "Permission denied" errors
Run terminal as Administrator (Windows) or use sudo (Linux/Mac)

---

## Directory Structure

```
codexa-core/
├── setup-codexa.js              # Smart installer (run this first!)
├── start-codexa.bat             # Start dashboard (Windows)
├── start-codexa.sh              # Start dashboard (Linux/Mac)
├── .claude/
│   ├── settings.json            # MCP servers config
│   ├── commands/                # 27+ slash commands
│   └── hooks/                   # Security & notification hooks
├── codexa.app/
│   ├── mcp-servers/
│   │   ├── scout-mcp/           # File discovery
│   │   ├── codexa-commands/     # Command discovery
│   │   ├── browser-mcp/         # Web automation
│   │   └── voice/               # Speech services
│   ├── agentes/                 # Domain agents
│   └── launcher/                # Visual dashboard
└── CLAUDE.md                    # Auto-loaded instructions
```

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│                    CODEXA QUICK REFERENCE                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SETUP (Terminal, outside Claude):                          │
│  ─────────────────────────────────                          │
│  node setup-codexa.js           # Full setup                │
│  node setup-codexa.js --check   # Health check              │
│  node setup-codexa.js --repair  # Fix issues                │
│                                                             │
│  START CLAUDE:                                              │
│  ──────────────                                             │
│  claude                         # Standard mode             │
│  claude --dangerously-skip-permissions  # Autonomous        │
│                                                             │
│  INSIDE CLAUDE CODE:                                        │
│  ───────────────────                                        │
│  /codexa-init                   # Health check              │
│  /codexa                        # Main orchestrator         │
│  /prime                         # System status             │
│                                                             │
│  DASHBOARD:                                                 │
│  ──────────                                                 │
│  start-codexa.bat               # Windows                   │
│  ./start-codexa.sh              # Linux/Mac                 │
│  http://localhost:3333          # Dashboard URL             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Version

- **Setup Script**: v2.0
- **Last Updated**: 2025-12-02
- **Tested On**: Windows 11, Node.js 24.x, Python 3.14
