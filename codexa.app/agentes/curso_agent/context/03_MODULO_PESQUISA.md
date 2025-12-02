# 🔵 MÓDULO 3: Pesquisa de Mercado

**Duração**: 1-2 horas
**Nível**: Intermediário
**Comando**: `/prime-pesquisa`

**🎮 XP Disponível:** 40 XP total
- Complete módulo: +25 XP
- Execute `/prime-pesquisa`: +10 XP
- Complete análise competitiva: +5 XP

**🏆 Achievements Disponíveis:**
- 🔍 **"Market Detective"** (Bronze) - Complete primeira análise competitiva
- 💎 **"Gap Finder"** (Silver) - Identifique 3+ oportunidades de nicho

> 💡 **Sistema de Gamificação Ativo**
> Veja `00_GAMIFICATION_SYSTEM.md` para detalhes completos.

---

## 🎯 OBJETIVOS

- ✅ Analisar concorrência automaticamente
- ✅ Identificar tendências de produtos
- ✅ Definir estratégia de precificação
- ✅ Descobrir gaps de mercado
- ✅ Tomar decisões baseadas em dados

---

## 📖 CONTEÚDO

### 1. O Pesquisa Agent

**Capacidades:**
- Análise competitiva em 9 marketplaces brasileiros
- 700+ URLs testadas automaticamente
- Workflows de pesquisa (quick, standard, comprehensive)
- SEO taxonomy builder

**Ative:**
```
/prime-pesquisa
```

---

### 2. Tipos de Pesquisa

**Quick Research (15-20min):**
- Overview rápido do mercado
- Top 10 concorrentes
- Faixa de preços
- Principais features

**Standard Research (30-40min):**
- Análise competitiva completa
- Tendências de categoria
- Gaps de oportunidade
- Recomendações estratégicas

**Comprehensive (60min+):**
- Deep dive em nicho
- Análise de reviews
- Sazonalidade
- Forecast de demanda

---

### 3. Passo a Passo

**PASSO 1: Defina seu objetivo**
```
Exemplos:
- "Quero lançar produto X"
- "Preciso entender concorrência Y"
- "Busco nicho lucrativo em categoria Z"
```

**PASSO 2: Carregue contexto**
```
/prime-pesquisa
```

**PASSO 3: Solicite pesquisa**
```
"Faça uma pesquisa standard sobre garrafas térmicas
no Mercado Livre, analisando:
- Top 10 concorrentes
- Faixa de preços
- Features mais valorizadas
- Gaps de oportunidade"
```

---

### 4. Análise Competitiva

**O que analisar:**

1. **Posicionamento**
   - Como se posicionam?
   - Qual o diferencial?
   - Quem é o público?

2. **Preços**
   - Faixa dominante
   - Estratégias (premium, econômico)
   - Promoções frequentes

3. **Features**
   - Características mais destacadas
   - Tabela comparativa
   - O que falta no mercado

4. **Reviews**
   - O que clientes elogiam
   - O que reclamam
   - Oportunidades de melhoria

---

### 5. Identificando Oportunidades

**Gap Analysis:**

```
Concorrentes oferecem:
- Garrafa 500ml (básica)
- Mantém 12h gelada
- Preço R$ 50-70

Oportunidade:
- Garrafa 500ml + 750ml (2 tamanhos)
- Mantém 24h gelada
- Preço R$ 89 (premium justificado)
- Diferencial: tampa com infusor de frutas
```

**Blue Ocean Strategy:**
- O que TODOS fazem? (evite)
- O que NINGUÉM faz? (explore)
- O que você pode fazer MELHOR?

---

### 6. Precificação Estratégica

**Métodos:**

1. **Custo + Margem**
   ```
   Custo: R$ 30
   Margem desejada: 3x
   Preço: R$ 90
   ```

2. **Baseado em Concorrência**
   ```
   Concorrente A: R$ 85
   Concorrente B: R$ 95
   Seu preço: R$ 89 (meio-termo)
   ```

3. **Value-Based**
   ```
   Valor percebido: Alto
   Benefício único: 24h gelada
   Premium: +20% vs concorrência
   Preço: R$ 99
   ```

---

### 7. Tendências e Sazonalidade

**Google Trends + Marketplace Data:**

```
Jan-Mar: Baixa (inverno)
Abr-Jun: Média
Jul-Set: ALTA (academia, verão)
Out-Dez: Alta (presentes)
```

**Ação:**
- Estoque alto em Jun-Set
- Promoções em Jan-Mar
- Lançamentos em Ago

---

### 8. Exercícios

**Exercício 1: Análise Competitiva**
1. Escolha uma categoria
2. Execute `/prime-pesquisa`
3. Solicite análise de top 5 produtos
4. Monte tabela comparativa

