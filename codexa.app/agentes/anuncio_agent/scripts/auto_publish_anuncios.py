"""
Auto-Publisher: Sincroniza anuncios gerados com Supabase + Shopify.

Este script fecha o gap entre:
  user_anuncios/*.md (anuncios gerados) → Supabase → Shopify → LP

Uso:
    python auto_publish_anuncios.py                    # Processa todos pendentes
    python auto_publish_anuncios.py --dry-run          # Simula sem alterar
    python auto_publish_anuncios.py --file arranhador  # Processa arquivo especifico

Requisitos:
    - SUPABASE_URL (env var ou default)
    - SUPABASE_SERVICE_ROLE_KEY (env var obrigatoria)
"""

import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# ============================================================================
# LOAD .ENV FILE
# ============================================================================

def load_dotenv():
    """Carrega variaveis de ambiente do .env mais proximo."""
    current = Path(__file__).parent if '__file__' in dir() else Path.cwd()

    # Procura .env subindo a arvore de diretorios
    for _ in range(5):
        env_file = current / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, val = line.split("=", 1)
                    key, val = key.strip(), val.strip()
                    if key and key not in os.environ:
                        os.environ[key] = val
            break
        current = current.parent

load_dotenv()


# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_DIR = Path(__file__).parent.parent if '__file__' in dir() else Path.cwd() / "codexa.app" / "agentes" / "anuncio_agent"
USER_ANUNCIOS_DIR = BASE_DIR / "user_anuncios"
PRODUCTS_CACHE = BASE_DIR / "scripts" / "products_cache.json"
PUBLISH_LOG = BASE_DIR / "scripts" / "publish_log.json"

SUPABASE_URL = os.getenv(
    "SUPABASE_URL",
    "https://fuuguegkqnpzrrhwymgw.supabase.co"
)
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
SUPABASE_ANON_KEY = os.getenv(
    "SUPABASE_ANON_KEY",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ1dWd1ZWdrcW5wenJyaHd5bWd3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjgxNjQ4NzIsImV4cCI6MjA0Mzc0MDg3Mn0.0e3x4rOUp8b3WYjkxEHNnvLwKbNrCcLxLNhJg2Lv1Qs"
)


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class AnuncioData:
    """Dados extraidos de um arquivo de anuncio .md"""
    filename: str
    titulo_a: str = ""
    titulo_b: str = ""
    titulo_c: str = ""
    descricao: str = ""
    bullets: list = field(default_factory=list)
    keywords: list = field(default_factory=list)
    preco: float = 0.0
    score: str = ""

    @property
    def best_title(self) -> str:
        """Retorna o melhor titulo (A preferencial)."""
        return self.titulo_a or self.titulo_b or self.titulo_c


@dataclass
class PublishResult:
    """Resultado de uma operacao de publicacao."""
    success: bool
    product_id: str
    anuncio_file: str
    message: str
    shopify_synced: bool = False
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


# ============================================================================
# MARKDOWN PARSER
# ============================================================================

