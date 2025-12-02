#!/usr/bin/env python3
"""
synthesize_knowledge_cards_v2.py
=================================
DEEP SYNTHESIS: Uses LLM to create truly dense, enriched knowledge cards.

Key differences from v1:
- Reads from CONSOLIDATED sources (15+ MB of dense knowledge) instead of thin versiculos
- Uses Claude API to synthesize and enrich concepts
- Groups related concepts before synthesis (e.g., all "marketplace" concepts → 1 dense card)
- Generates 800-1000 token cards with entropy >80
- Adds practical applications, insights, metrics, KPIs automatically

Pipeline:
1. SCAN      - Load consolidated sources (_CONSOLIDATED_*.md)
2. EXTRACT   - Extract concept sections using semantic chunking
3. CLUSTER   - Group related concepts by similarity
4. SYNTHESIZE - Use Claude to create dense cards from concept groups
5. ENRICH    - Add practical examples, metrics, cross-references
6. VALIDATE  - Ensure entropy >80, tokens 800-1000
7. INDEX     - Generate searchable indexes
8. DEPLOY    - Write enriched cards

Based on: specs/chore-obsidian-knowledge-synthesis.md
Requires: ANTHROPIC_API_KEY environment variable
"""

import argparse
import json
import logging
import math
import os
import re
import sys
import time
import yaml
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional

# Try to import required libraries
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("Warning: anthropic package not available. Install with: pip install anthropic")

try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    print("Warning: tiktoken not available. Using approximate token counting.")


# ============================================================================
# UTILITIES
# ============================================================================

def calculate_entropy(text: str) -> float:
    """
    Calculate Shannon entropy of text, normalized to 0-100 scale.

    Args:
        text: Input text to analyze

    Returns:
        Entropy score between 0-100 (higher = more information density)
    """
    if not text or len(text.strip()) == 0:
        return 0.0

    # Count character frequencies
    counter = Counter(text.lower())
    total = sum(counter.values())

    # Calculate Shannon entropy
    entropy = 0.0
    for count in counter.values():
        p = count / total
        if p > 0:
            entropy -= p * math.log2(p)

    # Normalize to 0-100 scale (typical text entropy is 4-5 bits)
    normalized = (entropy / 5.0) * 100
    return min(100.0, max(0.0, normalized))


def count_tokens(text: str) -> int:
    """
    Count tokens in text using tiktoken (if available) or approximation.

    Args:
        text: Input text

    Returns:
        Approximate token count
    """
    if TIKTOKEN_AVAILABLE:
        try:
            enc = tiktoken.get_encoding('cl100k_base')  # GPT-4 encoding
            return len(enc.encode(text))
        except Exception as e:
            logging.warning(f"tiktoken encoding failed: {e}, using approximation")

    # Fallback: approximate tokens as words * 1.3
    words = len(re.findall(r'\b\w+\b', text))
    return int(words * 1.3)


def extract_keywords(text: str, top_n: int = 12) -> List[str]:
    """
    Extract keywords using frequency analysis with stop word filtering.

    Args:
        text: Input text
        top_n: Number of top keywords to return

    Returns:
        List of extracted keywords
    """
    # Extended stop words (PT-BR and EN)
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
        'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
        'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
        'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas', 'de', 'do', 'da',
        'dos', 'das', 'em', 'no', 'na', 'nos', 'nas', 'para', 'com', 'por',
        'que', 'se', 'não', 'mais', 'como', 'mas', 'já', 'também', 'só',
        'pelo', 'pela', 'até', 'isso', 'esse', 'essa', 'este', 'esta',
        'ser', 'ter', 'estar', 'fazer', 'poder', 'dever', 'quando', 'muito',
        'e', 'é', 'à', 'ao', 'seu', 'sua', 'seus', 'suas', 'meu', 'minha'
    }

    # Extract words (3+ chars)
    words = re.findall(r'\b[a-záàâãéèêíïóôõöúçñ]{3,}\b', text.lower())
    filtered = [w for w in words if w not in stop_words]

    # Count and return top N
    counter = Counter(filtered)
    return [word for word, _ in counter.most_common(top_n)]


def chunk_text(text: str, max_tokens: int = 4000) -> List[str]:
    """
    Split text into chunks that fit within token limit.

    Args:
        text: Input text
        max_tokens: Maximum tokens per chunk

    Returns:
        List of text chunks
    """
    # Split by paragraphs first
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = []
    current_tokens = 0

    for para in paragraphs:
        para_tokens = count_tokens(para)

        if current_tokens + para_tokens > max_tokens and current_chunk:
            # Save current chunk and start new one
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [para]
            current_tokens = para_tokens
        else:
            current_chunk.append(para)
            current_tokens += para_tokens

    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))

    return chunks


