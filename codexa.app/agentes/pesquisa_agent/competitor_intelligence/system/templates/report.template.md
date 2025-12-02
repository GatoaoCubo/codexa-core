# {{report.title}} - {{report.type}}

**Data**: {{report.date}}
**Período**: {{report.period}}
**Modo**: {{report.mode}}
**Status**: {{report.status}}

---

## 📊 Resumo Executivo

{{#summary}}
### Principais Destaques

{{#highlights}}
- **{{title}}**: {{description}}
{{/highlights}}

### Métricas Gerais

| Métrica | Valor | Meta | Status |
|---------|-------|------|--------|
{{#metrics}}
| {{name}} | {{value}} | {{target}} | {{status}} |
{{/metrics}}

{{/summary}}

---

## 🎯 Fontes Processadas

### ✅ Sucesso ({{sources.success.count}})

{{#sources.success.items}}
#### {{number}}. {{name}}
- **Categoria**: {{category}}
- **Prioridade**: {{priority}}
- **Status**: {{status}}
- **Arquivo**: `{{file_path}}`
- **Confiabilidade**: {{reliability}}

**Dados Coletados**:
{{#data_points}}
- {{.}}
{{/data_points}}

{{/sources.success.items}}

---

### ⚠️ Falhas/Limitações ({{sources.failed.count}})

{{#sources.failed.items}}
#### {{number}}. {{name}}
- **URL**: {{url}}
- **Status**: {{error_status}}
- **Problema**: {{error_description}}
- **Ação**: {{recommended_action}}

{{/sources.failed.items}}

---

## 💡 Insights-Chave Identificados

{{#insights}}
### {{number}}. {{title}}

**Tipo**: {{type}}
**Fonte**: {{source}}
**Confiança**: {{confidence}}

**Insight**: {{description}}

**Impacto**: {{impact}}

**Ação Recomendada**: {{action}}

{{#if evidence}}
**Evidências**:
{{#evidence}}
- {{.}}
{{/evidence}}
{{/if}}

---

{{/insights}}

---

## 🚀 Oportunidades de Negócio

{{#opportunities}}
### {{number}}. {{title}}

- **Validação**: {{validation}}
- **Gap Competitivo**: {{gap}}
- **Posicionamento Sugerido**: {{positioning}}
- **Prioridade**: {{priority}}

{{#if details}}
**Detalhes**:
{{details}}
{{/if}}

---

{{/opportunities}}

---

## 🚨 Alertas e Riscos

{{#alerts}}
### {{severity}} - {{title}}

**Descrição**: {{description}}

**Impacto**: {{impact}}

**Mitigação**: {{mitigation}}

**Prazo**: {{timeline}}

---

{{/alerts}}

---

## 📈 Mudanças Detectadas

{{#if changes.count > 0}}
### Total de Mudanças: {{changes.count}}

{{#changes.items}}
#### {{source.name}}

**Tipo de Mudança**: {{change_type}}
**Campo**: {{field}}
**Antes**: {{before}}
**Depois**: {{after}}
**Impacto**: {{impact}}

---

{{/changes.items}}
{{else}}
Nenhuma mudança detectada neste período.
{{/if}}

---

## 📊 Análise Comparativa

{{#comparative_analysis}}
### {{title}}

{{#comparisons}}
| {{metric_name}} | {{#sources}}{{name}} | {{/sources}}
|-----------------|{{#sources}}---------|{{/sources}}
{{#metrics}}
| {{name}} | {{#values}}{{.}} | {{/values}}
{{/metrics}}

**Insights**:
{{#insights}}
- {{.}}
{{/insights}}

{{/comparisons}}
{{/comparative_analysis}}

---

## 📋 Próximas Ações Recomendadas

{{#actions}}
### {{category}}

{{#items}}
{{checkbox}} {{description}}
   {{#if context}}- **Contexto**: {{context}}{{/if}}
   {{#if priority}}- **Prioridade**: {{priority}}{{/if}}
   {{#if timeline}}- **Prazo**: {{timeline}}{{/if}}

{{/items}}
{{/actions}}

---

## 📁 Arquivos Gerados

{{#files}}
### {{category}}

{{#items}}
{{number}}. `{{path}}` ({{size}})
{{/items}}

{{/files}}

**Total de Arquivos**: {{files.total_count}}
**Tamanho Total**: {{files.total_size}}

---

## 📊 Métricas desta Execução

| Métrica | Valor | Alvo | Status | Observação |
|---------|-------|------|--------|------------|
{{#execution_metrics}}
| {{name}} | {{value}} | {{target}} | {{status}} | {{note}} |
{{/execution_metrics}}

### Análise de Performance

{{#performance_analysis}}
**{{category}}**: {{description}}
{{/performance_analysis}}

---

## 🔄 Comparação com Execuções Anteriores

{{#if baseline}}
**Baseline**: {{baseline.date}}

| Métrica | Atual | Baseline | Variação | Tendência |
|---------|-------|----------|----------|-----------|
{{#baseline_comparison}}
| {{name}} | {{current}} | {{baseline}} | {{change}} | {{trend}} |
{{/baseline_comparison}}

{{else}}
**Esta é a primeira execução** - métricas estabelecem baseline para futuras comparações.
{{/if}}

---

## 💬 Conclusões e Recomendações

### Status Geral
{{conclusion.overall_status}}

### Principais Conquistas
{{#conclusion.achievements}}
- {{.}}
{{/conclusion.achievements}}

### Desafios Encontrados
{{#conclusion.challenges}}
- {{.}}
{{/conclusion.challenges}}

### Recomendações Estratégicas
{{#conclusion.strategic_recommendations}}
{{number}}. **{{title}}**
   {{description}}

{{/conclusion.strategic_recommendations}}

---

## 🔗 Recursos e Links

{{#resources}}
- [{{name}}]({{url}}){{#if description}} - {{description}}{{/if}}
{{/resources}}

---

**Próxima Atualização Programada**: {{next_update}}
**Próxima Revisão de URLs**: {{next_url_review}}

---

**Relatório gerado por**: {{system.name}} v{{system.version}}
**Template**: {{template.name}} v{{template.version}}
**Timestamp**: {{timestamp}}
**Hash do Relatório**: {{report_hash}}
