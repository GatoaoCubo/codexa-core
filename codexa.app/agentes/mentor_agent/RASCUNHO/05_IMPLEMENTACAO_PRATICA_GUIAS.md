# 🚀 IMPLEMENTAÇÃO PRÁTICA E GUIAS TÁTICOS
## Do Conceito ao Código: Planos, Exemplos, Troubleshooting e Cheat Sheets

> **Axioma Fundamental:** "Conhecimento sem ação é filosofia. Ação sem conhecimento é caos. Este documento é a ponte entre ambos."

---

## 🎭 METÁFORA CENTRAL: DO MAPA AO TERRITÓRIO

Imagine que você tem:
- 📚 **4 documentos anteriores** = Mapa detalhado do território
- 🗺️ **Este documento** = GPS turn-by-turn

```
Documentos 1-4: "ONDE" e "COMO"
  ├─ Arquitetura LCM-AI
  ├─ Workflows de Agentes
  ├─ Hierarquia Claude Code
  └─ Meta-conhecimento

Documento 5: "FAÇA AGORA"
  ├─ Passo a passo executável
  ├─ Código copy-paste pronto
  ├─ Troubleshooting de erros comuns
  └─ Cheat sheets de referência rápida
```

---

## 📅 PARTE 1: PLANO DE 6 DIAS (MVP COMPLETO)

### **DIA 1: ESTRUTURA BASE** (Segunda-feira)

**Meta:** Criar árvore de diretórios + arquivos config

**Tempo:** 2 horas

```bash
#!/bin/bash
# setup_lcm.sh - Execute isto PRIMEIRO

# 1. Criar estrutura
mkdir -p lcm-ai/{00_∞_hub,−01_capture,−02_build,−03_index,−05_archive,+01_intake,+05_delivery,+08_feedback,skills,views}

# 2. Arquivos core
cat > lcm-ai/00_∞_hub/config.yaml << 'EOF'
system:
  name: "LCM-AI"
  version: "1.0.0"
  mode: "development"

paths:
  capture: "−01_capture/"
  build: "−02_build/"
  index: "−03_index/"
  delivery: "+05_delivery/"

skills:
  synthesizer:
    enabled: true
    max_words: 500
  tokenizer:
    enabled: true
    min_frequency: 2
  purpose_extractor:
    enabled: false  # Ativar depois
  qa_generator:
    enabled: false  # Ativar depois
  evaluator:
    enabled: false  # Ativar depois
EOF

# 3. Core Python (versão mínima)
cat > lcm-ai/00_∞_hub/core.py << 'EOF'
"""LCM-AI Core - Versão MVP Dia 1"""
import yaml
from pathlib import Path

class LCMCore:
    def __init__(self, config_path='config.yaml'):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        print(f"✅ LCM-AI {self.config['system']['version']} inicializado")
    
    def capture(self, file_path):
        """Move arquivo para capture/"""
        # TODO: Implementar dia 2
        pass
    
    def process(self, file_path):
        """Processa arquivo"""
        # TODO: Implementar dia 2
        pass

if __name__ == '__main__':
    core = LCMCore()
    print("Sistema pronto para desenvolvimento!")
EOF

# 4. Requirements
cat > lcm-ai/requirements.txt << 'EOF'
pyyaml>=6.0
anthropic>=0.7.0
python-dotenv>=1.0.0
EOF

# 5. Environment
cat > lcm-ai/.env.example << 'EOF'
ANTHROPIC_API_KEY=your_key_here
EOF

echo "✅ Estrutura base criada!"
echo "Next: cd lcm-ai && pip install -r requirements.txt"
```

**Checklist Dia 1:**
- [ ] Estrutura de pastas criada
- [ ] config.yaml funcional
- [ ] core.py executável (mesmo que vazio)
- [ ] requirements.txt listado
- [ ] .env.example criado

---

### **DIA 2: CORE + SKILL SYNTHESIZER** (Terça-feira)

**Meta:** Sistema processando 1 documento end-to-end

**Tempo:** 4 horas

