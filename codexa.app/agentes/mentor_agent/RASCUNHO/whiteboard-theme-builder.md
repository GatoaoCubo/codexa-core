# Lousa: Bundle .md — Meta‑Guia para Tema (PNGs) + Texto no Claude Code

> Whiteboard editável. Copie/baixe este arquivo como `whiteboard-theme-builder.md`. Tudo aqui segue a hierarquia: **Slash → Subagent/MCP → Skill → Plugin**.

---

## 0) Visão Rápida (Mapa Mental)
- **Core‑4**: Contexto · Modelos · Prompt · Ferramentas
- **Princípio‑raiz**: *“The prompt is the new fundamental unit of knowledge work.”* (o prompt é o átomo do fluxo)
- **Uso correto por nível**
  - **Slash** → tarefa atômica (manual, determinística)
  - **Subagent** → delegação especializada + **paralelismo** + **isolamento**
  - **MCP** → integrações externas (APIs/DB/FS/Imagem)
  - **Skill** → orquestração autônoma (carrega contexto sob demanda)
  - **Plugin** → empacotar e distribuir **commands/agents/skills/hooks/MCP** como toolkit compartilhável

---

## 1) Insights dos PNGs (Análise)
> Sumário do que as imagens reforçam e como virar requisitos do bundle

1) **Plugins** (empacotar & distribuir)  
   → Criar um **manifesto de plugin** listando `commands/`, `skills/`, `subagents/`, `hooks/` e `mcp/`. Facilita compartilhar a fábrica de tema como um toolkit único.

2) **Quadrante dos blocos (Skills, MCP, Subagent, Slash)**  
   → Usar o diagrama como **política de decisão** no QA: cada entrega deve citar *por que* está no bloco certo.

3) **Pasta de “output‑styles”** (vários .md)  
   → Padronizar **estilos de saída** (yaml‑structured, markdown‑focused, table‑based…). Inclua *templates* para copiar/colar.

4) **Prompt como unidade fundamental**  
   → Começar tudo com **Slash Commands** robustos e com saídas estruturadas (JSON/YAML) — depois compor.

5) **Listagem hierárquica (Skills, MCP, Subagents, Slash)**  
   → Reforça a **hierarquia**: nunca criar três ferramentas para a mesma ação atômica. Escolher **uma**.

6) **Pros/Cons de Skills**  
   → Pros: invocadas pelo agente; contexto progressivo; composição.  
   → Cons: *aninhamento limitado*; *cadeias longas* podem ser não determinísticas.  
   → Ação: testes de confiabilidade (goldens) e *fallbacks* via Slash quando necessário.

> Apêndice com imagens no fim do arquivo.

---

## 2) Estrutura de Pastas Sugerida
```
.claude/
  commands/theme/*.md
  commands/qa/*.md
  settings.json              # hooks e automações
skills/theme_builder/SKILL.md
subagents/art-director/README.md
subagents/copy-editor/README.md
mcp/config.json              # servidores/ferramentas conectadas
output-styles/*.md           # formatos prontos de saída
context/theme.yml            # single source of truth
assets/refs/                 # logos/paleta/exemplos
manual/outline.md            # esqueleto do texto
scripts/*.sh
plugin/manifest.json         # bundle para distribuição
dist/
```

---

## 3) CONTEXT (single source of truth)
```yaml
# context/theme.yml
project: "Tema PNGs + Manual"
brand:
  palette: ["#111111", "#f5f5f5", "#d4af37"]
  style_keywords: ["minimal", "editorial", "luxo-conceitual"]
image:
  shots: 9
  aspect: "1:1"
  constraints:
    - "sem texto na imagem"
    - "fundo branco ou derivação da paleta"
    - "produto inalterado; variações apenas de enquadramento/iluminação"
copy:
  tone: ["claro", "técnico", "elegante"]
  structure: ["Introdução", "Core‑4", "Hierarquia", "Boas práticas", "Conclusão"]
qa:
  image_checks: ["sem watermark", "sem artefatos", "consistência da paleta"]
  copy_checks: ["clareza", "coerência com hierarquia", "sem duplicidades"]
```

