# 💻 CÓDIGO PRONTO: CRUD Agent Completo

> **Copy & Paste Ready**: Código funcional para implementar agente CRUD

---

## 📦 Estrutura do Projeto

```
crud-agent/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   └── crud_agent.py
├── skills/
│   ├── __init__.py
│   └── file_operations.py
├── utils/
│   ├── __init__.py
│   ├── logger.py
│   └── git_helper.py
├── tests/
│   ├── test_crud_agent.py
│   └── test_file_operations.py
├── cli.py
├── requirements.txt
├── AGENTS.md
└── README.md
```

---

## 📄 requirements.txt

```txt
# Core
python>=3.10
click>=8.1.0
pydantic>=2.0.0

# Git
gitpython>=3.1.0

# GitHub API (opcional)
PyGithub>=2.1.0

# Logging
colorlog>=6.7.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
```

---

## 🛠️ utils/logger.py

```python
"""
Configuração de logging para o sistema
"""

import logging
import colorlog
from pathlib import Path

def setup_logger(name: str, log_file: str = "agent.log", level=logging.INFO):
    """
    Configura logger com cores e arquivo
    
    Args:
        name: Nome do logger
        log_file: Arquivo de log
        level: Nível de logging
        
    Returns:
        Logger configurado
    """
    # Criar diretório de logs
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configurar formatters
    console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(name)s%(reset)s - %(message)s",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Handler para console
    console_handler = colorlog.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(level)
    
    # Handler para arquivo
    file_handler = logging.FileHandler(log_dir / log_file)
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    
    # Configurar logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger
```

---

## 🛠️ utils/git-helper.py

```python
"""
Helpers para operações Git
"""

import subprocess
from pathlib import Path
from typing import Optional, List
from utils.logger import setup_logger

logger = setup_logger('git_helper')

class GitHelper:
    """Helper para operações Git"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self._verify_git_repo()
    
    def _verify_git_repo(self):
        """Verifica se é um repositório Git válido"""
        git_dir = self.repo_path / ".git"
        if not git_dir.exists():
            raise ValueError(f"{self.repo_path} não é um repositório Git válido")
    
    def _run_command(self, cmd: List[str]) -> subprocess.CompletedProcess:
        """Executa comando Git"""
        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            logger.debug(f"Git command: {' '.join(cmd)}")
            return result
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed: {e.stderr}")
            raise
    
    def add(self, path: str) -> bool:
        """Git add"""
        try:
            self._run_command(['git', 'add', path])
            logger.info(f"Added to git: {path}")
            return True
        except subprocess.CalledProcessError:
            return False
    
    def commit(self, message: str) -> Optional[str]:
        """Git commit"""
        try:
            result = self._run_command(['git', 'commit', '-m', message])
            # Extrair SHA do commit
            output = result.stdout
            if 'nothing to commit' in output:
                logger.warning("Nothing to commit")
                return None
            
            # SHA está na primeira linha
            sha = output.split()[1].strip('[]')
            logger.info(f"Committed: {sha[:7]} - {message}")
            return sha
        except subprocess.CalledProcessError:
            return None
    
    def status(self) -> str:
        """Git status"""
        result = self._run_command(['git', 'status', '--short'])
        return result.stdout
    
    def diff(self, path: str) -> str:
        """Git diff para um arquivo"""
        result = self._run_command(['git', 'diff', path])
        return result.stdout
    
    def log(self, n: int = 5) -> str:
        """Últimos N commits"""
        result = self._run_command([
            'git', 'log', 
            f'-{n}', 
            '--oneline', 
            '--decorate'
        ])
        return result.stdout
    
    def get_current_branch(self) -> str:
        """Obtém branch atual"""
        result = self._run_command(['git', 'branch', '--show-current'])
        return result.stdout.strip()
```

---

## 🧩 agents/base_agent.py

