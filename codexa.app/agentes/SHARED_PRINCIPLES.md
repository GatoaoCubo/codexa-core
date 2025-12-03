# SHARED_PRINCIPLES.md

**Cross-Agent Standards** | v2.0.0 | 2025-12-03

---

## Overview

Core operational principles followed by all agents in the codexa.app system. These guidelines ensure consistency, quality, and interoperability across specialized domains.

---

## 1. Trinity Pattern

Every domain follows a three-layer navigation structure:

```
PRIME.md        → Entry point (what/when/why) ← READ FIRST
INSTRUCTIONS.md → Operations (how to execute)
README.md       → Reference (architecture, details)
```

**Usage**:
- New to domain? Start with `PRIME.md` (2min context)
- Need to execute? Read `INSTRUCTIONS.md`
- Need deep details? Read `README.md`

---

## 2. Quality Gate

All outputs must meet minimum quality standards:

```
Threshold: ≥7.0/10.0
```

**Process**:
1. Generate output
2. Evaluate against rubric
3. IF score < 7.0 → Retry once with improvements
4. IF still < 7.0 → Flag for manual review

**Never** ship below-threshold work without explicit user approval.

---

## 3. Discovery-First Approach

Before creating new artifacts, search for existing templates:

```
1. Check agent's iso_vectorstore/
2. Search workflows/ and prompts/
3. Use mcp__scout__discover("description")
4. Reuse > Adapt > Create new
```

**Benefits**: Consistency, faster execution, less duplication.

---

## 4. Error Recovery Strategies

Handle failures intelligently based on error type:

| Strategy | When to Use | Example |
|----------|-------------|---------|
| **Retry** | Transient errors | API timeout, rate limit |
| **Fallback** | Alternative exists | Secondary model, cached data |
| **Fail Fast** | Unrecoverable | Missing credentials, invalid config |
| **Degrade** | Partial success OK | 18/22 items succeeded |

**Always log errors with context. Never fail silently.**

---

## 5. Placeholder Syntax

Use `{{PLACEHOLDER}}` for brand-agnostic deliverables:

```
✗ "codexa.app"        → ✓ {{BRAND_URL}}
✗ "#0D9488"           → ✓ {{PRIMARY_COLOR}}
✗ "Codexa"            → ✓ {{BRAND_NAME}}
```

**When to distill**:
- Marketing/sales materials
- Course/content templates
- Multi-brand deliverables

**When to skip**:
- Internal workflows (ADWs, HOPs)
- System config
- Single-use drafts

**Reference**: [docs/PLACEHOLDERS.md](../../docs/PLACEHOLDERS.md)

---

## 6. Meta-Construction Pattern

Build systems that build artifacts:

```
1 Template → N Plans → M Results
```

**When to go meta**:

| Signal | Go Meta | Do Direct |
|--------|---------|-----------|
| Repetition | Task repeats 3+ times | One-off task |
| Scale | 5+ similar items | 1-2 items |
| Similarity | 80%+ overlap | Unique requirements |

**Process**: Discover → Plan → Generate → Validate → Iterate

---

## Application

These principles are **guidelines for autonomous execution**, not rigid rules. Apply with context-aware judgment:

- Adapt to domain-specific needs
- Balance speed vs. thoroughness
- Prioritize user outcomes over process compliance

---

**Version**: 2.0.0 | **Type**: Cross-Agent Standards | **Updated**: 2025-12-03
