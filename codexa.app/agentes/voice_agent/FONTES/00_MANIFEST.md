# MANIFEST | voice_agent FONTES v1.0.0

**Package**: FONTES (Knowledge Base for Voice AI Systems)
**Agent**: voice_agent | **Version**: 1.0.0 | **Date**: 2025-12-05
**Scope**: TTS, STT, Voice UI Knowledge Cards
**Purpose**: Domain expertise for voice synthesis, recognition, and interaction design
**Files**: 8 | **Categories**: 3

---

## CATEGORY INDEX

### TTS_PLATFORMS/ (Text-to-Speech)
| File | Platform | Quality | Cost | Use Case |
|------|----------|---------|------|----------|
| elevenlabs.md | ElevenLabs | Premium | $$ | Production, emotion |
| openai_tts.md | OpenAI TTS | High | $ | GPT integration |
| edge_tts.md | Edge TTS | Good | Free | Prototyping, fallback |

### STT_PLATFORMS/ (Speech-to-Text)
| File | Platform | Quality | Speed | Use Case |
|------|----------|---------|-------|----------|
| whisper_api.md | OpenAI Whisper | Excellent | Fast | Transcription |
| elevenlabs_scribe.md | ElevenLabs Scribe | Premium | Fast | Low-latency apps |

### VOICE_UI/ (Voice User Interface)
| File | Focus | Patterns |
|------|-------|----------|
| interaction_patterns.md | Conversational Design | 12 patterns |
| accessibility.md | WCAG Voice Guidelines | A11y compliance |

---

## SEARCH TRIGGERS

### Por Funcionalidade
| Keyword | Files | Context |
|---------|-------|---------|
| "gerar voz", "text to speech", "TTS" | TTS_PLATFORMS/*.md | Voice synthesis |
| "transcrever", "speech to text", "STT" | STT_PLATFORMS/*.md | Voice recognition |
| "multilingual", "idiomas" | elevenlabs.md, whisper_api.md | Multi-language |
| "gratis", "free", "fallback" | edge_tts.md | Cost-free option |
| "emocao", "expressivo" | elevenlabs.md | Emotional voices |
| "acessibilidade", "wcag" | accessibility.md | Compliance |
| "conversacional", "dialogo" | interaction_patterns.md | UX design |

### Por Plataforma
| Platform | Primary File | Related |
|----------|--------------|---------|
| ElevenLabs | elevenlabs.md | elevenlabs_scribe.md |
| OpenAI | openai_tts.md | whisper_api.md |
| Microsoft | edge_tts.md | - |

---

## CROSS-AGENT REFERENCES

| Agent | Relationship | Trigger |
|-------|--------------|---------|
| video_agent | Voice narration for videos | `/prime-video` |
| curso_agent | Course audio generation | `/prime-curso` |
| anuncio_agent | Audio ads, product descriptions | `/prime-anuncio` |
| photo_agent | Accessibility descriptions | `/prime-photo` |

---

## FILE INVENTORY (8 Files)

### Foundation (00)
| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 00 | MANIFEST.md | ~400 | Package index, search triggers |

### TTS Platforms (3 files) ~2,100 tokens
| File | Tokens | Platform |
|------|--------|----------|
| elevenlabs.md | ~800 | ElevenLabs Multilingual v2 |
| openai_tts.md | ~700 | OpenAI TTS / GPT-4o Audio |
| edge_tts.md | ~600 | Microsoft Edge TTS (free) |

### STT Platforms (2 files) ~1,200 tokens
| File | Tokens | Platform |
|------|--------|----------|
| whisper_api.md | ~700 | OpenAI Whisper API |
| elevenlabs_scribe.md | ~500 | ElevenLabs Scribe v1 |

### Voice UI (2 files) ~1,400 tokens
| File | Tokens | Focus |
|------|--------|-------|
| interaction_patterns.md | ~800 | Conversational UX patterns |
| accessibility.md | ~600 | WCAG voice guidelines |

**Total Estimated Tokens**: ~5,500

---

## QUALITY STANDARDS

All knowledge cards follow:
- **Template**: ADW-300 Knowledge Card structure
- **Sections**: Executive Summary, Key Concepts, How to Apply, Examples, When to Use
- **Quality Score Target**: >= 0.75

---

## USAGE INSTRUCTIONS

### For LLM Context Loading
```
1. Load 00_MANIFEST.md first (this file)
2. Load category files based on task:
   - TTS task → TTS_PLATFORMS/*.md
   - STT task → STT_PLATFORMS/*.md
   - UX design → VOICE_UI/*.md
3. Cross-reference with agent HOPs in prompts/
```

### For Human Navigation
```
FONTES/
├── 00_MANIFEST.md              ← You are here
├── TTS_PLATFORMS/
│   ├── elevenlabs.md           ← Premium TTS
│   ├── openai_tts.md           ← OpenAI integration
│   └── edge_tts.md             ← Free fallback
├── STT_PLATFORMS/
│   ├── whisper_api.md          ← Best transcription
│   └── elevenlabs_scribe.md    ← Low-latency STT
└── VOICE_UI/
    ├── interaction_patterns.md ← Conversational UX
    └── accessibility.md        ← WCAG compliance
```

---

**Package**: voice_agent FONTES v1.0.0
**Status**: READY
**Date**: 2025-12-05