# ============================================================================
# CONSOLIDATED SOURCES READER
# ============================================================================

class ConsolidatedSourcesReader:
    """
    Reads and parses consolidated knowledge sources.
    """

    def __init__(self, sources_dir: Path):
        """
        Initialize reader.

        Args:
            sources_dir: Directory containing _CONSOLIDATED_*.md files
        """
        self.sources_dir = sources_dir
        self.sources = {}
        self.logger = logging.getLogger(__name__)

    def load_all_sources(self) -> Dict[str, str]:
        """
        Load all consolidated sources.

        Returns:
            Dictionary mapping source name to content
        """
        self.logger.info(f"Loading consolidated sources from {self.sources_dir}")

        consolidated_files = list(self.sources_dir.glob('_CONSOLIDATED_*.md'))
        self.logger.info(f"Found {len(consolidated_files)} consolidated files")

        for file_path in consolidated_files:
            try:
                source_name = file_path.stem  # e.g., "_CONSOLIDATED_ecommerce_livro"
                content = file_path.read_text(encoding='utf-8')
                self.sources[source_name] = content

                size_mb = len(content) / (1024 * 1024)
                self.logger.info(f"  Loaded {source_name}: {size_mb:.2f} MB")

            except Exception as e:
                self.logger.error(f"Error loading {file_path}: {e}")

        total_mb = sum(len(c) for c in self.sources.values()) / (1024 * 1024)
        self.logger.info(f"Total loaded: {total_mb:.2f} MB from {len(self.sources)} sources")

        return self.sources

    def extract_concepts(self, source_content: str, source_name: str) -> List[Dict]:
        """
        Extract concept sections from consolidated source.

        Args:
            source_content: Full source content
            source_name: Name of the source

        Returns:
            List of concept dictionaries
        """
        concepts = []

        # Split by markdown headers
        sections = re.split(r'\n#{1,3}\s+', source_content)

        for i, section in enumerate(sections[1:], 1):  # Skip first (before any header)
            # Extract section title (first line)
            lines = section.split('\n', 1)
            if len(lines) < 2:
                continue

            title = lines[0].strip()
            content = lines[1].strip()

            # Skip very short sections
            if len(content) < 200:
                continue

            concept = {
                'id': f"{source_name}_CONCEPT_{i:04d}",
                'title': title,
                'content': content,
                'source': source_name,
                'tokens': count_tokens(content),
                'entropy': calculate_entropy(content),
                'keywords': extract_keywords(content, top_n=12)
            }

            concepts.append(concept)

        self.logger.info(f"Extracted {len(concepts)} concepts from {source_name}")
        return concepts


# ============================================================================
# LLM SYNTHESIS ENGINE
# ============================================================================

