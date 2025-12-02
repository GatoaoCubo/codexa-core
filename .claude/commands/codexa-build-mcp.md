# /codexa-build-mcp | Create MCP Server

**Purpose**: Build Model Context Protocol (MCP) server for external API integration
**Time**: 30-60 minutes | **Output**: Functional MCP server with tools

---

## QUICK START

```bash
# Interactive mode
/codexa-build-mcp

# Specify API
/codexa-build-mcp --api="GitHub API"
```

---

## INPUT

**Required**:
- API name/description
- Authentication method
- Tools to expose (functions)
- Base URL (if applicable)

**Optional**:
- Rate limiting config
- Error handling strategy
- Caching requirements

---

## MCP SERVER COMPONENTS

1. **Server Config**: Name, version, authentication
2. **Tools Definition**: Functions exposed to Claude
3. **API Client**: Request handling + auth
4. **Error Handling**: Retries, fallbacks, logging
5. **Documentation**: Setup guide + examples

---

## STEPS

1. **Define API Integration**: Endpoints + auth + rate limits
2. **Create Tools**: Function definitions with input/output schemas
3. **Implement Handlers**: Request/response logic + error handling
4. **Add Authentication**: API keys, OAuth, tokens
5. **Test Integration**: Verify all tools functional
6. **Document Setup**: Installation + configuration guide

---

## VALIDATION

- Server config complete
- All tools defined with schemas
- Authentication working
- Error handling implemented
- Rate limiting configured
- Documentation complete
- Integration tests pass

---

## TROUBLESHOOTING

**Auth fails**: Verify API credentials | Check token format
**Rate limited**: Implement backoff | Add caching
**Tool not found**: Check function names | Verify registration
**Connection errors**: Check base URL | Verify network access

---

**Related**: MCP protocol docs | API documentation | Example MCP servers
