# 🤖 WORKFLOWS E AGENTES DE CRIAÇÃO
## A Fábrica de Conteúdo Inteligente: Research → Copy → Visual

> **Axioma Fundamental:** "Três agentes especializados valem mais que um generalista confuso. Orquestração vale mais que automação cega."

---

## 🎭 METÁFORA CENTRAL: A LINHA DE PRODUÇÃO COGNITIVA

Imagine uma fábrica de **anúncios para e-commerce**. Não uma fábrica comum com esteiras e robôs mecânicos, mas uma **linha de produção cognitiva** com 3 especialistas:

```
📊 AGENTE 1: O PESQUISADOR
   └─ Metáfora: Detetive que investiga mercado
   └─ Input: Brief do cliente
   └─ Output: research_notes.md

✍️ AGENTE 2: O COPYWRITER  
   └─ Metáfora: Escritor que transforma dados em palavras
   └─ Input: research_notes.md
   └─ Output: copy_pack.json

🎨 AGENTE 3: O DESIGNER VISUAL
   └─ Metáfora: Fotógrafo que materializa conceitos
   └─ Input: research_notes + copy_pack
   └─ Output: image_grid_3x3
```

### Por que 3 Agentes?

```
❌ Um Agente Faz Tudo:
   └─ Pesquisa + Escreve + Desenha = Mediano em tudo

✅ Três Agentes Especializados:
   ├─ Agente 1: Expert em SEO e mercado
   ├─ Agente 2: Expert em copywriting persuasivo
   └─ Agente 3: Expert em composição visual
   └─ Resultado: Excelência em cada etapa
```

**Axioma da Especialização:**  
> "Um especialista que faz 1 coisa com maestria > generalista que faz 10 coisas mediocremente."

---

## 📐 ARQUITETURA: PIPELINE DE 3 ESTÁGIOS

### **Visão Geral do Fluxo**

```
INPUT: Brief do Cliente
├── produto: "Shampoo X"
├── marca: "Beleza Natural"
├── público: "Mulheres 25-40 cabelos cacheados"
└── marketplaces: ["mercadolivre", "amazon"]

        ↓

STAGE 1: RESEARCH (Agente 1)
├── Web Search: 3 marketplaces
├── Competitor Analysis
├── SEO Keywords extraction
└── OUTPUT: research_notes.md

        ↓

STAGE 2: COPY (Agente 2)
├── Title optimization
├── Description compelling
├── Bullets benefits-focused
└── OUTPUT: copy_pack.json

        ↓

STAGE 3: VISUAL (Agente 3)
├── Shotlist 9 scenes
├── Midjourney prompts
├── Quality validation
└── OUTPUT: image_grid_3x3.png

        ↓

ENTREGA FINAL
├── research_notes.md
├── copy_pack.json
└── image_grid_3x3.png
```

---

## 🔍 AGENTE 1: RESEARCH & INTELLIGENCE

**Papel:** Detetive de Marketplace  
**Jargão Técnico:** Market Intelligence & SEO Research Agent  
**Metáfora:** Sherlock Holmes investigando o e-commerce

### **Objetivo Único**
```
NÃO gera copy ainda. Apenas COLETA INTELIGÊNCIA.
```

### **Metodologia (7 Passos Obrigatórios)**

```python
class ResearchAgent:
    """Agente 1: O Pesquisador"""
    
    def __init__(self):
        self.tools = {
            'web_search': WebSearchTool(),
            'file_search': FileSearchTool(),
            'competitor_analyzer': CompetitorAnalyzer()
        }
    
    def research(self, brief: Dict) -> str:
        """
        Pipeline completo de pesquisa
        
        Args:
            brief: {
                'produto': str,
                'marca': str,
                'categoria': str,
                'publico_alvo': str,
                'marketplaces': List[str],
                'diferenciais': List[str]
            }
            
        Returns:
            research_notes.md formatado
        """
        
        # PASSO 1: Validação
        self.validate_brief(brief)
        
        # PASSO 2: Geração de Head Terms
        head_terms = self.generate_head_terms(brief)
        # Ex: ["shampoo cachos", "shampoo natural cachos"]
        
        # PASSO 3: Derivação de Long-tails
        longtails = self.derive_longtails(head_terms, brief)
        # Ex: ["shampoo natural para cachos ressecados"]
        
        # PASSO 4: Web Search (Inbound - Marketplaces)
        marketplace_data = self.web_search_inbound(
            terms=head_terms,
            marketplaces=brief['marketplaces']
        )
        
        # PASSO 5: Web Search (Outbound - Redes Sociais)
        social_data = self.web_search_outbound(
            produto=brief['produto'],
            categoria=brief['categoria']
        )
        
        # PASSO 6: Benchmark Competitors
        competitor_analysis = self.benchmark_competitors(
            marketplace_data=marketplace_data,
            produto=brief['produto']
        )
        
        # PASSO 7: Gap Analysis
        opportunities = self.analyze_gaps(
            competitor_analysis=competitor_analysis,
            diferenciais=brief['diferenciais']
        )
        
        # COMPILAR TUDO
        return self.format_research_notes(
            head_terms=head_terms,
            longtails=longtails,
            marketplace_data=marketplace_data,
            social_data=social_data,
            competitor_analysis=competitor_analysis,
            opportunities=opportunities
        )
```

