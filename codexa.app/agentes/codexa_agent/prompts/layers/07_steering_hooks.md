# 07_steering_hooks | CODEXA Steering & Hooks System

**Layer Version**: 1.0.0 | **Created**: 2025-11-24
**Purpose**: Define user-configurable behavior modifications, hooks, and customization system
**Category**: Advanced Layer | **Composable**: Yes
**Integration**: All agents, customizable workflows

---

## OVERVIEW

CODEXA supports **steering hooks** - user-defined configurations that modify CODEXA's behavior without changing core prompts. This enables:
- **Personalization**: Adapt CODEXA to individual/team preferences
- **Project-Specific Rules**: Different behavior per project
- **Organization Standards**: Enforce company policies
- **Experimentation**: A/B test different approaches

**Inspired By**: Claude Code's hooks system, Cursor's rules, Windsurf's cascade configuration

---

## HOOK TYPES

### 1. Pre-Execution Hooks

**Trigger**: Before CODEXA executes any tool
**Purpose**: Modify request, add constraints, inject context

**Example Use Cases**:
- Add project-specific context to every request
- Enforce code style preferences
- Block certain operations (safety)
- Inject authentication tokens

**Configuration**:
```yaml
# .codexa/hooks.yml
pre_execution:
  - name: "inject_project_context"
    enabled: true
    priority: 1
    action: "append_to_prompt"
    content: |
      Project-specific context:
      - Framework: Next.js 14 with App Router
      - Database: PostgreSQL with Prisma
      - Testing: Vitest + React Testing Library
      - Style: Tailwind CSS + Shadcn UI

  - name: "enforce_test_creation"
    enabled: true
    priority: 2
    action: "add_requirement"
    content: "Always create tests alongside new code"
```

---

### 2. Post-Execution Hooks

**Trigger**: After CODEXA completes a task
**Purpose**: Validate output, run additional commands, notify

**Example Use Cases**:
- Auto-format code after generation
- Run linters/type checkers
- Send Slack notification on completion
- Update documentation automatically

**Configuration**:
```yaml
post_execution:
  - name: "auto_format"
    enabled: true
    priority: 1
    trigger: "file_modified"
    action: "run_command"
    command: "npm run format"

  - name: "type_check"
    enabled: true
    priority: 2
    trigger: "typescript_file_modified"
    action: "run_command"
    command: "tsc --noEmit"
    fail_on_error: true

  - name: "notify_team"
    enabled: false
    priority: 3
    trigger: "task_completed"
    action: "webhook"
    url: "https://hooks.slack.com/services/..."
    payload:
      text: "CODEXA completed task: {{task_name}}"
```

---

### 3. Validation Hooks

**Trigger**: Before committing changes
**Purpose**: Ensure quality gates pass

**Example Use Cases**:
- Check test coverage threshold
- Verify no console.log statements
- Ensure no TODOs in production code
- Validate API contract compatibility

**Configuration**:
```yaml
validation:
  - name: "test_coverage"
    enabled: true
    action: "run_command"
    command: "npm run test:coverage"
    success_pattern: "Coverage: (\\d+)%"
    min_threshold: 80

  - name: "no_console_logs"
    enabled: true
    action: "grep"
    pattern: "console\\.(log|warn|error)"
    files: "src/**/*.{ts,tsx}"
    allow_count: 0
    message: "Remove console statements before committing"

  - name: "no_todos_in_main"
    enabled: true
    action: "grep"
    pattern: "TODO|FIXME"
    files: "src/**/*"
    branches: ["main", "master", "production"]
    allow_count: 0
```

---

### 4. Tool Override Hooks

**Trigger**: When specific tool is about to be used
**Purpose**: Modify tool behavior, add flags, substitute tools

**Example Use Cases**:
- Always use specific prettier config
- Add --verbose to all test runs
- Use custom git commit template
- Substitute tools (use pnpm instead of npm)

