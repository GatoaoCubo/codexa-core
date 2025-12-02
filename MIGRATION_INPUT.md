# MIGRATION INPUT: Converter codexa.gato para Git Submodule

**Executar em**: `C:\Users\Dell\Documents\GitHub` (pasta raiz dos repos)
**Comando inicial**: Abrir terminal nesta pasta e iniciar Claude Code

---

## CONTEXTO (Leia primeiro)

Existem 2 repositórios que compartilham a mesma pasta `codexa.gato` via symlink:

```
C:\Users\Dell\Documents\GitHub\
├── connect-my-github/          ← Repo 1 (origin: GatoaoCubo/connect-my-github)
│   └── codexa.gato/            ← PASTA FÍSICA (sistema de agentes IA)
│
└── gato3-landing-pages/        ← Repo 2 (origin: GatoaoCubo/gato3-landing-pages)
    └── codexa.gato → SYMLINK   ← Aponta para connect-my-github/codexa.gato
```

**Problema**: Commits vão só para connect-my-github. O gato3-landing-pages fica dessincronizado.

**Solução**: Criar repo independente `codexa-core` e usar como submodule em ambos.

---

## TAREFA: Migração para Submodule

### Passo 1: Criar novo repositório codexa-core

```bash
# Criar novo repo no GitHub (usar gh cli)
gh repo create GatoaoCubo/codexa-core --public --description "CODEXA Multi-Agent System - Core"

# Clonar vazio
cd C:\Users\Dell\Documents\GitHub
git clone https://github.com/GatoaoCubo/codexa-core.git
```

### Passo 2: Mover conteúdo de codexa.gato para codexa-core

```bash
# Copiar todo o conteúdo (preservando estrutura)
cp -r connect-my-github/codexa.gato/* codexa-core/

# Entrar no novo repo
cd codexa-core

# Commit inicial
git add .
git commit -m "feat: Initial migration from connect-my-github/codexa.gato

Migrated complete CODEXA multi-agent system:
- 12 agents (anuncio, pesquisa, marca, mentor, photo, video, curso, qa, scout, ronronalda, voice, codexa)
- Knowledge Dissemination System with Phase 0
- 25 ADWs with cross-agent knowledge loading
- Pattern cards and playbooks

🤖 Generated with Claude Code"

git push origin main
```

### Passo 3: Remover codexa.gato de connect-my-github e adicionar como submodule

```bash
cd C:\Users\Dell\Documents\GitHub\connect-my-github

# Remover pasta (mantém backup se precisar)
mv codexa.gato codexa.gato.backup

# Adicionar como submodule
git submodule add https://github.com/GatoaoCubo/codexa-core.git codexa.gato

# Commit
git add .
git commit -m "refactor: Convert codexa.gato to git submodule

- Moved codexa.gato content to independent repo codexa-core
- Added as git submodule for better version control
- Enables sync between connect-my-github and gato3-landing-pages

🤖 Generated with Claude Code"

git push origin main
```

### Passo 4: Configurar gato3-landing-pages com submodule

```bash
cd C:\Users\Dell\Documents\GitHub\gato3-landing-pages

# Remover symlink antigo
rm codexa.gato

# Adicionar como submodule
git submodule add https://github.com/GatoaoCubo/codexa-core.git codexa.gato

# Commit
git add .
git commit -m "refactor: Replace symlink with git submodule

- Removed problematic symlink to connect-my-github/codexa.gato
- Added codexa-core as proper git submodule
- Now properly synced with codexa-core repo

🤖 Generated with Claude Code"

git push origin main
```

### Passo 5: Limpar backup

```bash
# Após confirmar que tudo funciona
cd C:\Users\Dell\Documents\GitHub\connect-my-github
rm -rf codexa.gato.backup
```

---

## VALIDAÇÃO

Após completar, verificar:

```bash
# Em connect-my-github
cd connect-my-github
git submodule status
# Deve mostrar: codexa.gato (commit hash)

# Em gato3-landing-pages
cd ../gato3-landing-pages
git submodule status
# Deve mostrar: codexa.gato (commit hash)

# Ambos apontando para mesmo commit do codexa-core
```

---

## WORKFLOW FUTURO

```bash
# Fazer mudanças nos agentes:
cd codexa-core
# editar arquivos
git commit -m "feat: nova feature"
git push

# Atualizar em connect-my-github:
cd ../connect-my-github
git submodule update --remote
git add codexa.gato
git commit -m "chore: update codexa-core submodule"
git push

# Atualizar em gato3-landing-pages:
cd ../gato3-landing-pages
git submodule update --remote
git add codexa.gato
git commit -m "chore: update codexa-core submodule"
git push
```

---

## ESTRUTURA FINAL

```
GitHub Repos:
├── GatoaoCubo/codexa-core           ← Sistema de agentes (independente)
├── GatoaoCubo/connect-my-github     ← DEV CODEXA (usa codexa-core como submodule)
└── GatoaoCubo/gato3-landing-pages   ← Empresa Gato³ (usa codexa-core como submodule)

Local:
C:\Users\Dell\Documents\GitHub\
├── codexa-core/                     ← Repo principal dos agentes
├── connect-my-github/
│   └── codexa.gato/                 ← Submodule → codexa-core
└── gato3-landing-pages/
    └── codexa.gato/                 ← Submodule → codexa-core
```

---

**IMPORTANTE**: Execute os comandos na ordem. Se algum falhar, pare e verifique antes de continuar.
