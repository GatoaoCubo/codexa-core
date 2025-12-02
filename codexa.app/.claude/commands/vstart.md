# /vstart - Start Voice Daemon

Inicia o daemon de voz em background para modo contínuo.

## O que faz

1. Inicia o `voice_daemon.py` em background
2. Ativa o hotkey F12 para push-to-talk
3. Permite conversa contínua sem precisar digitar /v

## Como usar

Após iniciar, pressione **F12** para falar a qualquer momento.

## Execução

```bash
cd voice && python voice_daemon.py start &
```

Aguarde a mensagem de confirmação e depois use F12 para falar.
