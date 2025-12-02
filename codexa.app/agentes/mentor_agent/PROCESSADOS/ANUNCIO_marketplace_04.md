# LIVRO: Marketplace
## CAPÍTULO 4

**Versículos consolidados**: 17
**Linhas totais**: 1182
**Gerado em**: 2025-11-13 18:45:49

---


<!-- VERSÍCULO 1/17 - marketplace_optimization_5_princípios_orientadores_para_treinar_llms_20251113.md (19 linhas) -->

# 5. Princípios Orientadores para Treinar LLMs

**Categoria**: marketplace_optimization
**Qualidade**: 0.87/1.00
**Data**: 20251113

## Conteúdo

1. **Formato Primeiro**: os modelos devem ser instruídos a respeitar JSON STRICT; qualquer saída inválida precisa acionar reparo ou retry.
2. **Fluxo Multi-etapas**: reforçar a sequência benchmark → síntese → geração → validação → empacotamento para maximizar consistência.
3. **Resiliência de Fornecedor**: manter fallback cross-vendor e monitorar métricas de sucesso para calibrar preferências dinâmicas.
4. **Enriquecimento Determinístico**: SEO e n

**Tags**: ecommerce, intermediate

**Palavras-chave**: Princípios, Orientadores, Treinar, LLMs

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 2/17 - marketplace_optimization_5_seções_adicionais_20251113.md (55 linhas) -->

