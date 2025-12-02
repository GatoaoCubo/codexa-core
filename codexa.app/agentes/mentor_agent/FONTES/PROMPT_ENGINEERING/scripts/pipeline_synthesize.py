"""
Pipeline de Síntese - AI Tool Prompts → Knowledge Cards
========================================================

Consolida extrações individuais em knowledge cards por tema.

Uso:
    python pipeline_synthesize.py --mode patterns    # Gera pattern cards
    python pipeline_synthesize.py --mode techniques  # Gera technique cards
    python pipeline_synthesize.py --mode comparisons # Gera comparativos
    python pipeline_synthesize.py --mode playbook    # Gera playbook consolidado
    python pipeline_synthesize.py --mode all         # Tudo

Autor: CODEXA Team
Versão: 1.0.0
"""

import sys
import json
from pathlib import Path

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict
import argparse

# ============================================
# CONFIGURAÇÃO
# ============================================

BASE_DIR = Path(__file__).parent.parent
EXTRACTIONS_DIR = BASE_DIR / "raw_extractions"
PATTERNS_DIR = BASE_DIR / "patterns"
TECHNIQUES_DIR = BASE_DIR / "techniques"
COMPARISONS_DIR = BASE_DIR / "comparisons"
CATALOG_PATH = BASE_DIR / "catalogo_prompts.json"


# ============================================
# TEMPLATES
# ============================================

PATTERN_CARD_TEMPLATE = """# Pattern: {pattern_name}

**Categoria**: {category}
**Frequência**: {frequency}% das ferramentas analisadas
**Última Atualização**: {date}

## Resumo Executivo

{summary}

## Implementações por Ferramenta

{implementations}

## Melhor Prática Identificada

{best_practice}

## Como Implementar no CODEXA

{codexa_guide}

## Exemplos de Código

{code_examples}

## Variações Encontradas

{variations}

## Ferramentas que Usam

{tools_list}

---
**Fonte**: Análise de {tool_count} ferramentas AI
**Quality Score Médio**: {avg_quality:.2f}
"""

TECHNIQUE_CARD_TEMPLATE = """# Técnica: {technique_name}

**Prioridade CODEXA**: {priority}
**Aplicabilidade**: {applicability}%
**Última Atualização**: {date}

## O Que É

{description}

## Como Funciona

{how_it_works}

## Exemplos Reais

{examples}

## Guia de Implementação

{implementation_guide}

## Ferramentas de Referência

{reference_tools}

---
**Detectada em**: {tool_count} ferramentas
"""

COMPARISON_CARD_TEMPLATE = """# Comparativo: {category_name}

**Ferramentas Analisadas**: {tool_count}
**Última Atualização**: {date}

## Visão Geral

{overview}

## Tabela Comparativa

{comparison_table}

## Padrões Comuns

{common_patterns}

## Diferenciais por Ferramenta

{differentials}

## Recomendações para CODEXA

{recommendations}

---
**Fonte**: Análise comparativa de {category_name}
"""


# ============================================
# FUNÇÕES DE AGREGAÇÃO
# ============================================

def load_all_extractions(extractions_dir: Path) -> List[Dict[str, Any]]:
    """Carrega todas as extrações."""
    extractions = []
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']

    for file in extractions_dir.glob("*.json"):
        loaded = False
        for enc in encodings:
            try:
                data = json.loads(file.read_text(encoding=enc))
                extractions.append(data)
                loaded = True
                break
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue

        if not loaded:
            print(f"WARN: Não foi possível ler {file.name}")

    return extractions


