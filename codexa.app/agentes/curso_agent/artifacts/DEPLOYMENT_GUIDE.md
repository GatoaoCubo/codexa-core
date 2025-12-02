# Deployment Guide | Hotmart Course Builder Agent

## 🚀 Quick Deploy (5 Minutes)

### Prerequisites Checklist
- [ ] OpenAI API account OR Anthropic API account OR CODEXA system access
- [ ] `MASTER_INSTRUCTIONS.md` file ready
- [ ] Context files (optional): market research, product announcement, brand strategy
- [ ] Internet connection (for API calls)

---

## 📍 Deployment Path A: OpenAI Agent Builder (Recommended for Beginners)

### Step 1: Access Agent Builder
1. Go to: https://platform.openai.com/playground
2. Click "Agents" tab (or "Assistants" if older interface)
3. Click "+ Create New Agent"

### Step 2: Configure Basic Settings
```
Name: Hotmart Course Builder Agent
Model: gpt-4o (recommended) or gpt-4o-mini (cost-effective)
Temperature: 0.7
Max Tokens: 16000
```

### Step 3: Load Instructions
1. Open `MASTER_INSTRUCTIONS.md` in a text editor
2. Copy entire content (Ctrl+A, Ctrl+C)
3. Paste into "Instructions" field in Agent Builder
4. Save

### Step 4: Enable Tools
Check these boxes:
- ✅ Code Interpreter (for generating diagrams)
- ✅ File Search (for searching context documents)
- ✅ Reasoning (if available - enhances pedagogical decisions)

### Step 5: Upload Context Files (Optional but Recommended)
1. Click "Knowledge" or "Files" section
2. Upload:
   - `codexa_market_research.md`
   - `codexa_product_announcement.md`
   - `codexa_brand_strategy_v2.md`
3. Enable "File Search" for these files

### Step 6: Test the Agent
Send test prompt:
```
"Create a course outline for CODEXA focused on Layer 1-2 transition,
priority on video scripts, 20 hours total, flexible timeline"
```

Expected response: Agent asks clarifying questions, then generates module outline

### Step 7: Deploy
- **For API Use**: Note the Agent ID (starts with `asst_...`)
- **For Playground Use**: Save agent and use directly in Playground
- **For Production**: Integrate via OpenAI API in your application

**Deployment Time**: ~5 minutes
**Cost Estimate**: ~$0.02-0.10 per course outline generation (GPT-4o pricing)

---

## 📍 Deployment Path B: Anthropic Console (Advanced)

### Step 1: Create Project
1. Go to: https://console.anthropic.com
2. Create New Project
3. Name: `CODEXA Course Builder`

### Step 2: Add Project Knowledge
1. Click "Knowledge" tab
2. Upload `MASTER_INSTRUCTIONS.md` as project knowledge
3. Upload context files (research, announcement, brand strategy)

### Step 3: Create Agent
```python
# Example API call (Python)
import anthropic

client = anthropic.Anthropic(api_key="your_api_key")

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    temperature=0.7,
    system=open("MASTER_INSTRUCTIONS.md").read(),  # Load instructions
    messages=[
        {
            "role": "user",
            "content": "Create a CODEXA course outline for Layer 1-2..."
        }
    ]
)

print(response.content)
```

### Step 4: Test
Run the script above with a test prompt

### Step 5: Deploy
- **API Integration**: Use the code above in your application
- **Console Use**: Save as template in Anthropic Console
- **Claude Code**: Integrate with local Claude Code CLI

**Deployment Time**: ~10 minutes
**Cost Estimate**: ~$0.01-0.05 per course outline (Claude pricing typically lower)

---

## 📍 Deployment Path C: CODEXA Internal (Native Integration)

### Step 1: Register Agent
Edit `codexa.app/agentes/51_AGENT_REGISTRY.json`:
```json
{
  "agents": [
    {
      "name": "hotmart_course_builder_agent",
      "display_name": "Hotmart Course Builder",
      "specialty": "Educational Content Architecture",
      "status": "production-ready",
      "version": "1.0.0",
      "created": "2025-11-20",
      "layers": [1, 2, 3],
      "dependencies": ["pesquisa_agent", "marca_agent", "anuncio_agent"],
      "artifacts_path": "agents/hotmart_course_builder_agent/artifacts/",
      "instructions_file": "MASTER_INSTRUCTIONS.md",
      "configuration_file": "AGENT_CONFIGURATION.json"
    }
  ]
}
```