```python
# lcm-ai/skills/skill_synthesizer.py

from anthropic import Anthropic
import os

class SkillSynthesizer:
    """
    Skill 1: Resumo inteligente
    
    Input: Documento texto longo
    Output: Resumo estruturado em Markdown
    """
    
    def __init__(self, max_words=500):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.max_words = max_words
    
    def synthesize(self, document_text: str) -> str:
        """
        Gera resumo estruturado
        
        Args:
            document_text: Texto completo do documento
            
        Returns:
            Markdown estruturado
        """
        
        prompt = f"""
<task>
Resuma o documento abaixo em no máximo {self.max_words} palavras.

<requirements>
- Use Markdown com headers (##)
- Estruture em seções lógicas
- Extraia pontos-chave como bullets
- Mantenha tone profissional mas acessível
</requirements>

<document>
{document_text[:10000]}  # Primeiros 10k chars
</document>

<output_format>
# Título do Documento

Parágrafo resumo executivo.

## Conceitos Principais
- Conceito 1
- Conceito 2

## Conclusões
...
</output_format>
</task>
"""
        
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.content[0].text


# Testar
if __name__ == '__main__':
    synthesizer = SkillSynthesizer(max_words=500)
    
    # Documento exemplo
    sample_doc = """
    Machine learning é um subcampo da inteligência artificial...
    [texto longo aqui]
    """
    
    summary = synthesizer.synthesize(sample_doc)
    print(summary)
```

**Core atualizado:**

```python
# lcm-ai/00_∞_hub/core.py (versão Dia 2)

import yaml
import shutil
from pathlib import Path
from datetime import datetime
import hashlib
import json

# Import skills
import sys
sys.path.append('../skills')
from skill_synthesizer import SkillSynthesizer

class LCMCore:
    def __init__(self, config_path='config.yaml'):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        
        # Inicializa skills
        self.skills = {}
        if self.config['skills']['synthesizer']['enabled']:
            self.skills['synthesizer'] = SkillSynthesizer(
                max_words=self.config['skills']['synthesizer']['max_words']
            )
        
        print(f"✅ LCM-AI {self.config['system']['version']} com {len(self.skills)} skills")
    
    def capture(self, file_path: str) -> str:
        """Move arquivo para capture/"""
        source = Path(file_path)
        dest = Path(self.config['paths']['capture']) / source.name
        shutil.copy2(source, dest)
        print(f"📥 Capturado: {source.name}")
        return str(dest)
    
    def process_document(self, file_path: str) -> dict:
        """
        Processa documento completo
        
        Returns:
            {
                'markdown': '...',
                'llm_json': {...},
                'meta_json': {...}
            }
        """
        
        # 1. Ler arquivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 2. Gerar hash (detectar duplicatas)
        file_hash = hashlib.sha256(content.encode()).hexdigest()[:12]
        
        # 3. Skill: Synthesizer
        if 'synthesizer' in self.skills:
            markdown = self.skills['synthesizer'].synthesize(content)
        else:
            markdown = content  # Fallback
        
        # 4. Gerar llm.json (básico por enquanto)
        llm_json = {
            'summary': markdown[:500],
            'hash': file_hash
        }
        
        # 5. Gerar meta.json
        meta_json = {
            'source_file': Path(file_path).name,
            'processed_at': datetime.now().isoformat(),
            'hash': file_hash,
            'domain': 'unknown',  # TODO: classificar
            'entity': 'unknown',
            'purpose': 'unknown'
        }
        
        # 6. Salvar Trinity
        self._save_trinity(file_hash, markdown, llm_json, meta_json)
        
        return {
            'markdown': markdown,
            'llm_json': llm_json,
            'meta_json': meta_json
        }
    
    def _save_trinity(self, file_id, markdown, llm_json, meta_json):
        """Salva os 3 arquivos"""
        build_path = Path(self.config['paths']['build'])
        build_path.mkdir(parents=True, exist_ok=True)
        
        # .md
        with open(build_path / f"{file_id}.md", 'w') as f:
            f.write(markdown)
        
        # .llm.json
        with open(build_path / f"{file_id}.llm.json", 'w') as f:
            json.dump(llm_json, f, indent=2)
        
        # .meta.json
        with open(build_path / f"{file_id}.meta.json", 'w') as f:
            json.dump(meta_json, f, indent=2)
        
        print(f"💎 Trinity gerado: {file_id}.*")


# CLI básico
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python core.py <arquivo.txt>")
        sys.exit(1)
    
    core = LCMCore()
    
    # Captura
    captured = core.capture(sys.argv[1])
    
    # Processa
    result = core.process_document(captured)
    
    print(f"\n✅ Processamento completo!")
    print(f"Hash: {result['meta_json']['hash']}")
```

