# Agents Output Directory

This directory contains outputs from CODEXA builder executions.

## 📁 Directory Structure

```
agents/
├── README.md                    # This file
├── .gitignore                   # Git ignore rules
├── _examples/                   # Reference examples (version controlled)
│   └── example_meta_constructor_5_phases/  # Full 5-phase workflow example
└── [temporary_outputs]/         # Runtime outputs (gitignored, auto-cleaned)
```

## 🎯 Purpose

When you run builders like:
- `02_agent_meta_constructor.py` - Creates multi-phase agent workflows
- `08_prompt_generator.py` - Executes ad-hoc prompts

They generate outputs in this directory with a unique ADW ID (e.g., `dd2b5962/`).

## 📋 Examples Policy

### ✅ What's in `_examples/`

**Maintained Examples** (1 per workflow type):

| Example Name | Workflow Type | Description |
|--------------|---------------|-------------|
| `example_meta_constructor_5_phases/` | Meta-Constructor | Full 5-phase workflow: Plan → Build → Test → Review → Document |

These are **reference implementations** showing:
- Complete workflow execution traces
- $argument chaining between phases
- Output structure and metadata
- Success criteria validation

### 🗑️ Temporary Outputs

All other directories (with ADW IDs like `a1b2c3d4/`) are **temporary test outputs**.

They are:
- Generated during development/testing
- Not committed to git (see `.gitignore`)
- Safe to delete when no longer needed

## 🧹 Cleanup Policy

### Manual Cleanup

```bash
# Delete all temporary outputs (keeps _examples)
find agents/ -maxdepth 1 -type d ! -name agents ! -name _examples -exec rm -rf {} +
```

### Automatic Cleanup (Recommended)

Add to your workflow:
```bash
# Keep only outputs from last 7 days
find agents/ -maxdepth 1 -type d -mtime +7 ! -name _examples -exec rm -rf {} +
```

## 📊 Example Structure

Each example contains:

```
example_meta_constructor_5_phases/
├── meta_construction_summary.json       # Overall workflow summary
├── meta-planner-{id}/                   # Phase 1: Strategic Planning
│   ├── cc_raw_output.jsonl              # Raw Claude Code output stream
│   ├── cc_raw_output.json               # Parsed JSON array
│   ├── cc_final_object.json             # Final response object
│   └── custom_summary_output.json       # Phase summary with metadata
├── meta-builder-{id}/                   # Phase 2: Artifact Construction
│   └── [same structure]
├── meta-tester-{id}/                    # Phase 3: Testing & Validation
│   └── [same structure]
├── meta-reviewer-{id}/                  # Phase 4: Critical Review
│   └── [same structure]
└── meta-documenter-{id}/               # Phase 5: Documentation
    └── [same structure]
```

## 🔍 Understanding Outputs

### ADW ID Format

- **Format**: `[a-z0-9]{8}` (8 hex chars)
- **Example**: `dd2b5962`
- **Purpose**: Unique identifier for each workflow execution
- **Generation**: `generate_short_id()` in `agent.py`

### Output Files

| File | Purpose |
|------|---------|
| `cc_raw_output.jsonl` | Streaming output (JSONL format) |
| `cc_raw_output.json` | All messages as JSON array |
| `cc_final_object.json` | Last message (final result) |
| `custom_summary_output.json` | Metadata + execution summary |
| `meta_construction_summary.json` | Overall workflow metadata |

### Metadata Fields

```json
{
  "agent_name": "meta-planner-dd2b59",
  "adw_id": "dd2b5962",
  "model": "sonnet",
  "working_dir": "/path/to/workspace",
  "prompt_length": 1677,
  "context_files": [],
  "status": "completed",
  "timestamp": "2025-11-13T09:08:20.243758"
}
```

## 🚀 Using Examples

### View Example Output

```bash
# See workflow summary
cat agents/_examples/example_meta_constructor_5_phases/meta_construction_summary.json

# See specific phase output
cat agents/_examples/example_meta_constructor_5_phases/meta-planner-*/custom_summary_output.json
```

### Copy Example as Template

```bash
# Create new workflow based on example
cp -r agents/_examples/example_meta_constructor_5_phases agents/my_new_workflow
```

## 📝 Adding New Examples

When adding a new reference example:

1. Run the builder to generate output
2. Verify it's a complete, successful execution
3. Move to `_examples/` with descriptive name:
   ```bash
   mv agents/{adw_id} agents/_examples/example_{workflow_type}
   ```
4. Update this README with example description
5. Commit to git

### Example Naming Convention

```
example_{workflow_type}_{variant}
```

Examples:
- `example_meta_constructor_5_phases` - Full meta-constructor
- `example_prompt_generator_single` - Single prompt execution
- `example_consolidation_workflow` - Consolidation workflow

## 🔒 Git Policy

### Tracked (in git)

- `agents/README.md` (this file)
- `agents/.gitignore`
- `agents/_examples/*` (reference examples)

### Ignored (not in git)

- `agents/{adw_id}/` (temporary test outputs)
- `agents/*.json` (loose files)
- `agents/*.jsonl` (loose files)

See `.gitignore` for full rules.

## 🆘 Troubleshooting

### "Too many files in agents/"

**Solution**: Clean up temporary outputs
```bash
# Safe: keeps _examples
rm -rf agents/[a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9]
```

### "Example output corrupted"

**Solution**: Regenerate from builders
```bash
# Re-run meta-constructor
python builders/02_agent_meta_constructor.py "Create a simple test agent" --model sonnet
```

### "Can't find example output"

**Solution**: Check `_examples/` folder
```bash
ls -la agents/_examples/
```

---

**Version**: 1.0.0
**Last Updated**: 2025-11-13
**Maintained by**: CODEXA System
