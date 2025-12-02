# Prompt Engineering: Da Mediocridade à Maestria

**Categoria**: llm_prompting
**Qualidade**: 0.91/1.00
**Data**: 20251120

## Conteúdo

### Por Que Prompt Engineering Importa Mais Que o Modelo

**Verdade inconveniente**: Um GPT-3.5 com prompt excelente derrota um GPT-4 com prompt medíocre em 70% das tarefas.

**Por quê**: LLMs são "pattern completion engines". Quanto melhor você estrutura o padrão de entrada (prompt), melhor o padrão de saída (output). O modelo é secundário.

**Analogia**: Imagine pedir direções para um local. "Me leva lá" vs "Preciso chegar na Rua X, 123, bairro Y, próximo ao ponto de referência Z, prefiro rota sem pedágios". Mesma pessoa dando direções, resultados drasticamente diferentes.

### Os 7 Princípios Fundamentais

#### 1. **Seja Explícito, Não Implícito**

❌ **Ruim**: "Escreva sobre e-commerce"
✅ **Bom**: "Escreva um guia de 800 palavras sobre otimização de títulos de produtos no Mercado Livre, incluindo 3 exemplos reais de antes/depois e foco em keywords long-tail para SEO"

**Regra**: Se um humano precisaria de clarificação, o LLM também precisa.

#### 2. **Forneça Contexto Estratificado**

Estrutura de prompt ideal:
```
[PAPEL] Você é [especialista em X com Y anos de experiência]
[TAREFA] Sua missão é [objetivo específico]
[CONTEXTO] [Informação necessária para executar bem]
[FORMATO] Retorne no formato [estrutura desejada]
[CONSTRAINTS] Limitações: [restrições específicas]
[EXEMPLOS] Aqui estão 2 exemplos: [input→output samples]
```

#### 3. **Use Few-Shot Learning (2-5 Exemplos)**

Zero-shot (sem exemplos): 60-70% de acerto
Few-shot (2-3 exemplos): 85-95% de acerto

**Exemplo prático**:
```
Tarefa: Extrair keywords de descrição de produto.

Exemplo 1:
Input: "Camiseta masculina 100% algodão, manga curta, gola redonda"
Output: ["camiseta", "masculina", "algodão", "manga curta", "gola redonda"]

Exemplo 2:
Input: "Smartphone Samsung Galaxy S23, 128GB, 5G, câmera 50MP"
Output: ["smartphone", "Samsung", "Galaxy S23", "128GB", "5G", "câmera", "50MP"]

Agora extraia keywords de:
Input: "[SUA_DESCRIÇÃO]"
Output:
```

**Por quê funciona**: Exemplos "calibram" o modelo para o padrão exato que você quer.

#### 4. **Estruture o Output (Sempre)**

❌ **Ruim**: "Me dê insights sobre este produto"
✅ **Bom**: "Analise este produto e retorne JSON com esta estrutura exata:
```json
{
  "strengths": ["string"],
  "weaknesses": ["string"],
  "opportunities": ["string"],
  "threats": ["string"],
  "recommendation": "string (100 chars max)"
}
```
"

**Benefícios**:
- Reduz alucinação (formato restrito limita criatividade indevida)
- Facilita parsing automatizado
- Output consistente entre execuções

#### 5. **Chain-of-Thought (Pense Passo-a-Passo)**

Para tarefas complexas, peça ao LLM para "mostrar o raciocínio":

```
[OPEN_VARIABLE: tarefa_complexa]

Antes de responder, pense passo-a-passo:
1. Qual é o problema central?
2. Quais fatores preciso considerar?
3. Qual abordagem faz mais sentido?
4. Qual é minha resposta final?

Formato:
<thinking>
[Raciocínio aqui]
</thinking>

<answer>
[Resposta final aqui]
</answer>
```

**Ganho**: +15-25% de acurácia em problemas que exigem lógica multi-etapa.

#### 6. **Negativa Prompting (Diga O Que NÃO Fazer)**

Além de instruir o que fazer, instrua o que evitar:

```
Escreva descrição de produto para marketplace.

✅ FAÇA:
- Use linguagem persuasiva mas factual
- Inclua especificações técnicas
- Destaque diferenciais competitivos

❌ NÃO FAÇA:
- Não use superlativos exagerados ("o melhor do mundo")
- Não faça claims de saúde não verificados
- Não use emojis em excesso (máx 2)
- Não escreva parágrafos >150 caracteres
```

#### 7. **Iterate com Feedback Loop**

Primeiro prompt raramente é perfeito. Processo iterativo:

```
Versão 1 → Teste → Identifique falhas → Refine prompt
Versão 2 → Teste → Melhore +20% → Refine prompt
Versão 3 → Teste → Melhore +10% → Prompt production-ready
```

**Anti-pattern comum**: Escrever mega-prompt complexo tentando acertar tudo de primeira. Resultado: prompt confuso que ninguém entende.

**Melhor approach**: Começar simples, adicionar complexidade incrementalmente onde necessário.

### Patterns Avançados

#### Pattern 1: **Persona Injection**

```
Você é [PERSONA] com estas características:
- [OPEN_VARIABLE: experiencia_anos] anos de experiência em [DOMINIO]
- Especialista em [ESPECIALIDADE_1], [ESPECIALIDADE_2], [ESPECIALIDADE_3]
- Trabalhou em [CONTEXTO_RELEVANTE]
- Seu estilo de comunicação é [TOM_VOZ]

Agora, como [PERSONA], [TAREFA].
```

**Exemplo real (CODEXA Anuncio Agent)**:
```
Você é um copywriter sênior especializado em marketplaces brasileiros,
com 10+ anos de experiência em Mercado Livre, Shopee e Amazon BR.
Você domina SEO de marketplace, compliance ANVISA/INMETRO, e gatilhos
mentais aplicados a e-commerce B2C.

Seu tom: persuasivo mas factual, direto, sem hype exagerado.

Agora escreva anúncio para: [PRODUTO]
```

**Ganho**: +10-20% em qualidade percebida e alinhamento de tom.

#### Pattern 2: **Constrained Generation**

Força o LLM a operar sob constraints explícitos:

```
Tarefa: Resuma este artigo.

Constraints RÍGIDOS:
- Exatamente 3 parágrafos (não 2, não 4)
- Cada parágrafo: 80-120 palavras
- Primeira frase de cada parágrafo deve ser negrito
- Última frase de cada parágrafo deve conectar ao próximo
- Não use bullet points ou listas
- Nível de leitura: 8º ano (simplicidade)

[ARTIGO]
```

**Benefício**: Output altamente previsível, fácil de integrar em sistemas automatizados.

#### Pattern 3: **Role-Play Dialog**

Para tarefas de análise ou crítica, crie diálogo entre papéis:

```
Simule conversa entre 3 especialistas analisando [TOPICO]:

Expert 1 (Otimista): Argumenta pontos positivos
Expert 2 (Cético): Levanta objeções e riscos
Expert 3 (Pragmático): Avalia trade-offs e propõe síntese

Formato:
Expert 1: [argumento]
Expert 2: [contra-argumento]
Expert 3: [síntese]

[Repita 2-3 rodadas]

Conclusão Final: [consenso dos 3]
```

**Ganho**: Análises mais balanceadas, menos viés, explora múltiplas perspectivas.

#### Pattern 4: **Meta-Prompting (Prompt que Gera Prompts)**

Útil para criar prompts customizados para casos específicos:

```
Você é um especialista em prompt engineering.

Gere um prompt otimizado para a seguinte tarefa:
[OPEN_VARIABLE: descricao_tarefa]

O prompt deve:
- Incluir papel, contexto, tarefa, formato, constraints
- Ter 2 exemplos few-shot
- Ser <500 tokens
- Maximizar clareza e especificidade

Output:
```

**Benefício**: Automação de criação de prompts para novos domínios.

### Debugging de Prompts (Quando Outputs Falham)

**Problema**: Output inconsistente, alucinação, formato errado

**Checklist de diagnóstico**:

1. **Ambiguidade**: Há múltiplas interpretações razoáveis do seu prompt?
   - Fix: Seja mais específico, adicione exemplos

2. **Falta de contexto**: O LLM tem informação suficiente?
   - Fix: Adicione background, defina termos ambíguos

3. **Constraints vagas**: "Seja breve" é vago. "80-120 palavras" é específico.
   - Fix: Quantifique limites sempre que possível

4. **Exemplos ruins**: Few-shot examples não representam variabilidade real
   - Fix: Use exemplos de edge cases, não só casos ideais

5. **Overloading**: Pedindo 10 coisas diferentes em um único prompt
   - Fix: Quebre em múltiplos prompts sequenciais

### Anti-Patterns (O Que Não Fazer)

❌ **Prompt Novels**: Prompts de 2000+ tokens raramente performam melhor que 300-500 tokens bem escritos

❌ **Vagueness Composta**: "Seja criativo mas profissional e inovador mas tradicional"

❌ **Exemplos Contraditórios**: Few-shot examples que seguem padrões inconsistentes

❌ **Implicit Assumptions**: Assumir que LLM "sabe" o que você quer sem explicitar

❌ **No Validation**: Rodar prompt em produção sem testar em 10-20 samples primeiro

### Ferramentas para Prompt Engineering

**Desenvolvimento**:
- [OPEN_VARIABLE: ferramenta_prompt_dev] (ex: PromptLayer, Helicone)
- [OPEN_VARIABLE: ferramenta_versioning] (ex: Git + markdown, LangSmith)

**Testing**:
- [OPEN_VARIABLE: ferramenta_eval] (ex: pytest + LLM-as-judge, Braintrust)

**Monitoramento Produção**:
- [OPEN_VARIABLE: ferramenta_observability] (ex: LangSmith, Weights & Biases)

### Métricas de Qualidade

**Sucesso de prompt mede-se por**:

1. **Consistency**: Mesmo input → outputs similares (≥85% similarity)
2. **Compliance**: Output segue formato/constraints (≥95%)
3. **Quality Score**: Humano ou LLM-judge rating (≥8/10)
4. **Task Completion**: Resolve o problema do usuário (≥90%)

### Exemplo Completo: Antes e Depois

**ANTES (Prompt Medíocre)**:
```
Escreva um anúncio para uma cadeira gamer.
```

**Output**: Genérico, sem SEO, 50% de chance de violar limites de caracteres ML.

**DEPOIS (Prompt Otimizado)**:
```
Você é um copywriter especializado em Mercado Livre com 10+ anos de experiência.

Tarefa: Escreva anúncio para cadeira gamer seguindo especificações exatas do ML.

Produto:
- Marca: [MARCA]
- Modelo: [MODELO]
- Características: [LISTA_CARACTERÍSTICAS]
- Público-alvo: Gamers 18-35 anos, classe B/C
- Diferencial: [DIFERENCIAL_COMPETITIVO]

Formato OBRIGATÓRIO:
{
  "titulo": "string (max 60 chars, keywords prioritários no início)",
  "descricao": "string (800-1200 chars, 3 parágrafos)",
  "bullets": ["string (max 8 items, começar com benefício)"],
  "keywords": ["string (10-15 keywords long-tail)"]
}

Constraints:
- Não use: "o melhor", "único", "revolucionário"
- Inclua: especificações técnicas + benefícios emocionais
- SEO: keywords naturalmente integrados (não keyword stuffing)

Exemplo:
[EXEMPLO DE ANÚNCIO BEM FEITO]

Agora gere o anúncio:
```

**Output**: 95% pronto para publicar, otimizado SEO, compliance garantido.

**Diferença**: 5 min de prompt engineering = 5x qualidade de output.

---

**Tags**: prompting, prompt-engineering, llm, best-practices, few-shot, chain-of-thought
**Palavras-chave**: Prompt engineering, best practices, few-shot, chain-of-thought, patterns
**Origem**: curso_agent/PRIME.md + iso_vectorstore/frameworks + Módulo 6
**Processado**: 20251120