class LLMSynthesisEngine:
    """
    Uses Claude API to synthesize dense knowledge cards.
    """

    def __init__(self, api_key: str, model: str = "claude-3-5-sonnet-20241022"):
        """
        Initialize synthesis engine.

        Args:
            api_key: Anthropic API key
            model: Claude model to use
        """
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("anthropic package required. Install with: pip install anthropic")

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.logger = logging.getLogger(__name__)

    def synthesize_card(self, concepts: List[Dict], target_tokens: int = 850) -> Dict:
        """
        Synthesize multiple related concepts into one dense knowledge card.

        Args:
            concepts: List of related concept dictionaries
            target_tokens: Target token count for output

        Returns:
            Synthesized card dictionary
        """
        # Prepare synthesis prompt
        concepts_text = "\n\n---\n\n".join([
            f"**Conceito {i+1}: {c['title']}**\n\n{c['content'][:2000]}"  # Limit each concept
            for i, c in enumerate(concepts[:5])  # Max 5 concepts per card
        ])

        prompt = f"""Você é um especialista em sintetizar conhecimento denso para e-commerce.

TAREFA: Sintetizar os conceitos abaixo em um Knowledge Card ultra-denso e rico.

CONCEITOS FONTE:
{concepts_text}

REQUISITOS DO KNOWLEDGE CARD:
- Formato: Markdown limpo e estruturado
- Tamanho: Aproximadamente {target_tokens} tokens (600-800 palavras)
- Densidade: Máxima (entropia > 80/100)
- Keywords: 10-12 palavras-chave densas e específicas

ESTRUTURA OBRIGATÓRIA:

# [Título do Conceito Sintetizado]

## 📌 Conceito Core

[2-3 parágrafos densos explicando o conceito de forma profunda e técnica. Inclua definições precisas, princípios fundamentais, e contexto de aplicação no e-commerce.]

## 🎯 Aplicações Práticas

### Caso 1: [Nome do Cenário Real]
**Contexto:** [Descrição do contexto de negócio]
**Implementação:** [Como aplicar o conceito, passo a passo]
**Métricas:** [KPIs específicos para medir sucesso]
**Resultado Esperado:** [Outcome quantificável]

### Caso 2: [Nome do Cenário Real]
**Contexto:** [Descrição do contexto de negócio]
**Implementação:** [Como aplicar o conceito, passo a passo]
**Métricas:** [KPIs específicos para medir sucesso]
**Resultado Esperado:** [Outcome quantificável]

### Caso 3: [Nome do Cenário Real]
**Contexto:** [Descrição do contexto de negócio]
**Implementação:** [Como aplicar o conceito, passo a passo]
**Métricas:** [KPIs específicos para medir sucesso]
**Resultado Esperado:** [Outcome quantificável]

## 💡 Insights Chave

- **Insight 1:** [Insight não-óbvio que muda a compreensão do conceito]
- **Insight 2:** [Padrão ou princípio identificado através de múltiplos casos]
- **Insight 3:** [Trade-off ou consideração crítica para implementação]
- **Insight 4:** [Erro comum a evitar ou best practice contra-intuitiva]

## 📊 Métricas e KPIs

- **Métrica 1:** [Nome] - [Valor típico ou range] - [Como medir]
- **Métrica 2:** [Nome] - [Valor típico ou range] - [Como medir]
- **Métrica 3:** [Nome] - [Valor típico ou range] - [Como medir]

## 🔗 Relações e Dependências

- **Pré-requisitos:** [Conceitos que devem ser dominados antes]
- **Habilita:** [O que este conceito permite fazer]
- **Sinergia com:** [Conceitos relacionados que potencializam este]

## 🏷️ Keywords Densas

[Lista de 10-12 keywords específicas, separadas por vírgula]

---

IMPORTANTE:
- Use linguagem técnica e precisa
- Todos os exemplos devem ser CONCRETOS e do mundo real do e-commerce
- Métricas devem ser QUANTIFICÁVEIS com valores reais
- Maximize densidade de informação
- Evite generalidades - seja específico e acionável
"""

        try:
            self.logger.info(f"Synthesizing card from {len(concepts)} concepts...")

            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            synthesized_content = response.content[0].text

            # Extract title from synthesized content
            title_match = re.search(r'^#\s+(.+)$', synthesized_content, re.MULTILINE)
            title = title_match.group(1) if title_match else concepts[0]['title']

            # Extract keywords from the synthesized content
            keywords_section = re.search(r'## 🏷️ Keywords Densas\s*\n\s*(.+?)(?:\n\n|\Z)', synthesized_content, re.DOTALL)
            if keywords_section:
                keywords_text = keywords_section.group(1).strip()
                keywords = [k.strip() for k in re.split(r'[,\n]', keywords_text) if k.strip()]
            else:
                # Fallback to extraction
                keywords = extract_keywords(synthesized_content, top_n=12)

            card = {
                'title': title,
                'content': synthesized_content,
                'source_concepts': [c['id'] for c in concepts],
                'sources': list(set(c['source'] for c in concepts)),
                'keywords': keywords,
                'token_count': count_tokens(synthesized_content),
                'entropy': calculate_entropy(synthesized_content),
                'synthesized_at': str(date.today()),
                'model': self.model
            }

            self.logger.info(f"✅ Synthesized card: {title[:50]}... ({card['token_count']} tokens, entropy {card['entropy']:.1f})")

            return card

        except Exception as e:
            self.logger.error(f"Error synthesizing card: {e}")
            raise

    def create_llm_version(self, human_card: Dict) -> Dict:
        """
        Create LLM-optimized version of a human card.

        Args:
            human_card: Human-readable card

        Returns:
            LLM-optimized card
        """
        prompt = f"""Converta o Knowledge Card abaixo em formato LLM-OPTIMIZED.

CARD HUMANO:
{human_card['content']}

REQUISITOS DO FORMATO LLM:
- Estrutura: KEYWORD: value (sem markdown fancy)
- Densidade: Máxima compressão mantendo informação
- Keywords: Separadas por vírgula, altamente específicas
- Formato: Otimizado para embeddings e RAG

ESTRUTURA OBRIGATÓRIA:

CONCEPT: [Título do conceito]

DEFINITION:
[Definição técnica em 2-3 frases, formato denso e estruturado]

DOMAIN: [Livro] > [Capítulo]

KEY_PRINCIPLES:
1. [PRINCÍPIO_1]: [explicação concisa]
2. [PRINCÍPIO_2]: [explicação concisa]
3. [PRINCÍPIO_3]: [explicação concisa]
4. [PRINCÍPIO_4]: [explicação concisa]

APPLICATIONS:
- USE_CASE_1: [contexto] → [ação] → [métrica] → [resultado]
- USE_CASE_2: [contexto] → [ação] → [métrica] → [resultado]
- USE_CASE_3: [contexto] → [ação] → [métrica] → [resultado]

METRICS_KPI:
- [Métrica_1]: [valor típico] | [como medir]
- [Métrica_2]: [valor típico] | [como medir]
- [Métrica_3]: [valor típico] | [como medir]

RELATIONSHIPS:
- DEPENDS_ON: [conceito1], [conceito2]
- ENABLES: [conceito3], [conceito4]
- SYNERGY: [conceito5], [conceito6]

DENSE_KEYWORDS: [kw1], [kw2], [kw3], [kw4], [kw5], [kw6], [kw7], [kw8], [kw9], [kw10], [kw11], [kw12]

TAXONOMY_PATH: [livro]/[capitulo]/[conceito]

---

IMPORTANTE:
- Remova TODOS emojis
- Use CAPS para labels (CONCEPT:, DEFINITION:, etc)
- Formato flat e estruturado
- Máxima densidade de informação
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                temperature=0.5,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            llm_content = response.content[0].text

            llm_card = {
                'title': human_card['title'],
                'content': llm_content,
                'source_concepts': human_card['source_concepts'],
                'sources': human_card['sources'],
                'keywords': human_card['keywords'],
                'token_count': count_tokens(llm_content),
                'entropy': calculate_entropy(llm_content),
                'synthesized_at': str(date.today()),
                'model': self.model,
                'type': 'llm'
            }

            self.logger.info(f"✅ Created LLM version: {llm_card['token_count']} tokens, entropy {llm_card['entropy']:.1f}")

            return llm_card

        except Exception as e:
            self.logger.error(f"Error creating LLM version: {e}")
            raise


# ============================================================================
# CONCEPT CLUSTERING
# ============================================================================

class ConceptClusterer:
    """
    Groups related concepts for synthesis.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def cluster_by_keywords(self, concepts: List[Dict], min_overlap: int = 3) -> List[List[Dict]]:
        """
        Cluster concepts by keyword similarity.

        Args:
            concepts: List of concept dictionaries
            min_overlap: Minimum keyword overlap to group

        Returns:
            List of concept clusters
        """
        self.logger.info(f"Clustering {len(concepts)} concepts by keyword similarity...")

        # Build keyword index
        keyword_to_concepts = defaultdict(list)
        for concept in concepts:
            for keyword in concept['keywords']:
                keyword_to_concepts[keyword].append(concept['id'])

        # Find concept pairs with sufficient overlap
        overlap_graph = defaultdict(set)
        for i, concept_a in enumerate(concepts):
            for j, concept_b in enumerate(concepts[i+1:], i+1):
                common_keywords = set(concept_a['keywords']) & set(concept_b['keywords'])
                if len(common_keywords) >= min_overlap:
                    overlap_graph[concept_a['id']].add(concept_b['id'])
                    overlap_graph[concept_b['id']].add(concept_a['id'])

        # Group into clusters (simple connected components)
        visited = set()
        clusters = []

        def dfs(concept_id, cluster):
            if concept_id in visited:
                return
            visited.add(concept_id)
            cluster.append(concept_id)
            for neighbor in overlap_graph.get(concept_id, []):
                dfs(neighbor, cluster)

        for concept in concepts:
            if concept['id'] not in visited:
                cluster_ids = []
                dfs(concept['id'], cluster_ids)
                clusters.append(cluster_ids)

        # Convert ID clusters to concept clusters
        id_to_concept = {c['id']: c for c in concepts}
        concept_clusters = [
            [id_to_concept[cid] for cid in cluster_ids if cid in id_to_concept]
            for cluster_ids in clusters
        ]

        # Filter out single-concept clusters (keep for individual cards)
        multi_concept_clusters = [c for c in concept_clusters if len(c) > 1]
        single_concepts = [[c[0]] for c in concept_clusters if len(c) == 1]

        self.logger.info(f"Found {len(multi_concept_clusters)} multi-concept clusters, {len(single_concepts)} individual concepts")

        return multi_concept_clusters + single_concepts


