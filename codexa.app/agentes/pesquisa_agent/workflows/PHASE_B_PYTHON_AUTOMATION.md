# PHASE B: PYTHON AUTOMATION PATTERN | pesquisa_agent

**Purpose**: Guide for implementing Python automation script for pesquisa_agent workflow
**Phase**: B (after Phase A conversational ADW validated)
**Status**: ⏳ Planned - Ready for implementation
**Version**: 1.0.0 | **Date**: 2025-11-17

---

## OVERVIEW

**Phase A** (COMPLETE ✅):
- Conversational ADW (100_ADW_RUN_PESQUISA.md)
- LLM reads workflow and executes manually
- User interacts conversationally
- Duration: 20-30 minutes with human guidance

**Phase B** (THIS DOCUMENT):
- Python automation script (`run_pesquisa_agent.py`)
- Script invokes LLM API to execute workflow automatically
- Minimal/no human interaction
- Duration: 20-30 minutes fully automated
- Batch processing support
- CI/CD integration ready

---

## ARCHITECTURE

### Script Structure

```
pesquisa_agent/workflows/
├── 100_ADW_RUN_PESQUISA.md           # Phase A (conversational)
├── run_pesquisa_agent.py              # Phase B (automated) ⭐ TO CREATE
├── requirements.txt                    # Python dependencies
├── .env.example                        # API keys template
└── automation/                         # Automation modules
    ├── __init__.py
    ├── llm_client.py                   # LLM API wrapper (Anthropic/OpenAI)
    ├── workflow_executor.py            # Workflow orchestration
    ├── phase_handlers.py               # Phase 1-9 implementations
    ├── validators.py                   # Quality gates
    └── output_generator.py             # Trinity output generation
```

### Dependencies

**Core**:
- `anthropic` (Claude API) OR `openai` (OpenAI API)
- `python-dotenv` (environment variables)
- `pydantic` (data validation)
- `requests` (web search if using custom tools)

**Optional**:
- `pillow` (image analysis if vision enabled)
- `pandas` (data processing for benchmark tables)
- `jinja2` (template rendering for research_notes.md)
- `pytest` (testing)

---

## IMPLEMENTATION GUIDE

### Step 1: Create requirements.txt

```txt
# LLM APIs
anthropic>=0.20.0  # Claude API
openai>=1.10.0     # OpenAI API (alternative)

# Core utilities
python-dotenv>=1.0.0  # Environment variables
pydantic>=2.5.0       # Data validation
requests>=2.31.0      # HTTP requests
jinja2>=3.1.2         # Template rendering

# Data processing
pandas>=2.1.0         # Benchmark tables
pillow>=10.1.0        # Image analysis (optional)

# Testing
pytest>=7.4.0         # Unit tests
pytest-asyncio>=0.21.0  # Async tests
```

### Step 2: Create .env.example

```bash
# LLM API Configuration
LLM_PROVIDER=anthropic  # or "openai"
ANTHROPIC_API_KEY=your_api_key_here
OPENAI_API_KEY=your_api_key_here

# Model Configuration
MODEL_NAME=claude-sonnet-3.5-20241022  # or gpt-4o
MAX_TOKENS=8000
TEMPERATURE=0.7

# Workflow Configuration
MIN_QUALITY_SCORE=0.75
MAX_DURATION_MINUTES=35
ENABLE_CACHING=true

# Output Configuration
OUTPUT_DIR=../user_research
SAVE_INTERMEDIATE=false  # Save phase outputs
REPORT_FORMAT=json  # json, markdown, pdf

# Logging
LOG_LEVEL=INFO
LOG_FILE=workflow_execution.log
```

### Step 3: Create llm_client.py

