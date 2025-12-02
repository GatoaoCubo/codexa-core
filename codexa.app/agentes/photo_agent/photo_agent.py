#!/usr/bin/env python3
"""
Photo Agent CLI - Marketplace & Brand Photography Prompt Generator

Purpose: Generate 9 photography prompts for Brazilian marketplaces or brand social media
Workflows:
  - marketplace: E-commerce listings (ML, Shopee, Amazon BR, Magalu)
  - brand: Social media content (Instagram, TikTok, Pinterest)

Usage:
  # Marketplace workflow
  python photo_agent.py --workflow marketplace --subject "Garrafa de água 750ml aço inox" --output outputs/garrafa

  # Brand workflow
  python photo_agent.py --workflow brand --subject "Garrafa HeroWater" --brand-strategy USER_DOCS/Marca/hero_water_brand_strategy.md --output outputs/hero_water_social

Version: 1.0.0
Author: CODEXA Meta-Construction System
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
import hashlib

# Import centralized path configuration
sys.path.insert(0, str(Path(__file__).parent))
from config.paths import (
    PATH_SCHEMAS,
    PATH_EXAMPLES,
    PATH_OUTPUTS,
)

# Import processors (to be created)
try:
    from processor import generate_marketplace_prompts, generate_brand_prompts
    from trinity_writer import write_trinity_output
except ImportError:
    print("⚠️  WARNING: processor.py or trinity_writer.py not found. Creating placeholder functions.")

    def generate_marketplace_prompts(subject, style="commercial"):
        """Placeholder for marketplace prompt generation"""
        return {"error": "processor.py not implemented yet"}

    def generate_brand_prompts(subject, brand_strategy_path, style="lifestyle"):
        """Placeholder for brand prompt generation"""
        return {"error": "processor.py not implemented yet"}

    def write_trinity_output(data, output_path, workflow):
        """Placeholder for trinity output writer"""
        print(f"⚠️  trinity_writer.py not implemented. Would write to: {output_path}")
        return {
            "markdown": f"{output_path}.md",
            "llm_json": f"{output_path}.llm.json",
            "metadata_json": f"{output_path}.meta.json"
        }


def parse_arguments():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Photo Agent - Generate photography prompts for marketplace or brand social media",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Marketplace workflow:
    python photo_agent.py --workflow marketplace --subject "Garrafa água 750ml aço inox" --output outputs/garrafa

  Brand workflow:
    python photo_agent.py --workflow brand --subject "Garrafa HeroWater" --brand-strategy USER_DOCS/Marca/hero_water_brand_strategy.md --output outputs/hero_water
        """
    )

    # Required arguments
    parser.add_argument(
        "--workflow",
        type=str,
        required=True,
        choices=["marketplace", "brand"],
        help="Workflow type: marketplace (e-commerce) or brand (social media)"
    )

    parser.add_argument(
        "--subject",
        type=str,
        required=True,
        help="Product description (e.g., 'Garrafa de água 750ml aço inox')"
    )

    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output base path (without extension, e.g., 'outputs/garrafa')"
    )

    # Optional arguments
    parser.add_argument(
        "--style",
        type=str,
        default=None,
        choices=["minimalist", "dramatic", "lifestyle", "editorial", "commercial"],
        help="Photography style preset (default: commercial for marketplace, lifestyle for brand)"
    )

    parser.add_argument(
        "--brand-strategy",
        type=str,
        default=None,
        help="Path to brand_strategy.md from marca_agent (required for brand workflow)"
    )

    parser.add_argument(
        "--marketplace",
        type=str,
        default="all",
        choices=["mercadolivre", "shopee", "magalu", "amazon_br", "all"],
        help="Target marketplace (marketplace workflow only, default: all)"
    )

    parser.add_argument(
        "--platforms",
        type=str,
        nargs="+",
        default=["instagram_feed", "instagram_stories"],
        choices=["instagram_feed", "instagram_stories", "facebook", "tiktok", "pinterest", "linkedin"],
        help="Target social media platforms (brand workflow only)"
    )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run validation after generation"
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="photo_agent v1.0.0"
    )

    return parser.parse_args()


def validate_inputs(args):
    """Validate input arguments"""
    errors = []

    # Brand workflow requires brand-strategy
    if args.workflow == "brand" and not args.brand_strategy:
        errors.append("--brand-strategy is required for brand workflow")

    # Check if brand-strategy file exists (if provided)
    if args.brand_strategy:
        brand_strategy_path = Path(args.brand_strategy)
        if not brand_strategy_path.exists():
            errors.append(f"Brand strategy file not found: {args.brand_strategy}")

    # Validate output path
    output_path = Path(args.output)
    output_dir = output_path.parent
    if not output_dir.exists():
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            if args.verbose:
                print(f"[OK] Created output directory: {output_dir}")
        except Exception as e:
            errors.append(f"Cannot create output directory {output_dir}: {e}")

    return errors


