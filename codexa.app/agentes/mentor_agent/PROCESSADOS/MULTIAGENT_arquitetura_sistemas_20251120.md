# Arquitetura Multi-Agent: Quando Usar Múltiplos LLMs vs Single LLM

**Categoria**: multiagent_systems
**Qualidade**: 0.88/1.00
**Data**: 20251120

## Conteúdo

### O Problema com Single-LLM para Tarefas Complexas

Imagine pedir para um único especialista construir uma casa inteira — arquitetura, elétrica, encanamento, acabamento. Tecnicamente possível, mas o resultado é medíocre comparado a uma equipe de especialistas. O mesmo se aplica a LLMs.

**Single-LLM**: Um modelo tentando fazer tudo. Funciona para tarefas simples, falha em workflows complexos.

**Multi-Agent**: Múltiplos modelos, cada um especializado em uma etapa. Orquestração coordenada produz output superior.

### Quando Usar Single-LLM (Simplicidade Vence)

✅ **Tarefas atômicas**: "Traduza este texto para inglês", "Resuma este artigo em 3 frases"
✅ **Latência crítica**: Quando você precisa de resposta em <2 segundos
✅ **Budget limitado**: Um LLM custa menos que orquestrar 5
✅ **Domínio narrow**: Tarefa específica onde especialização extra não adiciona valor
✅ **Prototipagem rápida**: MVP onde "good enough" é suficiente

**Exemplo**: Chatbot de FAQ simples. Single-LLM com prompt bem escrito resolve 95% dos casos.

### Quando Usar Multi-Agent (Complexidade Justifica)

✅ **Workflows de múltiplas etapas**: Pesquisa de mercado → Análise → Geração de copy → Validação → Formatação
✅ **Especialização de domínios**: Cada agente domina um nicho (ex: CODEXA tem 6 agentes especializados)
✅ **Quality gates**: Agente validador revisa output de agente gerador antes de entregar ao usuário
✅ **Paralelização**: Múltiplos agentes trabalham simultaneamente em subtasks independentes
✅ **Separação de concerns**: Agente de dados nunca escreve copy; agente de copy nunca consulta database

**Exemplo**: Sistema CODEXA. Anuncio_agent gera copy, Marca_agent valida tom de voz, Mentor_agent revisa qualidade. Resultado final é superior a qualquer agente sozinho.

### As 4 Arquiteturas Multi-Agent Fundamentais

#### 1. **Pipeline Sequencial** (A → B → C)

**Como funciona**: Output do Agente A é input do Agente B, que passa para Agente C.

**Quando usar**: Workflow linear onde cada etapa depende da anterior.

**Exemplo real**:
```
[Research Agent] → Coleta dados de mercado
    ↓
[Analysis Agent] → Extrai insights
    ↓
[Copy Agent] → Gera anúncio otimizado
    ↓
[Validation Agent] → Valida compliance ANVISA/INMETRO
```

**Prós**: Simples de implementar, fácil de debugar
**Contras**: Latência alta (soma de todos os agentes), falha em A quebra toda a pipeline

#### 2. **Scatter-Gather Paralelo** (A + B + C → Agregador)

**Como funciona**: Múltiplos agentes processam o mesmo input em paralelo, um agregador consolida os outputs.

**Quando usar**: Você quer múltiplas perspectivas ou precisa de velocidade.

**Exemplo real**:
```
Input: "Notebook Dell Inspiron 15"

[Agent 1: Concorrentes ML] → Lista 10 competidores
[Agent 2: Keywords Shopee] → Lista 30 keywords
[Agent 3: Preço médio Amazon] → Análise de pricing

→ [Aggregator] → Relatório consolidado unificado
```

**Prós**: Rápido (paralelo), robusto (falha de 1 agente não quebra sistema)
**Contras**: Complexo agregar outputs inconsistentes, custo maior

#### 3. **Hierarchical Supervisor** (Boss → Workers)

**Como funciona**: Agente supervisor delega subtasks para agentes workers, que retornam resultados para o supervisor revisar e decidir próximos passos.

**Quando usar**: Tarefas complexas onde a sequência de subtasks não é previsível antecipadamente.

**Exemplo real**:
```
[Supervisor: Codexa Agent]
    ↓ Analisa tarefa: "Criar identidade de marca"
    ↓ Delega:
[Worker 1: Análise de concorrentes] → Retorna report
[Worker 2: Proposta de paleta de cores] → Retorna opções
[Worker 3: Sugestões de tipografia] → Retorna recomendações
    ↓ Supervisor consolida + decide se precisa refinamento
```