**Configuration**:
```yaml
tool_overrides:
  - tool: "bash"
    pattern: "npm (install|add)"
    substitute: "pnpm $1"
    message: "Using pnpm instead of npm per project standards"

  - tool: "bash"
    pattern: "git commit"
    add_flags: "--signoff"

  - tool: "bash"
    pattern: "pytest"
    add_flags: "-v --cov=src"

  - tool: "edit"
    post_action: "run_command"
    command: "prettier --write {{file_path}}"
```

---

## STEERING CONFIGURATIONS

### Code Style Steering

**Force specific code patterns**:

```yaml
# .codexa/steering.yml
code_style:
  language: "typescript"
  preferences:
    - "Use function declarations, not arrow functions for top-level functions"
    - "Use named exports, avoid default exports"
    - "Prefer async/await over .then()"
    - "Use const for all variables unless reassignment needed"
    - "Destructure props in function parameters"

  forbidden_patterns:
    - pattern: "var "
      message: "Use const or let, never var"
    - pattern: "\\.then\\("
      message: "Use async/await instead of .then()"
      exceptions: ["src/legacy/**"]
```

---

### Testing Steering

```yaml
testing:
  framework: "vitest"
  coverage_threshold: 80
  requirements:
    - "Every exported function must have tests"
    - "Use AAA pattern (Arrange, Act, Assert)"
    - "Mock external dependencies"
    - "No tests should make real API calls"

  file_naming: "{{filename}}.test.ts"
  location: "Same directory as source file"
```

---

### Documentation Steering

```yaml
documentation:
  requirements:
    - "All public functions have JSDoc"
    - "Complex algorithms have explanatory comments"
    - "README updated for new features"

  auto_generate:
    - "Function signatures"
    - "Type definitions"
    - "Example usage"

  forbidden:
    - "Obvious comments (incrementing counter, etc.)"
    - "Commented-out code (delete or explain)"
```

---

### Git Workflow Steering

```yaml
git_workflow:
  commit_format: "conventional"  # feat/fix/docs/style/refactor/test/chore
  branch_naming: "{{type}}/{{description}}"  # feature/add-dark-mode
  require_issue_reference: true

  pre_commit:
    - "Run lint"
    - "Run type check"
    - "Run tests (affected)"

  pre_push:
    - "Run full test suite"
    - "Check coverage threshold"
```

---

## HOOK CONFIGURATION FILE

**Location**: `.codexa/hooks.yml` (project root)

**Full Example**:
```yaml
# CODEXA Hooks Configuration
# Version: 1.0.0

# Global settings
settings:
  enabled: true
  verbose_logging: false
  fail_on_hook_error: true  # Stop if hook fails

# Pre-execution hooks
pre_execution:
  - name: "enforce_branch_protection"
    enabled: true
    priority: 1
    condition: "git_branch == 'main'"
    action: "block"
    message: "Cannot execute on main branch. Switch to feature branch."

  - name: "add_security_context"
    enabled: true
    priority: 2
    action: "append_to_prompt"
    content: |
      Security requirements:
      - Never commit API keys, secrets, or credentials
      - Validate and sanitize all user inputs
      - Use parameterized queries (no string concatenation in SQL)
      - Set proper CORS headers

# Post-execution hooks
post_execution:
  - name: "format_on_save"
    enabled: true
    trigger: "file_modified"
    extensions: [".ts", ".tsx", ".js", ".jsx"]
    action: "run_command"
    command: "prettier --write {{file_path}}"

  - name: "update_imports"
    enabled: true
    trigger: "file_created"
    extensions: [".ts", ".tsx"]
    action: "run_command"
    command: "npx organize-imports-cli {{file_path}}"

# Validation hooks
validation:
  - name: "check_build"
    enabled: true
    action: "run_command"
    command: "npm run build"
    fail_on_error: true

  - name: "check_types"
    enabled: true
    action: "run_command"
    command: "tsc --noEmit"
    fail_on_error: true

# Tool overrides
tool_overrides:
  - tool: "bash"
    pattern: "npm install"
    substitute: "pnpm install"

  - tool: "write"
    extensions: [".ts", ".tsx"]
    post_action: "run_command"
    command: "eslint --fix {{file_path}}"

# Custom rules
custom_rules:
  - name: "no_any_type"
    pattern: ": any"
    files: "src/**/*.ts"
    severity: "error"
    message: "Do not use 'any' type. Use proper type definition."
    exceptions:
      - "src/types/legacy.ts"

  - name: "require_error_handling"
    pattern: "await .+ without try-catch"
    files: "src/**/*.ts"
    severity: "warning"
    message: "Wrap await calls in try-catch for error handling"
```

