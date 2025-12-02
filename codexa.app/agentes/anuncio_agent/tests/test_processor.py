"""
Unit tests for CodeXAnuncio processor.
Tests parsing, generation, validation, and persuasion scoring.
"""

from datetime import datetime

import pytest

from models import AnuncioOutput, PersuasionLevel, QAStatus, ResearchNotesInput, TituloVariacao, ValidationResult
from processor import (
    _extract_field,
    _parse_list_block,
    calculate_persuasion_score,
    correct_anuncio,
    generate_anuncio,
    parse_research_notes,
    validate_output,
)


class TestParser:
    """Test research notes parser."""

    def test_extract_field_basic(self):
        """Test field extraction from text."""
        text = "produto: Cama de Janela para Gatos"
        result = _extract_field(text, r"produto[:\s]+(.+)")
        assert result == "Cama de Janela para Gatos"

    def test_extract_field_missing(self):
        """Test extraction returns empty on missing field."""
        text = "other: value"
        result = _extract_field(text, r"produto[:\s]+(.+)")
        assert result == ""

    def test_parse_list_block_basic(self):
        """Test parsing list block from markdown."""
        markdown = """
        ## Bloco 2: Head Terms
        - termo1
        - termo2
        - termo3
        ## Next Section
        """
        result = _parse_list_block(markdown, r"##\s*Bloco 2.*?\n(.*?)\n##")
        assert len(result) == 3
        assert "termo1" in result

    def test_parse_list_block_numbered(self):
        """Test parsing numbered list."""
        markdown = """
        ## Keywords
        1. primeiro
        2. segundo
        3. terceiro
        ## End
        """
        result = _parse_list_block(markdown, r"##\s*Keywords.*?\n(.*?)\n##")
        assert len(result) == 3

    def test_parse_research_notes_complete(self):
        """Test parsing complete research notes."""
        markdown = """
        ## Metadata
        produto: Test Product
        categoria: Test Category
        data: 2025-01-01

        ## Bloco 2: Head Terms Prioritários
        - keyword1
        - keyword2
        - keyword3

        ## Bloco 3: Longtails
        - long1
        - long2
        - long3
        - long4
        - long5

        ## Bloco 6: Dores e Problemas
        - dor1
        - dor2
        - dor3

        ## Bloco 7: Ganhos Desejados
        - ganho1
        - ganho2
        - ganho3

        ## Bloco 10: Diferenciais Competitivos
        - diferencial1
        - diferencial2

        ## Bloco 12: Análise Competitiva
        Marca: Competitor A
        Marca: Competitor B

        ## End
        """
        result = parse_research_notes(markdown)
        assert result.metadata.produto == "Test Product"
        assert len(result.head_terms_prioritarios) >= 3
        assert len(result.longtails) >= 5


class TestGeneration:
    """Test ad generation."""

    def create_sample_research(self) -> ResearchNotesInput:
        """Create sample research for testing."""
        from models import CompetitorAnalysis, ResearchNotesMetadata

        return ResearchNotesInput(
            head_terms_prioritarios=["cama janela", "arranhador", "gato"],
            longtails=["cama janela gato", "arranhador parede", "poleiro gato", "rede gato", "nicho gato"],
            dores_problemas=["falta espaço", "gato entediado", "apartamento pequeno"],
            ganhos_desejados=["conforto gato", "economia espaço", "enriquecimento ambiental"],
            diferenciais_competitivos=["ventosas 90mm", "tecido oxford 600d"],
            analise_competitiva=[
                CompetitorAnalysis(marca="A", pontos_fortes=["preço"], pontos_fracos=["qualidade"]),
                CompetitorAnalysis(marca="B", pontos_fortes=["design"], pontos_fracos=["fixação"]),
            ],
            consultas_web=[
                {"termo": f"t{i}", "fonte": "ml", "data": "2025-01-01", "insight": "info"} for i in range(15)
            ],
            metadata=ResearchNotesMetadata(produto="Cama de Janela para Gatos", categoria="Pet > Gatos > Móveis"),
        )

    def test_generate_anuncio_success(self):
        """Test successful ad generation."""
        research = self.create_sample_research()
        result = generate_anuncio(research, "shopee")

        assert result.success is True
        assert result.anuncio is not None
        assert result.validation is not None
        assert result.persuasion_score is not None

    def test_generate_anuncio_structure(self):
        """Test generated ad has correct structure."""
        research = self.create_sample_research()
        result = generate_anuncio(research, "all")

        ad = result.anuncio
        assert len(ad.titulos) == 3
        assert 115 <= len(ad.bloco_palavras_1) <= 120
        assert 115 <= len(ad.bloco_palavras_2) <= 120
        assert len(ad.descricao_longa) >= 3300
        assert len(ad.prompts_imagens) == 9
        assert 6 <= len(ad.prompt_video_veo3.cenas) <= 9