**Exercício 2: Gap Finding**
1. Use a análise do exercício 1
2. Identifique 3 gaps de mercado
3. Valide com dados
4. Crie proposta de valor

**Exercício 3: Pricing Strategy**
1. Defina seus custos
2. Analise faixa de preços
3. Teste 3 estratégias
4. Escolha a melhor

---

## ⚙️ POR TRÁS DA CORTINA: Como o Pesquisa Agent Funciona

**O Pesquisa Agent não é "Google com IA".**

Ele é um **sistema de inteligência competitiva** automatizado.

**Os 4 Núcleos em Ação:**

1. **CONTEXT** (Ponto 12)
   - 700+ URLs de marketplaces brasileiros (testadas)
   - 9 marketplaces mapeados (ML, Amazon, Shopee, Magalu, etc)
   - Padrões de análise competitiva (Gap Analysis, Blue Ocean)
   - SEO taxonomy builder (automatiza categorização)

2. **MODEL** (Ponto 11)
   - Modo analítico para dados quantitativos
   - Modo estratégico para identificar oportunidades
   - Extended thinking para pesquisas comprehensive

3. **PROMPT** (Ponto 10)
   - 3 workflows: Quick (15min), Standard (30min), Comprehensive (60min)
   - Cada workflow tem suas próprias fases e quality gates
   - Output estruturado: .md (humano) + .llm.json (machine-readable)

4. **TOOLS** (Ponto 9)
   - Web scraping (respeitando robots.txt)
   - Price monitoring
   - Review sentiment analysis
   - Trend forecasting

**O Princípio: TEMPLATES > INSTANCES**

Pesquisa Agent não faz "uma pesquisa". Ele executa um **template de pesquisa** que você pode reusar infinitamente.

Quick Research = Template para validação rápida
Standard Research = Template para decisão informada
Comprehensive = Template para deep dive estratégico

> 📘 **Axioma: Template Your Engineering**
>
> _"Criar templates para sua engenharia transforma fluxos de trabalho e boas práticas em unidades reutilizáveis e escaláveis de sucesso agentivo."_
>
> **Regra de Scaling:**
> ```
> 1x TEMPLATE → ~5x PLANOS → ~10x RESULTADOS
> ```
>
> **Como funciona:**
> - Invista esforço **uma vez** em template de alta qualidade
> - Reuse o template para criar **múltiplos planos**
> - Cada plano produz **múltiplos resultados valiosos**
>
> **Por que é poderoso:**
> - Codificar padrões de resolução de problemas em templates cria uma **biblioteca viva** de expertise
> - Agentes executam esses templates com **alta precisão** em muitos conjuntos de problemas
> - Todo novo template **fortalece o sistema** que permite agentes resolverem e melhorarem com cada execução
>
> **Daily Actions:**
> - ✅ Converter prompts bem-sucedidos em templates reusáveis
> - ✅ Documentar padrões específicos do domínio
> - ✅ Versionar templates como código
> - ✅ Revisar e refinar templates baseado em resultados

**Feedback Loop: Ask → Validate → Resolve**

Quando Pesquisa Agent encontra dados conflitantes:
1. Identifica discrepância
2. Busca fonte adicional
3. Valida com terceira fonte
4. Entrega conclusão fundamentada

Isso é **quality assurance automática**.

**Composable Primitives:**

Pesquisa Agent + Anuncio Agent = Anúncio data-driven
Pesquisa Agent + Marca Agent = Posicionamento fundamentado
Pesquisa Agent + Photo Agent = Imagens que convertem (baseadas em análise)

**Preview do Módulo 6:**

Você vai aprender que "workflows" não são fixos. São **composable agentic primitives** - blocos LEGO que você pode combinar de infinitas formas.

Por enquanto, use os workflows prontos. Mas perceba: você está usando **ferramentas de estrategista**, não só "perguntando pra IA".

---

## 🎉 CONCLUSÃO

Você aprendeu a:
- ✅ Pesquisar mercado profissionalmente
- ✅ Analisar concorrência com dados
- ✅ Identificar oportunidades
- ✅ Definir preços estrategicamente

---

## 🎮 XP SUMMARY

**XP Ganho neste módulo:**
- Completou módulo: +25 XP
- Executou `/prime-pesquisa`: +10 XP
- Análise competitiva completa: +5 XP
**Total:** +40 XP

**Seu Status Após Módulo 3:**
- Level: **APPRENTICE** (Level 2)
- Total XP: 185/300
- Progress: ██████░░░░ 62%

**Achievements Desbloqueados:**
- 🔍 **"Market Detective"** - Primeira análise competitiva completa
- 💎 **"Gap Finder"** - Identificou 3+ oportunidades de nicho

**Próximo**: Módulo 4 - Estratégia de Marca (+50 XP disponível)

---

**Criado com ❤️ pelo time CODEXA**
