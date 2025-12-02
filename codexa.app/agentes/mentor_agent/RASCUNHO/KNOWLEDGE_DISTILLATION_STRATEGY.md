# 🔬 KNOWLEDGE DISTILLATION STRATEGY
## Processing 43K Raw Files into Operational LCM

**Input:** 43,000+ files (MD, JSON)  
**Goal:** Transform raw → structured → actionable knowledge  
**Method:** Multi-stage hierarchical distillation with organizational pipeline

---

## 📁 DIRECTORY STRUCTURE BLUEPRINT

```
knowledge_pipeline/
├── 00_raw/                          # Original 43K files (READ ONLY)
│   ├── batch_001/                   # Split into manageable batches
│   ├── batch_002/
│   └── ...
│
├── 01_staged/                       # Validated & normalized
│   ├── md_files/
│   ├── json_files/
│   └── metadata.json
│
├── 02_extracted/                    # Atomic facts extracted
│   ├── facts_by_batch/
│   ├── facts_unified.json
│   └── extraction_logs/
│
├── 03_clustered/                    # Organized by topic
│   ├── domain_auth/
│   ├── domain_payments/
│   ├── domain_inventory/
│   └── cluster_map.json
│
├── 04_patterns/                     # Recurring structures identified
│   ├── workflow_patterns/
│   ├── data_patterns/
│   ├── api_patterns/
│   └── patterns_catalog.json
│
├── 05_cards/                        # Knowledge cards generated
│   ├── by_domain/
│   ├── by_type/
│   ├── by_complexity/
│   └── cards_index.json
│
├── 06_indexed/                      # Search indexes built
│   ├── vector_store/
│   ├── keyword_index/
│   ├── graph_db/
│   └── hybrid_config.json
│
├── 07_validated/                    # Quality checked
│   ├── validation_reports/
│   ├── quality_metrics.json
│   └── approved_knowledge/
│
├── 08_production/                   # Deployed knowledge base
│   ├── api/
│   ├── cache/
│   └── monitoring/
│
└── scripts/                         # Pipeline automation
    ├── 01_scan.py
    ├── 02_normalize.py
    ├── 03_extract.py
    ├── 04_cluster.py
    ├── 05_synthesize.py
    ├── 06_index.py
    ├── 07_validate.py
    ├── 08_deploy.py
    └── pipeline_orchestrator.py
```

---

## 🚀 STEP-BY-STEP EXECUTION PIPELINE

### STEP 0: Pre-Flight Checklist

```bash
# Create directory structure
mkdir -p knowledge_pipeline/{00_raw,01_staged,02_extracted,03_clustered,04_patterns,05_cards,06_indexed,07_validated,08_production,scripts}

# Verify raw files
echo "Total files: $(find 00_raw -type f | wc -l)"
echo "MD files: $(find 00_raw -name "*.md" | wc -l)"
echo "JSON files: $(find 00_raw -name "*.json" | wc -l)"

# Estimate processing time
python scripts/00_estimate.py --input 00_raw
# Output: Estimated time: 8-12 hours for 43K files
```

---

### STEP 1: SCAN & INVENTORY (00_raw → 01_staged)

**Duration:** 15-30 min  
**Goal:** Understand what you have

```python
# scripts/01_scan.py

import os
import json
from pathlib import Path
from collections import defaultdict

class FileScanner:
    def __init__(self, raw_dir):
        self.raw = Path(raw_dir)
        self.inventory = {
            'total_files': 0,
            'by_type': defaultdict(int),
            'by_size': defaultdict(int),
            'duplicates': [],
            'corrupt': [],
            'metadata': {}
        }
    
    def scan(self):
        """Deep scan all files"""
        print("🔍 Scanning 43K files...")
        
        file_hashes = {}
        for file_path in self.raw.rglob('*'):
            if not file_path.is_file():
                continue
                
            self.inventory['total_files'] += 1
            
            # Type classification
            ext = file_path.suffix
            self.inventory['by_type'][ext] += 1
            
            # Size buckets
            size = file_path.stat().st_size
            bucket = self._size_bucket(size)
            self.inventory['by_size'][bucket] += 1
            
            # Duplicate detection
            file_hash = self._hash_file(file_path)
            if file_hash in file_hashes:
                self.inventory['duplicates'].append({
                    'original': file_hashes[file_hash],
                    'duplicate': str(file_path)
                })
            else:
                file_hashes[file_hash] = str(file_path)
            
            # Corruption check
            if not self._validate_file(file_path):
                self.inventory['corrupt'].append(str(file_path))
            
            # Progress
            if self.inventory['total_files'] % 1000 == 0:
                print(f"   Processed: {self.inventory['total_files']}")
        
        return self.inventory
    
    def _size_bucket(self, size):
        """Categorize by size"""
        if size < 1024: return 'tiny_<1KB'
        if size < 10*1024: return 'small_1-10KB'
        if size < 100*1024: return 'medium_10-100KB'
        if size < 1024*1024: return 'large_100KB-1MB'
        return 'huge_>1MB'
    
    def _hash_file(self, path):
        """Quick hash for duplicate detection"""
        import hashlib
        return hashlib.md5(path.read_bytes()).hexdigest()
    
    def _validate_file(self, path):
        """Check file integrity"""
        try:
            if path.suffix == '.json':
                json.loads(path.read_text())
            elif path.suffix == '.md':
                path.read_text(encoding='utf-8')
            return True
        except:
            return False
    
    def generate_report(self):
        """Create human-readable report"""
        report = f"""
        📊 INVENTORY REPORT
        ==================
        Total Files: {self.inventory['total_files']:,}
        
        By Type:
        {self._format_dict(self.inventory['by_type'])}
        
        By Size:
        {self._format_dict(self.inventory['by_size'])}
        
        Issues:
        - Duplicates: {len(self.inventory['duplicates'])}
        - Corrupt: {len(self.inventory['corrupt'])}
        """
        return report
    
    def _format_dict(self, d):
        return '\n'.join(f"  {k}: {v:,}" for k, v in sorted(d.items()))

# Execute
scanner = FileScanner('00_raw')
inventory = scanner.scan()

# Save results
with open('01_staged/inventory.json', 'w') as f:
    json.dump(inventory, f, indent=2)

print(scanner.generate_report())

# Decision point
if len(inventory['corrupt']) > 100:
    print("⚠️  WARNING: Many corrupt files detected. Manual review recommended.")
```

