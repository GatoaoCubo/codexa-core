# DESIGN_SYSTEM | CODEXA Design Standards Reference

**Version**: 2.0.0 | **Created**: 2025-11-24
**Type**: Reference Document (points to canonical source)

---

## CANONICAL SOURCE

**Full implementation**: `prompts/layers/06_design_system.md` (802 lines)

This file serves as a reference pointer. The complete design system is maintained as a composable prompt layer for integration with all UI-generating agents.

---

## QUICK REFERENCE

### Core Principles (Lovable Pattern)

1. **Semantic Tokens** - Reference by purpose, not value
2. **HSL Color System** - Human-readable, easy to manipulate
3. **Component-Driven** - Reusable, composable building blocks
4. **Accessibility-First** - WCAG AA minimum, AAA preferred
5. **Responsive by Default** - Mobile-first, progressive enhancement

### Color System (HSL)

```css
/* Semantic tokens - not color names */
--color-primary: hsl(221, 83%, 53%);
--color-background: hsl(0, 0%, 100%);
--color-text: hsl(222, 47%, 11%);
--color-error: hsl(0, 72%, 51%);
--color-success: hsl(142, 71%, 45%);
```

**Don't use**: `--color-blue-500`, `--color-red-600`
**Do use**: `--color-primary`, `--color-error`

### Spacing Scale (8px base)

| Token | Value | Usage |
|-------|-------|-------|
| `--space-1` | 4px | Tight spacing |
| `--space-2` | 8px | Default small |
| `--space-3` | 12px | - |
| `--space-4` | 16px | Default medium |
| `--space-6` | 24px | Section spacing |
| `--space-8` | 32px | Large spacing |

### Typography Scale

| Token | Size | Line Height | Usage |
|-------|------|-------------|-------|
| `--text-xs` | 12px | 1.5 | Captions |
| `--text-sm` | 14px | 1.5 | Secondary |
| `--text-base` | 16px | 1.5 | Body |
| `--text-lg` | 18px | 1.5 | Emphasis |
| `--text-xl` | 20px | 1.4 | Headings |

### Component Patterns

**Buttons**:
- Primary: Solid background, high contrast
- Secondary: Outline, subtle
- Ghost: Transparent, minimal

**Forms**:
- Labels above inputs
- Visible focus states
- Error states with color + icon

**Cards**:
- Consistent padding (`--space-4`)
- Subtle shadow or border
- Rounded corners (`--radius-md`)

---

## INTEGRATION

**To use full guide in prompts**:
```python
from src.runtime import PromptLoader

loader = PromptLoader()
design_system = loader.load_layer("06_design_system")
```

**For UI component generation**:
```yaml
prompt_composition:
  - 01_identity_layer.md
  - 06_design_system.md  # Include for UI tasks
  - 03_tool_usage_layer.md
```

---

## PLATFORM INFLUENCES

Design patterns from leading systems:
- **Lovable**: HSL colors, semantic tokens
- **v0/Vercel**: Component patterns, responsive design
- **Shadcn/Radix**: Accessibility, component API
- **Tailwind**: Utility-first approach

---

**Canonical Source**: `prompts/layers/06_design_system.md`
**Maintained By**: CODEXA Team
**Related**: `templates/CODE_STYLE_GUIDE.md`, `config/design_tokens.yml`
