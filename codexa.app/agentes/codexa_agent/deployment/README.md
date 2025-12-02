# CODEXA Deployment

Production deployment configuration for CODEXA agents.

---

## Quick Start

```bash
# Deploy
./scripts/deploy.sh deploy

# Check status
./scripts/deploy.sh status

# View logs
./scripts/deploy.sh logs
```

---

## Structure

```
deployment/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── config/
│   └── production.yml
└── scripts/
    ├── deploy.sh
    └── healthcheck.sh
```

---

## Commands

| Command | Action |
|---------|--------|
| `deploy.sh deploy` | Full deployment |
| `deploy.sh build` | Build images |
| `deploy.sh start` | Start services |
| `deploy.sh stop` | Stop services |
| `deploy.sh status` | Check status |
| `deploy.sh logs` | View logs |
| `deploy.sh health` | Health check |

---

**Full Guide**: [docs/DEPLOYMENT.md](../docs/DEPLOYMENT.md)