def parse_anuncio_markdown(filepath: Path) -> Optional[AnuncioData]:
    """
    Extrai dados estruturados de um arquivo de anuncio .md

    Args:
        filepath: Caminho para o arquivo .md

    Returns:
        AnuncioData com dados extraidos ou None se falhar
    """
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[ERROR] Nao foi possivel ler {filepath}: {e}")
        return None

    data = AnuncioData(filename=filepath.name)

    # Extrair preco: **Preco**: R$ XX,XX
    preco_match = re.search(r'\*\*Preco\*\*:\s*R\$\s*([\d,\.]+)', content, re.IGNORECASE)
    if not preco_match:
        preco_match = re.search(r'\*\*Preço\*\*:\s*R\$\s*([\d,\.]+)', content, re.IGNORECASE)
    if preco_match:
        preco_str = preco_match.group(1).replace(",", ".")
        try:
            data.preco = float(preco_str)
        except ValueError:
            pass

    # Extrair score
    score_match = re.search(r'\*\*Score\*\*:\s*([\d\.\/]+)', content, re.IGNORECASE)
    if score_match:
        data.score = score_match.group(1)

    # Extrair titulos (- A: ..., - B: ..., - C: ...)
    titulo_a = re.search(r'-\s*A:\s*(.+?)(?:\n|$)', content)
    titulo_b = re.search(r'-\s*B:\s*(.+?)(?:\n|$)', content)
    titulo_c = re.search(r'-\s*C:\s*(.+?)(?:\n|$)', content)

    if titulo_a:
        data.titulo_a = titulo_a.group(1).strip().strip('"\'')
    if titulo_b:
        data.titulo_b = titulo_b.group(1).strip().strip('"\'')
    if titulo_c:
        data.titulo_c = titulo_c.group(1).strip().strip('"\'')

    # Extrair descricao (entre ## DESCRICAO e proximo ##)
    desc_match = re.search(
        r'##\s*DESCRI[CÇ][AÃ]O\s*\n(.*?)(?=\n##|\n---|\Z)',
        content,
        re.IGNORECASE | re.DOTALL
    )
    if desc_match:
        data.descricao = desc_match.group(1).strip()[:3500]  # Limit 3500 chars

    # Extrair bullets (1. ... 2. ... etc)
    bullets_section = re.search(
        r'##\s*BULLETS?\s*\n(.*?)(?=\n##|\n---|\Z)',
        content,
        re.IGNORECASE | re.DOTALL
    )
    if bullets_section:
        bullets_text = bullets_section.group(1)
        # Captura bullets numerados
        bullets = re.findall(r'\d+\.\s*(.+?)(?=\n\d+\.|\n##|\n---|\Z)', bullets_text, re.DOTALL)
        data.bullets = [b.strip()[:300] for b in bullets if b.strip()][:10]

    # Extrair keywords (se existir secao)
    keywords_section = re.search(
        r'##\s*KEYWORDS?\s*\n(.*?)(?=\n##|\n---|\Z)',
        content,
        re.IGNORECASE | re.DOTALL
    )
    if keywords_section:
        kw_text = keywords_section.group(1)
        # Extrai palavras separadas por virgula ou espaco
        keywords = re.findall(r'[\w\-]+', kw_text.lower())
        data.keywords = list(set(keywords))[:100]  # Max 100 keywords unicas

    return data


# ============================================================================
# PRODUCT MATCHER
# ============================================================================

