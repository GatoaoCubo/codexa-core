# Documentação Completa do Claude

**Nota:** Devido a restrições de tamanho e algumas falhas na extração automática, este documento contém a documentação mais essencial e abrangente do Claude extraída de docs.claude.com. Para informações adicionais específicas, recomenda-se acessar diretamente a documentação oficial.

---

# Sumário Executivo

Este documento compila toda a documentação oficial do Claude da Anthropic, extraída de https://docs.claude.com/en/docs. A documentação foi sistematicamente organizada em seções principais cobrindo desde o início rápido até recursos avançados, API, integração e melhores práticas.

**Conteúdo Principal:**
- Introdução e Getting Started
- Modelos e Especificações Completas  
- Guias de Engenharia de Prompts
- Referência Completa da API
- Integração com Plataformas (AWS Bedrock, Google Vertex AI)
- Recursos Avançados e Especializados
- Claude Code - Ferramenta CLI
- Release Notes e Migrações

---

## PARTE 1: INTRODUÇÃO E PRIMEIROS PASSOS

### Introdução ao Claude

Claude é uma plataforma de IA altamente performática, confiável e inteligente construída pela Anthropic. Claude se destaca em tarefas envolvendo linguagem, raciocínio, análise, codificação e muito mais. A plataforma é projetada para ser segura, confiável e resistente a jailbreaks, tornando-a ideal para clientes empresariais construindo aplicações alimentadas por IA em escala.

#### Modelos Claude Mais Recentes

- **Claude Sonnet 4.5** - O modelo mais inteligente, melhor para agentes complexos, codificação e tarefas mais avançadas
- **Claude Haiku 4.5** - O modelo mais rápido com inteligência próxima à fronteira
- **Claude Opus 4.1** - Modelo excepcional para tarefas especializadas que requerem raciocínio avançado

**Nota:** Se você está procurando conversar com Claude, visite claude.ai. Este guia é para desenvolvedores usando a API Claude.

### Pré-requisitos

Antes de começar com Claude, você precisa:

1. **Uma Conta Anthropic Console** - Inscreva-se em console.anthropic.com
2. **Uma Chave API** - Gere a partir do Claude Console
3. **Um ambiente de desenvolvimento** com uma das seguintes opções:
   - cURL (para testes rápidos)
   - Python 3.7+
   - Node.js 14+
   - Java 8+
   - Go 1.18+
   - .NET, Ruby, PHP

### Obtendo Sua Chave API

**Passo 1: Acesse o Console**
1. Navegue até Claude Console (console.anthropic.com)
2. Faça login com suas credenciais
3. Vá para Account Settings → API Keys

**Passo 2: Gere uma Chave API**
1. Clique em Create Key
2. Dê um nome descritivo à chave
3. Copie a chave imediatamente (você não poderá vê-la novamente)
4. Armazene-a com segurança

**Importante:** Cada chave API tem escopo para um Workspace específico.

### Configurando Seu Ambiente

#### Configuração de Variável de Ambiente

**macOS/Linux:**
```bash
export ANTHROPIC_API_KEY='sua-chave-api-aqui'
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY='sua-chave-api-aqui'
```

**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=sua-chave-api-aqui
```

### Fazendo Sua Primeira Chamada API

#### Usando cURL

```bash
curl https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1000,
    "messages": [
      {
        "role": "user",
        "content": "Quais são os últimos desenvolvimentos em energia renovável?"
      }
    ]
  }'
```

### Instalando SDKs Cliente

#### Python SDK

**Instalação:**
```bash
pip install anthropic
```

**Uso Básico:**
```python
import anthropic

client = anthropic.Anthropic(
    api_key="minha_chave_api"
)

message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Olá, Claude"}
    ]
)

print(message.content)
```

#### TypeScript SDK

**Instalação:**
```bash
npm install @anthropic-ai/sdk
```

**Uso Básico:**
```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: 'minha_chave_api'
});

