# 23_subagent_patterns | Claude Code Subagent Construction Patterns

**Version**: 1.0.0 | **Created**: 2025-12-02
**Type**: Knowledge Base | **Category**: Meta-Construction
**Distilled From**: Voice-guided implementation session

---

## OVERVIEW

This document captures patterns, best practices, and lessons learned from implementing a complete Claude Code subagent system. Use this knowledge when constructing new subagent types or extending the system.

---

## CORE CONCEPTS

### What is a Subagent Type?

A subagent type is a persistent agent specification stored as a Markdown file with YAML frontmatter in `.claude/agents/`. Claude Code:
- Auto-detects which subagent to use based on task description
- Spawns isolated subagent instances via Task tool
- Fires SubagentStop hook on completion

### Subagent vs Agent

| Aspect | CODEXA Agent | Claude Code Subagent |
|--------|--------------|---------------------|
| Definition | Full folder (PRIME.md, iso_vectorstore, workflows) | Single .md file in .claude/agents/ |
| Context | Complete domain knowledge | Isolated ~20k tokens |
| Invocation | Manual via /prime-* | Automatic detection or Task tool |
| Persistence | Permanent | Per-execution |
| Purpose | Domain expertise | Task execution |

### The Bridge Pattern

```
CODEXA Agent (Full Knowledge)
        │
        │ Context Loading
        ▼
Claude Code Subagent (Execution)
        │
        │ Scout Integration
        ▼
Full Agent Knowledge Available
```

---

## SUBAGENT TYPE STRUCTURE

### Required YAML Frontmatter

```yaml
---
name: {agent}-agent              # Lowercase with hyphens
description: {auto-detect text}  # 1-2 sentences, action-oriented
tools: Tool1, Tool2, ...         # Comma-separated
model: sonnet|opus|haiku         # Match task complexity
permissionMode: default|acceptEdits|bypassPermissions
---
```

### Required Body Sections

```markdown
# {Display Name} - {Specialty}

{Role description paragraph}

## CRITICAL: Load Full Context First

**Before starting ANY task**, load your complete agent context:

```
1. Use mcp__scout__smart_context with agent="{agent_id}"
2. Read the PRIME.md: {path_to_prime}
3. Read critical iso_vectorstore files ({files})
4. Check workflows/{workflow_file} for execution patterns
5. {Additional context instructions}
```

This ensures you operate with full domain knowledge.

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

## MODEL SELECTION PATTERNS

### Opus (Complex/Creative)

Use for:
- Brand strategy and creative direction
- Photography prompt engineering
- Complex multi-phase reasoning

Examples: `marca-agent`, `photo-agent`, `codexa-meta`

### Sonnet (Balanced)

Use for:
- Research and analysis
- Copywriting and content creation
- General domain tasks

Examples: `pesquisa-agent`, `anuncio-agent`, `curso-agent`, `video-agent`, `mentor-agent`

### Haiku (Fast/Simple)

Use for:
- Validation and QA
- File discovery and navigation
- Quick interactions

Examples: `qa-agent`, `scout-agent`, `voice-agent`

---

## TOOL PATTERNS

### Always Include

```yaml
tools: ..., mcp__scout__smart_context, mcp__scout__discover
```

Scout tools enable context loading from the full agent.

### By Domain

| Domain | Core Tools |
|--------|-----------|
| Research | WebSearch, WebFetch, mcp__browser__* |
| Writing | Read, Write, Edit |
| Validation | Read, Bash, Grep, Glob |
| Discovery | Glob, Grep, mcp__scout__* |
| Voice | mcp__voice__* |
| Meta | All + Task |

### Permission Modes

| Mode | Use Case |
|------|----------|
| `default` | Read-heavy, minimal writes |
| `acceptEdits` | Creates/modifies files actively |
| `bypassPermissions` | Trusted automation pipelines |

---

## DESCRIPTION PATTERNS

### Good Descriptions (Auto-Detection Works)

```yaml
# Specific, action-oriented, keyword-rich
description: Use for Brazilian e-commerce market research, competitor analysis, SERP research, and product viability studies. Ideal for gathering market intelligence before creating listings.

description: Use for creating Brazilian marketplace listings, e-commerce copywriting, SEO-optimized titles, and compliant product descriptions. Transform research into sales copy.
```

### Bad Descriptions (Auto-Detection Fails)

```yaml
# Too vague
description: General agent for tasks.

# Too narrow
description: Only for Mercado Livre.

# Missing keywords
description: Helps with stuff.
```

### Description Formula

```
"Use for [action1], [action2], and [action3]. Ideal for [context/use case]."
```

---

## CONTEXT LOADING PATTERN

### Why It Matters

Subagents have isolated context (~20k tokens). Without explicit context loading, they operate with only the subagent definition - losing domain expertise.

### The CRITICAL Section

```markdown
## CRITICAL: Load Full Context First

**Before starting ANY task**, load your complete agent context:

```
1. Use mcp__scout__smart_context with agent="pesquisa_agent" to get prioritized file list
2. Read the PRIME.md: codexa.app/agentes/pesquisa_agent/PRIME.md
3. Read critical iso_vectorstore files (08_research_rules.json, 06_input_schema.json)
4. Check workflows/100_ADW_RUN_PESQUISA.md for execution patterns
```

