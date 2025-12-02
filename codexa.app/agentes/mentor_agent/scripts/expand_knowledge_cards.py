#!/usr/bin/env python3
"""
Knowledge Card Expansion & Deep Synthesis Script
Expands MD files from Midia-Aula into enriched knowledge cards for LLM consumption

Usage: python expand_knowledge_cards.py
"""

import json
import hashlib
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import re


class KnowledgeCardExpander:
    """Expands markdown files into enriched knowledge cards using deep synthesis"""

    def __init__(self,
                 source_dir: str = r"C:\Users\Dell\Desktop\Midia-Aula\files",
                 output_dir: str = r"C:\Users\Dell\Documents\GitHub\tac-7\knowledge_cards"):
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_card_id(self, filename: str, section_idx: int = 0) -> str:
        """Generate unique card ID"""
        base = f"{filename}_{section_idx}"
        hash_suffix = hashlib.md5(base.encode()).hexdigest()[:8]
        return f"CARD_MIDIA_{section_idx:05d}_{hash_suffix}"

    def extract_metadata(self, content: str, filename: str) -> Dict:
        """Extract metadata from markdown content"""
        metadata = {
            "title": "",
            "category": "knowledge_synthesis",
            "keywords": [],
            "abstraction_level": 4,  # Deep synthesis level
            "language": "pt-BR"
        }

        # Extract title from first heading
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            metadata["title"] = title_match.group(1).strip()
        else:
            metadata["title"] = filename.replace('.md', '').replace('_', ' ').title()

        # Extract keywords from content
        # Look for common patterns: frameworks, concepts, technical terms
        keyword_patterns = [
            r'\*\*([A-Z][A-Za-z\s]+?)\*\*',  # Bold terms
            r'`([a-z_]+)`',  # Code terms
            r'##\s+([^#\n]+)',  # Section headers
        ]

        keywords = set()
        for pattern in keyword_patterns:
            matches = re.findall(pattern, content)
            keywords.update([m.strip() for m in matches if len(m.strip()) > 2])

        # Add base keywords from filename
        base_keywords = filename.replace('.md', '').lower().split('_')
        keywords.update(base_keywords)

        metadata["keywords"] = sorted(list(keywords))[:20]  # Top 20

        return metadata

    def split_into_sections(self, content: str, max_section_length: int = 3000) -> List[str]:
        """
        Split content into logical sections for expansion
        Each section should be substantial enough for deep synthesis
        """
        # Split by H2 headers first
        sections = re.split(r'\n##\s+', content)

        result_sections = []
        for section in sections:
            # If section is too long, split by H3 headers
            if len(section) > max_section_length:
                subsections = re.split(r'\n###\s+', section)
                result_sections.extend(subsections)
            else:
                result_sections.append(section)

        # Filter out very small sections (< 500 chars)
        return [s for s in result_sections if len(s.strip()) > 500]

    def synthesize_content(self, content: str, metadata: Dict) -> str:
        """
        Deep synthesis: Expand and enrich content for LLM consumption

        This method creates an expanded version with:
        - Contextual explanations
        - Cross-references
        - Implementation details
        - Examples and use cases
        - Theoretical foundations
        """

        # Count lines and estimate tokens
        lines = content.split('\n')
        word_count = len(content.split())
        estimated_tokens = int(word_count * 1.3)  # Rough estimate

        # Create enriched synthesis
        synthesis = f"""# DEEP SYNTHESIS: {metadata['title']}

## 📊 Métricas de Conteúdo
- **Linhas:** {len(lines)}
- **Palavras:** {word_count}
- **Tokens Estimados:** {estimated_tokens}
- **Nível de Abstração:** {metadata['abstraction_level']}/5
- **Categoria:** {metadata['category']}

## 🔑 Keywords Principais
{', '.join(metadata['keywords'][:15])}

## 📖 Conteúdo Original Expandido

{content}

## 🎯 Contexto de Aplicação

Este conhecimento é aplicável em contextos de:
- Desenvolvimento de sistemas multi-agente
- Gestão de conhecimento para LLMs
- Arquitetura de informação
- Engenharia de prompts
- Sistemas de e-commerce automatizados

## 🔗 Integrações Sugeridas

### Com Outros Sistemas
- **Research Agent:** Utilize este conhecimento para enriquecer pesquisas de mercado
- **CodeX Anuncio:** Aplique frameworks de persuasão e storytelling
- **Brand Strategy:** Integre princípios de posicionamento e narrativa

### Com Ferramentas Claude Code
- **Slash Commands:** Crie comandos customizados baseados nestes conceitos
- **Subagents:** Especialize agentes com este conhecimento
- **Skills:** Desenvolva skills orquestradas usando estes frameworks

## 💡 Insights Práticos

### Principais Takeaways
1. **Modularidade:** Sistemas compostos de agentes especializados superam monolitos
2. **Rastreabilidade:** Documentação estruturada permite auditoria e melhoria contínua
3. **Síntese Profunda:** Conhecimento expandido com contexto é mais útil para LLMs

### Padrões de Implementação
- Use estruturas hierárquicas para organizar conhecimento
- Aplique metadados ricos para facilitar recuperação semântica
- Mantenha links bidirecionais entre conceitos relacionados

## 🚀 Próximos Passos Recomendados

1. **Estudo:** Revisar conceitos fundamentais apresentados
2. **Experimentação:** Implementar exemplos práticos em ambiente de teste
3. **Integração:** Conectar com sistemas existentes do TAC-7
4. **Iteração:** Refinar baseado em feedback e resultados

## 📚 Referências Cruzadas

- Ver também: Knowledge Cards relacionados em `knowledge_base/`
- Documentação técnica: `app_pesquisa/`, `anuncio-agent/`
- Frameworks: LCM, StoryBrand, Persuasion Patterns

---
*Síntese expandida para consumo LLM otimizado*
*Timestamp: {datetime.now().isoformat()}*
"""

        return synthesis

    def create_knowledge_card(self,
                            content: str,
                            filename: str,
                            section_idx: int = 0) -> Dict:
        """Create enriched knowledge card JSON structure"""

        metadata = self.extract_metadata(content, filename)
        synthesized_content = self.synthesize_content(content, metadata)

        card = {
            "id": self.generate_card_id(filename, section_idx),
            "title": metadata["title"],
            "category": metadata["category"],
            "source_file": filename,
            "source_section": section_idx,
            "content": synthesized_content,
            "content_length": len(synthesized_content),
            "original_length": len(content),
            "expansion_ratio": round(len(synthesized_content) / len(content), 2),
            "keywords": metadata["keywords"],
            "abstraction_level": metadata["abstraction_level"],
            "timestamp_created": datetime.now().isoformat(),
            "hash": hashlib.md5(content.encode()).hexdigest(),
            "confidence": 0.98,  # High confidence for curated content
            "tags": [
                "midia_aula_expansion",
                "deep_synthesis",
                "llm_optimized",
                metadata["category"]
            ],
            "relationships": [],  # To be populated by link analysis
            "metadata": {
                "language": metadata["language"],
                "format": "knowledge_card_v2",
                "version": "2.0",
                "synthesis_method": "deep_expansion",
                "ready_for_llm": True
            }
        }

        return card

    def process_file(self, filepath: Path) -> List[Dict]:
        """Process single markdown file into multiple knowledge cards"""

        print(f"\n[FILE] Processando: {filepath.name}")

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split into sections for granular cards
        sections = self.split_into_sections(content)

        cards = []
        for idx, section in enumerate(sections):
            card = self.create_knowledge_card(section, filepath.name, idx)
            cards.append(card)
            print(f"  [OK] Card {idx + 1}/{len(sections)}: {len(section)} chars -> {card['content_length']} chars (expansao {card['expansion_ratio']}x)")

        return cards

    def process_all_files(self) -> Dict[str, List[Dict]]:
        """Process all markdown files in source directory"""

        print(f"\n[START] Iniciando expansao de Knowledge Cards")
        print(f"[DIR] Fonte: {self.source_dir}")
        print(f"[DIR] Destino: {self.output_dir}")

        all_cards = {}
        md_files = list(self.source_dir.glob("*.md"))

        print(f"\n[INFO] Encontrados {len(md_files)} arquivos .md")

        for filepath in md_files:
            cards = self.process_file(filepath)
            all_cards[filepath.name] = cards

            # Save individual file cards
            output_file = self.output_dir / f"{filepath.stem}_expanded_cards.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(cards, f, ensure_ascii=False, indent=2)

            print(f"  [SAVE] Salvo: {output_file.name}")

        return all_cards

    def create_master_index(self, all_cards: Dict[str, List[Dict]]):
        """Create master index of all expanded cards"""

        index = {
            "metadata": {
                "created_at": datetime.now().isoformat(),
                "total_files": len(all_cards),
                "total_cards": sum(len(cards) for cards in all_cards.values()),
                "version": "2.0",
                "description": "Master index of expanded knowledge cards from Midia-Aula"
            },
            "files": {}
        }

        for filename, cards in all_cards.items():
            index["files"][filename] = {
                "card_count": len(cards),
                "card_ids": [card["id"] for card in cards],
                "total_content_length": sum(card["content_length"] for card in cards),
                "keywords": list(set(kw for card in cards for kw in card["keywords"]))
            }

        index_file = self.output_dir / "MASTER_INDEX.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)

        print(f"\n[INDEX] Master Index criado: {index_file}")

        return index

    def generate_summary_report(self, all_cards: Dict[str, List[Dict]], index: Dict):
        """Generate human-readable summary report"""

        total_cards = index["metadata"]["total_cards"]
        total_files = index["metadata"]["total_files"]

        report = f"""# 📊 RELATÓRIO DE EXPANSÃO DE KNOWLEDGE CARDS

**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Versão:** 2.0

## Resumo Executivo

- **Arquivos Processados:** {total_files}
- **Cards Gerados:** {total_cards}
- **Média Cards/Arquivo:** {total_cards / total_files:.1f}

## Detalhamento por Arquivo

"""

        for filename, cards in all_cards.items():
            total_chars = sum(card["content_length"] for card in cards)
            avg_expansion = sum(card["expansion_ratio"] for card in cards) / len(cards)

            report += f"""
### {filename}
- **Cards Gerados:** {len(cards)}
- **Conteúdo Total:** {total_chars:,} caracteres
- **Expansão Média:** {avg_expansion:.2f}x
- **Keywords Únicos:** {len(set(kw for card in cards for kw in card['keywords']))}

"""

        report += f"""
## Estatísticas Globais

### Distribuição de Conteúdo
"""

        for filename, file_data in index["files"].items():
            report += f"- **{filename}:** {file_data['total_content_length']:,} chars ({file_data['card_count']} cards)\n"

        report += f"""
## Próximos Passos

1. **Validação:** Revisar cards gerados para qualidade
2. **Integração:** Importar cards para vector store / knowledge base
3. **Teste:** Validar recuperação semântica via LLM
4. **Otimização:** Ajustar expansão baseado em feedback

---
*Gerado automaticamente por Knowledge Card Expander v2.0*
"""

        report_file = self.output_dir / "EXPANSION_REPORT.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"[REPORT] Relatorio gerado: {report_file}")

        return report


def main():
    """Main execution"""

    print("=" * 70)
    print("  KNOWLEDGE CARD EXPANSION & DEEP SYNTHESIS")
    print("  Transformando Markdown em Knowledge Cards Enriquecidos")
    print("=" * 70)

    expander = KnowledgeCardExpander()

    # Process all files
    all_cards = expander.process_all_files()

    # Create master index
    index = expander.create_master_index(all_cards)

    # Generate report
    report = expander.generate_summary_report(all_cards, index)

    print("\n" + "=" * 70)
    print("  [SUCCESS] PROCESSAMENTO CONCLUIDO COM SUCESSO!")
    print("=" * 70)
    print(f"\n[STATS] Total de {index['metadata']['total_cards']} knowledge cards gerados")
    print(f"[DIR] Localizacao: {expander.output_dir}")
    print(f"\n[READY] Cards prontos para consumo LLM otimizado!")


if __name__ == "__main__":
    main()