**Output Example:**
```
📊 INVENTORY REPORT
Total Files: 43,247

By Type:
  .md: 28,431
  .json: 14,816

By Size:
  tiny_<1KB: 8,234
  small_1-10KB: 22,891
  medium_10-100KB: 10,456
  large_100KB-1MB: 1,523
  huge_>1MB: 143

Issues:
  Duplicates: 432
  Corrupt: 27
```

---

### STEP 2: NORMALIZE & BATCH (00_raw → 01_staged)

**Duration:** 30-60 min  
**Goal:** Clean data, create batches for parallel processing

```python
# scripts/02_normalize.py

class FileNormalizer:
    def __init__(self, inventory, batch_size=500):
        self.inventory = inventory
        self.batch_size = batch_size
        
    def normalize_and_batch(self):
        """Clean and organize files"""
        print("🧹 Normalizing and batching...")
        
        # Remove duplicates (keep first occurrence)
        unique_files = self._deduplicate()
        
        # Fix encoding issues
        cleaned_files = self._fix_encoding(unique_files)
        
        # Create batches for parallel processing
        batches = self._create_batches(cleaned_files)
        
        # Copy to staged with normalized names
        self._stage_files(batches)
        
        return batches
    
    def _deduplicate(self):
        """Remove duplicate files"""
        seen = set()
        unique = []
        
        for dup in self.inventory['duplicates']:
            seen.add(dup['duplicate'])
        
        for file in all_files:
            if file not in seen:
                unique.append(file)
        
        print(f"   Removed {len(seen)} duplicates")
        return unique
    
    def _fix_encoding(self, files):
        """Fix encoding issues"""
        cleaned = []
        for file in files:
            try:
                # Try UTF-8
                content = Path(file).read_text(encoding='utf-8')
                cleaned.append(file)
            except UnicodeDecodeError:
                # Try latin-1 and convert
                content = Path(file).read_text(encoding='latin-1')
                # Re-encode as UTF-8
                new_path = file.replace('00_raw', '01_staged')
                Path(new_path).parent.mkdir(parents=True, exist_ok=True)
                Path(new_path).write_text(content, encoding='utf-8')
                cleaned.append(new_path)
        
        return cleaned
    
    def _create_batches(self, files):
        """Split into manageable batches"""
        batches = []
        for i in range(0, len(files), self.batch_size):
            batch = files[i:i+self.batch_size]
            batches.append({
                'id': f"batch_{i//self.batch_size:03d}",
                'files': batch,
                'size': len(batch)
            })
        
        print(f"   Created {len(batches)} batches")
        return batches
    
    def _stage_files(self, batches):
        """Organize staged files"""
        for batch in batches:
            batch_dir = Path(f"01_staged/{batch['id']}")
            batch_dir.mkdir(parents=True, exist_ok=True)
            
            # Create batch manifest
            manifest = {
                'batch_id': batch['id'],
                'file_count': batch['size'],
                'files': batch['files']
            }
            
            (batch_dir / 'manifest.json').write_text(
                json.dumps(manifest, indent=2)
            )

# Execute
normalizer = FileNormalizer(inventory, batch_size=500)
batches = normalizer.normalize_and_batch()

print(f"✅ Staged {len(batches)} batches in 01_staged/")
```

---

### STEP 3: PARALLEL EXTRACTION (01_staged → 02_extracted)

**Duration:** 2-4 hours  
**Goal:** Extract atomic facts from all files

```python
# scripts/03_extract.py

import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
import anthropic

class ParallelExtractor:
    def __init__(self, num_workers=8):
        self.workers = num_workers
        self.client = anthropic.Anthropic()
        
    def extract_all_batches(self, batches):
        """Process batches in parallel"""
        print(f"⚙️  Extracting with {self.workers} workers...")
        
        with ProcessPoolExecutor(max_workers=self.workers) as executor:
            futures = [
                executor.submit(self.extract_batch, batch)
                for batch in batches
            ]
            
            results = []
            for i, future in enumerate(futures):
                result = future.result()
                results.append(result)
                print(f"   Batch {i+1}/{len(batches)} complete")
        
        # Unify all extracted facts
        unified = self._unify_facts(results)
        return unified
    
    def extract_batch(self, batch):
        """Extract facts from one batch"""
        batch_facts = []
        
        manifest_path = Path(f"01_staged/{batch['id']}/manifest.json")
        manifest = json.loads(manifest_path.read_text())
        
        for file_path in manifest['files']:
            facts = self._extract_from_file(file_path)
            batch_facts.extend(facts)
        
        # Save batch results
        output_path = Path(f"02_extracted/{batch['id']}_facts.json")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(batch_facts, indent=2))
        
        return batch_facts
    
    def _extract_from_file(self, file_path):
        """Extract structured facts from single file"""
        content = Path(file_path).read_text()
        
        prompt = f"""Extract atomic knowledge units from this content.

FILE: {file_path}

CONTENT:
{content[:8000]}  # Limit context

Return JSON array of facts:
[
  {{
    "id": "uuid",
    "source": "{file_path}",
    "type": "concept|procedure|data|constraint|example",
    "content": "single discrete knowledge unit",
    "entities": ["entity1", "entity2"],
    "keywords": ["key1", "key2"],
    "relationships": [
      {{"type": "depends_on", "target": "other_fact_id"}},
      {{"type": "related_to", "target": "another_id"}}
    ]
  }}
]

Rules:
- One fact = one concept/procedure/rule
- Self-contained (understandable alone)
- Preserve critical context
- Extract all actionable knowledge
"""
        
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse JSON response
        import re
        json_match = re.search(r'\[.*\]', response.content[0].text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return []
    
    def _unify_facts(self, all_results):
        """Combine all batch results"""
        unified = []
        for batch_results in all_results:
            unified.extend(batch_results)
        
        # Save unified facts
        output = Path('02_extracted/facts_unified.json')
        output.write_text(json.dumps(unified, indent=2))
        
        print(f"✅ Extracted {len(unified):,} total facts")
        return unified

# Execute
extractor = ParallelExtractor(num_workers=8)
facts = extractor.extract_all_batches(batches)

# Generate extraction report
report = {
    'total_facts': len(facts),
    'by_type': count_by_type(facts),
    'avg_per_file': len(facts) / len(batches) / 500,
    'processing_time': '3.2 hours'
}

with open('02_extracted/report.json', 'w') as f:
    json.dump(report, f, indent=2)
```

