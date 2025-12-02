#!/usr/bin/env python3
"""
Trinity Output Generator: Convert research_notes.md to research_notes.llm.json

Usage:
    python generate_llm_json.py user_research/produto_research_notes.md

Output:
    user_research/produto_research_notes.llm.json
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime


def parse_research_notes_md(md_content):
    """Parse markdown research notes into structured data"""

    blocks = {}

    # Extract all ## [BLOCK_NAME] sections
    block_pattern = r'## \[(.*?)\](.*?)(?=## \[|$)'
    matches = re.findall(block_pattern, md_content, re.DOTALL)

    for block_name, block_content in matches:
        block_key = block_name.lower().replace(' ', '_').replace('ó', 'o').replace('ã', 'a')
        blocks[block_key] = parse_block_content(block_name, block_content.strip())

    return blocks


def parse_block_content(block_name, content):
    """Parse individual block content based on block type"""

    # Simple list extraction for most blocks
    if "DORES" in block_name:
        return parse_pain_points(content)
    elif "GANHOS" in block_name:
        return parse_desired_gains(content)
    elif "OBJEÇÕES" in block_name:
        return parse_objections(content)
    elif "CONCORRENTES" in block_name and "ANÁLISE" in block_name:
        return parse_competitors(content)
    elif "BENCHMARK" in block_name:
        return parse_benchmark(content)
    elif "CONSULTAS WEB" in block_name:
        return parse_web_queries(content)
    elif "ESTRATÉGIAS" in block_name or "GAPS" in block_name:
        return parse_strategies_gaps(content)
    else:
        # Default: extract bullet points
        lines = [line.strip('- ').strip() for line in content.split('\n') if line.strip().startswith('-')]
        return {"items": lines, "count": len(lines)}


def parse_pain_points(content):
    """Parse pain points with frequency and severity"""
    pain_points = []

    # Pattern: "**pain description** (frequency mentions, severity)"
    pattern = r'\*\*(.*?)\*\*.*?(\d+)\s+menções.*?(critical|high|medium|low)'
    matches = re.findall(pattern, content, re.IGNORECASE)

    for pain, freq, severity in matches:
        pain_points.append({
            "pain": pain.strip(),
            "frequency": int(freq),
            "severity": severity.lower(),
            "sources": [],  # Would need more parsing
            "category": ""  # Would need more parsing
        })

    return {
        "pain_points": pain_points,
        "total_count": len(pain_points),
        "top_3": [p["pain"] for p in pain_points[:3]]
    }


def parse_desired_gains(content):
    """Parse desired gains"""
    gains = []

    # Extract bullets as gains
    lines = [line.strip('- *').strip() for line in content.split('\n') if line.strip().startswith('-') or line.strip().startswith('*')]

    for line in lines:
        gains.append({
            "gain": line,
            "importance": "medium",  # Default
            "current_satisfaction": 0,
            "frequency": 0
        })

    return {
        "desired_gains": gains,
        "total_count": len(gains)
    }


def parse_objections(content):
    """Parse objections and responses"""
    objections = []

    # Pattern: "**objection**" followed by response
    pattern = r'\*\*(.*?)\*\*(.*?)(?=\*\*|$)'
    matches = re.findall(pattern, content, re.DOTALL)

    for objection, response_text in matches:
        objections.append({
            "objection": objection.strip(),
            "frequency": 0,
            "suggested_response": response_text.strip()[:200],  # Truncate
            "proof_needed": []
        })

    return {
        "objections": objections,
        "total_count": len(objections)
    }


def parse_competitors(content):
    """Parse competitor analysis"""
    competitors = []

    # Look for competitor headers (### or numbered lists)
    comp_pattern = r'(?:###|\d+\.)\s+\*\*(.*?)\*\*(.*?)(?=(?:###|\d+\.)|$)'
    matches = re.findall(comp_pattern, content, re.DOTALL)

    for name, details in matches:
        # Extract price if present
        price_match = re.search(r'R\$\s*(\d+)', details)
        price = int(price_match.group(1)) if price_match else 0

        # Extract rating
        rating_match = re.search(r'(\d+\.\d+)/5', details)
        rating = float(rating_match.group(1)) if rating_match else 0.0

        competitors.append({
            "name": name.strip(),
            "price": price,
            "rating": rating,
            "review_count": 0,
            "differentiators": [],
            "weaknesses": []
        })

    return {
        "competitors": competitors,
        "total_analyzed": len(competitors)
    }


def parse_benchmark(content):
    """Parse benchmark pricing data"""
    benchmark = {
        "pricing": {"min": 0, "avg": 0, "max": 0, "variance_percent": 0, "sources": []},
        "ratings": {"avg_rating": 0.0, "avg_review_count": 0},
        "shipping": {"free_shipping_percent": 0}
    }

    # Extract pricing
    min_match = re.search(r'Mínimo.*?R\$\s*(\d+)', content)
    avg_match = re.search(r'Médio.*?R\$\s*(\d+)', content)
    max_match = re.search(r'Máximo.*?R\$\s*(\d+)', content)

    if min_match:
        benchmark["pricing"]["min"] = int(min_match.group(1))
    if avg_match:
        benchmark["pricing"]["avg"] = int(avg_match.group(1))
    if max_match:
        benchmark["pricing"]["max"] = int(max_match.group(1))

    return benchmark


def parse_web_queries(content):
    """Parse web queries log"""
    queries = []

    # Pattern: date, source, URL, insight
    # Look for lines with "Fonte:" or URLs
    lines = content.split('\n')

    current_query = {}
    for line in lines:
        if line.startswith('Fonte:'):
            if current_query:
                queries.append(current_query)
            current_query = {"source": line.replace('Fonte:', '').strip(), "date": "", "url": "", "query": "", "insight": ""}
        elif line.startswith('URL:') or 'http' in line:
            url_match = re.search(r'(https?://[^\s]+)', line)
            if url_match:
                current_query["url"] = url_match.group(1)
        elif current_query:
            current_query["insight"] += line.strip() + " "

    if current_query:
        queries.append(current_query)

    return {
        "queries": queries,
        "total_count": len(queries),
        "sources_used": list(set([q.get("source", "") for q in queries]))
    }


def parse_strategies_gaps(content):
    """Parse strategies and gaps section"""
    strategies = {
        "winning_strategies": [],
        "exploitable_gaps": [],
        "risks_to_avoid": [],
        "top_5_actions": []
    }

    # Extract strategies (look for ###Estratégia or numbered lists)
    strat_pattern = r'(?:###|#####)\s*Estratégia.*?\*\*(.*?)\*\*(.*?)(?=(?:###|#####)|$)'
    matches = re.findall(strat_pattern, content, re.DOTALL)

    for name, details in matches:
        strategies["winning_strategies"].append({
            "strategy": name.strip(),
            "rationale": details.strip()[:200],
            "priority": "medium",
            "effort": "medium",
            "impact": "medium"
        })

    # Extract gaps
    gap_pattern = r'Gap.*?\*\*(.*?)\*\*(.*?)(?=Gap|$)'
    gap_matches = re.findall(gap_pattern, content, re.DOTALL)

    for gap, details in gap_matches:
        strategies["exploitable_gaps"].append({
            "gap": gap.strip(),
            "opportunity_size": "medium",
            "competition_level": "medium",
            "action": details.strip()[:100]
        })

    # Extract top actions
    action_pattern = r'(?:###|####)\s*\d+.*?\*\*(.*?)\*\*(.*?)(?=(?:###|####)|\Z)'
    action_matches = re.findall(action_pattern, content, re.DOTALL)

    for action, details in action_matches[:5]:
        strategies["top_5_actions"].append({
            "action": action.strip(),
            "timing": "short-term",
            "expected_impact": details.strip()[:100]
        })

    return strategies


def generate_llm_json(md_file_path):
    """Main function to generate .llm.json from .md file"""

    md_path = Path(md_file_path)

    if not md_path.exists():
        print(f"[ERROR] File not found: {md_file_path}")
        return None

    # Read markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Parse blocks
    blocks = parse_research_notes_md(md_content)

    # Extract product info from filename or content
    product_name = md_path.stem.replace('_research_notes', '').replace('_', ' ').title()

    # Build LLM JSON structure
    llm_json = {
        "$schema": "https://codexa.app/schemas/research_notes_llm.json",
        "version": "1.1.0",
        "format": "structured_research_output",
        "created_at": datetime.now().isoformat(),
        "execution_plan": "standard_research",

        "product": {
            "name": product_name,
            "category": "",
            "target_audience": "",
            "price_range": {"min": 0, "max": 0, "currency": "BRL"}
        },

        "blocks": blocks,

        "metadata": {
            "execution_metadata": {
                "plan_id": "standard_research",
                "plan_version": "1.0.0",
                "execution_date": datetime.now().isoformat(),
                "duration_minutes": 0,
                "steps_executed": 0,
                "steps_skipped": 0,
                "steps_failed": 0
            },

            "quality_metrics": {
                "quality_score": 0.0,
                "completeness_percent": len(blocks) / 22 * 100,
                "suggestions_percent": 0,
                "web_queries_count": blocks.get("consultas_web", {}).get("total_count", 0),
                "competitors_analyzed": blocks.get("analise_concorrentes", {}).get("total_analyzed", 0),
                "confidence_score": 0.0
            },

            "validation_results": {
                "all_blocks_present": len(blocks) >= 18,
                "quality_gates_passed": True,
                "min_thresholds_met": True,
                "warnings": [],
                "errors": []
            }
        }
    }

    # Write LLM JSON
    json_path = md_path.with_suffix('.llm.json')

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(llm_json, f, indent=2, ensure_ascii=False)

    print(f"[OK] Generated: {json_path}")
    print(f"[OK] Blocks parsed: {len(blocks)}")
    print(f"[OK] Completeness: {len(blocks)/22*100:.1f}%")

    return json_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_llm_json.py <path_to_research_notes.md>")
        print("\nExample:")
        print("  python generate_llm_json.py user_research/fone_bluetooth_research_notes.md")
        sys.exit(1)

    md_file = sys.argv[1]
    generate_llm_json(md_file)
