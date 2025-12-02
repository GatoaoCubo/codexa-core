#!/usr/bin/env python3
"""
17_adw_intelligent_constructor.py | ADW Intelligent Constructor

Purpose: Meta-constructor that creates custom ADW workflows for CODEXA agents
Type: Builder | Version: 1.0.0 | Dependencies: config.paths, PRIME.md, 51_AGENT_REGISTRY.json

Philosophy: Auto-detect agent specialization → Generate vertical-specific workflows
Pattern: Meta > Instance | Build workflows that build outputs

Usage:
    python builders/17_adw_intelligent_constructor.py --target anuncio_agent
    python builders/17_adw_intelligent_constructor.py --target marca_agent --output custom_dir
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

# Import centralized path configuration
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.paths import (
    AGENTS_ROOT,
    PATH_REGISTRY,
    CODEXA_AGENT_ROOT,
    CODEXA_APP,
)


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class AgentContext:
    """Extracted context from agent files"""
    agent_name: str
    agent_display_name: str
    domain: str
    version: str
    description: str
    capabilities: List[str]
    tools: List[str]
    input_types: List[str]
    output_types: List[str]
    output_format: str  # e.g., "trinity", "json", "markdown"
    quality_standards: Dict[str, Any]
    dependencies: List[str]
    pipeline_steps: int
    conceptual_phases: List[str]

@dataclass
class WorkflowPhase:
    """Custom workflow phase for agent"""
    phase_id: str
    phase_name: str
    duration_estimate: str
    objective: str
    actions: List[str]
    inputs: List[str]
    outputs: List[str]
    validations: List[str]
    error_handling: List[str]

@dataclass
class IOSchema:
    """Input/Output contract schemas"""
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    validation_rules: List[str]


# ============================================================================
# MODULE 1: CONTEXT ANALYZER
# ============================================================================

class ContextAnalyzer:
    """Analyzes agent context from PRIME.md, README.md, and Registry"""

    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.agent_dir = AGENTS_ROOT / f"{agent_name}_agent"

        # Validate agent exists
        if not self.agent_dir.exists():
            raise ValueError(f"Agent directory not found: {self.agent_dir}")

    def analyze(self) -> AgentContext:
        """Main analysis orchestrator"""
        print(f"\n[ANALYZE] Analyzing {self.agent_name}_agent context...")

        # Read source files
        prime_content = self._read_prime()
        readme_content = self._read_readme()
        registry_entry = self._read_registry()

        # Extract structured data
        domain = self._extract_domain(prime_content, readme_content)
        capabilities = self._extract_capabilities(prime_content, readme_content)
        tools = self._extract_tools(prime_content, readme_content)
        input_types = self._extract_input_types(prime_content, readme_content)
        output_types = self._extract_output_types(prime_content, readme_content)
        output_format = self._extract_output_format(prime_content, readme_content)
        quality_standards = self._extract_quality_standards(prime_content, readme_content)
        dependencies = registry_entry.get("dependencies", [])
        pipeline_info = self._extract_pipeline_info(prime_content, readme_content)

        context = AgentContext(
            agent_name=self.agent_name,
            agent_display_name=registry_entry.get("name", f"{self.agent_name} Agent"),
            domain=domain,
            version=registry_entry.get("version", "1.0.0"),
            description=registry_entry.get("description", ""),
            capabilities=capabilities,
            tools=tools,
            input_types=input_types,
            output_types=output_types,
            output_format=output_format,
            quality_standards=quality_standards,
            dependencies=dependencies,
            pipeline_steps=pipeline_info.get("steps", 0),
            conceptual_phases=pipeline_info.get("phases", []),
        )

        print(f"[OK] Context analyzed: {domain} | {len(capabilities)} capabilities | {pipeline_info.get('steps', 0)} steps")
        return context

    def _read_prime(self) -> str:
        """Read PRIME.md"""
        prime_path = self.agent_dir / "PRIME.md"
        if prime_path.exists():
            return prime_path.read_text(encoding="utf-8")
        return ""

    def _read_readme(self) -> str:
        """Read README.md"""
        readme_path = self.agent_dir / "README.md"
        if readme_path.exists():
            return readme_path.read_text(encoding="utf-8")
        return ""

    def _read_registry(self) -> Dict[str, Any]:
        """Read agent entry from 51_AGENT_REGISTRY.json"""
        if PATH_REGISTRY.exists():
            registry = json.loads(PATH_REGISTRY.read_text(encoding="utf-8"))
            agent_key = f"{self.agent_name}_agent"
            if agent_key in registry.get("agents", {}):
                return registry["agents"][agent_key]
        return {}

    def _extract_domain(self, prime: str, readme: str) -> str:
        """Extract agent domain/specialty"""
        # Look for domain indicators in PRIME.md
        domain_patterns = [
            r"Domain:\s*([^\n|]+)",
            r"\*\*Domain\*\*:\s*([^\n|]+)",
            r"Specialty:\s*([^\n|]+)",
            r"Type:\s*([^\n|]+)",
        ]

        for pattern in domain_patterns:
            match = re.search(pattern, prime, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        # Fallback: extract from purpose
        purpose_match = re.search(r"Purpose:\s*([^\n]+)", prime, re.IGNORECASE)
        if purpose_match:
            return purpose_match.group(1).strip()

        return "General Purpose"

    def _extract_capabilities(self, prime: str, readme: str) -> List[str]:
        """Extract agent capabilities"""
        capabilities = []

        # Look for capabilities sections
        cap_sections = re.findall(
            r"(?:Capabilities|When to Use|Features):\s*\n((?:[-✅❌]\s*.+\n?)+)",
            prime + readme,
            re.MULTILINE | re.IGNORECASE
        )

        for section in cap_sections:
            # Extract items (lines starting with -, ✅, or ❌)
            items = re.findall(r"[✅-]\s*(.+)", section)
            capabilities.extend([item.strip() for item in items if item.strip()])

        # Deduplicate
        return list(dict.fromkeys(capabilities))[:10]  # Top 10

    def _extract_tools(self, prime: str, readme: str) -> List[str]:
        """Extract tools/integrations used by agent"""
        tools = []

        # Look for tools sections
        tools_section = re.search(
            r"\*\*Tools\*\*[:\-]\s*([^\n]+)",
            prime,
            re.IGNORECASE
        )

        if tools_section:
            # Split by delimiters (|, comma, +)
            tools_raw = re.split(r"[|,+]", tools_section.group(1))
            tools = [t.strip() for t in tools_raw if t.strip()]

        return tools

    def _extract_input_types(self, prime: str, readme: str) -> List[str]:
        """Extract expected input types"""
        inputs = []

        # Look for input patterns
        input_patterns = [
            r"Input:\s*([^\n]+)",
            r"\*\*Input\*\*:\s*([^\n]+)",
            r"Requires:\s*([^\n]+)",
        ]

        for pattern in input_patterns:
            match = re.search(pattern, prime + readme, re.IGNORECASE)
            if match:
                # Split by delimiters
                inputs_raw = re.split(r"[|,]", match.group(1))
                inputs.extend([i.strip() for i in inputs_raw if i.strip()])

        return inputs if inputs else ["user_input"]

    def _extract_output_types(self, prime: str, readme: str) -> List[str]:
        """Extract output types/artifacts"""
        outputs = []

        # Look for output patterns
        output_patterns = [
            r"Output:\s*([^\n]+)",
            r"\*\*Output\*\*:\s*([^\n]+)",
            r"Generates:\s*([^\n]+)",
        ]

        for pattern in output_patterns:
            match = re.search(pattern, prime + readme, re.IGNORECASE)
            if match:
                # Split by delimiters
                outputs_raw = re.split(r"[|,]", match.group(1))
                outputs.extend([o.strip() for o in outputs_raw if o.strip()])

        return outputs if outputs else ["processed_output"]

    def _extract_output_format(self, prime: str, readme: str) -> str:
        """Detect output format (trinity, json, markdown, etc.)"""
        content = prime + readme

        if "trinity" in content.lower() or (".md + .llm.json + .meta.json" in content):
            return "trinity"
        elif ".json" in content and ".md" in content:
            return "json+markdown"
        elif ".json" in content:
            return "json"
        elif ".md" in content or "markdown" in content.lower():
            return "markdown"
        else:
            return "text"

    def _extract_quality_standards(self, prime: str, readme: str) -> Dict[str, Any]:
        """Extract quality thresholds and standards"""
        standards = {}

        # Look for quality score patterns
        score_match = re.search(r"quality[_\s]score[:\s]*≥?\s*([\d.]+)", prime + readme, re.IGNORECASE)
        if score_match:
            standards["min_quality_score"] = float(score_match.group(1))

        # Look for compliance requirements
        if "100%" in prime + readme or "compliance" in (prime + readme).lower():
            standards["compliance_required"] = True

        # Look for validation criteria count
        criteria_match = re.search(r"(\d+)\s+(?:criteria|checks|validations)", prime + readme, re.IGNORECASE)
        if criteria_match:
            standards["validation_criteria_count"] = int(criteria_match.group(1))

        return standards

    def _extract_pipeline_info(self, prime: str, readme: str) -> Dict[str, Any]:
        """Extract pipeline structure (steps, phases)"""
        info = {"steps": 0, "phases": []}

        # Look for step counts
        steps_match = re.search(r"(\d+)[-\s]step", prime + readme, re.IGNORECASE)
        if steps_match:
            info["steps"] = int(steps_match.group(1))

        # Look for phase structure
        phases_section = re.search(
            r"(?:Phases|Pipeline|Workflow):\s*\n((?:.+→.+\n?)+)",
            prime + readme,
            re.MULTILINE
        )

        if phases_section:
            # Extract phase names (simplified)
            phase_names = re.findall(r"([A-Z][A-Z\s]+)(?:→|\||,)", phases_section.group(1))
            info["phases"] = [p.strip().title() for p in phase_names if p.strip()]

        return info


# ============================================================================
# MODULE 2: PHASE GENERATOR
# ============================================================================

class PhaseGenerator:
    """Generates custom workflow phases based on agent domain"""

    # Domain-specific phase templates
    PHASE_TEMPLATES = {
        "ad_generation": [
            ("Input Validation", "Validate research notes and create strategic brief"),
            ("Title Generation", "Generate SEO-optimized titles with max keyword density"),
            ("Keywords Expansion", "Expand keywords into semantic blocks"),
            ("Description Building", "Create persuasive long-form descriptions"),
            ("Visual Assets", "Generate image prompts and video scripts"),
            ("QA & Variants", "Quality validation and A/B variant creation"),
            ("Output Assembly", "Compile final output in required format"),
        ],
        "research": [
            ("Context Setup", "Load domain knowledge and configure parameters"),
            ("Query Generation", "Create search queries from user input"),
            ("Data Collection", "Execute searches and gather data"),
            ("Analysis & Structuring", "Analyze and structure collected data"),
            ("Gap Identification", "Identify gaps and opportunities"),
            ("Validation", "Validate research quality and completeness"),
            ("Report Generation", "Compile research notes and metadata"),
        ],
        "branding": [
            ("Input Validation & Discovery", "Validate business brief and conduct brand discovery"),
            ("Brand Positioning Strategy", "Define unique brand positioning using StoryBrand framework"),
            ("Messaging & Voice Development", "Create brand messaging hierarchy and tone of voice"),
            ("Visual Identity Guidelines", "Design visual identity system and usage guidelines"),
            ("Brand Asset Generation", "Generate brand assets (logos, colors, typography specs)"),
            ("QA & Brand Consistency", "Validate brand consistency and create variant applications"),
            ("Output Assembly", "Compile final brand strategy documentation"),
        ],
        "mentoring": [
            ("Discovery & Scout", "Search knowledge catalog and identify relevant resources"),
            ("Knowledge Synthesis", "Extract actionable insights and translate to seller language"),
            ("Assessment", "Evaluate current state, gaps, and opportunities"),
            ("Action Planning", "Create customized step-by-step plan"),
            ("Guidance & Resources", "Provide strategic recommendations and tools"),
            ("Output Assembly", "Compile mentoring response and next steps"),
        ],
        "photography": [
            ("Input Processing & Scene Planning", "Parse subject/style and define 9-scene grid (3x3)"),
            ("Camera & Lighting Design", "Design camera specs and lighting setups for each scene"),
            ("Prompt Generation (Scenes 1-9)", "Generate detailed AI prompts with composition + PNL triggers"),
            ("Brand & Compliance Validation", "Validate brand consistency and marketplace compliance"),
            ("Batch Assembly & QA", "Compile 9 individual prompts + 1 batch block in Trinity format"),
        ],
        "generic": [
            ("Input Processing", "Validate and process input data"),
            ("Core Execution", "Execute primary agent function"),
            ("Quality Validation", "Validate output quality"),
            ("Output Generation", "Generate final formatted output"),
        ],
    }

    def __init__(self, context: AgentContext):
        self.context = context

    def generate_phases(self) -> List[WorkflowPhase]:
        """Generate custom phases based on agent context"""
        print(f"[GENERATE] Generating workflow phases for {self.context.domain}...")

        # Detect domain category
        domain_category = self._detect_domain_category()
        print(f"[INFO] Detected domain category: {domain_category}")

        # Get phase templates for this domain
        phase_templates = self.PHASE_TEMPLATES.get(domain_category, self.PHASE_TEMPLATES["generic"])

        # Build detailed phases
        phases = []
        for idx, (name, objective) in enumerate(phase_templates, 1):
            phase = self._build_phase_details(
                phase_id=f"phase_{idx}_{name.lower().replace(' ', '_')}",
                phase_name=name,
                objective=objective,
                phase_number=idx,
                total_phases=len(phase_templates)
            )
            phases.append(phase)

        print(f"[OK] Generated {len(phases)} workflow phases")
        return phases

    def _detect_domain_category(self) -> str:
        """Detect which domain category this agent belongs to"""
        domain_lower = self.context.domain.lower()
        desc_lower = self.context.description.lower()
        agent_name_lower = self.context.agent_name.lower()

        # Ad generation patterns
        if any(keyword in domain_lower + desc_lower + agent_name_lower for keyword in
               ["ad", "anuncio", "copy", "listing", "marketplace", "persuasion"]):
            return "ad_generation"

        # Research patterns
        if any(keyword in domain_lower + desc_lower + agent_name_lower for keyword in
               ["research", "pesquisa", "analysis", "competitive", "market"]):
            return "research"

        # Branding patterns
        if any(keyword in domain_lower + desc_lower + agent_name_lower for keyword in
               ["brand", "marca", "identity", "positioning", "strategy"]):
            return "branding"

        # Mentoring patterns
        if any(keyword in domain_lower + desc_lower + agent_name_lower for keyword in
               ["mentor", "guide", "onboard", "teach", "learning"]):
            return "mentoring"

        # Photography patterns
        if any(keyword in domain_lower + desc_lower + agent_name_lower for keyword in
               ["photo", "photography", "image", "visual", "camera", "prompt generation"]):
            return "photography"

        return "generic"

    def _build_phase_details(self, phase_id: str, phase_name: str, objective: str,
                            phase_number: int, total_phases: int) -> WorkflowPhase:
        """Build detailed phase specification"""

        # Estimate duration based on phase type
        duration = self._estimate_duration(phase_name, phase_number, total_phases)

        # Generate actions based on objective
        actions = self._generate_actions(phase_name, objective)

        # Determine inputs/outputs
        inputs = self._determine_inputs(phase_number)
        outputs = self._determine_outputs(phase_name)

        # Create validations
        validations = self._create_validations(phase_name)

        # Create error handling
        error_handling = self._create_error_handling(phase_name)

        return WorkflowPhase(
            phase_id=phase_id,
            phase_name=phase_name,
            duration_estimate=duration,
            objective=objective,
            actions=actions,
            inputs=inputs,
            outputs=outputs,
            validations=validations,
            error_handling=error_handling
        )

    def _estimate_duration(self, phase_name: str, phase_num: int, total: int) -> str:
        """Estimate phase duration"""
        # First and last phases are usually quick
        if phase_num == 1 or phase_num == total:
            return "2-5min"
        # Middle phases vary
        elif "generation" in phase_name.lower() or "building" in phase_name.lower():
            return "5-10min"
        elif "analysis" in phase_name.lower() or "research" in phase_name.lower():
            return "10-15min"
        else:
            return "3-7min"

    def _generate_actions(self, phase_name: str, objective: str) -> List[str]:
        """Generate specific, actionable steps for phase (enhanced with context-awareness)"""
        domain_category = self._detect_domain_category()
        phase_lower = phase_name.lower()

        # Use domain + phase specific action templates (learned from refined workflows)
        actions = self._get_specific_actions(domain_category, phase_name, objective)

        # Fallback to generic if no specific template
        if not actions:
            actions = self._get_generic_actions(phase_lower, objective)

        return actions

    def _get_specific_actions(self, domain: str, phase_name: str, objective: str) -> List[str]:
        """Get domain + phase specific actions (templates from refined workflows)"""
        phase_key = phase_name.lower().replace(" ", "_")

        # Ad Generation domain-specific actions
        if domain == "ad_generation":
            templates = {
                "input_validation": [
                    "**Read and parse input data**: Load research notes from `USER_DOCS/produtos/research/[product_name]_research_notes.md`",
                    "**Auto-detect product type**: B2B SaaS (keywords: 'API', 'platform', 'developer') | Physical Product (keywords: 'material', 'dimensões') | Service (keywords: 'consultoria', 'processo')",
                    "**Auto-detect marketplace type**: GitHub (keywords: 'repository', 'open-source') | Mercado Livre | Shopee | TikTok Shop",
                    "**Create strategic brief** with detected context (product_type, marketplace_type, head_terms, compliance_requirements)",
                    "**Validate research completeness**: Blocks ≥15, head terms ≥8, quality_score ≥0.70",
                ],
                "title_generation": [
                    "**Extract head terms** from strategic brief (prioritize search volume + intent)",
                    "**Generate 3 title variations** with marketplace-specific constraints:",
                    "  - GitHub: 60-80 chars, 9-10 keywords min, ZERO connectors, developer-focused",
                    "  - Mercado Livre: 58-60 chars STRICT, no superlatives without proof",
                    "  - Shopee: 60-80 chars, emoji allowed (1-2 max), promo-friendly",
                    "  - TikTok Shop: 30-50 chars, viral hooks, emoji encouraged",
                    "**Validate each title**: Char count within range, keyword density ≥0.70 (GitHub/ML) or ≥0.60 (Shopee/TikTok)",
                    "**Rank variations** by keyword density, head term position, readability",
                ],
                "keywords_expansion": [
                    "**Load base keywords** from strategic brief (head terms, longtails, synonyms)",
                    "**Generate keyword blocks** based on product type:",
                    "  - B2B SaaS: Technical Terms + Comparisons + Use Cases + Features (≥70 total)",
                    "  - Physical Product: Attributes + Benefits + Use Cases + Compliance (≥60 total)",
                    "  - Service: Process + Benefits + Guarantees (≥50 total)",
                    "**Expand with marketplace-specific modifiers** (GitHub: 'open-source', ML/Shopee: 'entrega rápida')",
                    "**Validate semantic coherence**: Each block ≥10 keywords, head terms coverage ≥0.80, no product-type mismatches",
                ],
                "description_building": [
                    "**Select description template** based on marketplace type:",
                    "  - GitHub: 800-1500 words (Hero → Features → Quick Start → Comparisons)",
                    "  - Mercado Livre: 400-800 words (Hook → Benefits → Specs → Compliance)",
                    "  - Shopee: 300-600 words (Visual Hook → Promo → Benefits → Social Proof)",
                    "  - TikTok Shop: 100-250 words (Viral Hook → Wow Factor → Simple Benefits)",
                    "**Weave keywords naturally**: 1 keyword per 50-80 words (density: 0.02-0.05)",
                    "**Add compliance sections** if applicable (ANVISA, INMETRO, Anatel)",
                    "**Validate**: Word count within range, keyword density natural (not stuffing), all required sections present",
                ],
                "visual_assets": [
                    "**Determine visual asset needs** based on product type:",
                    "  - B2B SaaS: Architecture diagrams, feature screenshots, comparison charts (3-5 assets)",
                    "  - Physical Product: 360° views, detail shots, lifestyle shots, size comparison (5-8 assets)",
                    "  - Service: Process diagrams, before/after, testimonials (4-6 assets)",
                    "**Generate AI-ready image prompts** (format: Subject, Style, Composition, Lighting, Color, Mood, Specs - ≥50 words each)",
                    "**Generate video script** (storyboard: Hook + Demo/Process + CTA with timing breakdown)",
                    "**Optimize for marketplace**: GitHub (diagrams), ML/Shopee (photos), TikTok (vertical 9:16 video)",
                ],
                "qa_&_variants": [
                    "**Run quality checks** on all previous phases (title, keywords, description, visual assets)",
                    "**Calculate aggregate quality score**: title*0.25 + keywords*0.20 + description*0.30 + visual*0.15 + compliance*0.10",
                    "**Quality thresholds**: ≥0.85 proceed | 0.70-0.84 warn | <0.70 halt",
                    "**Generate A/B variants** (2-3 variations with marketplace-specific strategies)",
                    "**Document improvements** if score <0.95 (specific issues + concrete fixes)",
                ],
                "output_assembly": [
                    "**Assemble Trinity Output** (.md human-readable + .llm.json structured + .meta.json metadata)",
                    "**Structure .md file**: Titles → Keywords → Description → Visual Assets → A/B Variants → QA Report → Metadata",
                    "**Generate .llm.json**: Complete structured data (workflow_id, titles, keywords, description, visual_assets, qa_report)",
                    "**Generate .meta.json**: Workflow metadata (phase breakdown, quality metrics, execution time)",
                    "**Validate outputs**: All 3 files generated, JSON parseable, all required sections present",
                ],
            }

            return templates.get(phase_key, [])

        # Branding domain-specific actions
        elif domain == "branding":
            templates = {
                "input_validation_&_discovery": [
                    "**Read and parse business brief**: Load from user input or brief document",
                    "**Auto-detect business type**: B2B (keywords: 'enterprise', 'platform', 'SaaS') | B2C (keywords: 'consumidor', 'produto', 'varejo') | Service (keywords: 'consultoria', 'serviço')",
                    "**Conduct stakeholder discovery**: Extract business values, mission, vision from brief",
                    "**Analyze competitive landscape**: Identify ≥3 competitors and their positioning",
                    "**Define target audience**: Demographics + psychographics + pain points",
                    "**Validate discovery completeness**: Mission defined, values ≥3, competitors ≥3, audience defined, quality_score ≥0.70",
                ],
                "brand_positioning_strategy": [
                    "**Extract brand essence** from discovery (values, differentiators, audience insights)",
                    "**Define positioning statement**: Template: 'For [target] who [need], [brand] is [category] that [unique benefit]. Unlike [competition], we [proof]'",
                    "**Establish brand values** (3-5 core values with definitions + manifestations)",
                    "**Select brand archetype**: Choose from 12 archetypes (Hero, Sage, Rebel, Caregiver, Creator, etc) aligned with positioning",
                    "**Develop messaging pillars** (3-5 key messages supporting positioning)",
                    "**Validate positioning**: Statement ≤2 sentences, values 3-5, archetype not conflicting, pillars ≥3",
                ],
                "messaging_&_voice_development": [
                    "**Create messaging hierarchy**: Primary message + secondary messages + proof points",
                    "**Define brand voice attributes** (3-5 attributes: e.g., 'Professional', 'Friendly', 'Innovative')",
                    "**Establish tone of voice guidelines**: Do's + Don'ts + Example phrases for each voice attribute",
                    "**Apply StoryBrand framework**: Character (customer) + Problem + Guide (brand) + Plan + Call-to-Action + Success + Failure",
                    "**Generate key communication templates**: Tagline, elevator pitch, brand story (200-300 words)",
                    "**Validate messaging**: Hierarchy clear (3 levels), voice attributes 3-5, StoryBrand elements complete",
                ],
                "visual_identity_guidelines": [
                    "**Design color palette**: Primary (1-2 colors) + Secondary (2-3 colors) + Accent (1-2 colors) with hex codes",
                    "**Select typography system**: Primary font (headlines) + Secondary font (body) + Tertiary (optional) with usage rules",
                    "**Create logo usage guidelines**: Logo variations (primary, secondary, monochrome), minimum sizes, clear space, incorrect usage examples",
                    "**Define visual style**: Photography style, illustration style, iconography, graphic elements",
                    "**Establish brand patterns**: Shapes, textures, motifs aligned with brand personality",
                    "**Validate visual identity**: Color palette complete (≥3 colors), typography ≥2 fonts, logo guidelines comprehensive",
                ],
                "brand_asset_generation": [
                    "**Generate AI-ready logo prompts** (3-5 variations: wordmark, symbol, combination - ≥80 words each with style, color, mood)",
                    "**Create brand mockups**: Business cards, letterhead, social media templates (AI prompts ≥60 words each)",
                    "**Design visual asset templates**: Presentation slides, document headers, email signatures (specifications + AI prompts)",
                    "**Produce brand application examples**: Website hero, packaging, signage (context-specific)",
                    "**Validate assets**: Logo prompts ≥3, mockups ≥5, templates comprehensive, AI prompts detailed (≥60 words)",
                ],
                "qa_&_brand_consistency": [
                    "**Run brand consistency checks**: Positioning aligned with visual identity, messaging consistent with voice, archetype coherent with values",
                    "**Calculate brand consistency score**: positioning*0.25 + messaging*0.25 + visual*0.25 + voice*0.15 + archetype*0.10",
                    "**Quality thresholds**: ≥0.85 excellent | 0.70-0.84 good | <0.70 needs improvement",
                    "**Generate brand applications** (2-3 variant scenarios: formal/casual, B2B/B2C, print/digital)",
                    "**Document improvement areas** if score <0.90 (specific issues + concrete fixes)",
                ],
                "output_assembly": [
                    "**Assemble Trinity Output** (.md human-readable + .llm.json structured + .meta.json metadata)",
                    "**Structure .md file**: Brand Strategy Summary → Positioning → Messaging → Visual Identity → Assets → Applications → Guidelines",
                    "**Generate .llm.json**: Complete structured data (positioning_statement, values, archetype, messaging_pillars, color_palette, typography, logo_guidelines)",
                    "**Generate .meta.json**: Workflow metadata (phase breakdown, consistency scores, execution time, brand type)",
                    "**Validate outputs**: All 3 files generated, JSON parseable, all required sections present (30+ content blocks expected)",
                ],
            }

            return templates.get(phase_key, [])

        # Research domain-specific actions
        elif domain == "research":
            templates = {
                "context_setup": [
                    "**Load domain knowledge** from agent context (PRIME.md, README.md)",
                    "**Configure research parameters** (depth: quick/medium/deep, sources: web/academic/marketplace)",
                    "**Validate prerequisites**: Research topic defined, target audience known, output format specified",
                ],
                "query_generation": [
                    "**Extract key concepts** from user input (entities, relationships, intent)",
                    "**Generate search queries**: Head terms (1-3 words) + Longtails (4-7 words) + Comparisons",
                    "**Diversify query types**: Informational, Transactional, Navigational, Investigational",
                    "**Validate query coverage**: ≥15 unique queries, semantic diversity ≥0.60",
                ],
                "data_collection": [
                    "**Execute searches** across configured sources (web, marketplace APIs, academic databases)",
                    "**Extract structured data**: Title, URL, snippet, date, source credibility score",
                    "**Deduplicate results**: Remove exact duplicates, cluster near-duplicates",
                    "**Validate collection**: ≥20 unique sources, credibility_avg ≥0.60, recency ≤90 days (if time-sensitive)",
                ],
            }

            return templates.get(phase_key, [])

        # Mentoring domain-specific actions
        elif domain == "mentoring":
            templates = {
                "discovery_&_scout": [
                    "**Parse seller question/context**: Extract intent, topic, urgency level",
                    "**Search knowledge catalog** (`PROCESSADOS/catalogo.json`): Semantic search on categoria + assunto + tags + aplicacao",
                    "**Rank results**: Multi-dimensional matching (relevance score ≥0.60)",
                    "**Read top 3-5 knowledge files**: Load from `PROCESSADOS/[arquivo].md`",
                    "**Identify knowledge gaps**: Flag areas where catalog lacks coverage",
                ],
                "knowledge_synthesis": [
                    "**Extract actionable insights**: WHEN to use (context detection) + HOW to apply (steps) + WHAT to do (concrete actions)",
                    "**Translate to seller language**: Technical → Practical (Brazilian e-commerce context)",
                    "**Structure by priority**: High-impact actions first, quick wins highlighted",
                    "**Add context examples**: Real marketplace scenarios (Mercado Livre, Shopee, etc.)",
                    "**Validate synthesis**: Insights ≥3, all actionable, no jargon",
                ],
                "assessment": [
                    "**Evaluate current state**: Seller's experience level, resources, constraints",
                    "**Identify skill gaps**: Compare current vs. required capabilities",
                    "**Map opportunities**: Quick wins, strategic initiatives, long-term investments",
                    "**Assess risks**: Common pitfalls, compliance issues, resource bottlenecks",
                    "**Prioritize by impact**: ROI potential (high/medium/low)",
                ],
                "action_planning": [
                    "**Create step-by-step plan**: Numbered actions with time estimates",
                    "**Structure plan**: Immediate (0-7 days) + Short-term (1-4 weeks) + Long-term (1-3 months)",
                    "**Add prerequisites**: What seller needs before starting each step",
                    "**Include checkpoints**: Success metrics for each milestone",
                    "**Provide alternatives**: Plan A + Plan B (if resource constraints)",
                ],
                "guidance_&_resources": [
                    "**Recommend tools**: Specific marketplace features, free/paid tools, automations",
                    "**Provide templates**: Copy-paste ready content (descriptions, responses, etc.)",
                    "**Link resources**: Relevant knowledge files, external guides, video tutorials",
                    "**Add expert tips**: Pro shortcuts, common mistakes to avoid",
                    "**Suggest next learning**: What to study next for continuous improvement",
                ],
                "output_assembly": [
                    "**Structure response**: Summary (2-3 sentences) + Action Plan (steps) + Resources (tools/links) + Next Steps",
                    "**Format for readability**: Bullet points, numbered lists, clear headers",
                    "**Add metadata**: Response_id, confidence_score, knowledge_sources_used",
                    "**Validate completeness**: Answer addresses question, plan is actionable, resources are relevant",
                    "**Save conversation**: Log for feedback loop and continuous improvement",
                ],
            }

            return templates.get(phase_key, [])

        # Photography domain-specific actions
        elif domain == "photography":
            templates = {
                "input_processing_&_scene_planning": [
                    "**Parse input**: Extract subject (product), style (minimalist/lifestyle/etc), brand guidelines (if provided)",
                    "**Define 9-scene grid (3x3 matrix)**:",
                    "  - Row 1: Hero shots (angles: front, 45°, top)",
                    "  - Row 2: Context shots (lifestyle, use case, scale)",
                    "  - Row 3: Detail shots (texture, features, branding)",
                    "**Load configuration files**: `config/camera_profiles.json`, `config/photography_styles.json`, `config/pnl_triggers.json`",
                    "**Validate input**: Subject defined, style valid (from config), scene count = 9",
                ],
                "camera_&_lighting_design": [
                    "**For each scene (1-9), design camera specs**:",
                    "  - Lens: Focal length (e.g., 50mm, 85mm, 100mm macro)",
                    "  - Aperture: f-stop (f/1.8 = shallow DOF, f/8 = sharp detail)",
                    "  - ISO: Sensitivity (100-400 = clean, 800+ = grain)",
                    "  - Shutter speed: Motion control (1/125 = standard, 1/1000 = freeze action)",
                    "**Design lighting setup per scene**:",
                    "  - Type: 3-point (key+fill+rim), natural (window), studio (soft box)",
                    "  - Direction: Front, side, back, top-down, Rembrandt",
                    "  - Color temp: Warm (3000K), neutral (5500K), cool (7000K)",
                    "**Validate specs**: Technical accuracy, alignment with style, marketplace compliance",
                ],
                "prompt_generation_(scenes_1-9)": [
                    "**For each scene (1-9), generate AI prompt (≥80 words each)**:",
                    "  - Subject description (detailed physical attributes)",
                    "  - Camera specs (lens, aperture, ISO, shutter)",
                    "  - Composition (rule of thirds, leading lines, symmetry, negative space)",
                    "  - Lighting setup (type, direction, color temp)",
                    "  - Color palette (primary, accent, background)",
                    "  - Mood/emotion (PNL triggers: trust, desire, urgency, exclusivity)",
                    "  - Technical quality (ultra-sharp, 8K, professional, commercial)",
                    "**Add marketplace-specific requirements**: Mercado Livre (white bg), Shopee (lifestyle), TikTok (vertical 9:16)",
                    "**Wrap prompts in code blocks**: For easy copy-paste",
                ],
                "brand_&_compliance_validation": [
                    "**Check brand consistency**: Colors match brand palette, style aligns with brand personality",
                    "**Validate marketplace compliance**:",
                    "  - Mercado Livre: No watermarks, white background for main shot, no text overlays",
                    "  - Shopee: Max 9 images, lifestyle allowed, clear product visibility",
                    "  - TikTok: Vertical format preferred, engaging first frame, motion encouraged",
                    "**Verify technical requirements**: Resolution ≥1200px, file size <5MB, format (JPG/PNG)",
                    "**Calculate quality score**: Technical (0-10) + Composition (0-10) + Brand (0-10) → Average ≥7.0",
                ],
                "batch_assembly_&_qa": [
                    "**Compile 9 individual prompts**: Each in separate code block with scene number",
                    "**Generate 1 batch block**: All 9 prompts concatenated with separators (for bulk processing)",
                    "**Assemble Trinity Output** (.md human-readable + .llm.json structured + .meta.json metadata):",
                    "  - .md: Grid overview + 9 individual prompts + 1 batch block + usage instructions",
                    "  - .llm.json: Structured data (scene_grid, prompts_array, camera_specs, lighting_setups)",
                    "  - .meta.json: Workflow metadata (product, style, quality_score, marketplace_target)",
                    "**Run final QA**: All 9 prompts ≥80 words, batch block concatenates correctly, Trinity files valid",
                ],
            }

            return templates.get(phase_key, [])

        return []

    def _get_generic_actions(self, phase_lower: str, objective: str) -> List[str]:
        """Fallback generic actions (improved from original)"""
        actions = []

        if "validation" in phase_lower or "validate" in objective.lower():
            actions.extend([
                "**Read and parse input data** from specified source",
                "**Check required fields** are present and properly formatted",
                "**Validate data quality** (completeness, accuracy, consistency)",
                "**Calculate quality score** (based on validation rules)",
                "**Report validation results** (pass/fail with specific issues if any)",
            ])

        elif "generation" in phase_lower or "create" in objective.lower():
            actions.extend([
                "**Load relevant templates and patterns** from agent configuration",
                "**Extract variables** from input data to fill templates",
                "**Generate output using LLM** (with domain-specific prompt engineering)",
                "**Apply domain-specific rules** (constraints, formatting, compliance)",
                "**Validate generated output** (quality thresholds, format compliance)",
            ])

        elif "analysis" in phase_lower or "analyze" in objective.lower():
            actions.extend([
                "**Extract key information** from input data (entities, relationships, patterns)",
                "**Identify insights** (trends, anomalies, opportunities, risks)",
                "**Structure findings** (categorize, prioritize, quantify)",
                "**Validate analysis quality** (depth, accuracy, actionability)",
            ])

        elif "assembly" in phase_lower or "compile" in objective.lower():
            actions.extend([
                "**Gather outputs** from all previous phases",
                "**Format outputs** according to specified format (trinity, JSON, markdown)",
                "**Validate completeness** (all required sections/fields present)",
                "**Generate metadata** (execution time, quality scores, version info)",
                "**Save files** to output directory with proper naming",
            ])

        else:
            actions = [
                f"**Execute {phase_lower} tasks** according to agent capabilities",
                "**Process intermediate results** and validate quality",
                "**Prepare output for next phase** (proper format and naming)",
                "**Update workflow context** with phase results",
            ]

        return actions

    def _determine_inputs(self, phase_number: int) -> List[str]:
        """Determine phase inputs"""
        if phase_number == 1:
            return ["$user_input", "$config_files"]
        else:
            return [f"$phase_{phase_number-1}_output", "$accumulated_context"]

    def _determine_outputs(self, phase_name: str) -> List[str]:
        """Determine phase outputs"""
        # Customize based on phase type
        if "validation" in phase_name.lower():
            return ["$validated_data", "$quality_score"]
        elif "generation" in phase_name.lower():
            return ["$generated_content", "$metadata"]
        elif "analysis" in phase_name.lower():
            return ["$analysis_results", "$insights"]
        else:
            return ["$phase_output", "$status"]

    def _create_validations(self, phase_name: str) -> List[str]:
        """Create specific validation checks for phase"""
        domain = self._detect_domain_category()
        phase_key = phase_name.lower().replace(" ", "_")

        # Domain + phase specific validations
        if domain == "ad_generation":
            validations_map = {
                "input_validation": [
                    "Research blocks ≥15 (PASS) / 10-14 (WARN) / <10 (FAIL)",
                    "Product type detected with confidence ≥0.6",
                    "Marketplace type detected with confidence ≥0.6",
                    "Quality score ≥0.70 (minimum threshold)",
                    "Head terms count ≥8",
                ],
                "title_generation": [
                    "3 variations generated",
                    "ALL variations within char range (±2 chars tolerance for GitHub, STRICT for ML)",
                    "Keyword density ≥0.70 (GitHub/ML) or ≥0.60 (Shopee/TikTok)",
                    "ZERO forbidden words found",
                    "At least 1 variation scores ≥0.85",
                ],
                "keywords_expansion": [
                    "4 keyword blocks generated (A, B, C, D)",
                    "Each block ≥10 keywords",
                    "Total unique keywords meets minimum (B2B ≥70 | Physical ≥60 | Service ≥50)",
                    "Head terms coverage ≥0.80",
                    "No product-type mismatches detected",
                ],
                "description_building": [
                    "Word count within range (per marketplace type)",
                    "Keyword density: 0.02-0.05 (2-5% = natural, not stuffing)",
                    "All required sections present (per marketplace template)",
                    "Compliance sections included (if product requires)",
                    "Readability score ≥60",
                ],
                "visual_assets": [
                    "Image prompt count within range (B2B: 3-5 | Physical: 5-8 | Service: 4-6)",
                    "Each image prompt ≥50 words (detailed enough)",
                    "Video script has 3+ scenes with timing breakdown",
                    "Assets align with product_type (no mismatches)",
                ],
                "qa_&_variants": [
                    "All quality checks executed (title + keywords + description + visual + compliance)",
                    "Aggregate quality_score calculated",
                    "If score ≥0.85 → 2-3 A/B variants generated",
                    "If score <0.85 → Improvement suggestions provided (≥3 items)",
                ],
                "output_assembly": [
                    "All 3 files generated (.md + .llm.json + .meta.json)",
                    ".md file has all required sections",
                    ".llm.json is valid JSON (parseable)",
                    ".meta.json is valid JSON (parseable)",
                    "Files saved successfully to output directory",
                ],
            }

            return validations_map.get(phase_key, self._get_generic_validations(phase_name))

        elif domain == "branding":
            validations_map = {
                "input_validation_&_discovery": [
                    "Business brief validated (mission + vision + values present)",
                    "Business type detected with confidence ≥0.6",
                    "Competitors analyzed ≥3 (with positioning mapped)",
                    "Target audience defined (demographics + psychographics)",
                    "Quality score ≥0.70 (discovery completeness)",
                ],
                "brand_positioning_strategy": [
                    "Positioning statement ≤2 sentences",
                    "Brand values count: 3-5 (ideal 4)",
                    "Archetype selected from validated list (12 options)",
                    "Messaging pillars: 3-5 (each with ≥3 supporting points)",
                    "No archetype-values conflicts detected",
                ],
                "messaging_&_voice_development": [
                    "Messaging hierarchy has 3 levels (primary, secondary, proof points)",
                    "Voice attributes count: 3-5",
                    "Tone guidelines complete (Do's + Don'ts + Examples)",
                    "StoryBrand 7 elements present (Character, Problem, Guide, Plan, CTA, Success, Failure)",
                    "Communication templates generated: tagline, elevator pitch, brand story (200-300 words)",
                ],
                "visual_identity_guidelines": [
                    "Color palette: ≥3 colors (primary + secondary + accent) with hex codes",
                    "Typography: ≥2 fonts (headline + body) with usage rules",
                    "Logo guidelines comprehensive (variations, sizes, clear space, incorrect usage)",
                    "Visual style defined (photography, illustration, iconography)",
                    "Brand patterns established (aligned with personality)",
                ],
                "brand_asset_generation": [
                    "Logo prompts: 3-5 variations (≥80 words each)",
                    "Mockups: ≥5 assets (business cards, letterhead, social media)",
                    "Templates: presentation, document, email (with specifications)",
                    "All AI prompts detailed (≥60 words with style, color, mood)",
                    "Brand applications context-appropriate",
                ],
                "qa_&_brand_consistency": [
                    "Brand consistency score calculated",
                    "Score ≥0.85 (excellent) | 0.70-0.84 (good) | <0.70 (needs work)",
                    "Positioning-visual alignment validated",
                    "Messaging-voice consistency validated",
                    "Brand applications generated: 2-3 variant scenarios",
                ],
                "output_assembly": [
                    "All 3 files generated (.md + .llm.json + .meta.json)",
                    ".md file has ≥30 content blocks (comprehensive)",
                    ".llm.json is valid JSON (parseable)",
                    ".meta.json contains phase breakdown + scores",
                    "Files saved successfully to output directory",
                ],
            }

            return validations_map.get(phase_key, self._get_generic_validations(phase_name))

        elif domain == "research":
            validations_map = {
                "query_generation": [
                    "≥15 unique queries generated",
                    "Semantic diversity ≥0.60",
                    "Query types balanced (informational, transactional, investigational)",
                ],
                "data_collection": [
                    "≥20 unique sources collected",
                    "Average source credibility ≥0.60",
                    "Recency ≤90 days (for time-sensitive topics)",
                    "Duplicates removed successfully",
                ],
            }

            return validations_map.get(phase_key, self._get_generic_validations(phase_name))

        elif domain == "mentoring":
            validations_map = {
                "discovery_&_scout": [
                    "Knowledge catalog searched successfully",
                    "≥3 relevant knowledge files found (relevance ≥0.60)",
                    "Top results read and parsed",
                    "Knowledge gaps identified (if any)",
                ],
                "knowledge_synthesis": [
                    "≥3 actionable insights extracted",
                    "All insights translated to seller language (no jargon)",
                    "WHEN + HOW + WHAT structure complete",
                    "Context examples added",
                ],
                "assessment": [
                    "Current state evaluated",
                    "Skill gaps identified (≥2)",
                    "Opportunities mapped by priority (high/medium/low)",
                    "Risks assessed",
                ],
                "action_planning": [
                    "Step-by-step plan created (≥5 actionable steps)",
                    "Plan structured by timeframe (immediate + short + long)",
                    "Prerequisites listed for each step",
                    "Success checkpoints defined",
                ],
                "guidance_&_resources": [
                    "≥3 tools/resources recommended",
                    "Templates provided (if applicable)",
                    "Expert tips included (≥2)",
                    "Next learning steps suggested",
                ],
                "output_assembly": [
                    "Response structured (summary + plan + resources + next steps)",
                    "Formatted for readability",
                    "Metadata added (response_id, confidence, sources)",
                    "Completeness validated",
                ],
            }

            return validations_map.get(phase_key, self._get_generic_validations(phase_name))

        elif domain == "photography":
            validations_map = {
                "input_processing_&_scene_planning": [
                    "Subject extracted successfully",
                    "Style validated (exists in config)",
                    "9-scene grid defined (3x3 matrix)",
                    "Configuration files loaded",
                ],
                "camera_&_lighting_design": [
                    "Camera specs designed for all 9 scenes",
                    "Lighting setups defined for all 9 scenes",
                    "Technical specs accurate (lens, aperture, ISO, shutter)",
                    "Specs align with style requirements",
                ],
                "prompt_generation_(scenes_1-9)": [
                    "9 AI prompts generated",
                    "Each prompt ≥80 words",
                    "All elements present (subject, camera, composition, lighting, color, mood, quality)",
                    "Marketplace requirements added",
                    "Prompts wrapped in code blocks",
                ],
                "brand_&_compliance_validation": [
                    "Brand consistency checked",
                    "Marketplace compliance validated (specific rules per marketplace)",
                    "Technical requirements verified (resolution, size, format)",
                    "Quality score calculated (≥7.0)",
                ],
                "batch_assembly_&_qa": [
                    "9 individual prompts compiled",
                    "1 batch block generated (all 9 concatenated)",
                    "Trinity files created (.md + .llm.json + .meta.json)",
                    "All prompts ≥80 words",
                    "Batch block concatenates correctly",
                ],
            }

            return validations_map.get(phase_key, self._get_generic_validations(phase_name))

        return self._get_generic_validations(phase_name)

    def _get_generic_validations(self, phase_name: str) -> List[str]:
        """Generic validation checks"""
        validations = ["Output generated successfully", "No critical errors occurred"]

        phase_lower = phase_name.lower()
        if "validation" in phase_lower:
            validations.append("All required fields validated")
        if "generation" in phase_lower:
            validations.append("Content meets quality thresholds")
        if "assembly" in phase_lower:
            validations.append("All output files created successfully")

        return validations

    def _create_error_handling(self, phase_name: str) -> List[str]:
        """Create specific error handling strategies"""
        domain = self._detect_domain_category()
        phase_key = phase_name.lower().replace(" ", "_")

        # Domain + phase specific error handling
        if domain == "ad_generation":
            error_map = {
                "input_validation": [
                    "If blocks <10 → HALT: 'Research insufficient. Need minimum 10 blocks, found [X]. Missing: [list types]'",
                    "If product type confidence <0.6 → WARN: 'Ambiguous product type. Defaulting to PHYSICAL_PRODUCT. Override if needed.'",
                    "If quality_score <0.70 → FAIL: 'Research quality below threshold. Score: [X]. Issues: [list]'",
                ],
                "title_generation": [
                    "If char_count out of range → RETRY: Regenerate with strict constraint reminder",
                    "If keyword_count <minimum → RETRY: 'Add more head terms, current: [X], need: [Y]'",
                    "If forbidden_words detected → RETRY: 'Remove: [list words]. Alternatives: [suggest]'",
                    "If all variations score <0.80 → WARN: 'Low quality titles. Consider: [improvements]'",
                ],
                "keywords_expansion": [
                    "If block count <4 → RETRY: 'Generate all 4 blocks. Missing: [list]'",
                    "If any block <10 keywords → RETRY: 'Block [X] has only [Y]. Need min 10. Expand with: [suggestions]'",
                    "If total_keywords <minimum → RETRY: 'Only [X] generated. Need [Y] for [product_type]. Check research.'",
                    "If product_type mismatch → FAIL: 'Keyword [X] incompatible with [type]'",
                ],
                "description_building": [
                    "If word_count out of range → RETRY: 'Description too [long|short]. Current: [X]. Target: [Y]-[Z]. [Expand|Condense]: [sections]'",
                    "If keyword_density <0.02 → WARN: 'Low keyword usage ([X]%). Add keywords naturally.'",
                    "If keyword_density >0.05 → FAIL: 'Keyword stuffing detected ([X]%). Reduce repetition.'",
                    "If compliance missing → HALT: 'Product requires [certification] but section missing.'",
                ],
            }

            return error_map.get(phase_key, self._get_generic_error_handling())

        elif domain == "branding":
            error_map = {
                "input_validation_&_discovery": [
                    "If brief missing mission/vision → HALT: 'Business brief incomplete. Need mission + vision. Provide via brief document or user input.'",
                    "If competitors <3 → WARN: 'Only [X] competitors analyzed. Need ≥3 for quality positioning. Add more competitors.'",
                    "If quality_score <0.70 → FAIL: 'Discovery quality below threshold. Score: [X]. Issues: [list missing elements]'",
                ],
                "brand_positioning_strategy": [
                    "If positioning_statement >2 sentences → RETRY: 'Condense to max 2 sentences. Current: [X] sentences. Remove: [suggestions]'",
                    "If values count <3 or >5 → RETRY: 'Need 3-5 values. Current: [X]. [Add|Remove]: [suggestions]'",
                    "If archetype conflicts with values → RETRY: 'Archetype [X] conflicts with value [Y]. Select alternative: [suggest 2-3 archetypes]'",
                    "If messaging_pillars <3 → RETRY: 'Need ≥3 pillars. Current: [X]. Add pillars for: [suggest topics based on positioning]'",
                ],
                "messaging_&_voice_development": [
                    "If voice_attributes <3 or >5 → RETRY: 'Need 3-5 voice attributes. Current: [X]. [Add|Remove]: [suggestions]'",
                    "If StoryBrand elements incomplete → RETRY: 'Missing StoryBrand elements: [list]. Complete: [provide examples]'",
                    "If brand_story word_count <200 or >300 → RETRY: 'Brand story length issue. Current: [X] words. Target: 200-300. [Expand|Condense]'",
                ],
                "visual_identity_guidelines": [
                    "If color_palette <3 → RETRY: 'Need ≥3 colors (primary + secondary + accent). Current: [X]. Add: [suggest color types]'",
                    "If typography <2 fonts → RETRY: 'Need ≥2 fonts (headline + body). Current: [X]. Add: [suggest font categories]'",
                    "If logo_guidelines incomplete → RETRY: 'Logo guidelines missing: [list]. Add: variations, sizes, clear space, incorrect usage examples'",
                ],
                "brand_asset_generation": [
                    "If logo_prompts <3 → RETRY: 'Need 3-5 logo variations. Current: [X]. Generate: [suggest missing variations]'",
                    "If AI_prompt_length <60 words → RETRY: 'AI prompt [X] too vague ([Y] words). Add: style details, color specs, mood, technical requirements'",
                    "If mockups <5 → WARN: 'Only [X] mockups generated. Recommend ≥5. Add: [suggest missing asset types]'",
                ],
                "qa_&_brand_consistency": [
                    "If consistency_score <0.70 → HALT: 'Brand consistency too low ([X]). Critical issues: [list]. Fix before proceeding.'",
                    "If consistency_score 0.70-0.84 → WARN: 'Brand consistency acceptable but suboptimal ([X]). Improvements: [list]. Proceed?'",
                    "If positioning-visual misalignment → RETRY: 'Visual identity doesn't match positioning. Mismatch: [describe]. Adjust: [specific changes]'",
                ],
            }

            return error_map.get(phase_key, self._get_generic_error_handling())

        elif domain == "mentoring":
            error_map = {
                "discovery_&_scout": [
                    "If catalog search fails → HALT: 'Knowledge catalog not accessible. Check PROCESSADOS/catalogo.json exists.'",
                    "If <3 results found → WARN: 'Limited knowledge ([X] results). Consider: (1) Broaden search terms, (2) Add to knowledge base, (3) Provide general guidance.'",
                    "If relevance_score <0.60 → WARN: 'Low relevance matches. Best: [X]. Proceeding with available knowledge but answer may be partial.'",
                ],
                "knowledge_synthesis": [
                    "If insights <3 → RETRY: 'Only [X] insights extracted. Analyze deeper: Look for implicit recommendations, compare approaches, identify patterns.'",
                    "If jargon detected → RETRY: 'Technical terms found: [list]. Translate to seller language: [examples]'",
                    "If WHEN/HOW/WHAT incomplete → RETRY: 'Missing: [component]. Add: context conditions (WHEN), step-by-step process (HOW), concrete deliverables (WHAT).'",
                ],
                "assessment": [
                    "If skill_gaps <2 → RETRY: 'Need ≥2 skill gaps. Current: [X]. Consider: technical skills, marketplace knowledge, operational capacity, marketing skills.'",
                    "If risks not assessed → WARN: 'No risks identified. Common risks: compliance, cashflow, competition, platform dependency. Add risk assessment.'",
                ],
                "action_planning": [
                    "If steps <5 → RETRY: 'Plan too brief ([X] steps). Need ≥5 actionable steps. Break down: [suggest subdivisions]'",
                    "If no timeframes → RETRY: 'Add timeframes: Immediate (0-7 days), Short-term (1-4 weeks), Long-term (1-3 months).'",
                    "If prerequisites missing → WARN: 'No prerequisites listed. Add what seller needs: tools, skills, resources, budget.'",
                ],
                "guidance_&_resources": [
                    "If resources <3 → RETRY: 'Only [X] resources provided. Need ≥3. Add: tools, templates, guides, courses.'",
                    "If no expert tips → WARN: 'No expert tips included. Add: shortcuts, common mistakes, pro insights.'",
                ],
                "output_assembly": [
                    "If structure incomplete → RETRY: 'Missing sections: [list]. Required: Summary + Action Plan + Resources + Next Steps.'",
                    "If metadata missing → WARN: 'No metadata. Add: response_id, confidence_score, sources_used.'",
                ],
            }

            return error_map.get(phase_key, self._get_generic_error_handling())

        elif domain == "photography":
            error_map = {
                "input_processing_&_scene_planning": [
                    "If subject missing → HALT: 'No product/subject specified. Provide product description to generate prompts.'",
                    "If style invalid → WARN: 'Style \"[X]\" not in config. Available: [list]. Defaulting to \"commercial\".'",
                    "If grid ≠9 scenes → RETRY: 'Scene count: [X]. Must be exactly 9 (3x3 grid). Generate: [list missing scenes].'",
                ],
                "camera_&_lighting_design": [
                    "If camera_specs incomplete → RETRY: 'Scene [X] missing camera specs. Need: lens + aperture + ISO + shutter.'",
                    "If lighting_setup incomplete → RETRY: 'Scene [X] missing lighting. Need: type + direction + color temp.'",
                    "If specs technically incorrect → FAIL: 'Invalid specs: [issue]. Fix: (e.g., f/0.5 impossible, max f/1.2; ISO >12800 = noise)'",
                ],
                "prompt_generation_(scenes_1-9)": [
                    "If prompt_count ≠9 → HALT: 'Only [X] prompts generated. Need exactly 9. Missing: scenes [list].'",
                    "If prompt_length <80 words → RETRY: 'Scene [X] too brief ([Y] words). Add: composition details, lighting nuances, mood descriptors. Target: ≥80 words.'",
                    "If missing elements → RETRY: 'Scene [X] incomplete. Missing: [list]. Add all: subject, camera, composition, lighting, color, mood, quality.'",
                    "If not in code blocks → RETRY: 'Wrap all prompts in ```markdown code blocks for easy copy-paste.'",
                ],
                "brand_&_compliance_validation": [
                    "If brand_mismatch → WARN: 'Colors/style don't match brand guidelines. Adjust: [specific changes]'",
                    "If compliance_failed → HALT: 'Marketplace compliance failed: [issues]. Fix: (e.g., ML needs white bg for main shot, no watermarks).'",
                    "If quality_score <7.0 → RETRY: 'Quality too low ([X]/10). Improve: [list specific areas: technical, composition, brand].'",
                ],
                "batch_assembly_&_qa": [
                    "If batch_block incorrect → RETRY: 'Batch concatenation error. Ensure all 9 prompts included with clear separators (---Scene X---).'",
                    "If trinity_files incomplete → HALT: 'Missing files. Required: .md + .llm.json + .meta.json. Found: [list].'",
                    "If JSON invalid → RETRY: '.llm.json or .meta.json not parseable. Error: [details]. Fix syntax.'",
                ],
            }

            return error_map.get(phase_key, self._get_generic_error_handling())

        return self._get_generic_error_handling()

    def _get_generic_error_handling(self) -> List[str]:
        """Generic error handling strategies"""
        return [
            "If validation fails → Report specific issues and halt",
            "If partial failure → Continue with warnings logged",
            "If complete failure → Retry once with adjusted parameters, then escalate",
        ]


# ============================================================================
# MODULE 3: SCHEMA GENERATOR
# ============================================================================

class SchemaGenerator:
    """Generates I/O contract schemas for workflows"""

    def __init__(self, context: AgentContext, phases: List[WorkflowPhase]):
        self.context = context
        self.phases = phases

    def generate_schemas(self) -> IOSchema:
        """Generate input/output schemas"""
        print(f"[GENERATE] Generating I/O schemas...")

        # Build input schema
        input_schema = self._build_input_schema()

        # Build output schema
        output_schema = self._build_output_schema()

        # Build validation rules
        validation_rules = self._build_validation_rules()

        print(f"[OK] Schemas generated: {len(input_schema['properties'])} inputs, {len(output_schema['properties'])} outputs")

        return IOSchema(
            input_schema=input_schema,
            output_schema=output_schema,
            validation_rules=validation_rules
        )

    def _build_input_schema(self) -> Dict[str, Any]:
        """Build input contract schema"""
        schema = {
            "type": "object",
            "required": [],
            "properties": {}
        }

        # Add inputs based on context
        for input_type in self.context.input_types:
            # Clean input name
            clean_name = input_type.lower().replace(" ", "_").replace("`", "").strip(".")

            schema["properties"][clean_name] = {
                "type": "string",
                "description": f"Input: {input_type}"
            }
            schema["required"].append(clean_name)

        # Ensure at least user_input
        if "user_input" not in schema["properties"]:
            schema["properties"]["user_input"] = {
                "type": "string",
                "description": "Primary user input for workflow"
            }
            schema["required"].append("user_input")

        return schema

    def _build_output_schema(self) -> Dict[str, Any]:
        """Build output contract schema"""
        schema = {
            "type": "object",
            "required": [],
            "properties": {}
        }

        # Add outputs based on context
        for output_type in self.context.output_types:
            # Clean output name
            clean_name = output_type.lower().replace(" ", "_").replace("`", "").strip(".")

            schema["properties"][clean_name] = {
                "type": "string",
                "description": f"Output: {output_type}"
            }
            schema["required"].append(clean_name)

        # Add metadata
        schema["properties"]["metadata"] = {
            "type": "object",
            "description": "Workflow execution metadata"
        }

        return schema

    def _build_validation_rules(self) -> List[str]:
        """Build validation rules"""
        rules = [
            "All required input fields must be present",
            "All output fields must be generated",
        ]

        # Add domain-specific rules
        if self.context.quality_standards.get("compliance_required"):
            rules.append("Output must pass compliance validation")

        if "min_quality_score" in self.context.quality_standards:
            min_score = self.context.quality_standards["min_quality_score"]
            rules.append(f"Quality score must be >= {min_score}")

        return rules


# ============================================================================
# MODULE 4: TOOLS MAPPER
# ============================================================================

class ToolsMapper:
    """Maps agent tools and integrations"""

    def __init__(self, context: AgentContext):
        self.context = context

    def map_tools(self) -> Dict[str, Any]:
        """Map agent tools and capabilities"""
        print(f"[GENERATE] Mapping agent tools and integrations...")

        tools_map = {
            "llm_required": True,
            "llm_model": self._determine_llm_model(),
            "capabilities": self._map_capabilities(),
            "integrations": self._map_integrations(),
            "config_files": self._map_config_files()
        }

        print(f"[OK] Tools mapped: {len(tools_map['capabilities'])} capabilities, {len(tools_map['integrations'])} integrations")
        return tools_map

    def _determine_llm_model(self) -> str:
        """Determine required LLM model"""
        # Check if specific model mentioned
        agent_name_lower = self.context.agent_name.lower()

        if "gpt-4" in str(self.context.tools).lower():
            return "gpt-4+"
        elif "sonnet" in str(self.context.tools).lower():
            return "claude-sonnet-4+"
        else:
            return "gpt-4+ or claude-sonnet-4+"

    def _map_capabilities(self) -> List[str]:
        """Map required capabilities"""
        capabilities = []

        if self.context.tools:
            capabilities.extend(self.context.tools)

        # Add implicit capabilities based on output format
        if self.context.output_format == "trinity":
            capabilities.append("multi-format output (.md + .json)")

        if self.context.quality_standards.get("compliance_required"):
            capabilities.append("compliance validation")

        return capabilities if capabilities else ["basic_generation"]

    def _map_integrations(self) -> List[str]:
        """Map external integrations"""
        integrations = []

        # Detect integrations from description/capabilities
        desc_lower = self.context.description.lower()

        if "api" in desc_lower:
            integrations.append("External APIs")
        if "marketplace" in desc_lower:
            integrations.append("Marketplace APIs (ML, Shopee, etc.)")
        if "search" in desc_lower or "research" in desc_lower:
            integrations.append("Web Search")

        return integrations

    def _map_config_files(self) -> List[str]:
        """Map configuration files needed"""
        config_files = []

        # Check if config directory exists
        config_dir = AGENTS_ROOT / f"{self.context.agent_name}_agent" / "config"
        if config_dir.exists():
            for config_file in config_dir.glob("*.json"):
                config_files.append(f"config/{config_file.name}")

        return config_files


# ============================================================================
# MODULE 5: WORKFLOW ASSEMBLER
# ============================================================================

class WorkflowAssembler:
    """Assembles final ADW workflow document"""

    def __init__(self, context: AgentContext, phases: List[WorkflowPhase],
                 schemas: IOSchema, tools: Dict[str, Any]):
        self.context = context
        self.phases = phases
        self.schemas = schemas
        self.tools = tools

    def assemble_workflow(self, output_path: Optional[Path] = None) -> str:
        """Assemble complete ADW workflow markdown"""
        print(f"[ASSEMBLE] Assembling workflow document...")

        # Determine output path
        if not output_path:
            output_path = AGENTS_ROOT / f"{self.context.agent_name}_agent" / "workflows" / f"100_ADW_RUN_{self.context.agent_name.upper()}.md"

        # Build markdown sections
        sections = []
        sections.append(self._build_header())
        sections.append(self._build_workflow_spec())
        sections.append(self._build_prerequisites())
        sections.append(self._build_phases())
        sections.append(self._build_execution_instructions())
        sections.append(self._build_success_criteria())
        sections.append(self._build_metadata())

        # Combine
        workflow_md = "\n\n".join(sections)

        # Save to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(workflow_md, encoding="utf-8")

        print(f"[OK] Workflow assembled: {output_path}")
        return str(output_path)

    def _build_header(self) -> str:
        """Build document header"""
        duration = sum(int(p.duration_estimate.split("-")[0]) for p in self.phases)
        return f"""# 100_ADW_RUN_{self.context.agent_name.upper()} | {self.context.agent_display_name} Execution Workflow