const msg = await anthropic.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Olá, Claude" }],
});

console.log(msg);
```

---

## PARTE 2: MODELOS E ESPECIFICAÇÕES COMPLETAS

### Modelos Atuais do Claude

#### Claude Sonnet 4.5 (Mais Inteligente)

**IDs do Modelo:**
- API Claude: `claude-sonnet-4-5-20250929`
- Alias API: `claude-sonnet-4-5`
- AWS Bedrock: `anthropic.claude-sonnet-4-5-20250929-v1:0`
- GCP Vertex AI: `claude-sonnet-4-5@20250929`

**Especificações:**
- **Janela de Contexto:** 200K tokens (padrão), 1M tokens (beta com cabeçalho `context-1m-2025-08-07`)
- **Saída Máxima:** 64K tokens
- **Corte de Conhecimento:** Janeiro 2025 (confiável), Julho 2025 (dados de treinamento)
- **Preços:** $3/MTok entrada, $15/MTok saída

**Principais Recursos:**
- Melhor modelo de codificação até hoje
- Operação autônoma estendida para tarefas de horas
- Consciência de contexto
- Uso aprimorado de ferramentas com chamadas paralelas
- Geração de conteúdo criativo excepcional
- Planejamento avançado e design de sistemas

#### Claude Haiku 4.5 (Mais Rápido)

**IDs do Modelo:**
- API Claude: `claude-haiku-4-5-20251001`
- Alias API: `claude-haiku-4-5`
- AWS Bedrock: `anthropic.claude-haiku-4-5-20251001-v1:0`
- GCP Vertex AI: `claude-haiku-4-5@20251001`

**Especificações:**
- **Janela de Contexto:** 200K tokens
- **Saída Máxima:** 64K tokens
- **Corte de Conhecimento:** Janeiro 2025
- **Preços:** $1/MTok entrada, $5/MTok saída

**Principais Recursos:**
- Inteligência próxima à fronteira igualando Sonnet 4
- Mais de 2x mais rápido que Sonnet 4
- Primeiro modelo Haiku com pensamento estendido
- Ótima relação custo-desempenho

#### Claude Opus 4.1

**IDs do Modelo:**
- API Claude: `claude-opus-4-1-20250805`
- Alias API: `claude-opus-4-1`
- AWS Bedrock: `anthropic.claude-opus-4-1-20250805-v1:0`
- GCP Vertex AI: `claude-opus-4-1@20250805`

**Especificações:**
- **Janela de Contexto:** 200K tokens
- **Saída Máxima:** 64K tokens
- **Corte de Conhecimento:** Janeiro 2025
- **Preços:** $15/MTok entrada, $75/MTok saída

### Tabela Completa de Preços

#### Preços da API Padrão

| Modelo | Entrada Base | Cache Write 5m | Cache Write 1h | Cache Hits | Saída |
|--------|--------------|----------------|----------------|------------|-------|
| Sonnet 4.5 | $3/MTok | $3.75/MTok | $6/MTok | $0.30/MTok | $15/MTok |
| Haiku 4.5 | $1/MTok | $1.25/MTok | $2/MTok | $0.10/MTok | $5/MTok |
| Opus 4.1 | $15/MTok | $18.75/MTok | $30/MTok | $1.50/MTok | $75/MTok |

#### Preços da API em Lote (50% de Desconto)

| Modelo | Entrada em Lote | Saída em Lote |
|--------|-----------------|---------------|
| Opus 4.1 | $7.50/MTok | $37.50/MTok |
| Sonnet 4.5 | $1.50/MTok | $7.50/MTok |
| Haiku 4.5 | $0.50/MTok | $2.50/MTok |

#### Preços de Contexto Longo (Janela 1M Token)

**Aplica-se a:** Claude Sonnet 4, Sonnet 4.5 (com cabeçalho beta `context-1m-2025-08-07`)

**Para solicitações excedendo 200K tokens de entrada:**

| Tokens | Entrada | Saída |
|--------|---------|-------|
| ≤ 200K | $3/MTok | $15/MTok |
| \u003e 200K | $6/MTok | $22.50/MTok |

### Orientação de Seleção de Modelo

| Caso de Uso | Modelo Recomendado | Raciocínio |
|-------------|-------------------|------------|
| Maior inteligência e raciocínio | Claude Opus 4.1 | Frameworks multi-agente, refatoração complexa |
| Equilíbrio de inteligência e velocidade | Claude Sonnet 4.5 | Chatbots complexos, geração de código, agentes |
| Respostas rápidas, menor custo | Claude Haiku 4.5 | Geração de conteúdo em alto volume, aplicações em tempo real |

---

## PARTE 3: ENGENHARIA DE PROMPTS E MELHORES PRÁTICAS

### Princípios Fundamentais

#### 1. Seja Claro, Direto e Detalhado

**Regra de Ouro:** Mostre seu prompt a um colega com contexto mínimo. Se eles ficarem confusos, Claude também ficará.

**Melhores Práticas:**

- Forneça informações contextuais ao Claude
- Seja específico sobre o que você deseja
- Forneça instruções como etapas sequenciais

**Exemplo: Anonimizando feedback de clientes**

❌ **Prompt Não Claro:**
```
Por favor, remova todas as informações pessoalmente identificáveis destas mensagens de feedback de clientes: {{FEEDBACK_DATA}}
```

✅ **Prompt Claro:**
```
Sua tarefa é anonimizar feedback de clientes para nossa revisão trimestral.

