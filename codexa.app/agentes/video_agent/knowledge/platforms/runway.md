# Runway Gen-3 Alpha - Guia de Prompt Engineering

**Versão**: Gen-3 Alpha / Turbo (2025) | **Empresa**: Runway | **Status**: Estabelecido

---

## Overview

Runway Gen-3 Alpha é referência em iteração rápida e controle de câmera. A versão Turbo oferece velocidade ainda maior para exploração criativa.

**Specs**:
- Duração: 5-10 segundos
- Resolução: até 1080p
- Modelos: Gen-3 Alpha (qualidade), Turbo (velocidade)
- Destaque: Camera Control feature

---

## Estrutura Oficial de Prompt

### Fórmula Runway
```
[camera movement]: [establishing scene]. [additional details].
```

### Separar Visual de Câmera
```
Visual: [descrição da cena, sujeito, ação]
Camera: [movimento, ângulo, lens]
```

### Exemplo
```
Low angle static shot: The camera is angled up at a confident entrepreneur as she stands in a modern glass office with city skyline visible. The dramatic sky is golden hour with warm light streaming in. She gestures toward a holographic dashboard floating beside her.
```

---

## Camera Control (Gen-3 Alpha Turbo)

### Movimentos Disponíveis
| Eixo | Movimento | Descrição |
|------|-----------|-----------|
| X | Horizontal | Esquerda/direita |
| Y | Vertical | Cima/baixo |
| Pan | Rotação H | Giro horizontal |
| Tilt | Rotação V | Giro vertical |
| Zoom | In/Out | Aproximar/afastar |
| Roll | Rotação | Inclinar frame |

### Recomendação
Sempre acompanhe camera controls com texto prompt para melhores resultados.

---

## Camera Keywords

### Ângulos
| Keyword | Efeito | Uso |
|---------|--------|-----|
| `low angle` | Poder, grandeza | Hero shots |
| `high angle` | Vulnerabilidade | Mostrar contexto |
| `overhead` | Vista superior | Layouts, produtos |
| `FPV` | Primeira pessoa | Imersão |
| `eye level` | Neutro, conexão | Diálogo, confiança |

### Movimentos
| Keyword | Efeito |
|---------|--------|
| `tracking` | Seguir sujeito |
| `establishing wide` | Mostrar contexto |
| `over the shoulder` | Perspectiva pessoal |
| `handheld` | Orgânico, documental |
| `dolly` | Movimento suave |

### Tipos de Shot
| Keyword | Descrição |
|---------|-----------|
| `wide angle` | Campo amplo |
| `close up` | Detalhe |
| `macro cinematography` | Extremo detalhe |
| `medium shot` | Cintura para cima |

---

## Best Practices

### 1. Evitar Negações
```
❌ "the camera doesn't move"
✅ "static locked shot"
```

### 2. Reforçar Ideias-Chave
Repetir conceitos importantes em diferentes seções:
```
"A hyperspeed shot flying through futuristic city. Camera rapidly flies through neon-lit streets at hyperspeed..."
```

### 3. Separar Ações
```
Subject action: [o que o sujeito faz]
Camera action: [o que a câmera faz]
Speed: [velocidade do movimento]
Transition: [como termina]
```

### 4. Um Movimento Principal
```
✅ "slow dolly forward" (um movimento)
❌ "dolly forward while panning and zooming" (múltiplos)
```

---

## Exemplos por Categoria

### FPV (First Person View)
```
FPV drone shot: A FPV drone flies through a modern glass office building, weaving between desks and through doorways. Employees work at computers as the camera zooms past. Natural office lighting, motion blur.
```

### Zoom Dramático
```
Super fast zoom out: Starting from extreme close-up of a glowing screen showing "CODEXA" logo, rapidly zooming out to reveal entrepreneur at desk, then entire modern office, then city skyline through windows.
```

### Tracking Shot
```
Handheld tracking shot: Following a confident businesswoman walking through a busy startup office, camera stays at shoulder level, slight movement adds energy. Other employees blur past in foreground.
```