---

## HOOK EXECUTION FLOW

```
User Request
    │
    ├─→ [Pre-Execution Hooks]
    │       ├─ Inject context
    │       ├─ Add requirements
    │       ├─ Block if needed
    │       └─ Modify request
    │
    ├─→ [CODEXA Processes Request]
    │       ├─ Planning
    │       ├─ Execution
    │       └─ Verification
    │
    ├─→ [Tool Override Hooks]  (during execution)
    │       ├─ Modify tool calls
    │       ├─ Add flags
    │       └─ Substitute tools
    │
    ├─→ [Post-Execution Hooks]
    │       ├─ Format code
    │       ├─ Run linters
    │       ├─ Update docs
    │       └─ Send notifications
    │
    ├─→ [Validation Hooks]
    │       ├─ Run tests
    │       ├─ Check coverage
    │       ├─ Verify quality gates
    │       └─ [FAIL] → Return to execution
    │
    └─→ [Complete] ✅
```

---

## HOOK PRIORITY SYSTEM

**Priority Values**: 1-100 (1 = highest priority)

**Execution Order**: Ascending (1 → 100)

```yaml
pre_execution:
  - name: "critical_safety_check"
    priority: 1  # Runs first

  - name: "add_context"
    priority: 10  # Runs after safety

  - name: "optional_enhancement"
    priority: 50  # Runs last
```

---

## CONDITIONAL HOOKS

**Conditions** - Run hook only when condition met:

```yaml
pre_execution:
  - name: "production_safety"
    enabled: true
    conditions:
      - type: "git_branch"
        operator: "equals"
        value: "main"
    action: "block"
    message: "Cannot modify main branch directly. Use PR workflow."

  - name: "api_key_warning"
    enabled: true
    conditions:
      - type: "file_pattern"
        operator: "matches"
        value: "*.env"
    action: "warn"
    message: "Modifying .env file. Ensure no secrets committed."

  - name: "large_file_warning"
    enabled: true
    conditions:
      - type: "file_size"
        operator: "greater_than"
        value: 1048576  # 1MB
    action: "warn"
    message: "File size exceeds 1MB. Consider optimization or git-lfs."
```

**Supported Condition Types**:
- `git_branch`: Current branch name
- `file_pattern`: File path pattern matching
- `file_size`: File size in bytes
- `file_extension`: File extension
- `time_of_day`: Time-based rules (e.g., no deploys after 5pm)
- `user`: User-specific rules
- `project`: Project-specific rules

---

## ENVIRONMENT-SPECIFIC HOOKS

**Different hooks per environment**:

```yaml
# .codexa/hooks.yml
environments:
  development:
    pre_execution:
      - name: "dev_speed_mode"
        action: "skip_optional_validations"

    validation:
      - name: "relaxed_coverage"
        min_threshold: 60

  staging:
    validation:
      - name: "standard_coverage"
        min_threshold: 75

  production:
    pre_execution:
      - name: "require_approval"
        action: "block"
        message: "Production changes require manual approval"

    validation:
      - name: "strict_coverage"
        min_threshold: 90
      - name: "security_scan"
        enabled: true
      - name: "performance_check"
        enabled: true
```

**Usage**:
```bash
# Set environment
export CODEXA_ENV=production

# Or in config
CODEXA_ENV=staging codexa build feature-x
```

---

## HOOK ACTIONS

### Action Types

1. **block**: Stop execution, show message
2. **warn**: Show warning, continue execution
3. **append_to_prompt**: Add text to CODEXA's context
4. **add_requirement**: Add task requirement
5. **run_command**: Execute shell command
6. **grep**: Search files for pattern
7. **webhook**: Send HTTP request
8. **substitute**: Replace tool/command

