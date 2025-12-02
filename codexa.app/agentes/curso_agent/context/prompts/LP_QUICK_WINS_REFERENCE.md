# LP QUICK WINS REFERENCE | Para Agente da Landing Page

**Created**: 2025-12-01
**Purpose**: Referencia de paths e conteudo dos Quick Wins para a LP

---

## PATHS DOS ARQUIVOS

### Versoes Completas (com metadata e changelog)

```
agentes/curso_agent/context/prompts/FREEMIUM_QW1_META_PROMPT_v2.md
agentes/curso_agent/context/prompts/FREEMIUM_QW2_PLAN_v2.md
agentes/curso_agent/context/prompts/FREEMIUM_QW3_IMPLEMENT_v2.md
agentes/curso_agent/context/prompts/FREEMIUM_QW_COMBINACOES.md
```

### Versoes Limpas para LP (so o prompt)

```
agentes/curso_agent/context/prompts/LP_EXPORT_QW1_META_PROMPT.md
agentes/curso_agent/context/prompts/LP_EXPORT_QW2_PLAN.md
agentes/curso_agent/context/prompts/LP_EXPORT_QW3_IMPLEMENT.md
```

---

## RESUMO PARA COPY DA LP

### QW1: META-PROMPT

**Titulo**: O Construtor Universal de Prompts
**Conceito**: DELEGACAO
**O que faz**: Transforma pedidos vagos em prompts estruturados que qualquer IA executa com excelencia
**Beneficio**: Voce nunca mais precisa escrever prompts - a IA faz isso por voce
**Linhas**: ~180

### QW2: PLAN

**Titulo**: O Planejador Universal
**Conceito**: SUPERVISAO
**O que faz**: Mostra o plano ANTES de executar para voce validar
**Beneficio**: Evita retrabalho - voce aprova antes de gastar tempo/tokens
**Linhas**: ~170

### QW3: IMPLEMENT

**Titulo**: O Executor de Ativos
**Conceito**: ATIVOS
**O que faz**: Executa e entrega em formato reutilizavel que funciona em qualquer IA
**Beneficio**: Cada interacao cria valor permanente - o Cerebro Empresarial
**Linhas**: ~190

---

## FLUXO VISUAL PARA LP

```
[OBJETIVO DO USUARIO]
        |
        v
+-------------------+
| QW1: META-PROMPT  |  "O que voce quer?"
| Constroi prompt   |  --> Prompt estruturado
+-------------------+
        |
        v
+-------------------+
| QW2: PLAN         |  "Como vou fazer?"
| Planeja execucao  |  --> Plano para aprovar
+-------------------+
        |
        v
+-------------------+
| QW3: IMPLEMENT    |  "Aprovado!"
| Executa e salva   |  --> Ativo reutilizavel
+-------------------+
        |
        v
[CEREBRO EMPRESARIAL]
  Conhecimento que escala
```

---

## VARIAVEIS QUE ACEITAM

Todos os 3 QWs aceitam dados do codexa.app:

| Label | O que e | Vem de |
|-------|---------|--------|
| [PESQUISA] | Dados de mercado/concorrencia | pesquisa_agent |
| [ANUNCIO] | Textos de anuncios | anuncio_agent |
| [FOTO] | Briefings visuais | photo_agent |
| [PLANO] | Plano estrategico | QW2 ou mentor_agent |

---

## DIFERENCIAIS PARA DESTACAR NA LP

1. **Funciona em qualquer IA** - ChatGPT, Claude, Gemini, etc.
2. **Aceita dados do CODEXA** - [PESQUISA], [ANUNCIO], [FOTO]
3. **Adapta automaticamente** - Simples, medio ou complexo
4. **Gera templates** - Reutilizaveis com [VARIAVEIS]
5. **Ciclo de escala** - Ativos geram mais ativos

---

## CALL TO ACTION SUGERIDO

**Titulo**: 3 Prompts. Infinitas Possibilidades.

**Subtitulo**: Construa seu Cerebro Empresarial - conhecimento proprietario que funciona em qualquer IA, para sempre.

**CTA Primario**: Baixar os 3 Quick Wins Gratis

**CTA Secundario**: Ver como funcionam juntos

---

## METRICAS DOS ARQUIVOS

| Arquivo | Linhas | Tokens (aprox) |
|---------|--------|----------------|
| QW1 META-PROMPT | 180 | ~2.500 |
| QW2 PLAN | 170 | ~2.300 |
| QW3 IMPLEMENT | 190 | ~2.600 |
| COMBINACOES | 230 | ~3.000 |
| **TOTAL** | **770** | **~10.400** |

---

## INSTRUCOES PARA O AGENTE DA LP

1. Use os arquivos `LP_EXPORT_*.md` (versoes limpas)
2. Os prompts estao prontos para copy-paste
3. Mantenha a estrutura de secoes (COMO USAR, IDENTIDADE, etc.)
4. Destaque o fluxo visual dos 3 QWs trabalhando juntos
5. Enfatize que funciona em QUALQUER LLM (portabilidade)
6. Mostre as labels de dados [PESQUISA], [ANUNCIO], [FOTO]
