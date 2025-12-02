# 📚 LCM-AI: Seu Kit Completo de Construção
## Guia de Como Usar Cada Documento

---

## 📦 O Que Você Recebeu

Criei **4 documentos complementares** para você entender e executar o plano:

```
1. 📄 lcm-ai-visual-didatica.html      ← Leia PRIMEIRO (visual bonito)
2. 📖 lcm-ai-visual-didatica.md        ← Texto puro (todo lugar)
3. ⚙️  lcm-ai-estructura-pratica.md    ← Durante implementação (referência)
4. 🎯 lcm-ai-cheat-sheet.txt          ← Quick reference (console/parede)
```

---

## 🎬 Como Usar Cada Um (Meu Roteiro Recomendado)

### PASSO 1️⃣: Entender a Visão (15 minutos)

**👉 Abra:** `lcm-ai-visual-didatica.html`

- Abra em qualquer navegador
- Leia de cima para baixo
- Veja as animações ASCII (árvore, fluxo, antes/depois)
- **Objetivo:** Entender POR QUÊ cada camada existe

**Perguntas que responde:**
- Por que raízes, tronco, galhos, folhas, fruto?
- Como um documento vira Trinity?
- Por que isto escala?

---

### PASSO 2️⃣: Validar a Lógica (30 minutos)

**👉 Leia:** `lcm-ai-visual-didatica.md`

- Mesma informação que HTML, mas em Markdown
- Copie/cole para qualquer lugar (Obsidian, Notion, GitHub)
- Mais fácil para anotar seus próprios insights

**Perguntas que responde:**
- Como a metáfora traduz pra código?
- Qual é meu plano de 6 dias?
- OPÇÃO A, B ou C?

---

### PASSO 3️⃣: Referência Durante Coding (Durante semana 1)

**👉 Use:** `lcm-ai-estructura-pratica.md`

- Mantenha aberta enquanto codifica
- É YAML + exemplos JSON + pseudocódigo
- Quando pergunta "qual é a estrutura de -02_build/?" → busca aqui
- Quando precisa de exemplo de `meta.json` → copie daqui

**Seções úteis:**
- `ARQUITETURA EM YAML` ← Quando estruturar
- `EXEMPLO: Um Documento Passou` ← Entender fluxo real
- `EXEMPLO: trinity.meta.json` ← Copie como template
- `CONFIG.YAML` ← Pesos iniciais

---

### PASSO 4️⃣: Cheat Sheet (Ao lado do Terminal)

**👉 Cole na Parede/Segundo Monitor:** `lcm-ai-cheat-sheet.txt`

- ASCII art de tudo
- Respostas rápidas
- Quando esquece "qual é Dia 3?"

---

## 🗺️ Fluxo de Leitura Ideal

```
SEGUNDA (Dia 1)
├─ Manhã: Leia HTML (15 min) + MD (30 min)
├─ Tarde: Leia estructura-pratica.md (30 min)
└─ Final: Escaneie cheat-sheet.txt (5 min)
└─ RESULTADO: Entende TUDO

TERÇA (Dia 2)
├─ Abra estructura-pratica.md + código
├─ Copie ejemplos (.meta.json, config.yaml)
└─ Codifique core.py

QUARTA-SEXTA
├─ Consulte estructura-pratica.md conforme precisa
├─ Cheat-sheet.txt para respostas rápidas
└─ HTML/MD só se quiser reaprender conceito
```

---

## 🎯 Cada Documento Responde Diferentes Perguntas

### HTML (Didático Visual)
**Quando abrir:** "Preciso ENTENDER isto"

- ✅ Explica metáforas
- ✅ Mostra fluxos visuais
- ✅ Antes vs Depois
- ❌ Não tem detalhes técnicos completos
- ❌ Não é reference document

**Exemplo de pergunta:**
- "Por que 8 é infinito?"
- "Como o sistema aprende?"
- "Por que isto escala?"

---

