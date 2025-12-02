# TAC-7 Backend Server

FastAPI backend server for the TAC-7 E-commerce Intelligence Platform.

## Overview

This backend provides:
- **Natural Language SQL Interface** - Query databases using Portuguese or English
- **Agent Integration** - API endpoints for all TAC-7 agents
- **File Processing** - CSV, JSON, JSONL data handling
- **Database Management** - SQLite with connection pooling and caching

## Quick Start

```bash
# Install dependencies
uv sync

# Run server
uv run python server.py

# Access API docs
# http://localhost:8000/docs
```

## Structure

```
app/server/
├── core/                    # Core modules (15 modules)
│   ├── llm_integration.py   # LLM APIs (Claude/OpenAI)
│   ├── sql_generator.py     # Natural language to SQL
│   ├── data_processor.py    # File processing
│   ├── cache_manager.py     # Caching layer
│   └── [other modules]
├── server.py                # Main FastAPI application
├── main.py                  # Application entry point
├── pyproject.toml           # Python dependencies
├── db/                      # SQLite database files
└── cache/                   # Cache storage
```

## Core Modules

Located in `core/` directory:
- **LLM Integration** - Anthropic Claude and OpenAI GPT-4 integration
- **SQL Generation** - Natural language query processing with security
- **File Processing** - CSV/JSON/JSONL import and export
- **Database Pooling** - Connection pool management
- **Caching** - Query result caching for performance
- **Export Utilities** - Data export in multiple formats

## Configuration

Environment variables (`.env`):
```bash
ANTHROPIC_API_KEY=your_key
OPENAI_API_KEY=your_key        # Optional
BACKEND_PORT=8000               # Default: 8000
DATABASE_PATH=db/data.db        # Default: db/data.db
LOG_LEVEL=INFO                  # Default: INFO
```

## API Endpoints

Main endpoints:
- `GET /` - Health check
- `GET /docs` - Interactive API documentation
- `POST /query` - Natural language SQL queries
- `POST /upload` - File upload (CSV/JSON)
- `GET /export` - Export data

## Testing

```bash
# Run unit tests
uv run pytest

# Run with coverage
uv run pytest --cov=core
```

## Dependencies

- **FastAPI** 0.115.13
- **Uvicorn** - ASGI server
- **SQLAlchemy** - ORM and database toolkit
- **Anthropic** - Claude API client
- **OpenAI** - GPT-4 API client
- **Pandas** - Data processing

## Related Documentation

- Main README: `/README.md`
- Frontend: `/app/client/README.md`
- API Documentation: http://localhost:8000/docs (when running)