# SUBAGENT_ARCHITECTURE.md

**Version**: 1.0.0 | **Created**: 2025-12-05 | **Status**: Production

Complete documentation for the CODEXA Claude Code subagent system.

---

## OVERVIEW

The subagent system bridges CODEXA's full agents (with PRIME.md, iso_vectorstore, workflows) to Claude Code's Task tool for parallel execution.

```
┌─────────────────────────────────────────────────────────────────┐
│                    CODEXA SUBAGENT SYSTEM                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   CODEXA Agent (Full Knowledge)                                  │
│   ├── PRIME.md (entry point)                                    │
│   ├── iso_vectorstore/ (knowledge base)                         │
│   ├── workflows/ (ADWs)                                         │
│   ├── prompts/ (HOPs)                                           │
│   └── config/ (rules, schemas)                                  │
│            │                                                     │
│            │ Scout Integration                                   │
│            ▼                                                     │
│   Claude Code Subagent (.claude/agents/{name}-agent.md)         │
│   ├── YAML frontmatter (name, description, tools, model)        │
│   ├── CRITICAL: Load Full Context First                         │
│   └── Capabilities + Quality Standards                          │
│            │                                                     │
│            │ Task Tool                                           │
│            ▼                                                     │
│   Parallel Execution (up to 10 concurrent)                      │
│            │                                                     │
│            │ SubagentStop Hook                                   │
│            ▼                                                     │
│   Metrics + TTS Notification                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## SUBAGENT TYPES

| Subagent | Model | Domain | Bridge To |
|----------|-------|--------|-----------|
| `pesquisa-agent` | sonnet | Market research | pesquisa_agent |
| `anuncio-agent` | sonnet | E-commerce copy | anuncio_agent |
| `marca-agent` | opus | Brand strategy | marca_agent |
| `photo-agent` | opus | Photography prompts | photo_agent |
| `video-agent` | sonnet | Video production | video_agent |
| `curso-agent` | sonnet | Course creation | curso_agent |
| `mentor-agent` | sonnet | Seller coaching | mentor_agent |
| `voice-agent` | haiku | Voice interface | voice_agent |
| `codexa-agent` | opus | Meta-construction | codexa_agent |
| `scout-agent` | haiku | File discovery | scout_agent |
| `qa-agent` | haiku | Quality validation | qa_gato3_agent |
| `ronronalda-agent` | sonnet | Personal assistant | ronronalda_agent |

---

## FILE STRUCTURE

```
.claude/
├── agents/                          # Subagent definitions
│   ├── TEMPLATE_subagent.md         # Universal template
│   ├── pesquisa-agent.md
│   ├── anuncio-agent.md
│   ├── marca-agent.md
│   ├── photo-agent.md
│   ├── video-agent.md
│   ├── curso-agent.md
│   ├── mentor-agent.md
│   ├── voice-agent.md
│   ├── codexa-agent.md
│   ├── scout-agent.md
│   ├── qa-agent.md
│   └── ronronalda-agent.md
│
├── hooks/
│   └── subagent_stop.py             # Metrics + TTS hook
│
├── commands/
│   ├── spawn.md                     # Generic parallel spawner
│   └── spawn-agents.md              # CODEXA pipelines
│
├── subagent_metrics.json            # Execution metrics (generated)
└── SUBAGENT_ARCHITECTURE.md         # This file
```

---

## SUBAGENT DEFINITION STRUCTURE

Each subagent file follows this structure:

```markdown
---
name: {agent}-agent
description: Use for {action1}, {action2}, and {action3}. Ideal for {context}.
tools: Read, Write, Edit, mcp__scout__smart_context, mcp__scout__discover, ...
model: sonnet|opus|haiku
permissionMode: default|acceptEdits|bypassPermissions
---

# {Display Name} - {Specialty}

{Role description}

## CRITICAL: Load Full Context First

**Before starting ANY task**, load your complete agent context:

```
1. Use mcp__scout__smart_context with agent="{agent_id}"
2. Read the PRIME.md: codexa.app/agentes/{agent_id}/PRIME.md
3. Read critical files: ...
4. Check workflows: ...
```

## Core Capabilities
{Numbered list}

## Output Format
{Expected outputs}

## Quality Standards
{Validation criteria}

## Language
{Language instructions}
```

---

## HOW AUTO-DETECTION WORKS

Claude Code auto-detects subagent type based on:

1. **Description keywords**: Match task to agent description
2. **Tool requirements**: Match needed tools to agent tools
3. **Context signals**: Detect domain-specific terms

### Description Best Practices

```yaml
# GOOD - Specific, action-oriented, keyword-rich
description: Use for Brazilian e-commerce market research, competitor analysis,
             SERP research, and product viability studies. Ideal for gathering
             market intelligence before creating listings.

