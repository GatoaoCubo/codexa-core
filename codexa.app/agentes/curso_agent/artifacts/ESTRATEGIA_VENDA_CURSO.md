# Estratégia de Venda: Curso + Repositório GitHub

> **Status:** 📋 Documentação para implementação futura
> **Objetivo:** Proteger código e integrar Hotmart + GitHub para venda do curso
> **Última atualização:** 2025-11-20

---

## 🎯 Problema a Resolver

Como vender acesso ao repositório `lm.codexa` junto com o curso, protegendo contra:
- ✗ Alunos que cancelam mas mantêm o código
- ✗ Compartilhamento não autorizado
- ✗ Pirataria e redistribuição
- ✗ Amigos que pegam código sem pagar

---

## 🏗️ Arquitetura Recomendada (Abordagem Híbrida)

```
┌─────────────────────────────────────────────────────────┐
│                    HOTMART (VENDAS)                     │
│  - Checkout de pagamento                                │
│  - Gestão de alunos                                     │
│  - Reembolsos e cancelamentos                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ Webhook (compra/cancelamento)
                     ▼
┌─────────────────────────────────────────────────────────┐
│              AUTOMAÇÃO (Make.com/Zapier)                │
│  - Recebe webhook do Hotmart                            │
│  - Valida dados do aluno                                │
│  - Chama GitHub API                                     │
│  - Envia email de boas-vindas                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ GitHub API (add/remove member)
                     ▼
┌─────────────────────────────────────────────────────────┐
│           GITHUB ORGANIZATION (ecomlm-academy)          │
│  ┌───────────────────────────────────────────────┐     │
│  │  Repositório: lm.codexa (PRIVADO)             │     │
│  │  - Código completo do curso                   │     │
│  │  - Atualizações contínuas                     │     │
│  │  - Acesso: Read-only para alunos              │     │
│  └───────────────────────────────────────────────┘     │
│                                                         │
│  Team: "Alunos Ativos"                                  │
│  - Adicionados automaticamente via API                  │
│  - Removidos se cancelarem                              │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                PROTEÇÕES ADICIONAIS                     │
│  ✓ LICENSE restritiva                                   │
│  ✓ Watermark no código (email do aluno)                │
│  ✓ Termos de uso assinados                             │
│  ✓ Comunidade exclusiva (Discord/Telegram)             │
│  ✓ Suporte técnico via GitHub Issues                   │
└─────────────────────────────────────────────────────────┘
```

---

## 📝 Implementação Passo a Passo

### Fase 1: Configuração GitHub Organization

**1.1 Criar Organization**
```bash
# Acesse: https://github.com/organizations/new
# Nome sugerido: ecomlm-academy
# Plan: Free (upgrade depois se necessário)
```

**1.2 Transferir Repositório**
```bash
# No repositório lm.codexa:
# Settings → General → Transfer ownership
# New owner: ecomlm-academy
# Confirmar transferência
```

**1.3 Criar Team "Alunos Ativos"**
```bash
# Organization → Teams → New team
# Team name: alunos-ativos
# Privacy: Secret
# Permissions: Read (somente leitura)
```

**1.4 Adicionar Repositório ao Team**
```bash
# Team → Repositories → Add repository
# Selecionar: lm.codexa
# Permission: Read
```

---

### Fase 2: Configuração Hotmart Webhooks

**2.1 Obter URL do Webhook**
```bash
# Criar conta em Make.com ou Zapier
# Criar novo "Scenario" (Make) ou "Zap" (Zapier)
# Trigger: Webhook
# Copiar URL do webhook
```

**2.2 Configurar no Hotmart**
```bash
# Hotmart → Ferramentas → Webhooks
# Adicionar nova URL
# Eventos para monitorar:
#   - PURCHASE_APPROVED (compra aprovada)
#   - PURCHASE_REFUNDED (reembolso)
#   - SUBSCRIPTION_CANCELLATION (cancelamento)
```

**2.3 Eventos Hotmart (Exemplos)**

Compra aprovada:
```json
{
  "event": "PURCHASE_APPROVED",
  "data": {
    "buyer": {
      "email": "aluno@example.com",
      "name": "Nome do Aluno"
    },
    "purchase": {
      "transaction": "HP12345678",
      "status": "approved"
    }
  }
}
```

Cancelamento:
```json
{
  "event": "SUBSCRIPTION_CANCELLATION",
  "data": {
    "buyer": {
      "email": "aluno@example.com"
    },
    "subscription": {
      "status": "cancelled"
    }
  }
}
```

---

### Fase 3: Automação (Make.com/Zapier)

**3.1 Fluxo de Compra Aprovada**

