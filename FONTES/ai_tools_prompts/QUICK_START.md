# AI Tools Prompts - Quick Start Guide

## What Is This?

A curated knowledge base of system prompts and operational patterns from 30+ popular AI coding tools. Use this to:

1. **Learn** how commercial AI tools are designed
2. **Build** platform-specific agents for CODEXA
3. **Orchestrate** multi-platform workflows
4. **Improve** CODEXA's own prompts and patterns

---

## Quick Usage

### 1. Query a Platform

```bash
/codexa-query_platform cursor
```

**Result**: Complete overview of Cursor's architecture, tools, and unique patterns

### 2. Compare Platforms

```bash
/codexa-query_platform cursor,devin,v0
```

**Result**: Side-by-side comparison of approaches and capabilities

### 3. Get Integration Ideas

```bash
/codexa-query_platform cursor --integration
```

**Result**: Specific suggestions for integrating Cursor patterns into CODEXA

---

## What's Included

### Platforms Currently Documented

**Code Assistants**:
- ✅ **Cursor** - Autonomous code editor assistant (COMPLETE)
- 🔄 Claude Code - CLI assistant (metadata only)
- 📁 Windsurf - Flow-state focused assistant (structure only)
- 📁 Replit - Integrated environment assistant (structure only)

**AI Builders**:
- 🔄 v0 - UI component generator (tools only)
- 📁 Lovable - Full app builder (structure only)

**Autonomous Agents**:
- 🔄 Devin - Autonomous software engineer (partial)

**Research**:
- 📁 Perplexity - Research agent (structure only)

**Orchestration**:
- 📁 Cursor Composer - Multi-step orchestrator (structure only)

Legend:
- ✅ Complete (prompt + tools + metadata + notes)
- 🔄 Partial (some files available)
- 📁 Structure only (ready for content)

---

## File Structure Per Platform

```
[platform]/
├── system_prompt.txt    # Main behavioral prompt
├── tools.json           # Tool definitions and usage
├── metadata.json        # Version, capabilities, dates
└── NOTES.md             # Unique patterns and insights
```

---

## Use Cases

### 1. Learning AI Architecture
**Goal**: Understand how commercial tools structure their prompts

**Steps**:
1. `/codexa-query_platform cursor --patterns`
2. Read cursor/NOTES.md for deep analysis
3. Compare with CODEXA's approach

**Outcome**: Insights for improving CODEXA architecture

### 2. Building Platform-Specific Agents
**Goal**: Create agent that generates Cursor-optimized code

**Steps**:
1. `/codexa-query_platform cursor`
2. `/codexa-build_agent --target cursor --spec [...]`
3. Agent uses Cursor patterns from knowledge base

**Outcome**: Agent that understands Cursor's expectations

### 3. Cross-Platform Orchestration
**Goal**: Workflow that uses multiple AI tools

**Steps**:
1. `/codexa-query_platform cursor,v0,devin`
2. `/codexa-orchestrate --platforms cursor,v0`
3. Generate workflows optimized for each platform

**Outcome**: Multi-platform automation

### 4. Prompt Engineering Reference
**Goal**: Improve CODEXA HOP quality

**Steps**:
1. Read cursor/NOTES.md patterns
2. Apply patterns to CODEXA HOPs
3. Test improvements

**Outcome**: More effective CODEXA prompts

---

## Key Insights from Cursor (Example)

### Autonomous Operation Pattern
**What**: Agent works until task complete, minimal user interruption
**Application**: Add to CODEXA orchestration workflows

### Semantic Search First
**What**: Natural language search before exact text matching
**Application**: Implement in CODEXA codebase exploration

### Memory Management
**What**: Persistent, cited, updateable agent memories
**Application**: Add memory layer to CODEXA agents

### Tool Orchestration
**What**: Combine tools strategically (semantic → grep → edit)
**Application**: Document tool combination patterns for CODEXA

