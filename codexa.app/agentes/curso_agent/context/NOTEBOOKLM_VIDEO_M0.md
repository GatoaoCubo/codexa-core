# NotebookLM: Video M0 - Destilação de Conhecimento

**Objetivo**: Material de referência para NotebookLM gerar vídeo de 10 minutos sobre Destilação de Conhecimento para YouTube.

---

## PARTE 1: LISTA DE ARQUIVOS PARA UPLOAD NO NOTEBOOKLM

### Arquivos Core (Upload obrigatório)

```
1. 00_MODULO_SUPER_FREEMIUM.md
   → Roteiro completo com timecodes, quick wins, axiomas

2. PRODUCAO_VIDEO_M0.md
   → Checklist de produção, assets, timeline, script teleprompter-ready

3. RESEARCH_BANCO_PALAVRAS_OTIMIZADAS.md
   → Banco de palavras validadas, hooks, triggers, terminologia técnica
```

### Arquivos de Suporte (Opcional, enriquecem contexto)

```
4. GLOSSARIO.md
   → 85+ termos técnicos validados com fontes acadêmicas

5. 00_GAMIFICATION_SYSTEM.md
   → Sistema de XP, achievements, progressão

6. ../iso_vectorstore/13_HOP_video_script.md
   → Template TAC-7 para scripts de vídeo educacional
```

### Caminhos Completos para Cópia

```
codexa.app/agentes/curso_agent/context/00_MODULO_SUPER_FREEMIUM.md
codexa.app/agentes/curso_agent/context/PRODUCAO_VIDEO_M0.md
codexa.app/agentes/curso_agent/context/RESEARCH_BANCO_PALAVRAS_OTIMIZADAS.md
codexa.app/agentes/curso_agent/context/GLOSSARIO.md
codexa.app/agentes/curso_agent/context/00_GAMIFICATION_SYSTEM.md
codexa.app/agentes/curso_agent/iso_vectorstore/13_HOP_video_script.md
```

---

## PARTE 2: PROMPT PARA NOTEBOOKLM

### Prompt Principal (Cole no NotebookLM após upload dos arquivos)

```
Você é um Video Production Specialist especializado em conteúdo educacional para e-commerce.

## TAREFA
Usando os documentos carregados como referência, ajude-me a produzir um vídeo de 10 minutos para YouTube sobre "Destilação de Conhecimento - O Novo Investimento".

## CONTEXTO DO VÍDEO
- Duração: 10 minutos
- Plataforma: YouTube (formato 16:9)
- Público: Sellers de e-commerce brasileiro que querem usar IA de forma inteligente
- Tom: Direto, prático, sem hype - como uma conversa com um amigo expert
- Objetivo: Converter viewers em assinantes do codexa.app

## ESTRUTURA DO VÍDEO (seguir roteiro em PRODUCAO_VIDEO_M0.md)

### Bloco 1: HOOK [00:00-00:30]
- Power word: "Imagine..."
- Contraste: manual vs automatizado
- Promessa: "nos próximos 10 minutos"

### Bloco 2: O QUE SÃO LLMs [00:30-02:00]
- Metáfora: Biblioteca de Alexandria
- Conceito: Compressão de conhecimento
- Pain point: "Não sabem nada sobre VOCÊ"

### Bloco 3: EVOLUÇÃO [02:00-04:00]
- 3 evoluções: Tools → Context → Agentic AI
- Metáfora: Estagiário que fala vs Estagiário que FAZ
- Termos técnicos: Function Calling, Knowledge Base, Agentic AI

### Bloco 4: OS 4 CORES [04:00-06:00]
- Framework visual: Model, Context, Prompt, Tools
- Insight: "Model é commodity, Conhecimento é diferencial"
- Conceito central: Destilação de Conhecimento

### Bloco 5: CAMADA ERRADA [06:00-07:30]
- 3 Camadas: Usuário → Automação → Meta-Construção
- Axioma: "Ativo, não aluguel"
- Dor: Camada 1 e 2 = você aluga inteligência

### Bloco 6: 3 QUICK WINS [07:30-09:30]
- QW1: Meta-Prompt (delegação)
- QW2: Plan (supervisão)
- QW3: Implement (ativos)
- Resultado: Conhecimento proprietário em 5 minutos

### Bloco 7: CTA [09:30-10:00]
- 6 agentes CODEXA
- Link na descrição
- "Nos vemos na Camada 3"

## REGRAS DE PRODUÇÃO

### SEMPRE
- Use terminologia validada do GLOSSARIO.md
- Aplique hooks do RESEARCH_BANCO_PALAVRAS_OTIMIZADAS.md
- Mantenha timing marks do roteiro
- Use exemplos do mercado brasileiro (Mercado Livre, Shopee)
- Inclua os 3 Quick Wins copy-paste ready

### NUNCA
- Usar hype words: "revolucionário", "mágico", "único no mercado"
- Prometer resultados garantidos
- Ignorar compliance (Procon, ANVISA se aplicável)
- Criar urgência fake com countdown

### GATILHOS MENTAIS PERMITIDOS
- Contraste (antes/depois)
- Autoridade (termos acadêmicos validados)
- Reciprocidade (conteúdo gratuito valioso)
- Afinidade (sellers para sellers)

## COMO ME AJUDAR

1. **Refinar roteiro**: Analise cada bloco e sugira melhorias baseado nas melhores práticas dos documentos

2. **Criar narração**: Gere texto para teleprompter que seja natural e conversacional

3. **Sugerir visuais**: Baseado no roteiro, sugira que tipo de gráfico/animação usar em cada momento

4. **Validar consistência**: Verifique se estou usando a terminologia correta e consistente

5. **Gerar variações**: Crie 3 opções de thumbnail text e 3 opções de título para A/B test

6. **Extrair citações**: Identifique as frases mais impactantes para usar como cortes/shorts

## OUTPUT ESPERADO

Para cada solicitação, forneça:
- Resposta direta e prática
- Referência ao documento fonte quando relevante
- Sugestão de melhoria se identificar oportunidade
- Validação contra os quality gates do roteiro
```

