"""
Data models for CodeXAnuncio.
KEYWORDS: models|schema|validation|pydantic|dense

Compact, production-ready models with validation.
"""

import math
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, field_validator

# ===== ENUMS =====


class SourceGrade(Enum):
    """Source quality grade."""

    A, B, C, D, E, F = 1.0, 0.9, 0.75, 0.6, 0.4, 0.2


class MarketplaceTarget(str, Enum):
    """Supported marketplaces."""

    MERCADO_LIVRE = "mercadolivre"
    SHOPEE = "shopee"
    MAGALU = "magalu"
    AMAZON = "amazon"
    ALL = "all"


class QAStatus(str, Enum):
    """QA status."""

    PASS, PARTIAL, FAIL = "PASS", "PARTIAL", "FAIL"


class PersuasionLevel(str, Enum):
    """Persuasion level."""

    POOR, FAIR, GOOD, EXCELLENT = "poor", "fair", "good", "excellent"


class CopyVariationType(str, Enum):
    """Copy variation types."""

    EQUILIBRADA, EMOCIONAL, TECNICA = "equilibrada", "emocional", "tecnica"


# ===== CONFIDENCE SCORING =====


class ConfidenceScore(BaseModel):
    """Multi-dimensional confidence scoring."""

    source_grade: SourceGrade
    novelty: int = Field(..., ge=1, le=5)
    corroboration: int = Field(..., ge=0)
    recency_days: int = Field(..., ge=0)

    def calculate(self) -> float:
        """Calculate overall confidence (0.0-1.0)."""
        return round(
            self.source_grade.value * 0.4
            + ((6 - self.novelty) / 5) * 0.2
            + min(self.corroboration / 5, 1.0) * 0.25
            + math.exp(-self.recency_days / 180) * 0.15,
            2,
        )

    def interpret(self) -> str:
        """Human-readable interpretation."""
        score = self.calculate()
        if score >= 0.90:
            return "EXCELLENT - High confidence"
        if score >= 0.75:
            return "GOOD - Reliable"
        if score >= 0.60:
            return "FAIR - Use with caution"
        return "POOR - Verify before use"


# ===== INPUT MODELS =====


class ObjecaoResposta(BaseModel):
    """Objection-response pair."""

    objecao: str
    resposta: str


class CompetitorAnalysis(BaseModel):
    """Competitor analysis."""

    marca: str
    pontos_fortes: list[str] = Field(default_factory=list)
    pontos_fracos: list[str] = Field(default_factory=list)
    preco_range: Optional[str] = None


class BenchmarkMetrics(BaseModel):
    """Market benchmark metrics."""

    preco_medio: Optional[str] = None
    volume_vendas: Optional[str] = None
    rating_medio: Optional[float] = None
    numero_avaliacoes: Optional[str] = None


class MarketplacePolitica(BaseModel):
    """Marketplace policy."""

    marketplace: str
    restricoes: list[str] = Field(default_factory=list)
    requisitos: list[str] = Field(default_factory=list)


class ConsultaWeb(BaseModel):
    """Web query record."""

    termo: str
    fonte: str
    data: str
    insight: str


class ResearchNotesMetadata(BaseModel):
    """Research metadata."""

    produto: str
    categoria: str
    data_pesquisa: Optional[str] = None
    versao: str = "1.0"


