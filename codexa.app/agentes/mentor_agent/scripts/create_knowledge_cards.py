#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CREATE KNOWLEDGE CARDS
======================

Atomizes consolidated knowledge into small, independent knowledge cards.
Each card is a self-contained unit of knowledge with full metadata.

Purpose:
- Break down large consolidated documents into atomic units
- Create JSON/YAML cards with complete metadata
- Enable LLM consumption, retrieval, and fine-tuning
- Support semantic search and clustering

Author: Claude Code - Knowledge Engineering System
Date: 2025-11-03
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import hashlib
import uuid

# Add config to path for centralized path management
sys.path.insert(0, str(Path(__file__).parent.parent / 'config'))
from paths import CODEXA_APP

class KnowledgeCardCreator:
    """Creates atomic knowledge cards from consolidated documents."""

    def __init__(self, consolidated_dir: Path, output_dir: Path):
        self.consolidated_dir = consolidated_dir
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.stats = {
            'total_cards_created': 0,
            'files_processed': 0,
            'categories': {},
            'errors': []
        }

    def create_cards_from_consolidations(self) -> Dict:
        """Process all consolidated files and create knowledge cards."""
        print("[START] Creating Knowledge Cards from Consolidated Documents\n")

        for cons_file in sorted(self.consolidated_dir.glob("_CONSOLIDATED_*.md")):
            self._process_consolidated_file(cons_file)

        self._generate_summary_report()
        return self.stats

    def _process_consolidated_file(self, file_path: Path):
        """Process a single consolidated file."""
        print(f"[PROCESSING] {file_path.name}")

        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Extract category from filename
            category = self._extract_category(file_path.name)

            # Split by headers (h2 = ##)
            sections = re.split(r'\n## ', content)

            for i, section in enumerate(sections[1:], 1):  # Skip intro
                # Extract title and content
                lines = section.split('\n')
                title = lines[0].strip() if lines else "Untitled"
                card_content = '\n'.join(lines[1:]).strip()

                if len(card_content) > 50:  # Only create cards with meaningful content
                    card = self._create_card(
                        title=title,
                        content=card_content,
                        category=category,
                        source_file=file_path.name,
                        section_num=i
                    )
                    self._save_card(card, category)

            self.stats['files_processed'] += 1
            if category not in self.stats['categories']:
                self.stats['categories'][category] = 0
            self.stats['categories'][category] += 1

        except Exception as e:
            self.stats['errors'].append({
                'file': str(file_path),
                'error': str(e)
            })
            print(f"  [ERROR] {str(e)}")

    def _create_card(self, title: str, content: str, category: str,
                     source_file: str, section_num: int) -> Dict:
        """Create a knowledge card with full metadata."""

        # Generate unique ID
        card_id = f"CARD_{category.upper()}_{section_num}_{uuid.uuid4().hex[:8]}"

        # Extract keywords from content
        keywords = self._extract_keywords(title, content)

        # Calculate abstraction level (1-5)
        abstraction_level = self._calculate_abstraction(content)

        # Create card
        card = {
            "id": card_id,
            "title": title,
            "category": category,
            "source_file": source_file,
            "source_section": section_num,
            "content": content,
            "content_length": len(content),
            "keywords": keywords,
            "abstraction_level": abstraction_level,
            "timestamp_created": datetime.now().isoformat(),
            "hash": hashlib.sha256(content.encode()).hexdigest()[:16],
            "confidence": 0.95,
            "tags": self._generate_tags(category, abstraction_level),
            "relationships": [],  # Will be populated during linking phase
            "metadata": {
                "language": "pt-BR",
                "format": "knowledge_card",
                "version": "1.0"
            }
        }

        self.stats['total_cards_created'] += 1
        return card

    def _save_card(self, card: Dict, category: str):
        """Save card to JSON file."""
        category_dir = self.output_dir / category
        category_dir.mkdir(parents=True, exist_ok=True)

        output_file = category_dir / f"{card['id']}.json"

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(card, f, ensure_ascii=False, indent=2)

    def _extract_category(self, filename: str) -> str:
        """Extract category from consolidated filename."""
        # Remove _CONSOLIDATED_ prefix and .md suffix
        name = filename.replace("_CONSOLIDATED_", "").replace(".md", "")

        # Map to categories
        if "ecommerce" in name.lower():
            return "ecommerce"
        elif "lem" in name.lower() or "paddleocr" in name.lower():
            return "lem"
        elif "python" in name.lower():
            return "python"
        elif "research" in name.lower():
            return "research"
        elif "integration" in name.lower():
            return "integration"
        else:
            return "general"

    def _extract_keywords(self, title: str, content: str) -> List[str]:
        """Extract keywords from title and content."""
        # Simple keyword extraction - expand in production
        words = (title + " " + content[:500]).lower()

        # Remove common words
        stop_words = {
            'o', 'a', 'de', 'para', 'com', 'em', 'é', 'são', 'que', 'do',
            'the', 'a', 'an', 'and', 'or', 'is', 'are', 'this', 'that'
        }

        # Extract capitalized words and key terms
        keywords = []
        for word in re.findall(r'\b\w+\b', title):
            if len(word) > 3 and word.lower() not in stop_words:
                keywords.append(word)

        return list(dict.fromkeys(keywords))[:10]  # Deduplicate and limit

    def _calculate_abstraction(self, content: str) -> int:
        """Calculate abstraction level (1-5) based on content characteristics."""
        # Simple heuristic - expand in production
        level = 3  # Default to middle

        # High abstraction (5)
        if any(word in content.lower() for word in ['principle', 'concept', 'framework', 'paradigm']):
            level = 5
        # Low abstraction (1)
        elif any(word in content.lower() for word in ['code', 'script', 'example', 'configuration']):
            level = 1
        # Medium-high (4)
        elif any(word in content.lower() for word in ['architecture', 'design', 'pattern', 'strategy']):
            level = 4
        # Medium-low (2)
        elif any(word in content.lower() for word in ['implementation', 'procedure', 'process', 'method']):
            level = 2

        return level

    def _generate_tags(self, category: str, abstraction_level: int) -> List[str]:
        """Generate tags for the card."""
        tags = [category]

        # Add abstraction level tag
        abstraction_tags = {
            1: "concrete",
            2: "implementation",
            3: "intermediate",
            4: "architectural",
            5: "abstract"
        }
        tags.append(abstraction_tags.get(abstraction_level, "intermediate"))

        return tags

    def _generate_summary_report(self):
        """Generate summary report of card creation."""
        print("\n" + "="*70)
        print("[COMPLETE] Knowledge Card Creation Summary")
        print("="*70)
        print(f"  Cards created: {self.stats['total_cards_created']}")
        print(f"  Files processed: {self.stats['files_processed']}")
        print(f"  Errors: {len(self.stats['errors'])}")
        print(f"\n  Cards by category:")
        for cat, count in self.stats['categories'].items():
            print(f"    - {cat}: {count}")

        if self.stats['errors']:
            print(f"\n  Errors encountered:")
            for err in self.stats['errors']:
                print(f"    - {err['file']}: {err['error']}")

        print("="*70 + "\n")


def main():
    """Main entry point."""

    # Default paths using centralized config
    repo_root = CODEXA_APP
    consolidated_dir = repo_root / "app_docs" / "RAW_LCM"
    output_dir = consolidated_dir / "KNOWLEDGE_CARDS"

    print(f"Repository root: {repo_root}")
    print(f"Consolidated dir: {consolidated_dir}")
    print(f"Output dir: {output_dir}\n")

    # Create knowledge cards
    creator = KnowledgeCardCreator(consolidated_dir, output_dir)
    stats = creator.create_cards_from_consolidations()

    # Save statistics
    stats_file = consolidated_dir / "knowledge_cards_creation_stats.json"
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(f"Statistics saved to: {stats_file}")


if __name__ == "__main__":
    main()
