# NotebookLM: Video LP - CODEXA Roteador

**Objetivo**: Material para NotebookLM gerar vídeo de 11 minutos sobre o Roteador CODEXA para Landing Page.

---

## TRINITY STRUCTURE

This file is part of a 3-file production system:

```
VIDEO_LP_ROTEADOR.md               → Script (what to say)
DIRECAO_VISUAL_LP_ROTEADOR.md      → Visual Direction (how it looks)
NOTEBOOKLM_VIDEO_LP_ROTEADOR.md    → NotebookLM Prompt (how to generate)
                                     ↑ YOU ARE HERE
```

**Separation of Concerns**:
- **Script**: Timecodes, narration, messaging, copy
- **Visual Direction**: Camera movements, lighting, mood, transitions
- **NotebookLM Prompt**: Instructions for AI to consume both files and generate production guidance

**Why separate?**
1. **Clarity**: Each file has one job
2. **Reusability**: Script can be read standalone, visuals can be referenced independently
3. **Iteration**: Update narration without touching camera specs, or vice versa

**Usage**: Upload script + visual direction + context files to NotebookLM. Use prompt below to iterate.

---

## PARTE 1: ARQUIVOS PARA UPLOAD NO NOTEBOOKLM

### Arquivos Core (Upload obrigatório)

```
1. VIDEO_LP_ROTEADOR.md
   → Script completo com timecodes, narração, gatilhos

2. DIRECAO_VISUAL_LP_ROTEADOR.md
   → Direção visual: câmera, iluminação, movimento, mood

3. RESEARCH_BANCO_PALAVRAS_OTIMIZADAS.md
   → Hooks, triggers, terminologia validada

4. GLOSSARIO.md
   → Termos técnicos (agente, pipeline, orquestração)
```

### Arquivos de Suporte (Enriquecem contexto)

```
5. ../anuncio_agent/PRIME.md
   → O que o anuncio_agent faz

6. ../pesquisa_agent/PRIME.md
   → O que o pesquisa_agent faz

7. ../photo_agent/PRIME.md
   → O que o photo_agent faz
```

### Caminhos para Cópia

```
codexa.app/agentes/curso_agent/context/VIDEO_LP_ROTEADOR.md
codexa.app/agentes/curso_agent/context/DIRECAO_VISUAL_LP_ROTEADOR.md
codexa.app/agentes/curso_agent/context/RESEARCH_BANCO_PALAVRAS_OTIMIZADAS.md
codexa.app/agentes/curso_agent/context/GLOSSARIO.md
codexa.app/agentes/anuncio_agent/PRIME.md
codexa.app/agentes/pesquisa_agent/PRIME.md
codexa.app/agentes/photo_agent/PRIME.md
```

---

## PARTE 2: PROMPT PRINCIPAL NOTEBOOKLM

```
Você é um Video Production Specialist especializado em vídeos de conversão para SaaS.

## TAREFA
Usando os documentos carregados (especialmente VIDEO_LP_ROTEADOR.md e DIRECAO_VISUAL_LP_ROTEADOR.md), ajude-me a produzir um vídeo de 11 minutos para a landing page do codexa.app sobre o Roteador em Linguagem Natural.

## CONTEXTO
- Duração: 11 minutos
- Plataforma: Landing page (embed) + YouTube
- Público: Sellers e-commerce BR que usam IA de forma fragmentada
- Tom: Direto, prático, com humor sutil (Cat Coding)
- Objetivo: Converter visitante em usuário (codexa.app)

## INPUTS PRIMÁRIOS
1. **VIDEO_LP_ROTEADOR.md**: Script completo com narração, timecodes, mensagens-chave
2. **DIRECAO_VISUAL_LP_ROTEADOR.md**: Especificações de câmera, iluminação, movimento, mood

## ESTRUTURA DO VÍDEO

### Bloco 1: HOOK [00:00-00:40]
- Mostrar resultado PRIMEIRO
- "Quero pesquisar e anunciar fone bluetooth" → Output pronto
- Contraste: 1 frase vs 50 minutos automático

### Bloco 2: PROBLEMA [00:45-02:30]
- Ferramentas fragmentadas (8 abas abertas)
- "Escravidão digital com mais passos"
- Dor: copiar/colar entre ferramentas

### Bloco 3: SOLUÇÃO [02:30-04:30]
- 4 comandos em português natural
- "Quero pesquisar [produto]"
- "Quero anunciar [produto]"
- "Quero pesquisar e anunciar [produto]"
- "Quero foto de [produto]"

### Bloco 4: DEMO [04:30-07:00]
- Pipeline real: Roteador → Pesquisa → Bridge → Anúncio → Entrega
- Mostrar 5 fases executando
- Score 0.87 no final

### Bloco 5: ESPECIALISTAS [07:00-08:30]
- Conhecimento destilado (cursos, mentorias, experiência)
- 3 agentes: pesquisa, anúncio, foto
- "Conversam entre si" (pipeline)

### Bloco 6: DIFERENCIAL [08:30-10:00]
- Dor de RH: "Humanos erram, curva longa, cada erro custa $$"
- Solução: "Qualquer pessoa, sem treinamento, pronto pra produção"
- Humor: "Cat Coding" (Pirulita)
- "Você orquestra. Sistema executa."

### Bloco 7: CTA [10:00-11:00]
- 4 comandos recap
- codexa.app
- "Teste grátis. 
- Tagline: "Um agente para todos governar, e com autonomia, executá-los."

## REGRAS

### SEMPRE
- Usar terminologia do GLOSSARIO.md
- Manter timing marks
- Exemplos brasileiros (ML, Shopee)
- Mencionar Cat Coding + Pirulita no diferencial

### NUNCA
- Hype words: "revolucionário", "mágico"
- Promessas garantidas
- Urgência fake

### GATILHOS PERMITIDOS
- Contraste (2h vs 47min)
- Prova real (score 0.87)
- Humor (Cat Coding)
- Escala sem risco (família/equipe)

## OUTPUT ESPERADO
Para cada solicitação:
- Resposta prática
- Referência ao documento fonte
- Validação contra quality gates
```

