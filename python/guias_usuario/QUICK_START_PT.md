# 🚀 CODEXA - Guia de Início Rápido

**Versão**: 1.0.0
**Atualizado**: 2025-11-11

---

## ⚡ Começando um Novo Chat

### Opção 1: Comando `/codexa` (RECOMENDADO)

Quando você iniciar uma nova conversa com Claude Code, simplesmente digite:

```
/codexa
```

**O que acontece:**
1. ✅ Carrega o README completo da CODEXA
2. ✅ Verifica status do sistema (6 módulos)
3. ✅ Fornece resumo de todas as capacidades
4. ✅ Mostra Quick Reference de comandos
5. ✅ Lista ADW agents e Claude commands disponíveis

**Resultado:**
Claude estará pronto para usar CODEXA imediatamente, sabendo:
- Todos os 6 módulos disponíveis
- Como executar operações CRUD, Scout e E-commerce
- Integração com ADW agents
- 52 comandos Claude disponíveis

---

### Opção 2: Comando `/prime codexa`

Alternativa usando o comando genérico de priming:

```
/prime codexa
```

**Diferença:**
- `/codexa` → Específico para CODEXA, mais completo
- `/prime codexa` → Genérico, menos estruturado

**Recomendação**: Use `/codexa` para melhor experiência

---

## 📋 Exemplos de Uso

### Exemplo 1: Iniciar e Criar Documentação

```
Você: /codexa

Claude: 🤖 CODEXA HOP-001 Meta-Agent Ready
        System Status: ✅ Operational
        Modules Loaded: 6
        [Mostra resumo completo]

Você: Crie uma documentação sobre nossa API

Claude: Vou usar o módulo CRUD para criar a documentação:
        python cli.py crud create docs/api-guide.md --content "..."
```

### Exemplo 2: Gerenciar Produtos E-commerce

```
Você: /codexa

Claude: [Sistema pronto - 6 módulos carregados]

Você: Liste todos os produtos da categoria Eletrônicos

Claude: python cli.py ecom products list --category "Eletrônicos"
```

### Exemplo 3: Planejamento Estratégico

```
Você: /codexa

Claude: [CODEXA inicializada]

Você: Crie um plano estratégico para Q4 2025

Claude: Vou usar o módulo strategy_mentor:
        python cli.py ecom strategy create-plan \
          --title "Q4 2025 Growth" \
          --objective "Aumentar vendas em 30%"
```

### Exemplo 4: Explorar Repositório

```
Você: /codexa

Claude: [Sistema pronto]

Você: Encontre todos os arquivos Python de teste

Claude: python cli.py scout find --pattern "test_*.py"
```

---

## 🎯 Quando Usar `/codexa`?

### ✅ Use `/codexa` quando:

- Iniciar um novo chat
- Precisar de operações CRUD (documentação)
- Gerenciar produtos e-commerce
- Planejar estratégias e KPIs
- Explorar estrutura de repositório
- Analisar concorrentes
- Organizar base de conhecimento

### ❌ NÃO use `/codexa` quando:

- Fazer perguntas gerais sobre programação
- Trabalhar em código fora de `codexa/`
- Usar outros agents específicos (use `/hop_anuncio`, `/hop_brand`, etc.)
- Apenas conversar sem precisar das ferramentas

---

## 🔄 Fluxo Típico de Trabalho

### Novo Chat → Tarefa CODEXA

```
1. Iniciar chat com Claude Code
2. Digite: /codexa
3. Aguarde carregamento (5-10 segundos)
4. Claude apresenta resumo do sistema
5. Você descreve sua necessidade
6. Claude executa usando CODEXA
```

### Exemplo Real:

```
[Novo Chat]
Você: /codexa

[5 segundos depois]
Claude: 🤖 CODEXA HOP-001 Meta-Agent Ready

        System Status: ✅ Operational
        Modules Loaded: 6
        Location: codexa/

        Available Capabilities:
        - CRUD Operations (6 ops)
        - Scout Operations (5 ops)
        - Product Manager (8 ops)
        - Strategy Mentor (5 ops)
        - Competitor Scout (3 ops)
        - Knowledge Base (3 ops)

        How can I assist you with CODEXA today?

Você: Preciso criar um catálogo de produtos para minha loja

Claude: Vou ajudar você a criar o catálogo usando o módulo product_manager.
        Quantos produtos você gostaria de adicionar inicialmente?

Você: Vamos começar com 3 produtos: Notebook, Mouse e Teclado

Claude: [Executa comandos CODEXA para criar os produtos...]
```

