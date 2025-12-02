"""
Unit tests for CodeXAnuncio models.
Tests data validation, confidence scoring, and model integrity.
"""


import pytest

from models import (
    CompetitorAnalysis,
    ConfidenceScore,
    MarketplaceTarget,
    PersuasionLevel,
    QAStatus,
    ResearchNotesInput,
    ResearchNotesMetadata,
    SourceGrade,
    TituloVariacao,
)


class TestConfidenceScore:
    """Test confidence scoring system."""

    def test_confidence_calculation_excellent(self):
        """Test excellent confidence score."""
        score = ConfidenceScore(source_grade=SourceGrade.A, novelty=1, corroboration=5, recency_days=0)
        result = score.calculate()
        assert result >= 0.90
        assert score.interpret() == "EXCELLENT - High confidence"

    def test_confidence_calculation_poor(self):
        """Test poor confidence score."""
        score = ConfidenceScore(source_grade=SourceGrade.F, novelty=5, corroboration=0, recency_days=365)
        result = score.calculate()
        assert result < 0.60
        assert score.interpret() == "POOR - Verify before use"

    def test_confidence_decay_over_time(self):
        """Test that recency impacts score."""
        recent = ConfidenceScore(source_grade=SourceGrade.A, novelty=3, corroboration=3, recency_days=0)
        old = ConfidenceScore(source_grade=SourceGrade.A, novelty=3, corroboration=3, recency_days=365)
        assert recent.calculate() > old.calculate()


class TestResearchNotesInput:
    """Test research notes validation."""

    def create_valid_research(self) -> ResearchNotesInput:
        """Create valid research notes for testing."""
        return ResearchNotesInput(
            head_terms_prioritarios=["termo1", "termo2", "termo3"],
            longtails=["long1", "long2", "long3", "long4", "long5"],
            dores_problemas=["dor1", "dor2", "dor3"],
            ganhos_desejados=["ganho1", "ganho2", "ganho3"],
            diferenciais_competitivos=["dif1", "dif2"],
            analise_competitiva=[
                CompetitorAnalysis(marca="A", pontos_fortes=["x"], pontos_fracos=["y"]),
                CompetitorAnalysis(marca="B", pontos_fortes=["x"], pontos_fracos=["y"]),
            ],
            consultas_web=[
                {"termo": f"t{i}", "fonte": "web", "data": "2025-01-01", "insight": f"i{i}"} for i in range(15)
            ],
            metadata=ResearchNotesMetadata(produto="Test Product", categoria="Test Category"),
        )

    def test_valid_research_notes(self):
        """Test valid research notes pass validation."""
        research = self.create_valid_research()
        assert research.metadata.produto == "Test Product"
        assert len(research.head_terms_prioritarios) >= 3
        assert len(research.longtails) >= 5

    def test_missing_required_fields_fail(self):
        """Test that missing required fields raise validation error."""
        with pytest.raises(Exception):
            ResearchNotesInput(
                head_terms_prioritarios=["a", "b"],  # Only 2, need 3
                longtails=["x"],  # Only 1, need 5
                dores_problemas=[],  # Empty, need 3
                ganhos_desejados=[],
                diferenciais_competitivos=[],
                analise_competitiva=[],
                consultas_web=[],
                metadata=ResearchNotesMetadata(produto="X", categoria="Y"),
            )

    def test_confidence_score_range(self):
        """Test confidence score is within valid range."""
        research = self.create_valid_research()
        research.confidence_score = 0.85
        assert 0.0 <= research.confidence_score <= 1.0

        with pytest.raises(Exception):
            research_invalid = self.create_valid_research()
            research_invalid.confidence_score = 1.5  # Invalid


class TestTituloVariacao:
    """Test title variation validation."""

    def test_valid_titulo_58_chars(self):
        """Test 58-character title passes."""
        texto = "A" * 58
        titulo = TituloVariacao(texto=texto, comprimento=58)
        assert titulo.comprimento == 58

    def test_valid_titulo_60_chars(self):
        """Test 60-character title passes."""
        texto = "B" * 60
        titulo = TituloVariacao(texto=texto, comprimento=60)
        assert titulo.comprimento == 60

    def test_invalid_titulo_too_short(self):
        """Test title <58 chars fails."""
        with pytest.raises(Exception):
            TituloVariacao(texto="Too short", comprimento=9)

    def test_invalid_titulo_too_long(self):
        """Test title >60 chars fails."""
        with pytest.raises(Exception):
            TituloVariacao(texto="X" * 61, comprimento=61)

    def test_length_mismatch_fails(self):
        """Test that comprimento must match actual length."""
        with pytest.raises(Exception):
            TituloVariacao(texto="A" * 58, comprimento=60)


class TestMarketplaceTarget:
    """Test marketplace enum."""

    def test_valid_marketplaces(self):
        """Test all valid marketplace values."""
        assert MarketplaceTarget.MERCADO_LIVRE.value == "mercadolivre"
        assert MarketplaceTarget.SHOPEE.value == "shopee"
        assert MarketplaceTarget.MAGALU.value == "magalu"
        assert MarketplaceTarget.AMAZON.value == "amazon"
        assert MarketplaceTarget.ALL.value == "all"

    def test_invalid_marketplace_fails(self):
        """Test invalid marketplace value fails."""
        with pytest.raises(ValueError):
            MarketplaceTarget("invalid_marketplace")


class TestEnums:
    """Test enum integrity."""

    def test_qa_status_values(self):
        """Test QA status enum values."""
        assert QAStatus.PASS.value == "PASS"
        assert QAStatus.PARTIAL.value == "PARTIAL"
        assert QAStatus.FAIL.value == "FAIL"

    def test_persuasion_level_values(self):
        """Test persuasion level enum values."""
        assert PersuasionLevel.POOR.value == "poor"
        assert PersuasionLevel.FAIR.value == "fair"
        assert PersuasionLevel.GOOD.value == "good"
        assert PersuasionLevel.EXCELLENT.value == "excellent"

    def test_source_grade_values(self):
        """Test source grade weights."""
        assert SourceGrade.A.value == 1.0
        assert SourceGrade.B.value == 0.9
        assert SourceGrade.F.value == 0.2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