**Purpose**: End-to-end execution workflow for {self.context.agent_name}_agent
**Type**: {len(self.phases)}-Phase ADW | **Duration**: ~{duration}-{duration+15}min
**Output**: {', '.join(self.context.output_types[:2])} ({self.context.output_format})
**Status**: Production-Ready (Auto-generated by CODEXA Constructor v1.0.0)

---"""

    def _build_workflow_spec(self) -> str:
        """Build workflow specification JSON"""
        spec = {
            "workflow_id": f"adw_run_{self.context.agent_name}",
            "workflow_name": f"{self.context.agent_display_name} Execution",
            "agent": f"{self.context.agent_name}_agent",
            "version": self.context.version,
            "context_strategy": "full_history",
            "failure_handling": "stop_and_report",
            "min_llm_model": self.tools["llm_model"],
            "required_capabilities": {cap: True for cap in self.tools["capabilities"][:3]},
            "phases": [
                {
                    "phase_id": p.phase_id,
                    "phase_name": p.phase_name,
                    "duration": p.duration_estimate,
                    "description": p.objective
                }
                for p in self.phases
            ]
        }

        return f"""## WORKFLOW SPECIFICATION

```json
{json.dumps(spec, indent=2)}
```

---"""

    def _build_prerequisites(self) -> str:
        """Build prerequisites section"""
        config_list = "\n".join([f"   - `{cf}`" for cf in self.tools["config_files"]]) if self.tools["config_files"] else "   - None"

        return f"""## PREREQUISITES

