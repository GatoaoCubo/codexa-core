#!/usr/bin/env python3
"""
Auto-Mapper - Sugere mapeamentos automáticos de versículos para agentes

Purpose: Analisar CAPITULOS novos e sugerir quais versículos devem ir para quais agentes
Input: Novo CAPITULO ou todos CAPITULOS
Output: Sugestões de mappings para knowledge_map.json

Usage:
    # Analisar novo CAPITULO e sugerir mappings
    python auto_mapper.py --capitulo CAPITULO_marketplace_63

    # Analisar todos CAPITULOS e gerar mappings completos
    python auto_mapper.py --scan-all

    # Aplicar sugestões automaticamente (adicionar ao knowledge_map.json)
    python auto_mapper.py --capitulo CAPITULO_marketplace_63 --auto-apply

Version: 1.0.0
Author: CODEXA Meta-Construction System
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import sys

# Add config to path for centralized path management
sys.path.insert(0, str(Path(__file__).parent.parent / 'config'))
from paths import PATH_PROCESSADOS, PATH_DISTRIBUICAO


class AutoMapper:
    """Mapeia automaticamente versículos para agentes"""

    def __init__(
        self,
        processados_dir: Optional[Path] = None,
        knowledge_map_path: Optional[Path] = None
    ):
        """
        Initialize auto-mapper

        Args:
            processados_dir: Path to PROCESSADOS/ directory
            knowledge_map_path: Path to knowledge_map.json
        """
        if processados_dir is None:
            processados_dir = PATH_PROCESSADOS

        if knowledge_map_path is None:
            knowledge_map_path = PATH_DISTRIBUICAO / "knowledge_map.json"

        self.processados_dir = Path(processados_dir)
        self.knowledge_map_path = Path(knowledge_map_path)

        # Load knowledge map
        with open(self.knowledge_map_path, "r", encoding="utf-8") as f:
            self.knowledge_map = json.load(f)

        # Agent profiles (what each agent needs)
        self.agent_profiles = {
            "anuncio_agent": {
                "prompts": {
                    "20_titulo_generator.md": {
                        "keywords": ["titulo", "seo", "keywords", "densidade", "marketplace", "otimizacao", "algoritmo", "imagem", "thumbnail", "visual", "foto"],
                        "themes": ["marketplace_optimization", "copywriting", "visual_design"],
                        "max_versiculos": 5
                    },
                    "40_bullet_points.md": {
                        "keywords": ["bullet", "features", "beneficios", "persuasao", "conversao", "imagem", "visual", "infografico"],
                        "themes": ["copywriting", "marketplace_optimization", "visual_design"],
                        "max_versiculos": 4
                    },
                    "50_descricao_builder.md": {
                        "keywords": ["descricao", "storytelling", "narrativa", "copy", "conversao", "imagem", "visual", "foto", "lifestyle"],
                        "themes": ["copywriting", "marketplace_optimization", "visual_design"],
                        "max_versiculos": 4
                    }
                }
            },
            "pesquisa_agent": {
                "prompts": {
                    "competitor_analysis.md": {
                        "keywords": ["competitiva", "analise", "concorrentes", "mercado", "gaps", "oportunidades"],
                        "themes": ["analise", "marketplace_optimization"],
                        "max_versiculos": 3
                    },
                    "seo_taxonomy.md": {
                        "keywords": ["seo", "taxonomia", "categorias", "keywords", "busca"],
                        "themes": ["marketplace_optimization"],
                        "max_versiculos": 3
                    }
                }
            },
            "brand_agent": {
                "prompts": {
                    "brand_strategy.md": {
                        "keywords": ["branding", "identidade", "posicionamento", "diferenciacao", "marca", "visual", "design", "paleta", "cores"],
                        "themes": ["branding", "estrategia", "visual_design"],
                        "max_versiculos": 4
                    }
                }
            }
        }

    def analyze_versiculo(self, versiculo_content: str) -> Dict:
        """
        Analyze versículo content to extract metadata

        Args:
            versiculo_content: Full versículo markdown content

        Returns:
            Dict with extracted metadata (title, keywords, category, quality)
        """
        metadata = {
            "title": None,
            "category": None,
            "quality": 0.0,
            "keywords": [],
            "tags": []
        }

        # Extract title (first # header)
        title_match = re.search(r'^#\s+(.+)$', versiculo_content, re.MULTILINE)
        if title_match:
            metadata["title"] = title_match.group(1).strip()

        # Extract category
        cat_match = re.search(r'\*\*Categoria\*\*:\s*(.+)', versiculo_content)
        if cat_match:
            metadata["category"] = cat_match.group(1).strip()

        # Extract quality
        qual_match = re.search(r'\*\*Qualidade\*\*:\s*([\d.]+)', versiculo_content)
        if qual_match:
            metadata["quality"] = float(qual_match.group(1))

        # Extract keywords (case-insensitive words in content)
        content_lower = versiculo_content.lower()

        # Common e-commerce keywords
        all_keywords = [
            "titulo", "seo", "keywords", "densidade", "marketplace", "otimizacao",
            "bullet", "features", "beneficios", "persuasao", "conversao",
            "descricao", "storytelling", "narrativa", "copy",
            "competitiva", "analise", "concorrentes", "mercado", "gaps",
            "branding", "identidade", "posicionamento", "diferenciacao",
            "algoritmo", "ranking", "busca", "visibilidade"
        ]

        for kw in all_keywords:
            if kw in content_lower:
                metadata["keywords"].append(kw)

        # Extract tags
        tags_match = re.search(r'\*\*Tags\*\*:\s*(.+)', versiculo_content)
        if tags_match:
            tags_str = tags_match.group(1).strip()
            metadata["tags"] = [t.strip() for t in tags_str.split(',')]

        return metadata

    def scan_capitulo(self, capitulo_name: str) -> List[Dict]:
        """
        Scan CAPITULO and extract all versículos with metadata

        Args:
            capitulo_name: CAPITULO name (ex: "CAPITULO_marketplace_01")

        Returns:
            List of versículo dicts with metadata
        """
        capitulo_file = self.processados_dir / f"{capitulo_name}.md"

        if not capitulo_file.exists():
            raise FileNotFoundError(f"CAPITULO not found: {capitulo_file}")

        # Read file
        with open(capitulo_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Find all versículo markers
        marker_pattern = r"<!-- VERSÍCULO (\d+)/(\d+) - ([^(]+)\((\d+) linhas\) -->"
        markers = list(re.finditer(marker_pattern, content))

        versiculos = []

        for idx, marker in enumerate(markers):
            versiculo_num = int(marker.group(1))
            total_versiculos = int(marker.group(2))
            filename = marker.group(3).strip()
            num_linhas = int(marker.group(4))

            # Extract content
            start_pos = marker.end()
            if idx + 1 < len(markers):
                end_pos = markers[idx + 1].start()
            else:
                end_pos = len(content)

            versiculo_content = content[start_pos:end_pos].strip()

            # Analyze content
            metadata = self.analyze_versiculo(versiculo_content)

            versiculos.append({
                "ref": f"{capitulo_name}:versiculo_{versiculo_num}",
                "num": versiculo_num,
                "total": total_versiculos,
                "filename": filename,
                "num_linhas": num_linhas,
                "metadata": metadata,
                "preview": versiculo_content[:200] + "..."
            })

        return versiculos

    def calculate_relevance(
        self,
        versiculo: Dict,
        prompt_config: Dict
    ) -> Tuple[float, List[str]]:
        """
        Calculate relevance score between versículo and prompt

        Args:
            versiculo: Versículo dict with metadata
            prompt_config: Prompt config from agent_profiles

        Returns:
            Tuple of (relevance_score, matching_keywords)
        """
        metadata = versiculo["metadata"]
        score = 0.0
        matching = []

        # Check keywords match
        prompt_keywords = set(prompt_config["keywords"])
        versiculo_keywords = set(metadata["keywords"])

        common_keywords = prompt_keywords & versiculo_keywords

        if common_keywords:
            # Score based on proportion of matching keywords
            keyword_score = len(common_keywords) / len(prompt_keywords)
            score += keyword_score * 0.6  # 60% weight
            matching.extend(common_keywords)

        # Check theme match
        prompt_themes = prompt_config.get("themes", [])
        versiculo_category = metadata.get("category", "")

        for theme in prompt_themes:
            if theme in versiculo_category:
                score += 0.3  # 30% weight
                matching.append(f"theme:{theme}")
                break

        # Boost by quality
        quality_boost = metadata.get("quality", 0.0) * 0.1  # 10% weight
        score += quality_boost

        # Normalize to 0-1
        score = min(1.0, score)

        return score, matching

    def suggest_mappings(
        self,
        capitulo_name: str,
        min_relevance: float = 0.30
    ) -> Dict:
        """
        Suggest mappings for a CAPITULO

        Args:
            capitulo_name: CAPITULO name (ex: "CAPITULO_marketplace_01")
            min_relevance: Minimum relevance score to suggest (default 0.30)

        Returns:
            Dict with suggestions per agent/prompt
        """
        print(f"\n🔍 Scanning {capitulo_name}...")

        # Scan CAPITULO
        versiculos = self.scan_capitulo(capitulo_name)
        print(f"   Found {len(versiculos)} versículos")

        suggestions = {}

        # For each agent
        for agent_name, agent_config in self.agent_profiles.items():
            suggestions[agent_name] = {}

            # For each prompt
            for prompt_file, prompt_config in agent_config["prompts"].items():
                print(f"\n📊 Analyzing for {agent_name}/{prompt_file}...")

                candidates = []

                # Score each versículo
                for versiculo in versiculos:
                    relevance, matching = self.calculate_relevance(
                        versiculo,
                        prompt_config
                    )

                    if relevance >= min_relevance:
                        candidates.append({
                            "versiculo": versiculo,
                            "relevance": relevance,
                            "matching": matching
                        })

                # Sort by relevance
                candidates.sort(key=lambda c: c["relevance"], reverse=True)

                # Take top N
                max_versiculos = prompt_config.get("max_versiculos", 3)
                top_candidates = candidates[:max_versiculos]

                if top_candidates:
                    suggestions[agent_name][prompt_file] = top_candidates
                    print(f"   ✅ Found {len(top_candidates)} suggestions (relevance ≥ {min_relevance:.2f})")
                else:
                    print(f"   ⚠️  No relevant versículos found (min relevance: {min_relevance:.2f})")

        return suggestions

    def format_suggestions(self, suggestions: Dict) -> str:
        """Format suggestions as human-readable text"""
        lines = []
        lines.append("\n" + "="*70)
        lines.append("📋 MAPPING SUGGESTIONS")
        lines.append("="*70)

        for agent_name, prompts in suggestions.items():
            if not prompts:
                continue

            lines.append(f"\n## {agent_name}")

            for prompt_file, candidates in prompts.items():
                lines.append(f"\n### {prompt_file}")
                lines.append(f"   Suggested versículos: {len(candidates)}")

                for i, candidate in enumerate(candidates, 1):
                    v = candidate["versiculo"]
                    rel = candidate["relevance"]
                    matching = candidate["matching"]

                    lines.append(f"\n   [{i}] {v['ref']}")
                    lines.append(f"       Título: {v['metadata']['title']}")
                    lines.append(f"       Relevância: {rel:.2f}")
                    lines.append(f"       Matching: {', '.join(matching)}")
                    lines.append(f"       Quality: {v['metadata']['quality']:.2f}")
                    lines.append(f"       Preview: {v['preview'][:80]}...")

        return "\n".join(lines)

    def apply_suggestions(
        self,
        suggestions: Dict,
        auto_apply: bool = False
    ) -> None:
        """
        Apply suggestions to knowledge_map.json

        Args:
            suggestions: Suggestions dict from suggest_mappings()
            auto_apply: If True, apply without confirmation
        """
        if not auto_apply:
            print("\n⚠️  This will modify knowledge_map.json")
            response = input("Continue? (y/n): ")
            if response.lower() != 'y':
                print("Aborted.")
                return

        # Load current map
        with open(self.knowledge_map_path, "r", encoding="utf-8") as f:
            km = json.load(f)

        mappings_added = 0

        # Add new mappings
        for agent_name, prompts in suggestions.items():
            for prompt_file, candidates in prompts.items():
                # Check if mapping already exists
                mapping_id = f"{agent_name}_{prompt_file.replace('.md', '')}_auto"

                existing = next(
                    (m for m in km["mappings"] if m["id"] == mapping_id),
                    None
                )

                if existing:
                    print(f"⚠️  Mapping {mapping_id} already exists, skipping")
                    continue

                # Create new mapping
                new_mapping = {
                    "id": mapping_id,
                    "agent": agent_name,
                    "prompt_file": f"prompts/{prompt_file}",
                    "inject_section": "## 📚 CONHECIMENTO TÉCNICO",
                    "inject_position": {
                        "anchor": "## Otimização por Marketplace",
                        "placement": "before",
                        "offset": -2
                    },
                    "source_themes": list(set(
                        self.agent_profiles[agent_name]["prompts"][prompt_file]["themes"]
                    )),
                    "versiculos": [],
                    "max_tokens": 1500,
                    "compression_strategy": "top_priority_versiculos",
                    "update_frequency": "on_capitulo_change",
                    "auto_generated": True,
                    "generated_at": datetime.now().isoformat()
                }

                # Add versículos
                for i, candidate in enumerate(candidates, 1):
                    v = candidate["versiculo"]

                    new_mapping["versiculos"].append({
                        "ref": v["ref"],
                        "tema": v["metadata"]["title"] or "Conhecimento Técnico",
                        "relevance": round(candidate["relevance"], 2),
                        "priority": i,
                        "tags": v["metadata"].get("tags", [])
                    })

                km["mappings"].append(new_mapping)
                mappings_added += 1
                print(f"✅ Added mapping: {mapping_id}")

        # Save updated map
        if mappings_added > 0:
            # Backup original
            backup_path = self.knowledge_map_path.with_suffix(
                f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            with open(backup_path, "w", encoding="utf-8") as f:
                json.dump(self.knowledge_map, f, indent=2, ensure_ascii=False)

            # Save updated
            with open(self.knowledge_map_path, "w", encoding="utf-8") as f:
                json.dump(km, f, indent=2, ensure_ascii=False)

            print(f"\n✅ Added {mappings_added} new mappings to knowledge_map.json")
            print(f"💾 Backup saved: {backup_path}")
        else:
            print("\n⚠️  No new mappings added (all already exist)")


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Auto-suggest versículo mappings for agents"
    )
    parser.add_argument(
        "--capitulo",
        help="CAPITULO name to analyze (ex: CAPITULO_marketplace_01)"
    )
    parser.add_argument(
        "--scan-all",
        action="store_true",
        help="Scan all CAPITULOS and suggest mappings"
    )
    parser.add_argument(
        "--auto-apply",
        action="store_true",
        help="Automatically apply suggestions (no confirmation)"
    )
    parser.add_argument(
        "--min-relevance",
        type=float,
        default=0.30,
        help="Minimum relevance score (0.0-1.0, default 0.30)"
    )

    args = parser.parse_args()

    # Validate args
    if not args.capitulo and not args.scan_all:
        parser.error("Must specify --capitulo or --scan-all")

    try:
        # Fix Windows encoding
        if sys.platform == 'win32':
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

        # Create auto-mapper
        mapper = AutoMapper()

        if args.capitulo:
            # Analyze single CAPITULO
            suggestions = mapper.suggest_mappings(
                args.capitulo,
                min_relevance=args.min_relevance
            )

            # Print suggestions
            print(mapper.format_suggestions(suggestions))

            # Apply if requested
            if suggestions and (args.auto_apply or input("\nApply suggestions? (y/n): ").lower() == 'y'):
                mapper.apply_suggestions(suggestions, auto_apply=True)

        elif args.scan_all:
            # Scan all CAPITULOS
            capitulos = list(mapper.processados_dir.glob("CAPITULO_*.md"))
            print(f"\nFound {len(capitulos)} CAPITULOS to scan")

            all_suggestions = {}

            for capitulo_file in capitulos:
                capitulo_name = capitulo_file.stem

                try:
                    suggestions = mapper.suggest_mappings(
                        capitulo_name,
                        min_relevance=args.min_relevance
                    )

                    # Merge suggestions
                    for agent, prompts in suggestions.items():
                        if agent not in all_suggestions:
                            all_suggestions[agent] = {}
                        for prompt, candidates in prompts.items():
                            if prompt not in all_suggestions[agent]:
                                all_suggestions[agent][prompt] = []
                            all_suggestions[agent][prompt].extend(candidates)

                except Exception as e:
                    print(f"⚠️  Error scanning {capitulo_name}: {e}")
                    continue

            # Print all suggestions
            print(mapper.format_suggestions(all_suggestions))

            # Apply if requested
            if all_suggestions and (args.auto_apply or input("\nApply all suggestions? (y/n): ").lower() == 'y'):
                mapper.apply_suggestions(all_suggestions, auto_apply=True)

        sys.exit(0)

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
