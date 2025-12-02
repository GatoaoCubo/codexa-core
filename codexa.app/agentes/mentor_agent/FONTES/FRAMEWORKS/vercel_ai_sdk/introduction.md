# Vercel AI SDK: Introduction & Overview

**Fonte**: ai-sdk.dev/docs/introduction
**Atualizado**: 2025-12-02
**Categoria**: FRAMEWORKS
**Plataforma**: Vercel AI SDK

---

## What is the AI SDK?

The AI SDK is a TypeScript toolkit designed to help developers build AI-powered applications and agents. It provides standardized integrations across multiple LLM providers, enabling developers to focus on building great AI applications rather than managing technical implementation details.

---

## Core Problem It Solves

Integrating large language models into applications is complicated and heavily dependent on specific model providers. The AI SDK addresses this by standardizing how you work with different AI models, regardless of which provider you choose.

---

## Main Features

| Feature | Description |
|---------|-------------|
| **Unified API** | Write code once and switch between LLM providers with minimal changes |
| **Streaming** | Built-in support for real-time data streaming |
| **Tool Calling** | Native support for function calling and tool integration |
| **Structured Data** | Generate and validate structured outputs from LLMs |

---

## Two Primary Libraries

### AI SDK Core
Unified API for:
- Generating text
- Structured objects
- Tool calls
- Building agents

### AI SDK UI
Framework-agnostic hooks for:
- Chat interfaces
- Generative UI components
- Real-time streaming display

---

## Supported Model Providers (25+)

| Provider | Status |
|----------|--------|
| OpenAI | ✅ |
| Anthropic | ✅ |
| Google Generative AI | ✅ |
| xAI Grok | ✅ |
| Amazon Bedrock | ✅ |
| Groq | ✅ |
| Mistral | ✅ |
| Cohere | ✅ |
| DeepSeek | ✅ |
| Vercel AI Gateway | ✅ |

---

## Supported Frameworks

- Next.js (App & Pages Router)
- React
- Vue.js / Nuxt
- Svelte / SvelteKit
- Node.js
- Expo

---

## Quick Example

```typescript
import { generateText } from "ai"

const { text } = await generateText({
  model: "google/gemini-3-pro-preview",
  prompt: "What is love?"
})
```

### Streaming Example

```typescript
import { streamText } from "ai"

const result = await streamText({
  model: openai("gpt-4o"),
  prompt: "Explain quantum computing",
})

for await (const text of result.textStream) {
  console.log(text)
}
```

---

## Aplicação CODEXA

**Quando usar este conhecimento:**
- Ao construir interfaces de chat com IA
- Ao implementar streaming de respostas LLM
- Ao criar aplicações React/Next.js com IA
- Ao unificar múltiplos provedores de LLM

**Tags**: vercel, ai_sdk, streaming, typescript, react, tool_calling
