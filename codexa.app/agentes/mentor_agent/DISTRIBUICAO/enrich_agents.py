#!/usr/bin/env python3
"""
Agent Enricher - Injeta conhecimento dos CAPITULOS em prompts de agentes

Purpose: Ler knowledge_map.json, extrair versículos, injetar em prompts
Input: knowledge_map.json + CAPITULOS (via knowledge_extractor)
Output: Prompts enriquecidos + .knowledge_version tracking

Usage:
    # Enrich all prompts for anuncio_agent
    python enrich_agents.py --agent anuncio_agent

    # Enrich specific mapping
    python enrich_agents.py --mapping anuncio_titulo_generator_v1

    # Dry-run (don't modify files)
    python enrich_agents.py --agent anuncio_agent --dry-run

Version: 1.0.0
Author: CODEXA Meta-Construction System
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import shutil
import sys

# Add config to path for centralized path management
sys.path.insert(0, str(Path(__file__).parent.parent / 'config'))
from paths import PATH_DISTRIBUICAO

# Import knowledge extractor
from knowledge_extractor import KnowledgeExtractor


class PromptNotFoundError(Exception):
    """Raised when target prompt file not found"""
    pass


class InjectionError(Exception):
    """Raised when injection fails"""
    pass


class AgentEnricher:
    """Injeta conhecimento em prompts de agentes"""

    def __init__(
        self,
        knowledge_map_path: Optional[Path] = None,
        dry_run: bool = False
    ):
        """
        Initialize enricher

        Args:
            knowledge_map_path: Path to knowledge_map.json
                              If None, uses centralized config
            dry_run: If True, don't modify files (just show what would happen)
        """
        if knowledge_map_path is None:
            knowledge_map_path = PATH_DISTRIBUICAO / "knowledge_map.json"

        self.knowledge_map_path = Path(knowledge_map_path)
        self.dry_run = dry_run
        self.extractor = KnowledgeExtractor()

        # Load knowledge map
        with open(self.knowledge_map_path, "r", encoding="utf-8") as f:
            self.knowledge_map = json.load(f)

        # Base directory (mentor_agent/)
        self.base_dir = self.knowledge_map_path.parent.parent

    def get_mappings_for_agent(self, agent_name: str) -> List[Dict]:
        """Get all mappings for a specific agent"""
        return [
            m for m in self.knowledge_map["mappings"]
            if m["agent"] == agent_name
        ]

    def get_mapping_by_id(self, mapping_id: str) -> Optional[Dict]:
        """Get mapping by ID"""
        for m in self.knowledge_map["mappings"]:
            if m["id"] == mapping_id:
                return m
        return None

    def extract_knowledge_for_mapping(
        self,
        mapping: Dict
    ) -> List[Dict]:
        """
        Extract all versículos for a mapping

        Args:
            mapping: Mapping dict from knowledge_map.json

        Returns:
            List of extracted versículo dicts (sorted by priority)
        """
        versiculos_config = mapping.get("versiculos", [])

        # Sort by priority (lower priority = higher importance)
        versiculos_config_sorted = sorted(
            versiculos_config,
            key=lambda v: v.get("priority", 999)
        )

        # Extract each versículo
        extracted = []

        for v_config in versiculos_config_sorted:
            ref = v_config["ref"]

            try:
                v_data = self.extractor.extract_versiculo(ref)
                v_data["config"] = v_config  # Add config metadata
                extracted.append(v_data)

            except Exception as e:
                print(f"WARNING: Failed to extract {ref}: {e}", file=sys.stderr)
                extracted.append({
                    "ref": ref,
                    "config": v_config,
                    "error": str(e),
                    "content": None
                })

        return extracted

    def format_knowledge_section(
        self,
        mapping: Dict,
        extracted_versiculos: List[Dict]
    ) -> str:
        """
        Format knowledge section for injection

        Args:
            mapping: Mapping dict
            extracted_versiculos: List of extracted versículo dicts

        Returns:
            Formatted markdown section
        """
        section_marker = mapping.get("inject_section", "## 📚 CONHECIMENTO TÉCNICO")
        max_tokens = mapping.get("max_tokens", 2000)

        # Build section
        lines = [section_marker, ""]

        # Add intro note
        lines.append(
            "*Este conhecimento foi injetado automaticamente do mentor_agent "
            "para enriquecer este prompt com expertise técnica validada.*"
        )
        lines.append("")

        # Add each versículo
        for v_data in extracted_versiculos:
            if v_data.get("error"):
                # Skip failed extractions
                continue

            config = v_data["config"]
            tema = config.get("tema", "Conhecimento Técnico")
            relevance = config.get("relevance", 0.0)
            tags = config.get("tags", [])

            # Add versículo header
            lines.append(f"### {tema}")
            lines.append(f"*Relevância: {relevance:.2f} | Tags: {', '.join(tags)}*")
            lines.append("")

            # Add content
            content = v_data["content"]
            lines.append(content)
            lines.append("")

            # Check token limit (rough estimate: 4 chars = 1 token)
            current_text = "\n".join(lines)
            estimated_tokens = len(current_text) // 4

            if estimated_tokens > max_tokens:
                lines.append(
                    f"*... (conteúdo truncado por limite de {max_tokens} tokens)*"
                )
                break

        # Add footer with metadata
        lines.append("---")
        lines.append("")
        lines.append("**Metadados da Injeção:**")
        lines.append(f"- **Versículos injetados**: {len([v for v in extracted_versiculos if not v.get('error')])}")
        lines.append(f"- **Fonte**: mentor_agent/PROCESSADOS/")
        lines.append(f"- **Última atualização**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"- **Versão do schema**: {self.knowledge_map.get('version', '1.0.0')}")
        lines.append("")

        refs = [v["ref"] for v in extracted_versiculos if not v.get("error")]
        lines.append(f"**Referências**: `{', '.join(refs)}`")
        lines.append("")

        return "\n".join(lines)

    def find_injection_position(
        self,
        prompt_content: str,
        mapping: Dict
    ) -> int:
        """
        Find position to inject knowledge section

        Args:
            prompt_content: Original prompt content
            mapping: Mapping dict with inject_position config

        Returns:
            Character position where to inject (or -1 if not found)
        """
        inject_pos_config = mapping.get("inject_position", {})

        if not inject_pos_config:
            # Default: inject at end
            return len(prompt_content)

        anchor = inject_pos_config.get("anchor")
        placement = inject_pos_config.get("placement", "before")
        offset = inject_pos_config.get("offset", 0)

        if not anchor:
            return len(prompt_content)

        # Find anchor in content
        anchor_match = re.search(re.escape(anchor), prompt_content, re.MULTILINE)

        if not anchor_match:
            print(
                f"WARNING: Anchor '{anchor}' not found in prompt. "
                f"Injecting at end.",
                file=sys.stderr
            )
            return len(prompt_content)

        # Calculate position
        if placement == "before":
            pos = anchor_match.start()
        else:  # after
            pos = anchor_match.end()

        # Apply offset (move position by N lines)
        if offset != 0:
            # Find Nth newline before/after position
            if offset < 0:
                # Move backward
                for _ in range(abs(offset)):
                    pos = prompt_content.rfind("\n", 0, pos)
                    if pos == -1:
                        pos = 0
                        break
            else:
                # Move forward
                for _ in range(offset):
                    pos = prompt_content.find("\n", pos + 1)
                    if pos == -1:
                        pos = len(prompt_content)
                        break

        return pos

    def inject_knowledge(
        self,
        mapping: Dict,
        extracted_versiculos: List[Dict]
    ) -> Dict:
        """
        Inject knowledge into prompt file

        Args:
            mapping: Mapping dict
            extracted_versiculos: List of extracted versículo dicts

        Returns:
            Dict with injection result (success, message, prompt_path, backup_path)
        """
        # Build paths
        agent_name = mapping["agent"]
        prompt_file = mapping["prompt_file"]
        agent_dir = self.base_dir.parent / agent_name
        prompt_path = agent_dir / prompt_file

        if not prompt_path.exists():
            raise PromptNotFoundError(
                f"Prompt file not found: {prompt_path}"
            )

        # Read original prompt
        with open(prompt_path, "r", encoding="utf-8") as f:
            original_content = f.read()

        # Check if knowledge section already exists
        section_marker = mapping.get("inject_section", "## 📚 CONHECIMENTO TÉCNICO")

        if section_marker in original_content:
            # Remove existing section
            original_content = self._remove_existing_section(
                original_content,
                section_marker
            )

        # Format knowledge section
        knowledge_section = self.format_knowledge_section(
            mapping,
            extracted_versiculos
        )

        # Find injection position
        inject_pos = self.find_injection_position(original_content, mapping)

        # Build enriched content
        enriched_content = (
            original_content[:inject_pos] +
            "\n\n" +
            knowledge_section +
            "\n\n" +
            original_content[inject_pos:]
        )

        # Dry-run check
        if self.dry_run:
            return {
                "success": True,
                "message": f"[DRY-RUN] Would inject knowledge into {prompt_path}",
                "prompt_path": str(prompt_path),
                "backup_path": None,
                "dry_run": True
            }

        # Create backup
        backup_path = prompt_path.with_suffix(f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
        shutil.copy2(prompt_path, backup_path)

        # Write enriched content
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(enriched_content)

        return {
            "success": True,
            "message": f"Successfully injected knowledge into {prompt_path}",
            "prompt_path": str(prompt_path),
            "backup_path": str(backup_path),
            "dry_run": False
        }

    def _remove_existing_section(
        self,
        content: str,
        section_marker: str
    ) -> str:
        """
        Remove existing knowledge section from content

        Args:
            content: Original content
            section_marker: Section marker (ex: "## 📚 CONHECIMENTO TÉCNICO")

        Returns:
            Content with section removed
        """
        # Find section start
        section_start = content.find(section_marker)

        if section_start == -1:
            return content

        # Find section end (next ## header or end of file)
        section_end = content.find("\n## ", section_start + len(section_marker))

        if section_end == -1:
            # Section goes until end of file
            return content[:section_start].rstrip() + "\n\n"

        # Remove section
        return (
            content[:section_start].rstrip() +
            "\n\n" +
            content[section_end:].lstrip()
        )

    def update_knowledge_version(
        self,
        agent_name: str,
        mapping: Dict,
        extracted_versiculos: List[Dict]
    ) -> None:
        """
        Update .knowledge_version file for agent

        Args:
            agent_name: Agent name (ex: "anuncio_agent")
            mapping: Mapping dict
            extracted_versiculos: List of extracted versículo dicts
        """
        agent_dir = self.base_dir.parent / agent_name
        version_file = agent_dir / ".knowledge_version"

        # Load existing or create new
        if version_file.exists():
            with open(version_file, "r", encoding="utf-8") as f:
                version_data = json.load(f)
        else:
            version_data = {
                "schema_version": self.knowledge_map.get("version", "1.0.0"),
                "knowledge_base_version": "2.0.0",
                "injections": []
            }

        # Add new injection record
        injection_record = {
            "mapping_id": mapping["id"],
            "prompt_file": mapping["prompt_file"],
            "timestamp": datetime.now().isoformat(),
            "versiculos": [
                v["ref"] for v in extracted_versiculos if not v.get("error")
            ],
            "num_versiculos": len([v for v in extracted_versiculos if not v.get("error")])
        }

        # Update or append
        existing_idx = next(
            (i for i, inj in enumerate(version_data["injections"])
             if inj["mapping_id"] == mapping["id"]),
            None
        )

        if existing_idx is not None:
            version_data["injections"][existing_idx] = injection_record
        else:
            version_data["injections"].append(injection_record)

        version_data["last_updated"] = datetime.now().isoformat()

        # Save (skip if dry-run)
        if not self.dry_run:
            with open(version_file, "w", encoding="utf-8") as f:
                json.dump(version_data, f, indent=2, ensure_ascii=False)

    def enrich_mapping(self, mapping: Dict) -> Dict:
        """
        Enrich single mapping

        Args:
            mapping: Mapping dict

        Returns:
            Dict with enrichment result
        """
        mapping_id = mapping["id"]
        agent_name = mapping["agent"]

        print(f"\n{'='*60}")
        print(f"Enriching: {mapping_id}")
        print(f"Agent: {agent_name}")
        print(f"Prompt: {mapping['prompt_file']}")
        print(f"{'='*60}\n")

        try:
            # Extract versículos
            print("📚 Extracting versículos...")
            extracted = self.extract_knowledge_for_mapping(mapping)

            success_count = len([v for v in extracted if not v.get("error")])
            error_count = len([v for v in extracted if v.get("error")])

            print(f"   ✅ Extracted: {success_count} versículos")
            if error_count > 0:
                print(f"   ⚠️  Errors: {error_count} versículos")

            # Inject knowledge
            print("\n💉 Injecting knowledge into prompt...")
            result = self.inject_knowledge(mapping, extracted)

            if result["success"]:
                print(f"   ✅ {result['message']}")
                if result.get("backup_path"):
                    print(f"   💾 Backup: {result['backup_path']}")

            # Update version tracking
            if not self.dry_run:
                print("\n📝 Updating version tracking...")
                self.update_knowledge_version(agent_name, mapping, extracted)
                print("   ✅ Version file updated")

            return {
                "success": True,
                "mapping_id": mapping_id,
                "extracted_count": success_count,
                "error_count": error_count,
                **result
            }

        except Exception as e:
            print(f"   ❌ ERROR: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()

            return {
                "success": False,
                "mapping_id": mapping_id,
                "error": str(e)
            }

    def enrich_agent(self, agent_name: str) -> List[Dict]:
        """
        Enrich all prompts for an agent

        Args:
            agent_name: Agent name (ex: "anuncio_agent")

        Returns:
            List of enrichment results
        """
        mappings = self.get_mappings_for_agent(agent_name)

        if not mappings:
            print(f"No mappings found for agent: {agent_name}", file=sys.stderr)
            return []

        print(f"\n🎯 Enriching agent: {agent_name}")
        print(f"   Found {len(mappings)} mapping(s)")

        results = []

        for mapping in mappings:
            result = self.enrich_mapping(mapping)
            results.append(result)

        return results


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Enrich agent prompts with knowledge from MENTOR"
    )
    parser.add_argument(
        "--agent",
        help="Agent name to enrich (ex: anuncio_agent)"
    )
    parser.add_argument(
        "--mapping",
        help="Specific mapping ID to enrich (ex: anuncio_titulo_generator_v1)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Don't modify files, just show what would happen"
    )
    parser.add_argument(
        "--knowledge-map",
        help="Path to knowledge_map.json (default: auto-detect)"
    )

    args = parser.parse_args()

    # Validate args
    if not args.agent and not args.mapping:
        parser.error("Must specify --agent or --mapping")

    try:
        # Fix Windows encoding
        if sys.platform == 'win32':
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

        # Create enricher
        enricher = AgentEnricher(
            knowledge_map_path=Path(args.knowledge_map) if args.knowledge_map else None,
            dry_run=args.dry_run
        )

        if args.dry_run:
            print("\n🔍 DRY-RUN MODE - No files will be modified\n")

        # Execute enrichment
        if args.mapping:
            # Enrich specific mapping
            mapping = enricher.get_mapping_by_id(args.mapping)
            if not mapping:
                print(f"ERROR: Mapping not found: {args.mapping}", file=sys.stderr)
                sys.exit(1)

            result = enricher.enrich_mapping(mapping)
            results = [result]

        else:
            # Enrich all mappings for agent
            results = enricher.enrich_agent(args.agent)

        # Summary
        print("\n" + "="*60)
        print("ENRICHMENT SUMMARY")
        print("="*60)

        success_count = len([r for r in results if r["success"]])
        error_count = len([r for r in results if not r["success"]])

        print(f"\n✅ Successful: {success_count}")
        print(f"❌ Failed: {error_count}")

        if error_count > 0:
            print("\nFailed mappings:")
            for r in results:
                if not r["success"]:
                    print(f"   - {r['mapping_id']}: {r.get('error', 'Unknown error')}")

        sys.exit(0 if error_count == 0 else 1)

    except Exception as e:
        print(f"FATAL ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)
