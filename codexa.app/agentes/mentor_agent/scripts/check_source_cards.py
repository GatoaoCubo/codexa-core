#!/usr/bin/env python3
import json
from pathlib import Path

cards_dir = Path('Cards_Conhecimento')
total_source = 0
cards_with_meta = []

for f in sorted(cards_dir.glob('*.json')):
    if f.name.startswith('_'):
        continue

    try:
        with open(f, 'r', encoding='utf-8') as file:
            data = json.load(file)

        meta = data.get('consolidation_metadata', {})
        src_count = meta.get('source_cards_count', 0)

        if src_count > 0:
            cards_with_meta.append((f.name, src_count))
            total_source += src_count
    except Exception as e:
        pass

print(f'Cards com source_cards_count: {len(cards_with_meta)}')
print(f'Total source cards condensados: {total_source:,}')
print(f'\nTop 10 cards por source count:')
for name, count in sorted(cards_with_meta, key=lambda x: x[1], reverse=True)[:10]:
    print(f'  {name}: {count:,} source cards')

print(f'\n{"="*60}')
print(f'RESUMO:')
print(f'  - Cards condensados: {len(cards_with_meta)}')
print(f'  - Source cards processados: {total_source:,}')
print(f'  - Ratio de condensacao: {total_source}/{len(cards_with_meta)} = {total_source/len(cards_with_meta) if len(cards_with_meta)>0 else 0:.1f}:1')
print(f'{"="*60}')
