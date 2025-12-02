#!/usr/bin/env python3
"""
Reforma completa de produto - anuncio_agent automation.
Analisa, corrige e atualiza produto no Supabase.

Usage: python scripts/reform_product.py <product_id> [--dry-run]
"""

import os
import sys
import json
import re
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

SUPABASE_URL = "https://fuuguegkqnpzrrhwymgw.supabase.co"
ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ1dWd1ZWdrcW5wenJyaHd5bWd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTc1MTUwMzIsImV4cCI6MjA3MzA5MTAzMn0.Hvc-uw7p6h2Iss5O893yAxBzUBdZbGjQyt9g5CPoO7A"

# Conectores proibidos em titulos (regra anuncio_agent)
FORBIDDEN_CONNECTORS = ["de", "para", "com", "e", "ou", "em", "a", "o", "as", "os", "do", "da", "dos", "das", "pelo", "pela"]


@dataclass
class ProductAnalysis:
    """Analise de problemas do produto."""
    product_id: str
    name: str
    issues: list
    severity: str  # low, medium, high, critical
    recommendations: list


@dataclass
class ProductReform:
    """Dados reformados do produto."""
    name: str
    tagline: str
    description: str
    seo_title: str
    seo_description: str
    seo_keywords: list


def fetch_product(product_id: str) -> dict:
    """Busca produto completo por ID."""
    api_url = f"{SUPABASE_URL}/rest/v1/products?id=eq.{product_id}&select=*"
    headers = {
        "apikey": ANON_KEY,
        "Authorization": f"Bearer {ANON_KEY}",
        "Content-Type": "application/json",
    }
    try:
        req = Request(api_url, headers=headers, method="GET")
        with urlopen(req, timeout=30) as response:
            products = json.loads(response.read().decode("utf-8"))
            return products[0] if products else {}
    except (HTTPError, URLError) as e:
        print(f"Erro ao buscar produto: {e}")
        return {}


def analyze_product(product: dict) -> ProductAnalysis:
    """Analisa produto e identifica problemas."""
    issues = []
    recommendations = []

    name = product.get("name", "")
    tagline = product.get("tagline", "")
    description = product.get("description", "")
    seo_title = product.get("seo_title", "")

    # 1. Verificar se name eh valido (nao pode ser frase/tagline)
    if len(name) > 70:
        issues.append("NAME_TOO_LONG: Nome excede 70 caracteres")
        recommendations.append("Encurtar nome para 58-60 chars com keywords")

    if name.endswith("."):
        issues.append("NAME_IS_TAGLINE: Nome termina com ponto (parece tagline)")
        recommendations.append("Substituir por nome de produto real")

    if name == tagline:
        issues.append("NAME_EQUALS_TAGLINE: Nome identico a tagline")
        recommendations.append("Diferenciar nome e tagline")

    # 2. Verificar conectores no nome
    name_words = name.lower().split()
    connectors_found = [w for w in name_words if w in FORBIDDEN_CONNECTORS]
    if len(connectors_found) > 2:
        issues.append(f"NAME_HAS_CONNECTORS: {len(connectors_found)} conectores encontrados")
        recommendations.append("Remover conectores para SEO (maximo 2)")

    # 3. Verificar SEO title
    if not seo_title:
        issues.append("NO_SEO_TITLE: Titulo SEO ausente")
        recommendations.append("Adicionar seo_title otimizado")
    elif len(seo_title) > 60:
        issues.append("SEO_TITLE_TOO_LONG: Titulo SEO > 60 chars")
        recommendations.append("Encurtar seo_title para 55-60 chars")

    # 4. Verificar description
    if len(description) > 300:
        issues.append("DESCRIPTION_TOO_LONG: Descricao curta muito longa")
        recommendations.append("Encurtar description para ~150 chars")

    # 5. Verificar keywords
    seo_keywords = product.get("seo_keywords", [])
    if len(seo_keywords) < 5:
        issues.append("FEW_KEYWORDS: Menos de 5 keywords SEO")
        recommendations.append("Adicionar mais keywords relevantes")

    # Determinar severidade
    critical_issues = [i for i in issues if "NAME_IS_TAGLINE" in i or "NAME_EQUALS_TAGLINE" in i]
    if critical_issues:
        severity = "critical"
    elif len(issues) >= 3:
        severity = "high"
    elif len(issues) >= 1:
        severity = "medium"
    else:
        severity = "low"

    return ProductAnalysis(
        product_id=product.get("id", ""),
        name=name,
        issues=issues,
        severity=severity,
        recommendations=recommendations
    )


