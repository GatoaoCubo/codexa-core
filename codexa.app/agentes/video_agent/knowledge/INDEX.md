# Knowledge Base Index | video_agent

**Base de conhecimento para geração de vídeo AI**

---

## Estrutura

```
knowledge/
├── INDEX.md (este arquivo)
│
├── platforms/              # Guias por plataforma
│   ├── veo3.md            # Google Veo 3
│   ├── sora2.md           # OpenAI Sora 2
│   ├── kling.md           # Kuaishou Kling 1.6
│   ├── hailuo.md          # MiniMax Hailuo
│   ├── runway.md          # Runway Gen-3 Alpha
│   └── pika.md            # Pika 2.0/2.1
│
├── prompt_engineering/     # Sistema de prompts
│   ├── anatomy.md         # Anatomia universal
│   ├── camera_vocabulary.md
│   ├── lighting_vocabulary.md
│   └── magic_words.md     # Palavras de qualidade
│
└── brand_alignment/        # Integração com marca
    └── brand_to_video.md  # Tradução marca → vídeo
```

---

## Plataformas Suportadas

| Plataforma | Empresa | Força Principal | Duração | Áudio |
|------------|---------|-----------------|---------|-------|
| **Veo 3** | Google | Diálogo, realismo | 8s | Sim |
| **Sora 2** | OpenAI | Cinematografia, narrativa | 20s | Sim |
| **Kling 1.6** | Kuaishou | Custo-benefício | 5s | Não |
| **Hailuo** | MiniMax | VFX, velocidade | 6s | Não |
| **Runway** | Runway | Iteração, controle | 10s | Não |
| **Pika** | Pika Labs | Efeitos, transformações | 8s | Não |

---

## Guia Rápido de Decisão

### Quando usar cada plataforma:

**Veo 3 (Google)**
- Vídeos com diálogo/narração
- Necessidade de áudio sincronizado
- Realismo máximo

**Sora 2 (OpenAI)**
- Narrativas cinematográficas
- Física realista (materiais, movimento)
- Vídeos mais longos (até 20s)

**Kling 1.6 (Kuaishou)**
- Orçamento limitado
- Animação de personagens
- Movimento fluido (60fps)

**Hailuo/MiniMax (MiniMax)**
- Geração rápida
- Efeitos visuais (VFX)
- Movimentos dinâmicos

**Runway Gen-3 (Runway)**
- Iteração rápida
- Controle de câmera preciso
- Workflow de produção

**Pika 2.0 (Pika Labs)**
- Efeitos especiais
- Transformações (Pikadditions/Pikaswaps)
- Storytelling sequencial

---

## Estrutura Universal de Prompt

```
[Camera + Movement] + [Subject + Description] + [Action] + [Environment] + [Lighting] + [Style] + [Audio]*
```

### Elementos Essenciais
1. **Camera**: movimento + ângulo + lens
2. **Subject**: quem/o que + descrição detalhada
3. **Action**: o que acontece
4. **Environment**: onde
5. **Lighting**: como ilumina + mood
6. **Style**: qualificadores de qualidade
7. **Audio**: (apenas Veo3/Sora2)

---

## Magic Words (Top 10)

1. `cinematic 4K quality`
2. `shallow depth of field`
3. `professional lighting`
4. `slow dolly forward`
5. `motion blur enabled`
6. `golden hour lighting`
7. `(no subtitles)` (Veo3)
8. `((element))` (Hailuo)
9. `--camera [movement]` (Pika)
10. `shot on 35mm film`

---

## Brand Alignment

### Tradução Marca → Vídeo
| Elemento da Marca | Tradução para Vídeo |
|-------------------|---------------------|
| Cor primária | Iluminação dominante |
| Cor secundária | Acentos, sombras |
| Tom de voz | Ritmo de edição |
| Personalidade | Movimento de câmera |
| Valores | Atmosfera, mood |

---

## Arquivos por Caso de Uso

### Gerar prompts para e-commerce
1. `platforms/[escolhida].md` - Sintaxe
2. `prompt_engineering/anatomy.md` - Estrutura
3. `brand_alignment/brand_to_video.md` - Alinhamento

### Entender vocabulário cinematográfico
1. `prompt_engineering/camera_vocabulary.md`
2. `prompt_engineering/lighting_vocabulary.md`

### Melhorar qualidade dos prompts
1. `prompt_engineering/magic_words.md`

---

## Referências Externas

### Documentação Oficial
- [Google Cloud - Veo Prompt Guide](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)
- [OpenAI Cookbook - Sora 2](https://cookbook.openai.com/examples/sora/sora2_prompting_guide)
- [Runway Help - Gen-3 Alpha](https://help.runwayml.com/hc/en-us/articles/30586818553107-Gen-3-Alpha-Prompting-Guide)

### Guias da Comunidade
- [Segmind - Kling Prompts](https://blog.segmind.com/best-text-to-video-prompts-for-kling-ai-with-examples/)
- [Curious Refuge - Hailuo Tips](https://curiousrefuge.com/blog/5-tips-for-using-minimax-ai-video-generator-by-hailuo-ai)
- [Pika AI - Prompt Guide](https://pikartai.com/prompt/)

---

**Versão**: 2.0.0
**Última atualização**: 2025-11-24
**Total de arquivos**: 11
