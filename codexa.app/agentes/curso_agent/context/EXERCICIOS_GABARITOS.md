# 📝 GABARITOS DOS EXERCÍCIOS

**Respostas esperadas para os exercícios de cada módulo.**

---

## MÓDULO 1: INTRODUÇÃO

### Exercício 1: Exploração Básica

**Tarefa**: Execute `/prime` e observe o dashboard.

**Resposta Esperada**:
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

**Verificação**:
- ✅ Conseguiu ver os 6 agentes? **Sim, listados em "DOMAIN AGENTS"**
- ✅ Status mostra "Core Files: ✅"? **Sim, na linha STATUS**
- ✅ Quantos comandos existem? **14 comandos**
- ✅ Quantos arquivos de conhecimento? **91 files**

---

### Exercício 2: Primeiro Contato com Agentes

**Tarefa**: Execute `/prime-anuncio` e depois `/prime-marca`. Compare os contextos.

**Resposta Esperada**:

Ao executar `/prime-anuncio`:
- Carrega contexto especializado em copywriting
- Menciona compliance ANVISA/INMETRO
- Fala sobre SEO de marketplace
- Pipeline de 7 fases

Ao executar `/prime-marca`:
- Carrega contexto de branding
- Menciona arquétipos de marca
- Fala sobre tom de voz
- Workflow de 8 fases

**Diferença Principal**:
> Cada `/prime-*` carrega conhecimento DIFERENTE para a mesma IA.
> É como trocar o "cérebro especialista" da IA.

---

### Exercício 3: Primeiro Anúncio

**Tarefa**: Crie um anúncio para garrafa de água reutilizável.

**Resposta Esperada** (exemplo):

```markdown
## TÍTULO
Garrafa Água Reutilizável 500ml Eco - Livre de BPA Esportes

## BULLET POINTS
• Material livre de BPA - segurança para sua saúde
• Capacidade 500ml - ideal para academia e escritório
• Design ergonômico - fácil de segurar durante exercícios
• Tampa com trava - evita vazamentos na bolsa
• Fácil de limpar - boca larga permite higienização completa

## COMPLIANCE CHECK
✅ Sem claims de saúde proibidos
✅ Informações técnicas verificáveis
✅ Adequado para marketplaces
```

---

## MÓDULO 2: ANÚNCIOS

### Exercício 1: Seu Primeiro Anúncio

**Tarefa**: Crie anúncio completo usando o template de brief.

**Critérios de Avaliação**:

| Critério | Pontuação |
|----------|-----------|
| Título tem palavra-chave principal | ✅/❌ |
| Título ≤ 60 caracteres | ✅/❌ |
| 5 bullet points com benefícios | ✅/❌ |
| Descrição usa storytelling | ✅/❌ |
| Compliance passou | ✅/❌ |

**Exemplo de Resposta CORRETA**:
```
Título: "Garrafa Térmica 500ml Inox - Mantém 24h Gelada" (50 chars) ✅
Bullet 1: Benefício (não feature) ✅
Compliance: Todos os checks verdes ✅
```

**Exemplo de Resposta INCORRETA**:
```
Título: "Garrafa de água muito boa para você comprar agora mesmo" (55 chars)
→ Problema: Não tem palavra-chave, muito genérico

Bullet 1: "Feita de aço inoxidável"
→ Problema: É feature, não benefício. Melhor: "Aço inoxidável premium - durabilidade garantida"
```

---

### Exercício 2: Comparação de Versões

**Tarefa**: Compare seu anúncio antigo com a versão do Anuncio Agent.

**O que observar**:

| Aspecto | Seu Anúncio | Versão CODEXA |
|---------|-------------|---------------|
| Título SEO | Provavelmente genérico | Palavra-chave + benefício |
| Bullets | Provavelmente features | Benefícios com números |
| Descrição | Provavelmente curta | Storytelling estruturado |
| Compliance | Manual ou inexistente | Automático |

---

### Exercício 3: Multi-Marketplace

**Tarefa**: Gere versões para ML, Amazon e Shopee.

**Diferenças Esperadas**:

| Aspecto | Mercado Livre | Amazon | Shopee |
|---------|---------------|--------|--------|
| Título | 60 chars max | 200 chars | 120 chars |
| Foco | Frete grátis | Reviews | Preço |
| Bullets | 5-7 | 5 | 3-5 |
| Descrição | 1000+ palavras | A+ Content | Curta |

---

## MÓDULO 3: PESQUISA

### Exercício 1: Análise Competitiva

**Tarefa**: Analise top 5 produtos de uma categoria.

**Resposta Esperada** (formato):

```markdown
## ANÁLISE COMPETITIVA: [Categoria]

### Top 5 Concorrentes

| # | Produto | Preço | Avaliação | Vendas/mês | Diferencial |
|---|---------|-------|-----------|------------|-------------|
| 1 | [Nome] | R$ XX | X.X★ | XXX | [Diferencial] |
| 2 | ... | ... | ... | ... | ... |

### Análise de Preços
- Média: R$ XX
- Mínimo: R$ XX
- Máximo: R$ XX
- Sua sugestão: R$ XX (justificativa)

### Features Mais Comuns
1. [Feature] - XX% dos concorrentes
2. [Feature] - XX% dos concorrentes
3. ...

### Gaps Identificados
1. [Gap] - Ninguém oferece X
2. [Gap] - Poucos mencionam Y
3. ...
```

---

### Exercício 2: Gap Finding

**Tarefa**: Identifique 3 gaps de mercado.

**O que é um GAP válido**:
- ✅ Algo que clientes reclamam mas nenhum concorrente oferece
- ✅ Feature popular em outro mercado mas ausente no BR
- ✅ Segmento de preço não atendido

