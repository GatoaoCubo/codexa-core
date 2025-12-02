# SHARED_PRINCIPLES | Universal Agent Guidelines

Princípios que se aplicam a **TODOS** os agents do sistema CODEXA.
Referenciado por cada agent PRIME.md.

**Version**: 1.1.0 | **Created**: 2025-11-29 | **Updated**: 2025-11-29

---

## 1. Tasks vs Roles Pattern

### Principle
**Assign tasks, not roles, to sub-agents**

### Why This Matters
| Roles (Bad) | Tasks (Good) |
|-------------|--------------|
| "You are a UX designer" | "Review this UI for accessibility" |
| Ambiguous, subjective | Specific, measurable |
| Context pollution | Context isolation |
| Inconsistent output | Predictable output |

### How to Apply

```yaml
# ❌ Role-based (vague results)
sub_agent:
  prompt: "You are a senior marketing expert"

# ✅ Task-based (specific results)
sub_agent:
  task: "Extract 5 pain points from these reviews"
  input: $customer_reviews
  output: pain_points_list (JSON array)
  success_criteria: ≥5 distinct pain points
```

### When to Use Sub-agents
- Parallel tasks (independent work)
- Context isolation (prevent pollution)
- Specialized validation
- Artifact generation

### Anti-patterns
- ❌ Giving sub-agents "personalities"
- ❌ Asking them to "think like an expert"
- ❌ Vague instructions without clear output

---

## 2. Human Ownership Principle

### Principle
**AI generates, Human owns**

### Why This Matters
- Accountability remains with the human
- AI lacks judgment for edge cases
- Speed without quality = technical debt
- You sign off on the output, not the AI

### Human Review Checklist

Before accepting any AI output:

```markdown
- [ ] **Accuracy**: Is the information factually correct?
- [ ] **Completeness**: Are all required elements present?
- [ ] **Quality**: Does it meet professional standards?
- [ ] **Compliance**: Does it follow rules/regulations?
- [ ] **Context**: Does it fit the intended use case?
```

### Domain-Specific Reviews

**For Code (codexa_agent)**:
- Security vulnerabilities
- Performance implications
- Test coverage

**For Copy (anuncio_agent)**:
- ANVISA/INMETRO compliance
- Marketplace rules
- Brand voice consistency

**For Research (pesquisa_agent)**:
- Source reliability
- Data freshness
- Bias detection

**For Knowledge (mentor_agent)**:
- Accuracy verification
- Practical applicability
- Seller-appropriate language

### Mindset
> "AI is your capable assistant - fast but needs supervision.
> Never deploy AI output without human validation."

---

## 3. Value Function Pattern

### Principle
**Add intermediate feedback signals, not just final pass/fail**

### Why Binary Feedback Fails
- Feedback comes too late (after full execution)
- No course correction during process
- Wasted effort on fundamentally flawed approaches

### Gradient Feedback Scale

| Confidence | Action |
|------------|--------|
| 0.0 - 0.3 | Stop, escalate, fundamental issue |
| 0.3 - 0.7 | Retry current step with refinement |
| 0.7 - 0.9 | Continue but flag for review |
| 0.9 - 1.0 | Proceed with high confidence |

### Implementation

```python
def value_aware_execution(task, threshold=0.7):
    for step in task.steps:
        result = execute_step(step)
        confidence = assess_confidence(result)

        if confidence < 0.3:
            return escalate_to_human(step, result)
        if confidence < threshold:
            result = retry_with_feedback(step)

    return final_validation(task)
```

### Application by Agent

**anuncio_agent**: Confidence scoring per copy element (title, bullets, description)
**pesquisa_agent**: Confidence per research block (competitor data, pricing, trends)
**mentor_agent**: Confidence per knowledge synthesis (accuracy, completeness)
**codexa_agent**: Confidence per build phase (plan, code, test, review)

---

## 4. Learning to Learn

### Principle
**Optimize for learning speed, not knowledge quantity**

### Paradigm Shift
- ❌ "System that knows how to build 100 things"
- ✅ "System that learns any new thing in 10 minutes"

### Success Metric
**Time to competence** on new task type, NOT quantity of task types known

