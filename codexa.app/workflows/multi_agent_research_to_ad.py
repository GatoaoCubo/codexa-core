#!/usr/bin/env python3
"""
Multi-Agent Workflow: Research → Ad Creation
============================================

Automated workflow that coordinates pesquisa_agent and anuncio_agent:
1. pesquisa_agent: Researches market/competitors
2. anuncio_agent: Creates optimized ads based on research

This demonstrates the power of centralized path orchestration.

Usage:
    # Run complete workflow
    python workflows/multi_agent_research_to_ad.py --product "Smart Watch XYZ"

    # Dry run (simulation only)
    python workflows/multi_agent_research_to_ad.py --product "Smart Watch XYZ" --dry-run

    # Specify marketplace
    python workflows/multi_agent_research_to_ad.py --product "Smart Watch XYZ" --marketplace mercadolivre

Version: 1.0.0
Created: 2025-11-16
Purpose: Demonstrate multi-agent coordination with centralized paths
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# === STEP 1: Import Global Orchestrator ===
# This is the KEY - one import gives us access to ALL agents!
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.paths import (
    get_agent_dir,
    get_agent_paths,
    get_agent_output,
    PATH_GLOBAL_OUTPUTS,
    AGENTS_ROOT,
)


class MultiAgentWorkflow:
    """Coordinates multiple agents in sequence."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run

        # === STEP 2: Get paths for ALL agents we need ===
        # No hardcoded paths! Everything comes from orchestrator
        self.pesquisa_paths = get_agent_paths('pesquisa')
        self.anuncio_paths = get_agent_paths('anuncio')

        # Create workflow output directory
        self.workflow_output = PATH_GLOBAL_OUTPUTS / "multi_agent_workflows"
        self.workflow_output.mkdir(parents=True, exist_ok=True)

        print(f"[OK] Workflow initialized")
        print(f"   Pesquisa Agent: {self.pesquisa_paths['root']}")
        print(f"   Anuncio Agent:  {self.anuncio_paths['root']}")
        print(f"   Workflow Output: {self.workflow_output}")
        print()

    def execute_research_phase(self, product_name: str, marketplace: str = "mercadolivre") -> Dict[str, Any]:
        """
        Phase 1: Execute research using pesquisa_agent.

        In a real implementation, this would:
        1. Call pesquisa_agent's research functions
        2. Save results to pesquisa_agent/outputs/
        3. Return structured research data
        """
        print("=" * 70)
        print("PHASE 1: RESEARCH (pesquisa_agent)")
        print("=" * 70)

        # === STEP 3: Access agent's output directory ===
        # The orchestrator knows where each agent stores outputs!
        research_output_dir = self.pesquisa_paths['outputs']
        research_file = research_output_dir / f"research_{product_name.replace(' ', '_')}.json"

        if self.dry_run:
            print(f">> [DRY RUN] Would execute research for: {product_name}")
            print(f"   Marketplace: {marketplace}")
            print(f"   Output would be saved to: {research_file}")

            # Simulate research data
            research_data = {
                "product": product_name,
                "marketplace": marketplace,
                "competitors": [
                    {"name": "Competitor A", "price": 299.90, "rating": 4.5},
                    {"name": "Competitor B", "price": 349.90, "rating": 4.7},
                    {"name": "Competitor C", "price": 279.90, "rating": 4.3},
                ],
                "market_insights": {
                    "avg_price": 309.90,
                    "top_keywords": ["smartwatch", "fitness", "bluetooth", "waterproof"],
                    "trending_features": ["heart rate monitor", "GPS", "sleep tracking"]
                },
                "timestamp": datetime.now().isoformat()
            }
        else:
            print(f">> Executing research for: {product_name}")
            print(f"   Marketplace: {marketplace}")

            # In real implementation, call pesquisa_agent here
            # Example:
            # from pesquisa_agent.research import execute_research
            # research_data = execute_research(product_name, marketplace)

            # For now, create mock data
            research_data = {
                "product": product_name,
                "marketplace": marketplace,
                "competitors": [],
                "market_insights": {},
                "timestamp": datetime.now().isoformat()
            }

            # Save research results
            research_output_dir.mkdir(exist_ok=True)
            with open(research_file, 'w', encoding='utf-8') as f:
                json.dump(research_data, f, indent=2, ensure_ascii=False)

            print(f"[OK] Research saved to: {research_file}")

        print()
        return research_data

    def execute_ad_creation_phase(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Phase 2: Create ads using anuncio_agent based on research.

        In a real implementation, this would:
        1. Load research data from pesquisa_agent
        2. Call anuncio_agent's ad creation functions
        3. Save ads to anuncio_agent/outputs/
        4. Return created ad data
        """
        print("=" * 70)
        print("PHASE 2: AD CREATION (anuncio_agent)")
        print("=" * 70)

        # === STEP 4: Cross-agent data access ===
        # Easy to read from one agent and write to another!
        anuncio_output_dir = self.anuncio_paths['outputs']
        ad_file = anuncio_output_dir / f"ad_{research_data['product'].replace(' ', '_')}.json"

        if self.dry_run:
            print(f">> [DRY RUN] Would create ad using research insights:")
            print(f"   Top Keywords: {research_data['market_insights'].get('top_keywords', [])}")
            print(f"   Avg Market Price: R$ {research_data['market_insights'].get('avg_price', 0)}")
            print(f"   Output would be saved to: {ad_file}")

            # Simulate ad data
            ad_data = {
                "product": research_data['product'],
                "title": f"{research_data['product']} - Fitness & Bluetooth - Waterproof",
                "description": "Smartwatch com monitor cardíaco, GPS integrado e resistente à água",
                "price_strategy": "competitive",
                "suggested_price": 289.90,
                "keywords": research_data['market_insights'].get('top_keywords', []),
                "bullet_points": [
                    "[OK] Monitor de frequência cardíaca 24/7",
                    "[OK] GPS integrado para tracking preciso",
                    "[OK] Resistente à água IP68",
                    "[OK] Bateria de até 7 dias",
                ],
                "created_from_research": True,
                "timestamp": datetime.now().isoformat()
            }
        else:
            print(f">> Creating ad for: {research_data['product']}")
            print(f"   Using research insights...")

            # In real implementation, call anuncio_agent here
            # Example:
            # from anuncio_agent.ad_creator import create_ad
            # ad_data = create_ad(research_data)

            # For now, create mock data
            ad_data = {
                "product": research_data['product'],
                "title": f"{research_data['product']} - Premium",
                "description": "Descrição otimizada baseada em pesquisa de mercado",
                "created_from_research": True,
                "timestamp": datetime.now().isoformat()
            }

            # Save ad results
            anuncio_output_dir.mkdir(exist_ok=True)
            with open(ad_file, 'w', encoding='utf-8') as f:
                json.dump(ad_data, f, indent=2, ensure_ascii=False)

            print(f"[OK] Ad saved to: {ad_file}")

        print()
        return ad_data

    def generate_workflow_report(self, research_data: Dict, ad_data: Dict) -> Path:
        """Generate consolidated workflow report."""
        print("=" * 70)
        print("PHASE 3: REPORT GENERATION")
        print("=" * 70)

        report = {
            "workflow": "Research → Ad Creation",
            "timestamp": datetime.now().isoformat(),
            "phases": {
                "1_research": {
                    "agent": "pesquisa_agent",
                    "product": research_data.get('product'),
                    "competitors_analyzed": len(research_data.get('competitors', [])),
                    "keywords_found": len(research_data.get('market_insights', {}).get('top_keywords', []))
                },
                "2_ad_creation": {
                    "agent": "anuncio_agent",
                    "title_created": ad_data.get('title'),
                    "price_suggested": ad_data.get('suggested_price'),
                }
            },
            "output_locations": {
                "research_output": str(self.pesquisa_paths['outputs']),
                "ad_output": str(self.anuncio_paths['outputs']),
                "workflow_report": str(self.workflow_output)
            }
        }

        # Save consolidated report
        report_file = self.workflow_output / f"workflow_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        if not self.dry_run:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"[OK] Workflow report saved to: {report_file}")
        else:
            print(f">> [DRY RUN] Report would be saved to: {report_file}")

        print()
        return report_file

    def execute(self, product_name: str, marketplace: str = "mercadolivre"):
        """Execute complete multi-agent workflow."""
        print("\n>> Starting Multi-Agent Workflow")
        print(f"   Product: {product_name}")
        print(f"   Marketplace: {marketplace}")
        print(f"   Mode: {'DRY RUN' if self.dry_run else 'LIVE'}")
        print()

        # Phase 1: Research
        research_data = self.execute_research_phase(product_name, marketplace)

        # Phase 2: Ad Creation
        ad_data = self.execute_ad_creation_phase(research_data)

        # Phase 3: Report
        report_file = self.generate_workflow_report(research_data, ad_data)

        print("=" * 70)
        print("[OK] WORKFLOW COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print()
        print("Summary:")
        print(f"  [OK] Research completed (pesquisa_agent)")
        print(f"  [OK] Ad created (anuncio_agent)")
        print(f"  [OK] Report generated")
        print()
        print("Next steps:")
        print(f"  1. Review research: {self.pesquisa_paths['outputs']}")
        print(f"  2. Review ad: {self.anuncio_paths['outputs']}")
        print(f"  3. Check workflow report: {report_file}")
        print()


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Multi-Agent Workflow: Research → Ad Creation'
    )
    parser.add_argument(
        '--product',
        type=str,
        required=True,
        help='Product name to research and create ad for'
    )
    parser.add_argument(
        '--marketplace',
        type=str,
        default='mercadolivre',
        choices=['mercadolivre', 'shopee', 'amazon', 'magazineluiza'],
        help='Target marketplace (default: mercadolivre)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate workflow without making changes'
    )

    args = parser.parse_args()

    # Execute workflow
    workflow = MultiAgentWorkflow(dry_run=args.dry_run)
    workflow.execute(args.product, args.marketplace)


if __name__ == "__main__":
    main()
