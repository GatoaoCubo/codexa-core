# BEM-VINDO AO CODEXA - Guia do Aluno

**Parabens por adquirir o curso! Este guia vai te ajudar a aproveitar ao maximo.**

---

## COMO ESTE CURSO FUNCIONA

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SEU FLUXO DE APRENDIZADO                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   HOTMART                    +           CLAUDE CODE                │
│   ────────                              ────────────                │
│   Assistir videos                       Praticar comandos           │
│   Ler workbooks                         Criar anuncios reais        │
│   Fazer exercicios                      Tirar duvidas com IA        │
│                                                                     │
│   ┌─────────────┐                       ┌─────────────┐             │
│   │  Teoria +   │  ───────────────────► │  Pratica +  │             │
│   │  Conceitos  │                       │  Resultados │             │
│   └─────────────┘                       └─────────────┘             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Este curso e diferente**: Voce nao so assiste videos, voce PRATICA com a mesma ferramenta que os profissionais usam.

---

## CONFIGURACAO INICIAL (15 minutos)

### Passo 1: Instale o Claude Code

**Windows (PowerShell como Admin):**
```powershell
winget install Anthropic.ClaudeCode
```

**macOS:**
```bash
brew install claude-code
```

**Linux:**
```bash
curl -fsSL https://claude.ai/install.sh | sh
```

**Verificacao:** Execute `claude --version` - deve mostrar versao 1.0+

---

### Passo 2: Configure sua API Key

1. Acesse: https://console.anthropic.com/settings/keys
2. Crie uma conta (se nao tiver)
3. Clique em "Create Key"
4. Copie a chave (comeca com `sk-ant-`)
5. No terminal:

```bash
claude config set api_key sk-ant-SUA-CHAVE-AQUI
```

**Custo estimado:** R$ 50-150/mes para uso moderado (5-20 anuncios/dia)

---

### Passo 3: Clone o Repositorio CODEXA

```bash
git clone https://github.com/codexa-ai/lm.codexa.git
cd lm.codexa
```

---

### Passo 4: Abra no Claude Code

```bash
claude .
```

**Primeiro comando - teste se funciona:**
```
/prime
```

**Resultado esperado:**
```
╔═══════════════════════════════════════════════════════════════╗
║              CODEXA SYSTEM NAVIGATOR v2.5                     ║
╚═══════════════════════════════════════════════════════════════╝

📊 STATUS:
  Agents: 6 | Knowledge: 91 files | Commands: 14
  Core Files: ✅

🤖 DOMAIN AGENTS (Use /prime-* to load context)
  /prime-codexa     → Meta-construction
  /prime-anuncio    → E-commerce ads
  /prime-pesquisa   → Market research
  /prime-marca      → Brand strategy
  /prime-photo      → Product photos
  /prime-mentor     → Onboarding
```

**Se aparecer isso, PARABENS! Voce esta pronto.**

---

## ESCOLHA SUA TRILHA

### Trilha Quick Win (30 min) - "So quero testar"
```
M0.5: Quick Win
→ Crie seu primeiro anuncio em 30 minutos
→ XP: 50 | Achievement: "First Blood"
```

### Trilha Express (4-6h) - "Quero resultado rapido"
```
M0.5 → M2 → M5
→ Anuncios + Fotos = Produto pronto para vender
→ XP: 140 | Level: APPRENTICE
```

### Trilha Completa (15-20h) - "Quero dominar"
```
M0 → M0.5 → M1 → M2 → M3 → M4 → M5 → M6
→ Todos os agentes + Meta-construcao
→ XP: 475 | Level: BUILDER
```

### Trilha Builder (10-12h) - "Sou dev, quero criar agentes"
```
M1 → M6A → M6B → M6C
→ Foco em meta-construcao e arquitetura
→ XP: 345 | Level: ARCHITECT
```

---

## COMO ESTUDAR CADA MODULO

### Fluxo Recomendado:

```
1. ASSISTA o video no Hotmart (20-30 min)
         │
         ↓
2. ABRA o Claude Code
         │
         ↓
3. EXECUTE os comandos mostrados no video
         │
         ↓
4. FACA os exercicios praticos
         │
         ↓
5. VALIDE seu resultado (compliance, qualidade)
         │
         ↓
6. PERGUNTE ao curso_agent se tiver duvidas
```

### Exemplo - Modulo 2 (Anuncios):

**1. Assista o video no Hotmart**

**2. Abra Claude Code e carregue o agente:**
```
/prime-anuncio
```

**3. Crie seu primeiro anuncio:**
```
Crie um anuncio completo para o Mercado Livre:

Produto: [SEU PRODUTO REAL]
- Material: [MATERIAL]
- Preco: R$ [PRECO]
- Diferencial: [O QUE FAZ ELE ESPECIAL]

Inclua:
1. Titulo SEO (max 60 caracteres)
2. 5 bullet points
3. Descricao de 500 palavras
4. Validacao de compliance
```

**4. Revise o resultado e ajuste conforme necessario**

**5. Copie para seu marketplace e publique!**

---

## COMANDOS PRINCIPAIS

### Navegacao
| Comando | O que faz |
|---------|-----------|
| `/prime` | Dashboard do sistema |
| `/prime-anuncio` | Carrega agente de anuncios |
| `/prime-pesquisa` | Carrega agente de pesquisa |
| `/prime-marca` | Carrega agente de marca |
| `/prime-photo` | Carrega agente de fotos |
| `/prime-mentor` | Carrega agente de suporte |
| `/prime-codexa` | Carrega agente de meta-construcao |

### Ajuda
| Comando | O que faz |
|---------|-----------|
| `/prime-curso` | Carrega contexto do curso (para tirar duvidas) |
| `/help` | Ajuda geral do Claude Code |

---

## COMO TIRAR DUVIDAS COM O CURSO_AGENT

O curso_agent (eu!) conhece TODO o conteudo do curso. Voce pode perguntar:

### Duvidas sobre conteudo:
```
/prime-curso

"Estou no modulo 2, nao entendi o que e compliance.
Pode explicar com um exemplo pratico?"
```

### Duvidas sobre comandos:
```
/prime-curso

"Qual comando uso para criar fotos de produto?
E como configuro o estilo?"
```

### Pedir explicacao alternativa:
```
/prime-curso

"O video falou sobre os 12 pontos de alavancagem
mas nao entendi. Pode explicar de outro jeito?"
```

### Pedir exercicio extra:
```
/prime-curso

"Terminei o modulo 3, quero mais pratica.
Me da um exercicio extra de pesquisa de mercado."
```

---

## SISTEMA DE GAMIFICACAO

### Seus Niveis

| Level | Nome | XP Necessario | Como Chegar |
|-------|------|---------------|-------------|
| 1 | NOOB | 0-99 | Comecou o curso |
| 2 | APPRENTICE | 100-299 | Completou M1 + M2 |
| 3 | BUILDER | 300-599 | Completou M1-M5 |
| 4 | ARCHITECT | 600-999 | Completou M6 |
| 5 | META-GOD | 1000+ | Criou agente proprio |

### Como Ganhar XP

| Acao | XP |
|------|-----|
| Assistir video | +5 |
| Completar exercicio | +10-20 |
| Criar anuncio real | +15 |
| Passar em compliance | +10 |
| Completar modulo | +30-50 |
| Projeto EcoFlow completo | +260 |

### Achievements Iniciais

| Achievement | Como Desbloquear |
|-------------|------------------|
| "First Blood" | Primeiro anuncio criado |
| "Compliance Master" | 10 anuncios passaram compliance |
| "Multi-Platform" | Anuncio em 3 marketplaces |
| "Brand Builder" | Completou estrategia de marca |
| "Photo Pro" | Gerou 9-grid de fotos |

---

## PROJETO PRATICO: ECOFLOW

Apos completar os modulos basicos, faca o **Projeto EcoFlow** - um case completo que integra tudo:

```
PROJETO ECOFLOW
───────────────
Produto: Garrafa Termica Eco-Friendly
Diferencial: 50% materiais reciclados + 1 arvore por venda

FASES:
1. Pesquisa de Mercado (M3) → 40 XP
2. Identidade de Marca (M4) → 50 XP
3. Anuncios Multi-Marketplace (M2) → 50 XP
4. Fotos Profissionais (M5) → 40 XP
5. Agente Customizado (M6) → 80 XP

TOTAL: 260 XP + Achievement "EcoFlow Master"
```

Arquivo completo: `context/PROJETO_ECOFLOW.md`

---

## RESOLUCAO DE PROBLEMAS

### "Comando nao encontrado"
```bash
# Verifique se esta na pasta certa
pwd
# Deve mostrar: .../lm.codexa

# Se nao estiver:
cd lm.codexa
claude .
```

### "API key invalida"
```bash
# Reconfigure a key
claude config set api_key sk-ant-SUA-CHAVE

# Verifique saldo em:
# https://console.anthropic.com/settings/billing
```

### "/prime nao mostra nada"
```bash
# Tente recarregar
/help

# Se persistir, feche e abra novamente
exit
claude .
```

### "Erro de conexao"
1. Verifique sua internet
2. Verifique saldo da API
3. Tente novamente em 1 minuto

### "Anuncio ficou estranho"
```
/prime-anuncio

"O anuncio anterior ficou muito generico.
Refaca com foco em [BENEFICIO ESPECIFICO]
e tom mais [FORMAL/CASUAL]"
```

---

## DICAS DE OURO

### 1. Pratique com produtos reais
Nao use exemplos genericos. Use SEU produto de verdade.

### 2. Salve seus melhores prompts
Quando um prompt funcionar bem, salve em um arquivo:
```
meus_prompts/
├── anuncio_eletronicos.md
├── anuncio_moda.md
└── pesquisa_nicho.md
```

### 3. Use o compliance SEMPRE
Antes de publicar qualquer anuncio:
```
"Valide este anuncio para compliance ANVISA/INMETRO/Procon"
```

### 4. Itere, nao desista
Se o resultado nao ficou bom, ajuste o prompt:
```
"Refaca o titulo com mais foco em [X]"
"A descricao ficou longa, resuma para 300 palavras"
"Adicione mais urgencia no CTA"
```

### 5. Documente seu progresso
```
/progress
```
(Em breve: sistema automatico de tracking)

---

## ONDE ENCONTRAR AJUDA

### Dentro do curso:
- `/prime-curso` → Pergunte sobre qualquer modulo
- `/prime-mentor` → Suporte geral
- `context/FAQ.md` → Perguntas frequentes
- `context/GLOSSARIO.md` → Termos tecnicos

### Comunidade:
- Discord: [LINK_DISCORD]
- Telegram: [LINK_TELEGRAM]

### Suporte tecnico:
- Email: [EMAIL_SUPORTE]
- Hotmart: Area do aluno

---

## PROXIMO PASSO

**Se voce acabou de configurar tudo:**

1. Execute `/prime` para verificar que funciona
2. Va para o Hotmart e assista o video do Quick Win (M0.5)
3. Volte aqui e execute `/prime-anuncio`
4. Crie seu primeiro anuncio!

**Tempo total: 30 minutos para seu primeiro resultado.**

---

## MENSAGEM FINAL

Voce agora tem acesso a mesma tecnologia que agencias cobram R$ 5.000+/mes.

A diferenca entre quem tem resultado e quem nao tem e simples: **PRATICA**.

Cada anuncio que voce criar, cada pesquisa que fizer, cada marca que desenvolver - voce esta construindo habilidades que valem ouro no mercado.

**Bora comecar!**

Execute agora:
```
/prime
```

E veja seu cerebro IA ganhar vida.

---

**Versao**: 1.0.0
**Criado**: 2025-11-25
**Para**: Alunos do Curso CODEXA
