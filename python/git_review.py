#!/usr/bin/env python3
"""
Git Review - Collect git change data for review
KEYWORDS: git|review|diff|security|quality
"""

import sys
import click
import subprocess
import json
from pathlib import Path
from datetime import datetime


@click.command()
@click.option('--mode', default='quick', type=click.Choice(['quick', 'detailed', 'security']), help='Review mode')
@click.option('--output-context', default='.git_review_context.json', help='Output context file')
def main(mode: str, output_context: str):
    """Collect git change data for review."""

    click.echo(f"[*] Gathering git changes (mode: {mode})")

    # 1. Get git status
    try:
        status_result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True, text=True, check=True
        )
        status_output = status_result.stdout
    except subprocess.CalledProcessError as e:
        click.echo(f"[ERROR] Git status failed: {e}", err=True)
        sys.exit(1)

    # 2. Get diff stats
    try:
        diff_stat_result = subprocess.run(
            ['git', 'diff', '--stat'],
            capture_output=True, text=True, check=True
        )
        diff_stat = diff_stat_result.stdout

        diff_cached_stat_result = subprocess.run(
            ['git', 'diff', '--cached', '--stat'],
            capture_output=True, text=True, check=True
        )
        diff_cached_stat = diff_cached_stat_result.stdout
    except subprocess.CalledProcessError as e:
        click.echo(f"[ERROR] Git diff failed: {e}", err=True)
        sys.exit(1)

    # 3. Get file list
    try:
        files_result = subprocess.run(
            ['git', 'diff', '--name-only'],
            capture_output=True, text=True, check=True
        )
        unstaged_files = [f for f in files_result.stdout.split('\n') if f]

        staged_result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            capture_output=True, text=True, check=True
        )
        staged_files = [f for f in staged_result.stdout.split('\n') if f]
    except subprocess.CalledProcessError as e:
        click.echo(f"[ERROR] Git file list failed: {e}", err=True)
        sys.exit(1)

    # 4. Get full diff content (for detailed mode)
    full_diff = None
    if mode in ['detailed', 'security']:
        try:
            diff_result = subprocess.run(
                ['git', 'diff'],
                capture_output=True, text=True, check=True
            )
            diff_cached_result = subprocess.run(
                ['git', 'diff', '--cached'],
                capture_output=True, text=True, check=True
            )
            full_diff = {
                'unstaged': diff_result.stdout,
                'staged': diff_cached_result.stdout
            }
        except subprocess.CalledProcessError as e:
            click.echo(f"[ERROR] Full diff failed: {e}", err=True)
            sys.exit(1)

    # 5. Count changes
    total_files = len(set(unstaged_files + staged_files))

    # Prepare context
    context = {
        'timestamp': datetime.now().isoformat(),
        'mode': mode,
        'status': status_output,
        'diff_stat': diff_stat,
        'diff_cached_stat': diff_cached_stat,
        'unstaged_files': unstaged_files,
        'staged_files': staged_files,
        'total_files': total_files,
        'full_diff': full_diff
    }

    # Write context file
    context_file = Path(output_context)
    context_file.write_text(json.dumps(context, indent=2), encoding='utf-8')

    # Output summary
    click.echo(f"\n[SUCCESS] Git review context prepared")
    click.echo(f"  Mode: {mode}")
    click.echo(f"  Total files changed: {total_files}")
    click.echo(f"  Unstaged: {len(unstaged_files)}")
    click.echo(f"  Staged: {len(staged_files)}")
    click.echo(f"  Context file: {context_file}")
    click.echo(f"\n[NEXT] Review analysis will be performed")

    return 0


if __name__ == '__main__':
    sys.exit(main())
