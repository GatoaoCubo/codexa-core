#!/usr/bin/env python3
"""
04_sales_collateral_builder.py | Sales Collateral Meta-Builder

Purpose: Generate landing pages, email sequences (6 emails), ad copy (3 platforms)
Output: Trinity format

Usage:
    python builders/04_sales_collateral_builder.py --course "CODEXA Layer 1-2" --output outputs/sales/
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.paths import PATH_OUTPUTS, PATH_PRIME, validate_paths


class SalesCollateralBuilder:
    """Generate sales collateral (landing page, emails, ads)"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.version = "2.0.0"
        if not validate_paths():
            raise RuntimeError("Path validation failed")

    def build(self, course_name: str, output_path: Optional[Path] = None) -> Dict:
        brand_voice = self._load_brand_voice()
        meta_prompt = self._construct_meta_prompt(course_name, brand_voice)

        if output_path is None:
            output_path = PATH_OUTPUTS / "sales"
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        # Extract basename if course_name is a file path
        if "/" in course_name or "\\" in course_name:
            course_path = Path(course_name)
            base_name = course_path.stem  # Get filename without extension
        else:
            base_name = course_name.lower().replace(" ", "_")
        sales_md = output_path / f"{base_name}_sales.md"
        sales_json = output_path / f"{base_name}_sales.llm.json"
        meta_json = output_path / f"{base_name}_sales.meta.json"

        self._write_files(sales_md, sales_json, meta_json, meta_prompt, course_name, brand_voice)

        return {"markdown": str(sales_md), "llm_json": str(sales_json), "metadata": str(meta_json), "status": "success"}

    def _load_brand_voice(self) -> Dict:
        return {
            "seed_words": ["Meta-Construção", "Destilação de Conhecimento", "Cérebro Plugável"],
            "tone": "disruptivo-sofisticado",
            "avoid": ["revolucionário", "mágico", "único no mercado"],
        }

    def _construct_meta_prompt(self, course_name: str, brand_voice: Dict) -> str:
        return f"""# META-PROMPT: Sales Collateral Generation

## Task
Generate complete sales package for "{course_name}".

## Deliverables
1. **Landing Page** (Hero, Problem, Solution, Proof, FAQ, CTA)
2. **Email Sequence** (6 emails: Awareness, Interest, Desire, Action, Onboarding, Engagement)
3. **Ad Copy** (Facebook, Google, LinkedIn variations)

## Brand Voice
**Seed Words**: {', '.join(brand_voice['seed_words'])}
**Tone**: {brand_voice['tone']}
**Avoid**: {', '.join(brand_voice['avoid'])}

## Requirements
- Landing page Hotmart-optimized
- Emails 200-400 words each
- Ads 50-150 characters
- [OPEN_VARIABLES] >=2: [PRECO], [GARANTIA_DIAS], [BONUS]
- Attack: banalização, lock-in, commodity knowledge

## Course
{course_name}
"""

    def _write_files(self, md_path, json_path, meta_path, prompt, course, brand):
        md_path.write_text(f"""# Sales Collateral | {course}

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Builder**: 04_sales_collateral_builder.py v{self.version}

---

## Meta-Prompt

{prompt}
""", encoding="utf-8")

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({"task": "sales_collateral", "course": course, "meta_prompt": prompt, "brand_voice": brand, "version": self.version}, f, indent=2, ensure_ascii=False)

        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump({"builder": "04_sales_collateral_builder.py", "version": self.version, "course": course, "format": "sales_package"}, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Generate sales collateral")
    parser.add_argument("--course", type=str, required=True)
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    builder = SalesCollateralBuilder(verbose=args.verbose)
    result = builder.build(course_name=args.course, output_path=Path(args.output) if args.output else None)
    print(f"Status: {result['status']}, Output: {result['markdown']}")


if __name__ == "__main__":
    main()
