# LIVRO: Copywriting
## CAPÍTULO 1

**Versículos consolidados**: 46
**Linhas totais**: 1179
**Gerado em**: 2025-11-13 18:45:48

---


<!-- VERSÍCULO 1/46 - copywriting_1_adicionar_novo_conhecimento_5_minut_20251113.md (53 linhas) -->

# 1️⃣ Adicionar Novo Conhecimento (5 Minutos)

**Categoria**: copywriting
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### Passo 1: Salve documento RAW

```bash
cp your_ecommerce_guide.md ecommerce-canon/GENESIS/RAW/
```

### Passo 2: Rode o distiller

```bash
cd ecommerce-canon
python AGENTS/distiller.py GENESIS/RAW/your_ecommerce_guide.md
```

**O que faz:**
- ✓ Extrai 5-10 "chunks" semânticos do documento
- ✓ Calcula entropia (0-100: densidade de informação)
- ✓ Classifica nível de abstração (Deus-vs-Todo)
- ✓ Sugere LIVRO/CAPÍTULO apropriado
- ✓ Salva como JSON em `GENESIS/PROCESSING/`

### Passo 3: Organize manualmente (ou automático)

```bash
# Opção A: Manual (mais controle)
# Edite chunks em GENESIS/PROCESSING/ e
# Mova-os para estrutura correta em LIVRO_*/CAPÍTULO_*/

# Opção B: Automático (em desenvolvimento)
# python AGENTS/organizer.py GENESIS/PROCESSING/
```

### Passo 4: Versione

```bash
git add ecommerce-canon/
git commit -m "CANON_ADD: [LIVRO]/[CAP] - descrição"
git tag canon-1.2.3
```

**Tags**: ecommerce, general, implementation

**Palavras-chave**: Minutos, Adicionar, Novo, Conhecimento

**Origem**: desconhecida


---


<!-- VERSÍCULO 2/46 - copywriting_1_conceito_raiz_galhos_1_20251113.md (18 linhas) -->

# 1) Conceito "Raiz & Galhos"

**Categoria**: copywriting
**Qualidade**: 0.67/1.00
**Data**: 20251113

## Conteúdo

- **Raiz (MD)**: documentação concisa, decisões canônicas e como aplicar.
- **Galhos (JSON)**: chaves legíveis por máquina para orquestrar LLMs (mesmos conteúdos).
- **Versão**: 1.0.0 — *integridade do bloco hermético* (SHA-256) informada ao final.

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Raiz, Galhos

**Origem**: _CONSOLIDATED_ECOMMERCE_RAW_FROM_GIT.md


---


<!-- VERSÍCULO 3/46 - copywriting_1_conceito_raiz_galhos_20251113.md (18 linhas) -->

# 1) Conceito "Raiz & Galhos"

**Categoria**: copywriting
**Qualidade**: 0.67/1.00
**Data**: 20251113

## Conteúdo

- **Raiz (MD)**: documentação concisa, decisões canônicas e como aplicar.
- **Galhos (JSON)**: chaves legíveis por máquina para orquestrar LLMs (mesmos conteúdos).
- **Versão**: 1.0.0 — *integridade do bloco hermético* (SHA-256) informada ao final.

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Raiz, Conceito, Galhos

**Origem**: desconhecida


---


<!-- VERSÍCULO 4/46 - copywriting_1_conceito_raiz_galhos_2_20251113.md (18 linhas) -->

# 1) Conceito "Raiz & Galhos"

**Categoria**: copywriting
**Qualidade**: 0.67/1.00
**Data**: 20251113

## Conteúdo

- **Raiz (MD)**: documentação concisa, decisões canônicas e como aplicar.
- **Galhos (JSON)**: chaves legíveis por máquina para orquestrar LLMs (mesmos conteúdos).
- **Versão**: 1.0.0 — *integridade do bloco hermético* (SHA-256) informada ao final.

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Raiz, Galhos

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 5/46 - copywriting_1_conceito_raiz_galhos_3_20251113.md (18 linhas) -->

# 1) Conceito "Raiz & Galhos"

**Categoria**: copywriting
**Qualidade**: 0.67/1.00
**Data**: 20251113

## Conteúdo

- **Raiz (MD)**: documentação concisa, decisões canônicas e como aplicar.
- **Galhos (JSON)**: chaves legíveis por máquina para orquestrar LLMs (mesmos conteúdos).
- **Versão**: 1.0.0 — *integridade do bloco hermético* (SHA-256) informada ao final.

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Raiz, Galhos

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 6/46 - copywriting_2_pipeline_do_backend_1_20251113.md (26 linhas) -->

