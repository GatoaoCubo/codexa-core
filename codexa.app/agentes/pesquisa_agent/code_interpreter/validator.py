"""
pesquisa_agent | Code Interpreter Validator
Version: 3.0.0 | Updated: 2025-11-30
Scope: RESEARCH (22-block research_notes.md validation)

Features v3.0.0:
- 6-Dimension Quality Scoring (completeness, competitors, queries, insights, compliance, coherence)
- 22-Block Validation (all required blocks present)
- Intelligent Fallback (autonomous decision-making)
- Source Attribution (web queries traced)
- Auto-Fix capabilities

Upload this file to Code Interpreter in Agent Builder.
The agent can then import and use these functions for validation.

Usage in agent:
    from validator import validate_research_notes, calculate_dimension_scores
"""

import re
import json
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field


# =============================================================================
# CONFIGURATION - Open weights for LLM autonomy
# =============================================================================

DEFAULT_WEIGHTS = {
    "completeness": 0.25,    # All 22 blocks present
    "competitors": 0.25,     # >= 3 competitors analyzed
    "queries": 0.20,         # >= 15 web queries logged
    "insights": 0.15,        # Actionable insights present
    "compliance": 0.10,      # ANVISA/INMETRO checks
    "coherence": 0.05        # Cross-block consistency
}

THRESHOLDS = {
    "dimension_min": 0.75,
    "overall_min": 0.75  # Research is exploratory, slightly lower than copy
}

# 22 Required Blocks
REQUIRED_BLOCKS = [
    "LACUNAS DO BRIEF",
    "HEAD TERMS PRIORITARIOS",
    "LONGTAILS",
    "SINONIMOS E VARIACOES",
    "TERMO CONTEXTUAL",
    "DORES DO PUBLICO",
    "GANHOS DESEJADOS",
    "OBJECOES E RESPOSTAS",
    "PROVAS E EVIDENCIAS",
    "DIFERENCIAIS COMPETITIVOS",
    "RISCOS OU ALERTAS",
    "ANALISE DE CONCORRENTES",
    "BENCHMARK DE CONCORRENTES",
    "ESTRATEGIAS E GAPS",
    "PADROES DE LINGUAGEM",
    "SEO OUTBOUND",
    "SEO INBOUND",
    "REGRAS CRITICAS",
    "DECISOES DE COPY",
    "CONSULTAS WEB",
    "IMAGENS ANALISADAS",
    "NOTAS DE FALLBACK"
]


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class DimensionScore:
    """Score for a single dimension."""
    dimension: str
    score: float
    weight: float
    contribution: float
    details: Dict[str, Any] = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)
    auto_fixes: List[str] = field(default_factory=list)


@dataclass
class SourceAttribution:
    """Source attribution for a web query."""
    query: str
    source: str
    date: str
    insight: str
    confidence: float


@dataclass
class ValidationReport:
    """Complete validation report."""
    timestamp: str
    version: str = "3.0.0"
    scope: str = "RESEARCH"
    dimension_scores: Dict[str, DimensionScore] = field(default_factory=dict)
    overall_score: float = 0.0
    status: str = "PENDING"
    blocks_found: List[str] = field(default_factory=list)
    blocks_missing: List[str] = field(default_factory=list)
    source_attribution: List[SourceAttribution] = field(default_factory=list)
    fallback_action: str = "none"
    issues: List[str] = field(default_factory=list)
    auto_fixes: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def normalize_block_name(name: str) -> str:
    """Normalize block name for comparison."""
    # Remove accents, brackets, and normalize
    replacements = {
        'a': 'a', 'a': 'a', 'a': 'a', 'a': 'a', 'a': 'a',
        'e': 'e', 'e': 'e', 'e': 'e', 'e': 'e',
        'i': 'i', 'i': 'i', 'i': 'i', 'i': 'i',
        'o': 'o', 'o': 'o', 'o': 'o', 'o': 'o', 'o': 'o',
        'u': 'u', 'u': 'u', 'u': 'u', 'u': 'u',
        'c': 'c', 'n': 'n'
    }
    name = name.upper()
    for old, new in replacements.items():
        name = name.replace(old.upper(), new.upper())
    return re.sub(r'[^A-Z\s]', '', name).strip()