```python
"""
Classe base para todos os agentes
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime
from utils.logger import setup_logger

class BaseAgent(ABC):
    """
    Classe base abstrata para agentes
    
    Todos os agentes devem herdar desta classe e implementar
    o método execute()
    """
    
    def __init__(self, name: str, version: str, config: Dict[str, Any]):
        """
        Inicializa agente
        
        Args:
            name: Nome do agente
            version: Versão do agente
            config: Configuração do agente
        """
        self.name = name
        self.version = version
        self.config = config
        self.logger = setup_logger(f"agent.{name}")
        self.execution_history: List[Dict] = []
        
        self.logger.info(f"Initialized {name} v{version}")
    
    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Método principal de execução do agente
        
        Args:
            task: Dicionário com informações da tarefa
            
        Returns:
            Resultado da execução com formato:
            {
                "status": "success|error|pending_confirmation",
                "message": "Mensagem descritiva",
                "data": {...}  # Dados específicos
            }
        """
        pass
    
    def log_execution(
        self, 
        task: Dict, 
        result: Dict, 
        duration: float
    ):
        """
        Registra execução para auditoria
        
        Args:
            task: Tarefa executada
            result: Resultado da execução
            duration: Duração em segundos
        """
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
        
        # Log com nível apropriado
        if execution_record["success"]:
            self.logger.info(
                f"Execution completed: {task.get('operation', 'unknown')}",
                extra=execution_record
            )
        else:
            self.logger.error(
                f"Execution failed: {result.get('message', 'unknown error')}",
                extra=execution_record
            )
    
    async def validate_input(self, task: Dict) -> tuple[bool, str]:
        """
        Valida entrada antes de processar
        
        Args:
            task: Tarefa a validar
            
        Returns:
            Tupla (válido, mensagem_erro)
        """
        required_fields = self.config.get("required_fields", [])
        
        for field in required_fields:
            if field not in task:
                msg = f"Missing required field: {field}"
                self.logger.error(msg)
                return False, msg
        
        return True, ""
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Retorna métricas do agente
        
        Returns:
            Dicionário com métricas
        """
        total = len(self.execution_history)
        successful = sum(1 for ex in self.execution_history if ex["success"])
        failed = total - successful
        
        avg_duration = (
            sum(ex["duration_seconds"] for ex in self.execution_history) / total
            if total > 0 else 0
        )
        
        return {
            "agent": self.name,
            "version": self.version,
            "metrics": {
                "total_executions": total,
                "successful": successful,
                "failed": failed,
                "success_rate": successful / total if total > 0 else 0,
                "average_duration_seconds": round(avg_duration, 3)
            },
            "last_execution": (
                self.execution_history[-1]["timestamp"] 
                if self.execution_history 
                else None
            )
        }
    
    def clear_history(self):
        """Limpa histórico de execuções"""
        self.execution_history = []
        self.logger.info("Execution history cleared")
```

---

## 🧩 skills/file_operations.py

