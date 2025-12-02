# ⚡ CLAUDE CODE, FERRAMENTAS E SKILLS
## A Hierarquia do Poder Computacional: Do Átomo ao Organismo

> **Axioma Fundamental:** "Um comando não é um skill. Um skill não é um plugin. Hierarquia mal compreendida = sistema mal construído."

---

## 🎭 METÁFORA CENTRAL: DA CÉLULA AO ORGANISMO

Imagine construir um ser vivo:

```
ÁTOMO (Slash Command)
   ↓ se combina em
MOLÉCULA (Subagent)  
   ↓ se organiza em
CÉLULA (MCP - Integração Externa)
   ↓ forma
ÓRGÃO (Skill - Workflow Autônomo)
   ↓ compõe
ORGANISMO (Plugin - Sistema Compartilhável)
```

**Por que essa hierarquia importa?**

```
❌ Erro Comum:
   Chamar tudo de "skill" ou "agent"
   └─ Confusão, retrabalho, impossível escalar

✅ Hierarquia Clara:
   Cada nível tem propósito específico
   └─ Composição previsível, escalável, debugável
```

---

## 📐 OS 4 PILARES FUNDAMENTAIS (CORE-4)

Antes de falar de comandos, agents ou skills, entenda os **4 pilares** que sustentam TODO sistema Claude Code:

### **Pilar 1: CONTEXTO (Single Source of Truth)**

**Jargão Técnico:** Configuration as Context  
**Metáfora:** O DNA que define identidade

```yaml
# context/project.yml - O genoma do projeto

project:
  name: "E-commerce Ads Factory"
  domain: "marketplace-optimization"
  
brand:
  name: "BelaNature"
  voice: "empoderador, natural, acolhedor"
  palette:
    - "#2d5016"  # Verde natural
    - "#f5f5dc"  # Bege suave
    - "#ffffff"  # Branco limpo
  typography:
    - "Montserrat"  # Títulos
    - "Open Sans"   # Corpo
    
goals:
  - "Aumentar conversão em 40%"
  - "Reduzir custo de produção em 60%"
  - "Manter brand consistency"
  
constraints:
  - "Compliance ANVISA para cosméticos"
  - "Sem claims médicos"
  - "Budget máximo R$ 500 por campanha"
  
audience:
  primary:
    - age: "25-40"
    - gender: "feminino"
    - interests: ["beleza natural", "sustentabilidade"]
  secondary:
    - age: "18-25"
    - interests: ["cuidados capilares", "vegano"]
```

**Axioma do Contexto:**  
> "Contexto mal definido = decisões erradas amplificadas a cada comando."

---

### **Pilar 2: MODELOS (Papéis e Responsabilidades)**

**Jargão Técnico:** Role-Based Orchestration  
**Metáfora:** Cada ator sabe seu papel na peça

```python
# Hierarquia de Modelos

ORCHESTRATOR (Claude Code)
├─ Coordena workflow geral
├─ Delega tarefas específicas
└─ Consolida outputs

SPECIALISTS (Subagents)
├─ Research Specialist
├─ Copy Specialist  
├─ Visual Specialist
└─ QA Specialist

TOOLS (MCPs + Nativos)
├─ web_search (nativo)
├─ file_search (nativo)
├─ google_drive_mcp (externo)
└─ notion_mcp (externo)
```

**Axioma dos Modelos:**  
> "Orquestrador que faz tudo não orquestra. Especialista que faz de tudo não especializa."

---

### **Pilar 3: PROMPT (Instruções Precisas)**

**Jargão Técnico:** Prompt Engineering as Code  
**Metáfora:** Receita de bolo vs. "faça um bolo bom"

