# /codexa-build_agent | Create Complete Isolated Agent

**Purpose**: Build production-ready agent using 5-phase meta-constructor
**Time**: 20-40 minutes (automated) | **Output**: 8 artifacts (MASTER_INSTRUCTIONS, AGENT_CONFIGURATION, README, etc.)

---

## QUICK START

```bash
# Interactive mode
/codexa-build_agent

# Or direct execution
uv run builders/02_agent_meta_constructor.py "Your agent description here"

# Example
uv run builders/02_agent_meta_constructor.py "Sentiment analysis agent for product reviews that generates scores (positive/neutral/negative) with detailed justifications"
```

---

## INPUT

**Required**: Clear agent description (1-3 sentences, 20-500 chars) describing purpose + domain + capabilities

**Optional**:
- Model: "opus" (default) or "sonnet"
- Target directory: Custom output path
- Verbose: Detailed logging

---

## 5-PHASE WORKFLOW

**Phase 1**: Plan - Strategic planning with [OPEN_VARIABLES] | Output: $plan
**Phase 2**: Build - Construct artifacts (MASTER_INSTRUCTIONS, AGENT_CONFIGURATION, VECTOR_STORE_MANIFEST, OUTPUT_SCHEMA) | Output: $artifacts
**Phase 3**: Test - Validation + test scenarios | Output: $test_results
**Phase 4**: Review - Critical analysis + quality score | Output: $review_notes, $quality_score
**Phase 5**: Document - Generate README, DEPLOYMENT_GUIDE, EXAMPLES, META_CONSTRUCTION_LOG | Output: $documentation

---

## OUTPUT

**8 Artifacts Created**:
1. MASTER_INSTRUCTIONS.md (2000-5000 words)
2. AGENT_CONFIGURATION.json (OpenAI config)
3. VECTOR_STORE_MANIFEST.md (knowledge files)
4. OUTPUT_SCHEMA.md (structure)
5. README.md (overview)
6. DEPLOYMENT_GUIDE.md (steps)
7. EXAMPLES.md (usage examples)
8. META_CONSTRUCTION_LOG.md (traceability)

---

## VALIDATION

✅ All 5 phases completed
✅ 8 artifacts present
✅ MASTER_INSTRUCTIONS 2000-5000 words
✅ Valid JSON configuration
✅ Quality score ≥7.0/10.0
✅ No [PLACEHOLDER] text
✅ Full traceability

---

## TROUBLESHOOTING

**Description too short**: Ensure ≥20 chars | Include purpose + domain
**Phase fails**: Check prerequisites (Python, uv, ANTHROPIC_API_KEY) | Run with --verbose
**Quality <7.0**: Review $review_notes | Re-run weakest phase
**Artifacts incomplete**: Check $plan completeness | Verify Phase 2 execution

---

**Related**: 91_meta_build_agent_HOP.md (execution logic) | 97_ADW_NEW_AGENT_WORKFLOW.md (workflow) | 02_agent_meta_constructor.py (implementation)
