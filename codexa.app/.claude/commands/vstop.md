# /vstop - Stop Voice Daemon

Para o daemon de voz que está rodando em background.

## O que faz

1. Envia sinal de shutdown para o daemon
2. Libera o hotkey F12
3. Limpa arquivos temporários

## Execução

```bash
cd voice && python voice_daemon.py stop
```
