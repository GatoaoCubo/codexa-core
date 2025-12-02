#!/usr/bin/env python3
"""
Generate Knowledge Graph and Cross-References

Creates:
- Knowledge graph based on shared keywords
- Cross-reference index between cards
- Domain-specific indices
- Visualization exports (JSON for D3.js/NetworkX)
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from typing import List, Dict, Any, Set, Tuple


class KnowledgeGraphGenerator:
    """Generate knowledge graphs and cross-references from cards"""

    def __init__(self, cards_dir: str = "Cards_Conhecimento"):
        self.cards_dir = Path(cards_dir)
        self.cards = []
        self.graph = {
            "nodes": [],
            "edges": [],
            "clusters": defaultdict(list)
        }
        self.cross_refs = defaultdict(list)

    def load_cards(self):
        """Load all knowledge cards"""
        print("[INFO] Loading knowledge cards...")

        for card_file in self.cards_dir.glob("*.json"):
            if card_file.name.startswith("_"):
                continue

            try:
                with open(card_file, 'r', encoding='utf-8') as f:
                    card = json.load(f)

                card['_filename'] = card_file.name
                card['_file_id'] = card.get('file_id', card_file.stem)
                self.cards.append(card)

            except Exception as e:
                print(f"[WARNING] Failed to load {card_file}: {e}")

        print(f"[INFO] Loaded {len(self.cards)} cards")

    def build_keyword_graph(self, min_shared_keywords: int = 2):
        """Build graph based on shared keywords between cards"""
        print(f"\n[GRAPH] Building keyword-based graph (min {min_shared_keywords} shared keywords)...")

        # Create nodes
        for card in self.cards:
            node = {
                "id": card['_file_id'],
                "label": card.get('title', 'Untitled'),
                "category": card.get('category', 'unknown'),
                "keywords": card.get('keywords', []),
                "type": "card"
            }
            self.graph['nodes'].append(node)
            self.graph['clusters'][node['category']].append(node['id'])

        # Create edges based on shared keywords
        edge_count = 0
        for i, card1 in enumerate(self.cards):
            kw1 = set(card1.get('keywords', []))

            for card2 in self.cards[i+1:]:
                kw2 = set(card2.get('keywords', []))
                shared = kw1.intersection(kw2)

                if len(shared) >= min_shared_keywords:
                    edge = {
                        "source": card1['_file_id'],
                        "target": card2['_file_id'],
                        "weight": len(shared),
                        "shared_keywords": list(shared),
                        "type": "keyword_similarity"
                    }
                    self.graph['edges'].append(edge)
                    edge_count += 1

                    # Add to cross-references
                    self.cross_refs[card1['_file_id']].append({
                        "target": card2['_file_id'],
                        "target_title": card2.get('title', 'Untitled'),
                        "relation": "shares_keywords",
                        "shared_keywords": list(shared),
                        "strength": len(shared)
                    })

        print(f"[GRAPH] Created {len(self.graph['nodes'])} nodes and {edge_count} edges")
        print(f"[GRAPH] Found {len(self.graph['clusters'])} clusters")

    def find_domain_connections(self):
        """Find connections between different domains"""
        print("\n[CROSS-REF] Finding cross-domain connections...")

        cross_domain_links = []

        for edge in self.graph['edges']:
            source_node = next((n for n in self.graph['nodes'] if n['id'] == edge['source']), None)
            target_node = next((n for n in self.graph['nodes'] if n['id'] == edge['target']), None)

            if source_node and target_node:
                if source_node['category'] != target_node['category']:
                    cross_domain_links.append({
                        "from_domain": source_node['category'],
                        "to_domain": target_node['category'],
                        "source_card": edge['source'],
                        "target_card": edge['target'],
                        "shared_keywords": edge['shared_keywords'],
                        "weight": edge['weight']
                    })

        print(f"[CROSS-REF] Found {len(cross_domain_links)} cross-domain connections")

        return cross_domain_links

    def generate_domain_indices(self):
        """Generate specialized indices by domain"""
        print("\n[INDICES] Generating domain-specific indices...")

        domain_indices = {}

        for category, card_ids in self.graph['clusters'].items():
            # Get cards in this category
            category_cards = [c for c in self.cards if c.get('category') == category]

            # Aggregate keywords
            all_keywords = []
            for card in category_cards:
                all_keywords.extend(card.get('keywords', []))

            keyword_freq = Counter(all_keywords)

            domain_indices[category] = {
                "name": category,
                "card_count": len(card_ids),
                "cards": [
                    {
                        "id": c['_file_id'],
                        "title": c.get('title', 'Untitled'),
                        "keywords": c.get('keywords', [])
                    }
                    for c in category_cards
                ],
                "top_keywords": [
                    {"keyword": kw, "frequency": freq}
                    for kw, freq in keyword_freq.most_common(10)
                ],
                "total_unique_keywords": len(keyword_freq)
            }

        print(f"[INDICES] Created {len(domain_indices)} domain indices")

        return domain_indices

    def export_graph_d3(self, filename: str = "knowledge_graph_d3.json"):
        """Export graph in D3.js format"""
        output_path = self.cards_dir / filename

        d3_format = {
            "nodes": self.graph['nodes'],
            "links": self.graph['edges'],
            "metadata": {
                "generated": datetime.now().isoformat(),
                "total_nodes": len(self.graph['nodes']),
                "total_edges": len(self.graph['edges']),
                "clusters": len(self.graph['clusters'])
            }
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(d3_format, f, indent=2, ensure_ascii=False)

        print(f"[EXPORT] D3.js graph: {filename}")

    def export_cross_references(self, filename: str = "cross_references.json"):
        """Export cross-references index"""
        output_path = self.cards_dir / filename

        # Convert to regular dict for JSON serialization
        cross_refs_dict = dict(self.cross_refs)

        # Add metadata
        export_data = {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "total_cards": len(self.cards),
                "total_relationships": sum(len(refs) for refs in cross_refs_dict.values())
            },
            "cross_references": cross_refs_dict
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        print(f"[EXPORT] Cross-references: {filename}")

    def export_domain_indices(self, domain_indices: Dict, filename: str = "domain_indices.json"):
        """Export domain-specific indices"""
        output_path = self.cards_dir / filename

        export_data = {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "total_domains": len(domain_indices)
            },
            "domains": domain_indices
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        print(f"[EXPORT] Domain indices: {filename}")

    def generate_markdown_index(self, domain_indices: Dict):
        """Generate human-readable markdown index"""
        output_path = self.cards_dir.parent / "DOMAIN_INDEX.md"

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        content = f"""# Knowledge Domain Index