# 2. Pipeline do Backend

**Categoria**: copywriting
**Qualidade**: 0.71/1.00
**Data**: 20251113

## Conteúdo

### 2.1 Entrada e Validação
- Normaliza o payload recebido do formulário (incluindo campos legados) e o valida com schemas estritos, rejeitando rotas ou métodos inesperados.
- Cada requisição gera erros diagnósticos padronizados que incluem contexto adicional: método, rota, tentativas de reparo e dicas para suporte.

### 2.2 Construção do Prompt
- O prompt mestre descreve uma sequência rígida de etapas (benchmark → síntese → geração → validação → empacotamento) e exige JSON STRICT.
- Regras de marketplace e SEO são incorporadas diretamente no prompt: limites de caracteres, remoção de stopwords, obrigatoriedade de seções (títulos, bullet points, FAQ, variações de copy, metadados de confiança, vs[] etc.).
- Um fallback textual alternativo garante que, mesmo sem acesso ao arquivo principal, as instruções críticas (fluxo, formato e política) sejam preservadas.

### 2.3 Orquestração dos Modelos
- Abstração central escolhe fornecedor (OpenAI, Gemini...), configura streaming, coleta telemetri

**Tags**: ecommerce, implementation

**Palavras-chave**: Pipeline, Backend

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 7/46 - copywriting_2_pipeline_do_backend_20251113.md (26 linhas) -->

# 2. Pipeline do Backend

**Categoria**: copywriting
**Qualidade**: 0.71/1.00
**Data**: 20251113

## Conteúdo

### 2.1 Entrada e Validação
- Normaliza o payload recebido do formulário (incluindo campos legados) e o valida com schemas estritos, rejeitando rotas ou métodos inesperados.
- Cada requisição gera erros diagnósticos padronizados que incluem contexto adicional: método, rota, tentativas de reparo e dicas para suporte.

### 2.2 Construção do Prompt
- O prompt mestre descreve uma sequência rígida de etapas (benchmark → síntese → geração → validação → empacotamento) e exige JSON STRICT.
- Regras de marketplace e SEO são incorporadas diretamente no prompt: limites de caracteres, remoção de stopwords, obrigatoriedade de seções (títulos, bullet points, FAQ, variações de copy, metadados de confiança, vs[] etc.).
- Um fallback textual alternativo garante que, mesmo sem acesso ao arquivo principal, as instruções críticas (fluxo, formato e política) sejam preservadas.

### 2.3 Orquestração dos Modelos
- Abstração central escolhe fornecedor (OpenAI, Gemini...), configura streaming, coleta telemetri

**Tags**: ecommerce, general, implementation

**Palavras-chave**: Pipeline, Backend

**Origem**: desconhecida


---


<!-- VERSÍCULO 8/46 - copywriting_2_psicologia_do_consumidor_motiva_es_1_20251113.md (28 linhas) -->

# 2) Psicologia do Consumidor (Motivações & Emoções)

**Categoria**: copywriting
**Qualidade**: 0.79/1.00
**Data**: 20251113

## Conteúdo

3. **Understanding The Four Key Reasons Why People Buy — Forbes (YEC)**  
   https://www.forbes.com/councils/theyec/2022/05/10/understanding-the-four-key-reasons-why-people-buy/  
   *Como usar:* matriz “problema / sentir-se compreendido / lógica / emoção”; ideal para justificar claims de copy.

4. **Consumer Psychology and Behavior — Verywell Mind**  
   https://www.verywellmind.com/what-is-consumer-psychology-2794899  
   *Como usar:* bases de psicologia de consumo; contextualiza emoções e tomada de decisão.

5. **Consumer Behavior — Psychology Today**  
   https://www.psychologytoday.com/us/basics/consumer-behavior  
   *Como usar:* visão geral rápida de comportamento do consumidor; bom para citações leves.

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Motivações, Psicologia, Consumidor, Emoções

**Origem**: desconhecida


---


<!-- VERSÍCULO 9/46 - copywriting_2_psicologia_do_consumidor_motiva_es_20251113.md (28 linhas) -->

# 2) Psicologia do Consumidor (Motivações & Emoções)

**Categoria**: copywriting
**Qualidade**: 0.79/1.00
**Data**: 20251113

## Conteúdo

3. **Understanding The Four Key Reasons Why People Buy — Forbes (YEC)**  
   https://www.forbes.com/councils/theyec/2022/05/10/understanding-the-four-key-reasons-why-people-buy/  
   *Como usar:* matriz “problema / sentir-se compreendido / lógica / emoção”; ideal para justificar claims de copy.

