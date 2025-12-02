# 🌳 MASTER KNOWLEDGE SYSTEM
## LCM-AI + Agentes + Documentação + Claude Code Framework
### Sistema Completo de Gestão de Conhecimento para IA

**Versão:** 2.0  
**Autores:** Sistema LCM-AI Core  
**Propósito:** Documento definitivo integrando arquitetura de conhecimento, workflows de agentes, metodologias de documentação e hierarquia de ferramentas Claude Code

---

## 📚 ÍNDICE NAVEGÁVEL

### PARTE I: FUNDAMENTOS
1. [Visão Geral do Ecossistema](#1-visão-geral)
2. [Princípios Fundamentais](#2-princípios-fundamentais)
3. [Metáfora da Árvore](#3-metáfora-da-árvore)

### PARTE II: ARQUITETURA LCM-AI
4. [Estrutura de Camadas](#4-estrutura-de-camadas)
5. [Raízes (−) - Ingestão e Arquivo](#5-raizes)
6. [Tronco (∞) - Orquestração](#6-tronco)
7. [Galhos (+) - Distribuição](#7-galhos)
8. [Folhas (Skills) - Transformação](#8-folhas)
9. [Fruto (13) - Aplicações](#9-fruto)

### PARTE III: WORKFLOWS DE AGENTES
10. [Framework Genérico de Agentes](#10-framework-agentes)
11. [Agente 1: Research & Intelligence](#11-agente-research)
12. [Agente 2: Copy Generation](#12-agente-copy)
13. [Agente 3: Visual Generation](#13-agente-visual)
14. [Integração e Orquestração](#14-integracao)

### PARTE IV: HIERARQUIA CLAUDE CODE
15. [Core-4: Contexto, Modelos, Prompt, Ferramentas](#15-core-4)
16. [Slash Commands (Primitivos)](#16-slash-commands)
17. [Subagents (Especialização)](#17-subagents)
18. [MCP (Integrações)](#18-mcp)
19. [Skills (Orquestração)](#19-skills)
20. [Plugins (Empacotamento)](#20-plugins)

### PARTE V: META-CONHECIMENTO
21. [Como LLMs Aprendem](#21-como-llms-aprendem)
22. [Destilação de Conhecimento](#22-destilacao)
23. [SFT e DPO para Documentação](#23-sft-dpo)
24. [Formatos Ótimos de Documentação](#24-formatos-otimos)

### PARTE VI: IMPLEMENTAÇÃO
25. [Plano de 6 Dias](#25-plano-6-dias)
26. [Configurações e Templates](#26-configuracoes)
27. [Testes e Validação](#27-testes)
28. [Antipadrões e Boas Práticas](#28-antipadroes)

### PARTE VII: CASOS DE USO
29. [E-commerce e Marketplace](#29-ecommerce)
30. [Documentação Técnica](#30-doc-tecnica)
31. [Gestão de Conhecimento](#31-gestao-conhecimento)

### APÊNDICES
A. [Glossário Completo](#apendice-a)  
B. [Referências e Bibliografia](#apendice-b)  
C. [Cheat Sheets](#apendice-c)

---

## PARTE I: FUNDAMENTOS

### 1. VISÃO GERAL DO ECOSSISTEMA

**O Sistema Integrado:**

```
                    APLICAÇÕES (13)
                         ↑
                    OUTPUTS (+)
                         ↑
        ┌────────────────┼────────────────┐
        │         CORE SYSTEM (∞)         │
        │    Orquestração · Skills        │
        │    Agentes · Documentação       │
        └────────────────┬────────────────┘
                         ↓
                    INPUTS (−)
                         ↓
                   DADOS BRUTOS
```

Este documento integra **4 sistemas complementares**:

1. **LCM-AI**: Arquitetura de gestão de conhecimento (árvore viva)
2. **Workflow de Agentes**: Sistema de 3 agentes especializados
3. **Meta-Guia**: Metodologia de documentação para LLMs
4. **Claude Code Framework**: Hierarquia Slash→Subagent→MCP→Skill→Plugin

**Princípio Unificador:**
> "Conhecimento é vivo quando organizado em camadas, acessível em contextos, e transformável por agentes especializados"

---

### 2. PRINCÍPIOS FUNDAMENTAIS

#### 2.1 Princípio do Prompt
> **"The prompt is the new fundamental unit of knowledge work"**

- Todo trabalho começa com um prompt bem estruturado
- Prompts são atômicos, composíveis, versionáveis
- Sistema construído em camadas de abstração sobre prompts

#### 2.2 Princípio da Separação
> **"Cada camada tem uma responsabilidade única"**

```
DADOS    ≠  PROCESSAMENTO  ≠  APRESENTAÇÃO
(Raízes)    (Tronco/Folhas)    (Galhos/Fruto)
```

#### 2.3 Princípio da Progressividade
> **"Conhecimento é revelado em camadas progressivas"**

- Usuário novato: TL;DR + Quick Start
- Usuário intermediário: Guias e exemplos
- Usuário expert: API Reference completa

#### 2.4 Princípio da Auditabilidade
> **"Tudo é rastreável, versionado, imutável na origem"**

- SHA256 para integridade
- Append-only logs
- Metadata completo em cada artefato

#### 2.5 Princípio da Composição
> **"Complexidade emerge de componentes simples"**

- Skills simples → Agentes compostos
- Slash commands → Skills → Subagents
- Nunca duplicar lógica atômica

---

### 3. METÁFORA DA ÁRVORE

#### 3.1 Por Que Árvore?

**Árvore é:**
- **Viva**: Respira, cresce, se adapta
- **Estruturada**: Raízes, tronco, galhos, folhas, fruto
- **Fractal**: Cada galho é uma mini-árvore
- **Resiliente**: Se um galho quebra, outros continuam
- **Cíclica**: Fruto gera semente que vira nova árvore

#### 3.2 Anatomia Funcional

```
        🌤️ SOL (Input/Energia)
        │
      🍎 FRUTO (13) ← Aplicações finais
        │
    🍃 FOLHAS (8/∞) ← Skills (fotossíntese)
      ↙ ↓ ↖
  ┌─────────────────┐
  │  GALHOS (+)     │ ← Distribuição
  │  Fluxo PARA     │
  │  FORA           │
  └────────┬────────┘
           │
      ╔════∞════╗
      ║  TRONCO ║ ← Orquestração (00_hub)
      ║ CORAÇÃO ║
      ║  (Core) ║
      ╚════╤════╝
           │
  ┌────────┴────────┐
  │  RAÍZES (−)     │ ← Ingestão & Arquivo
  │  Fluxo PARA     │
  │  DENTRO         │
  └─────────────────┘
           │
        🌍 SOLO (Dados brutos: 32k arquivos)
```

#### 3.3 Mapeamento Matemático

**Sua Notação Original:**
- **0 a 8**: A árvore em si (input → processamento → output)
- **8 (∞)**: Infinito - A transformação contínua (Skills)
- **13 (Builder)**: Fora da árvore - O fruto (Aplicações)

**Tradução para Estrutura:**
```
−08 ← −05 ← −03 ← −02 ← −01  (Raízes: entrada)
                    ↓
                 00_∞_hub      (Tronco: coração)
                    ↓
+01 → +02 → +03 → +05 → +08   (Galhos: saída)
                    ↓
              Skills (8=∞)     (Folhas: transformação)
                    ↓
                  App (13)     (Fruto: consumo)
```

---

## PARTE II: ARQUITETURA LCM-AI

### 4. ESTRUTURA DE CAMADAS

#### 4.1 Visão Hierárquica

```yaml
lcm-ai/
  # TRONCO (Orquestração)
  00_∞_hub/
    core.py              # Orquestrador principal
    config.yaml          # Pesos e configurações
    system_prompt.md     # Prompt raiz do sistema
    monitoring.jsonl     # Logs de decisões
  
  # RAÍZES (Input/Arquivo)
  −01_capture/           # Solo bruto (dados originais)
  −02_build/             # Fábrica (artefatos sintetizados)
    −02A_catalog/        # Catálogo navegável
    −02B_units/          # Unidades atômicas
  −03_index/             # Índice e busca
  −05_storage/           # Armazenamento frio
  −08_backup/            # Redundância
  
  # GALHOS (Output/Distribuição)
  +01_intake/            # Porta de entrada
  +02_route/             # Roteamento inteligente
  +03_execute/           # Execução de workflows
  +05_delivery/          # Entrega final
  +08_feedback/          # Feedback loop
  
  # FOLHAS (Transformação)
  skills/
    skill_synthesizer.py
    skill_tokenizer.py
    skill_purpose_extractor.py
    skill_qa_generator.py
    skill_evaluator.py
  
  # VIEWS (Organização Semântica)
  views/
    by-domain/           # Symlinks por domínio
    by-purpose/          # Symlinks por propósito
    by-entity/           # Symlinks por entidade
    by-date/             # Symlinks temporais
```

#### 4.2 Fluxo de Dados Completo

```
ENTRADA (Usuário sobe documento)
    ↓
+01_intake/ (Recebe e valida)
    ↓
+02_route/ (Decide: qual workflow?)
    ↓
00_∞_hub (Orquestra)
    ├→ skill_synthesizer()    # Resumos
    ├→ skill_tokenizer()       # Chunks
    ├→ skill_purpose_extractor() # Tags
    ├→ skill_qa_generator()    # Q&As
    └→ skill_evaluator()       # Score
    ↓
TRINITY NASCEU (.md + .llm.json + .meta.json)
    ↓
−02_build/ (Artefatos criados)
−03_index/ (Catalogado)
views/ (Symlinks organizados)
    ↓
+05_delivery/ (Disponível)
    ↓
SAÍDA (Usuário/App consome)
    ↓
+08_feedback/ (Aprende com uso)
    ↓
00_∞_hub (Atualiza pesos)
    ↓
SISTEMA MAIS INTELIGENTE 🧠
```

---

### 5. RAÍZES (−) - INGESTÃO E ARQUIVO

#### 5.1 Filosofia

> "Raízes crescem no escuro, absorvem nutrientes, nunca esquecem"

**Garantias:**
- ✅ Imutável (append-only)
- ✅ Versionado (git + SHA256)
- ✅ Auditável (quem, quando, por quê)
- ✅ Redundante (backup automático)

#### 5.2 Camadas de Raízes

##### −01_capture/ (Solo Bruto)
```
Função: Receber dados originais sem modificação
Estrutura:
  YYYYMMDD/
    HHmmss_<hash>.original
Política: Nunca deletar, nunca modificar
```

##### −02_build/ (Fábrica)
```
Função: Sintetizar artefatos
Estrutura:
  domain/entity/purpose/
    artifact.md          # Humano
    artifact.llm.json    # IA
    artifact.meta.json   # Metadados
Política: Imutável após criação
```

##### −03_index/ (Catálogo)
```
Função: Busca e navegação
Estrutura:
  search.db            # SQLite full-text
  embeddings.faiss     # Vetores para busca semântica
  taxonomy.yaml        # Árvore de conceitos
Política: Rebuild periódico
```

##### −05_storage/ (Frio)
```
Função: Dados antigos mas preservados
Estrutura:
  YYYY/MM/
    archived_*.tar.gz
Política: Compress + encrypt
```

##### −08_backup/ (Redundância)
```
Função: Disaster recovery
Estrutura:
  daily/
  weekly/
  monthly/
Política: 3-2-1 (3 cópias, 2 mídias, 1 offsite)
```

#### 5.3 Trinity Format

**Cada artefato gera 3 arquivos:**

**1. artifact.md (Humano)**
```markdown
# Título do Artefato

## Resumo (1 linha)
Essência em uma sentença.

## Resumo (2 linhas)
Contexto + valor principal.

## Resumo (3 linhas)
Problema + solução + benefício.

## Resumo (5 linhas)
[Fibonacci: mais detalhes]

## Resumo (8 linhas)
[Fibonacci: contexto completo]

## Conteúdo Principal
[Texto completo processado]

## Metadados
- Domain: [domain]
- Entity: [entity]
- Purpose: [purpose]
- Keywords: [tag1, tag2, tag3]

## Q&A
1. **Q:** [pergunta automática]  
   **A:** [resposta inferida]

[... 5 pares Q&A ...]
```

**2. artifact.llm.json (IA)**
```json
{
  "id": "sha256_hash",
  "content": {
    "full": "texto completo",
    "summaries": {
      "1": "uma linha",
      "2": "duas linhas",
      "3": "três linhas",
      "5": "cinco linhas",
      "8": "oito linhas"
    },
    "chunks": {
      "128": ["chunk1_128tokens", "chunk2_128tokens"],
      "256": ["chunk1_256tokens"],
      "384": ["chunk1_384tokens"],
      "640": ["chunk1_640tokens"],
      "1024": ["chunk1_1024tokens"]
    }
  },
  "metadata": {
    "domain": "domain_name",
    "entity": "entity_name",
    "purpose": ["purpose1", "purpose2"],
    "keywords": ["kw1", "kw2", "kw3"],
    "quality_score": 0.92,
    "created_at": "2025-01-15T10:30:00Z"
  },
  "qa_pairs": [
    {"question": "...", "answer": "..."},
    {"question": "...", "answer": "..."}
  ],
  "embeddings": {
    "model": "text-embedding-3-large",
    "vector": [0.123, -0.456, ...]
  }
}
```

**3. artifact.meta.json (Máquina)**
```json
{
  "provenance": {
    "original_file": "path/to/original",
    "sha256": "hash_do_original",
    "captured_at": "2025-01-15T09:00:00Z",
    "processed_at": "2025-01-15T10:30:00Z"
  },
  "processing": {
    "hub_version": "2.0",
    "skills_used": [
      {"name": "synthesizer", "version": "1.2", "duration_ms": 450},
      {"name": "tokenizer", "version": "1.0", "duration_ms": 120},
      {"name": "purpose_extractor", "version": "0.9", "duration_ms": 230},
      {"name": "qa_generator", "version": "1.1", "duration_ms": 890},
      {"name": "evaluator", "version": "1.0", "duration_ms": 340}
    ],
    "total_duration_ms": 2030
  },
  "taxonomy": {
    "domain": "ai-ml",
    "entity": "transformer",
    "purpose": ["education", "reference"],
    "confidence": 0.88
  },
  "quality": {
    "score": 0.92,
    "dimensions": {
      "clarity": 0.95,
      "completeness": 0.90,
      "accuracy": 0.91
    }
  },
  "relationships": {
    "similar_to": ["hash1", "hash2"],
    "references": ["hash3"],
    "referenced_by": []
  }
}
```

---

### 6. TRONCO (∞) - ORQUESTRAÇÃO

#### 6.1 Filosofia

> "Tronco bombeia seiva. Não sabe se vai chover. Só faz seu trabalho."

**Responsabilidades:**
- Receber requests
- Chamar Skills
- Coordenar workflows
- Monitorar tudo
- Aprender com feedback

#### 6.2 Core.py (Orquestrador)

```python
"""
core.py - Coração do Sistema LCM-AI
"""

import yaml
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Imports dos Skills
from skills.skill_synthesizer import synthesize
from skills.skill_tokenizer import tokenize
from skills.skill_purpose_extractor import extract_purpose
from skills.skill_qa_generator import generate_qa
from skills.skill_evaluator import evaluate

class LCMCore:
    """
    Orquestrador central do sistema LCM-AI.
    Coordena Skills, gerencia estado, aprende com feedback.
    """
    
    def __init__(self, config_path: str = "00_∞_hub/config.yaml"):
        self.config = self.load_config(config_path)
        self.monitoring_log = Path("00_∞_hub/monitoring.jsonl")
        
    def load_config(self, path: str) -> Dict:
        """Carrega configuração e pesos"""
        with open(path) as f:
            return yaml.safe_load(f)
    
    def process_document(self, doc_path: str) -> Dict:
        """
        Pipeline completo: documento → Trinity
        
        Args:
            doc_path: Caminho do documento original
            
        Returns:
            Dict com paths dos artefatos gerados
        """
        start_time = datetime.now()
        
        # 1. LOAD documento original
        doc = self.load_document(doc_path)
        doc_hash = hashlib.sha256(doc.encode()).hexdigest()
        
        # 2. CAPTURE original em −01_capture/
        capture_path = self.capture_original(doc, doc_hash)
        
        # 3. SKILLS pipeline
        results = {}
        
        # Skill 1: Synthesizer (resumos Fibonacci)
        results['summaries'] = synthesize(
            doc, 
            levels=self.config['skills']['synthesizer']['levels']
        )
        
        # Skill 2: Tokenizer (chunks Fibonacci)
        results['chunks'] = tokenize(
            doc,
            sizes=self.config['skills']['tokenizer']['sizes']
        )
        
        # Skill 3: Purpose Extractor (TUO: domain/entity/purpose)
        results['taxonomy'] = extract_purpose(
            doc,
            vocab=self.config['taxonomy']
        )
        
        # Skill 4: Q&A Generator
        results['qa_pairs'] = generate_qa(
            doc,
            n_questions=self.config['skills']['qa_generator']['n_questions']
        )
        
        # Skill 5: Evaluator (score de qualidade)
        results['quality'] = evaluate(
            doc,
            criteria=self.config['skills']['evaluator']['criteria']
        )
        
        # 4. EMITIR Trinity
        trinity_paths = self.emit_trinity(
            doc_hash=doc_hash,
            original_path=capture_path,
            content=doc,
            results=results
        )
        
        # 5. INDEXAR
        self.index_artifact(doc_hash, results['taxonomy'], trinity_paths)
        
        # 6. CRIAR SYMLINKS em views/
        self.create_views(doc_hash, results['taxonomy'], trinity_paths)
        
        # 7. LOG monitoramento
        duration = (datetime.now() - start_time).total_seconds()
        self.log_processing(doc_hash, results, duration)
        
        return {
            'hash': doc_hash,
            'trinity': trinity_paths,
            'quality': results['quality'],
            'duration_s': duration
        }
    
    def emit_trinity(
        self, 
        doc_hash: str, 
        original_path: str,
        content: str, 
        results: Dict
    ) -> Dict[str, str]:
        """
        Gera os 3 arquivos: .md, .llm.json, .meta.json
        """
        taxonomy = results['taxonomy']
        base_path = Path(
            f"−02_build/{taxonomy['domain']}/"
            f"{taxonomy['entity']}/{taxonomy['purpose'][0]}"
        )
        base_path.mkdir(parents=True, exist_ok=True)
        
        artifact_name = f"{doc_hash[:12]}"
        
        # 1. artifact.md (Humano)
        md_path = base_path / f"{artifact_name}.md"
        with open(md_path, 'w') as f:
            f.write(self.format_md(content, results))
        
        # 2. artifact.llm.json (IA)
        llm_path = base_path / f"{artifact_name}.llm.json"
        with open(llm_path, 'w') as f:
            json.dump(self.format_llm_json(doc_hash, content, results), f, indent=2)
        
        # 3. artifact.meta.json (Máquina)
        meta_path = base_path / f"{artifact_name}.meta.json"
        with open(meta_path, 'w') as f:
            json.dump(self.format_meta_json(
                doc_hash, original_path, results
            ), f, indent=2)
        
        return {
            'md': str(md_path),
            'llm_json': str(llm_path),
            'meta_json': str(meta_path)
        }
    
    def log_processing(self, doc_hash: str, results: Dict, duration: float):
        """
        Append ao monitoring.jsonl para aprendizado
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'doc_hash': doc_hash,
            'quality_score': results['quality']['score'],
            'taxonomy': results['taxonomy'],
            'duration_s': duration,
            'skills_performance': {
                skill: results.get(f'{skill}_time', 0)
                for skill in ['synthesizer', 'tokenizer', 'purpose_extractor', 
                             'qa_generator', 'evaluator']
            }
        }
        
        with open(self.monitoring_log, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def learn_from_feedback(self, doc_hash: str, feedback: Dict):
        """
        Ajusta pesos baseado em feedback do usuário
        
        Args:
            doc_hash: ID do artefato
            feedback: {'rating': 1-5, 'comments': str, 'aspect': str}
        """
        # Carrega histórico de feedback
        feedback_log = Path("+08_feedback/feedback.jsonl")
        
        # Registra feedback
        feedback_entry = {
            'timestamp': datetime.now().isoformat(),
            'doc_hash': doc_hash,
            'feedback': feedback
        }
        
        with open(feedback_log, 'a') as f:
            f.write(json.dumps(feedback_entry) + '\n')
        
        # Atualiza pesos se necessário
        if feedback['rating'] <= 2:  # Feedback negativo
            self.adjust_weights(feedback['aspect'], direction='down')
        elif feedback['rating'] >= 4:  # Feedback positivo
            self.adjust_weights(feedback['aspect'], direction='up')
        
    def adjust_weights(self, aspect: str, direction: str):
        """
        Ajusta pesos em config.yaml
        """
        adjustment = 0.05 if direction == 'up' else -0.05
        
        # Mapeamento aspecto → skill
        skill_map = {
            'summary': 'synthesizer',
            'chunking': 'tokenizer',
            'taxonomy': 'purpose_extractor',
            'questions': 'qa_generator',
            'quality': 'evaluator'
        }
        
        skill = skill_map.get(aspect)
        if skill:
            current_weight = self.config['skills'][skill].get('weight', 1.0)
            new_weight = max(0.1, min(2.0, current_weight + adjustment))
            self.config['skills'][skill]['weight'] = new_weight
            
            # Salva config atualizado
            with open("00_∞_hub/config.yaml", 'w') as f:
                yaml.dump(self.config, f)
```

#### 6.3 Config.yaml (Pesos e Parâmetros)

```yaml
# config.yaml - Configuração Central do Sistema

system:
  version: "2.0"
  hub: "00_∞_hub"
  monitoring: true

skills:
  synthesizer:
    enabled: true
    weight: 1.0
    levels: [1, 2, 3, 5, 8]  # Fibonacci
    strategy: "progressive"
    
  tokenizer:
    enabled: true
    weight: 1.0
    sizes: [128, 256, 384, 640, 1024]  # Fibonacci-ish
    overlap: 0.1
    
  purpose_extractor:
    enabled: true
    weight: 1.2  # Peso maior = mais importante
    method: "tfidf"
    top_k: 10
    
  qa_generator:
    enabled: true
    weight: 0.9
    n_questions: 5
    types: ["what", "how", "why", "when", "example"]
    
  evaluator:
    enabled: true
    weight: 1.0
    criteria:
      clarity: 0.3
      completeness: 0.3
      accuracy: 0.4

taxonomy:
  domains:
    - ai-ml
    - software-eng
    - business
    - science
    - personal
  
  entities:
    # Auto-expandido via TF-IDF
    min_confidence: 0.7
  
  purposes:
    - education
    - reference
    - tutorial
    - specification
    - research

routing:
  # Decisão de qual workflow usar
  threshold_quality: 0.7
  threshold_length: 5000  # tokens
  
  workflows:
    simple:
      condition: "length < 1000 AND type == 'note'"
      skills: ["synthesizer", "evaluator"]
    
    standard:
      condition: "default"
      skills: ["synthesizer", "tokenizer", "purpose_extractor", 
               "qa_generator", "evaluator"]
    
    complex:
      condition: "length > 5000 OR type == 'paper'"
      skills: ["synthesizer", "tokenizer", "purpose_extractor", 
               "qa_generator", "evaluator", "citation_extractor"]

feedback:
  enabled: true
  learning_rate: 0.05
  adjustment_threshold: 3  # Mínimo de feedbacks para ajustar

monitoring:
  log_path: "00_∞_hub/monitoring.jsonl"
  metrics:
    - duration
    - quality_score
    - skill_performance
  retention_days: 90
```

---

### 7. GALHOS (+) - DISTRIBUIÇÃO

#### 7.1 Filosofia

> "Galhos crescem pro céu. Cada um independente. Todos paralelos."

**Responsabilidades:**
- Receber requests (+01_intake)
- Rotear inteligentemente (+02_route)
- Executar workflows (+03_execute)
- Entregar resultados (+05_delivery)
- Coletar feedback (+08_feedback)

#### 7.2 Camadas de Galhos

##### +01_intake/ (Porta de Entrada)
```python
"""
Recebe documentos via múltiplos canais
"""

class IntakeManager:
    """Gerencia entrada de documentos"""
    
    channels = {
        'upload': 'Via UI web',
        'api': 'REST API /api/upload',
        'email': 'Email parsing',
        'webhook': 'Integrações externas',
        'filesystem': 'Watch folder'
    }
    
    def receive(self, source: str, payload: bytes) -> str:
        """
        Recebe documento, valida, enfileira
        
        Returns:
            job_id para tracking
        """
        # Validação básica
        if len(payload) > 100_000_000:  # 100MB
            raise ValueError("File too large")
        
        # Criar job
        job_id = self.create_job(source, payload)
        
        # Enfileirar para processamento
        self.queue.put(job_id)
        
        return job_id
```

##### +02_route/ (Roteamento Inteligente)
```python
"""
Decide qual workflow executar
"""

class Router:
    """Roteamento baseado em características do documento"""
    
    def route(self, doc_meta: Dict) -> str:
        """
        Decide workflow baseado em metadados
        
        Returns:
            workflow_name
        """
        # Scoring multi-dimensional
        scores = {
            'simple': self.score_simple(doc_meta),
            'standard': self.score_standard(doc_meta),
            'complex': self.score_complex(doc_meta)
        }
        
        # Escolhe workflow com maior score
        return max(scores, key=scores.get)
    
    def score_simple(self, meta: Dict) -> float:
        """Score para workflow simples"""
        score = 0.0
        
        if meta['length_tokens'] < 1000:
            score += 0.5
        
        if meta['type'] in ['note', 'snippet']:
            score += 0.3
        
        if meta.get('priority') == 'low':
            score += 0.2
        
        return score
```

##### +03_execute/ (Execução)
```python
"""
Executa workflows (futuramente paralelo)
"""

class WorkflowExecutor:
    """Executa workflows definidos"""
    
    def execute(self, job_id: str, workflow: str):
        """
        Executa workflow específico
        """
        # Carrega documento
        doc = self.load_job(job_id)
        
        # Executa baseado em workflow
        if workflow == 'simple':
            result = self.run_simple(doc)
        elif workflow == 'standard':
            result = self.run_standard(doc)
        elif workflow == 'complex':
            result = self.run_complex(doc)
        
        # Publica resultado
        self.publish_result(job_id, result)
        
        return result
    
    def run_standard(self, doc: str) -> Dict:
        """Workflow padrão (todos skills)"""
        core = LCMCore()
        return core.process_document(doc)
```

##### +05_delivery/ (Entrega)
```python
"""
Disponibiliza resultados
"""

class DeliveryManager:
    """Gerencia entrega de artefatos"""
    
    def deliver(self, job_id: str, format: str = 'json'):
        """
        Entrega resultado em formato solicitado
        
        Args:
            job_id: ID do job
            format: 'json' | 'markdown' | 'html' | 'pdf'
        """
        # Carrega Trinity
        trinity = self.load_trinity(job_id)
        
        # Formata conforme solicitado
        if format == 'json':
            return trinity['llm_json']
        elif format == 'markdown':
            return trinity['md']
        elif format == 'html':
            return self.md_to_html(trinity['md'])
        elif format == 'pdf':
            return self.md_to_pdf(trinity['md'])
```

##### +08_feedback/ (Aprendizado)
```python
"""
Coleta e processa feedback
"""

class FeedbackCollector:
    """Gerencia feedback loop"""
    
    def collect(self, job_id: str, rating: int, comment: str):
        """
        Registra feedback e aciona aprendizado
        """
        core = LCMCore()
        
        feedback = {
            'rating': rating,  # 1-5
            'comment': comment,
            'aspect': self.infer_aspect(comment)
        }
        
        # LCMCore aprende e ajusta pesos
        core.learn_from_feedback(job_id, feedback)
    
    def infer_aspect(self, comment: str) -> str:
        """
        Infere qual aspecto do sistema precisa melhorar
        """
        keywords = {
            'summary': ['resumo', 'síntese', 'TL;DR'],
            'chunking': ['chunks', 'divisão', 'tamanho'],
            'taxonomy': ['categorização', 'tags', 'organização'],
            'questions': ['perguntas', 'Q&A'],
            'quality': ['qualidade', 'ruim', 'excelente']
        }
        
        for aspect, kws in keywords.items():
            if any(kw in comment.lower() for kw in kws):
                return aspect
        
        return 'general'
```

---

### 8. FOLHAS (SKILLS) - TRANSFORMAÇÃO

#### 8.1 Filosofia

> "Folhas parecem passivas. Mas fazem fotossíntese: CO2 + luz → açúcar = vida"

**Princípios dos Skills:**
- ✅ Função pura (input → output, sem side effects)
- ✅ Uma responsabilidade
- ✅ Composível
- ✅ Testável isoladamente

#### 8.2 As 5 Folhas do Sistema

##### Skill 1: Synthesizer (Resumos Fibonacci)

```python
"""
skill_synthesizer.py - Gera resumos em progressão Fibonacci
"""

def synthesize(text: str, levels: List[int] = [1, 2, 3, 5, 8]) -> Dict[int, str]:
    """
    Gera resumos em múltiplos níveis de detalhe.
    
    Args:
        text: Documento completo
        levels: Níveis Fibonacci de linhas
        
    Returns:
        Dict mapeando nível → resumo
        
    Example:
        >>> doc = "Long document..."
        >>> summaries = synthesize(doc)
        >>> summaries[1]
        "One-line essence of the document"
        >>> summaries[8]
        "Eight-line comprehensive summary with context, 
         key points, implications, and next steps..."
    """
    summaries = {}
    
    for n_lines in levels:
        prompt = f"""
        Resuma o texto abaixo em EXATAMENTE {n_lines} linha(s).
        
        Regras:
        - Cada linha deve ser completa (terminar com ponto)
        - Progressão: mais linhas = mais detalhe, não repetição
        - {n_lines} linha(s): {"essência" if n_lines == 1 else "contexto progressivo"}
        
        Texto:
        {text}
        
        Resumo em {n_lines} linha(s):
        """
        
        # Chama LLM (abstração)
        summary = call_llm(prompt, max_tokens=n_lines * 50)
        
        summaries[n_lines] = summary.strip()
    
    return summaries
```

##### Skill 2: Tokenizer (Chunks Fibonacci)

```python
"""
skill_tokenizer.py - Divide em chunks de tamanhos Fibonacci
"""

import tiktoken

def tokenize(
    text: str, 
    sizes: List[int] = [128, 256, 384, 640, 1024],
    overlap: float = 0.1
) -> Dict[int, List[str]]:
    """
    Divide texto em chunks de diferentes tamanhos.
    
    Args:
        text: Documento completo
        sizes: Tamanhos em tokens (Fibonacci-ish)
        overlap: % de overlap entre chunks (padrão 10%)
        
    Returns:
        Dict mapeando tamanho → lista de chunks
        
    Example:
        >>> text = "Very long document..."
        >>> chunks = tokenize(text, sizes=[128, 256])
        >>> len(chunks[128])
        10  # 10 chunks de 128 tokens
        >>> len(chunks[256])
        5   # 5 chunks de 256 tokens (menos chunks, mais contexto)
    """
    enc = tiktoken.get_encoding("cl100k_base")
    tokens = enc.encode(text)
    
    all_chunks = {}
    
    for chunk_size in sizes:
        stride = int(chunk_size * (1 - overlap))
        chunks_for_size = []
        
        for i in range(0, len(tokens), stride):
            chunk_tokens = tokens[i:i + chunk_size]
            
            if len(chunk_tokens) < chunk_size // 2:
                # Chunk muito pequeno no final, ignora
                break
            
            chunk_text = enc.decode(chunk_tokens)
            chunks_for_size.append(chunk_text)
        
        all_chunks[chunk_size] = chunks_for_size
    
    return all_chunks
```

##### Skill 3: Purpose Extractor (TUO: Domain/Entity/Purpose)

```python
"""
skill_purpose_extractor.py - Extrai taxonomia via TF-IDF + LLM
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, List

def extract_purpose(
    text: str,
    vocab: Dict[str, List[str]]
) -> Dict[str, any]:
    """
    Extrai Domain, Entity, Purpose (TUO).
    
    Args:
        text: Documento
        vocab: Taxonomia de domínios/purposes conhecidos
        
    Returns:
        {
            'domain': 'ai-ml',
            'entity': 'transformer',
            'purpose': ['education', 'reference'],
            'confidence': 0.88,
            'keywords': ['attention', 'self-attention', 'encoder', ...]
        }
    """
    # 1. TF-IDF para keywords
    vectorizer = TfidfVectorizer(max_features=50, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    
    # Top-10 keywords por TF-IDF score
    scores = tfidf_matrix.toarray()[0]
    top_indices = scores.argsort()[-10:][::-1]
    keywords = [feature_names[i] for i in top_indices]
    
    # 2. LLM para Domain/Entity/Purpose
    prompt = f"""
    Analise o texto e classifique:
    
    **Domain** (escolha 1): {', '.join(vocab['domains'])}
    **Entity** (palavra-chave principal, máx 3 palavras)
    **Purpose** (escolha 1-3): {', '.join(vocab['purposes'])}
    
    Keywords detectados: {', '.join(keywords)}
    
    Texto (primeiras 500 palavras):
    {' '.join(text.split()[:500])}
    
    Responda em JSON:
    {{
        "domain": "...",
        "entity": "...",
        "purpose": ["...", "..."],
        "confidence": 0.0-1.0
    }}
    """
    
    result = call_llm(prompt, response_format="json")
    taxonomy = parse_json(result)
    taxonomy['keywords'] = keywords
    
    return taxonomy
```

##### Skill 4: Q&A Generator

```python
"""
skill_qa_generator.py - Gera perguntas e respostas automáticas
"""

def generate_qa(
    text: str,
    n_questions: int = 5,
    types: List[str] = ["what", "how", "why", "when", "example"]
) -> List[Dict[str, str]]:
    """
    Gera pares Q&A para compreensão.
    
    Args:
        text: Documento
        n_questions: Número de perguntas
        types: Tipos de perguntas
        
    Returns:
        [
            {"question": "What is X?", "answer": "X is..."},
            {"question": "How does Y work?", "answer": "Y works by..."}
        ]
    """
    qa_pairs = []
    
    for q_type in types[:n_questions]:
        prompt = f"""
        Baseado no texto abaixo, gere 1 pergunta do tipo "{q_type.upper()}"
        e sua resposta completa.
        
        Formato:
        Q: [pergunta clara e específica]
        A: [resposta completa em 2-3 sentenças]
        
        Texto:
        {text}
        
        Q&A:
        """
        
        response = call_llm(prompt, max_tokens=200)
        
        # Parse Q: e A:
        lines = response.strip().split('\n')
        question = lines[0].replace('Q:', '').strip()
        answer = '\n'.join(lines[1:]).replace('A:', '').strip()
        
        qa_pairs.append({
            'question': question,
            'answer': answer,
            'type': q_type
        })
    
    return qa_pairs
```

##### Skill 5: Evaluator

```python
"""
skill_evaluator.py - Avalia qualidade do documento/processamento
"""

def evaluate(
    text: str,
    criteria: Dict[str, float] = {
        'clarity': 0.3,
        'completeness': 0.3,
        'accuracy': 0.4
    }
) -> Dict[str, float]:
    """
    Avalia qualidade em múltiplas dimensões.
    
    Args:
        text: Documento
        criteria: Pesos para cada critério
        
    Returns:
        {
            'score': 0.92,  # Score agregado
            'dimensions': {
                'clarity': 0.95,
                'completeness': 0.90,
                'accuracy': 0.91
            },
            'confidence': 0.88
        }
    """
    prompt = f"""
    Avalie o texto abaixo em 3 dimensões (0-1):
    
    1. **Clarity** (Clareza): Linguagem clara? Fácil entender?
    2. **Completeness** (Completude): Cobre o tópico adequadamente?
    3. **Accuracy** (Precisão): Informação parece correta?
    
    Texto (primeiras 1000 palavras):
    {' '.join(text.split()[:1000])}
    
    Responda APENAS em JSON:
    {{
        "clarity": 0.0-1.0,
        "completeness": 0.0-1.0,
        "accuracy": 0.0-1.0,
        "confidence": 0.0-1.0
    }}
    """
    
    response = call_llm(prompt, response_format="json")
    dimensions = parse_json(response)
    
    # Score agregado (weighted average)
    score = sum(
        dimensions[dim] * weight
        for dim, weight in criteria.items()
    )
    
    return {
        'score': round(score, 3),
        'dimensions': dimensions,
        'confidence': dimensions.get('confidence', 0.8)
    }
```

---

### 9. FRUTO (13) - APLICAÇÕES

#### 9.1 Filosofia

> "Árvore faz fruto. Fruto cai. Alguém come. Semente nasce. Tudo recomeça."

**Características:**
- ✅ Desacoplado da árvore
- ✅ Consome via API
- ✅ Múltiplos "sabores" (web, mobile, CLI)
- ✅ Agnóstico de implementação interna

#### 9.2 Interfaces de Consumo

##### REST API

```python
"""
API REST para consumo externo
"""

from fastapi import FastAPI, UploadFile
from lcm_core import LCMCore

app = FastAPI()
core = LCMCore()

@app.post("/api/upload")
async def upload_document(file: UploadFile):
    """
    Recebe documento, processa, retorna job_id
    """
    content = await file.read()
    
    # Salva em +01_intake/
    job_id = save_to_intake(content, file.filename)
    
    # Enfileira processamento
    queue_processing(job_id)
    
    return {"job_id": job_id, "status": "queued"}

@app.get("/api/status/{job_id}")
def get_status(job_id: str):
    """
    Verifica status do processamento
    """
    status = check_job_status(job_id)
    return {"job_id": job_id, "status": status}

@app.get("/api/result/{job_id}")
def get_result(job_id: str, format: str = "json"):
    """
    Retorna resultado em formato solicitado
    """
    delivery = DeliveryManager()
    result = delivery.deliver(job_id, format)
    return result

@app.get("/api/search")
def search(q: str, limit: int = 10):
    """
    Busca semântica nos artefatos
    """
    from search_engine import search_artifacts
    results = search_artifacts(q, limit=limit)
    return {"results": results}

@app.post("/api/feedback/{job_id}")
def submit_feedback(job_id: str, rating: int, comment: str):
    """
    Envia feedback para aprendizado
    """
    feedback_collector = FeedbackCollector()
    feedback_collector.collect(job_id, rating, comment)
    return {"status": "feedback_received"}
```

##### Web Interface (Exemplo conceitual)

```javascript
// Frontend consome API REST

class LCMClient {
    constructor(apiUrl = 'http://localhost:8000') {
        this.apiUrl = apiUrl;
    }
    
    async upload(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${this.apiUrl}/api/upload`, {
            method: 'POST',
            body: formData
        });
        
        return await response.json();
    }
    
    async getResult(jobId, format = 'json') {
        const response = await fetch(
            `${this.apiUrl}/api/result/${jobId}?format=${format}`
        );
        return await response.json();
    }
    
    async search(query) {
        const response = await fetch(
            `${this.apiUrl}/api/search?q=${encodeURIComponent(query)}`
        );
        return await response.json();
    }
}

// Uso
const client = new LCMClient();

// Upload
const file = document.getElementById('fileInput').files[0];
const {job_id} = await client.upload(file);

// Poll status
const checkStatus = setInterval(async () => {
    const {status} = await client.getStatus(job_id);
    if (status === 'completed') {
        clearInterval(checkStatus);
        const result = await client.getResult(job_id);
        displayResult(result);
    }
}, 2000);
```

---

## PARTE III: WORKFLOWS DE AGENTES

### 10. FRAMEWORK GENÉRICO DE AGENTES

#### 10.1 Arquitetura de 3 Agentes

**Workflow padrão para criação de conteúdo:**

```
AGENTE 1: RESEARCH_NOTES
(Pesquisa + Intelligence)
        ↓
   Output: research_notes.md
        ↓
AGENTE 2: COPY_GENERATOR
(Redação + Estruturação)
        ↓
   Output: copy_pack.json
        ↓
AGENTE 3: IMAGE_GENERATOR
(Criação Visual)
        ↓
   Output: image_grid_3x3
        ↓
    ENTREGA FINAL
```

#### 10.2 Properties Comuns

Cada agente segue estrutura padrão:

```yaml
agent:
  name: "agent_name"
  version: "X.Y.Z"
  owner: "BRAND · LCM-AI"
  language: "pt-BR"
  visibility: "internal|public"
  task_type: "research|copy|visual|analysis"
  requires:
    - file_search
    - web_search
    - logging
```

#### 10.3 Fluxo de Dados Entre Agentes

```python
class AgentPipeline:
    """
    Orquestra workflow de múltiplos agentes
    """
    
    def __init__(self):
        self.agent1 = ResearchAgent()
        self.agent2 = CopyAgent()
        self.agent3 = VisualAgent()
    
    def execute(self, brief: Dict) -> Dict:
        """
        Executa pipeline completo
        
        Args:
            brief: {
                'produto': 'Nome do produto',
                'marca': 'Marca',
                'categoria': 'Categoria',
                'publico_alvo': 'Descrição',
                'marketplaces': ['mercadolivre', 'amazon'],
                'imagens_ref': ['url1', 'url2']
            }
            
        Returns:
            {
                'research': research_notes,
                'copy': copy_pack,
                'images': image_grid,
                'qa_report': validations
            }
        """
        # STAGE 1: Research
        research_notes = self.agent1.research(brief)
        
        # STAGE 2: Copy (usa research)
        copy_pack = self.agent2.generate_copy(
            brief=brief,
            research_notes=research_notes
        )
        
        # STAGE 3: Visual (usa research + copy)
        image_grid = self.agent3.generate_visuals(
            brief=brief,
            research_notes=research_notes,
            copy_pack=copy_pack
        )
        
        # VALIDATION
        qa_report = self.validate_outputs(
            research_notes,
            copy_pack,
            image_grid
        )
        
        return {
            'research': research_notes,
            'copy': copy_pack,
            'images': image_grid,
            'qa': qa_report
        }
```

---

### 11. AGENTE 1: RESEARCH & INTELLIGENCE

[Conteúdo completo do AGENTE 1 do documento AGENTES_AI_WORKFLOW_GENERICO.md]

#### 11.1 Papel e Objetivo

**Papel:** Pesquisador tático de marketplaces. Especialista em SEO e heurísticas de linguagem.

**Objetivo:** Consolidar insumos para planejamento de anúncio. NÃO gere copy nesta etapa.

#### 11.2 Metodologia (Ordem Obrigatória)

```python
class ResearchAgent:
    """Agente 1: Pesquisa e Intelligence"""
    
    def research(self, brief: Dict) -> str:
        """
        Executa pesquisa completa
        
        Returns:
            research_notes.md (formato estruturado)
        """
        steps = [
            self.validate_brief,
            self.generate_head_terms,
            self.derive_longtails,
            self.web_search_inbound,
            self.web_search_outbound,
            self.benchmark_competitors,
            self.analyze_gaps
        ]
        
        results = {}
        for step in steps:
            results[step.__name__] = step(brief, results)
        
        # Gera research_notes.md
        return self.format_research_notes(results)
    
    def generate_head_terms(self, brief: Dict, results: Dict) -> List[str]:
        """
        Gera termos principais de busca
        """
        produto = brief['produto']
        beneficio = brief.get('beneficio_principal', '')
        atributos = brief.get('atributos', [])
        
        terms = [
            produto,
            f"{produto} {beneficio}",
            f"{produto} {atributos[0]}" if atributos else produto
        ]
        
        return terms
    
    def web_search_inbound(self, brief: Dict, results: Dict) -> Dict:
        """
        Busca em marketplaces
        """
        head_terms = results['generate_head_terms']
        marketplaces = brief['marketplaces']
        
        findings = {}
        
        for marketplace in marketplaces:
            for term in head_terms:
                query = f'site:{marketplace}.com.br "{term}"'
                search_results = web_search(query)
                
                findings[f"{marketplace}_{term}"] = {
                    'patterns': extract_title_patterns(search_results),
                    'price_range': extract_price_range(search_results),
                    'common_claims': extract_claims(search_results)
                }
        
        return findings
```

[... continuar com todas as seções do workflow de agentes ...]

---

## PARTE IV: HIERARQUIA CLAUDE CODE

### 15. CORE-4: CONTEXTO, MODELOS, PROMPT, FERRAMENTAS

#### 15.1 Princípio Fundamental

> **"The prompt is the new fundamental unit of knowledge work"**

Todo sistema Claude Code é construído sobre 4 pilares:

```
    CONTEXTO
       ↓
    MODELOS ←→ PROMPT ←→ FERRAMENTAS
```

**1. CONTEXTO** (Single Source of Truth)
```yaml
# context/theme.yml
project: "Nome do Projeto"
brand:
  palette: ["#111111", "#f5f5f5"]
  style: ["minimal", "editorial"]
goals:
  - objetivo_1
  - objetivo_2
constraints:
  - restricao_1
  - restricao_2
```

**2. MODELOS** (Papéis)
- **Orchestrator**: Claude Code coordena
- **Specialists**: Subagents especializados
- **Tools**: MCPs para integrações

**3. PROMPT** (Instruções)
- Slash Commands: primitivos atômicos
- System Prompts: contexto persistente
- Few-shot Examples: aprendizado por exemplo

**4. FERRAMENTAS** (Capacidades)
- Bash, Python, APIs
- File system, Git
- MCPs customizados

---

### 16. SLASH COMMANDS (PRIMITIVOS)

#### 16.1 Filosofia

**Slash Commands são:**
- ✅ Atômicos (uma ação)
- ✅ Determinísticos (mesmo input → mesmo output)
- ✅ Composíveis (podem ser combinados)
- ✅ Versionados (evolução controlada)

#### 16.2 Estrutura de Comando

```markdown
# ~/.claude/commands/category/command-name.md

## Objetivo
[Uma linha descrevendo o que faz]

## Entradas
- `param1`: Descrição (tipo, exemplo)
- `param2`: Descrição (tipo, exemplo)

## Saídas
[Formato exato do output - JSON/YAML/Markdown]

## Exemplo
```bash
/category/command-name param1="valor" param2="valor"
```

## Output Exemplo
```json
{
  "result": "...",
  "metadata": {...}
}
```

## Validação
- [ ] Checklist 1
- [ ] Checklist 2

## Notas
[Considerações adicionais]
```

#### 16.3 Exemplos de Slash Commands

##### /theme/shotlist
```markdown
# ~/.claude/commands/theme/shotlist.md

## Objetivo
Gerar lista de 9 cenas fotográficas baseado em context/theme.yml

## Entradas
- `theme_path`: Caminho para context/theme.yml
- `n_shots`: Número de cenas (padrão: 9)

## Saídas
JSON array com estrutura por cena:
```json
[
  {
    "id": "S1",
    "goal": "hero",
    "composition": "produto 85%+ do frame",
    "lens": "50mm",
    "lighting": "softbox difusa 45°",
    "background": "branco",
    "risks": ["texto", "reflexo"]
  }
]
```

## Validação
- [ ] Exatamente n_shots cenas
- [ ] Cada cena tem todos campos obrigatórios
- [ ] IDs sequenciais (S1, S2, ...)
- [ ] Risks identificados
```

##### /qa/validate-output
```markdown
# ~/.claude/commands/qa/validate-output.md

## Objetivo
Validar outputs contra especificação

## Entradas
- `output_path`: Caminho do arquivo gerado
- `spec_path`: Caminho da especificação
- `type`: Tipo de validação ('image'|'copy'|'data')

## Saídas
```json
{
  "valid": true|false,
  "checks": [
    {"check": "nome_check", "passed": true|false, "details": "..."}
  ],
  "score": 0.0-1.0,
  "notes": "..."
}
```

## Exemplo
```bash
/qa/validate-output output_path="dist/image1.png" spec_path="context/theme.yml" type="image"
```
```

---

### 17. SUBAGENTS (ESPECIALIZAÇÃO)

#### 17.1 Quando Usar Subagent

**Use Subagent quando:**
- ✅ Tarefa requer especialização profunda
- ✅ Necessário isolamento de contexto
- ✅ Paralelização de trabalho
- ✅ Múltiplas iterações com memoria própria

**NÃO use Subagent quando:**
- ❌ Tarefa é atômica (use Slash Command)
- ❌ Não requer especialização
- ❌ Lógica já existe em outro lugar

#### 17.2 Estrutura de Subagent

```
subagents/nome-subagent/
  README.md              # Documentação
  system_prompt.md       # Prompt especializado
  context/               # Contexto específico
  tools/                 # Ferramentas auxiliares
  examples/              # Exemplos de I/O
```

#### 17.3 Exemplo: Art Director Subagent

```markdown
# subagents/art-director/README.md

## Papel
Crítico visual especializado em validação de imagens para marketplace

## Responsabilidades
1. Validar composição (regra dos terços, balance)
2. Checar consistência de paleta
3. Identificar artefatos/glitches
4. Verificar compliance (sem texto, watermarks)
5. Sugerir ajustes específicos

## Inputs
- `image_path`: Caminho da imagem
- `spec`: Especificação visual (de context/theme.yml)
- `shot_id`: ID da cena (S1-S9)

## Outputs
```json
{
  "shot_id": "S1",
  "verdict": "pass"|"needs_adjustment"|"fail",
  "scores": {
    "composition": 0.0-1.0,
    "lighting": 0.0-1.0,
    "palette_consistency": 0.0-1.0,
    "technical_quality": 0.0-1.0
  },
  "issues": [
    {"severity": "critical"|"warning", "description": "..."}
  ],
  "suggestions": [
    "Sugestão específica de melhoria"
  ]
}
```

## Invocação
```python
# Via Claude Code
result = subagent.art_director.review(
    image_path="dist/S1.png",
    spec=theme_spec,
    shot_id="S1"
)
```

## Especialização
- Treinado em princípios de fotografia de produto
- Conhece constraints de marketplaces (ML, Amazon, etc)
- Referência em lighting ratios (key:fill)
- Expert em detecção de artefatos de IA generativa
```

---

### 18. MCP (MODEL CONTEXT PROTOCOL)

#### 18.1 O Que É MCP

**MCP = Integrações Externas**

Protocolo para conectar LLMs com:
- 🗄️ Databases (SQL, NoSQL)
- 📁 File systems
- 🌐 APIs externas
- 🎨 Ferramentas de imagem
- 📊 Dashboards
- 💬 Chat platforms

#### 18.2 Configuração MCP

```json
// mcp/config.json
{
  "mcpServers": {
    "image_generator": {
      "command": "python",
      "args": ["/path/to/mcp_servers/image_gen.py"],
      "env": {
        "API_KEY": "${REPLICATE_API_KEY}"
      },
      "parallel": true,
      "timeout": 300
    },
    
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"],
      "env": {
        "GIT_REPO_PATH": "/workspace"
      }
    },
    
    "database": {
      "command": "python",
      "args": ["/path/to/mcp_servers/postgres.py"],
      "env": {
        "DB_URL": "${DATABASE_URL}"
      }
    }
  }
}
```

#### 18.3 Exemplo: MCP de Geração de Imagens

```python
"""
mcp_servers/image_gen.py
MCP Server para geração de imagens via Replicate
"""

import json
import sys
import replicate
from typing import Dict, List

class ImageGenMCP:
    """MCP para geração de imagens"""
    
    def __init__(self):
        self.client = replicate.Client(api_token=os.getenv("REPLICATE_API_KEY"))
    
    def generate(self, prompts: List[Dict]) -> List[str]:
        """
        Gera imagens em paralelo
        
        Args:
            prompts: [
                {
                    "id": "S1",
                    "prompt": "product photo...",
                    "negative": "text, watermark...",
                    "width": 1024,
                    "height": 1024
                }
            ]
            
        Returns:
            List de URLs das imagens geradas
        """
        outputs = []
        
        for prompt_data in prompts:
            output = self.client.run(
                "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
                input={
                    "prompt": prompt_data["prompt"],
                    "negative_prompt": prompt_data["negative"],
                    "width": prompt_data["width"],
                    "height": prompt_data["height"],
                    "num_outputs": 1
                }
            )
            
            outputs.append({
                "id": prompt_data["id"],
                "url": output[0]
            })
        
        return outputs
    
    def handle_request(self, request: Dict) -> Dict:
        """Handler principal do MCP"""
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "generate":
            return {
                "result": self.generate(params["prompts"])
            }
        
        return {"error": f"Unknown method: {method}"}

# MCP Server Loop
if __name__ == "__main__":
    mcp = ImageGenMCP()
    
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        
        request = json.loads(line)
        response = mcp.handle_request(request)
        
        print(json.dumps(response))
        sys.stdout.flush()
```

---

### 19. SKILLS (ORQUESTRAÇÃO)

#### 19.1 Diferença: Skills vs Slash Commands

```
SLASH COMMAND               SKILL
──────────────────────────────────────────
Primitivo atômico          Orquestração
Determinístico             Probabilístico
Stateless                  Stateful (contexto)
Manual invocation          Agent invocation
1 ação                     N ações compostas
```

#### 19.2 Estrutura de Skill

```markdown
# skills/skill-name/SKILL.md

## Propósito
[Objetivo de alto nível]

## Quando Usar
- Cenário 1
- Cenário 2

## Capacidades
- Capacidade 1 (via ferramenta X)
- Capacidade 2 (via ferramenta Y)

## Plano de Execução
1. Passo 1: Ação (ferramenta)
2. Passo 2: Ação (ferramenta)
3. [...]

## Entradas Esperadas
```json
{
  "input_field": "description"
}
```

## Saídas Geradas
```json
{
  "output_field": "description"
}
```

## Ferramentas Usadas
- `/slash/command`
- `subagent.name`
- `mcp.server_name.method`

## Exemplos
### Exemplo 1: [Nome]
**Input:**
```json
{...}
```

**Processo:**
1. Chama /slash/command1
2. Resultado → subagent.specialist
3. Final → mcp.delivery

**Output:**
```json
{...}
```
```

#### 19.3 Exemplo: Theme Builder Skill

```markdown
# skills/theme_builder/SKILL.md

## Propósito
Orquestrar criação completa de tema visual (PNGs + Manual) seguindo hierarquia Slash→Subagent→MCP→Skill

## Quando Usar
- Criar assets visuais para produto/marca
- Gerar documentação visual consistente
- Produzir material de marketing

## Plano de Execução

### Stage 1: Planning
1. `/theme/shotlist` → gera 9 cenas
2. Validação manual (opcional)
3. `/theme/image-prompts` → converte para prompts de IA

### Stage 2: Generation
4. `mcp.image_generator.generate(prompts)` → gera PNGs (parallel=true)
5. Aguarda conclusão (todas 9 imagens)

### Stage 3: Quality Assurance
6. `subagent.art_director.review(image)` para cada S1-S9 (paralelo)
7. `/qa/image` → validação formal contra spec
8. Se falhas: ajustar e regenerar

### Stage 4: Documentation
9. `/theme/manual-outline` → estrutura do manual
10. `subagent.copy_editor.write(outline)` → rascunho completo
11. `/qa/copy` → validação de texto

### Stage 5: Packaging
12. Organizar em `dist/tema-<date>/`
13. Gerar `report/qa.json`
14. Hooks automatizam: git tag, catalogar

## Saídas
```
dist/tema-20250115/
  pngs/
    S1.png
    S2.png
    [...]
    S9.png
  manual/
    manual.md
    manual.pdf
  report/
    qa.json
    metrics.json
```

## Ferramentas Usadas
- Slash: `/theme/*`, `/qa/*`
- Subagents: `art-director`, `copy-editor`
- MCP: `image_generator`, `git`
- Hooks: `postRun`, `onFileEdit`
```

---

### 20. PLUGINS (EMPACOTAMENTO)

#### 20.1 O Que São Plugins

**Plugin = Bundle compartilhável**

Empacota:
- ✅ Commands
- ✅ Skills
- ✅ Subagents
- ✅ MCP configs
- ✅ Output styles
- ✅ Hooks

**Para que?**
- Compartilhar toolkit completo
- Reutilizar em múltiplos projetos
- Distribuir para comunidade

#### 20.2 Manifest de Plugin

```json
// plugin/manifest.json
{
  "name": "theme-builder",
  "version": "0.1.0",
  "description": "Complete theme builder: PNGs + Manual",
  "author": "LCM-AI",
  "license": "MIT",
  
  "includes": {
    "commands": [
      ".claude/commands/theme",
      ".claude/commands/qa"
    ],
    "skills": [
      "skills/theme_builder"
    ],
    "subagents": [
      "subagents/art-director",
      "subagents/copy-editor"
    ],
    "mcp": [
      "mcp/config.json"
    ],
    "hooks": [
      ".claude/settings.json"
    ],
    "outputStyles": [
      "output-styles/yaml-structured.md",
      "output-styles/markdown-focused.md"
    ],
    "context": [
      "context/theme.yml"
    ]
  },
  
  "dependencies": {
    "python": ">=3.8",
    "replicate": ">=0.15.0"
  },
  
  "dist": "dist/"
}
```

#### 20.3 Instalação de Plugin

```bash
# Instalar plugin
claude plugin install theme-builder-0.1.0.tar.gz

# Lista plugins instalados
claude plugin list

# Desinstalar
claude plugin uninstall theme-builder
```

---

## PARTE V: META-CONHECIMENTO

### 21. COMO LLMS APRENDEM

[Conteúdo do META_GUIA_DOCUMENTACAO_LLM.md - Seção 1]

#### 21.1 Pipeline de Aprendizado

```
PRETRAINING (11T tokens)
    ↓
General language understanding
    ↓
SUPERVISED FINE-TUNING (10k examples)
    ↓
Task-specific skills
    ↓
PREFERENCE ALIGNMENT (DPO)
    ↓
Human-aligned outputs
    ↓
DEPLOYMENT (inference)
    ↓
Real-world usage
```

#### 21.2 Mecanismo de Atenção

```python
def attention(Q, K, V):
    """
    Q = Query (o que procuramos)
    K = Key (índices de conteúdo)
    V = Value (conteúdo real)
    """
    # Similaridade entre query e keys
    scores = matmul(Q, K.T) / sqrt(d_k)
    
    # Softmax → probabilidades
    weights = softmax(scores)
    
    # Weighted sum dos values
    output = matmul(weights, V)
    
    return output
```

**Implicações para Documentação:**
- Headers = Keys (índices)
- Conteúdo = Values (recuperado)
- Distância importa (context window)

---

### 22. DESTILAÇÃO DE CONHECIMENTO

[Conteúdo do META_GUIA sobre Knowledge Distillation]

#### 22.1 Abstraction Ladder

**Mesmo conceito, 5 níveis:**

```
NÍVEL 1: METÁFORA
"Imagine uma festa barulhenta..."

NÍVEL 2: CONCEITUAL
"Attention calcula importância relativa..."

NÍVEL 3: MATEMÁTICO
Attention(Q,K,V) = softmax(QK^T/√d_k) × V

NÍVEL 4: CÓDIGO
def attention(Q, K, V):
    ...

NÍVEL 5: EXEMPLO CONCRETO
# Input: "The cat sat"
# Query: "cat"
# Attention: [0.05, 0.30, 0.40, ...]
```

---

### 23. SFT E DPO PARA DOCUMENTAÇÃO

[Conteúdo do META_GUIA sobre SFT e DPO]

#### 23.1 Supervised Fine-Tuning

**Dataset de SFT para Docs:**

```json
{
  "instruction": "Documente a função calculate_loss()",
  
  "context": {
    "code": "def calculate_loss(logits, labels): ...",
    "usage": "loss = calculate_loss(output, target)"
  },
  
  "output": "# calculate_loss()\n\n**Purpose:** ..."
}
```

#### 23.2 Direct Preference Optimization

**Preference Pairs:**

```json
{
  "prompt": "Document the train() method",
  
  "chosen": "# train()\n\n**Purpose:** ...\n**Example:** ...",
  
  "rejected": "This method trains the model. Just call it."
}
```

---

### 24. FORMATOS ÓTIMOS DE DOCUMENTAÇÃO

[Conteúdo do META_GUIA sobre formatos]

#### 24.1 Markdown Estruturado

```markdown
# Nome da Função

> TL;DR: Uma linha de essência

## Metadados
- Tipo: Function
- Complexidade: ⭐⭐⭐

## Quick Start
```python
result = funcao(input)
```

## API Reference
[Detalhes completos...]
```

#### 24.2 JSON Schema

```json
{
  "function": "train",
  "signature": "train() -> TrainOutput",
  "parameters": [...],
  "returns": {...},
  "examples": [...]
}
```

---

## PARTE VI: IMPLEMENTAÇÃO

### 25. PLANO DE 6 DIAS

**SEGUNDA (Dia 1): Raízes & Tronco**
```bash
# Criar estrutura
mkdir -p lcm-ai/{00_∞_hub,skills,-01_capture,-02_build,+01_intake}

# Files básicos
touch 00_∞_hub/{core.py,config.yaml,system_prompt.md}
```

**TERÇA (Dia 2): Primeiro Coração**
```python
# Implementar core.py mínimo
# Integrar skill_synthesizer
# Testar: 1 doc → Trinity
```

**QUARTA (Dia 3): Tokenização**
```python
# Integrar skill_tokenizer
# Validar chunks Fibonacci
# Testar com 100 docs
```

**QUINTA (Dia 4): Taxonomia**
```python
# Integrar skill_purpose_extractor
# Refinar TF-IDF
# Ajustar vocabulário
```

**SEXTA (Dia 5): Pipeline Completo**
```python
# Integrar skill_qa_generator + evaluator
# Testar 1000 docs
# Monitorar performance
```

**SÁBADO (Dia 6): Análise**
```python
# Gerar monitoring.jsonl
# Identificar gargalos
# Planejar próxima iteração
```

---

### 26. CONFIGURAÇÕES E TEMPLATES

#### 26.1 Config.yaml Completo

[Já detalhado na Seção 6.3]

#### 26.2 System Prompt Template

```markdown
# system_prompt.md

Você é o Core Orchestrator do sistema LCM-AI.

## Seu Papel
- Coordenar Skills
- Tomar decisões baseadas em config.yaml
- Monitorar qualidade
- Aprender com feedback

## Seus Princípios
1. Separação de responsabilidades
2. Auditabilidade total
3. Aprendizado contínuo
4. Escalabilidade orgânica

## Processo Padrão
Para cada documento:
1. Receber em +01_intake/
2. Chamar Skills na ordem
3. Emitir Trinity
4. Indexar
5. Disponibilizar em +05_delivery/
6. Aguardar feedback em +08_feedback/

## Formato de Resposta
Sempre JSON estruturado para parsing determinístico.
```

---

### 27. TESTES E VALIDAÇÃO

#### 27.1 Testes Unitários (Skills)

```python
import pytest
from skills.skill_synthesizer import synthesize

def test_synthesizer_levels():
    """Testa se synthesizer gera todos níveis Fibonacci"""
    text = "Long document text..." * 100
    levels = [1, 2, 3, 5, 8]
    
    summaries = synthesize(text, levels)
    
    # Assert: todos níveis presentes
    assert set(summaries.keys()) == set(levels)
    
    # Assert: progressão de tamanho
    for i in range(len(levels) - 1):
        assert len(summaries[levels[i]]) < len(summaries[levels[i+1]])

def test_tokenizer_fibonacci():
    """Testa chunks Fibonacci"""
    from skills.skill_tokenizer import tokenize
    
    text = "word " * 10000
    sizes = [128, 256, 384]
    
    chunks = tokenize(text, sizes)
    
    # Assert: todos tamanhos presentes
    assert set(chunks.keys()) == set(sizes)
    
    # Assert: chunks menores = mais quantidade
    assert len(chunks[128]) > len(chunks[256])
```

#### 27.2 Testes de Integração

```python
def test_full_pipeline():
    """Testa pipeline completo: doc → Trinity"""
    from lcm_core import LCMCore
    
    core = LCMCore()
    
    # Documento de teste
    test_doc = """
    # Test Document
    This is a test document with enough content
    to trigger all Skills in the pipeline.
    [... 500 mais palavras ...]
    """
    
    # Processar
    result = core.process_document(test_doc)
    
    # Validações
    assert 'trinity' in result
    assert 'quality' in result
    assert result['quality']['score'] > 0.5
    
    # Trinity completo
    trinity = result['trinity']
    assert os.path.exists(trinity['md'])
    assert os.path.exists(trinity['llm_json'])
    assert os.path.exists(trinity['meta_json'])
```

#### 27.3 Golden Tests

```python
def test_golden_output():
    """
    Testa se output permanece consistente
    (regression test)
    """
    golden_input = load_file("tests/golden/input.txt")
    golden_output = load_json("tests/golden/expected_output.json")
    
    # Processar
    actual = core.process_document(golden_input)
    
    # Comparar (permite pequenas variações)
    similarity = compute_similarity(actual, golden_output)
    assert similarity > 0.95
```

---

### 28. ANTIPADRÕES E BOAS PRÁTICAS

#### 28.1 ❌ ANTIPADRÕES

**1. Duplicação de Lógica Atômica**
```python
# ❌ RUIM: Mesma lógica em 3 lugares
def skill_a():
    result = extract_keywords(text)  # Duplicado

def slash_command():
    result = extract_keywords(text)  # Duplicado

def subagent():
    result = extract_keywords(text)  # Duplicado

# ✅ BOM: Lógica em um lugar
# Slash command /extract/keywords é primitivo
# Skill e Subagent CHAMAM o slash command
```

**2. Pré-carregar Contexto Gigante**
```python
# ❌ RUIM: Carrega tudo no início
context = load_all_32k_files()  # 5GB na memória

# ✅ BOM: Progressive disclosure
context = load_metadata_only()  # 5MB
# Carrega conteúdo sob demanda quando necessário
```

**3. Skills Aninhados Demais**
```python
# ❌ RUIM: Skill → Skill → Skill → Skill (4 níveis)
# Fica não-determinístico e difícil debug

# ✅ BOM: Skill → Slash Commands (2 níveis max)
# Ou Skill → Subagent → Slash
```

**4. Sem Auditoria**
```python
# ❌ RUIM: Processa sem logging
result = process_secret_sauce(doc)

# ✅ BOM: Log tudo
log_entry = {
    'input_hash': sha256(doc),
    'timestamp': now(),
    'skills_used': [...]
}
monitoring_log.append(log_entry)
```

#### 28.2 ✅ BOAS PRÁTICAS

**1. Separação Clara de Camadas**
```
Dados (−)  ≠  Lógica (∞)  ≠  Interface (+)
```

**2. Trinity Sempre**
```
Todo artefato = .md + .llm.json + .meta.json
```

**3. Feedback Loop Implementado**
```python
# Sempre permitir feedback
user_feedback → adjust_weights → better_next_time
```

**4. Versionamento de Skills**
```yaml
skills:
  synthesizer:
    version: "1.2.0"
    # Mudança de versão = mudança de comportamento
```

**5. Config como Código**
```yaml
# config.yaml é versionado no Git
# Mudanças são rastreáveis
# Rollback é possível
```

---

## PARTE VII: CASOS DE USO

### 29. E-COMMERCE E MARKETPLACE

**Cenário:** Criar 100 anúncios de produtos para Mercado Livre

**Workflow:**

```python
# 1. Preparar brief de cada produto
briefs = load_products_csv("products.csv")

# 2. Pipeline de agentes para cada produto
pipeline = AgentPipeline()

for product in briefs:
    # Research
    research = pipeline.agent1.research({
        'produto': product['nome'],
        'marca': product['marca'],
        'categoria': product['categoria'],
        'publico_alvo': product['publico'],
        'marketplaces': ['mercadolivre']
    })
    
    # Copy
    copy = pipeline.agent2.generate_copy(
        brief=product,
        research_notes=research
    )
    
    # Visual
    images = pipeline.agent3.generate_visuals(
        brief=product,
        research_notes=research,
        copy_pack=copy
    )
    
    # Salvar
    save_listing(product['id'], research, copy, images)
```

**Resultado:**
- 100 anúncios completos
- Títulos otimizados para SEO
- Descrições persuasivas
- 9 imagens por produto (900 total)
- Tudo auditável e versionado

---

### 30. DOCUMENTAÇÃO TÉCNICA

**Cenário:** Documentar codebase de 500 arquivos Python

**Workflow:**

```python
# 1. Scan codebase
files = scan_directory("src/", pattern="*.py")

# 2. Processar cada arquivo
core = LCMCore()

for file_path in files:
    code = read_file(file_path)
    
    # Processar via LCM-AI
    result = core.process_document(code)
    
    # Trinity gerado automaticamente:
    # - file.md: Documentação humana
    # - file.llm.json: Para consumption de IA
    # - file.meta.json: Metadados (funções, classes, deps)

# 3. Gerar site de docs
generate_doc_site("−02_build/")
```

**Resultado:**
- Docs atualizados automaticamente
- Busca semântica funcional
- Q&A geradas para cada módulo
- Grafo de dependências visualizado

---

### 31. GESTÃO DE CONHECIMENTO

**Cenário:** Organizar 32.671 arquivos desorganizados

**Before:**
```
/Desktop/
  doc1.pdf
  doc1_v2.pdf
  doc1_FINAL.pdf
  doc1_FINAL_FINAL.pdf
  [... 32.667 mais ...]
```

**After:**
```
/lcm-ai/
  −02_build/
    ai-ml/
      transformer/
        education/
          abc123.md
          abc123.llm.json
          abc123.meta.json
    business/
      strategy/
        planning/
          [...]
  views/
    by-domain/
      ai-ml → symlinks
    by-purpose/
      education → symlinks
```

**Processo:**
```python
# 1. Capturar tudo
for file in glob("Desktop/*"):
    copy_to("−01_capture/")

# 2. Processar em lote
core = LCMCore()

for captured_file in list_captured():
    core.process_document(captured_file)

# 3. Sistema organiza automaticamente
# 4. Duplicatas eliminadas via SHA256
# 5. Busca funciona
```

**Resultado:**
- 32.671 → ~8.000 artefatos únicos
- Duplicatas removidas
- Busca em 0.2s
- Organização semântica automática

---

## APÊNDICES

### APÊNDICE A: GLOSSÁRIO COMPLETO

**Agente:** Sistema especializado que executa workflow específico

**Artefato:** Output processado (Trinity: .md + .llm.json + .meta.json)

**Core-4:** Contexto, Modelos, Prompt, Ferramentas (pilares Claude Code)

**DPO:** Direct Preference Optimization (alinhamento sem reward model)

**Galhos (+):** Camada de distribuição/output

**Hub (∞):** Orquestrador central (tronco da árvore)

**LCM-AI:** Living Contextual Memory for AI (sistema de gestão de conhecimento)

**MCP:** Model Context Protocol (integrações externas)

**Raízes (−):** Camada de ingestão/arquivo

**SFT:** Supervised Fine-Tuning (treinamento em exemplos rotulados)

**Skill:** Orquestração autônoma de múltiplas ações

**Slash Command:** Primitivo atômico determinístico

**Subagent:** Especialista com contexto isolado

**Trinity:** Trio de arquivos (.md, .llm.json, .meta.json)

**TUO:** Taxonomy Universal Ontology (domain/entity/purpose)

---

### APÊNDICE B: REFERÊNCIAS E BIBLIOGRAFIA

**Papers:**
1. "Attention Is All You Need" (Vaswani et al., 2017)
2. "SmolLM2: When Smol Goes Big" (HuggingFace, 2025)
3. "Direct Preference Optimization" (Rafailov et al., 2024)

**Repositórios:**
1. HuggingFace Transformers: https://github.com/huggingface/transformers
2. TRL (Transformer Reinforcement Learning): https://github.com/huggingface/trl
3. Claude Code: https://docs.claude.com/code

**Documentação:**
1. SmolLM Training Playbook: https://huggingface.co/spaces/HuggingFaceTB/smol-training-playbook
2. Model Context Protocol: https://modelcontextprotocol.io
3. Anthropic API Docs: https://docs.claude.com

---

### APÊNDICE C: CHEAT SHEETS

#### C.1 Quick Reference: Hierarquia

```
Slash Command (primitivo atômico)
    ↓ usa
Subagent (especialista isolado) ←→ MCP (integração externa)
    ↓ orquestra
Skill (workflow autônomo)
    ↓ empacota
Plugin (bundle compartilhável)
```

#### C.2 Quick Reference: Estrutura LCM-AI

```
RAÍZES (−):  −01 → −02 → −03 → −05 → −08
TRONCO (∞):  00_hub (core.py + config.yaml)
GALHOS (+):  +01 → +02 → +03 → +05 → +08
FOLHAS (8):  Skills (5 transformações)
FRUTO (13):  Apps (APIs, Web, Mobile)
```

#### C.3 Quick Reference: Plano 6 Dias

```
D1: Estrutura base
D2: Core + synthesizer
D3: Tokenizer + 100 docs
D4: Purpose extractor
D5: Pipeline completo
D6: Análise + iteração
```

---

## 🎯 CONCLUSÃO

Você agora possui:

✅ **Arquitetura completa** (LCM-AI: Raízes → Tronco → Galhos → Folhas → Fruto)  
✅ **Workflows de Agentes** (Research → Copy → Visual)  
✅ **Hierarquia Claude Code** (Slash → Subagent → MCP → Skill → Plugin)  
✅ **Meta-conhecimento** (Como LLMs aprendem, SFT, DPO, Destilação)  
✅ **Plano de implementação** (6 dias para MVP)  
✅ **Boas práticas** (Antipadrões, testes, validação)

**Este sistema é:**
- 🌱 **Vivo**: Respira, cresce, aprende com feedback
- 🌳 **Estruturado**: Cada camada tem responsabilidade clara
- 🔄 **Cíclico**: Fruto → Semente → Nova árvore
- 📈 **Escalável**: Começa simples, evolui naturalmente

**Próximo passo:** Escolha um caso de uso e implemente o MVP em 6 dias.

---

*Sistema construído com metáforas, executado com código, aprendendo dia a dia.*

**LCM-AI · Agentes · Claude Code · Meta-Conhecimento**  
**Versão 2.0 · 2025**