```markdown
❌ Prompt Vago:
"Pesquise sobre shampoo cachos"

✅ Prompt Estruturado:
<task>
  <objective>
    Pesquisar competidores de shampoo para cachos no Mercado Livre
  </objective>
  
  <methodology>
    1. Web search: site:mercadolivre.com.br "shampoo cachos"
    2. Analisar TOP 10 resultados
    3. Extrair padrões de título, preço, claims
  </methodology>
  
  <output_format>
    ```json
    {
      "competitors": [{
        "product": "...",
        "price": "...",
        "title_pattern": "..."
      }],
      "insights": ["..."]
    }
    ```
  </output_format>
  
  <constraints>
    - Máximo 10 resultados
    - Apenas produtos brasileiros
    - Evitar sellers não oficiais
  </constraints>
</task>
```

**Axioma do Prompt:**  
> "Prompt é contrato. Contrato vago gera entrega vaga. Contrato preciso gera entrega precisa."

---

### **Pilar 4: FERRAMENTAS (Capabilities)**

**Jargão Técnico:** Tool-Augmented LLM  
**Metáfora:** Cérebro com mãos, olhos, ouvidos

```python
# Taxonomia de Ferramentas

NATIVAS (Built-in Claude)
├── bash_tool          # Executa comandos shell
├── view               # Lê arquivos/diretórios
├── create_file        # Cria arquivos
├── str_replace        # Edita arquivos
└── web_search         # Busca na web

EXTERNAS via MCP (Model Context Protocol)
├── google_drive_mcp   # Acessa Google Drive
├── slack_mcp          # Envia/lê mensagens Slack
├── github_mcp         # Opera repositórios GitHub
└── database_mcp       # Queries SQL diretas

CUSTOMIZADAS (Skills)
├── skill_synthesizer  # Resumo inteligente
├── skill_tokenizer    # Extração de entidades
└── skill_qa_gen       # Gera Q&A automaticamente
```

**Axioma das Ferramentas:**  
> "LLM sem ferramentas é poeta. LLM com ferramentas certas é engenheiro."

---

## 🔧 NÍVEL 1: SLASH COMMANDS (Primitivos Atômicos)

**Definição:** Menor unidade executável. Um comando = uma ação determinística.

**Características:**
- ✅ **Atômico:** Faz UMA coisa
- ✅ **Determinístico:** Mesmo input → mesmo output
- ✅ **Composível:** Pode ser combinado com outros
- ✅ **Versionado:** `v1.0.0`, `v1.1.0`, etc.

### **Anatomia de um Slash Command**

```markdown
# ~/.claude/commands/marketplace/extract-price.md

## Nome
extract-price

## Versão
1.0.0

## Objetivo
Extrair preço de URL de marketplace (Mercado Livre, Amazon, Shopee)

## Inputs
- `url`: String (URL completa do produto)
- `marketplace`: Enum('mercadolivre' | 'amazon' | 'shopee')

## Outputs
```json
{
  "price": 45.90,
  "currency": "BRL",
  "original_price": 89.90,
  "discount_percent": 49,
  "shipping": "gratis"
}
```

## Algoritmo
1. `web_fetch(url)`
2. Parse HTML específico do marketplace
3. Extrai seletores:
   - Mercado Livre: `.price-tag-fraction`
   - Amazon: `.a-price-whole`
   - Shopee: `.items-center`
4. Normaliza formato
5. Retorna JSON

## Validação
- [ ] URL é válida
- [ ] Marketplace suportado
- [ ] Preço extraído é numérico
- [ ] Preço > 0

## Exemplo
```bash
/marketplace/extract-price url="https://mercadolivre.com.br/MLB123" marketplace="mercadolivre"
```

## Output Esperado
```json
{"price": 45.90, "currency": "BRL"}
```

## Dependências
- web_fetch (nativo)
- beautifulsoup (Python)

## Autor
Sistema LCM-AI

## Última Modificação
2025-01-10
```

### **Exemplos de Slash Commands Úteis**