```javascript
// 1. Webhook Trigger (Hotmart)
// 2. Filter: event == "PURCHASE_APPROVED"
// 3. HTTP Request: GitHub API

POST https://api.github.com/orgs/ecomlm-academy/invitations
Headers:
  Authorization: token ghp_YOUR_GITHUB_TOKEN
  Accept: application/vnd.github.v3+json
Body:
{
  "email": "{{buyer.email}}",
  "role": "direct_member",
  "team_ids": [12345678] // ID do team "alunos-ativos"
}

// 4. Enviar email de boas-vindas
Subject: Bem-vindo ao Curso! Acesso ao GitHub
Body:
  Olá {{buyer.name}},

  Você recebeu um convite para acessar o repositório privado do curso!

  1. Acesse seu email e aceite o convite do GitHub
  2. Entre em: https://github.com/ecomlm-academy/lm.codexa
  3. Clone o repositório: git clone https://github.com/ecomlm-academy/lm.codexa.git

  ⚠️ IMPORTANTE:
  - Este código é de uso exclusivo para alunos ativos
  - Redistribuição é proibida e ilegal
  - Ao aceitar, você concorda com nossos Termos de Uso

  Bons estudos!
```

**3.2 Fluxo de Cancelamento/Reembolso**

```javascript
// 1. Webhook Trigger (Hotmart)
// 2. Filter: event == "PURCHASE_REFUNDED" OR "SUBSCRIPTION_CANCELLATION"
// 3. Get GitHub username by email

GET https://api.github.com/search/users?q={{buyer.email}}+in:email

// 4. Remove from organization
DELETE https://api.github.com/orgs/ecomlm-academy/memberships/{{username}}

// 5. Log the removal
// 6. (Opcional) Enviar email informando remoção
```

---

### Fase 4: Proteções de Código

**4.1 LICENSE Restritiva**

Criar arquivo: `LICENSE`
```text
PROPRIETARY LICENSE - USO EXCLUSIVO PARA ALUNOS

Copyright (c) 2025 [SEU NOME/EMPRESA]

Este código é propriedade exclusiva de [SEU NOME/EMPRESA].

PERMISSÕES:
✓ Uso pessoal para fins de aprendizado
✓ Modificação para projetos pessoais
✓ Uso em portfólio pessoal (com atribuição)

PROIBIÇÕES:
✗ Redistribuição comercial ou gratuita
✗ Compartilhamento com terceiros
✗ Revenda ou sublicenciamento
✗ Uso em produtos comerciais sem autorização escrita

CONDIÇÕES:
- Acesso válido apenas durante matrícula ativa no curso
- Violações serão processadas nos termos da lei
- Código identificado com watermark por aluno

Para questões comerciais, contate: contato@seudominio.com
```

**4.2 Watermark no Código**

Adicionar em arquivos principais:
```javascript
/**
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 * 📚 lm.codexa - Large E-commerce Model
 * 🎓 Curso Completo de E-commerce com IA
 *
 * 👤 Licenciado para: {{ALUNO_EMAIL}}
 * 📅 Data de acesso: {{DATA_ACESSO}}
 * 🔐 ID de Licença: {{TRANSACTION_ID}}
 *
 * ⚠️  USO RESTRITO - Redistribuição Proibida
 * 📜 Veja LICENSE para termos completos
 * ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 */
```

**4.3 Termos de Uso (README)**

Adicionar em `README.md`:
```markdown
## ⚠️ Termos de Uso

Este repositório é **PRIVADO** e de uso **EXCLUSIVO** para alunos matriculados.

### Você PODE:
- ✅ Usar o código para aprender
- ✅ Modificar para projetos pessoais
- ✅ Incluir em seu portfólio (com atribuição)

### Você NÃO PODE:
- ❌ Compartilhar com amigos/colegas
- ❌ Revender ou redistribuir
- ❌ Postar publicamente (GitHub público, fóruns, etc.)
- ❌ Usar comercialmente sem autorização

### Consequências:
- Remoção imediata do acesso
- Banimento permanente
- Ação legal por violação de copyright

**Ao fazer clone deste repositório, você aceita estes termos.**
```

---

### Fase 5: Valor Além do Código (Anti-Pirataria)

**5.1 Comunidade Exclusiva**
```
Discord/Telegram Privado:
- Canal #dúvidas-código
- Canal #projetos-alunos
- Lives semanais
- Networking
```

**5.2 Atualizações Contínuas**
```
Releases mensais:
- Novos módulos
- Correções de bugs
- Features experimentais
- Integrações novas

→ Piratas ficam com versão desatualizada
```

**5.3 Suporte Técnico**
```
Via GitHub Issues (privadas):
- Resposta em até 24h
- Code review de projetos
- Debugging assistido
```

**5.4 Certificado de Conclusão**
```
Apenas alunos ativos recebem:
- Certificado digital
- Badge no LinkedIn
- Carta de recomendação (melhores alunos)
```

---

## 💰 Custos Estimados

| Item | Provedor | Custo Mensal | Observações |
|------|----------|--------------|-------------|
| GitHub Organization | GitHub | Grátis | Free plan suficiente inicialmente |
| Automação | Make.com | $9-29 | 1000-10000 operações/mês |
| Automação (Alt) | Zapier | $20-50 | Mais fácil, mais caro |
| Automação (Alt) | n8n Self-hosted | $5-10 | VPS DigitalOcean/Hetzner |
| Comunidade | Discord | Grátis | - |
| Email | SendGrid | Grátis | 100 emails/dia grátis |
| **TOTAL** | - | **$9-50/mês** | Escala com nº de alunos |

