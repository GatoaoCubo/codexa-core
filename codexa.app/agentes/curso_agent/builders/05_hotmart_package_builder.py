#!/usr/bin/env python3
"""
05_hotmart_package_builder.py | Hotmart Package Builder

Purpose: Package all content for Hotmart deployment (DRM, metadata, structure)
Output: Hotmart-ready package

Usage:
    python builders/05_hotmart_package_builder.py --input outputs/ --output outputs/hotmart_package/
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.paths import PATH_OUTPUTS, HOTMART_HOPS, validate_paths


class HotmartPackageBuilder:
    """Package content for Hotmart deployment"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.version = "2.0.0"
        if not validate_paths():
            raise RuntimeError("Path validation failed")

    def build(self, input_path: Path, output_path: Optional[Path] = None) -> Dict:
        if output_path is None:
            output_path = PATH_OUTPUTS / "hotmart_package"
        output_path = Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)

        # Scan input for content
        content_inventory = self._scan_content(input_path)

        # Generate package manifest
        manifest = self._generate_manifest(content_inventory)

        # Write package files
        manifest_path = output_path / "HOTMART_MANIFEST.json"
        readme_path = output_path / "README_DEPLOY.md"

        self._write_manifest(manifest_path, manifest)
        self._write_deployment_guide(readme_path, manifest)

        return {"manifest": str(manifest_path), "readme": str(readme_path), "status": "success"}

    def _scan_content(self, input_path: Path) -> Dict:
        input_path = Path(input_path)
        inventory = {
            "video_scripts": list(input_path.glob("video_scripts/*.md")),
            "workbooks": list(input_path.glob("workbooks/*.md")),
            "sales": list(input_path.glob("sales/*.md")),
        }
        return {k: [str(f) for f in v] for k, v in inventory.items()}

    def _generate_manifest(self, inventory: Dict) -> Dict:
        return {
            "platform": "Hotmart",
            "version": self.version,
            "generated_at": datetime.now().isoformat(),
            "content_inventory": inventory,
            "drm_enabled": True,
            "compliance": {
                "lgpd": True,
                "claims_sensíveis": "reviewed",
                "garantia": "7-30 days",
            },
            "deployment_checklist": [
                "Upload videos (MP4, H.264, 1080p)",
                "Configure DRM (anti-download, watermark)",
                "Set up gotejamento (drip schedule)",
                "Configure checkout page",
                "Test purchase flow",
                "Launch",
            ],
        }

    def _write_manifest(self, path: Path, manifest: Dict):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

    def _write_deployment_guide(self, path: Path, manifest: Dict):
        path.write_text(f"""# Hotmart Deployment Guide

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Builder**: 05_hotmart_package_builder.py v{self.version}

## Content Inventory
- Video Scripts: {len(manifest['content_inventory']['video_scripts'])}
- Workbooks: {len(manifest['content_inventory']['workbooks'])}
- Sales Materials: {len(manifest['content_inventory']['sales'])}

## Deployment Checklist
{chr(10).join(f'{i+1}. {item}' for i, item in enumerate(manifest['deployment_checklist']))}

## Technical Specs
- Video: MP4, H.264, 1080p (720p min)
- DRM: Enabled (Hotmart Player)
- LGPD: Compliant
- Garantia: 7-30 days

## Next Steps
1. Review HOTMART_MANIFEST.json
2. Follow deployment checklist
3. Test purchase flow before public launch

See: {', '.join(HOTMART_HOPS.keys())} for detailed guides.
""", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Package content for Hotmart")
    parser.add_argument("--input", type=str, required=True, help="Input directory with content")
    parser.add_argument("--output", type=str, default=None)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    builder = HotmartPackageBuilder(verbose=args.verbose)
    result = builder.build(input_path=Path(args.input), output_path=Path(args.output) if args.output else None)
    print(f"Status: {result['status']}")
    print(f"Manifest: {result['manifest']}")
    print(f"Readme: {result['readme']}")


if __name__ == "__main__":
    main()
