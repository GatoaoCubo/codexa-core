# Roteiro Hands-On: Módulo 05 - Fotos com IA

**Duração**: 12-15 minutos
**Formato**: Screencast com narração
**Objetivo**: Gerar grid 3x3 de fotos profissionais para marketplace

---

## SETUP DA TELA

```
┌─────────────────────────────────────────────────────────────┐
│  Claude Code (50%)         │  Galeria de imagens (50%)     │
│  ┌───────────────────────┐ │  ┌───────────────────────────┐│
│  │ Chat com agente       │ │  │ Preview das fotos geradas││
│  └───────────────────────┘ │  └───────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

---

## ROTEIRO DE GRAVAÇÃO

### [00:00 - 01:00] Contexto

**NARRAÇÃO:**
> "Foto ruim mata venda. Foto profissional converte. Neste hands-on, vou gerar 9 fotos de produto usando IA - o famoso grid 3x3 que todo marketplace pede. E você vai ver que não precisa de estúdio, fotógrafo, nem equipamento caro."

---

### [01:00 - 02:30] Carregando e Planejando

**DIGITAR:**
```
/prime-photo
```

**NARRAÇÃO:**
> "O Photo Agent trabalha com ADW - workflow de 5 fases - e HOP - prompts modulares. Mas você não precisa entender isso pra usar. Só precisa descrever o produto."

**MOSTRAR PLANEJAMENTO:**
```
PRODUTO: Garrafa térmica inox premium
MARKETPLACE: Mercado Livre
OBJETIVO: Grid 3x3 profissional

CENAS PLANEJADAS:
1. Hero shot (fundo branco)
2. Detalhe do material
3. Vista superior
4. Lifestyle outdoor
5. Comparação de tamanho
6. Embalagem
7. Uso em academia
8. Detalhe da tampa
9. Infográfico de features
```

---

### [02:30 - 06:00] Gerando o Grid

**DIGITAR:**
```
Cria grid 3x3 de fotos para garrafa térmica inox premium 500ml.

REQUISITOS MERCADO LIVRE:
- Mínimo 1200x1200px
- Fundo branco na principal
- 85% do espaço preenchido

ESTILO: Commercial-minimalist
MARCA: EcoFlow (sustentável, moderna)
CORES DA MARCA: Verde #87A878, Terracota #C67B5C

CENAS:
1. Hero shot - fundo branco, produto centralizado
2. Material - close no aço inox, textura visível
3. Top view - tampa aberta, interior visível
4. Lifestyle - pessoa bebendo durante trilha
5. Scale - garrafa ao lado de mão/objeto comum
6. Packaging - embalagem premium, eco-friendly
7. Gym - atleta com garrafa em academia moderna
8. Detail - mecanismo da tampa, vedação
9. Infographic - setas apontando features

Gera os prompts otimizados para cada cena.
```

**COMENTAR OUTPUT:**
> "Olha os prompts que ele gerou. Não é só 'foto de garrafa'. Tem especificação de câmera, iluminação, ângulo, contexto. É nível fotógrafo profissional."

**DESTACAR UM PROMPT:**
> "Cena 4, lifestyle: 'Product photography of premium stainless steel water bottle, held by athletic woman on mountain trail, golden hour lighting, shallow depth of field, shot on Sony A7III, 85mm f/1.8'. Isso gera foto de catálogo, não foto de celular."

---

### [06:00 - 09:00] Executando a Geração

**NARRAÇÃO:**
> "Agora vou pedir pra gerar. Dependendo da ferramenta de imagem que você usar - Midjourney, DALL-E, Leonardo - você copia esses prompts e executa."

**DIGITAR:**
```
Gera a imagem da Cena 1 (Hero shot).

Prompt otimizado para geração:
[Copia o prompt que ele criou]
```

**MOSTRAR RESULTADO (se tiver integração) OU EXPLICAR:**
> "Aqui eu copio esse prompt e colo no Midjourney. Em 60 segundos, tenho a foto. Vou fazer o mesmo pras outras 8."

**MOSTRAR GRID MONTADO (se tiver imagens de exemplo):**
> "Olha o resultado final: 9 fotos profissionais, consistentes em estilo, prontas pra subir no ML."

---

### [09:00 - 11:00] Validação e Ajustes

**DIGITAR:**
```
Valida se o grid atende requisitos do Mercado Livre:
- Resolução mínima?
- Fundo branco na principal?
- Variedade de ângulos?
- Brand consistency?
```

**COMENTAR:**
> "Ele valida automaticamente: resolução ok, fundo branco na hero, 9 ângulos diferentes, todas seguindo paleta da marca. Se algo estivesse errado, ele apontaria."

**PEDINDO AJUSTE:**
```
A Cena 7 (gym) ficou muito escura.
Refaz o prompt com iluminação mais clara, estilo Apple Store.
```

---

### [11:00 - 12:30] Adaptando para Outro Marketplace

**NARRAÇÃO:**
> "E se eu quiser adaptar pra Shopee? Requisitos são diferentes."

**DIGITAR:**
```
Adapta o grid para Shopee:
- Pode ter fundo colorido
- Lifestyle converte mais que produto isolado
- Público mais jovem

Quais cenas eu troco? Quais prompts ajusto?
```

**COMENTAR:**
> "Ele sugere trocar a Cena 1 por lifestyle como principal - Shopee é mais visual. E adicionar pessoa jovem usando o produto em todas as fotos possíveis."

---

### [12:30 - 13:00] Encerramento

**NARRAÇÃO:**
> "9 fotos profissionais, prontas pra marketplace, geradas com IA. Sem estúdio, sem fotógrafo, sem dias de trabalho. Isso é o Photo Agent."

**MOSTRAR NA TELA:**
```
GRID CRIADO:
✓ 9 cenas planejadas
✓ Prompts profissionais
✓ Brand consistency
✓ Marketplace compliance
✓ Variação de contexto

PRÓXIMO: Módulo 06 - Meta-Construção
```

---

## SCRIPT DE TROUBLESHOOTING

**Se a imagem ficar genérica:**
```
Imagem ficou muito stock photo.
Adiciona elementos únicos:
- Gotas de água na superfície
- Reflexo de montanha no metal
- Pessoa com estilo específico (não modelo genérico)
```

**Se as cores não baterem com a marca:**
```
As cores do ambiente não combinam com minha marca.
Paleta é verde #87A878 e terracota #C67B5C.
Ajusta o cenário pra ter elementos nessas cores.
```

**Se precisar de mais variedade:**
```
Preciso de 3 versões diferentes da Cena 4 (lifestyle):
- Uma em trilha
- Uma em praia
- Uma em escritório moderno
Mantém mesmo estilo e qualidade.
```

---

**Arquivo**: `outputs/hands_on/05_HANDS_ON_FOTOS.md`
**Criado**: 2025-11-25
**Versão**: 1.0.0