**Extraction Output:**
```json
[
  {
    "id": "fact_00001",
    "source": "01_staged/batch_001/auth_patterns.md",
    "type": "procedure",
    "content": "JWT authentication requires validation of signature, expiration, and issuer claims before granting access",
    "entities": ["JWT", "authentication", "claims"],
    "keywords": ["security", "validation", "access_control"],
    "relationships": [
      {"type": "implements", "target": "oauth2_pattern"},
      {"type": "requires", "target": "crypto_lib"}
    ]
  }
]
```

---

### STEP 4: CLUSTER & ORGANIZE (02_extracted → 03_clustered)

**Duration:** 30-60 min  
**Goal:** Group related facts by domain/topic

```python
# scripts/04_cluster.py

from sklearn.cluster import KMeans
from sentence_transformers import SentenceTransformer

class KnowledgeClusterer:
    def __init__(self, facts):
        self.facts = facts
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def cluster(self, n_clusters=50):
        """Organize facts into semantic clusters"""
        print("🎯 Clustering knowledge...")
        
        # Generate embeddings
        texts = [f['content'] for f in self.facts]
        embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Cluster
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(embeddings)
        
        # Organize by cluster
        clusters = self._organize_clusters(labels)
        
        # Name clusters
        named_clusters = self._name_clusters(clusters)
        
        # Save organized facts
        self._save_clusters(named_clusters)
        
        return named_clusters
    
    def _organize_clusters(self, labels):
        """Group facts by cluster label"""
        from collections import defaultdict
        clusters = defaultdict(list)
        
        for fact, label in zip(self.facts, labels):
            clusters[f"cluster_{label:03d}"].append(fact)
        
        return dict(clusters)
    
    def _name_clusters(self, clusters):
        """Generate semantic names for clusters"""
        named = {}
        
        for cluster_id, facts in clusters.items():
            # Get most common keywords
            all_keywords = []
            for f in facts:
                all_keywords.extend(f.get('keywords', []))
            
            # Most frequent = cluster theme
            from collections import Counter
            top_keywords = Counter(all_keywords).most_common(3)
            cluster_name = '_'.join([kw for kw, _ in top_keywords])
            
            named[cluster_name] = {
                'id': cluster_id,
                'name': cluster_name,
                'size': len(facts),
                'facts': facts
            }
        
        return named
    
    def _save_clusters(self, named_clusters):
        """Save organized clusters"""
        for name, cluster in named_clusters.items():
            output_dir = Path(f"03_clustered/{name}")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save cluster facts
            (output_dir / 'facts.json').write_text(
                json.dumps(cluster['facts'], indent=2)
            )
            
            # Save cluster metadata
            (output_dir / 'metadata.json').write_text(
                json.dumps({
                    'name': name,
                    'size': cluster['size'],
                    'themes': cluster.get('keywords', [])
                }, indent=2)
            )
        
        # Save cluster map
        cluster_map = {
            name: {'size': c['size'], 'themes': c['name'].split('_')}
            for name, c in named_clusters.items()
        }
        
        Path('03_clustered/cluster_map.json').write_text(
            json.dumps(cluster_map, indent=2)
        )

# Execute
clusterer = KnowledgeClusterer(facts)
clusters = clusterer.cluster(n_clusters=50)

print(f"✅ Organized into {len(clusters)} semantic clusters")
```

---

### STEP 5: PATTERN SYNTHESIS (03_clustered → 04_patterns)

**Duration:** 1-2 hours  
**Goal:** Identify recurring patterns within clusters

```python
# scripts/05_synthesize.py

class PatternSynthesizer:
    def __init__(self, clusters):
        self.clusters = clusters
        self.client = anthropic.Anthropic()
        
    def synthesize_all(self):
        """Extract patterns from each cluster"""
        print("🔄 Synthesizing patterns...")
        
        all_patterns = []
        
        for cluster_name, cluster_data in self.clusters.items():
            patterns = self._synthesize_cluster(cluster_name, cluster_data)
            all_patterns.extend(patterns)
            print(f"   {cluster_name}: {len(patterns)} patterns")
        
        # Save patterns
        self._save_patterns(all_patterns)
        return all_patterns
    
    def _synthesize_cluster(self, name, data):
        """Find patterns in one cluster"""
        facts = data['facts']
        
        # Group by type
        by_type = {}
        for fact in facts:
            fact_type = fact.get('type', 'unknown')
            by_type.setdefault(fact_type, []).append(fact)
        
        patterns = []
        
        # Analyze each type
        for fact_type, type_facts in by_type.items():
            if len(type_facts) < 3:  # Need minimum for pattern
                continue
            
            pattern = self._identify_pattern(name, fact_type, type_facts)
            if pattern:
                patterns.append(pattern)
        
        return patterns
    
    def _identify_pattern(self, cluster, fact_type, facts):
        """Use LLM to identify recurring pattern"""
        sample = facts[:10]  # Analyze sample
        
        prompt = f"""Analyze these {fact_type} facts from {cluster} cluster.

FACTS:
{json.dumps(sample, indent=2)}

Identify recurring pattern:
1. What structure repeats?
2. What are the variables?
3. What are the constants?
4. How would you abstract this?

Return JSON:
{{
  "pattern_name": "descriptive_name",
  "pattern_type": "{fact_type}",
  "structure": "abstract template",
  "variables": ["var1", "var2"],
  "constraints": ["rule1", "rule2"],
  "examples": [{{...}}],
  "use_cases": ["when to use this pattern"]
}}
"""
        
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse pattern
        import re
        json_match = re.search(r'\{.*\}', response.content[0].text, re.DOTALL)
        if json_match:
            pattern = json.loads(json_match.group())
            pattern['cluster'] = cluster
            pattern['source_facts'] = len(facts)
            return pattern
        
        return None
    
    def _save_patterns(self, patterns):
        """Organize and save patterns"""
        # By type
        by_type = {}
        for p in patterns:
            ptype = p.get('pattern_type', 'general')
            by_type.setdefault(ptype, []).append(p)
        
        for ptype, type_patterns in by_type.items():
            output = Path(f"04_patterns/{ptype}_patterns.json")
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(type_patterns, indent=2))
        
        # Unified catalog
        Path('04_patterns/patterns_catalog.json').write_text(
            json.dumps(patterns, indent=2)
        )
        
        print(f"✅ Synthesized {len(patterns)} patterns")

# Execute
synthesizer = PatternSynthesizer(clusters)
patterns = synthesizer.synthesize_all()
```

