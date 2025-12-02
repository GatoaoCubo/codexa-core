# ADW Workflow: 5-Phase Agent Development from Zero to Production

**Categoria**: multiagent_workflows
**Qualidade**: 0.89/1.00
**Data**: 20251120

## Conteúdo

### O Problema com Desenvolvimento Ad-Hoc de Agentes

**Approach comum (falha 60% das vezes)**:
"Vou criar um agente que faz X. [3 horas codando] Pronto! [deployment] [bugs em produção] [usuários confusos] [documentação inexistente]"

**Resultado**: Agente funciona no happy path, quebra em edge cases, ninguém além do criador entende como usar, manutenção é pesadelo.

**ADW Workflow resolve**: Processo estruturado em 5 fases que garante agentes production-ready, documentados, testados e mantíveis.

**Analogia**: ADW é o "Agile/Scrum" do desenvolvimento de agentes LLM. Não pule etapas.

### As 5 Fases do ADW (Agent Development Workflow)

#### **FASE 1: DISCOVERY (Descoberta)** [Duration: 1-3 dias]

**Objetivo**: Entender PROFUNDAMENTE o problema antes de escrever uma linha de código.

**Atividades obrigatórias**:

1. **Problem Definition**
```
- O QUE o agente deve fazer? (tarefa específica, não vaga)
- PARA QUEM? (persona específica de usuário)
- POR QUE existente não resolve? (gap analysis)
```

2. **Research Existing Solutions**
```
- Há agentes similares no mercado? (LangChain, CrewAI examples)
- O que eles fazem BEM?
- O que eles fazem MAL? (oportunidade de diferenciação)
```

3. **Requirements Gathering**
```
Functional Requirements:
- Input: [formato exato, validações]
- Processing: [etapas necessárias]
- Output: [formato exato, success criteria]

Non-Functional Requirements:
- Latency: [≤X segundos]
- Cost: [≤$Y por request]
- Quality: [≥Z% consistency]
```

4. **User Stories**
```
As a [USER_PERSONA],
I want to [TASK],
So that [BUSINESS_VALUE]

Example:
As a Brazilian e-commerce seller,
I want to generate marketplace-compliant product descriptions in <60 seconds,
So that I can publish 20+ products per day without manual copywriting
```

5. **Success Metrics Definition**
```
- Metric 1: [quantificável, ex: "95% dos outputs não requerem edição humana"]
- Metric 2: [latência, ex: "p95 latency ≤10s"]
- Metric 3: [custo, ex: "≤$0.15 per generation"]
```

**Deliverables Fase 1**:
- `DISCOVERY_REPORT.md` (5-10 páginas)
- User stories (3-7 histórias principais)
- Success metrics dashboard mockup

**Validation Gate**: Stakeholders aprovam problem definition e success metrics antes de prosseguir.

#### **FASE 2: DESIGN (Arquitetura)** [Duration: 2-5 dias]

**Objetivo**: Projetar arquitetura do agente ANTES de implementar.

**Atividades obrigatórias**:

1. **Agent Architecture Diagram**
```
[User Input]
    ↓
[Input Validator] → reject if invalid
    ↓
[Context Loader] → load from iso_vectorstore
    ↓
[LLM Orchestrator] → main processing
    ↓
[Output Formatter] → structure output
    ↓
[Quality Validator] → check constraints
    ↓
[User Output]
```

2. **HOPs Identification**
```
Liste TODOS os procedimentos que o agente executará.
Para cada um, escreva draft TAC-7:
- HOP_01: [Tarefa 1]
- HOP_02: [Tarefa 2]
- HOP_03: [Tarefa 3]
... etc
```

3. **Data Flow Specification**
```json
{
  "input_schema": {
    "field1": {"type": "string", "max_length": 100, "required": true},
    "field2": {"type": "array", "items": "string", "required": false}
  },
  "output_schema": {
    "result": {"type": "string", "format": "markdown"},
    "confidence": {"type": "float", "min": 0.0, "max": 1.0},
    "metadata": {"type": "object"}
  }
}
```

