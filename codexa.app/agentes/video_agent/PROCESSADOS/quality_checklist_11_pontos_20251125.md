# Checklist de Qualidade: 11 Pontos de Validacao

**Categoria**: quality_standards
**Assunto**: validacao_qualidade
**Nivel**: intermediario
**Aplicacao**: quando_validar_video
**Tags**: qualidade, checklist, validacao, 11-pontos

## RESUMO EXECUTIVO

Todo video produzido pelo video_agent passa por validacao de 11 pontos antes de ser entregue. Este checklist garante qualidade minima para uso em e-commerce e redes sociais.

## OS 11 PONTOS

### 1. Duracao (15-60s)

```python
def validate_duration(video, brief):
    actual = get_video_duration(video)
    expected = brief["duracao"]
    tolerance = expected * 0.10  # 10%

    return {
        "pass": expected - tolerance <= actual <= expected + tolerance,
        "actual": actual,
        "expected": expected,
        "tolerance": f"±{tolerance}s"
    }
```

**Criterio**: Duracao entre 15-60s, desvio maximo ±10%

### 2. Resolucao (>=1080p)

```python
def validate_resolution(video):
    width, height = get_video_dimensions(video)

    return {
        "pass": height >= 1080 or width >= 1920,
        "actual": f"{width}x{height}",
        "minimum": "1920x1080"
    }
```

**Criterio**: Minimo 1080p (1920x1080) ou equivalente

### 3. Frame Rate (>=24fps)

```python
def validate_fps(video):
    fps = get_video_fps(video)

    return {
        "pass": fps >= 24,
        "actual": fps,
        "minimum": 24
    }
```

**Criterio**: Minimo 24fps, ideal 30fps

### 4. Sincronizacao de Audio (±100ms)

```python
def validate_audio_sync(video, script):
    sync_errors = []
    for segment in script["narration"]:
        actual_start = detect_speech_start(video, segment["start"])
        drift = abs(actual_start - segment["start"])
        if drift > 0.1:  # 100ms
            sync_errors.append({
                "segment": segment["text"],
                "expected": segment["start"],
                "actual": actual_start,
                "drift_ms": drift * 1000
            })

    return {
        "pass": len(sync_errors) == 0,
        "errors": sync_errors,
        "tolerance": "±100ms"
    }
```

**Criterio**: Audio nao pode desviar mais de 100ms do timing

### 5. Text Overlays Visiveis

```python
def validate_text_visibility(video, overlays):
    issues = []
    for overlay in overlays:
        contrast = measure_text_contrast(video, overlay)
        if contrast < 4.5:  # WCAG AA
            issues.append({
                "text": overlay["text"],
                "contrast_ratio": contrast,
                "minimum": 4.5
            })

    return {
        "pass": len(issues) == 0,
        "issues": issues
    }
```

**Criterio**: Contraste minimo 4.5:1 (WCAG AA)

### 6. Brand Compliance (>=8.0/10)

```python
def validate_brand_compliance(video, brand_profile):
    scores = {
        "color_accuracy": check_colors(video, brand_profile["cores"]),
        "tone_match": check_tone(video, brand_profile["tom"]),
        "logo_placement": check_logo(video, brand_profile["logo"]),
        "typography": check_fonts(video, brand_profile["fontes"])
    }

    overall = sum(scores.values()) / len(scores)

    return {
        "pass": overall >= 8.0,
        "score": overall,
        "minimum": 8.0,
        "breakdown": scores
    }
```

**Criterio**: Score de brand compliance >= 8.0/10.0

### 7. Sem Artefatos/Glitches

```python
def validate_no_artifacts(video):
    issues = []

    # Check for common AI video artifacts
    artifacts_detected = detect_artifacts(video, types=[
        "face_distortion",
        "hand_anomaly",
        "flickering",
        "morphing_error",
        "resolution_drop",
        "color_banding"
    ])

    return {
        "pass": len(artifacts_detected) == 0,
        "issues": artifacts_detected
    }
```

**Criterio**: Zero artefatos visiveis (distorcao, flickering, morphing)

### 8. Tamanho de Arquivo (<50MB/min)

```python
def validate_file_size(video):
    size_mb = get_file_size_mb(video)
    duration_min = get_video_duration(video) / 60
    size_per_min = size_mb / duration_min

    return {
        "pass": size_per_min < 50,
        "actual_mb": size_mb,
        "per_minute": f"{size_per_min:.1f}MB/min",
        "maximum": "50MB/min"
    }
```

**Criterio**: Maximo 50MB por minuto de video

### 9. Codec H.264

```python
def validate_codec(video):
    codec = get_video_codec(video)

    return {
        "pass": codec.lower() in ["h264", "avc", "h.264"],
        "actual": codec,
        "required": "H.264"
    }
```

