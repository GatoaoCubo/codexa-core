#!/usr/bin/env python3
"""
Busca dados completos de um produto do Supabase.
Usage: python scripts/fetch_product.py <product_id>

Configuracao centralizada em: codexa-core/.env
"""

import sys
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# Add codexa.app to path for config imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from config.env_loader import supabase


def fetch_product(product_id: str) -> dict:
    """Busca produto completo por ID."""
    if not supabase.is_configured:
        print("ERRO: Supabase nao configurado no .env")
        return {}

    api_url = f"{supabase.url}/rest/v1/products?id=eq.{product_id}&select=*"
    headers = supabase.get_headers(admin=False)

    try:
        req = Request(api_url, headers=headers, method="GET")
        with urlopen(req, timeout=30) as response:
            products = json.loads(response.read().decode("utf-8"))
            return products[0] if products else {}
    except HTTPError as e:
        print(f"Erro HTTP {e.code}: {e.reason}")
        return {}
    except URLError as e:
        print(f"Erro de conexao: {e.reason}")
        return {}


def main():
    if len(sys.argv) < 2:
        # Busca primeiro produto como exemplo
        product_id = "ed1f6428-2f1c-4d24-a72f-10456c313733"  # Produto #5
    else:
        product_id = sys.argv[1]

    print(f"Buscando produto: {product_id}\n")
    product = fetch_product(product_id)

    if product:
        print(json.dumps(product, indent=2, ensure_ascii=False))

        # Salvar em arquivo
        output_file = f"scripts/product_{product_id[:8]}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(product, f, indent=2, ensure_ascii=False)
        print(f"\nSalvo em: {output_file}")
    else:
        print("Produto nao encontrado")


if __name__ == "__main__":
    main()