4. **Technology Stack Selection**
```
- LLM: [OPEN_VARIABLE: modelo_escolhido] (justificar por quê)
- Orquestração: [OPEN_VARIABLE: framework_escolhido] ou custom?
- Storage: iso_vectorstore (20 files) + [OPEN_VARIABLE: db_opcional]
- Monitoring: [OPEN_VARIABLE: ferramenta_observability]
```

5. **Error Handling Strategy**
```
IF input invalid → RETURN error message (never hallucinate fix)
IF LLM timeout → RETRY 2x with exponential backoff → THEN fallback
IF output validation fails → LOG + ALERT → RETURN partial result with warning
```

6. **Cost & Latency Budget**
```
Target: ≤$0.15 per request, ≤10s p95 latency

Budget breakdown:
- Input processing: $0.01, 0.5s
- LLM call (main): $0.10, 7s
- Output formatting: $0.02, 1s
- Validation: $0.02, 1.5s
TOTAL: $0.15, 10s ✅
```

**Deliverables Fase 2**:
- `DESIGN_DOC.md` (15-25 páginas com diagramas)
- HOPs drafts (TAC-7 skeleton)
- Schemas (JSON para input/output)
- Technology decision record (ADR format)

**Validation Gate**: Tech lead aprovação arquitetura + viabilidade orçamentária.

#### **FASE 3: DEVELOP (Implementação)** [Duration: 1-2 semanas]

**Objetivo**: Implementar o agente seguindo rigorosamente o design.

**Atividades obrigatórias**:

1. **Directory Structure Setup**
```
novo_agent/
├── PRIME.md (contexto do agente, 400-600 linhas)
├── README.md (quick start para usuários)
├── INSTRUCTIONS.md (guia de operação detalhado)
├── iso_vectorstore/ (20 arquivos de conhecimento)
│   ├── 01_QUICK_START.md
│   ├── 02_PRIME.md
│   ├── 09_HOP_main.md
│   ├── 10_HOP_secondary.md
│   ├── 11_ADW_workflow.md
│   └── ... (15 more)
├── workflows/ (HOPs completos TAC-7)
│   ├── HOP_01_main_task.md
│   ├── HOP_02_validation.md
│   └── ...
├── prompts/ (prompts LLM)
│   ├── main_orchestrator.md (400+ linhas)
│   ├── validator.md (200+ linhas)
│   └── ...
└── tests/ (unit + integration tests)
    ├── test_input_validation.py
    ├── test_llm_orchestration.py
    └── ...
```

2. **Implementation Order** (critical!)
```
Week 1:
- Day 1-2: Input validator + schemas
- Day 3-4: Context loader (iso_vectorstore)
- Day 5: Main LLM orchestrator (basic version)

Week 2:
- Day 1-2: Output formatter + validation
- Day 3: Error handling + retries
- Day 4-5: Polish + edge cases
```

3. **Code Quality Standards**
```python
# Example: Input validator
def validate_input(data: dict) -> tuple[bool, Optional[str]]:
    """
    Validates user input against schema.

    Args:
        data: Raw input from user

    Returns:
        (is_valid, error_message)

    Raises:
        Never raises (returns error message instead)
    """
    schema = load_schema("input_schema.json")

    try:
        validate(instance=data, schema=schema)
        return (True, None)
    except ValidationError as e:
        return (False, f"Validation failed: {e.message}")
```

4. **Prompt Engineering** (iterative)
```
V1: Basic prompt (200 tokens)
→ Test 10 samples
→ Identify failures
V2: Add constraints + examples (400 tokens)
→ Test 20 samples
→ Quality +30%
V3: Add error handling instructions (450 tokens)
→ Test 30 samples
→ Quality +15%
V4: Production-ready (480 tokens)
```