**Testar:**

```bash
# 1. Criar documento teste
cat > test_doc.txt << 'EOF'
Machine learning é uma área da inteligência artificial focada
em permitir que sistemas aprendam e melhorem através de dados,
sem serem explicitamente programados.
[adicione mais texto aqui...]
EOF

# 2. Processar
python lcm-ai/00_∞_hub/core.py test_doc.txt

# 3. Verificar output
ls lcm-ai/−02_build/
# Deve mostrar: abc123xyz.md, abc123xyz.llm.json, abc123xyz.meta.json
```

**Checklist Dia 2:**
- [ ] skill_synthesizer implementado
- [ ] core.py processa 1 documento
- [ ] Trinity gerado (.md + .llm.json + .meta.json)
- [ ] Hash SHA256 funcionando
- [ ] Testado com 1 documento real

---

### **DIA 3: TOKENIZER + BATCH** (Quarta-feira)

**Meta:** Processar 100 documentos em lote

**Tempo:** 4 horas

```python
# lcm-ai/skills/skill_tokenizer.py

from collections import Counter
import re

class SkillTokenizer:
    """
    Skill 2: Extração de entidades e keywords
    
    Input: Documento texto
    Output: {entities: [...], keywords: [...]}
    """
    
    def __init__(self, min_frequency=2):
        self.min_frequency = min_frequency
    
    def tokenize(self, document_text: str) -> dict:
        """
        Extrai entidades e keywords
        """
        
        # 1. Normalizar texto
        text = document_text.lower()
        
        # 2. Extrair palavras
        words = re.findall(r'\b[a-záàâãéèêíïóôõöúçñ]+\b', text)
        
        # 3. Remover stopwords (simplificado)
        stopwords = {'o', 'a', 'de', 'para', 'em', 'com', 'um', 'uma', 'é', 'que', 'do', 'da'}
        words_filtered = [w for w in words if w not in stopwords and len(w) > 3]
        
        # 4. Contar frequência
        word_freq = Counter(words_filtered)
        
        # 5. Top keywords
        keywords = [
            word for word, freq in word_freq.most_common(20)
            if freq >= self.min_frequency
        ]
        
        # 6. Detectar entidades nomeadas (simplificado)
        # Palavras capitalizadas
        entities = re.findall(r'\b[A-Z][a-záàâãéèêíïóôõöúçñ]+\b', document_text)
        entities_unique = list(set(entities))[:10]
        
        return {
            'keywords': keywords,
            'entities': entities_unique,
            'word_count': len(words),
            'unique_words': len(set(words))
        }


# Testar
if __name__ == '__main__':
    tokenizer = SkillTokenizer(min_frequency=2)
    
    sample = "Machine learning usa dados. Dados são processados por algoritmos..."
    result = tokenizer.tokenize(sample)
    print(result)
```

**Processamento em Lote:**

```python
# lcm-ai/00_∞_hub/batch_process.py

from core import LCMCore
from pathlib import Path
import time

def batch_process(input_dir: str, max_files: int = None):
    """
    Processa todos arquivos de um diretório
    
    Args:
        input_dir: Diretório com arquivos .txt
        max_files: Limite (None = todos)
    """
    
    core = LCMCore()
    
    # Listar arquivos
    files = list(Path(input_dir).glob('*.txt'))
    if max_files:
        files = files[:max_files]
    
    print(f"🔄 Processando {len(files)} arquivos...")
    
    start_time = time.time()
    results = []
    
    for i, file_path in enumerate(files, 1):
        try:
            # Captura
            captured = core.capture(str(file_path))
            
            # Processa
            result = core.process_document(captured)
            results.append(result)
            
            print(f"✅ [{i}/{len(files)}] {file_path.name}")
            
        except Exception as e:
            print(f"❌ [{i}/{len(files)}] {file_path.name}: {e}")
    
    elapsed = time.time() - start_time
    
    print(f"\n📊 Resumo:")
    print(f"  Total: {len(files)} arquivos")
    print(f"  Sucesso: {len(results)} ({len(results)/len(files)*100:.1f}%)")
    print(f"  Tempo: {elapsed:.1f}s ({elapsed/len(files):.2f}s/arquivo)")
    
    return results


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python batch_process.py <diretório>")
        sys.exit(1)
    
    batch_process(sys.argv[1], max_files=100)
```