def load_schema(workflow_type):
    """Load appropriate schema based on workflow type"""
    schema_map = {
        "marketplace": "photo_marketplace_output.json",
        "brand": "photo_brand_output.json"
    }

    schema_path = PATH_SCHEMAS / schema_map[workflow_type]

    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema = json.load(f)
        return schema
    except FileNotFoundError:
        print(f"[WARN] WARNING: Schema not found: {schema_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in schema {schema_path}: {e}")
        sys.exit(1)


def compute_input_hash(subject, workflow, **kwargs):
    """Compute SHA256 hash of input for traceability"""
    input_str = f"{subject}|{workflow}|{json.dumps(kwargs, sort_keys=True)}"
    return hashlib.sha256(input_str.encode('utf-8')).hexdigest()


def main():
    """Main execution flow"""
    args = parse_arguments()

    # Print header
    print("=" * 60)
    print("Photo Agent v1.0.0 - Photography Prompt Generator")
    print(f"Workflow: {args.workflow.upper()}")
    print("=" * 60)
    print()

    # Validate inputs
    if args.verbose:
        print("[*] Validating inputs...")

    errors = validate_inputs(args)
    if errors:
        print("[ERROR] INPUT VALIDATION ERRORS:")
        for error in errors:
            print(f"   - {error}")
        sys.exit(1)

    if args.verbose:
        print("[OK] Input validation passed")
        print()

    # Load appropriate schema
    if args.verbose:
        print(f"[*] Loading {args.workflow} schema...")

    schema = load_schema(args.workflow)
    if schema and args.verbose:
        print(f"[OK] Schema loaded: {schema.get('title', 'Unknown')}")
        print()

    # Generate prompts based on workflow
    print(f"[*] Generating {args.workflow} prompts...")
    print(f"   Subject: {args.subject}")

    start_time = datetime.now()

    try:
        if args.workflow == "marketplace":
            # Marketplace workflow
            style = args.style or "commercial"
            print(f"   Style: {style}")
            print(f"   Target: {args.marketplace}")
            print()

            output_data = generate_marketplace_prompts(
                subject=args.subject,
                style=style
            )

            # Add metadata
            if "metadata" not in output_data:
                output_data["metadata"] = {}

            output_data["metadata"].update({
                "target_marketplace": args.marketplace,
                "input_subject": args.subject,
                "generation_time_ms": int((datetime.now() - start_time).total_seconds() * 1000),
                "input_hash": compute_input_hash(args.subject, args.workflow, style=style, marketplace=args.marketplace)
            })

        elif args.workflow == "brand":
            # Brand workflow
            style = args.style or "lifestyle"
            print(f"   Style: {style}")
            print(f"   Brand Strategy: {args.brand_strategy}")
            print(f"   Platforms: {', '.join(args.platforms)}")
            print()

            output_data = generate_brand_prompts(
                subject=args.subject,
                brand_strategy_path=args.brand_strategy,
                style=style
            )

            # Add metadata
            if "metadata" not in output_data:
                output_data["metadata"] = {}

            output_data["metadata"].update({
                "target_platforms": args.platforms,
                "input_subject": args.subject,
                "generation_time_ms": int((datetime.now() - start_time).total_seconds() * 1000),
                "input_hash": compute_input_hash(args.subject, args.workflow, style=style, brand_strategy=args.brand_strategy)
            })

    except Exception as e:
        print(f"[ERROR] ERROR during prompt generation: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

    # Check for errors in output
    if "error" in output_data:
        print(f"[WARN] {output_data['error']}")
        print("   Processor not fully implemented yet.")
        print()
        print("[OK] EXAMPLES AVAILABLE:")
        examples_dir = PATH_EXAMPLES
        if examples_dir.exists():
            example_files = list(examples_dir.glob("*.md"))
            for ex in example_files:
                print(f"   - {ex.name}")
        sys.exit(0)

    # Write Trinity output
    print("[*] Writing Trinity output (.md + .llm.json + .meta.json)...")

    try:
        trinity_files = write_trinity_output(
            data=output_data,
            output_path=args.output,
            workflow=args.workflow
        )

        print("[OK] OUTPUT FILES:")
        print(f"   - Markdown: {trinity_files['markdown']}")
        print(f"   - LLM JSON: {trinity_files['llm_json']}")
        print(f"   - Metadata: {trinity_files['metadata_json']}")
        print()

    except Exception as e:
        print(f"[ERROR] ERROR writing output: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

    # Validation (if requested)
    if args.validate:
        print("[*] Running validation...")
        # TODO: Call validators
        print("[WARN] Validators not implemented yet")
        print()

    # Summary
    total_time = (datetime.now() - start_time).total_seconds()
    print("=" * 60)
    print(f"[SUCCESS] Generated {args.workflow} prompts")
    print(f"[TIME] Total time: {total_time:.2f}s")
    print("=" * 60)


if __name__ == "__main__":
    main()
