# 🚀 QUICK REFERENCE: CRUD com Agentes AI

> **TL;DR**: Guia rápido para ensinar agentes AI a realizar operações CRUD em repositórios

---

## 📌 CRUD - Os 4 Pilares

### Create (Criar)
```python
# Sempre verificar se já existe
if not file_exists(path):
    create_file(path, content)
    git_add_commit(path, "feat: add new file")
```

### Read (Ler)
```python
# Verificar existência primeiro
if file_exists(path):
    content = read_file(path)
    return content
```

### Update (Atualizar)
```python
# Backup antes de atualizar
backup = read_file(path)
update_file(path, new_content)
git_add_commit(path, "refactor: update file")
```

### Delete (Deletar)
```python
# SEMPRE pedir confirmação
if user_confirms():
    backup_file(path)
    delete_file(path)
    git_add_commit(path, "remove: delete file")
```

---

## 🎯 Arquivos de Instrução

### AGENTS.md (Universal)
```markdown
# Project: Nome do Projeto
# Stack: Python, FastAPI, PostgreSQL

## Commands
- Test: `pytest`
- Lint: `flake8`
- Format: `black .`

## Conventions
- Classes: PascalCase
- Functions: snake_case
- Max line: 100

## Permissions
✅ Read, test, format
❌ Delete, push, install
```

### CLAUDE.md (Claude Specific)
```markdown
# Role
AI coding assistant for Python project

# Quick Ref
- Main: `src/main.py`
- Tests: `tests/`
- Config: `config/`

# Patterns
- Async for I/O
- Type hints always
- Google docstrings
```

---

## 🛡️ Guardrails (Proteções)

### Arquivos Críticos - NUNCA deletar sem confirmação
- README.md
- LICENSE
- .gitignore
- package.json
- requirements.txt
- src/core/**

### Validações Obrigatórias
1. ✅ Verificar se arquivo existe
2. ✅ Validar permissões
3. ✅ Backup antes de modificar
4. ✅ Confirmar operações destrutivas
5. ✅ Logar todas as operações

---

## 💻 Implementação Rápida

### Skill de File Operations
```python
class FileOps:
    def create(path, content, msg):
        # Validar, criar, commit
        pass
    
    def read(path):
        # Verificar, ler, retornar
        pass
    
    def update(path, content, msg):
        # Backup, atualizar, commit
        pass
    
    def delete(path, msg, force=False):
        # Confirmar, backup, deletar
        pass
```

### System Prompt Base
```markdown
Você é um agente CRUD especializado.

ANTES de CRIAR:
1. Verificar se existe
2. Validar path
3. Commit descritivo

ANTES de ATUALIZAR:
1. Ler atual
2. Fazer backup
3. Aplicar mudanças

ANTES de DELETAR:
1. **SEMPRE** pedir confirmação
2. Fazer backup
3. Logar motivo
```

---

## 📁 Estrutura Recomendada

```
projeto/
├── .github/
│   └── AGENTS.md          # Instruções universais
├── .claude/
│   └── CLAUDE.md          # Instruções Claude
├── src/
│   ├── agents/            # Agentes AI
│   ├── skills/            # Skills especializados
│   └── core/              # Lógica principal
├── tests/
├── docs/
├── README.md              # Para humanos
└── CONTRIBUTING.md
```

---

## 🔄 Workflow de 3 Agentes

```
┌─────────────────────────┐
│  AGENTE 1: RESEARCH     │
│  Analisa + Pesquisa     │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│  AGENTE 2: GENERATOR    │
│  Gera Conteúdo/Código   │
└───────────┬─────────────┘
            ↓
┌─────────────────────────┐
│  AGENTE 3: VALIDATOR    │
│  Valida + Entrega       │
└─────────────────────────┘
```

---

## ⚡ Comandos Essenciais

### Git Operations
```bash
# Criar com commit
git add file.py
git commit -m "feat: add new feature"

# Atualizar com commit
git add file.py
git commit -m "refactor: improve logic"

# Deletar com commit
git rm file.py
git commit -m "remove: delete deprecated file"
```

### API GitHub (PyGithub)
```python
from github import Github

g = Github(token)
repo = g.get_repo("user/repo")

# Create
repo.create_file("path", "message", "content")

# Read
content = repo.get_contents("path")

# Update
repo.update_file("path", "message", "content", sha)

# Delete
repo.delete_file("path", "message", sha)
```

---

## 📊 Formato de Resposta Padrão

```json
{
  "operation": "create|read|update|delete",
  "status": "success|error|pending_confirmation",
  "file_path": "path/to/file",
  "message": "Descrição clara",
  "details": {
    "lines_added": 50,
    "commit_sha": "abc123..."
  }
}
```

---

## ⚙️ Configuração config.yaml

```yaml
agent:
  name: "crud_agent"
  version: "1.0.0"
  
permissions:
  read: true
  write: true
  delete: false  # Requer confirmação
  
critical_files:
  - "README.md"
  - "LICENSE"
  - ".gitignore"
  - "package.json"
  
backup:
  enabled: true
  directory: ".backups/"
  
logging:
  level: "INFO"
  file: "agent.log"
```

---

## 🎓 README Template Mínimo

```markdown
# Nome do Projeto

> Descrição em uma linha

## Quick Start

```bash
git clone repo
cd projeto
npm install
npm start
```

## Estrutura

```
src/
├── core/
├── agents/
└── utils/
```

## Comandos

- Test: `npm test`
- Build: `npm run build`
- Lint: `npm run lint`

## Contribuir

1. Fork
2. Feature branch
3. Commit
4. Pull Request
```

---

## 🔍 Checklist Rápido

### Antes de CRIAR
- [ ] Arquivo não existe?
- [ ] Path válido?
- [ ] Conteúdo validado?
- [ ] Mensagem de commit?

### Antes de ATUALIZAR
- [ ] Arquivo existe?
- [ ] Backup feito?
- [ ] Mudanças validadas?
- [ ] Commit descritivo?

### Antes de DELETAR
- [ ] Não é arquivo crítico?
- [ ] Usuário confirmou?
- [ ] Backup feito?
- [ ] Motivo documentado?

---

## 🚨 Regras de Ouro

1. **NUNCA** deletar sem confirmação
2. **SEMPRE** fazer backup antes de modificar
3. **SEMPRE** validar inputs
4. **SEMPRE** logar operações
5. **SEMPRE** usar mensagens de commit descritivas

---

## 📚 Recursos Rápidos

**Documentação Completa:** Ver `GUIA_COMPLETO_AGENTES_CRUD_REPOSITORIOS.md`

**GitHub Repos:**
- [NirDiamant/GenAI_Agents](https://github.com/NirDiamant/GenAI_Agents)
- [microsoft/ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners)
- [ai-in-pm/CRUD-Agentic-System](https://github.com/ai-in-pm/CRUD-Agentic-System)

**Artigos:**
- [Builder.io - AGENTS.md](https://www.builder.io/blog/agents-md)
- [GitHub Blog - AI Agents](https://github.blog/ai-and-ml/github-copilot/onboarding-your-ai-peer-programmer-setting-up-github-copilot-coding-agent-for-success/)

---

## 🎯 Próximos Passos

1. Criar `AGENTS.md` no seu repositório
2. Implementar `FileOperationsSkill`
3. Criar agente CRUD básico
4. Testar em ambiente dev
5. Iterar baseado em feedback

---

**Versão:** 1.0.0  
**Última atualização:** 2025-11-11

[📖 Ver Guia Completo](./GUIA_COMPLETO_AGENTES_CRUD_REPOSITORIOS.md)