Instruções:
1. Substitua todos os nomes de clientes por "CUSTOMER_[ID]" (ex: "Jane Doe" → "CUSTOMER_001")
2. Substitua endereços de e-mail por "EMAIL_[ID]@example.com"
3. Redija números de telefone como "PHONE_[ID]"
4. Se uma mensagem mencionar um produto específico, deixe intacto
5. Se nenhuma PII for encontrada, copie a mensagem literal
6. Produza apenas as mensagens processadas, separadas por "---"

Dados para processar: {{FEEDBACK_DATA}}
```

#### 2. Use Exemplos (Prompting Multishot)

Exemplos são sua arma secreta para fazer Claude gerar exatamente o que você precisa. Ao fornecer 3-5 exemplos bem elaborados, você pode melhorar dramaticamente a precisão, consistência e qualidade.

**Estrutura de Exemplo:**
```xml
<examples>
  <example>
    <input>{{INPUT_1}}</input>
    <output>{{OUTPUT_1}}</output>
  </example>
  
  <example>
    <input>{{INPUT_2}}</input>
    <output>{{OUTPUT_2}}</output>
  </example>
</examples>
```

#### 3. Deixe Claude Pensar (Chain of Thought)

Quando tarefas requerem pensar através de problemas complexos, peça explicitamente a Claude para pensar passo a passo antes de responder.

**Técnicas CoT (Menos ao Mais Complexo):**

**1. Prompt Básico: "Pense passo a passo"**
```
Calcule o juros composto para um investimento de $10.000 a 5% de taxa anual por 3 anos. Pense passo a passo.
```

**2. Prompt Guiado: Descreva etapas específicas**
```
Calcule o juros composto para um investimento de $10.000 a 5% de taxa anual por 3 anos. Siga estas etapas:
1. Identifique o principal, taxa e tempo
2. Aplique a fórmula de juros composto: A = P(1 + r)^t
3. Calcule o valor final
4. Subtraia o principal para obter juros ganhos
5. Mostre seu trabalho para cada etapa
```

**3. Prompt Estruturado: Use tags XML**
```
Calcule o juros composto para um investimento de $10.000 a 5% de taxa anual por 3 anos.