```bash
# Extração
/marketplace/extract-price url="..." marketplace="..."
/seo/extract-keywords text="..." max_keywords=10
/image/extract-colors image_url="..." palette_size=5

# Transformação
/text/summarize text="..." max_words=100
/text/translate text="..." target_lang="pt-BR"
/data/json-to-yaml input_file="data.json"

# Validação
/qa/validate-copy copy="..." rules="anvisa"
/qa/check-links markdown_file="README.md"
/qa/lint-code file="script.py" standard="pep8"

# Geração
/gen/uuid count=5
/gen/password length=16 complexity="high"
/gen/mock-data schema="user" count=100
```

**Axioma dos Slash Commands:**  
> "Comando que faz duas coisas deveria ser dois comandos. Atomicidade é virtude, não limitação."

---

## 🧩 NÍVEL 2: SUBAGENTS (Especialistas Isolados)

**Definição:** Contexto de especialização isolado. Um subagent = um especialista com contexto próprio.

**Diferença para Slash Command:**
```
Slash Command:
  - Sem memória
  - Sem contexto persistente
  - Input → Process → Output → Esquece

Subagent:
  - Memória de trabalho
  - Contexto especializado
  - Pode fazer múltiplas chamadas internas
  - Mantém estado durante conversa
```

### **Anatomia de um Subagent**

```python
# subagents/research_specialist.py

class ResearchSpecialist:
    """
    Subagent especializado em market research
    
    Contexto Isolado:
    - Histórico de buscas nesta sessão
    - Padrões identificados acumulativos
    - Insights progressivos
    """
    
    def __init__(self, context: ProjectContext):
        self.context = context
        self.search_history = []
        self.patterns = {}
        self.insights = []
    
    def research_product(
        self, 
        produto: str, 
        marketplaces: List[str]
    ) -> ResearchReport:
        """
        Pesquisa inteligente acumulativa
        """
        
        # Subagent MANTÉM estado entre chamadas
        for marketplace in marketplaces:
            # Chama slash commands internamente
            results = self.call_slash_command(
                '/marketplace/search',
                query=produto,
                marketplace=marketplace
            )
            
            # Acumula conhecimento
            self.search_history.append(results)
            
            # Identifica padrões progressivamente
            new_patterns = self.identify_patterns(results)
            self.patterns.update(new_patterns)
            
            # Gera insights incrementais
            new_insights = self.generate_insights(
                current_results=results,
                accumulated_knowledge=self.patterns
            )
            self.insights.extend(new_insights)
        
        # Consolida tudo
        return ResearchReport(
            history=self.search_history,
            patterns=self.patterns,
            insights=self.insights
        )
    
    def call_slash_command(self, command: str, **kwargs):
        """Subagent pode chamar slash commands"""
        # Implementação...
```

### **Quando usar Subagent vs Slash Command?**

```python
# Cenário 1: Simples, sem estado
✅ Slash Command
extract_price(url) → price
# Não precisa lembrar nada

# Cenário 2: Complexo, com estado
✅ Subagent
research_specialist.research_product(...)
# Precisa:
# - Acumular buscas
# - Identificar padrões entre buscas
# - Gerar insights progressivos
```

**Axioma dos Subagents:**  
> "Se precisa lembrar, é subagent. Se não precisa lembrar, é slash command."

---

## 🔌 NÍVEL 3: MCP (Model Context Protocol)

**Definição:** Ponte entre Claude e serviços externos. Um MCP = uma integração padronizada.

**Jargão Técnico:** Standardized External Service Integration  
**Metáfora:** Tomadas universais para diferentes aparelhos

### **Arquitetura MCP**

```
┌─────────────┐
│   CLAUDE    │
└──────┬──────┘
       │
       │ MCP Protocol (JSON-RPC)
       │
┌──────▼──────────────────────────┐
│   MCP SERVER (Python/Node)      │
├─────────────────────────────────┤
│  - Handle requests              │
│  - Authenticate                 │
│  - Transform data               │
│  - Return standardized format   │
└──────┬──────────────────────────┘
       │
       │ API Calls
       │
┌──────▼──────────┐
│  EXTERNAL       │
│  SERVICE        │
│  (Drive/Slack)  │
└─────────────────┘
```

