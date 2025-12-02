# Amazon Selling Partner API (SP-API) Overview

**Fonte**: developer-docs.amazon.com/sp-api
**Atualizado**: 2025-12-02
**Categoria**: MARKETPLACES
**Plataforma**: Amazon BR

---

## What is SP-API?

The Selling Partner API enables developers to create applications for Amazon sellers and vendors - applications for selling partners (sellers, vendors, or both).

---

## Primary Capabilities

| Capability | Description |
|------------|-------------|
| **Listings Management** | Create, update, and manage product listings |
| **Orders & Fulfillment** | Access order data and manage fulfillment workflows |
| **Inventory Management** | Track FBA and merchant-fulfilled inventory |
| **Financial Data** | Retrieve transactions, payments, and financial events |
| **Reports & Analytics** | Request and schedule operational reports |
| **Messaging** | Send notifications to customers |
| **Shipping** | Integrate shipping and logistics operations |

---

## Authentication & Authorization

SP-API uses a credential-based workflow:

### Steps

1. **Developer Registration** - Register as public or private developer
2. **Application Registration** - Create applications with LWA (Login with Amazon) credentials
3. **Authorization Workflows** - Sellers grant permission via authorization flow
4. **Tokens** - Applications receive refresh/access tokens for API calls

### Token Flow

```
Register App → Get LWA Credentials → Seller Authorizes → Receive Tokens → Make API Calls
```

---

## Key Resources

| Resource | Purpose |
|----------|---------|
| **API References** | Interactive documentation for all endpoints |
| **Sandbox Environment** | Test integration before production |
| **Code Samples** | Walkthroughs demonstrating best practices |
| **SDKs** | Pre-built libraries: C#, Java, Python, JavaScript, PHP |

---

## Getting Started

1. **Register** as developer in Solution Provider Portal
2. **Create** a sandbox application
3. **Make test calls** using provided sandbox
4. **Authorize** seller access
5. **Deploy** to production

---

## Main Endpoints

| API | Description |
|-----|-------------|
| `/catalog/items` | Product catalog data |
| `/orders` | Order information |
| `/fba/inventory` | FBA inventory levels |
| `/finances/transactions` | Financial transactions |
| `/reports` | Generate and retrieve reports |

---

## API Health

Monitor status at: [SP-API Health Dashboard](https://sellercentral.amazon.com/sp-api-status)

---

## Aplicação CODEXA

**Quando usar este conhecimento:**
- Ao integrar sistemas com Amazon Brasil
- Ao automatizar gestão de produtos FBA
- Ao sincronizar estoque entre plataformas
- Ao desenvolver ferramentas para sellers Amazon

**Tags**: amazon, sp_api, fba, marketplace, orders, inventory