---

## 📚 Recursos Adicionais

### Documentação Completa

- **README.md**: Referência completa de todos os módulos
- **EXAMPLES.md**: 10 exemplos detalhados de uso
- **Quick Reference**: Tabela rápida no README

### Comandos Relacionados

- `/hop_pesquisa` - Pesquisa de mercado (Brazilian marketplaces)
- `/hop_anuncio` - Geração de anúncios otimizados
- `/hop_brand` - Estratégia de marca
- `/mentor` - Planejamento estratégico

### Verificação Manual

Se você quiser verificar manualmente sem usar `/codexa`:

```bash
cd codexa/
python cli.py status
python cli.py --help
```

---

## 🆘 Solução de Problemas

### Problema: `/codexa` não funciona

**Solução**:
1. Verifique se está no repositório TAC-7
2. Tente `/prime codexa` como alternativa
3. Carregue manualmente: "Leia o README.md da pasta codexa/"

### Problema: Claude não entende comandos CODEXA

**Solução**:
1. Execute `/codexa` novamente
2. Certifique-se de que o status mostra "6 modules"
3. Use comandos completos: `python cli.py crud create ...`

### Problema: Módulos não carregam

**Solução**:
```bash
cd codexa/
pip install -r requirements.txt
python cli.py status
```

---

## 💡 Dicas Pro

### Dica 1: Sempre inicie com `/codexa`
Economize tempo! Não explique o que é CODEXA, deixe o comando fazer isso.

### Dica 2: Use Quick Reference
O README tem uma tabela "Need to... → Command" muito útil.

### Dica 3: Combine com outros comandos
```
/codexa                    # Carrega CODEXA
[trabalha com CODEXA]
/commit                    # Faz commit das mudanças
```

### Dica 4: README auto-atualiza
Se adicionar novos módulos:
```bash
python cli.py readme update
```

### Dica 5: Explore os agents ADW
CODEXA integra com 10 agents em `../adws/` - veja a seção no README.

---

## 📊 Comparação de Comandos

| Comando | Escopo | Quando Usar |
|---------|--------|-------------|
| `/codexa` | CODEXA HOP-001 (6 módulos) | Novo chat, operações CODEXA |
| `/prime` | Repositório geral | Entender todo o projeto TAC-7 |
| `/hop_pesquisa` | Pesquisa de mercado | Analisar produtos/mercados BR |
| `/hop_anuncio` | Geração de anúncios | Criar ads para marketplaces |
| `/hop_brand` | Estratégia de marca | Definir posicionamento de marca |
| `/mentor` | Planejamento estratégico | Criar planos e KPIs |

---

## ✅ Checklist de Início

Antes de começar a usar CODEXA em um novo chat:

- [ ] Executei `/codexa`
- [ ] Vi o resumo "CODEXA Ready" com 6 módulos
- [ ] Entendo quais operações estão disponíveis
- [ ] Sei como executar comandos (`python cli.py ...`)
- [ ] Conheço a Quick Reference no README

**Tudo pronto?** Comece a usar! 🚀

---

## 🎓 Aprendizado Progressivo

### Nível 1: Básico (Dia 1)
- Execute `/codexa`
- Use comandos CRUD básicos
- Liste e busque documentos

### Nível 2: Intermediário (Semana 1)
- Use Scout para explorar repositórios
- Gerencie produtos e-commerce
- Crie planos estratégicos

### Nível 3: Avançado (Mês 1)
- Integre com ADW agents
- Automatize workflows
- Use todos os 6 módulos em conjunto

---

**Pronto para começar?** Digite `/codexa` no seu próximo chat! 🎉

---

**Mantido por**: TAC-7 Team
**Parte de**: CODEXA HOP-001 Meta-Agent
**Versão do Sistema**: 1.0.0
