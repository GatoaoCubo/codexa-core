# Claude Code Custom Commands

Custom slash commands for CODEXA system workflows and operations.

**Total Commands**: 26 | **Version**: 2.0.0 | **Updated**: 2025-12-02

---

## Command Categories

### Navigation (2 commands)
| Command | Description |
|---------|-------------|
| `/prime` | System navigator - routes to appropriate agent |
| `/adw-list` | List all ADW workflows with specs |

### Domain Specialists (8 commands)
| Command | Agent | Phases | Time |
|---------|-------|--------|------|
| `/prime-codexa` | Meta-constructor | 5 | 15min-1h |
| `/prime-anuncio` | Ad generation | 7 | 23-38min |
| `/prime-pesquisa` | Market research | 9 | 20-30min |
| `/prime-marca` | Brand strategy | 7 | 21-36min |
| `/prime-mentor` | E-commerce mentoring | 6 | 16-31min |
| `/prime-photo` | AI photography | 5 | 15-30min |
| `/prime-video` | Video production | 5 | 15-60min |
| `/prime-scout` | Code navigation | - | Fast |

### Meta-Construction (8 commands)
| Command | Creates | Time |
|---------|---------|------|
| `/codexa-when-to-use` | Decision navigator | <30s |
| `/codexa-build-agent` | Complete agent | 20-40min |
| `/codexa-build-prompt` | HOP module (TAC-7) | 30-60min |
| `/codexa-build-command` | Slash command | 15-30min |
| `/codexa-build-schema` | Output schema | 10-20min |
| `/codexa-build-mcp` | MCP server | 30-60min |
| `/codexa-orchestrate` | Multi-phase workflow | Variable |
| `/codexa-cleanup` | Clean temp files | <5min |

### Voice Interface (6 commands)
| Command | Description |
|---------|-------------|
| `/v` | Voice mode v7.0 - single capture |
| `/vstart` | Start voice session |
| `/vstop` | Stop voice session |
| `/vstatus` | Check voice status |
| `/vgui` | Voice GUI interface |
| `/video` | Generate product video |

### Documentation (2 files)
| File | Purpose |
|------|---------|
| `README.md` | This index |
| `COMO_USAR.md` | Usage guide (Portuguese) |

---

## Quick Start

### Load Agent Context
```bash
/prime-pesquisa    # Market research specialist
/prime-anuncio     # Ad generation specialist
/prime-codexa      # Meta-construction specialist
```

### Execute Workflows
```bash
/prime pesquisa Product: Fone Bluetooth, Category: Eletrônicos
/prime anuncio USER_DOCS/research/fone_bluetooth.md
/prime mentor Como melhorar fotos de produto?
```

### Build Components
```bash
/codexa-when-to-use           # Decision tree
/codexa-build-agent           # Create new agent
/codexa-build-prompt          # Create HOP
/codexa-build-command         # Create command
```

---

## Decision Tree

```
What do you need?

├─ Learn about the system     → /prime
├─ Execute a workflow         → /prime {agent} {input}
│
├─ Load agent context
│   ├─ Market research        → /prime-pesquisa
│   ├─ Ad generation          → /prime-anuncio
│   ├─ Brand strategy         → /prime-marca
│   ├─ E-commerce mentoring   → /prime-mentor
│   ├─ Photo prompts          → /prime-photo
│   ├─ Video production       → /prime-video
│   ├─ Code navigation        → /prime-scout
│   └─ Meta-construction      → /prime-codexa
│
├─ Build something
│   ├─ New agent              → /codexa-build-agent
│   ├─ New HOP/prompt         → /codexa-build-prompt
│   ├─ New command            → /codexa-build-command
│   ├─ New schema             → /codexa-build-schema
│   ├─ New MCP server         → /codexa-build-mcp
│   └─ Not sure?              → /codexa-when-to-use
│
└─ Voice interface            → /v, /vstart, /vstop
```

---

## File Structure

```
.claude/commands/
├── README.md              # This index
├── COMO_USAR.md           # Usage guide (PT)
│
├── Navigation
│   ├── prime.md           # /prime
│   └── adw-list.md        # /adw-list
│
├── Domain Specialists
│   ├── prime-codexa.md    # /prime-codexa
│   ├── prime-anuncio.md   # /prime-anuncio
│   ├── prime-pesquisa.md  # /prime-pesquisa
│   ├── prime-marca.md     # /prime-marca
│   ├── prime-mentor.md    # /prime-mentor
│   ├── prime-photo.md     # /prime-photo
│   ├── prime-video.md     # /prime-video
│   └── prime-scout.md     # /prime-scout
│
├── Meta-Construction
│   ├── codexa-when-to-use.md
│   ├── codexa-build-agent.md
│   ├── codexa-build-prompt.md
│   ├── codexa-build-command.md
│   ├── codexa-build-schema.md
│   ├── codexa-build-mcp.md
│   ├── codexa-orchestrate.md
│   └── codexa-cleanup.md
│
└── Voice Interface
    ├── v.md
    ├── vstart.md
    ├── vstop.md
    ├── vstatus.md
    ├── vgui.md
    └── video.md
```

---

## Related Documentation

- **PRIME.md** (root) - System navigator
- **Agent Registry**: `51_AGENT_REGISTRY.json`
- **HOP Framework**: `42_HOP_FRAMEWORK.md`
- **Workflows**: `codexa.app/agentes/*/workflows/100_ADW_RUN_*.md`

---

## Status

✅ **PRODUCTION-READY** - All 26 commands registered and functional

---

**Maintainer**: CODEXA Meta-Constructor
**Version**: 2.0.0
**Last Updated**: 2025-12-02
