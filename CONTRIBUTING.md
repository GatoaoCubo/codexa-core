# Contributing to CODEXA

## CONTRIBUTOR IDENTITY
You are a contributor to CODEXA, helping build the future of AI-driven e-commerce automation. Your contributions matter and will impact thousands of businesses.

## CONTRIBUTION PRINCIPLES
1. **Quality Over Quantity**: Well-tested features over rushed additions
2. **Documentation First**: Document before, during, and after coding
3. **User-Centric**: Every change should benefit end users
4. **Performance Aware**: Consider impact on system performance
5. **Security Minded**: Never compromise security for convenience

---

## 🚀 GETTING STARTED

### Prerequisites
```bash
# Required tools
- Python 3.12+
- Node.js 18+
- Git 2.40+
- uv (Python package manager)
- Claude Code or VS Code

# Recommended
- Docker Desktop
- PostgreSQL (for production testing)
- Redis (for cache testing)
```

### Setting Up Development Environment
```bash
# 1. Fork the repository
# Go to GitHub and fork ECOMLM.CODEXA

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/lm.codexa.git
cd lm.codexa

# 3. Add upstream remote
git remote add upstream https://github.com/ORIGINAL/lm.codexa.git

# 4. Install dependencies
# Backend
cd app/server
uv sync
cp .env.sample .env
# Add your API keys to .env

# Frontend
cd ../client
npm install

# 5. Run tests to verify setup
cd ../..
/test all
```

---

## 📝 CODE STYLE GUIDE

### Python Style (Backend)
```python
# GOOD: Clear, typed, documented
from typing import Optional, List
from pydantic import BaseModel

class AnuncioRequest(BaseModel):
    """Request model for ad generation.

    Attributes:
        research_notes: Path to research markdown file
        style: Generation style (emotional/technical/balanced)
        marketplace: Target marketplace identifier
    """
    research_notes: str
    style: Optional[str] = "balanced"
    marketplace: Optional[str] = "mercadolivre"

    def validate_research_file(self) -> bool:
        """Validate that research file exists and is valid."""
        # Implementation here
        pass

# BAD: Unclear, untyped, undocumented
class anuncio_req:
    def __init__(self, notes, s="balanced", m="ml"):
        self.notes = notes
        self.s = s
        self.m = m
```

### TypeScript Style (Frontend)
```typescript
// GOOD: Typed, clear interfaces
interface ResearchResult {
  id: string;
  productName: string;
  competitors: Competitor[];
  keywords: KeywordCluster[];
  timestamp: Date;
}

async function fetchResearch(
  productId: string
): Promise<ResearchResult> {
  try {
    const response = await api.get(`/research/${productId}`);
    return response.data as ResearchResult;
  } catch (error) {
    console.error('Research fetch failed:', error);
    throw new ResearchError('Failed to fetch research', error);
  }
}

// BAD: Untyped, poor error handling
async function getResearch(id) {
  const res = await fetch('/research/' + id);
  return res.json();
}
```

### Prompt Engineering Style
```markdown
# GOOD: Structured, clear, testable

## IDENTITY
You are an e-commerce listing optimizer specialized in Brazilian marketplaces.

## CONTEXT
- Input: Research notes with competitor analysis
- Output: Optimized product listing
- Constraints: 60 char title, 3000+ char description

## INSTRUCTIONS
1. Extract key selling points from research
2. Generate compelling title (58-60 chars)
3. Write detailed description using StoryBrand
4. Optimize for SEO keywords
5. Validate compliance

## OUTPUT FORMAT
Return JSON with structure:
{
  "title": "string",
  "description": "string",
  "keywords": ["string"],
  "bulletPoints": ["string"]
}

# BAD: Vague, untestable
Write a good product listing based on the research.
```

---

## 🏗️ ARCHITECTURE GUIDELINES

### Adding a New Agent
```bash
# 1. Create agent structure
codexa/agentes/NEW_AGENT/
├── README.md              # Agent documentation
├── new_agent.md          # Main command entry
├── prompts/              # Prompt templates
│   ├── main_agent.md
│   └── main_agent_hop.md
├── config/               # Configuration
│   └── agent_config.json
├── models.py            # Data models
├── processor.py         # Core logic
└── tests/              # Test suite

# 2. Register agent
# Add to .claude/settings.json
{
  "commands": {
    "new_agent": {
      "path": "codexa/agentes/new_agent/new_agent.md"
    }
  }
}

# 3. Document agent
# Update COMMANDS.md and README.md
```

