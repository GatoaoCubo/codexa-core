#!/usr/bin/env python3
"""
Atualiza estoque de todos os produtos.
Usage: python scripts/update_stock.py <quantidade>
"""

import os
import sys
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from pathlib import Path


SUPABASE_URL = "https://fuuguegkqnpzrrhwymgw.supabase.co"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ1dWd1ZWdrcW5wenJyaHd5bWd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc1MTUwMzIsImV4cCI6MjA3MzA5MTAzMn0.Hvc-uw7p6h2Iss5O893yAxBzUBdZbGjQyt9g5CPoO7A"


def load_env():
    env_path = Path(__file__).parent.parent.parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())


def get_all_product_ids():
    """Busca IDs de todos os produtos."""
    api_url = f"{SUPABASE_URL}/rest/v1/products?select=id,name,quantity"
    headers = {
        "apikey": ANON_KEY,
        "Authorization": f"Bearer {ANON_KEY}",
    }
    req = Request(api_url, headers=headers)
    with urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def update_stock(product_id: str, quantity: int, service_key: str):
    """Atualiza estoque de um produto."""
    api_url = f"{SUPABASE_URL}/rest/v1/products?id=eq.{product_id}"
    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    body = json.dumps({"quantity": quantity}).encode("utf-8")
    req = Request(api_url, data=body, headers=headers, method="PATCH")
    try:
        with urlopen(req, timeout=30) as response:
            return True, json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        return False, e.read().decode("utf-8")


def main():
    load_env()

    quantity = int(sys.argv[1]) if len(sys.argv) > 1 else 23

    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    if not service_key:
        print("ERRO: SUPABASE_SERVICE_ROLE_KEY nao configurada")
        sys.exit(1)

    print(f"Atualizando estoque de todos os produtos para {quantity}...")

    products = get_all_product_ids()
    success = 0
    failed = 0

    for p in products:
        pid = p["id"]
        name = p["name"][:40]
        old_qty = p.get("quantity", 0)

        ok, _ = update_stock(pid, quantity, service_key)

        if ok:
            print(f"  OK: {name}... ({old_qty} -> {quantity})")
            success += 1
        else:
            print(f"  ERRO: {name}...")
            failed += 1

    print(f"\nResultado: {success} atualizados, {failed} falhas")


if __name__ == "__main__":
    main()
