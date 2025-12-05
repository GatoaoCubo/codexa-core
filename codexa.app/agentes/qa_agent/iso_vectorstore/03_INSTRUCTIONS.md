<!-- iso_vectorstore -->
<!--
  Source: INSTRUCTIONS.md
  Agent: qa_agent
  Synced: 2025-12-05
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# INSTRUCTIONS | qa_agent

## QUICK START

```bash
# 1. Prime the agent
/prime-qa

# 2. Run full suite
/qa-run-all

# 3. Check specific area
/qa-check pages|checkout|seo|a11y|chat|forms
```

## EXECUTION MODES

### Mode 1: Full Suite (30-45 min)

Complete validation of all aspects.

```
Steps:
1. Build verification (npm run build)
2. All pages load check
3. All images accessible
4. SEO audit all pages
5. Checkout flow test
6. AI chat test (4 scenarios)
7. B2B form submission test
8. Accessibility audit
9. Performance check (Lighthouse)
10. Generate full report
```

### Mode 2: Pre-Deploy (10-15 min)

Quick check before deployment.

### Mode 3: Post-Deploy (5 min)

Smoke test after deployment.

### Mode 4: Specific Check

Single area validation.

```
/qa-check pages     # All page loads
/qa-check checkout  # Checkout flow only
/qa-check seo       # SEO elements only
/qa-check a11y      # Accessibility only
/qa-check chat      # AI Chat only
/qa-check forms     # Forms only
```

## BEST PRACTICES

1. **Run on staging first** - Validate before production
2. **Screenshot failures** - Visual evidence helps debugging
3. **Log everything** - Detailed logs for troubleshooting
4. **Retry flaky tests** - Network issues happen
5. **Update selectors** - UI changes break tests
6. **Track metrics** - Compare runs over time

---

**Version**: 1.0.0
**Last Updated**: 2025-12-05
