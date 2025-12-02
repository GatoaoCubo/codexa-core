#!/bin/bash
# Script to run ADW in WSL with GitHub token

export GITHUB_PAT=${GITHUB_PAT:-"your-github-token-here"}
export PATH=$HOME/.local/bin:$PATH
cd /mnt/c/Users/Dell/tac-7/adws
~/.local/bin/uv run adw_plan_build_iso.py 1
