# 📖 Como Usar os Comandos ADW

## 🔍 Descobrindo Comandos Disponíveis

Os comandos slash do Claude Code são registrados automaticamente a partir dos arquivos `.md` neste diretório.

### Comandos Disponíveis

Digite `/` (barra) no chat do Claude Code e você verá os comandos disponíveis:

- `/prime` - Executar workflow ADW completo
- `/adw-list` - Listar todos os workflows ADW disponíveis

> **Nota**: Os comandos aparecem automaticamente após criar/modificar arquivos `.md` neste diretório.

---

## 🎯 Uso Básico

### 1. Listar Workflows

```bash
/adw-list
```

**O que faz**:
- Mostra todos os 5 workflows ADW
- Especificações completas (fases, duração, outputs)
- Input requirements
- Quality gates
- Exemplos de uso

---

### 2. Executar Workflow

```bash
/prime {agent_name} [input]
```

**Agentes disponíveis**:
- `pesquisa` - Market research
- `anuncio` - Ad generation
- `mentor` - Mentoring
- `marca` - Brand strategy
- `photo` - AI photography

**Exemplos**:

```bash
# Pesquisa de mercado
/prime pesquisa Product: Garrafa térmica, Category: Casa, Price: R$ 80-250

# Geração de anúncios
/prime anuncio USER_DOCS/produtos/research/garrafa_termica_research_notes.md

# Mentoria
/prime mentor Como melhorar títulos no Mercado Livre?

# Estratégia de marca
/prime marca Business: Garrafas sustentáveis, Mission: Reduzir plástico...

# Prompts de fotografia
/prime photo subject=Garrafa térmica, style=minimalist
```

---

## 🛠️ Como os Comandos Funcionam

### Estrutura de Arquivo

Cada comando é um arquivo `.md` neste diretório:

```
.claude/commands/
├── prime.md          → Cria comando /prime
├── adw-list.md       → Cria comando /adw-list
└── COMO_USAR.md      → Este arquivo (não é comando)
```

### Convenções de Nomenclatura

- ✅ **Use hífens**: `adw-list.md` → `/adw-list`
- ❌ **Evite underscores**: `adw_list.md` pode não funcionar
- ✅ **Use lowercase**: `prime.md` → `/prime`
- ❌ **Evite espaços**: Não use espaços no nome do arquivo

### Formato do Arquivo

```markdown
# Título do Comando

Descrição do que o comando faz.

## Arguments (opcional)

Lista de argumentos aceitos.

## Usage Examples

Exemplos práticos de uso.

## Detailed Instructions

Instruções detalhadas de execução.
```

---

## 🔄 Recarregando Comandos

Se você adicionar/modificar um comando e ele não aparecer:

1. **Salve o arquivo** `.md` no diretório `.claude/commands/`
2. **Reinicie o Claude Code** ou recarregue a janela
3. **Digite `/`** no chat para ver os comandos atualizados

---

## ✨ Criando Novos Comandos

### Exemplo: Criar `/adw-validate`

1. **Criar arquivo**: `.claude/commands/adw-validate.md`

2. **Estrutura básica**:

```markdown
# ADW Validate Command

Validate agent files and configurations.

## Usage

```bash
/adw-validate {agent_name}
```

## Arguments

- `{agent_name}`: Nome do agente (pesquisa, anuncio, mentor, marca, photo)

## What it checks

- PRIME.md exists
- ADW workflow exists
- All HOP prompts exist
- Config files are valid JSON
- Templates exist

## Example

```bash
/adw-validate pesquisa
```

Output:
```
✅ PRIME.md exists
✅ ADW workflow exists
✅ 12/12 HOP prompts found
✅ 4/4 config files valid
✅ 1/1 template found

Status: FUNCTIONAL
```
```

3. **Salvar arquivo**

4. **Usar comando**: `/adw-validate pesquisa`

---

## 📋 Comandos Futuros Planejados

- `/adw-quick {agent}` - Execute abbreviated workflow
- `/adw-validate {agent}` - Validate agent files
- `/adw-chain {agent1} {agent2}` - Chain workflows
- `/adw-status` - Show execution history
- `/adw-test {agent}` - Run test with sample data

---

## 🆘 Troubleshooting

### Comando não aparece na lista

**Problema**: Criei arquivo `.md` mas comando não aparece ao digitar `/`

**Soluções**:
1. Verifique se o arquivo está em `.claude/commands/`
2. Verifique se o nome do arquivo usa hífen (não underscore)
3. Recarregue o Claude Code
4. Verifique se o arquivo tem extensão `.md` (não `.txt`)

### Comando aparece mas não executa

**Problema**: Comando aparece na lista mas retorna erro ao executar

**Soluções**:
1. Verifique o conteúdo do arquivo `.md`
2. Certifique-se que as instruções estão claras
3. Teste com argumentos corretos
4. Veja logs de erro do Claude Code

---

## 📚 Documentação Relacionada

- **Quick Start**: `QUICK_START_ADW.md` - Guia rápido de uso
- **Review Técnico**: `ADW_TEST_REVIEW_REPORT.md` - Análise completa
- **README Comandos**: `.claude/commands/README.md` - Visão geral

---

**Versão**: 1.0.0
**Atualizado**: 2025-11-24
**Maintainer**: CODEXA Meta-Constructor