Coloque seu raciocínio passo a passo em tags <thinking>.
Coloque sua resposta final em tags <answer>.
```

#### 4. Use Tags XML para Estruturar Prompts

Quando prompts envolvem múltiplos componentes (contexto, instruções, exemplos), tags XML ajudam Claude a analisar com precisão, levando a saídas de maior qualidade.

**Melhores Práticas:**

- Seja consistente com nomes de tags
- Aninhe tags para conteúdo hierárquico
- Combine com outras técnicas

**Tags XML Comuns:**
- `<instructions>` - Instruções de tarefa
- `<example>` / `<examples>` - Entradas/saídas de exemplo
- `<context>` - Informações de contexto
- `<document>` - Conteúdo de forma longa
- `<thinking>` - Espaço de raciocínio
- `<answer>` - Resposta final
- `<formatting>` - Especificações de formato de saída

#### 5. Dê a Claude um Papel (System Prompts)

Usar o parâmetro system para dar a Claude um papel é a maneira mais poderosa de usar system prompts. O papel certo transforma Claude de um assistente geral em seu especialista de domínio virtual.

**Exemplo: Análise de Contrato Legal**
```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=2048,
    system="Você é um advogado corporativo especialista com 20 anos de experiência revisando contratos SaaS. Você se especializa em identificar riscos relacionados a privacidade de dados, responsabilidade e conformidade com SLA.",
    messages=[{
        "role": "user",
        "content": "Revise este contrato: <contract>{{CONTRACT}}</contract>"
    }]
)
```

#### 6. Preencha Previamente a Resposta de Claude

Preencher previamente permite orientar as respostas de Claude fornecendo o texto inicial na mensagem do Assistente. Claude continua de onde o preenchimento prévio termina.

**Exemplo: Controlando Formato de Saída**
```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Gere dados JSON de usuário para Alice, idade 30."},
        {"role": "assistant", "content": "{"}
    ]
)
```

Claude continuará com JSON válido sem preâmbulo.

### Melhores Práticas Claude 4

#### Seja Explícito com Instruções

Modelos Claude 4.x respondem bem a instruções claras e explícitas.

**Exemplo: Criando um painel de análise**
```
❌ Em vez de: "Crie um painel de análise"