def load_products_cache() -> list[dict]:
    """Carrega cache de produtos do Supabase."""
    if not PRODUCTS_CACHE.exists():
        print(f"[WARNING] Cache nao encontrado: {PRODUCTS_CACHE}")
        return []

    try:
        return json.loads(PRODUCTS_CACHE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[ERROR] Erro ao carregar cache: {e}")
        return []


def match_anuncio_to_product(anuncio: AnuncioData, products: list[dict]) -> Optional[dict]:
    """
    Encontra o produto correspondente ao anuncio.

    Estrategia de matching:
    1. Match por preco exato
    2. Match por palavras do filename no nome do produto
    3. Match por similaridade de titulo
    """
    filename_lower = anuncio.filename.lower().replace("_", " ").replace(".md", "")

    # Extrai palavras-chave do filename
    filename_words = set(re.findall(r'\w+', filename_lower))
    filename_words.discard("md")

    best_match = None
    best_score = 0

    for product in products:
        product_name_lower = product.get("name", "").lower()
        product_words = set(re.findall(r'\w+', product_name_lower))

        # Score baseado em palavras em comum
        common_words = filename_words & product_words
        score = len(common_words)

        # Bonus se preco bate
        if anuncio.preco > 0 and abs(product.get("price", 0) - anuncio.preco) < 1.0:
            score += 5

        # Bonus se slug contem palavras do filename
        slug = product.get("slug", "").lower()
        for word in filename_words:
            if len(word) > 3 and word in slug:
                score += 2

        if score > best_score:
            best_score = score
            best_match = product

    # Requer minimo de 2 pontos para considerar match
    if best_score >= 2:
        return best_match

    return None


# ============================================================================
# SUPABASE UPDATER
# ============================================================================

def update_product_in_supabase(
    product_id: str,
    anuncio: AnuncioData,
    dry_run: bool = False
) -> bool:
    """
    Atualiza produto no Supabase com dados do anuncio.

    Args:
        product_id: UUID do produto
        anuncio: Dados do anuncio
        dry_run: Se True, apenas simula

    Returns:
        True se sucesso
    """
    if dry_run:
        print(f"  [DRY-RUN] Atualizaria produto {product_id[:8]}...")
        print(f"    - Titulo: {anuncio.best_title[:50]}...")
        print(f"    - Bullets: {len(anuncio.bullets)} items")
        print(f"    - Keywords: {len(anuncio.keywords)} items")
        return True

    if not SUPABASE_SERVICE_ROLE_KEY:
        print("[ERROR] SUPABASE_SERVICE_ROLE_KEY nao configurada")
        return False

    # Prepara dados para update (usando colunas existentes no Supabase)
    update_data = {
        "name": anuncio.best_title,
        "description": anuncio.descricao[:500] if anuncio.descricao else None,
        "long_description": anuncio.descricao,
        "seo_title": anuncio.best_title,
        "seo_description": anuncio.descricao[:160] if anuncio.descricao else None,
        "features": anuncio.bullets,  # bullets vao para features
        "seo_keywords": anuncio.keywords[:50] if anuncio.keywords else None,  # max 50
        "seo_long_tail_keywords": anuncio.keywords[50:100] if len(anuncio.keywords) > 50 else None,
        "updated_at": datetime.now().isoformat(),
    }

    # Remove campos None
    update_data = {k: v for k, v in update_data.items() if v is not None}

    # Faz request para Supabase REST API
    url = f"{SUPABASE_URL}/rest/v1/products?id=eq.{product_id}"

    headers = {
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "apikey": SUPABASE_SERVICE_ROLE_KEY,
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }

    body = json.dumps(update_data).encode("utf-8")

    try:
        req = Request(url, data=body, headers=headers, method="PATCH")
        with urlopen(req, timeout=30) as response:
            if response.status in [200, 204]:
                return True
            else:
                print(f"  [ERROR] Status inesperado: {response.status}")
                return False

    except HTTPError as e:
        print(f"  [ERROR] HTTP {e.code}: {e.read().decode()}")
        return False
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False


def sync_product_to_shopify(product_id: str, dry_run: bool = False) -> bool:
    """
    Sincroniza produto com Shopify via Edge Function.
    """
    if dry_run:
        print(f"  [DRY-RUN] Sincronizaria {product_id} com Shopify")
        return True

    if not SUPABASE_SERVICE_ROLE_KEY:
        return False

    url = f"{SUPABASE_URL}/functions/v1/sync-shopify-product"

    headers = {
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
    }

    body = json.dumps({"productId": product_id}).encode("utf-8")

    try:
        req = Request(url, data=body, headers=headers, method="POST")
        with urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode())
            return result.get("success", False) or "shopifyProductId" in result
    except Exception as e:
        print(f"  [ERROR] Shopify sync: {e}")
        return False


# ============================================================================
# PUBLISH LOG
# ============================================================================

def load_publish_log() -> dict:
    """Carrega log de publicacoes."""
    if not PUBLISH_LOG.exists():
        return {"published": [], "failed": [], "last_run": None}

    try:
        return json.loads(PUBLISH_LOG.read_text(encoding="utf-8"))
    except:
        return {"published": [], "failed": [], "last_run": None}


def save_publish_log(log: dict):
    """Salva log de publicacoes."""
    log["last_run"] = datetime.now().isoformat()
    PUBLISH_LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")


def is_already_published(filename: str, log: dict) -> bool:
    """Verifica se arquivo ja foi publicado."""
    return filename in log.get("published", [])


# ============================================================================
# MAIN WORKFLOW
# ============================================================================

