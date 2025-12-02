#!/usr/bin/env python3
"""
Lista produtos do Supabase GATO3.
Usage: python scripts/list_products.py
"""

import os
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from pathlib import Path


def load_env():
    """Carrega variáveis do .env"""
    env_path = Path(__file__).parent.parent.parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ.setdefault(key.strip(), value.strip())


def list_products():
    """Lista todos os produtos do Supabase."""
    load_env()

    url = "https://fuuguegkqnpzrrhwymgw.supabase.co"
    # Anon key permite leitura de produtos (RLS configurado)
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ1dWd1ZWdrcW5wenJyaHd5bWd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc1MTUwMzIsImV4cCI6MjA3MzA5MTAzMn0.Hvc-uw7p6h2Iss5O893yAxBzUBdZbGjQyt9g5CPoO7A"

    # REST API para tabela products
    api_url = f"{url}/rest/v1/products?select=id,name,slug,price,status,created_at&order=created_at.desc"

    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    try:
        req = Request(api_url, headers=headers, method="GET")
        with urlopen(req, timeout=30) as response:
            products = json.loads(response.read().decode("utf-8"))
            return products
    except HTTPError as e:
        print(f"Erro HTTP {e.code}: {e.reason}")
        error_body = e.read().decode("utf-8")
        print(f"Detalhes: {error_body}")
        return []
    except URLError as e:
        print(f"Erro de conexão: {e.reason}")
        return []


def main():
    """Exibe lista formatada de produtos."""
    print("\n=== PRODUTOS GATO3 - Supabase ===\n")
    print("-" * 80)

    products = list_products()

    if not products:
        return

    print(f"{'#':<3} {'Nome':<40} {'Preço':>10} {'Status':<12} {'ID (UUID)'}")
    print("-" * 80)

    for i, p in enumerate(products, 1):
        name = p.get("name", "Sem nome")[:38]
        price = p.get("price", 0)
        status = p.get("status", "draft")
        pid = p.get("id", "")[:8] + "..."

        print(f"{i:<3} {name:<40} R${price:>8.2f} {status:<12} {pid}")

    print("-" * 80)
    print(f"Total: {len(products)} produtos\n")

    # Salvar JSON completo
    output_file = Path(__file__).parent / "products_cache.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)
    print(f"Cache salvo em: {output_file}")


if __name__ == "__main__":
    main()
