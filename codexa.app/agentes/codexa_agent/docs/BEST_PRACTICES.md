# BEST_PRACTICES | Compiled from 30+ AI Coding Platforms

**Version**: 1.0.0 | **Created**: 2025-11-24
**Purpose**: Actionable best practices for AI-assisted development
**Source**: Patterns extracted from 30+ leading platforms

---

## OVERVIEW

These practices are distilled from analyzing Claude Code, Devin, Cursor, Windsurf, Lovable, Poke, and 25+ other AI coding platforms. Each practice includes its source, rationale, and implementation guidance.

---

## 1. PLANNING PRACTICES

### 1.1 Always Research Before Writing

**Source**: Devin, Cursor
**Rationale**: Understanding existing code prevents conflicts and enables better solutions

```yaml
practice:
  name: "Research-First Development"
  steps:
    1. Explore codebase structure (Glob)
    2. Search for similar patterns (Grep)
    3. Read relevant files (Read)
    4. Document findings
    5. Only then plan changes
  anti_pattern: "Jump straight to coding"
```

**DO**:
- Spend 20-30% of time understanding before changing
- Document what you find
- Identify existing patterns to follow

**DON'T**:
- Start writing code immediately
- Assume you know the codebase
- Ignore existing implementations

---

### 1.2 Separate Planning from Execution

**Source**: Devin, Antigravity
**Rationale**: Prevents accidental changes during exploration

```yaml
practice:
  name: "Two-Phase Development"
  phases:
    planning:
      access: read_only
      activities: [explore, analyze, plan]
      output: implementation_plan.md

    execution:
      access: write
      activities: [implement, test, document]
      input: approved_plan
```

**DO**:
- Use separate "modes" for planning vs execution
- Get approval on plan before implementing
- Document the plan formally

**DON'T**:
- Mix exploration with implementation
- Skip the planning phase for "simple" tasks
- Implement without a written plan

---

### 1.3 Generate Artifacts

**Source**: Antigravity, Linear
**Rationale**: Creates reusable documentation and audit trail

```yaml
practice:
  name: "Artifact-Driven Development"
  required_artifacts:
    - implementation_plan.md: "Before coding"
    - task_checklist.md: "During coding"
    - walkthrough.md: "After complex features"
```

**DO**:
- Create implementation plan before coding
- Maintain living task checklist
- Generate walkthrough for complex features

**DON'T**:
- Keep plans only in your head
- Skip documentation for "obvious" changes
- Forget to update checklists

---

## 2. EXECUTION PRACTICES

### 2.1 Declare Task Boundaries

**Source**: Claude Code
**Rationale**: Provides visibility and enables safe rollback

```yaml
practice:
  name: "Explicit Task Boundaries"
  format:
    TASK_BOUNDARY: descriptive_name
    SCOPE: what_this_changes
    FILES: affected_files
    ROLLBACK: how_to_undo
```

**DO**:
- Declare boundaries before each major operation
- Include rollback information
- Keep scope focused

**DON'T**:
- Make changes without declaring intent
- Combine unrelated changes in one boundary
- Forget rollback strategy

---

### 2.2 Make Minimal Changes

**Source**: Claude Code, Cursor
**Rationale**: Reduces risk and improves reviewability

```yaml
practice:
  name: "Minimal Change Principle"
  rules:
    - Change only what's necessary
    - Don't refactor during bug fixes
    - Don't add features during fixes
    - Don't improve "while we're here"
```

**DO**:
- Fix the specific issue
- Keep changes focused
- Create separate tasks for improvements

**DON'T**:
- Refactor surrounding code
- Add "nice to have" features
- Change code style of untouched lines

---

### 2.3 Commit Incrementally

**Source**: Aider, Git best practices
**Rationale**: Enables easy rollback and clear history

```yaml
practice:
  name: "Incremental Commits"
  pattern:
    - One logical change per commit
    - Meaningful commit messages
    - Tests pass before commit
  message_format: "type(scope): description"
```

**DO**:
- Commit after each logical step
- Write meaningful commit messages
- Ensure tests pass before committing

**DON'T**:
- Batch many changes in one commit
- Use vague commit messages
- Commit broken code

---

## 3. CODE QUALITY PRACTICES

