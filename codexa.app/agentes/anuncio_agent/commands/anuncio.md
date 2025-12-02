# Anúncio - Marketplace Ad Generator

Generate optimized marketplace advertisements for Brazilian e-commerce platforms.

## Usage

```bash
/anuncio
```

## Description

This command executes the anuncio-agent's advertisement generation system, specialized for:
- Creating optimized marketplace ads for Brazilian e-commerce
- SEO-optimized product titles and descriptions
- Multi-marketplace adaptation (Mercado Livre, Shopee, Magalu, Amazon BR)
- Keyword generation and competitive positioning
- A/B testing variations

## Workflow

1. **Input Research** - Uses research_notes.md from pesquisa-agent
2. **Generate Ads** - Creates optimized marketplace announcements
3. **Multi-Channel** - Adapts content for different platforms
4. **Export** - Outputs to `USER_DOCS/produtos/marketplace/`

## Resources

- **Agent Location**: `/anuncio-agent/`
- **Command Definition**: `/anuncio-agent/.claude/commands/codexa/codexa.md`
- **HOP Template**: `/anuncio-agent/prompts/_HOP_TEMPLATE.md`
- **Output Directory**: `USER_DOCS/produtos/marketplace/anuncios/`

## Integration with Research

Works seamlessly with `/pesquisa` output:
```bash
# Step 1: Research
/pesquisa "product description"

# Step 2: Generate ads
/anuncio
```

## Note

This command redirects to the anuncio-agent's implementation. The historical version in `_historical/codex_anuncio.md` has been replaced by this integrated approach.