#!/usr/bin/env python3
"""
CODEXA CLI - Command-Line Interface

Unified interface for all CODEXA operations.
Provides access to CRUD, Scout, and E-commerce modules.
"""

import os
import sys
import json
import platform
import click
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Detect Windows and use ASCII-safe symbols
IS_WINDOWS = platform.system() == 'Windows'

from hop_orchestrator import HOPOrchestrator
from modules.crud_ops import CRUDOperations
from modules.scout_ops import ScoutOperations
from modules.ecommerce.product_manager import ProductManager
from modules.ecommerce.strategy_mentor import StrategyMentor
from modules.ecommerce.competitor_scout import CompetitorScout
from modules.ecommerce.knowledge_base import KnowledgeBase

console = Console(force_terminal=True, legacy_windows=False) if IS_WINDOWS else Console()


def get_symbol(name: str) -> str:
    """Get cross-platform symbol (emoji or ASCII)."""
    if IS_WINDOWS:
        symbols = {
            "check": "[OK]",
            "cross": "[X]",
            "robot": "[BOT]",
            "chart": "[CHART]",
            "doc": "[DOC]",
            "folder": "[DIR]",
            "warning": "[!]"
        }
    else:
        symbols = {
            "check": "✅",
            "cross": "❌",
            "robot": "🤖",
            "chart": "📊",
            "doc": "📄",
            "folder": "📁",
            "warning": "⚠️"
        }
    return symbols.get(name, "[*]" if IS_WINDOWS else "•")


def initialize_codexa(working_dir: str = None) -> HOPOrchestrator:
    """Initialize CODEXA orchestrator and register all modules."""
    if working_dir is None:
        working_dir = str(Path(__file__).parent)

    # Create orchestrator
    orchestrator = HOPOrchestrator(working_dir)

    # Register core modules
    crud_module = CRUDOperations(working_dir)
    scout_module = ScoutOperations(working_dir)

    orchestrator.register_module(crud_module)
    orchestrator.register_module(scout_module)

    # Register e-commerce modules
    product_module = ProductManager(working_dir)
    strategy_module = StrategyMentor(working_dir)
    competitor_module = CompetitorScout(working_dir)
    knowledge_module = KnowledgeBase(working_dir)

    orchestrator.register_module(product_module)
    orchestrator.register_module(strategy_module)
    orchestrator.register_module(competitor_module)
    orchestrator.register_module(knowledge_module)

    return orchestrator


@click.group()
@click.pass_context
def cli(ctx):
    """
    CODEXA - HOP Meta-Agent CLI

    Create, Organize, Read, Update, Delete E-com X-Agent
    Unified interface for documentation and e-commerce operations.
    """
    ctx.ensure_object(dict)
    ctx.obj['orchestrator'] = initialize_codexa()


# ==================== CRUD COMMANDS ====================

@cli.group()
def crud():
    """CRUD operations for documentation and data."""
    pass


@crud.command()
@click.argument('path')
@click.option('--content', help='File content')
@click.option('--type', 'data_type', default='document', help='Data type (document, json_data, etc.)')
@click.pass_context
def create(ctx, path, content, data_type):
    """Create a new document or data entry."""
    orchestrator = ctx.obj['orchestrator']

    result = orchestrator.route_operation(
        'crud',
        'create',
        path=path,
        content=content,
        data_type=data_type
    )

    if result['success']:
        console.print(Panel(f"[green]{get_symbol('check')} Created: {path}[/green]", border_style="green"))
    else:
        console.print(Panel(f"[red]{get_symbol('cross')} Error: {result['error']}[/red]", border_style="red"))


@crud.command()
@click.argument('path')
@click.option('--type', 'data_type', default='document', help='Data type')
@click.pass_context
def read(ctx, path, data_type):
    """Read a document or data entry."""
    orchestrator = ctx.obj['orchestrator']

    result = orchestrator.route_operation(
        'crud',
        'read',
        path=path,
        data_type=data_type
    )

    if result['success']:
        console.print(Panel(f"[cyan]{get_symbol('doc')} {path}[/cyan]", border_style="cyan"))

        if 'content' in result:
            syntax = Syntax(result['content'][:500], "markdown", theme="monokai")
            console.print(syntax)
        elif 'data' in result:
            console.print(json.dumps(result['data'], indent=2))
    else:
        console.print(Panel(f"[red]{get_symbol('cross')} Error: {result['error']}[/red]", border_style="red"))


@crud.command()
@click.option('--type', 'data_type', help='Filter by data type')
@click.option('--pattern', default='*', help='Glob pattern')
@click.pass_context
def list(ctx, data_type, pattern):
    """List all items."""
    orchestrator = ctx.obj['orchestrator']

    result = orchestrator.route_operation(
        'crud',
        'list',
        data_type=data_type,
        pattern=pattern
    )

    if result['success']:
        console.print(f"\n[cyan]Found {result['count']} items[/cyan]\n")
        for item in result['items'][:10]:  # Show first 10
            console.print(f"  • {item}")

        if result['count'] > 10:
            console.print(f"\n... and {result['count'] - 10} more")
    else:
        console.print(Panel(f"[red]{get_symbol('cross')} Error: {result['error']}[/red]", border_style="red"))


# ==================== SCOUT COMMANDS ====================

@cli.group()
def scout():
    """Scout operations for repository navigation."""
    pass


