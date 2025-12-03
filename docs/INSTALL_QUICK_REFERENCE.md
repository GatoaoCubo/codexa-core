# CODEXA Installation Quick Reference

> One-page guide for setting up a new Windows development environment

---

## Tools Installation (Windows)

### Via PowerShell (Admin)

```powershell
# Core Tools (Required)
winget install OpenJS.NodeJS.LTS      # Node.js 24.x
winget install Python.Python.3.12      # Python 3.12
winget install Git.Git                 # Git 2.52+
winget install GitHub.cli              # GitHub CLI

# Python Tools
pip install uv                         # Or: irm astral.sh/uv/install.ps1 | iex

# JavaScript Tools
npm install -g @anthropic-ai/claude-code  # Claude Code CLI

# Optional
winget install FFmpeg                  # Video processing
irm bun.sh/install.ps1 | iex          # Bun runtime
```

### Verify Installation

```powershell
node --version      # v24.x.x
python --version    # 3.12.x
uv --version        # 0.9.x
git --version       # 2.52.x
gh --version        # 2.83.x
npm --version       # 11.x.x
```

---

## PATH Locations (Windows)

| Tool | Default Path |
|------|-------------|
| Python | `C:\Users\{USER}\AppData\Local\Programs\Python\Python312\` |
| UV | `C:\Users\{USER}\.local\bin\` |
| Bun | `C:\Users\{USER}\.bun\bin\` |
| Node.js | `C:\Program Files\nodejs\` |
| Git | `C:\Program Files\Git\cmd\` |
| GitHub CLI | `C:\Program Files\GitHub CLI\` |
| npm global | `C:\Users\{USER}\AppData\Roaming\npm\` |

---

## Shell Shortcuts Setup

### PowerShell Profile

```powershell
# Add to $PROFILE (run: notepad $PROFILE)

function Start-ClaudeAdmin {
    Start-Process powershell -Verb RunAs -ArgumentList "-NoExit -Command cd '$PWD'; claude --dangerously-skip-permissions"
}
Set-Alias cc-admin Start-ClaudeAdmin

function Start-PSAdmin {
    Start-Process powershell -Verb RunAs -ArgumentList "-NoExit -Command cd '$PWD'"
}
Set-Alias admin Start-PSAdmin

function Start-Claude {
    claude --dangerously-skip-permissions
}
Set-Alias cc Start-Claude

function Go-Codexa {
    Set-Location 'C:\Users\PC\Documents\GitHub\codexa-core'
}
Set-Alias codexa Go-Codexa
```

### Git Bash (~/.bashrc)

```bash
# Add to ~/.bashrc

alias cc-admin='powershell -Command "Start-Process powershell -Verb RunAs -ArgumentList \"-NoExit -Command cd '\''$(pwd)'\''; claude --dangerously-skip-permissions\""'
alias admin='powershell -Command "Start-Process powershell -Verb RunAs -ArgumentList \"-NoExit -Command cd '\''$(pwd)'\''\""'
alias cc='claude --dangerously-skip-permissions'
alias codexa='cd /c/Users/PC/Documents/GitHub/codexa-core'
```

---

## CODEXA Project Setup

```bash
# 1. Clone
git clone https://github.com/GatoaoCubo/codexa-core.git
cd codexa-core

# 2. Run installer
node setup-codexa.js

# 3. Install MCP dependencies (if needed)
cd codexa.app/mcp-servers/scout-mcp && npm install
cd ../codexa-commands && npm install
cd ../browser-mcp && npm install
cd ../../launcher && npm install
cd ../../..

# 4. Start Claude Code
claude --dangerously-skip-permissions
```

---

## API Keys

### Required (at least 1)

| Key | Where to Get |
|-----|--------------|
| `ANTHROPIC_API_KEY` | https://console.anthropic.com |
| `OPENAI_API_KEY` | https://platform.openai.com |
| `GOOGLE_API_KEY` | https://aistudio.google.com |

### Where to Store

```
~/.codexa/credentials.json    # Persistent (recommended)
codexa.app/.env               # Project-specific
Environment variables         # System-wide
```

### Set via Environment

```powershell
# PowerShell (session)
$env:ANTHROPIC_API_KEY = "sk-ant-..."

# PowerShell (permanent)
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-...", "User")
```

---

## MCP Servers Status

| Server | Command | Purpose |
|--------|---------|---------|
| scout | `node codexa.app/mcp-servers/scout-mcp/index.js` | File discovery |
| codexa-commands | `node codexa.app/mcp-servers/codexa-commands/index.js` | Slash commands |
| browser | `node codexa.app/mcp-servers/browser-mcp/index.js` | Web automation |
| voice | `uv run codexa.app/voice/server.py` | Speech TTS |

---

## Health Check

```bash
# Full check
node setup-codexa.js --check

# Inside Claude Code
/codexa-init
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Python not found` | Add to PATH or use full path |
| `uv not found` | `irm astral.sh/uv/install.ps1 \| iex` |
| `MCP server failed` | `node setup-codexa.js --repair` |
| `npm install fails` | `npm cache clean --force` then retry |
| `Permission denied` | Run terminal as Administrator |
| `WSL2 not working` | Enable Hyper-V in BIOS/UEFI |

---

## WSL2 Setup (Optional)

```powershell
# PowerShell as Admin
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
Restart-Computer

# After restart
wsl --install -d Ubuntu
```

---

## Quick Commands Cheat Sheet

```
┌────────────────────────────────────────────────────────┐
│ COMMAND           │ ACTION                             │
├───────────────────┼────────────────────────────────────┤
│ cc                │ Start Claude Code (fast)           │
│ cc-admin          │ Start Claude Code as Admin         │
│ admin             │ Open PowerShell as Admin           │
│ codexa            │ Go to codexa-core folder           │
│ codexa-check      │ Run health check                   │
│ codexa-repair     │ Auto-fix issues                    │
└────────────────────────────────────────────────────────┘
```

---

**Version**: 1.0.0 | **Updated**: 2025-12-02 | **Source**: Live installation session
