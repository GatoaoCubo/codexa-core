# HOP 14: Titulo Generator | anuncio_agent v3.2.0

**Purpose**: Generate 3 titles (58-60 chars each) with maximum keyword density
**Scope**: TEXT-ONLY | **Output**: 3 title variations (A/B/C)

---

## REGRA CRITICA: ZERO PALAVRAS GRAMATICAIS

### PROIBIDO
- Artigos: o, a, os, as, um, uma
- Preposicoes: de, para, com, sem, em, por
- Conjuncoes: e, ou, mas, que
- Pronomes: esse, esta, seu, sua
- Verbos auxiliares: e, sao, esta

### PERMITIDO (apenas keywords)
- Substantivos: Cama, Gato, Janela, Ventosas
- Adjetivos: Segura, Lavavel, Premium, Resistente
- Numeros/specs: 90mm, 15kg, 55x39cm, 600D
- Marcas/modelos: Sony, XM5, Apple
- Beneficios: Fixacao, Conforto, Durabilidade

**Excecao unica**: "p/" (abreviacao de "para") se economizar >=3 chars

---

## INPUT

Do contexto de research_notes:
1. `head_terms`: Termos principais (ex: "Cama Gato Janela")
2. `diferenciais`: Features unicas (ex: "Ventosas 90mm")
3. `ganhos`: Beneficios (ex: "Conforto", "Seguranca")
4. `specs`: Especificacoes (ex: "ate 15kg", "55x39cm")

---

## FORMULAS DE COMPOSICAO

### Formula A: HEAD_TERM + SPEC + DIFERENCIAL + BENEFICIO
```
Cama Gato Janela Ventosas 90mm Fixacao Segura 15kg Oxford
58 chars | 10 keywords
```

### Formula B: HEAD_TERM + MATERIAL + BENEFICIO + DIMENSAO
```
Cama Gato Janela Oxford 600D Conforto Seguranca Lavavel 55cm
60 chars | 9 keywords
```

### Formula C: HEAD_TERM + CONTEXTO + DIFERENCIAL + SPEC
```
Cama Gato Janela Apartamento Sem Furos Ventosa 55x39 Premium
60 chars | 9 keywords
```

---

## EXECUCAO (5 Passos)

### Passo 1: Extrair Keywords do Input
```
HEAD_TERM: Cama Gato Janela
DIFERENCIAIS: Ventosas, 90mm, Oxford 600D, Sem Furos
GANHOS: Seguranca, Conforto, Fixacao
SPECS: 15kg, 55x39cm, 4 Ventosas
CONTEXTO: Apartamento, Varanda
```

### Passo 2: Criar Titulo A (Funcional Tecnico)
- HEAD_TERM + SPEC_NUMERO + DIFERENCIAL + BENEFICIO
- 8-10 keywords distintas
- 58-60 chars exatos

### Passo 3: Criar Titulo B (Beneficio Qualidade)
- HEAD_TERM + MATERIAL + BENEFICIO_EMOCIONAL + DIMENSAO
- Angulo diferente de A
- 58-60 chars exatos

### Passo 4: Criar Titulo C (Contextual)
- HEAD_TERM + CONTEXTO + DIFERENCIAL_UNICO + SPEC
- Angulo diferente de A e B
- 58-60 chars exatos

### Passo 5: Validacao Final
- [ ] ZERO conectores gramaticais em todos
- [ ] HEAD_TERM em position 0-15 de todos
- [ ] >= 8 keywords distintas por titulo
- [ ] 58-60 chars exatos por titulo
- [ ] >= 60% termos diferentes entre titulos

---

## TECNICAS DE COMPRESSAO

| Antes | Depois | Economia |
|-------|--------|----------|
| Cama de Gato para Janela | Cama Gato Janela | 9 chars |
| Quinze Quilos | 15kg | 9 chars |
| 55 cm x 39 cm | 55x39cm | 6 chars |
| para Apartamento | p/ Apartamento | 2 chars |

---

## OUTPUT FORMAT

```
TITULO A (Funcional):
{titulo_a}
Chars: {n}/60 | Keywords: {k}

TITULO B (Beneficio):
{titulo_b}
Chars: {n}/60 | Keywords: {k}

TITULO C (Contextual):
{titulo_c}
Chars: {n}/60 | Keywords: {k}
```

---

## VALIDACAO AUTOMATICA

```python
# Criterios de PASS
titulo_chars >= 58 and titulo_chars <= 60
keywords_count >= 8
conectores_count == 0
head_term_position <= 15
```

---

**HOP**: 14 | **Agent**: anuncio_agent | **Version**: 3.2.0
**Tokens**: ~800 (otimizado de ~26,000)
