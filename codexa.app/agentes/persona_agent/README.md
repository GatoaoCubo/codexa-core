# persona_agent | A Voz da Marca {{BRAND_NAME}}

> **Versao**: 1.0.0 (Template)
> **Tipo**: Agente Central de Interacao Humana
> **Status**: Meta-construido por todos os agentes

---

## O QUE E {{PERSONA_NAME}}

**{{PERSONA_NAME}} nao eh um chatbot. Eh a PERSONA da marca {{BRAND_NAME}}.**

Ela eh a unica interface humana da empresa:
- Chat no site (atual)
- WhatsApp Business (planejado)
- Email Marketing (planejado)
- Redes Sociais (planejado)
- Atendimento telefonico (futuro)

**Uma persona. Multiplos canais. Conhecimento vivo.**

---

## IDENTIDADE

| Atributo | Valor |
|----------|-------|
| Nome | {{PERSONA_NAME}} ({{PERSONA_NICKNAME}}) |
| Profissao | {{PERSONA_ROLE}} |
| Experiencia | {{PERSONA_EXPERIENCE}} |
| Filosofia | "{{PERSONA_PHILOSOPHY}}" |
| Abordagem | Observacao -> Ajuste -> Escolha |

### Tom de Voz (4D)
- **Formalidade**: Media
- **Humor**: Baixo-medio
- **Respeito**: Alto
- **Entusiasmo**: Medio

### Personalidade
- Acolhedora
- Didatica
- Sabia
- Minimalista
- Confiavel

---

## ARQUITETURA

```
persona_agent/
├── README.md                    # Este arquivo
├── VISION.md                    # Visao completa do agente
├── UX_IMPROVEMENTS.md           # Melhorias de UX planejadas
│
├── knowledge/                   # Base de conhecimento
│   ├── core/
│   │   └── identidade.md        # Quem eh {{PERSONA_NAME}}
│   ├── issues/                  # Problemas/comportamentos
│   │   ├── issue_1.md
│   │   ├── issue_2.md
│   │   └── ...
│   └── canais/                  # (a criar)
│       ├── site.md
│       ├── whatsapp.md
│       └── ...
│
└── templates/
    └── variaveis.md             # Sistema de {VARIAVEIS}
```

---

## COMO FUNCIONA

### Sistema de {VARIAVEIS}

{{PERSONA_NAME}} adapta respostas sem perder identidade:

```yaml
# Detectadas automaticamente
{CANAL}: site | whatsapp | email
{EMOCAO}: frustrado | ansioso | feliz
{ISSUE}: {{ISSUE_1}} | {{ISSUE_2}} | {{ISSUE_3}} | {{ISSUE_4}}

# Controlam a saida
{TOM}: acolhedor | tecnico | urgente
{TAMANHO}: curto | medio | longo
```

### Fluxo de Resposta

```
Usuario envia mensagem
       ↓
Detectar {VARIAVEIS}
       ↓
Buscar conhecimento relevante
       ↓
Gerar resposta adaptada
       ↓
Adicionar produtos (se aplicavel)
       ↓
Entregar no formato do {CANAL}
```

---

## IMPLEMENTACAO ATUAL

### Frontend
- `src/components/{{PERSONA_NICKNAME}}Chat.tsx` - Interface do chat
- `src/pages/{{PERSONA_NICKNAME}}Page.tsx` - Pagina /sac
- `src/hooks/use{{PERSONA_NAME}}.ts` - State management
- `src/lib/voice.ts` - Voz bidirecional

### Backend
- `supabase/functions/{{persona_id}}-chat/` - AI principal
- `supabase/functions/{{persona_id}}-recommendations/` - Produtos
- `supabase/functions/{{persona_id}}-tts/` - Text-to-speech

### Inteligencia
- Modelo: Gemini 2.5 Flash (via Lovable AI)
- Voz: OpenAI TTS (nova)
- Deteccao: Regex + keywords

---

## ROADMAP

### v0.1 (Atual)
- [x] Chat funcional no site
- [x] Deteccao de issues
- [x] Recomendacao de produtos
- [x] TTS com OpenAI
- [x] Red flags de seguranca

### v0.2 (Proximo)
- [ ] Melhorias UX (avatar, cores, mobile)
- [ ] Base de conhecimento estruturada
- [ ] Historico de sessao
- [ ] Contexto visivel

### v0.3
- [ ] Widget embeddable
- [ ] Memoria entre sessoes
- [ ] ElevenLabs voice

### v1.0
- [ ] WhatsApp Business
- [ ] Voz propria treinada
- [ ] Todos os canais unificados

---

## AGENTES QUE CONSTROEM {{PERSONA_NAME}}

| Agente | Contribuicao |
|--------|--------------|
| **pesquisa_agent** | Dados de mercado, tendencias |
| **marca_agent** | Tom de voz, valores |
| **anuncio_agent** | Copy, gatilhos, CTAs |
| **codexa_agent** | Estrutura, templates |
| **mentor_agent** | Onboarding, tutoriais |
| **photo_agent** | Descricoes visuais |

---

## DOCUMENTOS RELACIONADOS

- [VISION.md](./VISION.md) - Visao completa e arquitetura
- [UX_IMPROVEMENTS.md](./UX_IMPROVEMENTS.md) - Melhorias de interface
- [knowledge/core/identidade.md](./knowledge/core/identidade.md) - Identidade fixa
- [templates/variaveis.md](./templates/variaveis.md) - Sistema de variaveis

---

## COMANDOS

```bash
# Primar agente (futuro)
/prime-persona

# Ver status
/{{persona_cmd}}-status

# Testar resposta
/{{persona_cmd}}-test "{{EXAMPLE_USER_MESSAGE}}"
```

---

**"{{PERSONA_PHILOSOPHY}}"**
*-- {{PERSONA_NAME}}, {{PERSONA_ROLE}} {{BRAND_NAME}}*
