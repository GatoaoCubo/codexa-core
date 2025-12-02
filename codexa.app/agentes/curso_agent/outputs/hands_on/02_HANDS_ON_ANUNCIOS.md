# Roteiro Hands-On: Módulo 02 - Anúncios de E-commerce

**Duração**: 12-15 minutos
**Formato**: Screencast com narração
**Objetivo**: Criar um anúncio completo do zero ao publicável

---

## SETUP DA TELA

```
┌─────────────────────────────────────────────────────────────┐
│  Claude Code (70% da tela)  │  Notepad/Notion (30%)        │
│  ┌─────────────────────────┐│  ┌─────────────────────────┐ │
│  │ Chat com agente         ││  │ Brief do produto        │ │
│  │                         ││  │ (para copiar/colar)     │ │
│  └─────────────────────────┘│  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## ROTEIRO DE GRAVAÇÃO

### [00:00 - 01:00] Contexto

**NARRAÇÃO:**
> "Neste hands-on, vou criar um anúncio completo para Mercado Livre. Vou usar um produto real - uma garrafa térmica - e você vai ver todo o processo, desde o brief até o anúncio pronto pra publicar."

**MOSTRAR NA TELA (Notepad):**
```
BRIEF DO PRODUTO:
- Produto: Garrafa Térmica Inox Premium
- Capacidade: 500ml
- Material: Aço inoxidável 304
- Diferencial: Mantém temperatura 24h
- Público: 25-40 anos, praticam esportes
- Preço: R$ 89,90
- Marketplace: Mercado Livre
```

---

### [01:00 - 03:00] Carregando o Agente

**DIGITAR:**
```
/prime-anuncio
```

**NARRAÇÃO (enquanto carrega):**
> "Primeiro, carrego o Anuncio Agent. Ele vai trazer todo o conhecimento de copywriting, SEO de marketplace, e compliance."

**DEPOIS QUE CARREGAR:**
> "Pronto. Agora o Claude está verticalizado em anúncios. Vou colar o brief e pedir o anúncio completo."

---

### [03:00 - 06:00] Criando o Anúncio

**DIGITAR (copiando do Notepad):**
```
Crie um anúncio completo para Mercado Livre com:

PRODUTO:
- Garrafa Térmica Inox Premium 500ml
- Aço inoxidável 304
- Mantém temperatura por 24h
- Público: pessoas ativas 25-40 anos
- Preço: R$ 89,90

QUERO:
1. Título otimizado (máx 60 caracteres)
2. 5 bullet points focados em benefícios
3. Descrição de 500 palavras com storytelling
4. Validação de compliance
```

**ESPERAR OUTPUT E COMENTAR CADA PARTE:**

**Título:**
> "Olha o título: 'Garrafa Térmica Inox 500ml - Mantém 24h Gelada Premium'. Keywords no início, benefício principal, e 58 caracteres - dentro do limite."

**Bullets:**
> "Os bullet points estão focando em BENEFÍCIOS, não características. Veja: não é 'aço inox 304', é 'material que não enferruja e não deixa gosto'. Isso é copywriting de verdade."

**Descrição:**
> "A descrição segue o framework PAS - Problema, Agitação, Solução. Começa com a dor do cliente, amplifica, e apresenta o produto como solução."

**Compliance:**
> "E aqui embaixo tem a validação de compliance. Não precisa de registro ANVISA porque não é alimento nem cosmético. INMETRO não obrigatório para garrafas. Tudo limpo."

---

### [06:00 - 08:00] Pedindo Ajustes

**NARRAÇÃO:**
> "Agora vou mostrar algo importante: como pedir ajustes. Digamos que eu queira um tom mais premium no título."

**DIGITAR:**
```
Refaz o título com tom mais premium/sofisticado.
Quero que pareça produto de R$ 150+, não R$ 50.
```

**MOSTRAR NOVA VERSÃO E COMENTAR:**
> "Veja a diferença: ele trocou 'Gelada' por 'Temperatura Ideal', adicionou 'Design Elegante'. Palavras que justificam preço premium."

---

### [08:00 - 10:00] Adaptando para Outro Marketplace

**NARRAÇÃO:**
> "E se eu quiser o mesmo anúncio pra Shopee? Os requisitos são diferentes."

**DIGITAR:**
```
Adapta esse anúncio para Shopee.
Considera:
- Título pode ter até 80 caracteres
- Tom mais jovem/casual
- Foco em preço competitivo
```

**COMENTAR OUTPUT:**
> "Olha como mudou: título maior aproveitando os 80 caracteres, tom mais descontraído, e ele adicionou 'Frete Grátis' que é muito importante na Shopee."

---

### [10:00 - 12:00] Validação Final

**NARRAÇÃO:**
> "Antes de publicar, sempre peço uma validação final."

**DIGITAR:**
```
Faz um checklist de validação:
- SEO está ok?
- Compliance está ok?
- Alguma melhoria sugerida?
```

**MOSTRAR OUTPUT E COMENTAR:**
> "Ele me dá um checklist completo. SEO: keywords posicionadas ✓. Compliance: sem pendências ✓. E ainda sugere adicionar 'Pronta Entrega' no título se eu tiver estoque."

---

### [12:00 - 12:30] Encerramento

**NARRAÇÃO:**
> "Em menos de 10 minutos, criei um anúncio profissional, otimizado, com compliance validado, e adaptado pra dois marketplaces. Isso levaria 2-3 horas fazendo manual."

**MOSTRAR NA TELA:**
```
TEMPO ECONOMIZADO: ~2.5 horas
PRÓXIMO: Módulo 03 - Pesquisa de Mercado
```

---

## SCRIPT DE TROUBLESHOOTING (Se algo der errado)

**Se o output for genérico:**
> "Às vezes o output pode ficar genérico. Nesse caso, você adiciona mais contexto..."
```
Seja mais específico. Meu público são homens 30-40 que vão pra academia 5x/semana.
```

**Se faltar compliance:**
> "Se ele não mencionar compliance, você pergunta diretamente..."
```
Esse produto precisa de algum registro ANVISA ou INMETRO?
```

**Se o título passar do limite:**
> "Se o título ficar longo demais, peça pra encurtar..."
```
Título ficou com 65 caracteres. Preciso máximo 60. Encurta mantendo as keywords principais.
```

---

## CHECKLIST PRÉ-GRAVAÇÃO

- [ ] Brief do produto pronto no Notepad
- [ ] Claude Code com /prime-anuncio carregado
- [ ] Tela dividida configurada
- [ ] Exemplos de troubleshooting ensaiados

---

**Arquivo**: `outputs/hands_on/02_HANDS_ON_ANUNCIOS.md`
**Criado**: 2025-11-25
**Versão**: 1.0.0
