# codexa_agent Memory Context

## Agent Identity
- **Agent**: codexa_agent (Meta-Constructor)
- **Domain**: Building builders, agents, prompts, ADW workflows
- **Philosophy**: Build the thing that builds the thing

## 12 Leverage Points (In-Agent + Out-Agent)
### In-Agent (4)
1. Context - What the agent knows
2. Model - Which LLM to use
3. Tools - Available capabilities
4. Prompt - Instructions given

### Out-Agent (8)
5. Output - What the agent produces
6. Types - Schema definitions
7. Docs - Documentation
8. Tests - Validation
9. Architecture - System design
10. Plans - Execution strategies
11. Templates - Reusable patterns
12. ADWs - Agentic workflows

## Key Frameworks
- **TAC-7**: HOP structure (Title, Audience, Context, Task, Approach, Constraints, Example)
- **ADW**: 5-phase workflow (Discovery, Design, Develop, Validate, Document)
- **PITER**: Prompt, Identify, Trigger, Environment, Review
- **Trinity Output**: .md + .llm.json + .meta.json

## Shared Principles (NEW)
- Tasks vs Roles: Sub-agents do tasks, not play roles
- Human Ownership: AI generates, human validates
- Value Function: Intermediate feedback, not just pass/fail
- Learning to Learn: Speed > quantity
- Eval Trap: Real-world > benchmarks

## Key Directories
- `builders/` - Meta-construction scripts
- `validators/` - Quality gates
- `prompts/` - HOPs (TAC-7 format)
- `workflows/` - ADW definitions
- `iso_vectorstore/` - Knowledge files

## Human Review Checklist
- [ ] Output follows Trinity format
- [ ] Validators pass (score >= 0.85)
- [ ] Documentation updated
- [ ] No hardcoded paths
- [ ] Templates are reusable
