#!/bin/bash
#
# CODEXA.app Startup Script
# Initializes all services: MCP servers, Voice daemon, Dashboard
#
# Usage:
#   ./start-codexa.sh          # Start all services
#   ./start-codexa.sh --voice  # Start with voice enabled
#   ./start-codexa.sh --stop   # Stop all services
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODEXA_ROOT="$SCRIPT_DIR"
VOICE_DIR="$CODEXA_ROOT/codexa.app/voice"
LAUNCHER_DIR="$CODEXA_ROOT/codexa.app/launcher"
PID_DIR="$CODEXA_ROOT/.claude/pids"
LOG_DIR="$CODEXA_ROOT/.claude/logs"

# Ports
DASHBOARD_PORT=3333
VOICE_PORT=5000

# Create directories
mkdir -p "$PID_DIR" "$LOG_DIR"

# Functions
log() {
    echo -e "${BLUE}[CODEXA]${NC} $1"
}

success() {
    echo -e "${GREEN}[CODEXA]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[CODEXA]${NC} $1"
}

error() {
    echo -e "${RED}[CODEXA]${NC} $1"
}

check_port() {
    lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1
}

kill_port() {
    local port=$1
    if check_port $port; then
        local pid=$(lsof -Pi :$port -sTCP:LISTEN -t)
        kill $pid 2>/dev/null || true
        sleep 1
    fi
}

wait_for_health() {
    local url=$1
    local max_attempts=${2:-30}
    local attempt=0

    while [ $attempt -lt $max_attempts ]; do
        if curl -s "$url" >/dev/null 2>&1; then
            return 0
        fi
        attempt=$((attempt + 1))
        sleep 1
    done
    return 1
}

start_dashboard() {
    log "Starting Dashboard on port $DASHBOARD_PORT..."

    if check_port $DASHBOARD_PORT; then
        warn "Dashboard already running on port $DASHBOARD_PORT"
        return 0
    fi

    cd "$LAUNCHER_DIR"

    # Install deps if needed
    if [ ! -d "node_modules" ]; then
        log "Installing dashboard dependencies..."
        npm install --silent
    fi

    # Start in background
    nohup node server.js > "$LOG_DIR/dashboard.log" 2>&1 &
    echo $! > "$PID_DIR/dashboard.pid"

    # Wait for ready
    if wait_for_health "http://localhost:$DASHBOARD_PORT" 10; then
        success "Dashboard ready at http://localhost:$DASHBOARD_PORT"
    else
        error "Dashboard failed to start"
        return 1
    fi
}

start_voice() {
    log "Starting Voice daemon on port $VOICE_PORT..."

    if check_port $VOICE_PORT; then
        warn "Voice daemon already running on port $VOICE_PORT"
        return 0
    fi

    # Check for API key
    if [ -z "$ELEVENLABS_API_KEY" ] && [ -z "$OPENAI_API_KEY" ]; then
        warn "No voice API keys found. Voice will use local TTS."
    fi

    cd "$VOICE_DIR"

    # Start voice daemon
    nohup uv run server.py > "$LOG_DIR/voice.log" 2>&1 &
    echo $! > "$PID_DIR/voice.pid"

    # Wait for ready
    if wait_for_health "http://localhost:$VOICE_PORT/health" 15; then
        success "Voice daemon ready at http://localhost:$VOICE_PORT"
    else
        warn "Voice daemon not responding (may be optional)"
    fi
}

stop_services() {
    log "Stopping CODEXA services..."

    # Stop dashboard
    if [ -f "$PID_DIR/dashboard.pid" ]; then
        kill $(cat "$PID_DIR/dashboard.pid") 2>/dev/null || true
        rm "$PID_DIR/dashboard.pid"
        success "Dashboard stopped"
    fi

    # Stop voice
    if [ -f "$PID_DIR/voice.pid" ]; then
        kill $(cat "$PID_DIR/voice.pid") 2>/dev/null || true
        rm "$PID_DIR/voice.pid"
        success "Voice daemon stopped"
    fi

    # Kill by port as fallback
    kill_port $DASHBOARD_PORT
    kill_port $VOICE_PORT

    success "All services stopped"
}

show_status() {
    echo ""
    echo "╭─────────────────────────────────────────────────────────────╮"
    echo "│                    CODEXA.app Status                        │"
    echo "├─────────────────────────────────────────────────────────────┤"

    if check_port $DASHBOARD_PORT; then
        echo -e "│  Dashboard:  ${GREEN}● Running${NC} at http://localhost:$DASHBOARD_PORT      │"
    else
        echo -e "│  Dashboard:  ${RED}○ Stopped${NC}                                    │"
    fi

    if check_port $VOICE_PORT; then
        echo -e "│  Voice:      ${GREEN}● Running${NC} at http://localhost:$VOICE_PORT       │"
    else
        echo -e "│  Voice:      ${YELLOW}○ Not running${NC} (optional)                   │"
    fi

    echo "├─────────────────────────────────────────────────────────────┤"
    echo "│  MCP Servers: Configured in .mcp.json                       │"
    echo "│  - scout (path discovery)                                   │"
    echo "│  - codexa-commands (command discovery)                      │"
    echo "│  - browser (puppeteer)                                      │"
    echo "│  - voice (STT/TTS)                                          │"
    echo "├─────────────────────────────────────────────────────────────┤"
    echo "│  Commands:                                                  │"
    echo "│  - /codexa \"task\" - Primary orchestrator                    │"
    echo "│  - /prime - System status                                   │"
    echo "│  - /v - Voice mode                                          │"
    echo "╰─────────────────────────────────────────────────────────────╯"
    echo ""
}

# Main
case "${1:-start}" in
    start)
        log "Starting CODEXA.app services..."
        start_dashboard

        if [ "$2" == "--voice" ] || [ "$1" == "--voice" ]; then
            start_voice
        fi

        show_status
        success "CODEXA.app ready! Run 'claude' to start."
        ;;

    --voice)
        log "Starting CODEXA.app with Voice..."
        start_dashboard
        start_voice
        show_status
        ;;

    --stop|stop)
        stop_services
        ;;

    --status|status)
        show_status
        ;;

    *)
        echo "Usage: $0 [start|--voice|--stop|--status]"
        exit 1
        ;;
esac
