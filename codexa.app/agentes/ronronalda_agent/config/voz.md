# VOZ | Configuracao ElevenLabs

> Configuracao de voz para Ronronalda
> Ultima atualizacao: 2025-11-28

---

## VOZ ESCOLHIDA

### Primary: "Carla - Relaxing"

**Voice ID**: `carla` (verificar ID exato na API)

**Motivo da Escolha**:
- Tom naturalmente calmante - alinha com filosofia "Gato calmo, casa leve"
- Ideal para orientacao acolhedora
- Transmite confianca sem ser autoritaria
- Perfeita para temas sensiveis (estresse, problemas de saude)

**Descricao ElevenLabs**:
> "A naturally calming voice for meditation, affirmations, yoga, and relaxed narration"

---

## ALTERNATIVA

### Backup: "Senior Brazilian Female"

**Uso**: Se Carla nao estiver disponivel ou feedback negativo

**Motivo**:
- Voz madura e calorosa
- Transmite experiencia (alinha com "15 anos de etologia")
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
- Uso: Encaminhamento veterinario, alertas de saude
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
// supabase/functions/ronronalda-tts/index.ts
const voiceConfig = {
  voice_id: "carla", // ou ID especifico
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
ELEVENLABS_VOICE_ID=carla
```

---

## TESTES RECOMENDADOS

### Frases de Teste

1. **Saudacao**:
   "Ola! Eu sou a Ronronalda, sua parceira no cuidado felino."

2. **Orientacao Tecnica**:
   "A regra de ouro eh: numero de gatos mais um, de caixas de areia."

3. **Empatia**:
   "Entendo sua preocupacao. Vamos resolver isso juntos."

4. **Urgencia**:
   "Se houver sangue na urina, por favor, leve ao veterinario imediatamente."

---

## PROXIMOS PASSOS

- [ ] Validar voice_id exato na API ElevenLabs
- [ ] Testar com frases padrao
- [ ] Coletar feedback de usuarios beta
- [ ] Ajustar parametros baseado em feedback

---

**Versao**: 1.0.0
**Categoria**: Configuracao > Voz
