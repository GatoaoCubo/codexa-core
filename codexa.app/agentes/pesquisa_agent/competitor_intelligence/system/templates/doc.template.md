# {{source.name}}

**Fonte**: {{source.name}}
**URL**: {{source.urls.main}}
**Data de Coleta**: {{fetch_date}}
**Categoria**: {{category}}
**Prioridade**: {{source.priority}}

---

{{#if source.tier}}
## 📊 Classificação

**Tier**: {{source.tier}}
{{#if source.metrics.price_brl}}
**Preço**: R$ {{source.metrics.price_brl}}{{#if source.metrics.price_model}} ({{source.metrics.price_model}}){{/if}}
{{/if}}
{{#if source.metrics.duration_hours}}
**Duração**: {{source.metrics.duration_hours}} horas
{{/if}}
{{/if}}

---

## 🔍 Informações Coletadas

{{content.main}}

---

{{#if insights}}
## 💡 Insights-Chave

{{#insights}}
### {{number}}. {{title}}
**Tipo**: {{type}}
**Descrição**: {{description}}
**Impacto**: {{impact}}
**Ação Recomendada**: {{action}}
**Fonte de Dados**: {{source}}

{{/insights}}
{{/if}}

---

{{#if metrics}}
## 📊 Métricas Rastreadas

{{#metrics}}
| Métrica | Valor | Tendência |
|---------|-------|-----------|
{{#each this}}
| {{@key}} | {{value}} | {{trend}} |
{{/each}}
{{/metrics}}
{{/if}}

---

{{#if monitoring}}
## 🔔 Alertas Configurados

{{#monitoring}}
{{#if enabled}}
- **{{@key}}**: {{#if threshold}}Threshold: {{threshold}}{{else}}Ativo{{/if}}
{{/if}}
{{/monitoring}}
{{/if}}

---

{{#if competitive_analysis}}
## 🎯 Análise Competitiva

{{competitive_analysis}}
{{/if}}

---

{{#if opportunities}}
## 🚀 Oportunidades Identificadas

{{#opportunities}}
{{number}}. **{{title}}**
   - **Gap**: {{gap}}
   - **Validação**: {{validation}}
   - **Ação**: {{action}}

{{/opportunities}}
{{/if}}

---

{{#if risks}}
## ⚠️ Riscos e Alertas

{{#risks}}
- **{{type}}**: {{description}}
  - **Severidade**: {{severity}}
  - **Mitigação**: {{mitigation}}

{{/risks}}
{{/if}}

---

## 📈 Próximas Ações

{{#actions}}
{{#each categories}}
### {{name}}

{{#items}}
- [ ] {{description}}{{#if priority}} (Prioridade: {{priority}}){{/if}}
{{/items}}

{{/each}}
{{/actions}}

---

{{#if related_sources}}
## 🔗 Fontes Relacionadas

{{#related_sources}}
- [{{name}}]({{url}}){{#if description}} - {{description}}{{/if}}
{{/related_sources}}
{{/if}}

---

{{#if custom_sections}}
{{#custom_sections}}
## {{title}}

{{content}}

---

{{/custom_sections}}
{{/if}}

**Status**: {{status}}
**Confiabilidade**: {{reliability}}
**Próxima Atualização**: {{next_update}}
**Hash de Conteúdo**: {{content_hash}}

---

_Gerado por: Competitor Intelligence System {{system_version}}_
_Template: {{template_name}}_
_Timestamp: {{timestamp}}_