### Product Orbit
```
Smooth orbit shot: Camera slowly circles around a floating premium headphone, studio lighting creates moving highlights and shadows on the product surface. Clean white background, 360 degree rotation.
```

---

## Casos de Uso E-commerce

### Product Reveal
```
Dramatic reveal shot: Black screen fades to reveal premium sneaker floating in center frame, dramatic spot lighting creates strong shadows. Camera slowly pushes forward as secondary lights illuminate product details. Studio environment, 4K quality.
```

### Brand Story Opening
```
Establishing wide: Modern glass-walled office at golden hour, city skyline visible through windows. Camera slowly dollies forward toward entrepreneur at standing desk. Warm sunlight creates lens flares. Professional, aspirational mood.
```

### Feature Highlight
```
Macro cinematography: Extreme close-up of premium watch mechanism, gears moving in precise motion. Camera slowly pulls back revealing full watch face. Studio lighting, shallow depth of field, luxury aesthetic.
```

### CTA/Urgency
```
Dynamic zoom shot: Camera rapidly pushes into glowing CTA button on screen, "COMEÇAR AGORA" text pulses with energy. Particle effects surround button. Dark background with golden accent lighting, premium tech aesthetic.
```

---

## Image-to-Video

### Com Camera Control
1. Upload imagem de referência
2. Selecione movimento de câmera
3. Adicione prompt de texto
4. Ajuste intensidade do movimento

### Prompt para I2V
```
[Starting from uploaded image] The scene comes to life as [subject action]. Camera [movement description]. [Lighting and atmosphere].
```

---

## Workflow de Iteração

### Fase 1: Exploração (Turbo)
- Gerar múltiplas variantes rápidas
- Testar diferentes câmeras
- Refinar prompt baseado em resultados

### Fase 2: Refinamento (Alpha)
- Usar prompt otimizado
- Qualidade máxima
- Fine-tuning de detalhes

### Fase 3: Produção
- Exportar em resolução final
- Verificar continuidade
- Preparar para edição

---

## Integração com Workflow

### Runway → FFmpeg
```
1. Gerar clips no Runway
2. Download em máxima qualidade
3. Concatenar com FFmpeg
4. Adicionar áudio/overlays
```

### Multi-Shot Consistency
Manter descrições de personagem/ambiente consistentes:
```
Shot 1: "A woman with short dark hair, wearing navy blazer..."
Shot 2: "The same woman with short dark hair, navy blazer..."
Shot 3: "She (short dark hair, navy blazer) now..."
```

---

## Templates Rápidos

### Tech Product
```
[movement]: Premium [product] floating against dark gradient background, subtle blue accent lighting creating rim light, holographic UI elements appearing around product. Futuristic tech aesthetic, 4K cinematic quality.
```

### Fashion
```
[movement]: [clothing item] on confident model, fabric catching light with natural movement, professional fashion photography lighting, editorial style, slight motion blur for dynamism.
```

### Corporate/Brand
```
[movement]: Modern office environment at golden hour, [subject description] working confidently, warm natural lighting through large windows, professional aspirational mood, shallow depth of field.
```

---

## Referências

- [Runway Help - Gen-3 Alpha Prompting Guide](https://help.runwayml.com/hc/en-us/articles/30586818553107-Gen-3-Alpha-Prompting-Guide)
- [Runway Help - Camera Control](https://help.runwayml.com/hc/en-us/articles/34926468947347-Creating-with-Camera-Control-on-Gen-3-Alpha-Turbo)
- [Runway Academy - Gen-3 Alpha Beginner Guide](https://academy.runwayml.com/gen3-alpha/getting-started-with-gen3-alpha)
- [Runway Research - Introducing Gen-3 Alpha](https://runwayml.com/research/introducing-gen-3-alpha)
- [FilmArt - Runway Camera Control Guide](https://filmart.ai/runway-camera-control-runway-gen-3-camera-prompts/)

---

**Última atualização**: 2025-11-24