---

### STEP 6: KNOWLEDGE CARD GENERATION (04_patterns → 05_cards)

**Duration:** 30-60 min  
**Goal:** Create reusable knowledge cards

```python
# scripts/06_generate_cards.py

class CardGenerator:
    def __init__(self, patterns):
        self.patterns = patterns
        
    def generate_all_cards(self):
        """Transform patterns into knowledge cards"""
        print("💎 Generating knowledge cards...")
        
        cards = []
        for pattern in self.patterns:
            card = self._pattern_to_card(pattern)
            if card:
                cards.append(card)
        
        # Organize cards
        self._organize_cards(cards)
        return cards
    
    def _pattern_to_card(self, pattern):
        """Convert pattern to knowledge card format"""
        card = {
            'id': f"card_{len(cards):04d}",
            'name': pattern['pattern_name'],
            'type': pattern['pattern_type'],
            'domain': pattern['cluster'],
            
            # Deterministic (MUST BE)
            'purpose': pattern.get('use_cases', []),
            'constraints': pattern.get('constraints', []),
            'validation': self._generate_validation(pattern),
            
            # Non-deterministic (VOIDS)
            'implementation': None,  # Agent fills
            'optimization': None,    # Agent decides
            
            # Template structure
            'template': pattern.get('structure', ''),
            'variables': pattern.get('variables', []),
            'examples': pattern.get('examples', []),
            
            # Metadata
            'confidence': self._calculate_confidence(pattern),
            'usage_count': 0,
            'last_updated': datetime.now().isoformat()
        }
        
        return card
    
    def _generate_validation(self, pattern):
        """Create validation rules for card"""
        return {
            'required_fields': pattern.get('variables', []),
            'type_checks': self._infer_types(pattern),
            'business_rules': pattern.get('constraints', [])
        }
    
    def _calculate_confidence(self, pattern):
        """Confidence based on source facts count"""
        count = pattern.get('source_facts', 0)
        if count > 20: return 'high'
        if count > 10: return 'medium'
        return 'low'
    
    def _organize_cards(self, cards):
        """Save cards in organized structure"""
        # By domain
        by_domain = {}
        for card in cards:
            domain = card['domain']
            by_domain.setdefault(domain, []).append(card)
        
        for domain, domain_cards in by_domain.items():
            output_dir = Path(f"05_cards/by_domain/{domain}")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            for card in domain_cards:
                card_file = output_dir / f"{card['id']}.json"
                card_file.write_text(json.dumps(card, indent=2))
        
        # By type
        by_type = {}
        for card in cards:
            ctype = card['type']
            by_type.setdefault(ctype, []).append(card)
        
        for ctype, type_cards in by_type.items():
            output_dir = Path(f"05_cards/by_type/{ctype}")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            index_file = output_dir / 'index.json'
            index_file.write_text(json.dumps(type_cards, indent=2))
        
        # Master index
        Path('05_cards/cards_index.json').write_text(
            json.dumps(cards, indent=2)
        )
        
        print(f"✅ Generated {len(cards)} knowledge cards")

# Execute
generator = CardGenerator(patterns)
cards = generator.generate_all_cards()
```

---

### STEP 7: BUILD INDEXES (05_cards → 06_indexed)

**Duration:** 30-45 min  
**Goal:** Create searchable indexes

```python
# scripts/07_index.py

import faiss
import numpy as np

class IndexBuilder:
    def __init__(self, cards):
        self.cards = cards
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def build_all_indexes(self):
        """Create vector, keyword, and graph indexes"""
        print("📇 Building search indexes...")
        
        # 1. Vector index (semantic search)
        self._build_vector_index()
        
        # 2. Keyword index (exact match)
        self._build_keyword_index()
        
        # 3. Graph index (relationships)
        self._build_graph_index()
        
        # 4. Hybrid config
        self._create_hybrid_config()
    
    def _build_vector_index(self):
        """FAISS vector index for semantic search"""
        # Prepare texts
        texts = [
            f"{c['name']} {c['purpose']} {c['template']}"
            for c in self.cards
        ]
        
        # Generate embeddings
        embeddings = self.model.encode(texts)
        
        # Build FAISS index
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings).astype('float32'))
        
        # Save index
        output_dir = Path('06_indexed/vector_store')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        faiss.write_index(index, str(output_dir / 'faiss.index'))
        
        # Save card IDs mapping
        mapping = [c['id'] for c in self.cards]
        (output_dir / 'id_mapping.json').write_text(
            json.dumps(mapping, indent=2)
        )
        
        print(f"   ✓ Vector index: {len(self.cards)} cards")
    
    def _build_keyword_index(self):
        """Inverted index for keyword search"""
        from collections import defaultdict
        
        inverted_index = defaultdict(set)
        
        for card in self.cards:
            card_id = card['id']
            
            # Index name
            for word in card['name'].lower().split():
                inverted_index[word].add(card_id)
            
            # Index domain
            for word in card['domain'].lower().split('_'):
                inverted_index[word].add(card_id)
            
            # Index variables
            for var in card.get('variables', []):
                inverted_index[var.lower()].add(card_id)
        
        # Convert sets to lists for JSON
        inverted_index = {
            k: list(v) for k, v in inverted_index.items()
        }
        
        # Save
        output_dir = Path('06_indexed/keyword_index')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        (output_dir / 'inverted_index.json').write_text(
            json.dumps(inverted_index, indent=2)
        )
        
        print(f"   ✓ Keyword index: {len(inverted_index)} terms")
    
    def _build_graph_index(self):
        """Neo4j-style graph for relationships"""
        import networkx as nx
        
        G = nx.DiGraph()
        
        # Add card nodes
        for card in self.cards:
            G.add_node(
                card['id'],
                name=card['name'],
                type=card['type'],
                domain=card['domain']
            )
        
        # Add relationships (infer from domains and types)
        for card in self.cards:
            # Domain relationships
            for other in self.cards:
                if other['id'] != card['id']:
                    # Same domain = related
                    if card['domain'] == other['domain']:
                        G.add_edge(card['id'], other['id'], 
                                 type='same_domain')
                    
                    # Similar type = related
                    if card['type'] == other['type']:
                        G.add_edge(card['id'], other['id'],
                                 type='same_type')
        
        # Save graph
        output_dir = Path('06_indexed/graph_db')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        nx.write_gpickle(G, output_dir / 'knowledge_graph.gpickle')
        
        print(f"   ✓ Graph index: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    def _create_hybrid_config(self):
        """Configuration for hybrid search"""
        config = {
            'vector_weight': 0.7,
            'keyword_weight': 0.2,
            'graph_weight': 0.1,
            'top_k': 10,
            'min_score': 0.5
        }
        
        Path('06_indexed/hybrid_config.json').write_text(
            json.dumps(config, indent=2)
        )
        
        print("✅ All indexes built")

# Execute
indexer = IndexBuilder(cards)
indexer.build_all_indexes()
```

