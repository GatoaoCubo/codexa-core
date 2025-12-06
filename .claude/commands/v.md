# /v - Voice Mode v10.1

Interacao fluida por voz com feedback claro e timing otimizado.

## FLUXO SIMPLIFICADO

```
1. Falar "Pode falar" via TTS
2. AGUARDAR 1.5s (evita mic capturar TTS)
3. Iniciar gravacao (15s)
4. Polling rapido ate terminar
5. Processar e responder via TTS
```

## EXECUCAO IMEDIATA

Ao receber /v, execute EXATAMENTE nesta ordem:

### PASSO 1: Aviso Sonoro
```
mcp__voice__speak("Pode falar")
```
Isso avisa o usuario que a gravacao vai comecar.

### PASSO 2: DELAY OBRIGATORIO
```python
# Aguardar 1.5s para TTS terminar de tocar
# Isso evita que o microfone capture o proprio TTS
import time; time.sleep(1.5)  # Ou equivalente no contexto
```
**IMPORTANTE**: Sem este delay, os primeiros segundos de fala sao perdidos!

### PASSO 3: Iniciar Gravacao
```
mcp__voice__listen_start(max_duration=15, initial_timeout=5, language="pt")
```
Retorna session_id imediatamente.

### PASSO 4: Polling Rapido
```
LOOP ate status != "recording":
    mcp__voice__listen_poll(session_id)
    - "recording" + has_speech=True -> continuar
    - "recording" + has_speech=False -> continuar
    - "processing/transcribing" -> aguardar
    - "done" -> processar transcript
    - "timeout" -> informar "Nao detectei fala"
    - "error" -> informar erro
```

### PASSO 5: Processar e Responder
- Interpretar o comando/pergunta do usuario
- Executar acao se aplicavel
- Responder via `mcp__voice__speak("resposta curta")`

## REGRAS DE RESPOSTA

| Situacao | Resposta TTS |
|----------|--------------|
| Comando executado | "Feito" ou descricao curta |
| Pergunta respondida | Resposta em 1-2 frases |
| Nao entendeu | "Nao entendi. Repita por favor." |
| Timeout | "Nao detectei sua voz. Tente novamente." |
| Exit (parar/sair) | "Ate logo!" |

## EXEMPLO COMPLETO

```
Usuario digita: /v

Claude:
1. mcp__voice__speak("Pode falar")
2. [AGUARDA 1.5s - delay obrigatorio]
3. mcp__voice__listen_start(max_duration=15, ...)
   -> session_id: abc123
4. mcp__voice__listen_poll("abc123")
   -> status: recording, has_speech: True
5. mcp__voice__listen_poll("abc123")
   -> status: done, transcript: "quantos arquivos tem aqui"
6. [Conta arquivos na pasta atual]
7. mcp__voice__speak("Tem 15 arquivos nesta pasta")
```

## CONFIG

- **TTS**: ElevenLabs (prioridade) > Edge > pyttsx3
- **STT**: ElevenLabs Scribe (prioridade) > Google Speech
- **Microfone**: Auto-detect (system default)
- **Idioma**: pt-BR
- **Max duracao**: 15 segundos
- **Initial timeout**: 5 segundos (sai se nao detectar fala)
- **TTS→Record delay**: 1.5s (evita feedback)
- **VAD silence**: 2.0s (permite pausas naturais)

## EXIT KEYWORDS

parar, sair, exit, quit, stop, encerrar, tchau

---
**Version**: 10.1.0 | **Date**: 2025-12-06
**Mudancas v10.1**:
- Delay 1.5s entre TTS e gravacao (fix inicio cortado)
- VAD silence 2.0s (fix final cortado)
- Energy threshold mais sensivel