### 3.1 Write Explicit Code

**Source**: Cursor, Windsurf
**Rationale**: Self-documenting code reduces maintenance burden

```yaml
practice:
  name: "Explicit Over Implicit"
  guidelines:
    - Full type annotations
    - Descriptive variable names
    - Explicit imports (no wildcards)
    - Clear function signatures
```

**DO**:
```python
# Good
def calculate_total_price(
    items: list[CartItem],
    discount_percent: float = 0.0
) -> Decimal:
    """Calculate total price with optional discount."""
    subtotal = sum(item.price * item.quantity for item in items)
    discount = subtotal * (discount_percent / 100)
    return subtotal - discount
```

**DON'T**:
```python
# Bad
def calc(items, d=0):
    return sum(i.p * i.q for i in items) * (1 - d/100)
```

---

### 3.2 Validate at Boundaries

**Source**: Windsurf
**Rationale**: Trust internal code, validate external inputs

```yaml
practice:
  name: "Boundary Validation"
  boundaries:
    - User input
    - API responses
    - File reads
    - External services
  internal:
    - Trust function parameters
    - Don't over-validate
```

**DO**:
```python
# Validate at API boundary
@app.post("/users")
def create_user(data: UserCreate):  # Pydantic validates
    return user_service.create(data)  # Internal - trust it

# Internal function - no validation needed
def _format_user_name(first: str, last: str) -> str:
    return f"{first} {last}"  # Trust callers
```

**DON'T**:
```python
# Over-validation in internal code
def _format_user_name(first, last):
    if not isinstance(first, str):  # Unnecessary
        raise TypeError("first must be string")
    if not isinstance(last, str):   # Unnecessary
        raise TypeError("last must be string")
    return f"{first} {last}"
```

---

### 3.3 Follow Naming Conventions

**Source**: All platforms
**Rationale**: Consistent naming improves readability

```yaml
practice:
  name: "Consistent Naming"
  conventions:
    python:
      variables: snake_case
      functions: snake_case (verb_noun)
      classes: PascalCase
      constants: UPPER_SNAKE
    typescript:
      variables: camelCase
      functions: camelCase (verbNoun)
      classes: PascalCase
      constants: UPPER_SNAKE
```

**DO**:
```python
# Python
user_count = 0
def get_active_users() -> list[User]: ...
class UserRepository: ...
MAX_RETRY_COUNT = 3
```

```typescript
// TypeScript
const userCount = 0;
function getActiveUsers(): User[] { ... }
class UserRepository { ... }
const MAX_RETRY_COUNT = 3;
```

---

### 3.4 Keep Functions Short

**Source**: Cursor, Clean Code
**Rationale**: Short functions are easier to understand and test

```yaml
practice:
  name: "Function Size Limits"
  limits:
    target: 10-30 lines
    maximum: 50 lines
    ideal: "Fits on one screen"
```

**DO**:
- Extract helper functions
- Single responsibility per function
- Early returns for edge cases

**DON'T**:
- Write functions over 50 lines
- Mix multiple concerns
- Deep nesting (>3 levels)

---

## 4. TESTING PRACTICES

### 4.1 Write Test Before Fix

**Source**: Cursor, TDD
**Rationale**: Ensures fix actually addresses the issue

```yaml
practice:
  name: "Test-First Bug Fixing"
  steps:
    1. Write failing test that reproduces bug
    2. Verify test fails
    3. Implement fix
    4. Verify test passes
    5. Check no regressions
```

**DO**:
```python
# 1. Write failing test
def test_login_with_special_chars():
    result = login("user@test", "pass&word!")
    assert result.success  # This should fail initially

# 2. Fix the bug
# 3. Test now passes
```

---

### 4.2 Test Edge Cases

**Source**: Windsurf, Devin
**Rationale**: Edge cases cause most production bugs

```yaml
practice:
  name: "Edge Case Coverage"
  always_test:
    - Empty inputs
    - Null/None values
    - Boundary values (0, -1, max)
    - Special characters
    - Unicode
    - Very large inputs
```

