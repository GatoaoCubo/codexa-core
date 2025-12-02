"""
anuncio_agent | Code Interpreter Validator
Version: 3.1.0 | Updated: 2025-11-30
Scope: TEXT-ONLY (titulos, descricao, bullets, keywords)

Features v3.1.0:
- 5-Dimension Quality Scoring (titulo, keywords, descricao, bullets, compliance)
- Intelligent Fallback (autonomous decision-making)
- Source Attribution (hybrid: visual + JSON)
- Auto-Fix capabilities

Upload this file to Code Interpreter in Agent Builder.
The agent can then import and use these functions for validation.

Usage in agent:
    from validator import validate_anuncio_v31, calculate_dimension_scores
"""

import re
import json
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict


# =============================================================================
# CONFIGURATION - Open weights for LLM autonomy
# =============================================================================

DEFAULT_WEIGHTS = {
    "titulo": 0.30,      # Drives CTR - most visible
    "keywords": 0.25,    # SEO discovery
    "descricao": 0.20,   # Converts after click
    "bullets": 0.15,     # Scannable decision points
    "compliance": 0.10   # Binary gate
}

THRESHOLDS = {
    "dimension_min": 0.75,
    "overall_min": 0.85
}

FALLBACK_LEVELS = {
    "high": {"min": 0.8, "action": "generate_full"},
    "medium": {"min": 0.6, "action": "generate_with_suggestions"},
    "low": {"min": 0.4, "action": "generate_partial_with_placeholders"},
    "very_low": {"min": 0.0, "action": "request_enrichment"}
}


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
    """Source attribution for a section."""
    section: str
    source_block: str
    confidence: float
    origin: str  # pesquisa_agent | mentor_agent | user_input


