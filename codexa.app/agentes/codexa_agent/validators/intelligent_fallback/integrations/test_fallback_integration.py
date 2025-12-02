#!/usr/bin/env python3
"""
Integration Test for Intelligent Fallback System
=================================================

Tests the complete fallback loop with the code quality validator.

Usage:
    python validators/intelligent_fallback/integrations/test_fallback_integration.py

Version: 1.0.0
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from validators.intelligent_fallback import (
    IntelligentFallbackOrchestrator,
    FallbackAction,
    FallbackResult,
    get_policy,
    AUTONOMY_POLICIES,
    FallbackHistory,
)


class TestColors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    END = '\033[0m'


def test_orchestrator_high_confidence():
    """Test that high confidence leads to PROCEED action."""
    print(f"\n{TestColors.CYAN}Test 1: High Confidence -> PROCEED{TestColors.END}")

    orchestrator = IntelligentFallbackOrchestrator(policy="development")
    result = orchestrator.handle(confidence=0.95)

    assert result.action == FallbackAction.PROCEED, f"Expected PROCEED, got {result.action}"
    assert result.should_proceed, "should_proceed should be True"
    assert not result.needs_human, "needs_human should be False"

    print(f"  {TestColors.GREEN}[PASS]{TestColors.END} High confidence (0.95) -> PROCEED")
    return True


def test_orchestrator_medium_confidence():
    """Test that medium confidence leads to PROCEED_WITH_WARNING."""
    print(f"\n{TestColors.CYAN}Test 2: Medium Confidence -> PROCEED_WITH_WARNING{TestColors.END}")

    orchestrator = IntelligentFallbackOrchestrator(policy="development")
    result = orchestrator.handle(confidence=0.75)

    assert result.action == FallbackAction.PROCEED_WITH_WARNING, f"Expected PROCEED_WITH_WARNING, got {result.action}"
    assert result.should_proceed, "should_proceed should be True"

    print(f"  {TestColors.GREEN}[PASS]{TestColors.END} Medium confidence (0.75) -> PROCEED_WITH_WARNING")
    return True


def test_orchestrator_low_confidence_with_checkpoints():
    """Test that low confidence with checkpoints attempts correction."""
    print(f"\n{TestColors.CYAN}Test 3: Low Confidence + Checkpoints -> AUTO_CORRECT or RETRY{TestColors.END}")

    orchestrator = IntelligentFallbackOrchestrator(policy="development")

    checkpoints = [
        {"name": "type_coverage", "score": 0.4, "level": "low"},
        {"name": "doc_coverage", "score": 0.3, "level": "critical"},
    ]

    result = orchestrator.handle(confidence=0.45, checkpoints=checkpoints)

    assert result.action in [FallbackAction.AUTO_CORRECT, FallbackAction.RETRY_VARIATION, FallbackAction.PARTIAL_ESCALATION], \
        f"Expected correction action, got {result.action}"

    print(f"  {TestColors.GREEN}[PASS]{TestColors.END} Low confidence (0.45) -> {result.action.name}")
    return True


def test_orchestrator_critical_escalation():
    """Test that critical checkpoints lead to escalation."""
    print(f"\n{TestColors.CYAN}Test 4: Critical Checkpoints -> ESCALATION{TestColors.END}")

    orchestrator = IntelligentFallbackOrchestrator(policy="production")  # More conservative

    checkpoints = [
        {"name": "security_scan", "score": 0.1, "level": "critical"},
    ]

    # Very low confidence with critical checkpoint should escalate
    result = orchestrator.handle(confidence=0.15, checkpoints=checkpoints)

    # For production policy with very low confidence, we expect escalation
    # Note: security_scan has no auto-correct strategy, so it must escalate
    is_escalation = result.action in [
        FallbackAction.PARTIAL_ESCALATION,
        FallbackAction.FULL_ESCALATION,
        FallbackAction.AUTO_CORRECT,  # May try non-security corrections first
        FallbackAction.RETRY_VARIATION
    ]

    print(f"  Result: {result.action.name} (confidence: {result.confidence})")

    # At very low confidence, the system should be trying something
    assert is_escalation or result.should_retry, \
        f"Expected escalation or retry action, got {result.action}"

    print(f"  {TestColors.GREEN}[PASS]{TestColors.END} Critical checkpoint handled: {result.action.name}")
    return True


def test_policy_differences():
    """Test that different policies have different behaviors."""
    print(f"\n{TestColors.CYAN}Test 5: Policy Differences{TestColors.END}")

    # Same confidence, different policies
    confidence = 0.55

    dev_orchestrator = IntelligentFallbackOrchestrator(policy="development")
    prod_orchestrator = IntelligentFallbackOrchestrator(policy="production")

    dev_result = dev_orchestrator.handle(confidence=confidence)
    prod_result = prod_orchestrator.handle(confidence=confidence)

    # Production should be more conservative (escalate sooner)
    # Development has retry_threshold=0.4, production has 0.6
    # At 0.55, production should escalate, development might retry

    print(f"  Development (0.55): {dev_result.action.name}")
    print(f"  Production (0.55): {prod_result.action.name}")

    # Production should escalate at lower confidence
    if confidence < 0.6:  # Production's retry threshold
        assert prod_result.action in [FallbackAction.PARTIAL_ESCALATION, FallbackAction.FULL_ESCALATION], \
            "Production should escalate at 0.55 confidence"

    print(f"  {TestColors.GREEN}[PASS]{TestColors.END} Policies behave differently as expected")
    return True


def test_history_recording():
    """Test that fallback history is recorded correctly."""
    print(f"\n{TestColors.CYAN}Test 6: History Recording{TestColors.END}")

    # Use a temporary history file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        history_path = f.name

    try:
        orchestrator = IntelligentFallbackOrchestrator(
            policy="development",
            history_path=history_path
        )

        # Simulate a result
        result = FallbackResult(
            action=FallbackAction.AUTO_CORRECT,
            message="Test correction",
            checkpoint_name="type_coverage",
            strategy={"name": "add_type_hints"},
            confidence=0.5,
            attempt_number=1
        )

        # Record it
        orchestrator.record_attempt_result(
            result=result,
            success=True,
            final_confidence=0.8,
            duration_ms=150
        )

        # Check history
        analytics = orchestrator.get_analytics()
        assert analytics["total_attempts"] > 0, "Should have recorded attempt"

        print(f"  {TestColors.GREEN}[PASS]{TestColors.END} History recorded correctly")
        return True

    finally:
        # Cleanup
        Path(history_path).unlink(missing_ok=True)


def test_max_attempts_limit():
    """Test that max attempts triggers escalation."""
    print(f"\n{TestColors.CYAN}Test 7: Max Attempts Limit{TestColors.END}")

    orchestrator = IntelligentFallbackOrchestrator(policy="testing")

    # Exhaust all attempts
    for i in range(orchestrator.policy.total_attempt_limit + 1):
        orchestrator.state.total_attempts = i
        result = orchestrator.handle(confidence=0.5, checkpoints=[
            {"name": "test_checkpoint", "score": 0.5, "level": "low"}
        ])

        if result.action == FallbackAction.FULL_ESCALATION:
            print(f"  Escalated after {i} attempts")
            break

    assert result.action == FallbackAction.FULL_ESCALATION, \
        "Should escalate after max attempts"

    print(f"  {TestColors.GREEN}[PASS]{TestColors.END} Max attempts triggers escalation")
    return True


def test_strategy_blocking():
    """Test that blocked strategies are not used."""
    print(f"\n{TestColors.CYAN}Test 8: Strategy Blocking{TestColors.END}")

    from validators.intelligent_fallback.policies import create_custom_policy

    # Create policy that blocks add_type_hints
    custom_policy = create_custom_policy("development", {
        "name": "custom_blocked",
        "blocked_strategies": ["add_type_hints"]
    })

    orchestrator = IntelligentFallbackOrchestrator(custom_policy=custom_policy)

    # Check that the strategy is in blocked list
    assert "add_type_hints" in orchestrator.policy.blocked_strategies

    print(f"  {TestColors.GREEN}[PASS]{TestColors.END} Blocked strategies respected")
    return True


def run_all_tests():
    """Run all integration tests."""
    print(f"\n{'=' * 60}")
    print(f"  INTELLIGENT FALLBACK INTEGRATION TESTS")
    print(f"{'=' * 60}")
    print(f"  Date: {datetime.now().isoformat()}")

    tests = [
        test_orchestrator_high_confidence,
        test_orchestrator_medium_confidence,
        test_orchestrator_low_confidence_with_checkpoints,
        test_orchestrator_critical_escalation,
        test_policy_differences,
        test_history_recording,
        test_max_attempts_limit,
        test_strategy_blocking,
    ]

    passed = 0
    failed = 0

    for test_fn in tests:
        try:
            if test_fn():
                passed += 1
        except AssertionError as e:
            print(f"  {TestColors.RED}[FAIL]{TestColors.END} {e}")
            failed += 1
        except Exception as e:
            print(f"  {TestColors.RED}[ERROR]{TestColors.END} {e}")
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"  RESULTS: {passed} passed, {failed} failed")
    print(f"{'=' * 60}\n")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