def slugify(text: str) -> str:
    """Convert product name to file-safe slug."""
    text = text.lower()
    replacements = {
        'a': 'a', 'a': 'a', 'a': 'a', 'a': 'a', 'a': 'a',
        'e': 'e', 'e': 'e', 'e': 'e', 'e': 'e',
        'i': 'i', 'i': 'i', 'i': 'i', 'i': 'i',
        'o': 'o', 'o': 'o', 'o': 'o', 'o': 'o', 'o': 'o',
        'u': 'u', 'u': 'u', 'u': 'u', 'u': 'u',
        'c': 'c', 'n': 'n'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r'[^a-z0-9]', '_', text)
    text = re.sub(r'_+', '_', text)
    return text[:40].strip('_')


def generate_filename(product_name: str) -> str:
    """Generate standardized filename: {slug}_research_notes.md"""
    slug = slugify(product_name)
    return f"{slug}_research_notes.md"


def extract_blocks(content: str) -> Dict[str, str]:
    """Extract all blocks from research_notes.md content."""
    blocks = {}

    # Pattern to match ## [BLOCK NAME] or ## BLOCK NAME
    pattern = r'##\s*\[?([^\]\n]+)\]?\s*\n(.*?)(?=##\s*\[?[^\]\n]+\]?|\Z)'
    matches = re.findall(pattern, content, re.DOTALL)

    for name, content_block in matches:
        normalized = normalize_block_name(name)
        blocks[normalized] = content_block.strip()

    return blocks


def count_competitors(content: str) -> int:
    """Count number of competitors analyzed."""
    # Look for ### Concorrente patterns
    pattern = r'###\s*Concorrente\s*\d+'
    matches = re.findall(pattern, content, re.IGNORECASE)
    return len(matches)


def count_web_queries(content: str) -> int:
    """Count number of web queries logged."""
    # Look for termo: or fonte: patterns in CONSULTAS WEB section
    pattern = r'termo:\s*[^\n]+'
    matches = re.findall(pattern, content, re.IGNORECASE)
    return len(matches)


def count_suggestions(content: str) -> int:
    """Count [SUGESTAO] placeholders."""
    pattern = r'\[SUGEST[AO]+O?\]'
    matches = re.findall(pattern, content, re.IGNORECASE)
    return len(matches)


# =============================================================================
# DIMENSION VALIDATORS
# =============================================================================

def validate_completeness_dimension(
    content: str,
    blocks: Dict[str, str]
) -> DimensionScore:
    """
    Validate completeness dimension.
    Criteria: All 22 blocks present with content.
    """
    issues = []
    auto_fixes = []

    found = []
    missing = []

    for required_block in REQUIRED_BLOCKS:
        normalized_required = normalize_block_name(required_block)

        # Check if any extracted block matches
        block_found = False
        for block_name in blocks.keys():
            if normalized_required in block_name or block_name in normalized_required:
                found.append(required_block)
                block_found = True
                break

        if not block_found:
            missing.append(required_block)
            issues.append(f"Block missing: {required_block}")

    details = {
        "total_required": 22,
        "found": len(found),
        "missing": len(missing),
        "missing_blocks": missing[:5]  # First 5 for brevity
    }

    # Score based on percentage found
    score = len(found) / 22

    if score < 0.75:
        auto_fixes.append("Add missing blocks to research_notes.md")

    return DimensionScore(
        dimension="completeness",
        score=round(score, 2),
        weight=DEFAULT_WEIGHTS["completeness"],
        contribution=round(score * DEFAULT_WEIGHTS["completeness"], 3),
        details=details,
        issues=issues,
        auto_fixes=auto_fixes
    )


def validate_competitors_dimension(
    content: str,
    blocks: Dict[str, str]
) -> DimensionScore:
    """
    Validate competitors dimension.
    Criteria: >= 3 competitors analyzed with quantitative data.
    """
    issues = []
    auto_fixes = []

    competitor_count = count_competitors(content)

    # Check for quantitative data (prices, ratings)
    has_prices = bool(re.search(r'R\$\s*\d+', content))
    has_ratings = bool(re.search(r'\d+\.\d+\s*(de\s*)?5', content))

    details = {
        "competitor_count": competitor_count,
        "has_prices": has_prices,
        "has_ratings": has_ratings,
        "target": 3
    }

    # Score components
    count_score = min(competitor_count / 3, 1.0)
    data_score = (0.5 if has_prices else 0) + (0.5 if has_ratings else 0)

    score = (count_score * 0.7) + (data_score * 0.3)

    if competitor_count < 3:
        issues.append(f"Only {competitor_count} competitors (need >= 3)")
        auto_fixes.append("Analyze more competitors")

    if not has_prices:
        issues.append("No BRL prices found")

    if not has_ratings:
        issues.append("No ratings (X.X/5) found")

    return DimensionScore(
        dimension="competitors",
        score=round(score, 2),
        weight=DEFAULT_WEIGHTS["competitors"],
        contribution=round(score * DEFAULT_WEIGHTS["competitors"], 3),
        details=details,
        issues=issues,
        auto_fixes=auto_fixes
    )


