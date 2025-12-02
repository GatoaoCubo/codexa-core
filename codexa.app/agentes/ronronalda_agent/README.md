# ronronalda_agent | A Voz da Marca GATO3

> **Versao**: 0.1.0 (Em construcao)
> **Tipo**: Agente Central de Interacao Humana
> **Status**: Meta-construido por todos os agentes

---

## O QUE E RONRONALDA

**Ronronalda nao eh um chatbot. Eh a PERSONA da marca GATO3.**

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
| Nome | Ronronalda (Ro) |
| Profissao | Mentora felina |
| Experiencia | 15 anos em etologia aplicada |
| Filosofia | "Gato calmo, casa leve" |
| Abordagem | Observacao → Ajuste → Escolha |

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
ronronalda_agent/
├── README.md                    # Este arquivo
├── VISION.md                    # Visao completa do agente
├── UX_IMPROVEMENTS.md           # Melhorias de UX planejadas
│
├── knowledge/                   # Base de conhecimento
│   ├── core/
│   │   └── identidade.md        # Quem eh Ronronalda
│   ├── comportamentos/          # (a criar)
│   │   ├── arranhar.md
│   │   ├── xixi_fora.md
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

Ronronalda adapta respostas sem perder identidade:

```yaml
# Detectadas automaticamente
{CANAL}: site | whatsapp | email
{EMOCAO}: frustrado | ansioso | feliz
{ISSUE}: arranhar | xixi | vomito | estresse

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
- `src/components/RoChat.tsx` - Interface do chat
- `src/pages/RoPage.tsx` - Pagina /sac
- `src/hooks/useRonronalda.ts` - State management
- `src/lib/voice.ts` - Voz bidirecional

### Backend
- `supabase/functions/ronronalda-chat/` - AI principal
- `supabase/functions/ronronalda-recommendations/` - Produtos
- `supabase/functions/ronronalda-tts/` - Text-to-speech

### Inteligencia
- Modelo: Gemini 2.5 Flash (via Lovable AI)
- Voz: OpenAI TTS (nova)
- Deteccao: Regex + keywords

---

## ROADMAP

### v0.1 (Atual)
- [x] Chat funcional no site
- [x] Deteccao de 8 issues
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

## AGENTES QUE CONSTROEM RONRONALDA

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
/prime-ronronalda

# Ver status
/ro-status

# Testar resposta
/ro-test "Meu gato arranha o sofa"
```

---

**"Gato calmo, casa leve."**
*— Ronronalda, Mentora Felina GATO3*
