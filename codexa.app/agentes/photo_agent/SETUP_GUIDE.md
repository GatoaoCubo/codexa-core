# Photo Agent - Guia de Configuração Completo

**Configuração do zero para qualquer usuário**

Este guia mostra como configurar o photo_agent com geração automática de imagens usando Google AI Studio / Imagen API.

---

## 📋 Pré-requisitos

- Python 3.8+
- Conta Google (gratuita)
- Acesso à internet

---

## 🚀 Setup Rápido (5 minutos)

### Passo 1: Obter API Key do Google AI Studio

1. Acesse: **https://aistudio.google.com/app/apikey**
2. Faça login com sua conta Google
3. Clique em **"Create API Key"** ou **"Get API Key"**
4. Copie a chave gerada (começa com `AIzaSy...`)

**Importante**: Esta chave é GRATUITA e vem com quota generosa para uso pessoal.

---

### Passo 2: Configurar Arquivo .env

#### 2.1 Navegar até a pasta raiz do projeto

```bash
cd codexa.app
```

#### 2.2 Copiar arquivo de exemplo

**Windows (PowerShell/CMD):**
```bash
copy .env.example .env
```

**Linux/Mac:**
```bash
cp .env.example .env
```

#### 2.3 Editar o arquivo .env

Abra o arquivo `.env` em qualquer editor de texto e substitua:

```bash
# ANTES
GOOGLE_API_KEY=your_google_api_key_here

# DEPOIS (com sua chave real)
GOOGLE_API_KEY=AIzaSyC_sua_chave_aqui_abc123
```

**Salve o arquivo!**

---

### Passo 3: Verificar Configuração

```bash
python config/secrets.py
```

**Saída esperada:**
```
✓ Google API Key: AIzaSyC...
```

Se aparecer erro, revise o Passo 2.

---

## 🎨 Teste Rápido - Gerar Primeira Imagem

### Teste 1: Imagem Simples

```bash
cd agentes/photo_agent

python api_integrations/google_imagen.py \
  "Professional product photography of a red apple on white background, studio lighting, 8K" \
  --output test_image.png
```

**Resultado**: `test_image.png` criado com sucesso!

### Teste 2: Com Python

```python
from api_integrations.google_imagen import generate_image_with_prompt

result = generate_image_with_prompt(
    prompt="Professional photo of thermal water bottle, minimalist studio, 8K",
    output_path="my_product.png"
)

if result.success:
    print(f"✓ Imagem salva: {result.output_path}")
else:
    print(f"✗ Erro: {result.error_message}")
```

---

## 📖 Configurações Avançadas (Opcional)

### Modelos Disponíveis

O photo_agent suporta 3 modelos principais:

```python
# No arquivo .env, você pode configurar:

# Modelo padrão (recomendado - Nano Banana)
# Mais estável, melhor qualidade
DEFAULT_MODEL=gemini-2.5-flash-image-preview

# Alternativas:
# - gemini-2.0-flash-exp-image-generation (mais rápido)
# - gemini-3-pro-image-preview (premium, futuro)
```

### Ajustar Timeouts e Limites

```bash
# No arquivo .env:

# Timeout para requisições API (segundos)
GOOGLE_API_TIMEOUT=30

# Tamanho máximo de imagem de referência (MB)
MAX_IMAGE_SIZE_MB=10
```

---

## 🔧 Troubleshooting

### Erro: "API key not configured"

**Solução:**
1. Verifique se o arquivo `.env` existe em `codexa.app/.env`
2. Verifique se a linha `GOOGLE_API_KEY=` tem sua chave real
3. NÃO deixe espaços antes ou depois do `=`

### Erro: "Quota exceeded"

**Solução:**
1. Aguarde alguns segundos e tente novamente
2. Verifique seu uso em: https://ai.dev/usage?tab=rate-limit
3. O tier gratuito tem limites diários - pode precisar esperar reset

### Erro: "HTTP 500 Internal Error"

**Solução:**
1. O modelo pode estar temporariamente indisponível
2. Tente usar modelo alternativo:
```python
result = generate_image_with_prompt(
    prompt="...",
    model="gemini-2.0-flash-exp-image-generation"
)
```

### Erro: "Image too large"

**Solução:**
1. Redimensione sua imagem de referência
2. Use ferramentas como ImageMagick ou PIL:
```python
from PIL import Image
img = Image.open("produto.jpg")
img.thumbnail((2048, 2048))
img.save("produto_resized.jpg")
```

---

## 📊 Limites e Custos

### Tier Gratuito (Google AI Studio)

- **Custo**: R$ 0,00 (gratuito)
- **Limite**: ~50-100 imagens/dia (pode variar)
- **Qualidade**: Alta (1024x1024 pixels)
- **Modelos**: Todos disponíveis

### Se precisar de mais

1. Acesse: https://console.cloud.google.com
2. Ative billing no Google Cloud
3. Custos aproximados:
   - **Flash model**: ~$0.02/imagem
   - **Pro model**: ~$0.05/imagem

---

## 🎯 Próximos Passos

Agora que está configurado:

1. **Gerar 9 cenas de produto**: Use o workflow completo
2. **Adicionar imagens de referência**: Para máxima fidelidade
3. **Otimizar para marketplaces**: Mercado Livre, Shopee, Amazon
4. **Aplicar branding**: Cores e estilos da marca

**Ver workflows completos**: `workflows/110_ADW_IMAGE_TO_IMAGE.md`

---

## 🔒 Segurança

### IMPORTANTE: Proteja sua API Key

✅ **NUNCA** commite o arquivo `.env` no git
✅ **NUNCA** compartilhe sua API key publicamente
✅ **SEMPRE** use `.env.example` como template
✅ O arquivo `.gitignore` já protege `.env` automaticamente

Se você acidentalmente expôs sua chave:
1. Acesse https://aistudio.google.com/app/apikey
2. Revogue a chave antiga
3. Crie uma nova chave
4. Atualize seu `.env`

---

## 📚 Documentação Adicional

- **Quick Start API**: `QUICKSTART_API.md`
- **Workflows**: `INSTRUCTIONS.md`
- **Schemas**: `schemas/SCHEMAS_GUIDE.md`
- **Exemplos**: `examples/`

---

## 💬 Suporte

**Problemas?**
- Verifique `QUICKSTART_API.md` seção Troubleshooting
- Revise os logs de erro completos
- Teste com modelo alternativo

---

**Versão**: 1.0.0
**Última atualização**: 2025-11-24
**Compatível com**: Python 3.8+, Google AI Studio API v1beta
