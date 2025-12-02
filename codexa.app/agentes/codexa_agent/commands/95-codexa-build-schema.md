# /codexa-build_schema | Create Output Schema

**Purpose**: Build JSON Schema or execution plan with validation rules
**Time**: 10-20 minutes | **Output**: Validated schema ready for use

---

## QUICK START

```bash
# Interactive mode
/codexa-build_schema

# Specify type
/codexa-build_schema --type="json_schema"
/codexa-build_schema --type="execution_plan"
```

---

## INPUT

**Required**:
- Schema type (JSON Schema | Execution Plan)
- Data structure description
- Required fields
- Validation rules

**Optional**:
- Examples (for testing)
- Default values
- Custom validators

---

## SCHEMA TYPES

**JSON Schema**: Structured data validation
- Properties + types
- Required fields
- Constraints (min/max, patterns, enums)
- Examples

**Execution Plan**: Workflow specification
- Phases/steps
- Dependencies
- Input/output mappings
- Validation gates

---

## STEPS

1. **Define Structure**: Fields + types + nesting
2. **Add Validation**: Required fields + constraints + patterns
3. **Write Examples**: Sample valid/invalid data
4. **Test Schema**: Validate against examples
5. **Document**: Usage instructions + edge cases

---

## VALIDATION

✅ Schema valid (parseable JSON)
✅ All required fields documented
✅ Validation rules complete
✅ Examples provided (≥2)
✅ Edge cases handled
✅ Clear error messages

---

## TROUBLESHOOTING

**Schema invalid**: Check JSON syntax | Verify structure
**Validation too strict/loose**: Adjust constraints | Add/remove rules
**Examples fail**: Fix schema or examples | Check types
**Unclear errors**: Add better descriptions | Specify error messages

---

**Related**: JSON Schema docs | Example schemas | Validators