### Step 2: Create Slash Command
Create `.claude/commands/build_course.md`:
```markdown
# /build_course - Generate CODEXA Course for Hotmart

Execute: Load hotmart_course_builder_agent and generate comprehensive course content

Ask user for:
- Scope (Layer 1 only, 1-2 transition, 1-2-3 full, or custom)
- Priority output (video scripts, workbooks, exercises, sales page, or all)
- Target duration (10-50 hours)
- Timeline (hard deadline or flexible)

Then orchestrate course generation using hotmart_course_builder_agent.
```

### Step 3: Test Integration
```bash
# In terminal with Claude Code
/build_course
```

### Step 4: Deploy
- Agent is now available system-wide via `/build_course` command
- Can be orchestrated with other CODEXA agents (e.g., `pesquisa_agent` for market research first)

**Deployment Time**: ~15 minutes
**Cost**: Internal CODEXA credits (Anthropic API backend)

---

## 🧪 Testing Checklist

After deployment, verify these scenarios:

### Test 1: Basic Course Outline Generation
```
Prompt: "Create a 3-module course outline for CODEXA Layer 1 basics"

Expected Output:
- Module 1: [Title] - [Learning Objectives] - [Duration]
- Module 2: [Title] - [Learning Objectives] - [Duration]
- Module 3: [Title] - [Learning Objectives] - [Duration]
- Total: ~X hours
```
✅ Pass if: Generates 3 modules with objectives and timing

### Test 2: Video Script Generation
```
Prompt: "Generate video script for Module 1.1 - Introduction to Layers"

Expected Output:
- Hook (00:00-01:30)
- Core Content (01:30-08:00)
- Demonstration (08:00-12:00)
- Exercise Briefing (12:00-14:30)
- Recap (14:30-15:00)
```
✅ Pass if: Script includes all sections with timing marks

### Test 3: [OPEN_VARIABLES] Detection
```
Check generated content for patterns like:
- [SEU_CRM]
- [CATEGORIA_PRODUTO]
- [OPEN_VARIABLE: custom instruction]
```
✅ Pass if: At least 2 [OPEN_VARIABLES] per module

### Test 4: Brand Voice Compliance
```
Check for seed words:
- "Meta-Construção" (capitalized)
- "Destilação de Conhecimento"
- "Cérebro Plugável"
- "Layer 1/2/3" mentions

Avoid hype words:
- "revolucionário", "mágico", "único no mercado"
```
✅ Pass if: Uses seed words frequently, avoids hype

### Test 5: Quality Gate Validation
```
Ask agent: "Run quality validation on the video script you just created"

Expected Output:
- [ ] Hook timing ≤90s?
- [ ] Learning objectives measurable?
- [ ] Demonstration shows real CODEXA?
- [All checklist items from MASTER_INSTRUCTIONS]
```
✅ Pass if: Agent self-validates and reports issues

---

## 🔧 Configuration Tuning

### Adjust for Different Use Cases

#### Use Case 1: Fast Prototyping (Lower Quality, Faster)
```json
{
  "model": "gpt-4o-mini",
  "temperature": 0.9,
  "max_tokens": 8000,
  "instructions": "Prioritize speed over depth. Generate outlines only."
}
```
**When to use**: Brainstorming phase, client proposals, quick demos

#### Use Case 2: Production Quality (Higher Quality, Slower)
```json
{
  "model": "gpt-4o",
  "temperature": 0.7,
  "max_tokens": 16000,
  "instructions": "Prioritize quality and detail. Validate before delivering."
}
```
**When to use**: Final course content for paying students, public launches

#### Use Case 3: Sales-Focused (Marketing-Heavy)
```json
{
  "priority_output": "sales_page",
  "tone_adjustment": "More persuasive, less technical",
  "include_social_proof": true
}
```
**When to use**: Pre-launch campaigns, lead generation, affiliate recruitment

#### Use Case 4: Technical Deep-Dive (Layer 3 Only)
```json
{
  "scope": "Layer 3 only",
  "audience": "developers",
  "include_code_examples": true,
  "diagrams": "architecture_focused"
}
```
**When to use**: Advanced workshops, technical conference talks, enterprise training

---

## 📊 Monitoring & Maintenance

### Key Metrics to Track

#### Agent Performance
- **Latency**: Time to generate 1 module (target: <3min for outline, <10min for full content)
- **Token Usage**: Avg tokens per request (monitor for cost optimization)
- **Error Rate**: % of requests that fail or timeout (target: <2%)

#### Content Quality (Post-Production)
- **Student Completion Rate**: % who finish course (target: >60%)
- **Exercise Completion**: % who do hands-on labs (target: >70%)
- **Refund Rate**: % who request refunds (target: <5%)

