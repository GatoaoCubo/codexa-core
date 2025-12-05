# CODEXA Voice System v3.0

Sistema de voz para acessibilidade. Permite interagir com Claude Code usando apenas voz.

## IMPORTANTE: Funciona SEM API Keys!

O sistema de voz funciona **completamente grátis** usando:
- **TTS**: Edge TTS (Microsoft, grátis, boa qualidade)
- **STT**: Whisper local (OpenAI, grátis, offline)

A chave `ELEVENLABS_API_KEY` é **OPCIONAL** e só necessária se você quiser qualidade premium.

## Quick Start

### Windows

```batch
REM 1. Instalar dependências
python -m pip install -r codexa.app\voice\requirements.txt

REM 2. (OPCIONAL) Configurar .env na raiz do projeto
REM    Apenas se quiser usar ElevenLabs premium:
REM    ELEVENLABS_API_KEY=el_your_key_here
REM
REM    Se não configurar, usa Edge TTS (grátis, bom)

REM 3. No Claude Code, digitar:
REM /v
```

### Linux/macOS

```bash
# 1. Instalar dependências
pip install -r codexa.app/voice/requirements.txt

# 2. (OPCIONAL) Configurar .env na raiz do projeto
#    Apenas se quiser usar ElevenLabs premium

# 3. No Claude Code, digitar:
/v
```

## Fallback Automático

O sistema tenta automaticamente (em ordem):

### TTS (Text-to-Speech):
1. **Edge TTS** (FREE, online, boa qualidade) ← padrão
2. **ElevenLabs** (premium, se configurado)
3. **pyttsx3** (FREE, offline, qualidade básica) ← sempre funciona

### STT (Speech-to-Text):
- **Whisper** (FREE, offline, ótima qualidade) ← único método

## Uso

### Ativar Modo Voz
Digite `/v` no Claude Code. O sistema vai dizer "Modo voz ativado. Pode falar."

### Comandos por Voz
Após ativar, fale seus comandos normalmente:
- "Liste os arquivos"
- "Crie uma função soma"
- "Status do git"
- "Explique este código"

### Sair do Modo Voz
Diga qualquer um:
- "parar"
- "sair"
- "tchau"
- "exit"

## Estrutura

```
voice/
├── __init__.py       # Exports principais
├── config.py         # Configuracao centralizada
├── stt.py            # Speech-to-Text (ElevenLabs Scribe)
├── tts.py            # Text-to-Speech (Edge/ElevenLabs/pyttsx3)
├── server.py         # MCP Server
├── requirements.txt  # Dependencias
├── lib/              # Modulos avancados
│   ├── summarizer.py     # Resumo para TTS
│   └── device_manager.py # Gerenciamento de dispositivos
├── docs/             # Documentacao
│   ├── README.md
│   └── SETUP.md
├── setup/            # Wizard de configuracao
│   ├── __init__.py
│   ├── __main__.py
│   └── wizard.py
└── config/
    └── voices.json   # Catalogo de vozes
```

## TTS Fallback Chain

O sistema tenta usar TTS na seguinte ordem:
1. **Edge TTS** - Gratuito, online, boa qualidade
2. **ElevenLabs** - Premium (requer API key)
3. **pyttsx3** - Offline, sempre funciona

## Configuração

Edite o arquivo `.env` na raiz do projeto:

```env
# Nome do usuário
CODEXA_USER_NAME=SeuNome

# Idioma
CODEXA_LANGUAGE=pt
STT_LANGUAGE=pt

# ElevenLabs (opcional - premium)
ELEVENLABS_API_KEY=sua_chave_aqui

# Voz do Edge TTS
EDGE_VOICE=pt-BR-FranciscaNeural
```

## Vozes Disponíveis

### Edge TTS (Gratuito)
- `pt-BR-FranciscaNeural` - Feminina, natural
- `pt-BR-AntonioNeural` - Masculina
- `pt-PT-RaquelNeural` - Português de Portugal

### ElevenLabs (Premium)
Configure `ELEVENLABS_API_KEY` para usar vozes premium.

## Acessibilidade

Este sistema foi projetado para usuários que não podem digitar:

- Ativação com apenas 2 caracteres (`/v`)
- Respostas faladas automaticamente
- Loop contínuo (não precisa digitar novamente)
- Comandos de saída por voz

## Troubleshooting

### "ELEVENLABS_API_KEY not found" ou erro similar

**Resposta**: Isso é NORMAL! O sistema vai funcionar mesmo assim.

O voice server tenta os providers de TTS nesta ordem:
1. Edge TTS (FREE) - vai funcionar se tiver internet
2. ElevenLabs - só tenta se você configurou a API key
3. pyttsx3 (FREE, offline) - sempre funciona

**Solução**: Ignore o aviso. O sistema vai usar Edge TTS automaticamente.

### TTS não funciona / Sem som

**Causa comum**: Faltam dependências de áudio

**Solução**:
```bash
# Instalar todas as dependências
pip install -r codexa.app/voice/requirements.txt

# Ou individualmente:
pip install edge-tts  # Para Edge TTS (recomendado)
pip install pygame    # Para playback de áudio
pip install pyttsx3   # Para fallback offline
```

**Testar**:
```bash
cd codexa.app/voice
python tts.py "teste de voz"
```

### Microfone não detectado

**Solução**:
```bash
# Instalar dependências STT
pip install sounddevice soundfile webrtcvad faster-whisper

# Executar wizard de configuração
cd codexa.app/voice
python -m setup
```

### Edge TTS falha (sem internet)

**Resposta**: O sistema vai automaticamente usar pyttsx3 (offline).

**Para forçar offline**:
```env
# Adicionar no .env
TTS_PROVIDER=pyttsx3
```

### Qualidade de voz ruim

**Para melhorar**:

1. **Grátis**: Use Edge TTS (padrão, boa qualidade)
2. **Premium**: Configure ElevenLabs:
   ```env
   ELEVENLABS_API_KEY=el_sua_chave_aqui
   ```
   Obtenha chave em: https://elevenlabs.io/app/settings/api-keys

### Erro "Module not found"

**Solução**:
```bash
# Reinstalar todas as dependências
pip install -r codexa.app/voice/requirements.txt --force-reinstall
```

### ElevenLabs não funciona
1. Verifique a API key no `.env`
2. O sistema vai usar Edge TTS como fallback

## Versao

- **v2.1.0** - Bug fixes: .env loading, error messages, lib consolidation
- **v2.0.0** - Sistema unificado em codexa.gato
- **Status**: Production
- **Data**: 2025-11-28