### Meta-Learning Mechanisms
1. **Template Evolution**: Poor-performing templates → refined
2. **Pattern Extraction**: Successful outputs → patterns → new templates
3. **Feedback Integration**: Failures → root cause → improvement
4. **Knowledge Consolidation**: Multiple experiences → compressed principles

---

## 5. Eval Optimization Trap

### Principle
**Real-world validation trumps benchmark scores**

### The Paradox
AI that scores 99% on evaluations but fails basic real-world tasks

### Detection Signs
- High validator scores, low user satisfaction
- Edge cases cause catastrophic failures
- Metrics improve, real outcomes decline

### Prevention

```yaml
validation_strategy:
  automated:
    - Unit tests (pass/fail)
    - Quality validators (score)
    - Compliance checks (rules)

  real_world:
    - User feedback loop
    - Production monitoring
    - Edge case testing (manual)
    - "Does this make sense?" sanity check
```

---

## 6. Intelligent Fallback (v1.0.0)

### Principle
**Try to resolve before escalating to human**

### Why This Matters
- Reduces human interruptions for simple issues
- Enables refined autonomy (not binary)
- Learns from corrections over time
- Maintains Human Ownership for real decisions

### Fallback Cascade (6 Levels)

| Level | Confidence | Action | Behavior |
|-------|------------|--------|----------|
| 0 | >= 0.9 | `PROCEED` | Continue without interruption |
| 1 | >= 0.7 | `PROCEED_WITH_WARNING` | Continue, log warning |
| 2 | >= 0.5 | `AUTO_CORRECT` | Apply known fix, retry |
| 3 | >= 0.3 | `RETRY_VARIATION` | Try different approach |
| 4 | < 0.3 | `PARTIAL_ESCALATION` | Ask specific question |
| 5 | < 0.3 + critical | `FULL_ESCALATION` | Stop, wait for human |

### Autonomy Policies

| Policy | Max Retries | Escalation Threshold | Use Case |
|--------|-------------|---------------------|----------|
| `development` | 3 | 0.25 | Local dev, experimentation |
| `staging` | 2 | 0.30 | Testing, pre-production |
| `production` | 1 | 0.50 | Live systems, conservative |
| `research` | 5 | 0.15 | Maximum autonomy |

### How to Use (from any agent)

```python
# Import from codexa_agent
import sys
sys.path.insert(0, "../codexa_agent")

from validators.intelligent_fallback import (
    IntelligentFallbackOrchestrator,
    FallbackMixin,
    FallbackAction
)

# Option 1: Use orchestrator directly
orchestrator = IntelligentFallbackOrchestrator(policy="development")
result = orchestrator.handle(confidence=0.5, checkpoints=[...])

if result.should_retry:
    # Apply correction and retry
    pass
elif result.needs_human:
    # Show questions to user
    pass

# Option 2: Use mixin in your validator
class MyValidator(ValueFunctionMixin, FallbackMixin):
    def validate_with_fallback(self, target):
        return self.run_with_fallback(lambda: self.validate(target))
```

### Key Insight
> "Autonomia refinada = tentar resolver sozinho em casos simples,
> escalar rapidamente em casos críticos."

---

## Quick Reference

| Principle | One-liner |
|-----------|-----------|
| **Tasks vs Roles** | Sub-agents do tasks, not play roles |
| **Human Ownership** | AI generates, human validates |
| **Value Function** | Intermediate feedback, not just pass/fail |
| **Learning to Learn** | Speed of learning > quantity of knowledge |
| **Eval Trap** | Real-world > benchmarks |
| **Intelligent Fallback** | Try to resolve before escalating |

---

## How to Reference

Each agent PRIME.md should include:

```markdown
## SHARED PRINCIPLES

This agent follows universal principles defined in [SHARED_PRINCIPLES.md](../SHARED_PRINCIPLES.md):
- Tasks vs Roles (sub-agent design)
- Human Ownership (validation gates)
- Value Function (confidence scoring)

**Domain-specific application**: [agent-specific examples]
```

---

**Version**: 1.0.0
**Status**: Production
**Scope**: All agents in codexa.app/agentes/
