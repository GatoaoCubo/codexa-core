# CODEXA Agent - Deployment Guide

**Version**: 3.1.0
**Last Updated**: 2025-11-24

---

## Quick Start

```bash
# 1. Clone repository
git clone <repository-url>
cd codexa_agent

# 2. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 3. Deploy
./deployment/scripts/deploy.sh deploy
```

---

## Prerequisites

| Requirement | Minimum Version | Check Command |
|-------------|-----------------|---------------|
| Docker | 20.10+ | `docker --version` |
| Docker Compose | 2.0+ | `docker compose version` |
| Python | 3.11+ | `python --version` |

### API Keys Required

At least one LLM provider API key is required:

| Provider | Environment Variable | Get Key |
|----------|---------------------|---------|
| Anthropic (Claude) | `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) |
| OpenAI | `OPENAI_API_KEY` | [platform.openai.com](https://platform.openai.com) |
| Google (Gemini) | `GOOGLE_API_KEY` | [makersuite.google.com](https://makersuite.google.com) |

---

## Configuration

### Environment Variables

Create `.env` file in project root:

```bash
# Required: At least one API key
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIza...

# Environment settings
CODEXA_ENV=production          # production, development, test
CODEXA_LOG_LEVEL=INFO          # DEBUG, INFO, WARNING, ERROR

# Optional: Rate limiting overrides
RATE_LIMIT_RPM=50              # Requests per minute
RATE_LIMIT_TPM=100000          # Tokens per minute

# Optional: Audit logging
AUDIT_LOG_DIR=/app/logs/audit
AUDIT_RETENTION_DAYS=90
```

### Production Configuration

Edit `deployment/config/production.yml`:

```yaml
# Key settings
llm:
  default_provider: claude
  providers:
    claude:
      model: claude-sonnet-4-20250514
      max_tokens: 8192

rate_limiting:
  enabled: true
  per_provider:
    claude:
      requests_per_minute: 50
      tokens_per_minute: 100000

security:
  allowed_origins:
    - "https://your-domain.com"
```

---

## Deployment Options

### Option 1: Docker (Recommended)

```bash
# Full deployment
./deployment/scripts/deploy.sh deploy

# Individual commands
./deployment/scripts/deploy.sh build    # Build images only
./deployment/scripts/deploy.sh start    # Start services
./deployment/scripts/deploy.sh stop     # Stop services
./deployment/scripts/deploy.sh status   # Check status
./deployment/scripts/deploy.sh logs     # View logs
./deployment/scripts/deploy.sh health   # Health check
```

### Option 2: Docker Compose Direct

```bash
cd deployment/docker

# Production
docker-compose up -d codexa-agent

# Development
docker-compose --profile dev up -d

# Testing
docker-compose --profile test run codexa-test
```

### Option 3: Local Development

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run directly
python -m src.runtime.agent_runtime

# Run tests
pytest tests/ -v
```

---

## Health Checks

### Manual Health Check

```bash
./deployment/scripts/healthcheck.sh

# Individual checks
./deployment/scripts/healthcheck.sh --python
./deployment/scripts/healthcheck.sh --packages
./deployment/scripts/healthcheck.sh --api-keys
./deployment/scripts/healthcheck.sh --modules
./deployment/scripts/healthcheck.sh --disk
```

### Docker Health Check

```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' codexa-agent

# View health check logs
docker inspect --format='{{json .State.Health}}' codexa-agent | jq
```

---

## Monitoring

### Logs

```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f codexa-agent

# Local logs
tail -f logs/codexa.log
```

### Metrics

The system exposes metrics at `/metrics` endpoint (if enabled):

| Metric | Description |
|--------|-------------|
| `codexa_requests_total` | Total API requests |
| `codexa_tokens_used_total` | Total tokens consumed |
| `codexa_response_time_seconds` | Response time histogram |
| `codexa_error_rate` | Error rate by type |
| `codexa_cost_usd` | Estimated API costs |

---

## Security

### Production Checklist

- [ ] API keys stored securely (not in code)
- [ ] `.env` file not committed to git
- [ ] Rate limiting enabled
- [ ] Audit logging enabled
- [ ] Sandbox mode for bash tools
- [ ] Allowed paths configured for file tools
- [ ] CORS properly configured
- [ ] Running as non-root user

### File Permission Security

```yaml
# In production.yml
tools:
  file:
    allowed_paths:
      - /app/outputs
      - /app/artifacts
    blocked_paths:
      - /etc
      - /var
      - /root
```

### Audit Trail

All operations are logged to audit log:
- API calls
- Tool executions
- Authentication events
- Security violations

```bash
# View audit logs
cat logs/audit/audit_$(date +%Y-%m-%d).jsonl | jq
```

---

## Troubleshooting

### Common Issues

**Container won't start**
```bash
# Check logs
docker-compose logs codexa-agent

# Verify .env file
cat .env | grep -v '^#' | grep -v '^$'

# Rebuild image
docker-compose build --no-cache codexa-agent
```

**API key errors**
```bash
# Verify keys are loaded
docker exec codexa-agent env | grep API_KEY

# Test API key directly
curl -H "x-api-key: $ANTHROPIC_API_KEY" https://api.anthropic.com/v1/messages
```

**Rate limit errors**
```bash
# Check current rate limit status
docker exec codexa-agent python -c "
from src.auth import get_rate_limiter
limiter = get_rate_limiter()
print(limiter.get_stats())
"
```

**Disk space issues**
```bash
# Check disk usage
docker system df

# Clean up
docker system prune -a
```

### Rollback

```bash
# Rollback to previous deployment
./deployment/scripts/deploy.sh rollback

# Or manually
docker-compose down
docker-compose up -d --force-recreate codexa-agent
```

---

## Scaling

### Horizontal Scaling

```yaml
# docker-compose.yml
services:
  codexa-agent:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

### Load Balancing

For production, use a reverse proxy (nginx, traefik):

```nginx
upstream codexa {
    server codexa-agent-1:8000;
    server codexa-agent-2:8000;
    server codexa-agent-3:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://codexa;
    }
}
```

---

## Cost Management

### Monitoring Costs

```python
from src.llm import get_cost_tracker

tracker = get_cost_tracker()
print(tracker.get_daily_cost())
print(tracker.get_cost_by_provider())
```

### Cost Optimization

1. Use appropriate models:
   - `claude-haiku` for simple tasks
   - `claude-sonnet` for complex reasoning
   - `claude-opus` only when needed

2. Enable caching for repeated queries

3. Set token limits per workflow

4. Monitor and alert on cost thresholds

---

## Backup & Recovery

### Backup Artifacts

```bash
# Backup outputs and artifacts
tar -czf backup_$(date +%Y%m%d).tar.gz outputs/ artifacts/ logs/

# Backup to S3 (if configured)
aws s3 sync outputs/ s3://your-bucket/backups/
```

### Recovery

```bash
# Restore from backup
tar -xzf backup_20251124.tar.gz

# Restart services
./deployment/scripts/deploy.sh restart
```

---

## Support

- Issues: [GitHub Issues](https://github.com/your-repo/issues)
- Documentation: See `docs/` directory
- Logs: Check `logs/` directory

---

**Version History**:
- 3.1.0 (2025-11-24): Initial production deployment guide
