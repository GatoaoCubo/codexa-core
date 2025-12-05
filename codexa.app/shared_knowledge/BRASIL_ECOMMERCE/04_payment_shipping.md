# Brazilian Payment & Shipping Infrastructure

**Category**: Transactions & Logistics
**Version**: 1.0.0
**Last Updated**: 2025-12-05
**Cross-Reference**: anuncio_agent, pesquisa_agent, curso_agent

---

## Overview

Brazilian e-commerce has unique payment preferences and logistics challenges. Understanding PIX dominance, installment culture, and shipping complexity is critical for marketplace success.

---

## Payment Methods Landscape

### Market Share (2024)

| Method | Share | Trend |
|--------|-------|-------|
| PIX | 41% | Growing |
| Credit Card | 32% | Stable |
| Boleto Bancario | 12% | Declining |
| Debit Card | 8% | Stable |
| Digital Wallets | 5% | Growing |
| BNPL (Pix parcelado) | 2% | Growing |

---

## PIX - Instant Payments

### What It Is

- Central Bank instant payment system
- 24/7/365 operation
- Free for individuals
- Settlement in seconds

### Key Stats (2024)

```
Registered keys: 700M+
Monthly transactions: 4B+
E-commerce adoption: 41%
Average confirmation: 3 seconds
```

### Implementation for E-commerce

**PIX QR Code Types**:
| Type | Use Case | Expiration |
|------|----------|------------|
| Static | Fixed amount, reusable | None |
| Dynamic | Unique per transaction | Configurable |
| PIX Cobranca | With due date, interest | Custom |

**Integration Options**:
1. **PSP Direct**: Mercado Pago, PagSeguro, Stripe
2. **Bank API**: Banco do Brasil, Itau, Bradesco
3. **Marketplace Native**: Built into ML, Amazon, Shopee

**Best Practices**:
```markdown
[ ] Display PIX prominently (first option)
[ ] Show instant confirmation messaging
[ ] Offer discount for PIX (saves card fees)
[ ] Include copy-paste code + QR
[ ] Set reasonable expiration (15-30 min)
```

### PIX Parcelado (BNPL)

New trend allowing installments via PIX:

| Provider | Max Installments | Fees |
|----------|------------------|------|
| Mercado Pago | 12x | Variable |
| PicPay | 12x | Variable |
| Nubank | 12x | Variable |

---

## Credit Cards

### Brazilian Card Specifics

**Installment Culture**:
```
Parcelamento sem juros: Seller absorbs interest
Parcelamento com juros: Customer pays interest
Common: 3x, 6x, 10x, 12x sem juros
```

**Consumer Expectation**: 70%+ of purchases are installment-based

### Major Card Networks

| Network | Market Share | Notes |
|---------|--------------|-------|
| Mastercard | 40% | Most accepted |
| Visa | 38% | Most accepted |
| Elo | 15% | Brazilian network |
| Hipercard | 4% | Regional strength |
| Amex | 3% | Premium segment |

### Fraud Considerations

Brazil has high card fraud rates:

| Metric | Brazil | Global Avg |
|--------|--------|------------|
| Fraud rate | 3.5% | 1.8% |
| Chargebacks | 1.2% | 0.6% |
| 3DS adoption | Growing | Standard |

**Mitigation**:
- 3D Secure mandatory for high-value
- Address verification (CEP matching)
- Device fingerprinting
- Behavioral analysis
- Manual review for flagged orders

---

## Boleto Bancario

### Overview

Traditional Brazilian payment slip, declining but still relevant:

**Pros**:
- No card required (unbanked access)
- Lower fraud risk
- Cash payment option (loterica)

**Cons**:
- 1-3 day confirmation
- High abandonment (40%+)
- Expiration management

### Best Practices

```markdown
[ ] Offer discount for boleto (lower fees than card)
[ ] Clear expiration date display
[ ] Send reminder before expiration
[ ] Easy regeneration if expired
[ ] Show payment locations (loterica, bank, app)
```

### Boleto Optimization

| Tactic | Impact |
|--------|--------|
| 3-day expiration | Reduces abandonment |
| Email + WhatsApp reminder | +15% conversion |
| Discount incentive | +20% boleto choice |
| Easy reissue | Recovers 10% lost sales |

---

## Digital Wallets

### Major Players

| Wallet | Users (M) | E-commerce Integration |
|--------|-----------|------------------------|
| Mercado Pago | 50+ | Native on ML, widespread |
| PicPay | 30+ | Growing acceptance |
| PagBank | 25+ | PagSeguro ecosystem |
| Nubank | 90+ | Limited checkout presence |
| Iti (Itau) | 15+ | Growing |

### Wallet Benefits

- Pre-filled checkout (less friction)
- Stored payment methods
- Loyalty programs (cashback)
- One-click purchase
- Trust factor (known brand)

---

## Payment Gateway Comparison

### For Marketplaces (Built-in)

| Platform | Gateway | Fees |
|----------|---------|------|
| Mercado Livre | Mercado Pago | Included in commission |
| Amazon BR | Amazon Pay | Included in commission |
| Shopee | ShopeePay | Included in commission |
| Magalu | Magalu Pay | Included in commission |

### For Own E-commerce

| Gateway | PIX Fee | Card Fee | Best For |
|---------|---------|----------|----------|
| Mercado Pago | 0.99% | 4.99% + installment | SMB, fast setup |
| PagSeguro | 0.99% | 4.99% + installment | SMB, physical + online |
| Stripe | 0.8% | 3.99% + 0.30 | Tech-savvy, international |
| Pagar.me | Custom | Custom | Mid-market, customization |
| Adyen | Custom | Custom | Enterprise, global |

