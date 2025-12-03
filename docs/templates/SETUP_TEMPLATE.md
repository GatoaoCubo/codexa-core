# {{PROJECT_NAME}} Setup Guide

> **Universal installer for new PCs, new users, and maintenance**
>
> Template Version: 1.0.0 | Last Updated: {{LAST_UPDATED}}

---

## Quick Start (TL;DR)

```{{SHELL_TYPE}}
# 1. Clone
git clone {{GITHUB_REPO}}
cd {{PROJECT_NAME}}

# 2. Setup (installs everything)
node {{SETUP_SCRIPT}}

# 3. Start
{{START_COMMAND}}
```

---

## Configuration Variables

Before using this template, customize these values for YOUR installation:

| Variable | Your Value | Description |
|----------|-----------|-------------|
| `{{PROJECT_NAME}}` | | Project/repository name |
| `{{GITHUB_REPO}}` | | Git repository URL |
| `{{PROJECT_ROOT}}` | | Local installation path |
| `{{OS_TYPE}}` | Windows/macOS/Linux | Operating system |
| `{{SHELL_TYPE}}` | powershell/bash/zsh | Terminal shell |
| `{{PACKAGE_MANAGER}}` | winget/brew/apt-get | System package manager |
| `{{USER_HOME}}` | ~/.{{PROJECT_NAME}} | Credentials directory |
| `{{DASHBOARD_PORT}}` | 3333 | Web dashboard port |
| `{{VOICE_PORT}}` | 5000 | Voice server port (if applicable) |

---

## 1. Prerequisites

### Required Tools

| Tool | Min Version | Purpose | Check Command |
|------|-------------|---------|---------------|
| **Node.js** | {{NODE_MIN_VERSION}} | MCP servers, dashboard | `node --version` |
| **Python** | {{PYTHON_MIN_VERSION}} | Backend, agents | `python --version` |
| **uv** | {{UV_MIN_VERSION}} | Fast Python runner | `uv --version` |
| **Git** | {{GIT_MIN_VERSION}} | Version control | `git --version` |

### Optional Tools

| Tool | Purpose | Check Command |
|------|---------|---------------|
| **FFmpeg** | Video/audio processing | `ffmpeg -version` |
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

## 2. Clone & Setup Project

### Step 1: Clone Repository

```bash
git clone {{GITHUB_REPO}}
cd {{PROJECT_NAME}}
```

### Step 2: Run Smart Installer

```bash
node {{SETUP_SCRIPT}}
```

This will:
1. Check all prerequisites (Node.js, Python, uv, Git, FFmpeg)
2. Install NPM packages for all servers
3. Install Python packages
4. Configure settings
5. Prompt for API keys (stored in `{{USER_HOME}}/credentials.json`)

### Setup Command Options

| Command | Purpose |
|---------|---------|
| `node {{SETUP_SCRIPT}}` | Full interactive setup |
| `node {{SETUP_SCRIPT}} --check` | Health check only (no changes) |
| `node {{SETUP_SCRIPT}} --repair` | Fix issues automatically |
| `node {{SETUP_SCRIPT}} --apis` | Configure API keys only |
| `node {{SETUP_SCRIPT}} --help` | Show help |

---

## 3. API Keys Configuration

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
| `SUPABASE_URL` | Database | https://supabase.com/dashboard |
| `SUPABASE_SERVICE_ROLE_KEY` | Database admin | https://supabase.com/dashboard |
| `GITHUB_PAT` | Automation workflows | https://github.com/settings/tokens |

### Where Keys are Stored

```
{{USER_HOME}}/                    # User home (persistent)
├── config.json                   # Global settings
└── credentials.json              # API keys

{{PROJECT_ROOT}}/
├── .claude/settings.json         # Server config
└── {{ENV_FILE}}                  # Project environment
```

---

## 4. Running {{PROJECT_NAME}}

### Standard Mode (with permissions)

```bash
{{RUN_COMMAND}}
```
- Asks for confirmation before dangerous operations
- Recommended for learning and debugging

### Autonomous Mode (skip permissions)

```bash
{{RUN_COMMAND_FAST}}
```
- Faster, no confirmations
- Recommended for daily use

### Health Check

```bash
{{HEALTH_CHECK_COMMAND}}
```

---

## 5. Shell Shortcuts

The setup creates shortcuts in your shell profile:

| Shortcut | Command | Purpose |
|----------|---------|---------|
| `{{SHORTCUT_FAST}}` | `{{RUN_COMMAND_FAST}}` | Start (fast) |
| `{{SHORTCUT_STANDARD}}` | `{{RUN_COMMAND}}` | Start (standard) |
| `{{SHORTCUT_CHECK}}` | `node {{SETUP_SCRIPT}} --check` | Health check |
| `{{SHORTCUT_REPAIR}}` | `node {{SETUP_SCRIPT}} --repair` | Auto-fix issues |
| `{{SHORTCUT_GOTO}}` | `cd {{PROJECT_ROOT}}` | Navigate to project |

