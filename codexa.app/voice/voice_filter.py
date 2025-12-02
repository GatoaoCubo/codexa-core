#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODEXA Voice Filter v1.0
========================

Intelligent filtering for voice commands:
- Wake word detection ("codexa", "ei codexa", "hey codexa")
- Noise gate (minimum energy threshold)
- Transcript cleaning (removes noise artifacts)
- Command validation (filters invalid/too-short commands)

This module solves the problem of capturing ambient noise
(videos, games, conversations) as voice commands.
"""

import re
from typing import Optional, Tuple, List
from dataclasses import dataclass


# =============================================================================
# CONFIGURATION
# =============================================================================

@dataclass
class FilterConfig:
    """Voice filter configuration."""

    # Wake word settings
    wake_words: List[str] = None
    require_wake_word: bool = True
    wake_word_timeout: float = 30.0  # Seconds to listen after wake word

    # Noise filtering
    min_words: int = 1  # Minimum words for valid command
    max_noise_ratio: float = 0.5  # Max ratio of noise markers

    # Energy gate
    min_energy_threshold: float = 0.025  # Minimum RMS to consider speech

    def __post_init__(self):
        if self.wake_words is None:
            self.wake_words = [
                # Primary
                "codexa",
                "ei codexa",
                "hey codexa",
                "oi codexa",
                "ok codexa",
                # Common Whisper mishearings
                "codex",
                "codigo",
                "codesa",
                "codesá",
                "code",
                "code a",
                "code x",
                "code xa",
                "codex a",
                # Variations with prefix
                "ei codigo",
                "ei codex",
                "hey codex",
                "oi codigo",
            ]


# Default configuration
DEFAULT_CONFIG = FilterConfig()


# =============================================================================
# NOISE PATTERNS
# =============================================================================

# Patterns that indicate transcription of ambient noise, not speech
NOISE_PATTERNS = [
    # Parenthetical noise descriptions (ElevenLabs artifact)
    r"^\s*\([^)]+\)\s*$",  # "(corte de video)", "(sons de tiro)"
    r"\(corte[^)]*\)",
    r"\(sons? de[^)]*\)",
    r"\(musica[^)]*\)",
    r"\(barulho[^)]*\)",
    r"\(ruido[^)]*\)",
    r"\(silencio[^)]*\)",
    r"\(inaudivel[^)]*\)",
    r"\(incompreensivel[^)]*\)",
    r"\(vacuo[^)]*\)",

    # Common transcription artifacts
    r"^\s*\.+\s*$",  # Just dots
    r"^\s*,+\s*$",  # Just commas
    r"^\s*-+\s*$",  # Just dashes
    r"^\s*hmm+\s*$",  # Just "hmm"
    r"^\s*ah+\s*$",  # Just "ah"
    r"^\s*eh+\s*$",  # Just "eh"
    r"^\s*uh+\s*$",  # Just "uh"
    r"^\s*oh+\s*$",  # Just "oh"
    r"^\s*se\.?\s*$",  # Just "se" or "se."
    r"^\s*e\.?\s*$",  # Just "e" or "e."
    r"^\s*a\.?\s*$",  # Just "a" or "a."
    r"^\s*o\.?\s*$",  # Just "o" or "o."
]

# Compile patterns for efficiency
NOISE_REGEX = [re.compile(p, re.IGNORECASE) for p in NOISE_PATTERNS]


# =============================================================================
# WAKE WORD DETECTION
# =============================================================================

def detect_wake_word(
    transcript: str,
    config: FilterConfig = None
) -> Tuple[bool, Optional[str]]:
    """
    Check if transcript contains wake word and extract command.

    Args:
        transcript: The transcribed text
        config: Filter configuration

    Returns:
        Tuple of (wake_word_detected, command_after_wake_word)
        If wake word not required, returns (True, transcript)
    """
    if config is None:
        config = DEFAULT_CONFIG

    if not config.require_wake_word:
        return True, transcript.strip()

    text = transcript.lower().strip()

    for wake_word in config.wake_words:
        wake_lower = wake_word.lower()

        # Check if text starts with wake word
        if text.startswith(wake_lower):
            # Extract command after wake word
            command = transcript[len(wake_word):].strip()
            # Remove leading punctuation
            command = command.lstrip(",.:;!? ")
            return True, command if command else None

        # Check if wake word is anywhere in text (for "ei codexa faz X")
        if wake_lower in text:
            # Find position and extract what comes after
            pos = text.find(wake_lower)
            command = transcript[pos + len(wake_word):].strip()
            command = command.lstrip(",.:;!? ")
            return True, command if command else None

    return False, None


def is_wake_word_only(transcript: str, config: FilterConfig = None) -> bool:
    """
    Check if transcript is ONLY the wake word (no command).

    Returns True if user just said "codexa" to activate,
    indicating we should listen for the actual command.
    """
    if config is None:
        config = DEFAULT_CONFIG

    text = transcript.lower().strip()
    text = text.rstrip(",.:;!? ")

    for wake_word in config.wake_words:
        if text == wake_word.lower():
            return True

    return False


# =============================================================================
# NOISE FILTERING
# =============================================================================

def is_noise(transcript: str) -> bool:
    """
    Check if transcript appears to be noise rather than speech.

    Returns True if the transcript matches known noise patterns.
    """
    if not transcript or not transcript.strip():
        return True

    text = transcript.strip()

    # Check against noise patterns
    for pattern in NOISE_REGEX:
        if pattern.match(text):
            return True

    # Check if mostly parenthetical (noise description)
    paren_matches = re.findall(r"\([^)]+\)", text)
    if paren_matches:
        paren_text = "".join(paren_matches)
        if len(paren_text) > len(text) * 0.5:
            return True

    return False


def clean_transcript(transcript: str) -> str:
    """
    Clean transcript by removing noise artifacts.

    Removes parenthetical noise descriptions while keeping
    the actual speech content.
    """
    if not transcript:
        return ""

    text = transcript.strip()

    # Remove parenthetical noise descriptions
    text = re.sub(r"\([^)]*(?:corte|sons?|musica|barulho|ruido)[^)]*\)", "", text, flags=re.IGNORECASE)

    # Clean up extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


# Exit commands that always work (no wake word needed)
EXIT_COMMANDS_FILTER = [
    "parar", "sair", "exit", "stop", "pare", "para",
    "encerrar", "tchau", "finalizar", "quit"
]


def is_exit_command_filter(transcript: str) -> bool:
    """Check if transcript is an exit command."""
    text = transcript.lower().strip()
    return any(cmd in text for cmd in EXIT_COMMANDS_FILTER)


def is_valid_command(
    transcript: str,
    config: FilterConfig = None
) -> bool:
    """
    Check if transcript is a valid voice command.

    Filters out:
    - Empty/whitespace only
    - Known noise patterns
    - Too short (single letter/word that isn't a command)
    """
    if config is None:
        config = DEFAULT_CONFIG

    if not transcript or not transcript.strip():
        return False

    if is_noise(transcript):
        return False

    # Clean and check word count
    cleaned = clean_transcript(transcript)
    words = cleaned.split()

    # Allow single words if they're likely commands
    if len(words) < config.min_words:
        # Exception: single word commands that are valid
        single_word_commands = [
            "parar", "sair", "exit", "stop", "pare", "para",
            "ajuda", "help", "sim", "nao", "ok", "cancela",
            "repita", "lista", "busca", "cria", "abre", "fecha",
        ]
        if len(words) == 1 and words[0].lower() in single_word_commands:
            return True
        return False

    return True


# =============================================================================
# MAIN FILTER FUNCTION
# =============================================================================

@dataclass
class FilterResult:
    """Result of filtering a voice transcript."""

    # Was the input accepted?
    accepted: bool

    # The cleaned command (if accepted)
    command: Optional[str] = None

    # Rejection reason (if not accepted)
    reason: Optional[str] = None

    # Was wake word detected?
    wake_word_detected: bool = False

    # Should we wait for more input? (wake word only)
    awaiting_command: bool = False

    # Original transcript
    original: str = ""


def filter_voice_input(
    transcript: str,
    config: FilterConfig = None,
    previous_wake_word: bool = False
) -> FilterResult:
    """
    Main entry point for voice filtering.

    Applies all filters and returns structured result.

    Args:
        transcript: Raw transcribed text
        config: Filter configuration
        previous_wake_word: If True, wake word was detected in previous input

    Returns:
        FilterResult with acceptance status and cleaned command
    """
    if config is None:
        config = DEFAULT_CONFIG

    result = FilterResult(accepted=False, original=transcript)

    # Empty check
    if not transcript or not transcript.strip():
        result.reason = "empty"
        return result

    # Noise check (before wake word, to filter garbage)
    if is_noise(transcript):
        result.reason = "noise"
        return result

    # Exit commands ALWAYS work (no wake word needed)
    if is_exit_command_filter(transcript):
        result.accepted = True
        result.command = clean_transcript(transcript)
        result.wake_word_detected = False  # Not required for exit
        return result

    # Wake word handling
    if config.require_wake_word and not previous_wake_word:
        # Check for wake word
        detected, command = detect_wake_word(transcript, config)
        result.wake_word_detected = detected

        if not detected:
            result.reason = "no_wake_word"
            return result

        # Wake word only? Wait for command
        if is_wake_word_only(transcript, config) or command is None:
            result.awaiting_command = True
            result.reason = "awaiting_command"
            return result

        # Got wake word + command
        transcript = command
    else:
        result.wake_word_detected = previous_wake_word

    # Clean transcript
    cleaned = clean_transcript(transcript)

    # Validate as command
    if not is_valid_command(cleaned, config):
        result.reason = "invalid_command"
        return result

    # Success!
    result.accepted = True
    result.command = cleaned
    return result


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def should_ignore(transcript: str) -> bool:
    """
    Quick check if transcript should be ignored.

    Use this for fast filtering before more expensive operations.
    """
    return is_noise(transcript)


def extract_command(transcript: str, require_wake_word: bool = True) -> Optional[str]:
    """
    Simple helper to extract command from transcript.

    Returns None if transcript is invalid/noise.
    Returns cleaned command string if valid.
    """
    config = FilterConfig(require_wake_word=require_wake_word)
    result = filter_voice_input(transcript, config)
    return result.command if result.accepted else None


# =============================================================================
# CLI TEST
# =============================================================================

if __name__ == "__main__":
    # Test cases
    test_cases = [
        "(corte de video)",
        "(sons de tiro)",
        "Hmm...",
        "se",
        "codexa",
        "codexa liste os arquivos",
        "ei codexa qual a hora",
        "E serio que voce vai ficar ai em cima?",
        "Execute o comando prime",
        "hey codexa, busca arquivos python",
        "",
        "   ",
        "ok",
        "parar",
    ]

    print("=" * 60)
    print("Voice Filter Test")
    print("=" * 60)

    config = FilterConfig(require_wake_word=True)

    for test in test_cases:
        result = filter_voice_input(test, config)
        status = "ACCEPT" if result.accepted else "REJECT"
        reason = result.reason or ""
        command = result.command or ""

        print(f"\n[{status}] '{test}'")
        if result.accepted:
            print(f"  Command: '{command}'")
        else:
            print(f"  Reason: {reason}")
        if result.awaiting_command:
            print(f"  (Awaiting follow-up command)")