5. **Testing Throughout** (NOT after!)
```bash
# Run tests after EVERY feature implementation
pytest tests/ --verbose

# Maintain coverage ≥80%
pytest --cov=novo_agent tests/

# Integration tests with real LLM
pytest tests/integration/ --slow
```

**Deliverables Fase 3**:
- Working agent code (all components)
- 20 iso_vectorstore files populated
- HOPs TAC-7 completos (≥3 HOPs)
- Test suite (≥80% coverage)

**Validation Gate**: All tests pass + code review approved.

#### **FASE 4: VALIDATE (Validação & QA)** [Duration: 3-5 dias]

**Objetivo**: Garantir que agente atende requisitos de qualidade ANTES de deployment.

**Atividades obrigatórias**:

1. **5-Dimension Quality Check** (inspirado no mentor_agent)
```
Dimension 1: COMPLETENESS (100% de features implementadas?)
Dimension 2: CLARITY (documentação legível por novatos?)
Dimension 3: ACCURACY (outputs factuais corretos?)
Dimension 4: RELEVANCE (resolve problema real de usuário?)
Dimension 5: ACTIONABILITY (usuário consegue usar sem help?)

Score mínimo: ≥0.75/1.0 em CADA dimensão
```

2. **Benchmark Testing**
```
Test com 50+ inputs diversos:
- 30 happy path (casos típicos)
- 15 edge cases (inputs incomuns mas válidos)
- 5 error cases (inputs inválidos)

Métricas:
- Success rate: ≥90% (happy path) + ≥70% (edge cases)
- Latency p50: ≤7s, p95: ≤10s, p99: ≤15s
- Cost per request: ≤$0.15
- Quality score: ≥8/10 (human evaluation)
```

3. **User Acceptance Testing** (UAT)
```
Recrute 3-5 usuários beta (target persona):
- Dê acesso ao agente
- NÃO explique como usar (teste se README é suficiente)
- Observe sessões (screen recording)
- Colete feedback estruturado

Success: ≥80% conseguem primeira tarefa sem ajuda
```

4. **Load Testing**
```bash
# Simule carga de 100 requests simultâneos
locust -f load_test.py --users 100 --spawn-rate 10

Target:
- No crashes
- Latency degradation ≤20% (p95)
- Error rate ≤5%
```

5. **Security Review**
```
Checklist:
☐ Input sanitization (SQL injection, XSS)
☐ API keys não hardcoded (usar env vars)
☐ Rate limiting implementado
☐ Logs não expõem dados sensíveis
☐ GDPR compliance (se aplicável)
```

**Deliverables Fase 4**:
- Quality report (5-dimension scores)
- Benchmark results (50+ tests)
- UAT feedback summary
- Load test report
- Security audit passed

**Validation Gate**: Quality score ≥0.85 overall + UAT success ≥80%.

#### **FASE 5: DOCUMENT (Documentação & Handoff)** [Duration: 2-3 dias]

**Objetivo**: Documentar TUDO para que outros possam usar/manter o agente.

**Atividades obrigatórias**:

1. **PRIME.md (Contexto Completo)**
```markdown
# /prime-[nome_agente]

## Purpose
[1 parágrafo: O QUE o agente faz e PARA QUEM]

## Architecture Pillars
### 4 IN-AGENT Pillars
[Contexto, Modelo, Tools, Prompts]

### 8 OUT-AGENT Pillars
[Templates, Output, Types, Docs, Tests, Architecture, Plans, ADWs]

## Specialty
[Capabilities específicas, quando usar vs quando não usar]

## Key Files
[Lista de todos os arquivos importantes + descrição]

## Workflows
[Principais workflows/HOPs + quando usar cada um]
```

2. **README.md (Quick Start)**
```markdown
# [Nome Agent]

## What it does
[2 parágrafos: problema que resolve + como resolve]

## Quick Start
```bash
# 3-5 comandos para começar
/prime-[nome]
"[exemplo de prompt]"
```

## Key Features
- Feature 1
- Feature 2
- Feature 3

## Examples
[3 exemplos: básico, intermediário, avançado]

## Troubleshooting
[5 problemas comuns + soluções]
```