---

## PARTE 3: DIREÇÃO VISUAL POR SEÇÃO

### [00:00-00:40] HOOK - Resultado Primeiro

| Tempo | Visual | Câmera | Iluminação |
|-------|--------|--------|------------|
| 0:00-0:05 | Tela preta, cursor piscando | `static, eye level` | `low key, dark` |
| 0:05-0:10 | Texto aparece letra por letra | `static` | `spotlight on text` |
| 0:10-0:20 | Split screen: input → output | `static, clean composition` | `soft, neutral` |
| 0:20-0:30 | Output completo com checkmarks | `slow zoom in` | `warm, success green` |
| 0:30-0:40 | Contador "47min / 1 frase" | `static` | `high contrast` |

**Movimento Principal**: `slow zoom in` no output
**Mood**: Impacto, prova imediata

---

### [00:45-02:30] PROBLEMA - Ferramentas Fragmentadas

| Tempo | Visual | Câmera | Iluminação |
|-------|--------|--------|------------|
| 0:45-1:00 | 8 abas de navegador | `slow pan right` | `harsh, cold blue` |
| 1:00-1:20 | Ícones girando caóticos | `handheld, slight shake` | `flickering` |
| 1:20-1:40 | Pessoa copiando/colando | `medium shot` | `desaturated` |
| 1:40-2:00 | Relógio acelerando | `zoom out` | `red warning tint` |
| 2:00-2:20 | Texto "escravidão digital" | `static` | `dark, dramatic` |
| 2:20-2:30 | Fade to black, pausa | `static` | `fade to dark` |

**Movimento Principal**: `slow pan` + `handheld shake`
**Mood**: Frustração, caos, dor

---

### [02:30-04:30] SOLUÇÃO - 4 Comandos

| Tempo | Visual | Câmera | Iluminação |
|-------|--------|--------|------------|
| 2:30-2:45 | Interface limpa CODEXA | `slow dolly in` | `clean, bright` |
| 2:45-3:00 | Card 1: Pesquisa | `static` | `soft highlight` |
| 3:00-3:15 | Card 2: Anúncio | `static` | `soft highlight` |
| 3:15-3:30 | Card 3: Combo | `static` | `golden glow` |
| 3:30-3:45 | Card 4: Foto | `static` | `soft highlight` |
| 3:45-4:00 | Cursor digitando | `close-up` | `warm, inviting` |
| 4:00-4:30 | 4 cards lado a lado | `slow zoom out` | `balanced, clean` |

**Movimento Principal**: `slow dolly in` → `zoom out`
**Mood**: Clareza, simplicidade, alívio

---

### [04:30-07:00] DEMO - Pipeline Real

| Tempo | Visual | Câmera | Iluminação |
|-------|--------|--------|------------|
| 4:30-4:45 | Tela gravação real | `static, screencast` | `neutral` |
| 4:45-5:00 | Input digitado | `close-up on text` | `soft focus` |
| 5:00-5:20 | Fase 1: Roteador | `static` | `blue accent` |
| 5:20-5:40 | Fase 2: Pesquisa | `slow pan down list` | `green progress` |
| 5:40-6:00 | Fase 3: Bridge (seta) | `zoom on arrow` | `pulse effect` |
| 6:00-6:20 | Fase 4: Anúncio | `slow pan down checklist` | `green progress` |
| 6:20-6:40 | Fase 5: Entrega | `zoom in on files` | `success glow` |
| 6:40-7:00 | Score 0.87 grande | `slow zoom in` | `golden, celebration` |

**Movimento Principal**: `slow pan` em listas + `zoom` em resultados
**Mood**: Transparência, progresso, satisfação

---

### [07:00-08:30] ESPECIALISTAS - Conhecimento Destilado

