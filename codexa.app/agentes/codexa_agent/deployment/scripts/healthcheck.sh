#!/bin/bash
# CODEXA Agent - Health Check Script
# Version: 3.1.0

set -e

# Configuration
TIMEOUT=${HEALTHCHECK_TIMEOUT:-10}
RETRY_COUNT=${HEALTHCHECK_RETRIES:-3}
RETRY_DELAY=${HEALTHCHECK_RETRY_DELAY:-2}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check Python environment
check_python() {
    log_info "Checking Python environment..."
    if python --version > /dev/null 2>&1; then
        PYTHON_VERSION=$(python --version 2>&1)
        log_info "Python: $PYTHON_VERSION"
        return 0
    else
        log_error "Python not found"
        return 1
    fi
}

# Check required packages
check_packages() {
    log_info "Checking required packages..."

    PACKAGES=("anthropic" "openai" "python-dotenv" "pyyaml")
    MISSING=()

    for pkg in "${PACKAGES[@]}"; do
        if ! python -c "import $pkg" 2>/dev/null; then
            MISSING+=("$pkg")
        fi
    done

    if [ ${#MISSING[@]} -gt 0 ]; then
        log_warn "Missing packages: ${MISSING[*]}"
        return 1
    fi

    log_info "All required packages installed"
    return 0
}

# Check API keys
check_api_keys() {
    log_info "Checking API keys..."

    if [ -z "$ANTHROPIC_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
        log_error "No API keys configured (ANTHROPIC_API_KEY or OPENAI_API_KEY required)"
        return 1
    fi

    if [ -n "$ANTHROPIC_API_KEY" ]; then
        log_info "Anthropic API key: configured"
    fi

    if [ -n "$OPENAI_API_KEY" ]; then
        log_info "OpenAI API key: configured"
    fi

    return 0
}

# Check file permissions
check_permissions() {
    log_info "Checking file permissions..."

    DIRS=("/app/logs" "/app/outputs" "/app/artifacts")

    for dir in "${DIRS[@]}"; do
        if [ -d "$dir" ]; then
            if [ -w "$dir" ]; then
                log_info "Directory writable: $dir"
            else
                log_error "Directory not writable: $dir"
                return 1
            fi
        else
            log_warn "Directory does not exist: $dir"
        fi
    done

    return 0
}

# Check module imports
check_modules() {
    log_info "Checking CODEXA modules..."

    python -c "
from src.llm import get_llm_provider
from src.tools import ToolExecutor
from src.runtime import AgentRuntime
from src.auth import get_rate_limiter, get_audit_logger
print('All modules imported successfully')
" 2>/dev/null

    if [ $? -eq 0 ]; then
        log_info "All CODEXA modules loadable"
        return 0
    else
        log_error "Failed to import CODEXA modules"
        return 1
    fi
}

# Check disk space
check_disk_space() {
    log_info "Checking disk space..."

    AVAILABLE=$(df -BM /app 2>/dev/null | tail -1 | awk '{print $4}' | sed 's/M//')

    if [ -n "$AVAILABLE" ] && [ "$AVAILABLE" -lt 100 ]; then
        log_warn "Low disk space: ${AVAILABLE}MB available"
        return 1
    fi

    log_info "Disk space: ${AVAILABLE}MB available"
    return 0
}

# Run all health checks
run_health_checks() {
    log_info "Starting CODEXA health checks..."
    echo "=================================="

    CHECKS=(
        "check_python"
        "check_packages"
        "check_api_keys"
        "check_permissions"
        "check_modules"
        "check_disk_space"
    )

    FAILED=0
    PASSED=0

    for check in "${CHECKS[@]}"; do
        if $check; then
            ((PASSED++))
        else
            ((FAILED++))
        fi
        echo ""
    done

    echo "=================================="
    echo -e "Health Check Results: ${GREEN}$PASSED passed${NC}, ${RED}$FAILED failed${NC}"

    if [ $FAILED -gt 0 ]; then
        log_error "Health check failed"
        exit 1
    fi

    log_info "Health check passed"
    exit 0
}

# Main execution
case "${1:-}" in
    --python)
        check_python
        ;;
    --packages)
        check_packages
        ;;
    --api-keys)
        check_api_keys
        ;;
    --permissions)
        check_permissions
        ;;
    --modules)
        check_modules
        ;;
    --disk)
        check_disk_space
        ;;
    *)
        run_health_checks
        ;;
esac