**Prós**: Flexível, adapta-se dinamicamente a tarefas imprevisíveis
**Contras**: Supervisor é ponto único de falha, custo alto de coordenação

#### 4. **Specialist Handoff** (Agente escolhe próximo agente)

**Como funciona**: Cada agente decide qual agente chamar em seguida baseado no resultado de seu processamento.

**Quando usar**: Workflow não-linear onde a próxima etapa depende do resultado da etapa atual.

**Exemplo real**:
```
[Entry Agent] → Classifica tipo de produto
    ↓
    Se "Suplemento": → [Compliance Agent (ANVISA)]
    Se "Eletrônico": → [Compliance Agent (INMETRO)]
    Se "Têxtil": → [Copy Agent direto]
```

**Prós**: Eficiente (só chama agentes necessários), modular
**Contras**: Difícil prever fluxo completo, debugar é complexo

### Patterns Arquiteturais do CODEXA

O sistema CODEXA usa **Specialist Vertical + Hierarchical Supervisor**:

**6 Agentes Especialistas Verticais**:
- anuncio_agent (copywriting + compliance)
- pesquisa_agent (market research)
- marca_agent (branding)
- photo_agent (imagem + IA)
- mentor_agent (QA + ensino)
- codexa_agent (meta-construção)

**Hierarchical Coordination**: `/prime` (navigator) age como supervisor, direcionando usuário para agente especialista correto.

**Por que funciona**: Cada agente tem iso_vectorstore (conhecimento isolado), evitando "pollution" entre domínios. Anuncio_agent nunca precisa saber sobre meta-construção; Mentor_agent nunca gera copy.

### Quando Multi-Agent Falha (Anti-Patterns)

❌ **Over-Engineering Simples Tasks**: Usar 3 agentes para traduzir texto é overkill

❌ **Coordenação Caótica**: Agentes chamando agentes sem estrutura clara vira spaghetti code

❌ **Duplicate Responsibilities**: Dois agentes fazendo a mesma coisa gera conflito e confusão

❌ **No Fallback Plan**: Se Agente A falha e B depende dele, sistema inteiro quebra

❌ **Custo Sem ROI**: Pagar 5x mais em LLM calls para ganhar 10% de qualidade raramente vale a pena

### Decision Framework: Single vs Multi?

**Use Single-LLM se**:
- Tarefa completa em <200 tokens de output
- Domínio único bem definido
- Latência importa mais que perfeição
- Budget é constraint primário

**Use Multi-Agent se**:
- Workflow tem ≥3 etapas distintas claramente separáveis
- Especialização por etapa aumenta qualidade mensuravelmente
- Validação/QA são críticos (agente validador dedicado)
- Custo extra (2-5x) é justificável pelo ganho de qualidade

### Implementação Prática: Do Zero ao Multi-Agent

**Fase 1: Prove Single-LLM (Semana 1)**
- Implemente versão monolítica
- Meça: latência, quality score, custo

**Fase 2: Identifique Bottlenecks (Semana 2)**
- Onde Single-LLM falha consistentemente?
- Qual etapa se beneficiaria mais de especialização?

**Fase 3: Extraia Primeiro Agente (Semana 3)**
- Separe a etapa mais crítica em agente dedicado
- Compare quality antes/depois

**Fase 4: Adicione Agentes Incrementalmente (Semana 4+)**
- Adicione um agente por vez
- Valide ROI de cada novo agente
- Se ganho de qualidade <15%, não vale a pena

### Métricas para Avaliar Arquitetura

**Latência End-to-End**: Tempo de primeira chamada até output final
- Target: <10s para 80% dos casos
- Single-LLM: 2-5s | Multi-Agent: 8-30s

**Quality Score** (humano ou LLM-as-judge):
- Target: >85% satisfaction
- Single-LLM típico: 70-80% | Multi-Agent bem feito: 85-95%

**Cost per Request**:
- Single-LLM: $0.01-0.05
- Multi-Agent (3-5 agentes): $0.05-0.25

**Failure Rate**:
- Single-LLM: 5-10% (alucinação, formato errado)
- Multi-Agent com validação: 1-3%

### Exemplo Completo: Criação de Anúncio ML