def generate_reformed_name(product: dict) -> str:
    """Gera nome otimizado baseado nos dados do produto.

    Estrategia: Manter keywords do nome original, remover conectores em excesso,
    adicionar dimensao se ausente. Manter maximo de info util.
    """
    current_name = product.get("name", "")
    seo_title = product.get("seo_title", "")
    dimensions = product.get("dimensions", "")
    slug = product.get("slug", "")

    # Se nome atual termina com ponto (eh tagline), usar seo_title como base
    if current_name.endswith(".") or len(current_name) > 70:
        if seo_title and not seo_title.endswith("."):
            # Usar seo_title como base, que geralmente eh melhor
            base_name = seo_title
        else:
            # Construir do slug
            base_name = slug.replace("-", " ").title()
            # Adicionar tipo de produto
            if "caixa" in slug.lower() or "transporte" in slug.lower():
                base_name = "Caixa Transportadora Pet PP"
            elif "tapete" in slug.lower():
                base_name = "Tapete Refrescante Pet Gelado"
    else:
        base_name = current_name

    # Padronizar marca GATO3 (sem alterar "Gato" ou "Gatos" soltos)
    # Substitui apenas padroes de marca: "Gato ao Cubo", "Gato³", "GATO³"
    base_name = re.sub(r'Gato\s*ao\s*Cubo', 'GATO3', base_name, flags=re.IGNORECASE)
    base_name = re.sub(r'GATO[³]', 'GATO3', base_name)
    base_name = re.sub(r'\s+', ' ', base_name).strip()

    # Remover conectores em excesso (manter apenas 2)
    words = base_name.split()
    connector_count = 0
    cleaned_words = []
    for w in words:
        if w.lower() in FORBIDDEN_CONNECTORS:
            connector_count += 1
            if connector_count <= 2:
                cleaned_words.append(w)
            # Skip conectores alem do limite
        else:
            cleaned_words.append(w)

    base_name = " ".join(cleaned_words)

    # Adicionar dimensao se nao presente e disponivel
    if dimensions and not any(c.isdigit() for c in base_name):
        # Extrair dimensao principal
        dims_match = re.search(r'(\d+)\s*(?:cm|x|X)\s*(\d+)', dimensions)
        if dims_match:
            dim_str = f"{dims_match.group(1)}x{dims_match.group(2)}cm"
            if len(base_name) + len(dim_str) + 1 <= 60:
                base_name += f" {dim_str}"

    # Garantir que tem GATO3 no final se cabe
    if "GATO3" not in base_name and "GATO" not in base_name:
        if len(base_name) + 7 <= 60:
            base_name += " GATO3"

    # Truncar se necessario
    if len(base_name) > 60:
        base_name = base_name[:57].rsplit(' ', 1)[0] + "..."

    return base_name


def generate_reformed_tagline(product: dict, new_name: str) -> str:
    """Gera tagline baseada no produto."""
    # Usar why_it_works como base para tagline
    why_it_works = product.get("why_it_works", "")

    if why_it_works:
        # Primeira frase do why_it_works
        first_sentence = why_it_works.split(".")[0]
        if len(first_sentence) < 100:
            return first_sentence + "."

    # Fallback: criar tagline baseada nos beneficios
    benefits = product.get("benefits_emotional", [])
    if benefits:
        return benefits[0] if len(benefits[0]) < 100 else benefits[0][:97] + "..."

    # Ultimo fallback
    return f"O melhor {new_name.split()[0].lower()} para seu pet"


def generate_reformed_description(product: dict) -> str:
    """Gera descricao curta otimizada (~150 chars)."""
    description = product.get("description", "")
    long_description = product.get("long_description", "")

    # Se descricao atual esta boa, manter
    if 100 <= len(description) <= 200:
        return description

    # Tentar criar descricao do long_description
    if long_description:
        # Primeira frase significativa
        sentences = long_description.split(".")
        for s in sentences:
            if 80 <= len(s.strip()) <= 180:
                return s.strip() + "."

    # Encurtar descricao atual
    if description:
        if len(description) > 200:
            return description[:147] + "..."
        return description

    return ""


def generate_seo_title(product: dict, new_name: str) -> str:
    """Gera SEO title otimizado (55-60 chars)."""
    current_seo = product.get("seo_title", "")

    # Se atual esta bom, manter
    if current_seo and 50 <= len(current_seo) <= 60:
        return current_seo

    # Criar novo baseado no nome
    seo_title = new_name
    if "GATO3" not in seo_title and "GATO" not in seo_title:
        if len(seo_title) < 50:
            seo_title += " | GATO3"

    # Ajustar tamanho
    if len(seo_title) > 60:
        seo_title = seo_title[:57] + "..."

    return seo_title


def generate_seo_description(product: dict) -> str:
    """Gera SEO description otimizada (150-160 chars)."""
    current_seo = product.get("seo_description", "")

    # Se atual esta bom, manter
    if current_seo and 140 <= len(current_seo) <= 160:
        return current_seo

    # Criar novo
    description = product.get("description", "")
    if description:
        if len(description) <= 160:
            return description
        return description[:157] + "..."

    return current_seo


