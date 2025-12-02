#!/usr/bin/env python3
"""
Document Feature - Generate LLM-optimized documentation from git changes
KEYWORDS: document|feature|git-diff|markdown|app-docs
"""

import sys
import click
import subprocess
from pathlib import Path
from datetime import datetime
import shutil


@click.command()
@click.argument('adw_id')
@click.argument('spec_path', required=False)
@click.argument('screenshots_dir', required=False)
@click.option('--format', default='markdown', help='Output format (markdown, json)')
@click.option('--output-dir', default='app_docs', help='Output directory for documentation')
def main(adw_id: str, spec_path: str, screenshots_dir: str, format: str, output_dir: str):
    """Generate feature documentation from git changes and spec.

    Args:
        adw_id: 8-character ADW identifier
        spec_path: Optional path to specification file
        screenshots_dir: Optional directory containing screenshots to copy
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Analyze git changes
    click.echo("[*] Analyzing git changes...")
    try:
        stat_result = subprocess.run(
            ['git', 'diff', 'origin/main', '--stat'],
            capture_output=True, text=True, check=True
        )
        click.echo(stat_result.stdout)

        files_result = subprocess.run(
            ['git', 'diff', 'origin/main', '--name-only'],
            capture_output=True, text=True, check=True
        )
        changed_files = [f for f in files_result.stdout.split('\n') if f]

    except subprocess.CalledProcessError as e:
        click.echo(f"[ERROR] Git command failed: {e}", err=True)
        sys.exit(1)

    # 2. Read specification if provided
    spec_content = None
    if spec_path:
        spec_file = Path(spec_path)
        if spec_file.exists():
            click.echo(f"[*] Reading specification: {spec_path}")
            spec_content = spec_file.read_text(encoding='utf-8')
        else:
            click.echo(f"[WARN] Spec file not found: {spec_path}")

    # 3. Copy screenshots if provided
    screenshots = []
    if screenshots_dir:
        src_dir = Path(screenshots_dir)
        if src_dir.exists():
            assets_dir = output_dir / 'assets'
            assets_dir.mkdir(parents=True, exist_ok=True)

            click.echo(f"[*] Copying screenshots from {screenshots_dir}...")
            for screenshot in src_dir.glob('*.png'):
                dest = assets_dir / screenshot.name
                shutil.copy2(screenshot, dest)
                screenshots.append(screenshot.name)
                click.echo(f"  ✓ Copied: {screenshot.name}")

    # 4. Output collected information (to be consumed by LLM)
    output_data = {
        'adw_id': adw_id,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'spec_path': spec_path or 'N/A',
        'changed_files': changed_files,
        'screenshots': screenshots,
        'spec_content': spec_content,
        'output_dir': str(output_dir)
    }

    # Write to temp file for LLM consumption
    import json
    temp_file = Path('.document_context.json')
    temp_file.write_text(json.dumps(output_data, indent=2), encoding='utf-8')

    click.echo(f"\n[SUCCESS] Context prepared for documentation generation")
    click.echo(f"  ADW ID: {adw_id}")
    click.echo(f"  Changed files: {len(changed_files)}")
    click.echo(f"  Screenshots: {len(screenshots)}")
    click.echo(f"  Context file: {temp_file}")
    click.echo(f"\n[NEXT] LLM will generate documentation using this context")

    return 0


if __name__ == '__main__':
    sys.exit(main())
