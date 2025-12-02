# CODEXA Agent - Production Dockerfile
# Multi-stage build for minimal image size

# Stage 1: Builder
FROM python:3.12-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster package installation
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Copy requirements
COPY requirements.txt .
COPY requirements-dev.txt .

# Create virtual environment and install dependencies
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN uv pip install --no-cache-dir -r requirements.txt


# Stage 2: Production
FROM python:3.12-slim as production

WORKDIR /app

# Create non-root user for security
RUN groupadd -r codexa && useradd -r -g codexa codexa

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY src/ ./src/
COPY agents/ ./agents/
COPY config/ ./config/
COPY prompts/ ./prompts/
COPY builders/ ./builders/
COPY validators/ ./validators/

# Copy configuration files
COPY PRIME.md ./
COPY README.md ./
COPY pytest.ini ./

# Create necessary directories
RUN mkdir -p /app/logs /app/outputs /app/artifacts \
    && chown -R codexa:codexa /app

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV CODEXA_ENV=production
ENV CODEXA_LOG_LEVEL=INFO

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from src.runtime import agent_runtime; print('OK')" || exit 1

# Switch to non-root user
USER codexa

# Default command
CMD ["python", "-m", "src.runtime.agent_runtime"]


# Stage 3: Development
FROM production as development

USER root

# Install development dependencies
COPY --from=builder /opt/venv /opt/venv
RUN /opt/venv/bin/pip install -r requirements-dev.txt

# Development environment variables
ENV CODEXA_ENV=development
ENV CODEXA_LOG_LEVEL=DEBUG

USER codexa

CMD ["python", "-m", "pytest", "tests/", "-v"]
