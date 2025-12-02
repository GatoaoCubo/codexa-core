# Mentor Agent - Seu Guia Prático de E-commerce

**Versão 2.0 - Sistema Consolidado de Conhecimento + Mentoria**

Olá! Eu sou o Mentor Agent, seu conselheiro prático para vender mais nos marketplaces brasileiros (Mercado Livre, Shopee, Magalu, etc.).

---

## 🎯 O Que Eu Faço?

Imagina ter um mentor experiente que:
- ✅ Responde suas dúvidas sobre vendas em marketplaces
- ✅ Te ensina copywriting, SEO, estratégias de produto
- ✅ Transforma seus materiais (PDFs, vídeos, notas) em conhecimento organizado
- ✅ Monta aulas personalizadas sobre qualquer tema
- ✅ Fala sua língua (português BR, sem academicismo)

É exatamente isso que eu faço! 🚀

---

## 🚀 Como Usar (3 Modos)

### Modo 1: Perguntar Algo (Mais Comum)

Simplesmente me faça uma pergunta:

```
Você: "Como melhorar meu título no Mercado Livre?"

Eu: "Olha só, pro ML funcionar bem você precisa de 3 coisas no título:
1. Keywords que o pessoal busca (ex: 'masculina', 'algodão', 'premium')
2. Atributos específicos (tamanho, cor, material)
3. Diferenciais (ex: 'entrega rápida', 'kit com 3')

Exemplo prático:
❌ Antes: 'Camiseta Bonita'
✅ Depois: 'Camiseta Masculina Algodão Premium Malha Fria P ao GG'
📊 Resultado: +60% cliques

Quer que eu te ajude a montar o título dos seus produtos?"
```

**Como funciona por trás**:
1. Eu busco no meu catálogo de conhecimento
2. Leio os arquivos relevantes
3. Traduzo pra linguagem prática
4. Respondo com exemplos brasileiros

### Modo 2: Adicionar Conhecimento Novo

Você tem um PDF bacana? Um vídeo que ensina algo útil? Guia do Mercado Livre?

**É só colocar na pasta `RASCUNHO/` e usar o comando `/processar`**

```bash
# No seu computador:
# 1. Copie o arquivo pra RASCUNHO/
cp ~/Downloads/guia_shopee.pdf agentes/mentor_agent/RASCUNHO/

# 2. Execute o comando de processamento
/processar guia_shopee.pdf

# 3. Eu processo automaticamente e respondo
Eu: "✅ Processado! Cataloguei o guia da Shopee como [marketplace_optimization].
     📊 Quality Score: 0.87 (excellent)
     ⏱️ Time: 9.4s
     📁 Saved: marketplace_seo_shopee_20251113.md

     Agora posso te ajudar com dúvidas sobre SEO na Shopee.
     Quer aprender sobre algo específico?"
```

**Formatos suportados**: PDF, MD, TXT, DOCX, HTML, JSON, CSV, XLSX, MP4 (video), MP3 (audio), PNG/JPG (OCR)

**Opções avançadas**:
```bash
# Processar múltiplos arquivos de uma vez
/processar --batch

# Processamento detalhado (com context discovery)
/processar arquivo.pdf --mode thorough

# Forçar categoria específica
/processar arquivo.pdf --categoria marketplace_optimization
```

**O que eu faço automaticamente**:
1. **Extraio**: Leio o arquivo (PDF→text, video→transcript, image→OCR)
2. **Classifico**: Detecto categoria, assunto, nível, tags
3. **Sintetizo**: Organizo em formato estruturado (800-1200 palavras)
4. **Valido**: Checo qualidade em 5 dimensões (score ≥75%)
5. **Salvo**: Arquivo em `PROCESSADOS/` com nome descritivo
6. **Catalogo**: Atualizo índice para buscas futuras
7. **Pronto!** Agora posso usar esse conhecimento pra te ensinar!

### Modo 3: Pedir Uma Aula

Quer aprender sobre um tema completo?