**DO**:
```python
@pytest.mark.parametrize("input,expected", [
    ("", []),           # Empty
    (None, []),         # Null
    ("a", ["a"]),       # Single
    ("a,b,c", ["a","b","c"]),  # Normal
    ("a,,b", ["a","b"]),  # Double delimiter
])
def test_split_string(input, expected):
    assert split_string(input) == expected
```

---

## 5. DOCUMENTATION PRACTICES

### 5.1 Document Public APIs

**Source**: All platforms
**Rationale**: Public APIs need clear documentation

```yaml
practice:
  name: "API Documentation"
  required_for:
    - Public functions
    - Class methods
    - Module exports
  optional_for:
    - Private helpers (_prefix)
    - Internal utilities
```

**DO**:
```python
def process_order(
    order: Order,
    apply_discount: bool = True
) -> ProcessedOrder:
    """
    Process an order and calculate final totals.

    Args:
        order: The order to process
        apply_discount: Whether to apply eligible discounts

    Returns:
        ProcessedOrder with calculated totals

    Raises:
        InvalidOrderError: If order has no items
    """
```

---

### 5.2 Explain Why, Not What

**Source**: Claude Code, Clean Code
**Rationale**: Code shows what, comments explain why

```yaml
practice:
  name: "Why Comments"
  good_comments:
    - Business logic reasons
    - Non-obvious decisions
    - Workaround explanations
    - Performance considerations
  bad_comments:
    - Describing what code does
    - Obvious explanations
    - Outdated information
```

**DO**:
```python
# Retry up to 3 times because external API has intermittent failures
# See incident report: INC-1234
for attempt in range(3):
    try:
        return api.call()
    except TimeoutError:
        continue
```

**DON'T**:
```python
# Loop 3 times
for i in range(3):  # Set i to 0, 1, 2
    try:
        return api.call()  # Call the API
    except TimeoutError:
        continue  # Continue to next iteration
```

---

## 6. PARALLEL EXECUTION PRACTICES

### 6.1 Identify Independent Tasks

**Source**: Poke
**Rationale**: Only independent tasks can run in parallel

```yaml
practice:
  name: "Task Independence Analysis"
  criteria:
    independent:
      - Different files
      - No shared state
      - No call dependencies
    dependent:
      - Same file
      - Shared variables
      - Import relationships
```

**DO**:
- Analyze dependencies before parallelizing
- Group independent tasks into batches
- Maintain sync points between dependent tasks

---

### 6.2 Handle Failures Gracefully

**Source**: Poke, distributed systems
**Rationale**: One failure shouldn't stop everything

```yaml
practice:
  name: "Failure Isolation"
  strategies:
    - Isolate failed task
    - Continue other tasks
    - Retry failed task (max 2)
    - Report failures for review
```

**DO**:
```python
results = []
for task in parallel_tasks:
    try:
        result = await task.execute()
        results.append(("success", result))
    except Exception as e:
        results.append(("failed", str(e)))
        # Continue with other tasks
```

---

## 7. WORKFLOW PRACTICES

### 7.1 Use Quality Gates

**Source**: Devin, CI/CD
**Rationale**: Catch issues early

```yaml
practice:
  name: "Quality Gates"
  gates:
    - After planning: User approval
    - After implementation: Tests pass
    - After tests: Code quality check
    - Before merge: Full validation
```

**DO**:
- Define clear quality thresholds
- Automate gate checks
- Block progression on failure

---

### 7.2 Generate Reports

**Source**: Claude Code, All validators
**Rationale**: Structured reports enable automation

```yaml
practice:
  name: "##report Standard"
  format:
    module: string
    version: string
    status: success|warning|error
    metrics: {}
    issues: []
```

**DO**:
```yaml
##report:
  module: code_quality_validator
  version: 2.0.0
  status: warning
  metrics:
    files_checked: 10
    quality_score: 0.87
  issues:
    - severity: warning
      message: "Missing docstring"
      file: "utils.py"
      line: 42
```

---

## 8. ANTI-PATTERNS TO AVOID

### 8.1 Premature Abstraction

```yaml
anti_pattern:
  name: "Premature Abstraction"
  symptoms:
    - Creating interfaces for single implementations
    - Building "flexible" systems before needed
    - Over-engineering simple features
  solution: "Wait for 3 use cases before abstracting"
```

### 8.2 Shotgun Debugging