This ensures you operate with full domain knowledge, not just this summary.
```

### Scout Integration Flow

```
1. mcp__scout__smart_context returns prioritized files
2. Read PRIME.md (entry point)
3. Read high-priority iso_vectorstore files
4. Check relevant workflow
5. Execute with full context
```

---

## HOOK INTEGRATION PATTERNS

### SubagentStop Hook

Location: `.claude/hooks/subagent_stop.py`

Functions:
- `detect_subagent_type()` - Identifies agent type from input/transcript
- `collect_metrics()` - Tracks executions by type
- `announce_subagent_completion()` - TTS notification

### Type Detection

```python
SUBAGENT_TYPES = [
    "pesquisa-agent",
    "anuncio-agent",
    "marca-agent",
    # ... all custom types
    "general-purpose",  # built-in
    "Explore",          # built-in
    "Plan",             # built-in
]
```

### Metrics Structure

```json
{
  "by_type": {
    "pesquisa-agent": {
      "count": 15,
      "last_execution": "2025-12-02T10:30:00",
      "executions": [...]
    }
  },
  "total_executions": 45,
  "last_updated": "2025-12-02T10:30:00"
}
```

---

## PARALLEL EXECUTION PATTERNS

### Max Concurrent: 10

Claude Code limits to 10 concurrent subagents. Queue additional tasks.

### Independence Requirement

Only parallelize tasks that:
- Don't share state
- Modify different files
- Can be verified independently

### Batching Pattern

```
Batch 1 (parallel): pesquisa + marca + photo
  ↓ (sync point)
Batch 2 (parallel): anuncio (depends on pesquisa)
  ↓ (sync point)
Batch 3: qa validation
```

### spawn-agents Command

```bash
/spawn-agents product-pipeline "Product Name"
# Spawns: pesquisa + marca parallel, then anuncio sequential

/spawn-agents research-multi "Product Name"
# Spawns: 4 pesquisa agents for different marketplaces

/spawn-agents quality-audit
# Spawns: 4 qa agents checking different aspects
```

---

## LIMITATIONS & WORKAROUNDS

### Limitation 1: Custom subagent_type Parameter

**Issue**: Task tool's `subagent_type` parameter only accepts built-in types (`general-purpose`, `Explore`, `Plan`, `claude-code-guide`).

**Workaround**: Include agent instructions in Task prompt:
```
Task(
  prompt="You are the pesquisa-agent. First load context via mcp__scout__smart_context. Then research [topic]...",
  subagent_type="general-purpose"
)
```

Or rely on auto-detection based on description.

### Limitation 2: No Subagent Nesting

**Issue**: Subagents cannot spawn other subagents.

**Workaround**: Flat orchestration from main conversation only.

### Limitation 3: Context Isolation

**Issue**: Subagents don't share memory with main conversation.

**Workaround**: Use filesystem for inter-agent communication. Write results to files that other agents can read.

---

## TEMPLATE REFERENCE

Universal template: `.claude/agents/TEMPLATE_subagent.md`

### Placeholders

| Placeholder | Description |
|-------------|-------------|
| `{{AGENT_NAME}}` | Lowercase identifier |
| `{{AGENT_DISPLAY_NAME}}` | Human-readable name |
| `{{AGENT_DESCRIPTION}}` | Auto-detection text |
| `{{AGENT_SPECIALTY}}` | Domain specialty |
| `{{AGENT_ROLE_DESCRIPTION}}` | Role in first person |
| `{{AGENT_ID}}` | Folder name |
| `{{PROJECT_PATH}}` | Project path |
| `{{MODEL}}` | sonnet/opus/haiku |
| `{{PERMISSION_MODE}}` | Permission setting |
| `{{CRITICAL_FILES}}` | Context files |
| `{{WORKFLOW_FILE}}` | Main workflow |
| `{{CAPABILITIES_LIST}}` | Numbered capabilities |
| `{{OUTPUT_FORMAT}}` | Expected outputs |
| `{{FRAMEWORKS}}` | Methods used |
| `{{QUALITY_STANDARDS}}` | Validation rules |
| `{{LANGUAGE_INSTRUCTIONS}}` | Language guidance |

---

## QUICK REFERENCE

### Create New Subagent Type

```bash
1. Read source agent PRIME.md
2. Copy TEMPLATE_subagent.md
3. Fill placeholders
4. Add to .claude/agents/{name}-agent.md
5. Update SUBAGENT_TYPES in hook
6. Test auto-detection
```

### Verify Subagent System

```bash
1. ls .claude/agents/  # List all types
2. python -m py_compile .claude/hooks/subagent_stop.py  # Syntax check
3. cat .claude/settings.json | grep SubagentStop  # Hook configured
```

### Debug Auto-Detection

If subagent not detected:
1. Check description keywords match task
2. Verify no conflicting descriptions
3. Add more domain-specific terms
4. Test with explicit Task prompt

---

## RELATED FILES

| File | Purpose |
|------|---------|
| `95_meta_build_subagent_HOP.md` | Construction HOP |
| `206_ADW_SUBAGENT_CONSTRUCTION.md` | Full workflow |
| `.claude/agents/TEMPLATE_subagent.md` | Universal template |
| `.claude/SUBAGENT_ARCHITECTURE.md` | System documentation |
| `.claude/hooks/subagent_stop.py` | Metrics & notification hook |
| `.claude/commands/spawn-agents.md` | Orchestration command |

---

**Version**: 1.0.0
**Status**: Knowledge Base
**Distilled From**: Voice-guided implementation session (2025-12-02)
**Use Case**: Reference when constructing or extending subagent system
