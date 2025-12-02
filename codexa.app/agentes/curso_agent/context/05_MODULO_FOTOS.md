# 🟡 MÓDULO 5: Fotos com IA

**Duração**: 1-2 horas
**Nível**: Intermediário
**Comando**: `/prime-photo`

**🎮 XP Disponível:** 40 XP total
- Complete módulo: +25 XP
- Execute `/prime-photo`: +10 XP
- Crie 9-grid completo: +5 XP

**🏆 Achievements Disponíveis:**
- 📸 **"Visual Storyteller"** (Bronze) - Crie seu primeiro 9-grid
- 🎬 **"Art Director"** (Silver) - 3+ estilos fotográficos dominados

> 💡 **Sistema de Gamificação Ativo**
> Veja `00_GAMIFICATION_SYSTEM.md` para detalhes completos.

---

## 🎯 OBJETIVOS

- ✅ Gerar fotos profissionais com IA
- ✅ Criar múltiplos ângulos e estilos
- ✅ Otimizar para marketplaces
- ✅ Manter consistência de marca
- ✅ Usar técnicas avançadas de prompt

---

## 📖 CONTEÚDO

### 1. O Photo Agent

**Arquitetura Dual-Layer:**
- ADW (workflow 5 fases)
- HOP (5 prompts modulares)

**Capacidades:**
- 9 cenas em grid 3x3
- 12 perfis de câmera
- 7 estilos fotográficos
- Compliance de marketplace

**Ative:**
```
/prime-photo
```

---

### 2. Requisitos de Marketplace

**Mercado Livre:**
- Mín: 1200x1200px
- Fundo: Branco preferencial
- 85% do espaço preenchido

**Amazon BR:**
- Mín: 1000x1000px
- Recomendado: 2000x2000px
- Imagem principal: fundo branco

**Shopee:**
- Mín: 800x800px
- Múltiplos ângulos valorizados
- Lifestyle photos convertem mais

---

### 3. Workflow de Criação

**PASSO 1: Planeje as cenas**
```
Grid 3x3:
1. Hero shot (fundo branco)
2. Detalhe do material
3. Vista superior
4. Uso em ambiente
5. Comparação de tamanho
6. Embalagem
7. Lifestyle outdoor
8. Detalhe da tampa
9. Infográfico de features
```

**PASSO 2: Escolha estilo**
- Minimalist (clean, moderno)
- Dramatic (luz/sombra forte)
- Lifestyle (contexto real)
- Commercial (profissional)

**PASSO 3: Execute**
```
/prime-photo

"Crie 9 fotos de garrafa térmica eco-friendly,
estilo minimalist-commercial, incluindo:
- Hero shot fundo branco
- Lifestyle outdoor
- Detalhes de materiais"
```

---

### 4. Técnicas de Prompt

**Estrutura básica:**
```
[Tipo de foto] de [produto],
[estilo], [iluminação],
[ângulo], [contexto],
shot on [câmera]
```

**Exemplo:**
```
Product photography of eco-friendly water bottle,
minimalist commercial style, soft natural lighting,
45-degree angle, outdoor hiking context,
shot on Canon EOS R5
```

**Parâmetros técnicos:**
- ISO: 100-400 (cleanness)
- Aperture: f/2.8-f/8 (depth)
- Shutter: 1/125-1/250 (sharpness)
- Lens: 50mm, 85mm (product)

---

### 5. 7 Estilos Fotográficos

**1. Minimalist**
- Fundo limpo
- Cores neutras
- Foco no produto

**2. Dramatic**
- Contraste alto
- Sombras marcadas
- Visual impactante

**3. Lifestyle**
- Contexto real
- Pessoas usando
- Emoção

**4. Editorial**
- Composição artística
- Storytelling visual
- Alta qualidade

**5. Commercial**
- Profissional
- Direto ao ponto
- Confiável

**6. Cinematic**
- Mood dramático
- Cores gradientes
- Atmosfera

**7. Vintage**
- Filtros retrô
- Nostalgia
- Autêntico

---

### 6. Brand Alignment

**Consistência visual:**

```
Marca: EcoFlow (sustentável)
Estilo: Minimalist + Lifestyle
Cores: Verde, azul, branco
Contexto: Natureza, outdoor
Evitar: Plástico, poluição, urbano excessivo
```

**Validação:**
O Photo Agent valida automaticamente:
- Brand guidelines
- Paleta de cores
- Estilo consistente

---

### 7. Otimização para Conversão

**A/B Testing de imagens:**

**Versão A: Hero shot**
- Fundo branco
- Produto centralizado
- Baseline

**Versão B: Lifestyle**
- Contexto de uso
- Emoção
- Teste vs A

**Métricas:**
- CTR (Click-Through Rate)
- Conversion rate
- Time on page

---

### 8. Infográficos e Composições

**Imagem com texto:**
```
- Feature highlights
- Especificações técnicas
- Comparação antes/depois
- USPs visuais
```

**Ferramentas:**
- Canva (templates prontos)
- Figma (customização)
- PhotoRoom (remoção de fundo)

---

### 9. Exercícios

**Exercício 1: 9-Grid**
1. Escolha um produto
2. Execute `/prime-photo`
3. Solicite grid 3x3
4. Analise composição

**Exercício 2: Estilos**
1. Mesmo produto
2. Gere em 3 estilos diferentes
3. Compare resultados
4. Escolha melhor para seu público