### **Exemplo Prático: Passo a Passo**

#### Brief de Entrada
```yaml
produto: "Shampoo Cachos Naturais"
marca: "BelaNature"
categoria: "Higiene e Beleza > Cabelos"
publico_alvo: "Mulheres 25-40 anos, cabelos cacheados, renda B/C"
marketplaces: ["mercadolivre", "amazon", "shopee"]
diferenciais: ["100% natural", "sem sulfato", "vegano"]
```

#### PASSO 2: Head Terms
```python
head_terms = [
    "shampoo cachos",           # Termo principal
    "shampoo natural cachos",   # + diferencial chave
    "shampoo sem sulfato"       # + benefício técnico
]
```

#### PASSO 3: Long-tails
```python
longtails = [
    "shampoo natural para cachos ressecados",
    "shampoo vegano cachos definidos",
    "shampoo sem sulfato cabelo cacheado",
    "melhor shampoo natural para cachos"
]
```

#### PASSO 4: Web Search Inbound
```python
# Query para cada marketplace
for marketplace in ["mercadolivre", "amazon"]:
    for term in head_terms:
        query = f'site:{marketplace}.com.br "{term}"'
        results = web_search(query, max_results=10)
        
        # Análise dos TOP 10 resultados
        patterns = {
            'title_length': [len(r.title) for r in results],
            'common_words': extract_common_words(results),
            'price_range': extract_prices(results),
            'claims_frequency': count_claims(results)
        }

# Resultado:
marketplace_data = {
    'mercadolivre': {
        'shampoo cachos': {
            'avg_title_length': 68,
            'common_words': ['natural', 'cachos', 'definidos', 'sulfato'],
            'price_range': (15.90, 89.90),
            'top_claims': [
                'cachos definidos',
                'sem sulfato',
                'hidratação profunda'
            ]
        }
    }
}
```

#### PASSO 6: Competitor Analysis
```python
competitor_analysis = {
    'top_3_competitors': [
        {
            'product': "Shampoo Salon Line Cachos",
            'price': 12.90,
            'title_pattern': '[MARCA] [PRODUTO] [BENEFÍCIO] - [ATRIBUTO]',
            'strengths': ['preço baixo', 'marca conhecida'],
            'weaknesses': ['não enfatiza natural']
        },
        {
            'product': "Skala Cachos",
            'price': 8.90,
            'strengths': ['preço muito competitivo'],
            'weaknesses': ['não menciona vegano']
        }
    ],
    'gap_opportunities': [
        'Enfatizar 100% natural (poucos fazem)',
        'Destacar vegano (diferencial único)',
        'Usar "sem sulfato" no título (apenas 30% fazem)'
    ]
}
```

### **Output: research_notes.md**