**Checklist Dia 3:**
- [ ] skill_tokenizer implementado
- [ ] batch_process.py funcional
- [ ] Processados 100 documentos
- [ ] Tempo médio <2s/documento
- [ ] Taxa de sucesso >95%

---

### **DIA 4: PURPOSE EXTRACTOR** (Quinta-feira)

**Meta:** Classificação TUO automática

**Tempo:** 4 horas

```python
# lcm-ai/skills/skill_purpose_extractor.py

from anthropic import Anthropic
import os
import json

class SkillPurposeExtractor:
    """
    Skill 3: Classificação TUO (domain/entity/purpose)
    
    Input: Documento + metadata
    Output: {domain, entity, purpose}
    """
    
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def extract_purpose(self, document_text: str, keywords: list) -> dict:
        """
        Classifica documento em TUO
        """
        
        prompt = f"""
<task>
Classifique este documento nas 3 dimensões TUO:

1. DOMAIN (área do conhecimento):
   Opções: ai-ml, business, engineering, marketing, finance, health, education, legal, art, other

2. ENTITY (tópico específico):
   Inferir do conteúdo (ex: "machine-learning", "sales-strategy")

3. PURPOSE (finalidade):
   Opções: education, documentation, strategy, operational, creative, research, reference

<document_preview>
{document_text[:2000]}
</document_preview>

<keywords>
{', '.join(keywords[:10])}
</keywords>

<output_format>
Responda APENAS com JSON válido:
{{
  "domain": "...",
  "entity": "...",
  "purpose": "...",
  "confidence": 0.0-1.0
}}
</output_format>
</task>
"""
        
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse JSON
        text = response.content[0].text
        # Remove markdown se presente
        text = text.replace('```json', '').replace('```', '').strip()
        
        try:
            result = json.loads(text)
            return result
        except:
            # Fallback
            return {
                'domain': 'other',
                'entity': 'unknown',
                'purpose': 'reference',
                'confidence': 0.0
            }


# Integração no core.py
# Adicionar ao process_document():

        # 5. Skill: Purpose (se habilitado)
        if 'purpose_extractor' in self.skills:
            tuo = self.skills['purpose_extractor'].extract_purpose(
                document_text=content,
                keywords=llm_json.get('keywords', [])
            )
            
            # Atualizar meta_json
            meta_json['domain'] = tuo['domain']
            meta_json['entity'] = tuo['entity']
            meta_json['purpose'] = tuo['purpose']
            meta_json['tuo_confidence'] = tuo['confidence']
```

**Organizar em Views:**

```python
# lcm-ai/00_∞_hub/organize_views.py

from pathlib import Path
import json
import os

def organize_views(build_path='−02_build', views_path='views'):
    """
    Cria symlinks organizados por domain/entity/purpose
    """
    
    build = Path(build_path)
    views = Path(views_path)
    
    # Criar estrutura views
    (views / 'by-domain').mkdir(parents=True, exist_ok=True)
    (views / 'by-entity').mkdir(parents=True, exist_ok=True)
    (views / 'by-purpose').mkdir(parents=True, exist_ok=True)
    
    # Ler todos meta.json
    for meta_file in build.glob('*.meta.json'):
        with open(meta_file) as f:
            meta = json.load(f)
        
        file_id = meta_file.stem.replace('.meta', '')
        
        # Criar symlinks
        domain = meta.get('domain', 'other')
        entity = meta.get('entity', 'unknown')
        purpose = meta.get('purpose', 'reference')
        
        # By domain
        domain_dir = views / 'by-domain' / domain
        domain_dir.mkdir(exist_ok=True)
        for ext in ['.md', '.llm.json', '.meta.json']:
            source = (build / f"{file_id}{ext}").resolve()
            target = domain_dir / f"{file_id}{ext}"
            if source.exists() and not target.exists():
                os.symlink(source, target)
        
        # By entity
        entity_dir = views / 'by-entity' / entity
        entity_dir.mkdir(exist_ok=True)
        # ... similar symlinks
        
        # By purpose
        purpose_dir = views / 'by-purpose' / purpose
        purpose_dir.mkdir(exist_ok=True)
        # ... similar symlinks
    
    print("📁 Views organizados!")


if __name__ == '__main__':
    organize_views()
```

