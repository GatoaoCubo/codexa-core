# Magazine Luiza - Copy Specs

**Version**: 1.0.0 | **Marketplace**: Magazine Luiza | **Focus**: EAN + Ficha Tecnica Completa

---

## Overview

Magalu e o marketplace mais tecnico do Brasil. Copy aqui significa:
- **EAN obrigatorio** (sem excecoes)
- **Ficha tecnica completa** (ranking depende)
- **Padrao de titulo rigido** (Marca + Modelo + Specs)

---

## 1. TITULOS (Max 256 chars)

### Formula Magalu (Obrigatoria)
```
[MARCA] + [MODELO/LINHA] + [CARACTERISTICAS PRINCIPAIS] + [ESPECIFICACOES TECNICAS]
```

### Regras Especificas Magalu

| Regra | Obrigatorio | Exemplo |
|-------|-------------|---------|
| Marca primeiro | Sim | `Samsung Galaxy...` |
| Modelo especificado | Sim | `...S23 Ultra...` |
| Specs tecnicas | Sim | `...256GB 12GB RAM` |
| Sem CAIXA ALTA | Sim | NAO usar `PROMOÇÃO` |
| Sem texto imagem | Sim | Proibido overlay |

### Exemplos por Categoria

**Smartphones**:
```
Samsung Galaxy S23 Ultra Smartphone 256GB 12GB RAM Tela 6.8 5G Preto
Apple iPhone 15 Pro Max Smartphone 256GB Titanio Natural A17 Pro
Xiaomi Redmi Note 12 Pro Smartphone 128GB 6GB RAM Tela 6.67 AMOLED Azul
```

**Eletrodomesticos**:
```
Electrolux Geladeira Frost Free Duplex 474L Inox Painel Touch DF56S
Brastemp Maquina de Lavar 12kg Ciclo Tira Manchas Branca BWK12AB
LG Ar Condicionado Split Inverter 12000 BTUs Frio 220V Dual Voice
```

**Informatica**:
```
Dell Notebook Inspiron 15 Intel Core i7 16GB RAM SSD 512GB Tela 15.6 W11
Logitech Teclado Mecanico Gamer G Pro RGB Switch GX Blue ABNT2 Preto
Samsung Monitor Curvo 27 Polegadas Full HD 75Hz HDMI VA LC27F390FH
```

---

## 2. FICHA TECNICA (Obrigatoria)

### Campos Obrigatorios por Categoria

**Eletronicos**:
| Campo | Obrigatorio | Exemplo |
|-------|-------------|---------|
| Marca | Sim | Samsung |
| Modelo | Sim | UN50AU7700GXZD |
| EAN | Sim | 7892509115643 |
| NCM | Sim | 8528.72.00 |
| Voltagem | Sim | Bivolt |
| Garantia | Sim | 12 meses |
| Peso | Sim | 12.5 kg |
| Dimensoes produto | Sim | 111.8 x 64.5 x 6.0 cm |
| Dimensoes embalagem | Sim | 125 x 75 x 15 cm |

**Moda**:
| Campo | Obrigatorio | Exemplo |
|-------|-------------|---------|
| Marca | Sim | Reserva |
| Material | Sim | 100% Algodao |
| EAN | Sim | 7891234567890 |
| Tamanhos disponiveis | Sim | P, M, G, GG |
| Cores disponiveis | Sim | Preto, Branco, Azul |
| Genero | Sim | Masculino |

### Impacto da Ficha Tecnica

| Completude | Impacto no Ranking |
|------------|-------------------|
| 100% | Maximo ranqueamento |
| 80-99% | Bom ranqueamento |
| 60-79% | Ranqueamento medio |
| < 60% | Baixo ranqueamento |

---

## 3. EAN/GTIN (Obrigatorio!)

### O Que E EAN?

EAN (European Article Number) = Codigo de barras unico do produto.

### Regras EAN Magalu

| Regra | Requisito |
|-------|-----------|
| Obrigatoriedade | 100% (exceto casos especiais) |
| Formato | 13 digitos |
| Validacao | Digito verificador valido |
| Unicidade | 1 EAN = 1 SKU |

### Excecoes (Sem EAN)

- Produtos artesanais
- Produtos personalizados
- Algumas categorias especificas (mediante aprovacao)

### Onde Obter EAN?

1. **GS1 Brasil** - Fonte oficial
2. **Fabricante** - Codigo do produto
3. **Importador** - Deve registrar

---

## 4. DESCRICAO (Max 4,000 chars)

### Estrutura Magalu

```
[INTRODUCAO - 1 paragrafo]
O [Produto] [Marca] [Modelo] e a solucao ideal para [necessidade].

[BENEFICIOS PRINCIPAIS - 3-5 pontos]
- [Beneficio 1]: [explicacao]
- [Beneficio 2]: [explicacao]
- [Beneficio 3]: [explicacao]

[ESPECIFICACOES TECNICAS DETALHADAS]
- Dimensoes: [largura] x [altura] x [profundidade]
- Peso: [peso] kg
- Material: [material]
- Voltagem: [voltagem]
- Potencia: [potencia]
- Capacidade: [capacidade]

[CONTEUDO DA EMBALAGEM]
- 1x [produto principal]
- 1x [cabo/acessorio]
- 1x Manual de instrucoes
- Certificado de garantia

[GARANTIA]
Garantia do fabricante de [periodo].
Garantia estendida disponivel na compra.
```