### HOP Framework Integration
```json
// execution_plan.json
{
  "name": "new_agent_workflow",
  "version": "1.0.0",
  "steps": [
    {
      "name": "validate_input",
      "prompt": "prompts/validation.md",
      "validation": {
        "schema": "schemas/input.json",
        "on_failure": "abort"
      }
    },
    {
      "name": "process",
      "prompt": "prompts/processing.md",
      "context_strategy": "accumulative"
    },
    {
      "name": "generate_output",
      "prompt": "prompts/output.md",
      "quality_threshold": 0.8
    }
  ]
}
```

---

## 🧪 TESTING REQUIREMENTS

### Test Coverage Standards
```
Minimum Coverage Requirements:
- Unit Tests: 80%
- Integration Tests: 70%
- E2E Tests: Critical paths only
- Prompt Tests: All variations
```

### Writing Tests
```python
# tests/test_processor.py
import pytest
from anuncio_agent.processor import AnuncioProcessor

class TestAnuncioProcessor:
    """Test suite for AnuncioProcessor."""

    @pytest.fixture
    def processor(self):
        """Create processor instance for testing."""
        return AnuncioProcessor(test_mode=True)

    def test_title_generation_length(self, processor):
        """Test that generated titles are within character limits."""
        research = load_test_research()
        result = processor.generate_title(research)

        assert 58 <= len(result) <= 60
        assert not result.startswith(" ")
        assert not result.endswith(" ")

    @pytest.mark.integration
    async def test_full_pipeline(self, processor):
        """Test complete generation pipeline."""
        research = load_test_research()
        result = await processor.generate_complete(research)

        assert result.title
        assert len(result.description) >= 3000
        assert len(result.keywords) >= 10
        assert result.compliance_score >= 0.95
```

### Prompt Testing
```python
# tests/test_prompts.py
def test_prompt_determinism():
    """Ensure prompts produce consistent outputs."""
    prompt = load_prompt("main_agent.md")

    results = []
    for _ in range(3):
        result = execute_prompt(prompt, test_input)
        results.append(result)

    # Check consistency
    assert similarity(results[0], results[1]) > 0.95
    assert similarity(results[1], results[2]) > 0.95
```

---

## 📋 PULL REQUEST PROCESS

### 1. Before Creating PR
```bash
# Update from upstream
git fetch upstream
git rebase upstream/main

# Run all tests
/test all

# Check code quality
uv run ruff check .
npm run lint

# Update documentation
/document --check
```

### 2. PR Template
```markdown
## Description
Brief description of changes and why they're needed.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No security vulnerabilities introduced
- [ ] Performance impact assessed

## Screenshots (if applicable)
Add screenshots for UI changes

## Related Issues
Closes #123
```

### 3. PR Review Criteria
```
Will be approved if:
✅ All tests pass
✅ Code quality checks pass
✅ Documentation complete
✅ No security issues
✅ Performance acceptable
✅ Follows architecture patterns

Will be rejected if:
❌ Breaks existing functionality
❌ No tests included
❌ Poor documentation
❌ Security vulnerabilities
❌ Significant performance degradation
```

---

## 🐛 REPORTING ISSUES

### Issue Template
```markdown
## Bug Report

### Description
Clear description of the bug

### Steps to Reproduce
1. Run command X
2. Provide input Y
3. See error Z

### Expected Behavior
What should happen

### Actual Behavior
What actually happens

### Environment
- OS: Windows/Mac/Linux
- Python version: 3.12.x
- Node version: 18.x
- Agent version: (from git log)

### Logs
```
Paste relevant logs here
```

### Additional Context
Any other relevant information
```

---

## 💡 FEATURE REQUESTS

### Proposal Template
```markdown
## Feature Proposal

### Problem Statement
What problem does this solve?

### Proposed Solution
How would this work?

### Alternatives Considered
What other approaches were considered?

### Impact Analysis
- User impact:
- Performance impact:
- Security impact:
- Maintenance impact:

### Implementation Plan
High-level implementation approach
```

