#!/usr/bin/env python3
"""
CODEXA CLI - Optimized Command-Line Interface

Optimized version with lazy loading and reduced initialization time.
"""

import os
import sys
import json
import platform
import click
from pathlib import Path
from typing import Optional, Dict, Any

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Lazy imports - only load what we need
_modules_cache = {}


def get_module(module_name: str):
    """Lazy load modules only when needed."""
    if module_name not in _modules_cache:
        if module_name == 'crud':
            from modules.crud_ops import CRUDOperations
            _modules_cache[module_name] = CRUDOperations
        elif module_name == 'scout':
            from modules.scout_ops import ScoutOperations
            _modules_cache[module_name] = ScoutOperations
        elif module_name == 'product':
            from modules.ecommerce.product_manager import ProductManager
            _modules_cache[module_name] = ProductManager
        elif module_name == 'strategy':
            from modules.ecommerce.strategy_mentor import StrategyMentor
            _modules_cache[module_name] = StrategyMentor
        elif module_name == 'competitor':
            from modules.ecommerce.competitor_scout import CompetitorScout
            _modules_cache[module_name] = CompetitorScout
        elif module_name == 'knowledge':
            from modules.ecommerce.knowledge_base import KnowledgeBase
            _modules_cache[module_name] = KnowledgeBase
    return _modules_cache.get(module_name)


def quick_status():
    """Quick status check without loading all modules."""
    working_dir = Path(__file__).parent

    # Check basic status
    status = {
        "working_dir": str(working_dir),
        "git_repo": (working_dir.parent / ".git").exists(),
        "readme_exists": (working_dir / "README.md").exists(),
    }

    # Quick git info if available
    if status["git_repo"]:
        try:
            import subprocess
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=str(working_dir.parent),
                capture_output=True,
                text=True,
                timeout=1
            )
            status["git_branch"] = result.stdout.strip()
        except:
            status["git_branch"] = "unknown"

    return status


@click.group()
@click.option('--quiet', '-q', is_flag=True, help='Suppress initialization messages')
@click.pass_context
def cli(ctx, quiet):
    """
    CODEXA - HOP Meta-Agent CLI (Optimized)

    Create, Organize, Read, Update, Delete E-com X-Agent
    Fast and efficient interface for documentation and e-commerce operations.
    """
    ctx.ensure_object(dict)
    ctx.obj['quiet'] = quiet
    ctx.obj['working_dir'] = str(Path(__file__).parent)


@cli.command()
@click.pass_context
def status(ctx):
    """Show quick CODEXA system status."""
    info = quick_status()

    print("\n===== CODEXA System Status (Quick) =====")
    print(f"Working Directory: {info['working_dir']}")
    print(f"Git Repository: {'Yes' if info['git_repo'] else 'No'}")
    print(f"README Exists: {'Yes' if info['readme_exists'] else 'No'}")
    if info.get('git_branch'):
        print(f"Git Branch: {info['git_branch']}")
    print("========================================\n")


@cli.group()
@click.pass_context
def crud(ctx):
    """CRUD operations for documentation and data."""
    pass


@crud.command('list')
@click.option('--type', '-t', default='all', help='Type of items to list')
@click.option('--format', '-f', default='simple', help='Output format')
@click.pass_context
def crud_list(ctx, type, format):
    """List documents and data."""
    # Only load CRUD module when actually needed
    working_dir = ctx.obj['working_dir']
    CRUDOps = get_module('crud')

    if not ctx.obj['quiet']:
        print("Loading CRUD module...")

    crud_ops = CRUDOps(working_dir)
    result = crud_ops.list_items(data_type=type if type != 'all' else None)

    if format == 'json':
        import json
        print(json.dumps(result, indent=2))
    else:
        print(f"\nFound {result.get('count', 0)} items:")
        for item in result.get('items', [])[:10]:
            print(f"  - {item}")
        if result.get('count', 0) > 10:
            print(f"  ... and {result['count'] - 10} more")


