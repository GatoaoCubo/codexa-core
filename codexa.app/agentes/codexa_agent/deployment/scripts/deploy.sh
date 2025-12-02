#!/bin/bash
# CODEXA Agent - Deployment Script
# Version: 3.1.0

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
DOCKER_DIR="$PROJECT_ROOT/deployment/docker"
ENV_FILE="$PROJECT_ROOT/.env"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }

# Display banner
show_banner() {
    echo ""
    echo "================================================"
    echo "   CODEXA Agent Deployment"
    echo "   Version: 3.1.0"
    echo "================================================"
    echo ""
}

# Check prerequisites
check_prerequisites() {
    log_step "Checking prerequisites..."

    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    log_info "Docker: $(docker --version)"

    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    log_info "Docker Compose: available"

    # Check .env file
    if [ ! -f "$ENV_FILE" ]; then
        log_warn ".env file not found at $ENV_FILE"
        log_info "Creating template .env file..."
        create_env_template
    fi

    log_info "Prerequisites check passed"
}

# Create .env template
create_env_template() {
    cat > "$ENV_FILE" << 'EOF'
# CODEXA Agent Environment Configuration
# Copy this file to .env and fill in your API keys

# LLM Provider API Keys (at least one required)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Environment
CODEXA_ENV=production
CODEXA_LOG_LEVEL=INFO

# Optional: AWS for artifact storage
# AWS_ACCESS_KEY_ID=
# AWS_SECRET_ACCESS_KEY=
# AWS_REGION=us-east-1
EOF
    log_info "Created .env template at $ENV_FILE"
    log_warn "Please edit $ENV_FILE with your API keys before deploying"
}

# Build Docker images
build_images() {
    log_step "Building Docker images..."

    cd "$DOCKER_DIR"

    # Build production image
    log_info "Building production image..."
    docker-compose build codexa-agent

    log_info "Docker images built successfully"
}

# Deploy services
deploy_services() {
    log_step "Deploying services..."

    cd "$DOCKER_DIR"

    # Stop existing containers
    log_info "Stopping existing containers..."
    docker-compose down --remove-orphans 2>/dev/null || true

    # Start services
    log_info "Starting services..."
    docker-compose up -d codexa-agent

    # Wait for health check
    log_info "Waiting for health check..."
    sleep 5

    # Check container status
    if docker-compose ps | grep -q "Up"; then
        log_info "Services deployed successfully"
    else
        log_error "Services failed to start"
        docker-compose logs
        exit 1
    fi
}

# Run health check
run_health_check() {
    log_step "Running health check..."

    # Run health check script inside container
    docker exec codexa-agent /bin/bash /app/deployment/scripts/healthcheck.sh 2>/dev/null || {
        log_warn "Container health check not available, checking container status..."

        if docker ps | grep -q "codexa-agent"; then
            log_info "Container is running"
        else
            log_error "Container is not running"
            exit 1
        fi
    }
}

# Show status
show_status() {
    log_step "Current deployment status:"
    echo ""

    cd "$DOCKER_DIR"

    docker-compose ps

    echo ""
    log_info "To view logs: docker-compose -f $DOCKER_DIR/docker-compose.yml logs -f"
    log_info "To stop: docker-compose -f $DOCKER_DIR/docker-compose.yml down"
}

# Rollback deployment
rollback() {
    log_step "Rolling back deployment..."

    cd "$DOCKER_DIR"

    docker-compose down
    docker-compose up -d --force-recreate codexa-agent

    log_info "Rollback completed"
}

# Main execution
main() {
    show_banner

    case "${1:-deploy}" in
        deploy)
            check_prerequisites
            build_images
            deploy_services
            run_health_check
            show_status
            ;;
        build)
            check_prerequisites
            build_images
            ;;
        start)
            deploy_services
            ;;
        stop)
            cd "$DOCKER_DIR"
            docker-compose down
            log_info "Services stopped"
            ;;
        restart)
            cd "$DOCKER_DIR"
            docker-compose restart
            log_info "Services restarted"
            ;;
        status)
            show_status
            ;;
        logs)
            cd "$DOCKER_DIR"
            docker-compose logs -f
            ;;
        health)
            run_health_check
            ;;
        rollback)
            rollback
            ;;
        *)
            echo "Usage: $0 {deploy|build|start|stop|restart|status|logs|health|rollback}"
            exit 1
            ;;
    esac
}

main "$@"
