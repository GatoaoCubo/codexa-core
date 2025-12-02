# /codexa-init - System Health Check & Repair

## PURPOSE
Universal health check and repair command for CODEXA system. Use this when:
- Starting a new session to verify everything works
- After git pull to check for new dependencies
- When MCP servers fail to load
- When features aren't working as expected

## USAGE
```
/codexa-init              # Full health check
/codexa-init --repair     # Fix issues automatically
/codexa-init --apis       # Check API keys status
```

## EXECUTION

### Step 1: Run Health Check

Execute the following command to check system status:

```bash
node setup-codexa.js --check
```

The output will show:
- **Prerequisites**: Node.js, Python, uv, Git, FFmpeg
- **NPM Packages**: scout-mcp, codexa-commands, browser-mcp, launcher
- **MCP Servers**: scout, codexa-commands, browser, voice
- **API Keys**: ANTHROPIC, OPENAI, GOOGLE, ELEVENLABS, SUPABASE

### Step 2: Interpret Results

| Status | Meaning | Action |
|--------|---------|--------|
| `[OK]` | Working correctly | No action needed |
| `[Issues]` | Problems found | Run --repair |
| `[Partial]` | Some features unavailable | Optional fix |
| `[No LLM key]` | No AI provider configured | Configure API key |

### Step 3: Auto-Repair (if needed)

If issues are found, run:

```bash
node setup-codexa.js --repair
```

This will:
1. Reinstall broken NPM dependencies
2. Update MCP server configurations
3. Refresh Python packages

### Step 4: API Key Configuration

If API keys are missing:

```bash
node setup-codexa.js --apis
```

Required keys (at least one):
- `ANTHROPIC_API_KEY` - https://console.anthropic.com
- `OPENAI_API_KEY` - https://platform.openai.com
- `GOOGLE_API_KEY` - https://aistudio.google.com

## COMMON ISSUES

### "1 MCP server failed"
Run repair and restart Claude Code:
```bash
node setup-codexa.js --repair
# Then restart Claude Code
```

### "scout-mcp not loading"
Reinstall dependencies:
```bash
cd codexa.app/mcp-servers/scout-mcp
rm -rf node_modules
npm install
```

### "voice server not working"
Check Python and uv:
```bash
uv --version
python --version
uv run codexa.app/voice/server.py --help
```

### "No LLM responses"
Configure at least one API key in `~/.codexa/credentials.json` or environment variables.

## OUTPUT FORMAT

After running, provide a structured report:

```
CODEXA HEALTH CHECK
==================

Prerequisites:
  - Node.js: [version or NOT INSTALLED]
  - Python: [version or NOT INSTALLED]
  - uv: [version or NOT INSTALLED]
  - Git: [version or NOT INSTALLED]
  - FFmpeg: [version or NOT INSTALLED (optional)]

NPM Packages:
  - scout-mcp: [Installed/Not installed]
  - codexa-commands: [Installed/Not installed]
  - browser-mcp: [Installed/Not installed]
  - launcher: [Installed/Not installed]

MCP Servers:
  - scout: [Ready/Entry not found]
  - codexa-commands: [Ready/Entry not found]
  - browser: [Ready/Entry not found]
  - voice: [Ready/Entry not found]

API Keys:
  - ANTHROPIC_API_KEY: [Configured/Not set]
  - OPENAI_API_KEY: [Configured/Not set]
  - GOOGLE_API_KEY: [Configured/Not set]
  - ELEVENLABS_API_KEY: [Configured/Not set]

Status: [OK / NEEDS REPAIR / CRITICAL]
Action: [None needed / Run --repair / Manual intervention required]
```

## NOTES

- This command is **idempotent** - safe to run multiple times
- Configuration is stored in `~/.codexa/` (persists across projects)
- Project-specific config in `.claude/settings.json`
- After repair, **restart Claude Code** to reload MCP servers
