# AI Tools System Prompts - Knowledge Base

## Purpose

This directory contains system prompts, tool definitions, and behavioral patterns from popular AI coding assistants and platforms. This knowledge base enables:

1. **Cross-Platform Understanding**: How different AI tools structure their prompts
2. **Platform-Specific Agent Creation**: Build agents that generate code/prompts for specific platforms
3. **Orchestration**: Create workflows that leverage multiple AI tools
4. **Pattern Learning**: Study proven patterns from commercial AI products

## Source

Curated from: https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools
- **License**: GPL-3.0 (reference only, not direct copy)
- **Content**: 30,000+ lines documenting 30+ AI tools
- **Updates**: Repository updates via Discord community

## Structure

```
ai_tools_prompts/
├── README.md                    # This file
├── PLATFORM_REGISTRY.json       # Index of all platforms
└── [platform_name]/
    ├── system_prompt.txt        # Main behavioral prompt
    ├── tools.json               # Tool/function definitions
    ├── metadata.json            # Version, date, capabilities
    └── NOTES.md                 # Unique patterns and insights
```

## Platforms Included

### Code Assistants
- **cursor/**: Cursor Editor AI assistant
- **claude_code/**: Anthropic's Claude Code CLI
- **windsurf/**: Windsurf AI coding tool
- **replit/**: Replit AI agent

### AI Builders
- **v0/**: Vercel's v0 UI builder
- **lovable/**: Lovable app builder
- **cursor_composer/**: Cursor's composer mode

### Advanced Agents
- **devin/**: Devin AI software engineer
- **perplexity/**: Perplexity research agent

## Usage in CODEXA

### 1. Query Platform Details
```bash
/codexa-query_platform cursor
```
Returns system prompt structure, capabilities, and unique patterns.

### 2. Build Platform-Specific Agents
```bash
/codexa-build_for_cursor [project_spec]
```
Generates prompts/code optimized for Cursor's architecture.

### 3. Cross-Platform Orchestration
```bash
/codexa-orchestrate --platforms cursor,v0,claude_code
```
Creates workflows leveraging multiple platforms.

### 4. Pattern Analysis
Study how commercial tools handle:
- Multi-agent orchestration
- Context management
- Tool calling patterns
- Safety constraints
- Response formatting

## Integration with CODEXA

This knowledge base integrates with:
- `/prime-codexa`: Meta-construction system
- `/codexa-build_agent`: Agent creation (can target specific platforms)
- `/codexa-orchestrate`: Multi-platform workflows
- HOPs (High Order Prompts): Pattern inspiration for new HOPs

## Maintenance

- **Update Frequency**: Weekly check of source repository
- **Curation**: Focus on actionable patterns, not raw dumps
- **Documentation**: Each platform has NOTES.md with key insights
- **Version Tracking**: metadata.json tracks prompt versions

## Security Note

Per source repository warning: System prompts can be security vulnerabilities if exposed. Use this for:
- ✅ Learning and reference
- ✅ Defensive security analysis
- ✅ Pattern inspiration
- ❌ Direct copying (GPL-3.0 license)
- ❌ Exposing CODEXA's internal prompts

## Contributing

To add a new platform:
1. Create directory: `mkdir platform_name/`
2. Add files: `system_prompt.txt`, `tools.json`, `metadata.json`, `NOTES.md`
3. Update `PLATFORM_REGISTRY.json`
4. Document unique patterns in NOTES.md

---

**Last Updated**: 2025-11-24
**Maintained By**: CODEXA System
**Source Repository**: x1xhlol/system-prompts-and-models-of-ai-tools