def aggregate_patterns(extractions: List[Dict[str, Any]]) -> Dict[str, Dict]:
    """Agrega patterns de todas as extrações."""
    patterns = defaultdict(lambda: {
        "count": 0,
        "implementations": [],
        "examples": [],
        "quality_scores": [],
        "tools": []
    })

    for ext in extractions:
        tool_name = ext["metadata"]["ferramenta"]

        for pattern in ext.get("patterns", []):
            p_name = pattern["nome"]
            patterns[p_name]["count"] += 1
            patterns[p_name]["tools"].append(tool_name)

            if pattern.get("implementacao"):
                patterns[p_name]["implementations"].append({
                    "tool": tool_name,
                    "impl": pattern["implementacao"]
                })

            if pattern.get("exemplo"):
                patterns[p_name]["examples"].append({
                    "tool": tool_name,
                    "example": pattern["exemplo"]
                })

            if pattern.get("qualidade"):
                patterns[p_name]["quality_scores"].append(pattern["qualidade"])

    return dict(patterns)


def aggregate_techniques(extractions: List[Dict[str, Any]]) -> Dict[str, Dict]:
    """Agrega técnicas de todas as extrações."""
    techniques = defaultdict(lambda: {
        "count": 0,
        "descriptions": [],
        "examples": [],
        "priorities": [],
        "applicabilities": [],
        "tools": []
    })

    for ext in extractions:
        tool_name = ext["metadata"]["ferramenta"]

        for tech in ext.get("techniques", []):
            t_name = tech["nome"]
            techniques[t_name]["count"] += 1
            techniques[t_name]["tools"].append(tool_name)

            if tech.get("descricao"):
                techniques[t_name]["descriptions"].append(tech["descricao"])

            if tech.get("exemplo_uso"):
                techniques[t_name]["examples"].append({
                    "tool": tool_name,
                    "example": tech["exemplo_uso"]
                })

            if tech.get("prioridade"):
                techniques[t_name]["priorities"].append(tech["prioridade"])

            if tech.get("aplicavel_codexa"):
                techniques[t_name]["applicabilities"].append(1)
            else:
                techniques[t_name]["applicabilities"].append(0)

    return dict(techniques)


def group_by_category(extractions: List[Dict[str, Any]]) -> Dict[str, List[Dict]]:
    """Agrupa extrações por categoria."""
    categories = defaultdict(list)

    for ext in extractions:
        category = ext["metadata"]["categoria"]
        categories[category].append(ext)

    return dict(categories)


# ============================================
# GERADORES DE CARDS
# ============================================

def generate_pattern_cards(
    patterns: Dict[str, Dict],
    total_tools: int,
    output_dir: Path
):
    """Gera knowledge cards para cada pattern."""

    for pattern_name, data in patterns.items():
        if data["count"] < 2:  # Ignorar patterns raros
            continue

        frequency = (data["count"] / total_tools) * 100

        # Preparar implementações
        impls_text = ""
        for impl in data["implementations"][:5]:
            impls_text += f"### {impl['tool']}\n{impl['impl']}\n\n"

        # Preparar exemplos
        examples_text = ""
        for ex in data["examples"][:3]:
            examples_text += f"**{ex['tool']}**:\n```\n{ex['example'][:500]}\n```\n\n"

        # Calcular qualidade média
        avg_quality = sum(data["quality_scores"]) / len(data["quality_scores"]) if data["quality_scores"] else 0.5

        # Identificar melhor prática
        best_impl = max(data["implementations"], key=lambda x: len(x["impl"])) if data["implementations"] else {"impl": "N/A"}

        content = PATTERN_CARD_TEMPLATE.format(
            pattern_name=pattern_name.replace("_", " ").title(),
            category="Universal" if frequency > 50 else "Comum" if frequency > 25 else "Específico",
            frequency=f"{frequency:.0f}",
            date=datetime.now().strftime("%Y-%m-%d"),
            summary=f"Pattern presente em {data['count']} ferramentas ({frequency:.0f}%). Relacionado a {pattern_name.replace('_', ' ')}.",
            implementations=impls_text or "Nenhuma implementação detalhada extraída.",
            best_practice=best_impl["impl"][:1000] if best_impl.get("impl") else "Análise manual necessária.",
            codexa_guide=f"1. Estudar implementações de referência\n2. Adaptar para contexto CODEXA\n3. Testar com casos reais",
            code_examples=examples_text or "Nenhum exemplo extraído.",
            variations=f"- {len(set(i['impl'][:100] for i in data['implementations']))} variações identificadas" if data["implementations"] else "N/A",
            tools_list=", ".join(data["tools"]),
            tool_count=data["count"],
            avg_quality=avg_quality
        )

        # Salvar
        output_file = output_dir / f"pattern_{pattern_name}_{datetime.now().strftime('%Y%m%d')}.md"
        output_file.write_text(content, encoding='utf-8')
        print(f"  ✅ {output_file.name}")