**Single-LLM Approach**:
```
Prompt: "Crie anúncio para [produto]. Inclua título, descrição, keywords."
→ LLM gera tudo de uma vez
→ Output: 80% bom, 15% precisa ajuste, 5% unusable
→ Tempo: 4s | Custo: $0.02
```

**Multi-Agent Approach (CODEXA)**:
```
1. [Pesquisa Agent] → Analisa concorrentes ML (8s, $0.04)
2. [Marca Agent] → Define tom de voz da marca (3s, $0.01)
3. [Anuncio Agent] → Gera copy otimizada com contexto (12s, $0.06)
4. [Mentor Agent] → Valida qualidade + compliance (5s, $0.02)

→ Output: 95% pronto para publicar, 5% ajuste cosmético
→ Tempo total: 28s | Custo total: $0.13
```

**Trade-off**: 7x tempo, 6.5x custo, mas 95% vs 80% de qualidade. Para seller profissional, o ROI justifica.

### Ferramentas e Frameworks

**Para começar**:
- [OPEN_VARIABLE: framework_orquestracao] (ex: LangGraph, CrewAI, AutoGen)
- [OPEN_VARIABLE: ferramenta_monitoring] (ex: LangSmith, Weights & Biases)

**Stack recomendado do CODEXA**:
- Python 3.11+
- Anthropic Claude Sonnet 4 (agentes principais)
- Haiku (validações rápidas)
- Custom orchestration (não framework externo para máximo controle)

---

## Orquestração Prática: Implementação Real

### Pattern 1: Sequential Pipeline (Research → Copy → Visual)

**Caso real**: Sistema CODEXA gerando anúncios completos.

```python
from anthropic import Anthropic
import json

class MultiAgentOrchestrator:
    """Orquestrador de pipeline sequencial de 3 agentes"""

    def __init__(self):
        self.client = Anthropic()
        self.agents = {
            "research": self.research_agent,
            "copy": self.copy_agent,
            "visual": self.visual_agent
        }

    def run_pipeline(self, brief: dict) -> dict:
        """
        Executa pipeline completo: Research → Copy → Visual

        Args:
            brief: {
                "produto": "Tênis Nike Air Max",
                "specs": "Tamanho 42, preto, running...",
                "marketplaces": ["mercadolivre", "shopee"]
            }

        Returns:
            {
                "research_notes": "...",
                "copy_pack": {...},
                "images": [...]
            }
        """

        # STAGE 1: Research
        research_output = self.agents["research"](brief)

        # STAGE 2: Copy (usa research como contexto)
        copy_output = self.agents["copy"](
            brief=brief,
            research_context=research_output
        )

        # STAGE 3: Visual (usa research + copy)
        visual_output = self.agents["visual"](
            brief=brief,
            research_context=research_output,
            copy_context=copy_output
        )

        return {
            "research_notes": research_output,
            "copy_pack": copy_output,
            "images": visual_output
        }

    def research_agent(self, brief: dict) -> str:
        """Agente 1: Pesquisa marketplace e SEO"""

        prompt = f"""Você é um especialista em research de marketplace.

TAREFA: Analise o mercado para este produto:
- Produto: {brief['produto']}
- Specs: {brief['specs']}
- Marketplaces: {brief['marketplaces']}

INSTRUÇÕES:
1. Identifique 5-10 keywords principais (head terms)
2. Liste 3-5 concorrentes diretos
3. Analise padrões de títulos que convertem
4. Identifique gaps de mercado

Retorne em formato markdown estruturado."""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

    def copy_agent(self, brief: dict, research_context: str) -> dict:
        """Agente 2: Copywriting otimizado"""

        prompt = f"""Você é um copywriter expert em marketplaces brasileiros.

CONTEXTO DE PESQUISA:
{research_context}

PRODUTO:
{brief['produto']}
{brief['specs']}

TAREFA: Gere copy otimizada para marketplace:
1. Título (70 caracteres, SEO-friendly)
2. Descrição persuasiva (200-300 palavras)
3. 5 bullets de benefícios

Retorne JSON:
{{
  "titulo": "...",
  "descricao": "...",
  "bullets": ["...", "...", ...]
}}"""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

    def visual_agent(self, brief: dict, research_context: str, copy_context: dict) -> list:
        """Agente 3: Geração de conceitos visuais"""

        prompt = f"""Você é um diretor de arte para e-commerce.

RESEARCH:
{research_context}

COPY:
Título: {copy_context['titulo']}
Descrição: {copy_context['descricao']}

TAREFA: Crie 3 conceitos visuais para este produto.
Para cada conceito, descreva:
- Scene description (para fotografia)
- Composição visual
- Mood e lighting

Retorne JSON array:
[
  {{"concept": "...", "scene": "...", "composition": "...", "mood": "..."}},
  ...
]"""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        return json.loads(response.content[0].text)

# USO
orchestrator = MultiAgentOrchestrator()

brief = {
    "produto": "Tênis Nike Air Max 2024",
    "specs": "Running, tamanho 42, preto/branco, amortecimento Air...",
    "marketplaces": ["mercadolivre", "shopee"]
}

resultado = orchestrator.run_pipeline(brief)

print(resultado["copy_pack"]["titulo"])
# Output: "Tênis Nike Air Max 2024 Running Preto 42 | Amortecimento Air | Original"
```

