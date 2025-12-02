#!/usr/bin/env python3
"""
🧬 KNOWLEDGE CONDENSATION ENGINE - OPTIMIZED VERSION
Condensa 94K+ knowledge cards → 100 JSON files entrópicos e axiomáticos
Otimizado para consumo LLM com zero contexto
WITH PARALLEL LOADING & PROGRESS INDICATORS
"""

import json
import re
from pathlib import Path
from collections import Counter, defaultdict
from typing import List, Dict, Any, Tuple
import hashlib
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
import sys

# Opcional: clustering semântico avançado (instalar se necessário)
try:
    from sklearn.cluster import KMeans
    from sklearn.feature_extraction.text import TfidfVectorizer
    SKLEARN_AVAILABLE = True
except ImportError:
    print("[WARN] sklearn não disponível. Usando clustering básico por keywords.")
    SKLEARN_AVAILABLE = False


# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

INPUT_DIR = Path("Processados/knowledge_cards")
OUTPUT_DIR = Path("CONDENSED_KNOWLEDGE")
N_CLUSTERS = 100
MIN_REUSABILITY_SCORE = 0.7
MAX_WORKERS = 4  # Parallel workers for file loading

# Categorias semânticas para distribuição
SEMANTIC_CATEGORIES = {
    "prompt_engineering": ["prompt", "template", "instruction", "llm", "gpt", "claude"],
    "ml_pipeline": ["pipeline", "training", "model", "inference", "deploy"],
    "data_processing": ["transform", "etl", "data", "clean", "preprocess"],
    "agent_systems": ["agent", "orchestration", "multi-agent", "workflow"],
    "knowledge_mgmt": ["knowledge", "ontology", "graph", "semantic", "embedding"],
    "meta_construction": ["meta", "self-improving", "adaptive", "learning"],
    "quality_assurance": ["validation", "quality", "test", "check", "verify"],
    "crud_patterns": ["crud", "database", "sql", "storage", "persistence"],
    "api_design": ["api", "rest", "endpoint", "integration", "service"],
    "error_handling": ["error", "exception", "retry", "fallback", "resilience"],
}


# ============================================================================
# PARALLEL FILE LOADING
# ============================================================================

def load_single_card(card_file: Path) -> Dict[str, Any]:
    """Carrega um único card (para processamento paralelo)."""
    try:
        with open(card_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] Erro ao carregar {card_file.name}: {e}", file=sys.stderr)
        return None


def load_all_cards_parallel(input_dir: Path, max_workers: int = 4) -> List[Dict[str, Any]]:
    """Carrega todos os knowledge cards do diretório COM PARALELISMO."""
    print(f"[LOAD] Carregando cards de: {input_dir}")
    print(f"[PARALLEL] Usando {max_workers} workers paralelos")

    card_files = list(input_dir.glob("*.json"))
    total_files = len(card_files)
    print(f"[FOUND] {total_files} ficheiros encontrados")

    cards = []
    processed = 0

    # Processamento paralelo
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(load_single_card, f): f for f in card_files}

        for future in as_completed(futures):
            card = future.result()
            if card:
                cards.append(card)

            processed += 1
            # Progress indicator a cada 1000 files
            if processed % 1000 == 0:
                progress = (processed / total_files) * 100
                print(f"[PROGRESS] {processed}/{total_files} ({progress:.1f}%)")

    print(f"[OK] {len(cards)} cards carregados com sucesso")
    return cards


# ============================================================================
# CORE FUNCTIONS (Same as original)
# ============================================================================

def extract_keywords_from_card(card: Dict[str, Any]) -> List[str]:
    """Extrai keywords de um card (normalizado)."""
    keywords = []

    # Extrair de campos relevantes
    text = f"{card.get('title', '')} {card.get('content', '')} {card.get('domain', '')}"

    # Parse JSON aninhado se content for string
    if isinstance(card.get('content'), str):
        try:
            nested = json.loads(card['content'])
            if isinstance(nested, dict):
                text += f" {nested.get('title', '')} {' '.join(nested.get('keywords', []))}"
        except:
            pass

    # Normalizar e extrair palavras
    words = re.findall(r'\b[a-z_]{3,}\b', text.lower())

    # Filtrar stopwords básicas
    stopwords = {'the', 'and', 'for', 'with', 'this', 'that', 'from', 'are', 'was'}
    keywords = [w for w in words if w not in stopwords]

    return keywords


def assign_semantic_category(keywords: List[str]) -> str:
    """Atribui categoria semântica baseado em keywords."""
    scores = defaultdict(int)

    for keyword in keywords:
        for category, category_keywords in SEMANTIC_CATEGORIES.items():
            if keyword in category_keywords:
                scores[category] += 1

    if scores:
        return max(scores, key=scores.get)
    return "general_knowledge"


