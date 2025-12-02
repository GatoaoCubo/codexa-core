# Guia Completo: Mentor Agent

**Seu Professor Particular de IA para E-commerce**

---

## O QUE É O MENTOR AGENT?

O Mentor Agent é diferente dos outros 5 agentes. Enquanto eles **fazem** coisas (criar anúncios, pesquisar, etc), o Mentor **ensina** e **valida**.

```
┌─────────────────────────────────────────────────────────────┐
│ OUTROS AGENTES = EXECUTORES                                 │
│ - Anuncio Agent CRIA anúncios                              │
│ - Pesquisa Agent ANALISA mercado                           │
│ - Marca Agent DESENVOLVE identidade                        │
│ - Photo Agent GERA imagens                                 │
│ - CODEXA Agent CONSTRÓI sistemas                           │
├─────────────────────────────────────────────────────────────┤
│ MENTOR AGENT = PROFESSOR + COACH + VALIDADOR               │
│ - ENSINA como usar os outros agentes                       │
│ - VALIDA se o output está bom                              │
│ - RESOLVE problemas quando algo dá errado                  │
│ - PROCESSA seu conhecimento próprio                        │
│ - RESPONDE dúvidas sobre e-commerce                        │
└─────────────────────────────────────────────────────────────┘
```

---

## QUANDO USAR O MENTOR

### Use o Mentor quando:

| Situação | Exemplo |
|----------|---------|
| **Tem dúvida** | "O que é SEO de marketplace?" |
| **Quer aprender** | "Me ensina sobre copywriting" |
| **Quer validar** | "Esse anúncio está bom?" |
| **Tem problema** | "Output ficou ruim, o que faço?" |
| **Quer plano** | "Por onde começo a usar CODEXA?" |
| **Não sabe qual agente** | "Quero fazer X, qual usar?" |

### NÃO use o Mentor quando:

| Situação | Use este ao invés |
|----------|-------------------|
| Criar anúncio | `/prime-anuncio` |
| Pesquisar mercado | `/prime-pesquisa` |
| Criar marca | `/prime-marca` |
| Gerar fotos | `/prime-photo` |
| Construir sistemas | `/prime-codexa` |

**Regra simples:** Se quer **fazer algo**, use agente especializado. Se quer **aprender/validar**, use Mentor.

---

## COMO O MENTOR FUNCIONA

### Arquitetura 3-em-1

```
┌─────────────────────────────────────────────────────────────┐
│                    MENTOR AGENT                             │
├──────────────────┬──────────────────┬───────────────────────┤
│ 1. SCOUT         │ 2. PROCESSOR     │ 3. TEACHER            │
│ (Descoberta)     │ (Processamento)  │ (Ensino)              │
├──────────────────┼──────────────────┼───────────────────────┤
│ Busca no         │ Transforma seu   │ Explica de forma      │
│ catálogo de      │ conhecimento     │ prática, com          │
│ conhecimento     │ em arquivos      │ exemplos BR           │
│ interno          │ estruturados     │                       │
└──────────────────┴──────────────────┴───────────────────────┘
```

### Fluxo de uma Pergunta

```
1. Você pergunta: "Como melhorar meu título no ML?"
         ↓
2. Scout busca no catalogo.json
         ↓
3. Encontra: marketplace_titulos_otimizacao.md
         ↓
4. Lê o arquivo de conhecimento
         ↓
5. Traduz para linguagem de seller
         ↓
6. Responde com exemplos práticos
```

---

## FUNCIONALIDADES PRINCIPAIS

### 1. TIRAR DÚVIDAS (Modo Scout)

O Mentor busca na base de conhecimento e responde.

**Comando:**
```
/prime-mentor

"O que é [conceito]?"
"Como funciona [processo]?"
"Por que devo usar [técnica]?"
```

**Exemplo:**
```
/prime-mentor

"O que são gatilhos mentais e como uso em anúncios?"
```

**O Mentor vai:**
1. Buscar arquivos sobre gatilhos mentais
2. Explicar os 7 principais gatilhos
3. Dar exemplos de cada um aplicado a anúncios
4. Mostrar antes/depois real

---

### 2. AULA AO VIVO (Modo Teacher)

Quando você quer aprender algo a fundo.

**Comando:**
```
/prime-mentor

"Me ensina sobre [tópico]"
```

**Formato da aula:**
```
📚 AULA AO VIVO: [Título]

🎯 POR QUE ISSO IMPORTA?
[Impacto no seu negócio]

📖 OS 3-5 PILARES ESSENCIAIS
[Conceitos-chave explicados]

🛠️ COMO FAZER (PASSO-A-PASSO)
[Instruções práticas]

💡 EXEMPLO REAL
Antes: [situação ruim]
Depois: [situação melhorada]
Resultado: [métrica tangível]

✏️ EXERCÍCIO PRA VOCÊ
[Tarefa para aplicar]

🔗 PRÓXIMOS PASSOS
[O que estudar depois]
```

---

### 3. VALIDAÇÃO (Modo Coach)

Quando você quer feedback sobre algo que fez.