**Criterio**: Codec deve ser H.264 (maximo compatibilidade)

### 10. Aspect Ratio Correto

```python
def validate_aspect_ratio(video, brief):
    actual = get_aspect_ratio(video)
    expected = brief["formato"]  # "9:16", "16:9", "1:1"

    tolerance = 0.02  # 2% tolerance

    return {
        "pass": abs(actual - parse_ratio(expected)) < tolerance,
        "actual": actual,
        "expected": expected
    }
```

**Criterio**: Aspect ratio deve corresponder ao brief (9:16, 16:9, 1:1)

### 11. Metadata Completa (Trinity)

```python
def validate_metadata(output_files):
    required_files = [
        f"{base_name}.mp4",
        f"{base_name}.llm.json",
        f"{base_name}.meta.json"
    ]

    missing = [f for f in required_files if not exists(f)]

    if not missing:
        # Validate metadata content
        llm_json = load_json(f"{base_name}.llm.json")
        meta_json = load_json(f"{base_name}.meta.json")

        required_llm_fields = ["prompt_used", "shots", "platform"]
        required_meta_fields = ["duration", "resolution", "cost", "timestamp"]

        missing_llm = [f for f in required_llm_fields if f not in llm_json]
        missing_meta = [f for f in required_meta_fields if f not in meta_json]

    return {
        "pass": not missing and not missing_llm and not missing_meta,
        "files_present": not missing,
        "llm_complete": not missing_llm,
        "meta_complete": not missing_meta
    }
```

**Criterio**: Trinity output completo (.mp4, .llm.json, .meta.json)

## THRESHOLDS GLOBAIS

```json
{
  "quality_score_minimum": 7.0,
  "brand_compliance_minimum": 8.0,
  "clip_success_rate_minimum": 0.80,
  "all_11_points_required": true
}
```

## COMO APLICAR

### Validacao Completa

```python
def validate_video(video_path, brief, brand_profile=None):
    """
    Executa os 11 pontos de validacao
    """
    results = {
        "1_duration": validate_duration(video_path, brief),
        "2_resolution": validate_resolution(video_path),
        "3_fps": validate_fps(video_path),
        "4_audio_sync": validate_audio_sync(video_path, brief.get("script")),
        "5_text_visibility": validate_text_visibility(video_path, brief.get("overlays", [])),
        "6_brand_compliance": validate_brand_compliance(video_path, brand_profile) if brand_profile else {"pass": True, "score": "N/A"},
        "7_no_artifacts": validate_no_artifacts(video_path),
        "8_file_size": validate_file_size(video_path),
        "9_codec": validate_codec(video_path),
        "10_aspect_ratio": validate_aspect_ratio(video_path, brief),
        "11_metadata": validate_metadata(video_path)
    }

    passed = sum(1 for r in results.values() if r["pass"])
    overall_pass = passed == 11

    return {
        "overall_pass": overall_pass,
        "points_passed": f"{passed}/11",
        "quality_score": passed / 11 * 10,
        "results": results
    }
```

## EXEMPLO DE OUTPUT

```json
{
  "overall_pass": true,
  "points_passed": "11/11",
  "quality_score": 10.0,
  "results": {
    "1_duration": {"pass": true, "actual": 30.2, "expected": 30},
    "2_resolution": {"pass": true, "actual": "1920x1080"},
    "3_fps": {"pass": true, "actual": 30},
    "4_audio_sync": {"pass": true, "errors": []},
    "5_text_visibility": {"pass": true, "issues": []},
    "6_brand_compliance": {"pass": true, "score": 8.5},
    "7_no_artifacts": {"pass": true, "issues": []},
    "8_file_size": {"pass": true, "actual_mb": 12.5},
    "9_codec": {"pass": true, "actual": "H.264"},
    "10_aspect_ratio": {"pass": true, "actual": "9:16"},
    "11_metadata": {"pass": true, "files_present": true}
  }
}
```

## ARMADILHAS COMUNS

- **Erro 1**: Ignorar sync de audio -> Narracao dessincronizada
- **Erro 2**: Arquivo muito grande -> Upload falha em plataformas
- **Erro 3**: Codec errado -> Incompatibilidade em dispositivos
- **Erro 4**: Metadata incompleta -> Perde rastreabilidade

## QUANDO USAR

- Antes de entregar qualquer video
- Apos cada fase de producao (validacao parcial)
- Durante QA de lote de videos
- Troubleshooting de problemas

## RELACIONADO

- Ver tambem: platform_selection_guide_20251125.md
- Ver tambem: video_modes_text_vs_clean_20251125.md

---
**Fonte**: PRIME.md + validators/video_quality_validator.py
**Processado**: 2025-11-25
**Quality Score**: 0.91/1.0