### Pattern 2: Scatter-Gather Paralelo

**Caso real**: Pesquisar múltiplos marketplaces simultaneamente.

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class ParallelResearchOrchestrator:
    """Orquestrador paralelo para pesquisa multi-marketplace"""

    def __init__(self):
        self.client = Anthropic()

    async def research_parallel(self, produto: str, marketplaces: list) -> dict:
        """
        Pesquisa múltiplos marketplaces em paralelo

        Args:
            produto: "Tênis Nike Air Max"
            marketplaces: ["mercadolivre", "shopee", "amazon"]

        Returns:
            {
                "mercadolivre": {...},
                "shopee": {...},
                "amazon": {...}
            }
        """

        # Criar tasks paralelas (uma por marketplace)
        tasks = [
            self.research_marketplace(produto, mp)
            for mp in marketplaces
        ]

        # Executar em paralelo
        results = await asyncio.gather(*tasks)

        # Agregar resultados
        return {
            mp: result
            for mp, result in zip(marketplaces, results)
        }

    async def research_marketplace(self, produto: str, marketplace: str) -> dict:
        """Pesquisa um marketplace específico"""

        prompt = f"""Analise {marketplace} para: {produto}

Retorne:
1. 3 concorrentes principais
2. Faixa de preço
3. Keywords mais usadas
4. Padrão de títulos

JSON format."""

        # Executar em thread pool para não bloquear
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            response = await loop.run_in_executor(
                pool,
                lambda: self.client.messages.create(
                    model="claude-haiku-20250305",  # Haiku = mais rápido/barato
                    max_tokens=800,
                    messages=[{"role": "user", "content": prompt}]
                )
            )

        return json.loads(response.content[0].text)

# USO
orchestrator = ParallelResearchOrchestrator()

resultado = asyncio.run(
    orchestrator.research_parallel(
        produto="Tênis Nike Air Max",
        marketplaces=["mercadolivre", "shopee", "amazon"]
    )
)

# Resultado: 3x mais rápido que sequencial
# Tempo: ~8s (paralelo) vs ~24s (sequencial)
```

### Error Handling e Fallbacks

```python
class ResilientOrchestrator:
    """Orquestrador com error handling robusto"""

    def __init__(self):
        self.client = Anthropic()
        self.max_retries = 3
        self.fallback_model = "claude-haiku-20250305"

    def run_with_fallback(self, agent_func, *args, **kwargs):
        """
        Executa agente com retry + fallback automático

        Estratégia:
        1. Tenta com modelo principal (Sonnet)
        2. Se falha, retry 3x
        3. Se continua falhando, tenta Haiku (mais simples/robusto)
        4. Se Haiku falha, retorna resposta degradada
        """

        # Tentativa 1: Modelo principal
        for attempt in range(self.max_retries):
            try:
                return agent_func(*args, **kwargs)
            except Exception as e:
                if attempt < self.max_retries - 1:
                    print(f"Retry {attempt + 1}/{self.max_retries}: {e}")
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print(f"Modelo principal falhou. Tentando fallback...")

        # Tentativa 2: Fallback para Haiku
        try:
            return agent_func(*args, model=self.fallback_model, **kwargs)
        except Exception as e:
            print(f"Fallback falhou: {e}")
            return self.degraded_response(*args)

    def degraded_response(self, *args):
        """Resposta degradada quando tudo falha"""
        return {
            "status": "degraded",
            "message": "Não foi possível gerar resposta completa",
            "partial_data": {}
        }

