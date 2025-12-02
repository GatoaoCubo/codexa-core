#!/usr/bin/env python3
"""
CODEXA Voice Setup
==================

Setup wizard with voice instructions for accessibility users.

Usage:
    python -m codexa.app.voice.setup
"""

from .wizard import run_setup

__all__ = ['run_setup']