### **Exemplo: Google Drive MCP**

```python
# mcp_servers/google_drive_mcp.py

from anthropic import MCPServer

class GoogleDriveMCP(MCPServer):
    """
    MCP para integração com Google Drive
    """
    
    def __init__(self):
        super().__init__(name="google_drive")
        self.client = self.authenticate_google()
    
    @mcp_tool
    def search_files(
        self,
        query: str,
        file_type: Optional[str] = None,
        max_results: int = 10
    ) -> List[Dict]:
        """
        Busca arquivos no Google Drive
        
        Args:
            query: Termo de busca
            file_type: 'pdf' | 'docx' | 'xlsx' | None
            max_results: Máximo de resultados
            
        Returns:
            Lista de arquivos encontrados
        """
        
        # Monta query do Drive
        drive_query = f"name contains '{query}'"
        if file_type:
            mime_type = self.get_mime_type(file_type)
            drive_query += f" and mimeType='{mime_type}'"
        
        # Busca
        results = self.client.files().list(
            q=drive_query,
            pageSize=max_results,
            fields="files(id, name, mimeType, webViewLink)"
        ).execute()
        
        # Padroniza output
        return [
            {
                'id': file['id'],
                'name': file['name'],
                'type': file['mimeType'],
                'url': file['webViewLink']
            }
            for file in results.get('files', [])
        ]
    
    @mcp_tool
    def read_file(self, file_id: str) -> str:
        """Lê conteúdo de arquivo"""
        # Implementação...
    
    @mcp_tool  
    def create_file(
        self,
        name: str,
        content: str,
        folder_id: Optional[str] = None
    ) -> Dict:
        """Cria novo arquivo"""
        # Implementação...
```

### **Como Claude usa MCP**

```python
# Claude Code internamente faz:

# 1. Detecta necessidade de tool externo
user_query = "Encontre o arquivo 'vendas_2024.xlsx' no meu Drive"

# 2. Identifica MCP apropriado
mcp = load_mcp("google_drive")

# 3. Chama tool do MCP
results = mcp.search_files(
    query="vendas_2024.xlsx",
    file_type="xlsx"
)

# 4. Usa resultado no contexto
response = f"Encontrei: {results[0]['name']} - {results[0]['url']}"
```

### **MCPs Essenciais**

```yaml
# ~/.claude/mcp_config.yml

mcps:
  google_drive:
    enabled: true
    auth_method: "oauth2"
    scopes: ["drive.readonly", "drive.file"]
    
  slack:
    enabled: true
    workspace: "belaskin-team"
    channels: ["#marketing", "#vendas"]
    
  github:
    enabled: true
    repos: ["belaskin/ads-factory"]
    
  notion:
    enabled: true
    database_id: "abc123xyz"
    
  database:
    enabled: true
    connection_string: "postgresql://..."
    read_only: true
```

**Axioma dos MCPs:**  
> "Serviço externo sem MCP é inseguro. MCP mal feito é pior que não ter. Padronização é segurança."

---

## 🌿 NÍVEL 4: SKILLS (Workflows Autônomos)

**Definição:** Orquestração de múltiplos comandos/subagents/MCPs para realizar workflow completo.

**Diferença fundamental:**
```
Slash Command: Ação atômica
Subagent: Especialista com estado
MCP: Integração externa
Skill: ORQUESTRAÇÃO de todos acima
```

### **Anatomia de um Skill**