```
Você: "Me ensina sobre copywriting para marketplaces"

Eu: "📚 AULA AO VIVO: Copywriting para Marketplaces

🎯 POR QUE ISSO IMPORTA?
Seu texto é o vendedor que trabalha 24/7. Um copy bom aumenta conversão em 30-50%.

📖 OS 3 PILARES ESSENCIAIS
1. **Título**: SEO + clareza (70 caracteres ML, 80 Shopee)
   - Keywords que as pessoas buscam
   - Atributos específicos do produto
   - Diferencial competitivo

2. **Descrição**: Benefícios > Características
   - Não: 'Feito de algodão'
   - Sim: 'Mantém você fresco mesmo no calor'

3. **Gatilhos Mentais**: Urgência, prova social, autoridade
   - Urgência: 'Últimas 5 unidades'
   - Prova social: '500+ vendidos'
   - Autoridade: 'Líder de vendas'

🛠️ COMO FAZER (PASSO-A-PASSO)

[Passo 1] Pesquise keywords no buscador do marketplace
- Abra o ML/Shopee
- Digite palavra-chave do seu produto
- Veja sugestões que aparecem
- Anote as mais populares

[Passo 2] Monte o título (template):
'[PRODUTO] [MATERIAL] [DIFERENCIAL] [ATRIBUTO] [PÚBLICO]'
Ex: 'Camiseta Algodão Premium Malha Fria Masculina'

[Passo 3] Escreva a descrição:
- Primeiro parágrafo: Benefício principal
- Segundo parágrafo: 3-5 características
- Terceiro parágrafo: Gatilhos mentais
- Último parágrafo: Chamada pra ação

💡 EXEMPLO REAL

Antes:
Título: 'Camiseta Bonita'
Descrição: 'Camiseta de algodão. Várias cores.'

Depois:
Título: 'Camiseta Masculina Algodão Premium Malha Fria P-GG'
Descrição: 'Mantenha-se fresco o dia todo com nossa camiseta de malha fria premium.
Perfeita para o calor brasileiro! Algodão 100%, respirável e confortável.
Tamanhos P ao GG. + de 500 vendidas. Últimas unidades em estoque!'

Resultado: +60% cliques, +35% conversão

✏️ EXERCÍCIO PRA VOCÊ
Pega um produto seu agora e:
1. Reescreve o título usando o template acima
2. Adiciona 3 gatilhos mentais na descrição
3. Testa por 7 dias e compara as vendas

🔗 PRÓXIMOS PASSOS
- Aprenda sobre SEO específico de cada marketplace
- Descubra gatilhos mentais avançados
- Teste variações com A/B testing"
```

**Como funciona**:
1. Busco TODOS arquivos relacionados ao tema
2. Leio múltiplos conteúdos
3. Sintetizo em aula estruturada
4. Adapto ao seu nível (iniciante/intermediário/avançado)
5. Dou exemplos práticos brasileiros

---

## 📁 Como Está Organizado

```
mentor_agent/
│
├── RASCUNHO/              👈 VOCÊ coloca arquivos brutos aqui
│   ├── guia_ml.pdf
│   ├── video_shopee.mp4
│   └── notas_vendas.txt
│
├── USER/                  👈 VOCÊ coloca seus materiais pessoais aqui
│   ├── meus_produtos.xlsx
│   └── minhas_estrategias.md
│
├── PROCESSADOS/           👈 EU organizo conhecimento aqui
│   ├── catalogo.json      📚 Índice de todo conhecimento
│   ├── marketplace_titulos_otimizacao_20251113.md
│   ├── copywriting_descricao_conversao_20251113.md
│   └── branding_identidade_visual_20251113.md
│
├── config/                # Agent configuration files
├── prompts/               # HOP modules for mentoring
├── strategic_plans/       # Strategic planning documents
├── DISTRIBUICAO/          # Distribution materials
├── README.md              # This file
├── PRIME.md               # Agent philosophy and principles
├── INSTRUCTIONS.md        # AI assistant instructions
└── SETUP.md               # Platform setup guide
```

**Regras Simples**:
- ✅ Coloque seus arquivos em `RASCUNHO/` ou `USER/`
- ✅ Eu cuido do resto (processar, organizar, catalogar)
- ❌ Não mexa em `PROCESSADOS/` (é minha área de trabalho)

---

## 💡 Exemplos Práticos do Dia-a-Dia

### Exemplo 1: Dúvida Rápida
```
Você: "Quantos caracteres posso usar no título da Shopee?"
Eu: "Na Shopee você tem até 80 caracteres pro título.
     Dica: Use todos! Quanto mais keywords relevantes, melhor pro SEO."
```

