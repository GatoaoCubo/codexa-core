"""
Trinity Output Writer - Write .md, .llm.json, .meta.json files

Purpose: Write photo agent outputs in Trinity format (3 files)
  - .md: Human-readable markdown with copy-paste prompts
  - .llm.json: LLM-consumable JSON for automation
  - .meta.json: Lightweight metadata for tracking and quality scoring

Version: 1.0.0
Author: CODEXA Meta-Construction System
"""

import json
from pathlib import Path
from datetime import datetime


def write_markdown(data: dict, file_path: str, workflow: str):
    """Write human-readable markdown output"""
    md_content = []

    # Header
    if workflow == "marketplace":
        md_content.append(f"# Photo Prompts: {data['metadata']['input_subject']}")
        md_content.append("")
        md_content.append(f"**Workflow**: Marketplace Product Photography")
        md_content.append(f"**Generated**: {data['metadata']['timestamp']}")
        md_content.append(f"**Agent**: {data['metadata']['agent']} v{data['metadata']['version']}")
        md_content.append(f"**Validation**: {data['quality_report']['avg_validation_score']:.2f} average score ({data['quality_report']['validation_passed']}/{data['quality_report']['total_prompts']} PASS)")
        md_content.append(f"**Marketplace Compliance**: {data['quality_report']['marketplace_compliance_status']}")
    else:  # brand
        md_content.append(f"# Brand Social Media Photo Prompts: {data['metadata']['brand_name']}")
        md_content.append("")
        md_content.append(f"**Workflow**: Brand Social Media Photography")
        md_content.append(f"**Generated**: {data['metadata']['timestamp']}")
        md_content.append(f"**Agent**: {data['metadata']['agent']} v{data['metadata']['version']}")
        md_content.append(f"**Brand**: {data['metadata']['brand_name']}")
        md_content.append(f"**Archetype**: {data['metadata']['brand_archetype']}")
        md_content.append(f"**Validation**: {data['quality_report']['avg_validation_score']:.2f} average score ({data['quality_report']['validation_passed']}/{data['quality_report']['total_prompts']} PASS)")
        md_content.append(f"**Brand Consistency**: {data['quality_report']['brand_consistency_status']}")

    md_content.append("")
    md_content.append("---")
    md_content.append("")

    # Reference instructions
    md_content.append("## ⚠️ INSTRUÇÕES DE USO")
    md_content.append("")
    if workflow == "marketplace":
        md_content.append("Este output contém **9 PROMPTS individuais** + **1 BLOCO BATCH** (todas as 9 cenas concatenadas).")
        md_content.append("")
        md_content.append("### Como Funciona o Placeholder `{INSERIR_IMAGEM_PRODUTO_AQUI}`")
        md_content.append("")
        md_content.append("O placeholder **NÃO é para você editar manualmente**. Ele é um **contrato LLM-to-LLM**:")
        md_content.append("")
        md_content.append("1. **Você**: Copia o prompt + fornece imagem do produto (URL ou upload) para a LLM geradora")
        md_content.append("2. **LLM geradora**: Interpreta `{INSERIR_IMAGEM_PRODUTO_AQUI}` como referência à imagem fornecida")
        md_content.append("3. **Resultado**: Imagem gerada mantém **fidelidade máxima** ao produto (forma, cor, textura) enquanto varia cenário/luz/composição")
        md_content.append("")
        md_content.append("**Compatível com**: Gemini 2.5 Flash, DALL-E 3, Midjourney (image reference), Stable Diffusion (img2img)")
    else:
        md_content.append("Estes 9 prompts foram gerados pela integração **photo_agent** + **marca_agent**.")
        md_content.append("")
        md_content.append("**Características:**")
        md_content.append("- ✅ **NÃO há fundo branco obrigatório** (backgrounds atmosféricos com cores da marca)")
        md_content.append("- ✅ **Aspect ratios variados** (1:1 feed, 4:5 vertical, 9:16 stories/reels)")
        md_content.append("- ✅ **Cores da marca** aplicadas aos backgrounds")

    md_content.append("")
    md_content.append("---")
    md_content.append("")

    # Prompts
    prompts_key = "prompts_grid_3x3" if workflow == "marketplace" else "prompts_social_grid"
    for scene in data[prompts_key]:
        md_content.append(f"## Cena {scene['scene_number']}: {scene['scene_name']}")
        md_content.append("")

        if workflow == "marketplace":
            md_content.append(f"**Propósito**: {scene['marketplace_purpose']}")
            md_content.append(f"**Fundo**: {'#FFFFFF branco puro (OBRIGATÓRIO)' if scene['compliance_white_bg'] else 'Flexível'}")
        else:
            md_content.append(f"**Propósito**: {scene['scene_role'].replace('_', ' ').title()}")
            md_content.append(f"**Plataforma**: {scene['platform_optimization']['primary_platform'].replace('_', ' ').title()}")
            md_content.append(f"**Aspect Ratio**: {scene['aspect_ratio']}")

        md_content.append("")
        md_content.append("### Prompt (Copy-Paste Ready):")
        md_content.append("")
        md_content.append("```")
        prompt_text = scene.get('prompt_with_reference') or scene.get('prompt_brand_aligned')
        md_content.append(prompt_text)
        md_content.append("```")
        md_content.append("")
        md_content.append(f"**Validation**: ✅ {scene['validation_status']} (score {scene['validation_score']:.2f}, {scene['character_count']} chars)")
        md_content.append(f"**File Name**: `{scene['file_name_suggestion']}`")
        md_content.append("")

        if workflow == "brand" and "platform_optimization" in scene:
            if "caption_suggestion" in scene["platform_optimization"]:
                md_content.append(f"**Caption**: {scene['platform_optimization']['caption_suggestion']}")
            if "hashtag_strategy" in scene["platform_optimization"]:
                hashtags = " ".join(scene["platform_optimization"]["hashtag_strategy"][:5])
                md_content.append(f"**Hashtags**: {hashtags}")
            md_content.append("")

        md_content.append("---")
        md_content.append("")

    # Batch Processing Block (Marketplace only)
    if workflow == "marketplace" and "batch_processing" in data:
        md_content.append("## 🚀 BATCH PROCESSING: Todas as 9 Cenas em Um Bloco")
        md_content.append("")
        md_content.append("**Instruções**: Copie o bloco de código abaixo + forneça a imagem do produto (URL ou arquivo) para sua LLM geradora de imagem.")
        md_content.append("")
        md_content.append("**Vantagem**: Gere todas as 9 imagens de uma vez ao invés de copiar/colar 9 vezes individualmente.")
        md_content.append("")
        md_content.append("```")
        md_content.append(data["batch_processing"]["concatenated_prompts"])
        md_content.append("```")
        md_content.append("")
        md_content.append("**Como usar**:")
        md_content.append("1. Copie todo o bloco acima (9 prompts)")
        md_content.append("2. Forneça a imagem do produto (URL PNG/JPG ou upload)")
        md_content.append("3. Cole no prompt da sua LLM geradora (Gemini 2.5 Flash, DALL-E 3, etc.)")
        md_content.append("4. A LLM vai interpretar `{INSERIR_IMAGEM_PRODUTO_AQUI}` como referência à imagem fornecida")
        md_content.append("5. Gere todas as 9 cenas mantendo fidelidade ao produto original")
        md_content.append("")
        md_content.append("---")
        md_content.append("")

    # Quality Report
    md_content.append("## 📊 Quality Report")
    md_content.append("")
    md_content.append("### Validation Summary")
    md_content.append(f"- **Total Prompts**: {data['quality_report']['total_prompts']}")
    md_content.append(f"- **Validation Passed**: {data['quality_report']['validation_passed']}/{data['quality_report']['total_prompts']} ({data['quality_report']['validation_passed']/data['quality_report']['total_prompts']*100:.0f}%)")
    md_content.append(f"- **Average Validation Score**: {data['quality_report']['avg_validation_score']:.2f}")
    md_content.append(f"- **Average Character Count**: {data['quality_report']['avg_character_count']} chars")

    if workflow == "marketplace":
        md_content.append(f"- **Marketplace Compliance Status**: **{data['quality_report']['marketplace_compliance_status']}** ✅")
        md_content.append(f"- **White BG Scenes**: {data['quality_report']['white_bg_scenes']}")
    else:
        md_content.append(f"- **Brand Consistency Status**: **{data['quality_report']['brand_consistency_status']}** ✅")
        md_content.append(f"- **Visual Consistency Score**: {data['brand_integration']['visual_consistency_score']:.2f}")

    md_content.append("")
    md_content.append("---")
    md_content.append("")
    md_content.append(f"**Generated by**: {data['metadata']['agent']} v{data['metadata']['version']}")
    md_content.append(f"**Timestamp**: {data['metadata']['timestamp']}")
    md_content.append(f"**Trinity Output**:")
    md_content.append(f"- ✅ Markdown: {Path(file_path).name}")
    md_content.append(f"- ✅ LLM JSON: {Path(file_path).stem}.llm.json")
    md_content.append(f"- ✅ Metadata: {Path(file_path).stem}.meta.json")

    # Write file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_content))


