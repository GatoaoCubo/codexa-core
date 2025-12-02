# Configuracao de Vozes PT-BR para Narracao

**Categoria**: voice_configuration
**Assunto**: vozes_elevenlabs_ptbr
**Nivel**: intermediario
**Aplicacao**: quando_configurar_narracao
**Tags**: elevenlabs, tts, narracao, portugues, feminina, masculina

## RESUMO EXECUTIVO

O video_agent suporta narracao em portugues brasileiro (pt-br) com opcoes de vozes femininas e masculinas via ElevenLabs. A selecao correta da voz impacta diretamente na percepcao do produto e conexao com o publico-alvo.

## VOZES DISPONÍVEIS PT-BR

### Vozes Femininas

| Voice ID | Nome | Caracteristicas | Uso Recomendado |
|----------|------|-----------------|-----------------|
| `pMsXgVXv3BLzUgSXRplE` | **Camila** | Jovem, energetica, moderna | Moda, cosmeticos, lifestyle |
| `EXAVITQu4vr4xnSDxMaL` | **Bella** | Suave, sofisticada, premium | Luxo, joias, wellness |
| `XrExE9yKIg1WjnnlVkGX` | **Laura** | Profissional, confiavel | Tech, eletronicos, servicos |
| `nPczCjzI2devNBz1zQrb` | **Vitoria** | Calorosa, acolhedora | Casa, familia, organicos |

### Vozes Masculinas

| Voice ID | Nome | Caracteristicas | Uso Recomendado |
|----------|------|-----------------|-----------------|
| `TX3LPaxmHKxFdv7VOQHJ` | **Rafael** | Grave, autoritativo | Automotivo, premium, financas |
| `ErXwobaYiN019PkySvjV` | **Antoni** | Dinamico, jovem | Esportes, fitness, energia |
| `VR6AewLTigWG4xSOukaG` | **Eduardo** | Equilibrado, versatil | Uso geral, neutro |
| `pNInz6obpgDQGcFmaJgB` | **Lucas** | Entusiasmado, vendedor | Promocoes, ofertas, CTA forte |

## COMO APLICAR

### 1. Configuracao no Brief

```json
{
  "produto": "Nike Air Max 2024",
  "duracao": 30,
  "voice_config": {
    "voice_id": "pMsXgVXv3BLzUgSXRplE",
    "voice_name": "Camila",
    "gender": "feminina",
    "stability": 0.5,
    "similarity_boost": 0.75
  }
}
```

### 2. Selecao Automatica por Tom

```python
def auto_select_voice(tom, produto_categoria):
    """
    Selecao automatica baseada no tom do video e categoria
    """
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
    return voice_map.get(tom, voice_map["energetico"])
```

### 3. Parametros de Qualidade

```json
{
  "voice_settings": {
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0.0,
    "use_speaker_boost": true
  },
  "output_format": "mp3_44100_128",
  "model_id": "eleven_multilingual_v2"
}
```

## EXEMPLOS PRATICOS

### Exemplo 1: Video de Tenis Esportivo
**Tom**: Energetico
**Publico**: Jovens 18-35

```json
{
  "voice_id": "ErXwobaYiN019PkySvjV",
  "voice_name": "Antoni",
  "gender": "masculina",
  "narracao_exemplo": "Sinta a energia em cada passo! Nike Air Max - tecnologia que te leva mais longe."
}
```
**Resultado**: Voz dinamica que transmite movimento e energia

### Exemplo 2: Video de Skincare Premium
**Tom**: Sofisticado
**Publico**: Mulheres 25-45

```json
{
  "voice_id": "EXAVITQu4vr4xnSDxMaL",
  "voice_name": "Bella",
  "gender": "feminina",
  "narracao_exemplo": "Descubra o ritual de beleza que transforma sua pele. Lancome - a ciencia da beleza."
}
```
**Resultado**: Voz suave que transmite luxo e cuidado

### Exemplo 3: Video de Eletronico
**Tom**: Profissional
**Publico**: Geral 25-55

```json
{
  "voice_id": "XrExE9yKIg1WjnnlVkGX",
  "voice_name": "Laura",
  "gender": "feminina",
  "narracao_exemplo": "Samsung Galaxy S24 - inteligencia artificial que entende voce."
}
```
**Resultado**: Voz confiavel que transmite tecnologia

## ARMADILHAS COMUNS

- **Erro 1**: Usar voz masculina grave para produtos femininos -> Desconexao com publico
- **Erro 2**: Voz muito rapida para produtos premium -> Perde sofisticacao
- **Erro 3**: Stability muito alta (>0.7) -> Voz robotica, sem emocao
- **Erro 4**: Similarity muito baixa (<0.5) -> Voz inconsistente entre segmentos

## QUANDO USAR

- Quando criar videos com narracao em portugues brasileiro
- Quando o brief especifica genero de voz preferido
- Quando o tom do video requer voz especifica
- Quando o publico-alvo tem preferencia demografica clara

## RELACIONADO

- Ver tambem: video_modes_text_vs_clean_20251125.md
- Ver tambem: text_overlay_best_practices_20251125.md

---
**Fonte**: ElevenLabs Voice Library + CODEXA Best Practices
**Processado**: 2025-11-25
**Quality Score**: 0.92/1.0
