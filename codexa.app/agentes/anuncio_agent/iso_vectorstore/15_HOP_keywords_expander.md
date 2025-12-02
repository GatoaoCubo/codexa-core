# HOP 15: Keywords Expander | anuncio_agent v3.2.0

**Purpose**: Generate 2 keyword blocks (115-120 terms each) for SEO
**Scope**: TEXT-ONLY | **Output**: 2 deduplicated keyword blocks

---

## INPUT

Do contexto de research_notes:
1. `head_terms`: Termos principais (ex: ["cama gato", "caminha pet"])
2. `longtails`: Buscas long-tail (ex: ["cama gato janela ventosa"])
3. `sinonimos`: Variacoes morfologicas e sinonimos
4. `contextuais`: Contextos de uso (ex: ["apartamento", "varanda"])
5. `titulos_gerados`: Titulos ja criados (para deduplicate)

---

## BLOCO 1: HEAD TERMS + LSI (115-120 termos)

### Composicao

| Categoria | Quantidade | Exemplo |
|-----------|------------|---------|
| Head terms expandidos | 30-40 | cama gato, caminha gato, cama de gato |
| Sinonimos | 20-30 | poltrona, descanso, nicho, toca |
| LSI keywords | 30-40 | ventosa, oxford, lavavel, resistente |
| Specs com numeros | 15-20 | 15kg, 55x39cm, 90mm, 600D |

### Estrategias de Expansao

**Head terms**:
- Singular/plural: cama → camas
- Com/sem artigo: cama gato, cama de gato
- Ordem invertida: cama gato → gato cama

**LSI (Latent Semantic Indexing)**:
- Componentes: ventosa, suporte, almofada
- Materiais: oxford, poliester, espuma
- Caracteristicas: lavavel, resistente, duravel

---

## BLOCO 2: LONGTAILS + CONTEXTUAIS (115-120 termos)

### Composicao

| Categoria | Quantidade | Exemplo |
|-----------|------------|---------|
| Longtails completos | 40-50 | cama gato janela ventosa |
| Termos contextuais | 30-40 | apartamento, varanda, sacada |
| Ocasiao/sazonalidade | 20-30 | inverno, verao, dia todo |
| Keywords criativas | 15-25 | gato feliz, sem baguna, facil limpar |

---

## DEDUPLICATE (Obrigatorio)

Ordem de execucao:
1. Remover termos que estao nos titulos
2. Remover de BLOCO_2 termos que estao em BLOCO_1
3. Remover duplicatas exatas dentro de cada bloco
4. Remover termos >80% similares no mesmo bloco

```
For termo in BLOCO_2:
  If termo in TITULOS: remove
  If termo in BLOCO_1: remove
  If similaridade(termo, outro_BLOCO_2) > 0.8: remove
```

---

## COMPLIANCE

PROIBIDO:
- HTML/emojis/simbolos especiais
- Claims "#1", "melhor do Brasil"
- Termos terapeuticos sem ANVISA
- Links ou URLs
- Spam (mesma palavra 5+ vezes)

---

## OUTPUT FORMAT

```
BLOCO_PALAVRAS_1:
{termo1}, {termo2}, {termo3}, ...

Contagem: {n}/120 termos

BLOCO_PALAVRAS_2:
{termo1}, {termo2}, {termo3}, ...

Contagem: {n}/120 termos

Validacao:
- Duplicatas removidas: {n}
- Compliance: PASS/FAIL
```

---

## VALIDACAO

| Criterio | Target |
|----------|--------|
| Termos BLOCO_1 | 115-120 |
| Termos BLOCO_2 | 115-120 |
| Duplicatas entre blocos | 0 |
| Duplicatas com titulos | 0 |
| Compliance violations | 0 |

---

**HOP**: 15 | **Agent**: anuncio_agent | **Version**: 3.2.0
**Tokens**: ~600 (otimizado)