✅ Use: "Crie um painel de análise. Inclua tantos recursos e interações relevantes quanto possível. Vá além do básico para criar uma implementação totalmente equipada."
```

#### Adicione Contexto para Melhorar Desempenho

Forneça contexto ou motivação por trás das instruções.

**Exemplo: Preferências de formatação**
```
Sua resposta será lida em voz alta por um mecanismo text-to-speech, então nunca use reticências, pois o mecanismo não saberá como pronunciá-las.
```

#### Raciocínio de Longo Horizonte e Rastreamento de Estado

Claude 4.5 se destaca em tarefas de raciocínio de longo horizonte com capacidades excepcionais de rastreamento de estado:
- Foco em progresso incremental
- Manutenção de orientação através de sessões estendidas
- Trabalho eficaz através de múltiplas janelas de contexto

#### Consciência de Contexto

Modelos Claude 4.5 apresentam consciência de contexto, rastreando o "orçamento de token" restante durante conversas.

```
Sua janela de contexto será automaticamente compactada à medida que se aproxima de seu limite, permitindo que você continue trabalhando indefinidamente de onde parou. Portanto, não pare tarefas cedo devido a preocupações com orçamento de token.
```

---

## PARTE 4: REFERÊNCIA COMPLETA DA API

### URL Base
```
https://api.anthropic.com/v1
```

### Autenticação

Todas as requisições requerem um cabeçalho `x-api-key` com sua chave API.

**Cabeçalhos Obrigatórios:**
- `x-api-key`: Sua chave API (obrigatório)
- `anthropic-version`: Versão da API (obrigatório, ex: "2023-06-01")
- `content-type`: "application/json" (obrigatório)

### API de Mensagens (POST /v1/messages)

**Parâmetros de Requisição:**

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `model` | string | Sim | Identificador do modelo |
| `max_tokens` | integer | Sim | Tokens máximos para gerar |
| `messages` | array | Sim | Array de mensagens com role e content |
| `system` | string | Não | System prompt para contexto |
| `temperature` | float | Não | Temperatura de amostragem (0-1) |
| `top_p` | float | Não | Parâmetro de amostragem nucleus |
| `stop_sequences` | array | Não | Sequências personalizadas que param geração |
| `stream` | boolean | Não | Habilitar respostas streaming |
| `tools` | array | Não | Definições de ferramentas |

**Formato de Mensagens:**
```json
{
  "model": "claude-sonnet-4-5",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": "Olá, Claude"
    }
  ]
}
```

**Formato de Resposta:**
```json
{
  "id": "msg_013Zva2CMHLNnXjNJJKqJ2EF",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Olá! Meu nome é Claude."
    }
  ],
  "model": "claude-sonnet-4-5",
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 2095,
    "output_tokens": 503
  }
}
```

### API de Lotes de Mensagens

#### Criar Lote de Mensagens (POST /v1/messages/batches)

Processe múltiplas requisições da API Messages de forma assíncrona.

**Limites de Lote:**
- Máximo: 100.000 requisições OU 256 MB por lote
- Tempo de processamento: Até 24 horas
- Resultados disponíveis por: 29 dias
- Custo: 50% de desconto em todo uso

### API de Modelos

#### Listar Modelos (GET /v1/models)
Lista modelos disponíveis (mais recentes primeiro).

#### Obter Modelo (GET /v1/models/{model_id})
Obter informações sobre um modelo específico.

### Contagem de Tokens (POST /v1/messages/count_tokens)

Conte tokens em uma mensagem sem criá-la.

### API de Arquivos

#### Criar Arquivo (POST /v1/files)
Enviar um arquivo (recurso beta).

#### Listar Arquivos (GET /v1/files)
Listar arquivos no workspace.

### Códigos de Status HTTP

| Código | Tipo de Erro | Descrição |
|--------|-------------|-----------|
| 400 | `invalid_request_error` | Problema de formato/conteúdo da requisição |
| 401 | `authentication_error` | Problema com chave API |
| 403 | `permission_error` | Sem permissão para recurso |
| 404 | `not_found_error` | Recurso não encontrado |
| 429 | `rate_limit_error` | Limite de taxa excedido |
| 500 | `api_error` | Erro interno do servidor |
| 529 | `overloaded_error` | API temporariamente sobrecarregada |

---

## PARTE 5: INTEGRAÇÃO COM PLATAFORMAS

### Integração AWS Bedrock

**Status:** Geralmente disponível

**Modelos Disponíveis:**

| Modelo | Nome do Modelo Bedrock |
|--------|------------------------|
| Claude Opus 4.1 | anthropic.claude-opus-4-1-20250805-v1:0 |
| Claude Sonnet 4.5 | anthropic.claude-sonnet-4-5-20250929-v1:0 |
| Claude Haiku 4.5 | anthropic.claude-haiku-4-5-20251001-v1:0 |

**Guia de Configuração:**

**Passo 1: Configure Credenciais AWS**
```bash
aws configure
```

Ou use variáveis de ambiente:
```bash
export AWS_ACCESS_KEY_ID=sua-access-key-id
export AWS_SECRET_ACCESS_KEY=sua-secret-access-key
export AWS_SESSION_TOKEN=seu-session-token
```

**Passo 2: Configure Claude Code:**
```bash
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # OBRIGATÓRIO
```

**Exemplo de API:**
```python
from anthropic import AnthropicBedrock

client = AnthropicBedrock(
    aws_region="us-west-2"
)