```yaml
anti_pattern:
  name: "Shotgun Debugging"
  symptoms:
    - Randomly changing code hoping it works
    - Not understanding root cause
    - Adding try/except to hide errors
  solution: "Use systematic root cause analysis"
```

### 8.3 Copy-Paste Programming

```yaml
anti_pattern:
  name: "Copy-Paste Programming"
  symptoms:
    - Duplicating code blocks
    - Similar functions with slight variations
    - Fixing same bug in multiple places
  solution: "Extract shared functionality"
```

### 8.4 Magic Numbers/Strings

```yaml
anti_pattern:
  name: "Magic Values"
  symptoms:
    - Hardcoded numbers without explanation
    - String literals repeated
    - Configuration in code
  solution: "Use named constants"
```

### 8.5 Eval Optimization Trap

```yaml
anti_pattern:
  name: "Eval Optimization Trap"
  symptoms:
    - High validator scores but poor real-world results
    - System "passes tests" but users complain
    - Metrics improve while actual value decreases
    - Agent loops infinitely on edge cases despite 95%+ accuracy
  causes:
    - Validators too specific to test data
    - Metrics disconnected from user value
    - Optimizing for measurable over meaningful
    - Benchmark gaming (system learns to pass tests, not solve problems)
  solution: "Real-world validation + user testing + impact measurement"
```

**The Paradox**: AI that scores 99% on evaluations but fails on basic real-world tasks

**Why it happens**:
- Training/validation optimizes for specific metrics
- Those metrics don't capture real-world complexity
- System learns shortcuts that work on tests but fail in production

**Real example**:
```
Eval: "Fix this bug in the code"
Score: 95% success rate on benchmark

Reality: Agent fixes bug → introduces new bug → reverts →
reintroduces original bug → infinite loop
```

**Detection**:
- [ ] User satisfaction < validator scores
- [ ] Edge cases cause catastrophic failures
- [ ] System "passes" but doesn't deliver value
- [ ] Improvement on metrics, decline in real outcomes

**Solution checklist**:
1. **Validate with real users** - not just automated tests
2. **Measure impact** - business outcomes, not proxy metrics
3. **Test edge cases manually** - validators miss what they weren't designed for
4. **Add "sanity checks"** - does this output make sense to a human?

---

## 9. PERFORMANCE PRACTICES

### 9.1 Measure Before Optimizing

**Source**: All platforms
**Rationale**: Don't optimize without data

```yaml
practice:
  name: "Data-Driven Optimization"
  steps:
    1. Measure current performance
    2. Identify bottleneck
    3. Optimize specific bottleneck
    4. Measure improvement
    5. Repeat if needed
```

### 9.2 Optimize Hot Paths

**Source**: Performance engineering
**Rationale**: Focus on code that runs frequently

```yaml
practice:
  name: "Hot Path Focus"
  priorities:
    high: "Called 1000+ times"
    medium: "Called 100+ times"
    low: "Called < 10 times"
```

---

## 10. SECURITY PRACTICES

### 10.1 Never Trust Input

**Source**: OWASP, Windsurf
**Rationale**: All external input is potentially malicious

```yaml
practice:
  name: "Input Sanitization"
  always_sanitize:
    - User input
    - URL parameters
    - File uploads
    - API responses from untrusted sources
```

### 10.2 Keep Secrets Secret

**Source**: All platforms
**Rationale**: Exposed secrets compromise security

```yaml
practice:
  name: "Secret Management"
  rules:
    - Never commit secrets
    - Use environment variables
    - Rotate secrets regularly
    - Audit secret access
```

---

## PRACTICE CHECKLIST

### Before Starting
- [ ] Research existing code
- [ ] Create implementation plan
- [ ] Get plan approval

### During Development
- [ ] Declare task boundaries
- [ ] Make minimal changes
- [ ] Write tests
- [ ] Commit incrementally

### Before Completing
- [ ] Run all tests
- [ ] Run code quality validator
- [ ] Update documentation
- [ ] Generate ##report

---

**Version**: 1.1.0
**Last Updated**: 2025-11-29
**Sources**: 30+ AI coding platforms + Superintelligence insights
**Status**: Complete Reference
**Maintainer**: CODEXA Team