```python
"""
Skill para operações de arquivo com validações e segurança
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List
from utils.logger import setup_logger
from utils.git_helper import GitHelper

class FileOperationsSkill:
    """
    Skill para operações CRUD de arquivos com validações
    """
    
    # Arquivos que nunca devem ser deletados sem confirmação explícita
    CRITICAL_FILES = [
        'README.md',
        'LICENSE',
        '.gitignore',
        'package.json',
        'requirements.txt',
        'setup.py',
        'pyproject.toml'
    ]
    
    def __init__(self, repo_path: str = "."):
        """
        Inicializa skill
        
        Args:
            repo_path: Caminho do repositório
        """
        self.repo_path = Path(repo_path)
        self.git = GitHelper(repo_path)
        self.logger = setup_logger('file_operations')
        
        # Criar diretório de backups
        self.backup_dir = self.repo_path / ".backups"
        self.backup_dir.mkdir(exist_ok=True)
    
    def _is_critical_file(self, path: str) -> bool:
        """Verifica se é arquivo crítico"""
        filename = os.path.basename(path)
        return filename in self.CRITICAL_FILES
    
    def _make_backup(self, path: str) -> str:
        """Cria backup de um arquivo"""
        source = self.repo_path / path
        
        if not source.exists():
            raise FileNotFoundError(f"File {path} not found for backup")
        
        # Nome do backup com timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{source.name}.{timestamp}.backup"
        backup_path = self.backup_dir / backup_name
        
        shutil.copy2(source, backup_path)
        self.logger.info(f"Backup created: {backup_path}")
        
        return str(backup_path)
    
    def create(
        self, 
        path: str, 
        content: str, 
        commit_msg: str = None
    ) -> Dict:
        """
        Cria um novo arquivo
        
        Args:
            path: Caminho do arquivo
            content: Conteúdo do arquivo
            commit_msg: Mensagem de commit (opcional)
            
        Returns:
            Resultado da operação
        """
        full_path = self.repo_path / path
        
        # Validar se arquivo já existe
        if full_path.exists():
            return {
                "status": "error",
                "operation": "create",
                "file_path": path,
                "message": f"File {path} already exists. Use update() to modify."
            }
        
        try:
            # Criar diretórios se necessário
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Criar arquivo
            full_path.write_text(content, encoding='utf-8')
            
            # Git operations
            self.git.add(path)
            commit_msg = commit_msg or f"feat: add {path}"
            commit_sha = self.git.commit(commit_msg)
            
            self.logger.info(f"Created file: {path}")
            
            return {
                "status": "success",
                "operation": "create",
                "file_path": path,
                "message": f"File {path} created successfully",
                "details": {
                    "size": len(content),
                    "lines": content.count('\n') + 1,
                    "commit_sha": commit_sha
                }
            }
            
        except Exception as e:
            self.logger.exception(f"Error creating file {path}")
            return {
                "status": "error",
                "operation": "create",
                "file_path": path,
                "message": f"Failed to create file: {str(e)}"
            }
    
    def read(self, path: str) -> Dict:
        """
        Lê conteúdo de um arquivo
        
        Args:
            path: Caminho do arquivo
            
        Returns:
            Resultado com conteúdo do arquivo
        """
        full_path = self.repo_path / path
        
        if not full_path.exists():
            return {
                "status": "error",
                "operation": "read",
                "file_path": path,
                "message": f"File {path} not found"
            }
        
        try:
            content = full_path.read_text(encoding='utf-8')
            
            self.logger.info(f"Read file: {path}")
            
            return {
                "status": "success",
                "operation": "read",
                "file_path": path,
                "content": content,
                "details": {
                    "size": len(content),
                    "lines": content.count('\n') + 1,
                    "encoding": "utf-8"
                }
            }
            
        except Exception as e:
            self.logger.exception(f"Error reading file {path}")
            return {
                "status": "error",
                "operation": "read",
                "file_path": path,
                "message": f"Failed to read file: {str(e)}"
            }
    
    def update(
        self, 
        path: str, 
        new_content: str, 
        commit_msg: str = None
    ) -> Dict:
        """
        Atualiza arquivo existente
        
        Args:
            path: Caminho do arquivo
            new_content: Novo conteúdo
            commit_msg: Mensagem de commit (opcional)
            
        Returns:
            Resultado da operação
        """
        full_path = self.repo_path / path
        
        if not full_path.exists():
            return {
                "status": "error",
                "operation": "update",
                "file_path": path,
                "message": f"File {path} not found. Use create() for new file."
            }
        
        try:
            # Ler conteúdo antigo e fazer backup
            old_content = full_path.read_text(encoding='utf-8')
            backup_path = self._make_backup(path)
            
            # Atualizar arquivo
            full_path.write_text(new_content, encoding='utf-8')
            
            # Git operations
            self.git.add(path)
            commit_msg = commit_msg or f"refactor: update {path}"
            commit_sha = self.git.commit(commit_msg)
            
            self.logger.info(f"Updated file: {path}")
            
            # Calcular mudanças
            old_lines = old_content.count('\n') + 1
            new_lines = new_content.count('\n') + 1
            
            return {
                "status": "success",
                "operation": "update",
                "file_path": path,
                "message": f"File {path} updated successfully",
                "details": {
                    "old_size": len(old_content),
                    "new_size": len(new_content),
                    "old_lines": old_lines,
                    "new_lines": new_lines,
                    "lines_added": max(0, new_lines - old_lines),
                    "lines_removed": max(0, old_lines - new_lines),
                    "backup_path": backup_path,
                    "commit_sha": commit_sha
                }
            }
            
        except Exception as e:
            self.logger.exception(f"Error updating file {path}")
            return {
                "status": "error",
                "operation": "update",
                "file_path": path,
                "message": f"Failed to update file: {str(e)}"
            }
    
    def delete(
        self, 
        path: str, 
        commit_msg: str = None, 
        force: bool = False
    ) -> Dict:
        """
        Deleta arquivo com proteções
        
        Args:
            path: Caminho do arquivo
            commit_msg: Mensagem de commit (opcional)
            force: Forçar deleção de arquivos críticos
            
        Returns:
            Resultado da operação
        """
        # Verificar se é arquivo crítico
        if self._is_critical_file(path) and not force:
            return {
                "status": "pending_confirmation",
                "operation": "delete",
                "file_path": path,
                "message": f"⚠️ {path} is a critical file. Use force=True to confirm deletion.",
                "is_critical": True
            }
        
        full_path = self.repo_path / path
        
        if not full_path.exists():
            return {
                "status": "error",
                "operation": "delete",
                "file_path": path,
                "message": f"File {path} not found"
            }
        
        try:
            # Fazer backup antes de deletar
            backup_path = self._make_backup(path)
            
            # Deletar arquivo
            full_path.unlink()
            
            # Git operations
            self.git.add(path)  # Git add do arquivo removido
            commit_msg = commit_msg or f"remove: delete {path}"
            commit_sha = self.git.commit(commit_msg)
            
            self.logger.warning(
                f"Deleted file: {path} (backup at {backup_path})"
            )
            
            return {
                "status": "success",
                "operation": "delete",
                "file_path": path,
                "message": f"File {path} deleted successfully",
                "details": {
                    "backup_path": backup_path,
                    "commit_sha": commit_sha,
                    "was_critical": self._is_critical_file(path)
                }
            }
            
        except Exception as e:
            self.logger.exception(f"Error deleting file {path}")
            return {
                "status": "error",
                "operation": "delete",
                "file_path": path,
                "message": f"Failed to delete file: {str(e)}"
            }
    
    def list_files(self, directory: str = "", pattern: str = "*") -> Dict:
        """
        Lista arquivos em um diretório
        
        Args:
            directory: Diretório a listar (vazio = raiz)
            pattern: Padrão glob (ex: "*.py")
            
        Returns:
            Lista de arquivos
        """
        dir_path = self.repo_path / directory if directory else self.repo_path
        
        if not dir_path.exists():
            return {
                "status": "error",
                "operation": "list",
                "message": f"Directory {directory} not found"
            }
        
        try:
            files = []
            for item in dir_path.glob(pattern):
                if item.is_file():
                    rel_path = item.relative_to(self.repo_path)
                    stat = item.stat()
                    
                    files.append({
                        "path": str(rel_path),
                        "name": item.name,
                        "size": stat.st_size,
                        "is_critical": self._is_critical_file(str(rel_path))
                    })
            
            return {
                "status": "success",
                "operation": "list",
                "directory": directory or ".",
                "pattern": pattern,
                "files": files,
                "count": len(files)
            }
            
        except Exception as e:
            self.logger.exception(f"Error listing files in {directory}")
            return {
                "status": "error",
                "operation": "list",
                "message": f"Failed to list files: {str(e)}"
            }
```

