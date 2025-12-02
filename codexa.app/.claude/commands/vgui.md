# /vgui - Voice GUI Overlay

Abre a interface gráfica flutuante de voz.

## O que faz

1. Abre uma janela minimalista sempre no topo
2. Mostra status de gravação em tempo real
3. Exibe waveform e nível de áudio
4. Mostra última transcrição

## Modos

- **--daemon**: Conecta ao daemon para status em tempo real
- **--standalone**: Modo independente com botão de gravação

## Execução

```bash
cd voice && python voice_gui.py --daemon &
```

A janela é arrastável e pode ser fechada clicando no X.
