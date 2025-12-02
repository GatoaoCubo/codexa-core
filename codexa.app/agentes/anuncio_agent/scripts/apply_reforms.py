#!/usr/bin/env python3
"""
Aplica reformas em batch nos produtos do Supabase.
Usage: python scripts/apply_reforms.py [--dry-run]

Requer: SUPABASE_SERVICE_ROLE_KEY no ambiente ou .env
"""

import os
import sys
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from pathlib import Path
from datetime import datetime


SUPABASE_URL = "https://fuuguegkqnpzrrhwymgw.supabase.co"


def load_env():
    """Carrega variaveis do .env"""
    env_paths = [
        Path(__file__).parent.parent.parent.parent / ".env",
        Path(__file__).parent.parent.parent.parent.parent / ".env",
        Path.home() / ".env",
    ]
    for env_path in env_paths:
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        os.environ.setdefault(key.strip(), value.strip())


def update_product(product_id: str, updates: dict, service_key: str) -> tuple:
    """Atualiza produto no Supabase."""
    api_url = f"{SUPABASE_URL}/rest/v1/products?id=eq.{product_id}"

    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    body = json.dumps(updates).encode("utf-8")

    try:
        req = Request(api_url, data=body, headers=headers, method="PATCH")
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            return True, result
    except HTTPError as e:
        error_body = e.read().decode("utf-8")
        return False, {"code": e.code, "error": error_body}
    except URLError as e:
        return False, {"error": str(e.reason)}


def main():
    load_env()
    dry_run = "--dry-run" in sys.argv

    # Verificar service_role_key
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    if not service_key or "COLE" in service_key:
        print("=" * 60)
        print("ERRO: SUPABASE_SERVICE_ROLE_KEY nao configurada!")
        print()
        print("Configure a chave de uma das formas:")
        print("1. Variavel de ambiente: export SUPABASE_SERVICE_ROLE_KEY='eyJ...'")
        print("2. Arquivo .env: SUPABASE_SERVICE_ROLE_KEY=eyJ...")
        print()
        print("Obtenha em: https://supabase.com/dashboard/project/fuuguegkqnpzrrhwymgw/settings/api")
        print("=" * 60)
        sys.exit(1)

    # Carregar relatorio de analise
    report_file = Path(__file__).parent / "analysis_report.json"
    if not report_file.exists():
        print("Erro: Execute primeiro python scripts/analyze_all.py")
        sys.exit(1)

    with open(report_file, "r", encoding="utf-8") as f:
        report = json.load(f)

    reforms = report.get("reforms", [])
    if not reforms:
        print("Nenhuma reforma pendente.")
        return

    print("=" * 70)
    print(f"APLICANDO REFORMAS - {len(reforms)} produtos")
    print("=" * 70)

    if dry_run:
        print("[DRY RUN] Nenhuma alteracao sera aplicada\n")

    results = {"success": 0, "failed": 0, "skipped": 0}
    log = []

    for i, reform in enumerate(reforms, 1):
        pid = reform["id"]
        name = reform["name"]
        severity = reform["severity"]

        print(f"\n[{i:02d}/{len(reforms)}] {name} ({severity.upper()})")

        # Montar updates
        updates = {}

        # Apenas atualizar campos que realmente mudaram
        current = reform["current"]
        proposed = reform["proposed"]

        if current["name"] != proposed["name"]:
            updates["name"] = proposed["name"]
            print(f"  name: {current['name'][:40]}... -> {proposed['name'][:40]}...")

        if current.get("tagline") != proposed.get("tagline"):
            # So atualizar tagline se atual for None ou igual ao name
            if current.get("tagline") is None or current.get("tagline") == current.get("name"):
                updates["tagline"] = proposed["tagline"]
                print(f"  tagline: (atualizado)")

        if current.get("seo_title") != proposed.get("seo_title"):
            updates["seo_title"] = proposed["seo_title"]
            print(f"  seo_title: (atualizado)")

        if not updates:
            print("  Nenhuma alteracao necessaria")
            results["skipped"] += 1
            continue

        if dry_run:
            print("  [DRY RUN] Alteracoes nao aplicadas")
            results["skipped"] += 1
            continue

        # Aplicar
        success, response = update_product(pid, updates, service_key)

        if success:
            print("  OK - Aplicado com sucesso")
            results["success"] += 1
            log.append({
                "id": pid,
                "name": name,
                "status": "success",
                "updates": updates,
                "timestamp": datetime.now().isoformat()
            })
        else:
            print(f"  ERRO - {response}")
            results["failed"] += 1
            log.append({
                "id": pid,
                "name": name,
                "status": "failed",
                "error": response,
                "timestamp": datetime.now().isoformat()
            })

    # Resumo
    print("\n" + "=" * 70)
    print("RESUMO")
    print("=" * 70)
    print(f"Sucesso:  {results['success']}")
    print(f"Falhas:   {results['failed']}")
    print(f"Pulados:  {results['skipped']}")

    # Salvar log
    log_file = Path(__file__).parent / f"reform_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump({
            "summary": results,
            "dry_run": dry_run,
            "log": log
        }, f, indent=2, ensure_ascii=False)
    print(f"\nLog salvo: {log_file}")


if __name__ == "__main__":
    main()
