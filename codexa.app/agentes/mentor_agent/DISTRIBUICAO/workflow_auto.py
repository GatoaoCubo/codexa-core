#!/usr/bin/env python3
"""
Automated Workflow - Workflow completo automatizado de conhecimento

Purpose: Detectar novos CAPITULOS → Sugerir mappings → Enriquecer agentes
Input: None (detecta mudanças automaticamente)
Output: Agentes enriquecidos + relatório

Usage:
    # Workflow completo automatizado
    python workflow_auto.py

    # Workflow para CAPITULO específico
    python workflow_auto.py --capitulo CAPITULO_marketplace_63

    # Modo interativo (pede confirmação antes de cada ação)
    python workflow_auto.py --interactive

Version: 1.0.0
Author: CODEXA Meta-Construction System
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Add config to path for centralized path management
sys.path.insert(0, str(Path(__file__).parent.parent / 'config'))
from paths import MENTOR_AGENT_ROOT, PATH_PROCESSADOS, PATH_DISTRIBUICAO

# Import other DISTRIBUICAO scripts
from auto_mapper import AutoMapper
from enrich_agents import AgentEnricher


class AutomatedWorkflow:
    """Workflow automatizado completo"""

    def __init__(self, interactive: bool = False, min_relevance: float = 0.30):
        """
        Initialize workflow

        Args:
            interactive: If True, ask for confirmation before actions
            min_relevance: Minimum relevance score for mappings (default 0.30)
        """
        self.interactive = interactive
        self.min_relevance = min_relevance
        self.base_dir = MENTOR_AGENT_ROOT
        self.processados_dir = PATH_PROCESSADOS
        self.knowledge_map_path = PATH_DISTRIBUICAO / "knowledge_map.json"

        # Load knowledge map
        with open(self.knowledge_map_path, "r", encoding="utf-8") as f:
            self.knowledge_map = json.load(f)

    def detect_new_capitulos(self) -> List[str]:
        """
        Detect new CAPITULOS that don't have mappings yet

        Returns:
            List of CAPITULO names (ex: ["CAPITULO_marketplace_63"])
        """
        print("\n🔍 Detecting new CAPITULOS...")

        # Get all CAPITULOS
        all_capitulos = [
            f.stem for f in self.processados_dir.glob("CAPITULO_*.md")
        ]

        # Get CAPITULOS already mapped
        mapped_refs = set()
        for mapping in self.knowledge_map["mappings"]:
            for versiculo in mapping.get("versiculos", []):
                ref = versiculo["ref"]
                capitulo_name = ref.split(":")[0]
                mapped_refs.add(capitulo_name)

        # Find unmapped
        new_capitulos = [c for c in all_capitulos if c not in mapped_refs]

        print(f"   📚 Total CAPITULOS: {len(all_capitulos)}")
        print(f"   ✅ Already mapped: {len(mapped_refs)}")
        print(f"   🆕 New (unmapped): {len(new_capitulos)}")

        if new_capitulos:
            print(f"\n   New CAPITULOS:")
            for c in new_capitulos[:10]:  # Show first 10
                print(f"      - {c}")
            if len(new_capitulos) > 10:
                print(f"      ... and {len(new_capitulos) - 10} more")

        return new_capitulos

    def run_auto_mapping(self, capitulo_name: str) -> Dict:
        """
        Run auto-mapper for a CAPITULO

        Args:
            capitulo_name: CAPITULO name

        Returns:
            Suggestions dict
        """
        print(f"\n🤖 Auto-mapping {capitulo_name}...")

        mapper = AutoMapper()
        suggestions = mapper.suggest_mappings(capitulo_name, min_relevance=self.min_relevance)

        return suggestions

    def apply_mappings(self, suggestions: Dict) -> int:
        """
        Apply mapping suggestions

        Args:
            suggestions: Suggestions from auto-mapper

        Returns:
            Number of mappings added
        """
        if self.interactive:
            print("\n📋 Review suggestions:")
            mapper = AutoMapper()
            print(mapper.format_suggestions(suggestions))

            response = input("\nApply these mappings? (y/n): ")
            if response.lower() != 'y':
                print("Skipped.")
                return 0

        mapper = AutoMapper()
        mapper.apply_suggestions(suggestions, auto_apply=True)

        # Count added
        count = sum(
            len(prompts) for prompts in suggestions.values()
            if prompts
        )

        return count

    def enrich_affected_agents(self, suggestions: Dict) -> Dict:
        """
        Enrich agents affected by new mappings

        Args:
            suggestions: Suggestions from auto-mapper

        Returns:
            Dict with enrichment results per agent
        """
        affected_agents = list(suggestions.keys())

        if not affected_agents:
            print("\n⚠️  No agents to enrich")
            return {}

        print(f"\n💉 Enriching {len(affected_agents)} agent(s)...")

        if self.interactive:
            print(f"   Agents: {', '.join(affected_agents)}")
            response = input("\nProceed with enrichment? (y/n): ")
            if response.lower() != 'y':
                print("Skipped.")
                return {}

        enricher = AgentEnricher(dry_run=False)
        results = {}

        for agent_name in affected_agents:
            print(f"\n🎯 Enriching {agent_name}...")
            agent_results = enricher.enrich_agent(agent_name)
            results[agent_name] = agent_results

        return results

    def generate_report(
        self,
        capitulos_processed: List[str],
        mappings_added: int,
        enrichment_results: Dict
    ) -> str:
        """
        Generate workflow report

        Args:
            capitulos_processed: List of CAPITULOS processed
            mappings_added: Number of mappings added
            enrichment_results: Enrichment results dict

        Returns:
            Report string
        """
        lines = []
        lines.append("\n" + "="*70)
        lines.append("📊 AUTOMATED WORKFLOW REPORT")
        lines.append("="*70)
        lines.append(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # CAPITULOS processed
        lines.append(f"\n📚 CAPITULOS Processed: {len(capitulos_processed)}")
        for c in capitulos_processed:
            lines.append(f"   - {c}")

        # Mappings added
        lines.append(f"\n🗺️  Mappings Added: {mappings_added}")

        # Enrichment results
        lines.append(f"\n💉 Agents Enriched: {len(enrichment_results)}")

        for agent_name, results in enrichment_results.items():
            success_count = len([r for r in results if r.get("success")])
            error_count = len([r for r in results if not r.get("success")])

            lines.append(f"\n   {agent_name}:")
            lines.append(f"      ✅ Success: {success_count}")
            lines.append(f"      ❌ Errors: {error_count}")

            if error_count > 0:
                for r in results:
                    if not r.get("success"):
                        lines.append(f"         - {r.get('mapping_id')}: {r.get('error')}")

        # Summary
        lines.append("\n" + "="*70)
        total_success = sum(
            len([r for r in results if r.get("success")])
            for results in enrichment_results.values()
        )

        if total_success > 0:
            lines.append("✅ WORKFLOW COMPLETED SUCCESSFULLY")
        else:
            lines.append("⚠️  WORKFLOW COMPLETED WITH ERRORS")

        lines.append("="*70 + "\n")

        return "\n".join(lines)

    def run(self, capitulo_name: str = None):
        """
        Run complete automated workflow

        Args:
            capitulo_name: Optional specific CAPITULO to process
                          If None, processes all new CAPITULOS
        """
        print("\n🚀 Starting Automated Workflow...")
        print("="*70)

        # Step 1: Detect new CAPITULOS
        if capitulo_name:
            capitulos_to_process = [capitulo_name]
            print(f"\n📌 Processing specific CAPITULO: {capitulo_name}")
        else:
            capitulos_to_process = self.detect_new_capitulos()

            if not capitulos_to_process:
                print("\n✅ No new CAPITULOS to process. System is up to date!")
                return

        # Step 2: Auto-map each CAPITULO
        all_suggestions = {}

        for capitulo in capitulos_to_process:
            try:
                suggestions = self.run_auto_mapping(capitulo)

                # Merge suggestions
                for agent, prompts in suggestions.items():
                    if agent not in all_suggestions:
                        all_suggestions[agent] = {}
                    for prompt, candidates in prompts.items():
                        if prompt not in all_suggestions[agent]:
                            all_suggestions[agent][prompt] = []
                        all_suggestions[agent][prompt].extend(candidates)

            except Exception as e:
                print(f"⚠️  Error processing {capitulo}: {e}")
                continue

        if not all_suggestions:
            print("\n⚠️  No relevant mappings found")
            return

        # Step 3: Apply mappings
        mappings_added = self.apply_mappings(all_suggestions)

        if mappings_added == 0:
            print("\n⚠️  No mappings were added (may already exist)")
            return

        # Step 4: Enrich agents
        enrichment_results = self.enrich_affected_agents(all_suggestions)

        # Step 5: Generate report
        report = self.generate_report(
            capitulos_to_process,
            mappings_added,
            enrichment_results
        )

        print(report)

        # Save report
        report_file = PATH_DISTRIBUICAO / f"workflow_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"💾 Report saved: {report_file}")


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Run automated knowledge distribution workflow"
    )
    parser.add_argument(
        "--capitulo",
        help="Process specific CAPITULO (ex: CAPITULO_marketplace_63)"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive mode (ask for confirmation before actions)"
    )
    parser.add_argument(
        "--min-relevance",
        type=float,
        default=0.30,
        help="Minimum relevance score for mappings (default: 0.30)"
    )

    args = parser.parse_args()

    try:
        # Fix Windows encoding
        if sys.platform == 'win32':
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

        # Run workflow
        workflow = AutomatedWorkflow(
            interactive=args.interactive,
            min_relevance=args.min_relevance
        )
        workflow.run(capitulo_name=args.capitulo)

        sys.exit(0)

    except KeyboardInterrupt:
        print("\n\n⚠️  Workflow interrupted by user")
        sys.exit(1)

    except Exception as e:
        print(f"\nFATAL ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)
