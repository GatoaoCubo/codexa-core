"""
Scout FONTES Integration

Extends Scout search to include external documentation from FONTES/
Provides unified search across both PROCESSADOS/ (internal knowledge)
and FONTES/ (external documentation).
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class SearchResult:
    """Unified search result from PROCESSADOS or FONTES"""
    source_type: str  # 'processados' or 'fontes'
    file_path: str
    categoria: str
    assunto: str
    relevance_score: float
    fonte_id: Optional[str] = None  # Only for FONTES
    plataforma: Optional[str] = None  # Only for FONTES
    url_oficial: Optional[str] = None  # Only for FONTES
    topics: List[str] = None  # Only for FONTES
    tags: List[str] = None  # Only for PROCESSADOS

class ScoutFontes:
    """Extended Scout that searches both PROCESSADOS and FONTES"""

    def __init__(self, mentor_root: Path):
        self.mentor_root = Path(mentor_root)
        self.catalogo_processados_path = self.mentor_root / "PROCESSADOS" / "catalogo.json"
        self.catalogo_fontes_path = self.mentor_root / "FONTES" / "catalogo_fontes.json"

        # Load catalogs
        self.catalogo_processados = self._load_catalogo_processados()
        self.catalogo_fontes = self._load_catalogo_fontes()

    def _load_catalogo_processados(self) -> Dict:
        """Load PROCESSADOS/catalogo.json"""
        if not self.catalogo_processados_path.exists():
            return {'arquivos': []}

        with open(self.catalogo_processados_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _load_catalogo_fontes(self) -> Dict:
        """Load FONTES/catalogo_fontes.json"""
        if not self.catalogo_fontes_path.exists():
            return {'fontes': []}

        with open(self.catalogo_fontes_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def search_processados(self, query: str, top_k: int = 3) -> List[SearchResult]:
        """Search in PROCESSADOS/ (internal knowledge)"""
        results = []
        query_lower = query.lower()

        for arquivo in self.catalogo_processados.get('arquivos', []):
            score = 0.0

            # Match categoria
            if query_lower in arquivo.get('categoria', '').lower():
                score += 3.0

            # Match assunto
            if query_lower in arquivo.get('assunto', '').lower():
                score += 2.0

            # Match tags
            tags = arquivo.get('tags', [])
            for tag in tags:
                if query_lower in tag.lower():
                    score += 1.0

            # Match aplicacao
            aplicacao = arquivo.get('aplicacao', '')
            if query_lower in aplicacao.lower():
                score += 1.5

            if score > 0:
                results.append(SearchResult(
                    source_type='processados',
                    file_path=str(self.mentor_root / "PROCESSADOS" / arquivo['arquivo']),
                    categoria=arquivo.get('categoria', ''),
                    assunto=arquivo.get('assunto', ''),
                    relevance_score=score,
                    tags=tags
                ))

        # Sort by relevance
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:top_k]

    def search_fontes(self, query: str, top_k: int = 3) -> List[SearchResult]:
        """Search in FONTES/ (external documentation)"""
        results = []
        query_lower = query.lower()

        for fonte in self.catalogo_fontes.get('fontes', []):
            score = 0.0

            # Only search active fontes
            if fonte.get('status') != 'active':
                continue

            # Match categoria
            if query_lower in fonte.get('categoria', '').lower():
                score += 3.0

            # Match plataforma
            if query_lower in fonte.get('plataforma', '').lower():
                score += 3.0

            # Match nome
            if query_lower in fonte.get('nome', '').lower():
                score += 2.0

            # Match topics
            topics = fonte.get('topics', [])
            for topic in topics:
                if query_lower in topic.lower():
                    score += 2.0

            # Match aplicacao
            aplicacao = fonte.get('aplicacao', [])
            for app in aplicacao:
                if query_lower in app.lower():
                    score += 1.5

            if score > 0:
                # Find actual documentation files
                categoria = fonte['categoria']
                plataforma = fonte['plataforma']
                fonte_dir = self.mentor_root / "FONTES" / categoria / plataforma

                # Get list of files in fonte directory
                arquivos_locais = []
                if fonte_dir.exists():
                    arquivos_locais = [str(f) for f in fonte_dir.glob("*.md")
                                     if f.name != "README.md"]

                results.append(SearchResult(
                    source_type='fontes',
                    file_path=str(fonte_dir) if fonte_dir.exists() else None,
                    categoria=categoria,
                    assunto=plataforma,
                    relevance_score=score,
                    fonte_id=fonte['id'],
                    plataforma=plataforma,
                    url_oficial=fonte.get('url_oficial'),
                    topics=topics
                ))

        # Sort by relevance
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        return results[:top_k]

    def search_unified(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """
        Unified search across both PROCESSADOS and FONTES
        Returns combined results sorted by relevance
        """
        # Search both sources
        processados_results = self.search_processados(query, top_k=top_k)
        fontes_results = self.search_fontes(query, top_k=top_k)

        # Combine and sort
        all_results = processados_results + fontes_results
        all_results.sort(key=lambda x: x.relevance_score, reverse=True)

        return all_results[:top_k]

    def get_fonte_details(self, fonte_id: str) -> Optional[Dict]:
        """Get detailed information about a specific fonte"""
        for fonte in self.catalogo_fontes.get('fontes', []):
            if fonte['id'] == fonte_id:
                return fonte
        return None

    def should_search_fontes(self, query: str) -> bool:
        """
        Determine if query should also search FONTES
        Returns True for queries about external platforms/APIs
        """
        # Keywords that indicate external documentation search
        fontes_keywords = [
            # LLM platforms
            'anthropic', 'claude', 'openai', 'gpt', 'google', 'gemini', 'cohere',
            'api', 'llm', 'prompt engineering', 'tool use', 'function calling',
            'streaming', 'vision', 'embeddings', 'fine tuning',

            # Marketplaces
            'mercado livre', 'mercadolivre', 'ml', 'shopee', 'amazon', 'magalu',
            'magazine luiza', 'marketplace api', 'seo ml', 'listing api',

            # Frameworks
            'langchain', 'vercel', 'ai sdk', 'llamaindex', 'crewai',
            'rag', 'agents', 'chains', 'tools', 'vector store',

            # E-commerce
            'seo', 'google search', 'copywriting', 'conversion', 'cro',
            'analytics', 'ga4', 'google analytics'
        ]

        query_lower = query.lower()
        return any(keyword in query_lower for keyword in fontes_keywords)

    def smart_search(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """
        Smart search that decides whether to search FONTES based on query
        """
        # Always search PROCESSADOS
        processados_results = self.search_processados(query, top_k=top_k)

        # Conditionally search FONTES
        if self.should_search_fontes(query):
            fontes_results = self.search_fontes(query, top_k=top_k)

            # Combine results
            all_results = processados_results + fontes_results
            all_results.sort(key=lambda x: x.relevance_score, reverse=True)
            return all_results[:top_k]

        return processados_results


# Example usage
if __name__ == "__main__":
    # Initialize scout
    mentor_root = Path(__file__).parent.parent
    scout = ScoutFontes(mentor_root)

    # Example searches
    queries = [
        "como otimizar títulos no mercado livre",  # Should search both
        "anthropic claude api",  # Should search FONTES
        "prompt engineering best practices",  # Should search FONTES
        "estratégia de precificação",  # Should search PROCESSADOS only
    ]

    for query in queries:
        print(f"\n🔍 Query: {query}")
        print(f"   Should search FONTES? {scout.should_search_fontes(query)}")

        results = scout.smart_search(query, top_k=3)

        for i, result in enumerate(results, 1):
            print(f"\n   {i}. [{result.source_type.upper()}] {result.categoria} - {result.assunto}")
            print(f"      Score: {result.relevance_score:.2f}")
            if result.url_oficial:
                print(f"      URL: {result.url_oficial}")