**Comando:**
```
/prime-mentor

"Valida esse [anúncio/pesquisa/marca]:

[Cole seu trabalho]

Quero saber:
- Score de 0-10
- O que está bom
- O que precisa melhorar"
```

**O Mentor vai:**
1. Analisar usando critérios profissionais
2. Dar nota justificada
3. Apontar pontos fortes
4. Sugerir melhorias específicas
5. Dar versão melhorada se necessário

---

### 4. PROCESSAMENTO DE CONHECIMENTO

Você pode adicionar seu próprio conhecimento.

**Como funciona:**

```
SEU CONHECIMENTO                    MENTOR PROCESSA
┌─────────────────┐                ┌─────────────────┐
│ - PDFs          │                │ Extrai conteúdo │
│ - Anotações     │  ───────────►  │ Estrutura em MD │
│ - Transcrições  │                │ Cataloga        │
│ - Links         │                │ Indexa          │
└─────────────────┘                └─────────────────┘
                                           │
                                           ▼
                                   ┌─────────────────┐
                                   │ PRONTO PARA     │
                                   │ CONSULTA        │
                                   │ (Scout encontra)│
                                   └─────────────────┘
```

**Comando:**
```
/prime-mentor

"Processa esse conteúdo:

[Cole o conteúdo - texto, transcrição, etc]

Categoria: [marketplace/copywriting/branding/etc]
Assunto: [específico]"
```

---

## TOM DE VOZ DO MENTOR

O Mentor fala como um **mentor experiente**, não como professor acadêmico.

### ✅ COMO O MENTOR FALA:

```
"Olha só, vou te mostrar um macete que funciona direto..."

"Isso aqui já vi dar certo em 100+ lojas..."

"No ML, SEO é basicamente título + keywords. Te explico..."

"Cara, esse é um erro clássico. Vou te mostrar como evitar..."

"Funciona assim: primeiro você [passo], depois [passo]..."
```

### ❌ COMO O MENTOR NÃO FALA:

```
"Conforme a literatura acadêmica sugere..."

"Implementar uma estratégia multifacetada de otimização..."

"De acordo com as melhores práticas metodológicas..."

"A análise epistemológica do conceito indica..."
```

---

## INTEGRAÇÃO COM OUTROS AGENTES

O Mentor não compete com outros agentes - ele **complementa**.

### Fluxo Recomendado:

```
1. DÚVIDA? → /prime-mentor (aprende)
        ↓
2. FAZ → /prime-[agente] (executa)
        ↓
3. VALIDA → /prime-mentor (feedback)
        ↓
4. AJUSTA → /prime-[agente] (refina)
        ↓
5. APRENDE → /prime-mentor (registra o que funcionou)
```

### Exemplo Prático:

```
1. "Mentor, me ensina sobre SEO de título"
   → Mentor explica conceitos

2. /prime-anuncio → Cria anúncio

3. "Mentor, valida esse título que criei"
   → Mentor dá nota 7/10, sugere melhoria

4. /prime-anuncio → Ajusta título

5. "Mentor, funcionou! Como registro isso?"
   → Mentor processa como conhecimento seu
```

---

## PERGUNTAS FREQUENTES

### "O Mentor substitui os outros agentes?"

**Não.** Cada agente tem especialidade. Mentor ensina e valida, não executa.

### "Posso usar só o Mentor?"

**Pode**, mas vai ser menos eficiente. Os agentes especializados são otimizados para suas tarefas.

### "O Mentor sabe tudo?"

Ele sabe o que está no **catálogo de conhecimento** (91 arquivos). Para conhecimento novo, você precisa processar.

### "Como adiciono conhecimento meu?"

Use o comando de processamento ou adicione arquivos na pasta RASCUNHO do mentor_agent.

### "O Mentor pode errar?"

**Sim.** Sempre valide informações críticas. Mentor é assistente, não substitui seu julgamento.

---

## COMANDOS RÁPIDOS

| Quero... | Comando |
|----------|---------|
| Tirar dúvida | "O que é [X]?" |
| Aula completa | "Me ensina sobre [X]" |
| Validar trabalho | "Valida isso: [conteúdo]" |
| Resolver problema | "Tô com problema: [descreva]" |
| Saber qual agente | "Quero fazer [X], qual agente?" |
| Processar conteúdo | "Processa isso: [conteúdo]" |
| Plano de ação | "Monta plano pra [objetivo]" |
| Comparar opções | "A ou B, qual melhor pra [contexto]?" |

---

## RESUMO

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  MENTOR AGENT = Seu professor particular de e-commerce       │
│                                                              │
│  ENSINA: Conceitos, técnicas, estratégias                   │
│  VALIDA: Qualidade do que você produziu                     │
│  RESOLVE: Problemas quando algo dá errado                   │
│  PROCESSA: Transforma seu conhecimento em base consultável  │
│                                                              │
│  COMANDO: /prime-mentor                                      │
│  TOM: Mentor experiente, prático, sem academicismo          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

**Arquivo**: `outputs/extras/GUIA_MENTOR_AGENT.md`
**Criado**: 2025-11-25
**Usar como**: Anexo do Módulo 01 ou Material Complementar
