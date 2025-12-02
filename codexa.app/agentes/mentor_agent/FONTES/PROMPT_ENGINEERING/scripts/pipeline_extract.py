"""
Pipeline de Extração de Conhecimento - AI Tool Prompts
======================================================

Processa system prompts de ferramentas AI e extrai conhecimento estruturado.

Uso:
    python pipeline_extract.py --mode full          # Processa todos
    python pipeline_extract.py --mode single --tool cursor  # Processa um
    python pipeline_extract.py --mode list          # Lista ferramentas

Dependências:
    - anthropic (Claude API)
    - json, pathlib, datetime (stdlib)

Autor: CODEXA Team
Versão: 1.0.0
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import argparse

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# ============================================
# CONFIGURAÇÃO
# ============================================

# Paths
BASE_DIR = Path(__file__).parent.parent
SOURCE_DIR = Path(__file__).parent.parent.parent.parent.parent.parent.parent / "FONTES" / "ai_tools_prompts"
OUTPUT_DIR = BASE_DIR / "raw_extractions"
CATALOG_PATH = BASE_DIR / "catalogo_prompts.json"
SCHEMA_PATH = BASE_DIR / "extraction_schema.json"

# Categorias de ferramentas
TOOL_CATEGORIES = {
    "coding_ide": ["cursor", "windsurf", "augment_code", "vscode_agent", "xcode", "trae"],
    "ai_agent": ["devin", "manus", "lovable", "same_dev", "junie", "kiro", "emergent"],
    "open_source": ["cline", "bolt", "roocode", "codex_cli", "gemini_cli", "lumo"],
    "platform": ["claude_code", "anthropic", "replit", "v0", "perplexity", "notion_ai", "gemini"],
    "enterprise": ["cluely", "codebuddy", "comet_assistant", "amp", "qoder", "orchids", "leap", "poke", "warp", "dia", "traycer", "zai_code"]
}

# Extensões suportadas
SUPPORTED_EXTENSIONS = [".txt", ".md", ".yaml", ".yml", ".json"]


# ============================================
# PROMPT PARA EXTRAÇÃO (Claude)
# ============================================

EXTRACTION_PROMPT = """Você é um especialista em prompt engineering analisando system prompts de ferramentas AI.

Analise o prompt abaixo e extraia conhecimento estruturado no formato JSON especificado.

## PROMPT A ANALISAR:
```
{prompt_content}
```

## CONTEXTO:
- Ferramenta: {tool_name}
- Arquivo: {file_name}
- Categoria provável: {category}

## OUTPUT ESPERADO (JSON):
Retorne APENAS um JSON válido seguindo este schema:

```json
{{
  "metadata": {{
    "ferramenta": "{tool_name}",
    "versao": "<extrair do conteúdo ou 'unknown'>",
    "categoria": "<coding_ide|ai_agent|open_source|platform|enterprise>",
    "modelo_base": "<extrair se mencionado ou 'unknown'>",
    "data_extracao": "{extraction_date}",
    "tokens_original": <estimativa>,
    "linhas_original": {line_count},
    "arquivo_fonte": "{file_path}"
  }},
  "estrutura": {{
    "secoes_detectadas": [
      {{
        "nome": "<nome_secao>",
        "tokens_aprox": <numero>,
        "proposito": "<o que faz>",
        "exemplo_conteudo": "<trecho max 200 chars>"
      }}
    ],
    "formatacao": {{
      "usa_xml_tags": <true|false>,
      "usa_markdown": <true|false>,
      "usa_json_schemas": <true|false>,
      "usa_typescript": <true|false>,
      "usa_exemplos": <true|false>,
      "usa_good_bad_examples": <true|false>
    }}
  }},
  "patterns": [
    {{
      "nome": "<tool_calling|agent_loop|error_handling|context_management|code_generation|code_editing|search_strategy|task_management|memory_persistence|web_search|file_operations|terminal_commands|linting_validation|security_constraints|output_formatting|communication_style|proactiveness_level|planning_mode|multi_tool_parallel|citation_format>",
      "descricao": "<o que faz>",
      "implementacao": "<como é implementado>",
      "exemplo": "<trecho relevante>",
      "qualidade": <0.0-1.0>
    }}
  ],
  "techniques": [
    {{
      "nome": "<nome da técnica>",
      "descricao": "<o que faz>",
      "como_funciona": "<explicação>",
      "exemplo_uso": "<do prompt>",
      "aplicavel_codexa": <true|false>,
      "prioridade": "<critica|alta|media|baixa>"
    }}
  ],
  "insights_codexa": [
    "<insight 1 para melhorar agentes CODEXA>",
    "<insight 2>",
    "<insight 3>"
  ],
  "diferenciais": [
    "<o que esta ferramenta faz diferente/melhor>"
  ],
  "metricas": {{
    "clareza": <0.0-1.0>,
    "completude": <0.0-1.0>,
    "reusabilidade": <0.0-1.0>,
    "inovacao": <0.0-1.0>
  }}
}}
```

