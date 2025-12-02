"""
ML Knowledge Processor - Core Module
Unificação de: ml_processor_pipeline.py, meta_processor.py

Transforma entrada bruta (RAW) em Knowledge Cards estruturados otimizados.

Pipeline de Processamento:
    RAW Input (PDF, Audio, TXT, JSON, Image)
        ↓
    Source Analysis (tipo, domínio, conteúdo)
        ↓
    Content Extraction (extrai texto, conceitos, metadata)
        ↓
    Structuring (cria cardstructured)
        ↓
    Optimization (densidade de informação, linguagem para LLM)
        ↓
    Knowledge Card (MD estruturado, pronto para consumo)

Padrões Seguidos:
    - BLOCO 4: LLM-Optimized Documentation (máxima densidade)
    - BLOCO 7: Information Types (RAW → Structured → Processed → Crystallized)
    - BLOCO 16: Knowledge Distillation (evidência + confiança)
"""

import json
import hashlib
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Importar componentes existentes
try:
    from ml_crud_manager import MLCRUDManager, ProcessingStatus
except ImportError:
    MLCRUDManager = None
    ProcessingStatus = None


# ============================================================================
# ENUMS & DATA CLASSES
# ============================================================================

class SourceType(Enum):
    """Tipos de entrada"""
    PDF = "pdf"
    AUDIO = "audio"
    IMAGE = "image"
    TEXT = "text"
    JSON = "json"
    MARKDOWN = "markdown"
    CODE = "code"
    UNKNOWN = "unknown"


class ProcessingStage(Enum):
    """Estágios do processamento"""
    EXTRACTION = "extraction"          # Extrair conteúdo bruto
    ANALYSIS = "analysis"              # Analisar estrutura e domínio
    STRUCTURING = "structuring"        # Estruturar informações
    OPTIMIZATION = "optimization"      # Otimizar para LLM
    VALIDATION = "validation"          # Validar card


@dataclass
class ProcessingMetrics:
    """Métricas de processamento"""
    stage: ProcessingStage
    timestamp: str
    duration_seconds: float
    items_processed: int
    success_rate: float
    errors: List[str] = None

    def __post_init__(self):
        if self.errors is None:
            self.errors = []


@dataclass
class KnowledgeCardMetadata:
    """Metadata de um Knowledge Card"""
    card_id: str
    title: str
    source_type: SourceType
    source_file: str
    domain: str
    created_at: str
    updated_at: str
    version: str = "1.0"
    confidence_score: float = 1.0
    word_count: int = 0
    information_density: float = 0.0


# ============================================================================
# CONTENT EXTRACTOR
# ============================================================================

class ContentExtractor:
    """Extrai conteúdo de diferentes formatos de entrada"""

    @staticmethod
    def detect_source_type(filepath: Path) -> SourceType:
        """Detectar tipo de arquivo"""
        suffix = filepath.suffix.lower()

        type_map = {
            '.pdf': SourceType.PDF,
            '.mp3': SourceType.AUDIO,
            '.wav': SourceType.AUDIO,
            '.m4a': SourceType.AUDIO,
            '.png': SourceType.IMAGE,
            '.jpg': SourceType.IMAGE,
            '.jpeg': SourceType.IMAGE,
            '.gif': SourceType.IMAGE,
            '.txt': SourceType.TEXT,
            '.md': SourceType.MARKDOWN,
            '.json': SourceType.JSON,
            '.jsonl': SourceType.JSON,
            '.py': SourceType.CODE,
            '.js': SourceType.CODE,
            '.ts': SourceType.CODE,
        }

        return type_map.get(suffix, SourceType.UNKNOWN)

    @staticmethod
    def extract_text(filepath: Path) -> Optional[str]:
        """Extrair texto de arquivo"""
        try:
            source_type = ContentExtractor.detect_source_type(filepath)

            if source_type == SourceType.JSON:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return json.dumps(data, ensure_ascii=False, indent=2)

            elif source_type in [SourceType.TEXT, SourceType.MARKDOWN, SourceType.CODE]:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()

            elif source_type == SourceType.PDF:
                # Stub: implementar com PyPDF2
                return f"[PDF Content from {filepath.name}]"

            elif source_type == SourceType.AUDIO:
                # Stub: implementar com Whisper
                return f"[Audio transcription from {filepath.name}]"

            elif source_type == SourceType.IMAGE:
                # Stub: implementar com Vision API
                return f"[Image description from {filepath.name}]"

            else:
                return None

        except Exception as e:
            print(f"[!] Error extracting text from {filepath}: {e}")
            return None

    @staticmethod
    def extract_metadata(filepath: Path, content: str) -> Dict[str, Any]:
        """Extrair metadata do arquivo e conteúdo"""
        return {
            'filename': filepath.name,
            'file_size': filepath.stat().st_size,
            'created_time': datetime.fromtimestamp(filepath.stat().st_ctime).isoformat(),
            'modified_time': datetime.fromtimestamp(filepath.stat().st_mtime).isoformat(),
            'content_length': len(content),
            'line_count': len(content.split('\n')),
            'word_count': len(content.split()),
        }