---

### STEP 8: VALIDATE QUALITY (06_indexed → 07_validated)

**Duration:** 30-45 min  
**Goal:** Ensure quality before production

```python
# scripts/08_validate.py

class QualityValidator:
    def __init__(self, cards, indexes):
        self.cards = cards
        self.indexes = indexes
        
    def validate_all(self):
        """Run comprehensive validation"""
        print("✓ Validating quality...")
        
        results = {
            'card_quality': self._validate_cards(),
            'index_quality': self._validate_indexes(),
            'retrieval_quality': self._validate_retrieval(),
            'overall_score': 0
        }
        
        results['overall_score'] = self._calculate_overall(results)
        
        # Save report
        self._save_report(results)
        
        if results['overall_score'] < 0.8:
            print("⚠️  Quality below threshold. Review recommended.")
            return False
        
        print(f"✅ Quality score: {results['overall_score']:.2%}")
        return True
    
    def _validate_cards(self):
        """Validate card structure and content"""
        issues = []
        
        for card in self.cards:
            # Required fields
            required = ['id', 'name', 'type', 'purpose', 'template']
            for field in required:
                if field not in card:
                    issues.append(f"{card['id']}: missing {field}")
            
            # Non-empty purpose
            if not card.get('purpose'):
                issues.append(f"{card['id']}: empty purpose")
            
            # Valid template
            if not card.get('template'):
                issues.append(f"{card['id']}: empty template")
        
        return {
            'total_cards': len(self.cards),
            'issues': issues,
            'quality_score': 1 - (len(issues) / len(self.cards))
        }
    
    def _validate_indexes(self):
        """Validate index completeness"""
        # Check vector index
        vector_count = self._count_vector_entries()
        keyword_count = self._count_keyword_entries()
        graph_count = self._count_graph_nodes()
        
        expected = len(self.cards)
        
        return {
            'vector_coverage': vector_count / expected,
            'keyword_coverage': keyword_count / expected,
            'graph_coverage': graph_count / expected,
            'quality_score': min(
                vector_count / expected,
                keyword_count / expected,
                graph_count / expected
            )
        }
    
    def _validate_retrieval(self):
        """Test retrieval quality"""
        # Sample queries
        test_queries = [
            "authentication patterns",
            "payment processing",
            "database schema",
            "api endpoints",
            "error handling"
        ]
        
        results = []
        for query in test_queries:
            hits = self._test_search(query)
            results.append({
                'query': query,
                'hits': len(hits),
                'relevant': self._count_relevant(query, hits)
            })
        
        avg_precision = np.mean([
            r['relevant'] / r['hits'] if r['hits'] > 0 else 0
            for r in results
        ])
        
        return {
            'test_queries': len(test_queries),
            'avg_hits': np.mean([r['hits'] for r in results]),
            'avg_precision': avg_precision,
            'quality_score': avg_precision
        }
    
    def _calculate_overall(self, results):
        """Overall quality score"""
        scores = [
            results['card_quality']['quality_score'],
            results['index_quality']['quality_score'],
            results['retrieval_quality']['quality_score']
        ]
        return np.mean(scores)
    
    def _save_report(self, results):
        """Save validation report"""
        output_dir = Path('07_validated')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        (output_dir / 'validation_report.json').write_text(
            json.dumps(results, indent=2)
        )
        
        # Copy approved cards if quality is good
        if results['overall_score'] >= 0.8:
            import shutil
            shutil.copytree('05_cards', '07_validated/approved_knowledge')

# Execute
validator = QualityValidator(cards, indexer.indexes)
is_valid = validator.validate_all()

if not is_valid:
    print("❌ Validation failed. Fix issues before deployment.")
    sys.exit(1)
```

---

### STEP 9: DEPLOY TO PRODUCTION (07_validated → 08_production)

**Duration:** 15-30 min  
**Goal:** Make knowledge accessible to agents