def cluster_cards_basic(cards: List[Dict[str, Any]], n_clusters: int) -> Dict[int, List[Dict[str, Any]]]:
    """Clustering básico por keywords (fallback sem sklearn)."""
    print(f"[CLUSTER] Clustering básico por keywords...")

    # Extrair keywords de todos os cards
    all_keywords = []
    for card in cards:
        keywords = extract_keywords_from_card(card)
        all_keywords.extend(keywords)

    # Top N keywords como "clusters"
    top_keywords = [kw for kw, _ in Counter(all_keywords).most_common(n_clusters)]

    # Distribuir cards pelos clusters
    clusters = defaultdict(list)
    for card in cards:
        card_keywords = extract_keywords_from_card(card)

        # Encontrar melhor cluster
        best_cluster = 0
        best_score = 0
        for i, cluster_kw in enumerate(top_keywords):
            if cluster_kw in card_keywords:
                score = card_keywords.count(cluster_kw)
                if score > best_score:
                    best_score = score
                    best_cluster = i

        clusters[best_cluster].append(card)

    print(f"[OK] {len(clusters)} clusters criados")
    return dict(clusters)


def cluster_cards_advanced(cards: List[Dict[str, Any]], n_clusters: int) -> Dict[int, List[Dict[str, Any]]]:
    """Clustering avançado com TF-IDF + KMeans."""
    print(f"[CLUSTER] Clustering avançado com TF-IDF + KMeans...")

    # Extrair texto de cada card
    texts = []
    for card in cards:
        text = f"{card.get('title', '')} {card.get('content', '')}"
        texts.append(text)

    # TF-IDF
    vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
    X = vectorizer.fit_transform(texts)

    # KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X)

    # Organizar por cluster
    clusters = defaultdict(list)
    for i, card in enumerate(cards):
        clusters[labels[i]].append(card)

    print(f"[OK] {len(clusters)} clusters criados")
    return dict(clusters)


def extract_axioms(cluster_cards: List[Dict[str, Any]]) -> List[str]:
    """Extrai axiomas/princípios comuns de um cluster."""
    # Análise simples: padrões que aparecem em múltiplos cards
    all_content = []
    for card in cluster_cards:
        content = str(card.get('content', ''))
        all_content.append(content)

    # Buscar padrões comuns (frases curtas que repetem)
    patterns = []
    for content in all_content:
        sentences = re.split(r'[.!?]\s+', content)
        for sentence in sentences:
            if 5 < len(sentence.split()) < 20:  # Sentenças médias
                patterns.append(sentence.strip().lower())

    # Top padrões como "axiomas"
    axioms = [p for p, count in Counter(patterns).most_common(5) if count > 1]
    return axioms


def parametrize_content(content: str) -> Tuple[str, Dict[str, str]]:
    """Parametriza variáveis específicas em placeholders genéricos."""
    parameters = {}

    # Padrões a parametrizar
    replacements = [
        (r'gpt-[0-9a-z-]+', '{LLM_MODEL}', 'LLM model identifier'),
        (r'sk-[a-zA-Z0-9]+', '{API_KEY}', 'API authentication key'),
        (r'https?://[^\s]+', '{URL}', 'URL endpoint'),
        (r'/[a-z/]+/[a-z0-9_/.]+', '{FILE_PATH}', 'File system path'),
        (r'postgresql://[^\s]+', '{DATABASE_URL}', 'Database connection string'),
        (r'\b[A-Z_]{3,}\b', '{CONSTANT}', 'Configuration constant'),
    ]

    parametrized = content
    for pattern, placeholder, description in replacements:
        matches = re.findall(pattern, content)
        if matches:
            parametrized = re.sub(pattern, placeholder, parametrized)
            parameters[placeholder] = description

    return parametrized, parameters


def calculate_reusability_score(knowledge_block: Dict[str, Any]) -> float:
    """Calcula score de reutilização (0.0-1.0)."""
    score = 0.0

    # Presença de axiomas (+0.3)
    if knowledge_block.get('content', {}).get('axiom'):
        score += 0.3

    # Presença de parâmetros (+0.2)
    if knowledge_block.get('content', {}).get('parameters'):
        score += 0.2

    # Presença de heurísticas (+0.2)
    if knowledge_block.get('content', {}).get('heuristics'):
        score += 0.2

    # Presença de padrões (+0.15)
    if knowledge_block.get('content', {}).get('patterns'):
        score += 0.15

    # Presença de anti-padrões (+0.15)
    if knowledge_block.get('content', {}).get('anti_patterns'):
        score += 0.15

    return min(score, 1.0)