```python
"""
LLM API Client Wrapper
Supports: Anthropic Claude, OpenAI GPT
"""

import os
from typing import Dict, List, Optional
from anthropic import Anthropic
from openai import OpenAI
import anthropic
import openai


class LLMClient:
    """Unified LLM client supporting multiple providers"""

    def __init__(self, provider: str = "anthropic", model: str = None):
        self.provider = provider.lower()
        self.model = model or self._get_default_model()
        self.client = self._initialize_client()

    def _get_default_model(self) -> str:
        """Get default model for provider"""
        defaults = {
            "anthropic": "claude-sonnet-3.5-20241022",
            "openai": "gpt-4o"
        }
        return defaults.get(self.provider, "claude-sonnet-3.5-20241022")

    def _initialize_client(self):
        """Initialize API client"""
        if self.provider == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in environment")
            return Anthropic(api_key=api_key)

        elif self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment")
            return OpenAI(api_key=api_key)

        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def execute_prompt(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 8000,
        temperature: float = 0.7,
        tools: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Execute prompt and return response

        Returns:
            {
                "content": str,
                "tool_calls": List[Dict] (if tools used),
                "usage": Dict (token counts)
            }
        """

        if self.provider == "anthropic":
            return self._execute_anthropic(
                system_prompt, user_prompt, max_tokens, temperature, tools
            )
        elif self.provider == "openai":
            return self._execute_openai(
                system_prompt, user_prompt, max_tokens, temperature, tools
            )

    def _execute_anthropic(
        self, system, user, max_tokens, temperature, tools
    ) -> Dict:
        """Execute Claude API call"""

        messages = [{"role": "user", "content": user}]

        kwargs = {
            "model": self.model,
            "system": system,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        if tools:
            kwargs["tools"] = tools

        response = self.client.messages.create(**kwargs)

        # Parse response
        content = ""
        tool_calls = []

        for block in response.content:
            if block.type == "text":
                content += block.text
            elif block.type == "tool_use":
                tool_calls.append({
                    "id": block.id,
                    "name": block.name,
                    "input": block.input
                })

        return {
            "content": content,
            "tool_calls": tool_calls,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            }
        }

    def _execute_openai(
        self, system, user, max_tokens, temperature, tools
    ) -> Dict:
        """Execute OpenAI API call"""

        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]

        kwargs = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature
        }

        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"

        response = self.client.chat.completions.create(**kwargs)

        # Parse response
        message = response.choices[0].message
        content = message.content or ""
        tool_calls = []

        if message.tool_calls:
            for tc in message.tool_calls:
                tool_calls.append({
                    "id": tc.id,
                    "name": tc.function.name,
                    "input": eval(tc.function.arguments)  # Parse JSON string
                })

        return {
            "content": content,
            "tool_calls": tool_calls,
            "usage": {
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens
            }
        }
```

### Step 4: Create workflow_executor.py