# ============================================================================
# KNOWLEDGE CARD GENERATOR
# ============================================================================

class KnowledgeCardGenerator:
    """Gera Knowledge Cards estruturados a partir de conteúdo extraído"""

    CARD_TEMPLATE = """# {{TITLE}}

**Card ID**: {{CARD_ID}}
**Created**: {{CREATED_AT}}
**Domain**: {{DOMAIN}}
**Confidence**: {{CONFIDENCE}}%

## Key Concepts

{{KEY_CONCEPTS}}

## Core Knowledge

{{CORE_KNOWLEDGE}}

## Bullet Points

{{BULLET_POINTS}}

## Examples

{{EXAMPLES}}

## Related Concepts

{{RELATED_CONCEPTS}}

## Metadata

- **Source**: {{SOURCE_TYPE}}
- **Word Count**: {{WORD_COUNT}}
- **Information Density**: {{INFORMATION_DENSITY}}%
- **Version**: {{VERSION}}
"""

    def __init__(self):
        self.cards_dir = None

    def generate_card_id(self, domain: str, content_hash: str) -> str:
        """Gerar ID único para card"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"CARD_{domain.upper()}_{timestamp}_{content_hash[:8]}"

    def extract_key_concepts(self, content: str, max_items: int = 10) -> List[str]:
        """Extrair conceitos principais do conteúdo"""
        concepts = []

        # Buscar headers (Markdown)
        headers = re.findall(r'^#{1,3}\s+(.+)$', content, re.MULTILINE)
        concepts.extend(headers[:max_items])

        # Buscar PALAVRAS-CHAVE em CAPS (muito específicas)
        caps_words = re.findall(r'\b[A-Z][A-Z_]+\b', content)
        concepts.extend(list(set(caps_words))[:max_items // 2])

        # Remover duplicatas e limitar
        concepts = list(dict.fromkeys(concepts))[:max_items]

        return concepts

    def calculate_information_density(self, content: str) -> float:
        """Calcular densidade de informação (0-100%)"""
        # Heurística: proporção de conteúdo útil vs. filler
        lines = content.split('\n')
        empty_lines = sum(1 for line in lines if not line.strip())
        filler_words = sum(1 for word in content.lower().split()
                          if word in ['the', 'a', 'an', 'and', 'or', 'but'])

        useful_ratio = 1.0 - (empty_lines / len(lines) if lines else 0)
        filler_ratio = filler_words / len(content.split()) if content else 0

        density = (useful_ratio * 0.7 + (1 - filler_ratio) * 0.3) * 100
        return min(100.0, max(0.0, density))

    def generate(self,
                 content: str,
                 title: str,
                 source_type: SourceType,
                 domain: str = "general",
                 source_file: str = "unknown") -> str:
        """
        Gerar Knowledge Card em Markdown.

        Args:
            content: Conteúdo extraído
            title: Título do card
            source_type: Tipo de fonte
            domain: Domínio (ex: ecommerce, technical)
            source_file: Nome do arquivo origem

        Returns:
            Markdown estruturado do Knowledge Card
        """
        # Calcular hash para ID
        content_hash = hashlib.md5(content.encode()).hexdigest()
        card_id = self.generate_card_id(domain, content_hash)

        # Extrair componentes
        key_concepts = self.extract_key_concepts(content)
        information_density = self.calculate_information_density(content)
        word_count = len(content.split())

        # Truncar conteúdo para "Core Knowledge"
        core_knowledge = content[:2000] if len(content) > 2000 else content

        # Gerar bullet points
        bullet_points = self._generate_bullet_points(content)

        # Montar card do template
        card = self.CARD_TEMPLATE.replace("{{TITLE}}", title)
        card = card.replace("{{CARD_ID}}", card_id)
        card = card.replace("{{CREATED_AT}}", datetime.now().isoformat())
        card = card.replace("{{DOMAIN}}", domain)
        card = card.replace("{{CONFIDENCE}}", "95")  # Default confidence
        card = card.replace("{{KEY_CONCEPTS}}", "\n".join(f"- {c}" for c in key_concepts))
        card = card.replace("{{CORE_KNOWLEDGE}}", core_knowledge)
        card = card.replace("{{BULLET_POINTS}}", bullet_points)
        card = card.replace("{{EXAMPLES}}", "[Examples to be added]")
        card = card.replace("{{RELATED_CONCEPTS}}", "[Related concepts to be added]")
        card = card.replace("{{SOURCE_TYPE}}", source_type.value)
        card = card.replace("{{WORD_COUNT}}", str(word_count))
        card = card.replace("{{INFORMATION_DENSITY}}", f"{information_density:.1f}")
        card = card.replace("{{VERSION}}", "1.0")

        return card

    @staticmethod
    def _generate_bullet_points(content: str, max_items: int = 8) -> str:
        """Gerar bullet points do conteúdo"""
        # Buscar linhas que parecem importantes (começam com - ou *)
        bullets = re.findall(r'^[\s]*[-*]\s+(.+)$', content, re.MULTILINE)

        if bullets:
            return "\n".join(f"- {b.strip()}" for b in bullets[:max_items])
        else:
            # Fallback: quebrar em parágrafos e criar bullets
            paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
            bullets = [p[:100] + "..." if len(p) > 100 else p for p in paragraphs[:max_items]]
            return "\n".join(f"- {b}" for b in bullets)


# ============================================================================
# KNOWLEDGE PROCESSOR (Main Class)
# ============================================================================

class KnowledgeProcessor:
    """
    Processa arquivos RAW em Knowledge Cards estruturados.

    Responsabilidades:
    - Detectar tipo de fonte
    - Extrair conteúdo
    - Analisar e estruturar
    - Gerar Knowledge Cards
    - Validar qualidade
    """

    def __init__(self, raw_dir: str = "RAW", processed_dir: str = "Processados"):
        """Inicializar processador"""
        self.raw_dir = Path(raw_dir)
        self.processed_dir = Path(processed_dir)
        self.cards_dir = self.processed_dir / "knowledge_cards"
        self.reports_dir = self.processed_dir / "reports"

        # Criar diretórios
        for d in [self.raw_dir, self.processed_dir, self.cards_dir, self.reports_dir]:
            d.mkdir(parents=True, exist_ok=True)

        # Componentes
        self.extractor = ContentExtractor()
        self.generator = KnowledgeCardGenerator()
        self.crud = MLCRUDManager(data_dir=str(processed_dir)) if MLCRUDManager else None

        # Metrics
        self.processing_metrics: List[ProcessingMetrics] = []

    def process_file(self, filepath: Path) -> Optional[str]:
        """
        Processar um arquivo individual.

        Returns:
            Caminho do Knowledge Card gerado, ou None se falhou
        """
        try:
            # Stage 1: Extraction
            content = self.extractor.extract_text(filepath)
            if not content:
                return None

            source_type = self.extractor.detect_source_type(filepath)
            metadata = self.extractor.extract_metadata(filepath, content)

            # Stage 2: Analysis (extrair domínio do caminho)
            domain = self._extract_domain(filepath)

            # Stage 3: Generate Card
            card_content = self.generator.generate(
                content=content,
                title=filepath.stem,
                source_type=source_type,
                domain=domain,
                source_file=filepath.name
            )

            # Stage 4: Save Card
            card_filename = f"{domain}_{filepath.stem}_{hashlib.md5(content.encode()).hexdigest()[:8]}.md"
            card_path = self.cards_dir / card_filename

            with open(card_path, 'w', encoding='utf-8') as f:
                f.write(card_content)

            # Stage 5: Register in CRUD
            if self.crud:
                self.crud.create(
                    filepath=str(filepath),
                    status=ProcessingStatus.COMPLETED if ProcessingStatus else "completed",
                    cards_generated=1,
                    output_path=str(card_path)
                )

            return str(card_path)

        except Exception as e:
            print(f"[!] Error processing {filepath}: {e}")
            return None

    def process_directory(self,
                         input_dir: Path = None,
                         output_dir: Path = None,
                         recursive: bool = True) -> Dict[str, Any]:
        """
        Processar diretório completo de arquivos RAW.

        Returns:
            Dicionário com estatísticas de processamento
        """
        input_dir = input_dir or self.raw_dir
        output_dir = output_dir or self.cards_dir

        stats = {
            'timestamp': datetime.now().isoformat(),
            'input_directory': str(input_dir),
            'output_directory': str(output_dir),
            'files_processed': 0,
            'cards_generated': 0,
            'errors': [],
            'processing_time_seconds': 0,
        }

        start_time = datetime.now()

        try:
            # Listar arquivos
            if recursive:
                files = list(input_dir.rglob('*'))
            else:
                files = list(input_dir.glob('*'))

            files = [f for f in files if f.is_file()]

            for filepath in files:
                card_path = self.process_file(filepath)
                stats['files_processed'] += 1

                if card_path:
                    stats['cards_generated'] += 1
                else:
                    stats['errors'].append(str(filepath))

        except Exception as e:
            stats['errors'].append(f"Directory processing failed: {str(e)}")

        finally:
            duration = (datetime.now() - start_time).total_seconds()
            stats['processing_time_seconds'] = duration

        return stats

    @staticmethod
    def _extract_domain(filepath: Path) -> str:
        """Extrair domínio do caminho do arquivo"""
        parts = filepath.parts
        if len(parts) > 1:
            return parts[0].lower()
        return "general"


# ============================================================================
# CLI ENTRY POINT
# ============================================================================

def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="ML Knowledge Processor")
    parser.add_argument("--input", type=str, default="RAW", help="Input directory")
    parser.add_argument("--output", type=str, default="Processados", help="Output directory")
    parser.add_argument("--domain", type=str, default="general", help="Knowledge domain")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    processor = KnowledgeProcessor(raw_dir=args.input, processed_dir=args.output)
    results = processor.process_directory(recursive=True)

    if args.verbose:
        print(json.dumps(results, indent=2))
    else:
        print(f"[✓] Processed: {results['files_processed']} files")
        print(f"[✓] Generated: {results['cards_generated']} cards")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