4. **Consumer Psychology and Behavior — Verywell Mind**  
   https://www.verywellmind.com/what-is-consumer-psychology-2794899  
   *Como usar:* bases de psicologia de consumo; contextualiza emoções e tomada de decisão.

5. **Consumer Behavior — Psychology Today**  
   https://www.psychologytoday.com/us/basics/consumer-behavior  
   *Como usar:* visão geral rápida de comportamento do consumidor; bom para citações leves.

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Psicologia, Consumidor, Motivações, Emoções

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 10/46 - copywriting_4_conceitos_chave_20251113.md (34 linhas) -->

# 4️⃣ Conceitos-Chave

**Categoria**: copywriting
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### Entropia (0-100)

Mede **densidade de informação nova**:
- **80-100**: Muito específico, denso, inovador
- **50-79**: Bom para contexto, prático, balanceado
- **0-49**: Óbvio, genérico, repetitivo

### Deus-vs-Todo (Abstração)

**DEUS (Absoluto):**
- "ACID properties are fundamental..."
- Válido universalmente, atemporalmente

**TODO (Contextual):**
- "Our PostgreSQL 14.2 in us-east-1..."
- Específico de contexto, temporal

**MIXED:**
- Combina conceitos universais com aplicações práticas

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Chave, Conceitos

**Origem**: desconhecida


---


<!-- VERSÍCULO 11/46 - copywriting_4_infraestrutura_e_configura_o_1_20251113.md (17 linhas) -->

# 4. Infraestrutura e Configuração

**Categoria**: copywriting
**Qualidade**: 0.66/1.00
**Data**: 20251113

## Conteúdo

- Feature é registrada em catálogo central com rota dedicada, descrição e payload de health check para monitoramento.
- Configuração Supabase expõe a função edge com autenticação pública controlada, enquanto a validação de schema e o diagnóstico cuidam da segurança lógica.

**Tags**: ecommerce, intermediate

**Palavras-chave**: Infraestrutura, Configuração

**Origem**: _CONSOLIDATED_ECOMMERCE_VERSICULOS_FROM_GIT.md


---


<!-- VERSÍCULO 12/46 - copywriting_4_infraestrutura_e_configura_o_20251113.md (17 linhas) -->

# 4. Infraestrutura e Configuração

**Categoria**: copywriting
**Qualidade**: 0.66/1.00
**Data**: 20251113

## Conteúdo

- Feature é registrada em catálogo central com rota dedicada, descrição e payload de health check para monitoramento.
- Configuração Supabase expõe a função edge com autenticação pública controlada, enquanto a validação de schema e o diagnóstico cuidam da segurança lógica.

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Infraestrutura, Configuração

**Origem**: desconhecida


---


<!-- VERSÍCULO 13/46 - copywriting_4_infraestrutura_e_configura_o_2_20251113.md (17 linhas) -->

# 4. Infraestrutura e Configuração

**Categoria**: copywriting
**Qualidade**: 0.66/1.00
**Data**: 20251113

## Conteúdo

- Feature é registrada em catálogo central com rota dedicada, descrição e payload de health check para monitoramento.
- Configuração Supabase expõe a função edge com autenticação pública controlada, enquanto a validação de schema e o diagnóstico cuidam da segurança lógica.

**Tags**: ecommerce, intermediate

**Palavras-chave**: Infraestrutura, Configuração

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 14/46 - copywriting_4_notas_de_cita_o_e_boas_pr_ticas_1_20251113.md (21 linhas) -->

# 4) Notas de Citação e Boas Práticas

**Categoria**: copywriting
**Qualidade**: 0.78/1.00
**Data**: 20251113

## Conteúdo

- Cite números com parcimônia (ex.: “+63% preferem concluir no marketplace”), sempre mantendo **contexto**.  
- Evite afirmar **causalidade** onde a fonte apenas indica **correlação**.  
- Atualize dados anualmente para manter credibilidade (versões 2025 → revisar em 2026).  
- Para Mercado Livre, priorize **prova social própria** (avaliações reais) + **garantias claras**; use as fontes acima como **apoio** à lógica da copy, não como protagonista da mensagem.

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Boas, Práticas, Notas, Citação

**Origem**: desconhecida


---


<!-- VERSÍCULO 15/46 - copywriting_4_notas_de_cita_o_e_boas_pr_ticas_20251113.md (21 linhas) -->

# 4) Notas de Citação e Boas Práticas

**Categoria**: copywriting
**Qualidade**: 0.78/1.00
**Data**: 20251113

## Conteúdo

