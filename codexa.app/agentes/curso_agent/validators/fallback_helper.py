"""
Fallback Helper for curso_agent
================================

Provides easy access to Intelligent Fallback from codexa_agent.

Usage:
    from validators.fallback_helper import (
        IntelligentFallbackOrchestrator,
        FallbackMixin,
        FallbackAction
    )

Version: 1.0.0
"""

import sys
from pathlib import Path

# Add codexa_agent to path
CODEXA_PATH = Path(__file__).parent.parent.parent / "codexa_agent"
if str(CODEXA_PATH) not in sys.path:
    sys.path.insert(0, str(CODEXA_PATH))

# Import from codexa_agent
try:
    from validators.intelligent_fallback import (
        IntelligentFallbackOrchestrator,
        FallbackMixin,
        FallbackAction,
        FallbackResult,
        get_policy,
        detect_context,
        AUTONOMY_POLICIES,
    )
    from validators.value_function import (
        ValueFunctionMixin,
        GradientReport,
        ConfidenceLevel,
    )
    FALLBACK_AVAILABLE = True
except ImportError as e:
    FALLBACK_AVAILABLE = False
    import_error = str(e)

    # Provide dummy classes if import fails
    class FallbackMixin:
        def init_fallback(self, *args, **kwargs): pass
        def run_with_fallback(self, fn, **kwargs): return {"status": "unavailable", "result": fn()}

    class ValueFunctionMixin:
        def reset_checkpoints(self): pass
        def add_checkpoint(self, *args, **kwargs): pass
        def generate_gradient_report(self): return None


def check_availability():
    """Check if fallback is available and print status."""
    if FALLBACK_AVAILABLE:
        print("[OK] Intelligent Fallback available from codexa_agent")
        return True
    else:
        print(f"[!] Intelligent Fallback not available: {import_error}")
        return False


if __name__ == "__main__":
    check_availability()