### Markdown (Leitura Completa)
**Quando abrir:** "Preciso de tudo, mas em texto puro"

- ✅ Completo como HTML
- ✅ Copia pra qualquer lugar (GitHub, Notion, Obsidian)
- ✅ Busca fácil (Ctrl+F)
- ✅ Sem dependência de navegador

**Exemplo de pergunta:**
- "Qual é o plano de 6 dias mesmo?"
- "Como feedback loop funciona?"
- "Qual opção devo escolher?"

---

### Estructura (Prática Implementação)
**Quando abrir:** "Estou codificando AGORA"

- ✅ YAML estruturado
- ✅ Exemplos JSON reais
- ✅ Pseudocódigo comentado
- ✅ Templates para copiar/colar
- ❌ Não é para aprender conceitos
- ❌ É referência, não tutorial

**Exemplo de pergunta:**
- "Como estruturo -02_build/?"
- "Qual é o formato de .meta.json?"
- "Como config.yaml fica?"
- "Qual é a formula de routing_score?"

---

### Cheat Sheet (Quick Lookup)
**Quando abrir:** "Preciso de resposta em 5 segundos"

- ✅ ASCII art
- ✅ Uma folha só
- ✅ Tudo visual
- ✅ Cole na parede

**Exemplo de pergunta:**
- "Qual é Dia 2 mesmo?"
- "Quais são as 5 folhas?"
- "Como funciona Trinity?"

---

## 🔄 Fluxo de Referência (Durante Implementação)

```
Pergunta                    Qual arquivo consultar?
════════════════════════════════════════════════════════════════
"Entendo o conceito geral?"         → HTML ou Markdown (30 min)
"Qual é exatamente formato X?"      → Estructura-pratica.md
"Como funciona Y?"                  → Cheat-sheet.txt (ASCII)
"Tenho dúvida no conceito Z"        → Volta a HTML/Markdown
"Preciso de exemplo code real"      → Estructura-pratica.md
"Qual passo agora?"                 → Cheat-sheet.txt (Plano)
"Como feedback loop ajuda?"         → HTML ou Markdown
```

---

## 📋 Checklist: Você Está Pronto Para Começar?

```
☐ Abri HTML, entendi a visão geral
☐ Li Markdown, validei a lógica
☐ Escaneei estructura-pratica.md (pelo menos 2 seções)
☐ Salvei cheat-sheet.txt numa aba sempre aberta
☐ Tenho espaço em disco: /lcm-ai/ (comece com 5 GB)
☐ Tenho Python 3.8+ (para core.py)
☐ Escolhi: OPÇÃO A (code), B (design) ou C (híbrido)?
```

---

## 🚀 Começo REAL (Segunda-Feira)

### MANHÃ
```
09:00 - Abrir lcm-ai-visual-didatica.html
        Ler com calma, anotar insights
        [15 min]

09:15 - Abrir lcm-ai-visual-didatica.md
        Validar conceitos no seu próprio ritmo
        [30 min]

09:45 - Decidir: OPÇÃO A, B ou C?
        (Me chamar para confirmar)
        [5 min]
```

### TARDE
```
14:00 - Se OPÇÃO A ou C:
        Abrir lcm-ai-estructura-pratica.md
        Entender config.yaml + estrutura -02_build/
        [30 min]

14:30 - Terminal:
        mkdir -p lcm-ai/{...}
        touch config.yaml
        [5 min]

14:35 - Copiar estrutura básica de lcm-ai-estructura-pratica.md
        config.yaml preenchido com valores iniciais
        [15 min]

14:50 - Criar stubs de Skills (funções vazias em Python)
        [30 min]

15:20 - FIM DO DIA 1
        Você tem: Árvore estruturada + pesos iniciais + Skills vazios
```

---

## 💡 Dicas de Leitura

### Dica 1: Leia HTML em 2 Monitores
- Monitor 1: HTML aberto
- Monitor 2: Seu editor de código
- Vira de um lado pro outro
- Aprende visualmente enquanto prepara files