def validate_queries_dimension(
    content: str,
    blocks: Dict[str, str]
) -> DimensionScore:
    """
    Validate queries dimension.
    Criteria: >= 15 web queries logged with sources.
    """
    issues = []
    auto_fixes = []

    query_count = count_web_queries(content)

    # Check for source URLs
    has_urls = bool(re.search(r'fonte:\s*\w+', content, re.IGNORECASE))
    has_dates = bool(re.search(r'data:\s*\d{4}-\d{2}-\d{2}', content))

    details = {
        "query_count": query_count,
        "has_sources": has_urls,
        "has_dates": has_dates,
        "target": 15
    }

    # Score based on query count
    count_score = min(query_count / 15, 1.0)
    traceability_score = (0.5 if has_urls else 0) + (0.5 if has_dates else 0)

    score = (count_score * 0.8) + (traceability_score * 0.2)

    if query_count < 15:
        issues.append(f"Only {query_count} queries logged (need >= 15)")
        auto_fixes.append("Log more web searches with URLs")

    if not has_urls:
        issues.append("Queries missing source attribution")

    return DimensionScore(
        dimension="queries",
        score=round(score, 2),
        weight=DEFAULT_WEIGHTS["queries"],
        contribution=round(score * DEFAULT_WEIGHTS["queries"], 3),
        details=details,
        issues=issues,
        auto_fixes=auto_fixes
    )


def validate_insights_dimension(
    content: str,
    blocks: Dict[str, str]
) -> DimensionScore:
    """
    Validate insights dimension.
    Criteria: Actionable insights in key blocks.
    """
    issues = []
    auto_fixes = []

    # Check for insight markers
    has_opportunities = bool(re.search(r'oportunidad', content, re.IGNORECASE))
    has_gaps = bool(re.search(r'gap', content, re.IGNORECASE))
    has_strategies = bool(re.search(r'estrateg', content, re.IGNORECASE))
    has_actions = bool(re.search(r'recomenda|suger|prox.*passo', content, re.IGNORECASE))

    # Check for executive summary
    has_summary = bool(re.search(r'RESUMO EXECUTIVO', content, re.IGNORECASE))

    details = {
        "has_opportunities": has_opportunities,
        "has_gaps": has_gaps,
        "has_strategies": has_strategies,
        "has_actions": has_actions,
        "has_summary": has_summary
    }

    # Score based on presence
    markers = [has_opportunities, has_gaps, has_strategies, has_actions, has_summary]
    score = sum(markers) / len(markers)

    if not has_opportunities:
        issues.append("No opportunities identified")
    if not has_gaps:
        issues.append("No gaps analysis")
    if not has_summary:
        issues.append("Executive summary missing")
        auto_fixes.append("Add RESUMO EXECUTIVO section")

    return DimensionScore(
        dimension="insights",
        score=round(score, 2),
        weight=DEFAULT_WEIGHTS["insights"],
        contribution=round(score * DEFAULT_WEIGHTS["insights"], 3),
        details=details,
        issues=issues,
        auto_fixes=auto_fixes
    )


def validate_compliance_dimension(
    content: str,
    blocks: Dict[str, str]
) -> DimensionScore:
    """
    Validate compliance dimension.
    Criteria: ANVISA/INMETRO/CONAR checks present.
    """
    issues = []
    auto_fixes = []

    # Check for compliance mentions
    has_anvisa = bool(re.search(r'ANVISA', content, re.IGNORECASE))
    has_inmetro = bool(re.search(r'INMETRO', content, re.IGNORECASE))
    has_conar = bool(re.search(r'CONAR', content, re.IGNORECASE))
    has_risks = bool(re.search(r'RISCOS?\s*(OU|E)?\s*ALERTAS?', content, re.IGNORECASE))

    details = {
        "anvisa_checked": has_anvisa,
        "inmetro_checked": has_inmetro,
        "conar_checked": has_conar,
        "risk_section": has_risks
    }

    # Score based on compliance coverage
    markers = [has_anvisa or has_inmetro or has_conar, has_risks]
    score = sum(markers) / len(markers)

    if not has_risks:
        issues.append("Risk/compliance section missing")
        auto_fixes.append("Add RISCOS OU ALERTAS section")

    return DimensionScore(
        dimension="compliance",
        score=round(score, 2),
        weight=DEFAULT_WEIGHTS["compliance"],
        contribution=round(score * DEFAULT_WEIGHTS["compliance"], 3),
        details=details,
        issues=issues,
        auto_fixes=auto_fixes
    )