### Activate Shortcuts

```{{SHELL_TYPE}}
# Reload profile (or restart terminal)
{{RELOAD_PROFILE_CMD}}
```

---

## 6. Servers Reference

### Servers Overview

| Server | Language | Port | Purpose |
|--------|----------|------|---------|
{{#SERVERS}}
| **{{SERVER_NAME}}** | {{SERVER_LANG}} | {{SERVER_PORT}} | {{SERVER_PURPOSE}} |
{{/SERVERS}}

### Manual Server Testing

```bash
{{#SERVERS}}
# Test {{SERVER_NAME}}
{{SERVER_TEST_CMD}}

{{/SERVERS}}
```

---

## 7. Troubleshooting

### "Server failed to start"

```bash
# Run repair
node {{SETUP_SCRIPT}} --repair

# Or manually fix
cd {{SERVER_DIR}}
rm -rf node_modules
npm install

# Restart
```

### "Dependencies not working"

```bash
# Check versions
{{CHECK_VERSIONS_CMD}}

# Reinstall
{{REINSTALL_CMD}}
```

### "No API responses"

Configure at least one API key:
```bash
node {{SETUP_SCRIPT}} --apis
```

Or set environment variable:
```{{SHELL_TYPE}}
{{SET_ENV_CMD}} ANTHROPIC_API_KEY="sk-ant-..."
```

### "Permission denied" errors

- **Windows**: Run terminal as Administrator
- **Linux/Mac**: Use `sudo` for system-level operations

---

## 8. Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│                    {{PROJECT_NAME}} QUICK REFERENCE         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SETUP (Terminal, outside app):                             │
│  ─────────────────────────────────                          │
│  node {{SETUP_SCRIPT}}           # Full setup               │
│  node {{SETUP_SCRIPT}} --check   # Health check             │
│  node {{SETUP_SCRIPT}} --repair  # Fix issues               │
│  node {{SETUP_SCRIPT}} --apis    # Configure API keys       │
│                                                             │
│  START:                                                     │
│  ──────────────                                             │
│  {{SHORTCUT_FAST}}               # Autonomous (fast)        │
│  {{SHORTCUT_STANDARD}}           # Standard (with prompts)  │
│                                                             │
│  DASHBOARD:                                                 │
│  ──────────                                                 │
│  {{DASHBOARD_START_CMD}}         # Start dashboard          │
│  http://localhost:{{DASHBOARD_PORT}}  # Dashboard URL       │
│                                                             │
│  TROUBLESHOOTING:                                           │
│  ────────────────                                           │
│  {{SHORTCUT_CHECK}}              # Quick health check       │
│  {{SHORTCUT_REPAIR}}             # Auto-fix issues          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 9. Directory Structure

```
{{PROJECT_ROOT}}/
├── {{SETUP_SCRIPT}}                 # Smart installer
├── {{DASHBOARD_START_SCRIPT}}       # Dashboard starter
├── SETUP.md                         # This file (hydrated)
├── {{INSTRUCTIONS_FILE}}            # Auto-loaded instructions
│
├── {{CONFIG_DIR}}/
│   ├── settings.json                # Server config
│   ├── commands/                    # Slash commands
│   └── hooks/                       # Security hooks
│
├── {{SERVERS_DIR}}/
│   └── [server directories]         # Individual servers
│
└── {{APP_DIR}}/
    └── [application files]          # Main application
```

---

## Hydration Instructions

To use this template for YOUR project:

1. Copy this file to your project
2. Find and replace all `{{PLACEHOLDER}}` values with your specifics
3. Remove sections that don't apply
4. Add project-specific sections as needed

### Required Replacements

```
{{PROJECT_NAME}}      → Your project name
{{GITHUB_REPO}}       → Your git URL
{{SETUP_SCRIPT}}      → Your setup script name
{{RUN_COMMAND}}       → Your run command
{{RUN_COMMAND_FAST}}  → Your fast run command
```

### Optional Replacements

```
{{DASHBOARD_PORT}}    → Default: 3333
{{VOICE_PORT}}        → Default: 5000
{{NODE_MIN_VERSION}}  → Default: 18.0.0
{{PYTHON_MIN_VERSION}} → Default: 3.10.0
```

---

## Version

- **Template Version**: 1.0.0
- **Last Updated**: {{LAST_UPDATED}}
- **Tested On**: Windows 11, macOS, Ubuntu 22.04
- **Source**: Distilled from CODEXA installation experience

---

*This template follows the Distillation Principle: universal, reusable, brand-agnostic.*