**Checklist Dia 4:**
- [ ] skill_purpose_extractor implementado
- [ ] TUO classificado para todos documentos
- [ ] Views organizados (by-domain, by-entity, by-purpose)
- [ ] Symlinks funcionando
- [ ] Navegação intuitiva testada

---

### **DIA 5: QA + EVALUATOR** (Sexta-feira)

**Meta:** Pipeline completo com todos 5 skills

**Tempo:** 4 horas

```python
# lcm-ai/skills/skill_qa_generator.py

from anthropic import Anthropic
import os
import json

class SkillQAGenerator:
    """
    Skill 4: Geração de Q&A automático
    
    Input: Documento
    Output: [{'q': '...', 'a': '...'}, ...]
    """
    
    def __init__(self, n_questions=5):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.n_questions = n_questions
    
    def generate_qa(self, document_text: str) -> list:
        """
        Gera perguntas e respostas sobre o documento
        """
        
        prompt = f"""
<task>
Gere {self.n_questions} pares de pergunta-resposta sobre este documento.

<requirements>
- Perguntas devem testar compreensão
- Respostas devem ser concisas (1-2 sentenças)
- Varie dificuldade: fácil, média, difícil
</requirements>

<document>
{document_text[:3000]}
</document>

<output_format>
Responda APENAS com JSON array:
[
  {{"q": "Pergunta 1?", "a": "Resposta 1"}},
  {{"q": "Pergunta 2?", "a": "Resposta 2"}},
  ...
]
</output_format>
</task>
"""
        
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        text = response.content[0].text
        text = text.replace('```json', '').replace('```', '').strip()
        
        try:
            qa_pairs = json.loads(text)
            return qa_pairs[:self.n_questions]
        except:
            return []


# lcm-ai/skills/skill_evaluator.py

class SkillEvaluator:
    """
    Skill 5: Avaliação de qualidade
    
    Input: Documento + metadata + outputs
    Output: {score: 0.0-1.0, breakdown: {...}}
    """
    
    def __init__(self):
        self.weights = {
            'completeness': 0.3,
            'clarity': 0.3,
            'accuracy': 0.4
        }
    
    def evaluate(self, document_text: str, metadata: dict) -> dict:
        """
        Avalia qualidade do processamento
        """
        
        scores = {}
        
        # 1. Completeness (todos campos preenchidos?)
        required_fields = ['domain', 'entity', 'purpose', 'hash']
        filled = sum(1 for f in required_fields if metadata.get(f) != 'unknown')
        scores['completeness'] = filled / len(required_fields)
        
        # 2. Clarity (resumo compreensível?)
        summary = metadata.get('summary', '')
        has_structure = '##' in summary or '**' in summary
        right_length = 100 < len(summary) < 1000
        scores['clarity'] = (0.5 if has_structure else 0) + (0.5 if right_length else 0)
        
        # 3. Accuracy (TUO confidence)
        scores['accuracy'] = metadata.get('tuo_confidence', 0.5)
        
        # Weighted average
        final_score = sum(
            scores[k] * self.weights[k]
            for k in scores
        )
        
        return {
            'score': round(final_score, 3),
            'breakdown': scores,
            'grade': self._get_grade(final_score)
        }
    
    def _get_grade(self, score):
        if score >= 0.9: return 'A'
        if score >= 0.8: return 'B'
        if score >= 0.7: return 'C'
        if score >= 0.6: return 'D'
        return 'F'
```

**Pipeline Completo:**