def condense_cluster(cluster_cards: List[Dict[str, Any]], cluster_id: int) -> Dict[str, Any]:
    """Condensa um cluster em conhecimento entrópico."""

    # Extrair keywords do cluster
    all_keywords = []
    for card in cluster_cards:
        all_keywords.extend(extract_keywords_from_card(card))

    top_keywords = [kw for kw, _ in Counter(all_keywords).most_common(10)]

    # Categoria semântica
    category = assign_semantic_category(top_keywords)

    # Extrair axiomas
    axioms = extract_axioms(cluster_cards)

    # Criar knowledge blocks
    knowledge_blocks = []
    for i, card in enumerate(cluster_cards[:20]):  # Limitar a 20 por cluster
        content_str = str(card.get('content', ''))
        parametrized, parameters = parametrize_content(content_str)

        block = {
            "block_id": f"BLOCK_{cluster_id:03d}_{i:03d}",
            "type": "pattern",  # Pode ser refinado
            "title": str(card.get('title', 'Untitled'))[:100],
            "content": {
                "axiom": axioms[0] if axioms else None,
                "description": parametrized[:500],  # Limitar tamanho
                "parameters": parameters,
                "heuristics": [
                    "Aplicável quando {VAR} está disponível",
                    "Evitar quando {CONSTRAINT} é requerido"
                ],
                "patterns": top_keywords[:5],
            },
            "reusability_score": 0.0,
            "llm_applicability": [category],
        }

        block["reusability_score"] = calculate_reusability_score(block)
        knowledge_blocks.append(block)

    # Calcular metadata de consolidação
    quality_scores = [card.get('quality_score', 0) for card in cluster_cards]
    avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0

    condensed = {
        "file_id": f"CONDENSED_{cluster_id:03d}",
        "title": f"{category.replace('_', ' ').title()}",
        "category": category,
        "keywords": top_keywords[:15],
        "entropy_level": "high" if len(knowledge_blocks) > 15 else "medium",
        "abstraction_level": "pattern",
        "knowledge_blocks": knowledge_blocks,
        "consolidation_metadata": {
            "source_cards_count": len(cluster_cards),
            "avg_quality_score": round(avg_quality, 2),
            "condensation_ratio": f"{len(cluster_cards)}:{len(knowledge_blocks)}",
            "semantic_coherence": round(min(1.0, len(set(top_keywords)) / 50), 2),
            "timestamp": datetime.now().isoformat(),
        }
    }

    return condensed


def generate_semantic_filename(condensed: Dict[str, Any]) -> str:
    """Gera nome de arquivo semântico."""
    keywords = condensed.get('keywords', [])[:3]

    # Sanitizar keywords
    clean_keywords = []
    for kw in keywords:
        clean = re.sub(r'[^a-z0-9_]', '', kw.lower())
        if clean:
            clean_keywords.append(clean)

    if not clean_keywords:
        clean_keywords = [f"cluster_{condensed.get('file_id', 'unknown')}"]

    filename = "_".join(clean_keywords)
    return filename


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def main():
    """Pipeline principal de condensação."""
    print("=" * 80)
    print("KNOWLEDGE CONDENSATION ENGINE - OPTIMIZED")
    print("=" * 80)

    # Validar diretórios
    if not INPUT_DIR.exists():
        print(f"[ERROR] Diretório de input não encontrado: {INPUT_DIR}")
        return

    OUTPUT_DIR.mkdir(exist_ok=True)
    print(f"[OUTPUT] Output: {OUTPUT_DIR}")

    # STEP 1: Carregar cards COM PARALELISMO
    cards = load_all_cards_parallel(INPUT_DIR, MAX_WORKERS)
    if not cards:
        print("[ERROR] Nenhum card encontrado!")
        return

    # STEP 2: Clustering
    if SKLEARN_AVAILABLE and len(cards) > 100:
        clusters = cluster_cards_advanced(cards, N_CLUSTERS)
    else:
        clusters = cluster_cards_basic(cards, N_CLUSTERS)

    # STEP 3: Condensar cada cluster
    print(f"\n[CONDENSE] Condensando {len(clusters)} clusters...")
    condensed_files = []

    for cluster_id, cluster_cards in clusters.items():
        if not cluster_cards:
            continue

        print(f"  Cluster {cluster_id + 1}/{len(clusters)}: {len(cluster_cards)} cards")

        condensed = condense_cluster(cluster_cards, cluster_id)
        filename = generate_semantic_filename(condensed)

        # Salvar
        output_path = OUTPUT_DIR / f"{filename}.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(condensed, f, indent=2, ensure_ascii=False)

        condensed_files.append({
            "filename": f"{filename}.json",
            "cards_count": len(cluster_cards),
            "category": condensed.get('category'),
            "keywords": condensed.get('keywords', [])[:5]
        })

        print(f"    [OK] {filename}.json")

    # STEP 4: Gerar índice
    index = {
        "metadata": {
            "total_files": len(condensed_files),
            "total_source_cards": len(cards),
            "condensation_ratio": f"{len(cards)}:{len(condensed_files)}",
            "timestamp": datetime.now().isoformat(),
        },
        "files": condensed_files
    }

    index_path = OUTPUT_DIR / "_INDEX.json"
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 80)
    print(f"[SUCCESS] CONDENSACAO COMPLETA!")
    print(f"   [STATS] {len(cards)} cards -> {len(condensed_files)} files")
    print(f"   [OUTPUT] Output: {OUTPUT_DIR}")
    print(f"   [INDEX] Indice: {index_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()
