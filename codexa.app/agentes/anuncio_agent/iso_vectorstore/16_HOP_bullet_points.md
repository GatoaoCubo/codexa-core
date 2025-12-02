# HOP 16: Bullet Points | anuncio_agent v3.2.0

**Purpose**: Generate 10 strategic bullet points (250-299 chars each)
**Scope**: TEXT-ONLY | **Output**: 10 conversion-optimized bullets

---

## PROPOSITO TRIPLO

Cada bullet deve ser simultaneamente:
- **GANCHO**: Captura atencao nos primeiros 5-7 palavras
- **ISCA**: Cria desejo atraves de beneficios tangiveis
- **SEO**: Contem keywords naturalmente integradas

---

## ANATOMIA DO BULLET

```
[GANCHO] + [BENEFICIO/DIFERENCIAL] + [PROVA/SPEC] + [RESULTADO EMOCIONAL]
```

**Exemplo** (295 chars):
```
Fixacao em janela sem furos na parede - ventosas profissionais de 90mm suportam ate 15kg com margem de seguranca 2x - ideal para imoveis alugados onde voce nao pode danificar estruturas mas precisa de espaco vertical para seu gato descansar confortavelmente
```

---

## 5 CATEGORIAS (2 bullets cada)

### Cat 1: PROBLEMA → SOLUCAO (Bullets 1-2)
Formula: [DOR] + [COMO RESOLVE] + [RESULTADO]

### Cat 2: DIFERENCIAL COMPETITIVO (Bullets 3-4)
Formula: [DIFERENCIAL] + [COMPARACAO IMPLICITA] + [BENEFICIO EXCLUSIVO]

### Cat 3: BENEFICIO FUNCIONAL + EMOCIONAL (Bullets 5-6)
Formula: [SPEC TECNICA] + [VANTAGEM PRATICA] + [GANHO EMOCIONAL]

### Cat 4: PROVA SOCIAL / AUTORIDADE (Bullets 7-8)
Formula: [PROVA/CERTIFICACAO] + [O QUE GARANTE] + [REDUCAO DE RISCO]

### Cat 5: OCASIAO DE USO (Bullets 9-10)
Formula: [SITUACAO] + [COMO SE ENCAIXA] + [RESULTADO SITUACIONAL]

---

## REGRAS OBRIGATORIAS

### FAZER
- 250-299 chars exatos por bullet
- Keywords naturais (nao forcadas)
- Numeros concretos (nao "muito", usar "ate 15kg")
- Ratio beneficio:feature >= 2:1
- Ultimo terco conecta com ganho emocional
- Usar "voce", "seu", "sua" (cliente como heroi)

### EVITAR
- HTML/CSS/JS tags
- Emojis
- Claims "#1", "melhor do Brasil" sem prova
- Termos terapeuticos
- Superlativos vazios ("incrivel", "revolucionario")
- Repeticao de keywords entre bullets

---

## EXECUCAO (4 Passos)

### Passo 1: Analisar Input
Extrair:
- Top 3-5 dores/problemas
- Top 3-5 diferenciais
- Top 3-5 beneficios funcionais/emocionais
- Specs principais
- Keywords primarias/secundarias

### Passo 2: Distribuir nas 5 Categorias
- 2 bullets por categoria
- Mapear dados para cada bullet

### Passo 3: Redigir
Para cada bullet:
1. Escrever com gancho forte
2. Validar 250-299 chars
3. Se <250: expandir com detalhes
4. Se >299: comprimir palavras vazias

### Passo 4: Validar
- [ ] 10 bullets exatos
- [ ] Todos 250-299 chars
- [ ] 2 por categoria
- [ ] Zero repeticao excessiva
- [ ] Compliance OK

---

## OUTPUT FORMAT

```
BULLET POINTS ESTRATEGICOS:

1. {bullet_1}
   Chars: {n} | Cat: Problema-Solucao

2. {bullet_2}
   Chars: {n} | Cat: Problema-Solucao

3. {bullet_3}
   Chars: {n} | Cat: Diferencial

[...continua ate 10...]

Validacao:
- Todos 250-299 chars: PASS/FAIL
- Compliance: PASS/FAIL
- Keywords integradas: {n}
```

---

## METRICAS

| Metrica | Target |
|---------|--------|
| Total bullets | 10 exatos |
| Chars por bullet | 250-299 |
| Categorias cobertas | 5/5 |
| Compliance violations | 0 |

---

**HOP**: 16 | **Agent**: anuncio_agent | **Version**: 3.2.0
**Tokens**: ~700 (otimizado)