---

## 🔧 Ferramentas Necessárias

### GitHub
- [ ] Criar GitHub Organization
- [ ] Gerar Personal Access Token (PAT) com permissões:
  - `admin:org` - gerenciar organization
  - `repo` - acessar repositórios
  - `user` - ler informações de usuários

### Hotmart
- [ ] Configurar webhooks
- [ ] Testar eventos em sandbox
- [ ] Documentar transaction IDs

### Automação (Make.com exemplo)
- [ ] Criar conta em make.com
- [ ] Criar scenario "Adicionar Aluno"
- [ ] Criar scenario "Remover Aluno"
- [ ] Testar fluxos completos

### Email
- [ ] Configurar SendGrid/Mailgun
- [ ] Criar templates de email
- [ ] Testar envios

---

## 📊 Métricas de Sucesso

### KPIs para Monitorar:
- **Taxa de Conversão:** Compras → Acesso GitHub aceito
- **Taxa de Cancelamento:** % alunos que cancelam
- **Tempo de Ativação:** Compra → Clone do repo
- **Engajamento:** Commits, issues abertas, participação
- **Pirataria Detectada:** Watermarks encontrados externamente

### Dashboards:
```javascript
// Integrar com Google Analytics/Mixpanel:
- Compras por dia
- Acessos ativos ao repo
- Cancelamentos/Reembolsos
- Tempo médio de permanência
```

---

## 🚨 Plano de Contingência

### Se Detectar Pirataria:
1. **Identificar fonte** via watermark
2. **Remover acesso** do aluno original
3. **DMCA takedown** se postado publicamente
4. **Ação legal** se necessário (casos graves)

### Se Hotmart/GitHub cair:
1. **Backup manual** da lista de alunos
2. **Comunicação proativa** via email
3. **Acesso temporário** via repo alternativo

### Se Automação falhar:
1. **Alertas** via email/SMS
2. **Processo manual** temporário
3. **Fallback** para adição manual

---

## 📅 Roadmap de Implementação

### Sprint 1 (Semana 1-2): Setup Básico
- [x] Documentar estratégia (este arquivo)
- [ ] Criar GitHub Organization
- [ ] Transferir repositório
- [ ] Criar teams e permissões
- [ ] Escrever LICENSE e Termos

### Sprint 2 (Semana 3-4): Automação
- [ ] Configurar Make.com/Zapier
- [ ] Integrar Hotmart webhooks
- [ ] Testar fluxo de compra
- [ ] Testar fluxo de cancelamento
- [ ] Setup emails automatizados

### Sprint 3 (Semana 5-6): Proteções
- [ ] Implementar watermarking
- [ ] Criar sistema de tracking
- [ ] Setup monitoramento de pirataria
- [ ] Documentar processos

### Sprint 4 (Semana 7-8): Valor Extra
- [ ] Criar comunidade Discord/Telegram
- [ ] Planejar releases mensais
- [ ] Setup sistema de certificados
- [ ] Lançamento BETA

---

## 🔗 Recursos Úteis

### APIs e Documentação:
- [GitHub API - Organizations](https://docs.github.com/en/rest/orgs)
- [GitHub API - Teams](https://docs.github.com/en/rest/teams)
- [Hotmart Webhooks](https://developers.hotmart.com/docs/pt-BR/v1/webhook/)
- [Make.com Templates](https://www.make.com/en/templates)

### Templates:
- `docs/templates/email_welcome.html` - Email de boas-vindas
- `docs/templates/email_removal.html` - Email de remoção
- `docs/templates/termos_uso.md` - Termos de uso completos

### Scripts Úteis:
- `scripts/github_add_user.sh` - Adicionar aluno manualmente
- `scripts/github_remove_user.sh` - Remover aluno
- `scripts/watermark_code.py` - Adicionar watermark em código
- `scripts/check_piracy.py` - Verificar código público

---

## 📞 Próximos Passos

**Para implementar esta estratégia:**

1. **Revisar e aprovar** esta documentação
2. **Definir budget** (qual solução de automação usar)
3. **Criar GitHub Organization** (ou usar existente)
4. **Implementar automação** (começar com Make.com)
5. **Testar end-to-end** antes do lançamento
6. **Documentar para o curso_agent** integrar no curso

---

## 🤝 Responsabilidades

| Tarefa | Responsável | Status |
|--------|-------------|--------|
| Estratégia e Documentação | ✅ Completo | DONE |
| Setup GitHub Organization | Você | TODO |
| Configurar Hotmart Webhooks | Você | TODO |
| Implementar Automação | curso_agent | TODO |
| Criar Templates de Email | curso_agent | TODO |
| Testar Fluxos Completos | Você + curso_agent | TODO |
| Monitoramento e Manutenção | Contínuo | TODO |

---

**Documento mantido por:** Claude Code
**Versão:** 1.0
**Data:** 2025-11-20
**Próxima revisão:** Quando iniciar implementação
