# Anthropic Claude API Reference

> **Note**: This is an initial placeholder. Run `python scripts/fontes/refresh_fonte.py --fonte anthropic_docs` to fetch the latest documentation.

---

## 🔗 Official Documentation
- **Main URL**: https://docs.anthropic.com
- **API Reference**: https://docs.anthropic.com/en/api/getting-started
- **Status**: Pending initial fetch

---

## 📚 Quick Links

### Getting Started
- [API Getting Started](https://docs.anthropic.com/en/api/getting-started)
- [Authentication](https://docs.anthropic.com/en/api/getting-started#authentication)
- [Making Requests](https://docs.anthropic.com/en/api/messages)

### Core Concepts
- [Messages API](https://docs.anthropic.com/en/api/messages)
- [Streaming](https://docs.anthropic.com/en/api/streaming)
- [Vision](https://docs.anthropic.com/en/docs/build-with-claude/vision)
- [Tool Use (Function Calling)](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)

### Models
- **Claude 3.5 Sonnet** - Most intelligent model
- **Claude 3 Opus** - Powerful for complex tasks
- **Claude 3 Haiku** - Fast and cost-effective
- **Claude 3.7 Sonnet** - Latest (if available)

### Rate Limits
- Varies by tier and model
- Check official docs for current limits

---

## 🚀 Basic Usage Example

```python
import anthropic

client = anthropic.Anthropic(
    api_key="your-api-key"
)

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(message.content)
```

---

## 📖 Next Steps

1. **Fetch Latest Docs**: Run refresh script to get current documentation
2. **Explore Topics**: Prompt engineering, vision, tool use
3. **Check Updates**: Documentation is refreshed weekly (critical priority)

---

**Created**: 2025-11-24
**Last Refresh**: Never
**Priority**: Critical
**Refresh Frequency**: Weekly
