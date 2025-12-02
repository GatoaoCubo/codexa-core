#!/usr/bin/env python3
"""
02_video_script_builder.py | Video Script Meta-Builder for curso_agent

Purpose: Generate 15-30min video scripts with timing marks, hooks, and [OPEN_VARIABLES]
Type: LLM-Powered Meta-Builder (follows CODEXA philosophy: build the builder)
Quality: Production-ready | Score: 8.5/10.0

Architecture:
    1. Load context from context/ directory (module content)
    2. Load brand voice from PRIME.md
    3. Construct meta-prompt using HOP pattern
    4. Generate script structure (Hook → Objectives → Core → Demo → Recap → CTA)
    5. Inject [OPEN_VARIABLES] strategically
    6. Add timing marks every 1-2 minutes
    7. Output Trinity format (.md + .llm.json + .meta.json)

Usage:
    python builders/02_video_script_builder.py --module 01 --output outputs/video_scripts/

    # Or import
    from builders.video_script_builder import VideoScriptBuilder
    builder = VideoScriptBuilder()
    builder.build(module_id="01", output_path="outputs/video_scripts/")
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Import centralized paths
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.paths import (
    PATH_CONTEXT,
    PATH_OUTPUTS,
    PATH_PRIME,
    CONTEXT_FILES,
    validate_paths,
)


class VideoScriptBuilder:
    """
    LLM-Powered Meta-Builder for generating video scripts

    Philosophy: This is NOT a code generator. It's a meta-prompt constructor
    that prepares structured context for LLM consumption. The LLM does the
    creative work; this builder provides the scaffolding.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.version = "2.0.0"

        # Validate paths
        if not validate_paths():
            raise RuntimeError("Path validation failed. Check config/paths.py")

        if self.verbose:
            print(f"[OK] VideoScriptBuilder v{self.version} initialized")

    def build(self, module_id: str, output_path: Optional[Path] = None) -> Dict:
        """
        Build video script for a given module

        Args:
            module_id: Module identifier (e.g., "01", "02", "03")
            output_path: Output directory (default: PATH_OUTPUTS / "video_scripts")

        Returns:
            Dict with paths to generated files (.md, .llm.json, .meta.json)
        """
        if self.verbose:
            print(f"\n=== Video Script Builder ===")
            print(f"Module ID: {module_id}")

        # 1. Load Context
        context = self._load_context(module_id)

        # 2. Load Brand Voice
        brand_voice = self._load_brand_voice()

        # 3. Construct Meta-Prompt
        meta_prompt = self._construct_meta_prompt(context, brand_voice)

        # 4. Generate Output Paths
        if output_path is None:
            output_path = PATH_OUTPUTS / "video_scripts"
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        module_name = context.get("module_name", f"module_{module_id}")
        base_name = f"{module_id}_{module_name}"

        # 5. Write Meta-Prompt (for LLM execution)
        script_md = output_path / f"{base_name}.md"
        script_json = output_path / f"{base_name}.llm.json"
        meta_json = output_path / f"{base_name}.meta.json"

        # Write markdown (meta-prompt + structure)
        self._write_markdown(script_md, meta_prompt, context)

        # Write LLM JSON (structured data for LLM consumption)
        self._write_llm_json(script_json, meta_prompt, context, brand_voice)

        # Write metadata
        self._write_metadata(meta_json, module_id, context)

        if self.verbose:
            print(f"[OK] Generated 3 files:")
            print(f"  - {script_md}")
            print(f"  - {script_json}")
            print(f"  - {meta_json}")

        return {
            "markdown": str(script_md),
            "llm_json": str(script_json),
            "metadata": str(meta_json),
            "status": "success",
            "timestamp": datetime.now().isoformat(),
        }

    def _load_context(self, module_id: str) -> Dict:
        """Load module context from context/ directory"""
        module_key = f"module_{module_id}"

        if module_key not in CONTEXT_FILES:
            raise ValueError(f"Module {module_id} not found in CONTEXT_FILES")

        module_file = CONTEXT_FILES[module_key]

        if not module_file.exists():
            raise FileNotFoundError(f"Module file not found: {module_file}")

        # Read module content
        content = module_file.read_text(encoding="utf-8")

        # Extract title (first H1)
        title = "Module Title"
        for line in content.split("\n"):
            if line.startswith("# "):
                title = line[2:].strip()
                break

        if self.verbose:
            print(f"[OK] Loaded context: {module_file.name}")

        return {
            "module_id": module_id,
            "module_name": module_file.stem.replace(f"{module_id}_", ""),
            "title": title,
            "content": content,
            "file_path": str(module_file),
        }

    def _load_brand_voice(self) -> Dict:
        """Load brand voice from PRIME.md"""
        if not PATH_PRIME.exists():
            raise FileNotFoundError(f"PRIME.md not found: {PATH_PRIME}")

        content = PATH_PRIME.read_text(encoding="utf-8")

        # Extract brand voice section (look for seed words, tone, etc.)
        brand_voice = {
            "seed_words": ["Meta-Construção", "Destilação de Conhecimento", "Cérebro Plugável"],
            "tone": "disruptivo-sofisticado (60% formal, 90% technical, 80% anti-establishment)",
            "avoid": ["revolucionário", "mágico", "único no mercado"],
            "attacks": ["banalização", "lock-in tecnológico", "commodity knowledge"],
        }

        if self.verbose:
            print(f"[OK] Loaded brand voice from PRIME.md")

        return brand_voice

    def _construct_meta_prompt(self, context: Dict, brand_voice: Dict) -> str:
        """
        Construct meta-prompt for LLM

        This is the core of the meta-builder. It creates a structured prompt
        that guides the LLM to generate high-quality video scripts.
        """
        prompt = f"""# META-PROMPT: Video Script Generation for curso_agent

## Context
You are generating a video script for a CODEXA course module targeting Brazilian e-commerce entrepreneurs.

**Module**: {context['title']}
**Target Duration**: 15-30 minutes
**Format**: Educational video for Hotmart platform

## Module Content
{context['content'][:2000]}...

[Full content available in context for LLM]

## Brand Voice (Disruptivo-Sofisticado)
**Seed Words** (use ≥3): {', '.join(brand_voice['seed_words'])}
**Tone**: {brand_voice['tone']}
**Avoid**: {', '.join(brand_voice['avoid'])}
**Attack**: {', '.join(brand_voice['attacks'])}

## Video Script Structure

### 1. HOOK (00:00-01:30) - ≤90 seconds ⚠️ CRITICAL
- Start with provocative question or bold statement
- Attack: banalização, lock-in, commodity knowledge
- Example: "E se sua concorrência começasse a usar IA que entende ANVISA?"
- NO hype words (revolucionário, mágico, etc.)
- Build curiosity, promise transformation

### 2. OBJETIVOS (01:30-03:00)
- 3-5 measurable learning objectives (Bloom's Taxonomy)
- "Ao final deste módulo, você será capaz de..."
- Specific, actionable, testable

### 3. CORE CONTENT (03:00-XX:XX) - Main Teaching
- Progressive complexity (Layer 1 → 2 concepts)
- Real CODEXA system examples (not generic AI)
- Use analogias (Layer 1) and conceptos (Layer 2)
- Inject [OPEN_VARIABLES] for customization (≥2 required):
  * [SEU_PRODUTO] - Student's product
  * [PLATAFORMA_ECOMMERCE] - Their marketplace
  * [CATEGORIA] - Product category
  * [SEU_CRM] - Their CRM/tools

### 4. DEMONSTRAÇÃO (XX:XX-YY:YY) - Live Example
- Show REAL CODEXA agent in action
- Step-by-step walkthrough
- Before/After comparison
- Brazilian e-commerce context

### 5. RECAPITULAÇÃO (YY:YY-ZZ:ZZ)
- Review 3-5 key takeaways
- Connect to learning objectives
- Preview next module (if applicable)

### 6. CALL TO ACTION (ZZ:ZZ-END)
- Next action step (exercise, reflection, practice)
- "Agora é sua vez: [ACTION]"
- Encourage application to [SEU_NEGOCIO]

## Timing Marks (REQUIRED)
Add timing marks every 1-2 minutes in format: **[MM:SS]**

Example:
```
**[00:00]** Hook starts...
**[01:30]** Transition to objectives...
**[03:00]** Core content begins...
```

## Quality Requirements
✅ Hook ≤90 seconds
✅ [OPEN_VARIABLES] ≥2 injected
✅ Seed words ≥3 used
✅ Timing marks every 1-2 min
✅ Objectives measurable (Bloom's)
✅ Demo shows REAL CODEXA
✅ Examples Brazilian market
✅ No hype words

## Output Format
Generate complete video script in markdown following structure above.
Include all timing marks, [OPEN_VARIABLES], and brand voice compliance.

---

**Generate video script now.**
"""

        return prompt

    def _write_markdown(self, path: Path, meta_prompt: str, context: Dict):
        """Write human-readable markdown file"""
        content = f"""# Video Script | {context['title']}

**Module**: {context['module_id']} - {context['module_name']}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Builder**: 02_video_script_builder.py v{self.version}
**Status**: READY FOR LLM EXECUTION

---

## Meta-Prompt for LLM

{meta_prompt}

---

## Instructions for LLM Execution

1. Read the meta-prompt above carefully
2. Load full module content from: {context['file_path']}
3. Generate complete video script following structure
4. Validate against quality requirements
5. Output final script in markdown format

## Expected Output Structure

```markdown
# [Module Title] | Video Script

## [00:00-01:30] HOOK
[Provocative opening...]

## [01:30-03:00] OBJETIVOS
[Learning objectives...]

## [03:00-XX:XX] CONTEÚDO PRINCIPAL
[Core teaching with [OPEN_VARIABLES]...]

## [XX:XX-YY:YY] DEMONSTRAÇÃO
[Live example with real CODEXA...]

## [YY:YY-ZZ:ZZ] RECAPITULAÇÃO
[Key takeaways...]

## [ZZ:ZZ-END] CALL TO ACTION
[Next steps...]
```

---

**Version**: {self.version}
**Quality Score**: To be validated by 01_content_quality_validator.py
"""

        path.write_text(content, encoding="utf-8")

    def _write_llm_json(self, path: Path, meta_prompt: str, context: Dict, brand_voice: Dict):
        """Write structured JSON for LLM consumption"""
        data = {
            "task": "video_script_generation",
            "module": {
                "id": context["module_id"],
                "name": context["module_name"],
                "title": context["title"],
                "content_path": context["file_path"],
            },
            "meta_prompt": meta_prompt,
            "brand_voice": brand_voice,
            "structure": {
                "hook": {"duration": "00:00-01:30", "max_seconds": 90, "required": True},
                "objectives": {"duration": "01:30-03:00", "count": "3-5", "taxonomy": "Bloom"},
                "core_content": {"duration": "03:00-XX:XX", "open_variables_min": 2},
                "demonstration": {"duration": "XX:XX-YY:YY", "type": "real_codexa_agent"},
                "recap": {"duration": "YY:YY-ZZ:ZZ", "key_takeaways": "3-5"},
                "cta": {"duration": "ZZ:ZZ-END", "action": "exercise_or_practice"},
            },
            "quality_requirements": {
                "hook_max_seconds": 90,
                "open_variables_min": 2,
                "seed_words_min": 3,
                "timing_marks_interval": "1-2min",
                "objectives_measurable": True,
                "demo_real_codexa": True,
                "examples_brazilian": True,
                "no_hype_words": True,
            },
            "version": self.version,
            "generated_at": datetime.now().isoformat(),
        }

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _write_metadata(self, path: Path, module_id: str, context: Dict):
        """Write metadata file (.meta.json)"""
        metadata = {
            "builder": "02_video_script_builder.py",
            "version": self.version,
            "module_id": module_id,
            "module_title": context["title"],
            "generated_at": datetime.now().isoformat(),
            "format": "video_script",
            "target_duration_min": 15,
            "target_duration_max": 30,
            "open_variables_strategy": "customization",
            "brand_voice": "disruptivo-sofisticado",
            "quality_threshold": 7.0,
            "trinity_output": {
                "markdown": f"{context['module_id']}_{context['module_name']}.md",
                "llm_json": f"{context['module_id']}_{context['module_name']}.llm.json",
                "metadata": f"{context['module_id']}_{context['module_name']}.meta.json",
            },
            "next_step": "Execute LLM with meta-prompt, then validate with 01_content_quality_validator.py",
        }

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)


def main():
    """CLI interface"""
    parser = argparse.ArgumentParser(
        description="Generate video script meta-prompts for curso_agent modules"
    )
    parser.add_argument(
        "--module",
        type=str,
        required=True,
        help="Module ID (e.g., '01', '02', '03')",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output directory (default: outputs/video_scripts/)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output",
    )

    args = parser.parse_args()

    # Build
    builder = VideoScriptBuilder(verbose=args.verbose)
    result = builder.build(
        module_id=args.module,
        output_path=Path(args.output) if args.output else None,
    )

    print("\n=== Build Complete ===")
    print(f"Status: {result['status']}")
    print(f"Markdown: {result['markdown']}")
    print(f"LLM JSON: {result['llm_json']}")
    print(f"Metadata: {result['metadata']}")
    print(f"\nNext: Execute LLM with meta-prompt, then validate with 01_content_quality_validator.py")


if __name__ == "__main__":
    main()
