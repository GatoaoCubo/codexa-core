# Fine-Tuning e Knowledge Distillation: Guia Prático para LLMs

**Categoria**: llm_advanced
**Assunto**: fine_tuning_distillation
**Nível**: avançado
**Aplicação**: quando_customizar_llms_producao
**Tags**: sft, dpo, knowledge-distillation, fine-tuning, ml-pratico
**Quality Score**: 0.92/1.0

---

## RESUMO EXECUTIVO

Este documento ensina **como treinar LLMs customizados** via 3 técnicas principais: SFT (Supervised Fine-Tuning), DPO (Direct Preference Optimization) e Knowledge Distillation. Foco 100% prático: quando usar, como implementar, code snippets executáveis, e trade-offs reais para produção.

**Para quem**: Desenvolvedores que precisam customizar LLMs para casos específicos (agentes especializados, domínios proprietários, otimização custo/performance).

**Resultado esperado**: Criar versões customizadas de LLMs que:
- Performam 2-5x melhor em seu domínio específico
- Custam 10-50x menos em produção (via distillation)
- Evoluem continuamente com feedback de usuários

---

## CONCEITOS-CHAVE

### 1. SFT (Supervised Fine-Tuning): Ensinar o CERTO

**O que é**: Treinar LLM com pares `(input, output_correto)` para especializar em tarefa específica.

**Metáfora**: Professor corrigindo exercícios com gabarito vermelho.

**Quando usar**:
- ✅ Você tem 1K-100K exemplos rotulados de qualidade
- ✅ Tarefa tem "resposta certa" objetiva (tradução, extração, classificação)
- ✅ LLM base não performa bem na tarefa mesmo com prompting avançado
- ✅ Você precisa de consistência alta (não pode tolerar variação)

**Quando NÃO usar**:
- ❌ Tarefa é subjetiva (tom, estilo, preferências)
- ❌ Você tem <500 exemplos (overfitting garantido)
- ❌ LLM base já performa 90%+ com bom prompt
- ❌ Custo/tempo de fine-tuning não vale ganho marginal

**Code Prático (PyTorch + HuggingFace)**:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import Dataset

# 1. PREPARAR DADOS
training_data = [
    {
        "input": "Resuma: [texto longo sobre IA...]",
        "output": "IA transforma indústrias via automação de tarefas complexas."
    },
    {
        "input": "Classifique sentimento: 'Adorei este produto!'",
        "output": "Positivo"
    },
    # ... 10K exemplos mínimo
]

# Converter para formato HuggingFace
dataset = Dataset.from_dict({
    "text": [f"{ex['input']}\n\n{ex['output']}" for ex in training_data]
})

# 2. CARREGAR MODELO BASE
model_name = "HuggingFaceTB/SmolLM2-1.7B-Instruct"  # Modelo pequeno, rápido
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# 3. TOKENIZAR
def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, max_length=512)

tokenized_dataset = dataset.map(tokenize_function, batched=True)

# 4. CONFIGURAR TREINAMENTO
training_args = TrainingArguments(
    output_dir="./modelo_finetuned",
    num_train_epochs=3,              # 3 epochs suficiente para fine-tune
    per_device_train_batch_size=4,   # Ajustar conforme GPU
    learning_rate=2e-5,               # LR baixo para não "esquecer" pre-training
    weight_decay=0.01,
    logging_steps=100,
    save_steps=1000,
    eval_strategy="steps",
    eval_steps=500,
    warmup_steps=200,
    fp16=True,                        # Mixed precision = 2x mais rápido
)

# 5. TREINAR
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
)

trainer.train()

# 6. SALVAR MODELO CUSTOMIZADO
model.save_pretrained("./modelo_finetuned_final")
tokenizer.save_pretrained("./modelo_finetuned_final")
```

**Hyperparameters Críticos**:
- `learning_rate`: 1e-5 a 5e-5 (menor = mais conservador, evita "esquecer" base)
- `num_epochs`: 2-5 (mais = overfitting, menos = underfitting)
- `batch_size`: Máximo que cabe na GPU (maior = mais estável)
- `warmup_steps`: 10-20% do total (aquece gradualmente)

**Validação Obrigatória**:
```python
# Sempre separe train/validation/test
# 80% train, 10% validation, 10% test