def process_all_anuncios(
    dry_run: bool = False,
    sync_shopify: bool = True,
    filter_file: Optional[str] = None
) -> list[PublishResult]:
    """
    Processa todos os anuncios pendentes.

    Args:
        dry_run: Simula sem alterar dados
        sync_shopify: Se True, sincroniza com Shopify apos update
        filter_file: Se fornecido, processa apenas arquivo que contem esta string

    Returns:
        Lista de resultados
    """
    results = []

    # Carrega dados
    products = load_products_cache()
    if not products:
        print("[ERROR] Nenhum produto no cache. Execute list_products.py primeiro.")
        return results

    log = load_publish_log()

    # Lista arquivos .md
    anuncio_files = list(USER_ANUNCIOS_DIR.glob("*.md"))
    anuncio_files = [f for f in anuncio_files if f.name != "README.md"]

    if filter_file:
        anuncio_files = [f for f in anuncio_files if filter_file.lower() in f.name.lower()]

    print(f"\n{'='*60}")
    print(f"AUTO-PUBLISHER - {'DRY RUN' if dry_run else 'PRODUCAO'}")
    print(f"{'='*60}")
    print(f"Produtos no cache: {len(products)}")
    print(f"Anuncios encontrados: {len(anuncio_files)}")
    print(f"Ja publicados: {len(log.get('published', []))}")
    print(f"{'='*60}\n")

    for filepath in anuncio_files:
        filename = filepath.name

        # Skip ja publicados (exceto em dry-run)
        if not dry_run and is_already_published(filename, log):
            print(f"[SKIP] {filename} - ja publicado")
            continue

        print(f"\n[PROCESSING] {filename}")

        # Parse anuncio
        anuncio = parse_anuncio_markdown(filepath)
        if not anuncio:
            results.append(PublishResult(
                success=False,
                product_id="",
                anuncio_file=filename,
                message="Falha ao parsear markdown"
            ))
            continue

        print(f"  Titulo: {anuncio.best_title[:50]}...")
        print(f"  Preco: R$ {anuncio.preco}")
        print(f"  Score: {anuncio.score}")

        # Match com produto
        product = match_anuncio_to_product(anuncio, products)
        if not product:
            print(f"  [WARNING] Nenhum produto correspondente encontrado")
            results.append(PublishResult(
                success=False,
                product_id="",
                anuncio_file=filename,
                message="Produto nao encontrado no Supabase"
            ))
            if not dry_run:
                log.setdefault("failed", []).append(filename)
            continue

        product_id = product["id"]
        print(f"  Match: {product['name'][:40]}... (ID: {product_id[:8]}...)")

        # Update no Supabase
        if update_product_in_supabase(product_id, anuncio, dry_run):
            print(f"  [OK] Supabase atualizado")

            # Sync com Shopify
            shopify_ok = False
            if sync_shopify:
                shopify_ok = sync_product_to_shopify(product_id, dry_run)
                if shopify_ok:
                    print(f"  [OK] Shopify sincronizado")
                else:
                    print(f"  [WARNING] Shopify sync falhou")

            results.append(PublishResult(
                success=True,
                product_id=product_id,
                anuncio_file=filename,
                message="Publicado com sucesso",
                shopify_synced=shopify_ok
            ))

            if not dry_run:
                log.setdefault("published", []).append(filename)
        else:
            results.append(PublishResult(
                success=False,
                product_id=product_id,
                anuncio_file=filename,
                message="Falha ao atualizar Supabase"
            ))
            if not dry_run:
                log.setdefault("failed", []).append(filename)

    # Salva log
    if not dry_run:
        save_publish_log(log)

    # Resumo
    success_count = sum(1 for r in results if r.success)
    print(f"\n{'='*60}")
    print(f"RESUMO: {success_count}/{len(results)} publicados com sucesso")
    print(f"{'='*60}\n")

    return results


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Auto-publish anuncios para Supabase/Shopify")
    parser.add_argument("--dry-run", action="store_true", help="Simula sem alterar dados")
    parser.add_argument("--no-shopify", action="store_true", help="Nao sincroniza com Shopify")
    parser.add_argument("--file", type=str, help="Processa apenas arquivo que contem esta string")
    parser.add_argument("--list", action="store_true", help="Lista anuncios e produtos sem processar")

    args = parser.parse_args()

    if args.list:
        # Modo listagem
        products = load_products_cache()
        anuncios = list(USER_ANUNCIOS_DIR.glob("*.md"))
        anuncios = [f for f in anuncios if f.name != "README.md"]

        print("\n=== PRODUTOS NO SUPABASE ===")
        for p in products:
            print(f"  - {p['name'][:50]} | R$ {p['price']} | {p['id'][:8]}...")

        print(f"\n=== ANUNCIOS GERADOS ({len(anuncios)}) ===")
        for a in anuncios:
            print(f"  - {a.name}")

        sys.exit(0)

    # Verifica service role key
    if not SUPABASE_SERVICE_ROLE_KEY and not args.dry_run:
        print("[ERROR] SUPABASE_SERVICE_ROLE_KEY nao configurada")
        print("Configure via: export SUPABASE_SERVICE_ROLE_KEY='sua-chave'")
        sys.exit(1)

    # Processa
    results = process_all_anuncios(
        dry_run=args.dry_run,
        sync_shopify=not args.no_shopify,
        filter_file=args.file
    )

    # Exit code baseado em resultados
    if all(r.success for r in results):
        sys.exit(0)
    else:
        sys.exit(1)