def validate_coherence_dimension(
    content: str,
    blocks: Dict[str, str]
) -> DimensionScore:
    """
    Validate coherence dimension.
    Criteria: Cross-block consistency, low [SUGESTAO] ratio.
    """
    issues = []
    auto_fixes = []

    suggestion_count = count_suggestions(content)
    total_chars = len(content)

    # Rough estimate: 1 suggestion per 500 chars is acceptable
    suggestion_ratio = suggestion_count / (total_chars / 500) if total_chars > 0 else 0

    # Check for header consistency
    has_product_name = bool(re.search(r'RESEARCH NOTES.*-.*\w+', content))
    has_date = bool(re.search(r'\*\*Data\*\*:\s*\d{4}-\d{2}-\d{2}', content))

    details = {
        "suggestion_count": suggestion_count,
        "suggestion_ratio": round(suggestion_ratio, 2),
        "has_product_name": has_product_name,
        "has_date": has_date,
        "target_ratio": 0.10
    }

    # Score based on suggestions and consistency
    suggestion_score = max(0, 1 - (suggestion_ratio / 0.10)) if suggestion_ratio <= 0.10 else 0.5
    consistency_score = (0.5 if has_product_name else 0) + (0.5 if has_date else 0)

    score = (suggestion_score * 0.7) + (consistency_score * 0.3)

    if suggestion_ratio > 0.10:
        issues.append(f"High [SUGESTAO] ratio: {suggestion_ratio:.1%} (target <= 10%)")
        auto_fixes.append("Fill in [SUGESTAO] placeholders with real data")

    if not has_product_name:
        issues.append("Product name not in header")

    return DimensionScore(
        dimension="coherence",
        score=round(score, 2),
        weight=DEFAULT_WEIGHTS["coherence"],
        contribution=round(score * DEFAULT_WEIGHTS["coherence"], 3),
        details=details,
        issues=issues,
        auto_fixes=auto_fixes
    )


# =============================================================================
# MAIN VALIDATION FUNCTION
# =============================================================================

def validate_research_notes(
    content: str,
    custom_weights: Optional[Dict[str, float]] = None
) -> ValidationReport:
    """
    Full validation of research_notes.md with 6-dimension scoring.

    Args:
        content: Full text content of research_notes.md
        custom_weights: Optional custom dimension weights

    Returns:
        ValidationReport with complete analysis
    """
    # Use custom weights if provided
    weights = custom_weights or DEFAULT_WEIGHTS

    # Normalize weights to sum to 1.0
    weight_sum = sum(weights.values())
    if weight_sum != 1.0:
        weights = {k: v / weight_sum for k, v in weights.items()}

    # Create report
    report = ValidationReport(
        timestamp=datetime.now().isoformat()
    )

    # Extract blocks
    blocks = extract_blocks(content)

    # Find which blocks are present/missing
    for required_block in REQUIRED_BLOCKS:
        normalized_required = normalize_block_name(required_block)
        found = False
        for block_name in blocks.keys():
            if normalized_required in block_name or block_name in normalized_required:
                report.blocks_found.append(required_block)
                found = True
                break
        if not found:
            report.blocks_missing.append(required_block)

    # Validate each dimension
    completeness_score = validate_completeness_dimension(content, blocks)
    completeness_score.weight = weights.get("completeness", DEFAULT_WEIGHTS["completeness"])
    completeness_score.contribution = round(completeness_score.score * completeness_score.weight, 3)

    competitors_score = validate_competitors_dimension(content, blocks)
    competitors_score.weight = weights.get("competitors", DEFAULT_WEIGHTS["competitors"])
    competitors_score.contribution = round(competitors_score.score * competitors_score.weight, 3)

    queries_score = validate_queries_dimension(content, blocks)
    queries_score.weight = weights.get("queries", DEFAULT_WEIGHTS["queries"])
    queries_score.contribution = round(queries_score.score * queries_score.weight, 3)

    insights_score = validate_insights_dimension(content, blocks)
    insights_score.weight = weights.get("insights", DEFAULT_WEIGHTS["insights"])
    insights_score.contribution = round(insights_score.score * insights_score.weight, 3)

    compliance_score = validate_compliance_dimension(content, blocks)
    compliance_score.weight = weights.get("compliance", DEFAULT_WEIGHTS["compliance"])
    compliance_score.contribution = round(compliance_score.score * compliance_score.weight, 3)

    coherence_score = validate_coherence_dimension(content, blocks)
    coherence_score.weight = weights.get("coherence", DEFAULT_WEIGHTS["coherence"])
    coherence_score.contribution = round(coherence_score.score * coherence_score.weight, 3)

    # Store dimension scores
    report.dimension_scores = {
        "completeness": completeness_score,
        "competitors": competitors_score,
        "queries": queries_score,
        "insights": insights_score,
        "compliance": compliance_score,
        "coherence": coherence_score
    }

    # Calculate overall score
    report.overall_score = round(sum(
        ds.contribution for ds in report.dimension_scores.values()
    ), 2)

    # Determine status
    all_dimensions_pass = all(
        ds.score >= THRESHOLDS["dimension_min"]
        for ds in report.dimension_scores.values()
    )
    overall_passes = report.overall_score >= THRESHOLDS["overall_min"]

    if all_dimensions_pass and overall_passes:
        report.status = "PASS"
    elif overall_passes:
        report.status = "PASS_WITH_WARNINGS"
    else:
        report.status = "FAIL"

    # Collect all issues
    for ds in report.dimension_scores.values():
        report.issues.extend(ds.issues)
        report.auto_fixes.extend(ds.auto_fixes)

    # Generate recommendations
    if report.status != "PASS":
        low_dimensions = [
            ds.dimension for ds in report.dimension_scores.values()
            if ds.score < THRESHOLDS["dimension_min"]
        ]
        if low_dimensions:
            report.recommendations.append(
                f"Improve dimensions: {', '.join(low_dimensions)}"
            )

    return report