```python
# scripts/09_deploy.py

from fastapi import FastAPI
import uvicorn

class KnowledgeAPI:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.app = self._create_app()
        
    def _create_app(self):
        """Create FastAPI application"""
        app = FastAPI(title="Knowledge API")
        
        @app.get("/search")
        async def search(q: str, top_k: int = 10):
            """Hybrid search endpoint"""
            results = self.kb.search(q, top_k)
            return {"query": q, "results": results}
        
        @app.get("/card/{card_id}")
        async def get_card(card_id: str):
            """Get specific card"""
            card = self.kb.get_card(card_id)
            return card
        
        @app.get("/domain/{domain}")
        async def get_domain(domain: str):
            """Get all cards in domain"""
            cards = self.kb.get_by_domain(domain)
            return {"domain": domain, "cards": cards}
        
        @app.get("/health")
        async def health():
            """Health check"""
            return {"status": "healthy", "cards": len(self.kb.cards)}
        
        return app
    
    def deploy(self, port=8000):
        """Start API server"""
        print(f"🚀 Deploying API on port {port}...")
        
        # Copy to production
        import shutil
        shutil.copytree('07_validated/approved_knowledge', 
                       '08_production/knowledge_base')
        
        # Start server
        uvicorn.run(self.app, host="0.0.0.0", port=port)

# Execute
from knowledge_base import KnowledgeBase

kb = KnowledgeBase('07_validated/approved_knowledge')
api = KnowledgeAPI(kb)
api.deploy(port=8000)

print("✅ Knowledge API deployed at http://localhost:8000")
print("   Try: curl localhost:8000/search?q='authentication'")
```

---

## 🔄 COMPLETE ORCHESTRATION SCRIPT

```python
# pipeline_orchestrator.py

import sys
from pathlib import Path

class PipelineOrchestrator:
    def __init__(self, raw_dir='00_raw'):
        self.raw_dir = raw_dir
        self.stages = [
            ('scan', self.run_scan),
            ('normalize', self.run_normalize),
            ('extract', self.run_extract),
            ('cluster', self.run_cluster),
            ('synthesize', self.run_synthesize),
            ('cards', self.run_cards),
            ('index', self.run_index),
            ('validate', self.run_validate),
            ('deploy', self.run_deploy)
        ]
        
    def run_full_pipeline(self):
        """Execute complete pipeline"""
        print("🚀 Starting Knowledge Distillation Pipeline")
        print("=" * 60)
        
        for stage_name, stage_func in self.stages:
            print(f"\n▶️  STAGE: {stage_name.upper()}")
            try:
                stage_func()
                print(f"✅ {stage_name} complete")
            except Exception as e:
                print(f"❌ {stage_name} failed: {e}")
                sys.exit(1)
        
        print("\n" + "=" * 60)
        print("🎉 PIPELINE COMPLETE!")
        print(f"📊 Final stats:")
        self.print_final_stats()
    
    def run_scan(self):
        from scripts.scan import FileScanner
        scanner = FileScanner(self.raw_dir)
        inventory = scanner.scan()
        scanner.save('01_staged/inventory.json')
    
    def run_normalize(self):
        from scripts.normalize import FileNormalizer
        inventory = json.load(open('01_staged/inventory.json'))
        normalizer = FileNormalizer(inventory)
        batches = normalizer.normalize_and_batch()
    
    def run_extract(self):
        from scripts.extract import ParallelExtractor
        batches = self.load_batches()
        extractor = ParallelExtractor(num_workers=8)
        facts = extractor.extract_all_batches(batches)
    
    def run_cluster(self):
        from scripts.cluster import KnowledgeClusterer
        facts = json.load(open('02_extracted/facts_unified.json'))
        clusterer = KnowledgeClusterer(facts)
        clusters = clusterer.cluster(n_clusters=50)
    
    def run_synthesize(self):
        from scripts.synthesize import PatternSynthesizer
        clusters = self.load_clusters()
        synthesizer = PatternSynthesizer(clusters)
        patterns = synthesizer.synthesize_all()
    
    def run_cards(self):
        from scripts.generate_cards import CardGenerator
        patterns = json.load(open('04_patterns/patterns_catalog.json'))
        generator = CardGenerator(patterns)
        cards = generator.generate_all_cards()
    
    def run_index(self):
        from scripts.index import IndexBuilder
        cards = json.load(open('05_cards/cards_index.json'))
        indexer = IndexBuilder(cards)
        indexer.build_all_indexes()
    
    def run_validate(self):
        from scripts.validate import QualityValidator
        cards = json.load(open('05_cards/cards_index.json'))
        validator = QualityValidator(cards, None)
        if not validator.validate_all():
            raise Exception("Quality validation failed")
    
    def run_deploy(self):
        from scripts.deploy import KnowledgeAPI
        from knowledge_base import KnowledgeBase
        kb = KnowledgeBase('07_validated/approved_knowledge')
        api = KnowledgeAPI(kb)
        # Deploy in background
        import threading
        t = threading.Thread(target=api.deploy, daemon=True)
        t.start()
    
    def print_final_stats(self):
        """Print final statistics"""
        try:
            facts = json.load(open('02_extracted/facts_unified.json'))
            patterns = json.load(open('04_patterns/patterns_catalog.json'))
            cards = json.load(open('05_cards/cards_index.json'))
            
            print(f"  • Raw files processed: 43,247")
            print(f"  • Facts extracted: {len(facts):,}")
            print(f"  • Patterns identified: {len(patterns):,}")
            print(f"  • Knowledge cards: {len(cards):,}")
            print(f"  • API: http://localhost:8000")
        except:
            print("  Stats unavailable")

# Execute
if __name__ == "__main__":
    orchestrator = PipelineOrchestrator('00_raw')
    orchestrator.run_full_pipeline()
```

**Run the complete pipeline:**
```bash
python pipeline_orchestrator.py
```

**Expected timeline:**
- Scan: 15-30 min
- Normalize: 30-60 min  
- Extract: 2-4 hours
- Cluster: 30-60 min
- Synthesize: 1-2 hours
- Cards: 30-60 min
- Index: 30-45 min
- Validate: 30-45 min
- Deploy: 15-30 min

**Total: 6-10 hours**

---

## ✅ SUCCESS CRITERIA & VALIDATION

```yaml
quality_gates:
  gate_1_extraction:
    metric: "Facts per file"
    target: ">3 facts per file"
    
  gate_2_clustering:
    metric: "Cluster coherence"
    target: ">0.7 silhouette score"
    
  gate_3_patterns:
    metric: "Pattern confidence"
    target: ">70% high confidence"
    
  gate_4_retrieval:
    metric: "Search precision"
    target: ">85% relevant results"
    
  gate_5_production:
    metric: "API latency"
    target: "<100ms per query"
```