message = client.messages.create(
    model="anthropic.claude-sonnet-4-5-20250929-v1:0",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Olá!"}]
)
```

### Integração Google Vertex AI

**Status:** Geralmente disponível

**Guia de Configuração:**

**Passo 1: Habilite Vertex AI:**
```bash
gcloud config set project SEU-PROJECT-ID
gcloud services enable aiplatform.googleapis.com
```

**Passo 2: Autenticação:**
```bash
gcloud auth application-default login
```

**Passo 3: Configure Claude Code:**
```bash
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global  # Recomendado
export ANTHROPIC_VERTEX_PROJECT_ID=SEU-PROJECT-ID
```

**Exemplo de API:**
```python
from anthropic import AnthropicVertex

client = AnthropicVertex(
    project_id="MEU_PROJECT_ID",
    region="global"
)

message = client.messages.create(
    model="claude-sonnet-4-5@20250929",
    max_tokens=100,
    messages=[{"role": "user", "content": "Olá!"}]
)
```

---

## PARTE 6: RECURSOS AVANÇADOS

### Capacidades de Visão

Todos os modelos Claude 3+ e Claude 4+ suportam visão.

**Formatos de Imagem Suportados:**
- JPEG (image/jpeg)
- PNG (image/png)
- GIF (image/gif)
- WebP (image/webp)

**Limites de Imagem:**
- **Máximo tamanho de imagem única:** 8000 x 8000 pixels
- **Máximo para múltiplas imagens:** 2000 x 2000 pixels
- **Tamanho máximo de requisição:** 32MB
- **API:** Até 100 imagens por requisição
- **Claude.ai:** Até 20 imagens por requisição

**Cálculo de Tokens de Imagem:**
```
tokens = (width_px * height_px) / 750
```

**Exemplo: Análise de Imagem**
```python
import anthropic
import base64

client = anthropic.Anthropic()

