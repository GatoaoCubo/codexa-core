# pesquisa_agent Memory Context

## Agent Identity
- **Agent**: pesquisa_agent
- **Version**: 3.0.0
- **Domain**: Market research for Brazilian e-commerce
- **Output**: research_notes.md with 22 blocks + Trinity format

## Research Blocks (22)
1. LACUNAS DO BRIEF (brief gaps)
2. HEAD TERMS PRIORITARIOS (primary search terms)
3. LONGTAILS (longtail keywords)
4. SINONIMOS E VARIACOES (synonyms and variations)
5. TERMO CONTEXTUAL E OCASIAO (context and occasion)
6. DORES DO PUBLICO (audience pain points)
7. GANHOS DESEJADOS (desired gains)
8. OBJECOES E RESPOSTAS (objections and responses)
9. PROVAS E EVIDENCIAS (proofs and evidence)
10. DIFERENCIAIS COMPETITIVOS (competitive differentials)
11. RISCOS OU ALERTAS DE COMPLIANCE (compliance risks)
12. ANALISE DE CONCORRENTES (competitor analysis)
13. BENCHMARK DE CONCORRENTES (competitor benchmark)
14. ESTRATEGIAS E GAPS (strategies and gaps)
15. PADROES DE LINGUAGEM EFICAZ (effective language patterns)
16. SEO OUTBOUND (organic SEO)
17. SEO INBOUND (marketplace SEO)
18. REGRAS CRITICAS DE MARKETPLACE (marketplace rules)
19. DECISOES DE COPY INICIAIS (initial copy decisions)
20. CONSULTAS WEB (web queries)
21. IMAGENS ANALISADAS (image analysis)
22. NOTAS DE FALLBACK (fallback notes)
+ RESUMO EXECUTIVO (executive summary)

## Quality Standards
- All URLs must be real and verifiable
- Pricing in BRL, timestamped
- >= 3 competitors analyzed with quantitative data (prices, ratings)
- >= 15 web queries logged with URLs
- Pain points from actual customer reviews
- [SUGESTAO] placeholders <= 10%
- Confidence score >= 0.75

## 6-Dimension Scoring
| Dimension | Weight | Target |
|-----------|--------|--------|
| Completeness | 25% | 22/22 blocks |
| Competitors | 25% | >= 3 analyzed |
| Queries | 20% | >= 15 logged |
| Insights | 15% | Actionable |
| Compliance | 10% | ANVISA/INMETRO checked |
| Coherence | 5% | Low [SUGESTAO] ratio |

## Key Tools
- `mcp__browser__search_marketplace` - Search ML, Shopee, Amazon
- `mcp__browser__multi_search` - Search all 7 BR marketplaces
- `mcp__browser__screenshot` - Capture visual evidence
- `mcp__browser__screenshot_full` - Full page capture

## Validators
- `validate_iso.py` - ISO vectorstore compliance
- `code_interpreter/validator.py` - 22-block validation

## Workflow Pattern (9 Steps)
1. INTAKE VALIDATION - Validate brief (4 required fields)
2. QUERY BANK - Generate head terms + longtails
3. INBOUND SEARCH - Search 9 BR marketplaces
4. OUTBOUND SEARCH - SERP, social, Reclame Aqui
5. COMPETITOR ANALYSIS - Top 3-5 competitors
6. GAP IDENTIFICATION - Market gaps
7. COMPLIANCE CHECK - ANVISA, INMETRO, CONAR
8. SYNTHESIS - Consolidate insights
9. VALIDATION - Quality gates + output

## Human Review Checklist
- [ ] All URLs verified (not hallucinated)
- [ ] Pricing data current and in BRL
- [ ] Competitor analysis has >= 3 entries
- [ ] >= 15 queries logged with sources
- [ ] Reclame Aqui checked
- [ ] Quality score >= 0.75

## Integration
- **Upstream**: User brief (text or JSON)
- **Downstream**: anuncio_agent, marca_agent
- **Output**: research_notes.md (standalone, reusable)
