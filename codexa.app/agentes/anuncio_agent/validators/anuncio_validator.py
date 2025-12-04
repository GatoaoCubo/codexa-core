"""
anuncio_agent | Quality Validation Module
Version: 1.0.0
Scope: TEXT-ONLY (títulos, descricao, keywords, bullets)

Production-ready validator for anúncios with:
- Title validation (58-60 chars per ML algorithm)
- Keyword validation (60+ unique terms minimum)
- Description validation (3300+ chars)
- Multi-dimensional scoring (0-10 scale)
- JSON report export

Usage:
    from validators.anuncio_validator import AnuncioValidator

    validator = AnuncioValidator()
    report = validator.validate(
        titulos=["Título A", "Título B", "Título C"],
        descricao="Long description...",
        keywords_block_1="keyword1, keyword2, ...",
        keywords_block_2="keyword1, keyword2, ...",
        bullets=["Bullet 1", "Bullet 2", ...]
    )

    print(report.to_json())
"""

import json
import re
from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any


# =============================================================================
# VALIDATION REPORT DATA CLASSES
# =============================================================================

@dataclass
class ComponentScore:
    """Score for a single validation component."""
    name: str
    score: float  # 0-10
    max_score: float
    status: str  # "PASS" | "WARN" | "FAIL"
    details: Dict[str, Any] = field(default_factory=dict)
    issues: List[str] = field(default_factory=list)