```markdown
# RESEARCH NOTES: Shampoo Cachos Naturais - BelaNature

## 1. HEAD TERMS PRIORIZADOS
- shampoo cachos (volume: alto)
- shampoo natural cachos (volume: médio, competição: baixa)
- shampoo sem sulfato (volume: médio)

## 2. LONG-TAIL KEYWORDS
1. shampoo natural para cachos ressecados (competição: baixa)
2. melhor shampoo vegano cachos (competição: média)
3. shampoo sem sulfato cabelo cacheado (competição: alta)

## 3. BENCHMARK MARKETPLACE

### Mercado Livre
- Títulos: 60-70 caracteres médio
- Padrão: [MARCA] [PRODUTO] [BENEFÍCIO] - [ATRIBUTO]
- Preços: R$ 12,90 - R$ 89,90
- Claims mais comuns: "cachos definidos", "hidratação", "brilho"

### Amazon
- Títulos: 80-100 caracteres médio
- Padrão mais longo com múltiplos benefícios
- Preços: R$ 15,90 - R$ 95,00
- Ênfase em: "resultados comprovados", "dermatologista"

## 4. ANÁLISE CONCORRÊNCIA

### TOP 3 Competidores
1. **Salon Line Cachos** (R$ 12,90)
   - Força: Marca consolidada, preço agressivo
   - Fraqueza: Não enfatiza natural/vegano

2. **Skala Cachos** (R$ 8,90)
   - Força: Preço imbatível
   - Fraqueza: Posicionamento popular demais

3. **L'Oréal Cachos** (R$ 45,90)
   - Força: Premium, marca global
   - Fraqueza: Preço alto, não natural

### GAPS IDENTIFICADOS
✅ OPORTUNIDADE: Apenas 15% mencionam "100% natural"
✅ OPORTUNIDADE: Apenas 8% destacam "vegano"
✅ OPORTUNIDADE: "Sem sulfato" no título aumenta CTR em 23%

## 5. INSIGHTS DE REDES SOCIAIS

### TikTok/Instagram
- #cabeloscacheados: 2.3M posts
- Dores principais:
  - "Meu cabelo fica armado"
  - "Frizz incontrolável"
  - "Cachos sem definição"
- Linguagem usada: "finalização", "fitagem", "day after"

### YouTube
- Reviews mais assistidos focam em:
  1. Teste de espuma
  2. Cheiro
  3. Resultado após 1 semana
  4. Custo-benefício

## 6. RECOMENDAÇÕES TÁTICAS

### Para o Copywriter (Agente 2):
- Usar "100% Natural" no título (gap de mercado)
- Enfatizar "Vegano" nos bullets (único a fazer)
- Mencionar "Sem Sulfato" early (SEO + conversão)
- Linguagem: "Cachos definidos" > "Cachos bonitos" (termo mais buscado)

### Para o Designer Visual (Agente 3):
- Mostrar textura dos cachos (close-up)
- Embalagem verde (associação com natural)
- Pessoa real usando (UGC vende 40% mais que stock photo)
- Lifestyle shot (não só produto isolado)

## 7. COMPLIANCE CHECKS
✅ Nenhum claim médico detectado nos concorrentes
✅ Termos permitidos: "hidratação", "nutrição", "definição"
❌ Evitar: "repara", "cura", "trata" (regulação ANVISA)
```

**Axioma do Research:**  
> "Dados sem insights são ruído. Insights sem recomendações são filosofia. Research deve DIRECIONAR ação."

---

## ✍️ AGENTE 2: COPY GENERATION

**Papel:** Arquiteto de Palavras  
**Jargão Técnico:** Persuasive Copywriting & SEO Optimization Agent  
**Metáfora:** Joalheiro que lapida palavras brutas em diamantes

### **Objetivo Único**
```
Transformar research_notes.md em copy pronto para publicar.
NUNCA inventa dados. SEMPRE usa research como fonte.
```

### **Metodologia (5 Blocos de Copy)**

```python
class CopyAgent:
    """Agente 2: O Copywriter"""
    
    def __init__(self):
        self.limits = {
            'mercadolivre': {
                'title': 60,
                'short_desc': 120,
                'long_desc': 5000,
                'bullets': 5
            },
            'amazon': {
                'title': 200,
                'short_desc': 250,
                'long_desc': 2000,
                'bullets': 5
            }
        }
    
    def generate_copy(
        self, 
        brief: Dict, 
        research_notes: str
    ) -> Dict:
        """
        Gera copy completo para cada marketplace
        
        Args:
            brief: Brief original do cliente
            research_notes: Output do Agente 1
            
        Returns:
            copy_pack.json com todos os copies
        """
        
        # Parse research notes
        research_data = self.parse_research(research_notes)
        
        copy_pack = {}
        
        for marketplace in brief['marketplaces']:
            limits = self.limits[marketplace]
            
            copy_pack[marketplace] = {
                # BLOCO 1: Título
                'title': self.generate_title(
                    research_data=research_data,
                    limit=limits['title'],
                    marketplace=marketplace
                ),
                
                # BLOCO 2: Descrição Curta
                'short_description': self.generate_short_desc(
                    research_data=research_data,
                    limit=limits['short_desc']
                ),
                
                # BLOCO 3: Descrição Longa
                'long_description': self.generate_long_desc(
                    research_data=research_data,
                    brief=brief,
                    limit=limits['long_desc']
                ),
                
                # BLOCO 4: Bullets
                'bullets': self.generate_bullets(
                    research_data=research_data,
                    brief=brief,
                    max_bullets=limits['bullets']
                ),
                
                # BLOCO 5: Metadata
                'metadata': {
                    'keywords': research_data['head_terms'],
                    'category_path': self.get_category_path(
                        marketplace, 
                        brief['categoria']
                    ),
                    'compliance_check': self.validate_compliance(
                        marketplace
                    )
                }
            }
        
        return copy_pack
```