- Cite números com parcimônia (ex.: “+63% preferem concluir no marketplace”), sempre mantendo **contexto**.  
- Evite afirmar **causalidade** onde a fonte apenas indica **correlação**.  
- Atualize dados anualmente para manter credibilidade (versões 2025 → revisar em 2026).  
- Para Mercado Livre, priorize **prova social própria** (avaliações reais) + **garantias claras**; use as fontes acima como **apoio** à lógica da copy, não como protagonista da mensagem.

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Notas, Citação, Boas, Práticas

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 16/46 - copywriting_5_chunk_prompt_composition_library_20251113.md (38 linhas) -->

# 🔗 5-CHUNK PROMPT COMPOSITION LIBRARY

**Categoria**: copywriting
**Qualidade**: 0.87/1.00
**Data**: 20251113

## Conteúdo

### Chunk 1: Research Consolidation
- **Source**: All 6 pillars combined
- **Purpose**: Synthesize all research into strategic insights
- **Output**: JSON with insights, strengths, opportunities, gaps
- **Framework**: `app/como_pesquisa/02_prompt_composition/prompt_chunks_guide.md`

### Chunk 2: Keyword Extraction & Hierarchization
- **Source**: Pilar 4 + Pilar 3 (product research)
- **Purpose**: Organize keywords in 4-level hierarchy
- **Output**: Keywords array with search volume and intent

### Chunk 3: Competitive Gap Analysis
- **Source**: Pilar 2 + Pilar 1 (market dynamics)
- **Purpose**: Identify white space and differentiation angles
- **Output**: Gap analysis with positioning recommendations

### Chunk 4: Ad Structure Builder
- **Source**: All pillars + outputs from Chunks 1-3
- **Purpose**: Transform research into ad structure (headlines, bullets, FAQ)
- **Output**: Advertisement structure ready for copywriting

### Chunk 5: Ad Validation & Optimization
- **Source**: Chunk 4 

**Tags**: ecommerce, abstract

**Palavras-chave**: CHUNK, PROMPT, COMPOSITION, LIBRARY

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 17/46 - copywriting_7_governan_a_1_20251113.md (17 linhas) -->

# 7) Governança

**Categoria**: copywriting
**Qualidade**: 0.61/1.00
**Data**: 20251113

## Conteúdo

- **Versionamento**: manter `id` e `chave_canonica` estáveis; atualizar apenas campos de descrição/exemplos.
- **Incremental**: diffs referenciados pelo hash do bloco hermético para rastreio.

**Tags**: ecommerce, intermediate

**Palavras-chave**: Governança

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 18/46 - copywriting_7_governan_a_20251113.md (17 linhas) -->

# 7) Governança

**Categoria**: copywriting
**Qualidade**: 0.61/1.00
**Data**: 20251113

## Conteúdo

- **Versionamento**: manter `id` e `chave_canonica` estáveis; atualizar apenas campos de descrição/exemplos.
- **Incremental**: diffs referenciados pelo hash do bloco hermético para rastreio.

**Tags**: ecommerce, intermediate

**Palavras-chave**: Governança

**Origem**: _CONSOLIDATED_ECOMMERCE_RAW_FROM_GIT.md


---


<!-- VERSÍCULO 19/46 - copywriting_7_governan_a_2_20251113.md (17 linhas) -->

# 7) Governança

**Categoria**: copywriting
**Qualidade**: 0.61/1.00
**Data**: 20251113

## Conteúdo

- **Versionamento**: manter `id` e `chave_canonica` estáveis; atualizar apenas campos de descrição/exemplos.
- **Incremental**: diffs referenciados pelo hash do bloco hermético para rastreio.

**Tags**: ecommerce, intermediate

**Palavras-chave**: Governança

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 20/46 - copywriting_agentes_ai_conhecimento_completo_20251113.md (58 linhas) -->

# Agentes Ai Conhecimento Completo | copywriting

## CONCEITOS-CHAVE

• **Fundamentos**: Este conhecimento aborda conceitos essenciais para vendedores que querem crescer no e-commerce brasileiro
• **Aplicação Prática**: Técnicas e estratégias que você pode aplicar hoje mesmo nos seus produtos
• **Resultados Mensuráveis**: Foco em ações que geram impacto direto nas suas vendas
• **Marketplaces**: Conhecimento aplicável ao Mercado Livre, Shopee, Magalu e outros canais

## POR QUE IMPORTA

Se você vende online no Brasil, sabe que a concorrência está cada vez maior. Este conhecimento foi criado para te ajudar a se destacar da multidão e vender mais.

No cenário atual dos marketplaces brasileiros, quem domina as técnicas certas consegue resultados até 3x melhores que a média. Seja otimizando títulos para o algoritmo do Mercado Livre, criando descrições que convencem, ou automatizando processos repetitivos - cada detalhe conta.

