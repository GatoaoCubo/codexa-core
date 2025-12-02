# ⚙️ COMANDOS AVANÇADOS CODEXA

**Documentação completa dos comandos disponíveis no sistema.**

---

## 📋 ÍNDICE DE COMANDOS

| Categoria | Comandos |
|-----------|----------|
| Navegação | `/prime`, `/help` |
| Agentes | `/prime-anuncio`, `/prime-pesquisa`, `/prime-marca`, `/prime-photo`, `/prime-mentor`, `/prime-codexa` |
| Construção | `/codexa-build_agent`, `/codexa-build_prompt` |
| Utilitários | `/codexa-when_to_use`, `/progress` |

---

## 🧭 COMANDOS DE NAVEGAÇÃO

### `/prime`

**Propósito**: Dashboard principal do sistema. Mostra status e comandos disponíveis.

**Quando usar**:
- Ao iniciar uma sessão
- Para verificar se o sistema está funcionando
- Para ver lista de agentes disponíveis

**Saída esperada**:
```
╔═══════════════════════════════════════╗
║     CODEXA SYSTEM NAVIGATOR v2.5      ║
╚═══════════════════════════════════════╝

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

---

### `/help`

**Propósito**: Ajuda geral do Claude Code (não específico CODEXA).

**Quando usar**: Para comandos nativos do Claude Code.

---

## 🤖 COMANDOS DE AGENTES

### `/prime-anuncio`

**Propósito**: Carrega contexto especializado em criação de anúncios.

**O que carrega**:
- 91 arquivos de conhecimento de e-commerce
- Compliance rules (ANVISA, INMETRO, Procon)
- Frameworks de copywriting (PAS, AIDA, StoryBrand)
- Templates de anúncio para 9 marketplaces

**Quando usar**:
- Criar anúncios para marketplaces
- Otimizar anúncios existentes
- Validar compliance

**Exemplo de uso**:
```
/prime-anuncio

Crie um anúncio para:
- Produto: Garrafa térmica 500ml
- Marketplace: Mercado Livre
- Preço: R$ 89,90
- Diferencial: Mantém 24h gelada
```

---

### `/prime-pesquisa`

**Propósito**: Carrega contexto de análise de mercado e concorrência.

**O que carrega**:
- 700+ URLs de marketplaces testadas
- Frameworks de análise (Gap Analysis, Blue Ocean)
- Templates de pesquisa (Quick, Standard, Comprehensive)
- SEO taxonomy builder

**Quando usar**:
- Analisar concorrência
- Identificar tendências
- Definir preços
- Encontrar gaps de mercado

**Workflows disponíveis**:
```
Quick (15-20min): Overview rápido
Standard (30-40min): Análise completa
Comprehensive (60min+): Deep dive
```

---

### `/prime-marca`

**Propósito**: Carrega contexto de branding e identidade de marca.

**O que carrega**:
- 12 Arquétipos de Marca (Jung)
- Frameworks de posicionamento
- Psicologia de cores
- Templates de brand guidelines

**Quando usar**:
- Criar identidade de marca
- Definir posicionamento
- Desenvolver tom de voz
- Criar paleta de cores

**Output típico**:
```
- Arquétipos definidos
- Posicionamento escrito
- Tom de voz (4 dimensões)
- Paleta de cores
- Brand guidelines
```

---

### `/prime-photo`

**Propósito**: Carrega contexto de geração de imagens com IA.

**O que carrega**:
- 12 perfis de câmera
- 7 estilos fotográficos
- Requisitos de 9 marketplaces
- Templates de prompt para imagem

**Quando usar**:
- Gerar fotos de produtos
- Criar grids (3x3, 2x2)
- Adaptar imagens para marketplaces

**Parâmetros técnicos suportados**:
```
Camera: Canon, Sony, Fuji, etc.
ISO: 100-400
Aperture: f/2.8-f/8
Style: Minimalist, Dramatic, Lifestyle, etc.
```

---

### `/prime-mentor`

**Propósito**: Carrega contexto de ensino e suporte.

**O que carrega**:
- Documentação completa do sistema
- FAQ e troubleshooting
- Glossário de termos
- Materiais de estudo

**Quando usar**:
- Tirar dúvidas sobre o sistema
- Pedir explicações de conceitos
- Validar se você está no caminho certo

**Diferencial**: Usa "Seller-First Language" - explica em termos simples.

---

### `/prime-codexa`

**Propósito**: Carrega contexto de meta-construção (criar agentes).

**O que carrega**:
- 12 Pontos de Alavancagem
- Templates de agente
- Estrutura de HOPs e ADWs
- Builders e validators

**Quando usar**:
- Criar novos agentes
- Entender arquitetura do sistema
- Contribuir com o projeto

**Nível**: Avançado (requer Módulo 6)

---

## 🏗️ COMANDOS DE CONSTRUÇÃO

### `/codexa-build_agent`

**Propósito**: Assistente para criar um novo agente do zero.

**Prerequisito**: Ter executado `/prime-codexa` antes.

**Workflow**:
1. Define nome e propósito do agente
2. Identifica conhecimento necessário
3. Cria estrutura de pastas
4. Gera PRIME.md
5. Popula iso_vectorstore

**Exemplo**:
```
/codexa-build_agent

