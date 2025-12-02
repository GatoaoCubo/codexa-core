# /codexa-when-to-use | CODEXA Decision Navigator

**Role**: Interactive decision tree for choosing right meta-construction tool
**Philosophy**: Right tool for right job | Fast guidance <30s
**Output**: Direct command + time estimate + quick start + pitfalls

---

## DECISION TREE

**What do you want to BUILD?**

**A) HOP/Prompt** → Reusable prompt with validation
- Reused in multiple contexts? → `/codexa-build-prompt` | Time: 30-60min | HOP Framework (TAC-7)

**B) Complete Agent** → Isolated agent for OpenAI
- Full agent system? → `/codexa-build-agent` | Time: 20-40min | 5-phase ADW workflow

**C) Slash Command** → CLI shortcut
- Custom command? → `/codexa-build-command` | Time: 15-30min | Command template

**D) Output Schema** → JSON Schema or plan
- Structured output? → `/codexa-build-schema` | Time: 10-20min | Validation rules

**E) MCP Server** → External API integration
- Custom tools/APIs? → `/codexa-build-mcp` | Time: 30-60min | MCP protocol

**F) Multi-Phase Workflow** → Orchestrated ADW
- Multiple phases with deps? → `/codexa-orchestrate` | Time: Variable | Workflow spec

**G) Not sure** → Read PRIME.md | Check examples | Ask for clarification

---

## QUICK REFERENCE

| Build | Command | Time | Complexity |
|-------|---------|------|------------|
| HOP Module | `/codexa-build-prompt` | 30-60min | Medium |
| Agent | `/codexa-build-agent` | 20-40min | High |
| Command | `/codexa-build-command` | 15-30min | Low |
| Schema | `/codexa-build-schema` | 10-20min | Low |
| MCP Server | `/codexa-build-mcp` | 30-60min | Medium |
| Workflow | `/codexa-orchestrate` | Variable | High |

---

## COMMON PITFALLS

**HOP**: Forgetting to define all $variables in INPUT_CONTRACT | Not validating with hop_sync_validator
**Agent**: Description too vague (<20 chars) | Skipping validation phases
**Command**: Not following naming convention | Missing required sections
**Schema**: Incomplete validation rules | No examples
**MCP**: Missing authentication | Incomplete error handling
**Workflow**: Circular dependencies | Incomplete $arguments chaining

---

**Related**: PRIME.md (philosophy) | All /codexa-build-* commands | HOPs (examples)
