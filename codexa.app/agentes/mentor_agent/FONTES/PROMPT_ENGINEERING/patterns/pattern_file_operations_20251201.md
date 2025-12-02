# Pattern: File Operations

**Categoria**: Universal (Obrigatorio)
**Frequencia**: 86% das ferramentas analisadas
**Ultima Atualizacao**: 2025-12-02
**Quality Score**: 0.88

## Resumo Executivo

File operations sao essenciais para AI coding assistants. O pattern mais inovador e o uso de `// ... existing code ...` para edicoes parciais, reduzindo tokens e tempo.

## Implementacoes por Ferramenta

### Claude Code (Anthropic)
**Abordagem**: Edit tool com old_string/new_string
```markdown
Edit tool rules:
- MUST read file before editing
- old_string must be UNIQUE in file
- Preserve exact indentation
- Use replace_all for bulk renames
```
**Operacoes**: Read, Edit, Write, NotebookEdit

### Cursor
**Abordagem**: edit_file com `// ... existing code ...`
```typescript
type edit_file = (_: {
  target_file: string,
  instructions: string,
  code_edit: string  // Use "// ... existing code ..."
}) => any;
```
**Exemplo**:
```javascript
// ... existing code ...
FIRST_EDIT
// ... existing code ...
SECOND_EDIT
// ... existing code ...
```

### Devin
**Abordagem**: Comandos separados por operacao
```xml
<!-- Read -->
<open_file path="/path/to/file.py" start_line="123" end_line="456"/>

<!-- Edit -->
<str_replace path="/path/to/file">
<old_str>codigo antigo</old_str>
<new_str>codigo novo</new_str>
</str_replace>

<!-- Insert -->
<insert path="/path/to/file" insert_line="123">
nova linha
</insert>

<!-- Delete -->
<remove_str path="/path/to/file">
codigo para remover
</remove_str>
```
**Destaque**: `<find_and_edit>` para refactoring em massa

### v0 (Vercel)
**Abordagem**: CodeProject blocks
```markdown
Write: lang file="path/to/file"
Edit: // ... existing code ...
Delete: ...deleted...
Move: ...moved to path/to/new-file...
```

## Melhor Pratica Identificada

**Cursor/v0** com `// ... existing code ...`:
1. Reduz tokens significativamente
2. Usuario ve apenas mudancas
3. Sistema faz merge automatico
4. Previne overwrite acidental

## Como Implementar no CODEXA

```python
class FileOperations:
    def edit_with_diff(self, file_path: str, edits: list[dict]) -> str:
        content = self.read(file_path)
        for edit in edits:
            if edit["old"] not in content:
                raise ValueError(f"old_string nao encontrado")
            if content.count(edit["old"]) > 1:
                raise ValueError("old_string nao e unico")
            content = content.replace(edit["old"], edit["new"], 1)
        self.write(file_path, content)
        return self._generate_diff(file_path)
```

## Regras Universais

1. **SEMPRE ler antes de editar**
2. **old_string deve ser UNICO**
3. **Preservar indentacao**
4. **Nunca usar cat/echo/sed**
5. **Preferir editar vs criar**

## Code Citations

| Ferramenta | Formato |
|------------|---------|
| Claude Code | `file_path:line_number` |
| Cursor | `startLine:endLine:filepath` |

---
**Fonte**: Analise profunda de 5 ferramentas AI
**Quality Score**: 0.88/1.0
