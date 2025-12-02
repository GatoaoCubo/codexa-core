#!/bin/bash
# ADW-100 Documentation Validation Script
# Validates all agent documentation and generates reports

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODEXA_DIR="$(dirname "$SCRIPT_DIR")"
VALIDATOR="$CODEXA_DIR/validators/12_doc_sync_validator.py"
BUILDER="$CODEXA_DIR/builders/11_doc_sync_builder.py"
REPORTS_DIR="$CODEXA_DIR/workflows/reports"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Functions
print_header() {
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}============================================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Main execution
print_header "ADW-100 Documentation Validation"

echo "Working directory: $CODEXA_DIR"
echo ""

# Check if validator exists
if [ ! -f "$VALIDATOR" ]; then
    print_error "Validator not found: $VALIDATOR"
    exit 1
fi

# Parse arguments
MODE="validate"  # Default mode
AUTO_FIX=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --auto-fix)
            AUTO_FIX=true
            shift
            ;;
        --audit)
            MODE="audit"
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --auto-fix    Run builder in auto-fix mode if validation fails"
            echo "  --audit       Run audit only (no validation threshold)"
            echo "  --help        Show this help message"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Run validation
print_header "Step 1: Running Documentation Validator"

cd "$CODEXA_DIR"

if python "$VALIDATOR" --all --output "$REPORTS_DIR/validation_$(date +%Y%m%d_%H%M%S).md"; then
    print_success "All documentation meets quality standards (score ≥0.85)"
    VALIDATION_PASSED=true
else
    print_error "Documentation validation failed (score <0.85)"
    VALIDATION_PASSED=false
fi

echo ""

# Auto-fix if requested and validation failed
if [ "$AUTO_FIX" = true ] && [ "$VALIDATION_PASSED" = false ]; then
    print_header "Step 2: Running Auto-Fix (ADW-100 Builder)"

    if python "$BUILDER" --mode auto_fix; then
        print_success "Documentation auto-fixed successfully"
        echo ""

        print_header "Step 3: Re-validating After Auto-Fix"

        if python "$VALIDATOR" --all; then
            print_success "Validation passed after auto-fix!"
            exit 0
        else
            print_warning "Some issues remain after auto-fix. Manual intervention may be needed."
            exit 1
        fi
    else
        print_error "Auto-fix failed"
        exit 1
    fi
fi

# Exit with appropriate code
if [ "$VALIDATION_PASSED" = true ]; then
    print_header "Summary"
    print_success "Documentation validation completed successfully"
    echo ""
    echo "Latest report: $REPORTS_DIR/validation_$(date +%Y%m%d)_*.md"
    exit 0
else
    print_header "Summary"
    print_error "Documentation validation failed"
    echo ""
    echo "Options:"
    echo "  1. Review the validation report in $REPORTS_DIR"
    echo "  2. Run with --auto-fix to automatically fix issues"
    echo "  3. Manually fix issues and re-run validation"
    exit 1
fi