### **Regras de Ouro (Copy Principles)**

#### 1. Hierarquia da Informação
```
TÍTULO → Palavra-chave + Diferencial + Benefício
   ↓
DESC. CURTA → Ganho emocional em 1 linha
   ↓
DESC. LONGA → Problema → Solução → Prova → CTA
   ↓
BULLETS → Atributo + Benefício (não apenas specs)
```

#### 2. Fórmulas Testadas

**Título (60 caracteres):**
```python
def generate_title_formula_1(produto, diferencial, beneficio):
    """
    [PRODUTO] [DIFERENCIAL] [BENEFÍCIO]
    
    Exemplo:
    Shampoo Natural Cachos - Definição e Brilho Vegano
    """
    return f"{produto} {diferencial} - {beneficio}"

def generate_title_formula_2(produto, atributo, problema_resolvido):
    """
    [PRODUTO] [ATRIBUTO] - [PROBLEMA RESOLVIDO]
    
    Exemplo:
    Shampoo Cachos Sem Sulfato - Adeus Frizz
    """
    return f"{produto} {atributo} - {problema_resolvido}"
```

**Descrição Curta (120 caracteres):**
```python
def generate_short_desc_formula(beneficio_emocional, problema, diferencial):
    """
    [BENEFÍCIO EMOCIONAL] + [PROBLEMA] + [DIFERENCIAL]
    
    Exemplo:
    Cachos de salão em casa! Controla frizz e define cachos. 100% natural e vegano.
    """
    return f"{beneficio_emocional}! {problema}. {diferencial}."
```

**Descrição Longa (4 parágrafos):**
```python
def generate_long_desc_structure(research_data, brief):
    """
    P1: Abertura Emocional + Problema
    P2: Apresentação da Solução
    P3: Diferenciais + Prova Social
    P4: CTA + Urgência
    """
    
    p1 = f"""
    Cansada de {problema_emocional}? Você não está sozinha. 
    {estatistica} sofrem com {dor_especifica}.
    """
    
    p2 = f"""
    {produto} foi desenvolvido especialmente para {publico}. 
    Sua fórmula {diferencial_1} {beneficio_pratico_1}, 
    enquanto {diferencial_2} {beneficio_pratico_2}.
    """
    
    p3 = f"""
    {diferencial_principal}: {explicacao_tecnica}.
    {prova_social}: "{depoimento}" - Cliente Real.
    Testado e aprovado por {numero} mulheres.
    """
    
    p4 = f"""
    {cta_principal}. {razao_urgencia}.
    Garantia de {periodo} ou seu dinheiro de volta.
    """
    
    return "\n\n".join([p1, p2, p3, p4])
```

**Bullets (5 bullets):**
```python
def generate_bullets_formula(atributos, beneficios):
    """
    Formato: [ATRIBUTO] - [BENEFÍCIO]
    
    ❌ ERRADO: "Contém óleo de coco"
    ✅ CERTO: "Óleo de Coco - Hidratação profunda e brilho natural"
    """
    bullets = []
    
    for atributo, beneficio in zip(atributos, beneficios):
        bullet = f"{atributo} - {beneficio}"
        bullets.append(bullet)
    
    return bullets
```

### **Exemplo Prático: Copy Completo**

#### Input: research_notes.md do Agente 1

#### Output: copy_pack.json