@crud.command('read')
@click.argument('path')
@click.pass_context
def crud_read(ctx, path):
    """Read a document or data file."""
    working_dir = ctx.obj['working_dir']
    CRUDOps = get_module('crud')

    if not ctx.obj['quiet']:
        print("Loading CRUD module...")

    crud_ops = CRUDOps(working_dir)
    result = crud_ops.read_file(path)

    if result['success']:
        print(result['content'])
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")


@crud.command('create')
@click.argument('path')
@click.option('--content', '-c', help='Content to write')
@click.pass_context
def crud_create(ctx, path, content):
    """Create a new document."""
    working_dir = ctx.obj['working_dir']
    CRUDOps = get_module('crud')

    if not ctx.obj['quiet']:
        print("Loading CRUD module...")

    crud_ops = CRUDOps(working_dir)
    result = crud_ops.create_file(path, content or '')

    if result['success']:
        print(f"Created: {path}")
    else:
        print(f"Error: {result.get('error', 'Unknown error')}")


@cli.group()
@click.pass_context
def scout(ctx):
    """Scout operations for repository navigation."""
    pass


@scout.command('scan')
@click.option('--cache/--no-cache', default=True, help='Use cache')
@click.pass_context
def scout_scan(ctx, cache):
    """Scan repository structure."""
    working_dir = ctx.obj['working_dir']
    ScoutOps = get_module('scout')

    if not ctx.obj['quiet']:
        print("Loading Scout module...")

    scout_ops = ScoutOps(working_dir)
    result = scout_ops.scan_repository(use_cache=cache)

    print(f"\nRepository scan complete:")
    print(f"  Files: {result.get('stats', {}).get('total_files', 0)}")
    print(f"  Directories: {result.get('stats', {}).get('total_dirs', 0)}")
    print(f"  Size: {result.get('stats', {}).get('total_size', 0):,} bytes")


@scout.command('find')
@click.option('--pattern', '-p', help='Search pattern')
@click.option('--type', '-t', help='File type')
@click.pass_context
def scout_find(ctx, pattern, type):
    """Find files in repository."""
    working_dir = ctx.obj['working_dir']
    ScoutOps = get_module('scout')

    if not ctx.obj['quiet']:
        print("Loading Scout module...")

    scout_ops = ScoutOps(working_dir)
    result = scout_ops.find_files(pattern=pattern, file_type=type)

    print(f"\nFound {len(result.get('files', []))} files:")
    for file in result.get('files', [])[:10]:
        print(f"  - {file}")


@cli.group()
@click.pass_context
def ecom(ctx):
    """E-commerce operations."""
    pass


@ecom.group('products')
@click.pass_context
def ecom_products(ctx):
    """Product management operations."""
    pass


@ecom_products.command('list')
@click.pass_context
def products_list(ctx):
    """List products."""
    working_dir = ctx.obj['working_dir']
    ProductMgr = get_module('product')

    if not ctx.obj['quiet']:
        print("Loading Product Manager...")

    pm = ProductMgr(working_dir)
    result = pm.list_products()

    print(f"\nProducts ({result.get('count', 0)}):")
    for product in result.get('products', []):
        print(f"  - {product.get('name', 'Unknown')} (${product.get('price', 0)})")


@cli.command('quick')
@click.argument('operation')
@click.option('--module', '-m', help='Module to use')
@click.pass_context
def quick_command(ctx, operation, module):
    """
    Quick command execution without full initialization.

    Examples:
        codexa quick status
        codexa quick list --module crud
        codexa quick scan --module scout
    """
    if operation == 'status':
        ctx.invoke(status)
    elif operation == 'list' and module == 'crud':
        ctx.invoke(crud_list, type='document', format='simple')
    elif operation == 'scan' and module == 'scout':
        ctx.invoke(scout_scan, cache=True)
    else:
        print(f"Unknown quick operation: {operation}")


if __name__ == "__main__":
    # Set minimal logging
    import logging
    logging.basicConfig(level=logging.WARNING)

    # Run CLI
    cli()