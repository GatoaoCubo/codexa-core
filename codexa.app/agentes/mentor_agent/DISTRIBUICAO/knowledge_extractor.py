#!/usr/bin/env python3
"""
Knowledge Extractor - Extrai versículos dos CAPITULOS do MENTOR

Purpose: Ler arquivos CAPITULO_*.md e extrair versículos específicos
Input: Referência de versículo (ex: "CAPITULO_marketplace_01:versiculo_18")
Output: Bloco de markdown com conteúdo do versículo

Usage:
    from knowledge_extractor import extract_versiculo
    content = extract_versiculo("CAPITULO_marketplace_01:versiculo_18")

Version: 1.0.0
Author: CODEXA Meta-Construction System
"""

import re
import sys
from pathlib import Path
from typing import Optional, Dict, List
import json

# Add config to path for centralized path management
sys.path.insert(0, str(Path(__file__).parent.parent / 'config'))
from paths import PATH_PROCESSADOS


class VersiculoNotFoundError(Exception):
    """Raised when versículo reference is not found"""
    pass


class CapituloNotFoundError(Exception):
    """Raised when CAPITULO file does not exist"""
    pass


class KnowledgeExtractor:
    """Extrai versículos de arquivos CAPITULO"""

    def __init__(self, processados_dir: Optional[Path] = None):
        """
        Initialize extractor

        Args:
            processados_dir: Path to PROCESSADOS/ directory
                           If None, uses centralized config
        """
        if processados_dir is None:
            processados_dir = PATH_PROCESSADOS

        self.processados_dir = Path(processados_dir)

        if not self.processados_dir.exists():
            raise FileNotFoundError(
                f"PROCESSADOS directory not found: {self.processados_dir}"
            )

    def parse_reference(self, ref: str) -> Dict[str, str]:
        """
        Parse versículo reference

        Args:
            ref: Reference string (ex: "CAPITULO_marketplace_01:versiculo_18")

        Returns:
            Dict with 'capitulo' and 'versiculo_num' keys

        Raises:
            ValueError: If reference format is invalid
        """
        # Expected format: CAPITULO_{tema}_{num}:versiculo_{num}
        pattern = r"^(CAPITULO_[^:]+):versiculo_(\d+)$"
        match = re.match(pattern, ref)

        if not match:
            raise ValueError(
                f"Invalid reference format: {ref}\n"
                f"Expected: CAPITULO_{{tema}}_{{num}}:versiculo_{{num}}\n"
                f"Example: CAPITULO_marketplace_01:versiculo_18"
            )

        return {
            "capitulo": match.group(1),
            "versiculo_num": match.group(2)
        }

    def find_capitulo_file(self, capitulo_name: str) -> Path:
        """
        Find CAPITULO file in PROCESSADOS/

        Args:
            capitulo_name: Name like "CAPITULO_marketplace_01"

        Returns:
            Path to CAPITULO file

        Raises:
            CapituloNotFoundError: If file not found
        """
        capitulo_file = self.processados_dir / f"{capitulo_name}.md"

        if not capitulo_file.exists():
            raise CapituloNotFoundError(
                f"CAPITULO file not found: {capitulo_file}\n"
                f"Searched in: {self.processados_dir}"
            )

        return capitulo_file

    def extract_versiculo(
        self,
        ref: str,
        include_metadata: bool = True
    ) -> Dict[str, any]:
        """
        Extract versículo content from CAPITULO

        Args:
            ref: Reference string (ex: "CAPITULO_marketplace_01:versiculo_18")
            include_metadata: Include metadata in output (default True)

        Returns:
            Dict with keys:
                - content: Markdown content of versículo
                - metadata: Dict with versículo info (if include_metadata=True)
                - ref: Original reference
                - capitulo: Capitulo name
                - versiculo_num: Versículo number

        Raises:
            VersiculoNotFoundError: If versículo not found
            CapituloNotFoundError: If CAPITULO file not found
        """
        # Parse reference
        parsed = self.parse_reference(ref)
        capitulo_name = parsed["capitulo"]
        versiculo_num = int(parsed["versiculo_num"])

        # Find CAPITULO file
        capitulo_file = self.find_capitulo_file(capitulo_name)

        # Read file
        with open(capitulo_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract versículo
        versiculo_content, versiculo_metadata = self._extract_versiculo_from_content(
            content, versiculo_num
        )

        # Build result
        result = {
            "content": versiculo_content,
            "ref": ref,
            "capitulo": capitulo_name,
            "versiculo_num": versiculo_num
        }

        if include_metadata:
            result["metadata"] = versiculo_metadata

        return result

    def _extract_versiculo_from_content(
        self,
        content: str,
        versiculo_num: int
    ) -> tuple[str, Dict]:
        """
        Extract versículo from CAPITULO content

        Args:
            content: Full CAPITULO content
            versiculo_num: Versículo number to extract

        Returns:
            Tuple of (versiculo_content, versiculo_metadata)

        Raises:
            VersiculoNotFoundError: If versículo not found
        """
        # Marker pattern: <!-- VERSÍCULO X/Y - filename (Z linhas) -->
        marker_pattern = r"<!-- VERSÍCULO (\d+)/(\d+) - ([^(]+)\((\d+) linhas\) -->"

        # Find all versículo markers
        markers = list(re.finditer(marker_pattern, content))

        if not markers:
            raise VersiculoNotFoundError(
                f"No versículo markers found in CAPITULO\n"
                f"Expected marker format: <!-- VERSÍCULO X/Y - filename (Z linhas) -->"
            )

        # Find target versículo
        target_marker = None
        target_index = None

        for idx, marker in enumerate(markers):
            current_versiculo_num = int(marker.group(1))
            if current_versiculo_num == versiculo_num:
                target_marker = marker
                target_index = idx
                break

        if target_marker is None:
            total_versiculos = len(markers)
            raise VersiculoNotFoundError(
                f"Versículo {versiculo_num} not found\n"
                f"CAPITULO has {total_versiculos} versículos (1-{total_versiculos})"
            )

        # Extract metadata from marker
        total_versiculos = int(target_marker.group(2))
        filename = target_marker.group(3).strip()
        num_linhas = int(target_marker.group(4))

        metadata = {
            "versiculo_num": versiculo_num,
            "total_versiculos": total_versiculos,
            "filename": filename,
            "num_linhas": num_linhas
        }

        # Extract content between this marker and next marker
        start_pos = target_marker.end()

        # Find next marker (if exists)
        if target_index + 1 < len(markers):
            next_marker = markers[target_index + 1]
            end_pos = next_marker.start()
        else:
            # Last versículo - read until end of file
            end_pos = len(content)

        versiculo_content = content[start_pos:end_pos].strip()

        return versiculo_content, metadata

    def extract_multiple(
        self,
        refs: List[str],
        include_metadata: bool = True
    ) -> List[Dict]:
        """
        Extract multiple versículos

        Args:
            refs: List of reference strings
            include_metadata: Include metadata in output

        Returns:
            List of dicts (same format as extract_versiculo)
        """
        results = []

        for ref in refs:
            try:
                result = self.extract_versiculo(ref, include_metadata)
                results.append(result)
            except (VersiculoNotFoundError, CapituloNotFoundError) as e:
                # Add error entry
                results.append({
                    "ref": ref,
                    "error": str(e),
                    "content": None
                })

        return results

    def format_for_injection(
        self,
        versiculo_data: Dict,
        include_source: bool = True
    ) -> str:
        """
        Format versículo content for injection into prompt

        Args:
            versiculo_data: Output from extract_versiculo()
            include_source: Include source reference at end

        Returns:
            Formatted markdown string ready for injection
        """
        content = versiculo_data["content"]

        # Add source footer if requested
        if include_source and "metadata" in versiculo_data:
            metadata = versiculo_data["metadata"]
            ref = versiculo_data["ref"]

            footer = (
                f"\n\n---\n"
                f"*Fonte: {ref}*\n"
                f"*Arquivo: {metadata.get('filename', 'unknown')}*\n"
            )
            content = content + footer

        return content


# Convenience functions for direct usage

def extract_versiculo(ref: str, include_metadata: bool = True) -> Dict:
    """
    Convenience function to extract single versículo

    Args:
        ref: Reference string (ex: "CAPITULO_marketplace_01:versiculo_18")
        include_metadata: Include metadata in output

    Returns:
        Dict with versículo content and metadata
    """
    extractor = KnowledgeExtractor()
    return extractor.extract_versiculo(ref, include_metadata)


def extract_multiple(refs: List[str], include_metadata: bool = True) -> List[Dict]:
    """
    Convenience function to extract multiple versículos

    Args:
        refs: List of reference strings
        include_metadata: Include metadata in output

    Returns:
        List of dicts with versículo content and metadata
    """
    extractor = KnowledgeExtractor()
    return extractor.extract_multiple(refs, include_metadata)


# CLI interface
if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract versículos from MENTOR CAPITULOS"
    )
    parser.add_argument(
        "reference",
        help="Versículo reference (ex: CAPITULO_marketplace_01:versiculo_18)"
    )
    parser.add_argument(
        "--no-metadata",
        action="store_true",
        help="Don't include metadata in output"
    )
    parser.add_argument(
        "--format",
        choices=["json", "markdown"],
        default="markdown",
        help="Output format (default: markdown)"
    )
    parser.add_argument(
        "--no-source",
        action="store_true",
        help="Don't include source reference in markdown output"
    )

    args = parser.parse_args()

    try:
        # Fix Windows encoding for stdout
        if sys.platform == 'win32':
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

        # Extract versículo
        extractor = KnowledgeExtractor()
        result = extractor.extract_versiculo(
            args.reference,
            include_metadata=not args.no_metadata
        )

        # Output based on format
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            # Markdown format
            formatted = extractor.format_for_injection(
                result,
                include_source=not args.no_source
            )
            print(formatted)

        sys.exit(0)

    except (VersiculoNotFoundError, CapituloNotFoundError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)