@dataclass
class ValidationReport:
    """Complete validation report with breakdown and overall score."""
    timestamp: str
    version: str = "1.0.0"
    overall_score: float = 0.0  # 0-10
    status: str = "PENDING"  # "PASS" | "WARN" | "FAIL"
    component_scores: Dict[str, ComponentScore] = field(default_factory=dict)
    total_issues: int = 0
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert to JSON-serializable dictionary."""
        report_dict = {
            "timestamp": self.timestamp,
            "version": self.version,
            "overall_score": round(self.overall_score, 2),
            "status": self.status,
            "total_issues": self.total_issues,
            "components": {},
            "recommendations": self.recommendations
        }

        for name, score in self.component_scores.items():
            report_dict["components"][name] = {
                "score": round(score.score, 2),
                "max_score": score.max_score,
                "status": score.status,
                "details": score.details,
                "issues": score.issues
            }

        return report_dict

    def to_json(self) -> str:
        """Export report as formatted JSON string."""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)


# =============================================================================
# VALIDATOR CLASS
# =============================================================================

class AnuncioValidator:
    """
    Production-quality validator for anúncios.

    Dimensions:
    - Títulos: 3 variations, 58-60 chars each (ML optimization)
    - Keywords: 60+ unique terms across blocks
    - Descrição: 3300+ chars with StoryBrand structure
    - Bullets: 10 items, 250-299 chars each

    Scoring: 0-10 scale with weighted components
    """

    # Configuration constants
    TITLE_COUNT = 3
    TITLE_MIN_CHARS = 58
    TITLE_MAX_CHARS = 60

    KEYWORDS_MIN_UNIQUE = 60
    KEYWORDS_BLOCK_MIN = 115
    KEYWORDS_BLOCK_MAX = 120

    DESCRIPTION_MIN_CHARS = 3300

    BULLET_COUNT = 10
    BULLET_MIN_CHARS = 250
    BULLET_MAX_CHARS = 299

    # Scoring weights (sum = 1.0)
    WEIGHTS = {
        "titulos": 0.25,
        "keywords": 0.20,
        "descricao": 0.30,
        "bullets": 0.15,
        "compliance": 0.10
    }

    # Status thresholds
    PASS_THRESHOLD = 8.0
    WARN_THRESHOLD = 6.0

    def __init__(self):
        """Initialize validator."""
        self.report = None

    def validate(
        self,
        titulos: List[str],
        descricao: str,
        keywords_block_1: str,
        keywords_block_2: str,
        bullets: List[str],
        strict_mode: bool = False
    ) -> ValidationReport:
        """
        Validate anúncio content across all dimensions.

        Args:
            titulos: List of 3 title variations
            descricao: Long-form description text
            keywords_block_1: Comma-separated keywords
            keywords_block_2: Comma-separated keywords
            bullets: List of 10 bullet points
            strict_mode: If True, fails on any issue (default: False)

        Returns:
            ValidationReport with scores, issues, and recommendations
        """
        # Initialize report
        self.report = ValidationReport(
            timestamp=datetime.now().isoformat()
        )

        # Validate each dimension
        titulo_score = self._validate_titulos(titulos)
        keywords_score = self._validate_keywords(
            keywords_block_1, keywords_block_2
        )
        descricao_score = self._validate_descricao(descricao)
        bullets_score = self._validate_bullets(bullets)
        compliance_score = self._validate_compliance(
            titulos, descricao, keywords_block_1,
            keywords_block_2, bullets
        )

        # Store component scores
        self.report.component_scores = {
            "titulos": titulo_score,
            "keywords": keywords_score,
            "descricao": descricao_score,
            "bullets": bullets_score,
            "compliance": compliance_score
        }

        # Calculate weighted overall score
        self._calculate_overall_score()

        # Determine status
        self._determine_status(strict_mode)

        # Generate recommendations
        self._generate_recommendations()

        return self.report

    # =========================================================================
    # DIMENSION VALIDATORS
    # =========================================================================

    def _validate_titulos(self, titulos: List[str]) -> ComponentScore:
        """Validate title dimension (3 titles, 58-60 chars each)."""
        score = ComponentScore(
            name="titulos",
            score=0.0,
            max_score=10.0,
            status="FAIL",
            details={"titles": []},
            issues=[]
        )

        # Check count
        if len(titulos) != self.TITLE_COUNT:
            score.issues.append(
                f"Expected {self.TITLE_COUNT} titles, got {len(titulos)}"
            )

        valid_titles = 0
        for i, title in enumerate(titulos, 1):
            title_chars = len(title)
            is_valid = (
                self.TITLE_MIN_CHARS <= title_chars <= self.TITLE_MAX_CHARS
            )

            title_info = {
                "number": i,
                "chars": title_chars,
                "valid": is_valid,
                "text": title[:40] + "..." if len(title) > 40 else title
            }

            if not is_valid:
                if title_chars < self.TITLE_MIN_CHARS:
                    diff = self.TITLE_MIN_CHARS - title_chars
                    score.issues.append(
                        f"Title {i}: {title_chars} chars (need +{diff})"
                    )
                else:
                    diff = title_chars - self.TITLE_MAX_CHARS
                    score.issues.append(
                        f"Title {i}: {title_chars} chars (need -{diff})"
                    )
            else:
                valid_titles += 1

            score.details["titles"].append(title_info)

        # Calculate score: 0-10 scale
        # Base: validity of character counts (0-5)
        # Bonus: having all 3 titles (0-5)
        char_validity = (valid_titles / len(titulos)) * 5 if titulos else 0
        count_bonus = 5.0 if len(titulos) == self.TITLE_COUNT else 2.5
        score.score = char_validity + count_bonus

        # Determine status
        if valid_titles == self.TITLE_COUNT and len(titulos) == self.TITLE_COUNT:
            score.status = "PASS"
        elif valid_titles >= 2:
            score.status = "WARN"
        else:
            score.status = "FAIL"

        score.details["valid_count"] = valid_titles
        score.details["total_count"] = len(titulos)

        return score

    def _validate_keywords(
        self,
        keywords_block_1: str,
        keywords_block_2: str
    ) -> ComponentScore:
        """Validate keywords dimension (60+ unique, 115-120 per block)."""
        score = ComponentScore(
            name="keywords",
            score=0.0,
            max_score=10.0,
            status="FAIL",
            details={"blocks": {}},
            issues=[]
        )

        # Parse keywords
        block_1_terms = self._parse_keywords(keywords_block_1)
        block_2_terms = self._parse_keywords(keywords_block_2)

        # Validate each block
        block_statuses = []
        for i, terms in enumerate([block_1_terms, block_2_terms], 1):
            block_num = f"block_{i}"
            count = len(terms)
            is_valid = (
                self.KEYWORDS_BLOCK_MIN <= count <= self.KEYWORDS_BLOCK_MAX
            )

            block_info = {
                "count": count,
                "valid": is_valid
            }

            if not is_valid:
                if count < self.KEYWORDS_BLOCK_MIN:
                    diff = self.KEYWORDS_BLOCK_MIN - count
                    score.issues.append(
                        f"Keywords block {i}: {count} terms (need +{diff})"
                    )
                else:
                    diff = count - self.KEYWORDS_BLOCK_MAX
                    score.issues.append(
                        f"Keywords block {i}: {count} terms (need -{diff})"
                    )

            block_statuses.append(is_valid)
            score.details["blocks"][block_num] = block_info

        # Check for unique keywords
        all_terms = set(block_1_terms + block_2_terms)
        unique_count = len(all_terms)
        score.details["unique_count"] = unique_count
        score.details["total_count"] = len(block_1_terms) + len(block_2_terms)

        if unique_count < self.KEYWORDS_MIN_UNIQUE:
            diff = self.KEYWORDS_MIN_UNIQUE - unique_count
            score.issues.append(
                f"Unique keywords: {unique_count} (need +{diff})"
            )

        # Calculate score: 0-10
        # Block validity: 0-5
        # Unique count: 0-5
        block_score = 5.0 if all(block_statuses) else 2.5
        unique_score = (unique_count / self.KEYWORDS_MIN_UNIQUE) * 5
        unique_score = min(unique_score, 5.0)
        score.score = block_score + unique_score

        # Determine status
        if all(block_statuses) and unique_count >= self.KEYWORDS_MIN_UNIQUE:
            score.status = "PASS"
        elif all(block_statuses):
            score.status = "WARN"
        else:
            score.status = "FAIL"

        return score

    def _validate_descricao(self, descricao: str) -> ComponentScore:
        """Validate description (3300+ chars with StoryBrand elements)."""
        score = ComponentScore(
            name="descricao",
            score=0.0,
            max_score=10.0,
            status="FAIL",
            details={},
            issues=[]
        )

        chars = len(descricao)
        is_length_valid = chars >= self.DESCRIPTION_MIN_CHARS

        # Check for StoryBrand elements
        storybrand = {
            "problem": bool(
                re.search(r'(problema|dor|dificuldade|sofre)',
                         descricao, re.IGNORECASE)
            ),
            "solution": bool(
                re.search(r'(solução|resolve|soluciona)',
                         descricao, re.IGNORECASE)
            ),
            "success": bool(
                re.search(r'(resultado|sucesso|conquista|alcança)',
                         descricao, re.IGNORECASE)
            ),
            "cta": bool(
                re.search(r'(compre|adquira|garanta|peça|clique)',
                         descricao, re.IGNORECASE)
            )
        }

        storybrand_elements = sum(storybrand.values())

        score.details["chars"] = chars
        score.details["length_valid"] = is_length_valid
        score.details["storybrand"] = storybrand
        score.details["storybrand_elements"] = storybrand_elements

        if not is_length_valid:
            diff = self.DESCRIPTION_MIN_CHARS - chars
            score.issues.append(
                f"Description: {chars} chars (need +{diff})"
            )

        missing_elements = [
            k for k, v in storybrand.items() if not v
        ]
        if missing_elements:
            score.issues.append(
                f"Missing StoryBrand elements: {', '.join(missing_elements)}"
            )

        # Calculate score: 0-10
        # Length compliance: 0-5
        # StoryBrand elements: 0-5
        length_score = 5.0 if is_length_valid else (chars / self.DESCRIPTION_MIN_CHARS) * 5
        storybrand_score = (storybrand_elements / 4) * 5
        score.score = length_score + storybrand_score

        # Determine status
        if is_length_valid and storybrand_elements >= 3:
            score.status = "PASS"
        elif is_length_valid or storybrand_elements >= 3:
            score.status = "WARN"
        else:
            score.status = "FAIL"

        return score

    def _validate_bullets(self, bullets: List[str]) -> ComponentScore:
        """Validate bullets (10 items, 250-299 chars each)."""
        score = ComponentScore(
            name="bullets",
            score=0.0,
            max_score=10.0,
            status="FAIL",
            details={"bullets": []},
            issues=[]
        )

        # Check count
        if len(bullets) != self.BULLET_COUNT:
            score.issues.append(
                f"Expected {self.BULLET_COUNT} bullets, got {len(bullets)}"
            )

        valid_bullets = 0
        for i, bullet in enumerate(bullets, 1):
            chars = len(bullet)
            is_valid = (
                self.BULLET_MIN_CHARS <= chars <= self.BULLET_MAX_CHARS
            )

            bullet_info = {
                "number": i,
                "chars": chars,
                "valid": is_valid,
                "text": bullet[:40] + "..." if len(bullet) > 40 else bullet
            }

            if not is_valid:
                if chars < self.BULLET_MIN_CHARS:
                    diff = self.BULLET_MIN_CHARS - chars
                    score.issues.append(
                        f"Bullet {i}: {chars} chars (need +{diff})"
                    )
                else:
                    diff = chars - self.BULLET_MAX_CHARS
                    score.issues.append(
                        f"Bullet {i}: {chars} chars (need -{diff})"
                    )
            else:
                valid_bullets += 1

            score.details["bullets"].append(bullet_info)

        # Calculate score: 0-10
        # Count validity: 0-5
        # Character validity: 0-5
        count_score = 5.0 if len(bullets) == self.BULLET_COUNT else 2.5
        char_score = (valid_bullets / len(bullets)) * 5 if bullets else 0
        score.score = count_score + char_score

        # Determine status
        if valid_bullets == self.BULLET_COUNT and len(bullets) == self.BULLET_COUNT:
            score.status = "PASS"
        elif valid_bullets >= 8:
            score.status = "WARN"
        else:
            score.status = "FAIL"

        score.details["valid_count"] = valid_bullets
        score.details["total_count"] = len(bullets)

        return score

    def _validate_compliance(
        self,
        titulos: List[str],
        descricao: str,
        keywords_1: str,
        keywords_2: str,
        bullets: List[str]
    ) -> ComponentScore:
        """Validate compliance (no HTML, emojis, prohibited claims)."""
        score = ComponentScore(
            name="compliance",
            score=0.0,
            max_score=10.0,
            status="FAIL",
            details={},
            issues=[]
        )

        # Combine all text
        full_text = " ".join(titulos) + " " + descricao + " " + keywords_1 + " " + keywords_2 + " " + " ".join(bullets)

        # Check for HTML/CSS/JS
        has_html = bool(re.search(r'<[^>]+>', full_text))
        if has_html:
            score.issues.append("HTML/CSS/JS tags detected")

        # Check for emojis
        emoji_pattern = r'[\U0001F300-\U0001F9FF\U00002600-\U000027BF]'
        has_emoji = bool(re.search(emoji_pattern, full_text))
        if has_emoji:
            score.issues.append("Emoji characters detected")

        # Check for prohibited claims
        prohibited_patterns = {
            "number_1": r'#\s*1\b',
            "best_in_brazil": r'melhor\s+do\s+brasil',
            "market_leader": r'líder\s+de\s+mercado',
            "cure": r'cura\b',
            "miracle": r'milagr'
        }

        prohibited_found = []
        for pattern_name, pattern in prohibited_patterns.items():
            if re.search(pattern, full_text, re.IGNORECASE):
                prohibited_found.append(pattern_name)
                score.issues.append(f"Prohibited claim: {pattern_name}")

        # Check for external links
        has_links = bool(re.search(r'https?://|www\.', full_text))
        if has_links:
            score.issues.append("External links detected")

        # Calculate score: 0-10
        compliance_checks = [
            (not has_html, "html"),
            (not has_emoji, "emoji"),
            (not prohibited_found, "prohibited_claims"),
            (not has_links, "links")
        ]

        passed = sum(1 for check, _ in compliance_checks if check)
        score.score = (passed / len(compliance_checks)) * 10.0

        score.details = {
            "html": {"found": has_html},
            "emoji": {"found": has_emoji},
            "prohibited_claims": {"found": len(prohibited_found) > 0},
            "external_links": {"found": has_links}
        }

        # Determine status
        if score.score == 10.0:
            score.status = "PASS"
        elif score.score >= 7.5:
            score.status = "WARN"
        else:
            score.status = "FAIL"

        return score

    # =========================================================================
    # HELPER METHODS
    # =========================================================================

    def _parse_keywords(self, keywords_text: str) -> List[str]:
        """Parse comma-separated keywords, clean and deduplicate."""
        terms = [
            k.strip().lower()
            for k in keywords_text.split(',')
            if k.strip()
        ]
        return terms

    def _calculate_overall_score(self) -> None:
        """Calculate weighted overall score (0-10)."""
        total_score = 0.0

        for dimension, weight in self.WEIGHTS.items():
            if dimension in self.report.component_scores:
                component = self.report.component_scores[dimension]
                # Normalize component score from 0-10 to 0-1
                normalized = component.score / 10.0
                total_score += normalized * weight

        # Convert back to 0-10 scale
        self.report.overall_score = total_score * 10.0

    def _determine_status(self, strict_mode: bool = False) -> None:
        """Determine overall validation status."""
        # Count issues
        self.report.total_issues = sum(
            len(score.issues)
            for score in self.report.component_scores.values()
        )

        if strict_mode:
            # Strict: any issue = FAIL
            if self.report.total_issues == 0:
                self.report.status = "PASS"
            else:
                self.report.status = "FAIL"
        else:
            # Lenient: score-based
            if self.report.overall_score >= self.PASS_THRESHOLD:
                self.report.status = "PASS"
            elif self.report.overall_score >= self.WARN_THRESHOLD:
                self.report.status = "WARN"
            else:
                self.report.status = "FAIL"

    def _generate_recommendations(self) -> None:
        """Generate improvement recommendations based on issues."""
        recommendations = []

        for dimension, score in self.report.component_scores.items():
            if score.status != "PASS":
                if dimension == "titulos":
                    recommendations.append(
                        "Adjust titles to exactly 58-60 characters each"
                    )
                elif dimension == "keywords":
                    recommendations.append(
                        "Add more unique keywords or adjust block sizes to 115-120 terms"
                    )
                elif dimension == "descricao":
                    recommendations.append(
                        "Expand description to 3300+ chars and include StoryBrand elements"
                    )
                elif dimension == "bullets":
                    recommendations.append(
                        "Ensure all 10 bullets are 250-299 characters each"
                    )
                elif dimension == "compliance":
                    recommendations.append(
                        "Remove HTML, emojis, prohibited claims, and external links"
                    )

        self.report.recommendations = recommendations


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def validate_anuncio(
    titulos: List[str],
    descricao: str,
    keywords_block_1: str,
    keywords_block_2: str,
    bullets: List[str],
    strict_mode: bool = False
) -> Dict[str, Any]:
    """
    Convenience function to validate an anúncio and return JSON.

    Args:
        titulos: List of 3 title variations
        descricao: Long-form description
        keywords_block_1: Comma-separated keywords
        keywords_block_2: Comma-separated keywords
        bullets: List of 10 bullet points
        strict_mode: Strict validation (any issue = FAIL)

    Returns:
        Dictionary with validation report (JSON-serializable)
    """
    validator = AnuncioValidator()
    report = validator.validate(
        titulos=titulos,
        descricao=descricao,
        keywords_block_1=keywords_block_1,
        keywords_block_2=keywords_block_2,
        bullets=bullets,
        strict_mode=strict_mode
    )
    return report.to_dict()


# =============================================================================
# EXAMPLE / TEST
# =============================================================================

if __name__ == "__main__":
    # Example usage
    validator = AnuncioValidator()

    # Sample data
    sample_titulos = [
        "Whey Protein Premium 1kg - Ganho Muscular Rápido e Seguro",  # 58 chars
        "Proteína Concentrada 1kg - Potência Máxima para Atletas",    # 56 chars (short)
        "Whey Isolado 1kg - Absorção Rápida Pós-Treino Garantido"     # 57 chars (short)
    ]

    sample_descricao = "Nossa proteína whey premium é a escolha definitiva para atletas sérios. " * 60  # ~4200 chars

    sample_keywords_1 = ", ".join([f"keyword{i}" for i in range(115)])
    sample_keywords_2 = ", ".join([f"termo{i}" for i in range(115)])

    sample_bullets = [
        "Primeiro ponto importante " * 10,  # ~260 chars
        "Segundo ponto importante " * 10,
        "Terceiro ponto importante " * 10,
        "Quarto ponto importante " * 10,
        "Quinto ponto importante " * 10,
        "Sexto ponto importante " * 10,
        "Sétimo ponto importante " * 10,
        "Oitavo ponto importante " * 10,
        "Nono ponto importante " * 10,
        "Décimo ponto importante " * 10,
    ]

    # Validate
    report = validator.validate(
        titulos=sample_titulos,
        descricao=sample_descricao,
        keywords_block_1=sample_keywords_1,
        keywords_block_2=sample_keywords_2,
        bullets=sample_bullets
    )

    # Print results
    print("=== ANUNCIO VALIDATION REPORT ===")
    print(report.to_json())
