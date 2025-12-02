# Diagramas Visuais - Modulo 0 Super Freemium

**Versao**: 1.0.0 | **Data**: 2025-11-29
**Uso**: Assets visuais para video de 10 min + landing page

---

## 1. DIAGRAMA: OS 4 CORES

**Momento no video**: 04:00-06:00
**Conceito**: Os 4 pilares de qualquer agente de IA

### Representacao ASCII

```
                    ┌─────────────────────────────────────┐
                    │           AGENTE DE IA              │
                    │    (Agentic AI / Sistema Autonomo)  │
                    └─────────────────────────────────────┘
                                     │
           ┌─────────────────────────┼─────────────────────────┐
           │                         │                         │
           v                         v                         v
    ┌─────────────┐          ┌─────────────┐          ┌─────────────┐
    │   MODEL     │          │   CONTEXT   │          │   PROMPT    │
    │  (Cerebro)  │          │(Conhecimento│          │  (Pedido)   │
    │             │          │Proprietario)│          │             │
    │  GPT-4      │          │             │          │ Estruturado │
    │  Claude     │          │  Sua marca  │          │    vs       │
    │  Gemini     │          │  Produto    │          │   Vago      │
    │             │          │  Tom voz    │          │             │
    └─────────────┘          └─────────────┘          └─────────────┘
           │                         │                         │
           │                         │                         │
           └─────────────────────────┼─────────────────────────┘
                                     │
                                     v
                            ┌─────────────┐
                            │   TOOLS     │
                            │  (As Maos)  │
                            │             │
                            │  Pesquisar  │
                            │  Criar      │
                            │  Analisar   │
                            └─────────────┘
```

### Especificacoes para Designer

