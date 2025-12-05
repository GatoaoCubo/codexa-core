# Pesquisa - Market Research Agent

Execute comprehensive market research and competitive analysis for Brazilian marketplaces.

## Usage

```bash
/pesquisa
```

## Description

This command executes the pesquisa-agent's market research system, specialized for:
- Visual web scraping across 9 Brazilian marketplaces
- Competitor analysis and benchmarking
- SEO taxonomy extraction
- Price and positioning analysis
- Market gap identification

## Features

- **HOP System**: Higher-Order Prompts for customizable workflows
- **GPT-5 Vision**: Advanced visual analysis of marketplace listings
- **Multi-marketplace**: Coverage of ML, Shopee, Magalu, Amazon BR, and more
- **Real-time Data**: Live scraping and analysis

## Workflow

1. **Brief Intake** - Validate product/service brief
2. **Marketplace Scan** - Visual analysis of listings
3. **Competitor Analysis** - Benchmark against top performers
4. **SEO Extraction** - Identify key terms and taxonomy
5. **Report Generation** - Output to `USER_DOCS/produtos/research/`

## Resources

- **Agent Location**: `agentes/pesquisa_agent/`
- **Entry Point**: `PRIME.md` (TAC-7 framework)
- **HOP Plans**: `config/plans/` (standard_research.json, comprehensive_research.json)
- **Output**: `user_research/[produto]_research_notes.md` (+ .llm.json + _metadata.json)

## Related Commands

- `/anuncio` - Generate ads from research
- `/brand` - Create brand strategy
- `/mentor` - Strategic planning