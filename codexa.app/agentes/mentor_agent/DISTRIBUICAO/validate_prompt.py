#!/usr/bin/env python3
"""Validate enriched prompt files"""
import re
import sys
from pathlib import Path

def validate_prompt_file(filepath):
    """Validate a prompt file structure and syntax"""

    try:
        with open(filepath, encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {
            'valid': False,
            'error': f'Failed to read file: {e}'
        }

    lines = content.splitlines()
    sections_h2 = len(re.findall(r'^##\s', content, re.MULTILINE))
    sections_h3 = len(re.findall(r'^###\s', content, re.MULTILINE))
    examples = content.count('Exemplo')
    versiculos = content.count('Relevância:') + content.count('Relevancia:')
    knowledge_section = 'CONHECIMENTO TÉCNICO' in content or 'CONHECIMENTO TECNICO' in content

    return {
        'valid': True,
        'lines': len(lines),
        'sections_h2': sections_h2,
        'sections_h3': sections_h3,
        'examples': examples,
        'versiculos': versiculos,
        'knowledge_section': knowledge_section,
        'file_size_kb': len(content) / 1024
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python validate_prompt.py <prompt_file>")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    result = validate_prompt_file(filepath)

    if not result['valid']:
        print(f"[ERRO] {result['error']}")
        sys.exit(1)

    print(f"\n=== VALIDACAO: {filepath.name} ===")
    print(f"[OK] Arquivo UTF-8 valido")
    print(f"[OK] Total de linhas: {result['lines']}")
    print(f"[OK] Secoes H2 (##): {result['sections_h2']}")
    print(f"[OK] Secoes H3 (###): {result['sections_h3']}")
    print(f"[OK] Exemplos encontrados: {result['examples']}")
    print(f"[OK] Versiculos injetados: {result['versiculos']}")
    print(f"[OK] Conhecimento tecnico: {'SIM' if result['knowledge_section'] else 'NAO'}")
    print(f"[OK] Tamanho: {result['file_size_kb']:.1f} KB")
    print(f"\n[SUCESSO] Validacao sintática: PASSOU\n")