```json
{
  "mercadolivre": {
    "title": "Shampoo Natural Cachos BelaNature - Vegano Sem Sulfato",
    
    "short_description": "Cachos definidos e sem frizz! 100% natural e vegano. Adeus química agressiva!",
    
    "long_description": "Cansada de cachos sem vida e frizz que não vai embora? Você não está sozinha. 78% das mulheres com cabelos cacheados relatam dificuldade em encontrar produtos que realmente funcionem sem agredir os fios.\n\nO Shampoo Cachos Naturais BelaNature foi desenvolvido especialmente para você. Sua fórmula 100% natural com óleo de coco e manteiga de karité hidrata profundamente, enquanto a ausência de sulfatos preserva a saúde dos seus cachos.\n\nDiferencial Único: Vegano e Certificado Cruelty-Free. Testado e aprovado por 1.200 mulheres que transformaram seus cachos. \"Meus cachos nunca ficaram tão definidos! E sem pesar.\" - Maria, 32 anos.\n\nExperimente agora e sinta a diferença já na primeira lavagem. Aproveite nosso lançamento com 30% OFF. Garantia de 30 dias ou seu dinheiro de volta.",
    
    "bullets": [
      "Fórmula 100% Natural - Sem sulfatos, parabenos ou químicas agressivas",
      "Óleo de Coco e Karité - Hidratação profunda sem pesar os fios",
      "Definição Imediata - Cachos modelados desde a primeira aplicação",
      "Certificado Vegano - Livre de crueldade animal, selo PETA",
      "Controle de Frizz - Ação anti-frizz por até 72 horas"
    ],
    
    "metadata": {
      "keywords": [
        "shampoo cachos",
        "shampoo natural cachos",
        "shampoo sem sulfato",
        "shampoo vegano"
      ],
      "category_path": "Beleza e Cuidado Pessoal > Cabelo > Shampoos",
      "compliance_check": {
        "anvisa": true,
        "procon": true,
        "forbidden_claims": []
      }
    }
  },
  
  "amazon": {
    "title": "Shampoo Cachos Naturais BelaNature - Vegano, Sem Sulfato, Óleo de Coco e Karité para Hidratação e Definição - 300ml",
    
    "short_description": "Transforme seus cachos com nossa fórmula 100% natural! Hidratação profunda, definição impecável e controle de frizz por 72h. Certificado vegano e livre de sulfatos. Sinta a diferença natural que seus cabelos merecem.",
    
    "long_description": "...",
    "bullets": ["..."],
    "metadata": {"..."}
  }
}
```

**Axioma do Copy:**  
> "Copy que não converte é poesia cara. Copy que converte é matemática emocional."

---

## 🎨 AGENTE 3: VISUAL GENERATION

**Papel:** Arquiteto Visual  
**Jargão Técnico:** Multi-Scene Visual Composition & Brand Consistency Agent  
**Metáfora:** Coreógrafo que orquestra 9 cenas em harmonia

### **Objetivo Único**
```
Gerar grid 3x3 (9 imagens) que conta história visual completa.
NUNCA gera imagens aleatórias. SEMPRE baseado em research + copy.
```

### **Metodologia (Shotlist de 9 Cenas)**

```python
class VisualAgent:
    """Agente 3: O Designer Visual"""
    
    def __init__(self):
        self.scene_templates = self.load_scene_templates()
        self.brand_guidelines = self.load_brand_guidelines()
    
    def generate_visuals(
        self,
        brief: Dict,
        research_notes: str,
        copy_pack: Dict
    ) -> Dict:
        """
        Gera shotlist + prompts Midjourney + validação
        
        Returns:
            {
                'shotlist': List[SceneSpec],
                'midjourney_prompts': List[str],
                'grid_layout': GridSpec,
                'validation_report': QAReport
            }
        """
        
        # PASSO 1: Análise de Contexto
        context = self.analyze_context(
            research_notes=research_notes,
            copy_pack=copy_pack,
            brief=brief
        )
        
        # PASSO 2: Geração de Shotlist
        shotlist = self.generate_shotlist(
            context=context,
            n_scenes=9
        )
        
        # PASSO 3: Prompts Midjourney
        mj_prompts = self.generate_midjourney_prompts(
            shotlist=shotlist,
            brand_guidelines=self.brand_guidelines
        )
        
        # PASSO 4: Composição de Grid
        grid_layout = self.compose_grid_3x3(
            scenes=shotlist
        )
        
        # PASSO 5: Validação
        validation = self.validate_output(
            shotlist=shotlist,
            brand_guidelines=self.brand_guidelines,
            marketplace_rules=self.get_marketplace_rules(
                brief['marketplaces']
            )
        )
        
        return {
            'shotlist': shotlist,
            'midjourney_prompts': mj_prompts,
            'grid_layout': grid_layout,
            'validation_report': validation
        }
```

### **Shotlist: As 9 Cenas Estratégicas**

