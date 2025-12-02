# Guia de Selecao de Plataforma de Video IA

**Categoria**: platform_optimization
**Assunto**: escolha_plataforma_ia
**Nivel**: intermediario
**Aplicacao**: quando_escolher_plataforma
**Tags**: runway, pika, veo3, sora2, kling, hailuo

## RESUMO EXECUTIVO

O video_agent suporta 6 plataformas de video IA. Cada uma tem forcas especificas para diferentes casos de uso. A selecao correta impacta qualidade, custo e tempo de producao.

## MATRIZ DE COMPARACAO

| Plataforma | Duracao Max | Melhor Para | Custo | Audio Nativo |
|------------|-------------|-------------|-------|--------------|
| **Runway Gen-3** | 10s | Iteracao, camera control | $0.05/s | Nao |
| **Pika 2.0** | 8s | Efeitos, transformacoes | $0.03/s | Nao |
| **Veo 3 (Google)** | 8s | Dialogo, realismo | Premium | Sim |
| **Sora 2 (OpenAI)** | 20s | Cinematografia, fisica | Premium | Sim |
| **Kling 1.6** | 5s | Custo-beneficio, humanos | $0.02/s | Nao |
| **Hailuo (MiniMax)** | 6s | VFX, velocidade | $0.025/s | Nao |

## ARVORE DE DECISAO

```
START
  |
  v
[Video tem dialogo?]
  |
  +-- SIM --> Veo 3 (audio nativo)
  |
  +-- NAO --> [Duracao > 10s?]
                |
                +-- SIM --> Sora 2 (ate 20s)
                |
                +-- NAO --> [Precisa de VFX?]
                              |
                              +-- SIM --> Pika 2.0 ou Hailuo
                              |
                              +-- NAO --> [Orcamento limitado?]
                                            |
                                            +-- SIM --> Kling 1.6
                                            |
                                            +-- NAO --> Runway Gen-3 (padrao)
```

## COMO APLICAR

### Selecao Automatica no Brief

```json
{
  "produto": "Nike Air Max",
  "duracao": 30,
  "platform_preference": "auto",
  "requirements": {
    "dialogue": false,
    "vfx_heavy": false,
    "budget_conscious": false,
    "needs_iteration": true
  }
}
```

### Logica de Auto-Selecao

```python
def select_platform(requirements):
    if requirements.get("dialogue"):
        return "veo3"
    elif requirements.get("duration", 0) > 10:
        return "sora2"
    elif requirements.get("vfx_heavy"):
        return "hailuo" if requirements.get("speed") else "pika"
    elif requirements.get("budget_conscious"):
        return "kling"
    else:
        return "runway"  # Default
```

## DETALHES POR PLATAFORMA

### Runway Gen-3 Alpha (PADRAO)

**Forcas**:
- Controle preciso de camera
- Iteracao rapida
- Qualidade consistente
- API madura

**Syntax**:
```
[camera movement]: [scene]. [additional details].
```

**Exemplo**:
```
slow dolly forward: Nike sneaker on white surface, premium lighting. Cinematic 4K quality, shallow depth of field.
```

### Pika 2.0

**Forcas**:
- Efeitos especiais (Pikadditions)
- Transformacoes (Pikaswaps)
- Preco competitivo

**Syntax**:
```
[Style] + [Subject] + [Action] + [Environment] + [Lighting] + [Camera] --camera [movement]
```

**Exemplo**:
```
Cinematic product shot, Nike Air Max floating in air, soft particles around, dark studio. Professional lighting, slow orbit --camera orbit
```

### Veo 3 (Google)

**Forcas**:
- Audio nativo (dialogo)
- Alto realismo
- Consistencia de personagens

**Syntax**:
```
[Camera]: [Scene]. [Subject]. [Action]. [Lighting]. [Style]. Character says: "[text]" (no subtitles).
```

**Exemplo**:
```
Medium shot: Modern living room. Young woman trying on Nike sneakers. She smiles and walks confidently. Warm natural light. Lifestyle aesthetic. Character says: "Finally, comfort that lasts all day" (no subtitles).
```

### Sora 2 (OpenAI)

**Forcas**:
- Duracao longa (ate 20s)
- Fisica realista
- Narrativa complexa

**Syntax**:
```
LOOK: [visual style]
CAMERA: [movement]
LIGHTING: [setup]
ACTION: [description]
```

### Kling 1.6 (Kuaishou)

**Forcas**:
- Menor custo
- Bom com humanos
- 60fps opcao

**Syntax**:
```
[Subject], [description], [movement], [scene]. [Camera, lighting].
```

### Hailuo (MiniMax)

**Forcas**:
- Geracao rapida
- Bom para VFX
- Marcadores de enfase

**Syntax**:
```
[Camera] + ((elemento prioritario)) + [Subject] + [Action] + [Scene] + [Lighting]
```

## EXEMPLOS PRATICOS

### Exemplo 1: Video de Produto Simples
**Escolha**: Runway Gen-3
**Motivo**: Padrao, bom para iteracao, camera control

```json
{
  "platform": "runway",
  "shots": 6,
  "duration_per_shot": 5,
  "estimated_cost": "$1.50"
}
```

### Exemplo 2: Video com Pessoa Falando
**Escolha**: Veo 3
**Motivo**: Unica plataforma com audio nativo

```json
{
  "platform": "veo3",
  "dialogue": true,
  "audio_native": true,
  "estimated_cost": "$3.00"
}
```

### Exemplo 3: Video Longo de Marca
**Escolha**: Sora 2
**Motivo**: Suporta ate 20s por clip

```json
{
  "platform": "sora2",
  "max_duration": 20,
  "narrative_focus": true,
  "estimated_cost": "$5.00"
}
```

### Exemplo 4: Video com Orcamento Limitado
**Escolha**: Kling 1.6
**Motivo**: Menor custo por segundo

```json
{
  "platform": "kling",
  "cost_per_second": "$0.02",
  "30s_video_cost": "$0.60"
}
```

## ARMADILHAS COMUNS

- **Erro 1**: Usar Runway para videos com dialogo -> Nao tem audio nativo
- **Erro 2**: Usar Kling para qualidade maxima -> Limitacoes visuais
- **Erro 3**: Ignorar limites de duracao -> Clips cortados
- **Erro 4**: Nao adaptar prompt ao syntax da plataforma -> Resultados ruins

## QUANDO USAR

- Runway: Maioria dos casos, iteracao, produtos
- Pika: Efeitos especiais, transformacoes
- Veo3: Videos com fala, dialogo
- Sora2: Narrativas longas, cinematografico
- Kling: Orcamento apertado
- Hailuo: VFX rapido, movimento dinamico

## RELACIONADO

- Ver tambem: prompt_magic_words_ecommerce_20251125.md
- Ver tambem: quality_checklist_11_pontos_20251125.md

---
**Fonte**: knowledge/platforms/*.md
**Processado**: 2025-11-25
**Quality Score**: 0.85/1.0
