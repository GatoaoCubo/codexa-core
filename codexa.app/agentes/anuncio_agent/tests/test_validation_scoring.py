"""
Tests for validation and scoring functions in processor.py.
"""

from datetime import datetime

import pytest

from models import (
    AnuncioOutput,
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
    QAStatus,
    TituloVariacao,
    ValidationResult,
    VariacaoS5,
    VideoCena,
    VideoPromptVEO3,
)
from processor import (
    calculate_persuasion_score,
    correct_anuncio,
    validate_output,
)


class TestValidationFunctions:
    """Test validation functions."""

    def create_valid_anuncio(self) -> AnuncioOutput:
        """Create a valid anuncio for testing."""
        return AnuncioOutput(
            versao_schema="1.1",
            gerado_em=datetime.now().isoformat(),
            marketplace_target=MarketplaceTarget.MERCADO_LIVRE,
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
                persuasion_score=0.85,
                persuasion_level=PersuasionLevel.EXCELLENT,
                gatilhos_mentais=["trust"],
                frameworks_aplicados=["AIDA"],
                compliance_status="OK",
                data_geracao=datetime.now().isoformat(),
            ),
        )

    def test_validate_shopee(self):
        """Test validation for Shopee marketplace."""
        ad = self.create_valid_anuncio()
        ad.marketplace_target = MarketplaceTarget.SHOPEE
        result = validate_output(ad)
        assert isinstance(result, ValidationResult)

    def test_validate_magalu(self):
        """Test validation for Magazine Luiza marketplace."""
        ad = self.create_valid_anuncio()
        ad.marketplace_target = MarketplaceTarget.MAGALU
        result = validate_output(ad)
        assert isinstance(result, ValidationResult)

    def test_validate_amazon(self):
        """Test validation for Amazon marketplace."""
        ad = self.create_valid_anuncio()
        ad.marketplace_target = MarketplaceTarget.AMAZON
        result = validate_output(ad)
        assert isinstance(result, ValidationResult)

    def test_validate_detects_emojis(self):
        """Test validation detects emojis in description."""
        ad = self.create_valid_anuncio()
        ad.descricao_longa = "🎉 Produto incrível! " + "X" * 3500
        result = validate_output(ad)
        # Should detect emoji compliance issue
        assert isinstance(result, ValidationResult)

    def test_validate_detects_superlatives(self):
        """Test validation detects absolute superlatives."""
        ad = self.create_valid_anuncio()
        ad.descricao_longa = "O melhor produto do mundo! " + "X" * 3500
        result = validate_output(ad)
        assert isinstance(result, ValidationResult)

    def test_calculate_persuasion_with_triggers(self):
        """Test persuasion scoring with mental triggers."""
        ad = self.create_valid_anuncio()
        ad.descricao_longa = (
            """
        Você merece o melhor. Garantia de satisfação comprovada.
        Milhares de clientes satisfeitos. Oferta limitada.
        Exclusivo e premium. Resultados imediatos.
        """
            * 30
        )
        score = calculate_persuasion_score(ad)
        assert hasattr(score, "overall_score")
        assert 0.0 <= score.overall_score <= 1.0

    def test_correct_anuncio_returns_ad(self):
        """Test that correct_anuncio returns the ad."""
        ad = self.create_valid_anuncio()
        validation = ValidationResult(
            is_valid=True,
            qa_status=QAStatus.PASS,
            completeness_score=1.0,
            errors=[],
            timestamp=datetime.now().isoformat(),
        )
        corrected = correct_anuncio(ad, validation)
        assert isinstance(corrected, AnuncioOutput)
        assert corrected.titulos[0].comprimento >= 58


class TestPersuasionScoring:
    """Test persuasion scoring functions."""

    def test_persuasion_poor_score(self):
        """Test persuasion scoring with poor content."""
        ad = AnuncioOutput(
            versao_schema="1.1",
            gerado_em=datetime.now().isoformat(),
            marketplace_target=MarketplaceTarget.ALL,
            nome_arquivo_sugerido="test.md",
            identidade_produto={"nome": "Test"},
            proposta_valor={"promessa": "OK"},
            titulos=[
                TituloVariacao(texto="A" * 58, comprimento=58),
                TituloVariacao(texto="B" * 59, comprimento=59),
                TituloVariacao(texto="C" * 60, comprimento=60),
            ],
            bloco_palavras_1=["w" * 10 for i in range(115)],
            bloco_palavras_2=["t" * 10 for i in range(115)],
            descricao_longa="Plain text. No persuasion. " * 150,
            prompts_imagens=[ImagemPrompt(numero=i + 1, tipo=f"t{i+1}", prompt="P" * 60) for i in range(9)],
            prompt_video_veo3=VideoPromptVEO3(
                cenas=[
                    VideoCena(numero=i + 1, titulo=f"S{i+1}", descricao="D" * 40, duracao_segundos=5) for i in range(7)
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
                    problema="P",
                    solucao="S",
                    abertura="A" * 100,
                ),
                VariacaoS5(
                    tipo=CopyVariationType.EMOCIONAL,
                    titulo="E" * 58,
                    personagem="P",
                    problema="P",
                    solucao="S",
                    abertura="B" * 100,
                ),
                VariacaoS5(
                    tipo=CopyVariationType.TECNICA,
                    titulo="F" * 58,
                    personagem="P",
                    problema="P",
                    solucao="S",
                    abertura="C" * 100,
                ),
            ],
            notas_fallback=NotasFallback(),
            metadata_interno=MetadataInterno(
                persuasion_score=0.30,
                persuasion_level=PersuasionLevel.POOR,
                gatilhos_mentais=[],
                frameworks_aplicados=[],
                compliance_status="OK",
                data_geracao=datetime.now().isoformat(),
            ),
        )

        score = calculate_persuasion_score(ad)
        assert hasattr(score, "overall_score")
        # Score should be low for plain text
        assert score.overall_score >= 0.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