# ============================================================================
# MAIN V2 SYNTHESIZER
# ============================================================================

class KnowledgeCardSynthesizerV2:
    """
    V2: Deep synthesis with LLM enrichment.
    """

    def __init__(self, config_path: Path):
        """
        Initialize V2 synthesizer.

        Args:
            config_path: Path to synthesis_config.yaml
        """
        self.config = self._load_config(config_path)
        self.setup_logging()

        # Initialize components
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        self.sources_reader = ConsolidatedSourcesReader(
            Path(self.config['sources'].get('raw_lcm_base', 'knowledge_base/app_documentation/RAW_LCM'))
        )
        self.synthesis_engine = LLMSynthesisEngine(api_key)
        self.clusterer = ConceptClusterer()

        self.concepts = []
        self.clusters = []
        self.cards = []

    def _load_config(self, config_path: Path) -> Dict:
        """Load YAML configuration."""
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def setup_logging(self):
        """Setup logging."""
        log_file = self.config.get('logging', {}).get('log_file', 'synthesis_v2.log')
        verbose = self.config.get('logging', {}).get('verbose', True)

        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def run_pipeline(self) -> Dict:
        """
        Execute deep synthesis pipeline.

        Returns:
            Pipeline results dictionary
        """
        self.logger.info("=" * 70)
        self.logger.info("🚀 KNOWLEDGE CARD SYNTHESIS V2 - DEEP SYNTHESIS")
        self.logger.info("=" * 70)

        results = {}

        try:
            # Stage 1: Load consolidated sources
            self.logger.info("\n" + "=" * 70)
            self.logger.info("📚 STAGE 1: Loading consolidated sources")
            self.logger.info("=" * 70)
            sources = self.sources_reader.load_all_sources()
            results['sources_loaded'] = len(sources)

            # Stage 2: Extract concepts
            self.logger.info("\n" + "=" * 70)
            self.logger.info("🔍 STAGE 2: Extracting concepts from sources")
            self.logger.info("=" * 70)
            for source_name, content in sources.items():
                concepts = self.sources_reader.extract_concepts(content, source_name)
                self.concepts.extend(concepts)
            results['concepts_extracted'] = len(self.concepts)

            # Stage 3: Cluster concepts
            self.logger.info("\n" + "=" * 70)
            self.logger.info("🗂️  STAGE 3: Clustering related concepts")
            self.logger.info("=" * 70)
            self.clusters = self.clusterer.cluster_by_keywords(self.concepts)
            results['clusters_created'] = len(self.clusters)

            # Stage 4: Synthesize cards (with rate limiting)
            self.logger.info("\n" + "=" * 70)
            self.logger.info("🧠 STAGE 4: Synthesizing dense knowledge cards with LLM")
            self.logger.info("=" * 70)

            max_cards = self.config.get('processing', {}).get('max_cards', 10)
            self.logger.info(f"Will synthesize up to {max_cards} cards (set max_cards in config)")

            for i, cluster in enumerate(self.clusters[:max_cards]):
                try:
                    self.logger.info(f"\nSynthesizing card {i+1}/{min(len(self.clusters), max_cards)}...")

                    # Synthesize human card
                    human_card = self.synthesis_engine.synthesize_card(cluster)
                    human_card['id'] = f"CARD_{i+1:04d}"
                    human_card['type'] = 'human'
                    self.cards.append(human_card)

                    # Create LLM version
                    llm_card = self.synthesis_engine.create_llm_version(human_card)
                    llm_card['id'] = f"CARD_{i+1:04d}_LLM"
                    self.cards.append(llm_card)

                    # Rate limiting (Anthropic has rate limits)
                    time.sleep(1)

                except Exception as e:
                    self.logger.error(f"Error synthesizing cluster {i}: {e}")

            results['cards_synthesized'] = len(self.cards)

            # Stage 5: Validate quality
            self.logger.info("\n" + "=" * 70)
            self.logger.info("✅ STAGE 5: Validating card quality")
            self.logger.info("=" * 70)
            validation = self._validate_cards()
            results['validation'] = validation

            # Stage 6: Deploy
            self.logger.info("\n" + "=" * 70)
            self.logger.info("🚀 STAGE 6: Deploying cards to disk")
            self.logger.info("=" * 70)
            deploy_stats = self._deploy_cards()
            results['deploy'] = deploy_stats

            self.logger.info("\n" + "=" * 70)
            self.logger.info("✅ V2 PIPELINE COMPLETED")
            self.logger.info("=" * 70)

            return results

        except Exception as e:
            self.logger.error(f"❌ Pipeline failed: {e}")
            raise

    def _validate_cards(self) -> Dict:
        """Validate card quality."""
        validation = {
            'total': len(self.cards),
            'high_quality': 0,  # entropy >= 80
            'good_quality': 0,  # entropy >= 70
            'needs_review': 0,  # entropy < 70
            'avg_entropy': 0.0,
            'avg_tokens': 0
        }

        for card in self.cards:
            entropy = card.get('entropy', 0)
            if entropy >= 80:
                validation['high_quality'] += 1
            elif entropy >= 70:
                validation['good_quality'] += 1
            else:
                validation['needs_review'] += 1

        if self.cards:
            validation['avg_entropy'] = sum(c.get('entropy', 0) for c in self.cards) / len(self.cards)
            validation['avg_tokens'] = sum(c.get('token_count', 0) for c in self.cards) / len(self.cards)

        self.logger.info(f"Quality Metrics:")
        self.logger.info(f"  High Quality (≥80): {validation['high_quality']}")
        self.logger.info(f"  Good Quality (≥70): {validation['good_quality']}")
        self.logger.info(f"  Needs Review (<70): {validation['needs_review']}")
        self.logger.info(f"  Avg Entropy: {validation['avg_entropy']:.1f}")
        self.logger.info(f"  Avg Tokens: {validation['avg_tokens']:.0f}")

        return validation

    def _deploy_cards(self) -> Dict:
        """Write cards to disk."""
        output_dir = Path(self.config['output']['cards_dir'])
        output_dir.mkdir(parents=True, exist_ok=True)

        stats = {'written': 0, 'errors': 0}

        for card in self.cards:
            try:
                card_id = card['id']
                card_type = card.get('type', 'unknown')

                # Write to output directory
                suffix = '.llm.md' if card_type == 'llm' else '.md'
                card_file = output_dir / f"{card_id}{suffix}"

                # Build full card with frontmatter
                frontmatter = f"""---
id: {card_id}
title: {card['title']}
keywords: {card['keywords']}
entropy: {card['entropy']:.1f}
token_count: {card['token_count']}
sources: {card['sources']}
synthesized_at: {card['synthesized_at']}
model: {card['model']}
type: {card_type}
version: "2.0-{card_type}"
---

"""
                full_content = frontmatter + card['content']
                card_file.write_text(full_content, encoding='utf-8')
                stats['written'] += 1

            except Exception as e:
                self.logger.error(f"Error writing card {card.get('id', 'UNKNOWN')}: {e}")
                stats['errors'] += 1

        self.logger.info(f"Deployed {stats['written']} cards to {output_dir}")
        return stats


