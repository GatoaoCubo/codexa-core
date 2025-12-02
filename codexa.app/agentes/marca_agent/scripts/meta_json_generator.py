#!/usr/bin/env python3
"""
Brand Strategy .meta.json Generator
Version: 1.0.0
Date: 2025-11-14

Generates metadata JSON files for brand strategy outputs (Trinity Output pattern).
Implements CODEXA 8-Pillar Standard Output: .md (human) + .llm.json + .meta.json

Usage:
    python meta_json_generator.py brand_strategy.md
    python meta_json_generator.py --input brand_strategy.md --output brand_strategy.meta.json
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import hashlib


class BrandMetadataGenerator:
    """Generate .meta.json for brand strategy outputs."""

    def __init__(self, markdown_file: Path):
        """Initialize generator with markdown file."""
        self.markdown_file = Path(markdown_file)
        self.content = self._read_file()
        self.metadata = {}

    def _read_file(self) -> str:
        """Read markdown file content."""
        if not self.markdown_file.exists():
            raise FileNotFoundError(f"File not found: {self.markdown_file}")

        with open(self.markdown_file, 'r', encoding='utf-8') as f:
            return f.read()

    def extract_brand_names(self) -> List[str]:
        """Extract brand names from markdown."""
        names = []

        # Look for brand name section patterns
        patterns = [
            r"(?:Brand Name|Nome da Marca)[^\n]*:\s*([^\n]+)",
            r"##\s*(?:Brand Names|Nomes de Marca)\s*\n((?:[-*]\s*[^\n]+\n?)+)",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, self.content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                # Extract names from lists
                list_items = re.findall(r'[-*]\s*([^\n]+)', match)
                if list_items:
                    names.extend([item.strip().strip('*_`"') for item in list_items])
                else:
                    names.append(match.strip().strip('*_`"'))

        return names[:3] if names else []  # Max 3 names

    def extract_taglines(self) -> List[Dict[str, Any]]:
        """Extract taglines with length validation."""
        taglines = []

        # Look for tagline patterns
        patterns = [
            r"(?:Tagline|Slogan)[^\n]*:\s*([^\n]+)",
            r"##\s*(?:Taglines|Slogans)\s*\n((?:[-*]\s*[^\n]+\n?)+)",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, self.content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                # Extract from lists
                list_items = re.findall(r'[-*]\s*([^\n]+)', match)
                if list_items:
                    for item in list_items:
                        clean = item.strip().strip('*_`"')
                        taglines.append({
                            "text": clean,
                            "length": len(clean),
                            "valid": 40 <= len(clean) <= 60
                        })
                else:
                    clean = match.strip().strip('*_`"')
                    taglines.append({
                        "text": clean,
                        "length": len(clean),
                        "valid": 40 <= len(clean) <= 60
                    })

        return taglines[:3] if taglines else []

    def extract_archetype(self) -> Optional[str]:
        """Extract brand archetype."""
        patterns = [
            r"(?:Archetype|Arquétipo)[^\n]*:\s*([^\n]+)",
            r"(?:Primary Archetype|Arquétipo Primário)[^\n]*:\s*([^\n]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, self.content, re.IGNORECASE)
            if match:
                archetype = match.group(1).strip().strip('*_`"')
                # Extract just the archetype name if there's additional text
                archetype = archetype.split('(')[0].split('-')[0].strip()
                return archetype

        return None

    def extract_consistency_score(self) -> Optional[float]:
        """Extract brand consistency score."""
        patterns = [
            r"(?:Consistency Score|Brand Consistency)[^\n]*:\s*([\d.]+)",
            r"(?:Score|Pontuação)[^\n]*:\s*([\d.]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, self.content, re.IGNORECASE)
            if match:
                try:
                    score = float(match.group(1))
                    # Normalize to 0-1 if given as percentage
                    if score > 1.0:
                        score = score / 100.0
                    return round(score, 2)
                except ValueError:
                    continue

        return None

    def calculate_word_count(self) -> int:
        """Calculate word count of content."""
        # Remove markdown formatting
        text = re.sub(r'[#*_`\[\]()]', '', self.content)
        words = text.split()
        return len(words)

    def calculate_completeness_score(self) -> float:
        """Calculate how complete the brand strategy is (0-1)."""
        required_sections = [
            r"##\s*(?:Brand Identity|Identidade da Marca)",
            r"##\s*(?:Positioning|Posicionamento)",
            r"##\s*(?:Tone of Voice|Tom de Voz)",
            r"##\s*(?:Visual Identity|Identidade Visual)",
            r"##\s*(?:Brand Narrative|Narrativa)",
            r"##\s*(?:Brand Guidelines|Diretrizes)",
            r"##\s*(?:Validation|Validação)",
        ]

        found = sum(1 for pattern in required_sections if re.search(pattern, self.content, re.IGNORECASE))
        return round(found / len(required_sections), 2)

    def generate_content_hash(self) -> str:
        """Generate SHA-256 hash of content for version tracking."""
        return hashlib.sha256(self.content.encode('utf-8')).hexdigest()[:16]

    def generate_metadata(self) -> Dict[str, Any]:
        """Generate complete metadata structure."""
        brand_names = self.extract_brand_names()
        taglines = self.extract_taglines()
        archetype = self.extract_archetype()
        consistency_score = self.extract_consistency_score()
        word_count = self.calculate_word_count()
        completeness = self.calculate_completeness_score()
        content_hash = self.generate_content_hash()

        # Calculate quality indicators
        taglines_valid = all(t["valid"] for t in taglines) if taglines else False
        has_archetype = archetype is not None
        meets_word_count = 5000 <= word_count <= 8000

        metadata = {
            "version": "1.0.0",
            "schema": "brand_strategy_metadata_v1",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "source_file": str(self.markdown_file.name),
            "content_hash": content_hash,

            "execution": {
                "model": "unknown",  # Populated by agent during generation
                "temperature": None,
                "execution_time_seconds": None,
                "agent_version": "1.0.0"
            },

            "brand_summary": {
                "brand_names": brand_names,
                "brand_name_count": len(brand_names),
                "archetype": archetype,
                "taglines_count": len(taglines)
            },

            "content_metrics": {
                "word_count": word_count,
                "character_count": len(self.content),
                "estimated_reading_time_minutes": round(word_count / 200, 1),  # 200 wpm average
                "completeness_score": completeness,
                "target_word_count_range": "5000-8000",
                "meets_word_count_target": meets_word_count
            },

            "quality_scores": {
                "consistency_score": consistency_score,
                "consistency_threshold": 0.85,
                "meets_consistency_threshold": consistency_score >= 0.85 if consistency_score else False,

                "taglines_validation": {
                    "all_valid_length": taglines_valid,
                    "taglines": taglines
                },

                "archetype_validation": {
                    "has_archetype": has_archetype,
                    "archetype_valid": has_archetype  # TODO: Validate against 12 valid archetypes
                },

                "completeness": {
                    "score": completeness,
                    "required_sections_found": int(completeness * 7),  # 7 required sections
                    "total_required_sections": 7
                }
            },

            "validation_status": {
                "validated": False,  # Set to True after running brand_validator.py
                "validator_version": None,
                "validation_errors": [],
                "validation_warnings": [],
                "last_validated_at": None
            },

            "deployment": {
                "target_marketplace": "unknown",  # mercadolivre, shopee, amazon_br, magalu
                "deployment_ready": taglines_valid and has_archetype and completeness >= 0.85,
                "blocking_issues": self._identify_blocking_issues(
                    taglines_valid, has_archetype, consistency_score, completeness
                )
            },

            "file_relationships": {
                "markdown_file": str(self.markdown_file.name),
                "llm_json_file": str(self.markdown_file.with_suffix('.llm.json').name),
                "meta_json_file": str(self.markdown_file.with_suffix('.meta.json').name),
                "validation_report": None  # Populated after validation
            },

            "notes": {
                "trinity_output": "Part of CODEXA 8-Pillar Standard Output (.md + .llm.json + .meta.json)",
                "purpose": "Metadata for LLM consumption, tracking, and quality assurance",
                "generated_by": "meta_json_generator.py v1.0.0"
            }
        }

        return metadata

    def _identify_blocking_issues(
        self,
        taglines_valid: bool,
        has_archetype: bool,
        consistency_score: Optional[float],
        completeness: float
    ) -> List[str]:
        """Identify blocking issues preventing deployment."""
        issues = []

        if not taglines_valid:
            issues.append("Taglines do not meet 40-60 character requirement")

        if not has_archetype:
            issues.append("Missing brand archetype selection")

        if consistency_score and consistency_score < 0.85:
            issues.append(f"Consistency score {consistency_score} below threshold 0.85")

        if completeness < 0.85:
            issues.append(f"Strategy incomplete ({int(completeness*100)}% complete, need ≥85%)")

        return issues

    def save_metadata(self, output_path: Optional[Path] = None) -> Path:
        """Generate and save metadata to JSON file."""
        if output_path is None:
            output_path = self.markdown_file.with_suffix('.meta.json')

        metadata = self.generate_metadata()

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        return output_path


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate .meta.json metadata for brand strategy markdown files"
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Input brand_strategy.md file"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Output .meta.json file (default: <input>.meta.json)"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output to console"
    )

    args = parser.parse_args()

    # Generate metadata
    generator = BrandMetadataGenerator(args.input)
    output_path = generator.save_metadata(args.output)

    print(f"✓ Metadata generated: {output_path}")

    # Show summary
    metadata = generator.generate_metadata()
    print(f"\nSummary:")
    print(f"  Brand Names: {metadata['brand_summary']['brand_name_count']}")
    print(f"  Archetype: {metadata['brand_summary']['archetype'] or 'Not found'}")
    print(f"  Word Count: {metadata['content_metrics']['word_count']}")
    print(f"  Completeness: {int(metadata['content_metrics']['completeness_score']*100)}%")

    if metadata['quality_scores']['consistency_score']:
        print(f"  Consistency Score: {metadata['quality_scores']['consistency_score']}")

    if metadata['deployment']['blocking_issues']:
        print(f"\n⚠ Blocking Issues:")
        for issue in metadata['deployment']['blocking_issues']:
            print(f"    - {issue}")
    else:
        print(f"\n✓ Deployment Ready: Yes")

    # Pretty print if requested
    if args.pretty:
        print("\nFull Metadata:")
        print(json.dumps(metadata, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