---

## 🤖 agents/crud_agent.py

```python
"""
Agente especializado em operações CRUD
"""

import time
from typing import Dict, Any
from agents.base_agent import BaseAgent
from skills.file_operations import FileOperationsSkill

class CRUDAgent(BaseAgent):
    """
    Agente CRUD - Gerencia operações Create, Read, Update, Delete
    
    Task format:
    {
        "operation": "create|read|update|delete|list",
        "path": "path/to/file",
        "content": "...",  # Para create/update
        "commit_msg": "...",  # Opcional
        "force": False,  # Para delete de arquivos críticos
        "directory": "...",  # Para list
        "pattern": "*.py"  # Para list
    }
    """
    
    def __init__(self, repo_path: str = "."):
        """
        Inicializa CRUD Agent
        
        Args:
            repo_path: Caminho do repositório
        """
        config = {
            "required_fields": ["operation"],
            "allowed_operations": ["create", "read", "update", "delete", "list"]
        }
        
        super().__init__(
            name="crud_agent",
            version="1.0.0",
            config=config
        )
        
        self.file_ops = FileOperationsSkill(repo_path)
        self.logger.info(f"CRUD Agent initialized for repo: {repo_path}")
    
    async def validate_input(self, task: Dict) -> tuple[bool, str]:
        """Validação específica do CRUD Agent"""
        # Validação base
        valid, msg = await super().validate_input(task)
        if not valid:
            return False, msg
        
        # Validar operação
        operation = task.get("operation")
        allowed = self.config["allowed_operations"]
        
        if operation not in allowed:
            return False, f"Invalid operation: {operation}. Allowed: {allowed}"
        
        # Validar campos específicos por operação
        if operation in ["create", "read", "update", "delete"]:
            if "path" not in task:
                return False, f"Operation {operation} requires 'path' field"
        
        if operation in ["create", "update"]:
            if "content" not in task:
                return False, f"Operation {operation} requires 'content' field"
        
        return True, ""
    
    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executa operação CRUD
        
        Args:
            task: Dicionário com detalhes da tarefa
            
        Returns:
            Resultado da operação
        """
        start_time = time.time()
        
        # Validar entrada
        valid, error_msg = await self.validate_input(task)
        if not valid:
            result = {
                "status": "error",
                "message": error_msg
            }
            self.log_execution(task, result, time.time() - start_time)
            return result
        
        operation = task["operation"]
        
        try:
            # Executar operação apropriada
            if operation == "create":
                result = self.file_ops.create(
                    path=task["path"],
                    content=task["content"],
                    commit_msg=task.get("commit_msg")
                )
            
            elif operation == "read":
                result = self.file_ops.read(
                    path=task["path"]
                )
            
            elif operation == "update":
                result = self.file_ops.update(
                    path=task["path"],
                    new_content=task["content"],
                    commit_msg=task.get("commit_msg")
                )
            
            elif operation == "delete":
                result = self.file_ops.delete(
                    path=task["path"],
                    commit_msg=task.get("commit_msg"),
                    force=task.get("force", False)
                )
            
            elif operation == "list":
                result = self.file_ops.list_files(
                    directory=task.get("directory", ""),
                    pattern=task.get("pattern", "*")
                )
            
            else:
                result = {
                    "status": "error",
                    "message": f"Unknown operation: {operation}"
                }
        
        except Exception as e:
            self.logger.exception(f"Unexpected error in operation {operation}")
            result = {
                "status": "error",
                "operation": operation,
                "message": f"Unexpected error: {str(e)}"
            }
        
        # Logar execução
        duration = time.time() - start_time
        self.log_execution(task, result, duration)
        
        return result
```

