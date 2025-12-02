# Roteiro Hands-On: Módulo 01 - Introdução ao CODEXA

**Duração**: 8-10 minutos
**Formato**: Screencast com narração
**Objetivo**: Mostrar o sistema CODEXA funcionando em tempo real

---

## SETUP DA TELA

```
┌─────────────────────────────────────────────────────────────┐
│  Claude Code (tela principal)                               │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Terminal/Chat aberto                                    ││
│  │ Fonte: 16px (legível em 1080p)                         ││
│  │ Tema: Dark mode                                         ││
│  └─────────────────────────────────────────────────────────┘│
│  Webcam: Canto inferior direito (opcional)                  │
└─────────────────────────────────────────────────────────────┘
```

---

## ROTEIRO DE GRAVAÇÃO

### [00:00 - 00:30] Abertura

**NARRAÇÃO:**
> "Agora que você entendeu o que é CODEXA na teoria, vamos ver na prática. Vou abrir o Claude Code e mostrar exatamente como o sistema funciona."

**AÇÃO:** Mostrar tela do Claude Code aberta no diretório CODEXA

---

### [00:30 - 02:00] Comando /prime

**NARRAÇÃO:**
> "O primeiro comando que todo seller precisa conhecer é o `/prime`. Ele é o navegador do sistema - mostra o status e todos os agentes disponíveis."

**DIGITAR (devagar, mostrando cada tecla):**
```
/prime
```

**ESPERAR OUTPUT E COMENTAR:**
> "Olha só o que aparece: o dashboard mostra que temos 6 agentes disponíveis, 91 arquivos de conhecimento carregados, e 14 comandos prontos pra usar."

**DESTACAR NA TELA:**
- Status: ✅
- Agents: 6
- Knowledge: 91 files

---

### [02:00 - 04:00] Navegando pelos Agentes

**NARRAÇÃO:**
> "Cada agente tem seu próprio comando `/prime-*`. Vou mostrar como funciona a verticalização - quando você carrega um agente, o Claude vira especialista naquele assunto."

**DIGITAR:**
```
/prime-anuncio
```

**COMENTAR ENQUANTO CARREGA:**
> "Percebe que ele está carregando contexto específico de anúncios? São 20+ arquivos sobre copywriting, compliance, SEO de marketplace..."

**DEPOIS DIGITAR:**
```
/prime-pesquisa
```

**COMENTAR:**
> "Agora mudou - o contexto é de pesquisa de mercado. 700 URLs de marketplaces, frameworks de análise competitiva..."

---

### [04:00 - 06:30] Primeiro Pedido Real

**NARRAÇÃO:**
> "Agora vou fazer um pedido real. Vou pedir pro Anuncio Agent criar um título otimizado pra um produto simples."

**DIGITAR:**
```
/prime-anuncio

Crie um título otimizado para Mercado Livre:
Produto: Garrafa térmica de inox 500ml
Diferencial: Mantém gelado por 24h
Público: Pessoas que praticam esportes
```

**ESPERAR E COMENTAR O OUTPUT:**
> "Olha o resultado: ele não só criou o título, como já otimizou pra SEO do Mercado Livre. Tem as keywords principais no início, os atributos técnicos, e cabe nos 60 caracteres."

**DESTACAR:**
- Keywords posicionadas
- Caracteres contados
- Formato ML

---

### [06:30 - 08:00] Explorando a Estrutura

**NARRAÇÃO:**
> "Antes de terminar, quero mostrar onde está o conhecimento. Quando você executa `/prime-anuncio`, o Claude lê esses arquivos aqui..."

**MOSTRAR NA TELA (navegando pastas):**
```
agentes/anuncio_agent/
├── PRIME.md (mostrar brevemente)
├── iso_vectorstore/
│   ├── 01_conceitos.md
│   ├── 02_compliance.md
│   └── ... (mostrar lista)
```

**COMENTAR:**
> "São mais de 90 arquivos de conhecimento especializado. É por isso que o resultado é tão diferente de pedir pro ChatGPT genérico."

---

### [08:00 - 08:30] Encerramento

**NARRAÇÃO:**
> "Isso foi só o começo. Nos próximos módulos, você vai ver cada agente em ação com exemplos mais complexos. Por agora, o importante é: você viu que funciona, que é rápido, e que o conhecimento está todo documentado."

**MOSTRAR NA TELA:**
```
Próximo: Módulo 02 - Anúncios na Prática
```

---

## CHECKLIST PRÉ-GRAVAÇÃO

- [ ] Claude Code instalado e funcionando
- [ ] Repositório CODEXA clonado
- [ ] Fonte aumentada (16px+)
- [ ] Notificações desligadas
- [ ] Microfone testado
- [ ] Gravação de tela configurada (1080p)

## CHECKLIST PÓS-GRAVAÇÃO

- [ ] Audio sincronizado
- [ ] Zooms nos momentos certos
- [ ] Legendas adicionadas
- [ ] Thumbnail criada
- [ ] Duração final: 8-10 min

---

**Arquivo**: `outputs/hands_on/01_HANDS_ON_INTRODUCAO.md`
**Criado**: 2025-11-25
**Versão**: 1.0.0
