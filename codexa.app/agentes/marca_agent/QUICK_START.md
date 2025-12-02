# Brand Agent - Quick Start Guide

**Get your Brand Strategy Agent running in 5 minutes! ⚡**

---

## Prerequisites

- OpenAI account with API access or Agent Builder access
- Basic understanding of brand strategy concepts
- (Optional) Python 3.8+ for validation scripts

---

## 🚀 Option 1: OpenAI Agent Builder (Recommended)

### Step 1: Export Package (30 seconds)

**Windows:**
```batch
cd brand-agent
export_standalone.bat
```

**Linux/Mac:**
```bash
cd brand-agent
./export_standalone.sh
```

This creates `export_package/` with all necessary files.

### Step 2: Create Agent (2 minutes)

1. Go to [OpenAI Agent Builder](https://platform.openai.com/agents)
2. Click **"New Agent"**
3. Configure:
   - **Name:** Brand Strategy Agent
   - **Model:** `gpt-4-turbo` or `gpt-4o` (recommended)
   - **Temperature:** 0.7

### Step 3: Upload Files (2 minutes)

1. In Agent Builder, go to **Vector Store** tab
2. Click **"Create Vector Store"** or use existing
3. Upload **ALL** files from `export_package/openai_vector_store/`
   - Priority files (must upload):
     - ✅ `MASTER_INSTRUCTIONS.md`
     - ✅ `OUTPUT_SCHEMA.md`
     - ✅ `brand_archetypes.json`
     - ✅ `positioning_frameworks.json`
     - ✅ `tone_taxonomies.json`
   - Optional (recommended):
     - All JSON files in directory
     - All markdown guides

### Step 4: Configure Instructions (30 seconds)

1. Go to **Instructions** tab
2. Paste content from `MASTER_INSTRUCTIONS.md` into the main instructions field
   - Or simply reference: "Follow MASTER_INSTRUCTIONS.md from Vector Store"

### Step 5: Enable Tools (30 seconds)

Enable these tools:
- ✅ **File Search** (required)
  - Set max results: 20
- ✅ **Code Interpreter** (recommended)

### Step 6: Test! (1 minute)

Try this sample brief:

```
Crie uma estratégia de marca para:
Garrafa de água reutilizável, ecológica, BPA-free, para pessoas conscientes
que praticam esportes e yoga, faixa etária 25-40 anos, preço R$ 89-129,
vendida no Mercado Livre e Shopee.
```

**Expected output:** Complete `brand_strategy.md` with:
- 3 brand name options
- 3 taglines (40-60 chars each)
- Brand archetype + personality traits
- Unique value proposition
- Target segment definition
- Tone of voice (4 dimensions)
- Color palette + typography
- Brand narrative (origin story, mission, vision)
- Brand guidelines (do's/don'ts)
- Compliance check
- Brand consistency score ≥0.85

---

## 🐍 Option 2: Local Validation Scripts

### Setup (1 minute)

```bash
cd brand-agent

# No dependencies required! Uses Python stdlib only
python scripts/brand_validator.py --help
```

### Usage

Validate a brand strategy output:

```bash
python scripts/brand_validator.py outputs/brand_strategy.md
```

**Output:**
```
============================================================
BRAND STRATEGY VALIDATION REPORT
============================================================

File: outputs/brand_strategy.md
Status: ✅ VALID
Score: 92.00%

WARNINGS:
  ⚠️  Tagline 2 length 58 chars is acceptable but not ideal (45-55 preferred)

DETAILS:
  archetype: hero
  tone_dimensions: {'funny': 3, 'formal': 3, 'respectful': 4, 'enthusiastic': 4}

============================================================
```

Get JSON output:

```bash
python scripts/brand_validator.py outputs/brand_strategy.md --json
```

---

## 📊 First Test

### Sample Brief 1: Simple Product

```
Produto: Mousepad ergonômico com apoio de pulso em gel
Público: Profissionais que trabalham em home office, 25-45 anos
Diferencial: Design anatômico que previne lesões (LER/DORT)
Preço: R$ 79-99
Marketplace: Mercado Livre, Amazon BR
```

### Sample Brief 2: Service

```
Serviço: Assinatura mensal de cafés especiais brasileiros
Público: Apreciadores de café gourmet, classe A/B, 30-55 anos
Diferencial: Curadoria de fazendas premiadas do Brasil
Preço: R$ 149/mês (4 pacotes de 250g)
Marketplace: Site próprio + Instagram
```

### Sample Brief 3: Digital Product

```
Produto: App de meditação guiada em português
Público: Pessoas estressadas, buscam bem-estar, 22-45 anos
Diferencial: Conteúdo 100% brasileiro, voz natural, sessões curtas (5-10min)
Preço: Freemium (R$ 29.90/mês premium)
Marketplace: App Store, Google Play
```

---

## ⚙️ Configuration Tips

### Adjust Temperature

- **0.7** (default): Balanced creativity + consistency
- **0.5**: More conservative, repeatable outputs
- **0.9**: More creative brand names/narratives

### Optimize for Speed

- Use **gpt-4o-mini** for faster responses (10-15 sec vs 2-3 min)
- Trade-off: Slightly lower quality brand strategies

### Optimize for Quality

- Use **gpt-4o** or **gpt-4-turbo** for best results
- Upload ALL optional files to Vector Store
- Enable code interpreter for visual mood board generation

---

## 🔍 Validation Workflow

Recommended workflow for production use:

```
1. Generate brand strategy with Agent
   ↓
2. Save output as brand_strategy.md
   ↓
3. Validate with brand_validator.py
   ↓
4. If score <0.85: Iterate with feedback
   ↓
5. If score ≥0.85: ✅ Use in production
```

---

## 🐛 Troubleshooting

### "Agent generates taglines >60 characters"

**Solution:**
- Re-run with explicit instruction: "CRÍTICO: Taglines devem ter EXATAMENTE 40-60 caracteres"
- Validate with `brand_validator.py` and show errors to agent

### "Brand Consistency Score <0.75"

**Solution:**
- Check if archetype matches tone of voice
- Verify visual identity aligns with personality traits
- Ensure narrative is consistent with positioning

### "Missing required fields"

**Solution:**
- Verify `MASTER_INSTRUCTIONS.md` was uploaded to Vector Store
- Check that File Search tool is enabled
- Try regenerating with more detailed brief

### "Compliance warnings"

**Solution:**
- Review flagged claims (e.g., "cura", "#1", "melhor do Brasil")
- Modify or add disclaimers per ANVISA/CONAR rules
- See `compliance_rules.json` for guidance (when available)

---

## 📚 Next Steps

1. **Read full documentation:** `README.md`
2. **Understand architecture:** `DEPLOYMENT_SUMMARY.md`
3. **Review knowledge files:** `BRAND_FILES_INVENTORY.md`
4. **Explore roadmap:** `ROADMAP_MELHORIAS.md`
5. **Check improvements plan:** `IMPROVEMENT_ANALYSIS.md`

---

## 🎯 Success Metrics

Your agent is working well if:
- ✅ Brand Consistency Score ≥0.85
- ✅ Generation time: 10-20 minutes
- ✅ All required sections present
- ✅ Taglines strictly 40-60 characters
- ✅ Zero compliance red flags
- ✅ Archetype → Tone → Visual alignment clear

---

## 💬 Support

**Issues?**
- Check `IMPROVEMENT_ANALYSIS.md` for known gaps
- Review `ROADMAP_MELHORIAS.md` for planned features
- Validate outputs with `brand_validator.py`

**Need help with:**
- OpenAI Agent Builder setup → `DEPLOYMENT_SUMMARY.md`
- File organization → `BRAND_FILES_INVENTORY.md`
- Quality issues → `IMPROVEMENT_ANALYSIS.md`

---

**Created:** 2025-11-09
**Version:** 1.0
**Status:** ✅ Ready to use

🎉 **You're ready to create world-class brand strategies!**