**Exercício 3: Brand Consistency**
1. Use brand guidelines do Módulo 4
2. Gere fotos alinhadas
3. Valide consistência
4. Ajuste se necessário

---

## ⚙️ POR TRÁS DA CORTINA: Como o Photo Agent Funciona

**Photo Agent não é "gerador de imagens". É sistema de asset production.**

Ele combina **dois frameworks** - ADW (workflow) + HOP (prompts modulares) - para produção em escala.

**Os 4 Núcleos em Ação:**

1. **CONTEXT** (Ponto 12)
   - 12 perfis de câmera (Canon, Sony, Fuji, etc) com specs reais
   - 7 estilos fotográficos (Minimalist, Dramatic, Lifestyle, etc)
   - Requisitos de 9 marketplaces BR (resolução, aspect ratio, compliance)
   - Brand alignment rules (herda de Marca Agent automaticamente)
   - Biblioteca de composições testadas (grid 3x3, hero shots, lifestyle)

2. **MODEL** (Ponto 11)
   - Modo criativo para composição artística
   - Modo técnico para specs de marketplace
   - Extended reasoning para séries complexas (9-grid)

3. **PROMPT** (Ponto 10)
   - **ADW**: 5 fases (Plan→Generate→Validate→Refine→Deliver)
   - **HOP**: 5 prompts modulares reutilizáveis
   - Cada cena tem seu próprio prompt otimizado
   - Quality gates: resolução, marca, marketplace compliance

4. **TOOLS** (Ponto 9)
   - Image generation (API Google Imagen)
   - Resolution validator
   - Brand consistency checker
   - Marketplace compliance validator
   - Batch processor (9 images em paralelo)

**Arquitetura Dual-Layer: ADW + HOP**

**ADW** (AI Developer Workflow) = O QUE fazer
- 5 fases sequenciais
- Orquestra todo o processo
- Quality gates entre fases

**HOP** (Higher Order Prompts) = COMO fazer
- 5 prompts modulares
- Composable (mix and match)
- Reusáveis em outros projetos

**Por que 2 camadas?** Separação de responsabilidades:
- ADW = Lógica de negócio (quando gerar, validar, entregar)
- HOP = Lógica técnica (como construir cada prompt)

**O Princípio: PLANS (Ponto 3)**

Photo Agent não gera "1 foto". Ele executa um **PLAN** (plano de produção):
- 9 cenas definidas estrategicamente
- Ordem de geração otimizada
- Validação automática de cada output
- Refinamento se necessário

**Composable com Outros Agents:**

```
Marca Agent → define paleta, tom, estilo
         ↓
Photo Agent → herda automaticamente
         ↓
Anuncio Agent → usa fotos geradas
```

Isso é **$arguments-chaining** - output de um agent vira input de outro.

> 📘 **Axioma: Composable Agentic Primitives**
>
> _"Primitivas agentivas são blocos de construção pequenos e componíveis. Qualquer workflow pode ser construído compondo essas primitivas."_
>
> **Higher Order Prompts (HOPs):**
> - Um prompt que **aceita outros prompts** como parâmetros de entrada
> - Análogo a funções de ordem superior em programação, mas para sistemas agentivos
> - Permite workflows componíveis e reutilizáveis
>
> **As 12 Primitivas Componíveis:**
> ```
> OUT-AGENT (8):              IN-AGENT (4):
> - ADWs                      - Tools
> - Templates                 - Prompt
> - Plans                     - Model
> - Architecture              - Context
> - Tests
> - Documentation
> - Types
> - Standard Out
> ```
>
> **Poder Agentivo Geral:**
> O poder não vem de prompts únicos, mas de **primitivas reusáveis** que se compõem. Photo Agent é o melhor exemplo: ADW + HOP podem ser remixados para criar qualquer tipo de asset (vídeos, carrosséis, infográficos).
>
> **Daily Action:** Construir workflows compondo primitivas, não escrevendo prompts monolíticos.

**Feedback Loop: Validate → Refine**

1. Gera imagem
2. Valida: resolução? marca? marketplace?
3. Se falhar → ajusta prompt → regenera
4. Se passar → próxima cena
5. Ao final → valida SET inteiro (consistência)

**Preview do Módulo 6:**

Photo Agent é o melhor exemplo de **composable agentic primitives**. ADW + HOP podem ser remixados para criar qualquer tipo de asset (videos, carrosséis, infográficos).

No Módulo 6, você vai aprender a construir seus próprios ADWs e HOPs.

---

## 🎉 CONCLUSÃO

Você aprendeu:
- ✅ Gerar fotos profissionais com IA
- ✅ Otimizar para marketplaces
- ✅ Usar técnicas de prompt avançadas
- ✅ Manter consistência de marca

---

## 🎮 XP SUMMARY

**XP Ganho neste módulo:**
- Completou módulo: +25 XP
- Executou `/prime-photo`: +10 XP
- 9-grid completo criado: +5 XP
**Total:** +40 XP

**Seu Status Após Módulo 5:**
- Level: **APPRENTICE** (Level 2)
- Total XP: 275/300
- Progress: █████████░ 92%
- **Próximo nível em:** 25 XP

**Achievements Desbloqueados:**
- 📸 **"Visual Storyteller"** - Primeiro 9-grid criado
- 🎬 **"Art Director"** - 3+ estilos fotográficos dominados

**⚠️ Você está a 25 XP de virar BUILDER!**

**Próximo**: Módulo 6 - Meta-Construção (+200 XP disponível + Level Up garantido!)

---

**Criado com ❤️ pelo time CODEXA**