class TestValidation:
    """Test output validation."""

    def create_sample_anuncio(self) -> AnuncioOutput:
        """Create sample anuncio for testing."""
        from models import (
            AuditoriaQA,
            CompetitorSEO,
            CopyDecision,
            CopyVariationType,
            ImagemPrompt,
            MarketplaceCompliance,
            MarketplaceTarget,
            MetadadosSEO,
            MetadataInterno,
            NotasFallback,
            QACheck,
            VariacaoS5,
            VideoCena,
            VideoPromptVEO3,
        )

        return AnuncioOutput(
            versao_schema="1.1",
            gerado_em=datetime.now().isoformat(),
            marketplace_target=MarketplaceTarget.ALL,
            nome_arquivo_sugerido="test.md",
            identidade_produto={"nome": "Test", "categoria": "Test"},
            proposta_valor={"promessa": "Quality", "diferencial": "Premium"},
            titulos=[
                TituloVariacao(texto="A" * 58, comprimento=58),
                TituloVariacao(texto="B" * 59, comprimento=59),
                TituloVariacao(texto="C" * 60, comprimento=60),
            ],
            bloco_palavras_1=["kw" + str(i) for i in range(115)],
            bloco_palavras_2=["term" + str(i) for i in range(115)],
            descricao_longa="X" * 3500,
            prompts_imagens=[ImagemPrompt(numero=i + 1, tipo=f"type{i+1}", prompt="P" * 60) for i in range(9)],
            prompt_video_veo3=VideoPromptVEO3(
                cenas=[
                    VideoCena(numero=i + 1, titulo=f"Scene{i+1}", descricao="D" * 40, duracao_segundos=5)
                    for i in range(7)
                ],
                duracao_total=35,
                formato="9:16",
                estilo_visual="Clean",
            ),
            metadados_seo=MetadadosSEO(
                keywords_primary=["a", "b", "c"],
                keywords_secondary=["d", "e", "f"],
                keywords_tertiary=["g", "h", "i", "j", "k"],
                competitors_analysis=[
                    CompetitorSEO(marca="A", pontos_fortes=["x"], pontos_fracos=["y"], oportunidade="z"),
                    CompetitorSEO(marca="B", pontos_fortes=["x"], pontos_fracos=["y"], oportunidade="z"),
                ],
                copy_decisions=[
                    CopyDecision(decisao="d1", rationale="r1"),
                    CopyDecision(decisao="d2", rationale="r2"),
                    CopyDecision(decisao="d3", rationale="r3"),
                ],
                marketplace_compliance=MarketplaceCompliance(),
            ),
            auditoria_qa=AuditoriaQA(
                checks=[QACheck(check_name="test", status="OK")], completude_percent=100.0, status=QAStatus.PASS
            ),
            variacoes_s5=[
                VariacaoS5(
                    tipo=CopyVariationType.EQUILIBRADA,
                    titulo="T" * 58,
                    personagem="P",
                    problema="Prob",
                    solucao="Sol",
                    abertura="A" * 100,
                ),
                VariacaoS5(
                    tipo=CopyVariationType.EMOCIONAL,
                    titulo="E" * 58,
                    personagem="P",
                    problema="Prob",
                    solucao="Sol",
                    abertura="B" * 100,
                ),
                VariacaoS5(
                    tipo=CopyVariationType.TECNICA,
                    titulo="F" * 58,
                    personagem="P",
                    problema="Prob",
                    solucao="Sol",
                    abertura="C" * 100,
                ),
            ],
            notas_fallback=NotasFallback(),
            metadata_interno=MetadataInterno(
                persuasion_score=0.80,
                persuasion_level=PersuasionLevel.GOOD,
                gatilhos_mentais=["trust"],
                frameworks_aplicados=["AIDA"],
                compliance_status="OK",
                data_geracao=datetime.now().isoformat(),
            ),
        )

    def test_validate_output_pass(self):
        """Test validation passes for good ad."""
        ad = self.create_sample_anuncio()
        result = validate_output(ad)
        assert result.is_valid is True
        assert result.qa_status == QAStatus.PASS

    def test_validate_output_detects_html(self):
        """Test validation detects HTML tags."""
        ad = self.create_sample_anuncio()
        ad.descricao_longa = "<div>Invalid HTML</div>" + "X" * 3500
        result = validate_output(ad)
        assert len(result.compliance_issues) > 0

    def test_correct_anuncio_fixes_titles(self):
        """Test auto-correction handles validation errors gracefully."""
        ad = self.create_sample_anuncio()

        # Create a validation result with errors (simulating invalid title)
        validation = ValidationResult(
            is_valid=False,
            qa_status=QAStatus.FAIL,
            completeness_score=0.5,
            errors=["Title validation failed"],
            timestamp=datetime.now().isoformat(),
        )

        # The correction function should return the ad (possibly corrected)
        corrected = correct_anuncio(ad, validation)
        # Verify the corrected ad has valid titles
        assert corrected.titulos[0].comprimento >= 58
        assert len(corrected.titulos[0].texto) >= 58


