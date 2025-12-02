# Voice Library PT-BR | video_agent

**Version**: 1.0.0
**Purpose**: Reference guide for Portuguese (Brazilian) voice options in video narration

---

## VOZES DISPONIVEIS

### Vozes Femininas (ElevenLabs)

| Voice ID | Nome | Caracteristicas | Uso Recomendado |
|----------|------|-----------------|-----------------|
| `pMsXgVXv3BLzUgSXRplE` | **Camila** | Jovem, energetica, moderna | Moda, cosmeticos, lifestyle |
| `EXAVITQu4vr4xnSDxMaL` | **Bella** | Suave, sofisticada, premium | Luxo, joias, wellness |
| `XrExE9yKIg1WjnnlVkGX` | **Laura** | Profissional, confiavel | Tech, eletronicos, servicos |
| `nPczCjzI2devNBz1zQrb` | **Vitoria** | Calorosa, acolhedora | Casa, familia, organicos |

### Vozes Masculinas (ElevenLabs)

| Voice ID | Nome | Caracteristicas | Uso Recomendado |
|----------|------|-----------------|-----------------|
| `TX3LPaxmHKxFdv7VOQHJ` | **Rafael** | Grave, autoritativo | Automotivo, premium, financas |
| `ErXwobaYiN019PkySvjV` | **Antoni** | Dinamico, jovem | Esportes, fitness, energia |
| `VR6AewLTigWG4xSOukaG` | **Eduardo** | Equilibrado, versatil | Uso geral, neutro |
| `pNInz6obpgDQGcFmaJgB` | **Lucas** | Entusiasmado, vendedor | Promocoes, ofertas, CTA forte |

---

## AUTO-SELECAO

```python
def auto_select_voice(tom, gender_preference=None):
    voice_map = {
        "energetico": {
            "feminina": "pMsXgVXv3BLzUgSXRplE",  # Camila
            "masculina": "ErXwobaYiN019PkySvjV"   # Antoni
        },
        "sofisticado": {
            "feminina": "EXAVITQu4vr4xnSDxMaL",  # Bella
            "masculina": "TX3LPaxmHKxFdv7VOQHJ"   # Rafael
        },
        "profissional": {
            "feminina": "XrExE9yKIg1WjnnlVkGX",  # Laura
            "masculina": "VR6AewLTigWG4xSOukaG"   # Eduardo
        },
        "acolhedor": {
            "feminina": "nPczCjzI2devNBz1zQrb",  # Vitoria
            "masculina": "pNInz6obpgDQGcFmaJgB"   # Lucas
        }
    }
    gender = gender_preference or "feminina"
    return voice_map.get(tom, voice_map["energetico"])[gender]
```

---

## CONFIGURACAO

### Voice Settings Recomendados

```json
{
  "voice_id": "pMsXgVXv3BLzUgSXRplE",
  "voice_name": "Camila",
  "gender": "feminina",
  "stability": 0.5,
  "similarity_boost": 0.75,
  "style": 0.0,
  "use_speaker_boost": true
}
```

### Parametros

| Parametro | Range | Recomendado | Efeito |
|-----------|-------|-------------|--------|
| stability | 0.0-1.0 | 0.5 | Menor = mais expressivo, Maior = mais consistente |
| similarity_boost | 0.0-1.0 | 0.75 | Fidelidade a voz original |
| style | 0.0-1.0 | 0.0 | Estilizacao adicional |
| use_speaker_boost | bool | true | Melhora qualidade |

---

## EXEMPLOS POR CATEGORIA

### Tenis/Esportivo
```json
{
  "voice_id": "ErXwobaYiN019PkySvjV",
  "voice_name": "Antoni",
  "gender": "masculina",
  "exemplo": "Sinta a energia em cada passo!"
}
```

### Skincare/Premium
```json
{
  "voice_id": "EXAVITQu4vr4xnSDxMaL",
  "voice_name": "Bella",
  "gender": "feminina",
  "exemplo": "Descubra o ritual de beleza que transforma sua pele."
}
```

### Tech/Eletronicos
```json
{
  "voice_id": "XrExE9yKIg1WjnnlVkGX",
  "voice_name": "Laura",
  "gender": "feminina",
  "exemplo": "Inteligencia artificial que entende voce."
}
```

### Automotivo/Premium
```json
{
  "voice_id": "TX3LPaxmHKxFdv7VOQHJ",
  "voice_name": "Rafael",
  "gender": "masculina",
  "exemplo": "Potencia e elegancia em cada detalhe."
}
```

---

## ERROS COMUNS

- Usar voz grave masculina para produtos femininos
- Stability muito alta (>0.7) = voz robotica
- Similarity muito baixa (<0.5) = inconsistencia
- Narracao muito rapida para tom sofisticado

---

**File**: 21_voice_library_ptbr.md
**Category**: voice_configuration
**Last Updated**: 2025-11-25