class ResearchNotesInput(BaseModel):
    """Complete research notes input."""

    model_config = {"validate_assignment": True}

    # Keywords & SEO
    lacunas_do_brief: list[str] = Field(default_factory=list)
    head_terms_prioritarios: list[str] = Field(..., min_length=3)
    longtails: list[str] = Field(..., min_length=5)
    sinonimos_variacoes: list[str] = Field(default_factory=list)
    termo_contextual_ocasiao: list[str] = Field(default_factory=list)

    # Customer insights
    dores_problemas: list[str] = Field(..., min_length=3)
    ganhos_desejados: list[str] = Field(..., min_length=3)
    objecoes_respostas: list[ObjecaoResposta] = Field(default_factory=list)
    provas_disponiveis: list[str] = Field(default_factory=list)
    diferenciais_competitivos: list[str] = Field(..., min_length=2)

    # Market intelligence
    riscos_alertas_compliance: list[str] = Field(default_factory=list)
    analise_competitiva: list[CompetitorAnalysis] = Field(..., min_length=2)
    benchmark_metricas: Optional[BenchmarkMetrics] = None
    sugestoes_claims: list[str] = Field(default_factory=list)
    padroes_linguagem: list[str] = Field(default_factory=list)

    # Content patterns
    keywords_tendencia: list[str] = Field(default_factory=list)
    templates_copy: list[str] = Field(default_factory=list)
    politicas_marketplace: list[MarketplacePolitica] = Field(default_factory=list)
    guidelines_iniciais_copy: list[str] = Field(default_factory=list)

    # Audit trail
    consultas_web: list[ConsultaWeb] = Field(..., min_length=15)
    imagens_analisadas: list[str] = Field(default_factory=list)
    notas_fallback: list[str] = Field(default_factory=list)

    # Quality metrics
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    metadata: ResearchNotesMetadata


# ===== OUTPUT MODELS =====


class TituloVariacao(BaseModel):
    """Title variation."""

    texto: str = Field(..., min_length=58, max_length=60)
    comprimento: int = Field(..., ge=58, le=60)

    @field_validator("comprimento")
    @classmethod
    def validate_comprimento(cls, v, info):
        if "texto" in info.data and len(info.data["texto"]) != v:
            raise ValueError(f"Length mismatch: {v} != {len(info.data['texto'])}")
        return v


class ImagemPrompt(BaseModel):
    """Image generation prompt."""

    numero: int = Field(..., ge=1, le=9)
    tipo: str
    prompt: str = Field(..., min_length=50)


class VideoCena(BaseModel):
    """Video scene."""

    numero: int = Field(..., ge=1, le=9)
    titulo: str
    descricao: str = Field(..., min_length=30)
    duracao_segundos: int = Field(..., ge=3, le=15)


class VideoPromptVEO3(BaseModel):
    """VEO3 video prompt."""

    cenas: list[VideoCena] = Field(..., min_length=6, max_length=9)
    duracao_total: int = Field(..., ge=30, le=60)
    formato: str = "9:16"
    estilo_visual: str

    @field_validator("duracao_total")
    @classmethod
    def validate_duracao(cls, v, info):
        if "cenas" in info.data:
            total = sum(c.duracao_segundos for c in info.data["cenas"])
            if abs(total - v) > 5:
                raise ValueError(f"Duration mismatch: {v}s != {total}s")
        return v


class CompetitorSEO(BaseModel):
    """Competitor SEO analysis."""

    marca: str
    pontos_fortes: list[str]
    pontos_fracos: list[str]
    oportunidade: str


class CopyDecision(BaseModel):
    """Strategic copy decision."""

    decisao: str
    rationale: str


class MarketplaceCompliance(BaseModel):
    """Marketplace compliance status."""

    mercadolivre: str = Field("ok", pattern="^(ok|warning|alert)$")
    shopee: str = Field("ok", pattern="^(ok|warning|alert)$")
    magalu: str = Field("ok", pattern="^(ok|warning|alert)$")
    amazon: str = Field("ok", pattern="^(ok|warning|alert)$")


class MetadadosSEO(BaseModel):
    """SEO metadata."""

    keywords_primary: list[str] = Field(..., min_length=3, max_length=3)
    keywords_secondary: list[str] = Field(..., min_length=3, max_length=5)
    keywords_tertiary: list[str] = Field(..., min_length=5, max_length=10)
    competitors_analysis: list[CompetitorSEO] = Field(..., min_length=2)
    copy_decisions: list[CopyDecision] = Field(..., min_length=3)
    marketplace_compliance: MarketplaceCompliance


class QACheck(BaseModel):
    """Single QA check."""

    check_name: str
    status: Literal["OK", "FAIL"]
    details: str = ""