```python
"""
Workflow Executor
Orchestrates 9-phase pesquisa_agent workflow
"""

import json
import time
from pathlib import Path
from typing import Dict, List
from .llm_client import LLMClient
from .phase_handlers import PhaseHandlers
from .validators import WorkflowValidator
from .output_generator import OutputGenerator


class WorkflowExecutor:
    """Executes complete pesquisa_agent workflow"""

    def __init__(
        self,
        llm_client: LLMClient,
        prime_path: Path,
        template_path: Path,
        output_dir: Path
    ):
        self.llm = llm_client
        self.prime_context = prime_path.read_text(encoding="utf-8")
        self.template = template_path.read_text(encoding="utf-8")
        self.output_dir = output_dir

        self.handlers = PhaseHandlers(llm_client, self.prime_context)
        self.validator = WorkflowValidator()
        self.output_gen = OutputGenerator(template_path)

        self.context = {}  # Shared context across phases
        self.execution_log = []

    def execute(self, brief: Dict) -> Dict:
        """
        Execute complete 9-phase workflow

        Args:
            brief: Research brief dict with keys:
                - product: str
                - category: str
                - target_audience: str
                - price_range: str
                - marketplace_target: Optional[List[str]]
                - competitors: Optional[List[str]]

        Returns:
            {
                "success": bool,
                "duration_minutes": float,
                "quality_score": float,
                "outputs": {
                    "research_notes_md": Path,
                    "metadata_json": Path,
                    "queries_json": Path
                },
                "execution_log": List[Dict]
            }
        """

        start_time = time.time()

        try:
            # Phase 1: Discovery
            print("[Phase 1/9] Capability Discovery & Brief Validation...")
            p1_result = self.handlers.phase_1_discovery(brief)
            self.context.update(p1_result)
            self._log_phase(1, "discovery", p1_result, success=True)

            # Phase 2: Query Bank
            print("[Phase 2/9] Query Bank Generation...")
            p2_result = self.handlers.phase_2_query_bank(self.context)
            self.context.update(p2_result)
            self._log_phase(2, "query_bank", p2_result, success=True)

            # Phase 3: Inbound Search
            print("[Phase 3/9] Web Search INBOUND (Marketplaces)...")
            p3_result = self.handlers.phase_3_inbound_search(self.context)
            self.context.update(p3_result)
            self._log_phase(3, "inbound_search", p3_result, success=True)

            # Phase 4: Outbound Search
            print("[Phase 4/9] Web Search OUTBOUND (SERP & Social)...")
            p4_result = self.handlers.phase_4_outbound_search(self.context)
            self.context.update(p4_result)
            self._log_phase(4, "outbound_search", p4_result, success=True)

            # Phase 5: Competitor Analysis
            print("[Phase 5/9] Competitor Analysis & Benchmark...")
            p5_result = self.handlers.phase_5_competitor_analysis(self.context)
            self.context.update(p5_result)
            self._log_phase(5, "competitor_analysis", p5_result, success=True)

            # Phase 6: SEO Taxonomy
            print("[Phase 6/9] SEO Taxonomy & Strategy...")
            p6_result = self.handlers.phase_6_seo_taxonomy(self.context)
            self.context.update(p6_result)
            self._log_phase(6, "seo_taxonomy", p6_result, success=True)

            # Phase 7: Compliance
            print("[Phase 7/9] Compliance & Risk Analysis...")
            p7_result = self.handlers.phase_7_compliance(self.context)
            self.context.update(p7_result)
            self._log_phase(7, "compliance", p7_result, success=True)

            # Phase 8: Synthesis
            print("[Phase 8/9] Synthesis & Insights...")
            p8_result = self.handlers.phase_8_synthesis(self.context)
            self.context.update(p8_result)
            self._log_phase(8, "synthesis", p8_result, success=True)

            # Phase 9: Output Assembly
            print("[Phase 9/9] Output Assembly & Validation...")
            p9_result = self.handlers.phase_9_output_assembly(
                self.context, self.output_dir, self.output_gen
            )
            self.context.update(p9_result)
            self._log_phase(9, "output_assembly", p9_result, success=True)

            # Calculate metrics
            duration = (time.time() - start_time) / 60  # minutes
            quality_score = self.context.get("quality_score", 0.0)

            print(f"\n✅ Workflow completed successfully!")
            print(f"Duration: {duration:.1f} minutes")
            print(f"Quality Score: {quality_score:.2f}")

            return {
                "success": True,
                "duration_minutes": duration,
                "quality_score": quality_score,
                "outputs": p9_result["outputs"],
                "execution_log": self.execution_log
            }

        except Exception as e:
            duration = (time.time() - start_time) / 60
            print(f"\n❌ Workflow failed after {duration:.1f} minutes")
            print(f"Error: {str(e)}")

            return {
                "success": False,
                "duration_minutes": duration,
                "error": str(e),
                "execution_log": self.execution_log
            }

    def _log_phase(
        self, phase_num: int, phase_name: str, result: Dict, success: bool
    ):
        """Log phase execution"""
        self.execution_log.append({
            "phase": phase_num,
            "name": phase_name,
            "success": success,
            "timestamp": time.time(),
            "keys_added": list(result.keys()) if success else [],
            "error": result.get("error") if not success else None
        })
```

### Step 5: Create run_pesquisa_agent.py (Main Script)