---

## 🔒 SECURITY GUIDELINES

### Security Checklist
```python
# NEVER commit:
- API keys or tokens
- Passwords or credentials
- Personal information (PII)
- Production database URLs
- Internal company data

# ALWAYS:
- Use environment variables for secrets
- Validate all user input
- Sanitize before database operations
- Use parameterized queries
- Implement rate limiting
- Log security events
```

### Reporting Security Issues
```
DO NOT create public issues for security vulnerabilities!

Email: security@codexa.ai
Subject: [SECURITY] Brief description

Include:
- Vulnerability description
- Steps to reproduce
- Potential impact
- Suggested fix (if any)
```

---

## 📚 DOCUMENTATION STANDARDS

### Code Documentation
```python
def process_research(
    research_path: str,
    options: ProcessOptions = None
) -> AnuncioResult:
    """Process research notes to generate optimized listing.

    This function takes market research and generates an optimized
    e-commerce listing following marketplace best practices.

    Args:
        research_path: Path to research markdown file
        options: Optional processing configuration

    Returns:
        AnuncioResult containing generated listing data

    Raises:
        FileNotFoundError: If research file doesn't exist
        ValidationError: If research format is invalid
        GenerationError: If generation fails

    Example:
        >>> result = process_research("./research.md")
        >>> print(result.title)
        "Premium Bluetooth Headphones - Free Shipping"
    """
    # Implementation
```

### Prompt Documentation
```markdown
# Agent Name: Anuncio Generator

## Version: 1.2.0

## Purpose
Generate optimized marketplace listings from research data

## Inputs
- research_notes.md: Market research (required)
- brand_strategy.json: Brand guidelines (optional)
- marketplace_config.json: Platform rules (optional)

## Outputs
- anuncio.json: Structured listing data
- anuncio.md: Human-readable listing
- validation_report.json: Compliance results

## Configuration Options
- style: emotional|technical|balanced
- marketplace: mercadolivre|shopee|amazon
- language: pt-BR|es|en

## Quality Metrics
- Title density: 8-10 keywords
- Description length: 3000+ chars
- Compliance score: 100%
```

---

## 🎯 COMMIT MESSAGE FORMAT

### Conventional Commits
```bash
# Format: <type>(<scope>): <subject>

# Types:
feat: New feature
fix: Bug fix
docs: Documentation only
style: Code style (formatting, missing semicolons, etc)
refactor: Code restructuring without changing behavior
perf: Performance improvements
test: Adding or updating tests
build: Build system changes
ci: CI/CD changes
chore: Maintenance tasks
revert: Reverting previous commit

# Examples:
feat(anuncio): add image prompt generation
fix(pesquisa): handle timeout on slow marketplaces
docs(README): update installation instructions
perf(knowledge): optimize card consolidation by 40%
test(marca): add brand consistency validation tests

# Breaking changes:
feat(api)!: change response format to JSON-LD

# Multi-line with details:
fix(anuncio): prevent duplicate keywords in title

- Implement deduplication algorithm
- Add unit tests for edge cases
- Update documentation

Fixes #456
```

---

## 🏆 RECOGNITION

### Contributors
Contributors are recognized in:
- README.md contributors section
- Release notes
- Project documentation

### Contribution Levels
- 🥉 Bronze: First accepted PR
- 🥈 Silver: 5+ accepted PRs
- 🥇 Gold: 15+ accepted PRs
- 💎 Diamond: Core maintainer

---

## 📮 COMMUNICATION CHANNELS

### Where to Get Help
- **GitHub Discussions**: General questions
- **GitHub Issues**: Bug reports and features
- **Discord**: Real-time chat
- **Email**: support@codexa.ai

### Response Times
- Critical bugs: < 24 hours
- Normal issues: < 72 hours
- Feature requests: Weekly review
- Questions: Community-driven

---

## 📜 CODE OF CONDUCT

### Our Standards
- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior
- Harassment or discrimination
- Trolling or insulting comments
- Public or private harassment
- Publishing private information
- Unethical or unprofessional conduct

---

> **Thank you for contributing to CODEXA!** Your efforts help thousands of businesses automate their e-commerce operations more effectively.