---

## 4) MODELS (papéis)
- **Orchestrator**: coordena o fluxo (Claude Code)
- **Art Director**: crítica visual (valida PNGs)
- **Copy Strategist**: estrutura e polimento do texto
- **Tool Backends**: via **MCP** (imagem, git, drive, sql…)

Checklist de readiness ✅
- [ ] context/theme.yml definido
- [ ] mcp/config.json com endpoints válidos
- [ ] commands/ e output-styles/ presentes

---

## 5) PROMPT (Slash Commands — primitivos)
> Sempre comece por aqui. Saídas **estruturadas** são obrigatórias.

### 5.1 `/theme/shotlist`
```md
# ~/.claude/commands/theme/shotlist.md
## Objetivo
Gerar 9 cenas coerentes a partir de context/theme.yml.
## Saída (JSON por cena)
{"id":"S1","goal":"hero","lens":"50mm","light":"softbox","bg":"branco","risks":["texto","reflexo"]}
```

### 5.2 `/theme/image-prompts`
```md
# ~/.claude/commands/theme/image-prompts.md
Converta a shotlist em prompts de geração 1:1.
Saída por item: {"prompt":"…", "negative":"texto, watermark, artefatos", "ratio":"1:1"}
```

### 5.3 `/theme/manual-outline`
```md
# ~/.claude/commands/theme/manual-outline.md
Produza um índice cobrindo: Fundamento do Prompt/Slash; Subagents; MCP; Skills; Antipadrões; Boas práticas; Conclusão.
Saída: markdown com H2/H3.
```

### 5.4 `/qa/image`
```md
# ~/.claude/commands/qa/image.md
Valide PNGs contra context/theme.yml → JSON: {id, checks:{no_text, palette_ok, artifacts:false}, notes}
```

### 5.5 `/qa/copy`
```md
# ~/.claude/commands/qa/copy.md
Valide o texto: estrutura, clareza, hierarquia correta, ausência de redundância → JSON de diagnóstico.
```

---

## 6) TOOLS — Subagents, MCP, Skills, Hooks, Plugins

### 6.1 Subagents (especialização)
- **art-director** → consome shotlist, critica PNGs (paralelo)
- **copy-editor** → reescreve seções conforme estilo

> Cada subagent deve declarar **entradas/saídas** e não replicar lógica já presente nos Slash Commands.

### 6.2 MCP (integrações)
Exemplo de stub:
```json
// mcp/config.json
{
  "image": {"endpoint": "http://localhost:7000/generate", "parallel": true},
  "git": {"repo_path": "/workspace"},
  "drive": {"root": "./dist"}
}
```

### 6.3 Skill (orquestração)
```md
# skills/theme_builder/SKILL.md
## Propósito
Orquestrar Tema (PNGs + Manual) seguindo a hierarquia.
## Plano
1) /theme/shotlist → 2) /theme/image-prompts
3) mcp.image.generate (parallel=true)
4) subagents/art-director (crítica por S1..S9)
5) /qa/image
6) /theme/manual-outline
7) subagents/copy-editor → rascunho final
8) /qa/copy
9) Empacotar em dist/tema-<date>/
## Saídas
- dist/pngs/*.png
- dist/manual/manual.md
- dist/report/qa.json
```

### 6.4 Hooks (automação determinística)
```json
// .claude/settings.json
{
  "hooks": {
    "postRun": ["./scripts/catalogar.sh"],
    "onFileEdit": ["./scripts/lint_md.sh"],
    "onGitCommit": ["./scripts/tag_build.sh"]
  }
}
```