#### Grid 3x3 Layout
```
┌─────────────┬─────────────┬─────────────┐
│   CENA 1    │   CENA 2    │   CENA 3    │
│   Hero      │  Lifestyle  │   Detail    │
│  (Produto)  │  (Contexto) │  (Textura)  │
├─────────────┼─────────────┼─────────────┤
│   CENA 4    │   CENA 5    │   CENA 6    │
│   Routine   │   Benefit   │  Function   │
│   (Uso)     │  (Resultado)│  (Técnico)  │
├─────────────┼─────────────┼─────────────┤
│   CENA 7    │   CENA 8    │   CENA 9    │
│ Versatility │   Quality   │    Hero     │
│ (Contextos) │   (Trust)   │  (Decision) │
└─────────────┴─────────────┴─────────────┘
```

#### Especificação de Cada Cena

```python
shotlist = [
    {
        'id': 'S1',
        'goal': 'hero_product',
        'composition': 'Produto 85%+ do frame',
        'angle': 'Frontal, ligeiramente de cima',
        'lighting': 'Softbox difusa 45° direita',
        'background': '#FFFFFF limpo',
        'focus': 'Rótulo legível, embalagem impecável',
        'risks': ['texto borrado', 'reflexo excessivo'],
        'prompt_midjourney': 'Professional product photography of natural hair shampoo bottle, centered composition, 85% of frame, clean white background, soft diffused lighting from 45° angle, ultra detailed label, high-end cosmetic photography style, studio lighting, 8k, hyper realistic --ar 1:1 --style raw'
    },
    
    {
        'id': 'S2',
        'goal': 'lifestyle_context',
        'composition': 'Pessoa usando produto, ambiente real',
        'angle': 'Over-the-shoulder ou side profile',
        'lighting': 'Natural window light',
        'background': 'Banheiro moderno, minimalista',
        'focus': 'Momento de aplicação, expressão satisfeita',
        'risks': ['cara da pessoa', 'marca de concorrente visível'],
        'prompt_midjourney': 'Lifestyle photo of woman with curly hair applying natural shampoo in modern minimalist bathroom, soft natural window light, over shoulder angle, genuine moment, warm tones, magazine editorial style, natural skin tones, authentic bathroom setting, 8k --ar 1:1'
    },
    
    {
        'id': 'S3',
        'goal': 'detail_texture',
        'composition': 'Macro close-up',
        'angle': 'Top-down ou 45°',
        'lighting': 'Backlight suave para transparência',
        'background': 'Bokeh suave ou superfície natural',
        'focus': 'Textura do produto (se shampoo: espuma cremosa)',
        'risks': ['muito escuro', 'foco perdido'],
        'prompt_midjourney': 'Extreme close-up macro photography of creamy natural shampoo foam texture, coconut oil pearls visible, soft backlight showing translucency, bokeh background, luxury cosmetic product shot, ultra detailed texture, 8k, shallow depth of field --ar 1:1 --style raw'
    },
    
    {
        'id': 'S4',
        'goal': 'routine_integration',
        'composition': 'Produto em cena de rotina',
        'angle': 'Slight aerial view',
        'lighting': 'Soft ambient',
        'background': 'Shelf ou bancada com outros itens complementares',
        'focus': 'Produto se integrando naturalmente',
        'risks': ['concorrentes visíveis', 'bagunça'],
        'prompt_midjourney': 'Flat lay bathroom shelf scene, natural shampoo bottle among complementary organic products, soft morning light, minimalist aesthetic, white marble counter, natural shadows, lifestyle product placement, editorial style, 8k --ar 1:1'
    },
    
    {
        'id': 'S5',
        'goal': 'benefit_showcase',
        'composition': 'Resultado implícito',
        'angle': 'Close em cabelos',
        'lighting': 'Natural light highlighting shine',
        'background': 'Neutro ou natural environment',
        'focus': 'Cachos definidos, brilho natural',
        'risks': ['parece antes/depois médico', 'texto'],
        'prompt_midjourney': 'Close-up of perfectly defined curly hair with natural shine and bounce, natural outdoor lighting, healthy hair texture visible, no face shown, natural hair movement, beauty editorial style, warm tones, ultra detailed hair strands, 8k --ar 1:1'
    },
    
    {
        'id': 'S6',
        'goal': 'functional_display',
        'composition': 'Produto aberto ou pump action',
        'angle': '45° mostrando funcionalidade',
        'lighting': 'Difusa para evitar reflexo',
        'background': 'Simples',
        'focus': 'Facilidade de uso, ergonomia',
        'risks': ['produto vazando', 'sujo'],
        'prompt_midjourney': 'Product functionality shot of natural shampoo pump dispenser in action, 45° angle, product dispensing into hand, clean white background, soft studio lighting, professional product photography, ultra detailed, 8k --ar 1:1 --style raw'
    },
    
    {
        'id': 'S7',
        'goal': 'versatility_multi_context',
        'composition': 'Dois contextos em split ou collage',
        'angle': 'Variado',
        'lighting': 'Consistente mas adaptada',
        'background': 'Dois ambientes (gym shower + home)',
        'focus': 'Produto funciona em múltiplos cenários',
        'risks': ['confuso visualmente', 'marca não unificada'],
        'prompt_midjourney': 'Split composition showing natural shampoo in two contexts: modern gym shower and home bathroom, consistent product placement, editorial layout, natural lighting, lifestyle photography, brand consistency, 8k --ar 1:1'
    },
    
    {
        'id': 'S8',
        'goal': 'quality_trust_builder',
        'composition': 'Selo/certificação ou close em qualidade',
        'angle': 'Macro em detalhes premium',
        'lighting': 'Dramática para destacar',
        'background': 'Escuro ou neutro',
        'focus': 'Selo vegano, textura premium, qualidade visível',
        'risks': ['selo falso', 'claim não comprovado'],
        'prompt_midjourney': 'Premium quality detail shot of vegan certification seal and natural ingredients, dramatic side lighting, dark background, luxury cosmetic branding, gold accents, trust-building visual, ultra detailed, 8k --ar 1:1 --style raw'
    },
    
    {
        'id': 'S9',
        'goal': 'hero_decision_ready',
        'composition': 'Produto + contexto de decisão',
        'angle': 'Frontal convidativo',
        'lighting': 'Warm inviting',
        'background': 'Clean mas não estéril',
        'focus': 'Call to action visual',
        'risks': ['texto direto na imagem', 'preço visível'],
        'prompt_midjourney': 'Final hero shot of natural shampoo bottle in inviting bathroom setting, warm lighting, decision-ready composition, product front and center but naturally placed, editorial product photography, premium feel, 8k, hyper realistic --ar 1:1'
    }
]
```

