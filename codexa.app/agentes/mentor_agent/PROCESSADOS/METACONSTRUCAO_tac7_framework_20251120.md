# TAC-7 Framework: Como Documentar Procedimentos LLM-Legíveis

**Categoria**: metaconstrucao_frameworks
**Qualidade**: 0.92/1.00
**Data**: 20251120

## Conteúdo

### O Problema com Documentação Tradicional para LLMs

**Documentação humana típica**:
"Configure o sistema seguindo as melhores práticas. Ajuste conforme necessário. Consulte a documentação completa para detalhes."

**Resultado para LLM**: Total confusão. Sem informações acionáveis, referencias vagas, zero estrutura.

**TAC-7 resolve isso**: Framework de 7 componentes obrigatórios que torna documentação simultaneamente legível por humanos E processável por LLMs.

**Metáfora**: TAC-7 é o "JSON Schema" da documentação procedural. Estrutura rígida que força clareza.

### Os 7 Componentes Obrigatórios (TAC-7)

#### 1. **T**itle (Título)

**O que é**: Nome descritivo e único do procedimento.

**Regras**:
- ✅ Específico, não genérico ("Product Description Generator", não "Generator")
- ✅ Action-oriented (verbo + substantivo)
- ✅ Único no sistema (sem duplicação)

**Exemplo**:
```markdown
# HOP: Mercado Livre Ad Compliance Validator
```

#### 2. **A**udience (Audiência)

**O que é**: Para quem este procedimento é destinado.

**Regras**:
- ✅ Persona específica ("Sellers creating marketplace listings")
- ✅ Skill level explícito ("Intermediate users familiar with [PREREQUISITE]")
- ❌ NUNCA vago ("Everyone", "Users")

**Exemplo**:
```markdown
**Audience**: Brazilian e-commerce sellers publishing products on Mercado Livre,
with basic understanding of SEO and marketplace regulations.
Assumes user has product information ready (name, specs, photos).
```

#### 3. **C**ontext (Contexto)

**O que é**: QUANDO usar este procedimento. Triggers específicos.

**Regras**:
- ✅ Situações específicas que ativam este HOP
- ✅ Pré-condições obrigatórias
- ✅ "Se X, então use este HOP. Se Y, use HOP Z instead."

**Exemplo**:
```markdown
**Context**: Use this HOP when:
- ✅ You have completed product research (via /prime-pesquisa)
- ✅ Product category requires ANVISA or INMETRO compliance
- ✅ You need to validate ad copy BEFORE publishing to marketplace
- ❌ DON'T use if: Product is digital/services (different compliance rules)
```

#### 4. **T**ask (Tarefa)

**O que é**: O QUE este procedimento faz. Output esperado.

**Regras**:
- ✅ Descrever transformação: Input → Output
- ✅ Especificar formato exato do output
- ✅ Métricas de sucesso quantificáveis

**Exemplo**:
```markdown
**Task**: Generate SEO-optimized product description for Mercado Livre marketplace.

Input:
- Product name, specs, target audience, differentiators

Output (JSON):
{
  "titulo": "string (max 60 chars)",
  "descricao": "string (800-1200 chars, 3 paragraphs)",
  "bullets": ["string (8 items, benefit-focused)"],
  "keywords": ["string (10-15 long-tail keywords)"],
  "compliance_check": {"anvisa": bool, "inmetro": bool}
}

Success criteria:
- Title contains ≥3 primary keywords
- Description passes compliance validator
- Bullets start with benefits, not features
```

#### 5. **A**pproach (Abordagem)

**O que é**: COMO fazer a tarefa. Passo-a-passo executável.

**Regras**:
- ✅ Sequência numerada de etapas
- ✅ Cada etapa é atômica (não subdivisível)
- ✅ Sem ambiguidade (LLM pode executar sem clarificação)
- ✅ Incluir comandos/código quando aplicável

**Exemplo**:
```markdown
**Approach**:

1. **Keyword Research** (3 min)
   - Extract primary keywords from product name
   - Identify 5-7 secondary keywords from specs
   - Query search volume via [OPEN_VARIABLE: ferramenta_keywords]

2. **Compliance Check** (2 min)
   - IF product.category in ["saude", "alimentos", "cosmeticos"]:
     - Run ANVISA validator (regex patterns + prohibited terms)
   - IF product.category in ["eletronicos", "brinquedos"]:
     - Run INMETRO validator (certification requirements)

3. **Title Generation** (2 min)
   - Template: "[KEYWORD_1] [KEYWORD_2] [DIFFERENTIATOR] [SPECS]"
   - Validate: length ≤60 chars
   - Ensure: primary keyword in first 20 chars

4. **Description Writing** (5 min)
   - Paragraph 1: Problem + Solution (emotional hook)
   - Paragraph 2: Specifications (technical details)
   - Paragraph 3: Differentiators + CTA (why buy from you)
   - Apply StoryBrand framework: [LINK_TO_FRAMEWORK]

5. **Bullet Points** (2 min)
   - 8 bullets: 6 benefits + 2 specifications
   - Format: "[BENEFIT] - [specification]"
   - Example: "Economia de até 40% na conta de luz - Motor A+++"

6. **Validation** (1 min)
   - Run through checklist:
     ☐ All required fields present
     ☐ Character limits respected
     ☐ No prohibited terms (compliance)
     ☐ Keywords density 2-3% (not stuffing)

TOTAL TIME: ~15 minutes
```