| Elemento | Cor Sugerida | Icone |
|----------|--------------|-------|
| MODEL | Azul (#3B82F6) | Cerebro / Chip |
| CONTEXT | Verde (#10B981) | Pasta / Livro |
| PROMPT | Amarelo (#F59E0B) | Balao de fala |
| TOOLS | Roxo (#8B5CF6) | Engrenagem / Mao |
| Container AGENTE | Cinza escuro (#1F2937) | - |

### Texto para Cada Quadrante

**MODEL (Cerebro)**
```
O que: Qual LLM voce usa
Exemplos: GPT-4, Claude, Gemini
Define: Teto de inteligencia
Insight: "E commodity - todo mundo tem acesso"
```

**CONTEXT (Conhecimento Proprietario)**
```
O que: O que a LLM sabe sobre VOCE
Exemplos: Marca, produto, publico, tom de voz
Define: Diferenciacao
Insight: "E o que diferencia - PORTAVEL e REUTILIZAVEL"
```

**PROMPT (O Pedido)**
```
O que: Como voce instrui a LLM
Exemplos: Vago vs Estruturado
Define: Qualidade do output
Insight: "Vago = resultado vago"
```

**TOOLS (As Maos)**
```
O que: O que a LLM pode fazer
Exemplos: Pesquisar, criar, analisar
Define: Capacidades
Insight: "A LLM deixou de so falar - ela AGE"
```

### Animacao Sugerida

1. Aparecem os 4 quadrantes vazios
2. MODEL aparece primeiro (zoom in)
3. CONTEXT aparece (destaque verde - "o diferencial")
4. PROMPT aparece
5. TOOLS aparece
6. Setas conectam tudo ao centro "AGENTE"
7. Highlight final em CONTEXT: "Conhecimento Proprietario e o novo investimento"

---

## 2. DIAGRAMA: AS 3 CAMADAS

**Momento no video**: 06:00-07:30
**Conceito**: Piramide de uso de IA (onde voce esta vs onde deveria estar)

### Representacao ASCII

```
                              /\
                             /  \
                            /    \
                           / C3   \
                          /        \
                         / META-    \
                        / CONSTRUCAO \
                       /   (Agentic)  \
                      /________________\
                     /                  \
                    /        C2          \
                   /     AUTOMACAO        \
                  /       (SaaS)           \
                 /                          \
                /____________________________\
               /                              \
              /            C1                  \
             /         USUARIO                  \
            /       (Application)                \
           /                                      \
          /________________________________________\

         ────────────────────────────────────────────
         MAIORIA          <──────>          OBJETIVO
         ESTA AQUI                          CODEXA
```

### Versao Detalhada (3 Blocos)

```
┌─────────────────────────────────────────────────────────────────────┐
│  CAMADA 3: META-CONSTRUCAO (Agentic Layer)                         │
│  ─────────────────────────────────────────                         │
│  Voce cria o sistema → Sistema cria resultados → Voce supervisiona │
│                                                                     │
│  Caracteristicas:                                                   │
│  • Recursive Self-Improvement (RSI)                                 │
│  • Conhecimento e SEU (portavel)                                    │
│  • 1 template → 1000 resultados                                     │
│  • ATIVO que valoriza com tempo                                     │
│                                                                     │
│  Resultado: "1 anuncio em 5 minutos"                               │
└─────────────────────────────────────────────────────────────────────┘
                                 ▲
                                 │ OBJETIVO
                                 │
┌─────────────────────────────────────────────────────────────────────┐
│  CAMADA 2: AUTOMACAO (SaaS Layer)                                  │
│  ─────────────────────────────────                                 │
│  Voce usa SaaS → Zapier conecta → Output automatico                │
│                                                                     │
│  Problemas:                                                         │
│  • R$ 300-500/mes em assinaturas                                   │
│  • Output generico                                                  │
│  • Conhecimento fica com FORNECEDOR                                │
│                                                                     │
│  Dor: "Pago 10 assinaturas diferentes"                             │
└─────────────────────────────────────────────────────────────────────┘
                                 ▲
                                 │
                                 │
┌─────────────────────────────────────────────────────────────────────┐
│  CAMADA 1: USUARIO (Application Layer)                             │
│  ─────────────────────────────────────                             │
│  Voce escreve prompt → IA responde → Voce valida → Repete          │
│                                                                     │
│  Problemas:                                                         │
│  • Voce e o gargalo                                                │
│  • Nao escala                                                       │
│  • Trabalho repetitivo                                              │
│                                                                     │
│  Dor: "Gasto 2 horas pra criar 1 anuncio"                          │
└─────────────────────────────────────────────────────────────────────┘
                                 ▲
                                 │ MAIORIA AQUI
```

### Especificacoes para Designer

| Camada | Cor | Emocao |
|--------|-----|--------|
| C1 Usuario | Vermelho (#EF4444) | Frustrado, cansado |
| C2 Automacao | Amarelo (#F59E0B) | Confuso, gastando |
| C3 Meta | Verde (#10B981) | Confiante, no controle |

### Texto-Chave

**Axioma Visual**:
```
CAMADA 1-2: Voce ALUGA inteligencia
            Paga todo mes. Conhecimento fica com outro.

CAMADA 3:   Voce POSSUI inteligencia
            Investe uma vez. Ativo valoriza com tempo.
```

### Animacao Sugerida

1. Mostra piramide completa
2. Destaca C1 em vermelho: "Maioria esta aqui"
3. Mostra dor: "2 horas pra 1 anuncio"
4. Transicao para C2: "Tentam resolver com SaaS"
5. Mostra problema: "R$ 500/mes, output generico"
6. Zoom em C3: "Onde voce deveria estar"
7. Highlight verde: "ATIVO, nao aluguel"

---

## 3. DIAGRAMA: BIBLIOTECA DE ALEXANDRIA

**Momento no video**: 00:30-02:00
**Conceito**: Metafora para explicar o que e uma LLM

### Representacao ASCII

```
     BIBLIOTECA DE ALEXANDRIA              LLM (Large Language Model)
     (Mundo Antigo)                        (Mundo Digital)

     ┌───────────────────┐                 ┌───────────────────┐
     │  ╔═══════════════╗│                 │  ╔═══════════════╗│
     │  ║ PAPIRO PAPIRO ║│                 │  ║ Wikipedia     ║│
     │  ║ PAPIRO PAPIRO ║│                 │  ║ Livros        ║│
     │  ║ PAPIRO PAPIRO ║│    ═══════>     │  ║ Forums        ║│
     │  ║ PAPIRO PAPIRO ║│   "Comprimido"  │  ║ Codigo        ║│
     │  ║ PAPIRO PAPIRO ║│                 │  ║ Artigos       ║│
     │  ╚═══════════════╝│                 │  ╚═══════════════╝│
     │     📜📜📜📜📜     │                 │     💾 1TB        │
     └───────────────────┘                 └───────────────────┘

     "Todo conhecimento                    "Internet inteira
      do mundo antigo                       escaneada e comprimida
      num lugar"                            num arquivo"
```

### Versao Simplificada

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│     📚 BIBLIOTECA          ═══>         🧠 LLM                  │
│                                                                 │
│     Todo conhecimento               Internet comprimida         │
│     do mundo antigo                 em 1 terabyte               │
│                                                                 │
│     Sabia TUDO                      Sabe um pouco de TUDO       │
│     sobre o passado                                             │
│                                                                 │
│                    MAS NAO SABE NADA SOBRE VOCE                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Texto para Narrador

```
"Imagina a Biblioteca de Alexandria.
Todo conhecimento do mundo antigo num lugar.

Agora imagina que alguem escaneou a internet inteira -
Wikipedia, livros, forums, codigo, artigos -
e comprimiu em um arquivo de 1 terabyte.

Isso e uma LLM.

ChatGPT, Claude, Gemini...
Sao bibliotecas ambulantes.
Sabem um pouco de TUDO.

Mas nao sabem NADA sobre VOCE."
```

---

## 4. DIAGRAMA: ESTAGIARIO QUE FAZ

**Momento no video**: 02:00-04:00
**Conceito**: Evolucao de LLM para Agente (Tools/Function Calling)

### Representacao ASCII

```
ANTES (2022)                          DEPOIS (2023+)
LLM = Estagiario que FALA             AGENTE = Estagiario que FAZ

┌─────────────────────────┐           ┌─────────────────────────┐
│                         │           │                         │
│    👤 ────> 🤖          │           │    👤 ────> 🤖 ────> 🌐 │
│                         │           │              │          │
│  "Como faco isso?"      │           │  "Pesquisa   │          │
│                         │           │   concorrentes"         │
│    🤖 ────> 👤          │           │              v          │
│                         │           │           📊 📈 📋      │
│  "Faz assim..."         │           │                         │
│                         │           │  ELE PESQUISA, MONTA,   │
│  VOCE tem que fazer     │           │  ANALISA, ENTREGA       │
│                         │           │                         │
└─────────────────────────┘           └─────────────────────────┘

    ❌ So explica                         ✅ EXECUTA
    ❌ Voce faz o trabalho                ✅ Ele faz o trabalho
    ❌ Ferramenta                         ✅ Funcionario digital
```

### Evolucao em Timeline

```
2022                    2023                    2024
  │                       │                       │
  v                       v                       v
┌─────┐               ┌─────┐               ┌─────┐
│ LLM │──────────────>│TOOLS│──────────────>│AGENT│
│     │               │     │               │     │
│Texto│               │Acoes│               │Auto │
│ so  │               │     │               │nomo │
└─────┘               └─────┘               └─────┘
  │                       │                       │
  │                       │                       │
  v                       v                       v
"Responde"            "Age no mundo"         "Planeja e executa"
```

### Especificacoes para Designer

| Estado | Cor | Emocao |
|--------|-----|--------|
| ANTES | Cinza (#9CA3AF) | Limitado |
| DEPOIS | Verde (#10B981) | Capacitado |
| Seta evolucao | Azul (#3B82F6) | Progresso |

---

## 5. INFOGRAFICO: 3 QUICK WINS

**Momento no video**: 07:30-09:30
**Conceito**: O fluxo completo Delegacao → Supervisao → Ativo

### Representacao ASCII

```
┌─────────────────────────────────────────────────────────────────────┐
│                     3 QUICK WINS CODEXA                             │
│              De Usuario para Meta-Construtor em 5 min               │
└─────────────────────────────────────────────────────────────────────┘

     ┌──────────────────┐
     │  QW1: META-PROMPT│
     │    (Delegacao)   │
     │                  │
     │  "Voce e um      │
     │   construtor de  │
     │   prompts..."    │
     └────────┬─────────┘
              │
              │  IA faz perguntas
              │  IA entrega prompt estruturado
              │  Voce SALVA
              v
     ┌──────────────────┐
     │   QW2: PLAN      │
     │  (Supervisao)    │
     │                  │
     │  "Me mostra o    │
     │   plano antes    │
     │   de executar"   │
     └────────┬─────────┘
              │
              │  IA mostra etapas
              │  Voce VALIDA ou ajusta
              │  Voce APROVA
              v
     ┌──────────────────┐
     │  QW3: IMPLEMENT  │
     │     (Ativo)      │
     │                  │
     │  "Entrega em     │
     │   formato        │
     │   reutilizavel"  │
     └────────┬─────────┘
              │
              │  IA executa
              │  Voce SALVA como arquivo
              │
              v
     ┌──────────────────┐
     │   CONHECIMENTO   │
     │   PROPRIETARIO   │
     │                  │
     │  ✅ Portavel     │
     │  ✅ Reutilizavel │
     │  ✅ Seu pra sempre│
     └──────────────────┘
```

### Versao Cards Horizontais

```
┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐
│     1      │     │     2      │     │     3      │     │    ✓      │
│            │     │            │     │            │     │            │
│  META-     │ ──> │   PLAN     │ ──> │ IMPLEMENT  │ ──> │   ATIVO   │
│  PROMPT    │     │            │     │            │     │            │
│            │     │            │     │            │     │            │
│ Delegacao  │     │ Supervisao │     │  Criacao   │     │Proprietario│
│            │     │            │     │            │     │            │
│ "Constroi  │     │ "Mostra    │     │ "Entrega   │     │ Portavel   │
│  pra mim"  │     │  antes"    │     │  salvavel" │     │ Reutiliza  │
└────────────┘     └────────────┘     └────────────┘     └────────────┘
     🔨                 👁️                 📦               💎
   Builder           Validator          Executor           Asset
```

### Cores por Quick Win

| QW | Cor | Icone | Palavra-Chave |
|----|-----|-------|---------------|
| QW1 | Azul (#3B82F6) | Martelo/Construir | DELEGACAO |
| QW2 | Amarelo (#F59E0B) | Olho/Validar | SUPERVISAO |
| QW3 | Verde (#10B981) | Caixa/Entregar | ATIVO |
| Final | Roxo (#8B5CF6) | Diamante | PROPRIETARIO |

---

## 6. DIAGRAMA: CONHECIMENTO PORTAVEL

**Conceito**: Mostrar que o conhecimento funciona em qualquer LLM

### Representacao ASCII

```
┌─────────────────────────────────────────────────────────────────────┐
│                  CONHECIMENTO PROPRIETARIO                          │
│                     (Seu arquivo .md)                               │
└───────────────────────────┬─────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            v               v               v
      ┌──────────┐    ┌──────────┐    ┌──────────┐
      │          │    │          │    │          │
      │ ChatGPT  │    │  Claude  │    │  Gemini  │
      │    ✅    │    │    ✅    │    │    ✅    │
      │          │    │          │    │          │
      └──────────┘    └──────────┘    └──────────┘
            │               │               │
            v               v               v
      ┌──────────┐    ┌──────────┐    ┌──────────┐
      │  Mesmo   │    │  Mesmo   │    │  Mesmo   │
      │ resultado│    │ resultado│    │ resultado│
      │    🎯    │    │    🎯    │    │    🎯    │
      └──────────┘    └──────────┘    └──────────┘


        "E SEU. Nao da plataforma."
        "Funciona hoje, amanha, daqui 10 anos."
```

---

## 7. AXIOMA VISUAL: ATIVO vs ALUGUEL

**Conceito**: Contraste entre possuir vs alugar inteligencia

### Representacao ASCII

```
┌─────────────────────────────┐     ┌─────────────────────────────┐
│      ❌ ALUGUEL             │     │      ✅ ATIVO               │
│      (Camada 1-2)           │     │      (Camada 3)             │
├─────────────────────────────┤     ├─────────────────────────────┤
│                             │     │                             │
│  📅 Paga TODO mes           │     │  💰 Investe UMA vez         │
│                             │     │                             │
│  🔒 Conhecimento fica       │     │  🔓 Conhecimento e SEU      │
│     com fornecedor          │     │                             │
│                             │     │  📈 Ativo VALORIZA          │
│  📉 Dinheiro vai embora     │     │     com o tempo             │
│                             │     │                             │
│  🔄 Dependencia eterna      │     │  🚀 Liberdade total         │
│                             │     │                             │
└─────────────────────────────┘     └─────────────────────────────┘

         R$ 300-500/mes                    R$ 0 depois de criar
         Output generico                   Output personalizado
         Preso na plataforma               Portavel pra qualquer LLM
```

---

## USO DOS DIAGRAMAS

### No Video (10 min)

| Tempo | Diagrama | Duracao |
|-------|----------|---------|
| 00:30-02:00 | Biblioteca de Alexandria | 1:30 |
| 02:00-04:00 | Estagiario que Faz | 2:00 |
| 04:00-06:00 | 4 CORES | 2:00 |
| 06:00-07:30 | 3 Camadas | 1:30 |
| 07:30-09:30 | 3 Quick Wins | 2:00 |

### Na Landing Page

1. Hero: 3 Quick Wins (versao horizontal)
2. Secao "O Problema": 3 Camadas
3. Secao "A Solucao": 4 CORES
4. Secao "Portabilidade": Conhecimento Portavel
5. CTA: Ativo vs Aluguel

### Para Photo Agent / Canva

Cada diagrama acima pode ser convertido em:
- Slide de apresentacao
- Imagem para redes sociais
- Thumbnail de video
- Infografico para download

---

## PALETA DE CORES CODEXA

| Uso | Cor | Hex | RGB |
|-----|-----|-----|-----|
| Primaria (Acao) | Verde | #10B981 | 16, 185, 129 |
| Secundaria (Info) | Azul | #3B82F6 | 59, 130, 246 |
| Alerta (Atencao) | Amarelo | #F59E0B | 245, 158, 11 |
| Erro (Evitar) | Vermelho | #EF4444 | 239, 68, 68 |
| Premium | Roxo | #8B5CF6 | 139, 92, 246 |
| Texto | Cinza escuro | #1F2937 | 31, 41, 55 |
| Background | Cinza claro | #F3F4F6 | 243, 244, 246 |

---

**Versao**: 1.0.0
**Criado**: 2025-11-29
**Uso**: Video M0 Super Freemium + Landing Page + Social Media

---

> "Criar conhecimento especializado que qualquer LLM pode usar
> e o novo investimento."
