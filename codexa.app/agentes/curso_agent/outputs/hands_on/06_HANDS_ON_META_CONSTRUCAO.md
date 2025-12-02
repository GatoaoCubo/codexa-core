# Roteiro Hands-On: Módulo 06 - Meta-Construção

**Duração**: 20-25 minutos
**Formato**: Screencast com narração
**Objetivo**: Criar um agente customizado do zero

---

## SETUP DA TELA

```
┌─────────────────────────────────────────────────────────────┐
│  Claude Code (70%)         │  VS Code/Editor (30%)         │
│  ┌───────────────────────┐ │  ┌───────────────────────────┐│
│  │ Chat com CODEXA Agent │ │  │ Arquivos sendo criados   ││
│  └───────────────────────┘ │  └───────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

---

## ROTEIRO DE GRAVAÇÃO

### [00:00 - 02:00] Contexto

**NARRAÇÃO:**
> "Este é o módulo mais avançado do curso. Até agora você USOU os agentes. Agora vai CRIAR um. Vou construir um agente customizado do zero - um 'Email Agent' que escreve sequências de email marketing. E você vai entender como o sistema CODEXA funciona por dentro."

**MOSTRAR OBJETIVO:**
```
OBJETIVO: Criar email_agent
FUNÇÃO: Gerar sequências de email marketing
CAPACIDADES:
- 6 tipos de email (boas-vindas, carrinho abandonado, etc)
- Templates com [OPEN_VARIABLES]
- Validação de subject lines
- A/B testing automático
```

---

### [02:00 - 04:00] Carregando o CODEXA Agent

**DIGITAR:**
```
/prime-codexa
```

**NARRAÇÃO:**
> "O CODEXA Agent é o arquiteto do sistema. Ele constrói outros agentes. Quando você executa esse comando, está ativando o modo de meta-construção."

**COMENTAR:**
> "Percebe que o contexto é diferente? São os 12 pontos de alavancagem, os templates, os padrões de arquitetura. Conhecimento sobre COMO construir, não sobre O QUE fazer."

---

### [04:00 - 08:00] Definindo a Arquitetura

**DIGITAR:**
```
Quero criar um novo agente: email_agent

PROPÓSITO:
Gerar sequências de email marketing para e-commerce brasileiro

CAPACIDADES:
- Criar 6 tipos de email:
  1. Boas-vindas
  2. Carrinho abandonado
  3. Pós-compra
  4. Reengajamento
  5. Lançamento
  6. Promocional

- Cada email com:
  - Subject line otimizada
  - Preview text
  - Corpo do email
  - CTA claro

- Validação:
  - Subject lines testadas
  - Spam words check
  - Mobile preview

Gera a estrutura de arquivos seguindo o padrão CODEXA.
```

**COMENTAR OUTPUT:**
> "Olha a estrutura que ele criou. Segue o padrão fractal do CODEXA: PRIME.md, README.md, iso_vectorstore, prompts, validators. Mesma arquitetura dos outros agentes."

**DESTACAR:**
```
email_agent/
├── PRIME.md (instruções principais)
├── README.md (quick start)
├── iso_vectorstore/
│   ├── 01_email_types.md
│   ├── 02_subject_formulas.md
│   ├── 03_spam_words.md
│   └── ...
├── prompts/
│   ├── HOP_email_sequence.md
│   └── HOP_subject_generator.md
└── validators/
    └── spam_check_validator.py
```

---

### [08:00 - 12:00] Criando o PRIME.md

**DIGITAR:**
```
Agora gera o PRIME.md completo para o email_agent.

Inclui:
- Seção Purpose
- 4 IN-AGENT pillars (Context, Model, Prompt, Tools)
- Workflows disponíveis
- Exemplos de uso
- Quality gates
```

**MOSTRAR OUTPUT (parcial) E COMENTAR:**
> "Veja o PRIME.md sendo criado. Tem a mesma estrutura dos outros agentes: Purpose claro, arquitetura definida, workflows documentados. Isso é Template Your Engineering em ação."

**DESTACAR SEÇÃO:**
```markdown
## 🎯 PURPOSE
Email Agent: Gerador de sequências de email marketing
otimizado para e-commerce brasileiro.

Provides: Email sequences | Subject line optimization |
Spam check | A/B variants | Mobile preview

## 🤖 WHEN TO USE
Use `/prime-email` when:
- Creating welcome sequences
- Recovering abandoned carts
- Launching new products
- Reactivating dormant customers
```

---

### [12:00 - 16:00] Criando um HOP (Higher-Order Prompt)

**DIGITAR:**
```
Cria o HOP para geração de sequência de carrinho abandonado.