#### 6. **C**onstraints (Restrições)

**O que é**: Limitações, regras que NUNCA devem ser violadas.

**Regras**:
- ✅ Hard limits (character counts, timing, budget)
- ✅ Prohibited actions ("NEVER do X")
- ✅ Edge cases treatment

**Exemplo**:
```markdown
**Constraints**:

**Hard Limits**:
- Título: EXACTLY ≤60 characters (ML truncates after)
- Descrição: 800-1200 characters (optimal SEO range)
- Bullets: EXACTLY 8 items (ML interface limit)
- Processing time: ≤60 seconds total (user patience threshold)

**Prohibited**:
- ❌ NEVER use superlatives without proof ("o melhor", "único no mundo")
- ❌ NEVER make health claims without ANVISA approval
- ❌ NEVER guarantee results ("você vai emagrecer")
- ❌ NEVER use competitor brand names in copy

**Edge Cases**:
- IF product name >40 chars → abbreviate in title, full name in description
- IF no differentiators provided → extract from specs or competitor comparison
- IF compliance check fails → HALT and request user clarification (don't guess)

**Dependencies**:
- Requires: /prime-pesquisa output (keywords, competitors)
- Optional: /prime-marca output (brand voice, tone)
```

#### 7. **E**xample (Exemplo)

**O que é**: Demonstração completa end-to-end.

**Regras**:
- ✅ Input real (não placeholder genérico)
- ✅ Processo passo-a-passo executado
- ✅ Output real completo
- ✅ Inclui edge cases quando relevante

**Exemplo**:
```markdown
**Example**: Cadeira Gamer "ErgoX Pro"

**INPUT**:
Product: Cadeira Gamer ErgoX Pro
Specs: Apoio lombar ajustável, reclinável 180°, couro sintético, 150kg
Target: Gamers 18-35 anos, classe B/C
Differentiator: Única com garantia 5 anos no mercado nacional
Price: R$ 1.299

**EXECUTION**:

Step 1 - Keyword Research:
Primary: "cadeira gamer"
Secondary: "cadeira gamer reclinável", "cadeira escritório ergonômica", "poltrona gamer"
Long-tail: "cadeira gamer suporte 150kg", "cadeira gamer garantia 5 anos"

Step 2 - Compliance Check:
Category: Móveis → No ANVISA/INMETRO specific requirements
Check "garantia 5 anos" → Legal (backed by manufacturer policy document)

Step 3 - Title Generation:
"Cadeira Gamer ErgoX Pro Reclinável 180° Lombar Suporte 150kg"
Validation: 59 chars ✅ | Primary keyword in first 20 chars ✅

Step 4 - Description Writing:
[... full description generated following paragraph structure ...]

Step 5 - Bullets:
- Conforto extremo durante 12h+ de jogatina - Apoio lombar ajustável
- Posicione como quiser - Reclinável até 180° para relaxar entre partidas
- Durabilidade profissional - Garantia incrível de 5 anos (líder no Brasil)
[... 5 more bullets ...]

Step 6 - Validation:
☑ All fields present
☑ Title: 59/60 chars
☑ Description: 1.087 chars (within 800-1200)
☑ No prohibited terms
☑ Keyword density: 2.4% ✅

**OUTPUT** (JSON):
{
  "titulo": "Cadeira Gamer ErgoX Pro Reclinável 180° Lombar Suporte 150kg",
  "descricao": "[full 1087-char description]",
  "bullets": [
    "Conforto extremo durante 12h+ de jogatina - Apoio lombar ajustável",
    "Posicione como quiser - Reclinável até 180° para relaxar entre partidas",
    "Durabilidade profissional - Garantia incrível de 5 anos (líder no Brasil)",
    "Suporta até 150kg com segurança - Estrutura reforçada testada",
    "Couro sintético premium - Fácil limpeza, resistente a manchas",
    "Rodinhas silenciosas - Não arranha o piso, mobilidade total",
    "Ajuste de altura pneumático - Encontre a ergonomia perfeita",
    "Design agressivo gamer - Vermelho/preto, estilo racing profissional"
  ],
  "keywords": [
    "cadeira gamer", "cadeira gamer reclinável", "cadeira escritório ergonômica",
    "cadeira gamer suporte 150kg", "cadeira gamer garantia 5 anos",
    "cadeira gamer couro", "poltrona gamer", "cadeira gamer ergonomica"
  ],
  "compliance_check": {"anvisa": false, "inmetro": false, "passed": true}
}

TOTAL TIME: 14 minutes
```

