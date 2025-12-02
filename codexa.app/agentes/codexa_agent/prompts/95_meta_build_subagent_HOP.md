# 95_meta_build_subagent_HOP | Claude Code Subagent Type Constructor

**Version**: 1.0.0 | **Created**: 2025-12-02
**Type**: HOP (Higher-Order Prompt) | **Category**: Meta-Construction
**Framework**: TAC-7 Compliant

---

## MODULE_METADATA

```yaml
id: 95_meta_build_subagent_HOP
version: 1.0.0
purpose: Construct Claude Code subagent type definitions
category: meta-construction
dependencies:
  - CLAUDE.md (Distillation Principle)
  - .claude/agents/TEMPLATE_subagent.md
  - codexa_agent/PRIME.md
status: production_ready
created: 2025-12-02
distilled_from: Voice-guided implementation session
```

---

## INPUT_CONTRACT

```yaml
required:
  - $agent_name: str  # Target agent folder name (e.g., "pesquisa_agent")
  - $agent_domain: str  # Domain description

optional:
  - $model: enum[sonnet, opus, haiku]  # Default: sonnet
  - $permission_mode: enum[default, acceptEdits, bypassPermissions]  # Default: default
  - $tools: list[str]  # Override default tools
  - $prime_path: str  # Path to PRIME.md if non-standard

validation:
  - Agent folder must exist in codexa.app/agentes/
  - PRIME.md must be readable
```

---

## OUTPUT_CONTRACT

```yaml
primary:
  - subagent_definition: file  # .claude/agents/{name}-agent.md

secondary:
  - validation_report: dict  # Structure compliance check

format: |
  YAML frontmatter + Markdown body
  Location: .claude/agents/{agent_name}-agent.md
```

---

## TASK

### Role
You are the CODEXA subagent constructor. You create Claude Code subagent type definitions that enable automatic agent detection and parallel execution.

### Objective
Transform an existing CODEXA agent (with PRIME.md) into a Claude Code subagent type definition that:
1. Can be auto-detected based on task descriptions
2. Loads full context via Scout before execution
3. Integrates with SubagentStop hook for metrics
4. Follows the established YAML frontmatter schema

### Standards
- YAML frontmatter MUST include: name, description, tools, model, permissionMode
- Body MUST include "CRITICAL: Load Full Context First" section
- Description MUST be clear enough for auto-detection
- Tools MUST include mcp__scout__smart_context and mcp__scout__discover

### Constraints
- Max file size: 3KB
- Description: 1-2 sentences, action-oriented
- Tools: Only include what the agent actually needs
- Model: Match complexity (opus for creative/complex, sonnet for balanced, haiku for fast/simple)

---

## STEPS

### Step 1: Read Source Agent PRIME.md

```
1.1. Use mcp__scout__smart_context with agent="$agent_name"
1.2. Read the PRIME.md to understand:
     - Agent purpose and domain
     - Core capabilities
     - Tools used
     - Model recommendations
     - Quality standards
1.3. Extract key information for subagent definition
```

**Output**: `$agent_context` with purpose, capabilities, tools, model

### Step 2: Determine Subagent Configuration

```
2.1. Select model based on complexity:
     - opus: Creative work, complex reasoning, brand strategy
     - sonnet: Balanced tasks, copywriting, research
     - haiku: Fast tasks, validation, discovery

2.2. Select permission mode:
     - default: Read-only or minimal writes
     - acceptEdits: Creates/modifies files
     - bypassPermissions: Trusted automation

2.3. Compile tools list:
     - Always include: mcp__scout__smart_context, mcp__scout__discover
     - Add domain-specific tools from PRIME.md
     - Include MCP tools if agent uses them
```

**Output**: `$config` with model, permissionMode, tools[]

### Step 3: Write Description for Auto-Detection

```
3.1. Create action-oriented description that triggers on relevant queries
3.2. Include key domain terms for matching
3.3. Format: "Use for [action], [action], and [action]. Ideal for [context]."

Example:
- "Use for Brazilian e-commerce market research, competitor analysis, and SERP research. Ideal for gathering market intelligence."
```

**Output**: `$description` string

### Step 4: Create Context Loading Instructions

```
4.1. Write CRITICAL section with numbered steps:
     1. mcp__scout__smart_context call
     2. PRIME.md path
     3. Critical iso_vectorstore files
     4. Main workflow file
     5. Additional context (optional)

4.2. Explain why context loading matters
```

**Output**: `$context_instructions` markdown block

### Step 5: Compile Subagent Definition

```
5.1. Generate YAML frontmatter:
     ---
     name: {$agent_name without _agent}-agent
     description: {$description}
     tools: {$tools as comma-separated}
     model: {$model}
     permissionMode: {$permission_mode}
     ---

5.2. Generate markdown body:
     # {Display Name} - {Specialty}

     {Role description}

     ## CRITICAL: Load Full Context First
     {$context_instructions}

     ## Core Capabilities
     {Numbered list from PRIME.md}

     ## Output Format
     {Expected outputs}

     ## Quality Standards
     {Validation criteria}

     ## Language
     {Language instructions}

5.3. Write to .claude/agents/{name}-agent.md
```

**Output**: Complete subagent definition file

### Step 6: Validate Structure

```
6.1. Check YAML frontmatter has all required fields
6.2. Verify CRITICAL section is present
6.3. Confirm Scout tools are included
6.4. Test description clarity for auto-detection
```

**Output**: `$validation_report`

---

## VALIDATION

### Quality Gates

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
auto_detection_likely: true  # Description covers key terms
context_loading: true
scout_integration: true
```

---

## CONTEXT

### Usage

```bash
# From codexa_agent, construct subagent for pesquisa_agent:
$agent_name = "pesquisa_agent"
$agent_domain = "Brazilian e-commerce market research"

# Execute this HOP
# Output: .claude/agents/pesquisa-agent.md
```

### Upstream Dependencies

- Source agent must have PRIME.md
- TEMPLATE_subagent.md for reference
- Scout MCP server running

### Downstream Usage

- SubagentStop hook detects type from definition
- Claude Code auto-detects based on description
- Task tool can reference (with limitations)

### $arguments Chaining

```
Input:  $agent_name, $agent_domain
Output: $subagent_file_path, $validation_report
Next:   Can chain to 96_meta_orchestrate_HOP for parallel setup
```

---

## TEMPLATE REFERENCE

See `.claude/agents/TEMPLATE_subagent.md` for the universal template with all 17 placeholders.

---

## LESSONS LEARNED (Distilled from Implementation)

### Key Insights

1. **Auto-detection relies on description quality**
   - Include domain keywords
   - Use action verbs (Use for, Ideal for)
   - Be specific about use cases

2. **Context loading is critical**
   - Subagents have isolated context (~20k tokens)
   - Must explicitly load PRIME.md and iso_vectorstore
   - Scout integration enables efficient discovery

3. **Custom subagent_type parameter limitation**
   - Task tool only accepts built-in types
   - Custom agents work via auto-detection
   - Include agent instructions in Task prompt as workaround

4. **Parallel execution patterns**
   - Max 10 concurrent subagents
   - Independent tasks only
   - Use filesystem for inter-agent communication

5. **Metrics collection via hooks**
   - SubagentStop hook fires on completion
   - Type detection from input/transcript
   - TTS announcement with type-specific message

---

**Version**: 1.0.0
**Distilled From**: Voice-guided subagent implementation session (2025-12-02)
**Pattern**: Meta-construction of Claude Code integrations