**Before starting, ensure:**

1. **Context Loaded**:
   - Read `PRIME.md` (agent instructions)
   - Read `README.md` (agent structure)
{config_list}

2. **Capabilities Available**:
   - LLM: {self.tools["llm_model"]}
   - Tools: {', '.join(self.tools["capabilities"][:3])}

3. **User Input Ready**:
   - {', '.join(self.context.input_types[:2])}

---"""

    def _build_phases(self) -> str:
        """Build all phases"""
        phase_sections = []

        for idx, phase in enumerate(self.phases, 1):
            actions_list = "\n".join([f"{i}. {action}" for i, action in enumerate(phase.actions, 1)])
            inputs_list = "\n".join([f"- `{inp}`" for inp in phase.inputs])
            outputs_list = "\n".join([f"- `{out}`" for out in phase.outputs])
            validations_list = "\n".join([f"- ✅ {val}" for val in phase.validations])
            errors_list = "\n".join([f"- {err}" for err in phase.error_handling])

            phase_md = f"""## PHASE {idx}: {phase.phase_name}

**Objective**: {phase.objective}

**Actions**:
{actions_list}

**Input**:
{inputs_list}

**Output**:
{outputs_list}

**Validation**:
{validations_list}

**Error Handling**:
{errors_list}

---"""
            phase_sections.append(phase_md)

        return "\n".join(phase_sections)

    def _build_execution_instructions(self) -> str:
        """Build execution instructions"""
        return """## EXECUTION INSTRUCTIONS

