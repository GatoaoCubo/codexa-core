# LlamaIndex Overview & Core Concepts Guide

**Fonte**: developers.llamaindex.ai
**Atualizado**: 2025-12-02
**Categoria**: FRAMEWORKS
**Plataforma**: LlamaIndex

---

## What is LlamaIndex?

LlamaIndex is a framework designed to build LLM-powered agents and applications that work with your data. The platform bridges the gap between large language models and proprietary information.

> "Your data may be private or specific to the problem you're trying to solve. It's behind APIs, in SQL databases, or trapped in PDFs and slide decks."

---

## Core Concept: Context Augmentation

The fundamental problem LlamaIndex solves: LLMs possess broad training but lack access to organization-specific data.

Context augmentation makes your proprietary information available to LLMs, enabling accurate, relevant responses grounded in your actual data.

---

## Key Components

### Data Infrastructure

| Component | Description |
|-----------|-------------|
| **Data Connectors** | Ingest from APIs, PDFs, databases, etc. |
| **Data Indexes** | Structure info for LLM consumption |
| **Query Engines** | Q&A interfaces |
| **Chat Engines** | Conversational interfaces |

### Agent & Workflow Capabilities

| Component | Description |
|-----------|-------------|
| **Agents** | LLM-powered assistants with tools |
| **Workflows** | Event-driven multi-step processes |

### Supporting Features
- Observability/Evaluation
- Vector Indexing
- Semantic Search

---

## Retrieval-Augmented Generation (RAG)

The most common implementation pattern:

```
Query → Retrieve Relevant Context → Augment Prompt → LLM Response
```

Ensures responses are grounded in actual information rather than hallucinated content.

---

## Primary Use Cases

- Question-answering systems
- Intelligent chatbots
- Document understanding and data extraction
- Autonomous research agents
- Multi-modal applications
- Model fine-tuning

---

## Quick Start Implementation

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Load documents
documents = SimpleDirectoryReader("data").load_data()

# Create index
index = VectorStoreIndex.from_documents(documents)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("your question")
```

---

## Architecture Layers

| Level | For | Features |
|-------|-----|----------|
| **High-Level** | Beginners | 5 lines of code implementation |
| **Low-Level** | Advanced | Custom connectors, indices, retrievers |

---

## Availability

| Platform | Status |
|----------|--------|
| Python | ✅ Primary |
| TypeScript | ✅ Available |
| LlamaCloud | Enterprise managed service |

---

## Aplicação CODEXA

**Quando usar este conhecimento:**
- Ao implementar RAG (Retrieval-Augmented Generation)
- Ao construir sistemas de Q&A sobre documentos
- Ao indexar conhecimento para busca semântica
- Ao criar chatbots com dados proprietários

**Tags**: llamaindex, rag, indexing, vector_stores, embeddings, retrieval
