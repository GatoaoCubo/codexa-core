"""
Example usage scenarios for anuncio_validator module.

Demonstrates:
1. Basic validation
2. JSON export
3. Batch processing
4. Integration patterns
5. Quality gates
"""

import json
from typing import List, Dict, Any
from anuncio_validator import AnuncioValidator, validate_anuncio


# =============================================================================
# EXAMPLE 1: BASIC VALIDATION
# =============================================================================

def example_basic_validation():
    """Simple validation of a single anúncio."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic Validation")
    print("=" * 70)

    validator = AnuncioValidator()

    titulos = [
        "Whey Protein Premium 1kg - Ganho Muscular Rápido Garantido",
        "Proteína Isolada 1kg - Absorção Máxima Pós-Treino Intenso",
        "Whey Concentrado 1kg - Força e Resistência para Atletas"
    ]

    descricao = """
    Nossa proteína whey premium é a escolha definitiva para atletas sérios.
    Formulada com ingredientes de alta qualidade, oferece o melhor custo-benefício
    do mercado. Desenvolvida em laboratório certificado com rigoroso controle de qualidade.

    PROBLEMA: Muitos atletas enfrentam dificuldade em ganhar massa muscular de forma
    eficiente e segura. A maioria dos suplementos disponíveis não oferecem qualidade
    consistente ou contêm ingredientes de origem duvidosa.

    SOLUÇÃO: Nossa proteína whey resolve esse problema com 100% de ingredientes puros
    e testados. A fórmula foi desenvolvida para máxima absorção e síntese proteica.
    Cada lote passa por testes rigorosos de pureza e potência.

    SUCESSO: Atletas que usam nosso produto relatam ganho de 5-7kg de massa muscular
    em 90 dias, com melhora significativa em força e resistência. Centenas de reviews
    5 estrelas confirmam a eficácia e qualidade.

    AÇÃO: Adquira agora e comece sua transformação corporal. Garantia de satisfação
    de 30 dias ou dinheiro de volta. Compre com confiança de quem realmente se importa
    com sua saúde e performance.
    """ * 2  # Ensure 3300+ chars

    keywords_1 = ", ".join([
        "whey protein", "proteína whey", "suplemento musculação",
        "ganho muscular", "proteína concentrada", "whey isolado",
        "suplemento fitness", "proteína para treino", "musculação",
        "força atlética", "performance esportiva", "suplementação",
        "proteína pura", "whey premium", "incremento muscular",
    ] * 7)  # Repeat to reach 115+ terms

    keywords_2 = ", ".join([
        "treino de força", "hipertrofia", "recuperação muscular",
        "pré-treino", "pós-treino", "suplemento seguro",
        "qualidade premium", "composto proteico", "aminoácidos",
        "bcaa proteína", "musculação natural", "evolução física",
        "resistência atletica", "ganhos garantidos", "saúde fitness",
    ] * 7)  # Repeat to reach 115+ terms

    bullets = [
        "Proteína whey 100% concentrada com absorção rápida e eficiente para máxima síntese proteica muscular." * 3,
        "Ingredientes testados em laboratório certificado com rigoroso controle de qualidade e pureza garantida." * 3,
        "Fornece 25g de proteína por scoop com todos os aminoácidos essenciais necessários para recuperação completa." * 3,
        "Produção em instalações de classe mundial com certificações internacionais de segurança e higiene." * 3,
        "Solúvel em água fria ou leite, com sabor agradável e textura cremosa sem aglomerados ou resíduo." * 3,
        "Indicado para atletas, praticantes de musculação e pessoas que buscam aumentar ingestão proteica diária." * 3,
        "Compatível com dietas keto, paleo e vegetarianas dependendo da escolha de sabor específico selecionado." * 3,
        "Promove recuperação muscular acelerada após treinos intensos e contribui para aumento de volume muscular." * 3,
        "Mantém energia constante durante treino prolongado e acelera ganhos de força em curto prazo comprovado." * 3,
        "Garantia de satisfação com devolução integral de dinheiro em 30 dias se não ficar satisfeito com resultado." * 3,
    ]

    report = validator.validate(
        titulos=titulos,
        descricao=descricao,
        keywords_block_1=keywords_1,
        keywords_block_2=keywords_2,
        bullets=bullets
    )

    print(f"\nValidation Results:")
    print(f"Overall Score: {report.overall_score:.2f}/10.0")
    print(f"Status: {report.status}")
    print(f"Total Issues: {report.total_issues}")
    print(f"\nComponent Scores:")
    for name, score in report.component_scores.items():
        print(f"  {name.capitalize()}: {score.score:.2f}/10.0 ({score.status})")

    if report.recommendations:
        print(f"\nRecommendations:")
        for rec in report.recommendations:
            print(f"  - {rec}")


# =============================================================================
# EXAMPLE 2: JSON EXPORT
# =============================================================================

def example_json_export():
    """Export validation report as JSON."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: JSON Export")
    print("=" * 70)

    # Quick validation
    result = validate_anuncio(
        titulos=[
            "Sample Title One",
            "Sample Title Two",
            "Sample Title Three"
        ],
        descricao="X" * 3300,  # Exactly 3300 chars
        keywords_block_1=", ".join([f"term{i}" for i in range(115)]),
        keywords_block_2=", ".join([f"word{i}" for i in range(115)]),
        bullets=["Y" * 270 for _ in range(10)]  # 10 bullets, ~270 chars each
    )

    # Export as JSON
    json_str = json.dumps(result, indent=2, ensure_ascii=False)
    print("\nJSON Report (first 500 chars):")
    print(json_str[:500] + "\n...\n")

    # Pretty print summary
    print(f"Score: {result['overall_score']}/10")
    print(f"Status: {result['status']}")
    print(f"Issues: {result['total_issues']}")