# BAD - Too vague
description: General agent for tasks.
```

---

## CONTEXT LOADING (CRITICAL)

Subagents have isolated context (~20k tokens). Without explicit context loading, they operate with minimal knowledge.

### The CRITICAL Section

Every subagent MUST include:

```markdown
## CRITICAL: Load Full Context First

**Before starting ANY task**, load your complete agent context:

1. Use mcp__scout__smart_context with agent="{agent_id}"
2. Read the PRIME.md: codexa.app/agentes/{agent_id}/PRIME.md
3. Read critical iso_vectorstore files
4. Check workflows for execution patterns
```

### Scout Integration Flow

```
1. mcp__scout__smart_context → prioritized file list
2. Read PRIME.md → entry point
3. Read high-priority files → domain knowledge
4. Execute task → with full context
```

---

## PARALLEL EXECUTION

### Limits

- **Max concurrent**: 10 subagents
- **Timeout**: 2 min per agent
- **Recommended**: 3-7 for best performance

### Patterns

**Sequential (dependency chain)**:
```
pesquisa-agent → anuncio-agent → photo-agent
```

**Parallel (independent tasks)**:
```
┌─ marca-agent ──┐
│                ├──► Aggregate
└─ photo-agent ──┘
```

**Mixed (sequential + parallel)**:
```
pesquisa-agent
      │
      ▼
┌─────┴─────┐
▼           ▼
anuncio   marca
      │
      ▼
  photo-agent
```

---

## HOOKS

### SubagentStop Hook

Location: `.claude/hooks/subagent_stop.py`

**Functions**:
1. `detect_subagent_type()` - Identify agent from task
2. `collect_metrics()` - Track executions by type
3. `announce_completion()` - TTS notification (optional)

**Metrics Structure**:
```json
{
  "by_type": {
    "pesquisa-agent": {
      "count": 15,
      "last_execution": "2025-12-05T10:30:00",
      "executions": [...]
    }
  },
  "total_executions": 45,
  "last_updated": "2025-12-05T10:30:00"
}
```

**TTS Messages** (Portuguese BR):
- `pesquisa-agent`: "Pesquisa concluída"
- `anuncio-agent`: "Anúncio gerado"
- `marca-agent`: "Estratégia de marca pronta"
- etc.

---

## COMMANDS

### /spawn (Generic)

```
/spawn
1. explore: find ADW files
2. explore: find HOP files
3. plan: design new feature
```

### /spawn-agents (CODEXA Pipelines)

```
/spawn-agents product-pipeline "Product Name"
/spawn-agents research-multi "Product Name"
/spawn-agents content-suite "Product Name"
/spawn-agents quality-audit
/spawn-agents course-builder "Module Topic"
```

---

## LIMITATIONS

### 1. Custom subagent_type Parameter

**Issue**: Task tool only accepts built-in types (general-purpose, Explore, Plan, claude-code-guide).

**Workaround**: Include agent instructions in Task prompt:
```
Task(
  prompt="You are the pesquisa-agent. First load context via mcp__scout__smart_context...",
  subagent_type="general-purpose"
)
```

### 2. No Subagent Nesting

**Issue**: Subagents cannot spawn other subagents.

**Workaround**: Flat orchestration from main conversation only.

### 3. Context Isolation

**Issue**: Subagents don't share memory with main conversation.

**Workaround**: Use filesystem for inter-agent communication.

---

## QUALITY VALIDATION

### Checklist

- [ ] YAML frontmatter valid and complete
- [ ] Description enables auto-detection
- [ ] CRITICAL context loading section present
- [ ] Scout tools included in tools list
- [ ] Model appropriate for domain complexity
- [ ] File size under 3KB
- [ ] Language instructions present

### Success Criteria

```yaml
structure_valid: true
auto_detection_likely: true
context_loading: true
scout_integration: true
```

---

## RELATED FILES

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project laws (LAW 4: Agentic Design) |
| `23_subagent_patterns.md` | Pattern documentation |
| `206_ADW_SUBAGENT_CONSTRUCTION.md` | Construction workflow |
| `95_meta_build_subagent_HOP.md` | Construction HOP |

---

## CHANGELOG

### v1.0.0 (2025-12-05)
- Initial release
- 12 subagent definitions created
- SubagentStop hook implemented
- spawn-agents command created
- Full documentation

---

**Created by**: CODEXA Meta-Constructor
**Status**: Production Ready
**Total Subagents**: 12
**Total Files**: 15 (12 agents + 1 template + 1 hook + 1 command)