### Por Que TAC-7 Funciona (Neurociência do Aprendizado LLM)

**Problema dos LLMs**: Context window limitado força priorização. Sem estrutura, LLM "perde" informação crítica.

**TAC-7 resolve via**:

1. **Chunking cognitivo**: 7 componentes são límite humano de working memory (Miller's Law: 7±2 items)

2. **Hierarquia explícita**: LLM "sabe" que Constraints > Approach (não pode violar restrições mesmo que abordagem sugira)

3. **Redundância estratégica**: Example reforça o que Approach descreveu abstratamente

4. **Validação automática**: LLM pode auto-verificar se output cumpre Task + Constraints

5. **Composibilidade**: HOPs TAC-7 são "funções puras" — podem ser chainadas/orquestradas

### TAC-7 vs Outros Frameworks

**vs. Markdown genérico**:
- Markdown: Estrutura fraca, interpretação ambígua
- TAC-7: Estrutura rígida, zero ambiguidade

**vs. JSON Schema**:
- JSON: Ótimo para dados, ruim para procedimentos
- TAC-7: Híbrido (markdown legível + estrutura rígida)

**vs. SOAP (Software documentation)**:
- SOAP: Foco em interfaces técnicas
- TAC-7: Foco em procedimentos executáveis por LLMs

### Implementando TAC-7 na Prática

**Passo 1: Identifique procedimento repetível**
- Algo que você faz 5+ vezes com pequenas variações
- Tem input/output claramente definidos

**Passo 2: Escreva TAC-7 draft (30 min)**
- Siga template rigorosamente
- Não pule nenhum componente

**Passo 3: Teste com LLM (10 min)**
```
Aqui está um HOP TAC-7:
[COLE SEU HOP]

Execute este procedimento para:
[INPUT REAL]
```

**Passo 4: Refine baseado no output (15 min)**
- LLM errou? → Approach ou Constraints vagos
- LLM pulou etapas? → Approach não explícito o suficiente
- Output inconsistente? → Example não cobre variabilidade

**Passo 5: Valide com 5+ inputs diversos (20 min)**
- Edge cases, happy path, error cases
- Quality score deve ser ≥85% consistency

**TOTAL**: ~75 min para criar HOP production-ready

### Quality Checklist para HOPs TAC-7

✅ **Title**: Único no sistema? Action-oriented?
✅ **Audience**: Persona específica + skill level explícito?
✅ **Context**: Condições de ativação CLARAS? Quando NÃO usar também descrito?
✅ **Task**: Input/Output/Success criteria quantificáveis?
✅ **Approach**: Cada step é executável sem clarificação adicional?
✅ **Constraints**: Hard limits quantificados? Prohibited actions listados?
✅ **Example**: Input real, não placeholder? Mostra edge cases?

**VALIDAÇÃO FINAL**: LLM consegue executar HOP sem fazer perguntas adicionais? Se sim, TAC-7 está pronto.

### Anti-Patterns (Erros Comuns)

❌ **HOP muito genérico**: "Content Generator" (qual tipo de content? qual formato?)

❌ **Approach com subjectividade**: "Escreva um texto convincente" (o que é "convincente"?)

❌ **Constraints vagos**: "Seja breve" (quantos chars? palavras?)

❌ **Example com placeholders**: Input: "[PRODUTO]" (use input REAL)

❌ **Misturar múltiplas tasks**: HOP que faz 3 coisas diferentes (quebre em 3 HOPs)

### Ferramentas & Templates

**Template TAC-7 em Markdown**:
```markdown
# HOP: [TITULO_UNICO]

**Audience**: [persona específica]

**Context**: Use when:
- ✅ [condição 1]
- ✅ [condição 2]
- ❌ DON'T use if: [condição negativa]

**Task**: [O que faz]
Input: [formato input]
Output: [formato output]
Success: [critérios quantificáveis]

**Approach**:
1. [Step 1 - nome] (tempo estimado)
   - [substep executável]
   - [substep executável]
2. [Step 2 - nome] (tempo estimado)
   ...

**Constraints**:
- NEVER: [ações proibidas]
- LIMIT: [limites quantificados]
- IF edge_case: THEN [tratamento]

**Example**:
INPUT: [input real]
EXECUTION: [passo-a-passo]
OUTPUT: [output completo]
TIME: [tempo real]
```

**Versionamento**:
- Adicione campo `Version: X.Y.Z` no cabeçalho
- Track mudanças: `## Changelog: v1.0→1.1: Added [feature]`

---

**Tags**: tac7, framework, hop, meta-construcao, documentacao, llm-legivel
**Palavras-chave**: TAC-7, HOP, framework, procedimentos, LLM-legível, documentação
**Origem**: curso_agent/PRIME.md + 06_MODULO_META_CONSTRUCAO.md + iso_vectorstore/09_HOP_main.md
**Processado**: 20251120