```python
# Atualizar core.py com todos skills

def process_document(self, file_path: str) -> dict:
    """Pipeline completo com 5 skills"""
    
    # 1. Ler
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    file_hash = hashlib.sha256(content.encode()).hexdigest()[:12]
    
    # 2. Synthesizer
    markdown = self.skills['synthesizer'].synthesize(content)
    
    # 3. Tokenizer
    tokens = self.skills['tokenizer'].tokenize(content)
    
    # 4. Purpose
    tuo = self.skills['purpose_extractor'].extract_purpose(
        document_text=content,
        keywords=tokens['keywords']
    )
    
    # 5. QA Generator
    qa_pairs = self.skills['qa_generator'].generate_qa(content)
    
    # 6. Montar outputs
    llm_json = {
        'summary': markdown[:500],
        'keywords': tokens['keywords'],
        'entities': tokens['entities'],
        'qa_pairs': qa_pairs,
        'word_count': tokens['word_count']
    }
    
    meta_json = {
        'source_file': Path(file_path).name,
        'processed_at': datetime.now().isoformat(),
        'hash': file_hash,
        'domain': tuo['domain'],
        'entity': tuo['entity'],
        'purpose': tuo['purpose'],
        'tuo_confidence': tuo['confidence']
    }
    
    # 7. Evaluator
    quality = self.skills['evaluator'].evaluate(content, meta_json)
    meta_json['quality_score'] = quality['score']
    meta_json['quality_grade'] = quality['grade']
    
    # 8. Salvar Trinity
    self._save_trinity(file_hash, markdown, llm_json, meta_json)
    
    return {
        'markdown': markdown,
        'llm_json': llm_json,
        'meta_json': meta_json,
        'quality': quality
    }
```

**Checklist Dia 5:**
- [ ] skill_qa_generator implementado
- [ ] skill_evaluator implementado
- [ ] Pipeline completo funcional
- [ ] Todos 5 skills integrados
- [ ] Quality score em meta.json

---

### **DIA 6: ANÁLISE + ITERAÇÃO** (Sábado)

**Meta:** Processar TODOS documentos + análise

**Tempo:** 6 horas

```python
# lcm-ai/00_∞_hub/analyze_results.py

import json
from pathlib import Path
from collections import Counter, defaultdict
import statistics

def analyze_results(build_path='−02_build'):
    """
    Análise completa dos resultados
    """
    
    build = Path(build_path)
    
    # Coletar todos meta.json
    all_meta = []
    for meta_file in build.glob('*.meta.json'):
        with open(meta_file) as f:
            all_meta.append(json.load(f))
    
    print(f"📊 Análise de {len(all_meta)} documentos processados\n")
    
    # 1. Distribuição por Domain
    domains = Counter(m['domain'] for m in all_meta)
    print("🌍 Distribuição por Domain:")
    for domain, count in domains.most_common():
        pct = count/len(all_meta)*100
        print(f"  {domain:20s}: {count:4d} ({pct:5.1f}%)")
    
    # 2. Distribuição por Purpose
    purposes = Counter(m['purpose'] for m in all_meta)
    print("\n🎯 Distribuição por Purpose:")
    for purpose, count in purposes.most_common():
        pct = count/len(all_meta)*100
        print(f"  {purpose:20s}: {count:4d} ({pct:5.1f}%)")
    
    # 3. Quality Scores
    scores = [m.get('quality_score', 0) for m in all_meta]
    grades = Counter(m.get('quality_grade', 'F') for m in all_meta)
    
    print("\n⭐ Quality Scores:")
    print(f"  Média: {statistics.mean(scores):.3f}")
    print(f"  Mediana: {statistics.median(scores):.3f}")
    print(f"  Min: {min(scores):.3f}")
    print(f"  Max: {max(scores):.3f}")
    
    print("\n📈 Distribuição de Grades:")
    for grade in ['A', 'B', 'C', 'D', 'F']:
        count = grades[grade]
        pct = count/len(all_meta)*100
        print(f"  {grade}: {count:4d} ({pct:5.1f}%)")
    
    # 4. TUO Confidence
    confidences = [m.get('tuo_confidence', 0) for m in all_meta]
    print("\n🎲 TUO Confidence:")
    print(f"  Média: {statistics.mean(confidences):.3f}")
    print(f"  >0.8 (alta): {sum(1 for c in confidences if c > 0.8)} docs")
    print(f"  <0.5 (baixa): {sum(1 for c in confidences if c < 0.5)} docs")
    
    # 5. Top Entities
    entities = Counter()
    for m in all_meta:
        entities[m.get('entity', 'unknown')] += 1
    
    print("\n🏷️ Top 10 Entities:")
    for entity, count in entities.most_common(10):
        pct = count/len(all_meta)*100
        print(f"  {entity:30s}: {count:4d} ({pct:5.1f}%)")
    
    # 6. Recomendações
    print("\n💡 Recomendações:")
    
    low_quality = sum(1 for s in scores if s < 0.6)
    if low_quality > len(all_meta) * 0.1:
        print(f"  ⚠️ {low_quality} docs com score <0.6 - revisar pipeline")
    
    low_conf = sum(1 for c in confidences if c < 0.5)
    if low_conf > len(all_meta) * 0.2:
        print(f"  ⚠️ {low_conf} docs com baixa TUO confidence - melhorar classifier")
    
    unknown_domain = sum(1 for m in all_meta if m['domain'] == 'other')
    if unknown_domain > len(all_meta) * 0.1:
        print(f"  ⚠️ {unknown_domain} docs não classificados - expandir taxonomia")


if __name__ == '__main__':
    analyze_results()
```