| Tempo | Visual | Câmera | Iluminação |
|-------|--------|--------|------------|
| 7:00-7:15 | Diagrama orbital | `slow orbit` | `soft, warm` |
| 7:15-7:30 | Ícones: cursos, mentorias | `pan across icons` | `subtle glow each` |
| 7:30-7:45 | Funil destilação → agentes | `slow dolly in` | `gradient warm` |
| 7:45-8:00 | 3 cards agentes | `static, reveal one by one` | `accent color each` |
| 8:00-8:15 | Setas conectando | `slow pan following arrows` | `pulse on connection` |
| 8:15-8:30 | "Você no centro" | `slow zoom out` | `spotlight center` |

**Movimento Principal**: `orbit` + `dolly in`
**Mood**: Expertise, integração, poder

---

### [08:30-10:00] DIFERENCIAL - Escale Sem Risco

| Tempo | Visual | Câmera | Iluminação |
|-------|--------|--------|------------|
| 8:30-8:45 | Pessoa treinando funcionário | `medium shot, handheld` | `harsh, stressful` |
| 8:45-9:00 | Notificação reclamação + $ | `close-up` | `red warning` |
| 9:00-9:15 | Ciclo vicioso (diagrama) | `slow orbit` | `desaturated` |
| 9:15-9:30 | "CODEXA quebra ciclo" | `static, text` | `transition to warm` |
| 9:30-9:45 | Família/equipe usando | `wide shot, warm` | `golden, happy` |
| 9:45-10:00 | Score verde + gato 🐱 | `static` | `playful, warm` |

**Momento Cat Coding** (9:50-10:00):
```
[VISUAL: Você relaxado, gato no colo]
Câmera: medium shot, slight handheld (casual)
Iluminação: warm, cozy, home office vibe
Texto overlay: "CAT CODING 😼"
Música: drop para algo mais leve/divertido
```

**Movimento Principal**: `handheld` stress → `static` calm
**Mood**: Dor → Alívio → Humor

---

### [10:00-11:00] CTA - Comece Agora

| Tempo | Visual | Câmera | Iluminação |
|-------|--------|--------|------------|
| 10:00-10:15 | 4 comandos recap | `static` | `clean, bright` |
| 10:15-10:30 | Botão pulsando | `slow zoom in` | `CTA green glow` |
| 10:30-10:45 | "Teste grátis" texto | `static` | `trust blue` |
| 10:45-10:55 | Fade to black | `fade` | `dim to dark` |
| 10:55-11:00 | Logo + Tagline | `static` | `subtle golden rim` |

**Tagline Final**:
```
CODEXA.
Um agente para todos governar,
e com autonomia, executá-los.
```

**Movimento Principal**: `slow zoom in` no CTA
**Mood**: Confiança, ação, fechamento épico

---

## PARTE 4: STYLE PRESET

| Parâmetro | Valor | Justificativa |
|-----------|-------|---------------|
| **Tone** | `calm → energetic → calm` | Jornada emocional |
| **Camera** | `smooth, deliberate` | Confiança, controle |
| **Lighting** | `cold → warm transition` | Problema → Solução |
| **Pacing** | `medium, varies` | Mantém atenção |
| **Music** | `tension build → release → upbeat end` | Arco narrativo |

---

## PARTE 5: PROMPTS AUXILIARES

### Para Narração Teleprompter

```
Analise o Bloco [X] do VIDEO_LP_ROTEADOR.md e:

1. Reescreva para soar natural quando falado
2. Adicione pausas [PAUSA - 2s]
3. Marque ênfases [ÊNFASE: palavra]
4. Verifique timing (cabe no tempo?)

Output: Texto teleprompter-ready
```

### Para Gerar Shorts

```
Identifique 5 momentos para cortes:

1. Hook (0:00-0:30) - "1 frase, tudo pronto"
2. Problema (1:40-2:00) - "Escravidão digital"
3. Solução (3:45-4:00) - 4 comandos
4. Cat Coding (9:45-10:00) - Pirulita
5. Tagline (10:55-11:00) - "Um agente..."

Para cada: hook 3s + core + CTA
```

### Para Thumbnail

```
Gere 5 variações de thumbnail text:

1. Contraste: "2h → 1 FRASE"
2. Curiosidade: "Cat Coding?"
3. Promessa: "Escale sem treinar ninguém"
4. Dor: "Pare de copiar/colar"
5. Resultado: "Score 0.87 automático"
```

---

## PARTE 6: CHECKLIST PRÉ-PRODUÇÃO

- [ ] Script teleprompter-ready
- [ ] Assets visuais listados
- [ ] Música selecionada (arco narrativo)
- [ ] Screencasts gravados (demo real)
- [ ] Foto da Pirulita pronta 🐱
- [ ] Tagline LOTR no final

---

**Versão**: 1.1.0
**Criado**: 2025-12-03
**Atualizado**: 2025-12-03
**Integração**:
- VIDEO_LP_ROTEADOR.md v2.1.0
- DIRECAO_VISUAL_LP_ROTEADOR.md v1.0.0
**Uso**: Upload script + visual direction + context → Cole prompt → Itere

## Changelog
- **v1.1.0** (2025-12-03): Added TRINITY STRUCTURE section, included DIRECAO_VISUAL_LP_ROTEADOR.md as core file, clarified dual-input consumption
- **v1.0.0** (2025-12-03): Initial NotebookLM prompt with embedded visual direction
