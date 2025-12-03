# /codexa-build-command | Create Slash Command

**Purpose**: Build new slash command for Claude Code CLI
**Time**: 15-30 minutes | **Output**: Command file ready for use

---

## QUICK START

```bash
# Interactive mode
/codexa-build-command

# Or direct execution
uv run codexa.app/agentes/codexa_agent/builders/05_command_generator.py
```

---

## INPUT

**Required**:
- Command name (e.g., "analyze_code", "generate_docs")
- Purpose (1-2 sentences)
- Parameters (if any)
- Expected behavior

**Optional**:
- Template reference (existing command to use as base)
- Output format preferences

---

## COMMAND STRUCTURE

```markdown
# /command_name | Short Description

**Purpose**: What it does
**Usage**: /command_name [args]

## TASK
What the command should accomplish

## STEPS
1. Step 1
2. Step 2
...

## OUTPUT
Expected result

## EXAMPLES
Usage examples
```

---

## STEPS

1. **Define Command**: Name + purpose + parameters
2. **Write Task Section**: Clear objective + constraints
3. **Define Steps**: Numbered actionable steps (3-7)
4. **Specify Output**: Expected result format
5. **Add Examples**: 2-3 usage examples
6. **Validate**: Test command execution
7. **Document**: Usage instructions

---

## VALIDATION

- Command name follows convention (verb_noun or action_target)
- Purpose clear (1-2 sentences)
- Steps actionable (3-7 numbered)
- Examples provided (>=2)
- Output format specified
- Command file <1000 lines

---

## TROUBLESHOOTING

**Command not recognized**: Check filename | Verify placement in .claude/commands/ directory
**Execution fails**: Check syntax | Test steps manually
**Unclear behavior**: Add more examples | Clarify steps

---

**Related**: Existing commands (examples) | codexa.app/agentes/codexa_agent/builders/05_command_generator.py (implementation)