```python
#!/usr/bin/env python3
"""
Pesquisa Agent - Automated Research Workflow Runner
Phase B: Python Automation

Usage:
    python run_pesquisa_agent.py \\
        --brief "Product: X, Category: Y, Audience: Z, Price: R$ A-B" \\
        --output user_research/

    python run_pesquisa_agent.py \\
        --brief-file brief.json \\
        --output user_research/ \\
        --model claude-sonnet-3.5

Version: 1.0.0 (Phase B)
"""

import argparse
import json
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from workflows.automation.llm_client import LLMClient
from workflows.automation.workflow_executor import WorkflowExecutor


def parse_brief_string(brief_str: str) -> dict:
    """Parse brief from command line string"""
    brief = {}

    # Split by comma
    parts = [p.strip() for p in brief_str.split(",")]

    for part in parts:
        if ":" in part:
            key, value = part.split(":", 1)
            key = key.strip().lower().replace(" ", "_")
            value = value.strip()
            brief[key] = value

    # Map to expected keys
    expected_keys = {
        "product": ["product", "produto"],
        "category": ["category", "categoria"],
        "target_audience": ["audience", "target_audience", "publico"],
        "price_range": ["price", "price_range", "preco", "faixa_preco"]
    }

    normalized = {}
    for expected_key, aliases in expected_keys.items():
        for alias in aliases:
            if alias in brief:
                normalized[expected_key] = brief[alias]
                break

    return normalized


def main():
    parser = argparse.ArgumentParser(
        description="Pesquisa Agent - Automated Market Research",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Brief from command line
  python run_pesquisa_agent.py \\
    --brief "Product: Garrafa térmica, Category: Casa, Audience: Atletas, Price: R$ 80-150"

  # Brief from JSON file
  python run_pesquisa_agent.py --brief-file brief.json

  # Custom model and output directory
  python run_pesquisa_agent.py \\
    --brief-file brief.json \\
    --output /path/to/output \\
    --model gpt-4o
        """
    )

    parser.add_argument(
        "--brief",
        type=str,
        help="Research brief as string (comma-separated fields)"
    )
    parser.add_argument(
        "--brief-file",
        type=Path,
        help="Research brief as JSON file"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("../user_research"),
        help="Output directory (default: ../user_research)"
    )
    parser.add_argument(
        "--model",
        type=str,
        help="LLM model name (default: from .env)"
    )
    parser.add_argument(
        "--provider",
        type=str,
        choices=["anthropic", "openai"],
        help="LLM provider (default: from .env)"
    )
    parser.add_argument(
        "--min-quality",
        type=float,
        default=0.75,
        help="Minimum quality score (default: 0.75)"
    )

    args = parser.parse_args()

    # Load environment variables
    load_dotenv()

    # Parse brief
    if args.brief:
        brief = parse_brief_string(args.brief)
    elif args.brief_file:
        with open(args.brief_file, 'r', encoding='utf-8') as f:
            brief = json.load(f)
    else:
        parser.print_help()
        print("\nError: Either --brief or --brief-file required")
        sys.exit(1)

    # Validate brief
    required = ["product", "category", "target_audience", "price_range"]
    missing = [k for k in required if k not in brief]
    if missing:
        print(f"Error: Missing required brief fields: {missing}")
        sys.exit(1)

    # Initialize LLM client
    provider = args.provider or "anthropic"
    llm = LLMClient(provider=provider, model=args.model)

    # Initialize workflow executor
    agent_dir = Path(__file__).parent.parent
    executor = WorkflowExecutor(
        llm_client=llm,
        prime_path=agent_dir / "PRIME.md",
        template_path=agent_dir / "templates" / "research_notes.md",
        output_dir=args.output
    )

    # Execute workflow
    print("="*70)
    print("PESQUISA AGENT - Automated Research Workflow")
    print("="*70)
    print(f"Product: {brief['product']}")
    print(f"Category: {brief['category']}")
    print(f"Provider: {provider} ({llm.model})")
    print(f"Output: {args.output}")
    print("="*70)
    print()

    result = executor.execute(brief)

    # Report results
    print("\n" + "="*70)
    print("EXECUTION SUMMARY")
    print("="*70)

    if result["success"]:
        print(f"✅ Status: SUCCESS")
        print(f"Duration: {result['duration_minutes']:.1f} minutes")
        print(f"Quality Score: {result['quality_score']:.2f}")
        print(f"\nOutputs:")
        for name, path in result["outputs"].items():
            print(f"  - {name}: {path}")

        if result["quality_score"] < args.min_quality:
            print(f"\n⚠️  WARNING: Quality score below minimum ({args.min_quality})")
            sys.exit(2)

        sys.exit(0)

    else:
        print(f"❌ Status: FAILED")
        print(f"Duration: {result['duration_minutes']:.1f} minutes")
        print(f"Error: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

---

## USAGE EXAMPLES

### Example 1: Simple Brief (Command Line)

```bash
python run_pesquisa_agent.py \
  --brief "Product: Garrafa térmica 1L, Category: Casa e Jardim, Audience: Atletas 25-45 anos, Price: R$ 80-150"
```

### Example 2: JSON Brief File

**brief.json**:
```json
{
  "product": "Fone de ouvido Bluetooth esportivo",
  "category": "Eletrônicos > Áudio",
  "target_audience": "Atletas, praticantes de corrida, 18-35 anos",
  "price_range": "R$ 150 - R$ 280",
  "marketplace_target": ["Mercado Livre", "Shopee"],
  "competitors": ["JBL Endurance Run", "Xiaomi Mi Sports"],
  "special_requirements": "Resistente à água IPX5+"
}
```

```bash
python run_pesquisa_agent.py \
  --brief-file brief.json \
  --output user_research/ \
  --model claude-sonnet-3.5
```

### Example 3: Batch Processing

```bash
# Create multiple brief files
echo '{"product": "Product A", ...}' > brief_1.json
echo '{"product": "Product B", ...}' > brief_2.json

# Run in loop
for brief in brief_*.json; do
  python run_pesquisa_agent.py \
    --brief-file "$brief" \
    --output "batch_research/" \
    --min-quality 0.80
