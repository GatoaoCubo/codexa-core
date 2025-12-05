"""
Gerador de Imagens - Garrafa Termica Inox Gato
Usa Google Imagen 4.0 para gerar 9 imagens profissionais
"""

import os
import json
from datetime import datetime
from pathlib import Path

# Verificar se a API key existe
api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    # Tentar carregar do .env
    env_path = Path(__file__).parent.parent.parent.parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                if line.startswith("GOOGLE_API_KEY=") or line.startswith("GEMINI_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break

if not api_key:
    print("[ERRO] GOOGLE_API_KEY nao encontrada!")
    print("Configure a variavel de ambiente ou adicione no .env")
    exit(1)

print(f"[OK] API Key encontrada: {api_key[:10]}...")

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("[ERRO] Pacote google-genai nao instalado!")
    print("Execute: pip install google-genai")
    exit(1)

# Configurar cliente
client = genai.Client(api_key=api_key)

# Diretorio de saida
OUTPUT_DIR = Path(__file__).parent / "imagens_geradas"
OUTPUT_DIR.mkdir(exist_ok=True)

# Prompts otimizados para Imagen (mais curtos e diretos)
PROMPTS = {
    "01_HERO_WHITE": """Professional product photography, stainless steel thermal bottle with cat ear design lid in metallic blue finish, centered on pure white background, soft studio lighting with rim light highlighting metallic edges, sharp focus, 8K quality commercial photography, no text no logos""",

    "02_HERO_GRADIENT": """Professional product photography, metallic blue stainless steel thermal bottle with cat ear lid, three-quarter angle view, soft blue to white gradient background, premium studio lighting with controlled reflections on inox surface, sharp focus, commercial quality""",

    "03_SCALE_HAND": """Lifestyle photography, feminine hand holding metallic blue stainless steel thermal bottle with cat ears lid, neutral background with soft bokeh, natural window lighting, showing ergonomic grip and 500ml size scale, candid feel, sharp focus""",

    "04_LIFESTYLE_DESK": """Lifestyle photography, metallic blue thermal bottle with cat ears on modern minimalist desk, laptop and small plant nearby, clean office environment, natural window light, work-from-home aesthetic, shallow depth of field""",

    "05_LIFESTYLE_GYM": """Lifestyle photography, metallic blue stainless steel cat bottle on gym workout bench, white towel and dumbbells blurred in background, modern fitness center, active lifestyle context, shallow depth of field""",

    "06_LIFESTYLE_OUTDOOR": """Lifestyle photography, metallic blue thermal bottle with cat ears in outdoor park during golden hour, natural wood bench, green trees in soft bokeh background, warm sunlight creating rim light on metallic surface, serene nature aesthetic""",

    "07_DETAIL_EARS": """Macro photography, extreme close-up of cat ear design on thermal bottle lid in metallic blue, sculptural detail of ears, soft neutral background blur, controlled lighting revealing metallic texture and premium finish, 8K detail""",

    "08_DETAIL_TEXTURE": """Macro photography, close-up of stainless steel thermal bottle body surface in metallic blue, showing brushed inox texture and premium coating, soft gradient background, controlled highlight strip on metallic surface""",

    "09_SOCIAL_FLATLAY": """Flat lay photography, metallic blue thermal bottle with cat ears as hero element on pure white background, arranged with sunglasses and wireless earbuds, overhead 90-degree angle, Instagram aesthetic, clean social media style, sharp focus throughout"""
}

# Log de geracao
generation_log = {
    "product": "Garrafa Termica Inox Gato Azul",
    "generated_at": datetime.now().isoformat(),
    "model": "imagen-4.0-generate-001",
    "results": []
}

print(f"\n{'='*60}")
print("GERANDO 9 IMAGENS COM GOOGLE IMAGEN 4.0")
print(f"{'='*60}\n")

for i, (scene_name, prompt) in enumerate(PROMPTS.items(), 1):
    print(f"[{i}/9] Gerando {scene_name}...")

    try:
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="4:3",
            )
        )

        if response.generated_images:
            image_data = response.generated_images[0].image.image_bytes
            filename = f"{scene_name}_{datetime.now().strftime('%H%M%S')}.png"
            filepath = OUTPUT_DIR / filename

            with open(filepath, 'wb') as f:
                f.write(image_data)

            file_size = filepath.stat().st_size / 1024  # KB
            print(f"      [OK] Salvo: {filename} ({file_size:.1f} KB)")

            generation_log["results"].append({
                "scene": scene_name,
                "filename": filename,
                "size_kb": round(file_size, 1),
                "status": "success"
            })
        else:
            print(f"      [WARN] Nenhuma imagem gerada")
            generation_log["results"].append({
                "scene": scene_name,
                "status": "no_image"
            })

    except Exception as e:
        print(f"      [ERRO] {str(e)[:100]}")
        generation_log["results"].append({
            "scene": scene_name,
            "status": "error",
            "error": str(e)[:200]
        })

# Salvar log
log_path = OUTPUT_DIR / "generation_log.json"
with open(log_path, 'w', encoding='utf-8') as f:
    json.dump(generation_log, f, indent=2, ensure_ascii=False)

# Resumo
success_count = sum(1 for r in generation_log["results"] if r["status"] == "success")
print(f"\n{'='*60}")
print(f"RESULTADO: {success_count}/9 imagens geradas com sucesso")
print(f"Diretorio: {OUTPUT_DIR}")
print(f"Log: {log_path}")
print(f"{'='*60}\n")
