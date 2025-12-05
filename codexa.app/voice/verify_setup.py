#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODEXA Voice - Setup Verification Script
=========================================

Verifies that all dependencies are installed and configured correctly.
Run this after installing dependencies to ensure the voice server will work.
"""

import sys
import os
from pathlib import Path

# Colors for terminal output (Windows compatible)
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def check_python_version():
    """Check if Python version is 3.10+"""
    print(f"{BLUE}Checking Python version...{RESET}")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"  {GREEN}✓{RESET} Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"  {RED}✗{RESET} Python {version.major}.{version.minor}.{version.micro} (need 3.10+)")
        return False

def check_dependency(package_name, import_name=None):
    """Check if a Python package is installed"""
    if import_name is None:
        import_name = package_name

    try:
        __import__(import_name)
        print(f"  {GREEN}✓{RESET} {package_name}")
        return True
    except ImportError:
        print(f"  {RED}✗{RESET} {package_name} (not installed)")
        return False

def check_all_dependencies():
    """Check all required dependencies"""
    print(f"\n{BLUE}Checking dependencies...{RESET}")

    deps = [
        ("sounddevice", "sounddevice"),
        ("soundfile", "soundfile"),
        ("numpy", "numpy"),
        ("edge-tts", "edge_tts"),
        ("pyttsx3", "pyttsx3"),
        ("pygame", "pygame"),
        ("python-dotenv", "dotenv"),
        ("mcp", "mcp"),
        ("elevenlabs", "elevenlabs"),
    ]

    results = []
    for package, import_name in deps:
        results.append(check_dependency(package, import_name))

    return all(results)

def check_env_file():
    """Check if .env file exists and has API key"""
    print(f"\n{BLUE}Checking .env configuration...{RESET}")

    project_root = Path(__file__).parent.parent.parent
    env_path = project_root / ".env"

    if not env_path.exists():
        print(f"  {YELLOW}!{RESET} .env file not found at {env_path}")
        print(f"  {YELLOW}→{RESET} Create .env with: ELEVENLABS_API_KEY=sk_your_key_here")
        return False

    print(f"  {GREEN}✓{RESET} .env file exists")

    # Check for API key
    with open(env_path, 'r') as f:
        content = f.read()
        if "ELEVENLABS_API_KEY" in content and "sk_" in content:
            print(f"  {GREEN}✓{RESET} ELEVENLABS_API_KEY configured")
            return True
        else:
            print(f"  {YELLOW}!{RESET} ELEVENLABS_API_KEY not found or invalid")
            print(f"  {YELLOW}→{RESET} Add to .env: ELEVENLABS_API_KEY=sk_your_key_here")
            return False

def check_audio_devices():
    """Check if audio devices are available"""
    print(f"\n{BLUE}Checking audio devices...{RESET}")

    try:
        import sounddevice as sd
        devices = sd.query_devices()

        # Find input device
        input_devices = [d for d in devices if d['max_input_channels'] > 0]
        if input_devices:
            print(f"  {GREEN}✓{RESET} Found {len(input_devices)} input device(s)")
            default_input = sd.query_devices(kind='input')
            print(f"    Default: {default_input['name']}")
        else:
            print(f"  {RED}✗{RESET} No input devices found")
            return False

        # Find output device
        output_devices = [d for d in devices if d['max_output_channels'] > 0]
        if output_devices:
            print(f"  {GREEN}✓{RESET} Found {len(output_devices)} output device(s)")
            default_output = sd.query_devices(kind='output')
            print(f"    Default: {default_output['name']}")
        else:
            print(f"  {RED}✗{RESET} No output devices found")
            return False

        return True

    except Exception as e:
        print(f"  {RED}✗{RESET} Error checking audio devices: {e}")
        return False

def main():
    """Run all verification checks"""
    print("=" * 60)
    print("CODEXA Voice - Setup Verification")
    print("=" * 60)

    checks = []

    # Run all checks
    checks.append(("Python Version", check_python_version()))
    checks.append(("Dependencies", check_all_dependencies()))
    checks.append(("Environment", check_env_file()))
    checks.append(("Audio Devices", check_audio_devices()))

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    all_passed = True
    for name, passed in checks:
        status = f"{GREEN}PASS{RESET}" if passed else f"{RED}FAIL{RESET}"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print(f"\n{GREEN}✓ All checks passed!{RESET}")
        print(f"\nYou can now use the voice server:")
        print(f"  1. Start Claude Code")
        print(f"  2. Type /v to start voice mode")
        print(f"\nOr test manually:")
        print(f"  python codexa.app/voice/server.py")
    else:
        print(f"\n{RED}✗ Some checks failed{RESET}")
        print(f"\nTo fix:")
        print(f"  1. Install missing dependencies:")
        print(f"     python -m pip install -r codexa.app/voice/requirements.txt")
        print(f"  2. Configure .env file with your ElevenLabs API key")
        print(f"  3. Check audio device settings in Windows")

    return 0 if all_passed else 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Verification cancelled{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Error: {e}{RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