### Exemplo 2: Estratégia Complexa
```
Você: "Como competir com vendedor que vende mais barato?"
Eu: "Boa pergunta! Competir só no preço é armadilha. Te mostro 3 estratégias:

1. **Diferenciação**:
   - Adicione brinde (ex: embalagem premium, manual em português)
   - Resultado: Mesmo preço maior, converte melhor

2. **Bundle (Kit)**:
   - Venda 2-3 produtos juntos
   - Preço unitário menor, margem total maior
   - Resultado: Valor percebido 2x maior

3. **Posicionamento**:
   - Foque em público específico (ex: 'para atletas')
   - Crie anúncios segmentados
   - Resultado: Menos concorrência direta

Qual dessas faz mais sentido pro seu produto?"
```

### Exemplo 3: Material do Usuário
```
Você: *Adiciona planilha_produtos.xlsx em USER/*

Você: "Coloquei minha planilha de produtos em USER/"

Eu: "Legal! Vou processar...
     ✅ Identifiquei 47 produtos
     ✅ Detectei 3 categorias: moda, eletrônicos, casa
     ✅ Catalogado como [estrategia_produto]

     Quer que eu analise e sugira melhorias nos títulos?"
```

---

## 🎓 Temas Que Eu Domino

- **Marketplace Optimization**: SEO, títulos, descrições, fotos
- **Copywriting**: Gatilhos mentais, storytelling, conversão
- **Estratégia de Produto**: Mix, precificação, posicionamento
- **Análise de Concorrência**: Como estudar e se diferenciar
- **Compliance Legal**: O que pode/não pode, como evitar bloqueios
- **Branding**: Identidade visual, nome da loja, reputação
- **Visual Design**: Fotos que vendem, infográficos
- **Customer Experience**: Atendimento, avaliações, pós-venda
- **Operações & Logística**: Estoque, envio, prazo de entrega
- **Financeiro & Precificação**: Margem, custos, promoções

---

## ❓ Perguntas Frequentes

### "Você substitui os outros agentes?"
Não! Eu sou o **professor**, os outros são **especialistas**:
- `/prime-anuncio` - Cria anúncios completos
- `/prime-pesquisa` - Faz pesquisa de mercado
- `/prime-marca` - Desenvolve estratégia de marca

**Quando usar cada um?**
- **Mentor (eu)**: Aprender, entender, treinar
- **Anuncio**: Criar anúncio pronto
- **Pesquisa**: Descobrir produtos/tendências
- **Brand**: Criar identidade visual

### "Preciso saber programar?"
**Não!** Zero programação. É só conversar comigo.

### "Quanto conhecimento você tem?"
Atualmente:
- 10 categorias principais
- Crescendo conforme você adiciona materiais
- Base herdada: 66k+ cards processados (97.5% qualidade)

### "Posso confiar nas informações?"
Sim! Tudo que eu te ensino:
- ✅ Validado em 5 dimensões (completude, clareza, precisão, relevância, acionabilidade)
- ✅ Score de qualidade >75%
- ✅ Exemplos testados em lojas brasileiras
- ✅ Atualizado com práticas atuais de 2025

### "E se eu tiver dúvida específica da minha loja?"
Me conta! Quanto mais contexto você der, melhor eu ajudo.

```
Ruim: "Como vender mais?"
Bom: "Vendo camisetas no ML, 50 vendas/mês. Como dobrar isso?"
Ótimo: "Vendo camisetas masculinas no ML, ticket médio R$45,
        concorrentes entre R$35-50. Como diferenciar sem baixar preço?"
```

---

## 🚨 Regras Importantes

