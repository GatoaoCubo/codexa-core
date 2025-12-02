#!/usr/bin/env python3
"""Analyze current coverage and suggest next steps"""
import json
import sys
from pathlib import Path
from collections import Counter

# Add config to path for centralized path management
sys.path.insert(0, str(Path(__file__).parent.parent / 'config'))
from paths import PATH_DISTRIBUICAO, PATH_PROCESSADOS

# Load knowledge map
km_path = PATH_DISTRIBUICAO / "knowledge_map.json"
km = json.load(open(km_path, encoding='utf-8'))

# Load all CAPITULOS
processados_dir = PATH_PROCESSADOS
all_capitulos = [f.stem for f in processados_dir.glob("CAPITULO_*.md")]

print("=== STATUS ATUAL DO MAPEAMENTO ===\n")
print(f"Total de CAPITULOS existentes: {len(all_capitulos)}")
print(f"Total de mappings ativos: {len(km.get('mappings', []))}\n")

# Analyze mapped vs unmapped
mapped_capitulos = set()
for mapping in km.get('mappings', []):
    for versiculo_ref in mapping.get('versiculos', []):
        if isinstance(versiculo_ref, dict):
            capitulo = versiculo_ref.get('capitulo', '')
        else:
            capitulo = versiculo_ref.split(':')[0] if ':' in str(versiculo_ref) else ''
        if capitulo:
            mapped_capitulos.add(capitulo)

unmapped_capitulos = set(all_capitulos) - mapped_capitulos

print(f"CAPITULOS mapeados: {len(mapped_capitulos)}")
print(f"CAPITULOS NAO mapeados: {len(unmapped_capitulos)}\n")

# Analyze unmapped by theme
unmapped_by_theme = Counter()
for cap in unmapped_capitulos:
    theme = cap.replace('CAPITULO_', '').split('_')[0]
    unmapped_by_theme[theme] += 1

print("=== CAPITULOS NAO MAPEADOS POR TEMA ===\n")
for theme, count in unmapped_by_theme.most_common():
    print(f"  {theme}: {count} capitulos")
    # Show examples
    examples = [c for c in unmapped_capitulos if c.startswith(f'CAPITULO_{theme}_')][:3]
    for ex in examples:
        print(f"    - {ex}")
    if count > 3:
        print(f"    ... e mais {count - 3}")
    print()

# Analyze current prompt coverage
print("=== PROMPTS ATUAIS ===\n")
for mapping in km.get('mappings', []):
    prompt = mapping['prompt_file']
    versiculo_count = len(mapping.get('versiculos', []))
    print(f"  {prompt}: {versiculo_count} versiculos")

print("\n=== ESTRATEGIA PARA CONTINUAR ===\n")
print("OPCAO 1: CRIAR NOVOS PROMPTS")
print("  Criar prompts especificos para temas nao cobertos:")
for theme, count in unmapped_by_theme.most_common(5):
    print(f"    - {theme}_prompt.md (cobre {count} CAPITULOS)")

print("\nOPCAO 2: EXPANDIR PROMPTS EXISTENTES")
print("  Adicionar keywords aos prompts atuais para capturar mais CAPITULOS")

print("\nOPCAO 3: AJUSTAR THRESHOLD DE RELEVANCIA")
print("  Atualmente: 0.30")
print("  Reduzir para: 0.25 (mais CAPITULOS serao mapeados)")

print("\nOPCAO 4: WORKFLOW INCREMENTAL")
print("  Re-executar workflow apenas para CAPITULOS nao mapeados")
print("  Evita reprocessar os 88 ja mapeados")