done
```

### Example 4: CI/CD Integration

```yaml
# .github/workflows/research.yml
name: Automated Research
on:
  workflow_dispatch:
    inputs:
      brief_json:
        description: 'Research brief JSON'
        required: true

jobs:
  research:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd agentes/pesquisa_agent/workflows
          pip install -r requirements.txt

      - name: Run research
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          cd agentes/pesquisa_agent/workflows
          echo '${{ github.event.inputs.brief_json }}' > brief.json
          python run_pesquisa_agent.py \
            --brief-file brief.json \
            --output ../user_research/ \
            --min-quality 0.75

      - name: Upload results
        uses: actions/upload-artifact@v3
        with:
          name: research-results
          path: agentes/pesquisa_agent/user_research/
```

---

## TESTING STRATEGY

### Unit Tests

**test_llm_client.py**:
```python
import pytest
from workflows.automation.llm_client import LLMClient

def test_anthropic_client_initialization():
    client = LLMClient(provider="anthropic")
    assert client.provider == "anthropic"
    assert "claude" in client.model

def test_openai_client_initialization():
    client = LLMClient(provider="openai")
    assert client.provider == "openai"
    assert "gpt" in client.model

# Add more tests...
```

### Integration Tests

**test_workflow_execution.py**:
```python
import pytest
from pathlib import Path
from workflows.automation.workflow_executor import WorkflowExecutor

@pytest.fixture
def sample_brief():
    return {
        "product": "Test Product",
        "category": "Test Category",
        "target_audience": "Test Audience",
        "price_range": "R$ 100 - R$ 200"
    }

def test_full_workflow_execution(sample_brief, tmp_path):
    # Setup
    llm = LLMClient(provider="anthropic")
    executor = WorkflowExecutor(
        llm_client=llm,
        prime_path=Path("../PRIME.md"),
        template_path=Path("../templates/research_notes.md"),
        output_dir=tmp_path
    )

    # Execute
    result = executor.execute(sample_brief)

    # Assert
    assert result["success"] == True
    assert result["quality_score"] >= 0.75
    assert (tmp_path / "test_product_research_notes.md").exists()

# Add more tests...
```

---

## DEPLOYMENT CHECKLIST

### Pre-Deployment
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] API keys configured in `.env`
- [ ] Unit tests passing (`pytest tests/unit/`)
- [ ] Integration tests passing (`pytest tests/integration/`)
- [ ] Documentation complete

### Deployment
- [ ] Script executable (`chmod +x run_pesquisa_agent.py`)
- [ ] Tested with sample brief
- [ ] Validated output quality (≥0.75)
- [ ] Batch processing tested
- [ ] Error handling verified

### Post-Deployment
- [ ] Monitor execution times (target: 20-30 min)
- [ ] Track quality scores (≥0.75 consistently)
- [ ] Collect user feedback
- [ ] Optimize bottlenecks (web searches, LLM calls)

---

## PERFORMANCE OPTIMIZATION

### Caching
- Cache web search results (deduplicate queries)
- Cache LLM responses for identical prompts
- Cache marketplace data (refresh every 24h)

### Parallelization
- Run marketplace searches in parallel (Phase 3)
- Run SERP/social searches in parallel (Phase 4)
- Process competitors in parallel (Phase 5)

### Cost Optimization
- Use smaller model for simple phases (Phase 1, 9)
- Use vision only when screenshots critical
- Batch LLM calls where possible

---

## MAINTENANCE

### Monthly
- Review quality scores (ensure ≥0.75 avg)
- Update marketplace URLs if changed
- Update compliance rules (ANVISA, INMETRO)
- Rotate API keys if needed

### Quarterly
- Benchmark against manual execution
- Optimize prompt engineering (reduce tokens)
- Update dependencies (`pip list --outdated`)
- Review error logs for patterns

### Annually
- Major version upgrade (LLM models)
- Architecture review (new patterns, tools)
- User survey (satisfaction, feature requests)

---

**Version**: 1.0.0 (Planning)
**Status**: ⏳ Ready for Implementation (after Phase A validation)
**Estimated Implementation Time**: 2-3 days
**Maintainer**: CODEXA Meta-Constructor

---

> 🎯 **Goal**: Fully automated research execution with 1 command
> 📊 **Success**: Quality ≥0.75, Duration ≤30 min, Batch processing ready
> 🔄 **Evolution**: Phase A (manual) → Phase B (automated) → Phase C (optimized)
