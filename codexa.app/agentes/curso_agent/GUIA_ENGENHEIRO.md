# GUIA DO ENGENHEIRO - Revisao e Deploy para Hotmart

**Para voce que criou o curso e precisa publicar no Hotmart.**

**Tempo estimado**: 4-6 horas para revisao completa + 2-3 horas para configurar Hotmart

---

## VISAO GERAL DO FLUXO

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FLUXO ENGENHEIRO → HOTMART                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. REVISAR           2. GRAVAR           3. CONFIGURAR             │
│  ───────────         ─────────           ─────────────              │
│  Markdown files  →   Videos/Audio   →   Hotmart Club               │
│  (este repo)         (OBS/Loom)         (modulos/aulas)            │
│                                                                     │
│  context/*.md        MP4 files          Upload + Config             │
│       │                  │                    │                     │
│       ↓                  ↓                    ↓                     │
│  Revisar/Editar     Gravar ou IA       Publicar                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## FASE 1: NAVEGACAO E REVISAO DO CONTEUDO

### 1.1 Estrutura dos Arquivos do Curso

```
curso_agent/context/
├── 00_INDICE_CURSO_CODEXA.md      ← COMECE AQUI (indice geral)
├── 00_MODULO_ISCA_DIGITAL.md      ← M0: Freemium (10 min)
├── 00B_MODULO_QUICK_WIN.md        ← M0.5: Quick Win (30 min)
├── 00C_TRILHAS_APRENDIZADO.md     ← Guia das 4 trilhas
├── 00_GAMIFICATION_SYSTEM.md      ← Sistema de XP/niveis
│
├── 01_MODULO_INTRODUCAO.md        ← M1: Introducao (1-2h)
├── 02_MODULO_ANUNCIOS.md          ← M2: Anuncios (2-3h)
├── 03_MODULO_PESQUISA.md          ← M3: Pesquisa (1-2h)
├── 04_MODULO_MARCA.md             ← M4: Marca (2-3h)
├── 05_MODULO_FOTOS.md             ← M5: Fotos (1-2h)
├── 06_INDEX_META_CONSTRUCAO.md    ← M6: Navegador (3 partes)
├── 06_MODULO_META_CONSTRUCAO.md   ← M6: Meta-construcao (3.5h)
│
├── PROJETO_ECOFLOW.md             ← Case completo end-to-end
├── EXERCICIOS_GABARITOS.md        ← Gabaritos dos exercicios
├── COMANDOS_AVANCADOS.md          ← Documentacao de comandos
│
├── FAQ.md                         ← Perguntas frequentes
├── FAQ_10_MENTIRAS.md             ← Objecoes e mitos
├── GLOSSARIO.md                   ← Termos tecnicos
├── ARGUMENTOS_CORE_CURSO.md       ← Argumentos de venda
└── RECURSOS_EXTRAS.md             ← Links e materiais
```

### 1.2 Ordem de Revisao Recomendada

**Sessao 1 (1h): Visao Geral**
```bash
# Abra no VS Code ou Claude Code
code curso_agent/context/

# Leia nesta ordem:
1. 00_INDICE_CURSO_CODEXA.md       # Entenda a estrutura
2. 00C_TRILHAS_APRENDIZADO.md      # Entenda as 4 trilhas
3. 00_GAMIFICATION_SYSTEM.md       # Entenda o sistema de XP
```

**Sessao 2 (2h): Modulos Core**
```
4. 00_MODULO_ISCA_DIGITAL.md       # Isca para capturar leads
5. 00B_MODULO_QUICK_WIN.md         # Onboarding rapido
6. 01_MODULO_INTRODUCAO.md         # Introducao completa
7. 02_MODULO_ANUNCIOS.md           # Agente principal
```

**Sessao 3 (2h): Modulos Avancados**
```
8. 03_MODULO_PESQUISA.md           # Pesquisa de mercado
9. 04_MODULO_MARCA.md              # Branding
10. 05_MODULO_FOTOS.md             # Fotos com IA
11. 06_INDEX_META_CONSTRUCAO.md    # Leia o indice primeiro
12. 06_MODULO_META_CONSTRUCAO.md   # Meta-construcao (longo!)
```

**Sessao 4 (1h): Materiais de Apoio**
```
13. PROJETO_ECOFLOW.md             # Projeto pratico
14. EXERCICIOS_GABARITOS.md        # Respostas dos exercicios
15. FAQ.md + FAQ_10_MENTIRAS.md    # Suporte
```

### 1.3 Como Revisar Cada Arquivo

**Checklist de Revisao por Modulo:**

```markdown
## REVISAO: [NOME_MODULO]

### Conteudo
- [ ] Objetivos de aprendizado claros?
- [ ] Exemplos sao relevantes para Brasil?
- [ ] Exercicios sao praticos?
- [ ] XP e achievements fazem sentido?

### Tecnico
- [ ] Comandos funcionam? (testar /prime-*)
- [ ] Links internos funcionam?
- [ ] Sem referencias a GPT-5 ou modelos inexistentes?

### Pedagogico
- [ ] Fluxo logico (conceito → exemplo → pratica)?
- [ ] Duracao realista?
- [ ] Nivel de dificuldade adequado?

### Notas
- [ ] O que precisa mudar:
- [ ] O que esta otimo:
```

---

## FASE 2: EDICAO E PERSONALIZACAO

### 2.1 Editando com Claude Code

```bash
# Abra o projeto
cd lm.codexa
claude .

# Carregue o contexto do curso
/prime-curso

# Peca para revisar um modulo especifico
"Revise o modulo 02_MODULO_ANUNCIOS.md e sugira melhorias"

# Peca para ajustar tom ou conteudo
"Reescreva a secao 4.2 com mais exemplos praticos de Mercado Livre"
```

### 2.2 Variaveis a Personalizar

Busque e substitua estes placeholders:

| Placeholder | Substituir Por |
|-------------|----------------|
| `[SEU_EMAIL]` | Seu email de suporte |
| `[LINK_DISCORD]` | Link do seu Discord/Telegram |
| `[PRECO_CURSO]` | Preco real (R$ X,XX) |
| `[GARANTIA_DIAS]` | Dias de garantia (7, 15, 30) |
| `codexa` | Seu dominio/repo |

### 2.3 Personalizacoes Recomendadas

**1. Adicione seu contexto:**
- Seus cases de sucesso
- Depoimentos de clientes
- Exemplos do seu nicho

**2. Ajuste o tom:**
```markdown
# Se quiser mais formal:
"Este modulo apresenta os conceitos fundamentais..."

# Se quiser mais casual (padrao CODEXA):
"Bora entender como isso funciona na pratica..."
```

**3. Adicione bonus:**
- Templates exclusivos
- Planilhas
- Checklists em PDF

---

## FASE 3: PREPARACAO DOS VIDEOS

### 3.1 Opcao A: Gravar Voce Mesmo

**Setup Minimo:**
- Microfone USB (Blue Yeti, HyperX)
- OBS Studio (gratis) ou Loom (facil)
- Tela do computador + webcam opcional

**Workflow:**
```
1. Abra o markdown do modulo
2. Use como roteiro (ja tem timing)
3. Grave demonstrando na tela
4. Exporte MP4 1080p
```

**Dica**: Os markdowns ja tem marcacoes de tempo:
```markdown
### [00:00-01:30] Hook
### [01:30-05:00] Conceito Principal
### [05:00-10:00] Demonstracao
```

### 3.2 Opcao B: IA para Audio/Video

**Ferramentas:**
- **ElevenLabs**: Gera audio a partir de texto
- **HeyGen/Synthesia**: Gera video com avatar
- **DALL-E/Midjourney**: Gera imagens para slides

**Workflow IA:**
```
1. Extraia texto do markdown
2. Gere audio no ElevenLabs
3. Crie slides no Canva/PowerPoint
4. Sincronize audio + slides
5. Exporte MP4
```

### 3.3 Estrutura de Arquivos de Video

```
videos/
├── M0_isca_digital.mp4           (10 min)
├── M0.5_quick_win.mp4            (30 min)
├── M1_introducao/
│   ├── M1_01_boas_vindas.mp4     (5 min)
│   ├── M1_02_o_que_e_codexa.mp4  (15 min)
│   ├── M1_03_instalacao.mp4      (10 min)
│   └── M1_04_primeiro_comando.mp4 (15 min)
├── M2_anuncios/
│   ├── M2_01_...
│   └── ...
└── ...
```

---

## FASE 4: CONFIGURACAO NO HOTMART

### 4.1 Criar Produto

1. Acesse: https://app.hotmart.com
2. Produtos → Criar Produto
3. Tipo: **Curso Online (Club)**
4. Nome: "CODEXA - Cerebro IA para Sellers"
5. Categoria: Marketing Digital > E-commerce

### 4.2 Estrutura do Club

```
CODEXA Club/
├── Pilar 1: Fundamentos
│   ├── Modulo 0: Isca Digital (GRATUITO)
│   ├── Modulo 0.5: Quick Win
│   └── Modulo 1: Introducao
│
├── Pilar 2: Agentes Core
│   ├── Modulo 2: Anuncios
│   ├── Modulo 3: Pesquisa
│   ├── Modulo 4: Marca
│   └── Modulo 5: Fotos
│
├── Pilar 3: Avancado
│   ├── Modulo 6A: Fundamentos Agentivos
│   ├── Modulo 6B: Criando Seu Agente
│   └── Modulo 6C: Composables
│
├── Bonus
│   ├── Projeto EcoFlow (Case Completo)
│   ├── Gabaritos dos Exercicios
│   └── Documentacao de Comandos
│
└── Recursos
    ├── FAQ
    ├── Glossario
    └── Comunidade
```

### 4.3 Configurar Gotejamento (Drip)

**Recomendacao:**
```
Dia 0: M0, M0.5, M1 (onboarding completo)
Dia 3: M2 (anuncios - o mais valioso)
Dia 7: M3 + M4
Dia 14: M5
Dia 21: M6A
Dia 28: M6B + M6C
Dia 30: Bonus liberados
```

### 4.4 Configurar Preco e Pagamento

**Sugestao de Precificacao:**
```
Preco cheio: R$ 997
Preco lancamento: R$ 497 (50% off)
Parcelamento: 12x de R$ 49,70

Garantia: 7 dias (padrao Hotmart)
```

### 4.5 Upload dos Videos

```
Para cada aula:
1. Upload do video (MP4)
2. Adicionar descricao (copie do markdown)
3. Anexar materiais (PDF do workbook)
4. Configurar duracao
5. Ativar DRM (protecao)
```

### 4.6 Materiais Complementares

**O que fazer upload:**
- Workbooks em PDF (gere a partir dos markdowns)
- Checklists
- Templates (se tiver)
- Links para recursos externos

**Como gerar PDFs:**
```bash
# Usando pandoc (instale: brew install pandoc)
pandoc 01_MODULO_INTRODUCAO.md -o M1_Workbook.pdf

# Ou use Notion/Google Docs para formatar melhor
```

---

## FASE 5: CONFIGURACAO DO ALUNO + CLAUDE CODE

### 5.1 O Diferencial do Curso

**IMPORTANTE**: Este curso e diferente porque:
1. Aluno assiste video no Hotmart
2. Aluno abre Claude Code no mesmo repositorio
3. Aluno pratica com os agentes reais
4. Aluno pode perguntar para o curso_agent

### 5.2 Instrucoes para Aluno (incluir no Club)

Crie uma aula "Como usar Claude Code" com:
```markdown
## Configuracao do Ambiente de Pratica

1. Clone o repositorio:
   git clone https://github.com/codexa-ai/lm.codexa.git
   cd lm.codexa

2. Instale Claude Code:
   npm install -g @anthropic/claude-code

3. Configure API Key:
   claude config set api_key sk-ant-xxx

4. Abra o projeto:
   claude .

5. Teste:
   /prime

Pronto! Agora voce pode praticar junto com os videos.
```

### 5.3 Suporte via curso_agent

O aluno pode perguntar:
```
/prime-curso

"Estou no modulo 2, nao entendi a parte de compliance.
Pode me explicar de outro jeito?"
```

E o curso_agent (voce, Claude) vai responder baseado no contexto do curso.

---

## CHECKLIST FINAL PRE-LANCAMENTO

```markdown
## CHECKLIST DE LANCAMENTO

### Conteudo
- [ ] Todos os modulos revisados
- [ ] Videos gravados/gerados
- [ ] Workbooks em PDF
- [ ] Exercicios com gabaritos

### Hotmart
- [ ] Produto criado
- [ ] Estrutura de modulos configurada
- [ ] Videos uploaded
- [ ] Gotejamento configurado
- [ ] Preco e pagamento configurado
- [ ] Pagina de vendas pronta
- [ ] Garantia configurada

### Tecnico
- [ ] Repositorio publico (ou acesso para alunos)
- [ ] Instrucoes de instalacao claras
- [ ] API key funciona
- [ ] Comandos testados

### Marketing
- [ ] Copy de vendas pronta (use ARGUMENTOS_CORE_CURSO.md)
- [ ] Email sequence configurado
- [ ] Pixel de tracking instalado

### Suporte
- [ ] Canal de suporte definido (Discord/Telegram)
- [ ] FAQ pronto
- [ ] Onboarding automatico configurado
```

---

## COMANDOS UTEIS

### Revisar conteudo com Claude Code:
```bash
/prime-curso
"Liste todos os exercicios do modulo 2 com seus objetivos"
"Gere um resumo de 1 paragrafo de cada modulo"
"Encontre inconsistencias entre os modulos"
```

### Gerar materiais:
```bash
/curso_workbook --module 02
/curso_validate --all
```

### Verificar qualidade:
```bash
"Execute validacao de brand voice em todos os modulos"
"Verifique se ha referencias a GPT-5 no conteudo"
```

---

## SUPORTE

Duvidas sobre este guia?
1. Pergunte ao curso_agent: `/prime-curso`
2. Consulte: `artifacts/DEPLOYMENT_GUIDE.md`
3. Veja: `builders/05_hotmart_package_builder.py`

---

**Versao**: 1.0.0
**Criado**: 2025-11-25
**Para**: Engenheiro/Criador do Curso CODEXA
