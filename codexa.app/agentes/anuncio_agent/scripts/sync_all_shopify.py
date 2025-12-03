#!/usr/bin/env python3
"""
Sincroniza todos os produtos do Supabase com Shopify.
Usage: python scripts/sync_all_shopify.py

Configuracao centralizada em: codexa-core/.env
"""

import json
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from pathlib import Path

# Add codexa.app to path for config imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from config.env_loader import supabase


def get_all_products():
    """Busca todos os produtos."""
    api_url = f"{supabase.url}/rest/v1/products?select=id,name,shopify_product_id&order=created_at.asc"
    headers = supabase.get_headers(admin=False)
    req = Request(api_url, headers=headers)
    with urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def sync_to_shopify(product_id: str, service_key: str):
    """Chama Edge Function sync-shopify-product."""
    api_url = f"{supabase.url}/functions/v1/sync-shopify-product"
    headers = {
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
    }
    body = json.dumps({"productId": product_id}).encode("utf-8")

    try:
        req = Request(api_url, data=body, headers=headers, method="POST")
        with urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
            return True, result
    except HTTPError as e:
        error_body = e.read().decode("utf-8")
        return False, {"code": e.code, "error": error_body}
    except URLError as e:
        return False, {"error": str(e.reason)}


def main():
    service_key = supabase.service_role_key
    if not service_key:
        print("ERRO: SUPABASE_SERVICE_ROLE_KEY nao configurada")
        return

    print("=" * 70)
    print("SINCRONIZANDO TODOS OS PRODUTOS COM SHOPIFY")
    print("=" * 70)

    products = get_all_products()
    print(f"\nTotal: {len(products)} produtos\n")

    success = 0
    failed = 0

    for i, p in enumerate(products, 1):
        pid = p["id"]
        name = p["name"][:45]
        shopify_id = p.get("shopify_product_id", "N/A")

        print(f"[{i:02d}/{len(products)}] {name}...")
        print(f"         Shopify ID: {shopify_id}")

        ok, result = sync_to_shopify(pid, service_key)

        if ok:
            print(f"         OK - Sincronizado!")
            success += 1
        else:
            print(f"         ERRO: {result}")
            failed += 1

        # Rate limiting - espera 1s entre requests
        if i < len(products):
            time.sleep(1)

    print("\n" + "=" * 70)
    print(f"RESULTADO: {success} sincronizados, {failed} falhas")
    print("=" * 70)


if __name__ == "__main__":
    main()
