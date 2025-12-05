# CODEXA System Map | For External LLMs

**Purpose**: Help external LLMs (ChatGPT, Gemini, Claude web) understand the CODEXA ecosystem when only one `iso_vectorstore/` is available.

---

## You Are Currently In: {{AGENT_NAME}}

This agent specializes in: {{AGENT_SPECIALTY}}

---

## The Complete Agent Ecosystem

CODEXA has **12 specialized agents** that work together:

### Content Creation Agents
| Agent | Domain | Input | Output |
|-------|--------|-------|--------|
| `anuncio_agent` | E-commerce copywriting | Product brief | Marketplace listings |
| `photo_agent` | AI photography | Subject description | Midjourney/DALL-E prompts |
| `video_agent` | Video production | Product/concept | Scripts, storyboards |
| `curso_agent` | Online courses | Topic/audience | Course structure, scripts |

### Strategy Agents
| Agent | Domain | Input | Output |
|-------|--------|-------|--------|
| `pesquisa_agent` | Market research | Product/niche | 22-block research notes |
| `marca_agent` | Brand strategy | Business info | 32-block brand identity |
| `mentor_agent` | E-commerce coaching | Question/problem | Practical guidance |

### System Agents
| Agent | Domain | Input | Output |
|-------|--------|-------|--------|
| `codexa_agent` | Meta-construction | Agent spec | New agents/prompts |
| `scout_agent` | File discovery | Query/pattern | Relevant file paths |
| `qa_agent` | Quality assurance | Content | Validation report |
| `voice_agent` | Voice interface | Speech | Text commands |
| `persona_agent` | Chat personas | User message | Personalized response |

---

## How Agents Connect (Common Chains)

```
PRODUCT CONTENT PIPELINE:
  pesquisa_agent → anuncio_agent → photo_agent
  (research)       (copy)          (visuals)

BRAND-ALIGNED CONTENT:
  marca_agent → anuncio_agent
  (brand)       (copy)

COURSE PRODUCTION:
  curso_agent → video_agent → voice_agent
  (structure)   (scripts)     (narration)

FULL PRODUCT LAUNCH:
  pesquisa → marca → anuncio → photo → video
```

---

## If You Need Another Agent

Since you only have access to `{{AGENT_NAME}}` right now:

### Option 1: Ask the User
"To complete this task, I would need the `pesquisa_agent` context. Would you like to upload that iso_vectorstore?"

### Option 2: Work with Available Context
"I can provide [partial output] with current context. For [missing part], you would need [other agent]."

### Option 3: Provide Handoff Brief
Generate a handoff brief that can be given to another agent:
```markdown
## Handoff to: {{TARGET_AGENT}}
**From**: {{CURRENT_AGENT}}
**Context**: [summary of what was done]
**Request**: [what the next agent should do]
**Data**: [relevant outputs to pass forward]
```

---

## File Navigation Pattern

When you receive an `iso_vectorstore/`, read files in this order:

```
ORIENTATION (5 min):
  00_SYSTEM_MAP.md     → This file (ecosystem context)
  01_QUICK_START.md    → Agent-specific quick start
  00_MANIFEST.md       → List of available files

UNDERSTANDING (10 min):
  02_PRIME.md          → Agent identity & philosophy
  03_INSTRUCTIONS.md   → How to execute workflows

EXECUTION (as needed):
  06_input_schema.json → What inputs are required
  07_output_template   → What outputs look like
  11_ADW_orchestrator  → Workflow phases
  13-18_HOP_*.md       → Detailed prompt modules
```

---

## Quality Standards (Apply to All Agents)

All CODEXA agents follow:
- **Trinity Output**: .md (human) + .llm.json (structured) + .meta.json (metadata)
- **Quality Gate**: Outputs must score ≥7.0/10.0
- **Brazilian Portuguese**: Primary language for content
- **Marketplace Compliance**: ANVISA, INMETRO, platform rules

---

## Common Variables Across Agents

```
$product_name     → Name of the product being processed
$category         → Product category/niche
$target_audience  → Who the content is for
$marketplace      → Target platform (ML, Shopee, etc.)
$brand_voice      → Tone from marca_agent (if available)
$research_notes   → Output from pesquisa_agent (if available)
```

---

## When You Don't Know What To Do

1. **Read PRIME.md first** - It tells you what this agent does
2. **Check input_schema.json** - It tells you what inputs are needed
3. **Follow the ADW orchestrator** - It tells you the workflow phases
4. **Ask the user** - When context is missing

---

**Template Version**: 1.0.0
**System**: CODEXA Meta-Construction Framework
**For**: External LLM Navigation
