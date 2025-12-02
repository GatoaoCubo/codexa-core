# ❓ FAQ - Perguntas Frequentes

**Curso CODEXA**
**Versão**: 1.0.0
**Data**: 2025-11-19

---

## 📋 ÍNDICE

- [Geral](#geral)
- [Instalação e Setup](#instalação-e-setup)
- [Uso dos Agentes](#uso-dos-agentes)
- [Troubleshooting](#troubleshooting)
- [Avançado](#avançado)
- [Comercial](#comercial)

---

## 🌍 GERAL

### O que é o CODEXA?

CODEXA é um sistema de 6 agentes especializados de IA para automatizar tarefas de e-commerce no Brasil. É o "Cérebro IA para Sellers", reduzindo trabalho manual de 40 horas para menos de 6 horas por produto.

### Preciso saber programar para usar?

**Não!** O CODEXA foi desenhado para ser acessível a qualquer pessoa. Você só precisa:
- Saber usar comandos simples (como `/prime-anuncio`)
- Descrever o que precisa em linguagem natural
- Seguir os exercícios do curso

### Quanto custa o CODEXA?

O curso CODEXA é pay-once (pagamento único). Você também paga pelo uso da API do Claude (Anthropic).

**Custos estimados:**
- **Custo por anúncio completo**: ~R$ 0,50 (inclui validação de compliance)
- **Uso leve** (5-10 anúncios/dia): R$ 50-100/mês
- **Uso moderado** (20-50 anúncios/dia): R$ 150-300/mês
- **Uso intenso** (100+ anúncios/dia): R$ 400-750/mês

O sistema usa Claude Sonnet 4.5 para garantir qualidade máxima.

### Quais marketplaces são suportados?

O sistema é otimizado para 9 marketplaces brasileiros:
- Mercado Livre
- Amazon BR
- Shopee
- Magalu
- Shopify
- Lojas Integradas
- Tray
- Nuvemshop
- Bling

### Posso usar para outros países?

Sim, mas o sistema foi otimizado para o mercado brasileiro (compliance ANVISA/INMETRO, padrões locais). Para adaptar a outros países, você precisará customizar alguns HOPs.

---

## 🔧 INSTALAÇÃO E SETUP

### Como instalo o CODEXA?

Siga os passos do Módulo 1:
1. Tenha Python 3.8+ e Claude Code instalados
2. Clone o repositório do GitHub
3. Execute `npm install` ou equivalente
4. Configure suas credenciais da API Anthropic
5. Execute `/prime` para verificar se tudo está funcionando

### Não sei usar o terminal. Tem interface gráfica?

Atualmente o CODEXA funciona via linha de comando (CLI). Uma interface gráfica está planejada para versões futuras. O CLI é mais simples do que parece - o Módulo 1 te guia passo a passo.

### Meu `/prime` não funciona. O que fazer?

Verifique:
1. Você está no diretório correto? (Use `pwd` ou `cd` para verificar)
2. Os arquivos `.claude/commands/` existem?
3. Suas credenciais da API estão configuradas?
4. Execute `/help` para ver comandos disponíveis

### Posso usar com outros LLMs além do Claude?

Os HOPs são agnósticos a LLM (funcionam com qualquer modelo), mas o sistema de comandos `/prime` foi otimizado para Claude Code. Para usar com GPT-4 ou outros, você precisará adaptar a estrutura de comandos.

---

## 🤖 USO DOS AGENTES

### Qual agente devo usar primeiro?

Para um produto novo, a ordem recomendada é:
1. **Pesquisa Agent** → Entenda o mercado
2. **Marca Agent** → Defina identidade
3. **Anuncio Agent** → Crie textos
4. **Photo Agent** → Gere imagens
5. **Mentor Agent** → Valide tudo

### Posso usar apenas um agente?

Sim! Cada agente funciona independentemente. Se você só precisa criar anúncios, use apenas o Anuncio Agent. Se só quer pesquisa de mercado, use apenas o Pesquisa Agent.

### Como faço para o agente "lembrar" de conversas anteriores?

Os comandos `/prime-*` carregam o contexto completo do agente. Para continuidade entre sessões:
- Salve os outputs importantes em arquivos
- Referencie esses arquivos na próxima conversa
- Use o Mentor Agent para manter histórico de projetos

### Quanto tempo leva para gerar um anúncio completo?

Com o Anuncio Agent:
- Quick mode: 2-3 minutos
- Standard mode: 5-8 minutos
- Full workflow (7 fases): 10-15 minutos

### Os anúncios gerados são únicos?

Sim! Cada anúncio é gerado do zero baseado nas suas informações. O sistema não usa templates fixos, mas sim frameworks de copywriting profissional.

### Posso editar os outputs gerados?

Absolutamente! Os outputs são pontos de partida profissionais. Você pode (e deve):
- Ajustar o tom de voz
- Adicionar detalhes específicos
- Adaptar para sua necessidade
- Pedir variações ao agente

---

## 🔍 TROUBLESHOOTING

### O agente não entende minhas instruções. Por quê?

Dicas para instruções mais claras:
- Seja específico: "Crie anúncio de garrafa térmica 500ml" é melhor que "Faça um anúncio"
- Forneça contexto: público-alvo, marketplace, diferencial
- Use os templates dos exercícios como guia
- Divida tarefas complexas em passos menores

### O output não está bom. O que fazer?

1. Peça ao agente para refazer: "Refaça o título focando mais em benefícios"
2. Forneça exemplos: "Quero um tom como este exemplo..."
3. Use feedback iterativo: "Gostei do início, mas mude o final para..."
4. Tente o Mentor Agent para validação de qualidade

### Como valido se o compliance está correto?

O Anuncio Agent faz validação automática, mas você deve:
- Verificar se números de registro ANVISA/INMETRO são reais (o agente marca quando são necessários)
- Consultar o site oficial dos órgãos reguladores
- Ter um advogado revisar produtos de risco (medicamentos, eletrônicos)

### Meu Brand Consistency Score é baixo (<0.85). Como melhorar?

Isso significa inconsistências na sua marca. Verifique:
- Paleta de cores está definida e sendo usada?
- Tom de voz está documentado no Brand Guidelines?
- Todos os materiais seguem o mesmo arquétipo?
- Use o Marca Agent para revisar e corrigir

### O Photo Agent não gera boas imagens. Por quê?

O Photo Agent gera **prompts** de imagens, não as imagens em si. Você precisa:
1. Copiar os prompts gerados
2. Usar em ferramentas como Midjourney, DALL-E, Stable Diffusion
3. Iterar nos prompts conforme necessário
4. Seguir as especificações técnicas (resolução, formato)

---

## 🚀 AVANÇADO

### Como crio meu próprio agente customizado?

Use o Codexa Agent (Módulo 6):
1. Execute `/prime-codexa`
2. Use o workflow ADW de 5 fases
3. Siga o comando `/codexa-build_agent`
4. Documente usando TAC-7 framework
5. Valide e teste com casos reais

### O que é um HOP e como escrevo um?

HOP (High-Order Prompt) é um prompt modular reutilizável. Para criar:
1. Siga o TAC-7 framework (7 componentes obrigatórios)
2. Use o comando `/codexa-build_prompt`
3. Veja exemplos em `codexa.app/agentes/*/iso_vectorstore/`
4. Teste e refine iterativamente

### Posso contribuir com o projeto?

Sim! Veja o Módulo 6 - seção "Contribuindo com CODEXA":
- Reporte bugs no GitHub Issues
- Sugira novos agentes ou features
- Crie HOPs para gaps identificados
- Melhore a documentação
- Faça pull requests

### Como integro o CODEXA com APIs de marketplace?

Atualmente o CODEXA gera outputs (textos, estratégias, prompts). Para integração com APIs:
- Use os outputs como input para suas ferramentas de publicação
- Desenvolva scripts que consumam os JSONs gerados
- Considere usar o Codexa Agent para criar um novo agente de "Auto-Publisher"

### O sistema funciona offline?

Não completamente. Você precisa de:
- Conexão para API do Claude (requisição online)
- Arquivos locais do CODEXA (iso_vectorstore) funcionam offline
- Para uso totalmente offline, considere usar LLMs locais (Llama, Mistral) com os HOPs

---

## 💰 COMERCIAL

### Posso usar o CODEXA comercialmente?

Sim! O CODEXA é open-source. Você pode:
- Usar para seus próprios produtos
- Oferecer como serviço para clientes
- Integrar em suas ferramentas
- Apenas respeite a licença do projeto (verifique LICENSE no repositório)

### Posso vender anúncios criados pelo CODEXA?

Sim! Os outputs gerados pertencem a você. Você pode:
- Vender anúncios como freelancer
- Oferecer pacotes de criação de conteúdo
- Usar em agências de e-commerce
- Criar produtos digitais (templates, cursos)

### Quantos produtos posso processar por mês?

Não há limite técnico no CODEXA. O limite é:
- Seu plano da API Anthropic (tokens disponíveis)
- Seu tempo para revisar outputs
- Capacidade de processamento do seu computador

Em média, com plano padrão da API, você processa 100-200 produtos completos por mês.

### Há suporte técnico oficial?

Atualmente:
- Documentação completa (curso + READMEs)
- GitHub Issues para bugs
- Comunidade no Discord (se disponível)
- Suporte comercial dedicado: em planejamento

### Onde encontro mais recursos e tutoriais?

- **Documentação oficial**: `codexa.app/README.md`
- **Guias rápidos**: `codexa.app/agentes/*/QUICK_START.md`
- **Este curso**: Módulos 1-6
- **Exemplos práticos**: `codexa.app/agentes/*/outputs/`
- **GitHub**: Issues, Discussions, Wiki

---

## 🎓 CERTIFICAÇÃO

### Como obtenho o certificado do curso?

Complete todos os exercícios dos 6 módulos e demonstre:
- Criar anúncio profissional em <10 minutos
- Realizar pesquisa competitiva completa
- Desenvolver estratégia de marca consistente
- Gerar grid 9-fotos otimizado
- Entender arquitetura CODEXA

(Sistema de certificação formal em desenvolvimento)

---

## 📞 SUPORTE

Ainda tem dúvidas?

1. Revise os módulos relevantes do curso
2. Consulte o glossário (GLOSSARIO.md)
3. Verifique os exemplos práticos
4. Abra uma issue no GitHub
5. Consulte a comunidade

---

**Criado com ❤️ pelo time CODEXA**
**"Build the thing that builds the thing"**