# 5️⃣ Seções Adicionais

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Itens Inclusos (What's in the Box)

```
📦 NA CAIXA VEM:
✓ Notebook XYZ (lacrado)
✓ Carregador original
✓ Cabo USB-C
✓ Manual em português
✓ Nota fiscal
✓ Garantia 2 anos
```

### Dicas de Uso

```
💡 DICAS PARA APROVEITAR AO MÁXIMO:

1. SETUP INICIAL (5 min):
   - Instale drivers de wi-fi e áudio (vêm no HD)
   - Configure Windows Update
   - Deixe primeira carga completa (importante para bateria)

2. PERFORMANCE:
   - Feche apps desnecessários no startup
   - Use SSD para grande maioria de arquivos
   - RAM é compartilhada: se precisa de 16GB usados, considere upgrade

3. DURABILIDADE:
   - Limpe ventilação 1x por mês (ar comprimido)
   - Use mochila acolchoada no transporte
   - Não bloqueie ventiladores com travesseiro
   - Desligue propriamente (não passe para hibernação)

4. BATERIA:
   - Deixe carga entre 20-80% para longevidade
   - Evite uso contínuo em 100% (reduz ciclos)
   - Em desuso prolongado, mantenha em ~50%
```

---

**Tags**: general, intermediate

**Palavras-chave**: Adicionais, Seções

**Origem**: unknown


---


<!-- VERSÍCULO 3/17 - marketplace_optimization_61_execution_contexts_20251113.md (45 linhas) -->

# 6.1 EXECUTION CONTEXTS

**Categoria**: marketplace_optimization
**Qualidade**: 0.79/1.00
**Data**: 20251113

## Conteúdo

```yaml
in_loop_mode:
  when: [exploration, learning, debugging, novel_problems]
  characteristics:
    human_presence: high
    feedback: immediate
    iteration: rapid
    context: conversational
  best_for: prototype_development
  
out_loop_mode:
  when: [known_patterns, defined_workflows, async_tasks]
  characteristics:
    human_presence: review_only
    feedback: batch
    iteration: automated
    context: documented
  best_for: production_workloads
  framework: PITER
  
zero_touch_mode:
  when: [mature_systems, high_confidence, full_coverage]
  characteristics:
    human_presence: prompt_only
    feedback: metrics_only
    iteration: self_directed
    context: comprehensive
  best_for: continuous_deployment
  requirement: "90%+ success rate"
```

**Tags**: abstract, general

**Palavras-chave**: EXECUTION, CONTEXTS

**Origem**: unknown


---


<!-- VERSÍCULO 4/17 - marketplace_optimization_62_scaling_patterns_20251113.md (45 linhas) -->

# 6.2 SCALING PATTERNS

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

```yaml
horizontal_scaling:
  strategy: multiple_specialized_agents
  benefit: parallel_processing
  pattern:
    - decompose_task
    - assign_specialists
    - aggregate_results
    
vertical_scaling:
  strategy: deeper_agent_chains
  benefit: progressive_refinement
  pattern:
    - rough_draft
    - refinement
    - polish
    - validation
    
fractal_scaling:
  strategy: self_similar_patterns
  benefit: infinite_composition
  pattern:
    - primitive→workflow
    - workflow→system
    - system→ecosystem
```

---

# 🛠️ CARD 7: CONSTRUCTION PROTOCOL

**Tags**: architectural, general

**Palavras-chave**: PATTERNS, SCALING

**Origem**: unknown


---


<!-- VERSÍCULO 5/17 - marketplace_optimization_6_agente_3_image_generator_20251113.md (221 linhas) -->

# 6. AGENTE 3: IMAGE GENERATOR

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### 6.1 Objetivos e Responsabilidades

**Objetivo Principal:**
Criar um grid de 9 imagens profissionais que comuniquem visualmente o valor do produto, mantenham consistência de marca e otimizem para conversão em marketplaces.

**Responsabilidades:**
1. ✅ Manter brand identity (cores, forma, estética)
2. ✅ Criar 9 cenas distintas mas coerentes
3. ✅ Balancear hero shots (1,9) com lifestyle (2-8)
4. ✅ Demonstrar benefícios visualmente
5. ✅ Seguir regras técnicas (iluminação, resolução)
6. ✅ Cumprir compliance de imagens de marketplace
7. ✅ Otimizar para conversão (hierarquia visual)

**NÃO é responsabilidade:**
- ❌ Fazer pesquisa de mercado
- ❌ Escrever copy
- ❌ Definir produto
- ❌ Fazer edição pós-generativa (deve sair pronto)

### 6.2 Fundamentos de Fotografia de Produto

#### Teoria de Composição

**Regra dos Terços**
```
Grid 3x3:
+-----+-----+-----+
|     |     |     |
|  *  |     |  *  |  * = Pontos de interesse
+-----+-----+-----+
|     |     |     |
|     |     |     |
+-----+-----+-----+
|     |     |     |
|  *  |     |  *  |
+-----+-----+-----+

Produto deve estar em um dos pontos *
Ou seguir uma das linhas
```

**Golden Ratio (Fibonacci)**
```
Espiral de Fibonacci guia o olho:
    ____
   |    |___
   |        |
   |________|

Produto principal no centro da espiral
Elementos secundários seguem a curvatura
```

**Hierarquia Visual**

```
1. TAMANHO (maior = mais importante)
2. CONTRASTE (alto contraste chama atenção)
3. COR (cores quentes avançam, frias recuam)
4. NITIDEZ (foco atrai olho)
5. POSIÇÃO (centro > bordas)
6. ISOLAMENTO (espaço negativo)
```

#### Teoria de Iluminação

**Setup Clássico de 3 Pontos**

```
        KEY LIGHT
           💡
          /  \
         /    \
        /      \
    👤PRODUTO    
      /    \
     /      \
💡         💡
FILL      BACK/RIM
```

**Key Light (Luz Principal)**
- Posição: 45° acima e lateral do produto
- Intensidade: Mais forte (100%)
- Função: Define forma e textura

**Fill Light (Luz de Preenchimento)**
- Posição: Oposta à key, mais baixa
- Intensidade: Mais fraca (30-50%)
- Função: Suaviza sombras

**Back/Rim Light (Luz de Contorno)**
- Posição: Atrás do produto, alto
- Intensidade: Média (60-80%)
- Função: Separa produto do fundo

**Tipos de Luz por Objetivo**

| Tipo | Descrição | Quando Usar |
|------|-----------|-------------|
| Hard Light | Sombras duras, contraste alto | Produtos metálicos, definição de forma |
| Soft Light | Sombras suaves, transições graduais | Produtos têxteis, pele, orgânicos |
| Diffused | Luz espalhada, sem sombras | Fundo branco, e-commerce clean |
| Directional | Luz com direção clara | Criar mood, drama, produto premium |

**Temperatura de Cor**

```
KELVIN SCALE:
2000K  ■■■■■□□□□□  (Vela - muito quente)
3000K  ■■■■■■□□□□  (Lâmpada incandescente)
4000K  ■■■■■■■□□□  (Fluorescente fria)
5500K  ■■■■■■■■□□  (Luz do dia - neutro)
6500K  ■■■■■■■■■□  (Céu nublado - frio)
8000K  ■■■■■■■■■■  (Sombra - muito frio)

Para E-commerce:
- Fundo branco: 5000-5500K (daylight neutro)
- Lifestyle warm: 3500-4500K (acolhedor)
- Lifestyle cool: 5500-6500K (moderno, tech)
```

#### Teoria de Cor

**Círculo Cromático**

```
        AMARELO
           |
     VERDE |  LARANJA
        \  |  /
         \ | /
    CIANO-+-VERMELHO
         / | \
        /  |  \
      AZUL | MAGENTA
           |
         ROXO
```

**Esquemas de Cor**

1. **Monocromático**
```
Uma cor + suas variações de saturação/luminosidade
Exemplo: Azul escuro → Azul médio → Azul claro
Uso: Produtos elegantes, minimalistas
```

2. **Análogo**
```
Cores adjacentes no círculo
Exemplo: Azul → Azul-verde → Verde
Uso: Harmonia natural, produtos orgânicos
```

3. **Complementar**
```
Cores opostas no círculo
Exemplo: Azul ↔ Laranja
Uso: Alto contraste, chamar atenção
```

4. **Tríade**
```
Três cores igualmente espaçadas
Exemplo: Vermelho + Amarelo + Azul
Uso: Vibrante, energético, infantil
```

**Psicologia das Cores por Categoria**

```python
COR_PSICOLOGIA = {
    'vermelho': {
        'emocao': ['energia', 'paixão', 'urgência'],
        'uso': 'CTAs, promoções, produtos esportivos',
        'evitar': 'Produtos relaxantes, saúde (exceto urgência)'
    },
    'azul': {
        'emocao': ['confiança', 'profissionalismo', 'calma'],
        'uso': 'Corporativo, tecnologia, saúde',
        'evitar': 'Alimentos (suprime apetite)'
    },
    'verde': {
        'emocao': ['natural', 'sustentável', 'crescimento'],
        'uso': 'Produtos orgânicos, financeiro, saúde',
        'evitar': 'Tecnologia futurista'
    },
    'amarelo': {
        'emocao': ['otimismo', 'atenção', 'alegria'],
        'uso': 'Chamar atenção, produtos infantis',
        'evitar': 'Overuse (cansa visão)'
    },
    'laranja': {
        'emocao': ['entusiasmo', 'criatividade', 'aventura'],
        'uso': 'CTAs secundários, esportes',
        'evitar': 'Produtos premium de luxo'
    },
    'roxo': {
        'emocao': ['luxo', 'criatividade', 'sabedoria'],
        'uso': 'Premium, beleza, espiritual',
        'evitar': 'Produ

[... content truncated ...]

**Tags**: concrete, general

**Palavras-chave**: GENERATOR, IMAGE, AGENTE

**Origem**: unknown


---


<!-- VERSÍCULO 6/17 - marketplace_optimization_6_call_to_action_cta_20251113.md (49 linhas) -->

# 6️⃣ Call-to-Action (CTA)

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Tipos de CTA

```
URGÊNCIA BAIXA:
"Compre Agora" / "Saiba Mais"

URGÊNCIA MÉDIA:
"Aproveite a Promoção" / "Garanta o Seu" / "Faça o Pedido"

URGÊNCIA ALTA:
"Últimas 5 unidades!" / "Promoção válida até amanhã!"
"Não deixe para depois - Compre Agora"
```

### Exemplo de CTA Estratégica

```
❌ GENÉRICO:
"Comprar"

✅ COM BENEFÍCIO:
"Ganhe 11h de produtividade - Compre Agora"

✅ COM URGÊNCIA:
"Últimas 3 em estoque - Compre Antes que Acabe"

✅ COM GARANTIA:
"Compre com Confiança - 30 dias de devolução"

✅ COM SENSAÇÃO:
"Comece a Programar 3x Mais Rápido - Clique Aqui"
```

---

**Tags**: general, intermediate

**Palavras-chave**: Call, Action

**Origem**: unknown


---


<!-- VERSÍCULO 7/17 - marketplace_optimization_6_controle_de_versão_20251113.md (32 linhas) -->

# 6) Controle de Versão

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

- v1.0 (31/07/2025): lista original dos ficheiros.  
- v1.1 (12/08/2025): reagrupado por tema, com “Como usar” e “Mapas rápidos”.



---

### RAW_007_GLOSSARY.md

# Technical Glossary - TAC-7 Project

**Version:** 1.0
**Date:** 2025-11-02
**Status:** Complete
**Language:** English with Portuguese translations

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Controle, Versão

**Origem**: unknown


---


<!-- VERSÍCULO 8/17 - marketplace_optimization_6_livros_de_e_commerce_20251113.md (37 linhas) -->

# 🎯 6 LIVROS de E-Commerce

**Categoria**: marketplace_optimization
**Qualidade**: 0.67/1.00
**Data**: 20251113

## Conteúdo

### 📖 LIVRO_01: FUNDAMENTALS
Business models, customer journey, market analysis
- **CAPÍTULO_01**: Business Models (B2C, B2B, Marketplace, SaaS)
- **CAPÍTULO_02**: Customer Journey (Awareness, Consideration, Purchase, Retention)

### 📖 LIVRO_02: PRODUCT_MANAGEMENT
Products, catalog, taxonomy, pricing
- **CAPÍTULO_01**: Catalog Architecture (Taxonomy, Attributes, Variants)
- **CAPÍTULO_02**: Data Enrichment (Descriptions, Images, SEO)
- **CAPÍTULO_03**: Pricing Strategy (Dynamic pricing, promotions, discounts)

### 📖 LIVRO_03: OPERATIONS
Inventory, orders, fulfillment, logistics
- **CAPÍTULO_01**: Inventory (Stock levels, safety stock, forecasting)
- **CAPÍTULO_02**: Orders (Order management, tracking, returns)
- **CAPÍTULO_03**: Fulfillment (Warehouse, shipping, last-mile)

### 📖 LIVRO_04: TECHNOLOGY
Architecture, database, APIs, infrastructure
- **CAPÍTULO_01**: Architecture (Monolith, microservices, scalability)
- **CAPÍTULO_02**: Database Design (SQL, NoSQL, caching)
- **CAPÍTULO_03

**Tags**: ecommerce, concrete

**Palavras-chave**: LIVROS, Commerce

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 9/17 - marketplace_optimization_6_supervised_fine_tuning_sft_para_documentação_20251113.md (162 linhas) -->

# 6. SUPERVISED FINE-TUNING (SFT) PARA DOCUMENTAÇÃO

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### 6.1 O que é SFT Aplicado a Docs

**Definição:**
Treinar um LLM em exemplos (input, output) estruturados para aprender a consumir e gerar documentação técnica de alta qualidade.

**Pipeline:**

```
BASE MODEL (pré-treinado) → SFT (docs) → SPECIALIZED DOC MODEL
      ↓                            ↓                    ↓
  General language          Task-specific        Expert em docs técnicas
  11T tokens               10k-50k examples      Entende padrões, gera bem
```

### 6.2 Criando Dataset de SFT para Documentação

**Estrutura de Exemplo:**

```json
{
  "instruction": "Documente a função calculate_loss() que calcula cross-entropy loss para LLM training.",
  
  "context": {
    "code": "def calculate_loss(logits, labels): return F.cross_entropy(logits.view(-1, logits.size(-1)), labels.view(-1))",
    "usage_example": "loss = calculate_loss(model_output, target_tokens)",
    "related_functions": ["backward()", "optimizer.step()"]
  },
  
  "output": "# calculate_loss()\n\n**Purpose:** Computes cross-entropy loss for language model training.\n\n**Signature:**\n```python\ndef calculate_loss(logits: Tensor, labels: Tensor) -> Tensor\n```\n\n**Parameters:**\n- `logits` (Tensor): Model output logits, shape [batch_size, seq_len, vocab_size]\n- `labels` (Tensor): Ground truth token IDs, shape [batch_size, seq_len]\n\n**Returns:**\n- Tensor: Scalar loss value (lower is better)\n\n**Usage:**\n```python\nlogits = model(input_ids)  # [8, 512, 50257]\nlabels = target_tokens      # [8, 512]\nloss = calculate_loss(logits, labels)\nloss.backward()  # Compute gradients\n```\n\n**Note:** Function flattens inputs for efficient computation. Equivalent to:\n```python\nF.cross_entropy(\n    logits.view(-1, vocab_size),  # [batch*seq, vocab]\n    labels.view(-1)                # [batch*seq]\n)\n```\n\n**Related:**\n- [backward()](#backward) - Computes gradients from loss\n- [optimizer.step()](#step) - Updates weights using gradients"
}
```

**Dataset Curation Guidelines:**

1. **Diversidade de Formatos**
```json
{
  "types": [
    "function_documentation",
    "class_documentation",
    "module_overview",
    "tutorial_creation",
    "api_reference",
    "troubleshooting_guide",
    "concept_explanation",
    "code_example_generation"
  ]
}
```

2. **Qualidade > Quantidade**
```
GOLD: 1,000 exemplos perfeitamente curados
> 
SILVER: 10,000 exemplos medíocres
```

3. **Negative Examples (Learn what NOT to do)**
```json
{
  "instruction": "Documente função sort_list()",
  
  "bad_output": "Esta função ordena uma lista. Use assim: sort_list(my_list)",
  
  "good_output": "# sort_list()\n\n**Purpose:** Sorts a list in ascending order using quicksort algorithm.\n\n**Complexity:** O(n log n) average, O(n²) worst case\n\n**Signature:**\n```python\ndef sort_list(lst: List[int], reverse: bool = False) -> List[int]\n```\n\n**Parameters:**\n- `lst`: List of integers to sort\n- `reverse`: If True, sorts in descending order (default: False)\n\n**Returns:** New sorted list (original unchanged)\n\n**Examples:**\n```python\n# Ascending (default)\nassert sort_list([3,1,2]) == [1,2,3]\n\n# Descending\nassert sort_list([3,1,2], reverse=True) == [3,2,1]\n```",
  
  "label": "good"
}
```

### 6.3 Training Configuration for SFT

```python
from transformers import TrainingArguments
from trl import SFTTrainer

# Dataset de documentação
doc_dataset = load_dataset("tech_docs_sft", split="train")

# Configuração otimizada para SFT de docs
training_args = TrainingArguments(
    # Output
    output_dir="./doc_model_sft",
    
    # Epochs (SFT tipicamente usa poucas épocas)
    num_train_epochs=3,  # 3-5 é padrão para SFT
    
    # Batch size
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,  # Effective batch = 4*4 = 16
    
    # Learning rate
    learning_rate=2e-5,  # Menor que pretraining (1e-4)
    lr_scheduler_type="cosine",
    warmup_ratio=0.1,
    
    # Regularização
    weight_decay=0.01,
    max_grad_norm=1.0,
    
    # Precision
    bf16=True,  # Se GPU suporta
    
    # Logging
    logging_steps=10,
    evaluation_strategy="steps",
    eval_steps=100,
    save_steps=500,
    
    # Memory optimization
    gradient_checkpointing=True,
    optim="adamw_torch_fused",  # Mais rápido
    
    # Output
    report_to="wandb",
    load_best_model_at_end=True,
)

# Trainer
trainer = SFTTrainer(
    model=base_model,
    args=training_args,
    train_dataset=doc_dataset,
    eval_dataset=doc_dataset_eval,
    
    # Formatting
    dataset_text_field="text",  # Campo com texto formatado
    max_seq_length=2048,        # Docs podem ser longos
    
    # Packing (eficiência)
    packing=True,  # Combina múltiplos exemplos curtos em um batch
)

# Train!
trainer.train()
```

### 6.4 Formatting de Dataset para SFT

**Formato de Chat Template:**

```python
# Chat template para documentação técnica
chat_template = """<|system|>
You are a technical documentation expert. Generate clear, comprehensive documentation following best practices

[... content truncated ...]

**Tags**: abstract, general

**Palavras-chave**: TUNING, DOCUMENTAÇÃO, FINE, SUPERVISED

**Origem**: unknown


---


<!-- VERSÍCULO 10/17 - marketplace_optimization_71_bootstrap_sequence_20251113.md (69 linhas) -->

# 7.1 BOOTSTRAP SEQUENCE

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

```python
def bootstrap_agentic_system():
    """Self-constructing system genesis"""
    
    # Phase 0: Assess
    problem_classes = identify_problem_domains()
    success_criteria = define_validation_methods()
    
    # Phase 1: Primitives
    primitives = {
        'commands': create_slash_commands(),
        'templates': encode_problem_patterns(),
        'context': establish_single_source_truth(),
        'validators': setup_test_infrastructure()
    }
    
    # Phase 2: Composition
    workflows = {}
    for problem_class in problem_classes:
        workflows[problem_class] = compose_adw(
            primitives=primitives,
            pattern=problem_class.pattern,
            validation=success_criteria[problem_class]
        )
    
    # Phase 3: Automation
    piter = setup_out_loop_execution(
        workflows=workflows,
        triggers=identify_triggers(),
        environment=create_safe_containers()
    )
    
    # Phase 4: Specialization
    agents = {}
    for responsibility in decompose_responsibilities():
        agents[responsibility] = create_specialized_agent(
            purpose=responsibility,
            context=minimal_required_context(responsibility),
            tools=required_tools(responsibility)
        )
    
    # Phase 5: Optimization
    while system.confidence < 0.9:
        add_feedback_loops()
        minimize_context()
        measure_kpis()
        iterate()
    
    # Phase 6: Zero-Touch
    if system.confidence >= 0.9:
        enable_zero_touch_mode()
    
    return system
```

**Tags**: concrete, general

**Palavras-chave**: SEQUENCE, BOOTSTRAP

**Origem**: unknown


---


<!-- VERSÍCULO 11/17 - marketplace_optimization_72_meta_learning_loop_20251113.md (48 linhas) -->

# 7.2 META-LEARNING LOOP

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

```yaml
continuous_improvement:
  monitor:
    - success_rates
    - execution_time
    - resource_usage
    - error_patterns
    
  analyze:
    - identify_bottlenecks
    - find_failure_modes
    - discover_patterns
    
  adapt:
    - update_templates
    - refine_prompts
    - adjust_context
    - evolve_workflows
    
  validate:
    - a_b_testing
    - gradual_rollout
    - metric_tracking
    
  propagate:
    - successful_patterns_become_templates
    - templates_become_workflows
    - workflows_become_standards
```

---

# 📊 CARD 8: KPI FRAMEWORK

**Tags**: abstract, general

**Palavras-chave**: LEARNING, LOOP, META

**Origem**: unknown


---


<!-- VERSÍCULO 12/17 - marketplace_optimization_7_preference_alignment_e_dpo_20251113.md (180 linhas) -->

# 7. PREFERENCE ALIGNMENT E DPO

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### 7.1 O que é Preference Alignment

**Problema:** Modelo pós-SFT gera documentação tecnicamente correta mas não necessariamente no formato preferido por humanos.

**Solução:** Treinar modelo a preferir outputs de alta qualidade sobre outputs de baixa qualidade.

**Métodos:**

```
RLHF (Reinforcement Learning from Human Feedback)
├── Complexo: Treina reward model separado
├── Instável: PPO pode divergir
└── Caro: Requer muitas avaliações humanas

DPO (Direct Preference Optimization)
├── Simples: Otimização direta
├── Estável: Supervised learning
└── Eficiente: Sem reward model intermediário
```

### 7.2 Criando Preference Dataset

**Estrutura:**

```json
{
  "prompt": "Document the train() method of SFTTrainer",
  
  "chosen": "# SFTTrainer.train()\n\n**Purpose:** Executes supervised fine-tuning loop.\n\n**Signature:**\n```python\ndef train() -> TrainOutput\n```\n\n**Returns:** TrainOutput containing:\n- `global_step` (int): Total training steps\n- `training_loss` (float): Final average loss\n- `metrics` (dict): Additional metrics (lr, grad_norm, etc.)\n\n**Example:**\n```python\ntrainer = SFTTrainer(model, args, dataset)\noutput = trainer.train()\nprint(f\"Final loss: {output.training_loss:.3f}\")\n```\n\n**Workflow:**\n1. Iterates over training dataset\n2. Computes loss for each batch\n3. Backpropagates gradients\n4. Updates model weights\n5. Logs metrics periodically\n\n**Tips:**\n- Use `gradient_accumulation_steps` for larger effective batch size\n- Enable `gradient_checkpointing` to reduce memory\n- Monitor loss curve - should decrease steadily\n\n**Related:**\n- [TrainingArguments](#args) - Configure hyperparameters\n- [SFTConfig](#config) - SFT-specific settings",
  
  "rejected": "This method trains the model. Just call it:\n```python\ntrainer.train()\n```\n\nIt returns a TrainOutput object with the results."
}
```

**Critérios de Preferência:**

| Aspecto | Chosen (Preferido) | Rejected (Rejeitado) |
|---------|-------------------|---------------------|
| **Estrutura** | Headers claros, seções lógicas | Sem estrutura, texto corrido |
| **Exemplos** | Código completo, comentado | Código snippet incompleto |
| **Profundidade** | Explica como funciona | Apenas o que faz |
| **Links** | Referências a conceitos relacionados | Sem cross-references |
| **Troubleshooting** | Dicas práticas | Sem tips |
| **Completude** | Cobre todos parâmetros | Info faltando |

**Gerando Pares Automaticamente:**

```python
def generate_preference_pairs(base_model, enhanced_model, prompts):
    """
    Gera pares (chosen, rejected) usando dois modelos
    """
    pairs = []
    
    for prompt in prompts:
        # Gera com modelo base (rejeitado)
        rejected = base_model.generate(prompt)
        
        # Gera com modelo enhanced (escolhido)
        chosen = enhanced_model.generate(prompt)
        
        # Valida qualidade
        if quality_score(chosen) > quality_score(rejected):
            pairs.append({
                'prompt': prompt,
                'chosen': chosen,
                'rejected': rejected
            })
    
    return pairs

def quality_score(doc):
    """
    Score automático de qualidade
    """
    score = 0
    
    # Estrutura
    if '##' in doc:  # Tem headers
        score += 2
    
    # Exemplos
    if '```python' in doc:  # Tem code blocks
        score += 3
    
    # Completude
    if len(doc) > 500:  # Suficientemente detalhado
        score += 1
    
    # Links
    if '[' in doc and ']' in doc:  # Tem referências
        score += 2
    
    return score
```

### 7.3 DPO Training

```python
from trl import DPOTrainer, DPOConfig

# Preference dataset
preference_data = load_dataset("tech_docs_preferences")

# Configuração DPO
dpo_config = DPOConfig(
    # Base config
    output_dir="./doc_model_dpo",
    num_train_epochs=1,  # DPO tipicamente usa 1-2 épocas
    
    # Batch size
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    
    # Learning rate (menor que SFT)
    learning_rate=5e-7,  # Muito menor!
    lr_scheduler_type="cosine",
    warmup_ratio=0.1,
    
    # DPO specific
    beta=0.1,  # Controla strength de preference (típico: 0.1-0.5)
    loss_type="sigmoid",  # ou "hinge"
    
    # Regularização
    max_grad_norm=1.0,
    
    # Memory
    gradient_checkpointing=True,
    bf16=True,
    
    # Logging
    logging_steps=10,
    save_steps=100,
    report_to="wandb"
)

# Trainer
dpo_trainer = DPOTrainer(
    model=sft_model,  # Modelo pós-SFT
    ref_model=sft_model_copy,  # Reference model (frozen copy)
    args=dpo_config,
    train_dataset=preference_data,
    
    # Tokenizer
    tokenizer=tokenizer,
    max_length=2048,
    max_prompt_length=512
)

# Train!
dpo_trainer.train()
```

**O que DPO faz matematicamente:**

```
Loss_DPO = -log(σ(β · (log π_θ(y_w|x) - log π_θ(y_l|x)
                        - log π_ref(y_w|x) + log π_ref(y_l|x))))

Onde:
- y_w: Output preferido (chosen)
- y_l: Output não-preferido (rejected)
- π_θ: Modelo sendo tr

[... content truncated ...]

**Tags**: abstract, general

**Palavras-chave**: ALIGNMENT, PREFERENCE

**Origem**: unknown


---


<!-- VERSÍCULO 13/17 - marketplace_optimization_81_agentic_metrics_20251113.md (55 linhas) -->

# 8.1 AGENTIC METRICS

**Categoria**: marketplace_optimization
**Qualidade**: 0.79/1.00
**Data**: 20251113

## Conteúdo

```yaml
efficiency_metrics:
  attempts_to_success:
    optimize: minimize
    target: "<3 iterations"
    
  human_intervention_rate:
    optimize: minimize
    target: "<10%"
    
  execution_time:
    optimize: minimize_within_quality
    target: "sub_minute_for_common_tasks"
    
quality_metrics:
  validation_pass_rate:
    optimize: maximize
    target: ">95%"
    
  streak_length:
    optimize: maximize
    target: ">100_consecutive_successes"
    
  output_completeness:
    optimize: maximize
    target: "100%_requirements_met"
    
scale_metrics:
  parallel_execution:
    optimize: maximize
    target: "100+_concurrent_agents"
    
  problem_class_coverage:
    optimize: maximize
    target: "90%_of_identified_classes"
    
  reuse_rate:
    optimize: maximize
    target: ">80%_template_reuse"
```

**Tags**: general, intermediate

**Palavras-chave**: METRICS, AGENTIC

**Origem**: unknown


---


<!-- VERSÍCULO 14/17 - marketplace_optimization_82_system_health_20251113.md (45 linhas) -->

# 8.2 SYSTEM HEALTH

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

```yaml
monitoring:
  real_time:
    - agent_status
    - queue_depth
    - error_rates
    - latency_percentiles
    
  batch_analysis:
    - success_trends
    - cost_per_task
    - quality_distribution
    - learning_curve
    
  alerts:
    - validation_failure_spike
    - context_overflow
    - infinite_loops
    - resource_exhaustion
    
  dashboards:
    - agent_utilization
    - workflow_performance
    - template_effectiveness
    - roi_tracking
```

---

# 🌟 CARD 9: ADVANCED PATTERNS

**Tags**: architectural, general

**Palavras-chave**: SYSTEM, HEALTH

**Origem**: unknown


---


<!-- VERSÍCULO 15/17 - marketplace_optimization_91_compositional_intelligence_20251113.md (37 linhas) -->

# 9.1 COMPOSITIONAL INTELLIGENCE

**Categoria**: marketplace_optimization
**Qualidade**: 0.79/1.00
**Data**: 20251113

## Conteúdo

```yaml
prompt_algebra:
  addition:
    operation: "prompt_a + prompt_b"
    result: combined_capability
    example: "research + writing = report_generation"
    
  multiplication:
    operation: "prompt × n"
    result: scaled_execution
    example: "product_description × 100 = catalog"
    
  composition:
    operation: "f(g(x))"
    result: chained_transformation
    example: "analyze(summarize(document))"
    
  recursion:
    operation: "prompt(prompt)"
    result: meta_generation
    example: "template_generator(requirements)"
```

**Tags**: concrete, general

**Palavras-chave**: INTELLIGENCE, COMPOSITIONAL

**Origem**: unknown


---


<!-- VERSÍCULO 16/17 - marketplace_optimization_92_emergence_patterns_20251113.md (37 linhas) -->

# 9.2 EMERGENCE PATTERNS

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

```yaml
emergent_capabilities:
  threshold_effects:
    pattern: "quantity→quality_transition"
    example: "enough_examples→generalization"
    
  compositional_generalization:
    pattern: "known_parts→novel_wholes"
    example: "primitives→unforeseen_workflows"
    
  recursive_improvement:
    pattern: "system_improves_system"
    example: "agents_optimizing_agents"
    
  swarm_intelligence:
    pattern: "simple_rules→complex_behavior"
    example: "specialized_agents→emergent_solutions"
```

---

# 🔮 CARD 10: META DIRECTIVES

**Tags**: concrete, general

**Palavras-chave**: PATTERNS, EMERGENCE

**Origem**: unknown


---


<!-- VERSÍCULO 17/17 - marketplace_optimization__10_minute_workflows_20251113.md (46 linhas) -->

# 💡 10-Minute Workflows

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Workflow A: New Product Launch (10 min)
```
1. Run: /research [complete]
2. Review: Markdown report (3 min)
3. Copy: Chunk 4 + 5 to Claude
4. Generate: Ad copy
```

### Workflow B: Competitive Intelligence (5 min)
```
1. Run: /analyze_competitors [with URLs]
2. Review: Gaps and positioning (2 min)
3. Copy: Chunk 3 for differentiation
```

### Workflow C: SEO/SEM Strategy (3 min)
```
1. Run: /extract_keywords
2. Review: 4-level keyword hierarchy (1 min)
3. Use: Keywords in campaigns
```

### Workflow D: AI-Powered Copywriting (5 min)
```
1. Run: /research [with AI Composition: true]
2. Copy: All 5 chunks
3. Paste: Into Claude/ChatGPT
4. Generate: Multiple copy variants
```

---

**Tags**: architectural, general

**Palavras-chave**: Workflows, Minute

**Origem**: unknown


---


<!-- FIM DO CAPÍTULO 4 -->
<!-- Total: 17 versículos, 1182 linhas -->