**Checklist Dia 6:**
- [ ] Todos documentos processados
- [ ] Análise estatística completa
- [ ] Identificados gargalos
- [ ] Ajustes de config feitos
- [ ] Documentação atualizada

---

## 📋 PARTE 2: CHEAT SHEETS DE REFERÊNCIA RÁPIDA

### **Cheat Sheet: Core Commands**

```bash
# Setup
git clone https://github.com/seu-repo/lcm-ai
cd lcm-ai
pip install -r requirements.txt
cp .env.example .env  # Adicionar API keys

# Processar 1 documento
python 00_∞_hub/core.py documento.txt

# Processar lote
python 00_∞_hub/batch_process.py ./docs/

# Organizar views
python 00_∞_hub/organize_views.py

# Análise
python 00_∞_hub/analyze_results.py

# Buscar documento
grep -r "machine learning" views/by-domain/

# Ver metadata
cat −02_build/abc123xyz.meta.json | jq
```

### **Cheat Sheet: Estrutura de Arquivos**

```
lcm-ai/
├── 00_∞_hub/              ← Cérebro
│   ├── core.py            ← Orquestrador
│   ├── config.yaml        ← Configuração
│   ├── batch_process.py   ← Lote
│   └── organize_views.py  ← Views
├── skills/                ← Transformações
│   ├── skill_synthesizer.py
│   ├── skill_tokenizer.py
│   ├── skill_purpose_extractor.py
│   ├── skill_qa_generator.py
│   └── skill_evaluator.py
├── −01_capture/           ← Input raw
├── −02_build/             ← Trinity files
├── −03_index/             ← Search index
├── +05_delivery/          ← Output pronto
└── views/                 ← Navegação
    ├── by-domain/
    ├── by-entity/
    └── by-purpose/
```

### **Cheat Sheet: Config.yaml**

```yaml
# Configuração essencial

system:
  name: "LCM-AI"
  version: "1.0.0"
  mode: "production"  # ou "development"

paths:
  capture: "−01_capture/"
  build: "−02_build/"
  index: "−03_index/"
  delivery: "+05_delivery/"

skills:
  synthesizer:
    enabled: true
    max_words: 500        # Tamanho do resumo
  
  tokenizer:
    enabled: true
    min_frequency: 2      # Freq mínima palavra
  
  purpose_extractor:
    enabled: true
    
  qa_generator:
    enabled: true
    n_questions: 5        # Nº de perguntas
  
  evaluator:
    enabled: true
    weights:
      completeness: 0.3
      clarity: 0.3
      accuracy: 0.4
```

### **Cheat Sheet: Trinity Files**

```bash
# Cada documento vira 3 arquivos:

abc123xyz.md           # Humano lê
abc123xyz.llm.json     # IA consome
abc123xyz.meta.json    # Sistema rastreia

# Exemplo meta.json:
{
  "source_file": "original.pdf",
  "processed_at": "2025-01-10T14:30:00",
  "hash": "abc123xyz",
  "domain": "ai-ml",
  "entity": "machine-learning",
  "purpose": "education",
  "tuo_confidence": 0.85,
  "quality_score": 0.92,
  "quality_grade": "A"
}
```

---

## 🐛 PARTE 3: TROUBLESHOOTING

### **Problema 1: API Rate Limit**

```
❌ Erro: Rate limit exceeded (429)

✅ Solução:
# Adicionar throttling no core.py

import time

def process_document(self, file_path):
    # ... código normal ...
    
    # Sleep entre chamadas
    time.sleep(1)  # 1 segundo entre documentos
    
    return result
```