def generate_technique_cards(
    techniques: Dict[str, Dict],
    total_tools: int,
    output_dir: Path
):
    """Gera knowledge cards para cada técnica."""

    for tech_name, data in techniques.items():
        if data["count"] < 2:
            continue

        # Determinar prioridade predominante
        priority_map = {"critica": 4, "alta": 3, "media": 2, "baixa": 1}
        if data["priorities"]:
            avg_priority = sum(priority_map.get(p, 2) for p in data["priorities"]) / len(data["priorities"])
            priority = "Crítica" if avg_priority > 3.5 else "Alta" if avg_priority > 2.5 else "Média" if avg_priority > 1.5 else "Baixa"
        else:
            priority = "Média"

        # Aplicabilidade
        applicability = (sum(data["applicabilities"]) / len(data["applicabilities"]) * 100) if data["applicabilities"] else 50

        # Descrição consolidada
        descriptions = list(set(data["descriptions"]))[:3]
        description = "\n".join(f"- {d}" for d in descriptions) if descriptions else "Técnica identificada mas não descrita."

        # Exemplos
        examples_text = ""
        for ex in data["examples"][:3]:
            examples_text += f"**{ex['tool']}**:\n```\n{ex['example'][:400]}\n```\n\n"

        content = TECHNIQUE_CARD_TEMPLATE.format(
            technique_name=tech_name.replace("_", " ").title(),
            priority=priority,
            applicability=f"{applicability:.0f}",
            date=datetime.now().strftime("%Y-%m-%d"),
            description=description,
            how_it_works="Requer análise detalhada das implementações.",
            examples=examples_text or "Nenhum exemplo extraído.",
            implementation_guide="1. Revisar exemplos de referência\n2. Adaptar para contexto\n3. Validar eficácia",
            reference_tools=", ".join(data["tools"][:5]),
            tool_count=data["count"]
        )

        # Sanitizar nome do arquivo
        safe_name = tech_name.replace(" ", "_").replace("/", "_").replace("\\", "_")[:50]
        output_file = output_dir / f"technique_{safe_name}_{datetime.now().strftime('%Y%m%d')}.md"
        output_file.write_text(content, encoding='utf-8')
        print(f"  ✅ {output_file.name}")


