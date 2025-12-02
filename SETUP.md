# CODEXA Setup Guide

> **Universal installer for new PCs, new users, and maintenance**

## Quick Start (TL;DR)

```bash
# 1. Clone
git clone https://github.com/GatoaoCubo/codexa-core.git
cd codexa-core

# 2. Setup (installs everything)
node setup-codexa.js

# 3. Start Claude Code
claude --dangerously-skip-permissions
```

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Install Claude Code](#2-install-claude-code)
3. [Clone & Setup Project](#3-clone--setup-project)
4. [API Keys Configuration](#4-api-keys-configuration)
5. [Running Claude Code](#5-running-claude-code)
6. [PowerShell Shortcuts](#6-powershell-shortcuts)
7. [MCP Servers Reference](#7-mcp-servers-reference)
8. [Dependencies Reference](#8-dependencies-reference)
9. [Troubleshooting](#9-troubleshooting)
10. [Quick Reference Card](#10-quick-reference-card)

---

## 1. Prerequisites

### Required Tools

| Tool | Min Version | Purpose | Check Command |
|------|-------------|---------|---------------|
| **Node.js** | 18.0.0 | MCP servers, dashboard | `node --version` |
| **Python** | 3.10.0 | Voice server, agents | `python --version` |
| **uv** | 0.1.0 | Fast Python runner | `uv --version` |
| **Git** | 2.0.0 | Version control | `git --version` |

### Optional Tools

| Tool | Purpose | Check Command |
|------|---------|---------------|
| **FFmpeg** | Video generation (video_agent) | `ffmpeg -version` |
| **Docker** | Containerized deployment | `docker --version` |

### Installation by Platform

#### Windows (PowerShell as Admin)

```powershell
# Required
winget install OpenJS.NodeJS.LTS
winget install Python.Python.3.12
winget install Git.Git
pip install uv

# Optional
winget install FFmpeg
winget install Docker.DockerDesktop
```

#### macOS (Homebrew)

```bash
# Required
brew install node python@3.12 git
pip install uv

# Optional
brew install ffmpeg
brew install --cask docker
```

#### Linux (Ubuntu/Debian)

```bash
# Required
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs python3.12 python3-pip git
pip install uv

# Optional
sudo apt install ffmpeg
# Docker: https://docs.docker.com/engine/install/ubuntu/
```

---

## 2. Install Claude Code

```bash
# Install globally
npm install -g @anthropic-ai/claude-code

# First time login (opens browser)
claude
```

---

## 3. Clone & Setup Project

### Step 1: Clone Repository

```bash
git clone https://github.com/GatoaoCubo/codexa-core.git
cd codexa-core
```

### Step 2: Run Smart Installer

```bash
node setup-codexa.js
```

This will:
1. ✅ Check all prerequisites (Node.js, Python, uv, Git, FFmpeg)
2. ✅ Install NPM packages for all MCP servers
3. ✅ Install Python packages (voice, agents)
4. ✅ Configure `.claude/settings.json`
5. ✅ Prompt for API keys (stored in `~/.codexa/credentials.json`)

### Setup Command Options

| Command | Purpose |
|---------|---------|
| `node setup-codexa.js` | Full interactive setup |
| `node setup-codexa.js --check` | Health check only (no changes) |
| `node setup-codexa.js --repair` | Fix issues automatically |
| `node setup-codexa.js --apis` | Configure API keys only |
| `node setup-codexa.js --help` | Show help |

---

## 4. API Keys Configuration

### Required (at least one LLM provider)

| Key | Service | Get it at |
|-----|---------|-----------|
| `ANTHROPIC_API_KEY` | Claude API | https://console.anthropic.com |
| `OPENAI_API_KEY` | OpenAI/GPT | https://platform.openai.com/api-keys |
| `GOOGLE_API_KEY` | Google Gemini | https://aistudio.google.com/app/apikey |

### Optional (for specific features)

| Key | Feature | Get it at |
|-----|---------|-----------|
| `ELEVENLABS_API_KEY` | Premium voice TTS | https://elevenlabs.io |
| `SUPABASE_URL` | Database (anuncio_agent) | https://supabase.com/dashboard |
| `SUPABASE_SERVICE_ROLE_KEY` | Database admin | https://supabase.com/dashboard |
| `RUNWAY_API_KEY` | Video generation | https://runwayml.com |
| `PIKA_API_KEY` | Video generation (alt) | https://pika.art |
| `GITHUB_PAT` | ADW workflows | https://github.com/settings/tokens |

### Where Keys are Stored

```
~/.codexa/                    # User home (persistent)
├── config.json               # Global settings
└── credentials.json          # API keys

codexa-core/
├── .claude/settings.json     # MCP servers config
└── codexa.app/.env           # Project environment
```

---

## 5. Running Claude Code

### Standard Mode (with permissions)

```bash
claude
```
- Asks for confirmation before dangerous operations
- Recommended for learning and debugging

### Autonomous Mode (skip permissions)

```bash
claude --dangerously-skip-permissions
```
- Faster, no confirmations
- Safe for CODEXA (has security hooks)
- Recommended for daily use

### Health Check Inside Claude

```
/codexa-init
```

---

## 6. PowerShell Shortcuts

The setup creates shortcuts in your PowerShell profile:

| Shortcut | Command | Purpose |
|----------|---------|---------|
| `cc` | `claude --dangerously-skip-permissions` | Start Claude (fast) |
| `ccs` | `claude` | Start Claude (standard) |
| `codexa-check` | `node setup-codexa.js --check` | Health check |
| `codexa-repair` | `node setup-codexa.js --repair` | Auto-fix issues |
| `goto-codexa` | `cd codexa-core` | Navigate to project |

### Activate Shortcuts

```powershell
# Reload profile (or restart PowerShell)
. $PROFILE
```

---

## 7. MCP Servers Reference

### Servers Overview

| Server | Language | Port | Purpose |
|--------|----------|------|---------|
| **scout** | Node.js | stdio | File discovery, navigation |
| **codexa-commands** | Node.js | stdio | Slash command discovery |
| **browser** | Node.js | stdio | Web automation (Puppeteer) |
| **voice** | Python | 5000 | Speech-to-text, text-to-speech |

### Manual Server Testing

```bash
# Test scout-mcp
node codexa.app/mcp-servers/scout-mcp/index.js

# Test codexa-commands
node codexa.app/mcp-servers/codexa-commands/index.js

# Test browser-mcp
node codexa.app/mcp-servers/browser-mcp/index.js

# Test voice
uv run codexa.app/voice/server.py --help
```

---

## 8. Dependencies Reference

### NPM Packages by Component

#### scout-mcp
```json
{
  "@modelcontextprotocol/sdk": "^1.0.0",
  "glob": "^10.3.10",
  "minimatch": "^9.0.0"
}
```

#### codexa-commands
```json
{
  "@modelcontextprotocol/sdk": "^0.5.0",
  "glob": "^10.3.10",
  "minimatch": "^9.0.3"
}
```

#### browser-mcp
```json
{
  "@modelcontextprotocol/sdk": "^0.5.0",
  "puppeteer": "^24.31.0",
  "puppeteer-extra": "^3.3.6",
  "puppeteer-extra-plugin-stealth": "^2.11.2"
}
```

#### launcher (dashboard)
```json
{
  "express": "^4.18.2",
  "chalk": "^5.3.0",
  "ora": "^8.0.0",
  "boxen": "^7.1.1",
  "inquirer": "^9.2.12",
  "open": "^10.0.0"
}
```

### Python Packages by Component

#### voice (codexa.app/voice/requirements.txt)
```
sounddevice>=0.4.6
soundfile>=0.12.1
numpy>=1.24.0
edge-tts>=6.1.0
pyttsx3>=2.90
elevenlabs>=1.0.0
pygame>=2.5.0
python-dotenv>=1.0.0
mcp>=0.1.0
```

#### video_agent
```
anthropic>=0.28.0
httpx>=0.25.0
aiofiles>=23.2.0
python-dotenv>=1.0.0
pydantic>=2.5.0
elevenlabs>=0.3.0
ffmpeg-python>=0.2.0
Pillow>=10.0.0
rich>=13.0.0
tqdm>=4.66.0
tenacity>=8.2.0
```

#### codexa_agent
```
anthropic==0.45.0
openai==1.52.0
google-generativeai==0.8.3
python-dotenv==1.0.0
pyyaml==6.0.1
aiofiles==23.2.1
```

#### app/server (FastAPI backend)
```
fastapi>=0.115.13
uvicorn>=0.34.3
python-multipart>=0.0.20
openai>=1.3.0
anthropic>=0.50.0
pandas>=1.5.0
python-dotenv>=1.0.1
```

### Manual Installation Commands

```bash
# NPM packages (if setup-codexa.js fails)
cd codexa.app/mcp-servers/scout-mcp && npm install
cd codexa.app/mcp-servers/codexa-commands && npm install
cd codexa.app/mcp-servers/browser-mcp && npm install
cd codexa.app/launcher && npm install

# Python packages
uv pip install -r codexa.app/voice/requirements.txt
uv pip install -r codexa.app/agentes/video_agent/requirements.txt
uv pip install -r codexa.app/agentes/codexa_agent/requirements.txt
```

---

## 9. Troubleshooting

### "1 MCP server failed"

```bash
# Run repair
node setup-codexa.js --repair

# Or manually fix scout-mcp
cd codexa.app/mcp-servers/scout-mcp
rm -rf node_modules
npm install

# Restart Claude Code
```

### "scout-mcp not loading"

```bash
# Check if it runs manually
node codexa.app/mcp-servers/scout-mcp/index.js

# If error about zod-to-json-schema, reinstall
cd codexa.app/mcp-servers/scout-mcp
rm -rf node_modules package-lock.json
npm install
```

### "voice server not working"

```bash
# Check Python and uv
python --version   # Should be 3.10+
uv --version       # Should be installed

# Test voice server
uv run codexa.app/voice/server.py --help

# Install dependencies manually
uv pip install -r codexa.app/voice/requirements.txt
```

### "No LLM responses"

Configure at least one API key:
```bash
node setup-codexa.js --apis
```

Or set environment variable:
```bash
# Windows PowerShell
$env:ANTHROPIC_API_KEY = "sk-ant-..."

# Linux/Mac
export ANTHROPIC_API_KEY="sk-ant-..."
```

### "Permission denied" errors

- **Windows**: Run terminal as Administrator
- **Linux/Mac**: Use `sudo` for system-level operations

### "npm install fails"

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### "Python packages fail to install"

```bash
# Use pip directly instead of uv
pip install -r requirements.txt

# Or upgrade uv
pip install --upgrade uv
```

---

## 10. Quick Reference Card

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
│  node setup-codexa.js --apis    # Configure API keys        │
│                                                             │
│  START CLAUDE:                                              │
│  ──────────────                                             │
│  cc                             # Autonomous (fast)         │
│  ccs                            # Standard (with prompts)   │
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
│  MCP SERVERS:                                               │
│  ────────────                                               │
│  scout           # File discovery (1800+ files indexed)     │
│  codexa-commands # 46 slash commands                        │
│  browser         # Puppeteer web automation                 │
│  voice           # STT/TTS (port 5000)                      │
│                                                             │
│  TROUBLESHOOTING:                                           │
│  ────────────────                                           │
│  codexa-check                   # Quick health check        │
│  codexa-repair                  # Auto-fix issues           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
codexa-core/
├── setup-codexa.js              # Smart installer
├── start-codexa.bat             # Dashboard (Windows)
├── start-codexa.sh              # Dashboard (Linux/Mac)
├── SETUP.md                     # This file
├── CLAUDE.md                    # Auto-loaded instructions
│
├── .claude/
│   ├── settings.json            # MCP servers config
│   ├── commands/                # 27+ slash commands
│   │   ├── codexa.md
│   │   ├── codexa-init.md
│   │   ├── prime.md
│   │   └── ...
│   └── hooks/                   # Security hooks
│       ├── pre_tool_use.py
│       ├── notification.py
│       └── session_stop.py
│
├── codexa.app/
│   ├── mcp-servers/
│   │   ├── scout-mcp/           # File discovery
│   │   ├── codexa-commands/     # Command discovery
│   │   └── browser-mcp/         # Web automation
│   ├── voice/                   # Voice server (Python)
│   ├── agentes/                 # Domain agents
│   │   ├── anuncio_agent/
│   │   ├── codexa_agent/
│   │   ├── curso_agent/
│   │   ├── mentor_agent/
│   │   ├── pesquisa_agent/
│   │   ├── photo_agent/
│   │   ├── video_agent/
│   │   └── ...
│   └── launcher/                # Visual dashboard
│
└── app/
    ├── server/                  # FastAPI backend
    └── client/                  # Vite frontend
```

---

## Version

- **Setup Script**: v2.0
- **Last Updated**: 2025-12-02
- **Tested On**: Windows 11, Node.js 24.x, Python 3.14
- **Repository**: https://github.com/GatoaoCubo/codexa-core
