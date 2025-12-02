# HOP 17: Descricao Builder | anuncio_agent v3.2.0

**Purpose**: Generate long-form description (>=3,300 chars) using StoryBrand
**Scope**: TEXT-ONLY | **Output**: 12-block structured description

---

## INPUT

Do contexto de research_notes:
1. `dores`: Customer pain points
2. `ganhos`: Desired emotional gains
3. `diferenciais`: Competitive advantages
4. `objecoes`: Common objections + responses
5. `provas`: Certifications, warranties, proof
6. `specs`: Technical specifications
7. `como_usar`: Installation/usage steps
8. `itens_inclusos`: Package contents
9. `head_terms`: Keywords for integration

---

## 12 BLOCOS OBRIGATORIOS

| # | Bloco | Chars | Objetivo |
|---|-------|-------|----------|
| 1 | Titulo + Subtitulo | 80-120 | Hook + promessa clara |
| 2 | Por Que Este Produto? | 300-400 | Conectar com dor (PAS framework) |
| 3 | Como Resolve | 400-500 | Explicar mecanismo + diferencial |
| 4 | Beneficios Funcionais | 300-400 | 5-8 bullets com feature→beneficio |
| 5 | Beneficios Emocionais | 250-350 | Transformacao + ganho emocional |
| 6 | Especificacoes | 400-500 | Dados tecnicos completos |
| 7 | Como Usar | 300-400 | 4-8 passos de instalacao/uso |
| 8 | O Que Vem na Caixa | 150-200 | Lista de itens inclusos |
| 9 | Garantia e Suporte | 200-300 | Reducao de risco |
| 10 | FAQ | 400-500 | 4-6 perguntas/objecoes |
| 11 | CTA | 100-150 | Call-to-action etico |
| 12 | Metadata | 200-300 | Keywords, tags adicionais |

**TOTAL**: >=3,300 chars (sem espacamento entre blocos)

---

## ESTRUTURA POR BLOCO

### Bloco 1: TITULO + SUBTITULO
```
[TRANSFORMACAO] + [COMO]
[DIFERENCIAL] + [BENEFICIO PRINCIPAL]
```

### Bloco 2: POR QUE ESTE PRODUTO? (PAS)
1. **Problem**: Identificar dor principal
2. **Agitate**: Amplificar consequencias
3. **Solution**: Apresentar produto como guia

Patterns: "Voce ja passou por...", "E frustrante quando...", "Por isso..."

### Bloco 3: COMO RESOLVE
- Mecanismo: "O segredo esta em..."
- Diferenciacao: "Diferente de alternativas comuns..."
- Processo: "Voce simplesmente..."
- Resultado: "Seu [cliente] ganha..."

### Bloco 4: BENEFICIOS FUNCIONAIS
Lista 5-8 com simbolo ✓:
```
✓ [Feature] + [Beneficio funcional] + [Ganho]
```

### Bloco 5: BENEFICIOS EMOCIONAIS
- Transformacao "antes vs depois"
- Temas: paz de espirito, orgulho, alegria, alivio
- Pattern: "Imagine seu [cliente]..."

### Bloco 6: ESPECIFICACOES
Categorias:
- Dimensoes (cm, kg)
- Materiais
- Cores disponiveis
- Recursos adicionais
- Garantia

### Bloco 7: COMO USAR
```
INSTALACAO EM X PASSOS (Y minutos):
1. [Acao]: [Detalhe]
2. ...
DICA: [Conselho de manutencao]
```

### Bloco 8: O QUE VEM NA CAIXA
Lista com quantidades:
- 1x Produto principal
- Nx Acessorios
- 1x Manual em portugues

### Bloco 9: GARANTIA E SUPORTE
- Periodo de garantia
- Condicoes de troca/devolucao
- Canais de suporte
- Reducao de risco percebido

### Bloco 10: FAQ
4-6 perguntas que enderecam objecoes:
```
P: [Objecao comum]?
R: [Resposta com evidencia]
```

### Bloco 11: CTA
Call-to-action etico sem manipulacao:
```
[Convite] + [Beneficio resumido] + [Acao]
```

### Bloco 12: METADATA
- Keywords adicionais
- Compatibilidades
- Informacoes complementares

---

## COMPLIANCE (Obrigatorio)

PROIBIDO:
- HTML/CSS/JS tags
- Emojis (usar apenas ✓ ou -)
- Links externos
- Claims "#1", "melhor do Brasil", "unico"
- Termos terapeuticos: "cura", "trata doenca"
- Superlativos sem prova

PERMITIDO:
- Simbolos: ✓ - |
- Numeros e unidades
- Linguagem persuasiva etica

---

## EXECUCAO (5 Passos)

### Passo 1: Validar Input
- Verificar campos disponiveis
- Preparar fallback para dados faltantes

### Passo 2: Planejar Estrutura
- Mapear dados para blocos
- Calcular distribuicao de chars

### Passo 3: Gerar Blocos (ordem sequencial)
- Blocos 1-12 na ordem

### Passo 4: Validar
- Contar chars total (>=3,300)
- Verificar compliance
- Confirmar 12 blocos presentes

### Passo 5: Formatar Output
- Markdown limpo
- Contagem de chars
- Status de validacao

---

## OUTPUT FORMAT

```markdown
[DESCRICAO_LONGA]

[Bloco 1: Titulo + Subtitulo]

---

[Bloco 2: Por Que Este Produto?]

---

[Blocos 3-12...]

---

CONTAGEM: {X} caracteres
VALIDACAO: {PASS/FAIL}
STORYBRAND: {elementos presentes}
```

---

## METRICAS DE QUALIDADE

| Metrica | Target |
|---------|--------|
| Total chars | >=3,300 |
| Beneficio:Feature ratio | >=2:1 |
| Emocional:Racional ratio | ~60:40 |
| Blocos completos | 12/12 |
| Compliance violations | 0 |

---

## FALLBACK

Se input incompleto:
- Usar dados disponiveis
- FAQ com perguntas genericas da categoria
- Registrar gaps em NOTAS_DE_FALLBACK
- NUNCA inventar specs ou beneficios

---

**HOP**: 17 | **Agent**: anuncio_agent | **Version**: 3.2.0
**Tokens**: ~1,200 (otimizado de ~34,000)