# Métricas essenciais:
# - Perplexity (quanto menor, melhor)
# - Acurácia na tarefa específica
# - Human evaluation (amostra de 100 outputs)

# Red flags:
# - Train loss cai mas val loss sobe = OVERFITTING
# - Model repete outputs = COLLAPSE
# - Perda de capacidade em outras tarefas = CATASTROPHIC FORGETTING
```

---

### 2. DPO (Direct Preference Optimization): Ensinar o MELHOR

**O que é**: Treinar LLM com pares `(prompt, resposta_boa, resposta_ruim)` para alinhar com preferências humanas **sem** reward model intermediário.

**Metáfora**: Sommelier escolhendo "este vinho > aquele vinho" sem precisar dar nota numérica.

**Diferença vs RLHF**:
```
RLHF (Complexo):
  Dados → Treina Reward Model → RL via PPO → Modelo alinhado
  Problema: Reward model pode ser instável, RL é difícil de calibrar

DPO (Simples):
  Dados → DPO direto → Modelo alinhado
  Vantagem: Sem reward model, mais estável, mais rápido
```

**Quando usar**:
- ✅ Tarefa tem múltiplas respostas "corretas" mas algumas são **melhores**
- ✅ Você tem feedback humano (thumbs up/down, rankings)
- ✅ Precisa alinhar tom, estilo, helpful vs harmful
- ✅ SFT já funcionou mas precisa de refinamento

**Quando NÃO usar**:
- ❌ Tarefa tem resposta binária certa/errada (use SFT)
- ❌ Feedback humano é inconsistente/ruidoso
- ❌ Você tem <1K pares de preferência

**Code Prático (TRL Library)**:

```python
from trl import DPOTrainer
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import Dataset

# 1. PREPARAR DADOS DPO
dpo_data = [
    {
        "prompt": "Escreva email profissional pedindo reunião",
        "chosen": "Prezado Sr. João,\n\nGostaria de agendar reunião...",  # ✅ Melhor
        "rejected": "Oi João, blz? Vamos marcar papo? Vlw"              # ❌ Pior
    },
    {
        "prompt": "Resuma este artigo sobre IA: [...]",
        "chosen": "IA revoluciona indústrias através de...",            # ✅ Claro
        "rejected": "IA tipo assim faz umas coisas legais..."           # ❌ Vago
    },
    # ... 5K-50K pares mínimo
]

dataset = Dataset.from_dict({
    "prompt": [ex["prompt"] for ex in dpo_data],
    "chosen": [ex["chosen"] for ex in dpo_data],
    "rejected": [ex["rejected"] for ex in dpo_data],
})

# 2. CARREGAR MODELO (já fine-tuned com SFT idealmente)
model = AutoModelForCausalLM.from_pretrained("./modelo_finetuned_final")
ref_model = AutoModelForCausalLM.from_pretrained("./modelo_finetuned_final")  # Frozen
tokenizer = AutoTokenizer.from_pretrained("./modelo_finetuned_final")

# 3. CONFIGURAR DPO
from trl import DPOConfig

dpo_config = DPOConfig(
    output_dir="./modelo_dpo",
    num_train_epochs=1,              # DPO geralmente 1 epoch suficiente
    per_device_train_batch_size=2,   # Precisa carregar 2 modelos = menos batch
    learning_rate=5e-7,               # Muito menor que SFT
    beta=0.1,                         # Força do KL penalty (0.1 padrão)
    logging_steps=10,
)

# 4. TREINAR DPO
trainer = DPOTrainer(
    model=model,
    ref_model=ref_model,
    args=dpo_config,
    train_dataset=dataset,
    tokenizer=tokenizer,
)

trainer.train()