## REGRAS:
1. Extraia TODOS os patterns presentes (mínimo 3, máximo 10)
2. Extraia TODAS as técnicas únicas (mínimo 2, máximo 8)
3. Forneça pelo menos 3 insights para CODEXA
4. Seja específico nos exemplos - use trechos reais do prompt
5. Avalie qualidade/métricas objetivamente
6. Retorne APENAS o JSON, sem explicações

JSON:"""


# ============================================
# FUNÇÕES DE PROCESSAMENTO
# ============================================

def discover_tools(source_dir: Path) -> Dict[str, List[Path]]:
    """Descobre todas as ferramentas e seus arquivos."""
    tools = {}

    for item in source_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            tool_name = item.name
            files = []

            # Busca arquivos na pasta da ferramenta
            for file in item.rglob("*"):
                if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS:
                    files.append(file)

            if files:
                tools[tool_name] = files

    return tools


def get_tool_category(tool_name: str) -> str:
    """Determina a categoria de uma ferramenta."""
    tool_lower = tool_name.lower().replace(" ", "_").replace("-", "_")

    for category, tools in TOOL_CATEGORIES.items():
        if tool_lower in tools or any(t in tool_lower for t in tools):
            return category

    return "enterprise"  # default


def read_prompt_file(file_path: Path) -> str:
    """Lê conteúdo de um arquivo de prompt."""
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            return file_path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue

    # Se nenhum encoding funcionar
    return file_path.read_bytes().decode('utf-8', errors='replace')


def estimate_tokens(text: str) -> int:
    """Estima tokens (aproximado: 4 chars = 1 token)."""
    return len(text) // 4


def extract_with_claude(
    prompt_content: str,
    tool_name: str,
    file_name: str,
    file_path: str,
    category: str,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """Extrai conhecimento usando Claude API."""

    try:
        import anthropic
    except ImportError:
        print("ERRO: anthropic não instalado. Execute: pip install anthropic")
        return None

    api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERRO: ANTHROPIC_API_KEY não encontrada")
        return None

    client = anthropic.Anthropic(api_key=api_key)

    # Preparar prompt
    extraction_request = EXTRACTION_PROMPT.format(
        prompt_content=prompt_content[:50000],  # Limitar tamanho
        tool_name=tool_name,
        file_name=file_name,
        file_path=file_path,
        category=category,
        extraction_date=datetime.now().strftime("%Y-%m-%d"),
        line_count=prompt_content.count('\n') + 1
    )

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[
                {"role": "user", "content": extraction_request}
            ]
        )

        # Extrair JSON da resposta
        response_text = response.content[0].text

        # Tentar encontrar JSON na resposta
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            return json.loads(json_match.group())
        else:
            print(f"WARN: Não foi possível extrair JSON para {tool_name}/{file_name}")
            return None

    except Exception as e:
        print(f"ERRO na extração Claude para {tool_name}: {e}")
        return None


def extract_without_llm(
    prompt_content: str,
    tool_name: str,
    file_name: str,
    file_path: str,
    category: str
) -> Dict[str, Any]:
    """Extração básica sem LLM (fallback)."""

    lines = prompt_content.split('\n')
    tokens = estimate_tokens(prompt_content)

    # Detectar formatação
    usa_xml = bool(re.search(r'<[a-z_]+>', prompt_content, re.IGNORECASE))
    usa_markdown = bool(re.search(r'^#+\s', prompt_content, re.MULTILINE))
    usa_json = '"type"' in prompt_content or '"properties"' in prompt_content
    usa_typescript = 'type ' in prompt_content and '=>' in prompt_content
    usa_exemplos = '<example>' in prompt_content.lower() or '```' in prompt_content

    # Detectar seções
    secoes = []
    section_patterns = [
        (r'#\s*Tools?', 'tools'),
        (r'#\s*Instructions?', 'instructions'),
        (r'<tool_calling>', 'tool_calling'),
        (r'<communication>', 'communication'),
        (r'#\s*Code', 'code_handling'),
    ]

    for pattern, nome in section_patterns:
        if re.search(pattern, prompt_content, re.IGNORECASE):
            secoes.append({
                "nome": nome,
                "tokens_aprox": 0,
                "proposito": f"Seção de {nome}",
                "exemplo_conteudo": ""
            })

    # Detectar patterns básicos
    patterns = []
    pattern_checks = [
        ('tool_calling', r'tool|function|namespace'),
        ('task_management', r'todo|task'),
        ('file_operations', r'read_file|write_file|edit'),
        ('terminal_commands', r'bash|terminal|command'),
        ('security_constraints', r'security|malware|defensive'),
    ]

    for nome, regex in pattern_checks:
        if re.search(regex, prompt_content, re.IGNORECASE):
            patterns.append({
                "nome": nome,
                "descricao": f"Padrão {nome} detectado",
                "implementacao": "Detectado via regex",
                "exemplo": "",
                "qualidade": 0.5
            })

    return {
        "metadata": {
            "ferramenta": tool_name,
            "versao": "unknown",
            "categoria": category,
            "modelo_base": "unknown",
            "data_extracao": datetime.now().strftime("%Y-%m-%d"),
            "tokens_original": tokens,
            "linhas_original": len(lines),
            "arquivo_fonte": file_path
        },
        "estrutura": {
            "secoes_detectadas": secoes,
            "formatacao": {
                "usa_xml_tags": usa_xml,
                "usa_markdown": usa_markdown,
                "usa_json_schemas": usa_json,
                "usa_typescript": usa_typescript,
                "usa_exemplos": usa_exemplos,
                "usa_good_bad_examples": '<good-example>' in prompt_content.lower()
            }
        },
        "patterns": patterns,
        "techniques": [],
        "insights_codexa": [
            "Extração básica - requer análise manual",
            f"Prompt tem {tokens} tokens",
            f"Categoria: {category}"
        ],
        "diferenciais": [],
        "metricas": {
            "clareza": 0.5,
            "completude": 0.5,
            "reusabilidade": 0.5,
            "inovacao": 0.5
        },
        "_extraction_method": "regex_fallback"
    }


def process_tool(
    tool_name: str,
    files: List[Path],
    output_dir: Path,
    use_llm: bool = True,
    api_key: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Processa todos os arquivos de uma ferramenta."""

    results = []
    category = get_tool_category(tool_name)

    for file_path in files:
        print(f"  📄 Processando: {file_path.name}")

        content = read_prompt_file(file_path)

        # Pular arquivos muito pequenos ou binários
        if len(content) < 100 or '\x00' in content:
            print(f"    ⏭️ Ignorado (muito pequeno ou binário)")
            continue

        # Extrair
        relative_path = str(file_path.relative_to(SOURCE_DIR))

        if use_llm:
            extraction = extract_with_claude(
                content, tool_name, file_path.name, relative_path, category, api_key
            )
            if extraction is None:
                extraction = extract_without_llm(
                    content, tool_name, file_path.name, relative_path, category
                )
        else:
            extraction = extract_without_llm(
                content, tool_name, file_path.name, relative_path, category
            )

        if extraction:
            # Salvar extração individual (sempre UTF-8)
            output_file = output_dir / f"{tool_name}_{file_path.stem}.json"
            output_file.write_text(json.dumps(extraction, indent=2, ensure_ascii=False), encoding='utf-8')
            print(f"    ✅ Salvo: {output_file.name}")

            results.append(extraction)

    return results


