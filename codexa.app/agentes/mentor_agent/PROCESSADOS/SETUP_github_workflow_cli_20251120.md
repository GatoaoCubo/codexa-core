# Setup Mínimo: GitHub + Claude CLI + [OPEN_VARIABLE: Editor]

**Categoria**: setup_prerequisites
**Qualidade**: 0.89/1.00
**Data**: 20251120

## Conteúdo

### Setup Mínimo para Trabalhar com CODEXA

Antes de usar o sistema CODEXA, você precisa configurar 3 ferramentas essenciais. Este guia assume ZERO conhecimento prévio e te leva do zero ao operacional em [OPEN_VARIABLE: tempo_estimado_minutos] minutos.

**Pré-requisitos**: Apenas um computador com Windows, Mac ou Linux. Nada mais.

### 1️⃣ Criar Conta no GitHub (5 min)

**O que é GitHub**: Plataforma que armazena código-fonte e permite versionamento (histórico de todas as mudanças). Pense nele como "Google Drive para código", mas infinitamente mais poderoso.

**Por que você precisa**:
- Todo o código do CODEXA está hospedado no GitHub
- Para "clonar" (baixar) o projeto para sua máquina
- Para contribuir com melhorias e receber atualizações

**Passo-a-passo**:
1. Acesse https://github.com/signup
2. Crie conta (email + senha + nome de usuário)
3. Verifique email
4. **IMPORTANTE**: Guarde seu username — você vai precisar

**Teste**: Acesse https://github.com/[SEU_USERNAME] — deve ver seu perfil

### 2️⃣ Instalar Git (Ferramenta de Versionamento) (5 min)

**O que é Git**: Software que permite gerenciar versões de código. É a "máquina do tempo" do desenvolvedor — volte para qualquer versão anterior do código.

**Instalação por sistema operacional**:

**Windows**:
```bash
# Baixe em: https://git-scm.com/download/win
# Execute o instalador
# Aceite todas as opções padrão (apenas clique "Next" até o fim)
```

**Mac**:
```bash
# Abra Terminal (Cmd+Space → digite "Terminal")
# Cole este comando:
xcode-select --install
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install git -y
```

**Teste** (em qualquer terminal):
```bash
git --version
# Deve mostrar: git version 2.X.X
```

**Configure Git** (obrigatório uma vez):
```bash
git config --global user.name "[SEU_NOME]"
git config --global user.email "[SEU_EMAIL_GITHUB]"
```

### 3️⃣ Instalar GitHub CLI (Superpoder para GitHub) (5 min)

**O que é GitHub CLI**: Ferramenta oficial do GitHub para operar direto do terminal. Clonar projetos, criar branches, abrir PRs — tudo sem sair da linha de comando.

**Por que você precisa**: Automações do CODEXA usam `gh` commands. Sem isso, você terá que fazer tudo manualmente no navegador (lento e chato).

**Instalação**:

**Windows**:
```bash
# Via winget (Windows 10+)
winget install --id GitHub.cli

# OU baixe em: https://cli.github.com/
```

**Mac**:
```bash
brew install gh
```

**Linux**:
```bash
# Ubuntu/Debian
sudo apt install gh -y

# Arch
sudo pacman -S github-cli
```

**Autenticação** (CRÍTICO):
```bash
# Execute:
gh auth login

# Escolha:
# - GitHub.com
# - HTTPS
# - Yes (autenticação via browser)
# - Abra o link que aparece
# - Cole o código
# - Done!
```

**Teste**:
```bash
gh repo list
# Deve listar seus repositórios (ou vazio se não tem nenhum ainda)
```

### 4️⃣ Instalar Claude CLI (Opcional mas Recomendado) (5 min)

**O que é Claude CLI**: Interface de linha de comando oficial para interagir com Claude (o LLM da Anthropic). Permite rodar prompts, acessar APIs, e integrar Claude em scripts.

**Por que é recomendado**: Alguns workflows avançados do CODEXA usam Claude CLI para automações. Não é obrigatório para começar, mas você vai querer mais tarde.

**Instalação**:
```bash
# Requer Node.js (se não tem: https://nodejs.org/)
npm install -g @anthropic-ai/cli

# OU via pip (Python)
pip install anthropic-cli
```

**Configuração**:
```bash
# Pegue sua API key em: https://console.anthropic.com/

# Configure:
export ANTHROPIC_API_KEY="sua-key-aqui"

# Adicione no seu ~/.bashrc ou ~/.zshrc para persistir
```

**Teste**:
```bash
anthropic --version
# Deve mostrar versão instalada
```

### 5️⃣ Escolher e Configurar [OPEN_VARIABLE: Editor] (10 min)

