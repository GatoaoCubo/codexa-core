# Gemini API Documentation Overview

**Fonte**: ai.google.dev/gemini-api/docs
**Atualizado**: 2025-12-02
**Categoria**: LLM_PLATFORMS
**Plataforma**: Google AI

---

## Overview

The Gemini API is Google's developer platform for building with advanced AI models. Supports multiple programming languages: Python, JavaScript, Go, Java, C#, and REST APIs.

---

## Available Models

### Current Generation

| Model | Description |
|-------|-------------|
| **Gemini 3 Pro** | Most intelligent model, best for multimodal understanding |
| **Gemini 2.5 Pro** | Excels at coding and complex reasoning |
| **Gemini 2.5 Flash** | Balanced performance with 1M token context window |
| **Gemini 2.5 Flash-Lite** | Fastest and most cost-efficient multimodal model |

### Specialized Models

| Model | Use Case |
|-------|----------|
| **Veo 3.1** | Video generation with native audio |
| **Nano Banana/Pro** | Image generation and editing |

---

## Core Capabilities

- **Text generation** with various model tiers
- **Multimodal understanding** (images, video, audio, documents)
- **Structured outputs** in JSON format
- **Function calling** for agentic workflows
- **Real-time voice applications** via Live API

### Specific Features

| Feature | Details |
|---------|---------|
| Image understanding | Process and analyze images |
| Video processing | Generate and understand video content |
| Document understanding | Up to 1000 PDF pages |
| Speech generation | Audio output capabilities |
| Long context | Millions of tokens |
| Thinking/reasoning | Step-by-step problem solving |

---

## Tools & Integrations

| Tool | Description |
|------|-------------|
| Google Search | Real-time web grounding |
| Google Maps | Location-based grounding |
| Code execution | Built-in code environment |
| Computer Use | Interface automation |
| File Search | Document retrieval |
| URL context | Web page processing |

---

## Getting Started

- **Free tier** available without billing setup
- **Google AI Studio** for testing and prototyping
- **API keys** managed through AI Studio dashboard

### SDK Installation

```bash
# Python
pip install google-generativeai

# JavaScript
npm install @google/generative-ai
```

### Basic Usage (Python)

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-2.5-flash')

response = model.generate_content("Explain quantum computing")
print(response.text)
```

---

## Pricing Tiers

| Tier | Best For |
|------|----------|
| Flash-Lite | High volume, cost-sensitive |
| Flash | Balanced performance/cost |
| Pro | Maximum capability |

---

## Aplicação CODEXA

**Quando usar este conhecimento:**
- Ao escolher modelos para diferentes tarefas
- Ao implementar multimodal (imagens, vídeo, áudio)
- Ao otimizar custos de LLM
- Ao comparar alternativas ao Claude

**Tags**: gemini, google_ai, multimodal, function_calling, long_context
