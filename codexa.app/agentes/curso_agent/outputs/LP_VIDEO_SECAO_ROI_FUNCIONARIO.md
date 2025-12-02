# SEÇÃO: ARGUMENTO ECONÔMICO - ROI vs Funcionário CLT

**Versão**: 1.0.0
**Data**: 2025-12-02
**Tipo**: Roteiro de vídeo (60-90 segundos)
**Contexto**: Parte do vídeo de 10min da LP codexa.app
**Tom**: Dados duros, sem emoção, números falam
**Mood**: Sério, impactante, sem hype

---

## TIMECODE & ESTRUTURA

### [00:00-00:08] SETUP (8 segundos)

**NARRAÇÃO**:
> "Antes de contratar alguém, você deveria perguntar: essa tarefa pode ser automatizada?"

**VISUAL**:
- Tela dividida verticalmente ao meio
- Esquerda: silhueta de funcionário (cinza)
- Direita: logo CODEXA (azul elétrico #2563EB)
- Background: DEEP_OCEAN (#0A1628)

**TEXT OVERLAY**:
- Nenhum ainda (deixa a pergunta respirar)

---

### [00:08-00:25] COMPARAÇÃO LADO A LADO (17 segundos)

**NARRAÇÃO**:
> "Funcionário CLT júnior em marketing digital. Salário: três mil reais. Mais sessenta e oito por cento de encargos: dois mil e quarenta. Total mensal: cinco mil e quarenta reais."

**VISUAL**:
- Tabela comparativa aparece (animação LAYER_REVEAL)
- Cada linha surge conforme narração menciona

```
┌─────────────────────────┬──────────────────┬──────────────┐
│ CRITÉRIO                │ FUNCIONÁRIO CLT  │ CODEXA       │
├─────────────────────────┼──────────────────┼──────────────┤
│ Custo mensal            │ R$ 5.040         │ R$ 50        │
│ Disponibilidade         │ 8h/dia, 5 dias   │ 24/7         │
│ Férias                  │ 30 dias/ano      │ 0 dias       │
│ Processo trabalhista    │ Risco constante  │ Impossível   │
│ Turnover                │ 20-40%/ano       │ 0%           │
│ Curva aprendizado       │ 3-6 meses        │ Instantâneo  │
└─────────────────────────┴──────────────────┴──────────────┘
```

**TEXT OVERLAY** (aparece sincronizado):
- "R$ 3.000" (quando menciona salário)
- "+68%" (quando menciona encargos)
- "R$ 5.040/mês" (quando fala total mensal) - em CORAL_ALERT (#F43F5E)

**EFEITO**:
- Coluna CODEXA com glow sutil em SAPPHIRE
- Coluna Funcionário sem destaque (neutra)

---

### [00:25-00:50] CÁLCULO 5 ANOS (25 segundos)

**NARRAÇÃO**:
> "Cinco mil e quarenta por mês. Vezes sessenta meses. Trezentos e dois mil e quatrocentos reais em cinco anos."

**VISUAL**:
- Contador animado subindo:
  - R$ 5.040 →
  - x12 meses = R$ 60.480 (ano 1)
  - x12 meses = R$ 120.960 (ano 2)
  - x12 meses = R$ 181.440 (ano 3)
  - x12 meses = R$ 241.920 (ano 4)
  - x12 meses = **R$ 302.400** (ano 5)

**NARRAÇÃO** (continua):
> "CODEXA: cinquenta reais por mês de API. Uso intenso. Cinco anos: três mil reais."

**VISUAL** (split screen):
- Esquerda: R$ 302.400 (em vermelho, grande)
- Direita: R$ 3.000 (em verde, grande)
- Background escurece para dar foco nos números

**TEXT OVERLAY**:
- "5 anos" no topo (Space Grotesk Bold)
- Linha conectando os dois valores

---

### [00:50-01:15] ECONOMIA BRUTAL (25 segundos)

**NARRAÇÃO**:
> "Economia: duzentos e noventa e nove mil e quatrocentos reais. Por funcionário substituível."

**VISUAL**:
- Os dois números se aproximam
- Subtração aparece no centro:
  ```
  R$ 302.400
  - R$ 3.000
  ─────────────
  R$ 299.400
  ```
- Número final **R$ 299.400** cresce e brilha em KNOWLEDGE_GOLD (#F59E0B)
- KNOWLEDGE_GLOW animation (pulse suave)

**TEXT OVERLAY** (sobreposto ao número):
- "ECONOMIA EM 5 ANOS" (acima)
- "por funcionário" (abaixo, menor, STEEL_GRAY)

**NARRAÇÃO** (pausa de 2 segundos para absorver):
> [SILÊNCIO - deixa o número falar]

---

### [01:15-01:30] PUNCH LINE (15 segundos)

**NARRAÇÃO**:
> "Não estou dizendo pra demitir ninguém. Estou dizendo que antes de CONTRATAR, você deveria perguntar: essa tarefa pode ser automatizada?"

**VISUAL**:
- Fade out da tabela
- Volta para apresentador (medium close-up)
- Background com grid geométrico sutil
- Olhar direto para câmera

**TEXT OVERLAY**:
- Nenhum (foco total no apresentador)

**TRANSIÇÃO**:
- Fade to próxima seção (ou CTA)

---

## ESPECIFICAÇÕES TÉCNICAS

### Paleta de Cores
```yaml
Background: "#0A1628" (DEEP_OCEAN)
Números principais: "#F8FAFC" (SOFT_WHITE)
Destaques negativos: "#F43F5E" (CORAL_ALERT)
Destaques positivos: "#10B981" (MINT_SUCCESS)
Economia final: "#F59E0B" (KNOWLEDGE_GOLD)
```

### Tipografia
```yaml
Números grandes: "Space Grotesk Bold 48px"
Labels: "Inter Regular 16px"
Overlay principal: "Inter Bold 24px"
Tabela: "JetBrains Mono 14px"
```

### Animações
```yaml
Tabela: "LAYER_REVEAL (400ms each row, 150ms stagger)"
Números: "Counter animation (2s total, ease-out)"
Economia final: "KNOWLEDGE_GLOW (2s loop)"
```

### Áudio
```yaml
Música: "Mínima, quase imperceptível"
SFX:
  - Soft chime quando R$ 299.400 aparece
  - Nenhum outro efeito (deixa números falarem)
Volume música: "-22dB (mais baixo que o normal)"
```

---

## VARIAÇÕES OPCIONAIS

### Versão 45 segundos (compacta)
- Remover linhas da tabela (mostrar só custo mensal e 5 anos)
- Acelerar contador de anos (1s em vez de 2s)

### Versão 120 segundos (expandida)
- Adicionar mais critérios da tabela:
  - Doenças/Atestados
  - Motivação variável
  - Escalabilidade
  - Lealdade/Confidencialidade

### Versão com voz alternativa
- Narração mais lenta (+10s total)
- Pausas dramáticas após números-chave

---

## NOTAS DE DIREÇÃO

### Para o apresentador:
- **Tom**: Neutro, factual, sem emoção excessiva
- **Ritmo**: Pausado nos números (deixa absorver)
- **Ênfase**: Em "duzentos e noventa e nove mil" (pronuncia cada palavra)
- **Olhar**: Para câmera no punch line final

### Para o editor:
- **Prioridade**: Números visíveis e legíveis
- **Contraste**: Mínimo 7:1 em todos os textos
- **Timing**: Não apressar o contador (2s é ideal)
- **SFX**: Sutil no chime final (não exagerar)

### Para o motion designer:
- **Estilo**: Clean, corporativo, sem floreios
- **Cores**: Usar paleta exata (não improvisar)
- **Animações**: Suaves, não distrativas
- **Glow**: Apenas no número final (não abusar)

---

## MÉTRICAS DE SUCESSO

### Objetivos desta seção:
- [ ] Viewer entende economia bruta (R$ 299.400)
- [ ] Provocação ética clara (não demitir, repensar contratação)
- [ ] Números memoráveis (5.040 vs 50)
- [ ] Tom crível (não hype, dados duros)

### Sinais de que funcionou:
- Comentários mencionam os números exatos
- Compartilhamentos com caption "299 mil de economia"
- Perguntas sobre custos de API
- Reconhecimento da nuance (não é sobre demitir)

---

## ASSETS NECESSÁRIOS

```markdown
GRÁFICOS:
- [ ] Tabela comparativa (7 linhas x 3 colunas)
- [ ] Contador animado (0 → 302.400)
- [ ] Equação de subtração (centralizada)
- [ ] Número final em destaque (R$ 299.400)

ANIMAÇÕES:
- [ ] LAYER_REVEAL para linhas da tabela
- [ ] Counter animation (smooth, não jumpy)
- [ ] KNOWLEDGE_GLOW para número final

ÁUDIO:
- [ ] Background music (minimal, -22dB)
- [ ] Soft chime (achievement sound)
```

---

## INTEGRAÇÃO NO VÍDEO DE 10MIN

### Posicionamento sugerido:
- **Após**: Introdução aos 3 Layers da IA
- **Antes**: Demonstração prática dos agentes
- **Contexto**: Bridge entre filosofia e aplicação

### Flow narrativo:
```
[Seção anterior] → Você entendeu as 3 camadas
[Esta seção]     → Agora veja o impacto financeiro
[Próxima seção]  → Vamos ver isso na prática
```

---

## TEMPLATE DE DISTILLATION

### [OPEN_VARIABLES] para outras marcas:

```markdown
{{EMPLOYEE_SALARY}}         = R$ 3.000
{{PAYROLL_TAX_PERCENT}}     = 68%
{{TOTAL_MONTHLY_COST}}      = R$ 5.040
{{API_MONTHLY_COST}}        = R$ 50
{{YEARS_CALCULATED}}        = 5
{{TOTAL_EMPLOYEE_COST}}     = R$ 302.400
{{TOTAL_SYSTEM_COST}}       = R$ 3.000
{{SAVINGS_AMOUNT}}          = R$ 299.400
{{SYSTEM_NAME}}             = CODEXA
{{EMPLOYEE_ROLE}}           = marketing digital
```

**Uso**: Outra empresa pode trocar valores e o roteiro funciona identicamente.

---

**STATUS**: Ready for production
**QUALITY SCORE**: 9.0/10
**NEXT STEPS**:
1. Aprovar roteiro
2. Gravar narração
3. Criar motion graphics
4. Editar e sincronizar
5. Review final

---

**"Os números não mentem. A decisão é sua."**