class AuditoriaQA(BaseModel):
    """QA audit."""

    checks: list[QACheck]
    completude_percent: float = Field(..., ge=0, le=100)
    status: QAStatus
    issues_encontrados: list[str] = Field(default_factory=list)
    acoes_recomendadas: list[str] = Field(default_factory=list)


class VariacaoS5(BaseModel):
    """S5 copy variation."""

    tipo: CopyVariationType
    titulo: str = Field(..., min_length=58, max_length=60)
    personagem: str
    problema: str
    solucao: str
    abertura: str = Field(..., min_length=80, max_length=800)


class NotasFallback(BaseModel):
    """Fallback notes."""

    inferencias: list[str] = Field(default_factory=list)
    alertas_qualidade: list[str] = Field(default_factory=list)
    metadados_nao_utilizados: list[str] = Field(default_factory=list)
    sugestoes_melhoria: list[str] = Field(default_factory=list)


class MetadataInterno(BaseModel):
    """Internal metadata."""

    persuasion_score: float = Field(..., ge=0.0, le=1.0)
    persuasion_level: PersuasionLevel
    gatilhos_mentais: list[str]
    frameworks_aplicados: list[str]
    compliance_status: Literal["OK", "WARNING", "ALERT"]
    gerado_por: str = "CodeXAnuncio v1.1"
    data_geracao: str


class AnuncioOutput(BaseModel):
    """Complete ad output."""

    # Header
    versao_schema: str = "1.1"
    gerado_em: str
    marketplace_target: MarketplaceTarget

    # Identity
    nome_arquivo_sugerido: str
    identidade_produto: dict[str, str]
    proposta_valor: dict[str, str]

    # Content
    titulos: list[TituloVariacao] = Field(..., min_length=3, max_length=3)
    bloco_palavras_1: list[str] = Field(..., min_length=115, max_length=120)
    bloco_palavras_2: list[str] = Field(..., min_length=115, max_length=120)
    descricao_longa: str = Field(..., min_length=3300)

    # Visual
    prompts_imagens: list[ImagemPrompt] = Field(..., min_length=9, max_length=9)
    prompt_video_veo3: VideoPromptVEO3

    # Metadata
    metadados_seo: MetadadosSEO
    auditoria_qa: AuditoriaQA
    variacoes_s5: list[VariacaoS5] = Field(..., min_length=3, max_length=3)
    notas_fallback: NotasFallback
    metadata_interno: MetadataInterno


# ===== VALIDATION & SCORING =====


class ValidationResult(BaseModel):
    """Validation result."""

    is_valid: bool
    qa_status: QAStatus
    compliance_issues: list[str] = Field(default_factory=list)
    completeness_score: float = Field(..., ge=0.0, le=1.0)
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    timestamp: str


class PersuasionScore(BaseModel):
    """Persuasion scoring."""

    overall_score: float = Field(..., ge=0.0, le=1.0)
    level: PersuasionLevel

    # Components
    gatilhos_mentais_score: float = Field(..., ge=0.0, le=1.0)
    storybrand_structure_score: float = Field(..., ge=0.0, le=1.0)
    beneficios_densidade_score: float = Field(..., ge=0.0, le=1.0)
    provas_evidencias_score: float = Field(..., ge=0.0, le=1.0)

    # Detected elements
    gatilhos_detectados: list[str]
    frameworks_detectados: list[str]
    beneficios_count: int
    features_count: int
    beneficio_feature_ratio: float

    # Recommendations
    recomendacoes: list[str] = Field(default_factory=list)


# ===== PROCESSING =====


class GenerationContext(BaseModel):
    """Generation context."""

    research_input: ResearchNotesInput
    marketplace_target: MarketplaceTarget
    copy_rules: dict[str, Any]
    persuasion_patterns: dict[str, Any]
    marketplace_specs: dict[str, Any]
    started_at: str
    phase: str = "initialization"


class GenerationResult(BaseModel):
    """Generation result."""

    success: bool
    anuncio: Optional[AnuncioOutput] = None
    validation: Optional[ValidationResult] = None
    persuasion_score: Optional[PersuasionScore] = None
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    duration_seconds: float
    timestamp: str
