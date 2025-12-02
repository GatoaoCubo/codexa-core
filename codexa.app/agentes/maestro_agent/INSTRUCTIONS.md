# MAESTRO - Instructions

## COMO USAR

### Via Slash Command
```
/maestro "Lance os 10 produtos do catálogo com pesquisa completa"
```

### Via Linguagem Natural (quando MAESTRO está ativo)
```
User: "Quero criar uma marca para pet shop com tudo"
```

---

## OPERAÇÕES DISPONÍVEIS

### 1. Product Launch Pipeline
```
/maestro "Lance [N] produtos com [escopo]"

Escopos:
- "pesquisa" → só pesquisa_agent
- "pesquisa e anúncio" → pesquisa → anuncio
- "completo" → pesquisa → anuncio → photo
- "full" → pesquisa → marca → anuncio → photo → video
```

### 2. Brand Creation
```
/maestro "Crie uma marca para [categoria]"

Flow: pesquisa_agent → marca_agent → photo_agent
```

### 3. Batch Processing
```
/maestro "Gere [X] para todos os produtos"

X pode ser:
- "anúncios"
- "fotos"
- "vídeos"
- "pesquisas"
```

### 4. Course Creation
```
/maestro "Crie um curso sobre [tema]"

Flow: mentor_agent → curso_agent
```

### 5. Quality Audit
```
/maestro "Valide qualidade do [target]"

Flow: qa_gato3_agent
```

---

## FLAGS

| Flag | Descrição |
|------|-----------|
| `--dry-run` | Mostra plano sem executar |
| `--auto` | Executa sem confirmação |
| `--verbose` | Logs detalhados |
| `--max-concurrent=N` | Limite de spawns paralelos |

---

## EXEMPLOS COMPLETOS

### Exemplo 1: Launch Batch
```
/maestro "Lance os 22 produtos do catálogo com pesquisa e anúncio"

MAESTRO Response:
├── Phase 1: Load products_cache.json (22 items)
├── Phase 2: Spawn 22× pesquisa_agent (5 concurrent)
├── Phase 3: Spawn 22× anuncio_agent (5 concurrent)
└── Phase 4: Aggregate & validate

Estimated: ~45min, 44 spawns
Confirm? [Y/n]
```

### Exemplo 2: Brand Creation
```
/maestro "Crie marca completa para loja de eletrônicos gamer"

MAESTRO Response:
├── Phase 1: pesquisa_agent → market analysis
├── Phase 2: marca_agent → brand strategy
├── Phase 3: photo_agent → visual identity prompts
└── Phase 4: Consolidate brand book

Estimated: ~20min, 3 spawns
Confirm? [Y/n]
```

### Exemplo 3: Dry Run
```
/maestro --dry-run "Gere vídeos para os 5 top sellers"

MAESTRO Plan (DRY RUN - não executará):
├── Phase 1: Query top 5 from products_cache
├── Phase 2: Spawn 5× video_agent parallel
├── Phase 3: Collect & validate videos
└── Output: outputs/videos/batch_YYYY-MM-DD/

Would spawn: 5 tasks
Would take: ~15min
```

---

## INTEGRAÇÃO COM SCOUT

O Maestro usa automaticamente o Scout para:

1. **Carregar NAVIGATION_MAP.json** → sua memória
2. **Descobrir contexto** antes de cada spawn
3. **Validar paths** de outputs

```javascript
// Internamente o Maestro faz:
const context = await scout.smart_context({
  agent: "anuncio_agent",
  task: "ad_generation"
});

spawn(anuncio_agent, { context: context.must_read });
```

---

## QUALITY GATES

Cada spawn é validado:

| Metric | Threshold | Action if Fail |
|--------|-----------|----------------|
| Content Quality | ≥7.0/10 | Retry 1x |
| Compliance | PASS | Block + Alert |
| Format | Valid | Auto-fix |

---

## TROUBLESHOOTING

### "Agent not found"
→ Verifique se o agent existe no NAVIGATION_MAP

### "ADW not mapped"
→ Use `--verbose` para ver o plano detalhado

### "Spawn timeout"
→ Aumente timeout ou reduza `--max-concurrent`

### "Quality gate failed"
→ Verifique outputs individuais em `outputs/`

---

**Version**: 1.0.0
**Depends**: NAVIGATION_MAP.json, scout-mcp, all domain agents
