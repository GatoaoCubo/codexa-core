#!/bin/bash
#
# Competitor Intelligence Change Monitor
# Monitors sources for changes and alerts on significant updates.
#
# Usage:
#   ./monitor_changes.sh --daily       # Daily monitoring
#   ./monitor_changes.sh --compare     # Compare with previous snapshot
#   ./monitor_changes.sh --alert       # Send alerts for changes

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
SOURCES_DIR="$ROOT_DIR/sources"
SNAPSHOTS_DIR="$ROOT_DIR/snapshots"
DOCS_DIR="$ROOT_DIR/docs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get today's date
TODAY=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)

# Create snapshot directory
SNAPSHOT_TODAY="$SNAPSHOTS_DIR/$TODAY"
mkdir -p "$SNAPSHOT_TODAY"

# Monitor function
monitor_sources() {
    log_info "Starting competitor intelligence monitoring..."

    # Check if previous snapshot exists
    YESTERDAY=$(date -d "yesterday" +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d 2>/dev/null || date +%Y-%m-%d)
    SNAPSHOT_PREV="$SNAPSHOTS_DIR/$YESTERDAY"

    if [ ! -d "$SNAPSHOT_PREV" ]; then
        log_warning "No previous snapshot found for comparison"
        log_info "Creating baseline snapshot..."
        return 0
    fi

    log_info "Comparing with snapshot: $SNAPSHOT_PREV"

    # Compare snapshots
    CHANGES_DETECTED=0

    # Check each source file
    for source_file in "$SOURCES_DIR"/*.json; do
        if [ -f "$source_file" ]; then
            filename=$(basename "$source_file")
            log_info "Checking: $filename"

            # Compare with previous version
            if [ -f "$SNAPSHOT_PREV/$filename" ]; then
                if ! diff -q "$source_file" "$SNAPSHOT_PREV/$filename" > /dev/null 2>&1; then
                    log_warning "Changes detected in: $filename"
                    CHANGES_DETECTED=$((CHANGES_DETECTED + 1))

                    # Show diff
                    diff "$SNAPSHOT_PREV/$filename" "$source_file" | head -20
                fi
            fi

            # Copy current version to today's snapshot
            cp "$source_file" "$SNAPSHOT_TODAY/"
        fi
    done

    if [ $CHANGES_DETECTED -eq 0 ]; then
        log_success "No changes detected in source files"
    else
        log_warning "Total changes detected: $CHANGES_DETECTED files"
    fi

    return $CHANGES_DETECTED
}

# Generate change report
generate_report() {
    log_info "Generating change report..."

    REPORT_FILE="$SNAPSHOT_TODAY/change_report_$TIMESTAMP.md"

    cat > "$REPORT_FILE" << EOF
# Competitor Intelligence Change Report

**Date**: $TODAY
**Timestamp**: $TIMESTAMP

## Summary

- Monitored Sources: $(find "$SOURCES_DIR" -name "*.json" | wc -l)
- Changes Detected: $1
- Snapshot Location: $SNAPSHOT_TODAY

## Categories Monitored

1. AI Courses Platforms
2. Marketplaces Documentation
3. E-commerce Trends
4. Compliance Sources

## Actions Recommended

EOF

    if [ "$1" -gt 0 ]; then
        cat >> "$REPORT_FILE" << EOF
- [ ] Review changed source files
- [ ] Update documentation as needed
- [ ] Fetch new content from updated sources
- [ ] Notify team of significant changes
- [ ] Update competitor analysis

## Changed Files

EOF
        # List changed files
        find "$SNAPSHOT_TODAY" -name "*.json" -exec basename {} \; >> "$REPORT_FILE"
    else
        cat >> "$REPORT_FILE" << EOF
- [x] No changes detected - no action required

EOF
    fi

    log_success "Report generated: $REPORT_FILE"

    # Display report
    cat "$REPORT_FILE"
}

# Fetch updates for changed sources
fetch_updates() {
    log_info "Fetching updates for changed sources..."

    # This would trigger the Python script to fetch updates
    if [ -f "$SCRIPT_DIR/fetch_docs.py" ]; then
        python3 "$SCRIPT_DIR/fetch_docs.py" --all --verbose
    else
        log_error "fetch_docs.py not found"
        return 1
    fi
}

# Alert function (placeholder)
send_alerts() {
    log_info "Sending alerts..."

    # Placeholder for alert system
    # Could integrate with:
    # - Email notifications
    # - Slack webhooks
    # - Discord webhooks
    # - GitHub issues

    log_warning "Alert system not configured yet"
    log_info "Configure alerts in monitor_changes.sh"
}

# Main execution
main() {
    case "${1:-}" in
        --daily)
            log_info "=== Daily Monitoring Run ==="
            monitor_sources
            CHANGES=$?
            generate_report $CHANGES

            if [ $CHANGES -gt 0 ]; then
                log_info "Changes detected, fetching updates..."
                fetch_updates
            fi
            ;;
        --compare)
            log_info "=== Comparison Mode ==="
            monitor_sources
            CHANGES=$?
            generate_report $CHANGES
            ;;
        --alert)
            log_info "=== Alert Mode ==="
            monitor_sources
            CHANGES=$?
            if [ $CHANGES -gt 0 ]; then
                send_alerts
            fi
            ;;
        --fetch)
            log_info "=== Fetch Updates ==="
            fetch_updates
            ;;
        *)
            echo "Competitor Intelligence Change Monitor"
            echo ""
            echo "Usage:"
            echo "  $0 --daily       Run daily monitoring"
            echo "  $0 --compare     Compare with previous snapshot"
            echo "  $0 --alert       Send alerts for changes"
            echo "  $0 --fetch       Fetch updates for all sources"
            echo ""
            exit 1
            ;;
    esac
}

main "$@"
