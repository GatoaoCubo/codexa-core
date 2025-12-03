# Multi-Agent Orchestration Guide

## 🎯 Overview

Com a infraestrutura de path normalization implementada, criar workflows que coordenam múltiplos agentes é **extremamente simples**.

## 🏗️ Arquitetura

```
codexa.app/
├── config/
│   └── paths.py                    ← 🌟 GLOBAL ORCHESTRATOR
│                                      Single source of truth
│
├── agentes/
│   ├── pesquisa_agent/             ← Agent 1
│   │   ├── outputs/                   (managed by orchestrator)
│   │   └── config/paths.py            (connects to global)
│   │
│   ├── anuncio_agent/              ← Agent 2
│   │   ├── outputs/                   (managed by orchestrator)
│   │   └── config/paths.py            (connects to global)
│   │
│   └── [other agents]/
│
└── workflows/                      ← 🚀 MULTI-AGENT WORKFLOWS
    ├── multi_agent_research_to_ad.py
    └── [your custom workflows]
```

---

## ✨ Key Benefits

### ✅ **1. Single Import = Access to All Agents**

**ANTES (hardcoded paths):**
```python
# ❌ Hardcoded, fragile
pesquisa_dir = Path(__file__).parent.parent / "agentes" / "pesquisa_agent"
anuncio_dir = Path(__file__).parent.parent / "agentes" / "anuncio_agent"

# ❌ Breaks if structure changes
output_dir = pesquisa_dir / "outputs"
```

**AGORA (orchestrator):**
```python
# ✅ One import, everything works
from config.paths import get_agent_paths

# ✅ Type-safe, validated, consistent
pesquisa = get_agent_paths('pesquisa')
anuncio = get_agent_paths('anuncio')
```

---

### ✅ **2. Cross-Agent Data Flow is Trivial**

```python
# Step 1: pesquisa_agent creates research
research_output = get_agent_output('pesquisa', 'market_research.json')
with open(research_output, 'w') as f:
    json.dump(research_data, f)

# Step 2: anuncio_agent reads research (different agent!)
research_input = get_agent_output('pesquisa', 'market_research.json')
research_data = json.load(open(research_input))

# Step 3: anuncio_agent creates ad
ad_output = get_agent_output('anuncio', 'optimized_ad.json')
with open(ad_output, 'w') as f:
    json.dump(ad_data, f)
```

**No hardcoded paths. No guessing. Just works.** ✨

---

### ✅ **3. Agent Discovery is Automatic**

```python
from config.paths import get_all_agents

# Get ALL agents dynamically
for agent in get_all_agents():
    print(f"Found agent: {agent.name}")
    paths = get_agent_paths(agent.name.replace('_agent', ''))
    print(f"  Outputs: {paths['outputs']}")
```

**Output:**
```
Found agent: anuncio_agent
  Outputs: C:/.../agentes/anuncio_agent/outputs
Found agent: codexa_agent
  Outputs: C:/.../agentes/codexa_agent/outputs
Found agent: marca_agent
  Outputs: C:/.../agentes/marca_agent/outputs
...
```

---

## 🚀 Available Functions

### **Core Functions:**

```python
from config.paths import (
    get_agent_dir,        # Get agent's root directory
    get_agent_paths,      # Get all standard paths for an agent
    get_all_agents,       # List all available agents
    get_agent_output,     # Get path to specific output file
    AGENTS_ROOT,          # Path to agentes/ directory
    PATH_GLOBAL_OUTPUTS,  # Global outputs directory
)
```

### **Function Reference:**

#### `get_agent_dir(agent_name: str) -> Path`
```python
# Get agent's root directory
anuncio_root = get_agent_dir('anuncio')
# Returns: Path('.../agentes/anuncio_agent')

# Also accepts full name
anuncio_root = get_agent_dir('anuncio_agent')
# Returns: Same path
```

#### `get_agent_paths(agent_name: str) -> Dict[str, Path]`
```python
# Get ALL standard paths for an agent
paths = get_agent_paths('anuncio')

# Returns dictionary with:
{
    'root': Path('.../anuncio_agent'),
    'builders': Path('.../anuncio_agent/builders'),
    'validators': Path('.../anuncio_agent/validators'),
    'templates': Path('.../anuncio_agent/templates'),
    'workflows': Path('.../anuncio_agent/workflows'),
    'prompts': Path('.../anuncio_agent/prompts'),
    'config': Path('.../anuncio_agent/config'),
    'outputs': Path('.../anuncio_agent/outputs'),
    'logs': Path('.../anuncio_agent/logs'),
}
```

#### `get_agent_output(agent_name: str, filename: str) -> Path`
```python
# Get path to specific output file
research_file = get_agent_output('pesquisa', 'market_research.json')
# Returns: Path('.../pesquisa_agent/outputs/market_research.json')
```

#### `get_all_agents() -> List[Path]`
```python
# List all agent directories
agents = get_all_agents()
# Returns: [Path('.../anuncio_agent'), Path('.../codexa_agent'), ...]
```

---

## 📋 Example Workflows