---

## 💻 cli.py

```python
"""
Interface de linha de comando para o CRUD Agent
"""

import asyncio
import click
import json
from pathlib import Path
from agents.crud_agent import CRUDAgent

# Cores para output
def success(msg): return click.style(msg, fg="green")
def error(msg): return click.style(msg, fg="red")
def warning(msg): return click.style(msg, fg="yellow")
def info(msg): return click.style(msg, fg="cyan")
def bold(msg): return click.style(msg, bold=True)

@click.group()
@click.option('--repo', default=".", help='Repository path')
@click.pass_context
def cli(ctx, repo):
    """CRUD Agent CLI - Manage files with AI assistance"""
    ctx.ensure_object(dict)
    ctx.obj['repo'] = repo
    ctx.obj['agent'] = CRUDAgent(repo)

@cli.command()
@click.argument('path')
@click.option('--content', '-c', help='File content')
@click.option('--file', '-f', type=click.Path(exists=True), help='Read content from file')
@click.option('--message', '-m', help='Commit message')
@click.pass_context
def create(ctx, path, content, file, message):
    """Create a new file"""
    agent = ctx.obj['agent']
    
    # Obter conteúdo
    if file:
        content = Path(file).read_text()
    elif not content:
        click.echo(error("Error: Must provide --content or --file"))
        return
    
    # Executar
    task = {
        "operation": "create",
        "path": path,
        "content": content,
        "commit_msg": message
    }
    
    result = asyncio.run(agent.execute(task))
    
    # Output
    if result["status"] == "success":
        click.echo(success(f"✅ {result['message']}"))
        details = result.get('details', {})
        if details:
            click.echo(info(f"   Size: {details.get('size')} bytes"))
            click.echo(info(f"   Lines: {details.get('lines')}"))
            click.echo(info(f"   Commit: {details.get('commit_sha', 'N/A')[:7]}"))
    else:
        click.echo(error(f"❌ {result['message']}"))

@cli.command()
@click.argument('path')
@click.option('--output', '-o', type=click.Path(), help='Save to file')
@click.pass_context
def read(ctx, path, output):
    """Read file content"""
    agent = ctx.obj['agent']
    
    task = {
        "operation": "read",
        "path": path
    }
    
    result = asyncio.run(agent.execute(task))
    
    if result["status"] == "success":
        content = result["content"]
        
        if output:
            Path(output).write_text(content)
            click.echo(success(f"✅ Content saved to {output}"))
        else:
            click.echo(info(f"📄 {bold(path)}"))
            click.echo("-" * 50)
            click.echo(content)
            click.echo("-" * 50)
        
        details = result.get('details', {})
        click.echo(info(f"📊 Lines: {details.get('lines')}, Size: {details.get('size')} bytes"))
    else:
        click.echo(error(f"❌ {result['message']}"))

@cli.command()
@click.argument('path')
@click.option('--content', '-c', help='New content')
@click.option('--file', '-f', type=click.Path(exists=True), help='Read content from file')
@click.option('--message', '-m', help='Commit message')
@click.pass_context
def update(ctx, path, content, file, message):
    """Update existing file"""
    agent = ctx.obj['agent']
    
    # Obter conteúdo
    if file:
        content = Path(file).read_text()
    elif not content:
        click.echo(error("Error: Must provide --content or --file"))
        return
    
    task = {
        "operation": "update",
        "path": path,
        "content": content,
        "commit_msg": message
    }
    
    result = asyncio.run(agent.execute(task))
    
    if result["status"] == "success":
        click.echo(success(f"✅ {result['message']}"))
        details = result.get('details', {})
        if details:
            click.echo(info(f"   Lines: {details.get('old_lines')} → {details.get('new_lines')}"))
            click.echo(info(f"   Added: +{details.get('lines_added')}, Removed: -{details.get('lines_removed')}"))
            click.echo(info(f"   Backup: {details.get('backup_path')}"))
    else:
        click.echo(error(f"❌ {result['message']}"))

@cli.command()
@click.argument('path')
@click.option('--force', is_flag=True, help='Force delete critical files')
@click.option('--message', '-m', help='Commit message')
@click.pass_context
def delete(ctx, path, force, message):
    """Delete a file"""
    agent = ctx.obj['agent']
    
    # Confirmar com usuário
    if not force:
        if not click.confirm(f"⚠️  Delete {path}?"):
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
        click.echo(success(f"✅ {result['message']}"))
        details = result.get('details', {})
        if details.get('backup_path'):
            click.echo(warning(f"💾 Backup: {details['backup_path']}"))
    elif result["status"] == "pending_confirmation":
        click.echo(warning(f"⚠️  {result['message']}"))
        click.echo("Use --force to confirm deletion of critical file")
    else:
        click.echo(error(f"❌ {result['message']}"))

@cli.command()
@click.option('--directory', '-d', default="", help='Directory to list')
@click.option('--pattern', '-p', default="*", help='File pattern (e.g., *.py)')
@click.pass_context
def list(ctx, directory, pattern):
    """List files in directory"""
    agent = ctx.obj['agent']
    
    task = {
        "operation": "list",
        "directory": directory,
        "pattern": pattern
    }
    
    result = asyncio.run(agent.execute(task))
    
    if result["status"] == "success":
        files = result.get('files', [])
        
        click.echo(info(f"\n📁 {bold(result['directory'])} ({result['count']} files matching '{pattern}')"))
        click.echo("-" * 70)
        
        for f in files:
            critical = " 🔒" if f['is_critical'] else ""
            size_kb = f['size'] / 1024
            click.echo(f"  {f['path']:<50} {size_kb:>8.2f} KB{critical}")
        
        click.echo("-" * 70)
    else:
        click.echo(error(f"❌ {result['message']}"))

@cli.command()
@click.pass_context
def metrics(ctx):
    """Show agent metrics"""
    agent = ctx.obj['agent']
    metrics = agent.get_metrics()
    
    click.echo(info(f"\n📊 {bold('Agent Metrics')}"))
    click.echo("-" * 50)
    click.echo(f"Agent: {metrics['agent']} v{metrics['version']}")
    
    m = metrics['metrics']
    click.echo(f"Total Executions: {m['total_executions']}")
    click.echo(success(f"Successful: {m['successful']}"))
    click.echo(error(f"Failed: {m['failed']}"))
    click.echo(f"Success Rate: {m['success_rate']:.1%}")
    click.echo(f"Avg Duration: {m['average_duration_seconds']:.3f}s")
    
    if metrics['last_execution']:
        click.echo(f"Last Execution: {metrics['last_execution']}")
    click.echo("-" * 50)

@cli.command()
@click.option('--output', '-o', default='agent_report.json', help='Output file')
@click.pass_context
def report(ctx, output):
    """Generate execution report"""
    agent = ctx.obj['agent']
    
    report = {
        "metrics": agent.get_metrics(),
        "execution_history": agent.execution_history
    }
    
    with open(output, 'w') as f:
        json.dump(report, f, indent=2)
    
    click.echo(success(f"✅ Report saved to {output}"))

if __name__ == '__main__':
    cli(obj={})
```

