# HOP_TAC7: Transformar Documentos em Módulos de Curso Digital

> **Propósito**: Converter qualquer documento-base (artigo, whitepaper, manual, relatório) em um curso digital modular, claro e acessível, usando **axiomas didáticos** e **metáforas explicativas** para driblar jargões técnicos sem perder rigor.

---

## 1) MODULE_METADATA
- **id**: `doc2course_axiomas_metaforas.v1`
- **version**: `1.0.0`
- **category**: `builder` | `curriculum`
- **owner**: `codexa_agent`
- **dependencies**: `None`
- **tags**: ["curriculum", "metáforas", "axiomas", "clareza", "antijargão", "instrucional"]
- **inputs_contract_ref**: `INPUT_CONTRACT`
- **outputs_contract_ref**: `OUTPUT_CONTRACT`
- **quality_gates**: `VALIDATION`

---

## 2) INPUT_CONTRACT
Estrutura e validação dos **$variables**.

```yaml
$variables:
  $doc:
    type: string|markdown|html|pdf_text
    required: true
    description: Conteúdo textual do documento-base (ou extração OCR se PDF).
    examples:
      - "Manual técnico do produto X, seções 1–6, 8.2" 
  $audiencia:
    type: string
    required: true
    enum_examples:
      - iniciantes
      - técnicos em migração
      - gestores não técnicos
  $objetivos:
    type: list[string]
    required: true
    description: Objetivos de aprendizagem mensuráveis (estilo Bloom).
    example:
      - "Explicar o conceito A em termos cotidianos"
      - "Aplicar o processo B em um caso prático"
  $escopo:
    type: string
    required: false
    default: "essencial"
    enum: [essencial, estendido]
  $nivel:
    type: string
    required: false
    enum: [leigo, fundamental, intermediário, avançado]
    default: leigo
  $formato:
    type: list[string]
    required: false
    enum: [video_curto, leitura_guiada, laboratório, quiz, estudo_de_caso, projeto]
    default: [leitura_guiada, quiz]
  $voz:
    type: string
    required: false
    enum: [neutra, inspiradora, prática, bem_humorada]
    default: prática
  $idioma:
    type: string
    required: false
    enum: [pt-BR, es-ES, en-US]
    default: pt-BR
  $restricoes:
    type: list[string]
    required: false
    examples: ["sem imagens externas", "citá-las em ABNT", "tempo total ≤ 60 min"]
  $metaforas_seed:
    type: list[string]
    required: false
    description: Metáforas preferidas ou domínios de analogia (cozinha, esporte, viagem etc.).
  $axiomas_seed:
    type: list[string]
    required: false
    description: Princípios essenciais a preservar (ex.: "segurança > desempenho").
  $tamanho_modulo:
    type: string
    required: false
    enum: [micro (10–15min), curto (20–30min), padrão (40–60min)]
    default: padrão
  $plataforma:
    type: string
    required: false
    examples: ["LMS genérico", "Moodle", "Notion", "SCORM-ish"]
```

**Validação mínima**
- `$doc.length >= 800` caracteres
- `len($objetivos) >= 2`
- `$idioma in {pt-BR, es-ES, en-US}`

---

## 3) OUTPUT_CONTRACT
O HOP deve retornar **um JSON estruturado** pronto para implementação.

```json
{
  "course": {
    "title": "string",
    "subtitle": "string",
    "audience": "string",
    "level": "string",
    "duration_estimate_min": 0,
    "modules": [
      {
        "module_id": "string",
        "title": "string",
        "overview": "string",
        "axioms": ["string"],
        "key_metaphors": [
          {"name": "string", "analogy": "string", "limits": "string"}
        ],
        "learning_objectives": ["string"],
        "lessons": [
          {
            "lesson_id": "string",
            "title": "string",
            "content_outline": ["string"],
            "explain_like_Im_five": "string",
            "worked_example": "string",
            "glossary_antijargao": [
              {"jargao": "string", "explicacao_simples": "string", "metafora": "string"}
            ],
            "activities": [
              {"type": "quiz|reflexao|lab|estudo_de_caso|projeto",
               "task": "string",
               "rubric": ["string"],
               "bloom_level": "Remember|Understand|Apply|Analyze|Evaluate|Create"}
            ],
            "assessment_items": [
              {"stem": "string", "options": ["A","B","C","D"], "answer": "A", "rationale": "string", "bloom_level": "string"}
            ],
            "assets": {
              "script_video": "string",
              "slides_outline": ["string"],
              "image_prompts": ["string"],
              "alt_text": ["string"]
            }
          }
        ]
      }
    ],
    "capstone": {
      "brief": "string",
      "deliverables": ["string"],
      "evaluation_rubric": ["string"]
    },
    "accessibility_notes": ["string"],
    "references": [
      {"label": "string", "citation": "string"}
    ]
  },
  "metrics": {
    "jargon_reduction_ratio": 0.0,
    "coverage_vs_objectives": 0.0,
    "readability_index": 0.0,
    "validation_score": 0.0
  }
}
```

---

## 4) TASK (Role • Objective • Standards • Constraints)
**Role**: Arquiteto instrucional + Redator técnico antijargão.

**Objective**: Destilar o documento em um curso modular que preserve exatidão e aumente compreensão via **axiomas** (princípios invariantes) e **metáforas** (analogias concretas com limites claros).

**Standards**:
- Objetivos no formato observável (Bloom)
- Variedade de avaliação (diagnóstica, formativa, somativa)
- Acessibilidade: alt-text, leitura em voz alta, linguagem inclusiva
- Clareza medível (FKGL/FERNANDA-like aprox.)
- Metáforas com **limites declarados** (onde a analogia falha)

