# Roteiro Hands-On: Módulo 03 - Pesquisa de Mercado

**Duração**: 12-15 minutos
**Formato**: Screencast com narração
**Objetivo**: Executar análise competitiva completa em tempo real

---

## SETUP DA TELA

```
┌─────────────────────────────────────────────────────────────┐
│  Claude Code (tela cheia)                                   │
│  Zoom em momentos de output importante                      │
└─────────────────────────────────────────────────────────────┘
```

---

## ROTEIRO DE GRAVAÇÃO

### [00:00 - 01:00] Contexto

**NARRAÇÃO:**
> "Você está pensando em vender um produto novo. Antes de comprar estoque, precisa saber: tem mercado? Quem são os concorrentes? Qual preço praticar? Vou te mostrar como descobrir tudo isso em 15 minutos com o Pesquisa Agent."

---

### [01:00 - 02:30] Carregando e Explicando

**DIGITAR:**
```
/prime-pesquisa
```

**NARRAÇÃO:**
> "O Pesquisa Agent tem acesso a 9 marketplaces brasileiros e mais de 700 URLs testadas. Ele não só busca dados - ele ANALISA e entrega insights."

**MOSTRAR LISTA DOS 9 MARKETPLACES:**
> "Mercado Livre, Amazon BR, Shopee, Magalu, Submarino, Americanas, Casas Bahia, Carrefour e Via Varejo. Tudo num comando só."

---

### [02:30 - 06:00] Quick Research (Validação Rápida)

**NARRAÇÃO:**
> "Primeiro, vou fazer uma Quick Research - validação rápida de 15-20 minutos. Quero saber se vale a pena entrar no mercado de fones bluetooth."

**DIGITAR:**
```
Quick research: fones de ouvido bluetooth no Mercado Livre

Quero saber:
- Tem demanda? (volume de vendas)
- Quem são os top 5 sellers?
- Faixa de preço dominante
- Muita ou pouca concorrência?
```

**COMENTAR OUTPUT:**
> "Olha só o que ele trouxe em segundos: volume alto de buscas, top 5 sellers identificados com preço médio de cada um, faixa dominante entre R$ 80-150, e uma avaliação: 'mercado saturado em fones genéricos, mas oportunidade em nichos específicos'."

**DESTACAR:**
- Volume de demanda
- Faixa de preço
- Nível de concorrência

---

### [06:00 - 10:00] Standard Research (Análise Completa)

**NARRAÇÃO:**
> "Agora vou aprofundar com Standard Research. Quero entender os GAPS - o que está faltando no mercado."

**DIGITAR:**
```
Standard research: fones de ouvido bluetooth

Análise dos 4 pilares:

PILAR 1 - Posicionamento:
- Como os top 5 se posicionam?
- Qual diferencial de cada um?

PILAR 2 - Preços:
- Faixa premium vs econômica
- Quem cobra mais e por quê?

PILAR 3 - Features:
- O que TODO MUNDO oferece?
- O que NINGUÉM oferece? (gap)

PILAR 4 - Reviews:
- Principais elogios
- Principais reclamações
- Oportunidades de melhoria
```

**PAUSAR E COMENTAR CADA PILAR:**

**Posicionamento:**
> "Pilar 1: Veja que os top sellers se dividem em 'barato chinês' e 'premium importado'. Não tem ninguém no meio-termo 'qualidade brasileira com suporte local'."

**Preços:**
> "Pilar 2: Premium cobra 3x mais mas tem reviews melhores. Econômico vende mais volume mas margem apertada."

**Features:**
> "Pilar 3 é o mais importante. O que ninguém oferece? 'Garantia estendida nacional', 'suporte em português por WhatsApp', 'manual em vídeo'. Isso é OPORTUNIDADE."

**Reviews:**
> "Pilar 4: Reclamações mais comuns? 'Bateria dura pouco', 'manual em chinês', 'não tem suporte'. Se você resolver ESSES problemas, se diferencia."

---

### [10:00 - 12:00] Definindo Estratégia de Preço

**NARRAÇÃO:**
> "Com essa análise, vou pedir uma recomendação de precificação."

**DIGITAR:**
```
Baseado na análise, recomende estratégia de preço:

Meu produto:
- Fone bluetooth de qualidade média-alta
- Custo de R$ 45 por unidade
- Quero margem de pelo menos 2x
- Diferencial: suporte em português + garantia 1 ano

Qual preço praticar? Justifique.
```

**COMENTAR OUTPUT:**
> "Ele recomenda R$ 129,90 - posicionamento 'custo-benefício premium'. Não é o mais barato, mas justifica pelo suporte e garantia. E ainda sugere criar bundle: 'fone + case + cabo extra por R$ 149,90'."

---

### [12:00 - 13:00] Comprehensive (Menção)

**NARRAÇÃO:**
> "Se eu fosse investir alto - digamos, importar container - faria Comprehensive Research de 60+ minutos. Ela inclui sazonalidade, forecast de demanda, e estratégia de entrada completa. Mas pra validação inicial, Quick + Standard resolvem."

---

### [13:00 - 13:30] Encerramento

**NARRAÇÃO:**
> "Em 15 minutos, descobri: tem mercado, concorrência é alta mas tem gaps, e tenho uma estratégia de preço justificada. Decisão baseada em DADOS, não achismo."

**MOSTRAR NA TELA:**
```
DADOS COLETADOS:
✓ Demanda validada
✓ Concorrência mapeada
✓ Gaps identificados
✓ Preço definido

PRÓXIMO: Módulo 04 - Estratégia de Marca
```

---

## SCRIPT DE TROUBLESHOOTING

**Se o output for superficial:**
```
Preciso de mais profundidade no Pilar 3 (Features).
Liste pelo menos 10 features que os concorrentes oferecem
e 5 que NINGUÉM oferece ainda.
```

**Se faltar dados de preço:**
```
Preciso de faixa de preço mais detalhada:
- Preço mínimo
- Preço médio
- Preço máximo
- Preço mais comum (moda)
```

**Se quiser comparar marketplaces:**
```
Compara o mesmo produto no Mercado Livre vs Shopee:
- Onde tem mais demanda?
- Onde o preço médio é maior?
- Onde vale mais a pena entrar?
```

---

**Arquivo**: `outputs/hands_on/03_HANDS_ON_PESQUISA.md`
**Criado**: 2025-11-25
**Versão**: 1.0.0
