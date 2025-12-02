# CODEXA - HOP Meta-Agent Command

Initialize and execute the CODEXA (Create Organize Read Update Delete E-com X-Agent) HOP Meta-Agent.

## Usage

```bash
/codexa
```

## Description

CODEXA is a comprehensive HOP (Hierarchical Orchestration Pattern) meta-agent that consolidates:
- **CRUD operations** for documentation and e-commerce data
- **Scout capabilities** for intelligent repository navigation
- **Strategic planning** (mentor pattern) for business KPIs
- **Self-documentation** through introspection and auto-update
- **E-commerce management** including products, competitors, and knowledge base
- **Repository analysis** with caching and pattern matching

## Core Capabilities

### 1. CRUD Operations
```bash
python codexa/cli.py crud create <path> --content "..."
python codexa/cli.py crud read <path>
python codexa/cli.py crud list --type document
python codexa/cli.py crud search --keyword "..."
```

### 2. Scout Navigation
```bash
python codexa/cli.py scout scan --cache
python codexa/cli.py scout find --pattern "*.py"
python codexa/cli.py scout stats
```

### 3. E-commerce Management
```bash
python codexa/cli.py ecom products create --name "..." --price 99
python codexa/cli.py ecom strategy create-plan --title "..."
python codexa/cli.py ecom competitor add --name "..." --price 99
python codexa/cli.py ecom knowledge search --keyword "..."
```

### 4. System Operations
```bash
python codexa/cli.py status
python codexa/cli.py readme update
```

## Resources

- **Main Directory**: `/codexa/`
- **CLI Entry Point**: `/codexa/cli.py`
- **HOP Orchestrator**: `/codexa/hop_orchestrator.py`
- **Modules**: `/codexa/modules/` (crud, scout, ecommerce, etc.)
- **Documentation**: `/codexa/README.md`, `/codexa/EXAMPLES.md`

## Implementation Note

This is the CODEXA Meta-Agent located at the repository root (`/codexa/`).
For the anuncio-agent's ad generation command, use `/codex_anuncio` instead.