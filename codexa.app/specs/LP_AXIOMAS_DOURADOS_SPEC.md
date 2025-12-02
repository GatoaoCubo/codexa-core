# SPEC: Axiomas Dourados - Easter Eggs de Alta Entropia

> **Conceito**: Versículos axiomáticos que condensam sabedoria fundamental em formato denso.
> **Inspiração**: Estrutura bíblica + Dense Keywords Information (LLMs)
> **Foco**: Engajamento através de descoberta e revelação progressiva.

---

## FILOSOFIA

### Por que Axiomas?

```
AXIOMA = Verdade fundamental que não precisa de prova
ENTROPIA = Densidade informacional por caractere
VERSÍCULO = Unidade mínima de sabedoria completa
```

**Princípio**: Cada axioma deve ser:
1. **Auto-contido** - Faz sentido isoladamente
2. **Denso** - Máxima informação em mínimas palavras
3. **Atemporal** - Verdade que não expira
4. **Acionável** - Gera insight ou ação

---

## ESTRUTURA C.O.D.E.X.A

Cada letra do CODEXA revela um **Livro de Axiomas**:

| Letra | Livro | Tema | Axiomas |
|-------|-------|------|---------|
| **C** | Cognição | Inteligência & Decisão | 2 |
| **O** | Orquestração | Sistemas & Coordenação | 2 |
| **D** | Descoberta | Pesquisa & Análise | 2 |
| **E** | Emergência | Valor & Crescimento | 2 |
| **X** | Variável | O Elemento Humano | 2 |
| **A** | Autonomia | Ação & Execução | 2 |

**Total**: 12 Axiomas Dourados

---

## OS 12 AXIOMAS DOURADOS

> **Formato**: Máximo 6 palavras. SEO da alma. Alta entropia.

### LIVRO C - COGNIÇÃO

| Código | Axioma | Chars |
|--------|--------|-------|
| **C:1** | *Entenda antes. Erre menos.* | 23 |
| **C:2** | *Dado ignorado vira concorrente.* | 28 |

### LIVRO O - ORQUESTRAÇÃO

| Código | Axioma | Chars |
|--------|--------|-------|
| **O:1** | *Maestro não toca. Orquestra.* | 26 |
| **O:2** | *Simples funciona. Complexo aparenta.* | 32 |

### LIVRO D - DESCOBERTA

| Código | Axioma | Chars |
|--------|--------|-------|
| **D:1** | *Pesquisa reduz todo custo.* | 24 |
| **D:2** | *Oportunidade: dado não buscado.* | 28 |

### LIVRO E - EMERGÊNCIA

| Código | Axioma | Chars |
|--------|--------|-------|
| **E:1** | *Todo emerge. Soma não.* | 20 |
| **E:2** | *Conhecimento compõe. Nunca expira.* | 30 |

### LIVRO X - VARIÁVEL (O HUMANO)

| Código | Axioma | Chars |
|--------|--------|-------|
| **X:1** | *Melhor IA: a sua.* | 17 |
| **X:2** | *Segredo: quem alimenta.* | 21 |

### LIVRO A - AUTONOMIA

| Código | Axioma | Chars |
|--------|--------|-------|
| **A:1** | *Propósito + autonomia = ação.* | 26 |
| **A:2** | *Constrói ativos. Não aluga.* | 24 |

---

### RESUMO VISUAL (para LP)

```
C:1  Entenda antes. Erre menos.
C:2  Dado ignorado vira concorrente.
O:1  Maestro não toca. Orquestra.
O:2  Simples funciona. Complexo aparenta.
D:1  Pesquisa reduz todo custo.
D:2  Oportunidade: dado não buscado.
E:1  Todo emerge. Soma não.
E:2  Conhecimento compõe. Nunca expira.
X:1  Melhor IA: a sua.
X:2  Segredo: quem alimenta.
A:1  Propósito + autonomia = ação.
A:2  Constrói ativos. Não aluga.
```

**Média**: 24 caracteres por axioma
**Máximo**: 32 caracteres (O:2)
**Mínimo**: 17 caracteres (X:1)

---

## IMPLEMENTAÇÃO NA LP

### 1. Easter Egg Principal: Logo CODEXA Interativo

```
Localização: Navbar
Comportamento: Hover em cada letra revela axioma
Visual: Tooltip dourado com borda amber animada
```

**Interação**:
```
[Hover na letra C] → Tooltip: "C:1 — Quem entende antes de agir..."
[Click] → Expande para versão completa + ícone de copiar
```

### 2. Easter Eggs nos Agentes (Axioms existentes)

```
Atual: "Dados viram decisões" (estático)
Novo: Hover revela axioma completo D:1
```