@scout.command()
@click.option('--target', default='.', help='Target directory')
@click.option('--cache/--no-cache', default=True, help='Use cache')
@click.pass_context
def scan(ctx, target, cache):
    """Scan repository and build structure map."""
    orchestrator = ctx.obj['orchestrator']

    # Skip spinner on Windows to avoid encoding issues
    if IS_WINDOWS:
        console.print("[yellow]Scanning repository...[/yellow]")
        result = orchestrator.route_operation(
            'scout',
            'scan',
            target=target,
            use_cache=cache
        )
    else:
        with console.status("[yellow]Scanning repository...[/yellow]"):
            result = orchestrator.route_operation(
                'scout',
                'scan',
                target=target,
                use_cache=cache
            )

    if result['success']:
        stats = result['stats']

        table = Table(title=f"{get_symbol('chart')} Repository Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="white")

        table.add_row("Total Files", str(stats.get('total_files', 0)))
        table.add_row("Total Directories", str(stats.get('total_dirs', 0)))
        table.add_row("File Types", str(len(stats.get('file_types', {}))))
        table.add_row("Source", result['source'])

        console.print(table)
    else:
        console.print(Panel(f"[red]{get_symbol('cross')} Error: {result['error']}[/red]", border_style="red"))


@scout.command()
@click.option('--pattern', help='File pattern (e.g., *.py)')
@click.option('--extension', help='File extension (e.g., py)')
@click.pass_context
def find(ctx, pattern, extension):
    """Find files by pattern or extension."""
    orchestrator = ctx.obj['orchestrator']

    result = orchestrator.route_operation(
        'scout',
        'find',
        pattern=pattern,
        extension=extension
    )

    if result['success']:
        console.print(f"\n[cyan]Found {result['count']} files[/cyan]\n")
        for match in result['matches'][:15]:
            console.print(f"  • {match}")

        if result['count'] > 15:
            console.print(f"\n... and {result['count'] - 15} more")
    else:
        console.print(Panel(f"[red]{get_symbol('cross')} Error: {result['error']}[/red]", border_style="red"))


@scout.command()
@click.pass_context
def stats(ctx):
    """Get repository statistics."""
    orchestrator = ctx.obj['orchestrator']

    result = orchestrator.route_operation('scout', 'stats')

    if result['success']:
        console.print(Panel(
            f"[cyan]Repository Statistics[/cyan]\n\n"
            f"Files: {result['stats'].get('total_files', 0)}\n"
            f"Directories: {result['stats'].get('total_dirs', 0)}\n"
            f"Annotations: {result.get('annotations_count', 0)}",
            border_style="cyan"
        ))
    else:
        console.print(Panel(f"[red]{get_symbol('cross')} Error: {result['error']}[/red]", border_style="red"))


# ==================== E-COMMERCE COMMANDS ====================

@cli.group()
def ecom():
    """E-commerce operations."""
    pass


@ecom.group()
def products():
    """Product management."""
    pass


@products.command('list')
@click.option('--category', help='Filter by category')
@click.pass_context
def list_products(ctx, category):
    """List all products."""
    orchestrator = ctx.obj['orchestrator']

    result = orchestrator.route_operation(
        'product_manager',
        'list',
        category=category
    )

    if result['success']:
        console.print(f"\n[cyan]Found {result['count']} products[/cyan]\n")

        for product in result['products'][:5]:
            console.print(f"  • [{product['id']}] {product['name']} - ${product['price']}")

        if result['count'] > 5:
            console.print(f"\n... and {result['count'] - 5} more")
    else:
        console.print(Panel(f"[red]{get_symbol('cross')} Error: {result['error']}[/red]", border_style="red"))


# ==================== README COMMANDS ====================

@cli.group()
def readme():
    """README management."""
    pass


@readme.command()
@click.pass_context
def update(ctx):
    """Update README with current capabilities."""
    orchestrator = ctx.obj['orchestrator']

    # Skip spinner on Windows to avoid encoding issues
    if IS_WINDOWS:
        console.print("[yellow]Updating README...[/yellow]")
        success = orchestrator.update_readme()
    else:
        with console.status("[yellow]Updating README...[/yellow]"):
            success = orchestrator.update_readme()

    if success:
        console.print(Panel(
            f"[green]{get_symbol('check')} README updated successfully![/green]\n\n"
            f"Location: {orchestrator.readme_path}\n"
            f"Modules documented: {len(orchestrator.modules)}",
            border_style="green"
        ))
    else:
        console.print(Panel(f"[red]{get_symbol('cross')} Failed to update README[/red]", border_style="red"))


# ==================== STATUS COMMAND ====================

@cli.command()
@click.pass_context
def status(ctx):
    """Show CODEXA system status."""
    orchestrator = ctx.obj['orchestrator']

    status_info = orchestrator.get_status()

    table = Table(title=f"{get_symbol('robot')} CODEXA System Status")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="white")

    table.add_row("Working Directory", str(status_info['working_dir']))
    table.add_row("Modules Registered", str(status_info['modules_registered']))
    table.add_row("README Exists", get_symbol('check') if status_info['readme_exists'] else get_symbol('cross'))
    table.add_row("Git Repository", get_symbol('check') if status_info['git_repo'] else get_symbol('cross'))
    table.add_row("Git Branch", status_info['git_branch'] or "N/A")

    console.print(table)

    console.print("\n[cyan]Registered Modules:[/cyan]")
    for module_name in status_info['modules']:
        console.print(f"  • {module_name}")


if __name__ == '__main__':
    cli()
