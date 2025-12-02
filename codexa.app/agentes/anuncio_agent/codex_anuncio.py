#!/usr/bin/env python3
"""
CodeXAnuncio Meta-Agent - Standalone CLI v1.2.0
KEYWORDS: codex|anuncio|cli|standalone|marketplace|ad-generation|dense|HOP

Dense, production-ready ad generation system for Brazilian marketplaces.
Processes research notes → generates optimized marketplace ads with ZERO conectores.

Version: 1.2.0
Updated: 2025-11-11
Status: Production-Ready
"""

import argparse
import json
import sys
from pathlib import Path

# Import centralized path configuration
sys.path.insert(0, str(Path(__file__).parent))
from config.paths import ANUNCIO_AGENT_ROOT, PATH_OUTPUTS, PATH_SRC

# Add src/ to path for imports
sys.path.insert(0, str(PATH_SRC))

# Dense imports - all core functionality
from models import (
    AnuncioOutput,
)
from processor import (
    ClosedLoopValidator,
    calculate_persuasion_score,
    correct_anuncio,
    generate_anuncio,
    parse_research_notes,
    validate_output,
)
from trinity_writer import TrinityOutputWriter


class CodeXAnuncioCLI:
    """Compact CLI interface for CodeXAnuncio."""

    def __init__(self):
        self.base_path = ANUNCIO_AGENT_ROOT
        self.version = "1.2.0"

    def run(self, args: argparse.Namespace) -> int:
        """Execute command based on args."""

        if args.command == "generate":
            return self._generate(args)
        if args.command == "validate":
            return self._validate(args)
        if args.command == "version":
            return 0

        return 1

    def _generate(self, args: argparse.Namespace) -> int:
        """Generate ad from research notes."""

        try:
            # Read research notes
            research_path = Path(args.input)
            if not research_path.exists():
                return 1

            with open(research_path, encoding="utf-8") as f:
                markdown_content = f.read()

            research = parse_research_notes(markdown_content)


            # Generate ad

            if args.auto_correct:
                # Use closed-loop validator
                validator = ClosedLoopValidator(max_attempts=args.max_attempts)

                result = validator.validate_with_correction(
                    execute_fn=lambda: generate_anuncio(research, args.marketplace),
                    validate_fn=lambda r: validate_output(r.anuncio) if r.success else r.validation,
                    correct_fn=lambda a, v: correct_anuncio(a.anuncio, v) if hasattr(a, "anuncio") else a,
                )

                if len(result) == 2:
                    anuncio, validation = result
                    persuasion = calculate_persuasion_score(anuncio)
                else:
                    result_obj = result
                    anuncio = result_obj.anuncio
                    validation = result_obj.validation
                    persuasion = result_obj.persuasion_score
            else:
                # Direct generation
                result = generate_anuncio(research, args.marketplace)
                anuncio = result.anuncio
                validation = result.validation
                persuasion = result.persuasion_score

            if not anuncio:
                print("❌ Geração falhou. Erros encontrados:")
                for _error in result.errors:
                    print(f"  • {_error}")
                return 1

            # Output results

            # Save output
            if args.output:
                output_path = Path(args.output)
            else:
                output_path = PATH_OUTPUTS / anuncio.nome_arquivo_sugerido

            output_path.parent.mkdir(parents=True, exist_ok=True)

            if args.format == "trinity":
                # Trinity output (3 files)
                writer = TrinityOutputWriter(output_path.parent)
                writer.write(anuncio, validation, persuasion, output_path.stem)
            elif args.format == "json":
                # Single JSON file
                with open(output_path.with_suffix(".json"), "w", encoding="utf-8") as f:
                    json.dump(anuncio.model_dump(), f, ensure_ascii=False, indent=2)
            elif args.format == "markdown":
                # Single markdown file
                from trinity_writer import TrinityOutputWriter

                writer = TrinityOutputWriter(output_path.parent)
                md_content = writer._to_markdown(anuncio, validation, persuasion)
                with open(output_path.with_suffix(".md"), "w", encoding="utf-8") as f:
                    f.write(md_content)

            # Show warnings if any
            if validation.warnings:
                print("\n⚠️  Avisos:")
                for _warning in validation.warnings:
                    print(f"  • {_warning}")

            # Show issues if any
            if validation.compliance_issues:
                print("\n🚨 Issues de Compliance:")
                for _issue in validation.compliance_issues:
                    print(f"  • {_issue}")

            # Show recommendations
            if persuasion.recomendacoes:
                print("\n💡 Recomendações (Top 3):")
                for _rec in persuasion.recomendacoes[:3]:
                    print(f"  • {_rec}")

            # Show success summary
            print(f"\n✅ Anúncio gerado com sucesso!")
            print(f"   QA Status: {validation.qa_status}")
            print(f"   Persuasion: {persuasion.nivel}")
            print(f"   Compliance: {validation.compliance_score}%")

            return 0

        except Exception:
            if args.verbose:
                import traceback

                traceback.print_exc()
            return 1

    def _validate(self, args: argparse.Namespace) -> int:
        """Validate existing anuncio JSON."""

        try:
            anuncio_path = Path(args.input)
            if not anuncio_path.exists():
                return 1

            with open(anuncio_path, encoding="utf-8") as f:
                data = json.load(f)

            anuncio = AnuncioOutput(**data)
            validation = validate_output(anuncio)
            persuasion = calculate_persuasion_score(anuncio)

            print(f"\n🔍 Validando: {anuncio_path.name}")
            print(f"   QA Status: {validation.qa_status}")
            print(f"   Persuasion: {persuasion.nivel} ({persuasion.score:.2f})")
            print(f"   Compliance: {validation.compliance_score}%")

            if validation.errors:
                print("\n❌ Erros:")
                for _error in validation.errors:
                    print(f"  • {_error}")

            if validation.compliance_issues:
                print("\n🚨 Issues de Compliance:")
                for _issue in validation.compliance_issues:
                    print(f"  • {_issue}")

            if persuasion.recomendacoes:
                print("\n💡 Recomendações:")
                for _rec in persuasion.recomendacoes:
                    print(f"  • {_rec}")

            if validation.is_valid:
                print("\n✅ Validação PASSOU")
            else:
                print("\n❌ Validação FALHOU")

            return 0 if validation.is_valid else 1

        except Exception:
            if args.verbose:
                import traceback

                traceback.print_exc()
            return 1