# 5. SALVAR MODELO ALINHADO
model.save_pretrained("./modelo_dpo_final")
```

**Hyperparameter Beta**:
```python
# Beta controla trade-off entre seguir preferências vs manter capacidade original

beta = 0.01   # Muito permissivo, quase não muda
beta = 0.1    # Padrão, equilíbrio bom
beta = 0.5    # Agressivo, forte alinhamento mas pode perder capabilities
beta = 1.0    # Muito agressivo, risco de overfitting

# Regra: Comece com 0.1, aumente se model não alinha suficiente
```

**Pipeline Completo (SFT → DPO)**:
```python
# FASE 1: SFT com dados rotulados
sft_model = finetune_sft(
    base="SmolLM2-1.7B",
    data=labeled_examples,  # 10K exemplos com gabarito
)

# FASE 2: Coletar feedback em produção
# Usuários marcam outputs como 👍 ou 👎

# FASE 3: DPO com preferências
dpo_model = align_dpo(
    base=sft_model,
    data=preference_pairs,  # 5K pares (chosen/rejected)
)

# FASE 4: Deploy versão alinhada
deploy(dpo_model)

# FASE 5: Repeat mensalmente (continuous learning loop)
```

---

### 3. Knowledge Distillation: Comprimir INTELIGÊNCIA

**O que é**: Treinar modelo **pequeno** (aluno) para imitar modelo **grande** (professor), mantendo 70-90% da qualidade com 10-50x menos custo.

**Metáfora**: Mestre (GPT-4) ensinando aprendiz (SmolLM) — aprendiz nunca será mestre, mas aprende 80% das lições por 2% do preço.

**Quando usar**:
- ✅ Professor (GPT-4/Claude) é muito caro/lento para produção
- ✅ Você precisa rodar 1M+ chamadas/dia
- ✅ Latência é crítica (<100ms)
- ✅ Você aceita 10-20% de perda de qualidade por 50x redução de custo

**Trade-offs Reais**:
```
Professor (GPT-4):
  Qualidade: 10/10
  Custo: $0.03/1K tokens = $30/1M tokens
  Latência: 2-5 segundos

Aluno Destilado (SmolLM 1.7B):
  Qualidade: 7-8/10
  Custo: $0.0005/1K tokens = $0.50/1M tokens (60x mais barato!)
  Latência: 50-200ms (10-25x mais rápido!)

Vale a pena? DEPENDE do caso de uso.
```

**Casos Ideais para Distillation**:
1. **Chatbots de suporte**: Respostas repetitivas, padrões claros
2. **Classificação em escala**: Sentiment analysis, topic tagging
3. **Extração de dados**: Parsing de documentos estruturados
4. **Geração de variações**: Product descriptions, email templates

**Casos RUINS para Distillation**:
1. **Raciocínio complexo**: Matemática avançada, lógica multi-step
2. **Criatividade alta**: Copywriting premium, storytelling
3. **Domínio super-especializado**: Questões médicas/legais raras

**Code Prático (Soft Labels)**:

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# 1. CARREGAR PROFESSOR E ALUNO
professor = AutoModelForCausalLM.from_pretrained("gpt-4")  # Hipotético
aluno = AutoModelForCausalLM.from_pretrained("SmolLM2-1.7B")

tokenizer = AutoTokenizer.from_pretrained("SmolLM2-1.7B")

# 2. CORPUS DE TREINO (não precisa ser rotulado!)
corpus = load_unlabeled_documents(n=100_000)  # 100K docs

# 3. DISTILLATION LOOP
temperature = 2.0  # "Suaviza" probabilidades do professor

for doc in corpus:
    tokens = tokenizer(doc, return_tensors="pt")

    # Professor gera SOFT LABELS (distribuição de probabilidades)
    with torch.no_grad():
        professor_logits = professor(**tokens).logits / temperature
        professor_probs = torch.softmax(professor_logits, dim=-1)

    # Aluno tenta imitar distribuição
    aluno_logits = aluno(**tokens).logits / temperature
    aluno_probs = torch.softmax(aluno_logits, dim=-1)

    # Loss = KL Divergence (distância entre distribuições)
    kl_loss = torch.nn.functional.kl_div(
        torch.log(aluno_probs),
        professor_probs,
        reduction='batchmean'
    )

    # Backprop no aluno
    kl_loss.backward()
    optimizer.step()

# 4. VALIDAR ALUNO
# Compare outputs de professor vs aluno em test set
# Métricas: BLEU, ROUGE, Human eval
```

