# Video Agent Outputs

Este diretorio contem os videos gerados pelo video_agent.

## Trinity Output Format

Cada video gerado produz 4 arquivos:

```
{nome}_{duracao}s.mp4       # Video final
{nome}_{duracao}s.md        # Relatorio legivel
{nome}_{duracao}s.llm.json  # Dados estruturados para LLM
{nome}_{duracao}s.meta.json # Metadata e metricas
```

### .mp4 - Video Final
- Video renderizado pronto para uso
- Inclui narracao, musica e text overlays (se modo overlay)
- Codec H.264, compativel com todas plataformas

### .md - Relatorio Markdown
- Resumo da geracao
- Storyboard com descricao de cada shot
- Script de narracao
- Metricas de qualidade
- Custos

### .llm.json - Dados para LLM
- Estrutura JSON completa
- Todos os prompts usados
- Configuracoes aplicadas
- Util para re-geracao ou analise

### .meta.json - Metadata
- Especificacoes tecnicas do video
- Metricas de performance
- Validacao de qualidade (11 pontos)
- Compatibilidade por plataforma

## Exemplo Incluido

- `example_nike_30s.*` - Exemplo completo de video Nike Air Max

## Limpeza

Videos antigos podem ser removidos manualmente ou via script:

```bash
# Manter apenas ultimos 10 videos
ls -t *.mp4 | tail -n +11 | xargs rm -f
```

## Armazenamento

Para producao, configure AWS S3:

```env
AWS_S3_BUCKET=video-agent-outputs
AWS_REGION=us-east-1
```

---
**video_agent v2.0.0**
