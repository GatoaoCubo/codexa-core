# Relatório de Gaps por Agente

> **Data**: 2025-11-30 | **Auditoria P1**

## Resumo Executivo

| Categoria | Agentes |
|-----------|---------|
| **Completos** (8) | codexa, mentor, curso, video, pesquisa, anuncio, photo, marca |
| **Mínimos** (4) | ronronalda, qa_gato3, scout, voice |

---

## Agentes Maduros (Sem gaps críticos)

### ✅ codexa_agent (220 files)
- **Status**: Referência
- **iso_vectorstore**: 17 arquivos (completo)
- **Gaps**: Nenhum crítico

### ✅ mentor_agent (291 files)
- **Status**: Referência
- **iso_vectorstore**: 19 arquivos (completo)
- **Gaps**: Nenhum crítico

### ✅ curso_agent (161 files)
- **Status**: Completo
- **iso_vectorstore**: 20 arquivos (completo)
- **Gaps menores**: 
  - Falta HOPs explícitos em prompts/ (usa HOP_ prefix em context/prompts/)

### ✅ video_agent (96 files)
- **Status**: Completo
- **iso_vectorstore**: 19 arquivos (completo)
- **Gaps**: Nenhum crítico

### ✅ pesquisa_agent (89 files)
- **Status**: Completo
- **iso_vectorstore**: 19 arquivos (completo)
- **Gaps**: Nenhum crítico

### ✅ anuncio_agent (82 files)
- **Status**: Completo
- **iso_vectorstore**: 19 arquivos (completo)
- **Gaps**: Nenhum crítico

### ✅ photo_agent (68 files)
- **Status**: Completo
- **iso_vectorstore**: 19 arquivos (completo)
- **Gaps**: Nenhum crítico

### ✅ marca_agent (55 files)
- **Status**: Completo
- **iso_vectorstore**: 25 arquivos (o mais completo!)
- **Gaps**: Nenhum crítico

---

## Agentes Mínimos (Precisam expansão)

### ⚠️ ronronalda_agent (14 files)
**Gaps Críticos:**
- [ ] iso_vectorstore incompleto (apenas 01_QUICK_START.md)
- [ ] Falta ADW workflow
- [ ] Falta HOPs estruturados
- [ ] Falta CHANGELOG.md

**Ações Recomendadas:**
1. Expandir iso_vectorstore (02-20)
2. Criar 100_ADW_RUN_RONRONALDA.md
3. Criar prompts/10_main_agent_HOP.md

### ⚠️ qa_gato3_agent (11 files)
**Gaps Críticos:**
- [ ] iso_vectorstore incompleto (apenas 01_QUICK_START.md)
- [ ] Falta ADW workflow
- [ ] Falta CHANGELOG.md

**Pontos Positivos:**
- Tem 4 HOPs bem definidos

**Ações Recomendadas:**
1. Expandir iso_vectorstore (02-20)
2. Criar workflows/100_ADW_RUN_QA.md

### ⚠️ scout_agent (8 files)
**Gaps Críticos:**
- [ ] iso_vectorstore incompleto (apenas 01_QUICK_START.md)
- [ ] Falta ADW workflow
- [ ] Falta HOPs
- [ ] Falta CHANGELOG.md

**Nota:** Scout é um MCP Server, estrutura pode ser diferente

**Ações Recomendadas:**
1. Expandir iso_vectorstore (02-20)
2. Documentar MCP tools como HOPs

### ⚠️ voice_agent (8 files)
**Gaps Críticos:**
- [ ] iso_vectorstore incompleto (apenas 01_QUICK_START.md)
- [ ] Falta ADW workflow
- [ ] Falta CHANGELOG.md

**Pontos Positivos:**
- Tem 1 HOP definido

**Ações Recomendadas:**
1. Expandir iso_vectorstore (02-20)
2. Criar workflows/100_ADW_RUN_VOICE.md

---

## Matriz de Gaps

| Agente | iso_vs | ADW | HOP | CHANGELOG | ARCH |
|--------|--------|-----|-----|-----------|------|
| codexa | ✅ 17 | ✅ 16 | ✅ 5 | ✅ | ✅ |
| mentor | ✅ 19 | ✅ 3 | ✅ 3 | ❌ | ✅ |
| curso | ✅ 20 | ✅ 4 | ⚠️ | ✅ | ✅ |
| video | ✅ 19 | ✅ 3 | ✅ 5 | ❌ | ❌ |
| pesquisa | ✅ 19 | ✅ 3 | ✅ 1 | ❌ | ✅ |
| anuncio | ✅ 19 | ✅ 2 | ✅ 1 | ❌ | ✅ |
| photo | ✅ 19 | ✅ 3 | ✅ 5 | ❌ | ❌ |
| marca | ✅ 25 | ✅ 3 | ✅ 2 | ✅ | ✅ |
| ronronalda | ❌ 1 | ❌ | ❌ | ❌ | ❌ |
| qa_gato3 | ❌ 1 | ❌ | ✅ 4 | ❌ | ❌ |
| scout | ❌ 1 | ❌ | ❌ | ❌ | ❌ |
| voice | ❌ 1 | ❌ | ✅ 1 | ❌ | ❌ |

---

## Prioridade de Ações

### P0 - Crítico (próxima sessão)
1. **Expandir iso_vectorstore** dos 4 agentes mínimos
2. **Criar ADWs básicos** para agentes sem workflow

### P1 - Importante
1. Adicionar CHANGELOG.md aos agentes que faltam
2. Padronizar numeração de arquivos

### P2 - Nice to have
1. Adicionar ARCHITECTURE.md onde falta
2. Unificar padrão de HOPs (prompts/ vs iso_vectorstore/)

---

**Gerado por**: Scout Audit P1
**Próxima revisão**: Após implementação P0
