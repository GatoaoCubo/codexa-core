# /codexa-build_prompt | Create HOP Module

**Purpose**: Build HOP (Higher-Order Prompt) module following TAC-7 framework
**Time**: 30-60 minutes | **Output**: Complete TAC-7 compliant HOP

---

## QUICK START

```bash
# Interactive mode
/codexa-build_prompt

# Or direct execution
uv run builders/08_prompt_generator.py
```

---

## INPUT

**Required**:
- Module ID (e.g., "sentiment_analyzer")
- Purpose (1-2 sentences)
- Category (builder|validator|analyzer|transformer)
- Inputs ($variables with types)
- Outputs ($variables with structures)
- Domain context

**Optional**:
- Template reference (existing HOP as base)
- Strict validation mode

---

## TAC-7 FRAMEWORK

**1. MODULE_METADATA**: ID, version, purpose, dependencies, category
**2. INPUT_CONTRACT**: Required/optional $variables + types + validation
**3. OUTPUT_CONTRACT**: Primary/secondary outputs + structure
**4. TASK**: Role, objective, quality standards, constraints
**5. STEPS**: 3-7 numbered actionable steps
**6. VALIDATION**: Quality gates (✅ checks) + score threshold ≥7.0
**7. CONTEXT**: Usage, upstream/downstream, $arguments chaining, assumptions

---

## STEPS

1. **Parse Specification**: Extract module ID, purpose, category, I/O
2. **Generate Metadata**: MODULE_METADATA section
3. **Write INPUT_CONTRACT**: All $inputs with types + validation
4. **Write OUTPUT_CONTRACT**: All $outputs with structures
5. **Write TASK**: Role + objective + standards + constraints
6. **Write STEPS**: 3-7 numbered actionable steps
7. **Write VALIDATION**: Quality gates + score criteria
8. **Write CONTEXT**: Usage + chaining + assumptions
9. **Validate & Finalize**: Run hop_sync_validator | Fix errors

---

## VALIDATION

✅ All 7 TAC-7 sections present
✅ All $variables typed + validated
✅ Steps actionable (3-7)
✅ Quality gates defined
✅ No orphaned variables
✅ hop_sync_validator passes
✅ <1000 lines

---

## TROUBLESHOOTING

**Orphaned variable**: Define in INPUT_CONTRACT or remove usage
**Validator fails**: Check TAC-7 structure | Verify all sections present
**Steps unclear**: Make more specific + actionable
**Quality <7.0**: Add more validation rules | Clarify contracts

---

**Related**: 94_meta_build_prompt_HOP.md (execution logic) | 08_prompt_generator.py (implementation) | 07_hop_sync_validator.py (validation)