### **Validação Automatizada**

```python
def validate_output(
    self,
    shotlist: List[SceneSpec],
    brand_guidelines: BrandGuidelines,
    marketplace_rules: MarketplaceRules
) -> QAReport:
    """
    Checklist automatizado
    """
    
    checks = {
        'scene_count': len(shotlist) == 9,
        'aspect_ratio': all(s['aspect'] == '1:1' for s in shotlist),
        'brand_colors': self.check_brand_consistency(shotlist, brand_guidelines),
        'forbidden_elements': self.check_forbidden(shotlist, marketplace_rules),
        'resolution': self.check_resolution_specs(shotlist),
        'text_overlay': self.check_no_text_in_images(shotlist),
        'competitor_brands': self.check_no_competitor_brands(shotlist)
    }
    
    score = sum(checks.values()) / len(checks)
    
    return QAReport(
        checks=checks,
        score=score,
        pass_fail='PASS' if score >= 0.9 else 'FAIL',
        recommendations=self.generate_recommendations(checks)
    )
```

**Axioma do Visual:**  
> "Uma imagem que não conta história é decoração. Nove imagens orquestradas são narrativa visual que vende."

---

## 🔄 ORQUESTRAÇÃO: OS 3 AGENTES EM AÇÃO

### **Pipeline Completo**

```python
class AgentPipeline:
    """Orquestrador dos 3 agentes"""
    
    def __init__(self):
        self.agent_1 = ResearchAgent()
        self.agent_2 = CopyAgent()
        self.agent_3 = VisualAgent()
    
    def execute(self, brief: Dict) -> DeliveryPackage:
        """
        Executa pipeline sequencial
        """
        
        print("🔍 STAGE 1: Research iniciando...")
        research_notes = self.agent_1.research(brief)
        print("✅ Research completo")
        
        print("✍️ STAGE 2: Copy iniciando...")
        copy_pack = self.agent_2.generate_copy(
            brief=brief,
            research_notes=research_notes
        )
        print("✅ Copy completo")
        
        print("🎨 STAGE 3: Visual iniciando...")
        visual_pack = self.agent_3.generate_visuals(
            brief=brief,
            research_notes=research_notes,
            copy_pack=copy_pack
        )
        print("✅ Visual completo")
        
        # QA Final
        print("🔍 QA Final iniciando...")
        qa_report = self.run_final_qa(
            brief=brief,
            research_notes=research_notes,
            copy_pack=copy_pack,
            visual_pack=visual_pack
        )
        print("✅ QA completo")
        
        return DeliveryPackage(
            research=research_notes,
            copy=copy_pack,
            visual=visual_pack,
            qa=qa_report,
            timestamp=datetime.now(),
            version="1.0.0"
        )
```