def main():
    """Main CLI entry point."""

    parser = argparse.ArgumentParser(
        description="CodeXAnuncio - Marketplace Ad Generation Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate ad from research notes
  python codex_anuncio.py generate research_notes.md

  # Generate for specific marketplace with auto-correction
  python codex_anuncio.py generate research_notes.md -m shopee --auto-correct

  # Generate trinity output (3 files)
  python codex_anuncio.py generate research_notes.md -f trinity

  # Validate existing ad
  python codex_anuncio.py validate anuncio.json
        """,
    )

    parser.add_argument("--version", action="version", version="CodeXAnuncio 1.2.0")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate ad from research notes")
    gen_parser.add_argument("input", help="Path to research_notes.md")
    gen_parser.add_argument(
        "-m",
        "--marketplace",
        choices=["mercadolivre", "shopee", "magalu", "amazon", "all"],
        default="all",
        help="Target marketplace (default: all)",
    )
    gen_parser.add_argument("-o", "--output", help="Output file path")
    gen_parser.add_argument(
        "-f",
        "--format",
        choices=["trinity", "json", "markdown"],
        default="trinity",
        help="Output format (default: trinity)",
    )
    gen_parser.add_argument("--auto-correct", action="store_true", help="Enable automatic correction loop")
    gen_parser.add_argument("--max-attempts", type=int, default=3, help="Max correction attempts (default: 3)")
    gen_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    # Validate command
    val_parser = subparsers.add_parser("validate", help="Validate existing ad")
    val_parser.add_argument("input", help="Path to anuncio JSON file")
    val_parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    # Version command
    subparsers.add_parser("version", help="Show version")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    cli = CodeXAnuncioCLI()
    return cli.run(args)


if __name__ == "__main__":
    sys.exit(main())