# USO
orchestrator = ResilientOrchestrator()

resultado = orchestrator.run_with_fallback(
    orchestrator.research_agent,
    brief={"produto": "..."}
)

# Se Sonnet falhar → tenta Haiku
# Se Haiku falhar → retorna resposta degradada (não quebra sistema)
```

### Monitoring e Observability

```python
import time
from functools import wraps

class ObservableOrchestrator:
    """Orquestrador com monitoring completo"""

    def __init__(self):
        self.client = Anthropic()
        self.metrics = {
            "requests": 0,
            "errors": 0,
            "total_latency": 0,
            "total_cost": 0
        }

    def monitor(self, agent_name: str):
        """Decorator para monitorar execução de agentes"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start = time.time()

                try:
                    # Executar agente
                    result = func(*args, **kwargs)

                    # Registrar sucesso
                    latency = time.time() - start
                    self.log_success(agent_name, latency, result)

                    return result

                except Exception as e:
                    # Registrar erro
                    self.log_error(agent_name, str(e))
                    raise

            return wrapper
        return decorator

    def log_success(self, agent_name: str, latency: float, result: any):
        """Log de execução bem-sucedida"""
        self.metrics["requests"] += 1
        self.metrics["total_latency"] += latency

        # Estimar custo (aproximado)
        tokens = len(str(result)) / 4  # Estimativa rough
        cost = tokens * 0.000003  # $0.003/1K tokens
        self.metrics["total_cost"] += cost

        print(f"✅ {agent_name}: {latency:.2f}s | ${cost:.4f}")

    def log_error(self, agent_name: str, error: str):
        """Log de erro"""
        self.metrics["errors"] += 1
        print(f"❌ {agent_name}: {error}")

    def get_metrics(self) -> dict:
        """Retorna métricas agregadas"""
        return {
            "total_requests": self.metrics["requests"],
            "error_rate": self.metrics["errors"] / max(self.metrics["requests"], 1),
            "avg_latency": self.metrics["total_latency"] / max(self.metrics["requests"], 1),
            "total_cost": self.metrics["total_cost"]
        }

    @monitor("research")
    def research_agent(self, brief: dict) -> str:
        """Agente monitorado"""
        # ... implementação ...
        pass

# USO
orchestrator = ObservableOrchestrator()

# Executar 100 requests
for i in range(100):
    orchestrator.research_agent(brief={...})

# Ver métricas
metrics = orchestrator.get_metrics()
print(f"""
Total Requests: {metrics['total_requests']}
Error Rate: {metrics['error_rate']:.2%}
Avg Latency: {metrics['avg_latency']:.2f}s
Total Cost: ${metrics['total_cost']:.2f}
""")

# Output:
# Total Requests: 100
# Error Rate: 2.00%
# Avg Latency: 3.42s
# Total Cost: $1.45
```

### Quando Usar Cada Pattern

**Sequential Pipeline**:
- ✅ Cada etapa depende da anterior
- ✅ Ordem importa (research antes de copy)
- ✅ Latência não é crítica (<30s aceitável)

**Scatter-Gather Paralelo**:
- ✅ Subtasks independentes
- ✅ Latência crítica (precisa ser rápido)
- ✅ Quer múltiplas perspectivas

**Hierarchical Supervisor**:
- ✅ Workflow dinâmico (não previsível)
- ✅ Agente supervisor decide próximos passos
- ✅ Tarefas complexas com múltiplos caminhos possíveis

---

## Relacionado

- Ver também: LLM_fine_tuning_distillation_pratico_20251124.md (customizar agentes)
- Ver também: MULTIAGENT_adw_workflow_5_fases_20251120.md (workflow ADW detalhado)
- Ver também: METACONSTRUCAO_tac7_framework_20251120.md (criar novos agentes)

---

**Tags**: multiagent, arquitetura, orquestracao, pipeline, single-llm, especialização, error-handling, monitoring
**Palavras-chave**: Multi-agent, arquitetura, orquestração, pipeline, coordenação, specialists, fallback, observability
**Origem**: curso_agent/PRIME.md + 06_MODULO_META_CONSTRUCAO.md + 01_AGENTES_AI_ORQUESTRACAO.md + 02_WORKFLOWS_AGENTES_CRIACAO.md
**Processado**: 20251120
**Atualizado**: 20251124 (adicionadas seções práticas de orquestração)