1. **Sempre me consulte primeiro** - Busco no catálogo antes de responder
2. **Forneça contexto** - Quanto mais detalhes, melhor a resposta
3. **Adicione materiais em RASCUNHO/** - Eu processo e organizo
4. **Pratique os exercícios** - Conhecimento sem ação = zero resultado
5. **Pergunte de novo** - Se não ficou claro, me peça pra explicar diferente

---

## 📞 Como Começar AGORA

**Passo 1**: Me faça uma pergunta sobre vendas em marketplace

**Passo 2**: Adicione um material útil em `RASCUNHO/` (guia, PDF, vídeo)

**Passo 3**: Peça uma aula sobre um tema que você quer dominar

**Pronto! É só isso.** 🎉

---

## 🔧 Para Desenvolvedores & AI Assistants

### Arquitetura Técnica (v2.0)

O mentor_agent v2.0 consolida 3 componentes principais:

**1. Scout Global Navigator** (`prompts/scout_global_navigator_HOP.md`)
- Navega todo projeto codexa (../../ até raiz)
- Escaneia 9 PRIME.md + 24 README.md de todos agentes
- Calcula relevância para tarefa (0.0-1.0 scoring)
- Retorna TOP 5 contextos mais relevantes
- Performance: 2-4 min para full scan

**2. Knowledge Processor** (`prompts/knowledge_processor_HOP.md`)
- Pipeline: Extract → Classify → Synthesize → Validate
- Suporta 12 formatos (PDF, video, audio, images, docs)
- Categoriza em 10 categorias + 27 tags
- Target output: 800-1200 tokens, seller language
- Performance: 10-30s (text), 30-120s (video)

**3. Quality Validator 5D** (`prompts/quality_validator_5d_HOP.md`)
- 5 dimensões: Completeness, Clarity, Accuracy, Relevance, Actionability
- Threshold: Overall ≥0.75 (excellent/good), per-dimension ≥0.60
- Auto-improvement: Se 0.60-0.74, tenta melhorar dimensões fracas (max 3x)
- Inherited from conhecimento_agent (97.5% quality rate on 66k+ cards)
- Performance: 3-6s por validação

### Comando /processar

**Orquestra os 3 componentes acima**:
```bash
/processar [file] [--batch] [--categoria name] [--mode standard|fast|thorough]
```

**Flow**:
1. (Optional) Scout Navigator - Se --mode thorough
2. Knowledge Processor - Processa arquivo
3. Quality Validator - Valida e auto-melhora se necessário
4. Save + Catalog update

### Documentação Completa

- **PRIME.md** - Arquitetura (4+8 pillars)
- **INSTRUCTIONS.md** - Guia operacional para AI assistants
- **INTEGRATION.md** - Sistema consolidado, integração de componentes
- **HOPs em prompts/** - Módulos TAC-7 reutilizáveis

### Performance Benchmarks

| Operation | Time |
|-----------|------|
| Scout Navigator (full) | 2-4 min |
| Process PDF | 10-15s |
| Process Video | 30-120s |
| Quality Validation | 3-6s |
| **Total (standard mode)** | **10-30s** |

**Quality Rate**: 97.5% (baseline herdado de conhecimento_agent)

---

## 🚀 NOVO! Sistema de Distribuição de Conhecimento (v2.1)

**O que há de novo**: mentor_agent agora distribui conhecimento automaticamente para outros agentes!

### Como Funciona

1. **Fonte Única**: Todo conhecimento está em `PROCESSADOS/CAPITULOS/`
2. **Extração Automática**: Script extrai versículos específicos
3. **Injeção Controlada**: Conhecimento é injetado em prompts de agentes especializados
4. **Versionamento**: Sistema rastreia o que foi injetado em cada agente

### Exemplo Prático

```bash
# Enriquecer prompts do anuncio_agent com conhecimento técnico
cd DISTRIBUICAO/
python enrich_agents.py --agent anuncio_agent

# Resultado:
# ✅ anuncio_agent/prompts/20_titulo_generator.md enriquecido
#    → Adicionada seção "📚 CONHECIMENTO TÉCNICO"
#    → Conhecimento sobre SEO, keywords, otimização de títulos
# ✅ .knowledge_version criado (tracking de versão)
```

### Benefícios

- ✅ **Agentes mais inteligentes**: Prompts enriquecidos com expertise técnica
- ✅ **Fonte única**: Atualiza CAPITULOS → todos agentes se beneficiam
- ✅ **Escalável**: Fácil adicionar novos agentes ou novos conhecimentos
- ✅ **Versionado**: Rastreável via git + .knowledge_version

### Documentação Completa

📖 **Quer saber mais?** Leia:
- `DISTRIBUICAO/README.md` - Como usar o sistema
- `DISTRIBUICAO/DESIGN_REVIEW.md` - Decisões arquiteturais
- `DISTRIBUICAO/knowledge_map.json` - Configuração de mapeamentos

### Status Atual

**Agentes Enriquecidos**:
- ✅ `anuncio_agent/prompts/20_titulo_generator.md` (2 versículos injetados)

**Próximos**:
- ⏳ `anuncio_agent/prompts/40_bullet_points.md`
- ⏳ `anuncio_agent/prompts/50_descricao_builder.md`
- ⏳ `pesquisa_agent/prompts/competitor_analysis.md`

---

**Versão**: 2.1.0 (+ Sistema de Distribuição de Conhecimento)
**Última Atualização**: 2025-11-14
**Feito para**: Sellers de e-commerce brasileiro

---

> 💡 **Lembre-se**: Eu não sou só um banco de dados. Sou seu mentor.
> Quanto mais você usa, mais eu aprendo sobre você e melhor te ajudo! 🚀