**Opção A: VS Code (Recomendado para iniciantes)**

VS Code é um editor gratuito, leve, com suporte nativo a Git e extensões poderosas.

**Instalação**:
- Baixe em: https://code.visualstudio.com/
- Instale normalmente
- Abra e instale extensões:
  - GitLens (visualizador de Git)
  - Markdown All in One (para editar READMEs)
  - [OPEN_VARIABLE: extensao_linguagem] (se for trabalhar com código)

**Opção B: Cursor (Recomendado para usuários Claude)**

Cursor é um fork do VS Code com integração nativa de Claude. Se você usa Claude intensamente, é superior.

**Instalação**:
- Baixe em: https://cursor.sh/
- Instale (idêntico a VS Code)
- Na primeira abertura, conecte sua conta Claude
- Mesmo suporte de extensões que VS Code

**Configuração mínima (qualquer editor)**:
```json
// Settings.json (Ctrl+Shift+P → "Open Settings JSON")
{
  "editor.formatOnSave": true,
  "files.autoSave": "afterDelay",
  "git.autofetch": true,
  "terminal.integrated.defaultProfile.windows": "Git Bash"
}
```

### 6️⃣ Clonar o Projeto CODEXA (2 min)

Agora que tudo está instalado, clone o projeto:

```bash
# Navegue para onde quer salvar (ex: Desktop)
cd ~/Desktop

# Clone o repositório
gh repo clone [OPEN_VARIABLE: seu-usuario]/lm.codexa

# OU use Git direto:
git clone https://github.com/[OPEN_VARIABLE: seu-usuario]/lm.codexa.git

# Entre no diretório
cd lm.codexa
```

**Teste**:
```bash
# Liste arquivos
ls

# Deve ver: codexa.app/, agentes/, README.md, etc.
```

### 7️⃣ Verificação Final: Sistema Operacional (1 min)

Execute este checklist no terminal dentro do diretório do projeto:

```bash
# Checklist de setup
git --version && echo "✅ Git OK" || echo "❌ Git FALTANDO"
gh --version && echo "✅ GitHub CLI OK" || echo "❌ GitHub CLI FALTANDO"
anthropic --version && echo "✅ Claude CLI OK" || echo "⚠️ Claude CLI opcional"
code --version && echo "✅ VS Code OK" || echo "⚠️ Editor não detectado (OK se usa Cursor)"
```

**Todos os ✅?** Você está pronto para trabalhar!

**Algum ❌?** Revise a seção correspondente acima.

### Workflow Básico: Seu Primeiro Dia

Agora que está configurado, este é o fluxo de trabalho diário:

```bash
# 1. Abra o terminal no diretório do projeto
cd ~/Desktop/lm.codexa

# 2. Puxe atualizações do GitHub (sempre faça isso antes de trabalhar)
git pull origin main

# 3. Abra o editor
code .   # VS Code
# OU
cursor . # Cursor

# 4. Faça suas modificações nos arquivos

# 5. Veja o que mudou
git status

# 6. Adicione mudanças para commit
git add .

# 7. Crie um commit (snapshot da mudança)
git commit -m "Descrição do que você fez"

# 8. Envie para o GitHub
git push origin main
```

### Troubleshooting Comum

**"Permission denied (publickey)"** ao fazer `git push`:
```bash
# Configure SSH keys (mais seguro que HTTPS):
ssh-keygen -t ed25519 -C "[SEU_EMAIL]"
# Pressione Enter 3x
# Copie a key pública:
cat ~/.ssh/id_ed25519.pub
# Cole em: GitHub Settings → SSH and GPG keys → New SSH key
```

**"fatal: not a git repository"**:
```bash
# Você não está no diretório do projeto. Navegue:
cd ~/Desktop/lm.codexa
```

**"command not found: gh/git/code"**:
- Reinicie o terminal após instalação
- Verifique se adicionou ao PATH (instaladores normalmente fazem isso automaticamente)

### Próximos Passos

Agora que seu ambiente está configurado:

1. Leia o `README.md` do projeto CODEXA
2. Execute `/prime` para ver o sistema navigator
3. Escolha um agente para explorar (recomendação: comece pelo `/prime-mentor`)
4. Faça seus primeiros commits modificando arquivos simples

**Tempo total de setup**: ~30 min (incluindo troubleshooting)
**Benefício**: Ambiente profissional de desenvolvimento pronto para colaborar no CODEXA e qualquer outro projeto open-source

---

**Tags**: setup, github, git, cli, prerequisites, vscode, cursor, workflow
**Palavras-chave**: GitHub, Git, CLI, setup, instalação, workflow, clone
**Origem**: curso_agent/START_HERE.md + Módulo 1 Introdução
**Processado**: 20251120