**Constraints**:
- Evitar jargões sem definição imediata
- Cada termo técnico ⇒ 1 definição simples + 1 metáfora
- Cada lição ⇒ ≥1 atividade aplicada
- Respeitar `$tamanho_modulo` e `$formato`

---

## 5) STEPS (TAC-7)
### 5.1 Descobrir & Mapear
- Ler `$doc` e extrair tópicos, termos e relações.
- Identificar jargões e dependências conceituais.
- Capturar possíveis axiomas do domínio e validar com `$axiomas_seed`.

### 5.2 Definir Objetivos & Axiomas
- Converter `$objetivos` em objetivos Bloom-alinhados.
- Consolidar 3–7 **axiomas** do curso (curtos, testáveis, atemporais).

### 5.3 Desenhar Metáforas com Limites
- Criar 2–4 **metáforas-mestras** conectadas a `$audiencia` (usar `$metaforas_seed` se houver).
- Para cada metáfora: indicar **limites** e **contraexemplos**.

### 5.4 Arquitetar Currículo
- Fatiar em módulos e lições respeitando `$tamanho_modulo` e `$formato`.
- Produzir **outlines**, exemplos trabalhados e atividades aplicadas.

### 5.5 Antijargão & Glossário Vivo
- Substituir jargões por definições simples + metáforas.
- Gerar `glossary_antijargao` por lição.

### 5.6 Avaliação & Acessibilidade
- Criar itens com níveis Bloom variados e justificativas.
- Incluir alt-text, narração opcional e notas de acessibilidade.

### 5.7 Medir & Embalar
- Calcular `jargon_reduction_ratio`, `readability_index`, `coverage_vs_objectives`.
- Montar saída conforme `OUTPUT_CONTRACT`.

---

## 6) VALIDATION (Quality Gates ≥ 7.0/10.0)
Checklist automatizável:
1. **Cobertura**: ≥90% dos objetivos mapeados em lições.
2. **Axiomas**: 3–7, curtos, verificáveis, usados nas lições.
3. **Metáforas**: ≥2 com limites explícitos; nenhuma metáfora enganosa.
4. **Antijargão**: Cada termo técnico tem dupla (definição simples + metáfora).
5. **Acessibilidade**: Alt-text presente em todos os assets; linguagem inclusiva.
6. **Avaliação**: Itens com níveis Bloom variados e rationale.
7. **Legibilidade**: Índice alvo ≥ 60 (escala adaptada) **ou** justificado.
8. **Coerência**: Duração total compatível com `$tamanho_modulo`.
9. **Formato**: JSON válido e aderente ao `OUTPUT_CONTRACT`.
10. **Score**: `validation_score >= 7.0`.

Métricas (pseudo):
- `jargon_reduction_ratio = (jargoes_detectados - jargoes_finais) / max(1,jargoes_detectados)`
- `coverage_vs_objectives = objetivos_cobertos / total_objetivos`
- `readability_index = função(tempo_médio_frase, palavras_complexas)`

---

## 7) CONTEXT (Uso, $arguments chaining, Assunções)
**Uso recomendado**:
- Quando houver material técnico denso que precisa virar curso com linguagem acessível.
- Ideal para onboarding de públicos não técnicos e trilhas mistas.

**$arguments chaining**:
- `plan.modules[*].lessons[*].assessment_items -> doc_sync_validator` (opcional)
- `course.assets.image_prompts -> gerador de imagens` (opcional)
- `references -> normalizador ABNT/APA` (opcional)

**Assunções**:
- `$doc` está limpo de PII sensível.
- Citações e direitos autorais são responsabilidade do solicitante.

---

## 8) PROMPT TEMPLATE (Pronto para uso)

```prompt
Você é um Arquiteto Instrucional antijargão. Converta o documento abaixo em um curso digital conforme TAC-7.

[ENTRADA]
$doc

[PARÂMETROS]
- audiência: $audiencia
- objetivos: $objetivos
- escopo: $escopo
- nível: $nivel
- formato preferido: $formato
- voz: $voz
- idioma: $idioma
- restrições: $restricoes
- metáforas seed: $metaforas_seed
- axiomas seed: $axiomas_seed
- tamanho do módulo: $tamanho_modulo
- plataforma: $plataforma

[REGRAS]
1) Cada termo técnico => definição simples + metáfora + limites da metáfora.
2) 3–7 axiomas curtos, usados ao longo das lições.
3) Objetivos alinhados à Taxonomia de Bloom.
4) Acessibilidade: inclua alt-text, linguagem inclusiva e avisos de conteúdo quando aplicável.
5) Output **APENAS** no JSON `OUTPUT_CONTRACT` especificado.
6) Incluir métricas: `jargon_reduction_ratio`, `coverage_vs_objectives`, `readability_index`, `validation_score`.

[SAÍDA]
JSON válido segundo OUTPUT_CONTRACT.
```

---

## 9) EXEMPLO MÍNIMO (ilustrativo)
*(resumo; troque pelo seu conteúdo real)*

- **Axiomas**: "Dados > opiniões", "Segurança primeiro", "Iterar > travar".
- **Metáforas**: "Pipeline = cozinha industrial" (limite: não captura concorrência fina), "Cache = mochila de viagem" (limite: capacidade finita), "Thread = pista de corrida" (limite: preempção não modelada).

---

## 10) COMO EXECUTAR (1 linha)
```
HOP: {module_id:"doc2course_axiomas_metaforas.v1", inputs:{ $doc:"...", $audiencia:"gestores não técnicos", $objetivos:["Entender X","Aplicar Y"], $nivel:"fundamental", $formato:["leitura_guiada","quiz"], $tamanho_modulo:"padrão"}}
```
