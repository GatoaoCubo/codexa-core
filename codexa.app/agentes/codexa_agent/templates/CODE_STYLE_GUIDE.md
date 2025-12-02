# CODE_STYLE_GUIDE | CODEXA Code Standards Reference

**Version**: 2.0.0 | **Created**: 2025-11-24
**Type**: Reference Document (points to canonical source)

---

## CANONICAL SOURCE

**Full implementation**: `prompts/layers/05_code_conventions.md` (918 lines)

This file serves as a reference pointer. The complete code style guide is maintained as a composable prompt layer for integration with all agents.

---

## QUICK REFERENCE

### Core Principles

1. **Readability First** - Code is read 10x more than written
2. **Explicit Over Implicit** - High verbosity, make intent clear (Cursor pattern)
3. **Type Safety Everywhere** - Full type annotations
4. **Validate at Boundaries** - Trust internal code (Windsurf pattern)
5. **Conventional** - Follow language idioms

### Naming Conventions

| Element | Python | TypeScript |
|---------|--------|------------|
| Variables | `snake_case` | `camelCase` |
| Functions | `verb_noun` | `verbNoun` |
| Classes | `PascalCase` | `PascalCase` |
| Constants | `UPPER_SNAKE` | `UPPER_SNAKE` |
| Files | `snake_case.py` | `kebab-case.ts` |

### Code Structure Limits

| Metric | Target | Maximum |
|--------|--------|---------|
| Function length | 10-30 lines | 50 lines |
| File length | 200-400 lines | 600 lines |
| Line length | 80 chars | 88 chars (Black) |

### Documentation Requirements

- **Public functions**: Must have docstring/JSDoc
- **Complex logic**: Explain "why", not "what"
- **Workarounds**: Document with issue reference

### Anti-Patterns to Avoid

- Magic numbers/strings (use constants)
- Premature abstraction
- Mutable default arguments (Python)
- Catching broad exceptions
- Over-validation in internal code

---

## INTEGRATION

**To use full guide in prompts**:
```python
from src.runtime import PromptLoader

loader = PromptLoader()
code_conventions = loader.load_layer("05_code_conventions")
```

**To validate code quality**:
```bash
python validators/13_code_quality_validator.py --file path/to/file.py
```

---

## PLATFORM INFLUENCES

Patterns synthesized from 30+ AI coding platforms:
- **Cursor**: High verbosity, explicit types
- **Windsurf**: Defensive programming, boundary validation
- **Claude Code**: Clear error messages, self-documenting
- **Devin**: Structured documentation
- **Copilot**: Conventional patterns

---

**Canonical Source**: `prompts/layers/05_code_conventions.md`
**Maintained By**: CODEXA Team
**Related**: `templates/DESIGN_SYSTEM.md`, `validators/13_code_quality_validator.py`