---

## PARTE 3: PROMPTS AUXILIARES

### Para Gerar Variações de Título

```
Analise o documento PRODUCAO_VIDEO_M0.md e gere 5 variações de título para o vídeo seguindo o formato [HOOK] + [PROMESSA] + [TEMPO]:

1. Foco em dor (problema do usuário)
2. Foco em ganho (resultado prometido)
3. Foco em curiosidade (segredo/revelação)
4. Foco em contraste (antes vs depois)
5. Foco em autoridade (metodologia/expertise)

Para cada título, explique qual gatilho mental está sendo ativado.
```

### Para Gerar Descrição YouTube

```
Usando os documentos como referência, gere uma descrição completa para o YouTube que inclua:

1. Hook (primeira frase que aparece no preview)
2. Lista de tópicos abordados (bullet points)
3. Timestamps corretos (alinhados com PRODUCAO_VIDEO_M0.md)
4. Os 3 Quick Wins copy-paste ready
5. Links para codexa.app
6. Hashtags relevantes para SEO
7. CTA para inscrição no canal

Formato: Descrição pronta para copiar e colar no YouTube.
```

### Para Refinar Narração

```
Analise o Bloco [X] do roteiro em PRODUCAO_VIDEO_M0.md e:

1. Reescreva para soar mais natural quando falado em voz alta
2. Adicione pausas dramáticas onde necessário [PAUSA - 2s]
3. Sugira entonação [↑ subir tom] [↓ descer tom]
4. Identifique palavras que precisam de ênfase [ÊNFASE: palavra]
5. Verifique timing (deve caber no tempo alocado)

Output: Texto teleprompter-ready com marcações de direção.
```

### Para Gerar Script de Shorts/Cortes

```
Identifique nos documentos os 5 momentos mais impactantes que funcionariam como:

1. YouTube Shorts (vertical, 60s)
2. Instagram Reels (vertical, 90s)
3. TikTok (vertical, 60s)

Para cada momento, forneça:
- Timestamp no vídeo original
- Hook de abertura (3s)
- Core message (essência)
- CTA de fechamento
- Hashtags específicas da plataforma
```

### Para Validar Qualidade

```
Revise o roteiro completo contra os quality gates:

CHECKLIST:
- [ ] Hook em ≤90 segundos?
- [ ] Objetivos com verbos Bloom nível 3-4?
- [ ] ≥2 OPEN_VARIABLES para customização?
- [ ] Timing marks a cada 2-3 minutos?
- [ ] Demonstração mostra CODEXA real?
- [ ] Exemplos do mercado brasileiro?
- [ ] Seed words presentes (Meta-Construção, Destilação)?
- [ ] Sem hype words?
- [ ] Duração 9-11 minutos?

Para cada item que falhar, sugira correção específica.
```

---

## PARTE 4: INTEGRAÇÃO COM /prime-video

### Pipeline de 5 Estágios (do video_agent)

```
Brief → [Concept] → [Script] → [Visual] → [Production] → [Editing] → Video
          ~5s         ~3s        ~10s        120-300s         ~15s
```

### Aplicação ao M0

| Estágio | Aplicação M0 | Output |
|---------|--------------|--------|
| **Concept** | Storyboard 7 blocos | Estrutura validada |
| **Script** | Narração teleprompter | 00_MODULO_SUPER_FREEMIUM.md |
| **Visual** | Assets/diagramas | PRODUCAO_VIDEO_M0.md checklist |
| **Production** | Gravação câmera + screencast | 4-day timeline |
| **Editing** | Cortes + música + text overlays | MP4 final |

### Narrative Arc (Video Agent)

```
Hook (0-30s) → Build (30s-6min) → Benefit (6-7:30) → Proof (7:30-9:30) → CTA (9:30-10:00)
```

### Style Preset Recomendado

| Parâmetro | Valor | Justificativa |
|-----------|-------|---------------|
| Style | **calm** | Conteúdo educacional, não promo |
| Camera | Slow, smooth | Transmite confiança |
| Lighting | Soft, warm | Ambiente acolhedor |
| Pacing | Slow dissolves | Tempo para absorver |
| Use Case | Educational, premium | Posicionamento CODEXA |

---

## PARTE 5: CHECKLIST PRÉ-UPLOAD

Antes de fazer upload no NotebookLM:

- [ ] Verificar se arquivos estão na versão mais recente
- [ ] Remover seções de metadata/versioning se exceder limite
- [ ] Confirmar que todos os [OPEN_VARIABLE] estão preenchidos
- [ ] Testar prompt principal em conversa de teste

### Limites NotebookLM

- Máximo 50 fontes por notebook
- ~500.000 palavras por fonte
- Formatos aceitos: .txt, .pdf, .md, Google Docs

---

**Versão**: 1.0.0
**Criado**: 2025-11-29
**Autor**: Curso Agent
**Uso**: Upload no NotebookLM → Cole prompt → Itere sobre outputs