Nome: eco_product_agent
Propósito: Conteúdo para produtos sustentáveis
Conhecimento: Certificações ambientais, claims permitidos
```

**Output**:
```
eco_product_agent/
├── PRIME.md
├── README.md
├── INSTRUCTIONS.md
└── iso_vectorstore/
    ├── 01_quick_start.md
    ├── 02_certificacoes.md
    └── ...
```

---

### `/codexa-build_prompt`

**Propósito**: Assistente para criar HOPs (Higher-Order Prompts).

**Prerequisito**: Ter executado `/prime-codexa` antes.

**Workflow**:
1. Define objetivo do prompt
2. Identifica variáveis (inputs)
3. Define output esperado
4. Estrutura em formato TAC-7

**Exemplo**:
```
/codexa-build_prompt

Objetivo: Gerar descrição de produto sustentável
Inputs: nome_produto, material, certificacao
Output: Descrição de 500 palavras
```

**Output** (formato TAC-7):
```markdown
# HOP: Descrição Produto Sustentável

## MODULE_METADATA
Type: HOP
Version: 1.0.0

## INPUT_CONTRACT
$nome_produto: string (required)
$material: string (required)
$certificacao: string (optional)

## OUTPUT_CONTRACT
Primary: descricao.md
Format: Markdown, 500 palavras

## TASK
Gerar descrição persuasiva para produto sustentável...
```

---

## 🔧 COMANDOS UTILITÁRIOS

### `/codexa-when_to_use`

**Propósito**: Árvore de decisão para escolher o agente certo.

**Output**:
```
🌳 ÁRVORE DE DECISÃO CODEXA

┌─ Preciso criar conteúdo de venda?
│  └─ Sim → /prime-anuncio
│
├─ Preciso entender o mercado?
│  └─ Sim → /prime-pesquisa
│
├─ Preciso definir identidade?
│  └─ Sim → /prime-marca
│
├─ Preciso de imagens?
│  └─ Sim → /prime-photo
│
├─ Tenho dúvidas?
│  └─ Sim → /prime-mentor
│
└─ Quero criar algo novo?
   └─ Sim → /prime-codexa
```

---

### `/progress`

**Propósito**: Mostra seu progresso no curso (XP, nível, achievements).

**Output**:
```
🎮 SEU PROGRESSO CODEXA
━━━━━━━━━━━━━━━━━━━━━
Level: APPRENTICE (2) 🔧
XP: 145/300
Progress: ████████░░ 48%

Módulos: 4/10 ✓
Achievements: 6/20

Próximo milestone: BUILDER (300 XP)
Faltam: 155 XP
```

---

## 📝 DICAS DE USO

### 1. Sempre comece com `/prime`
Verifica se o sistema está funcionando antes de carregar agentes.

### 2. Um agente por vez
Não misture contextos. Se estava em `/prime-anuncio` e precisa de pesquisa, execute `/prime-pesquisa` primeiro.

### 3. Seja específico nos prompts
```
❌ "Crie um anúncio"
✅ "Crie um anúncio para garrafa térmica 500ml, R$ 89,90, para Mercado Livre"
```

### 4. Use os workflows prontos
Cada agente tem workflows otimizados. Use-os em vez de inventar do zero.

### 5. Valide antes de publicar
Sempre peça validação de compliance antes de publicar anúncios.

---

## 🔗 REFERÊNCIA RÁPIDA

```
NAVEGAÇÃO
  /prime              Dashboard principal
  /help               Ajuda Claude Code

AGENTES
  /prime-anuncio      Criar anúncios
  /prime-pesquisa     Pesquisa de mercado
  /prime-marca        Branding
  /prime-photo        Fotos com IA
  /prime-mentor       Dúvidas e suporte
  /prime-codexa       Meta-construção

CONSTRUÇÃO (avançado)
  /codexa-build_agent    Criar agente
  /codexa-build_prompt   Criar HOP

UTILITÁRIOS
  /codexa-when_to_use    Árvore de decisão
  /progress              Ver progresso
```