# =============================================================================
# EXAMPLE 3: BATCH PROCESSING
# =============================================================================

def example_batch_processing():
    """Validate multiple anúncios in batch."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Batch Processing")
    print("=" * 70)

    products = [
        {
            "id": "PROD_001",
            "name": "Whey Protein",
            "titulos": [
                "Whey Protein 1kg - Ganho Muscular Rápido Garantido",
                "Proteína Premium - Qualidade Comprovada em Laboratório",
                "Suplemento Whey 1kg - Potência Máxima para Treino"
            ],
            "descricao": "A melhor proteína do mercado. " * 120,
            "keywords_1": ", ".join([f"term{i}" for i in range(115)]),
            "keywords_2": ", ".join([f"word{i}" for i in range(115)]),
            "bullets": ["Benefit " * 40 for _ in range(10)]
        },
        {
            "id": "PROD_002",
            "name": "BCAA Supplement",
            "titulos": [
                "BCAA Premium 500g - Força e Resistência Garantidas",
                "Aminoácidos Branqueados - Performance Atlética Máxima",
                "BCAA Concentrado - Recuperação Muscular Acelerada"
            ],
            "descricao": "Melhore seu treino. " * 180,
            "keywords_1": ", ".join([f"amino{i}" for i in range(115)]),
            "keywords_2": ", ".join([f"bcaa{i}" for i in range(115)]),
            "bullets": ["Feature " * 35 for _ in range(10)]
        }
    ]

    results = []
    validator = AnuncioValidator()

    for product in products:
        report = validator.validate(
            titulos=product['titulos'],
            descricao=product['descricao'],
            keywords_block_1=product['keywords_1'],
            keywords_block_2=product['keywords_2'],
            bullets=product['bullets']
        )

        results.append({
            "product_id": product['id'],
            "product_name": product['name'],
            "validation": report.to_dict()
        })

    print(f"\nProcessed {len(results)} products:")
    for result in results:
        print(f"  {result['product_id']} ({result['product_name']}): "
              f"{result['validation']['overall_score']:.2f}/10 - "
              f"{result['validation']['status']}")


# =============================================================================
# EXAMPLE 4: QUALITY GATE
# =============================================================================

def example_quality_gate():
    """Implement a quality gate for publication."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Quality Gate for Publication")
    print("=" * 70)

    validator = AnuncioValidator()

    # Test data: intentionally flawed
    report = validator.validate(
        titulos=["Short", "Also Short", "Still Too Short"],  # Will fail
        descricao="Short description",  # Will fail
        keywords_block_1=", ".join([f"term{i}" for i in range(115)]),
        keywords_block_2=", ".join([f"word{i}" for i in range(115)]),
        bullets=["X" * 100 for _ in range(10)]  # Too short
    )

    # Quality gate logic
    print("\nQuality Gate Evaluation:")
    print("-" * 70)

    # Gate 1: Compliance (must pass)
    compliance_score = report.component_scores['compliance'].score
    if compliance_score < 10.0:
        print("[FAIL] GATE 1 (Compliance): BLOCKED - Remove prohibited content")
    else:
        print("[PASS] GATE 1 (Compliance): PASSED")

    # Gate 2: Content completeness
    descricao_score = report.component_scores['descricao'].score
    if descricao_score < 5.0:
        print("[FAIL] GATE 2 (Content): BLOCKED - Description incomplete/too short")
    else:
        print("[PASS] GATE 2 (Content): PASSED")

    # Gate 3: Overall quality
    if report.overall_score >= 8.0:
        decision = "[PASS] APPROVED - Ready for publication"
    elif report.overall_score >= 6.0:
        decision = "[WARN] FLAGGED - Needs review before publication"
    else:
        decision = "[FAIL] REJECTED - Requires substantial revision"

    print(f"[INFO] GATE 3 (Overall Quality): {decision}")
    print(f"   Score: {report.overall_score:.2f}/10")