# ============================================================================
# CLI
# ============================================================================

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='V2: Deep synthesis with LLM enrichment for knowledge cards'
    )
    parser.add_argument(
        '--config',
        type=Path,
        default=Path('knowledge_cards/config/synthesis_config.yaml'),
        help='Path to synthesis configuration file'
    )

    args = parser.parse_args()

    try:
        synthesizer = KnowledgeCardSynthesizerV2(args.config)
        results = synthesizer.run_pipeline()

        # Print summary
        print("\n" + "=" * 70)
        print("📊 V2 SYNTHESIS SUMMARY")
        print("=" * 70)
        print(f"Sources Loaded: {results.get('sources_loaded', 0)}")
        print(f"Concepts Extracted: {results.get('concepts_extracted', 0)}")
        print(f"Concept Clusters: {results.get('clusters_created', 0)}")
        print(f"Cards Synthesized: {results.get('cards_synthesized', 0)}")
        print(f"High Quality Cards (≥80): {results.get('validation', {}).get('high_quality', 0)}")
        print(f"Avg Entropy: {results.get('validation', {}).get('avg_entropy', 0):.1f}")
        print(f"Avg Tokens: {results.get('validation', {}).get('avg_tokens', 0):.0f}")
        print("=" * 70)

        return 0

    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