---

## 🧪 tests/test_crud_agent.py

```python
"""
Testes para CRUD Agent
"""

import pytest
from pathlib import Path
from agents.crud_agent import CRUDAgent

@pytest.fixture
def temp_repo(tmp_path):
    """Cria repositório temporário para testes"""
    repo = tmp_path / "test_repo"
    repo.mkdir()
    
    # Inicializar git
    import subprocess
    subprocess.run(['git', 'init'], cwd=repo, capture_output=True)
    subprocess.run(['git', 'config', 'user.name', 'Test'], cwd=repo)
    subprocess.run(['git', 'config', 'user.email', 'test@test.com'], cwd=repo)
    
    return repo

@pytest.fixture
def agent(temp_repo):
    """Cria agente para testes"""
    return CRUDAgent(str(temp_repo))

@pytest.mark.asyncio
async def test_create_file(agent, temp_repo):
    """Testa criação de arquivo"""
    task = {
        "operation": "create",
        "path": "test.txt",
        "content": "Hello, World!",
        "commit_msg": "test: add test file"
    }
    
    result = await agent.execute(task)
    
    assert result["status"] == "success"
    assert result["operation"] == "create"
    assert (temp_repo / "test.txt").exists()

@pytest.mark.asyncio
async def test_create_existing_file_fails(agent, temp_repo):
    """Testa que criar arquivo existente falha"""
    # Criar arquivo primeiro
    (temp_repo / "existing.txt").write_text("exists")
    
    task = {
        "operation": "create",
        "path": "existing.txt",
        "content": "new content"
    }
    
    result = await agent.execute(task)
    
    assert result["status"] == "error"
    assert "already exists" in result["message"].lower()

@pytest.mark.asyncio
async def test_read_file(agent, temp_repo):
    """Testa leitura de arquivo"""
    # Criar arquivo
    content = "Test content"
    (temp_repo / "read.txt").write_text(content)
    
    task = {
        "operation": "read",
        "path": "read.txt"
    }
    
    result = await agent.execute(task)
    
    assert result["status"] == "success"
    assert result["content"] == content

@pytest.mark.asyncio
async def test_update_file(agent, temp_repo):
    """Testa atualização de arquivo"""
    # Criar arquivo inicial
    path = temp_repo / "update.txt"
    path.write_text("original")
    
    task = {
        "operation": "update",
        "path": "update.txt",
        "content": "updated content"
    }
    
    result = await agent.execute(task)
    
    assert result["status"] == "success"
    assert path.read_text() == "updated content"
    assert "backup_path" in result["details"]

@pytest.mark.asyncio
async def test_delete_file(agent, temp_repo):
    """Testa deleção de arquivo"""
    # Criar arquivo
    path = temp_repo / "delete.txt"
    path.write_text("to be deleted")
    
    task = {
        "operation": "delete",
        "path": "delete.txt",
        "force": True  # Force para não precisar confirmar
    }
    
    result = await agent.execute(task)
    
    assert result["status"] == "success"
    assert not path.exists()
    assert "backup_path" in result["details"]

@pytest.mark.asyncio
async def test_delete_critical_file_requires_force(agent, temp_repo):
    """Testa que arquivos críticos requerem force=True"""
    # Criar arquivo crítico
    (temp_repo / "README.md").write_text("important")
    
    task = {
        "operation": "delete",
        "path": "README.md",
        "force": False
    }
    
    result = await agent.execute(task)
    
    assert result["status"] == "pending_confirmation"
    assert "critical" in result["message"].lower()

@pytest.mark.asyncio
async def test_invalid_operation(agent):
    """Testa operação inválida"""
    task = {
        "operation": "invalid_op",
        "path": "test.txt"
    }
    
    result = await agent.execute(task)
    
    assert result["status"] == "error"
    assert "invalid operation" in result["message"].lower()

@pytest.mark.asyncio
async def test_agent_metrics(agent, temp_repo):
    """Testa métricas do agente"""
    # Executar algumas operações
    await agent.execute({
        "operation": "create",
        "path": "test1.txt",
        "content": "test"
    })
    
    await agent.execute({
        "operation": "read",
        "path": "test1.txt"
    })
    
    metrics = agent.get_metrics()
    
    assert metrics["agent"] == "crud_agent"
    assert metrics["metrics"]["total_executions"] >= 2
    assert metrics["metrics"]["success_rate"] > 0
```