```python
# skills/marketplace_listing_skill.py

class MarketplaceListingSkill:
    """
    Skill completo: Brief → Anúncio pronto
    
    Orquestra:
    - 3 Subagents (Research, Copy, Visual)
    - 15+ Slash Commands
    - 2 MCPs (Drive, Midjourney)
    """
    
    def __init__(self):
        # Subagents
        self.research = ResearchSpecialist()
        self.copy = CopySpecialist()
        self.visual = VisualSpecialist()
        
        # MCPs
        self.drive_mcp = load_mcp('google_drive')
        self.mj_mcp = load_mcp('midjourney')
    
    def execute(self, brief: Dict) -> ListingPackage:
        """
        Workflow completo autônomo
        """
        
        # STAGE 1: Research
        # Usa: Subagent + MCPs + Slash Commands
        research_notes = self.research.research_product(
            produto=brief['produto'],
            marketplaces=brief['marketplaces']
        )
        
        # Salva no Drive (MCP)
        research_file = self.drive_mcp.create_file(
            name=f"research_{brief['produto']}.md",
            content=research_notes.to_markdown()
        )
        
        # STAGE 2: Copy
        # Usa: Subagent + Slash Commands
        copy_pack = self.copy.generate_copy(
            brief=brief,
            research=research_notes
        )
        
        # Valida compliance (Slash Command)
        compliance = self.call_slash_command(
            '/qa/validate-copy',
            copy=copy_pack.to_json(),
            rules='anvisa'
        )
        
        if not compliance['passed']:
            # Re-gera com ajustes
            copy_pack = self.copy.regenerate_with_fixes(
                original=copy_pack,
                issues=compliance['issues']
            )
        
        # Salva no Drive
        copy_file = self.drive_mcp.create_file(
            name=f"copy_{brief['produto']}.json",
            content=copy_pack.to_json()
        )
        
        # STAGE 3: Visual
        # Usa: Subagent + MCP Externo + Slash Commands
        shotlist = self.visual.generate_shotlist(
            research=research_notes,
            copy=copy_pack
        )
        
        # Gera imagens via Midjourney MCP
        images = []
        for scene in shotlist:
            image = self.mj_mcp.imagine(
                prompt=scene.midjourney_prompt,
                aspect_ratio="1:1"
            )
            images.append(image)
        
        # Compõe grid 3x3 (Slash Command)
        grid = self.call_slash_command(
            '/image/compose-grid',
            images=images,
            layout='3x3'
        )
        
        # Salva no Drive
        grid_file = self.drive_mcp.upload_file(
            name=f"grid_{brief['produto']}.png",
            file_data=grid
        )
        
        # STAGE 4: Package Final
        return ListingPackage(
            research_file=research_file,
            copy_file=copy_file,
            grid_file=grid_file,
            timestamp=datetime.now(),
            status='ready'
        )
```

### **Skills Essenciais no LCM-AI**

```python
# Transformação de Documentos
skill_synthesizer      # 100 páginas → 1 página
skill_tokenizer        # Extrai entidades/keywords
skill_purpose_extractor # Classifica propósito
skill_qa_generator     # Gera Q&A automaticamente
skill_evaluator        # Score de qualidade

# Criação de Conteúdo
skill_marketplace_listing  # Brief → Anúncio completo
skill_blog_post           # Tópico → Artigo SEO
skill_social_media_pack   # Ideia → Posts 7 plataformas

# Análise e Intelligence
skill_competitor_analysis  # URLs → Benchmark report
skill_sentiment_analysis   # Reviews → Insights
skill_trend_detector       # Keywords → Trend report
```

**Axioma dos Skills:**  
> "Skill não é comando grande. Skill é orquestração inteligente de comandos pequenos."

---

## 📦 NÍVEL 5: PLUGINS (Sistemas Compartilháveis)

**Definição:** Bundle completo de skills + subagents + MCPs + configs empacotados para distribuição.

**Metáfora:** Plugin = órgão transplantável entre organismos

### **Anatomia de um Plugin**

