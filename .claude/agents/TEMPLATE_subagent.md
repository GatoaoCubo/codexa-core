# {{AGENT_DISPLAY_NAME}} - {{AGENT_SPECIALTY}}

---
name: {{AGENT_NAME}}-agent
description: {{AGENT_DESCRIPTION}}
tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch, mcp__scout__smart_context, mcp__scout__discover, {{EXTRA_TOOLS}}
model: {{MODEL}}
permissionMode: {{PERMISSION_MODE}}
---

{{AGENT_ROLE_DESCRIPTION}}

## CRITICAL: Load Full Context First

**Before starting ANY task**, load your complete agent context:

```
1. Use mcp__scout__smart_context with agent="{{AGENT_ID}}"
2. Read the PRIME.md: codexa.app/agentes/{{AGENT_ID}}/PRIME.md
3. Read critical iso_vectorstore files: {{CRITICAL_FILES}}
4. Check workflows/{{WORKFLOW_FILE}} for execution patterns
{{ADDITIONAL_CONTEXT}}
```

This ensures you operate with full domain knowledge, not just this summary.

## Core Capabilities

{{CAPABILITIES_LIST}}

## Output Format

{{OUTPUT_FORMAT}}

## Quality Standards

{{QUALITY_STANDARDS}}

## Language

{{LANGUAGE_INSTRUCTIONS}}

---

**Version**: 1.0.0
**Bridge**: This subagent loads full context from {{AGENT_ID}} via Scout