# =============================================================================
# EXAMPLE 5: STRICT MODE
# =============================================================================

def example_strict_mode():
    """Compare lenient vs strict validation modes."""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Strict Mode Comparison")
    print("=" * 70)

    # Data with minor issues
    titulos = [
        "Nearly Perfect Title One - Almost 58 Chars Long",  # 50 chars
        "Second Title That's Close to Requirements Here",     # 50 chars
        "Third And Final Title Here Long Enough Almost"        # 50 chars
    ]
    descricao = "X" * 3300
    keywords_1 = ", ".join([f"term{i}" for i in range(115)])
    keywords_2 = ", ".join([f"word{i}" for i in range(115)])
    bullets = ["Y" * 270 for _ in range(10)]

    validator = AnuncioValidator()

    # Lenient mode
    report_lenient = validator.validate(
        titulos=titulos,
        descricao=descricao,
        keywords_block_1=keywords_1,
        keywords_block_2=keywords_2,
        bullets=bullets,
        strict_mode=False
    )

    # Strict mode
    report_strict = validator.validate(
        titulos=titulos,
        descricao=descricao,
        keywords_block_1=keywords_1,
        keywords_block_2=keywords_2,
        bullets=bullets,
        strict_mode=True
    )

    print("\nComparison Results:")
    print(f"Lenient Mode: {report_lenient.overall_score:.2f}/10 ({report_lenient.status})")
    print(f"Strict Mode:  {report_strict.overall_score:.2f}/10 ({report_strict.status})")
    print(f"\nTotal Issues Detected: {report_lenient.total_issues}")
    print(f"  - Títulos: {len(report_lenient.component_scores['titulos'].issues)}")
    print(f"  - Keywords: {len(report_lenient.component_scores['keywords'].issues)}")
    print(f"  - Descrição: {len(report_lenient.component_scores['descricao'].issues)}")
    print(f"  - Bullets: {len(report_lenient.component_scores['bullets'].issues)}")
    print(f"  - Compliance: {len(report_lenient.component_scores['compliance'].issues)}")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("ANUNCIO VALIDATOR - EXAMPLE USAGE SCENARIOS")
    print("=" * 70)

    example_basic_validation()
    example_json_export()
    example_batch_processing()
    example_quality_gate()
    example_strict_mode()

    print("\n" + "=" * 70)
    print("All examples completed!")
    print("=" * 70 + "\n")
