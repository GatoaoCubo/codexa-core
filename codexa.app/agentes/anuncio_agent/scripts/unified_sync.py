#!/usr/bin/env python3
"""
UNIFIED SYNC - Full bidirectional sync Shopify <-> Supabase

Usage:
    python unified_sync.py pull          # Shopify -> Supabase (all fields)
    python unified_sync.py push          # Supabase -> Shopify (all fields)
    python unified_sync.py bidirectional # Smart sync (newer wins)
    python unified_sync.py single <id>   # Sync single product

Options:
    --scope=all|inventory|content|price  # What to sync (default: all)
    --dry-run                            # Preview without applying
    --force                              # Ignore timestamps, always push

Examples:
    python unified_sync.py pull --scope=inventory
    python unified_sync.py push --scope=content
    python unified_sync.py bidirectional --dry-run
    python unified_sync.py single abc123 --force

Config: codexa-core/.env
"""

import json
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from pathlib import Path

# Add codexa.app to path for config imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from config.env_loader import supabase


def call_unified_sync(mode: str, scope: str = "all", product_id: str = None,
                      dry_run: bool = False, force: bool = False):
    """Call the unified-sync Edge Function."""
    api_url = f"{supabase.url}/functions/v1/unified-sync"

    headers = {
        "Authorization": f"Bearer {supabase.service_role_key}",
        "Content-Type": "application/json",
    }

    body = {
        "mode": mode,
        "scope": scope,
        "dryRun": dry_run,
        "force": force,
    }

    if product_id:
        body["productId"] = product_id

    try:
        req = Request(api_url, data=json.dumps(body).encode("utf-8"),
                     headers=headers, method="POST")
        with urlopen(req, timeout=300) as response:  # 5 min timeout
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        error_body = e.read().decode("utf-8")
        return {"success": False, "error": f"HTTP {e.code}: {error_body}"}
    except URLError as e:
        return {"success": False, "error": str(e.reason)}


def print_result(result: dict):
    """Pretty print sync results."""
    print("\n" + "=" * 70)

    if not result.get("success", False):
        print(f"ERROR: {result.get('error', 'Unknown error')}")
        return

    stats = result.get("stats", {})
    print(f"MODE: {result.get('mode', 'unknown').upper()}")
    print(f"SCOPE: {result.get('scope', 'all')}")
    print(f"DURATION: {result.get('duration_ms', 0)}ms")
    print("-" * 70)
    print(f"TOTAL:    {stats.get('total', 0)}")
    print(f"SYNCED:   {stats.get('synced', 0)} ({stats.get('created', 0)} created, {stats.get('updated', 0)} updated)")
    print(f"SKIPPED:  {stats.get('skipped', 0)}")
    print(f"ERRORS:   {stats.get('errors', 0)}")
    print("=" * 70)

    # Print product details
    products = result.get("products", [])
    if products:
        print("\nPRODUCTS:")
        for p in products:
            icon = {
                "created": "+",
                "updated": "~",
                "skipped": "-",
                "error": "!",
            }.get(p.get("action"), "?")

            name = p.get("name", "Unknown")[:40]
            action = p.get("action", "unknown")
            direction = p.get("direction", "none")

            line = f"  [{icon}] {name:42s} {action:10s} ({direction})"

            if p.get("error"):
                line += f" ERROR: {p['error'][:30]}"
            elif p.get("changes"):
                changes = list(p["changes"].keys())[:3]
                line += f" changes: {', '.join(changes)}"

            print(line)

    print()


def main():
    args = sys.argv[1:]

    if not args or args[0] in ["-h", "--help"]:
        print(__doc__)
        return

    mode = args[0]

    if mode not in ["pull", "push", "bidirectional", "single"]:
        print(f"Invalid mode: {mode}")
        print("Valid modes: pull, push, bidirectional, single")
        return

    # Parse options
    scope = "all"
    product_id = None
    dry_run = False
    force = False

    for arg in args[1:]:
        if arg.startswith("--scope="):
            scope = arg.split("=")[1]
        elif arg == "--dry-run":
            dry_run = True
        elif arg == "--force":
            force = True
        elif mode == "single" and not product_id:
            product_id = arg

    if mode == "single" and not product_id:
        print("Error: product ID required for single mode")
        print("Usage: python unified_sync.py single <product-id>")
        return

    # Validate
    if not supabase.service_role_key:
        print("ERROR: SUPABASE_SERVICE_ROLE_KEY not configured")
        return

    # Execute
    print("=" * 70)
    print("UNIFIED SYNC")
    print(f"Mode: {mode} | Scope: {scope}")
    print(f"Dry Run: {dry_run} | Force: {force}")
    if product_id:
        print(f"Product ID: {product_id}")
    print("=" * 70)
    print("\nExecuting... (this may take a few minutes)")

    result = call_unified_sync(
        mode=mode,
        scope=scope,
        product_id=product_id,
        dry_run=dry_run,
        force=force
    )

    print_result(result)


if __name__ == "__main__":
    main()