**Soft Labels vs Hard Labels**:
```python
# HARD LABEL (SFT tradicional)
# Binário: certo ou errado
input = "O gato"
label = "dorme"  # Única resposta aceita

# SOFT LABEL (Distillation)
# Distribuição de probabilidades do professor
input = "O gato"
soft_label = {
    "dorme": 0.45,    # Alta probabilidade
    "come": 0.20,     # Média probabilidade
    "pula": 0.15,     # Baixa probabilidade
    "mia": 0.10,      # Baixa
    "voa": 0.001      # Quase zero
}

# Vantagem: Aluno aprende NUANCES
# "dorme" é melhor, mas "come" não é absurdo
# "voa" é virtualmente impossível
```

**Pipeline Completo de Distillation**:

```python
from distillation_lib import DistillationPipeline  # Hipotético

# FASE 1: Definir Professor e Aluno
pipeline = DistillationPipeline(
    teacher="gpt-4-turbo",           # Ou Claude Sonnet 4
    student="SmolLM2-1.7B-base",     # Modelo leve
    task="summarization"             # Tarefa específica
)

# FASE 2: Coletar dados não rotulados
corpus = load_domain_documents(
    domain="ecommerce",
    n=50_000
)

# FASE 3: Professor gera labels automáticos
labeled_corpus = pipeline.teacher_label(
    corpus=corpus,
    output_format="summary"
)

# FASE 4: Treinar aluno com soft labels
student_model = pipeline.distill(
    data=labeled_corpus,
    epochs=10,
    temperature=2.0,
    alpha=0.7  # 70% soft labels, 30% hard labels
)

# FASE 5: Validar tradeoff qualidade/custo
metrics = pipeline.evaluate(
    test_set=validation_data,
    metrics=["quality", "latency", "cost"]
)

print(metrics)
# {
#   "quality": 0.82,        # 82% da qualidade do professor
#   "latency": "120ms",     # 15x mais rápido
#   "cost_reduction": "52x" # 52x mais barato
# }

# FASE 6: Deploy se trade-off aceitável
if metrics["quality"] > 0.75 and metrics["cost_reduction"] > 20:
    deploy_student(student_model)
```

---

## COMO APLICAR: Workflow Completo

### Use Case Real: Agente Anúncio (CODEXA)

**Problema**: Anuncio_Agent usa GPT-4 para gerar copy de marketplace. Custo = $500/mês para 100K gerações.

**Solução**: SFT → DPO → Distillation

**FASE 1: SFT (Especializar)**
```python
# Coletar 10K exemplos reais de anúncios high-performing
training_data = [
    {
        "input": "Produto: Tênis Nike Air Max\nEspecs: Tamanho 42, Preto...",
        "output": "Tênis Nike Air Max Preto 42 | Conforto Máximo | Entrega Rápida SP"
    },
    # ... 10K exemplos
]

# Fine-tune SmolLM
anuncio_sft = finetune_sft(
    base="SmolLM2-1.7B",
    data=training_data,
    epochs=3
)

# Resultado: Modelo especializado em copy de marketplace
```

**FASE 2: DPO (Alinhar com Conversão)**
```python
# Coletar feedback real: quais anúncios converteram melhor?
dpo_data = [
    {
        "prompt": "Gere anúncio para: Tênis Nike...",
        "chosen": "Título otimizado que converteu 8%",    # A/B test winner
        "rejected": "Título genérico que converteu 2%"   # A/B test loser
    },
    # ... 5K pares
]

# Alinhar com conversão real
anuncio_dpo = align_dpo(
    base=anuncio_sft,
    data=dpo_data
)

# Resultado: Modelo que gera copy que CONVERTE
```