---

## 📖 README.md

```markdown
# 🤖 CRUD Agent

> AI-powered file operations with safety guardrails and Git integration

## ✨ Features

- ✅ **CRUD Operations**: Create, Read, Update, Delete files
- 🛡️ **Safety Guardrails**: Protection for critical files
- 📦 **Automatic Backups**: Before any destructive operation
- 🔄 **Git Integration**: Automatic commits with descriptive messages
- 📊 **Metrics & Logging**: Track all operations
- 🎯 **CLI Interface**: Easy command-line usage

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Usage

```bash
# Create file
python cli.py create src/new.py --content "def hello(): pass"

# Read file
python cli.py read src/new.py

# Update file
python cli.py update src/new.py --content "def hello(): print('Hi')"

# Delete file
python cli.py delete src/old.py --force

# List files
python cli.py list --directory src --pattern "*.py"

# View metrics
python cli.py metrics
```

## 📦 Project Structure

```
crud-agent/
├── agents/           # Agent implementations
├── skills/           # Specialized skills
├── utils/            # Utilities
├── tests/            # Tests
├── cli.py            # CLI interface
└── requirements.txt
```

## 🧪 Testing

```bash
pytest tests/ -v
```

## 📝 License

MIT
```

---

## ⚙️ AGENTS.md