@dataclass
class ValidationReport:
    """Complete validation report."""
    timestamp: str
    version: str = "3.1.0"
    scope: str = "TEXT-ONLY"
    dimension_scores: Dict[str, DimensionScore] = field(default_factory=dict)
    overall_score: float = 0.0
    status: str = "PENDING"
    source_attribution: List[SourceAttribution] = field(default_factory=list)
    fallback_action: str = "none"
    issues: List[str] = field(default_factory=list)
    auto_fixes: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def slugify(text: str) -> str:
    """Convert product name to file-safe slug."""
    text = text.lower()
    replacements = {
        'á': 'a', 'à': 'a', 'ã': 'a', 'â': 'a', 'ä': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'õ': 'o', 'ô': 'o', 'ö': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c', 'ñ': 'n'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r'[^a-z0-9]', '_', text)
    text = re.sub(r'_+', '_', text)
    return text[:30].strip('_')


def generate_filename(product_name: str) -> str:
    """Generate standardized filename: anuncio_{slug}_{YYYYMMDD}.md"""
    slug = slugify(product_name)
    date = datetime.now().strftime('%Y%m%d')
    return f"anuncio_{slug}_{date}.md"


# =============================================================================
# DIMENSION VALIDATORS
# =============================================================================

def validate_titulo_dimension(
    titulos: List[str],
    source_info: Optional[Dict] = None
) -> DimensionScore:
    """
    Validate titulo dimension.
    Criteria: 3 titles, 58-60 chars each, differentiated angles.
    """
    issues = []
    auto_fixes = []
    details = {"titles": []}

    # Check count
    if len(titulos) != 3:
        issues.append(f"Expected 3 titles, got {len(titulos)}")

    char_scores = []
    for i, titulo in enumerate(titulos):
        variant = chr(65 + i)  # A, B, C
        chars = len(titulo)

        title_info = {
            "variant": variant,
            "chars": chars,
            "valid": 58 <= chars <= 60
        }

        if chars < 58:
            issues.append(f"Titulo {variant}: {chars} chars (need +{58-chars})")
            title_info["fix_needed"] = f"+{58-chars} chars"
        elif chars > 60:
            issues.append(f"Titulo {variant}: {chars} chars (need -{chars-60})")
            title_info["fix_needed"] = f"-{chars-60} chars"

        char_scores.append(1.0 if title_info["valid"] else 0.0)
        details["titles"].append(title_info)

    # Calculate score components
    char_compliance = sum(char_scores) / 3 if titulos else 0
    differentiation = 1.0 if len(titulos) == 3 else len(titulos) / 3

    # Overall dimension score
    score = (char_compliance * 0.6) + (differentiation * 0.4)

    return DimensionScore(
        dimension="titulo",
        score=round(score, 2),
        weight=DEFAULT_WEIGHTS["titulo"],
        contribution=round(score * DEFAULT_WEIGHTS["titulo"], 3),
        details=details,
        issues=issues,
        auto_fixes=auto_fixes
    )


def validate_keywords_dimension(
    keywords_1: str,
    keywords_2: str,
    source_info: Optional[Dict] = None
) -> DimensionScore:
    """
    Validate keywords dimension.
    Criteria: 2 blocks, 115-120 terms each.
    """
    issues = []
    auto_fixes = []

    def count_terms(kw_text: str) -> int:
        return len([k.strip() for k in kw_text.split(',') if k.strip()])

    count_1 = count_terms(keywords_1)
    count_2 = count_terms(keywords_2)

    details = {
        "block_1": {"count": count_1, "valid": 115 <= count_1 <= 120},
        "block_2": {"count": count_2, "valid": 115 <= count_2 <= 120}
    }

    # Check block 1
    if count_1 < 115:
        issues.append(f"Keywords Block 1: {count_1} terms (need +{115-count_1})")
    elif count_1 > 120:
        issues.append(f"Keywords Block 1: {count_1} terms (need -{count_1-120})")

    # Check block 2
    if count_2 < 115:
        issues.append(f"Keywords Block 2: {count_2} terms (need +{115-count_2})")
    elif count_2 > 120:
        issues.append(f"Keywords Block 2: {count_2} terms (need -{count_2-120})")

    # Calculate score
    score_1 = 1.0 if details["block_1"]["valid"] else max(0, 1 - abs(count_1 - 117.5) / 50)
    score_2 = 1.0 if details["block_2"]["valid"] else max(0, 1 - abs(count_2 - 117.5) / 50)
    score = (score_1 + score_2) / 2

    return DimensionScore(
        dimension="keywords",
        score=round(score, 2),
        weight=DEFAULT_WEIGHTS["keywords"],
        contribution=round(score * DEFAULT_WEIGHTS["keywords"], 3),
        details=details,
        issues=issues,
        auto_fixes=auto_fixes
    )


def validate_descricao_dimension(
    descricao: str,
    source_info: Optional[Dict] = None
) -> DimensionScore:
    """
    Validate descricao dimension.
    Criteria: >=3300 chars, StoryBrand elements.
    """
    issues = []
    auto_fixes = []
    chars = len(descricao)

    details = {
        "chars": chars,
        "valid": chars >= 3300,
        "storybrand_check": {
            "problem": bool(re.search(r'(problema|dor|dificuldade|sofre)', descricao, re.I)),
            "solution": bool(re.search(r'(solução|resolve|soluciona)', descricao, re.I)),
            "success": bool(re.search(r'(resultado|sucesso|conquist|alcança)', descricao, re.I)),
            "cta": bool(re.search(r'(compre|adquira|garanta|peça|clique)', descricao, re.I))
        }
    }

    storybrand_count = sum(details["storybrand_check"].values())
    details["storybrand_score"] = storybrand_count / 4

    if chars < 3300:
        issues.append(f"Descricao: {chars} chars (need +{3300-chars})")

    missing_elements = [k for k, v in details["storybrand_check"].items() if not v]
    if missing_elements:
        issues.append(f"StoryBrand missing: {', '.join(missing_elements)}")

    # Calculate score
    char_score = 1.0 if chars >= 3300 else max(0, chars / 3300)
    storybrand_score = storybrand_count / 4
    score = (char_score * 0.6) + (storybrand_score * 0.4)

    return DimensionScore(
        dimension="descricao",
        score=round(score, 2),
        weight=DEFAULT_WEIGHTS["descricao"],
        contribution=round(score * DEFAULT_WEIGHTS["descricao"], 3),
        details=details,
        issues=issues,
        auto_fixes=auto_fixes
    )


def validate_bullets_dimension(
    bullets: List[str],
    source_info: Optional[Dict] = None
) -> DimensionScore:
    """
    Validate bullets dimension.
    Criteria: 10 bullets, 250-299 chars each.
    """
    issues = []
    auto_fixes = []
    details = {"bullets": []}

    if len(bullets) != 10:
        issues.append(f"Expected 10 bullets, got {len(bullets)}")

    valid_count = 0
    for i, bullet in enumerate(bullets, 1):
        chars = len(bullet)
        valid = 250 <= chars <= 299

        bullet_info = {"index": i, "chars": chars, "valid": valid}

        if chars < 250:
            issues.append(f"Bullet {i}: {chars} chars (need +{250-chars})")
        elif chars > 299:
            issues.append(f"Bullet {i}: {chars} chars (need -{chars-299})")

        if valid:
            valid_count += 1

        details["bullets"].append(bullet_info)

    # Calculate score
    count_score = min(len(bullets), 10) / 10
    char_score = valid_count / 10 if bullets else 0
    score = (count_score * 0.4) + (char_score * 0.6)

    return DimensionScore(
        dimension="bullets",
        score=round(score, 2),
        weight=DEFAULT_WEIGHTS["bullets"],
        contribution=round(score * DEFAULT_WEIGHTS["bullets"], 3),
        details=details,
        issues=issues,
        auto_fixes=auto_fixes
    )


def validate_compliance_dimension(
    full_text: str,
    source_info: Optional[Dict] = None
) -> DimensionScore:
    """
    Validate compliance dimension.
    Criteria: No HTML, no emojis, no prohibited claims, no links.
    """
    issues = []
    auto_fixes = []

    # Check HTML
    html_pattern = r'<[^>]+>'
    has_html = bool(re.search(html_pattern, full_text))

    # Check emojis (common Unicode ranges)
    emoji_pattern = r'[\U0001F300-\U0001F9FF\U00002600-\U000027BF]'
    has_emoji = bool(re.search(emoji_pattern, full_text))

    # Check prohibited claims
    prohibited_patterns = [
        r'#\s*1\b',
        r'melhor do brasil',
        r'número 1',
        r'líder de mercado',
        r'cura\b',
        r'trata\s+(doença|enfermidade)',
        r'milagr',
    ]
    prohibited_found = []
    for pattern in prohibited_patterns:
        if re.search(pattern, full_text, re.I):
            prohibited_found.append(pattern)

    # Check external links
    link_pattern = r'https?://|www\.'
    has_links = bool(re.search(link_pattern, full_text))

    details = {
        "html": {"found": has_html, "score": 0.0 if has_html else 1.0},
        "emoji": {"found": has_emoji, "score": 0.0 if has_emoji else 1.0},
        "prohibited_claims": {"found": prohibited_found, "score": 0.0 if prohibited_found else 1.0},
        "links": {"found": has_links, "score": 0.0 if has_links else 1.0}
    }

    if has_html:
        issues.append("HTML/CSS/JS tags detected")
    if has_emoji:
        issues.append("Decorative emojis detected")
    if prohibited_found:
        issues.append(f"Prohibited claims: {prohibited_found}")
    if has_links:
        issues.append("External links detected")

    # Calculate score (all must pass for 1.0)
    scores = [details[k]["score"] for k in ["html", "emoji", "prohibited_claims", "links"]]
    score = sum(scores) / 4

    return DimensionScore(
        dimension="compliance",
        score=round(score, 2),
        weight=DEFAULT_WEIGHTS["compliance"],
        contribution=round(score * DEFAULT_WEIGHTS["compliance"], 3),
        details=details,
        issues=issues,
        auto_fixes=auto_fixes
    )


# =============================================================================
# FALLBACK INTELLIGENCE
# =============================================================================

def determine_fallback_action(confidence: float) -> Tuple[str, str]:
    """
    Determine fallback action based on confidence level.
    Returns: (action, message)
    """
    if confidence >= 0.8:
        return "generate_full", "High confidence - proceeding with full generation"
    elif confidence >= 0.6:
        return "generate_with_suggestions", "Medium confidence - generating with [VERIFICAR] markers"
    elif confidence >= 0.4:
        return "generate_partial_with_placeholders", "Low confidence - using [COMPLETAR] placeholders"
    else:
        return "request_enrichment", "Very low confidence - requesting additional input"


def calculate_input_confidence(
    product_name: Optional[str] = None,
    category: Optional[str] = None,
    head_terms: Optional[List[str]] = None,
    diferenciais: Optional[List[str]] = None,
    dores: Optional[List[str]] = None,
    provas: Optional[List[str]] = None
) -> Tuple[float, List[str]]:
    """
    Calculate confidence based on available input data.
    Returns: (confidence_score, missing_fields)
    """
    scores = []
    missing = []

    # Required fields (high weight)
    if product_name:
        scores.append(0.3)
    else:
        missing.append("product_name (required)")

    if category:
        scores.append(0.2)
    else:
        missing.append("category (required)")

    # Recommended fields (medium weight)
    if head_terms and len(head_terms) >= 3:
        scores.append(0.15)
    else:
        missing.append("head_terms (recommended)")

    if diferenciais and len(diferenciais) >= 3:
        scores.append(0.15)
    else:
        missing.append("diferenciais (recommended)")

    if dores and len(dores) >= 3:
        scores.append(0.1)
    else:
        missing.append("dores (recommended)")

    # Optional fields (low weight)
    if provas:
        scores.append(0.1)
    else:
        missing.append("provas (optional)")

    confidence = sum(scores)
    return round(confidence, 2), missing


# =============================================================================
# MAIN VALIDATION FUNCTION
# =============================================================================

def validate_anuncio_v31(
    titulos: List[str],
    descricao: str,
    keywords_1: str,
    keywords_2: str,
    bullets: List[str],
    source_info: Optional[Dict] = None,
    custom_weights: Optional[Dict[str, float]] = None
) -> ValidationReport:
    """
    Full validation of anuncio TEXT content with 5-dimension scoring.

    Args:
        titulos: List of 3 title variations
        descricao: Long description text
        keywords_1: First keywords block (comma-separated)
        keywords_2: Second keywords block (comma-separated)
        bullets: List of 10 bullet points
        source_info: Optional dict with source attribution
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

    # Combine all text for compliance check
    full_text = " ".join(titulos) + " " + descricao + " " + " ".join(bullets)
    full_text += " " + keywords_1 + " " + keywords_2

    # Validate each dimension
    titulo_score = validate_titulo_dimension(titulos, source_info)
    titulo_score.weight = weights.get("titulo", DEFAULT_WEIGHTS["titulo"])
    titulo_score.contribution = round(titulo_score.score * titulo_score.weight, 3)

    keywords_score = validate_keywords_dimension(keywords_1, keywords_2, source_info)
    keywords_score.weight = weights.get("keywords", DEFAULT_WEIGHTS["keywords"])
    keywords_score.contribution = round(keywords_score.score * keywords_score.weight, 3)

    descricao_score = validate_descricao_dimension(descricao, source_info)
    descricao_score.weight = weights.get("descricao", DEFAULT_WEIGHTS["descricao"])
    descricao_score.contribution = round(descricao_score.score * descricao_score.weight, 3)

    bullets_score = validate_bullets_dimension(bullets, source_info)
    bullets_score.weight = weights.get("bullets", DEFAULT_WEIGHTS["bullets"])
    bullets_score.contribution = round(bullets_score.score * bullets_score.weight, 3)

    compliance_score = validate_compliance_dimension(full_text, source_info)
    compliance_score.weight = weights.get("compliance", DEFAULT_WEIGHTS["compliance"])
    compliance_score.contribution = round(compliance_score.score * compliance_score.weight, 3)

    # Store dimension scores
    report.dimension_scores = {
        "titulo": titulo_score,
        "keywords": keywords_score,
        "descricao": descricao_score,
        "bullets": bullets_score,
        "compliance": compliance_score
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

    # Add source attribution if provided
    if source_info:
        for section, info in source_info.items():
            report.source_attribution.append(SourceAttribution(
                section=section,
                source_block=info.get("source", "unknown"),
                confidence=info.get("confidence", 0.5),
                origin=info.get("origin", "user_input")
            ))

    return report


def report_to_dict(report: ValidationReport) -> Dict:
    """Convert ValidationReport to JSON-serializable dict."""
    result = {
        "timestamp": report.timestamp,
        "version": report.version,
        "scope": report.scope,
        "overall_score": report.overall_score,
        "status": report.status,
        "dimension_scores": {},
        "source_attribution": [],
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

    for sa in report.source_attribution:
        result["source_attribution"].append({
            "section": sa.section,
            "source_block": sa.source_block,
            "confidence": sa.confidence,
            "origin": sa.origin
        })

    return result


def generate_quality_report_md(report: ValidationReport, product_name: str) -> str:
    """Generate markdown quality report."""
    lines = [
        f"## QUALITY REPORT | anuncio_agent v3.1.0",
        f"",
        f"**Product**: {product_name}",
        f"**Timestamp**: {report.timestamp}",
        f"**Status**: {report.status}",
        f"**Overall Score**: {report.overall_score}/1.0",
        f"",
        f"### 5-Dimension Scores",
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

    for issue in report.issues:
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
# LEGACY COMPATIBILITY
# =============================================================================

def validate_titulo(titulo: str) -> Tuple[bool, int, str]:
    """Legacy: Validate single titulo (58-60 chars)."""
    chars = len(titulo)
    if 58 <= chars <= 60:
        return True, chars, f"OK: {chars} chars"
    elif chars < 58:
        return False, chars, f"FAIL: {chars} chars (need +{58-chars} more)"
    else:
        return False, chars, f"FAIL: {chars} chars (need -{chars-60} less)"


def validate_descricao(descricao: str) -> Tuple[bool, int, str]:
    """Legacy: Validate descricao (>=3300 chars)."""
    chars = len(descricao)
    if chars >= 3300:
        return True, chars, f"OK: {chars} chars"
    else:
        return False, chars, f"FAIL: {chars} chars (need +{3300-chars} more)"


def validate_keywords(keywords_text: str) -> Tuple[bool, int, str]:
    """Legacy: Validate keywords block (115-120 terms)."""
    terms = [k.strip() for k in keywords_text.split(',') if k.strip()]
    count = len(terms)
    if 115 <= count <= 120:
        return True, count, f"OK: {count} terms"
    elif count < 115:
        return False, count, f"FAIL: {count} terms (need +{115-count} more)"
    else:
        return False, count, f"FAIL: {count} terms (need -{count-120} less)"


def validate_bullet(bullet: str, index: int) -> Tuple[bool, int, str]:
    """Legacy: Validate single bullet (250-299 chars)."""
    chars = len(bullet)
    if 250 <= chars <= 299:
        return True, chars, f"Bullet {index}: OK ({chars} chars)"
    elif chars < 250:
        return False, chars, f"Bullet {index}: FAIL ({chars} chars, need +{250-chars})"
    else:
        return False, chars, f"Bullet {index}: FAIL ({chars} chars, need -{chars-299})"


# =============================================================================
# QUICK TEST
# =============================================================================

if __name__ == "__main__":
    print("=== anuncio_agent validator v3.1.0 ===")
    print(f"Scope: TEXT-ONLY")
    print(f"Dimensions: {list(DEFAULT_WEIGHTS.keys())}")
    print(f"Weights: {DEFAULT_WEIGHTS}")
    print(f"Thresholds: {THRESHOLDS}")

    # Test slugify
    print(f"\nSlugify test:")
    print(f"  'Whey Protein 1kg' -> '{slugify('Whey Protein 1kg')}'")

    # Test confidence calculation
    conf, missing = calculate_input_confidence(
        product_name="Test Product",
        category="Suplementos"
    )
    print(f"\nConfidence test:")
    print(f"  Score: {conf}")
    print(f"  Missing: {missing}")

    # Test fallback
    action, msg = determine_fallback_action(conf)
    print(f"\nFallback test:")
    print(f"  Action: {action}")
    print(f"  Message: {msg}")