#### Business Impact
- **Sales Conversion**: % from sales page to enrollment (target: >5%)
- **Course Revenue**: Monthly recurring revenue if subscription
- **NPS Score**: Net Promoter Score from students (target: >70)

### Monthly Maintenance Tasks

**Week 1**: Review student feedback → Identify weakest modules
**Week 2**: Regenerate weak modules using agent with feedback incorporated
**Week 3**: A/B test old vs new content (50/50 split)
**Week 4**: Deploy winning version, document learnings

---

## 🆘 Troubleshooting

### Issue 1: Agent Not Generating Content
**Symptom**: Agent responds with "I can't do that" or generic refusal

**Diagnosis**:
1. Check if `MASTER_INSTRUCTIONS.md` was loaded correctly
2. Verify model supports long context (16k+ tokens)
3. Check if tools (Code Interpreter, File Search) are enabled

**Solution**:
- Re-paste instructions (might have been truncated)
- Upgrade to GPT-4o or Claude Sonnet 4
- Enable tools in configuration

---

### Issue 2: Content Too Generic (Lacks Specificity)
**Symptom**: Generated content feels like "generic AI course" not "CODEXA course"

**Diagnosis**:
1. Check if context files (research, announcement, brand strategy) were uploaded
2. Verify File Search is enabled
3. Check if agent is actually reading context (ask "What are the 6 CODEXA core agents?")

**Solution**:
- Upload context files to vector store
- Explicitly tell agent: "Use codexa_product_announcement.md as source of truth"
- Add more specific prompts: "Generate Module 1 focusing on anuncio_agent features"

---

### Issue 3: [OPEN_VARIABLES] Missing or Poorly Placed
**Symptom**: Content is too rigid (no customization flexibility)

**Diagnosis**:
1. Check temperature setting (too low = too conservative)
2. Review instruction emphasis on [OPEN_VARIABLES] strategy

**Solution**:
- Increase temperature to 0.7-0.8
- Add explicit prompt: "Include at least 3 [OPEN_VARIABLES] for tech stack and business context"
- Show examples of good [OPEN_VARIABLE] usage

---

### Issue 4: Brand Voice Inconsistency
**Symptom**: Agent uses hype words ("revolucionário") or wrong tone

**Diagnosis**:
1. Check if brand strategy was uploaded
2. Verify agent read the "BRAND VOICE" section of MASTER_INSTRUCTIONS
3. Check if conflicting instructions exist in prompt

**Solution**:
- Re-upload `codexa_brand_strategy_v2.md`
- Add reminder in prompt: "Maintain disruptivo-sofisticado tone, avoid hype"
- Show examples of correct vs incorrect voice

---

### Issue 5: Token Limit Exceeded
**Symptom**: Agent truncates content mid-sentence or refuses to generate long content

**Diagnosis**:
1. Check max_tokens setting (should be 16000 for full modules)
2. Check if context + instructions + prompt exceed model limit
3. Check if model supports long context (GPT-4o: 128k, Claude Sonnet 4: 200k)

**Solution**:
- Increase max_tokens to 16000
- Generate content in smaller chunks (1 section at a time, not full module)
- Use streaming mode to handle long outputs

---

## 📚 Additional Resources

### Documentation
- **CODEXA Agent SDK**: https://docs.codexa.app/agents
- **OpenAI Agent Builder Guide**: https://platform.openai.com/docs/assistants
- **Anthropic Claude API**: https://docs.anthropic.com/claude/reference

### Community
- **CODEXA Architects Forum**: https://community.codexa.app
- **GitHub Issues**: https://github.com/codexa/agents/issues
- **Discord**: https://discord.gg/codexa (for real-time help)

### Training
- **Agent Development Workshop**: Monthly webinar (check CODEXA events)
- **Certification Program**: "Certified CODEXA Architect" (3 levels)

---

## 🎯 Success Criteria

You've successfully deployed when:

✅ Agent generates course outline in <5 minutes
✅ Content includes [OPEN_VARIABLES] for customization
✅ Brand voice matches CODEXA style (disruptivo-sofisticado)
✅ Quality validation passes all checklists
✅ Test prompts produce expected outputs (see Testing Checklist)
✅ First course module is production-ready without major edits

**Ready to launch**: Start generating real course content and iterate based on student feedback!

---

**Deployment Guide Version**: 1.0.0
**Last Updated**: 2025-11-20
**Maintained By**: CODEXA Meta-Construction Team

*Deploy fast, iterate faster.* 🚀
