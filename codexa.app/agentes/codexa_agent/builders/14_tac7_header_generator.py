#!/usr/bin/env python3
"""
Add TAC-7 headers to remaining prompts in pesquisa_agent
"""

import sys
from pathlib import Path

# Import centralized path configuration
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.paths import PATH_PROMPTS

prompts_to_update = [
    {
        "file": "web_search_inbound.md",
        "id": "web_search_inbound_v1",
        "purpose": "Execute marketplace searches (BR platforms) to extract SEO patterns, competitors, pricing",
        "category": "data_collection",
        "execution_time": "8-10 min",
        "required_inputs": ["$query_list", "$validated_brief.marketplace_target"],
        "primary_outputs": ["SEO INBOUND", "PADRÕES DE LINGUAGEM", "CONSULTAS WEB"],
        "export_vars": {
            "competitors": "Competitor products found in marketplaces",
            "marketplace_patterns": "Title and messaging patterns"
        }
    },
    {
        "file": "web_search_outbound.md",
        "id": "web_search_outbound_v1",
        "purpose": "Execute SERP + social searches (Google, YouTube, TikTok, Reclame Aqui) for organic insights",
        "category": "data_collection",
        "execution_time": "8-10 min",
        "required_inputs": ["$query_list"],
        "primary_outputs": ["SEO OUTBOUND", "DORES DO PÚBLICO", "GANHOS DESEJADOS", "CONSULTAS WEB"],
        "export_vars": {
            "organic_keywords": "Content keywords from SERP",
            "pain_points_initial": "Initial pain points from reviews/social"
        }
    },
    {
        "file": "competitor_analysis.md",
        "id": "competitor_analysis_v1",
        "purpose": "Deep dive into top 3-5 competitors with quantitative benchmarking",
        "category": "competitive_intelligence",
        "execution_time": "6-8 min",
        "required_inputs": ["$competitors", "$validated_brief"],
        "primary_outputs": ["ANÁLISE DE CONCORRENTES", "BENCHMARK DE CONCORRENTES", "DIFERENCIAIS COMPETITIVOS"],
        "export_vars": {
            "competitor_list": "Detailed competitor profiles",
            "benchmark_data": "Aggregated metrics (price, rating, review count)"
        }
    },
    {
        "file": "seo_taxonomy.md",
        "id": "seo_taxonomy_v1",
        "purpose": "Consolidate and cluster keywords semantically for SEO strategy",
        "category": "seo_intelligence",
        "execution_time": "4-6 min",
        "required_inputs": ["$marketplace_patterns", "$organic_keywords"],
        "primary_outputs": ["SEO INBOUND", "SEO OUTBOUND"],
        "export_vars": {
            "seo_clusters": "Semantic keyword clusters",
            "negative_keywords": "Keywords to avoid"
        }
    },
    {
        "file": "image_analysis.md",
        "id": "image_analysis_v1",
        "purpose": "Analyze product images for visual trends, context, quality assessment",
        "category": "visual_intelligence",
        "execution_time": "3-5 min",
        "required_inputs": ["$validated_brief.image_urls"],
        "primary_outputs": ["IMAGENS ANALISADAS"],
        "export_vars": {
            "visual_insights": "Visual trends and quality assessment"
        }
    }
]

tac7_header_template = """
## 📋 MODULE_METADATA (TAC-7 Header)

```yaml
id: {id}
version: 1.0.0
purpose: "{purpose}"
category: {category}
dependencies:
  - config/accessible_urls.md (relevant sections)
  - web_search capability (required for most modules)
execution_time: {execution_time}
isolation: module
portability: llm_agnostic
```

## 📥 INPUT_CONTRACT

**Required Inputs**:
{required_inputs_formatted}

**Optional Inputs**: (see original content below)

## 📤 OUTPUT_CONTRACT

**Primary Outputs**: {primary_outputs_formatted}

**Export Variables**:
```yaml
{export_vars_formatted}
```

## 🎯 TASK

**Role**: {role}
**Objective**: {objective}
**Standards**: (see original content below)
**Constraints**: Max execution time: {execution_time}, All queries logged

## ✅ VALIDATION (Quality Gates)

(See original content for specific validation criteria)

## 🔗 CONTEXT (Usage & Integration)

**Upstream Dependencies**: Previous steps in execution plan
**Downstream Consumers**: Subsequent steps + output blocks
**Data Flow**: (see original content)

---

"""

def generate_tac7_header(prompt_config):
    # Format required inputs
    req_inputs = "\n".join([f"- `{inp}` - Input parameter" for inp in prompt_config["required_inputs"]])

    # Format primary outputs
    prim_outputs = ", ".join([f"`[{out}]`" for out in prompt_config["primary_outputs"]])

    # Format export vars
    export_vars = "\n".join([f"{key}: \"{value}\"" for key, value in prompt_config["export_vars"].items()])

    # Infer role from category
    role_map = {
        "data_collection": "Data Collection Specialist",
        "competitive_intelligence": "Competitive Intelligence Analyst",
        "seo_intelligence": "SEO Strategy Specialist",
        "visual_intelligence": "Visual Analysis Specialist"
    }
    role = role_map.get(prompt_config["category"], "Research Specialist")

    # Generate header
    header = tac7_header_template.format(
        id=prompt_config["id"],
        purpose=prompt_config["purpose"],
        category=prompt_config["category"],
        execution_time=prompt_config["execution_time"],
        required_inputs_formatted=req_inputs,
        primary_outputs_formatted=prim_outputs,
        export_vars_formatted=export_vars,
        role=role,
        objective=prompt_config["purpose"]
    )

    return header

def add_header_to_file(file_path, header):
    """Add TAC-7 header after first heading"""
    # Use centralized PATH_PROMPTS instead of relative path
    full_path = PATH_PROMPTS / file_path

    if not full_path.exists():
        print(f"[SKIP] File not found: {full_path}")
        return False

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if TAC-7 header already exists
    if "MODULE_METADATA (TAC-7 Header)" in content:
        print(f"[SKIP] TAC-7 header already exists: {file_path}")
        return False

    # Find first heading (should be module name)
    lines = content.split('\n')
    insert_index = None

    for i, line in enumerate(lines):
        if line.startswith('# ') and i == 0:
            # Insert after first heading
            insert_index = i + 1
            break

    if insert_index is None:
        print(f"[ERROR] Could not find insertion point: {file_path}")
        return False

    # Insert header
    lines.insert(insert_index, header)
    new_content = '\n'.join(lines)

    # Write back
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[OK] Added TAC-7 header to: {file_path}")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("Adding TAC-7 Headers to Pesquisa Agent Prompts")
    print("=" * 60)

    updated_count = 0

    for prompt_config in prompts_to_update:
        header = generate_tac7_header(prompt_config)
        if add_header_to_file(prompt_config["file"], header):
            updated_count += 1

    print("=" * 60)
    print(f"Summary: {updated_count}/{len(prompts_to_update)} files updated")
    print("=" * 60)