### **Problema 2: Out of Memory**

```
❌ Erro: MemoryError ao processar 1000+ docs

✅ Solução:
# Processar em chunks

def batch_process(input_dir, chunk_size=50):
    files = list(Path(input_dir).glob('*.txt'))
    
    for i in range(0, len(files), chunk_size):
        chunk = files[i:i+chunk_size]
        
        for file in chunk:
            process(file)
        
        # Limpar memória entre chunks
        import gc
        gc.collect()
```

### **Problema 3: JSON Parse Error**

```
❌ Erro: json.loads() failed

✅ Solução:
# Sanitizar output do LLM

def safe_json_parse(text):
    # Remove markdown
    text = text.replace('```json', '').replace('```', '')
    text = text.strip()
    
    try:
        return json.loads(text)
    except:
        # Fallback: extrair JSON manual
        import re
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            return {}  # Fallback vazio
```

### **Problema 4: Symlink Quebrado**

```
❌ Erro: Symlink aponta para arquivo inexistente

✅ Solução:
# Verificar antes de criar symlink

def safe_symlink(source, target):
    if not source.exists():
        print(f"⚠️ Source não existe: {source}")
        return False
    
    if target.exists():
        target.unlink()  # Remove symlink antigo
    
    os.symlink(source, target)
    return True
```

---

## 📖 PARTE 4: EXEMPLOS COMPLETOS

### **Exemplo 1: Processar Documentação de Código**

```python
# use_case_code_docs.py

from core import LCMCore
from pathlib import Path

def process_code_documentation(repo_path: str):
    """
    Processa todos arquivos .md de um repositório
    """
    
    core = LCMCore()
    
    # Buscar todos .md
    docs = list(Path(repo_path).rglob('*.md'))
    print(f"📚 Encontrados {len(docs)} documentos")
    
    # Processar
    for doc in docs:
        try:
            captured = core.capture(str(doc))
            result = core.process_document(captured)
            print(f"✅ {doc.name}: {result['meta_json']['quality_grade']}")
        except Exception as e:
            print(f"❌ {doc.name}: {e}")
    
    # Gerar índice
    core.organize_views()
    
    print("\n✅ Documentação processada!")
    print("📁 Navegue: views/by-purpose/documentation/")


if __name__ == '__main__':
    import sys
    process_code_documentation(sys.argv[1])
```

### **Exemplo 2: Monitorar Pasta com Watchdog**

```python
# monitor_folder.py

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core import LCMCore
import time

class DocumentHandler(FileSystemEventHandler):
    def __init__(self):
        self.core = LCMCore()
    
    def on_created(self, event):
        if event.is_directory:
            return
        
        if event.src_path.endswith('.txt'):
            print(f"🆕 Novo arquivo: {event.src_path}")
            
            try:
                captured = self.core.capture(event.src_path)
                result = self.core.process_document(captured)
                print(f"✅ Processado: {result['meta_json']['hash']}")
            except Exception as e:
                print(f"❌ Erro: {e}")


def watch_folder(folder_path):
    """
    Monitora pasta e processa automaticamente
    """
    
    handler = DocumentHandler()
    observer = Observer()
    observer.schedule(handler, folder_path, recursive=False)
    observer.start()
    
    print(f"👀 Monitorando: {folder_path}")
    print("Ctrl+C para parar")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()


if __name__ == '__main__':
    import sys
    watch_folder(sys.argv[1] if len(sys.argv) > 1 else './input')
```

---

## 🎯 CONCLUSÃO

**Este documento consolidou:**

✅ **Plano de 6 dias** → MVP funcional  
✅ **Cheat sheets** → Referência rápida  
✅ **Troubleshooting** → Resolver problemas comuns  
✅ **Exemplos** → Casos de uso reais  

**Próximos Passos:**

1. Seguir plano dia a dia
2. Adaptar para seu caso de uso
3. Iterar baseado em feedback
4. Escalar conforme necessidade

**Axioma Final:**  
> "Plano sem execução é sonho. Execução sem plano é pesadelo. Este documento é o mapa. Você é o explorador. Boa viagem!"

---

**Fim da Consolidação de 5 Documentos**  
*Sistema LCM-AI completo: Fundamentos → Workflows → Ferramentas → Meta-conhecimento → Implementação*