**FASE 3: Distillation (Otimizar Custo)**
```python
# Professor = anuncio_dpo (já especializado)
# Aluno = SmolLM-360M (4x menor)

anuncio_distilled = distill(
    teacher=anuncio_dpo,
    student="SmolLM-360M-base",
    corpus=unlabeled_product_specs  # 100K specs não rotulados
)

# Resultado:
# - Qualidade: 88% do modelo DPO
# - Custo: $10/mês (50x redução!)
# - Latência: 80ms (20x mais rápido)
```

**ROI Final**:
- Investimento: 3 semanas de dev + $200 em compute
- Economia anual: $500/mês → $10/mês = $5.880/ano
- Payback: <1 mês

---

## ARMADILHAS COMUNS

### ❌ Erro 1: Fine-tune com dados ruins
```python
# RUIM: Dados sujos, inconsistentes
bad_data = [
    {"input": "resumo isso", "output": "resumo de algo"},  # Vago
    {"input": "Traduza: hello", "output": "olá"},          # Ok
    {"input": "classifique", "output": "positivo"},        # Sem contexto
]

# BOM: Dados limpos, consistentes, diversos
good_data = [
    {"input": "Resuma em 2 frases: [texto completo 200 palavras]",
     "output": "Frase 1 clara. Frase 2 clara."},
    {"input": "Traduza para português formal: 'Hello, how are you?'",
     "output": "Olá, como você está?"},
]

# REGRA: 1K exemplos excelentes > 10K exemplos medíocres
```

### ❌ Erro 2: Overfitting (memorizar em vez de generalizar)
```python
# Sinais de overfitting:
# - Train loss: 0.05 (excelente)
# - Val loss: 2.5 (péssimo)
# - Model repete exatamente exemplos de treino
# - Performa mal em inputs ligeiramente diferentes

# Solução:
# - Reduzir epochs (3 → 1)
# - Aumentar dropout (0.1 → 0.3)
# - Adicionar regularização (weight_decay=0.01)
# - Aumentar diversidade de dados
```

### ❌ Erro 3: Escolher tarefa errada para distillation
```python
# RUIM para distillation:
# - Raciocínio complexo (ex: provas matemáticas)
# - Tarefas ultra-especializadas (ex: diagnóstico médico raro)
# - Criatividade alta (ex: roteiro de filme)

# BOM para distillation:
# - Classificação (ex: sentiment analysis)
# - Extração (ex: NER, parsing)
# - Geração de variações (ex: paraphrasing)
# - Tarefas repetitivas com padrões claros
```

---

## QUANDO USAR: Decision Tree

```
Preciso customizar LLM?
  ├─ LLM base + bom prompt já funciona 90%+?
  │   └─ NÃO FINE-TUNE. Use prompting avançado.
  │
  ├─ Tenho 1K-100K exemplos rotulados?
  │   ├─ SIM → Use SFT
  │   └─ NÃO → Colete dados primeiro
  │
  ├─ Tarefa é objetiva (resposta certa) ou subjetiva (preferência)?
  │   ├─ Objetiva → SFT suficiente
  │   └─ Subjetiva → SFT + DPO
  │
  └─ Custo/latência são críticos?
      ├─ SIM → Após SFT/DPO, faça Distillation
      └─ NÃO → Deploy modelo fine-tuned diretamente
```

---

## RELACIONADO

- Ver também: LLM_prompting_best_practices_20251120.md (quando prompting basta)
- Ver também: LLM_context_management_strategies_20251120.md (otimizar context window)
- Ver também: MULTIAGENT_arquitetura_sistemas_20251120.md (agents especializados via fine-tune)

---

**Fonte**:
- KNOWLEDGE_DISTILLATION_STRATEGY.md
- 04_CONHECIMENTO_APRENDIZADO_META.md
- SmolLM Training Playbook (HuggingFace)
**Processado**: 2025-11-24
**Quality Score**: 0.92/1.0