---

## Shipping & Logistics

### Carrier Landscape

| Carrier | Coverage | Speed | Best For |
|---------|----------|-------|----------|
| Correios | 100% BR | 3-15 days | Universal reach |
| Jadlog | 97% | 2-7 days | B2B, volume |
| Total Express | 85% | 2-5 days | Same-day metros |
| Loggi | Major metros | Same-day | Express delivery |
| Azul Cargo | 95% | 1-3 days | Air freight |
| Lalamove | Major metros | Hours | Last-mile express |

### Fulfillment Models

```
1. SELF-FULFILLMENT
   Seller → Carrier → Customer
   Pro: Control, margins
   Con: Complexity, scale limits

2. 3PL (Third-Party Logistics)
   Seller → 3PL Warehouse → Carrier → Customer
   Pro: Scale, expertise
   Con: Costs, less control

3. MARKETPLACE FULFILLMENT
   Seller → ML Full / Amazon FBA → Customer
   Pro: Prime badges, trust
   Con: Fees, inventory commitment

4. DROPSHIPPING
   Seller → Supplier → Customer
   Pro: No inventory
   Con: Margins, quality control
```

### Shipping Cost Reality

**Average Costs (2024)**:
| Distance | Weight | Correios (PAC) | Private |
|----------|--------|----------------|---------|
| Same state | 1kg | R$ 18-25 | R$ 15-20 |
| Adjacent state | 1kg | R$ 25-35 | R$ 20-30 |
| Cross-country | 1kg | R$ 40-60 | R$ 35-50 |

**Free Shipping Thresholds**:
| Platform | Typical Threshold |
|----------|-------------------|
| Mercado Livre | R$ 79-199 (seller choice) |
| Amazon | R$ 99 (Prime: lower) |
| Shopee | Subsidized (varies) |
| Average D2C | R$ 149-299 |

### Delivery Time Expectations

| Region | Consumer Expectation | Reality |
|--------|---------------------|---------|
| Sao Paulo capital | 1-2 days | Achievable |
| Rio de Janeiro capital | 2-3 days | Achievable |
| State capitals | 3-5 days | Standard |
| Interior cities | 5-10 days | Standard |
| Remote areas | 10-20 days | Challenge |

---

## Logistics Challenges

### Geographic Factors

```
Brazil Size: 8.5M km2 (continental)
Time Zones: 4
Road Quality: Variable
Infrastructure: Concentrated in SE

Challenge Areas:
- Amazon region (river transport needed)
- Northeast interior (sparse coverage)
- Border regions (security concerns)
```

### Tax Complexity (ICMS by State)

Shipping across state lines triggers tax obligations:

| Origin | Destination | DIFAL Responsibility |
|--------|-------------|---------------------|
| SP (18%) | MG (18%) | None |
| SP (18%) | BA (20.5%) | Seller owes 2.5% to BA |
| SP (18%) | RJ (22%) | Seller owes 4% to RJ |

**Solution**: Use tax-compliant shipping integrations or fulfillment partners.

### Returns Logistics

**Reverse Logistics Challenge**:
- Customer expectation: Free returns
- Reality: Expensive, complex
- Average return rate: 5-15% (category dependent)

**Best Practices**:
```markdown
[ ] Clear return policy (7 days CDC minimum)
[ ] Prepaid return label or pickup
[ ] Quick refund process (builds trust)
[ ] Exchange option (retain sale)
[ ] Return reason tracking (reduce future returns)
```

---

## Integration Recommendations

### Shipping Aggregators

| Platform | Carriers | Best For |
|----------|----------|----------|
| Melhor Envio | 10+ | SMB, rate comparison |
| Frenet | 15+ | Mid-market, API |
| Intelipost | 20+ | Enterprise, optimization |
| Mandae | 8+ | High volume |

### Recommended Stack (SMB)

```
Payment: Mercado Pago (all-in-one)
Shipping: Melhor Envio (aggregation)
ERP: Bling or Tiny (operations)
Hub: Ideris (multi-marketplace)
```

### Recommended Stack (Enterprise)

```
Payment: Adyen or custom (multi-acquirer)
Shipping: Intelipost (optimization)
ERP: SAP or TOTVS
OMS: Custom or Sterling
WMS: Manhattan or custom
```

---

## Key Metrics to Track

### Payment

| Metric | Target | Alert |
|--------|--------|-------|
| Approval rate | >85% | <75% |
| Chargeback rate | <0.5% | >1% |
| PIX conversion | >90% | <80% |
| Boleto conversion | >60% | <50% |

### Shipping

| Metric | Target | Alert |
|--------|--------|-------|
| On-time delivery | >95% | <90% |
| Shipping cost % of GMV | <8% | >12% |
| Return rate | <10% | >15% |
| Customer satisfaction (shipping) | >4.5 | <4.0 |

---

## 2025 Trends

1. **PIX Automatico**: Recurring payments via PIX
2. **PIX Garantido**: Credit line for PIX purchases
3. **Drone Delivery**: Pilots in major metros
4. **Locker Networks**: Pickup point expansion
5. **Carbon-Neutral Shipping**: Growing consumer demand
6. **Real-Time Tracking**: GPS-level visibility standard

---

**Type**: Knowledge Card | **Domain**: Payment & Logistics BR