```
marketplace-optimizer-plugin/
├── README.md                    # Documentação
├── plugin.yml                   # Manifest
├── skills/                      # Skills incluídos
│   ├── listing_skill.py
│   └── competitor_skill.py
├── subagents/                   # Subagents incluídos
│   ├── research_specialist.py
│   └── copy_specialist.py
├── commands/                    # Slash commands incluídos
│   └── marketplace/
│       ├── extract-price.md
│       └── search-product.md
├── mcps/                        # MCPs necessários
│   └── requirements.txt         # (referências)
├── context/                     # Configs padrão
│   └── defaults.yml
├── tests/                       # Testes automatizados
│   ├── test_skills.py
│   └── test_integration.py
└── examples/                    # Exemplos de uso
    └── quickstart.md
```

### **Plugin Manifest**

```yaml
# plugin.yml

name: "marketplace-optimizer"
version: "2.1.0"
author: "LCM-AI Team"
license: "MIT"
description: "Complete marketplace listing optimization toolkit"

requirements:
  claude_version: ">=sonnet-4-5"
  python_version: ">=3.10"
  
dependencies:
  mcps:
    - google_drive: ">=1.0.0"
    - midjourney: ">=2.0.0"
  python_packages:
    - beautifulsoup4: ">=4.12.0"
    - requests: ">=2.31.0"

includes:
  skills:
    - marketplace_listing_skill
    - competitor_analysis_skill
  subagents:
    - research_specialist
    - copy_specialist
    - visual_specialist
  commands:
    - marketplace/extract-price
    - marketplace/search-product
    - seo/extract-keywords

configuration:
  defaults_file: "context/defaults.yml"
  customizable:
    - marketplaces_list
    - brand_guidelines
    - compliance_rules

installation:
  auto_setup: true
  requires_auth:
    - google_drive
    - midjourney
```

### **Como Instalar/Usar Plugin**

```bash
# Instalação
claude plugin install marketplace-optimizer

# Configuração
claude plugin configure marketplace-optimizer \
  --marketplaces "mercadolivre,amazon" \
  --brand-file "my-brand.yml"

# Uso
claude run marketplace-optimizer \
  --brief "brief.yml" \
  --output "outputs/"

# Resultado:
# outputs/
#   ├── research_notes.md
#   ├── copy_pack.json
#   └── visual_grid.png
```

**Axioma dos Plugins:**  
> "Plugin bem feito instala em 1 comando, usa em 2, entrega valor em 3. Plugin mal feito confunde em 1, quebra em 2, abandona em 3."

---

## 🔄 HIERARQUIA COMPLETA: COMPOSIÇÃO

### **Visualização da Pirâmide**

```
               ┌──────────────┐
               │   PLUGIN     │ (Bundle compartilhável)
               └──────┬───────┘
                      │
               ┌──────▼───────┐
               │    SKILL     │ (Orquestração autônoma)
               └──────┬───────┘
                      │
          ┌───────────┼───────────┐
          │           │           │
    ┌─────▼─────┐ ┌──▼──┐ ┌─────▼─────┐
    │ SUBAGENT  │ │ MCP │ │   SLASH   │
    │(Contexto) │ │(Ext)│ │  COMMAND  │
    └───────────┘ └─────┘ └───────────┘
```

### **Regras de Composição**

```python
# Regra 1: Slash Commands são indivisíveis
❌ Slash command que chama outro slash command diretamente
✅ Skill que orquestra múltiplos slash commands

# Regra 2: Subagents podem usar Slash Commands
✅ Subagent.call_slash_command('/extract-price', ...)

# Regra 3: Skills orquestram tudo
✅ Skill usa: Subagents + MCPs + Slash Commands

# Regra 4: Plugins empacotam, não executam
✅ Plugin contém Skills
❌ Plugin executa diretamente

# Regra 5: MCPs são pontes, não orquestradores
✅ MCP expõe ferramentas
❌ MCP não orquestra workflow
```