def update_catalog(catalog_path: Path, extractions: List[Dict[str, Any]]):
    """Atualiza o catálogo master com novas extrações."""

    catalog = json.loads(catalog_path.read_text(encoding='utf-8'))

    for ext in extractions:
        # Adicionar ao índice
        catalog["extractions"].append({
            "ferramenta": ext["metadata"]["ferramenta"],
            "arquivo": ext["metadata"]["arquivo_fonte"],
            "categoria": ext["metadata"]["categoria"],
            "data": ext["metadata"]["data_extracao"],
            "patterns": [p["nome"] for p in ext.get("patterns", [])],
            "metricas": ext.get("metricas", {})
        })

        # Indexar patterns
        for pattern in ext.get("patterns", []):
            pattern_name = pattern["nome"]
            if pattern_name not in catalog["patterns_index"]:
                catalog["patterns_index"][pattern_name] = []
            catalog["patterns_index"][pattern_name].append(ext["metadata"]["ferramenta"])

        # Indexar techniques
        for tech in ext.get("techniques", []):
            tech_name = tech["nome"]
            if tech_name not in catalog["techniques_index"]:
                catalog["techniques_index"][tech_name] = []
            catalog["techniques_index"][tech_name].append(ext["metadata"]["ferramenta"])

    # Atualizar stats
    catalog["stats"]["processed"] = len(catalog["extractions"])
    catalog["stats"]["last_updated"] = datetime.now().isoformat()

    # Salvar (sempre UTF-8)
    catalog_path.write_text(json.dumps(catalog, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"\n📊 Catálogo atualizado: {catalog['stats']['processed']} extrações")


# ============================================
# CLI
# ============================================

def main():
    parser = argparse.ArgumentParser(description="Pipeline de Extração de Prompts AI")
    parser.add_argument("--mode", choices=["full", "single", "list", "stats"], default="list",
                       help="Modo de operação")
    parser.add_argument("--tool", type=str, help="Nome da ferramenta (para mode=single)")
    parser.add_argument("--no-llm", action="store_true", help="Usar apenas extração regex")
    parser.add_argument("--api-key", type=str, help="Anthropic API key")

    args = parser.parse_args()

    # Verificar diretórios
    if not SOURCE_DIR.exists():
        print(f"ERRO: Diretório fonte não encontrado: {SOURCE_DIR}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Descobrir ferramentas
    tools = discover_tools(SOURCE_DIR)

    if args.mode == "list":
        print("\n📦 Ferramentas Disponíveis:\n")
        for category, category_tools in TOOL_CATEGORIES.items():
            print(f"  [{category}]")
            for tool in tools.keys():
                if tool.lower().replace("-", "_") in category_tools:
                    files = tools[tool]
                    print(f"    • {tool} ({len(files)} arquivos)")
        print(f"\n  Total: {len(tools)} ferramentas, {sum(len(f) for f in tools.values())} arquivos")

    elif args.mode == "stats":
        if CATALOG_PATH.exists():
            catalog = json.loads(CATALOG_PATH.read_text())
            print("\n📊 Estatísticas do Catálogo:\n")
            print(f"  Processados: {catalog['stats']['processed']}")
            print(f"  Pendentes: {catalog['stats']['pending']}")
            print(f"  Última atualização: {catalog['stats']['last_updated']}")
            print(f"\n  Patterns indexados: {len(catalog['patterns_index'])}")
            print(f"  Técnicas indexadas: {len(catalog['techniques_index'])}")
        else:
            print("Catálogo ainda não existe. Execute com --mode full")

    elif args.mode == "single":
        if not args.tool:
            print("ERRO: --tool é obrigatório para mode=single")
            return

        if args.tool not in tools:
            print(f"ERRO: Ferramenta '{args.tool}' não encontrada")
            return

        print(f"\n🔧 Processando: {args.tool}\n")
        results = process_tool(
            args.tool, tools[args.tool], OUTPUT_DIR,
            use_llm=not args.no_llm, api_key=args.api_key
        )

        if results:
            update_catalog(CATALOG_PATH, results)

    elif args.mode == "full":
        print(f"\n🚀 Processamento Completo: {len(tools)} ferramentas\n")

        all_results = []
        for i, (tool_name, files) in enumerate(tools.items(), 1):
            print(f"\n[{i}/{len(tools)}] 🔧 {tool_name}")
            results = process_tool(
                tool_name, files, OUTPUT_DIR,
                use_llm=not args.no_llm, api_key=args.api_key
            )
            all_results.extend(results)

        if all_results:
            update_catalog(CATALOG_PATH, all_results)

        print(f"\n✅ Completo! {len(all_results)} extrações realizadas.")


if __name__ == "__main__":
    main()