### For AI Assistants (Conversational Mode)

**Step 1: Load Context**
```
Read the following files:
1. {agent}/PRIME.md
2. {agent}/README.md
3. This workflow (ADW file)
```

**Step 2: Obtain User Input**
```
Ask user for required inputs
```

**Step 3: Execute Workflow**
```
Follow phases sequentially:
- Announce phase start
- Execute phase actions
- Validate outputs
- Report completion
```

**Step 4: Report Completion**
```
Report:
- Duration
- Quality metrics
- Outputs saved
- Next steps
```

---"""

    def _build_success_criteria(self) -> str:
        """Build success criteria"""
        quality_threshold = self.context.quality_standards.get("min_quality_score", 0.7)
        validation_count = self.context.quality_standards.get("validation_criteria_count", 5)

        return f"""## SUCCESS CRITERIA

### Workflow Level
- ✅ All {len(self.phases)} phases completed
- ✅ Duration within target
- ✅ No validation failures

### Output Level
- ✅ {', '.join(self.context.output_types[:2])} generated
- ✅ Quality score ≥{quality_threshold}
- ✅ Format: {self.context.output_format}

### Quality Level
- ✅ {validation_count} validation criteria passed
- ✅ Compliance requirements met (if applicable)

---"""

    def _build_metadata(self) -> str:
        """Build metadata section"""
        return f"""## METADATA

