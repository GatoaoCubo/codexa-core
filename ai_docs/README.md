# 🤖 AI Documentation Hub

## PURPOSE
This directory contains technical documentation for AI components, prompts, and implementation details of the ECOMLM.CODEXA system.

## STRUCTURE

### Core Documentation
- **HOP_FRAMEWORK.md** - Higher-Order Prompt framework documentation
- **AGENT_SPECIFICATIONS.md** - Detailed specifications for each agent
- **PROMPT_ENGINEERING_GUIDE.md** - Best practices for prompt development
- **API_REFERENCE.md** - Complete API endpoint documentation
- **ML_PIPELINE.md** - Machine learning pipeline documentation

### Agent-Specific Documentation
- **agents/** - Individual agent technical documentation
  - pesquisa/ - Market research agent docs
  - anuncio/ - Ad generation agent docs
  - marca/ - Brand strategy agent docs
  - conhecimento/ - Knowledge extraction agent docs
  - mentor/ - Strategic planning agent docs
  - scout/ - Repository intelligence agent docs

### Integration Guides
- **integrations/** - External service integration
  - anthropic.md - Claude API integration
  - openai.md - GPT API integration
  - marketplace_apis.md - Marketplace integration

### Development Resources
- **development/** - Development-specific documentation
  - testing_guide.md - Testing strategies
  - debugging_guide.md - Debugging techniques
  - performance_optimization.md - Performance tips

## QUICK LINKS

| Document | Description |
|----------|-------------|
| [HOP Framework](HOP_FRAMEWORK.md) | Understanding the Higher-Order Prompt system |
| [Agent Specs](AGENT_SPECIFICATIONS.md) | Detailed agent capabilities and interfaces |
| [Prompt Guide](PROMPT_ENGINEERING_GUIDE.md) | Writing effective prompts |
| [API Reference](API_REFERENCE.md) | Complete API documentation |
| [ML Pipeline](ML_PIPELINE.md) | Machine learning workflows |

## NAVIGATION

### For Developers
Start with:
1. [AGENT_SPECIFICATIONS.md](AGENT_SPECIFICATIONS.md) - Understand agent architecture
2. [HOP_FRAMEWORK.md](HOP_FRAMEWORK.md) - Learn the prompt framework
3. [API_REFERENCE.md](API_REFERENCE.md) - API integration details

### For Prompt Engineers
Focus on:
1. [PROMPT_ENGINEERING_GUIDE.md](PROMPT_ENGINEERING_GUIDE.md) - Prompt best practices
2. Agent-specific prompt documentation in `agents/*/prompts.md`
3. [HOP_FRAMEWORK.md](HOP_FRAMEWORK.md) - Advanced prompt composition

### For ML Engineers
Review:
1. [ML_PIPELINE.md](ML_PIPELINE.md) - ML workflow documentation
2. [Knowledge extraction docs](agents/conhecimento/) - Data preparation
3. Training data generation guides

## DOCUMENT STATUS

| Document | Version | Status | Last Updated |
|----------|---------|--------|--------------|
| HOP_FRAMEWORK | 1.0 | ✅ Complete | 2024-11-12 |
| AGENT_SPECIFICATIONS | 1.0 | ✅ Complete | 2024-11-12 |
| PROMPT_ENGINEERING_GUIDE | 1.0 | ✅ Complete | 2024-11-12 |
| API_REFERENCE | 1.0 | ✅ Complete | 2024-11-12 |
| ML_PIPELINE | 1.0 | 🔄 In Progress | 2024-11-12 |

## CONTRIBUTING

To add or update documentation:
1. Follow the documentation template in `templates/`
2. Update this README with new documents
3. Ensure cross-references are valid
4. Submit PR with `docs:` prefix

## DOCUMENTATION STANDARDS

All documents should include:
- **PURPOSE** section explaining the document's goal
- **AUDIENCE** section identifying target readers
- **PREREQUISITES** listing required knowledge
- **VERSION** information and changelog
- **EXAMPLES** demonstrating concepts
- **REFERENCES** to related documents

---

> **Note**: This documentation is continuously updated as the system evolves. Always refer to the latest version for current information.