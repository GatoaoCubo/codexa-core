# Brazilian E-commerce Regulatory Framework

**Category**: Legal & Compliance
**Version**: 1.0.0
**Last Updated**: 2025-12-05
**Cross-Reference**: pesquisa_agent, curso_agent, anuncio_agent

---

## Overview

Brazilian e-commerce operates under a multi-layered regulatory framework combining consumer protection, data privacy, and tax compliance requirements.

---

## LGPD Essentials

### Lei Geral de Protecao de Dados (Law 13.709/2018)

**Effective**: September 2020 (penalties from August 2021)

| Requirement | Implementation |
|-------------|----------------|
| Consent | Explicit opt-in for data collection |
| Purpose Limitation | Declare specific use cases |
| Data Minimization | Collect only necessary data |
| Access Rights | User portal for data requests |
| Breach Notification | 72h to ANPD + affected users |
| DPO Appointment | Required for most e-commerce |

**Penalties**:
- Warning with deadline
- Simple fine: 2% of revenue (max R$ 50 million per infraction)
- Daily fine until compliance
- Public disclosure of violation
- Data deletion order

### Practical Checklist

```markdown
[ ] Privacy policy in Portuguese (clear language)
[ ] Cookie consent banner with opt-out
[ ] Data retention policy defined
[ ] User data export/deletion mechanism
[ ] Third-party processor agreements (DPA)
[ ] ANPD registration (when required)
```

---

## CDC - Consumer Defense Code

### Codigo de Defesa do Consumidor (Law 8.078/1990)

**Core Rights for E-commerce**:

| Right | Description | Deadline |
|-------|-------------|----------|
| Direito de Arrependimento | Cancel without reason | 7 days from receipt |
| Garantia Legal | Defect warranty | 30 days (non-durable), 90 days (durable) |
| Informacao Clara | Product specifications | Pre-purchase |
| Oferta Vinculante | Honor advertised price | Duration of campaign |

### Required Disclosures

Every product listing MUST include:

1. **Seller Identification**: CNPJ, Razao Social, address
2. **Total Price**: Including shipping, taxes visible
3. **Payment Conditions**: Installments, interest rates
4. **Delivery Timeline**: Estimated days, shipping method
5. **Exchange/Return Policy**: Clear process description
6. **SAC Contact**: Phone, email, chat availability

### E-commerce Decree (7.962/2013)

Additional online-specific requirements:

- 24/7 order tracking access
- Purchase summary before confirmation
- Electronic contract available for download
- Immediate purchase confirmation email

---

## Marco Civil da Internet

### Law 12.965/2014

**Relevance for E-commerce**:

| Principle | Application |
|-----------|-------------|
| Net Neutrality | No platform-specific throttling |
| Provider Liability | Not liable for user content (until notified) |
| Data Retention | Connection logs: 1 year; App logs: 6 months |
| Court Orders | Required for content removal (except specific cases) |

**Notice and Takedown**: Platforms must have clear reporting mechanisms for IP violations, defamation, and illegal content.

---

## Tax & Fiscal Compliance

### NFe/NFC-e Requirements

| Document | Use Case | Mandatory Fields |
|----------|----------|------------------|
| NF-e | B2B sales | CNPJ, NCM, CFOP, ICMS |
| NFC-e | B2C retail | CPF (optional), product codes |
| CT-e | Shipping | Carrier data, route |

### ICMS E-commerce (DIFAL)

Since 2024 changes:

- **Origin State**: Collects internal rate
- **Destination State**: Collects DIFAL differential
- **Calculation**: Destination rate - Origin internal rate

**Example**: SP (18%) to BA (20.5%) = 2.5% DIFAL to BA

### Simples Nacional Limits

```
MEI: R$ 81,000/year (no marketplace restrictions)
ME: R$ 360,000/year
EPP: R$ 4.8 million/year
```

---

## Platform-Specific Compliance

### Mercado Livre

- Mandatory NFe for all categories (since 2023)
- Mercado Envios fiscal integration
- Reputation system tied to compliance

### Amazon BR

- FBA requires specific labeling
- Tax calculation at checkout
- Seller verification (CNPJ + bank)

### Shopee

- CPF/CNPJ validation
- NFe integration available
- Cross-border limits (remessa conforme)

---

## Advertising Regulations

### CONAR Guidelines

| Category | Restriction |
|----------|-------------|
| Comparative Ads | Must be objective, verifiable |
| Children | No direct purchase appeals |
| Health Claims | ANVISA approval required |
| Financial | Clear APR, total cost disclosure |

### Prohibited Claims

- "Best price guaranteed" (without proof)
- "Risk-free" (misleading)
- Fake urgency without real limitation
- Testimonials without disclosure

---

## Compliance Checklist Summary

```markdown
## Pre-Launch
[ ] CNPJ active and regular
[ ] Privacy policy published
[ ] Terms of service published
[ ] SAC channels operational
[ ] NFe emission configured

## Operations
[ ] 7-day return process defined
[ ] Shipping tracking provided
[ ] Price consistency (ad = checkout)
[ ] Stock accuracy maintained
[ ] Customer data secured (LGPD)

## Marketing
[ ] Claims verifiable
[ ] Disclosures present
[ ] No prohibited content
[ ] Influencer partnerships disclosed
```

---

## Resources

- **ANPD**: https://www.gov.br/anpd/
- **PROCON-SP**: https://www.procon.sp.gov.br/
- **CONAR**: http://www.conar.org.br/
- **Receita Federal**: https://www.gov.br/receitafederal/

---

## Key Dates 2025

| Date | Event |
|------|-------|
| Jan 1 | New ICMS rates effective |
| Mar 15 | ANPD audit cycle begins |
| Jul 1 | New consumer protection guidelines |
| Nov 15 | Black Friday compliance focus |

---

**Type**: Knowledge Card | **Domain**: Regulatory Compliance BR