## COMO FAZER

1. **Comece pelo básico**: Analise sua situação atual e identifique onde você pode melhorar
2. **Aplique as técnicas**: Implemente as estratégias de forma gradual, começando pelos produtos mais importantes
3. **Teste e ajuste**: Monitore os resultados e faça ajustes conforme necessário
4. **Escale o que funciona**: Quando encontrar uma estratégia vencedora, replique para todos os produtos
5. **Automatize processos**: Use ferramentas e scripts para economizar tempo nas tarefas repetitivas
6. **Acompanhe métricas**: Fique de olho em conversão, visualizações e posição nos resultados de busca
7. **Mantenha-se atualizado**: Os marketplaces mudam constantemente - adapte suas estratégias

## EXEMPLO REAL

**Antes**: Vendedor com 50 produtos no Mercado Livre, títulos genéricos, fotos padrão do fornecedor, descrições copiadas. Taxa de conversão: 1.2%, aparecendo na 5ª página de resultados.

**Depois**: Após aplicar as técnicas de otimização - títulos com palavras-chave estratégicas, fotos profissionais com fundo branco, descrições persuasivas com gatilhos mentais, uso de ferramentas de automação para atualizar preços.

**Resultado**: Taxa de conversão subiu para 3.8% (+217%), produtos aparecendo na primeira página, vendas aumentaram de 15 para 42 unidades/mês por produto (+180%). Tempo gasto em gestão reduziu de 4h para 1h por dia graças à automação.

## BOAS PRÁTICAS

• **Seja consistente**: Aplique as técnicas em todos os seus produtos, não apenas em alguns
• **Teste sempre**: O que funciona para um vendedor pode não funcionar para outro - teste e descubra o que dá certo no seu nicho
• **Foque no cliente**: Pense sempre em como facilitar a decisão de compra do seu cliente
• **Use dados**: Baseie suas decisões em números reais, não em achismos
• **Automatize o repetitivo**: Use ferramentas para economizar tempo e focar no estratégico

## PRÓXIMOS PASSOS

Depois de dominar este conteúdo, explore:
• Técnicas avançadas de SEO para marketplaces
• Estratégias de precificação dinâmica
• Automação de processos com Python
• Análise de concorrência e benchmarking
• Gatilhos mentais aplicados ao e-commerce

---
**Categoria**: copywriting
**Nível**: básico
**Tags**: mercadolivre, shopee, magalu, seo, conversao
**Aplicação**: quando_criar_anuncios
**Fonte**: RASCUNHO/AGENTES_AI_CONHECIMENTO_COMPLETO.md
**Processado**: 20251113


---


<!-- VERSÍCULO 21/46 - copywriting_app_docs_master_backup_ecommerce_canon_20251113.md (20 linhas) -->

# [app_docs\_MASTER_BACKUP\ecommerce-canon\GENESIS\RAW\RAW_011_Brand_Master.md]

**Categoria**: copywriting
**Qualidade**: 0.76/1.00
**Data**: 20251113

## Conteúdo

Lines: 70

# Brand Assistant — MASTER PROMPT (v4)

> Objetivo: transformar qualquer insumo do usuário (texto/imagens) em um **Brandbook** claro e utilizável, com JSON `brand_guidelines` validado + um Markdown humano amigável.

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: app_docs, canon, Core, RAW_011_Brand_Master, ecommerce, Conceito, GENESIS, _MASTER_BACKUP

**Origem**: desconhecida


---


<!-- VERSÍCULO 22/46 - copywriting_changelog_1_20251113.md (38 linhas) -->

# Changelog

**Categoria**: copywriting
**Qualidade**: 0.69/1.00
**Data**: 20251113

## Conteúdo

