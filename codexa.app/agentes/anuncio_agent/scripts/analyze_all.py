#!/usr/bin/env python3
"""
Analisa todos os produtos e gera relatorio.
Usage: python scripts/analyze_all.py
"""

import json
from pathlib import Path
from reform_product import fetch_product, analyze_product, reform_product

# IDs dos 22 produtos
PRODUCTS = [
    ("bd629e95-f695-4be3-8b5b-4241ab852c4e", "Tapete 65x50"),
    ("33f19248-49ee-4cc8-b9c8-17052ee0889a", "Tapete 50x90"),
    ("72f6c8e3-615f-4eaa-9f8c-aefabc8dfdb4", "Tapete 40x50"),
    ("2354fdee-3f9d-4a8a-abbd-8d725a94876a", "Portao Retratil 2"),
    ("ed1f6428-2f1c-4d24-a72f-10456c313733", "Caixa Transporte PP"),
    ("44ad323b-e1c5-4009-a1aa-b8ef4e644164", "Guia Passeio"),
    ("aa91cfe0-de40-433c-a42d-1396b2a98399", "Bola Frisbee"),
    ("ad11178b-ead7-491a-8981-62f93bd7ad22", "Escova Catnip"),
    ("6b7f62d0-7f78-4b68-a18b-e32e90710eb0", "Laser Pet"),
    ("205dfb4a-e6b7-4dee-8615-beba911ef920", "Assento Carro"),
    ("01dd38d3-5607-4d1b-8b8c-c62965a1fa1b", "Arranhador"),
    ("19f5b892-1fb3-4389-84f8-486f14ee1ead", "Caixa Transporte R"),
    ("c55f2f6c-8e81-4374-a498-cb70fdc72572", "Tapete Gelado"),
    ("02a81a77-8dfd-470e-bd1d-ef108adcc849", "Corda Catnip"),
    ("30bbe2ff-9157-42c8-b932-c6b327349db1", "Portao Retratil"),
    ("e2a93ae8-55c4-409a-9515-d5c3d3962b83", "Mochila Astronauta"),
    ("62449357-e638-4d25-8ba2-3df4922ad957", "Cama Janela"),
    ("a98f4ccd-8910-4d59-a405-fcba001a58fb", "Varinha Ventosa"),
    ("52ae57ec-b816-47d9-82db-49c5f5227991", "Rolo Tira Pelos"),
    ("3b08f364-fc8f-4f9b-97be-736326ecd5c6", "Pote Retratil"),
    ("e7b800dc-7d43-4139-b110-06bebf05a136", "Bola Inteligente"),
    ("495d92ad-b773-41ab-904b-7c2e6c7e861b", "Corda Pilha"),
]


def main():
    print("=" * 80)
    print("ANALISE COMPLETA - 22 PRODUTOS GATO3")
    print("=" * 80)

    results = {
        "critical": [],
        "high": [],
        "medium": [],
        "low": []
    }

    reforms = []

    for i, (pid, short_name) in enumerate(PRODUCTS, 1):
        print(f"\n[{i:02d}/22] Analisando: {short_name}...", end=" ")

        product = fetch_product(pid)
        if not product:
            print("ERRO - nao encontrado")
            continue

        analysis = analyze_product(product)
        results[analysis.severity].append({
            "id": pid,
            "name": short_name,
            "current_name": product.get("name", "")[:50],
            "issues": analysis.issues,
            "recommendations": analysis.recommendations
        })

        print(f"{analysis.severity.upper()} ({len(analysis.issues)} issues)")

        # Gerar reforma se necessario
        if analysis.severity != "low":
            reform = reform_product(product)
            reforms.append({
                "id": pid,
                "name": short_name,
                "severity": analysis.severity,
                "current": {
                    "name": product.get("name", ""),
                    "tagline": product.get("tagline", ""),
                    "seo_title": product.get("seo_title", "")
                },
                "proposed": {
                    "name": reform.name,
                    "tagline": reform.tagline,
                    "seo_title": reform.seo_title
                }
            })

    # Resumo
    print("\n" + "=" * 80)
    print("RESUMO")
    print("=" * 80)
    print(f"CRITICAL: {len(results['critical'])} produtos")
    print(f"HIGH:     {len(results['high'])} produtos")
    print(f"MEDIUM:   {len(results['medium'])} produtos")
    print(f"LOW (OK): {len(results['low'])} produtos")

    # Detalhar problemas criticos
    if results["critical"]:
        print("\n" + "-" * 80)
        print("PRODUTOS CRITICOS (precisam correcao urgente)")
        print("-" * 80)
        for p in results["critical"]:
            print(f"\n  {p['name']}:")
            print(f"    Nome atual: {p['current_name']}...")
            for issue in p["issues"]:
                print(f"    - {issue}")

    # Salvar relatorio
    report = {
        "summary": {
            "critical": len(results["critical"]),
            "high": len(results["high"]),
            "medium": len(results["medium"]),
            "low": len(results["low"]),
            "total_need_reform": len(reforms)
        },
        "details": results,
        "reforms": reforms
    }

    output_file = Path(__file__).parent / "analysis_report.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\nRelatorio salvo: {output_file}")

    # Resumo de reformas
    print("\n" + "=" * 80)
    print(f"REFORMAS PROPOSTAS: {len(reforms)} produtos")
    print("=" * 80)

    for r in reforms:
        print(f"\n[{r['severity'].upper()}] {r['name']}")
        print(f"  ANTES: {r['current']['name'][:55]}...")
        print(f"  DEPOIS: {r['proposed']['name']}")


if __name__ == "__main__":
    main()
