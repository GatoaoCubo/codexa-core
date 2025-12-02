# SESSION HANDOFF | CODEXA Landing Page Development

**Data**: 2025-11-30
**Projeto**: CODEXA.app Landing Page
**Repo**: `C:\Users\Dell\Documents\GitHub\connect-my-github`

---

## CONTEXTO RÁPIDO

Estamos desenvolvendo a Landing Page do **CODEXA.app** - sistema de 3 agentes IA especializados para e-commerce brasileiro (Pesquisa, Anúncio, Fotos).

**Modelo de negócio**: Assinatura mensal (7 dias grátis)
**Posicionamento**: "Cérebro IA proprietário que valoriza com o tempo"
**Curso**: É BÔNUS, não produto principal

---

## O QUE FOI FEITO NESTA SESSÃO

### 1. LP Completamente Reescrita (`src/pages/Index.tsx`)
- ❌ Removido: Jargões técnicos (iso_vectorstore, TAC-7, 5D/6D, HOP)
- ❌ Removido: 6 agentes → agora só 3 core
- ❌ Removido: "Pagamento único" → agora "Assinatura"
- ✅ Adicionado: Seção Economia (comparação vs agências/funcionários)
- ✅ Adicionado: "7 dias grátis", "Cancele quando quiser"
- ✅ Adicionado: Valores reais (R$ 384k/ano, R$ 302k vs R$ 3k)

### 2. MatrixRain Easter Eggs Premium (`src/components/MatrixRain.tsx`)
- Símbolos dourados: `$ ◆ X ★ E C O M L M`
- Cada símbolo tem mensagens temáticas (Seed Words da marca)
- Densidade sutil (4%)
- Tooltip premium com gradiente amber/gold

### 3. Pesquisa de Validação de Claims
- 12 claims do site validados com fontes reais
- JSON estruturado gerado para uso no código

---

## ARQUIVOS IMPORTANTES

```
# Landing Page
src/pages/Index.tsx              # LP principal (v4.0)
src/components/MatrixRain.tsx    # Background com easter eggs (v4.0)
src/components/ThemeToggle.tsx   # Toggle dark/light mode

# Pesquisa e Validação
codexa.gato/codexa.app/agentes/pesquisa_agent/outputs/CLAIMS_VALIDATION_LP.json

# Brand Strategy (referência)
codexa.gato/codexa.app/agentes/marca_agent/outputs/brand_strategy/brand_strategy_codexa_v2.md

# ADW do Pesquisa Agent
codexa.gato/codexa.app/agentes/pesquisa_agent/workflows/100_ADW_RUN_PESQUISA.md

# Curso (referência para argumentos)
codexa.gato/codexa.app/agentes/curso_agent/context/ARGUMENTOS_CORE_CURSO.md
```

---

## COMMITS REALIZADOS

```bash
8c84725 feat(MatrixRain): Premium multi-symbol easter eggs system
9d21040 refactor(LP): Complete rewrite for subscription model
```

**Status Git**: Up to date with origin/main (Lovable)

---

## PARA REINICIAR

```bash
# Navegar para o projeto
cd "C:\Users\Dell\Documents\GitHub\connect-my-github"

# Iniciar servidor dev
npm run dev

# Servidor roda em: http://localhost:8080
```

---

## ESTRUTURA ATUAL DA LP

```
1. Navbar (Assinar CTA)
2. HeroSection
   - "Seu cérebro IA que valoriza com o tempo"
   - R$ 384k/ano, 5min vs 2h, 100% privado
   - Video placeholder (ainda Rick Roll)
   - "7 dias grátis", "Cancele quando quiser", "Bônus: curso"

3. EconomiaSection
   - Tabela comparativa: Agência, Fotógrafo, Pesquisa, Analista
   - Total: R$ 384.000/ano
   - Comparação Funcionário 5 anos vs CODEXA

4. AgentsSection
   - Pesquisa (/prime-pesquisa)
   - Anúncio (/prime-anuncio)
   - Fotos (/prime-photo)

5. ValueSection
   - 6 cards: Privado, Anti-frágil, Valoriza, Qualquer IA, 24h, Ativo

6. FAQSection
   - 6 perguntas focadas em sellers

7. FinalCTASection
   - "Começar 7 dias grátis"

8. Footer
```

---

## CLAIMS VALIDADOS (resumo)

| Claim | Status | Fonte |
|-------|--------|-------|
| R$ 302k funcionário 5 anos | ✅ | FGV/CNI |
| R$ 5k/mês agência | ✅ | Leadster |
| R$ 1.5k/sessão fotógrafo | ✅ | Cronoshare |
| 90% PMEs sem IA | ✅ | IBGE/Cetic.br |
| ChatGPT usa dados p/ treino | ✅ | Olhar Digital |
| Claude NÃO usa dados | ✅ | Anthropic |
| ~R$ 0,50 por anúncio | ✅ | OpenAI Pricing |

**JSON completo**: `codexa.app/agentes/pesquisa_agent/outputs/CLAIMS_VALIDATION_LP.json`

---

## PRÓXIMOS PASSOS SUGERIDOS

1. **Substituir video placeholder** - Rick Roll → Video real do CODEXA
2. **Adicionar CHECKOUT_URL** - Integrar com sistema de pagamento
3. **Adicionar fontes na LP** - Credibilidade com dados validados
4. **Testar mobile responsiveness** - Verificar em diferentes dispositivos
5. **SEO meta tags** - Title, description, OG tags
6. **Analytics** - Google Analytics / Hotjar

---

## SEED WORDS DA MARCA (usar na comunicação)

- **Meta-Construção** - Camada acima das LLMs
- **Cérebro Plugável** - Funciona com qualquer IA
- **Destilação de Conhecimento** - Expertise proprietária
- **Anti-frágil** - Melhora com mudanças
- **Layer 3** - Categoria única
- **Ativo Digital** - Não é despesa, é patrimônio

---

## PALETA DE CORES

```
Primary (Teal): hsl(174, 72%, 46%)
Amber (Easter eggs): #F59E0B
Neural Black: #0B0D17
Meta Purple: #8B5CF6
Synapse Green: #10B981
```

---

**Para continuar**: Leia este arquivo + `src/pages/Index.tsx` + `CLAIMS_VALIDATION_LP.json`
