# 📚 GUIA COMPLETO: AGENTES AI, CRUD E ORGANIZAÇÃO DE REPOSITÓRIOS

> **Compilação Completa**: Conhecimento dos arquivos do projeto + Pesquisas Web sobre como ensinar agentes AI a realizar operações CRUD em repositórios

---

## 📋 ÍNDICE

1. [Organização de Repositórios](#organização-de-repositórios)
2. [Como Construir README.md Profissional](#como-construir-readmemd)
3. [CRUD: Create, Read, Update, Delete](#crud-operações-fundamentais)
4. [Como Ensinar Agentes AI a Realizar CRUD](#ensinando-agentes-crud)
5. [Arquivos de Instruções para Agentes](#arquivos-de-instrução-para-agentes)
6. [Estrutura LCM-AI (Living Contextual Memory)](#estrutura-lcm-ai)
7. [Framework de Agentes Genérico](#framework-de-agentes)
8. [Boas Práticas e Padrões](#boas-práticas)
9. [Exemplos Práticos](#exemplos-práticos)
10. [Recursos e Referências](#recursos-e-referências)

---

## 1. ORGANIZAÇÃO DE REPOSITÓRIOS

### 1.1 Estrutura Base Recomendada

```
nome-do-projeto/
├── .github/
│   ├── workflows/          # GitHub Actions
│   └── AGENTS.md          # Instruções para agentes AI
├── docs/
│   ├── api/               # Documentação da API
│   ├── architecture/      # Diagramas e arquitetura
│   └── guides/            # Guias de uso
├── src/                   # Código fonte
│   ├── core/             # Funcionalidades principais
│   ├── agents/           # Agentes AI
│   ├── skills/           # Skills especializados
│   └── utils/            # Utilitários
├── tests/                 # Testes
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── scripts/              # Scripts de automação
├── config/               # Arquivos de configuração
├── .claude/              # Configurações para Claude
│   └── commands/         # Slash commands
├── README.md             # Para humanos
├── AGENTS.md             # Para agentes AI
├── CLAUDE.md             # Para Claude especificamente
├── CONTRIBUTING.md       # Guia de contribuição
└── LICENSE               # Licença do projeto
```

### 1.2 Princípios de Organização

**Separação de Concerns:**
- Código de produção em `/src`
- Testes isolados em `/tests`
- Documentação centralizada em `/docs`
- Configurações em `/config`

**Hierarquia Clara:**
```
Raiz
├─ Camada de Raízes (-)     # Ingestão, Arquivo, Histórico
├─ Camada de Tronco (0)     # Orquestração Central
└─ Camada de Galhos (+)     # Distribuição, Output
```

**Imutabilidade e Versionamento:**
- Usar Git para controle de versão
- Branches por feature/bugfix
- Commits pequenos e frequentes
- Tags para releases

---

## 2. COMO CONSTRUIR README.md

### 2.1 Template de README Profissional

```markdown
# 📦 Nome do Projeto

> **TL;DR:** Uma linha descrevendo o que o projeto faz

![Badge de Status](https://img.shields.io/badge/status-active-success.svg)
![Versão](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Licença](https://img.shields.io/badge/license-MIT-green.svg)

## 📖 Sobre

[2-3 parágrafos explicando:]
- **O que é**: Descrição clara do projeto
- **Por que existe**: Problema que resolve
- **Quando usar**: Casos de uso principais

## ✨ Features

- ✅ Feature 1: Descrição breve
- ✅ Feature 2: Descrição breve
- ✅ Feature 3: Descrição breve
- 🚧 Feature 4: Em desenvolvimento

## 🚀 Quick Start

### Pré-requisitos

```bash
node >= 18.0.0
npm >= 9.0.0
python >= 3.10
```

### Instalação

```bash
# Clone o repositório
git clone https://github.com/usuario/projeto.git

# Entre no diretório
cd projeto

# Instale dependências
npm install

# Configure ambiente
cp .env.example .env
```

### Uso Básico

```javascript
// Exemplo mínimo funcional
import { Component } from './src/core';

const instance = new Component({
  option1: 'value1',
  option2: 'value2'
});

const result = await instance.execute();
console.log(result);
```

## 📚 Documentação

- [Guia Completo](docs/guides/complete-guide.md)
- [API Reference](docs/api/README.md)
- [Exemplos](docs/examples/)
- [FAQ](docs/FAQ.md)

## 🏗️ Arquitetura

```
┌─────────────────────────────────────┐
│         User Interface              │
├─────────────────────────────────────┤
│      Orchestration Layer            │
│  ┌─────────┬─────────┬─────────┐   │
│  │ Agent 1 │ Agent 2 │ Agent 3 │   │
│  └─────────┴─────────┴─────────┘   │
├─────────────────────────────────────┤
│         Core Services               │
├─────────────────────────────────────┤
│         Data Layer                  │
└─────────────────────────────────────┘
```

## 🧪 Testes

```bash
# Executar todos os testes
npm test

# Testes unitários
npm run test:unit

# Testes de integração
npm run test:integration

# Coverage
npm run test:coverage
```

## 📦 Deploy

### Desenvolvimento
```bash
npm run dev
```

### Produção
```bash
npm run build
npm start
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

1. Fork o projeto
2. Crie sua branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Changelog

Ver [CHANGELOG.md](CHANGELOG.md) para histórico de versões.

## 👥 Autores

- **Seu Nome** - *Trabalho Inicial* - [@username](https://github.com/username)

Ver também a lista de [contribuidores](https://github.com/usuario/projeto/contributors).

## 📄 Licença

Este projeto está sob a licença MIT - veja [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- Inspiração
- Referências
- etc

## 📞 Contato

- Email: seu@email.com
- Twitter: [@username](https://twitter.com/username)
- LinkedIn: [Seu Nome](https://linkedin.com/in/username)

---

**[⬆ Voltar ao topo](#nome-do-projeto)**
```

### 2.2 Seções Essenciais de um README

1. **Título e Descrição**: Clara e concisa
2. **Badges**: Status, versão, licença, CI/CD
3. **Quick Start**: Instalação e uso rápido
4. **Documentação**: Links para docs detalhadas
5. **Contribuição**: Como contribuir
6. **Licença**: Tipo de licença

---

## 3. CRUD: OPERAÇÕES FUNDAMENTAIS

### 3.1 O que é CRUD?

**CRUD** é um acrônimo para as quatro operações básicas de persistência:

- **C**reate (Criar)
- **R**ead (Ler)
- **U**pdate (Atualizar)
- **D**elete (Deletar)

### 3.2 CRUD em Repositórios Git

#### Create (Criar)

```python
# Criar novo arquivo
def create_file(path: str, content: str):
    """
    Cria um novo arquivo no repositório
    
    Args:
        path: Caminho do arquivo
        content: Conteúdo do arquivo
    """
    with open(path, 'w') as f:
        f.write(content)
    
    # Adicionar ao git
    subprocess.run(['git', 'add', path])
    subprocess.run(['git', 'commit', '-m', f'Create {path}'])
```

#### Read (Ler)

```python
# Ler arquivo existente
def read_file(path: str) -> str:
    """
    Lê conteúdo de um arquivo
    
    Args:
        path: Caminho do arquivo
        
    Returns:
        Conteúdo do arquivo como string
    """
    with open(path, 'r') as f:
        return f.read()
```

#### Update (Atualizar)

```python
# Atualizar arquivo existente
def update_file(path: str, new_content: str):
    """
    Atualiza conteúdo de um arquivo existente
    
    Args:
        path: Caminho do arquivo
        new_content: Novo conteúdo
    """
    with open(path, 'w') as f:
        f.write(new_content)
    
    # Commit da mudança
    subprocess.run(['git', 'add', path])
    subprocess.run(['git', 'commit', '-m', f'Update {path}'])
```

#### Delete (Deletar)

```python
# Deletar arquivo
def delete_file(path: str):
    """
    Remove um arquivo do repositório
    
    Args:
        path: Caminho do arquivo a ser removido
    """
    import os
    os.remove(path)
    
    # Remover do git
    subprocess.run(['git', 'rm', path])
    subprocess.run(['git', 'commit', '-m', f'Delete {path}'])
```

### 3.3 CRUD com API GitHub

```python
from github import Github

class GitHubCRUD:
    """Classe para operações CRUD via API do GitHub"""
    
    def __init__(self, token: str, repo_name: str):
        self.g = Github(token)
        self.repo = self.g.get_repo(repo_name)
    
    def create_file(self, path: str, content: str, commit_msg: str):
        """Cria um novo arquivo no repositório"""
        self.repo.create_file(
            path=path,
            message=commit_msg,
            content=content,
            branch="main"
        )
    
    def read_file(self, path: str) -> str:
        """Lê conteúdo de um arquivo"""
        file_content = self.repo.get_contents(path)
        return file_content.decoded_content.decode()
    
    def update_file(self, path: str, new_content: str, commit_msg: str):
        """Atualiza arquivo existente"""
        file_content = self.repo.get_contents(path)
        self.repo.update_file(
            path=path,
            message=commit_msg,
            content=new_content,
            sha=file_content.sha,
            branch="main"
        )
    
    def delete_file(self, path: str, commit_msg: str):
        """Deleta arquivo"""
        file_content = self.repo.get_contents(path)
        self.repo.delete_file(
            path=path,
            message=commit_msg,
            sha=file_content.sha,
            branch="main"
        )
```

---

## 4. COMO ENSINAR AGENTES AI A REALIZAR CRUD

### 4.1 Princípios Fundamentais

**1. Documentação Clara**
- Sempre documente as operações permitidas
- Use exemplos práticos
- Defina limites e permissões

**2. Instruções Explícitas**
- Especifique quando criar vs. atualizar
- Defina naming conventions
- Estabeleça padrões de commit

**3. Guardrails (Proteções)**
- Nunca deletar arquivos críticos sem confirmação
- Sempre fazer backup antes de operações destrutivas
- Validar entradas antes de executar

### 4.2 System Prompt para CRUD

```markdown
# AGENTE CRUD - INSTRUÇÕES DE SISTEMA

## Papel
Você é um assistente especializado em operações CRUD em repositórios Git.

## Capacidades
Você pode:
- ✅ Criar novos arquivos
- ✅ Ler arquivos existentes
- ✅ Atualizar conteúdo de arquivos
- ✅ Deletar arquivos (com confirmação)

## Processo de Decisão

### Antes de CRIAR:
1. Verificar se o arquivo já existe
2. Validar o caminho de destino
3. Confirmar naming convention
4. Criar com mensagem de commit descritiva

### Antes de LER:
1. Verificar se o arquivo existe
2. Validar permissões de leitura
3. Retornar conteúdo formatado

### Antes de ATUALIZAR:
1. Ler conteúdo atual primeiro
2. Fazer backup do estado anterior
3. Aplicar mudanças incrementais
4. Commit com descrição clara das mudanças

### Antes de DELETAR:
1. **SEMPRE** pedir confirmação do usuário
2. Verificar se não é arquivo crítico
3. Fazer backup antes de deletar
4. Commit explicando motivo da remoção

## Arquivos Críticos (NUNCA deletar sem aprovação explícita)
- README.md
- LICENSE
- .gitignore
- package.json / requirements.txt
- src/core/**
- config/**

## Padrões de Commit

### Create
```
feat: add <component> <description>

Exemplo: feat: add user authentication module
```

### Update
```
refactor: update <component> <what_changed>

Exemplo: refactor: update API endpoints to use async/await
```

### Delete
```
remove: delete <component> <reason>

Exemplo: remove: delete deprecated utility functions
```

## Validações Obrigatórias

Antes de qualquer operação:
1. ✅ Validar sintaxe (se aplicável)
2. ✅ Verificar se não quebra dependências
3. ✅ Confirmar com usuário se operação destrutiva
4. ✅ Fazer backup se necessário

## Exemplo de Workflow

```python
# Exemplo de como você deve executar uma operação CRUD

# CENÁRIO: Usuário pede para criar um novo módulo

# 1. VALIDAR
if file_exists(path):
    ask_user("Arquivo já existe. Deseja sobrescrever?")

# 2. EXECUTAR
content = generate_module_code(specifications)
create_file(path, content)

# 3. CONFIRMAR
git_add(path)
git_commit("feat: add new authentication module")

# 4. INFORMAR
return f"✅ Módulo criado com sucesso em {path}"
```

## Regras de Segurança

1. **Nunca executar comandos shell arbitrários**
2. **Sempre validar inputs do usuário**
3. **Usar paths relativos, nunca absolutos**
4. **Verificar permissões antes de operações de escrita**
5. **Fazer log de todas as operações**

## Formato de Resposta

Sempre responda estruturadamente:

```json
{
  "operation": "create|read|update|delete",
  "status": "success|error|pending_confirmation",
  "file_path": "path/to/file",
  "message": "Descrição do que foi feito",
  "details": {
    "lines_added": 50,
    "lines_removed": 0,
    "commit_sha": "abc123..."
  }
}
```
```

### 4.3 Skills para CRUD

```python
# skills/file_operations.py

class FileOperationsSkill:
    """
    Skill para operações de arquivo com validações
    """
    
    CRITICAL_FILES = [
        'README.md',
        'LICENSE',
        '.gitignore',
        'package.json',
        'requirements.txt'
    ]
    
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.logger = setup_logger('file_operations')
    
    def create(self, path: str, content: str, commit_msg: str = None) -> dict:
        """
        Cria um novo arquivo com validações
        """
        # Validar path
        if os.path.exists(os.path.join(self.repo_path, path)):
            return {
                "status": "error",
                "message": f"Arquivo {path} já existe. Use update() para modificar."
            }
        
        # Criar arquivo
        full_path = os.path.join(self.repo_path, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w') as f:
            f.write(content)
        
        # Git operations
        commit_msg = commit_msg or f"feat: add {path}"
        subprocess.run(['git', 'add', path], cwd=self.repo_path)
        result = subprocess.run(
            ['git', 'commit', '-m', commit_msg],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        
        self.logger.info(f"Created file: {path}")
        
        return {
            "status": "success",
            "operation": "create",
            "file_path": path,
            "message": f"Arquivo {path} criado com sucesso",
            "commit": result.stdout
        }
    
    def read(self, path: str) -> dict:
        """
        Lê conteúdo de um arquivo
        """
        full_path = os.path.join(self.repo_path, path)
        
        if not os.path.exists(full_path):
            return {
                "status": "error",
                "message": f"Arquivo {path} não encontrado"
            }
        
        with open(full_path, 'r') as f:
            content = f.read()
        
        return {
            "status": "success",
            "operation": "read",
            "file_path": path,
            "content": content,
            "size": len(content),
            "lines": content.count('\n') + 1
        }
    
    def update(self, path: str, new_content: str, commit_msg: str = None) -> dict:
        """
        Atualiza arquivo existente com backup
        """
        full_path = os.path.join(self.repo_path, path)
        
        if not os.path.exists(full_path):
            return {
                "status": "error",
                "message": f"Arquivo {path} não existe. Use create() para novo arquivo."
            }
        
        # Backup do conteúdo anterior
        with open(full_path, 'r') as f:
            old_content = f.read()
        
        backup_path = f"{full_path}.backup"
        with open(backup_path, 'w') as f:
            f.write(old_content)
        
        # Atualizar arquivo
        with open(full_path, 'w') as f:
            f.write(new_content)
        
        # Git operations
        commit_msg = commit_msg or f"refactor: update {path}"
        subprocess.run(['git', 'add', path], cwd=self.repo_path)
        result = subprocess.run(
            ['git', 'commit', '-m', commit_msg],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        
        # Remover backup se tudo OK
        os.remove(backup_path)
        
        self.logger.info(f"Updated file: {path}")
        
        return {
            "status": "success",
            "operation": "update",
            "file_path": path,
            "message": f"Arquivo {path} atualizado com sucesso",
            "changes": {
                "old_size": len(old_content),
                "new_size": len(new_content),
                "diff_lines": abs(
                    old_content.count('\n') - new_content.count('\n')
                )
            },
            "commit": result.stdout
        }
    
    def delete(self, path: str, commit_msg: str = None, force: bool = False) -> dict:
        """
        Deleta arquivo com confirmação para arquivos críticos
        """
        # Verificar se é arquivo crítico
        if os.path.basename(path) in self.CRITICAL_FILES and not force:
            return {
                "status": "pending_confirmation",
                "message": f"⚠️ {path} é um arquivo crítico. Confirme com force=True",
                "file_path": path
            }
        
        full_path = os.path.join(self.repo_path, path)
        
        if not os.path.exists(full_path):
            return {
                "status": "error",
                "message": f"Arquivo {path} não encontrado"
            }
        
        # Fazer backup antes de deletar
        backup_dir = os.path.join(self.repo_path, '.backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        backup_path = os.path.join(backup_dir, f"{os.path.basename(path)}.deleted")
        shutil.copy2(full_path, backup_path)
        
        # Deletar arquivo
        os.remove(full_path)
        
        # Git operations
        commit_msg = commit_msg or f"remove: delete {path}"
        subprocess.run(['git', 'rm', path], cwd=self.repo_path)
        result = subprocess.run(
            ['git', 'commit', '-m', commit_msg],
            cwd=self.repo_path,
            capture_output=True,
            text=True
        )
        
        self.logger.warning(f"Deleted file: {path} (backup at {backup_path})")
        
        return {
            "status": "success",
            "operation": "delete",
            "file_path": path,
            "message": f"Arquivo {path} deletado (backup em {backup_path})",
            "backup_location": backup_path,
            "commit": result.stdout
        }
```

---

## 5. ARQUIVOS DE INSTRUÇÕES PARA AGENTES

### 5.1 AGENTS.md - Padrão Universal

```markdown
# AGENTS.md

## Project Overview

This repository contains [brief description].

**Stack**: Python 3.10+, FastAPI, PostgreSQL, Redis

## Build & Test

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Type checking
mypy src/

# Linting
flake8 src/ --max-line-length=100

# Format code
black src/
```

## Architecture

```
src/
├── core/          # Core business logic
├── api/           # API endpoints
├── agents/        # AI agents
├── models/        # Data models
└── utils/         # Utilities
```

### Key Components

- **core/engine.py**: Main orchestration engine
- **agents/crud_agent.py**: CRUD operations handler
- **api/routes.py**: API route definitions

## Development Workflow

### Branch Naming
- `feature/description`
- `bugfix/issue-number-description`
- `hotfix/critical-issue`

### Commit Convention
```
type(scope): description

Types: feat, fix, refactor, docs, test, chore
Example: feat(agents): add file operations skill
```

### PR Requirements
- [ ] All tests passing
- [ ] Code coverage > 80%
- [ ] Type hints complete
- [ ] Documentation updated
- [ ] Reviewed by at least one maintainer

## Conventions & Patterns

### Code Style
- PEP 8 compliant
- Max line length: 100 characters
- Use type hints everywhere
- Docstrings in Google style

### Naming
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private: prefix with `_`

### File Structure
```python
"""Module docstring."""

# Standard library imports
import os
import sys

# Third-party imports
import numpy as np
from fastapi import FastAPI

# Local imports
from .core import Engine
from .utils import helper

# Constants
MAX_RETRIES = 3

# Classes and functions
class MyClass:
    """Class docstring."""
    pass
```

## Security & Permissions

### Allowed Without Prompt
- Read any file in `src/`, `tests/`, `docs/`
- Run unit tests
- Format code with black
- Type check with mypy

### Ask First
- Installing new dependencies
- Modifying `requirements.txt`
- Git push operations
- Deleting files
- Changing configuration files

### Never Allow
- Exposing API keys or secrets
- Modifying `.git/` directory directly
- Running arbitrary shell commands
- Accessing files outside project root

## Domain-Specific Rules

### CRUD Operations
- Always validate input before DB operations
- Use transactions for multi-step operations
- Log all CRUD operations
- Never hard-delete; use soft delete (is_deleted flag)

### API Design
- RESTful principles
- Consistent error responses
- Pagination for list endpoints
- Rate limiting on all endpoints

### Database
- Use SQLAlchemy ORM
- Migrations via Alembic
- Connection pooling configured
- Indexes on frequently queried fields

## Common Tasks

### Add New Endpoint
1. Define Pydantic model in `models/`
2. Create route in `api/routes.py`
3. Add business logic in `core/`
4. Write tests in `tests/api/`
5. Update API docs

### Add New Agent
1. Create file in `agents/` folder
2. Inherit from `BaseAgent`
3. Implement required methods
4. Add to agent registry
5. Document in `docs/agents/`

## Troubleshooting

### Tests Failing
- Check database connection
- Clear Redis cache: `redis-cli FLUSHALL`
- Rebuild test fixtures: `pytest --fixtures`

### Import Errors
- Verify virtual environment active
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

## Resources

- [API Documentation](docs/api/README.md)
- [Architecture Guide](docs/architecture/DESIGN.md)
- [Contributing Guide](CONTRIBUTING.md)
```

### 5.2 CLAUDE.md - Específico para Claude

```markdown
# CLAUDE.md

## Repository Context for Claude

This file provides Claude-specific guidance for working with this codebase.

## Your Role

You are an AI coding assistant helping with this Python project. You have
access to file operations, can run commands, and should follow the patterns
established in this codebase.

## Quick Reference

### File Locations
- Main application: `src/core/engine.py`
- API routes: `src/api/routes.py`
- Models: `src/models/`
- Tests: `tests/`
- Config: `config/settings.yaml`

### Common Commands
```bash
# Run app locally
python -m src.main

# Run tests
pytest

# Check types
mypy src/

# Format
black src/ tests/
```

## Coding Patterns

### Error Handling
Always use try-except with specific exceptions:

```python
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise CustomException(f"Failed to X: {e}") from e
```

### Async Operations
Use async/await for I/O operations:

```python
async def fetch_data(id: int) -> Data:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"/api/data/{id}") as response:
            return await response.json()
```

### Database Operations
Always use context managers:

```python
async with get_db_session() as session:
    result = await session.execute(query)
    await session.commit()
```

## Decision Trees

### When to Create a New File
- New feature with >100 lines: Create new module
- Utility function: Add to `utils/helpers.py`
- New API endpoint: Add to existing route file
- New model: Create in `models/`

### When to Modify vs. Create
- Bug fix: Modify existing file
- New feature that extends existing: Modify with backward compatibility
- Completely new feature: Create new file/module

## Testing Strategy

Always write tests for:
- New functions/classes
- Bug fixes (regression test)
- API endpoints
- Database operations

Test structure:
```python
def test_feature_success_case():
    """Test the happy path."""
    result = function_under_test(valid_input)
    assert result == expected_output

def test_feature_error_case():
    """Test error handling."""
    with pytest.raises(ExpectedException):
        function_under_test(invalid_input)
```

## Git Workflow

1. Create feature branch
2. Make changes
3. Run tests locally
4. Commit with conventional message
5. Push and create PR

**Don't automatically push**. Ask user first.

## Specific Guidance for This Project

### Agent Development
When creating or modifying agents:
1. Inherit from `BaseAgent`
2. Implement `execute()` method
3. Add proper error handling
4. Include comprehensive docstrings
5. Write unit tests

Example:
```python
class NewAgent(BaseAgent):
    """
    Agent for doing X.
    
    This agent handles Y by doing Z.
    """
    
    async def execute(self, task: Task) -> Result:
        """
        Execute the agent's main task.
        
        Args:
            task: Task description with parameters
            
        Returns:
            Result object with status and data
            
        Raises:
            AgentError: If execution fails
        """
        try:
            # Implementation
            pass
        except Exception as e:
            raise AgentError(f"Failed to execute: {e}") from e
```

### API Development
When adding API endpoints:
1. Define Pydantic models first
2. Add route with proper HTTP method
3. Add OpenAPI documentation
4. Implement business logic in core/
5. Write integration tests

### Database Changes
1. Create Alembic migration
2. Test migration up and down
3. Update models
4. Clear cache if needed

## Questions to Ask Before Acting

Before making changes, consider:
- Is this the right file to modify?
- Will this break existing functionality?
- Are there tests for this?
- Does this follow project conventions?
- Should I ask the user for confirmation?

## When in Doubt

If you're unsure about:
- Project structure decisions
- Breaking changes
- Security implications
- Performance impacts

**ASK THE USER FIRST** rather than proceeding with assumptions.
```

### 5.3 copilot-instructions.md (GitHub Copilot)

```markdown
# GitHub Copilot Instructions

## Project Context
Python project using FastAPI, SQLAlchemy, and async/await patterns.

## Code Style
- Follow PEP 8
- Use type hints always
- Max line length: 100
- Google-style docstrings

## Patterns to Use

### Async Functions
```python
async def fetch_user(user_id: int) -> User:
    """Fetch user from database."""
    async with get_db() as session:
        result = await session.get(User, user_id)
        return result
```

### Error Handling
```python
try:
    result = await operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise CustomError("Readable message") from e
```

### Logging
```python
logger.info("Operation started", extra={"user_id": user_id})
logger.error("Operation failed", extra={"error": str(e)}, exc_info=True)
```

## Don't Generate
- Hard-coded credentials
- Untyped code
- Synchronous database calls
- Print statements (use logging)
- TODO comments without tickets

## Testing
Generate tests that:
- Test both success and failure cases
- Use fixtures for common setup
- Are independent and can run in any order
- Have descriptive names

```python
def test_user_creation_succeeds():
    """Test that valid user data creates user successfully."""
    user = create_user(valid_data)
    assert user.id is not None
    assert user.email == valid_data["email"]
```

## Security
Never generate:
- API keys or secrets
- SQL queries with string concatenation
- Unvalidated user input in commands
- Direct file system access without validation
```

---

## 6. ESTRUTURA LCM-AI (Living Contextual Memory)

### 6.1 Filosofia da Árvore

```
                    🌳 LCM-AI TREE
                         │
        ┌────────────────┼────────────────┐
        │                │                │
    📊 FRUTO        🌿 FOLHAS       🌱 GALHOS (+)
   (Output)      (Processing)     (Distribution)
                     │
                 🌲 TRONCO (0)
                (Orchestration)
                     │
          ┌──────────┼──────────┐
          │          │          │
      💾 RAÍZES (-)
   (Ingestion & Archive)
```

### 6.2 Estrutura de Diretórios

```
lcm-ai/
├── 00_∞_hub/               # TRONCO - Orquestração
│   ├── core.py            # Motor principal
│   ├── config.yaml        # Configuração e pesos
│   ├── system_prompt.md   # Prompt do sistema
│   └── monitoring.jsonl   # Logs de operação
│
├── skills/                 # FOLHAS - Skills especializados
│   ├── skill_synthesizer.py
│   ├── skill_tokenizer.py
│   ├── skill_purpose_extractor.py
│   ├── skill_qa_generator.py
│   └── skill_evaluator.py
│
├── -01_capture/           # RAÍZES - Captura bruta
│   └── YYYYMMDD/
│       └── HHmmss_hash.original
│
├── -02_build/             # RAÍZES - Artefatos construídos
│   └── domain/
│       └── entity/
│           └── purpose/
│               ├── artifact.md          # Humano
│               ├── artifact.llm.json    # IA
│               └── artifact.meta.json   # Metadados
│
├── -03_index/             # RAÍZES - Índice e busca
│   ├── search.db          # SQLite full-text
│   ├── embeddings.faiss   # Vetores
│   └── taxonomy.yaml      # Taxonomia
│
├── -05_storage/           # RAÍZES - Armazenamento frio
│   └── YYYY/MM/
│       └── archived_*.tar.gz
│
├── -08_backup/            # RAÍZES - Backup
│   ├── daily/
│   ├── weekly/
│   └── monthly/
│
├── +01_intake/            # GALHOS - Entrada
│   └── upload/
│
├── +02_route/             # GALHOS - Roteamento
│   └── routing_decisions.json
│
├── +03_execute/           # GALHOS - Execução
│   └── execution_logs/
│
├── +05_delivery/          # GALHOS - Entrega
│   └── outputs/
│
├── +08_feedback/          # GALHOS - Feedback
│   └── user_feedback.jsonl
│
└── views/                 # Symlinks para organização
    ├── by-domain/
    ├── by-entity/
    ├── by-purpose/
    └── by-date/
```

### 6.3 Trinity Format

Cada artefato gera 3 arquivos:

**1. artifact.md** (Para humanos)
```markdown
# Título do Artefato

## Resumo (1 linha)
Essência em uma sentença.

## Resumo (2 linhas)
Contexto + valor principal.

## Resumo (3 linhas)
Problema + solução + benefício.

## Resumo (5 linhas)
[Fibonacci: mais detalhes]

## Resumo (8 linhas)
[Fibonacci: contexto completo]

## Conteúdo Principal
[Texto completo processado]

## Metadados
- Domain: [domain]
- Entity: [entity]
- Purpose: [purpose]
- Keywords: [tag1, tag2, tag3]

## Q&A
1. **P:** Pergunta relevante?
   **R:** Resposta concisa.
```

**2. artifact.llm.json** (Para IA)
```json
{
  "version": "1.0",
  "hash": "sha256:...",
  "domain": "ai-ml",
  "entity": "transformer",
  "purpose": "education",
  "summaries": {
    "1_line": "...",
    "2_lines": "...",
    "3_lines": "...",
    "5_lines": "...",
    "8_lines": "..."
  },
  "content_chunks": [
    {
      "id": "chunk_001",
      "tokens": 128,
      "embedding": [0.123, 0.456, ...],
      "text": "..."
    }
  ],
  "qa_pairs": [
    {
      "question": "...",
      "answer": "...",
      "confidence": 0.95
    }
  ],
  "keywords": ["keyword1", "keyword2"],
  "related_artifacts": ["uuid1", "uuid2"]
}
```

**3. artifact.meta.json** (Metadados)
```json
{
  "uuid": "abc123...",
  "created_at": "2025-01-15T10:30:00Z",
  "source_file": "original.pdf",
  "source_hash": "sha256:...",
  "processing": {
    "skills_used": [
      "synthesizer",
      "tokenizer",
      "purpose_extractor",
      "qa_generator",
      "evaluator"
    ],
    "processing_time": 2.5,
    "model_version": "claude-sonnet-4-5"
  },
  "taxonomy": {
    "domain": "ai-ml",
    "entity": "transformer",
    "purpose": "education"
  },
  "metrics": {
    "quality_score": 0.92,
    "novelty_score": 0.78,
    "utility_score": 0.85
  },
  "version_history": [
    {
      "version": "1.0",
      "timestamp": "2025-01-15T10:30:00Z",
      "changes": "Initial creation"
    }
  ]
}
```

---

## 7. FRAMEWORK DE AGENTES GENÉRICO

### 7.1 Arquitetura de 3 Agentes

```
┌─────────────────────────────────────────┐
│   AGENTE 1: RESEARCH & INTELLIGENCE     │
│   (Pesquisa + Análise)                  │
│   • Web search                          │
│   • Competitor analysis                 │
│   • SEO research                        │
│   • Pattern identification              │
└────────────┬────────────────────────────┘
             │
             ↓ research_notes.md
             │
┌────────────┴────────────────────────────┐
│   AGENTE 2: GENERATOR                   │
│   (Geração de Conteúdo)                 │
│   • Copy generation                     │
│   • Code generation                     │
│   • Documentation                       │
│   • Compliance check                   │
└────────────┬────────────────────────────┘
             │
             ↓ generated_content.json
             │
┌────────────┴────────────────────────────┐
│   AGENTE 3: VALIDATOR & DELIVERER       │
│   (Validação + Entrega)                 │
│   • Quality checks                      │
│   • Format validation                   │
│   • Final assembly                      │
│   • Delivery prep                       │
└────────────┬────────────────────────────┘
             │
             ↓ final_output/
             │
┌────────────┴────────────────────────────┐
│           ENTREGA FINAL                 │
└─────────────────────────────────────────┘
```

### 7.2 Implementação Base de Agente

```python
# agents/base_agent.py

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime
import logging

class BaseAgent(ABC):
    """
    Classe base para todos os agentes do sistema
    """
    
    def __init__(self, name: str, version: str, config: Dict[str, Any]):
        self.name = name
        self.version = version
        self.config = config
        self.logger = logging.getLogger(f"agent.{name}")
        self.execution_history: List[Dict] = []
    
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Método principal de execução do agente
        
        Args:
            task: Dicionário com informações da tarefa
            
        Returns:
            Resultado da execução
        """
        pass
    
    def log_execution(self, task: Dict, result: Dict, duration: float):
        """Registra execução para auditoria"""
        execution_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent": self.name,
            "version": self.version,
            "task": task,
            "result": result,
            "duration_seconds": duration,
            "success": result.get("status") == "success"
        }
        self.execution_history.append(execution_record)
        self.logger.info(f"Execution completed", extra=execution_record)
    
    async def validate_input(self, task: Dict) -> bool:
        """Valida entrada antes de processar"""
        required_fields = self.config.get("required_fields", [])
        
        for field in required_fields:
            if field not in task:
                self.logger.error(f"Missing required field: {field}")
                return False
        
        return True
    
    def get_metrics(self) -> Dict[str, Any]:
        """Retorna métricas do agente"""
        total_executions = len(self.execution_history)
        successful = sum(1 for ex in self.execution_history if ex["success"])
        
        return {
            "agent": self.name,
            "version": self.version,
            "total_executions": total_executions,
            "successful_executions": successful,
            "success_rate": successful / total_executions if total_executions > 0 else 0,
            "average_duration": sum(ex["duration_seconds"] for ex in self.execution_history) / total_executions if total_executions > 0 else 0
        }

# agents/crud_agent.py

from typing import Dict, Any
import time
from .base_agent import BaseAgent
from skills.file_operations import FileOperationsSkill

class CRUDAgent(BaseAgent):
    """
    Agente especializado em operações CRUD
    """
    
    def __init__(self, repo_path: str, config: Dict[str, Any]):
        super().__init__(
            name="crud_agent",
            version="1.0.0",
            config=config
        )
        self.file_ops = FileOperationsSkill(repo_path)
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa operação CRUD
        
        Task format:
        {
            "operation": "create|read|update|delete",
            "path": "path/to/file",
            "content": "...",  # Para create/update
            "commit_msg": "...",  # Opcional
            "force": False  # Para delete de arquivos críticos
        }
        """
        start_time = time.time()
        
        # Validar entrada
        if not await self.validate_input(task):
            result = {
                "status": "error",
                "message": "Invalid task input"
            }
            self.log_execution(task, result, time.time() - start_time)
            return result
        
        operation = task["operation"]
        path = task["path"]
        
        try:
            # Executar operação apropriada
            if operation == "create":
                result = self.file_ops.create(
                    path=path,
                    content=task["content"],
                    commit_msg=task.get("commit_msg")
                )
            
            elif operation == "read":
                result = self.file_ops.read(path=path)
            
            elif operation == "update":
                result = self.file_ops.update(
                    path=path,
                    new_content=task["content"],
                    commit_msg=task.get("commit_msg")
                )
            
            elif operation == "delete":
                result = self.file_ops.delete(
                    path=path,
                    commit_msg=task.get("commit_msg"),
                    force=task.get("force", False)
                )
            
            else:
                result = {
                    "status": "error",
                    "message": f"Unknown operation: {operation}"
                }
            
        except Exception as e:
            self.logger.exception(f"Error executing {operation} on {path}")
            result = {
                "status": "error",
                "message": str(e),
                "operation": operation,
                "path": path
            }
        
        duration = time.time() - start_time
        self.log_execution(task, result, duration)
        
        return result
```

---

## 8. BOAS PRÁTICAS

### 8.1 Princípios Gerais

**1. Clarity over Cleverness**
- Código claro > código "inteligente"
- Nomes descritivos
- Funções pequenas e focadas

**2. Fail Fast and Loud**
- Validar inputs cedo
- Exceptions específicas
- Logging adequado

**3. Immutability When Possible**
- Dados imutáveis por padrão
- Append-only logs
- Versionamento de tudo

**4. Security First**
- Nunca hard-code secrets
- Validar todas as entradas
- Princípio do menor privilégio

**5. Observability**
- Log tudo relevante
- Métricas de performance
- Traces para debugging

### 8.2 Patterns para Agentes

**Pattern 1: Plan-Act-Reflect**
```python
async def plan_act_reflect(task: Dict) -> Dict:
    """
    Padrão de 3 fases para execução de tarefas
    """
    # PLAN
    plan = await create_execution_plan(task)
    log_plan(plan)
    
    # ACT
    results = []
    for step in plan["steps"]:
        result = await execute_step(step)
        results.append(result)
        
        # Early exit on critical failure
        if result["status"] == "critical_error":
            break
    
    # REFLECT
    reflection = await analyze_results(results)
    improvements = await identify_improvements(reflection)
    
    return {
        "plan": plan,
        "results": results,
        "reflection": reflection,
        "improvements": improvements
    }
```

**Pattern 2: Chain of Responsibility**
```python
class Handler(ABC):
    """Handler base para chain of responsibility"""
    
    def __init__(self):
        self.next_handler = None
    
    def set_next(self, handler):
        self.next_handler = handler
        return handler
    
    @abstractmethod
    async def handle(self, request: Dict) -> Dict:
        pass

class ValidationHandler(Handler):
    async def handle(self, request: Dict) -> Dict:
        if not self.validate(request):
            return {"status": "error", "message": "Validation failed"}
        
        if self.next_handler:
            return await self.next_handler.handle(request)
        
        return {"status": "success"}

class ExecutionHandler(Handler):
    async def handle(self, request: Dict) -> Dict:
        result = await self.execute(request)
        
        if self.next_handler:
            return await self.next_handler.handle({**request, **result})
        
        return result

# Uso
validation = ValidationHandler()
execution = ExecutionHandler()
logging = LoggingHandler()

validation.set_next(execution).set_next(logging)

result = await validation.handle(task)
```

**Pattern 3: Observer para Monitoring**
```python
class Observable:
    """Subject que notifica observers"""
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        self._observers.append(observer)
    
    def detach(self, observer: Observer):
        self._observers.remove(observer)
    
    def notify(self, event: Dict):
        for observer in self._observers:
            observer.update(event)

class Observer(ABC):
    @abstractmethod
    def update(self, event: Dict):
        pass

class MetricsObserver(Observer):
    def update(self, event: Dict):
        # Atualizar métricas
        metrics.increment(event["type"])
        metrics.record_duration(event["duration"])

class LoggingObserver(Observer):
    def update(self, event: Dict):
        # Logar evento
        logger.info(f"Event: {event['type']}", extra=event)

# Uso
agent = CRUDAgent(repo_path)
agent.attach(MetricsObserver())
agent.attach(LoggingObserver())

# Quando agent executa, observadores são notificados
```

---

## 9. EXEMPLOS PRÁTICOS

### 9.1 Exemplo Completo: CRUD Agent com CLI

```python
# cli.py - Interface de linha de comando

import asyncio
import click
from agents.crud_agent import CRUDAgent

@click.group()
def cli():
    """CRUD Agent CLI"""
    pass

@cli.command()
@click.argument('path')
@click.option('--content', '-c', required=True, help='File content')
@click.option('--message', '-m', help='Commit message')
def create(path: str, content: str, message: str):
    """Create a new file"""
    agent = CRUDAgent(repo_path=".")
    
    task = {
        "operation": "create",
        "path": path,
        "content": content,
        "commit_msg": message
    }
    
    result = asyncio.run(agent.execute(task))
    
    if result["status"] == "success":
        click.echo(click.style(f"✅ {result['message']}", fg="green"))
    else:
        click.echo(click.style(f"❌ {result['message']}", fg="red"))

@cli.command()
@click.argument('path')
def read(path: str):
    """Read file content"""
    agent = CRUDAgent(repo_path=".")
    
    task = {
        "operation": "read",
        "path": path
    }
    
    result = asyncio.run(agent.execute(task))
    
    if result["status"] == "success":
        click.echo(click.style("📄 File content:", fg="blue"))
        click.echo(result["content"])
        click.echo(click.style(f"\n📊 Lines: {result['lines']}, Size: {result['size']} bytes", fg="cyan"))
    else:
        click.echo(click.style(f"❌ {result['message']}", fg="red"))

@cli.command()
@click.argument('path')
@click.option('--content', '-c', required=True, help='New content')
@click.option('--message', '-m', help='Commit message')
def update(path: str, content: str, message: str):
    """Update existing file"""
    agent = CRUDAgent(repo_path=".")
    
    task = {
        "operation": "update",
        "path": path,
        "content": content,
        "commit_msg": message
    }
    
    result = asyncio.run(agent.execute(task))
    
    if result["status"] == "success":
        click.echo(click.style(f"✅ {result['message']}", fg="green"))
        changes = result.get("changes", {})
        if changes:
            click.echo(click.style(f"📊 Changes: {changes}", fg="cyan"))
    else:
        click.echo(click.style(f"❌ {result['message']}", fg="red"))

@cli.command()
@click.argument('path')
@click.option('--force', is_flag=True, help='Force delete critical files')
@click.option('--message', '-m', help='Commit message')
def delete(path: str, force: bool, message: str):
    """Delete a file"""
    agent = CRUDAgent(repo_path=".")
    
    if not force:
        if not click.confirm(f"Are you sure you want to delete {path}?"):
            click.echo("Cancelled.")
            return
    
    task = {
        "operation": "delete",
        "path": path,
        "force": force,
        "commit_msg": message
    }
    
    result = asyncio.run(agent.execute(task))
    
    if result["status"] == "success":
        click.echo(click.style(f"✅ {result['message']}", fg="green"))
        if "backup_location" in result:
            click.echo(click.style(f"💾 Backup: {result['backup_location']}", fg="yellow"))
    elif result["status"] == "pending_confirmation":
        click.echo(click.style(f"⚠️  {result['message']}", fg="yellow"))
        click.echo("Use --force to confirm deletion of critical file")
    else:
        click.echo(click.style(f"❌ {result['message']}", fg="red"))

@cli.command()
def metrics():
    """Show agent metrics"""
    agent = CRUDAgent(repo_path=".")
    metrics = agent.get_metrics()
    
    click.echo(click.style("\n📊 Agent Metrics:", fg="blue", bold=True))
    click.echo(f"Agent: {metrics['agent']} v{metrics['version']}")
    click.echo(f"Total Executions: {metrics['total_executions']}")
    click.echo(f"Successful: {metrics['successful_executions']}")
    click.echo(f"Success Rate: {metrics['success_rate']:.2%}")
    click.echo(f"Avg Duration: {metrics['average_duration']:.3f}s")

if __name__ == '__main__':
    cli()
```

**Uso:**
```bash
# Criar arquivo
python cli.py create src/new_module.py --content "def hello(): pass" --message "feat: add new module"

# Ler arquivo
python cli.py read src/new_module.py

# Atualizar arquivo
python cli.py update src/new_module.py --content "def hello(): print('Hi')" --message "refactor: improve hello function"

# Deletar arquivo
python cli.py delete src/old_module.py --message "remove: delete deprecated module"

# Ver métricas
python cli.py metrics
```

### 9.2 Exemplo: Integration com GitHub API

```python
# integrations/github_crud.py

from github import Github, GithubException
from typing import Dict, Optional
import base64

class GitHubCRUDIntegration:
    """
    Integração com GitHub API para operações CRUD remotas
    """
    
    def __init__(self, token: str, repo_name: str):
        self.g = Github(token)
        self.repo = self.g.get_repo(repo_name)
        self.branch = "main"
    
    async def create_file(
        self,
        path: str,
        content: str,
        commit_message: str,
        branch: Optional[str] = None
    ) -> Dict:
        """Cria arquivo via GitHub API"""
        try:
            branch = branch or self.branch
            
            # Verificar se arquivo já existe
            try:
                self.repo.get_contents(path, ref=branch)
                return {
                    "status": "error",
                    "message": f"File {path} already exists on {branch}"
                }
            except GithubException as e:
                if e.status != 404:
                    raise
            
            # Criar arquivo
            result = self.repo.create_file(
                path=path,
                message=commit_message,
                content=content,
                branch=branch
            )
            
            return {
                "status": "success",
                "message": f"File {path} created successfully",
                "commit": {
                    "sha": result["commit"].sha,
                    "url": result["commit"].html_url
                },
                "content": {
                    "sha": result["content"].sha,
                    "url": result["content"].html_url
                }
            }
            
        except GithubException as e:
            return {
                "status": "error",
                "message": f"GitHub API error: {e.data.get('message', str(e))}"
            }
    
    async def read_file(self, path: str, branch: Optional[str] = None) -> Dict:
        """Lê arquivo via GitHub API"""
        try:
            branch = branch or self.branch
            
            file_content = self.repo.get_contents(path, ref=branch)
            
            if file_content.encoding == "base64":
                content = base64.b64decode(file_content.content).decode('utf-8')
            else:
                content = file_content.decoded_content.decode('utf-8')
            
            return {
                "status": "success",
                "path": path,
                "content": content,
                "size": file_content.size,
                "sha": file_content.sha,
                "url": file_content.html_url
            }
            
        except GithubException as e:
            if e.status == 404:
                return {
                    "status": "error",
                    "message": f"File {path} not found on {branch}"
                }
            return {
                "status": "error",
                "message": f"GitHub API error: {e.data.get('message', str(e))}"
            }
    
    async def update_file(
        self,
        path: str,
        new_content: str,
        commit_message: str,
        branch: Optional[str] = None
    ) -> Dict:
        """Atualiza arquivo via GitHub API"""
        try:
            branch = branch or self.branch
            
            # Obter SHA atual do arquivo
            file_content = self.repo.get_contents(path, ref=branch)
            
            # Atualizar arquivo
            result = self.repo.update_file(
                path=path,
                message=commit_message,
                content=new_content,
                sha=file_content.sha,
                branch=branch
            )
            
            return {
                "status": "success",
                "message": f"File {path} updated successfully",
                "commit": {
                    "sha": result["commit"].sha,
                    "url": result["commit"].html_url
                },
                "content": {
                    "sha": result["content"].sha,
                    "url": result["content"].html_url
                }
            }
            
        except GithubException as e:
            return {
                "status": "error",
                "message": f"GitHub API error: {e.data.get('message', str(e))}"
            }
    
    async def delete_file(
        self,
        path: str,
        commit_message: str,
        branch: Optional[str] = None
    ) -> Dict:
        """Deleta arquivo via GitHub API"""
        try:
            branch = branch or self.branch
            
            # Obter SHA atual do arquivo
            file_content = self.repo.get_contents(path, ref=branch)
            
            # Deletar arquivo
            result = self.repo.delete_file(
                path=path,
                message=commit_message,
                sha=file_content.sha,
                branch=branch
            )
            
            return {
                "status": "success",
                "message": f"File {path} deleted successfully",
                "commit": {
                    "sha": result["commit"].sha,
                    "url": result["commit"].html_url
                }
            }
            
        except GithubException as e:
            return {
                "status": "error",
                "message": f"GitHub API error: {e.data.get('message', str(e))}"
            }
    
    async def list_files(self, path: str = "", branch: Optional[str] = None) -> Dict:
        """Lista arquivos em um diretório"""
        try:
            branch = branch or self.branch
            
            contents = self.repo.get_contents(path, ref=branch)
            
            files = []
            for content in contents:
                files.append({
                    "name": content.name,
                    "path": content.path,
                    "type": content.type,
                    "size": content.size,
                    "sha": content.sha,
                    "url": content.html_url
                })
            
            return {
                "status": "success",
                "path": path,
                "files": files,
                "count": len(files)
            }
            
        except GithubException as e:
            return {
                "status": "error",
                "message": f"GitHub API error: {e.data.get('message', str(e))}"
            }
```

---

## 10. RECURSOS E REFERÊNCIAS

### 10.1 Repositórios GitHub Relevantes

**Agentes AI:**
- [NirDiamant/GenAI_Agents](https://github.com/NirDiamant/GenAI_Agents) - Tutoriais completos sobre agentes
- [microsoft/ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners) - 12 lições para iniciantes
- [ashishpatel26/500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects) - 500 casos de uso
- [ai-in-pm/CRUD-Agentic-System](https://github.com/ai-in-pm/CRUD-Agentic-System) - Sistema específico de CRUD com agentes

**Framework e Tools:**
- [panaversity/learn-agentic-ai](https://github.com/panaversity/learn-agentic-ai) - Agentic AI com Dapr e Kubernetes
- [jim-schwoebel/awesome_ai_agents](https://github.com/jim-schwoebel/awesome_ai_agents) - Lista de 1500+ recursos

### 10.2 Artigos e Documentação

**Best Practices:**
- [Builder.io - AGENTS.md Guide](https://www.builder.io/blog/agents-md)
- [Skywork AI - AGENTS.md Configuration](https://skywork.ai/blog/agent/agents-md-configuration-standardizing-ai-agent-instructions-across-teams/)
- [GitHub Blog - Onboarding AI Agents](https://github.blog/ai-and-ml/github-copilot/onboarding-your-ai-peer-programmer-setting-up-github-copilot-coding-agent-for-success/)

**Patterns e Workflows:**
- [Medium - Building with AI Coding Agents](https://medium.com/@elisheba.t.anderson/building-with-ai-coding-agents-best-practices-for-agent-workflows-be1d7095901b)
- [Medium - AI Agent for README files](https://medium.com/@filipespacheco/i-created-an-ai-agent-to-build-readme-files-here-is-what-i-learn-3ae207771d37)

**Tools e Platforms:**
- [Azure AI - File Search Tool](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/file-search)
- [Factory.ai - AGENTS.md Documentation](https://docs.factory.ai/cli/configuration/agents-md)

### 10.3 Padrões de Arquivo de Configuração

**Arquivos Suportados por Diferentes Tools:**
- `AGENTS.md` - Universal (Codex, Factory, etc.)
- `CLAUDE.md` - Claude Code specific
- `copilot-instructions.md` - GitHub Copilot
- `.junie/guidelines.md` - JetBrains Junie
- `TEAM_GUIDE.md` - Team conventions

### 10.4 Checklists Úteis

**Checklist: Criar Novo Agente**
- [ ] Herdar de `BaseAgent`
- [ ] Implementar método `execute()`
- [ ] Adicionar validação de entrada
- [ ] Implementar error handling
- [ ] Adicionar logging
- [ ] Escrever testes unitários
- [ ] Documentar no README
- [ ] Adicionar ao registry de agentes

**Checklist: Configurar Repositório para Agentes**
- [ ] Criar `AGENTS.md` na raiz
- [ ] Definir estrutura de pastas clara
- [ ] Adicionar `CONTRIBUTING.md`
- [ ] Configurar CI/CD
- [ ] Adicionar pre-commit hooks
- [ ] Documentar arquitetura
- [ ] Definir naming conventions
- [ ] Estabelecer branching strategy

**Checklist: Operação CRUD Segura**
- [ ] Validar permissões
- [ ] Verificar se arquivo existe (create/read/update/delete)
- [ ] Fazer backup (update/delete)
- [ ] Validar conteúdo/sintaxe
- [ ] Usar mensagens de commit descritivas
- [ ] Logar operação
- [ ] Confirmar com usuário (operações destrutivas)
- [ ] Testar em dry-run primeiro

---

## 📝 CONCLUSÃO

Este guia compilou conhecimento de múltiplas fontes para fornecer um recurso completo sobre:

1. **Organização de Repositórios**: Estruturas claras e escaláveis
2. **README Profissional**: Templates e melhores práticas
3. **CRUD Operations**: Implementação segura e robusta
4. **Ensino de Agentes**: Como documentar e instruir agentes AI
5. **Framework LCM-AI**: Sistema completo de gestão de conhecimento
6. **Padrões e Práticas**: Patterns testados em produção

**Próximos Passos Sugeridos:**
1. Adaptar templates para seu contexto específico
2. Implementar agente CRUD básico
3. Criar arquivo AGENTS.md para seu repositório
4. Testar em ambiente de desenvolvimento
5. Iterar baseado em feedback

**Lembre-se:**
- Começar simples, evoluir gradualmente
- Documentar tudo claramente
- Validar inputs sempre
- Fazer backup de operações destrutivas
- Medir e monitorar resultados

---

**Mantido por:** Sistema LCM-AI  
**Última atualização:** 2025-11-11  
**Versão:** 1.0.0

[⬆ Voltar ao topo](#guia-completo-agentes-ai-crud-e-organização-de-repositórios)
