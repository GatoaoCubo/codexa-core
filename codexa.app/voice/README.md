# CODEXA Voice System v2.0

Sistema de voz para acessibilidade. Permite interagir com Claude Code usando apenas voz.

## Quick Start

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Executar setup (opcional - configura e testa)
python -m setup

# 3. No Claude Code, digitar:
/v
```

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

### TTS não funciona
1. Verifique se pygame está instalado: `pip install pygame`
2. Teste: `python tts.py "teste"`

### Microfone não detectado
1. Verifique se sounddevice está instalado: `pip install sounddevice`
2. Execute o setup: `python -m setup`

### ElevenLabs não funciona
1. Verifique a API key no `.env`
2. O sistema vai usar Edge TTS como fallback

## Versao

- **v2.1.0** - Bug fixes: .env loading, error messages, lib consolidation
- **v2.0.0** - Sistema unificado em codexa.gato
- **Status**: Production
- **Data**: 2025-11-28