### 6.5 Plugin (bundle compartilhável)
```json
// plugin/manifest.json (template)
{
  "name": "theme-builder",
  "version": "0.1.0",
  "includes": {
    "commands": [".claude/commands/theme", ".claude/commands/qa"],
    "skills": ["skills/theme_builder"],
    "subagents": ["subagents/art-director", "subagents/copy-editor"],
    "hooks": [".claude/settings.json"],
    "mcp": ["mcp/config.json"],
    "outputStyles": ["output-styles"]
  },
  "dist": "dist/"
}
```
> **Nota**: o formato exato do manifesto pode variar conforme a versão do Claude Code. Use este arquivo como **template** de empacotamento.

---

## 7) Output‑styles (templates de resposta)
`output-styles/yaml-structured.md`
```md
# Saída YAML Estruturada
```yaml
summary: "..."
shots: [{id: S1, verdict: pass, notes: "..."}]
copy_quality: {readability: "B2/C1", hierarchy_ok: true}
```
```

`output-styles/markdown-focused.md`
```md
## Sumário
- …

## PNGs (S1..S9)
- **S1**: OK — notas…

## Texto
- Estrutura, tom e ajustes…
```

---

## 8) Testes de Aceitação
```json
{
  "images": {"count": 9, "ratio": "1:1", "forbidden": ["texto", "watermark", "artefatos"], "palette_consistency": true},
  "copy": {"sections": ["Introdução","Core‑4","Hierarquia","Boas práticas","Conclusão"], "readability": "B2/C1", "matches_hierarchy": true},
  "packaging": {"dist_exists": true, "qa_report": "dist/report/qa.json", "git_tag": "tema-<date>"}
}
```

Checklist de liberação ✅
- [ ] 9 PNGs válidos e revisados
- [ ] Manual em `dist/manual/manual.md`
- [ ] `report/qa.json` gerado
- [ ] Tag criada no repositório

---

## 9) Antipadrões a evitar
- Repetir a **mesma ação atômica** em três lugares (Slash + Subagent + Skill)
- **Pré‑carregar** contexto gigante; prefira metadados e *progressive disclosure*
- Encadear muitas Skills sem *goldens* de confiabilidade

---

## 10) Como rodar (roteiro humano)
1. Preencha `context/theme.yml`
2. Execute `/theme/shotlist` → revise
3. Execute `/theme/image-prompts` → gere com `mcp.image.generate`
4. Rodar **art-director** (paralelo) → ajuste onde falhar
5. `/qa/image` → garantir conformidade
6. `/theme/manual-outline` → **copy-editor** → `/qa/copy`
7. Hooks empacotam e geram `dist/`
8. `plugin/manifest.json` permite compartilhar o toolkit

---

## Apêndice — PNGs (referência)

**A. Plugins (empacotamento)**  
![Plugins](sandbox:/mnt/data/288e693a-9ca2-48fe-aee2-8428e418d703.png)

**B. Quadrante (Skills/MCP/Subagent/Slash)**  
![Quadrante](sandbox:/mnt/data/39b2bcf4-d53e-4858-ade2-165207891b87.png)

**C. Output‑styles (pasta)**  
![Output Styles](sandbox:/mnt/data/6b7a834d-b808-4b61-86fe-97ae9a113af7.png)

**D. Prompt = unidade fundamental**  
![Prompt Fundamental](sandbox:/mnt/data/284c8854-3e95-4e9f-b6d0-278bcd7fcdfe.png)

**E. Lista hierárquica (Skills→MCP→Subagents→Slash)**  
![Hierarquia](sandbox:/mnt/data/160d8d72-8490-4fad-b94e-2ba0e84a4668.png)

**F. Pros/Cons de Skills**  
![Pros e Cons](sandbox:/mnt/data/74fb476b-800a-4a1f-a65a-d7b12e6e9cb8.png)

**G. Quadrante com exemplos**  
![Quadrante Exs](sandbox:/mnt/data/2acd709d-f2ec-46bc-a60d-8ff8bb5f176a.png)
