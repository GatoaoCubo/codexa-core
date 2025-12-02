# Mercado Livre API Documentation Overview

**Fonte**: developers.mercadolivre.com.br
**Atualizado**: 2025-12-02
**Categoria**: MARKETPLACES
**Plataforma**: Mercado Livre

---

## Platform Structure

The Mercado Livre developers site organizes API documentation by business unit:

| Unit | Description |
|------|-------------|
| **Mercado Libre** | Core marketplace functionality |
| **Mercado Shops** | Store management features |
| **Mercado Envios** | Shipping and logistics |
| **Mercado Pago** | Payment processing |

---

## Key Documentation Sections

### Application Management
Consulte as informações essenciais para trabalhar com as APIs do Mercado Livre.

### Cross-Cutting Resources
- User and application management
- Common integration patterns
- Shared security practices

### Security Framework
- Developer security guidelines
- API authentication protocols (OAuth 2.0)
- Best practices for secure integration

---

## Access Requirements

1. **Registrar conta** no portal de desenvolvedores
2. **Criar aplicação** através do painel de gerenciamento
3. **Revisar documentação** de autenticação e segurança

---

## Authentication (OAuth 2.0)

### Fluxo de Autenticação

```
1. Usuário autoriza app → Redirect com CODE
2. App troca CODE por ACCESS_TOKEN
3. App usa ACCESS_TOKEN nas requisições
4. ACCESS_TOKEN expira → Use REFRESH_TOKEN
```

### Endpoints Base

| Ambiente | URL |
|----------|-----|
| **Produção Brasil** | `https://api.mercadolibre.com` |
| **Auth** | `https://auth.mercadolivre.com.br` |

---

## Principais APIs

### Items API
Gerenciamento de anúncios:
- Criar, editar, pausar, reativar
- Gerenciar variações
- Atualizar estoque e preço

### Categories API
Navegação de categorias:
- Listar categorias
- Atributos por categoria
- Fichas técnicas

### Orders API
Gerenciamento de vendas:
- Listar pedidos
- Detalhes de venda
- Atualizar status

### Questions API
Perguntas e respostas:
- Listar perguntas
- Responder perguntas
- Gerenciar FAQ

---

## Rate Limits

| Tipo | Limite |
|------|--------|
| **Por App** | Varia por endpoint |
| **Por Usuário** | Varia por endpoint |
| **Burst** | Proteção contra picos |

---

## Boas Práticas

1. **Cache de tokens**: Evite gerar novo token a cada request
2. **Tratamento de erros**: Implemente retry com backoff
3. **Logs**: Registre todas as interações para debug
4. **Webhooks**: Use notificações em vez de polling

---

## Aplicação CODEXA

**Quando usar este conhecimento:**
- Ao integrar sistemas com Mercado Livre
- Ao automatizar gestão de anúncios
- Ao sincronizar estoque/preços
- Ao desenvolver ferramentas para sellers

**Tags**: mercadolivre, api, oauth, items, orders, marketplace