3. **INSTRUCTIONS.md (Operational Guide)**
```markdown
Gerado automaticamente via doc_sync ou escrito manualmente.
Contém:
- Todos os HOPs do agente (TAC-7 completo)
- Comandos disponíveis
- Edge cases conhecidos
- Maintenance procedures
```

4. **Video Walkthrough** (optional mas recomendado)
```
- 5-10 min screencast
- Mostra uso básico + 1 exemplo avançado
- Narrado explicando decisões
- Hospedado no YouTube/Loom
```

5. **Handoff Checklist**
```
☐ PRIME.md completo (400+ linhas)
☐ README.md com quick start
☐ INSTRUCTIONS.md operacional
☐ 20 iso_vectorstore files populated
☐ ≥3 HOPs TAC-7 documentados
☐ Tests passing (≥80% coverage)
☐ Deployment guide (como colocar em produção)
☐ Monitoring setup (dashboards configurados)
☐ Handoff meeting scheduled (transferência para time de ops)
```

**Deliverables Fase 5**:
- Documentação completa (PRIME + README + INSTRUCTIONS)
- Video walkthrough
- Handoff meeting completed

**Validation Gate**: Novo membro do time consegue fazer deployment seguindo documentação.

### Métricas de Sucesso do ADW

**Process Metrics**:
- Total duration: 2-4 semanas (discovery → production)
- Rework rate: ≤15% (quão frequentemente precisa refazer fases)
- Documentation completeness: 100% (nenhum placeholder/TODO restante)

**Quality Metrics**:
- 5-dimension score: ≥0.85
- Test coverage: ≥80%
- UAT success: ≥80%
- Production uptime (first month): ≥99.5%

### Anti-Patterns do ADW (Erros Fatais)

❌ **Pular Discovery**: "Sei o que preciso, vou direto pro código"
→ Resultado: Resolve problema errado ou de forma subótima

❌ **Design minimalista**: "Vou descobrindo enquanto codifico"
→ Resultado: Refactoring constante, arquitetura spaghetti

❌ **Desenvolver sem testar**: "Vou testar tudo no fim"
→ Resultado: Bugs descobertos tarde, difíceis de corrigir

❌ **Validation superficial**: "Testei 3 casos, funciona"
→ Resultado: Edge cases quebram em produção

❌ **Documentação afterthought**: "Vou documentar quando tiver tempo"
→ Resultado: Documentação never happens, agente é unmaintainable

### Tools & Templates

**Template ADW Tracking**:
```markdown
# ADW Tracker: [Nome Agent]

## Status Dashboard
- DISCOVERY: ✅ Complete (2024-11-15)
- DESIGN: ✅ Complete (2024-11-18)
- DEVELOP: 🟨 In Progress (60% done)
- VALIDATE: ⬜ Not Started
- DOCUMENT: ⬜ Not Started

## Metrics
- Days elapsed: 8/20
- Budget spent: $450/$1000
- Quality score (current): 0.78/1.0
- Test coverage: 75%/80%
```

**Ferramentas recomendadas**:
- Project management: [OPEN_VARIABLE: ferramenta_gestao] (ex: Linear, GitHub Projects)
- Documentation: [OPEN_VARIABLE: ferramenta_docs] (ex: Notion, Obsidian)
- Testing: pytest + [OPEN_VARIABLE: ferramenta_eval]

---

**Tags**: adw, workflow, agent-development, 5-phase, discovery, design, develop, validate, document
**Palavras-chave**: ADW, workflow, 5 fases, desenvolvimento, agentes, processo, qualidade
**Origem**: curso_agent/PRIME.md + 06_MODULO_META_CONSTRUCAO.md + iso_vectorstore/11_ADW_workflow.md
**Processado**: 20251120
