# CHEAT SHEET: CODEXA Agent (Meta-Construção)

**10 Prompts Prontos para Copiar e Usar**

---

## SETUP

```
/prime-codexa
```

---

## 1. CRIAR NOVO AGENTE

```
Cria novo agente: [nome]_agent

PROPÓSITO:
[Descreva em 1-2 frases o que o agente faz]

CAPACIDADES:
1. [Capacidade 1]
2. [Capacidade 2]
3. [Capacidade 3]

Gera estrutura completa:
- PRIME.md
- README.md
- iso_vectorstore/ com arquivos base
- Pelo menos 1 HOP
- Pelo menos 1 validator
```

---

## 2. CRIAR HOP (Higher-Order Prompt)

```
Cria HOP para [tarefa específica]:

Segue TAC-7 framework:

1. CONTEXT - O que o agente precisa saber
2. INPUT_CONTRACT - Parâmetros de entrada
3. OUTPUT_CONTRACT - Formato de saída
4. PROMPT_BODY - Instruções principais
5. EXAMPLES - 2 exemplos completos
6. VALIDATION - Como validar output
7. META - Versão, autor, data
```

---

## 3. CRIAR WORKFLOW (ADW)

```
Cria workflow de [X] fases:

NOME: ADW_[nome]
OBJETIVO: [o que o workflow faz]

Para cada fase:
- Nome da fase
- Input esperado
- Output gerado
- Quality gate (como validar)
- Próxima fase

Inclui $arguments chaining entre fases.
```

---

## 4. CRIAR VALIDATOR

```
Cria validator para [tipo de conteúdo]:

NOME: [nome]_validator

CHECKS:
1. [Regra 1] - peso: [X]%
2. [Regra 2] - peso: [X]%
3. [Regra 3] - peso: [X]%

OUTPUT:
- Score total (0-10)
- Pass/Fail (threshold: [X])
- Lista de issues encontrados
- Sugestões de fix
```

---

## 5. EXPANDIR AGENTE EXISTENTE

```
Expande [nome]_agent com nova capacidade:

CAPACIDADE NOVA:
[Descreva o que quer adicionar]

Atualiza:
1. PRIME.md - adiciona seção
2. iso_vectorstore/ - novos arquivos de conhecimento
3. prompts/ - novo HOP se necessário
4. validators/ - ajusta validação

Mantém compatibilidade com capacidades existentes.
```

---

## 6. CRIAR TEMPLATE REUTILIZÁVEL

```
Cria template para [tipo de output]:

FORMATO:
[Descreva estrutura desejada]

VARIÁVEIS:
- $var1: [tipo] - [descrição]
- $var2: [tipo] - [descrição]
- $var3: [tipo] - [descrição]

ZONAS DE GERAÇÃO:
[Onde LLM preenche dinamicamente]

EXEMPLO PREENCHIDO:
[Mostre 1 exemplo completo]
```

---

## 7. CRIAR INTEGRAÇÃO ENTRE AGENTES

```
Cria integração entre [agent1] e [agent2]:

FLUXO:
1. [Agent1] gera [output1]
2. [Output1] vira input de [Agent2]
3. [Agent2] gera [output2]

IMPLEMENTA:
- $arguments chaining
- Formato compatível entre outputs/inputs
- Fallback se um agente falhar
- Log de execução
```

---

## 8. DIAGNOSTICAR AGENTE

```
Diagnostica problemas no [nome]_agent:

SINTOMA:
[Descreva o que está acontecendo]

ESPERADO:
[O que deveria acontecer]

Verifica:
1. PRIME.md completo?
2. iso_vectorstore/ tem conhecimento suficiente?
3. Comando /prime-[nome] configurado?
4. Conflitos com outros agentes?
5. Context pollution?

Me dá diagnóstico e correção.
```

---

## 9. OTIMIZAR PERFORMANCE

```
Otimiza [nome]_agent para velocidade:

ATUAL:
- Tempo de resposta: [X]s
- Tamanho do context: [X] tokens

OBJETIVO:
- Tempo: <[X]s
- Context: <[X] tokens

Sugere:
1. Arquivos para remover/consolidar
2. Prompts para encurtar
3. Conhecimento para cachear
4. Fases para paralelizar
```

---

## 10. DOCUMENTAR AGENTE

```
Gera documentação completa para [nome]_agent:

FORMATO:
1. README.md - Quick start (usuário)
2. INSTRUCTIONS.md - Guia operacional (AI)
3. ARCHITECTURE.md - Decisões técnicas (dev)
4. CHANGELOG.md - Histórico de versões

Cada arquivo deve ser autocontido.
Inclui exemplos práticos em cada seção.
```

---

## OS 12 PONTOS DE ALAVANCAGEM

```
IN-AGENT (Configure no início - 20%):
┌─────────────────────────────────────┐
│ 12. Context   - O que o agente sabe │
│ 11. Model     - Capacidade de razão │
│ 10. Prompt    - Como você instrui   │
│ 9.  Tools     - O que ele pode fazer│
└─────────────────────────────────────┘

OUT-AGENT (Construa sempre - 80%):
┌─────────────────────────────────────┐
│ 8. Standard Out  - Formato saída    │
│ 7. Types         - Fluxo de dados   │
│ 6. Documentation - Base conhecimento│
│ 5. Tests         - Auto-validação   │
│ 4. Architecture  - Padrões          │
│ 3. Plans         - Prompts massivos │
│ 2. Templates     - Prompts reusáveis│
│ 1. ADWs          - Workflows AFK ⭐ │
└─────────────────────────────────────┘
```

---

## ESTRUTURA PADRÃO DE AGENTE

```
[nome]_agent/
├── PRIME.md           ← Instruções principais
├── README.md          ← Quick start
├── INSTRUCTIONS.md    ← Guia AI
├── iso_vectorstore/   ← Conhecimento
│   ├── 01_conceitos.md
│   ├── 02_workflows.md
│   └── catalogo.json
├── prompts/           ← HOPs
│   └── HOP_[tarefa].md
├── validators/        ← Quality gates
│   └── [nome]_validator.py
└── workflows/         ← ADWs
    └── ADW_[nome].md
```

---

## QUICK FIXES

| Preciso de... | Comando |
|---------------|---------|
| Só estrutura | "Gera só árvore de arquivos, não conteúdo" |
| Agente simples | "Versão minimal: só PRIME + 1 HOP" |
| Copiar de outro | "Clona estrutura do [agente] com novo propósito" |
| Versionar | "Cria v2.0 mantendo v1.0 funcional" |
| Testar | "Gera 3 casos de teste para o agente" |

---

## REGRA DE OURO

```
┌──────────────────────────────────────────────────┐
│  TEMPLATE YOUR ENGINEERING                        │
│                                                  │
│  1 Template → 5 Plans → 10 Results               │
│                                                  │
│  Não resolva 1 problema.                         │
│  Construa sistema que resolve CLASSE de problemas│
└──────────────────────────────────────────────────┘
```

---

**Arquivo**: `outputs/cheat_sheets/CHEAT_SHEET_META_CONSTRUCAO.md`
**Imprimir**: 2 páginas frente/verso
