# /orchestrator | Track Agent Consumption & Creation

**Purpose**: Monitor agent resource usage (consumption) and output quality (creation)
**Usage**: Track costs | Measure quality | Analyze efficiency

---

## QUICK START

```bash
cd orchestrator
python example_usage.py
```

**Generates**: Execution summaries | Consumption/creation reports | JSON data in `data/executions/`

---

## TRACKED METRICS

### Consumption
- LLM tokens used + costs
- Files read
- API calls made
- Web fetches performed

### Creation
- Files written
- Quality scores
- Validation results
- Output artifacts

---

## USE CASES

**Cost Analysis**: Track token usage + API costs per agent
**Quality Monitoring**: Measure output quality scores
**Efficiency**: Identify expensive operations
**Optimization**: Find bottlenecks in workflows

---

**Related**: Agent metrics | Cost tracking | Quality monitoring