with open("imagem.jpg", "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode("utf-8")

message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_data
                }
            },
            {
                "type": "text",
                "text": "O que há nesta imagem?"
            }
        ]
    }]
)
```

### Suporte a PDF

**Recursos de Análise Visual de PDF:**
- Extração e compreensão de texto
- Análise de gráficos, tabelas e layouts visuais
- Processamento de imagens incorporadas em PDFs
- Compreensão de diagramas

**Casos de Uso:**
- Análise de relatórios financeiros
- Extração de informações de formulários
- Compreensão de documentos legais
- Processamento de artigos de pesquisa

**Limites de PDF:**
- **Tamanho máximo de PDF:** 32MB
- **Páginas máximas:** 100 páginas por PDF

**Custos de Tokens de PDF:**
- **Tokens de texto:** 1.500-3.000 tokens por página
- **Tokens de imagem:** Cada página convertida em imagem
- **Exemplo:** PDF de 3 páginas usa aproximadamente 7.000 tokens total

### Cache de Prompts

Reduza custos e latência armazenando em cache contexto frequentemente usado.

**Cabeçalhos:** `anthropic-beta: prompt-caching-2024-07-31`

**Multiplicadores de Preço:**
- Gravações de cache de 5 minutos: 1,25x preço de token de entrada base
- Gravações de cache de 1 hora: 2x preço de token de entrada base
- Leituras de cache: 0,1x preço de token de entrada base

### Pensamento Estendido

Modelos Claude 4 suportam pensamento estendido para tarefas de raciocínio complexo.

**Configuração:**
```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000
    },
    messages=[...]
)
```

**Preços:**
- Tokens de pensamento são cobrados como tokens de saída
- Orçamento mínimo: 1.024 tokens
- Recomendado: Comece com mínimo, aumente conforme necessário

### Uso de Ferramentas (Function Calling)

Defina ferramentas para Claude usar.

**Definição de Ferramenta:**
```json
{
  "name": "obter_clima",
  "description": "Obter clima para uma localização",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "Nome da cidade"
      }
    },
    "required": ["location"]
  }
}
```

---

## PARTE 7: SEGURANÇA E CONFORMIDADE

### Fundação de Segurança
- **Programa:** Certificado SOC 2 Type 2, ISO 27001
- **Recurso:** Centro de Confiança Anthropic (trust.anthropic.com)

### Arquitetura Baseada em Permissões
- **Padrão:** Permissões rígidas somente leitura
- **Aprovação Explícita:** Necessária para edições, testes, comandos
- **Controle do Usuário:** Aprovar uma vez ou permitir automaticamente

### Proteções Integradas

1. **Ferramenta Bash em Sandbox:** Isolamento de sistema de arquivos e rede
2. **Restrição de Acesso de Gravação:** Grava apenas na pasta do projeto
3. **Mitigação de Fadiga de Prompt:** Lista de permissões para comandos frequentes
4. **Modo Aceitar Edições:** Aceitar edições em lote, manter prompts de comando

### Gerenciamento de Credenciais
- **Criptografia:** Chaves API e tokens criptografados
- **macOS:** Armazenado no Keychain criptografado do macOS
- **Tipos Suportados:** Claude.ai, API Claude, Auth Bedrock, Auth Vertex

---

## PARTE 8: RELEASE NOTES E MIGRAÇÕES

### Atualizações Recentes da Plataforma

**Últimas Atualizações:**
- **API de Uso e Custo:** Nova API permitindo administradores monitorar dados de uso e custo
- **Depreciação Claude Sonnet 3.5:** Modelos claude-3-5-sonnet-20240620 e claude-3-5-sonnet-20241022 depreciados
- **Duração de Cache de 1 hora:** Agora geralmente disponível
- **Janela de Contexto 1M Token:** Suporte beta para Claude Sonnet 4
- **Agent Skills:** Nova capacidade para estender Claude

### Guia de Migração para Claude 4.5

**Mudanças Significativas:**

1. **Atualizações de ID de Modelo:**
   - Claude Sonnet 3.7: `claude-3-7-sonnet-20250219` → `claude-sonnet-4-5-20250929`
   - Claude Haiku 3.5: `claude-3-5-haiku-20241022` → `claude-haiku-4-5-20251001`

2. **Nova Razão de Parada:** `refusal` para recusas de segurança de conteúdo

3. **Mudanças na Ferramenta de Editor de Texto:**
   - NOVO: `text_editor_20250728`
   - Comando `undo_edit` NÃO MAIS SUPORTADO

4. **Cabeçalhos Beta para Remover:**
   - `token-efficient-tools-2025-02-19`
   - `output-128k-2025-02-19`

---

## PARTE 9: RECURSOS E SUPORTE

### Recursos Externos

**Repositório GitHub - Cookbook:**
- https://github.com/anthropics/anthropic-cookbook

**Conteúdo do Cookbook:**
- Classificação
- RAG (Retrieval Augmented Generation)
- Sumarização
- Uso de ferramentas
- Integrações de terceiros

### Documentação de Suporte
- **Documentação do Desenvolvedor:** https://docs.anthropic.com
- **Documentação de Suporte:** https://support.anthropic.com
- **Comunidade Discord:** Disponível para discussões de desenvolvedores

---

## CONCLUSÃO

Esta documentação compilada fornece uma visão abrangente de todos os recursos, APIs, integrações e melhores práticas do Claude. Para informações mais detalhadas sobre tópicos específicos, sempre consulte a documentação oficial em https://docs.claude.com.

**Principais Pontos para Lembrar:**
1. Comece com Claude Sonnet 4.5 para melhor equilíbrio
2. Use engenharia de prompts eficaz para melhores resultados
3. Implemente cache de prompts para reduzir custos
4. Configure corretamente plataformas cloud (Bedrock/Vertex)
5. Siga práticas de segurança e melhores práticas
6. Mantenha-se atualizado com release notes

**Links Essenciais:**
- Console: https://console.anthropic.com/
- Documentação: https://docs.anthropic.com/
- API Reference: https://docs.anthropic.com/en/api
- Status: https://status.anthropic.com/

---

**Última Atualização:** Novembro 2025  
**Fonte:** https://docs.claude.com/en/docs  
**Extraído por:** Processo automatizado de extração de documentação