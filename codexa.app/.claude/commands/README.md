# Claude Code Custom Commands

Custom slash commands for CODEXA system workflows and operations.

## Available Commands

### `/prime {agent_name} [input]`

Execute a complete ADW (Agentic Developer Workflow) from start to finish.

**Supported agents**:
- `pesquisa` - Market research (9 phases, 20-30min)
- `anuncio` - Ad generation (7 phases, 23-38min)
- `mentor` - E-commerce mentoring (6 phases, 16-31min)
- `marca` - Brand strategy (7 phases, 21-36min)
- `photo` - AI photography prompts (5 phases, 15-30min)

**Examples**:
```bash
/prime pesquisa Product: Fone Bluetooth, Category: Eletrônicos, Price: R$ 150-400
/prime anuncio USER_DOCS/produtos/research/fone_bluetooth_research_notes.md
/prime mentor Como melhorar fotos de produto no Mercado Livre?
/prime marca Business: Fones premium, Mission: Democratizar áudio de qualidade
/prime photo subject=Fone Bluetooth, style=lifestyle
```

**What it does**:
1. Loads agent context (PRIME.md + ADW + configs)
2. Executes all workflow phases sequentially
3. Validates outputs at each phase
4. Generates final deliverables
5. Reports completion with quality metrics

---

### `/adw-list`

Display all available ADW workflows with detailed specifications.

**What it shows**:
- Workflow file paths
- Phase count and duration
- Input requirements
- Quality gates
- Usage examples
- Summary statistics

**Example**:
```bash
/adw-list
```

---

## Command Architecture

All commands are defined in `.claude/commands/*.md` files using markdown format.

### File Structure

```
.claude/
└── commands/
    ├── README.md          # This file
    ├── prime.md           # /prime command implementation
    └── adw-list.md        # /adw-list command implementation
```

### Command Format

Each command file contains:
1. **Title**: Brief description
2. **Usage**: Syntax and parameters
3. **Instructions**: Detailed execution steps
4. **Examples**: Real-world usage examples
5. **Notes**: Additional context and references

## Related Documentation

- **ADW Test Review**: `ADW_TEST_REVIEW_REPORT.md` (full technical review)
- **Workflows**: `agentes/*/workflows/100_ADW_RUN_*.md`
- **HOP Prompts**: `agentes/*/prompts/*.md`
- **Agent Registry**: `51_AGENT_REGISTRY.json`

## Status

✅ **PRODUCTION-READY**

All commands are functional and tested with the CODEXA agent system.

## Future Commands (Planned)

- `/adw_quick {agent}` - Execute abbreviated workflow (quick mode)
- `/adw_validate {agent}` - Validate agent files and configurations
- `/adw_chain {agent1} {agent2}` - Chain multiple workflows
- `/adw_status` - Show execution status and history

---

**Maintainer**: CODEXA Meta-Constructor
**Version**: 1.0.0
**Last Updated**: 2025-11-24