### Action Examples

```yaml
# Block action
- name: "block_example"
  action: "block"
  message: "This operation is not allowed"

# Warn action
- name: "warn_example"
  action: "warn"
  message: "Proceed with caution"

# Append to prompt
- name: "add_context"
  action: "append_to_prompt"
  content: "Use TypeScript strict mode"

# Run command
- name: "run_formatter"
  action: "run_command"
  command: "prettier --write src/**/*.ts"
  fail_on_error: false

# Webhook
- name: "notify_slack"
  action: "webhook"
  url: "https://hooks.slack.com/..."
  method: "POST"
  payload:
    text: "Task completed"
```

---

## USER PREFERENCES

**Personal Preferences** (`.codexa/user.yml`):

```yaml
# User-specific preferences (not committed to repo)
user:
  name: "Developer Name"
  email: "dev@example.com"

preferences:
  code_style:
    prefer_semicolons: false
    quote_style: "single"
    trailing_comma: "es5"

  editor:
    line_length: 88
    tab_size: 2

  notifications:
    slack_webhook: "https://hooks.slack.com/..."
    email_on_completion: true

  ai_settings:
    verbosity: "high"  # high/medium/low
    explanation_level: "detailed"  # minimal/standard/detailed
    always_show_reasoning: true
```

---

## TEAM STANDARDS

**Team-wide Standards** (`.codexa/team.yml`, committed to repo):

```yaml
# Team standards enforced for all team members
team:
  name: "Engineering Team"
  standards_version: "1.0.0"

code_standards:
  language: "typescript"
  style_guide: "airbnb"
  formatter: "prettier"
  linter: "eslint"

  required_patterns:
    - "Use async/await"
    - "Prefer functional components (React)"
    - "Use named exports"

  forbidden_patterns:
    - "No console.log in production code"
    - "No any type"
    - "No non-null assertions (!)"

testing_standards:
  framework: "vitest"
  coverage_minimum: 80
  location: "Adjacent to source files"

git_standards:
  commit_format: "conventional"
  branch_naming: "{{type}}/{{ticket}}-{{description}}"
  require_pr: true
  min_approvals: 1
```

---

## IMPLEMENTATION

### Hook Configuration Loader

```python
# builders/adw_modules/hook_loader.py
from pathlib import Path
import yaml
from typing import Optional, Dict, List

class HookConfiguration:
    """Load and manage CODEXA hooks configuration."""

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize hook configuration loader."""
        self.config_path = config_path or Path(".codexa/hooks.yml")
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load hooks configuration from YAML file."""
        if not self.config_path.exists():
            return {"settings": {"enabled": False}}

        with open(self.config_path, encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get_pre_execution_hooks(self) -> List[Dict]:
        """Get pre-execution hooks sorted by priority."""
        hooks = self.config.get("pre_execution", [])
        return sorted(hooks, key=lambda h: h.get("priority", 50))

    def get_post_execution_hooks(self) -> List[Dict]:
        """Get post-execution hooks sorted by priority."""
        hooks = self.config.get("post_execution", [])
        return sorted(hooks, key=lambda h: h.get("priority", 50))

    def is_enabled(self) -> bool:
        """Check if hooks system is enabled."""
        return self.config.get("settings", {}).get("enabled", False)
```

---

## INTEGRATION

This layer defines customization system for:
- All agents (can be steered by hooks)
- All workflows (can be customized)
- Tool execution (can be overridden)
- Validation gates (can be added/modified)

**Composition**:
```yaml
prompt_layers:
  - 01_identity_layer.md
  - 02_operating_modes.md
  - 03_tool_usage_layer.md
  - 07_steering_hooks.md  ← YOU ARE HERE
```

---

**Layer Maintained By**: CODEXA Team
**Last Updated**: 2025-11-24
**Related Layers**: 02_operating_modes.md, 03_tool_usage_layer.md, 08_workflows.md
**Influenced By**: Claude Code hooks, Cursor rules, Windsurf cascade, pre-commit hooks
