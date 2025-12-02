#!/usr/bin/env python3
"""
01_course_outline_builder.py | Course Outline Meta-Builder

Purpose: Generate course outlines (modules, objectives, timing, prerequisites)
Architecture: LLM-Powered Meta-Builder (generates structured prompts)
Output: Trinity format (.md + .llm.json + .meta.json)

Usage:
    python builders/01_course_outline_builder.py --scope "1-2" --duration 20 --output outputs/outlines/
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.paths import PATH_CONTEXT, PATH_OUTPUTS, PATH_PRIME, CONTEXT_FILES, validate_paths


class CourseOutlineBuilder:
    """Generate course outlines with module structure, objectives, and timing"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.version = "2.0.0"

        if not validate_paths():
            raise RuntimeError("Path validation failed")

        if self.verbose:
            print(f"[OK] CourseOutlineBuilder v{self.version} initialized")

    def build(self, scope: str, duration_hours: int, output_path: Optional[Path] = None) -> Dict:
        """
        Build course outline

        Args:
            scope: Layer scope ("1", "1-2", "1-2-3", "custom")
            duration_hours: Target duration in hours (10-50)
            output_path: Output directory

        Returns:
            Dict with paths to generated files
        """
        if self.verbose:
            print(f"\n=== Course Outline Builder ===")
            print(f"Scope: Layer {scope}")
            print(f"Duration: {duration_hours}h")

        # Load all context
        context = self._load_all_context()

        # Construct meta-prompt
        meta_prompt = self._construct_meta_prompt(scope, duration_hours, context)

        # Generate outputs
        if output_path is None:
            output_path = PATH_OUTPUTS / "outlines"
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        base_name = f"outline_layer_{scope.replace('-', '_')}_{duration_hours}h"

        outline_md = output_path / f"{base_name}.md"
        outline_json = output_path / f"{base_name}.llm.json"
        meta_json = output_path / f"{base_name}.meta.json"

        self._write_markdown(outline_md, meta_prompt, scope, duration_hours)
        self._write_llm_json(outline_json, meta_prompt, scope, duration_hours, context)
        self._write_metadata(meta_json, scope, duration_hours)

        if self.verbose:
            print(f"[OK] Generated: {outline_md}")

        return {
            "markdown": str(outline_md),
            "llm_json": str(outline_json),
            "metadata": str(meta_json),
            "status": "success",
            "timestamp": datetime.now().isoformat(),
        }

    def _load_all_context(self) -> Dict:
        """Load all course context files"""
        context = {}
        for key, path in CONTEXT_FILES.items():
            if path.exists():
                context[key] = path.read_text(encoding="utf-8")[:500]  # Preview only
        return context

    def _construct_meta_prompt(self, scope: str, duration: int, context: Dict) -> str:
        """Construct meta-prompt for outline generation"""
        prompt = f"""# META-PROMPT: Course Outline Generation

## Task
Generate complete course outline for CODEXA e-commerce education.

**Scope**: Layer {scope}
**Duration**: {duration} hours total
**Target**: Brazilian e-commerce entrepreneurs

## Requirements

### Module Structure
- Module count: {self._calculate_module_count(duration)}
- Duration per module: {duration // self._calculate_module_count(duration)}h average
- Progressive complexity: Layer 1 → 2 → 3

### Each Module Must Have:
1. **Title** - Clear, outcome-focused (e.g., "Dominar anuncio_agent")
2. **Learning Objectives** - 3-5 measurable (Bloom's Taxonomy)
3. **Duration** - Realistic estimate (theory + practice + exercises)
4. **Prerequisites** - What student needs before starting
5. **Key Topics** - 5-7 bullet points
6. **Deliverables** - What student creates/produces
7. **Layer Mapping** - Which CODEXA layers covered

### Quality Requirements
- Objectives measurable (use Bloom's verbs)
- Duration realistic (tested or well-reasoned)
- Prerequisites explicit (no hidden dependencies)
- Topics actionable (students can DO something)
- Deliverables concrete (actual files/outputs)

## Available Content
{len(context)} context files loaded:
{', '.join(context.keys())}

## Output Format
Generate markdown outline with modules, objectives, timing, prerequisites.
"""
        return prompt

    def _calculate_module_count(self, duration_hours: int) -> int:
        """Calculate optimal module count based on duration"""
        if duration_hours <= 10:
            return 4
        elif duration_hours <= 20:
            return 6
        elif duration_hours <= 30:
            return 8
        else:
            return 10

    def _write_markdown(self, path: Path, meta_prompt: str, scope: str, duration: int):
        """Write markdown file"""
        content = f"""# Course Outline | CODEXA E-COM LM

**Scope**: Layer {scope}
**Duration**: {duration} hours
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Builder**: 01_course_outline_builder.py v{self.version}

---

## Meta-Prompt for LLM

{meta_prompt}

---

**Next**: Execute LLM to generate complete outline, then use other builders for content.
"""
        path.write_text(content, encoding="utf-8")

    def _write_llm_json(self, path: Path, meta_prompt: str, scope: str, duration: int, context: Dict):
        """Write LLM JSON"""
        data = {
            "task": "course_outline_generation",
            "scope": scope,
            "duration_hours": duration,
            "module_count": self._calculate_module_count(duration),
            "meta_prompt": meta_prompt,
            "context_files": list(context.keys()),
            "version": self.version,
            "generated_at": datetime.now().isoformat(),
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _write_metadata(self, path: Path, scope: str, duration: int):
        """Write metadata"""
        metadata = {
            "builder": "01_course_outline_builder.py",
            "version": self.version,
            "scope": scope,
            "duration_hours": duration,
            "module_count": self._calculate_module_count(duration),
            "generated_at": datetime.now().isoformat(),
            "format": "course_outline",
            "quality_threshold": 7.0,
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Generate course outlines")
    parser.add_argument("--scope", type=str, required=True, help="Layer scope (1, 1-2, 1-2-3)")
    parser.add_argument("--duration", type=int, required=True, help="Duration in hours (10-50)")
    parser.add_argument("--output", type=str, default=None, help="Output directory")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    builder = CourseOutlineBuilder(verbose=args.verbose)
    result = builder.build(
        scope=args.scope,
        duration_hours=args.duration,
        output_path=Path(args.output) if args.output else None,
    )

    print(f"\n=== Build Complete ===")
    print(f"Status: {result['status']}")
    print(f"Output: {result['markdown']}")


if __name__ == "__main__":
    main()