### Dica 2: Copie Exemplos do Estructura
- Toda vez que precisa de JSON/YAML
- Não reescreve do zero
- Copia do documento, adapta valores
- Mais rápido, menos erro

### Dica 3: Cheat-Sheet na Parede
- Imprima ou cole em Post-its
- Quando esquece "qual é prioridade 5?"
- Só olha lá, não precisa abrir arquivo

### Dica 4: Markdown no Obsidian/Notion
- Copie lcm-ai-visual-didatica.md completo
- Crie um "vault" só pra LCM-AI
- Adicione anotações suas conforme aprende
- Fica seu conhecimento "versionado"

---

## 📞 Quando Me Chamar (Próximos Passos)

**Depois que ler os 4 documentos, me fale:**

```
1. "Entendi a visão, quero começar"
   → Dou você os scripts prontos (OPÇÃO A)

2. "Quero validar minha versão do plano"
   → Refinamos o YAML juntos (OPÇÃO B)

3. "Estou preso em [seção específica]"
   → Ajudo com esse conceito

4. "Pronto dia 1, qual é dia 2?"
   → Guio você pelo fluxo
```

---

## 🎁 Bônus: Estrutura de Pastas Pronta (Copie e Cole)

```bash
#!/bin/bash
# Execute isto no terminal após entender tudo

mkdir -p lcm-ai/{00_∞_hub,skills,tests}
mkdir -p lcm-ai/{+01_intake,+02_route,+03_execute,+05_delivery,+08_feedback}
mkdir -p lcm-ai/{-01_capture,-02_build/-02B_units,-03_index,-05_storage,-08_backup}
mkdir -p lcm-ai/views/{by-domain,by-purpose,by-entity,by-date}

touch lcm-ai/00_∞_hub/core.py
touch lcm-ai/00_∞_hub/config.yaml
touch lcm-ai/00_∞_hub/system_prompt.md
touch lcm-ai/00_∞_hub/monitoring.jsonl

touch lcm-ai/skills/skill_synthesizer.py
touch lcm-ai/skills/skill_tokenizer.py
touch lcm-ai/skills/skill_purpose_extractor.py
touch lcm-ai/skills/skill_qa_generator.py
touch lcm-ai/skills/skill_evaluator.py

echo "✅ Árvore estruturada! Próximo: copiar config.yaml de estructura-pratica.md"
```

---

## 📊 Resumo Dos 4 Documentos

| Arquivo | Tipo | Tamanho | Quando | Mantém Aberto? |
|---------|------|---------|--------|-----------------|
| **HTML** | Didático | 20KB | Entender | Não (lê 1x) |
| **Markdown** | Completo | 15KB | Aprender | Sim (referência) |
| **Estructura** | Prático | 25KB | Codificar | **SIM** (sempre) |
| **Cheat** | Quick | 8KB | Buscar rápido | Sim (parede/aba) |

---

## 🎯 Meta Final

**Você quer:**
- [ ] Entender POR QUÊ cada layer existe
- [ ] Saber COMO começa dia 1
- [ ] Ter EXEMPLOS prontos pra copiar
- [ ] Resposta rápida quando esquece algo

**Você consegue tudo isto em:**
- ✅ HTML: visão
- ✅ Markdown: conhecimento
- ✅ Estructura: código
- ✅ Cheat: velocidade

---

## 🌳 Próximo Passo

1. Abra `lcm-ai-visual-didatica.html` em novo aba
2. Leia com calma
3. Me diga: entendeu a sacada da árvore?
4. Depois: OPÇÃO A, B ou C?

---

*Lembre-se: Você não está apenas aprendendo um sistema.*
*Você está aprendendo a CULTIVAR uma árvore viva.*

*E árvores crescem com paciência, água e luz.*
*Seus documentos são água. Seu código é luz. Começe segunda.*

🌱 → 🌳 → 🍎