**Generated:** {timestamp}
**Total Cards:** {len(self.cards)}
**Total Domains:** {len(domain_indices)}

---

## Domains Overview

"""

        for domain, data in sorted(domain_indices.items(), key=lambda x: x[1]['card_count'], reverse=True):
            content += f"### {domain}\n\n"
            content += f"- **Cards:** {data['card_count']}\n"
            content += f"- **Unique Keywords:** {data['total_unique_keywords']}\n\n"

            content += "**Top Keywords:**\n"
            for kw_data in data['top_keywords'][:5]:
                content += f"- `{kw_data['keyword']}` ({kw_data['frequency']}x)\n"

            content += "\n**Cards in this domain:**\n"
            for card in data['cards'][:10]:  # Limit to 10 for readability
                content += f"- [{card['title']}](Cards_Conhecimento/{card['id']}.json)\n"

            if len(data['cards']) > 10:
                content += f"- ... and {len(data['cards']) - 10} more\n"

            content += "\n---\n\n"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[EXPORT] Markdown index: DOMAIN_INDEX.md")

    def generate_statistics(self):
        """Generate summary statistics"""
        print("\n" + "=" * 80)
        print("KNOWLEDGE GRAPH STATISTICS")
        print("=" * 80)

        print(f"\nCards: {len(self.cards)}")
        print(f"Nodes: {len(self.graph['nodes'])}")
        print(f"Edges: {len(self.graph['edges'])}")
        print(f"Clusters: {len(self.graph['clusters'])}")

        print("\nCluster distribution:")
        for category, card_ids in sorted(self.graph['clusters'].items(), key=lambda x: len(x[1]), reverse=True):
            print(f"  {category}: {len(card_ids)} cards")

        avg_connections = len(self.graph['edges']) * 2 / len(self.graph['nodes']) if self.graph['nodes'] else 0
        print(f"\nAverage connections per card: {avg_connections:.2f}")


def main():
    print("=" * 80)
    print("KNOWLEDGE GRAPH & CROSS-REFERENCE GENERATOR")
    print("=" * 80)

    generator = KnowledgeGraphGenerator()

    # Load cards
    generator.load_cards()

    # Build graph
    generator.build_keyword_graph(min_shared_keywords=2)

    # Find cross-domain connections
    cross_domain = generator.find_domain_connections()

    # Generate domain indices
    domain_indices = generator.generate_domain_indices()

    # Export everything
    print("\n" + "=" * 80)
    print("EXPORTING")
    print("=" * 80)

    generator.export_graph_d3()
    generator.export_cross_references()
    generator.export_domain_indices(domain_indices)
    generator.generate_markdown_index(domain_indices)

    # Statistics
    generator.generate_statistics()

    print("\n" + "=" * 80)
    print("COMPLETE")
    print("=" * 80)
    print("\nGenerated files:")
    print("- knowledge_graph_d3.json (for visualization)")
    print("- cross_references.json (relationships index)")
    print("- domain_indices.json (domain-specific indices)")
    print("- DOMAIN_INDEX.md (human-readable index)")


if __name__ == "__main__":
    main()