**Visual**:
```css
.axiom-gold {
  color: amber-500;
  cursor: help;
  border-bottom: 1px dashed amber-500/50;
}

.axiom-gold:hover::after {
  content: attr(data-full-axiom);
  /* tooltip dourado */
}
```

### 3. Easter Egg de Coleta

```
Mecânica: Usuário que descobrir 6+ axiomas
Recompensa: Badge "Sábio" + desconto especial?
Tracking: localStorage + analytics event
```

### 4. Footer Oculto

```
Localização: Triplo-click no copyright
Revela: Lista completa dos 12 axiomas
Visual: Modal dourado estilo "pergaminho"
```

---

## COMPONENTES REACT

### AxiomTooltip Component

```tsx
interface AxiomProps {
  code: string;      // "C:1", "D:2", etc.
  short: string;     // Versão curta (já existente)
  full: string;      // Axioma completo
  entropy: number;   // Score 0-1
}

const AxiomTooltip = ({ code, short, full, entropy }: AxiomProps) => (
  <span
    className="axiom-gold cursor-help"
    title={`${code} — ${full}`}
  >
    {short}
    <span className="axiom-indicator">✦</span>
  </span>
);
```

### AxiomReveal Component (Logo interativo)

```tsx
const CODEXA_AXIOMS = {
  C: { short: "Cognição", axiom: "C:1", full: "Quem entende antes de agir..." },
  O: { short: "Orquestração", axiom: "O:1", full: "Um maestro não toca..." },
  // ...
};

const CodexaLogo = () => {
  const [revealedLetter, setRevealedLetter] = useState<string | null>(null);

  return (
    <div className="flex">
      {Object.entries(CODEXA_AXIOMS).map(([letter, data]) => (
        <span
          key={letter}
          onMouseEnter={() => setRevealedLetter(letter)}
          onMouseLeave={() => setRevealedLetter(null)}
          className="axiom-letter"
        >
          {letter}
          {revealedLetter === letter && (
            <AxiomTooltip {...data} />
          )}
        </span>
      ))}
    </div>
  );
};
```

---

## ANALYTICS & GAMIFICAÇÃO

### Eventos a Trackear

```js
// Google Analytics / Plausible
trackEvent('axiom_discovered', { code: 'C:1', method: 'hover' });
trackEvent('axiom_copied', { code: 'D:2' });
trackEvent('all_axioms_found', { count: 12, time_to_complete: 'PT5M' });
```

### Recompensas (Futuro)

| Axiomas Descobertos | Recompensa |
|---------------------|------------|
| 3 | Badge "Curioso" |
| 6 | Badge "Explorador" + 5% desconto |
| 12 | Badge "Sábio" + 10% desconto + Easter egg secreto |

---

## VISUAL DESIGN

### Paleta Dourada

```css
--axiom-gold: #FFAA00;
--axiom-gold-light: #FFD54F;
--axiom-gold-dark: #FF8F00;
--axiom-glow: 0 0 20px rgba(255, 170, 0, 0.3);
```

### Animações

```css
@keyframes axiom-reveal {
  0% { opacity: 0; transform: translateY(-10px); }
  100% { opacity: 1; transform: translateY(0); }
}

@keyframes axiom-glow {
  0%, 100% { box-shadow: var(--axiom-glow); }
  50% { box-shadow: 0 0 30px rgba(255, 170, 0, 0.5); }
}
```

### Tipografia

```css
.axiom-text {
  font-family: 'Crimson Text', Georgia, serif; /* Estilo bíblico */
  font-style: italic;
  letter-spacing: 0.02em;
}

.axiom-code {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75em;
  color: var(--axiom-gold-dark);
}
```

---

## ROADMAP DE IMPLEMENTAÇÃO

### Fase 1: Fundação (Esta sessão)
- [ ] Criar constante AXIOMS com os 12 axiomas
- [ ] Implementar AxiomTooltip básico
- [ ] Aplicar nos axioms existentes dos agentes

### Fase 2: Logo Interativo
- [ ] Refatorar logo CODEXA para interativo
- [ ] Cada letra revela axioma no hover
- [ ] Animação de revelação

### Fase 3: Gamificação
- [ ] Tracking de axiomas descobertos
- [ ] Sistema de badges
- [ ] Easter egg do footer

### Fase 4: Otimização
- [ ] A/B test de conversão
- [ ] Ajustar baseado em heatmaps
- [ ] Integrar com CRM para descontos

---

## MÉTRICAS DE SUCESSO

| Métrica | Target |
|---------|--------|
| Hover rate nos axiomas | > 15% dos visitantes |
| Axiomas descobertos/sessão | > 3 em média |
| Tempo na página | +30% vs baseline |
| Conversão (quem descobriu 6+) | +20% vs quem não descobriu |

---

**Versão**: 1.0.0
**Criado**: 2025-12-01
**Status**: SPEC PRONTA PARA IMPLEMENTAÇÃO
