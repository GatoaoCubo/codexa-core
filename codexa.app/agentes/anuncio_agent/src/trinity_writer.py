"""
Trinity Output Writer for CodeXAnuncio.
KEYWORDS: codex|anuncio|trinity|output|llm-optimized|metadata

Implements the Trinity Output Pattern from AGENTIC_FRAMEWORK_INTEGRATION.md:
- Human-readable Markdown (.md)
- LLM-optimized JSON (.llm.json)
- Metadata JSON (.meta.json)
"""

import json
from datetime import datetime
from pathlib import Path

from models import AnuncioOutput, PersuasionScore, ValidationResult


class TrinityOutputWriter:
    """
    Generate three versions of every output following Trinity Pattern.
    Based on AGENTIC_FRAMEWORK_INTEGRATION.md Section 5.
    """

    def __init__(self, base_path: Path):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def write(self, anuncio: AnuncioOutput, validation: ValidationResult, persuasion_score: PersuasionScore, name: str):
        """
        Write human_readable, llm_optimized, and metadata versions.

        Args:
            anuncio: Generated ad output
            validation: Validation result
            persuasion_score: Persuasion score
            name: Base filename (without extension)
        """

        # 1. Human-readable Markdown
        human_path = self.base_path / f"{name}.md"
        with open(human_path, "w", encoding="utf-8") as f:
            f.write(self._to_markdown(anuncio, validation, persuasion_score))

        # 2. LLM-optimized JSON
        llm_path = self.base_path / f"{name}.llm.json"
        llm_data = {
            "version": "1.0.0",
            "content": anuncio.model_dump(),
            "prompt_hints": self._extract_prompt_hints(anuncio),
            "semantic_tags": self._extract_semantic_tags(anuncio),
            "token_count": self._estimate_tokens(anuncio),
            "quality_metrics": {
                "validation_status": validation.qa_status.value,
                "completeness_score": validation.completeness_score,
                "persuasion_score": persuasion_score.overall_score,
                "persuasion_level": persuasion_score.level.value,
            },
        }
        with open(llm_path, "w", encoding="utf-8") as f:
            json.dump(llm_data, f, ensure_ascii=False, indent=2)

        # 3. Metadata JSON
        meta_path = self.base_path / f"{name}.meta.json"
        metadata = {
            "created_at": datetime.now().isoformat(),
            "quality_score": persuasion_score.overall_score,
            "validation_status": validation.qa_status.value,
            "completeness": validation.completeness_score,
            "agent_version": "CodeXAnuncio v1.1",
            "marketplace_target": anuncio.marketplace_target.value,
            "confidence_score": validation.completeness_score,
            "gatilhos_mentais": persuasion_score.gatilhos_detectados,
            "frameworks": persuasion_score.frameworks_detectados,
            "compliance_issues": validation.compliance_issues,
            "warnings": validation.warnings,
        }
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)


    def _to_markdown(self, anuncio: AnuncioOutput, validation: ValidationResult, persuasion: PersuasionScore) -> str:
        """Convert anuncio to human-readable markdown."""

        md = f"""# {anuncio.identidade_produto.get('nome', 'Produto')}

**Generated**: {anuncio.gerado_em}
**Marketplace**: {anuncio.marketplace_target.value}
**Quality**: {validation.qa_status.value} ({validation.completeness_score:.0%})
**Persuasion**: {persuasion.level.value.upper()} ({persuasion.overall_score:.2f})

---

## Identidade do Produto

**Nome**: {anuncio.identidade_produto.get('nome', 'N/A')}
**Categoria**: {anuncio.identidade_produto.get('categoria', 'N/A')}
**Diferenciais**: {anuncio.identidade_produto.get('diferenciais', 'N/A')}

## Proposta de Valor

**Promessa**: {anuncio.proposta_valor.get('promessa', 'N/A')}
**Diferencial**: {anuncio.proposta_valor.get('diferencial', 'N/A')}

---

## Títulos (3 variações)

"""

        for i, titulo in enumerate(anuncio.titulos, 1):
            md += f"{i}. **{titulo.texto}** ({titulo.comprimento} chars)\n"

        md += f"""
---

## Bloco de Palavras 1 ({len(anuncio.bloco_palavras_1)} keywords)

{', '.join(anuncio.bloco_palavras_1[:20])}...

## Bloco de Palavras 2 ({len(anuncio.bloco_palavras_2)} keywords)

{', '.join(anuncio.bloco_palavras_2[:20])}...

---

## Descrição Longa ({len(anuncio.descricao_longa)} chars)

{anuncio.descricao_longa[:500]}...

---

## Prompts de Imagens (9 imagens)

"""

        for prompt in anuncio.prompts_imagens[:3]:
            md += f"{prompt.numero}. **{prompt.tipo}**: {prompt.prompt[:80]}...\n"

        md += f"""
(+ {len(anuncio.prompts_imagens) - 3} more image prompts)

## Prompt de Vídeo VEO3

**Formato**: {anuncio.prompt_video_veo3.formato}
**Duração**: {anuncio.prompt_video_veo3.duracao_total}s
**Estilo**: {anuncio.prompt_video_veo3.estilo_visual}
**Cenas**: {len(anuncio.prompt_video_veo3.cenas)}

---

## Metadados SEO

**Primary Keywords**: {', '.join(anuncio.metadados_seo.keywords_primary)}
**Secondary Keywords**: {', '.join(anuncio.metadados_seo.keywords_secondary[:5])}

**Competitors Analyzed**: {len(anuncio.metadados_seo.competitors_analysis)}

"""

        for comp in anuncio.metadados_seo.competitors_analysis[:2]:
            md += f"- **{comp.marca}**: {comp.oportunidade}\n"

        md += """
**Copy Decisions**:

"""

        for decision in anuncio.metadados_seo.copy_decisions:
            md += f"- {decision.decisao}: _{decision.rationale}_\n"

        md += """
---

## Variações S5 (3 tipos)

"""

        for var in anuncio.variacoes_s5:
            md += f"""
### {var.tipo.value.upper()}

**Título**: {var.titulo}
**Personagem**: {var.personagem}
**Problema**: {var.problema}
**Solução**: {var.solucao}
**Abertura**: {var.abertura[:100]}...

"""

        md += f"""
---

## Auditoria QA

**Status**: {anuncio.auditoria_qa.status.value}
**Completude**: {anuncio.auditoria_qa.completude_percent:.1f}%
**Checks Passed**: {len([c for c in anuncio.auditoria_qa.checks if c.status == 'OK'])}/{len(anuncio.auditoria_qa.checks)}

**Issues**: {len(anuncio.auditoria_qa.issues_encontrados)}
**Recommended Actions**: {len(anuncio.auditoria_qa.acoes_recomendadas)}

---

## Metadata Interno

**Persuasion Score**: {anuncio.metadata_interno.persuasion_score:.2f} ({anuncio.metadata_interno.persuasion_level.value})
**Gatilhos Mentais**: {', '.join(anuncio.metadata_interno.gatilhos_mentais)}
**Frameworks**: {', '.join(anuncio.metadata_interno.frameworks_aplicados)}
**Compliance**: {anuncio.metadata_interno.compliance_status}
**Generated By**: {anuncio.metadata_interno.gerado_por}
**Date**: {anuncio.metadata_interno.data_geracao}

---

## Persuasion Analysis

**Overall Score**: {persuasion.overall_score:.2f} ({persuasion.level.value})

**Component Scores**:
- Gatilhos Mentais: {persuasion.gatilhos_mentais_score:.2f}
- StoryBrand Structure: {persuasion.storybrand_structure_score:.2f}
- Benefícios Densidade: {persuasion.beneficios_densidade_score:.2f}
- Provas e Evidências: {persuasion.provas_evidencias_score:.2f}

**Detected Gatilhos**: {', '.join(persuasion.gatilhos_detectados)}

**Recommendations**:
"""

        for rec in persuasion.recomendacoes:
            md += f"- {rec}\n"

        md += """
---

**End of Document**
"""

        return md

    def _extract_prompt_hints(self, anuncio: AnuncioOutput) -> list[str]:
        """Extract prompt hints for LLM consumption."""
        return [
            "Focus on TITULOS for headline variations",
            "BLOCO_PALAVRAS_1 and _2 contain SEO-optimized keywords",
            "DESCRICAO_LONGA is structured with StoryBrand framework",
            "Confidence scores indicate data quality and reliability",
            "VARIACOES_S5 provide different copy angles: equilibrada, emocional, tecnica",
        ]

    def _extract_semantic_tags(self, anuncio: AnuncioOutput) -> list[str]:
        """Extract semantic tags for LLM indexing."""
        tags = [
            "ad_generation",
            "marketplace_copy",
            "persuasive_writing",
            anuncio.marketplace_target.value,
            anuncio.identidade_produto.get("categoria", "").lower().replace(" ", "_"),
        ]

        # Add framework tags
        tags.extend(anuncio.metadata_interno.frameworks_aplicados)

        # Add quality indicators
        tags.append(f"quality_{anuncio.metadata_interno.persuasion_level.value}")

        return [tag for tag in tags if tag]

    def _estimate_tokens(self, anuncio: AnuncioOutput) -> int:
        """Estimate token count using rough approximation."""
        content_str = json.dumps(anuncio.model_dump())
        # Rough estimate: 1 token ≈ 4 characters
        return len(content_str) // 4
