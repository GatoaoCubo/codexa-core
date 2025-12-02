# Pattern: Terminal Commands

**Categoria**: Universal (Obrigatorio)
**Frequencia**: 84% das ferramentas analisadas
**Ultima Atualizacao**: 2025-12-02
**Quality Score**: 0.87

## Resumo Executivo

Terminal commands permitem que AI assistants executem operacoes de sistema. As implementacoes variam em controle de sessao, timeout, e execucao em background.

## Implementacoes por Ferramenta

### Claude Code (Anthropic)
**Abordagem**: Bash tool com timeout e background
```json
{
  "name": "Bash",
  "parameters": {
    "command": "npm run build",
    "description": "Build the project",
    "timeout": 120000,
    "run_in_background": false
  }
}
```
**Regras**:
- Timeout max 600000ms (10 min)
- Default 120000ms (2 min)
- Use `&&` para comandos sequenciais
- NUNCA usar cd, preferir paths absolutos

### Cursor
**Abordagem**: run_terminal_cmd com is_background
```typescript
type run_terminal_cmd = (_: {
  command: string,
  is_background: boolean,
  explanation?: string,
}) => any;
```
**Regras**:
- Shell inicializa no project root
- Verificar working directory no chat history
- Usar --yes para comandos nao-interativos

### Devin
**Abordagem**: Shell com ID de sessao
```xml
<shell id="shellId" exec_dir="/absolute/path/to/dir">
git add file.py && git commit -m "message"
</shell>

<view_shell id="shellId"/>

<kill_shell_process id="shellId"/>
```
**Destaque**: Multiplas sessoes simultaneas com IDs

### Windsurf
**Abordagem**: run_command com cwd
```markdown
CRITICAL: When using run_command NEVER include `cd`.
Instead specify the desired directory as cwd.
```
**Regras**:
- Comando unsafe = confirmacao obrigatoria
- Unsafe: delete files, mutate state, install deps, external requests

## Melhor Pratica Identificada

**Devin** oferece controle mais granular:
1. Sessoes com IDs unicos
2. View/Kill de processos running
3. exec_dir explicito (sem cd)
4. Suporte a bracketed paste mode

## Como Implementar no CODEXA

```python
class TerminalManager:
    SAFE_COMMANDS = [
        "npm install", "pip install", "git status", "git diff",
        "npm run build", "npm run test", "pytest", "ls", "pwd"
    ]

    DANGEROUS_PATTERNS = [
        "rm -rf", "sudo rm", "DROP DATABASE", "DELETE FROM",
        "> /dev/", "mkfs", "dd if="
    ]

    def execute(self, command: str, cwd: str, timeout: int = 120):
        # Validate safety
        safety = self._check_safety(command)
        if safety == "dangerous":
            raise ValueError("Comando potencialmente perigoso")
        if safety == "needs_confirmation":
            return {"status": "needs_confirmation", "command": command}

        # Execute
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            timeout=timeout,
            capture_output=True,
            text=True
        )
        return {
            "status": "success" if result.returncode == 0 else "error",
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    def _check_safety(self, command: str) -> str:
        for pattern in self.DANGEROUS_PATTERNS:
            if pattern in command:
                return "dangerous"
        for safe in self.SAFE_COMMANDS:
            if command.startswith(safe):
                return "safe"
        return "needs_confirmation"
```

## Regras Universais

1. **Nunca usar cd** - Usar cwd/exec_dir
2. **Comandos nao-interativos** - Sempre --yes, -y
3. **Timeout adequado** - Default 2min, max 10min
4. **Background para long-running** - Servidores, watchers
5. **Explicar comandos complexos** - Usuario deve entender

## Comandos Git (Consenso)

```markdown
Git Safety Protocol:
- NEVER force push
- NEVER run destructive commands (hard reset)
- NEVER skip hooks (--no-verify)
- NEVER use git add . (ser especifico)
- NEVER commit without verificar changes
- ALWAYS usar git status antes de commit
```

---
**Fonte**: Analise profunda de 5 ferramentas AI
**Quality Score**: 0.87/1.0