### Explanation-Driven
**What**: Every tool call requires explanation field
**Application**: Add to CODEXA tool calling protocol

---

## Adding New Platforms

### Manual Addition

1. **Create Directory**:
   ```bash
   mkdir FONTES/ai_tools_prompts/[platform_name]
   ```

2. **Create Files**:
   - `system_prompt.txt` - Copy or summarize system prompt
   - `tools.json` - Document available tools
   - `metadata.json` - Platform metadata
   - `NOTES.md` - Analyze unique patterns

3. **Update Registry**:
   Edit `PLATFORM_REGISTRY.json`:
   ```json
   {
     "platforms": {
       "new_platform": {
         "name": "New Platform",
         "category": "code_assistant",
         "description": "...",
         "capabilities": [...],
         "unique_patterns": [...]
       }
     }
   }
   ```

4. **Test**:
   ```bash
   /codexa-query_platform new_platform
   ```

### Automated Addition (Future)

```bash
/codexa-import_platform --url [github_url] --platform [name]
```

Auto-fetches, parses, and adds platform to knowledge base.

---

## Integration with CODEXA

### Current Integration Points

1. **`/codexa-query_platform`** - Query knowledge base
2. **`/codexa-build_agent`** - Use patterns in agent creation (future)
3. **`/codexa-orchestrate`** - Multi-platform workflows (future)
4. **HOPs** - Pattern reference for prompt engineering

### Future Integration

- **`/codexa-analyze_patterns`** - Extract patterns from new platforms
- **`/codexa-build_for_[platform]`** - Platform-specific code generation
- **`/codexa-compare_approaches`** - Architectural comparison
- **Agent Memory System** - Inspired by Cursor's memory management

---

## Best Practices

### When Querying

1. **Start Broad**: `/codexa-query_platform cursor`
2. **Then Focus**: `/codexa-query_platform cursor --patterns`
3. **Compare**: `/codexa-query_platform cursor,devin`
4. **Apply**: Use insights in your work

### When Adding Platforms

1. **Be Selective**: Focus on unique, valuable patterns
2. **Analyze Don't Copy**: Extract insights, don't duplicate
3. **Document Insights**: NOTES.md is most important file
4. **Update Registry**: Keep PLATFORM_REGISTRY.json current

### When Using Patterns

1. **Understand Context**: Why does the pattern exist?
2. **Adapt Don't Copy**: Fit CODEXA's architecture
3. **Test**: Validate pattern effectiveness
4. **Document**: Note what worked/didn't work

---

## Troubleshooting

### Command Not Found
**Issue**: `/codexa-query_platform` not recognized
**Fix**: Ensure `.claude/commands/codexa-query_platform.md` exists

### Platform Not Found
**Issue**: Platform requested doesn't exist
**Fix**: Run `/codexa-query_platform` (no args) to see available platforms

### Incomplete Data
**Issue**: Platform has empty or missing files
**Fix**: This is normal for new additions. Add data manually or via repo source.

---

## Resources

**Source Repository**: https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools
**License**: GPL-3.0 (reference only, not direct copy)
**CODEXA Docs**: `codexa.app/README.md`
**Registry**: `FONTES/ai_tools_prompts/PLATFORM_REGISTRY.json`

---

## Contributing

To expand this knowledge base:

1. **Find New Platforms**: Monitor source repo for updates
2. **Extract Patterns**: Focus on unique, reusable patterns
3. **Document Insights**: Write comprehensive NOTES.md
4. **Share**: Update PLATFORM_REGISTRY.json
5. **Test**: Verify with `/codexa-query_platform`

---

**Next Steps**:
1. Run: `/codexa-query_platform cursor` to see example
2. Read: `cursor/NOTES.md` for detailed pattern analysis
3. Apply: Use insights in your CODEXA work
4. Expand: Add more platforms as needed

---

**Last Updated**: 2025-11-24
**Status**: Active - Cursor fully documented, others partial
**Maintainer**: CODEXA System