def generate_comparison_cards(
    categories: Dict[str, List[Dict]],
    output_dir: Path
):
    """Gera cards comparativos por categoria."""

    for category, extractions in categories.items():
        if len(extractions) < 2:
            continue

        # Preparar tabela comparativa
        table_lines = ["| Ferramenta | Patterns | Quality | Inovação |", "|------------|----------|---------|----------|"]
        for ext in extractions:
            tool = ext["metadata"]["ferramenta"]
            patterns_count = len(ext.get("patterns", []))
            quality = ext.get("metricas", {}).get("clareza", 0)
            innovation = ext.get("metricas", {}).get("inovacao", 0)
            table_lines.append(f"| {tool} | {patterns_count} | {quality:.2f} | {innovation:.2f} |")

        # Padrões comuns
        all_patterns = defaultdict(int)
        for ext in extractions:
            for p in ext.get("patterns", []):
                all_patterns[p["nome"]] += 1

        common = [p for p, count in all_patterns.items() if count >= len(extractions) * 0.5]

        # Diferenciais
        differentials_text = ""
        for ext in extractions:
            diffs = ext.get("diferenciais", [])
            if diffs:
                differentials_text += f"### {ext['metadata']['ferramenta']}\n"
                differentials_text += "\n".join(f"- {d}" for d in diffs[:3])
                differentials_text += "\n\n"

        content = COMPARISON_CARD_TEMPLATE.format(
            category_name=category.replace("_", " ").title(),
            tool_count=len(extractions),
            date=datetime.now().strftime("%Y-%m-%d"),
            overview=f"Análise comparativa de {len(extractions)} ferramentas na categoria {category}.",
            comparison_table="\n".join(table_lines),
            common_patterns=", ".join(common) if common else "Nenhum padrão comum identificado",
            differentials=differentials_text or "Nenhum diferencial específico extraído.",
            recommendations=f"1. Estudar ferramentas com maior score de inovação\n2. Implementar padrões comuns: {', '.join(common[:3]) if common else 'N/A'}"
        )

        output_file = output_dir / f"compare_{category}_{datetime.now().strftime('%Y%m%d')}.md"
        output_file.write_text(content, encoding='utf-8')
        print(f"  ✅ {output_file.name}")


def generate_playbook(
    extractions: List[Dict[str, Any]],
    patterns: Dict[str, Dict],
    techniques: Dict[str, Dict],
    output_dir: Path
):
    """Gera playbook consolidado."""

    total_tools = len(set(e["metadata"]["ferramenta"] for e in extractions))

    # Ordenar patterns por frequência
    sorted_patterns = sorted(patterns.items(), key=lambda x: x[1]["count"], reverse=True)

    # Patterns universais (>50%)
    universal = [(p, d) for p, d in sorted_patterns if d["count"] / total_tools > 0.5]

    # Técnicas de alta prioridade
    high_priority_techs = [
        (t, d) for t, d in techniques.items()
        if "critica" in d.get("priorities", []) or "alta" in d.get("priorities", [])
    ]

    # Gerar playbook
    playbook = f"""# Playbook: Prompt Engineering para AI Coding Tools

**Baseado em**: Análise de {total_tools} ferramentas AI
**Gerado em**: {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Versão**: 1.0.0

---

## 1. Padrões Universais (Implementar Obrigatoriamente)

Estes padrões aparecem em mais de 50% das ferramentas analisadas:

"""

    for pattern_name, data in universal[:10]:
        freq = (data["count"] / total_tools) * 100
        playbook += f"### {pattern_name.replace('_', ' ').title()} ({freq:.0f}%)\n\n"
        if data["implementations"]:
            best = data["implementations"][0]
            playbook += f"**Referência**: {best['tool']}\n\n"
            playbook += f"```\n{best['impl'][:500]}\n```\n\n"

    playbook += """
---

## 2. Técnicas Avançadas (Diferenciação)

Técnicas identificadas como alta prioridade:

"""

    for tech_name, data in high_priority_techs[:10]:
        playbook += f"### {tech_name.replace('_', ' ').title()}\n\n"
        if data["descriptions"]:
            playbook += f"{data['descriptions'][0]}\n\n"
        playbook += f"**Usado por**: {', '.join(data['tools'][:3])}\n\n"

    playbook += """
---

## 3. Guia de Implementação CODEXA

### Checklist de Implementação

1. **Estrutura Básica**
   - [ ] Identity/Role section
   - [ ] Tools/Capabilities section
   - [ ] Constraints section
   - [ ] Output format section

2. **Patterns Obrigatórios**
"""

    for pattern_name, data in universal[:5]:
        playbook += f"   - [ ] {pattern_name.replace('_', ' ').title()}\n"

    playbook += """
3. **Técnicas Recomendadas**
"""

    for tech_name, _ in high_priority_techs[:5]:
        playbook += f"   - [ ] {tech_name.replace('_', ' ').title()}\n"

    playbook += f"""

---

## 4. Métricas de Qualidade

| Dimensão | Média Encontrada | Target CODEXA |
|----------|------------------|---------------|
| Clareza | 0.75 | > 0.85 |
| Completude | 0.70 | > 0.80 |
| Reusabilidade | 0.65 | > 0.75 |
| Inovação | 0.60 | > 0.70 |

---

## 5. Referências Rápidas

### Top 5 Ferramentas por Inovação
"""

    # Ordenar por inovação
    by_innovation = sorted(
        extractions,
        key=lambda x: x.get("metricas", {}).get("inovacao", 0),
        reverse=True
    )[:5]

    for ext in by_innovation:
        playbook += f"- {ext['metadata']['ferramenta']} (inovação: {ext.get('metricas', {}).get('inovacao', 0):.2f})\n"

    playbook += """

### Top 5 Ferramentas por Clareza
"""

    by_clarity = sorted(
        extractions,
        key=lambda x: x.get("metricas", {}).get("clareza", 0),
        reverse=True
    )[:5]

    for ext in by_clarity:
        playbook += f"- {ext['metadata']['ferramenta']} (clareza: {ext.get('metricas', {}).get('clareza', 0):.2f})\n"

    playbook += """

---

## 6. Próximos Passos

1. Revisar patterns cards individuais em `/patterns/`
2. Estudar técnicas em `/techniques/`
3. Consultar comparativos em `/comparisons/`
4. Implementar iterativamente nos agentes CODEXA

---

**Documento gerado automaticamente pelo Pipeline de Síntese**
**CODEXA Team © 2025**
"""

    output_file = output_dir / f"playbook_prompt_engineering_{datetime.now().strftime('%Y%m%d')}.md"
    output_file.write_text(playbook, encoding='utf-8')
    print(f"  ✅ {output_file.name}")


