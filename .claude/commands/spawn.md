# /spawn - Parallel Agent Orchestrator

**Version**: 2.0.0 | **Type**: Computational Multiplier

Launch N agents in parallel to maximize throughput. Any LLM/agent can use this.

---

## QUICK START

```
/spawn
1. explore: find all ADW files
2. explore: find all HOP files
3. plan: design new caching system
```

LLM executes 3 Task tools in ONE message → results return together.

---

## PRESETS (Ready-to-Use)

### 🔍 Discovery Preset (10 scouts)
```
/spawn preset:discovery
```
Expands to 10 parallel scouts checking: agents/, docs/, mcp-servers/, commands/, outputs/, templates/, scripts/, root files, path_registry validation, broken links.

### 🏥 Health Check (5 validators)
```
/spawn preset:health
```
Validates: CLAUDE.md compliance, LAW violations, broken paths, missing files, quality gates.

### 📊 Full Audit (10 analysts)
```
/spawn preset:audit
```
Complete project audit: structure, docs, code quality, dependencies, tests, security.

### 🚀 Performance (3 optimizers)
```
/spawn preset:perf
```
Analyze: slow operations, large files, optimization opportunities.

---

## AGENT TYPES

| Type | subagent_type | Best For |
|------|---------------|----------|
| `explore` | Explore | Find files, understand codebase, quick searches |
| `plan` | Plan | Design implementations, architecture decisions |
| `guide` | claude-code-guide | Claude Code docs, SDK questions |
| `review` | general-purpose | Code review, quality checks |
| `build` | general-purpose | Create files, implement features |
| `test` | general-purpose | Run tests, validate outputs |
| (no type) | general-purpose | Any task |

---

## SYNTAX

### Basic
```
/spawn
1. [type]: [task description]
2. [type]: [task description]
...
```

### With Count
```
/spawn 10
explore: check all agent paths
```
Spawns 10 explore agents, each with different scope.

### With Preset
```
/spawn preset:[name]
```

### With Model Override
```
/spawn model:haiku
1. explore: quick file search
2. explore: another quick search
```
Uses haiku for fast, cheap operations.

---

## EXAMPLES

### Example 1: Path Diagnostics (10 agents)
```
/spawn
1. explore: validate agents/ paths and structure
2. explore: validate docs/ paths and links
3. explore: validate mcp-servers/ configuration
4. explore: validate .claude/commands/ files
5. explore: check outputs/ directories
6. explore: check templates/ organization
7. explore: find orphaned scripts
8. explore: validate root config files
9. review: cross-reference path_registry.json
10. review: find broken markdown links
```

### Example 2: LAW Compliance Check
```
/spawn
1. review: check LAW 1 compliance (distillation)
2. review: check LAW 2 compliance (fractal nav)
3. review: check LAW 5 compliance (ordinal seq)
4. explore: find hardcoded brand content
5. explore: find files without PRIME.md
```

### Example 3: Multi-Agent Workflow
```
/spawn
1. explore: find current curso_agent structure
2. explore: find video script templates
3. plan: design new video workflow
4. guide: how to create custom slash commands
```

### Example 4: Code Generation
```
/spawn
1. build: create validator for LAW 1
2. build: create validator for LAW 2
3. build: create test suite for validators
```

### Example 5: Quick Parallel Search
```
/spawn model:haiku
1. explore: files mentioning "supabase"
2. explore: files mentioning "shopify"
3. explore: files mentioning "anthropic"
4. explore: files mentioning "openai"
```

---

## HOW IT WORKS

```
┌─────────────────────────────────────────────────────────────────┐
│  USER INPUT                    LLM EXECUTION                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  /spawn                        ┌──────────────────────────┐    │
│  1. explore: X                 │ Task(Explore, "X")       │──┐ │
│  2. explore: Y           →     │ Task(Explore, "Y")       │──┤ │
│  3. plan: Z                    │ Task(Plan, "Z")          │──┤ │
│                                └──────────────────────────┘  │ │
│                                          ↓                   │ │
│                                   ALL IN PARALLEL ───────────┘ │
│                                          ↓                     │
│                                ┌──────────────────────────┐    │
│                                │ Collected Results        │    │
│                                │ Formatted Output         │    │
│                                └──────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

---

## LLM INSTRUCTIONS

When `/spawn` is invoked:

### 1. Parse Input
```python
def parse_spawn(input):
    lines = input.strip().split('\n')
    config = {'model': None, 'preset': None, 'count': None}
    tasks = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith('/spawn'):
            # Check for modifiers
            if 'model:' in line:
                config['model'] = line.split('model:')[1].split()[0]
            if 'preset:' in line:
                config['preset'] = line.split('preset:')[1].split()[0]
            if match := re.search(r'/spawn\s+(\d+)', line):
                config['count'] = int(match.group(1))
            continue

        # Remove number prefix
        line = re.sub(r'^\d+\.\s*', '', line)

        # Detect type
        type_map = {
            'explore:': 'Explore',
            'plan:': 'Plan',
            'guide:': 'claude-code-guide',
            'review:': 'general-purpose',
            'build:': 'general-purpose',
            'test:': 'general-purpose'
        }

        agent_type = 'general-purpose'
        task = line

        for prefix, atype in type_map.items():
            if line.lower().startswith(prefix):
                agent_type = atype
                task = line[len(prefix):].strip()
                break

        tasks.append((agent_type, task))

    return config, tasks