**O que NÃO é um GAP válido**:
- ❌ "Ninguém vende produto X" (pode não ter demanda)
- ❌ "Concorrente não tem Instagram" (irrelevante para marketplace)

**Exemplo de GAP bem identificado**:
```
Gap: Nenhum concorrente oferece garantia estendida de 2 anos.
Evidência: 15% das avaliações negativas mencionam "quebrou rápido".
Oportunidade: Oferecer garantia de 2 anos como diferencial premium.
```

---

## MÓDULO 4: MARCA

### Exercício 1: Defina Seu Arquétipo

**Tarefa**: Escolha arquétipo primário + secundário.

**Resposta Esperada** (exemplo):

```markdown
## ARQUÉTIPOS ESCOLHIDOS

### Primário: O Cuidador
Justificativa: Nosso produto protege a saúde e o meio ambiente.
Características aplicáveis:
- Responsabilidade
- Proteção
- Confiança

### Secundário: O Explorador
Justificativa: Nosso público usa o produto em atividades outdoor.
Características aplicáveis:
- Liberdade
- Aventura
- Descoberta

### Como se manifesta na marca:
- Copy: "Proteja sua hidratação em qualquer aventura"
- Visual: Cores de natureza + imagens outdoor
- Tom: Acolhedor mas inspirador
```

---

### Exercício 2: Framework de Posicionamento

**Tarefa**: Escreva seu posicionamento usando o framework.

**Template**:
```
Para [público-alvo]
que [necessidade/problema],
[nome da marca] é [categoria]
que [benefício único].

Diferente de [concorrência],
nós [diferencial chave].
```

**Exemplo CORRETO**:
```
Para pessoas ativas e conscientes
que querem hidratação sustentável,
EcoFlow é a garrafa térmica
que mantém temperatura por 24h sem poluir.

Diferente das marcas tradicionais,
nós usamos 100% materiais reciclados
e plantamos 1 árvore por garrafa vendida.
```

**Exemplo INCORRETO** (e por quê):
```
Para todo mundo (muito amplo)
que quer uma garrafa boa (vago),
EcoFlow é uma garrafa (óbvio)
que é melhor que as outras (não específico).
```

---

## MÓDULO 5: FOTOS

### Exercício 1: 9-Grid

**Tarefa**: Planeje as 9 cenas do seu grid.

**Resposta Esperada**:

```markdown
## GRID 3x3 - [Produto]

| 1. Hero Shot | 2. Detalhe Material | 3. Vista Superior |
| 4. Lifestyle | 5. Escala | 6. Embalagem |
| 7. Lifestyle 2 | 8. Infográfico | 9. Detalhe |

### Cena 1: Hero Shot
- Ângulo: Frontal 45°
- Fundo: Branco puro
- Iluminação: Soft box
- Objetivo: Mostrar produto completo

### Cena 4: Lifestyle
- Contexto: Pessoa na academia
- Emoção: Energia, movimento
- Iluminação: Natural
- Objetivo: Mostrar uso real
```

---

### Exercício 2: Variação de Estilos

**Tarefa**: Gere mesmo produto em 3 estilos diferentes.

**Comparação Esperada**:

| Aspecto | Minimalist | Dramatic | Lifestyle |
|---------|------------|----------|-----------|
| Fundo | Branco/neutro | Escuro/gradiente | Ambiente real |
| Luz | Soft, difusa | Contraste alto | Natural |
| Foco | Produto isolado | Produto destacado | Produto em contexto |
| Emoção | Clean, moderno | Impactante | Autêntico |
| Uso | Hero shot | Anúncio premium | Social media |

---

## MÓDULO 6: META-CONSTRUÇÃO

### Exercício: Quiz dos 12 Pontos

**1. Qual é o ponto de MAIOR alavancagem?**
- [ ] Context
- [ ] Model
- [x] ADWs (AI Developer Workflows)
- [ ] Tools

**2. Os 4 IN-AGENT são:**
- [x] Context, Model, Prompt, Tools
- [ ] Plans, Templates, ADWs, Tests
- [ ] Documentation, Types, Standard Out, Architecture

**3. O que significa "Template Your Engineering"?**
- [ ] Usar templates de código
- [x] Criar soluções reutilizáveis que resolvem CLASSES de problemas
- [ ] Copiar templates de outros projetos

**4. O que é um HOP (Higher-Order Prompt)?**
- [ ] Um prompt muito longo
- [x] Um prompt que aceita outros prompts como parâmetros
- [ ] Um prompt de alta qualidade

**5. Qual a proporção ideal de tempo na camada agentiva?**
- [ ] 20%
- [x] 50% ou mais
- [ ] 100%

---

## 📊 CRITÉRIOS GERAIS DE AVALIAÇÃO

### Resposta EXCELENTE (10/10)
- ✅ Segue o formato pedido
- ✅ Inclui todos os elementos
- ✅ Mostra raciocínio/justificativa
- ✅ É específico, não genérico

### Resposta BOA (7-8/10)
- ✅ Segue o formato
- ✅ Inclui maioria dos elementos
- ⚠️ Algumas partes genéricas
- ⚠️ Falta justificativa

### Resposta INSUFICIENTE (<7/10)
- ❌ Não segue formato
- ❌ Faltam elementos
- ❌ Muito genérico
- ❌ Sem raciocínio

---

## 💡 DICA FINAL

Se sua resposta não se parece com o gabarito:
1. **Releia o módulo** - Pode ter perdido algum conceito
2. **Refaça o exercício** - Prática leva à melhoria
3. **Compare com exemplos** - Use o gabarito como referência
4. **Pergunte ao Mentor** - Execute `/prime-mentor` para tirar dúvidas

**Não existe resposta "errada" em exercícios criativos** - O gabarito é uma REFERÊNCIA, não a única resposta possível.