```markdown
# AGENTS.md

## Project: CRUD Agent

AI-powered file operations system with safety guardrails.

## Tech Stack

- Python 3.10+
- GitPython
- Click (CLI)
- Pytest

## Commands

```bash
# Install
pip install -r requirements.txt

# Test
pytest tests/ -v

# Run
python cli.py --help

# Format
black .

# Lint
flake8 .
```

## Architecture

```
agents/
├── base_agent.py     # Base agent class
└── crud_agent.py     # CRUD implementation

skills/
└── file_operations.py  # File ops skill

utils/
├── logger.py         # Logging setup
└── git_helper.py     # Git operations
```

## Conventions

- Classes: `PascalCase`
- Functions: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private: prefix with `_`

## Safety Rules

### Never Delete Without Confirmation

Critical files:
- README.md
- LICENSE
- .gitignore
- package.json
- requirements.txt

### Always Backup

Before:
- Update operations
- Delete operations

## Git Workflow

```bash
# Feature branch
git checkout -b feature/description

# Commit
git commit -m "feat: description"

# Types: feat, fix, refactor, docs, test
```

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=agents --cov=skills

# Specific test
pytest tests/test_crud_agent.py -k test_create
```
```

---

**Pronto para uso!** 🎉

Copie os arquivos acima e você terá um **CRUD Agent completamente funcional** com:

✅ Operações CRUD seguras  
✅ Integração Git automática  
✅ Proteção de arquivos críticos  
✅ Backups automáticos  
✅ CLI completo  
✅ Testes  
✅ Logging e métricas  
✅ Documentação

[📖 Ver Guia Completo](./GUIA_COMPLETO_AGENTES_CRUD_REPOSITORIOS.md)