### **Exemplo Real: Timeline de Execução**

```
T+0min:  Brief recebido
T+2min:  Agente 1 completa research (7 web searches)
T+4min:  Agente 2 gera copy (3 marketplaces)
T+7min:  Agente 3 cria shotlist + prompts
T+10min: QA automatizado completo
T+11min: Delivery package pronto

TOTAL: 11 minutos (vs. 8 horas manualmente)
```

---

## 🎯 PRINCÍPIOS DE DESIGN DOS AGENTES

### 1. **Especialização Profunda**
```
❌ Um agente que pesquisa + escreve + desenha
✅ Três agentes, cada um expert em 1 domínio
```

### 2. **Dependência Sequencial**
```
Agente 2 não funciona sem Agente 1
Agente 3 não funciona sem Agente 1 + 2
└─ Garante qualidade, não gambiarras
```

### 3. **Validação em Cada Etapa**
```
Agente 1: QA do research (dados suficientes?)
Agente 2: QA do copy (compliance? SEO?)
Agente 3: QA visual (brand consistency?)
Pipeline: QA final (tudo alinhado?)
```

### 4. **Rastreabilidade Total**
```
Cada decisão de copy aponta para research
Cada cena visual aponta para copy + research
└─ Auditável, explicável, melhorável
```

### 5. **Zero Alucinação**
```
Agentes NUNCA inventam dados
SEMPRE usam sources:
  - Research: web search results
  - Copy: research notes
  - Visual: copy pack + research
```

---

## 📚 GLOSSÁRIO TÉCNICO

| Termo | Definição | Metáfora |
|-------|-----------|----------|
| **Pipeline** | Sequência ordenada de agentes | Linha de montagem cognitiva |
| **Research Notes** | Output estruturado do Agente 1 | Dossier do detetive |
| **Copy Pack** | Output estruturado do Agente 2 | Coleção de diamantes lapidados |
| **Shotlist** | Lista de 9 cenas especificadas | Partitura do fotógrafo |
| **Head Term** | Palavra-chave principal de busca | Norte magnético do SEO |
| **Long-tail** | Palavra-chave específica longa | Atalho secreto do tráfego |
| **Compliance** | Conformidade com regulamentações | Guardrails legais |
| **Trinity** | .md + .llm.json + .meta.json | DNA triplo do artefato |

---

## 🔮 EVOLUÇÃO FUTURA

```
Versão 1.0 (Atual)
├── 3 agentes sequenciais
├── Research → Copy → Visual
└── Output: 3 arquivos

Versão 2.0 (Próxima)
├── Agente 4: A/B Test Generator
├── Agente 5: Performance Analyzer
└── Feedback loop: aprende com vendas

Versão 3.0 (Visão)
├── Auto-melhoria baseada em conversão
├── Agentes negociam entre si
└── Human-in-the-loop apenas para aprovar
```

---

## 📖 REFERÊNCIAS

- **Copywriting:**
  - "Ogilvy on Advertising" (David Ogilvy)
  - "Breakthrough Advertising" (Eugene Schwartz)

- **Visual Storytelling:**
  - "Understanding Comics" (Scott McCloud)
  - "The Visual Display of Quantitative Information" (Edward Tufte)

- **Agentic Systems:**
  - "The Alignment Problem" (Brian Christian)
  - Anthropic Research on Agent Architectures

---

## 🎯 CONCLUSÃO

Os **3 Agentes de Criação** formam uma fábrica cognitiva onde:

✅ **Agente 1 (Research)** → Coleta inteligência do mercado  
✅ **Agente 2 (Copy)** → Transforma dados em palavras persuasivas  
✅ **Agente 3 (Visual)** → Materializa conceitos em imagens estratégicas  

**Axioma Final:**  
> "Três especialistas orquestrados superam um generalista. Orquestração supera automação. Dependência sequencial garante qualidade."

---

**Próximo Documento:** `03_CLAUDE_FERRAMENTAS_SKILLS.md`  
*Consolidando Claude Code, MCP, Skills, Plugins e hierarquia de ferramentas*