---

**43K files → Operational knowledge in 6-10 hours** ✨



```yaml
phase_1_rapid_scan:
  script: |
    # Analyze file structure
    find . -type f -name "*.md" | wc -l
    find . -type f -name "*.json" | wc -l
    
    # Extract metadata
    for file in *.md; do
      echo "$file: $(wc -l < $file) lines, $(stat -f%z $file) bytes"
    done
    
  output:
    - file_count_by_type
    - size_distribution
    - naming_patterns
    - directory_structure

phase_2_semantic_clustering:
  agent_prompt: |
    Analyze sample of 100 files. Identify:
    - Content types (docs, configs, data, code)
    - Topic clusters (features, infrastructure, business_logic)
    - Metadata patterns
    - Relationships between files
    
  output:
    - taxonomy.json
    - cluster_map.json
```

---

## STAGE 2: HIERARCHICAL EXTRACTION

```yaml
layer_1_ATOMIC_FACTS:
  method: "Extract discrete knowledge units"
  
  script: |
    /extract_facts --batch *.md *.json
    
  output: facts_db.json
  structure:
    - fact_id
    - source_file
    - content
    - type: [concept, procedure, constraint, example]
    - relationships: [parent, related, depends_on]

layer_2_PATTERN_RECOGNITION:
  method: "Identify recurring structures"
  
  prompt: |
    Analyze facts_db. Find:
    - Repeated patterns
    - Common workflows
    - Standard structures
    - Anti-patterns
    
  output: patterns_db.json

layer_3_KNOWLEDGE_CARDS:
  method: "Crystallize into reusable templates"
  
  process:
    1. Group related patterns
    2. Abstract to general case
    3. Parameterize specifics
    4. Add validation rules
    
  output: knowledge_cards/
    - by_topic/
    - by_type/
    - by_use_case/
```

---

## STAGE 3: INDEXING STRATEGY

```yaml
vector_embeddings:
  tool: sentence-transformers
  chunks: 512_tokens
  overlap: 50_tokens
  
  index:
    - semantic_search
    - similarity_matching
    - context_retrieval

keyword_index:
  tool: whoosh / elasticsearch
  fields:
    - title
    - content
    - tags
    - file_path
    
  queries:
    - boolean_search
    - phrase_matching
    - faceted_navigation

graph_index:
  nodes: [files, concepts, entities]
  edges: [references, depends_on, related_to]
  
  queries:
    - relationship_traversal
    - dependency_chains
    - impact_analysis

hybrid_retrieval:
  combine:
    - vector_similarity (70%)
    - keyword_match (20%)
    - graph_proximity (10%)
```

---

## STAGE 4: AGENT ACCESS PATTERNS

```yaml
pattern_1_CONTEXTUAL_INJECTION:
  use_case: "Agent needs relevant context"
  
  workflow:
    1. Agent receives task
    2. Extract key terms
    3. Query hybrid index (top 10 results)
    4. Inject into context window
    5. Agent executes with knowledge
    
  implementation: |
    context = retrieve_knowledge(task_keywords, limit=10)
    prompt = f"{context}\n\nTask: {task}"
    result = agent.execute(prompt)

pattern_2_JUST_IN_TIME_LOOKUP:
  use_case: "Agent discovers it needs info"
  
  workflow:
    1. Agent executing
    2. Encounters unknown term
    3. Calls /knowledge_search <term>
    4. Receives definition/context
    5. Continues with new knowledge
    
  tool: |
    def knowledge_search(query):
        results = index.search(query, top_k=3)
        return summarize(results)

pattern_3_BATCH_PREPROCESSING:
  use_case: "Pre-load common knowledge"
  
  workflow:
    1. Analyze frequent queries
    2. Pre-generate summaries
    3. Cache in fast storage
    4. Serve instantly
    
  cache_structure:
    common_concepts/
      - api_patterns.md
      - db_schemas.md
      - business_rules.md

pattern_4_PROGRESSIVE_REFINEMENT:
  use_case: "Start broad, narrow down"
  
  workflow:
    1. Initial coarse search (100 results)
    2. Agent analyzes relevance
    3. Refined search with feedback
    4. Final context (10 most relevant)
```

---

## STAGE 5: DISTILLATION SCRIPTS

```python
# master_distiller.py

import os
import json
from pathlib import Path

class KnowledgeDistiller:
    def __init__(self, source_dir, output_dir):
        self.source = Path(source_dir)
        self.output = Path(output_dir)
        
    def stage_1_inventory(self):
        """Scan and classify all files"""
        inventory = {
            'md_files': [],
            'json_files': [],
            'total_size': 0,
            'clusters': {}
        }
        
        for file in self.source.rglob('*'):
            if file.suffix == '.md':
                inventory['md_files'].append(str(file))
            elif file.suffix == '.json':
                inventory['json_files'].append(str(file))
                
        return inventory
    
    def stage_2_extract_facts(self, inventory):
        """Extract atomic knowledge units"""
        facts = []
        
        # Batch process with agent
        for batch in chunk(inventory['md_files'], 100):
            prompt = f"""
            Extract structured facts from these files:
            {batch}
            
            Return JSON array of:
            {{
              "fact_id": "uuid",
              "source": "file_path",
              "content": "knowledge_unit",
              "type": "concept|procedure|constraint",
              "tags": ["tag1", "tag2"]
            }}
            """
            
            result = agent_call(prompt)
            facts.extend(result)
            
        return facts
    
    def stage_3_build_index(self, facts):
        """Create searchable index"""
        from sentence_transformers import SentenceTransformer
        
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Vector embeddings
        texts = [f['content'] for f in facts]
        embeddings = model.encode(texts)
        
        # Save to FAISS or similar
        save_vector_index(embeddings, facts)
        
    def stage_4_generate_cards(self, facts):
        """Create knowledge cards from patterns"""
        patterns = identify_patterns(facts)
        
        for pattern in patterns:
            card = create_knowledge_card(
                pattern=pattern,
                examples=pattern.instances,
                template=pattern.abstract_form
            )
            
            save_card(card, self.output / 'cards')
    
    def run_full_pipeline(self):
        """Execute complete distillation"""
        print("Stage 1: Inventory...")
        inventory = self.stage_1_inventory()
        
        print("Stage 2: Extract facts...")
        facts = self.stage_2_extract_facts(inventory)
        
        print("Stage 3: Build index...")
        self.stage_3_build_index(facts)
        
        print("Stage 4: Generate cards...")
        self.stage_4_generate_cards(facts)
        
        print("Distillation complete!")

# Usage
distiller = KnowledgeDistiller(
    source_dir='./raw_files',
    output_dir='./knowledge_base'
)
distiller.run_full_pipeline()
```