### **Example 1: Sequential Processing**
```python
# pesquisa → anuncio → marca
from config.paths import get_agent_paths, get_agent_output

# Phase 1: Research
pesquisa = get_agent_paths('pesquisa')
research_output = pesquisa['outputs'] / 'market_analysis.json'
# ... execute research ...

# Phase 2: Create Ad (using research)
anuncio = get_agent_paths('anuncio')
research_data = json.load(open(research_output))
ad_output = anuncio['outputs'] / 'optimized_ad.json'
# ... create ad using research_data ...

# Phase 3: Brand Consistency Check
marca = get_agent_paths('marca')
ad_data = json.load(open(ad_output))
brand_output = marca['outputs'] / 'brand_validation.json'
# ... validate ad against brand guidelines ...
```

### **Example 2: Parallel Processing**
```python
# Process product across multiple agents simultaneously
from config.paths import get_all_agents, get_agent_paths
import threading

def process_with_agent(agent_name, product_data):
    paths = get_agent_paths(agent_name)
    output = paths['outputs'] / f"{product_data['id']}_result.json"
    # ... process ...

# Process in parallel
product = {"id": "123", "name": "Smart Watch"}
threads = []

for agent in ['pesquisa', 'anuncio', 'marca']:
    t = threading.Thread(target=process_with_agent, args=(agent, product))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

### **Example 3: Conditional Routing**
```python
# Route based on product type
from config.paths import get_agent_paths

def route_product(product_type, product_data):
    if product_type == 'physical':
        # Use anuncio_agent
        agent = get_agent_paths('anuncio')
    elif product_type == 'digital':
        # Use different agent
        agent = get_agent_paths('digital_product')

    output_file = agent['outputs'] / f"{product_data['id']}.json"
    # ... process ...
```

---

## 🎯 Real-World Use Cases

### **1. Market Research → Ad Creation Pipeline**
```
pesquisa_agent (research)
    ↓ (market_data.json)
anuncio_agent (create ad)
    ↓ (ad_draft.json)
marca_agent (brand check)
    ↓ (final_ad.json)
```

### **2. Product Launch Workflow**
```
pesquisa_agent (competitor analysis)
    ↓
anuncio_agent (create listings)
    ↓
mentor_agent (strategy validation)
    ↓
marca_agent (brand consistency)
```

### **3. Continuous Optimization**
```
While True:
    pesquisa_agent (monitor market)
    ↓
    IF market_changed:
        anuncio_agent (update ads)
        ↓
        marca_agent (validate changes)
```

---

## 🛠️ Best Practices

### ✅ **DO:**
```python
# ✅ Use orchestrator functions
paths = get_agent_paths('anuncio')

# ✅ Use Path objects consistently
output = paths['outputs'] / 'result.json'

# ✅ Let orchestrator handle validation
agent_dir = get_agent_dir('pesquisa')  # Raises error if not found
```

### ❌ **DON'T:**
```python
# ❌ Don't hardcode agent paths
bad_path = Path("../../agentes/anuncio_agent")

# ❌ Don't guess output locations
bad_output = Path("./outputs/result.json")

# ❌ Don't bypass orchestrator
bad_agent = AGENTS_ROOT / "anuncio_agent"  # Use get_agent_dir() instead
```

---

## 📊 Performance Benefits

**Before (Hardcoded Paths):**
- ❌ ~50 lines to setup paths
- ❌ Breaks on directory changes
- ❌ No validation
- ❌ Agent coupling

**After (Orchestrator):**
- ✅ ~3 lines to setup paths
- ✅ Resilient to structure changes
- ✅ Automatic validation
- ✅ Complete decoupling

---

## 🚦 Quick Start Template

```python
#!/usr/bin/env python3
"""
My Custom Multi-Agent Workflow
"""
import sys
from pathlib import Path

# Import orchestrator
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.paths import get_agent_paths, get_agent_output

def main():
    # Get agent paths
    agent1 = get_agent_paths('pesquisa')
    agent2 = get_agent_paths('anuncio')

    # Phase 1: Agent 1 processes
    output1 = agent1['outputs'] / 'step1_result.json'
    # ... your code ...

    # Phase 2: Agent 2 uses Agent 1's output
    input2 = get_agent_output('pesquisa', 'step1_result.json')
    output2 = agent2['outputs'] / 'step2_result.json'
    # ... your code ...

    print("✅ Workflow complete!")

if __name__ == "__main__":
    main()
```

---

## 📚 Additional Resources

- **Global Orchestrator Source:** `codexa.app/config/paths.py`
- **Example Workflow:** `codexa.app/workflows/multi_agent_research_to_ad.py`
- **Agent Registry:** `codexa.app/51_AGENT_REGISTRY.json`

---

## 🎉 Summary

Com o **Global Orchestrator**, criar ADWs multi-agent é agora:

✅ **Simples** - 1 import, tudo funciona
✅ **Seguro** - Paths validados automaticamente
✅ **Escalável** - Adicione agentes sem quebrar código
✅ **Manutenível** - Mudanças de estrutura em 1 lugar

**Resultado:** 10x menos código, 100x menos problemas! 🚀