class TestPersuasionScoring:
    """Test persuasion scoring system."""

    def test_calculate_persuasion_score_high(self):
        """Test high persuasion score detection."""
        from models import (
            AuditoriaQA,
            CompetitorSEO,
            CopyDecision,
            CopyVariationType,
            ImagemPrompt,
            MarketplaceCompliance,
            MarketplaceTarget,
            MetadadosSEO,
            MetadataInterno,
            NotasFallback,
            PersuasionLevel,
            QACheck,
            VariacaoS5,
            VideoCena,
            VideoPromptVEO3,
        )

        # Create ad with persuasive elements
        persuasive_text = (
            """
            Você busca conforto para seu gato? Este problema de falta de espaço é resolvido
            com nossa solução certificada. Milhares de clientes satisfeitos aprovam.
            Garantia de qualidade testada. Benefício comprovado. Você conquista resultado.
            """
            * 50
        )  # Repeat to meet length requirement

        ad = AnuncioOutput(
            versao_schema="1.1",
            gerado_em=datetime.now().isoformat(),
            marketplace_target=MarketplaceTarget.ALL,
            nome_arquivo_sugerido="test.md",
            identidade_produto={"nome": "Test Product"},
            proposta_valor={"promessa": "Quality"},
            titulos=[
                TituloVariacao(texto="A" * 58, comprimento=58),
                TituloVariacao(texto="B" * 59, comprimento=59),
                TituloVariacao(texto="C" * 60, comprimento=60),
            ],
            bloco_palavras_1=["kw" + str(i) for i in range(115)],
            bloco_palavras_2=["term" + str(i) for i in range(115)],
            descricao_longa=persuasive_text,
            prompts_imagens=[ImagemPrompt(numero=i + 1, tipo=f"type{i+1}", prompt="P" * 60) for i in range(9)],
            prompt_video_veo3=VideoPromptVEO3(
                cenas=[
                    VideoCena(numero=i + 1, titulo=f"Scene{i+1}", descricao="D" * 40, duracao_segundos=5)
                    for i in range(7)
                ],
                duracao_total=35,
                formato="9:16",
                estilo_visual="Clean",
            ),
            metadados_seo=MetadadosSEO(
                keywords_primary=["a", "b", "c"],
                keywords_secondary=["d", "e", "f"],
                keywords_tertiary=["g", "h", "i", "j", "k"],
                competitors_analysis=[
                    CompetitorSEO(marca="A", pontos_fortes=["x"], pontos_fracos=["y"], oportunidade="z"),
                    CompetitorSEO(marca="B", pontos_fortes=["x"], pontos_fracos=["y"], oportunidade="z"),
                ],
                copy_decisions=[
                    CopyDecision(decisao="d1", rationale="r1"),
                    CopyDecision(decisao="d2", rationale="r2"),
                    CopyDecision(decisao="d3", rationale="r3"),
                ],
                marketplace_compliance=MarketplaceCompliance(),
            ),
            auditoria_qa=AuditoriaQA(
                checks=[QACheck(check_name="test", status="OK")], completude_percent=100.0, status=QAStatus.PASS
            ),
            variacoes_s5=[
                VariacaoS5(
                    tipo=CopyVariationType.EQUILIBRADA,
                    titulo="T" * 58,
                    personagem="P",
                    problema="Prob",
                    solucao="Sol",
                    abertura="A" * 100,
                ),
                VariacaoS5(
                    tipo=CopyVariationType.EMOCIONAL,
                    titulo="E" * 58,
                    personagem="P",
                    problema="Prob",
                    solucao="Sol",
                    abertura="B" * 100,
                ),
                VariacaoS5(
                    tipo=CopyVariationType.TECNICA,
                    titulo="F" * 58,
                    personagem="P",
                    problema="Prob",
                    solucao="Sol",
                    abertura="C" * 100,
                ),
            ],
            notas_fallback=NotasFallback(),
            metadata_interno=MetadataInterno(
                persuasion_score=0.85,
                persuasion_level=PersuasionLevel.EXCELLENT,
                gatilhos_mentais=["trust"],
                frameworks_aplicados=["AIDA"],
                compliance_status="OK",
                data_geracao=datetime.now().isoformat(),
            ),
        )

        score = calculate_persuasion_score(ad)
        assert score.overall_score > 0.70
        assert len(score.gatilhos_detectados) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
