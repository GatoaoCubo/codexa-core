# LIVRO: Operacoes
## CAPÍTULO 48

**Versículos consolidados**: 1
**Linhas totais**: 234
**Gerado em**: 2025-11-15 08:40:00

---

<!-- VERSÍCULO 1/1 - fractal_migration_patterns.md (234 linhas) -->

# Padrões de Migração Fractal | Arquitetura Auto-Contida

## CONCEITOS-CHAVE

• **Arquitetura Fractal**: Cada agente é auto-contido - comandos, prompts, configs vivem DENTRO do agente
• **Eliminação de Duplicação**: Um arquivo, um lugar - nunca duplicar entre root e agent folders
• **Commands Co-Localizados**: `/anuncio` vive em `anuncio_agent/commands/`, não em root
• **Meta-Construção Vertical**: CODEXA meta-commands vivem em `codexa_agent/commands/`, não dispersos

## POR QUE IMPORTA

A migração fractal do sistema CODEXA (Nov 2025) demonstrou como arquitetura mal organizada gera:
- **Duplicação Silenciosa**: 9 arquivos duplicados entre root e agents
- **Referências Quebradas**: 27+ referências obsoletas a `scout_agent` consolidado
- **Confusão de Ownership**: Comandos genéricos sem dono claro
- **Manutenção Dupla**: Atualizar em 2 lugares ou criar inconsistência

Após implementar fractal:
- ✅ Zero duplicação (de 9 → 0 arquivos duplicados)
- ✅ Ownership claro (cada comando tem um agent dono)
- ✅ Navegação intuitiva (procure no agent, não no root)
- ✅ Escalabilidade (novo agent = nova pasta isolada)

## PADRÕES DE MIGRAÇÃO

### Padrão 1: Consolidação de Comandos Agent-Specific

**Antes (Duplicado)**:
```
commands/
├── anuncio.md          # Root copy
└── brand.md            # Root copy

agentes/
├── anuncio_agent/
│   └── commands/anuncio.md    # Agent copy (IDENTICAL)
└── marca_agent/
    └── commands/brand.md      # Agent copy (IDENTICAL)
```

**Depois (Fractal)**:
```
agentes/
├── anuncio_agent/
│   └── commands/anuncio.md    # ÚNICO lugar
└── marca_agent/
    └── commands/brand.md      # ÚNICO lugar

commands/  → DELETED (root commands folder removed)
```

