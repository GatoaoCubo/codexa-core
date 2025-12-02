import json

km = json.load(open('knowledge_map.json', encoding='utf-8'))
mappings = km.get('mappings', [])

print('\n=== KNOWLEDGE MAP SUMMARY ===')
print(f'Total mappings: {len(mappings)}\n')

for m in mappings:
    print(f'* {m["prompt_file"]}')
    print(f'  Versiculos: {len(m.get("versiculos", []))}')
    print()