---

## STAGE 6: AGENT INTEGRATION

```yaml
integration_1_CONTEXT_TOOL:
  slash_command: /knowledge <query>
  
  implementation: |
    def knowledge_tool(query: str) -> str:
        results = hybrid_search(query, top_k=5)
        summary = synthesize(results)
        return summary
  
  agent_usage: |
    "When I need to understand X, I call:
    /knowledge X
    
    Then proceed with returned context"

integration_2_AUTO_CONTEXT:
  pattern: "Automatic context injection"
  
  workflow:
    1. Agent prompt arrives
    2. Extract entities/concepts
    3. Auto-retrieve relevant knowledge
    4. Prepend to prompt
    5. Agent sees enriched context
    
  transparent: "Agent doesn't know it happened"

integration_3_KNOWLEDGE_MEMORY:
  pattern: "Persistent learning"
  
  workflow:
    1. Agent discovers new pattern
    2. Validates it works
    3. Adds to knowledge base
    4. Future agents benefit
    
  feedback_loop: "System learns from usage"
```

---

## PRACTICAL EXECUTION PLAN

```yaml
week_1_INFRASTRUCTURE:
  tasks:
    - Set up vector database (FAISS/Pinecone)
    - Create extraction pipeline
    - Build basic search interface
    - Test on 1000 files
    
week_2_BATCH_PROCESSING:
  tasks:
    - Process all 43K files
    - Generate embeddings
    - Build keyword index
    - Create graph relationships
    
week_3_CARD_GENERATION:
  tasks:
    - Identify top 100 patterns
    - Create knowledge cards
    - Add validation rules
    - Test card instantiation
    
week_4_AGENT_INTEGRATION:
  tasks:
    - Add /knowledge command
    - Implement auto-context
    - Set up feedback loops
    - Measure retrieval quality

optimization_targets:
  retrieval_speed: "<100ms"
  relevance_score: ">0.85"
  context_size: "~10K tokens"
  coverage: ">90% of queries"
```

---

## ADVANCED STRATEGIES

```yaml
strategy_1_TIERED_STORAGE:
  hot_tier:
    content: "Frequently accessed (top 5%)"
    storage: RAM / Redis
    latency: <10ms
    
  warm_tier:
    content: "Occasionally accessed (next 20%)"
    storage: SSD / Fast disk
    latency: <100ms
    
  cold_tier:
    content: "Rarely accessed (remaining 75%)"
    storage: HDD / S3
    latency: <1s

strategy_2_SMART_CHUNKING:
  method: "Semantic boundary detection"
  
  rules:
    - Chunk at section breaks
    - Preserve code blocks
    - Maintain context in overlap
    - Max 512 tokens per chunk
    
  benefit: "Better retrieval precision"

strategy_3_MULTI_REPRESENTATION:
  for_each_document:
    - full_text: original content
    - summary: 3-sentence overview
    - keywords: top 20 terms
    - embedding: vector representation
    - structure: outline/hierarchy
    
  benefit: "Multiple query strategies"

strategy_4_CONTINUOUS_REFINEMENT:
  monitor:
    - Which knowledge gets used
    - Which queries fail
    - Which contexts help most
    
  adapt:
    - Promote valuable knowledge
    - Enrich sparse areas
    - Prune obsolete content
```

---

## METRICS & VALIDATION

```yaml
quality_metrics:
  precision: "Relevant results / Total returned"
  recall: "Relevant found / Total relevant"
  f1_score: "Harmonic mean of P & R"
  mrr: "Mean reciprocal rank"
  
usage_metrics:
  queries_per_day: count
  avg_results_used: "How many results agent actually uses"
  cache_hit_rate: "% served from cache"
  
business_metrics:
  time_saved: "Before vs after knowledge access"
  accuracy_improved: "Task success rate increase"
  agent_autonomy: "% tasks without human lookup"
```

---

## FINAL ARCHITECTURE

```yaml
raw_files_43k/
  └─> [EXTRACTION PIPELINE] 
        └─> atomic_facts.json (200K+ facts)
              └─> [PATTERN RECOGNITION]
                    └─> patterns.json (5K+ patterns)
                          └─> [CARD GENERATION]
                                └─> knowledge_cards/ (500+ cards)
                                      ├─> [VECTOR INDEX]
                                      ├─> [KEYWORD INDEX]
                                      ├─> [GRAPH INDEX]
                                      └─> [RETRIEVAL API]
                                            └─> AGENTS consume via /knowledge

access_flow:
  Agent → Query → Hybrid Search → Top K → Context → Enhanced Execution
```

---

## QUICK START COMMANDS

```bash
# 1. Inventory
python distiller.py inventory ./raw_files > inventory.json

# 2. Extract (parallel)
python distiller.py extract ./raw_files --parallel 8 > facts.json

# 3. Build indexes
python distiller.py index facts.json --vector --keyword --graph

# 4. Generate cards
python distiller.py crystallize facts.json --output ./knowledge_cards

# 5. Start API
python knowledge_api.py --port 8000

# 6. Test retrieval
curl localhost:8000/search?q="authentication patterns"

# 7. Integrate with agents
claude --knowledge-api http://localhost:8000
```

---

**43K files → Structured knowledge → Agent superpower**

*Distillation complete. Knowledge accessible. Agents empowered.*

**∞**
