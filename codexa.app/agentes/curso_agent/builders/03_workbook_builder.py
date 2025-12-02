#!/usr/bin/env python3
"""
03_workbook_builder.py | Workbook Meta-Builder

Purpose: Generate 8-15 page workbooks (theory + exercises + reflection)
Output: Trinity format

Usage:
    python builders/03_workbook_builder.py --module 01 --output outputs/workbooks/
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.paths import PATH_CONTEXT, PATH_OUTPUTS, CONTEXT_FILES, validate_paths


class WorkbookBuilder:
    """Generate workbooks with theory, exercises, and reflection questions"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.version = "2.0.0"
        if not validate_paths():
            raise RuntimeError("Path validation failed")

    def build(self, module_id: str, output_path: Optional[Path] = None) -> Dict:
        context = self._load_context(module_id)
        meta_prompt = self._construct_meta_prompt(context)

        if output_path is None:
            output_path = PATH_OUTPUTS / "workbooks"
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        base_name = f"{module_id}_workbook"
        wb_md = output_path / f"{base_name}.md"
        wb_json = output_path / f"{base_name}.llm.json"
        meta_json = output_path / f"{base_name}.meta.json"

        self._write_files(wb_md, wb_json, meta_json, meta_prompt, context)

        return {"markdown": str(wb_md), "llm_json": str(wb_json), "metadata": str(meta_json), "status": "success"}

    def _load_context(self, module_id: str) -> Dict:
        module_key = f"module_{module_id}"
        if module_key not in CONTEXT_FILES:
            raise ValueError(f"Module {module_id} not found")
        return {
            "module_id": module_id,
            "content": CONTEXT_FILES[module_key].read_text(encoding="utf-8"),
        }

    def _construct_meta_prompt(self, context: Dict) -> str:
        return f"""# META-PROMPT: Workbook Generation

## Task
Generate 8-15 page workbook for Module {context['module_id']}.

## Structure
1. **Cover Page** - Title, objectives, time estimate
2. **Theory Section** - Key concepts (2-3 pages)
3. **Guided Exercises** - Step-by-step (3-4 pages)
4. **Hands-On Practice** - Student does it (2-3 pages)
5. **Reflection Questions** - Deep thinking (1 page)
6. **Resources & Next Steps** - Links, references (1 page)

## Requirements
- Total: 8-15 pages
- Exercises actionable (students DO something)
- [OPEN_VARIABLES] >=2 for customization
- PDF-ready formatting

## Content
{context['content'][:1000]}...
"""

    def _write_files(self, md_path, json_path, meta_path, prompt, context):
        md_path.write_text(f"""# Workbook | Module {context['module_id']}

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Builder**: 03_workbook_builder.py v{self.version}

---

## Meta-Prompt

{prompt}
""", encoding="utf-8")

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({"task": "workbook_generation", "module_id": context['module_id'], "meta_prompt": prompt, "version": self.version}, f, indent=2, ensure_ascii=False)

        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump({"builder": "03_workbook_builder.py", "version": self.version, "module_id": context['module_id'], "format": "workbook", "pages_target": "8-15"}, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Generate workbooks")
    parser.add_argument("--module", type=str, required=True)
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    builder = WorkbookBuilder(verbose=args.verbose)
    result = builder.build(module_id=args.module, output_path=Path(args.output) if args.output else None)
    print(f"Status: {result['status']}, Output: {result['markdown']}")


if __name__ == "__main__":
    main()