**Ação**:
1. Verificar identidade com `diff`
2. Deletar root copy
3. Atualizar `.claude/settings.json` para apontar agentes/*/commands/

### Padrão 2: Meta-Commands Verticalizados

**Antes (Misplaced)**:
```
commands/
├── 90_codexa_when_to_use.md
├── 91_codexa_build_agent.md
├── 92_codexa_build_command.md
└── ... (7 meta-commands)

agentes/
└── codexa_agent/
    └── commands/
        └── ... (mesmos 7 arquivos)
```

**Depois (Vertical)**:
```
agentes/
└── codexa_agent/
    └── commands/
        ├── 90_codexa_when_to_use.md     # Source of truth
        ├── 91_codexa_build_agent.md
        ├── 92_codexa_build_command.md
        ├── 93_codexa_build_mcp.md
        ├── 94_codexa_build_prompt.md
        ├── 95_codexa_build_schema.md
        ├── 96_codexa_orchestrate.md
        ├── 98_codexa_cleanup.md         # Exclusive to agent
        ├── codexa.md
        ├── codexa_quick.md
        ├── codexa_run.md
        └── orchestrator.md
```

**Rationale**: CODEXA commands constroem o sistema CODEXA → pertencem ao `codexa_agent`

### Padrão 3: Builders & Validators Organizados

**Antes (Flat Root)**:
```
codexa.app/
├── 01_agent_builder.py
├── 02_agent_meta_constructor.py
├── 03_build_task.py
├── 04_chore_task.py
├── 05_command_generator.py
├── 06_cron_orchestrator.py
├── 07_hop_sync_validator.py
├── 08_prompt_generator.py
├── 09_readme_validator.py
└── 10_taxonomy_validator.py
```

**Depois (Hierárquico)**:
```
agentes/
└── codexa_agent/
    ├── builders/
    │   ├── 01_agent_builder.py
    │   ├── 02_agent_meta_constructor.py
    │   ├── 03_build_task.py
    │   ├── 04_chore_task.py
    │   ├── 05_command_generator.py
    │   ├── 06_cron_orchestrator.py
    │   ├── 08_prompt_generator.py
    │   ├── 11_doc_sync_builder.py
    │   ├── 13_fractal_nav_sync.py
    │   ├── 14_tac7_header_generator.py
    │   └── 15_trinity_output_generator.py
    └── validators/
        ├── 07_hop_sync_validator.py
        ├── 09_readme_validator.py
        ├── 10_taxonomy_validator.py
        └── 12_doc_sync_validator.py
```

**Rationale**: Builders constroem, validators validam - semântica clara

### Padrão 4: Workflows ADW Auto-Documentados

**Estrutura**:
```
agentes/
└── codexa_agent/
    └── workflows/
        ├── 97_ADW_NEW_AGENT_WORKFLOW.md
        ├── 98_ADW_CONSOLIDATION_WORKFLOW.md
        ├── 99_ADW_SYSTEM_UPGRADE_WORKFLOW.md
        ├── 100_ADW_DOC_SYNC_WORKFLOW.md
        ├── README_ADW_100.md
        └── reports/
            ├── ADW_100_sync_20251114_*.json
            ├── ADW_100_sync_20251114_*.md
            ├── fractal_nav_sync_*.json
            └── FRACTAL_NAV_FINAL_REPORT.md
```

**Características**:
- Numeração 97-100+ (acima dos commands 90-96)
- Reports timestampados (.json + .md)
- README específico para workflow 100
- Auto-documentação de execução

## LIMPEZA DE ARQUIVOS TEMPORÁRIOS

### Padrão de Detecção

**Backups de Prompts**:
```bash
# Detectar
find . -name "*.backup_*"

# Padrões encontrados
prompts/20_titulo_generator.backup_20251113_*.md
prompts/40_bullet_points.backup_20251113_*.md
```

**Caches Python**:
```bash
# Detectar
find . -type d -name "__pycache__"
find . -name "*.pyc"

# Sempre deletar - nunca versionar
```

**Reports Antigos**:
```bash
# Manter apenas o mais recente
workflow_report_*.txt   → Keep latest only
ADW_*_sync_*.json       → Archive old after 7 days
```

**Arquivos NUL/nul (Windows)**:
```bash
# Detectar e remover
find . -name "nul" -o -name "NUL"
```

## CORREÇÃO DE REFERÊNCIAS OBSOLETAS

### Padrão de Consolidação de Agentes

**Cenário**: `scout_agent` + `conhecimento_agent` → `mentor_agent` (Nov 2025)

**Referências a Corrigir**:
```markdown
# ANTES (obsoleto)
/prime-scout → Code discovery specialist
/prime-knowledge → ML training datasets

# DEPOIS (consolidado)
/prime-mentor → Onboarding (guides, tutorials, code discovery)
```

**Arquivos Afetados** (11 encontrados):
- PRIME.md (root)
- README.md (root)
- Agent READMEs (anuncio, pesquisa, marca)
- Integration guides

**Comando de Detecção**:
```bash
grep -r "scout_agent\|conhecimento_agent" \
  --exclude-dir=_archived \
  --exclude-dir=.git \
  --include="*.md"
```

## MIGRAÇÃO SEGURA - CHECKLIST

### Antes de Deletar
- [ ] Criar backup: `cp -r commands/ _archived/commands_backup_$(date +%Y%m%d)/`
- [ ] Verificar identidade: `diff -r commands/ agentes/*/commands/`
- [ ] Git add backup: `git add _archived/`
- [ ] Commit backup: `git commit -m "chore: backup before fractal migration"`

### Durante Migração
- [ ] Deletar duplicatas do root FIRST
- [ ] Atualizar references em PRIME.md, README.md
- [ ] Verificar `.claude/settings.json` paths
- [ ] Testar um command de cada agent: `/anuncio`, `/codexa-when_to_use`

### Após Migração
- [ ] Remover pastas vazias: `commands/`, `git/`, `e2e/`
- [ ] Limpar backups de prompts
- [ ] Atualizar 41_DOCUMENTATION_INDEX.md
- [ ] Git status clean check
- [ ] Commit fractal: `git commit -m "refactor(architecture): implement fractal architecture - commands live with agents"`

## MÉTRICAS DE SUCESSO

### Antes da Migração Fractal
| Métrica | Valor |
|---------|-------|
| Root `commands/` files | 19 |
| Duplicated files | 9 |
| Agent command folders | 2 |
| Orphaned commands | 2 |
| Python files in root | 10+ |

### Depois da Migração Fractal
| Métrica | Valor | Melhoria |
|---------|-------|----------|
| Root `commands/` files | 0 | -100% ✅ |
| Duplicated files | 0 | -100% ✅ |
| Agent command folders | 5 | +150% ✅ |
| Orphaned commands | 0 | -100% ✅ |
| Python files organized | builders/ + validators/ | Clear hierarchy ✅ |

## APLICAÇÃO PRÁTICA

**Quando criar novo agente**:
1. Estrutura fractal desde o início:
   ```
   agentes/
   └── novo_agent/
       ├── commands/
       │   └── novo.md           # Command próprio
       ├── prompts/
       │   └── *_HOP.md          # HOPs específicos
       ├── config/
       ├── src/
       └── PRIME.md, README.md
   ```

2. NUNCA criar command em root
3. NUNCA duplicar entre root e agent
4. Registrar em `51_AGENT_REGISTRY.json`

**Quando refatorar agentes existentes**:
1. Detectar duplicação: `diff -r commands/ agentes/*/commands/`
2. Mover orphans: `commands/X.md → agentes/X_agent/commands/X.md`
3. Atualizar referências: `grep -r "commands/X.md"`
4. Deletar root após verificação

**Quando consolidar agentes**:
1. Mapear dependências: quem referencia `old_agent`?
2. Atualizar todos os `/prime-old` → `/prime-new`
3. Mover artifacts: `old_agent/X → new_agent/X`
4. Archive: `mv old_agent/ _archived/agents/old_agent_deprecated_$(date +%Y%m%d)/`
5. Commit: "refactor(agents): consolidate old_agent into new_agent"
