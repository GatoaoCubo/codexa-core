# VOZ | Configuracao ElevenLabs

> Configuracao de voz para {{PERSONA_NAME}}
> Ultima atualizacao: {{CURRENT_DATE}}

---

## VOZ ESCOLHIDA

### Primary: "{{VOICE_NAME}}"

**Voice ID**: `{{VOICE_ID}}` (verificar ID exato na API)

**Motivo da Escolha**:
- Tom naturalmente calmante - alinha com filosofia "{{PERSONA_PHILOSOPHY}}"
- Ideal para orientacao acolhedora
- Transmite confianca sem ser autoritaria
- Perfeita para temas sensiveis

**Descricao ElevenLabs**:
> "{{VOICE_DESCRIPTION}}"

---

## ALTERNATIVA

### Backup: "{{BACKUP_VOICE_NAME}}"

**Uso**: Se voz principal nao estiver disponivel ou feedback negativo

**Motivo**:
- Voz madura e calorosa
- Transmite experiencia (alinha com "{{PERSONA_EXPERIENCE}}")
- Portugues brasileiro nativo
- Tom amigavel e acessivel

---

## CONFIGURACOES DE VOZ

```json
{
  "voice_settings": {
    "stability": 0.65,
    "similarity_boost": 0.75,
    "style": 0.3,
    "use_speaker_boost": true
  },
  "model_id": "eleven_multilingual_v2"
}
```

### Parametros Explicados

| Parametro | Valor | Motivo |
|-----------|-------|--------|
| stability | 0.65 | Balanco entre consistencia e naturalidade |
| similarity_boost | 0.75 | Manter caracteristicas vocais unicas |
| style | 0.3 | Expressividade moderada (nao exagerada) |
| speaker_boost | true | Clareza em diferentes dispositivos |

---

## ADAPTACAO POR CONTEXTO

### Tom Acolhedor (Default)
```json
{
  "stability": 0.65,
  "style": 0.3
}
```
- Uso: Orientacoes gerais, duvidas comuns

### Tom Urgente (Red Flags)
```json
{
  "stability": 0.75,
  "style": 0.4
}
```
- Uso: Encaminhamento profissional, alertas
- Mais estavel e expressivo

### Tom Celebratorio
```json
{
  "stability": 0.55,
  "style": 0.5
}
```
- Uso: Parabenizar progresso, feedback positivo
- Mais dinamico e animado

---

## INTEGRACAO

### Endpoint TTS Existente

```typescript
// supabase/functions/{{persona_id}}-tts/index.ts
const voiceConfig = {
  voice_id: "{{VOICE_ID}}", // ou ID especifico
  model_id: "eleven_multilingual_v2",
  voice_settings: {
    stability: 0.65,
    similarity_boost: 0.75,
    style: 0.3,
    use_speaker_boost: true
  }
};
```

### Variaveis de Ambiente

```env
ELEVENLABS_API_KEY=sk_...
ELEVENLABS_VOICE_ID={{VOICE_ID}}
```

---

## TESTES RECOMENDADOS

### Frases de Teste

1. **Saudacao**:
   "Ola! Eu sou a {{PERSONA_NAME}}, sua parceira em {{DOMAIN_EXPERTISE_PT}}."

2. **Orientacao Tecnica**:
   "{{TECHNICAL_ADVICE_EXAMPLE}}"

3. **Empatia**:
   "Entendo sua preocupacao. Vamos resolver isso juntos."

4. **Urgencia**:
   "{{URGENCY_ADVICE_EXAMPLE}}"

---

## PROXIMOS PASSOS

- [ ] Validar voice_id exato na API ElevenLabs
- [ ] Testar com frases padrao
- [ ] Coletar feedback de usuarios beta
- [ ] Ajustar parametros baseado em feedback

---

**Versao**: 1.0.0
**Categoria**: Configuracao > Voz
