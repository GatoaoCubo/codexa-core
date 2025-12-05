# Voice Server - Quick Start

> **TL;DR**: Funciona SEM configurar nenhuma API key!

## 1-Minute Setup

### Windows

```batch
REM Instalar dependências
python -m pip install -r codexa.app\voice\requirements.txt

REM Testar TTS
cd codexa.app\voice
python tts.py "teste de voz"

REM Usar no Claude Code
REM Digite: /v
```

### Linux/macOS

```bash
# Instalar dependências
pip install -r codexa.app/voice/requirements.txt

# Testar TTS
cd codexa.app/voice
python tts.py "teste de voz"

# Usar no Claude Code
# Digite: /v
```

## FAQ

### Preciso configurar ELEVENLABS_API_KEY?

**NÃO!** O sistema funciona sem nenhuma API key.

O voice server usa:
- **TTS**: Edge TTS (Microsoft, grátis, boa qualidade)
- **STT**: Whisper local (OpenAI, grátis, offline)

### Como melhorar a qualidade de voz?

A qualidade padrão (Edge TTS) já é boa!

Se quiser qualidade premium:
1. Crie conta em https://elevenlabs.io
2. Pegue API key em https://elevenlabs.io/app/settings/api-keys
3. Adicione no `.env` (raiz do projeto):
   ```env
   ELEVENLABS_API_KEY=el_sua_chave_aqui
   ```

### E se eu não tiver internet?

O sistema cai automaticamente para **pyttsx3** (offline, sempre funciona).

Para forçar modo offline:
```env
# Adicionar no .env
TTS_PROVIDER=pyttsx3
```

### Onde fica o .env?

Na **raiz do projeto** (não dentro de `voice/`):

```
codexa-core/
├── .env              ← AQUI (copiar de .env.example)
├── .env.example      ← Template com todas as variáveis
└── codexa.app/
    └── voice/
        └── server.py
```

### Como copiar .env.example?

**Windows**:
```batch
copy .env.example .env
```

**Linux/macOS**:
```bash
cp .env.example .env
```

**Depois editar** `.env` e adicionar suas chaves (se quiser).

### Erro "ELEVENLABS_API_KEY not found"

**Isso é NORMAL!** Ignore.

O sistema vai usar Edge TTS (grátis, bom) automaticamente.

### TTS não funciona

**Causa comum**: Falta `edge-tts` ou `pygame`

**Solução**:
```bash
pip install edge-tts pygame pyttsx3
```

**Testar**:
```bash
cd codexa.app/voice
python tts.py "teste"
```

### Microfone não funciona

**Solução**:
```bash
# Instalar dependências STT
pip install sounddevice soundfile webrtcvad faster-whisper

# Executar wizard
cd codexa.app/voice
python -m setup
```

## Providers Disponíveis

### TTS (Text-to-Speech)

| Provider | Custo | Qualidade | Online? | Configuração |
|----------|-------|-----------|---------|--------------|
| **Edge TTS** | FREE | Boa | Sim | Nenhuma (padrão) |
| ElevenLabs | Pago | Premium | Sim | ELEVENLABS_API_KEY |
| pyttsx3 | FREE | Básica | Não | Nenhuma (fallback) |

### STT (Speech-to-Text)

| Provider | Custo | Qualidade | Online? | Configuração |
|----------|-------|-----------|---------|--------------|
| **Whisper** | FREE | Ótima | Não | Nenhuma (único método) |

## Vozes Disponíveis

### Edge TTS (Grátis)

Portuguese-BR:
- `pt-BR-FranciscaNeural` (feminina, padrão)
- `pt-BR-AntonioNeural` (masculina)
- `pt-BR-BrendaNeural` (feminina)

Para mudar voz:
```env
# Adicionar no .env
EDGE_VOICE=pt-BR-AntonioNeural
```

## Estrutura de Fallback

```
TTS Request
    │
    ├─> Edge TTS (FREE, online)
    │   └─> SUCCESS → Use Edge TTS
    │   └─> FAIL ↓
    │
    ├─> ElevenLabs (premium, se configurado)
    │   └─> SUCCESS → Use ElevenLabs
    │   └─> FAIL ↓
    │
    └─> pyttsx3 (FREE, offline)
        └─> SUCCESS → Use pyttsx3
        └─> FAIL → Erro total
```

## Arquivos de Configuração

### .env (raiz do projeto)

```env
# Voice (TODAS OPCIONAIS)
ELEVENLABS_API_KEY=el_sua_chave_aqui  # Opcional
ELEVENLABS_VOICE_ID=pMsXgVXv3BLzUgSXRplE
EDGE_VOICE=pt-BR-FranciscaNeural
TTS_PROVIDER=auto  # auto, edge, elevenlabs, pyttsx3
VOICE_LANGUAGE=pt-BR
```

### Prioridades

1. **Variáveis de ambiente** (.env)
2. **Padrões do código** (config.py)
3. **Fallback automático** (tts.py)

## Troubleshooting

### Verificar se está funcionando

```bash
cd codexa.app/voice

# Testar TTS
python tts.py "olá mundo"

# Verificar config
python config.py

# Testar microfone (se STT instalado)
python stt.py
```

### Logs do servidor

O voice server imprime logs para stderr:
```
CODEXA Voice Server v3.0
=========================================
NEW: Poll-based API (listen_start, listen_poll, listen_stop)
LEGACY: Blocking API (listen, speak, listen_and_respond)
=========================================
```

### Forçar provider específico

Para testar um provider específico:

```python
# Testar Edge TTS
python -c "from tts import speak; speak('teste', provider='edge')"

# Testar pyttsx3
python -c "from tts import speak; speak('teste', provider='pyttsx3')"

# Testar ElevenLabs (precisa API key)
python -c "from tts import speak; speak('teste', provider='elevenlabs')"
```

## Próximos Passos

1. ✅ Instalar dependências
2. ✅ Testar TTS
3. (Opcional) Configurar ElevenLabs
4. Usar `/v` no Claude Code
5. Falar comandos normalmente

## Documentação Completa

- **README.md** - Documentação completa do sistema
- **SETUP.md** - Guia de setup detalhado
- **.env.example** - Template de configuração
- **docs/API_KEYS_REFERENCE.md** - Referência de todas as API keys