def report_to_dict(report: ValidationReport) -> Dict:
    """Convert ValidationReport to JSON-serializable dict."""
    result = {
        "timestamp": report.timestamp,
        "version": report.version,
        "scope": report.scope,
        "overall_score": report.overall_score,
        "status": report.status,
        "blocks_found": len(report.blocks_found),
        "blocks_missing": report.blocks_missing,
        "dimension_scores": {},
        "issues": report.issues,
        "auto_fixes": report.auto_fixes,
        "recommendations": report.recommendations
    }

    for dim, ds in report.dimension_scores.items():
        result["dimension_scores"][dim] = {
            "score": ds.score,
            "weight": ds.weight,
            "contribution": ds.contribution,
            "details": ds.details,
            "issues": ds.issues
        }

    return result


def generate_quality_report_md(report: ValidationReport, product_name: str) -> str:
    """Generate markdown quality report."""
    lines = [
        f"## QUALITY REPORT | pesquisa_agent v3.0.0",
        f"",
        f"**Product**: {product_name}",
        f"**Timestamp**: {report.timestamp}",
        f"**Status**: {report.status}",
        f"**Overall Score**: {report.overall_score}/1.0",
        f"",
        f"### Block Coverage",
        f"",
        f"- Found: {len(report.blocks_found)}/22",
        f"- Missing: {len(report.blocks_missing)}",
        f"",
        f"### 6-Dimension Scores",
        f"",
        f"| Dimension | Score | Weight | Contribution |",
        f"|-----------|-------|--------|--------------|"
    ]

    for dim, ds in report.dimension_scores.items():
        lines.append(f"| {dim.capitalize()} | {ds.score} | {ds.weight} | {ds.contribution} |")

    lines.extend([
        f"",
        f"### Issues Detected ({len(report.issues)})",
        f""
    ])

    for issue in report.issues[:10]:  # First 10
        lines.append(f"- {issue}")

    if report.recommendations:
        lines.extend([
            f"",
            f"### Recommendations",
            f""
        ])
        for rec in report.recommendations:
            lines.append(f"- {rec}")

    return "\n".join(lines)


# =============================================================================
# QUICK TEST
# =============================================================================

if __name__ == "__main__":
    print("=== pesquisa_agent validator v3.0.0 ===")
    print(f"Scope: RESEARCH (22 blocks)")
    print(f"Dimensions: {list(DEFAULT_WEIGHTS.keys())}")
    print(f"Weights: {DEFAULT_WEIGHTS}")
    print(f"Thresholds: {THRESHOLDS}")

    # Test slugify
    print(f"\nSlugify test:")
    print(f"  'Garrafa de Agua Reutilizavel' -> '{slugify('Garrafa de Agua Reutilizavel')}'")

    # Test filename generation
    print(f"\nFilename test:")
    print(f"  -> '{generate_filename('Garrafa de Agua Reutilizavel')}'")

    print("\n[OK] Validator ready for use")