Segue o TAC-7 framework:
1. CONTEXT - O que o agente precisa saber
2. INPUT_CONTRACT - Parâmetros de entrada
3. OUTPUT_CONTRACT - Formato de saída
4. PROMPT_BODY - Instruções principais
5. EXAMPLES - Pelo menos 2 exemplos
6. VALIDATION - Como validar output
7. META - Versão, autor, etc
```

**COMENTAR OUTPUT:**
> "Isso é um HOP - Higher-Order Prompt. É um template de prompt que aceita parâmetros. Você passa o nome do produto, preço, e ele gera toda a sequência customizada."

**DESTACAR INPUT_CONTRACT:**
```markdown
## INPUT_CONTRACT
$product_name: string (required) - Nome do produto abandonado
$product_price: number (required) - Preço em R$
$customer_name: string (optional) - Nome do cliente
$cart_items: number (optional) - Qtd de itens no carrinho
$brand_tone: enum ["casual", "formal", "urgente"] (default: "casual")
```

---

### [16:00 - 19:00] Testando o Agente

**NARRAÇÃO:**
> "Agora vou testar o agente que acabei de criar."

**DIGITAR:**
```
Carrega o email_agent e gera uma sequência de carrinho abandonado:

PRODUTO: Tênis Nike Air Max
PREÇO: R$ 599,90
CLIENTE: João
ITENS NO CARRINHO: 1
TOM: casual-urgente
```

**COMENTAR OUTPUT:**
> "Olha a sequência: 3 emails, espaçados em 1h, 24h e 72h. Subject lines testadas, corpo persuasivo, CTAs claros. E tudo seguindo as regras que definimos no PRIME."

**MOSTRAR EMAILS:**
```
EMAIL 1 (1h após abandono):
Subject: João, você esqueceu algo 👟
Preview: Seu Nike Air Max tá esperando...

EMAIL 2 (24h após):
Subject: Últimas unidades do seu tênis
Preview: O estoque tá acabando, João

EMAIL 3 (72h após):
Subject: 10% OFF só pra você finalizar
Preview: Cupom exclusivo de recuperação
```

---

### [19:00 - 21:00] Validando com Quality Gate

**DIGITAR:**
```
Roda validação completa:
- Spam words check
- Subject line score (1-10)
- Mobile preview ok?
- CTA clarity score
```

**COMENTAR:**
> "Todos os emails passaram no spam check. Subject lines com score 8.5/10 em média. Mobile preview ok. CTA clarity 9/10. Pronto pra usar."

---

### [21:00 - 23:00] Reflexão: Os 12 Pontos

**NARRAÇÃO:**
> "O que acabamos de fazer? Usamos os 12 pontos de alavancagem:"

**MOSTRAR NA TELA:**
```
PONTOS USADOS:
✓ 12. Context - Conhecimento de email marketing
✓ 10. Prompt  - HOPs com TAC-7
✓ 6.  Documentation - PRIME.md, README
✓ 5.  Tests - Validators de spam/quality
✓ 4.  Architecture - Estrutura fractal
✓ 2.  Templates - HOPs reutilizáveis
✓ 1.  ADWs - Workflow de geração

RESULTADO: Agente funcional em 20 minutos
```

**NARRAÇÃO:**
> "Isso é meta-construção. Você não escreveu código complexo. Você ORQUESTROU a criação de um sistema usando templates e padrões."

---

### [23:00 - 24:00] Encerramento

**NARRAÇÃO:**
> "Você acabou de criar um agente do zero. Não copiou, não baixou pronto - CONSTRUIU. Isso é o poder do CODEXA: não é só usar IA, é criar SEUS PRÓPRIOS sistemas de IA."

**MOSTRAR NA TELA:**
```
AGENTE CRIADO:
✓ email_agent funcional
✓ 6 tipos de email
✓ HOPs reutilizáveis
✓ Validators ativos
✓ Documentação completa

VOCÊ AGORA É: BUILDER (Level 3)
PRÓXIMO NÍVEL: Criar agentes que criam agentes
```

---

## SCRIPT DE TROUBLESHOOTING

**Se o agente não funcionar:**
```
O agente criado não está respondendo corretamente.
Verifica:
1. PRIME.md está completo?
2. iso_vectorstore tem os arquivos?
3. Comando /prime-email existe?
```

**Se quiser adicionar capacidade:**
```
Quero que o email_agent também faça:
- Segmentação por comportamento
- Personalização por histórico de compra

Expande o PRIME.md e cria novos HOPs.
```

**Se quiser integrar com outros agentes:**
```
Como faço pra Anuncio Agent usar os emails que Email Agent cria?
Cria um workflow de integração.
```

---

## NOTA PARA O INSTRUTOR

Este hands-on é o mais longo e complexo. Considere:
- Gravar em 2 partes se necessário
- Ter backup de arquivos pré-criados caso algo falhe
- Mostrar resultado final mesmo se geração demorar

---

**Arquivo**: `outputs/hands_on/06_HANDS_ON_META_CONSTRUCAO.md`
**Criado**: 2025-11-25
**Versão**: 1.0.0