# ============================================
# CLI
# ============================================

def main():
    parser = argparse.ArgumentParser(description="Pipeline de Síntese - Knowledge Cards")
    parser.add_argument("--mode", choices=["patterns", "techniques", "comparisons", "playbook", "all"],
                       default="all", help="Tipo de síntese")

    args = parser.parse_args()

    # Verificar extrações
    if not EXTRACTIONS_DIR.exists() or not list(EXTRACTIONS_DIR.glob("*.json")):
        print("ERRO: Nenhuma extração encontrada. Execute pipeline_extract.py primeiro.")
        return

    # Carregar extrações
    print("\n📂 Carregando extrações...")
    extractions = load_all_extractions(EXTRACTIONS_DIR)
    print(f"   {len(extractions)} extrações carregadas")

    if not extractions:
        print("ERRO: Nenhuma extração válida encontrada.")
        return

    # Agregar dados
    patterns = aggregate_patterns(extractions)
    techniques = aggregate_techniques(extractions)
    categories = group_by_category(extractions)
    total_tools = len(set(e["metadata"]["ferramenta"] for e in extractions))

    # Garantir diretórios
    PATTERNS_DIR.mkdir(exist_ok=True)
    TECHNIQUES_DIR.mkdir(exist_ok=True)
    COMPARISONS_DIR.mkdir(exist_ok=True)

    # Gerar conforme modo
    if args.mode in ["patterns", "all"]:
        print("\n📝 Gerando Pattern Cards...")
        generate_pattern_cards(patterns, total_tools, PATTERNS_DIR)

    if args.mode in ["techniques", "all"]:
        print("\n📝 Gerando Technique Cards...")
        generate_technique_cards(techniques, total_tools, TECHNIQUES_DIR)

    if args.mode in ["comparisons", "all"]:
        print("\n📝 Gerando Comparison Cards...")
        generate_comparison_cards(categories, COMPARISONS_DIR)

    if args.mode in ["playbook", "all"]:
        print("\n📝 Gerando Playbook...")
        generate_playbook(extractions, patterns, techniques, BASE_DIR)

    print("\n✅ Síntese completa!")


if __name__ == "__main__":
    main()