### Formatacao

- **SEM HTML** - Texto puro apenas
- Paragrafos curtos
- Listas com hifens
- Specs em formato padronizado

---

## 5. IMAGENS (10-15 recomendado)

### Hierarquia de Imagens Magalu

| Posicao | Tipo | Requisito |
|---------|------|-----------|
| 1 | Principal | Fundo branco PURO |
| 2-4 | Angulos | Diferentes perspectivas |
| 5-7 | Detalhes | Close-ups de features |
| 8-10 | Em uso | Contexto/lifestyle |
| 11-15 | Extras | Dimensoes, embalagem |

### Regras de Imagem Magalu

| Regra | Obrigatorio |
|-------|-------------|
| Sem texto | Sim - PROIBIDO overlay |
| Sem logos | Sim - exceto no produto |
| Fundo branco | Sim - imagem principal |
| Min 1000x1000 | Sim |
| Max 5MB | Sim |
| JPG ou PNG | Sim |

### O Que NAO Pode na Imagem

- Texto sobreposto
- Logomarcas de concorrentes
- Informacoes de contato
- Links ou URLs
- Precos ou promocoes
- Watermarks de outros sites

---

## 6. VIDEO

### Especificacoes

| Aspecto | Requisito |
|---------|-----------|
| Duracao max | 120 segundos |
| Formato | MP4 |
| Tamanho max | 50MB |
| Resolucao | 1080p recomendado |

### Conteudo Sugerido

```
[0-10s] Apresentacao do produto
[10-40s] Demonstracao de uso
[40-70s] Features principais
[70-100s] Especificacoes tecnicas
[100-120s] Garantia e CTA
```

---

## 7. CATEGORIAS ESPECIAIS

### Eletroeletronicos

**Obrigatorios**:
- Voltagem especificada
- Garantia informada
- Selo INMETRO (quando aplicavel)
- Homologacao ANATEL (telecomunicacoes)

**Exemplo de Specs**:
```
Voltagem: Bivolt (110V/220V)
Potencia: 1200W
Certificacoes: INMETRO, ANATEL
Garantia: 12 meses fabricante
```

### Alimentos/Bebidas

**Obrigatorios**:
- Registro ANVISA
- Data de validade
- Informacoes nutricionais
- Condicoes de armazenamento

### Produtos Infantis

**Obrigatorios**:
- Certificacao INMETRO
- Faixa etaria recomendada
- Avisos de seguranca
- Materiais atoxicos

---

## 8. SEO INTERNO MAGALU

### Fatores de Ranqueamento

| Fator | Peso | Como Otimizar |
|-------|------|---------------|
| Completude cadastro | 20-25% | 100% dos campos |
| EAN correto | 10-15% | Validar digito |
| Qualidade imagens | 10-15% | Min 10 fotos HQ |
| Ficha tecnica | 15-20% | Todos atributos |
| Preco competitivo | 15-20% | Monitorar mercado |
| Disponibilidade | 10-15% | Estoque sempre |

### Checklist SEO Magalu

- [ ] EAN valido e correto
- [ ] NCM correto para categoria
- [ ] Titulo formato: Marca + Modelo + Specs
- [ ] Ficha tecnica 100% preenchida
- [ ] 10+ imagens alta qualidade
- [ ] Imagem principal fundo branco puro
- [ ] Zero texto em imagens
- [ ] Descricao 2500-3500 chars
- [ ] Garantia especificada
- [ ] Voltagem informada (eletronicos)
- [ ] Certificacoes listadas (quando aplicavel)

---

## 9. ERROS QUE BLOQUEIAM PUBLICACAO

| Erro | Consequencia | Como Evitar |
|------|--------------|-------------|
| EAN invalido | Bloqueio | Validar antes |
| EAN duplicado | Bloqueio | 1 EAN por SKU |
| Texto em imagem | Rejeicao | Fotos limpas |
| CAIXA ALTA | Rejeicao | Title case |
| Ficha incompleta | Baixo ranking | 100% campos |
| Sem garantia | Problema legal | Sempre informar |
| Voltagem omitida | Problema SAC | Especificar sempre |

---

## 10. INTEGRACAO COM ERP

### Sistemas Compativeis

- Bling
- Tiny ERP
- Olist
- VTEX
- Tray

### Campos de Integracao

| Campo ERP | Campo Magalu |
|-----------|--------------|
| SKU | Codigo interno |
| EAN | Codigo de barras |
| Titulo | Nome do produto |
| Descricao | Descricao longa |
| Preco | Preco de venda |
| Estoque | Quantidade disponivel |

---

**Sync**: `config/marketplace_specs.json` (magalu)
**Last Updated**: 2025-12-05
