#!/usr/bin/env python3
import json
from pathlib import Path

cards_dir = Path('Cards_Conhecimento')
card_stats = []

for f in sorted(cards_dir.glob('*.json')):
    # Ignorar arquivos auxiliares
    if f.name.startswith('_') or f.name in ['ANALYSIS_ECOMMERCE_CARDS.json',
                                              'cross_references.json',
                                              'domain_indices.json',
                                              'ECOMMERCE_ENRICHMENT_REPORT.json',
                                              'knowledge_graph_d3.json']:
        continue

    try:
        # Contar linhas do arquivo
        with open(f, 'r', encoding='utf-8') as file:
            lines = len(file.readlines())

        # Obter tamanho em KB
        size_kb = f.stat().st_size / 1024

        # Carregar JSON para obter metadata
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)

        meta = data.get('consolidation_metadata', {})
        src_count = meta.get('source_cards_count', 0)
        blocks = len(data.get('knowledge_blocks', []))

        card_stats.append({
            'name': f.name,
            'lines': lines,
            'size_kb': size_kb,
            'source_cards': src_count,
            'blocks': blocks
        })
    except Exception as e:
        print(f"[ERROR] {f.name}: {e}")

# Calcular estatísticas
total_lines = sum([c['lines'] for c in card_stats])
avg_lines = total_lines / len(card_stats) if card_stats else 0
total_size = sum([c['size_kb'] for c in card_stats])
avg_size = total_size / len(card_stats) if card_stats else 0

print(f"{'='*70}")
print(f"ANÁLISE DE LINHAS DOS KNOWLEDGE CARDS")
print(f"{'='*70}\n")

print(f"Total de cards analisados: {len(card_stats)}")
print(f"Total de linhas: {total_lines:,}")
print(f"Média de linhas por card: {avg_lines:,.1f}")
print(f"Tamanho total: {total_size:,.1f} KB ({total_size/1024:.2f} MB)")
print(f"Média de tamanho por card: {avg_size:,.1f} KB")

# Estatísticas de distribuição
lines_list = [c['lines'] for c in card_stats]

if lines_list:
    min_lines = min(lines_list)
    max_lines = max(lines_list)
    median_lines = sorted(lines_list)[len(lines_list)//2]

    print(f"\n{'='*70}")
    print(f"DISTRIBUIÇÃO DE LINHAS")
    print(f"{'='*70}\n")
    print(f"Mínimo: {min_lines:,} linhas")
    print(f"Máximo: {max_lines:,} linhas")
    print(f"Mediana: {median_lines:,} linhas")
else:
    print(f"\n{'='*70}")
    print(f"DISTRIBUIÇÃO DE LINHAS")
    print(f"{'='*70}\n")
    print("Nenhum card encontrado para análise")

# Top 10 maiores cards
if card_stats:
    print(f"\n{'='*70}")
    print(f"TOP 10 MAIORES CARDS (por linhas)")
    print(f"{'='*70}\n")

    for i, card in enumerate(sorted(card_stats, key=lambda x: x['lines'], reverse=True)[:10], 1):
        print(f"{i:2d}. {card['name']:45s} {card['lines']:6,} linhas | {card['size_kb']:7.1f} KB | {card['blocks']:2d} blocos | {card['source_cards']:,} sources")

    # Top 10 menores cards
    print(f"\n{'='*70}")
    print(f"TOP 10 MENORES CARDS (por linhas)")
    print(f"{'='*70}\n")

    for i, card in enumerate(sorted(card_stats, key=lambda x: x['lines'])[:10], 1):
        print(f"{i:2d}. {card['name']:45s} {card['lines']:6,} linhas | {card['size_kb']:7.1f} KB | {card['blocks']:2d} blocos | {card['source_cards']:,} sources")

# Distribuição por faixas
print(f"\n{'='*70}")
print(f"DISTRIBUIÇÃO POR FAIXAS DE LINHAS")
print(f"{'='*70}\n")

ranges = [
    (0, 500, "0-500 linhas"),
    (500, 1000, "500-1,000 linhas"),
    (1000, 2000, "1,000-2,000 linhas"),
    (2000, 5000, "2,000-5,000 linhas"),
    (5000, 10000, "5,000-10,000 linhas"),
    (10000, float('inf'), "10,000+ linhas")
]

for min_val, max_val, label in ranges:
    count = len([c for c in card_stats if min_val <= c['lines'] < max_val])
    if count > 0:
        percentage = (count / len(card_stats)) * 100
        print(f"{label:20s}: {count:3d} cards ({percentage:5.1f}%)")

# Relação linhas vs source cards
print(f"\n{'='*70}")
print(f"EFICIÊNCIA DE CONDENSAÇÃO")
print(f"{'='*70}\n")

total_sources = sum([c['source_cards'] for c in card_stats])
print(f"Total source cards: {total_sources:,}")
print(f"Total linhas nos cards condensados: {total_lines:,}")
print(f"Ratio: {total_sources:,} source cards → {total_lines:,} linhas")
print(f"Eficiência: Cada linha representa ~{total_sources/total_lines:.1f} source cards")

print(f"\n{'='*70}\n")