- v1.0.0 ({datetime.now().strftime('%Y-%m-%d')}): Versão inicial
"""

    # ==================== FASE 4: VALIDAÇÃO ====================

    async def validate_versículos(self, versículos: List[Path]) -> List[Path]:
        """Valida qualidade de versículos."""
        validated = []

        for vers_path in versículos:
            checks = {
                'has_title': self.validator.check_has_title(vers_path),
                'has_entropy': self.validator.check_has_entropy(vers_path),
                'entropy_threshold': self.validator.check_entropy_threshold(vers_path),
                'valid_markdown': self.validator.check_valid_markdown(vers_path),
                'no_duplicates': self.validator.check_no_duplicates(vers_path),
                'proper_relations': self.validator.check_relations(vers_path),
            }

            if all(checks.values()):
                validated.append(vers_path)
            else:
                failed = [k for k, v in checks.items() if not v

**Tags**: ecommerce, implementation

**Palavras-chave**: Changelog

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 23/46 - copywriting_changelog_20251113.md (38 linhas) -->

# Changelog

**Categoria**: copywriting
**Qualidade**: 0.69/1.00
**Data**: 20251113

## Conteúdo

- v1.0.0 ({datetime.now().strftime('%Y-%m-%d')}): Versão inicial
"""

    # ==================== FASE 4: VALIDAÇÃO ====================

    async def validate_versículos(self, versículos: List[Path]) -> List[Path]:
        """Valida qualidade de versículos."""
        validated = []

        for vers_path in versículos:
            checks = {
                'has_title': self.validator.check_has_title(vers_path),
                'has_entropy': self.validator.check_has_entropy(vers_path),
                'entropy_threshold': self.validator.check_entropy_threshold(vers_path),
                'valid_markdown': self.validator.check_valid_markdown(vers_path),
                'no_duplicates': self.validator.check_no_duplicates(vers_path),
                'proper_relations': self.validator.check_relations(vers_path),
            }

            if all(checks.values()):
                validated.append(vers_path)
            else:
                failed = [k for k, v in checks.items() if not v

**Tags**: ecommerce, general, implementation

**Palavras-chave**: Changelog

**Origem**: desconhecida


---


<!-- VERSÍCULO 24/46 - copywriting_checklist_implementation_1_20251113.md (27 linhas) -->

# ✅ Checklist: Implementation

**Categoria**: copywriting
**Qualidade**: 0.70/1.00
**Data**: 20251113

## Conteúdo

- [ ] Copy all 6 core Python files to app/server/
- [ ] Copy all 5 command files to .claude/commands/
- [ ] Copy documentation files
- [ ] Add imports to server.py
- [ ] Call init_research_agent_routes(app)
- [ ] Set ANTHROPIC_API_KEY in .env
- [ ] Test /api/research/start endpoint
- [ ] Test /research command
- [ ] Monitor logs and metrics
- [ ] Deploy to production

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Checklist, Implementation

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 25/46 - copywriting_checklist_implementation_20251113.md (27 linhas) -->

# ✅ Checklist: Implementation

**Categoria**: copywriting
**Qualidade**: 0.70/1.00
**Data**: 20251113

## Conteúdo

- [ ] Copy all 6 core Python files to app/server/
- [ ] Copy all 5 command files to .claude/commands/
- [ ] Copy documentation files
- [ ] Add imports to server.py
- [ ] Call init_research_agent_routes(app)
- [ ] Set ANTHROPIC_API_KEY in .env
- [ ] Test /api/research/start endpoint
- [ ] Test /research command
- [ ] Monitor logs and metrics
- [ ] Deploy to production

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Checklist, Implementation

**Origem**: desconhecida


---


<!-- VERSÍCULO 26/46 - copywriting_como_usar_20251113.md (69 linhas) -->

# 🎮 Como Usar

**Categoria**: copywriting
**Qualidade**: 0.71/1.00
**Data**: 20251113

## Conteúdo

### Instalação

```bash
# O arquivo já está pronto
cd agents/
ls ecommerce_agent.py
```

### Execução Básica

```bash
python ecommerce_agent.py
```

**Saída**:
1. 2 cenários de teste (sucesso + falha)
2. Relatório completo
3. Dados em JSON para integração

### Customização

```python
# Criar seu próprio agente
agente = AgenteEcommerce()

# Adicionar produtos
agente.produtos['meu_produto'] = Produto(
    id="prod_001",
    nome="Meu Produto",
    descricao="Descrição detalhada aqui...",
    preco=99.90,
    categoria="Categoria",
    ética_score=0.95
)

# Adicionar clientes
agente.clientes['meu_cliente'] = Cliente(
    id="cli_001",
    nome="Nome Cliente",
    email="cliente@email.com"
)

# Processar compra
decisao = agente.iniciar_decisao_compra("cli_001", "prod_001")
pode_comprar = agente.processar_implementacao(decisao, produto, cliente)

if pode_comprar:
    agente.processar_compra(decisao, produto, cliente)

# Ver relatório
print(agente.gerar_relatorio())
```

---

**Tags**: ecommerce, implementation

**Palavras-chave**: Como, Usar

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 27/46 - copywriting_conceito_core_10_20251113.md (28 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### Knowledge Card
**English:** Structured JSON object containing extracted knowledge with ID, source, title, content, and keywords for indexing and retrieval.

**Portuguese:** Objeto JSON estruturado contendo conhecimento extraído com ID, fonte, título, conteúdo e palavras-chave para indexação e recuperação.

**Structure:**
```json
{
  "id": "GENESIS_CARD_0001",
  "source": "BIBLIA_LCM_GENESIS",
  "title": "Knowledge Card Title",
  "content": "Summary (max 500 chars)",
  "full_content": "Comple

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 28/46 - copywriting_conceito_core_11_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.61/1.00
**Data**: 20251113

## Conteúdo

### Etapa 1 Completa: Cultura Organizacional e Inovação – Vídeo Introdutório e KIT DIGITAL

[Roteiro do vídeo e conteúdo PDF já desenvolvidos acima]

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ECOMMERCE_VERSICULOS_FROM_GIT.md


---


<!-- VERSÍCULO 29/46 - copywriting_conceito_core_12_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.61/1.00
**Data**: 20251113

## Conteúdo

### Chunk 4: Ad Brief Generation
**Purpose**: Create advertising briefs

**Input**: Research consolidated data
**Output**: Ad copy variations, CTAs, value props

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 30/46 - copywriting_conceito_core_13_20251113.md (22 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.61/1.00
**Data**: 20251113

## Conteúdo

### Chunk 5: Copy Optimization
**Purpose**: Optimize ad copy for conversion

**Input**: Ad copy + research context
**Output**: Optimized variations by element

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 31/46 - copywriting_conceito_core_14_20251113.md (18 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.68/1.00
**Data**: 20251113

## Conteúdo

### 2.1 Entrada e Validação
- Normaliza o payload recebido do formulário (incluindo campos legados) e o valida com schemas estritos, rejeitando rotas ou métodos inesperados.
- Cada requisição gera erros diagnósticos padronizados que incluem contexto adicional: método, rota, tentativas de reparo e dicas para suporte.

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 32/46 - copywriting_conceito_core_15_20251113.md (19 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### 2.2 Construção do Prompt
- O prompt mestre descreve uma sequência rígida de etapas (benchmark → síntese → geração → validação → empacotamento) e exige JSON STRICT.
- Regras de marketplace e SEO são incorporadas diretamente no prompt: limites de caracteres, remoção de stopwords, obrigatoriedade de seções (títulos, bullet points, FAQ, variações de copy, metadados de confiança, vs[] etc.).
- Um fallback textual alternativo garante que, mesmo sem acesso ao arquivo principal, as instruções crític

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 33/46 - copywriting_conceito_core_16_20251113.md (18 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.69/1.00
**Data**: 20251113

## Conteúdo

### 3.2 Exibição do Resultado
- Visualização estruturada reconstrói o JSON retornado, exibindo seções copiáveis (títulos, descrição segmentada, FAQ, benefícios, keywords, bloco `vs[]`, metadados de confiança).
- Métricas agregadas (contagem de caracteres, quantidade de títulos, estatísticas SEO) são destacadas para facilitar ajustes rápidos.

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 34/46 - copywriting_conceito_core_17_20251113.md (18 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.68/1.00
**Data**: 20251113

## Conteúdo

### 2.1 Entrada e Validação
- Normaliza o payload recebido do formulário (incluindo campos legados) e o valida com schemas estritos, rejeitando rotas ou métodos inesperados.
- Cada requisição gera erros diagnósticos padronizados que incluem contexto adicional: método, rota, tentativas de reparo e dicas para suporte.

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 35/46 - copywriting_conceito_core_18_20251113.md (19 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### 2.2 Construção do Prompt
- O prompt mestre descreve uma sequência rígida de etapas (benchmark → síntese → geração → validação → empacotamento) e exige JSON STRICT.
- Regras de marketplace e SEO são incorporadas diretamente no prompt: limites de caracteres, remoção de stopwords, obrigatoriedade de seções (títulos, bullet points, FAQ, variações de copy, metadados de confiança, vs[] etc.).
- Um fallback textual alternativo garante que, mesmo sem acesso ao arquivo principal, as instruções crític

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 36/46 - copywriting_conceito_core_19_20251113.md (29 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.68/1.00
**Data**: 20251113

## Conteúdo

### Opção 5: Composição de Prompts (5-Chunk Library)

```bash
/compose_prompts
Use Research Report: (from previous /research execution)
Focus Areas: market, keywords, competitors, ads, copy
Output Format: markdown
Include Context: true
```

**Tempo estimado**: 1-2 minutos
**Output**: 5 AI-ready prompts ready for Claude/ChatGPT

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 37/46 - copywriting_conceito_core_1_20251113.md (19 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.62/1.00
**Data**: 20251113

## Conteúdo

### Tipografia
- **Poppins** (títulos/CTAs 600–800)  
- **Roboto** (corpo/UI 400–500)  
Boas práticas: desativar ligaturas; tracking +2 a +4 em títulos longos; LH 120–140%.

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 38/46 - copywriting_conceito_core_20251113.md (32 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.66/1.00
**Data**: 20251113

## Conteúdo

#### 6. research_agent_meta.py (500+ linhas)

**Conteúdo**:
- Meta-research system
- Quality scoring
- Performance tracking
- Optimization engine

**Funcionalidades**:
```
- Quality scoring (0-100)
- Efficiency analysis
- Bottleneck detection
- Recommendations generation
```

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 39/46 - copywriting_conceito_core_20_20251113.md (18 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.69/1.00
**Data**: 20251113

## Conteúdo

### 3.2 Exibição do Resultado
- Visualização estruturada reconstrói o JSON retornado, exibindo seções copiáveis (títulos, descrição segmentada, FAQ, benefícios, keywords, bloco `vs[]`, metadados de confiança).
- Métricas agregadas (contagem de caracteres, quantidade de títulos, estatísticas SEO) são destacadas para facilitar ajustes rápidos.

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 40/46 - copywriting_conceito_core_21_20251113.md (26 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.65/1.00
**Data**: 20251113

## Conteúdo

### Caso 4: Composição de Prompts para IA

**Fluxo**:
1. Execute `/research` para coletar dados
2. Execute `/compose_prompts`
3. Copy-paste chunks no Claude/ChatGPT

**Tempo total**: 10-15 minutos
**Resultado**: 5 prompts otimizados para AI

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 41/46 - copywriting_conceito_core_22_20251113.md (21 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.66/1.00
**Data**: 20251113

## Conteúdo

claude, copie-chunk, substitua, research-consolidation, execute, com-claude, 
1. execute /research
2. copie chunk 1 (research consolidation)
3. cole no claude/chatgpt
4. substitua variáveis pelo seu contexto
5. execute o prompt

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core, Keywords

**Origem**: desconhecida


---


<!-- VERSÍCULO 42/46 - copywriting_conceito_core_23_20251113.md (18 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.64/1.00
**Data**: 20251113

## Conteúdo

### O QUÊ é este Sistema?

O **Research Agent System** é uma plataforma completa de inteligência de mercado que automatiza a pesquisa e transformação de dados em insumos para criação de conteúdo de alta conversão.

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 43/46 - copywriting_conceito_core_24_20251113.md (21 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### Overview

A 5-Chunk Library é um sistema modular para compor prompts inteligentes que transformam dados de pesquisa em insumos para criação de conteúdo.

**Localização**: `.claude/commands/compose_prompts.md`
**Framework**: `app/como_pesquisa/02_prompt_composition/prompt_chunks_guide.md`

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 44/46 - copywriting_conceito_core_25_20251113.md (32 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.67/1.00
**Data**: 20251113

## Conteúdo

#### 3. research_agent_orchestrator.py (500+ linhas)

**Conteúdo**:
- Orquestração principal do pipeline
- Coordenação de agentes
- Agregação de resultados
- Error handling

**Métodos**:
```
- orchestrate_research()
- run_parallel_agents()
- aggregate_results()
- generate_report()
```

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 45/46 - copywriting_conceito_core_26_20251113.md (29 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.71/1.00
**Data**: 20251113

## Conteúdo

### ⚙️ Método PASTOR (Emocional com História)
Crie uma copy emocional com a estrutura **PASTOR**.  
- Produto: {{nome_produto}}  
- Persona: {{publico_ideal}}  
- Problema: {{dor_principal}}  
- Amplificação: {{amplificacao_dor}}  
- Solução: {{solucao_produto}}  
- Testemunho: {{testemunho}}  
- Oferta: {{oferta}}  
- Ação: {{cta}}  

Formato: até **500 caracteres**. Estilo carrossel ou vídeo curto.  

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 46/46 - copywriting_conceito_core_27_20251113.md (26 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.70/1.00
**Data**: 20251113

## Conteúdo

### ⚙️ Mini-Story (Storytelling Rápido pra Reels ou Stories)
Crie uma copy estilo **Mini-Story** com os elementos:  
1. Dor ou situação real → {{dor_principal}}  
2. Descoberta ou virada → {{descoberta}}  
3. Resultado → {{beneficio}}  
4. Chamada pra ação → {{cta}}  

Persona: {{publico_ideal}}  
Produto: {{nome_produto}}  

Formato: tom de conversa, para vídeo de até **30s**.

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- FIM DO CAPÍTULO 1 -->
<!-- Total: 46 versículos, 1179 linhas -->