---

## 🎯 DECISÃO: QUANDO USAR CADA NÍVEL?

### **Árvore de Decisão**

```
PERGUNTA 1: Precisa estado/memória entre chamadas?
├─ NÃO → Slash Command
└─ SIM → PERGUNTA 2

PERGUNTA 2: É integração externa?
├─ SIM → MCP
└─ NÃO → PERGUNTA 3

PERGUNTA 3: É workflow com múltiplas etapas?
├─ SIM → Skill
└─ NÃO → Subagent

PERGUNTA 4: Quer distribuir/compartilhar?
└─ SIM → Plugin (empacota Skill)
```

### **Exemplos Práticos**

```python
# Caso 1: "Extrair preço de URL"
→ Slash Command (/marketplace/extract-price)
Motivo: Ação atômica, sem estado

# Caso 2: "Pesquisar produto acumulando insights"
→ Subagent (ResearchSpecialist)
Motivo: Precisa estado entre buscas

# Caso 3: "Buscar arquivos no Google Drive"
→ MCP (google_drive_mcp)
Motivo: Integração externa padronizada

# Caso 4: "Brief → Anúncio completo (research+copy+visual)"
→ Skill (marketplace_listing_skill)
Motivo: Workflow multi-etapas

# Caso 5: "Sistema completo para distribuir"
→ Plugin (marketplace-optimizer-plugin)
Motivo: Bundle para compartilhar
```

---

## 📚 GLOSSÁRIO TÉCNICO

| Termo | Definição | Metáfora |
|-------|-----------|----------|
| **Core-4** | 4 pilares: Contexto, Modelos, Prompt, Ferramentas | Fundação da casa |
| **Slash Command** | Primitivo atômico determinístico | Átomo |
| **Subagent** | Especialista com contexto persistente | Molécula |
| **MCP** | Integração externa padronizada | Célula |
| **Skill** | Orquestração autônoma de workflow | Órgão |
| **Plugin** | Bundle distribuível | Organismo |
| **Atomicidade** | Propriedade de fazer UMA coisa | Indivisibilidade |
| **Composabilidade** | Capacidade de combinar | LEGO |
| **Determinismo** | Mesmo input → mesmo output | Previsibilidade |

---

## 🔮 EVOLUÇÃO FUTURA

```
Versão Atual
├── Hierarquia de 5 níveis
├── MCPs manuais
└── Plugins estáticos

Versão 2.0
├── Auto-geração de Slash Commands
├── MCPs auto-descobertos
└── Skills que se auto-otimizam

Versão 3.0
├── Plugins que evoluem com uso
├── Hierarquia dinâmica (auto-reorganiza)
└── Emergência de novos níveis
```

---

## 📖 REFERÊNCIAS

- **Model Context Protocol:**
  - Spec: https://modelcontextprotocol.io
  - Examples: https://github.com/anthropics/mcp-examples

- **Claude Code:**
  - Docs: https://docs.claude.com/code
  - Best Practices: https://docs.anthropic.com

- **Agent Architectures:**
  - "Building LLM-Powered Applications" (O'Reilly)
  - Anthropic Research Papers

---

## 🎯 CONCLUSÃO

A **hierarquia Claude Code** é arquitetura, não acidente:

✅ **Slash Commands** → Primitivos atômicos  
✅ **Subagents** → Especialistas com memória  
✅ **MCPs** → Pontes externas seguras  
✅ **Skills** → Orquestradores autônomos  
✅ **Plugins** → Sistemas distribuíveis  

**Axioma Final:**  
> "Hierarquia não é burocracia. É clareza. Sem hierarquia, sistema colapsa em complexidade. Com hierarquia, sistema escala em elegância."

---

**Próximo Documento:** `04_CONHECIMENTO_APRENDIZADO_META.md`  
*Consolidando meta-conhecimento, SFT, DPO, destilação e como LLMs aprendem*