```

### 2. Handle Presets
```python
PRESETS = {
    'discovery': [
        ('Explore', 'validate agents/ directory structure and paths'),
        ('Explore', 'validate docs/ directory and check links'),
        ('Explore', 'validate mcp-servers/ configuration'),
        ('Explore', 'validate .claude/commands/ files'),
        ('Explore', 'check outputs/ directory organization'),
        ('Explore', 'check templates/ structure'),
        ('Explore', 'find scripts and validate paths'),
        ('Explore', 'validate root configuration files'),
        ('general-purpose', 'validate path_registry.json references'),
        ('general-purpose', 'find broken markdown links across repo'),
    ],
    'health': [
        ('general-purpose', 'check CLAUDE.md LAW compliance'),
        ('Explore', 'find LAW 1 violations (hardcoded brands)'),
        ('Explore', 'find LAW 2 violations (missing PRIME.md)'),
        ('general-purpose', 'validate all paths in path_registry.json'),
        ('general-purpose', 'check quality gate scores in outputs'),
    ],
    'audit': [
        ('Explore', 'audit agents/ structure completeness'),
        ('Explore', 'audit documentation coverage'),
        ('general-purpose', 'audit code quality patterns'),
        ('general-purpose', 'audit external dependencies'),
        ('general-purpose', 'audit test coverage'),
        ('general-purpose', 'audit security patterns'),
        ('Explore', 'audit workflow (ADW) completeness'),
        ('Explore', 'audit prompt (HOP) organization'),
        ('general-purpose', 'audit MCP server configuration'),
        ('general-purpose', 'audit environment variables'),
    ],
    'perf': [
        ('Explore', 'find large files (>100KB)'),
        ('general-purpose', 'identify slow operations in scripts'),
        ('general-purpose', 'find optimization opportunities'),
    ]
}
```

### 3. Execute in Parallel
- Send ONE message with ALL Task tool calls
- Each Task gets: description, prompt, subagent_type, optional model
- Wait for all results

### 4. Format Output
```markdown
## /spawn Results (N agents)

### 1. [type]: [task]
[Result summary]

### 2. [type]: [task]
[Result summary]

...

---
✅ All N agents completed in parallel
⏱️ Total time: ~Xs (vs ~NXs sequential)
```

---

## INTEGRATION WITH LAWS

| LAW | How /spawn Helps |
|-----|------------------|
| LAW 2 (Fractal) | Spawn explores to find PRIME.md files |
| LAW 3 (Meta) | Spawn builders to create templates |
| LAW 4 (Agentic) | Spawn multiple domain agents |
| LAW 5 (Ordinal) | Spawn scouts to validate numbering |
| LAW 7 (Recovery) | Spawn validators for error checking |

---

## LIMITS & PERFORMANCE

| Limit | Value | Reason |
|-------|-------|--------|
| Max parallel | 10 | Claude Code limit |
| Timeout | 2 min/agent | Prevent hanging |
| Recommended | 3-7 | Best performance |

### Model Selection
- `haiku`: Fast, cheap - use for simple searches
- `sonnet`: Balanced - default
- `opus`: Deep analysis - complex tasks

---

## AUTONOMY

Any agent can call `/spawn` internally:
```
Agent A receives complex task
  → Parses into subtasks
  → Calls /spawn with 5 sub-agents
  → Collects results
  → Synthesizes answer
```

This enables **recursive parallelization**.

---

**Version**: 2.0.0
**Updated**: 2025-12-03
**Type**: Computational Multiplier (Claude Code Enhancement)