def reform_product(product: dict) -> ProductReform:
    """Gera dados reformados do produto."""
    new_name = generate_reformed_name(product)
    new_tagline = generate_reformed_tagline(product, new_name)
    new_description = generate_reformed_description(product)
    new_seo_title = generate_seo_title(product, new_name)
    new_seo_description = generate_seo_description(product)

    # Keywords - manter as atuais se boas
    current_keywords = product.get("seo_keywords", [])

    return ProductReform(
        name=new_name,
        tagline=new_tagline,
        description=new_description,
        seo_title=new_seo_title,
        seo_description=new_seo_description,
        seo_keywords=current_keywords
    )


def update_product(product_id: str, updates: dict, service_role_key: str) -> bool:
    """Atualiza produto no Supabase usando service_role_key."""
    api_url = f"{SUPABASE_URL}/rest/v1/products?id=eq.{product_id}"

    headers = {
        "apikey": service_role_key,
        "Authorization": f"Bearer {service_role_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    body = json.dumps(updates).encode("utf-8")

    try:
        req = Request(api_url, data=body, headers=headers, method="PATCH")
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            return len(result) > 0
    except HTTPError as e:
        print(f"Erro HTTP {e.code}: {e.reason}")
        error_body = e.read().decode("utf-8")
        print(f"Detalhes: {error_body}")
        return False
    except URLError as e:
        print(f"Erro de conexao: {e.reason}")
        return False


def print_analysis(analysis: ProductAnalysis):
    """Imprime analise formatada."""
    print("\n" + "=" * 60)
    print(f"ANALISE: {analysis.name[:50]}...")
    print("=" * 60)
    print(f"ID: {analysis.product_id}")
    print(f"Severidade: {analysis.severity.upper()}")
    print()

    if analysis.issues:
        print("PROBLEMAS ENCONTRADOS:")
        for i, issue in enumerate(analysis.issues, 1):
            print(f"  {i}. {issue}")
    else:
        print("Nenhum problema encontrado!")

    if analysis.recommendations:
        print("\nRECOMENDACOES:")
        for i, rec in enumerate(analysis.recommendations, 1):
            print(f"  {i}. {rec}")


def print_reform(product: dict, reform: ProductReform):
    """Imprime comparacao antes/depois."""
    print("\n" + "-" * 60)
    print("REFORMA PROPOSTA")
    print("-" * 60)

    print("\n[NAME]")
    print(f"  ANTES: {product.get('name', '')[:60]}")
    print(f"  DEPOIS: {reform.name}")

    print("\n[TAGLINE]")
    print(f"  ANTES: {product.get('tagline', '')[:60]}")
    print(f"  DEPOIS: {reform.tagline[:60]}...")

    print("\n[SEO_TITLE]")
    print(f"  ANTES: {product.get('seo_title', '')}")
    print(f"  DEPOIS: {reform.seo_title}")

    print("\n[DESCRIPTION]")
    print(f"  ANTES: {product.get('description', '')[:80]}...")
    print(f"  DEPOIS: {reform.description[:80]}...")


def main():
    dry_run = "--dry-run" in sys.argv

    # Pegar product_id dos argumentos
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print("Usage: python reform_product.py <product_id> [--dry-run]")
        print("\nExemplo: python reform_product.py ed1f6428-2f1c-4d24-a72f-10456c313733")
        sys.exit(1)

    product_id = args[0]

    print(f"\nBuscando produto: {product_id}")
    product = fetch_product(product_id)

    if not product:
        print("Produto nao encontrado!")
        sys.exit(1)

    # Analisar
    analysis = analyze_product(product)
    print_analysis(analysis)

    if analysis.severity == "low":
        print("\nProduto OK - nenhuma reforma necessaria")
        return

    # Reformar
    reform = reform_product(product)
    print_reform(product, reform)

    if dry_run:
        print("\n[DRY RUN] Nenhuma alteracao aplicada")
        return

    # Verificar service_role_key
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    if not service_key or "COLE" in service_key:
        print("\n" + "!" * 60)
        print("ATENCAO: Para aplicar as mudancas, configure SUPABASE_SERVICE_ROLE_KEY")
        print("!" * 60)

        # Salvar reforma proposta em arquivo
        output = {
            "product_id": product_id,
            "analysis": {
                "issues": analysis.issues,
                "severity": analysis.severity,
                "recommendations": analysis.recommendations
            },
            "reform": {
                "name": reform.name,
                "tagline": reform.tagline,
                "description": reform.description,
                "seo_title": reform.seo_title,
                "seo_description": reform.seo_description
            }
        }
        output_file = Path(__file__).parent / f"reform_{product_id[:8]}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\nReforma salva em: {output_file}")
        return

    # Aplicar reforma
    print("\nAplicando reforma...")
    updates = {
        "name": reform.name,
        "tagline": reform.tagline,
        "seo_title": reform.seo_title,
    }

    success = update_product(product_id, updates, service_key)

    if success:
        print("Reforma aplicada com sucesso!")
    else:
        print("Erro ao aplicar reforma")


if __name__ == "__main__":
    main()