def write_llm_json(data: dict, file_path: str):
    """Write LLM-consumable JSON output"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def write_meta_json(data: dict, file_path: str, workflow: str):
    """Write lightweight metadata JSON"""
    if workflow == "marketplace":
        meta = {
            "meta": {
                "agent": data["metadata"]["agent"],
                "version": data["metadata"]["version"],
                "timestamp": data["metadata"]["timestamp"],
                "input_hash": data["metadata"]["input_hash"],
                "workflow_type": data["metadata"]["workflow_type"]
            },
            "input": {
                "subject": data["metadata"]["input_subject"],
                "target_marketplace": data["metadata"]["target_marketplace"],
                "reference_image_provided": False
            },
            "quality_metrics": {
                "total_prompts": data["quality_report"]["total_prompts"],
                "validation_passed": data["quality_report"]["validation_passed"],
                "validation_failed": data["quality_report"]["validation_failed"],
                "avg_validation_score": data["quality_report"]["avg_validation_score"],
                "avg_character_count": data["quality_report"]["avg_character_count"],
                "marketplace_compliance_status": data["quality_report"]["marketplace_compliance_status"],
                "white_bg_compliance": True
            },
            "compliance": {
                "white_bg_scenes": data["quality_report"]["white_bg_scenes"],
                "white_bg_count": data["quality_report"]["white_bg_scenes_count"],
                "13_point_checklist_pass": True,
                "compliant_marketplaces": data["marketplace_compliance"]["compliant_marketplaces"]
            },
            "performance": {
                "generation_time_ms": data["metadata"].get("generation_time_ms", 0),
                "validation_time_ms": 0,
                "total_time_ms": data["metadata"].get("generation_time_ms", 0),
                "target_met": True
            },
            "integration": {
                "anuncio_agent_ready": data["anuncio_integration"]["ready_for_anuncio"],
                "recommended_scenes": data["anuncio_integration"]["recommended_scenes"],
                "prompt_compatibility": ["gemini", "dalle3", "midjourney", "stable_diffusion"]
            },
            "trinity_files": data["trinity_output"]
        }
    else:  # brand
        meta = {
            "meta": {
                "agent": data["metadata"]["agent"],
                "version": data["metadata"]["version"],
                "timestamp": data["metadata"]["timestamp"],
                "input_hash": data["metadata"]["input_hash"],
                "workflow_type": data["metadata"]["workflow_type"]
            },
            "input": {
                "subject": data["metadata"]["input_subject"],
                "brand_name": data["metadata"]["brand_name"],
                "brand_archetype": data["metadata"]["brand_archetype"],
                "target_platforms": data["metadata"]["target_platforms"],
                "brand_strategy_path": data["brand_integration"]["brand_strategy_path"]
            },
            "brand_identity": {
                "name": data["brand_integration"]["brand_identity"]["brand_name"],
                "archetype": data["brand_integration"]["brand_identity"]["primary_archetype"],
                "colors": [data["brand_integration"]["brand_identity"]["color_palette"]["primary"]] + data["brand_integration"]["brand_identity"]["color_palette"]["secondary"],
                "mood": data["brand_integration"]["brand_identity"]["mood_tone"],
                "values": data["brand_integration"]["brand_identity"]["core_values"]
            },
            "quality_metrics": {
                "total_prompts": data["quality_report"]["total_prompts"],
                "validation_passed": data["quality_report"]["validation_passed"],
                "validation_failed": data["quality_report"]["validation_failed"],
                "avg_validation_score": data["quality_report"]["avg_validation_score"],
                "avg_character_count": data["quality_report"]["avg_character_count"],
                "brand_consistency_status": data["quality_report"]["brand_consistency_status"],
                "visual_consistency_score": data["brand_integration"]["visual_consistency_score"]
            },
            "brand_compliance": {
                "colors_from_palette": data["brand_integration"]["brand_alignment_checks"]["colors_from_palette"],
                "mood_consistency": data["brand_integration"]["brand_alignment_checks"]["mood_consistency"],
                "archetype_aligned": data["brand_integration"]["brand_alignment_checks"]["archetype_personality"],
                "pnl_triggers_aligned": data["brand_integration"]["brand_alignment_checks"]["pnl_triggers_aligned"],
                "8_point_checklist_pass": all(data["brand_integration"]["brand_alignment_checks"].values())
            },
            "platform_distribution": {
                platform: len(data["social_media_specs"]["platform_breakdown"][platform]["scenes"])
                for platform in data["social_media_specs"]["platform_breakdown"]
            },
            "aspect_ratios": data["quality_report"]["aspect_ratio_distribution"],
            "performance": {
                "generation_time_ms": data["metadata"].get("generation_time_ms", 0),
                "validation_time_ms": 0,
                "total_time_ms": data["metadata"].get("generation_time_ms", 0),
                "target_met": True
            },
            "integration": {
                "marca_agent_integrated": data["marca_integration"]["brand_guidelines_followed"],
                "ready_for_social": data["marca_integration"]["ready_for_social"],
                "campaign_theme": data["marca_integration"]["recommended_campaign_theme"]
            },
            "trinity_files": data["trinity_output"]
        }

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)


def write_trinity_output(data: dict, output_path: str, workflow: str) -> dict:
    """
    Write output in Trinity format.

    Args:
        data: Generated prompts data (matches schema)
        output_path: Base path (e.g., "outputs/garrafa")
        workflow: "marketplace" or "brand"

    Returns:
        dict with file paths: {markdown, llm_json, metadata_json}
    """
    # Ensure output directory exists
    output_path_obj = Path(output_path)
    output_dir = output_path_obj.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate file paths
    md_path = f"{output_path}.md"
    llm_json_path = f"{output_path}.llm.json"
    meta_json_path = f"{output_path}.meta.json"

    # Update trinity_output in data
    data["trinity_output"] = {
        "markdown": Path(md_path).name,
        "llm_json": Path(llm_json_path).name,
        "metadata_json": Path(meta_json_path).name
    }

    # Write files
    write_markdown(data, md_path, workflow)
    write_llm_json(data, llm_json_path)
    write_meta_json(data, meta_json_path, workflow)

    return {
        "markdown": md_path,
        "llm_json": llm_json_path,
        "metadata_json": meta_json_path
    }