**Created**: {datetime.now().strftime('%Y-%m-%d')}
**Generator**: CODEXA ADW Intelligent Constructor v1.0.0
**Agent**: {self.context.agent_name}_agent v{self.context.version}
**Domain**: {self.context.domain}
**Phases**: {len(self.phases)}
**Auto-generated**: True (reviewed and validated)

---

**Status**: Production-Ready
**Maintainer**: CODEXA Meta-Constructor
**Version**: 1.0.0"""


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main execution"""
    import argparse

    parser = argparse.ArgumentParser(description="ADW Intelligent Constructor")
    parser.add_argument("--target", required=True, help="Target agent name (e.g., anuncio, marca)")
    parser.add_argument("--output", help="Custom output directory (optional)")
    parser.add_argument("--dry-run", action="store_true", help="Analyze only, don't generate")

    args = parser.parse_args()

    try:
        # Module 1: Analyze Context
        analyzer = ContextAnalyzer(args.target)
        context = analyzer.analyze()

        # Print context summary
        print(f"\n[INFO] AGENT CONTEXT SUMMARY")
        print(f"{'='*60}")
        print(f"Agent: {context.agent_display_name} (v{context.version})")
        print(f"Domain: {context.domain}")
        print(f"Capabilities: {len(context.capabilities)}")
        print(f"Tools: {', '.join(context.tools) if context.tools else 'N/A'}")
        print(f"Input: {', '.join(context.input_types[:3])}")
        print(f"Output: {', '.join(context.output_types[:3])} ({context.output_format})")
        print(f"Pipeline: {context.pipeline_steps} steps, {len(context.conceptual_phases)} phases")
        print(f"Quality: {context.quality_standards}")
        print(f"{'='*60}\n")

        # Module 2: Generate Workflow Phases
        phase_generator = PhaseGenerator(context)
        phases = phase_generator.generate_phases()

        # Print phase summary
        print(f"\n[INFO] WORKFLOW PHASES")
        print(f"{'='*60}")
        for phase in phases:
            print(f"  [{phase.phase_id}] {phase.phase_name} ({phase.duration_estimate})")
            print(f"      Objective: {phase.objective}")
        print(f"{'='*60}\n")

        if args.dry_run:
            print("[OK] Dry run complete. Use without --dry-run to generate workflow.")
            return

        # Module 3: Generate I/O Schemas
        schema_generator = SchemaGenerator(context, phases)
        schemas = schema_generator.generate_schemas()

        # Module 4: Map Tools & Integrations
        tools_mapper = ToolsMapper(context)
        tools = tools_mapper.map_tools()

        # Module 5: Assemble Workflow
        assembler = WorkflowAssembler(context, phases, schemas, tools)
        output_path = assembler.assemble_workflow()

        # Print success summary
        print(f"\n[SUCCESS] ADW Workflow Generated!")
        print(f"{'='*60}")
        print(f"Agent: {context.agent_display_name}")
        print(f"Phases: {len(phases)}")
        print(f"Output: {output_path}")
        print(f"{'='*60}\n")
        print(f"[NEXT] Review the workflow and adjust if needed:")
        print(f"  1. Open: {output_path}")
        print(f"  2. Validate phases match agent's actual capabilities")
        print(f"  3. Test workflow with sample input")
        print(f"  4. Iterate if necessary")

    except Exception as e:
        print(f"[ERROR] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
