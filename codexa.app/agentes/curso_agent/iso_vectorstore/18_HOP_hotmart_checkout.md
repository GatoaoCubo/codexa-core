# HOP: Hotmart Checkout Configuration for Maximum Conversion

**Version**: 1.0.0
**Type**: Sales Optimization HOP
**Agent**: curso_agent
**TAC-7 Compliant**: Yes

---

## TAC-7 STRUCTURE

### T - Title
**Configure High-Converting Checkout Page with Payment Methods, Guarantees, and Recovery Flows**

### A - Audience
- Course creators launching products on Hotmart
- Curso agent executing checkout optimization workflow
- Producers migrating from other platforms and need Hotmart-specific setup

### C - Context
**When to use this HOP:**
- After product approval and Club setup complete
- Before public launch or paid traffic campaigns
- When optimizing existing checkout for better conversion
- After A/B testing checkout variations

**Prerequisites:**
- [ ] Product created and approved in Hotmart
- [ ] Pricing defined (single payment or subscription)
- [ ] Guarantee period decided (7, 15, or 30 days)
- [ ] Brand assets ready (logo, colors, trust badges)
- [ ] Sales copy written (headline, bullets, CTA)
- [ ] Payment methods decision made (card, PIX, boleto)

### T - Task
**Configure a conversion-optimized checkout page on Hotmart with branded design, multiple payment methods, clear guarantees, and automated recovery flows to maximize sales and minimize abandoned carts.**

### A - Approach

---

## STEP 1: Access Checkout Configuration

1. Log in to Hotmart panel: https://app-vlc.hotmart.com
2. Navigate to: **Produtos → [Seu Produto] → Checkout**
3. You'll see two tabs:
   - **Página de Pagamento** (Payment Page) - main checkout config
   - **Ofertas** (Offers) - pricing and variations
4. Start with **Página de Pagamento**

---

## STEP 2: Choose Checkout Type

Hotmart offers 2 checkout types:

**Option A: Checkout Padrão Hotmart (Standard)**
- Pre-built layout by Hotmart
- Fast setup (5-10 min)
- Limited customization (colors, logo only)
- Mobile-optimized out of the box
- **Use when**: You want quick launch, no design skills

**Option B: Checkout Personalizado (Custom)**
- Full control over layout and elements
- Requires HTML/CSS knowledge (or developer)
- Embed on your own domain
- **Use when**: You have landing page builder (ClickFunnels, Elementor) and want full brand control

**Recommendation**: Start with **Checkout Padrão** (easier), optimize later with custom if needed.

**To select**:
1. In Checkout settings, find "Tipo de Checkout"
2. Choose: **Padrão Hotmart**
3. Save

---

## STEP 3: Customize Visual Appearance

**3.1 Upload Logo:**
- Click **"Personalização" → "Logo"**
- Upload PNG (transparent background recommended)
- Size: 200x60px to 300x90px
- Max file size: 2MB
- Preview on desktop and mobile
- Save

**3.2 Set Brand Colors:**
- **Primary Color**: Main CTA button, links (use your brand primary)
  - Example: #FF5733 (vibrant, high contrast)
  - Avoid: Low contrast colors (white on yellow)
- **Secondary Color**: Headers, accents (use brand secondary)
- **Background Color**: Page background (white or light gray recommended)
- **Text Color**: Body text (dark gray #333 or black #000)
- Use color picker or paste hex codes
- Save

**3.3 Add Header Image (Optional):**
- Upload banner: 1200x400px
- Shows product cover, course preview, or hero image
- Should include: Product name + key benefit
- Example: "Curso CODEXA - Domine IA para E-Commerce em 30 Dias"
- Max file size: 5MB
- Save

**3.4 Preview Checkout:**
- Click **"Visualizar Checkout"** (Preview Checkout)
- Test on:
  - Desktop (Chrome, Firefox, Safari)
  - Mobile (phone simulator or real device)
- Check:
  - Logo displays correctly
  - Colors have sufficient contrast (WCAG AA)
  - Text is readable
  - CTA button stands out
- Return and adjust if needed

---

## STEP 4: Configure Payment Methods

**4.1 Enable Payment Methods:**

Navigate to: **Checkout → Métodos de Pagamento**

**Credit Card (Cartão de Crédito):**
- Status: ✅ Always Enable (mandatory, highest conversion)
- Brands accepted: Visa, Mastercard, Amex, Elo, Hipercard (Hotmart default)
- Installments: Configure max (see Step 4.2)
- Security: 3D Secure enabled by Hotmart (fraud prevention)

**PIX (Instant Payment):**
- Status: ✅ Enable (recommended, instant approval)
- Auto-approval: Yes (instant Club access)
- Expiration: Not applicable (instant or abandoned)
- Conversion tip: Offer small discount for PIX (e.g., 5% off)

**Boleto Bancário:**
- Status: ⚠️ Enable with caution (7-day wait, lower completion rate)
- Expiration: 3-7 days (3 days = urgency, 7 days = flexibility)
- Recovery flows: Mandatory (see Step 7)
- Use when: Targeting audience without credit card access (lower-income)

**Parcelado Hotmart (Hotmart Installments):**
- Status: ✅ Enable if eligible (invite-only feature)
- Allows installments even for customers without credit limit
- Hotmart assumes risk, charges fee
- Increases conversions by 20-30% (reported by Hotmart)
- Check eligibility: Contact Hotmart support

**Deposit/Wire Transfer:**
- Status: ❌ Disable (rarely used, manual processing)

**International Payments (PayPal, etc.):**
- Status: Configure if selling to international audience
- Requires Hotmart review (submit request)

**Save payment methods**

---

**4.2 Configure Installments (Parcelamento):**

1. Go to: **Checkout → Parcelamento**
2. Set **Max Installments**:
   - Low-ticket (<R$ 200): 3-6x
   - Mid-ticket (R$ 200-1000): 6-10x
   - High-ticket (>R$ 1000): 10-12x
3. **Minimum per installment**: R$ 30-50 (prevents tiny installments)
4. **Interest (Juros)**:
   - Option A: **0% interest, you absorb fees** (recommended for trust)
   - Option B: **Pass interest to customer** (Hotmart calculates rate)
   - Recommendation: Absorb fees for better conversion (especially launches)
5. **Display**: Show all installments on checkout (e.g., "12x de R$ 49,90")
6. Save

---

## STEP 5: Write Checkout Copy

**5.1 Headline (Above the Fold):**

Formula: **[Transformation] em [Timeframe] sem [Pain Point]**

Examples:
- ✅ "Domine IA para E-Commerce em 30 Dias sem Programar"
- ✅ "Fature R$ 10k/mês com Dropshipping em 90 Dias ou Devolv emos Seu Dinheiro"
- ❌ "Curso de E-Commerce" (too vague)

**Where to add**: Checkout → Descrição → Título Principal

---

**5.2 Bullet Points (What's Included):**

Formula: **[Feature] para [Benefit] ([Proof])**

Examples:
- ✅ "6 módulos em vídeo (8h de conteúdo) para dominar anúncios em Mercado Livre (+ 300 alunos aprovados)"
- ✅ "Templates prontos de e-mails e anúncios para copiar e colar no seu negócio (economize 20h/semana)"
- ✅ "Acesso vitalício + updates grátis para sempre ter o método mais atualizado"

**Where to add**: Checkout → Descrição → "O que está incluído"

**Quantity**: 5-8 bullets (more = decision paralysis)

---

**5.3 Guarantee Statement:**

Formula: **"Garantia incondicional de [X] dias. Se não gostar, devolvemos 100% do seu dinheiro, sem perguntas."**

Examples:
- ✅ "Garantia de 7 dias. Teste o curso, se não for para você, devolvemos cada centavo."
- ✅ "30 dias de garantia total. Zero risco para você."

**Where to add**: Checkout → Seção "Garantia" (below payment form)

**Visual**: Add trust badge (shield icon + "Garantia" text)

---

**5.4 Call-to-Action (CTA Button):**

Formula: **[Action Verb] + [Benefit/Outcome]**

Examples:
- ✅ "Quero Dominar E-Commerce Agora"
- ✅ "Começar Minha Transformação"
- ✅ "Sim, Eu Quero Acesso Imediato"
- ❌ "Comprar" (boring, transactional)
- ❌ "Clique Aqui" (no value stated)

**Where to add**: Checkout → Botão de Pagamento → Texto do Botão

**Color**: High contrast (orange, green, red) vs. page background

---

**5.5 FAQ Section (Below Checkout):**

Add 5-7 common objections:

1. **"Quanto tempo tenho para concluir o curso?"**
   - "Acesso vitalício! Estude no seu ritmo, sem pressa."

2. **"Funciona para iniciantes?"**
   - "Sim! 80% dos alunos nunca tinham vendido online antes."

3. **"E se eu não tiver resultados?"**
   - "Garantia de [X] dias. Devolução total, sem perguntas."

4. **"Preciso de conhecimento técnico?"**
   - "Zero! Tudo é explicado passo a passo, mesmo para quem nunca usou computador."

5. **"Quanto tempo por dia preciso dedicar?"**
   - "30-60 minutos por dia é suficiente. Curso desenhado para quem tem rotina corrida."

6. **"O curso é atualizado?"**
   - "Sim! Updates gratuitos sempre que houver mudanças nas plataformas."

7. **"Como acesso o curso após a compra?"**
   - "Imediatamente! Você receberá email com login e senha na hora."

**Where to add**: Checkout → Seção "Perguntas Frequentes" (custom HTML or use Hotmart FAQ module)

---

## STEP 6: Add Trust Elements

**6.1 Trust Badges:**

Add these elements to increase credibility:

- ✅ **Certificado SSL**: "Pagamento 100% Seguro" (Hotmart includes by default)
- ✅ **Bandeiras de Cartão**: Visa, Mastercard, Amex logos
- ✅ **Garantia**: Shield icon + "7 Dias de Garantia"
- ✅ **Suporte**: "Suporte em até 24h" (if you offer)
- ✅ **Política de Privacidade**: Link to privacy page (LGPD compliance)

**Where to add**: Checkout → Personalização → Elementos de Confiança

Upload badge images (PNG, 100x100px each) or use Hotmart defaults.

---

**6.2 Social Proof:**

Add testimonials or stats:

- "**Mais de 500 alunos** já transformaram seus negócios"
- "⭐⭐⭐⭐⭐ **4.9/5** de avaliação média (230 reviews)"
- "**João Silva** faturou R$ 15k no primeiro mês após o curso"

**Where to add**: Checkout → Descrição → Seção de Depoimentos

Include:
- Student name (first name + last initial for privacy)
- Photo (if authorized)
- Result/transformation (specific, measurable)
- Avoid: Fake testimonials (violates Hotmart policy, risks ban)

---

**6.3 Scarcity/Urgency (Optional, Use Ethically):**

Only if TRUE:

- ✅ "Vagas limitadas: Restam 12 vagas nesta turma" (if cohort-based)
- ✅ "Bônus expira em 48h" (if launch promotion)
- ✅ "Preço sobe para R$ 997 em 3 dias" (if real price increase)
- ❌ Fake countdown timers (unethical, harms brand)
- ❌ "Últimas vagas!" (if digital product with unlimited capacity)

**Where to add**: Checkout → Banner Superior (top bar with countdown)

---

## STEP 7: Configure Offers & Pricing

**7.1 Create Main Offer:**

1. Go to: **Produtos → [Seu Produto] → Ofertas → Criar Oferta**
2. **Nome da Oferta** (internal): "Oferta Principal - Lançamento 2025"
3. **Tipo de Oferta**:
   - **Pagamento Único** (one-time purchase)
   - **Assinatura** (recurring monthly/yearly)
4. **Preço**:
   - Single: R$ [value] (e.g., R$ 497)
   - Subscription: R$ [value]/mês (e.g., R$ 97/mês)
5. **Moeda**: BRL (Real)
6. **Parcelamento**: Enable, max [X]x (e.g., 12x de R$ 49,90)
7. **Garantia**: [7/15/30] dias
8. **Status**: Ativa (Active)
9. Save

**7.2 Add Bonuses (Optional):**

Under offer settings:

1. Click **"+ Adicionar Bônus"**
2. Bonus 1:
   - Name: "Template Pack de Anúncios (Valor: R$ 197)"
   - Description: "50 templates prontos de copy"
   - Image: 400x400px product mockup
3. Bonus 2:
   - Name: "Acesso ao Grupo VIP no WhatsApp (Valor: R$ 97/mês)"
   - Description: "Suporte e networking com outros alunos"
4. Save bonuses
5. Bonuses display on checkout as "Você também recebe:"

**Pro Tip**: Anchor pricing with bonuses (e.g., "Valor total: R$ 1.291, Hoje: R$ 497")

---

**7.3 Create Upsell/Downsell (Advanced):**

After main offer purchase:

1. **Upsell**: Premium offer (e.g., "+ Consultoria 1-on-1: R$ 997")
   - Shown on thank-you page after checkout
   - One-click purchase (no re-entering card)
2. **Downsell**: Cheaper alternative (e.g., "Só o Módulo Anúncios: R$ 197")
   - Shown if main offer declined

**To configure**:
- Produtos → [Seu Produto] → Ofertas → Funil de Vendas (Sales Funnel)
- Create upsell/downsell offers
- Set triggers (show upsell after purchase, downsell after decline)
- Save

---

## STEP 8: Generate Checkout Link

1. Go to: **Produtos → [Seu Produto] → Ofertas → [Oferta Principal]**
2. Find: **"Link de Pagamento"** (Payment Link)
3. Copy full URL: `https://pay.hotmart.com/X12345678Y?off=abcd1234`
4. **Customize URL** (optional):
   - Add UTM parameters for tracking:
     ```
     ?off=abcd1234&utm_source=instagram&utm_medium=stories&utm_campaign=lancamento_jan2025
     ```
   - Track which traffic sources convert best
5. Use link shortener (bitly, rebrandly) for cleaner URLs:
   - Long: `https://pay.hotmart.com/X12345678Y?off=abcd1234`
   - Short: `curso.com.br/comprar` (redirect to Hotmart)

---

## STEP 9: Configure Recovery Flows

**Why**: 60-70% of checkout visitors abandon cart. Recovery flows recapture 10-20% of lost sales.

**9.1 Cart Abandonment Recovery:**

1. Go to: **Produtos → [Seu Produto] → Marketing → Recuperação de Carrinho**
2. Enable: ✅ Ativar Recuperação Automática
3. **Email Sequence**:
   - **Email 1** (1 hour after abandonment):
     - Subject: "Ainda tem dúvida sobre o [Curso]?"
     - Body: Address common objection + guarantee reminder
     - CTA: "Voltar para o Checkout"
   - **Email 2** (24 hours):
     - Subject: "[Nome], sua vaga ainda está reservada por 24h"
     - Body: Scarcity + social proof
     - CTA: "Garantir Minha Vaga Agora"
   - **Email 3** (48 hours):
     - Subject: "Última chance: Bônus expira em 6 horas"
     - Body: Urgency + FOMO
     - CTA: "Não Perder Esta Oportunidade"
4. Customize email templates (Hotmart provides defaults)
5. Save and activate

---

**9.2 Pending Payment Recovery (Boleto/PIX):**

For boleto (takes 1-3 days to clear):

1. Go to: **Produtos → [Seu Produto] → Marketing → Recuperação de Boleto**
2. Enable: ✅ Ativar
3. **Email Reminders**:
   - **24h before expiration**: "Seu boleto expira amanhã! Pague agora para garantir acesso"
   - **Day of expiration**: "URGENTE: Boleto expira hoje às 23h59"
4. **Alternative Payment Offer**:
   - "Prefere pagar com cartão? Clique aqui para trocar" (link to checkout with card pre-selected)
5. Save

For PIX parcelado (installment PIX, if available):
- Similar flow: Remind before expiration
- Offer card as alternative

---

## STEP 10: Test Checkout (Critical)

**10.1 Create Test Coupon:**

1. Go to: **Produtos → [Seu Produto] → Cupons → Criar Cupom**
2. **Código**: TESTE100 (internal use only)
3. **Desconto**: 100% (free test purchase)
4. **Validade**: Today only (expire after testing)
5. **Uso máximo**: 5 uses (you + team)
6. Save

---

**10.2 Run Full Test Purchase:**

1. Open checkout link in **incognito/private browser**
2. Enter test data:
   - Name: Test Student
   - Email: yourtest+1@gmail.com (Gmail + trick for multiple tests)
   - CPF: Use CPF generator (geradorcpf.com) - test CPF only
3. Apply test coupon: TESTE100
4. Select payment method: **Cartão** (credit card)
5. Enter test card (Hotmart provides test card numbers):
   - Approved: 4111 1111 1111 1111, CVV: 123, Exp: 12/30
   - Declined: 4000 0000 0000 0002 (to test error handling)
6. Complete purchase

---

**10.3 Verify Full Flow:**

After test purchase, check:

- [ ] **Email confirmation**: Received within 2 minutes
- [ ] **Club access**: Login works, all modules visible (or dripped correctly)
- [ ] **Welcome email**: Received (if configured)
- [ ] **Thank-you page**: Displays correctly, upsell shown (if configured)
- [ ] **Mobile experience**: Repeat test on phone
- [ ] **Analytics tracking**: Purchase event fired (check FB Pixel, Google Analytics)
- [ ] **Invoice generated**: Available in Hotmart panel
- [ ] **Refund process**: Test refund (optional, to verify guarantee flow)

If any issue: Fix and retest. **DO NOT launch** until all checks pass.

---

**10.4 Deactivate Test Coupon:**

1. Go to: **Cupons → [TESTE100] → Status: Inativo**
2. Save (prevents accidental public use)

---

## STEP 11: A/B Testing (Post-Launch Optimization)

After 50-100 sales, optimize with A/B tests:

**Test 1: Headline**
- Version A: "Domine E-Commerce em 30 Dias"
- Version B: "Fature R$ 10k/mês com E-Commerce"
- Winner: Higher conversion rate (track in Google Optimize or Hotmart native A/B)

**Test 2: Guarantee Period**
- Version A: 7 days guarantee
- Version B: 30 days guarantee
- Hypothesis: Longer guarantee = higher trust = higher conversion (test it!)

**Test 3: Payment Methods Display**
- Version A: All methods visible by default
- Version B: Card pre-selected, others in dropdown
- Winner: Version with lower cart abandonment

**Test 4: Social Proof Placement**
- Version A: Testimonials above checkout form
- Version B: Testimonials below checkout form
- Winner: Version with higher scroll-to-purchase rate

**How to A/B test in Hotmart**:
- Create 2 offers with different settings (e.g., Oferta A, Oferta B)
- Split traffic 50/50 (use URL rotator or ad platform split)
- Run for 7-14 days or until statistical significance (min 50 conversions per variation)
- Implement winner, archive loser

---

### C - Constraints

**Technical Limits:**
- Max offers per product: 50
- Max coupons per product: Unlimited
- Max bonuses per offer: 10
- Checkout load time: <3 seconds (Hotmart optimized)
- Mobile responsive: Automatic (Hotmart handles)

**Payment Processing:**
- Hotmart fee: 9.9% + R$ 1.00 per transaction (Brazilian sales)
- International: 14.9% (PayPal, Stripe)
- Payout schedule: 15-30 days after purchase (depending on payment method)
- Minimum payout: R$ 50 (accumulated balance)

**Compliance Requirements:**
- Privacy policy link: Mandatory (LGPD)
- Refund policy: Must be visible on checkout
- No false claims: Hotmart reviews and can reject checkout pages
- No absolute income promises: "Guaranteed R$ 10k" = REJECTED
- Use disclaimers: "Results vary based on effort"

**Best Practices:**
- ✅ Test checkout on 3+ browsers (Chrome, Firefox, Safari)
- ✅ Test on mobile (40-60% of traffic)
- ✅ Load time <3 seconds (compress images, remove heavy scripts)
- ✅ Clear CTA above the fold (visible without scrolling)
- ✅ Max 2-3 form fields (more = friction)
- ❌ Don't overload with popups (exit intent OK, but limit to 1)
- ❌ Don't auto-play video with sound (user experience killer)
- ❌ Don't hide guarantee (transparency = trust)

---

### E - Example

**Scenario**: Launching "Curso CODEXA - IA para E-Commerce" with optimized checkout

**Input:**
- Product approved in Hotmart
- Pricing: R$ 497 (12x de R$ 49,90)
- Guarantee: 7 days
- Target: 100 sales in first month
- Traffic source: Instagram ads

**Execution:**

**Day 1: Visual Setup**
1. Upload logo (300x90px, transparent PNG)
2. Set colors: Primary #FF5733, Secondary #333, Background #FFF
3. Add header image: 1200x400px with course cover + headline
4. Preview on desktop + mobile → Looks good ✅

**Day 2: Payment & Copy**
5. Enable payment methods: Card (12x), PIX, Boleto
6. Set installments: Max 12x, min R$ 40 per installment, 0% interest (absorb fees)
7. Write checkout copy:
   - Headline: "Domine IA para E-Commerce em 30 Dias e Fature Mais sem Contratar Agência"
   - Bullets: 8 benefits (modules, templates, support, lifetime access)
   - CTA: "Quero Dominar IA Agora"
   - Guarantee: "7 dias para testar. Se não gostar, devolvo 100%."
8. Add FAQ: 7 common objections answered

**Day 3: Trust & Offers**
9. Add trust badges: SSL, card brands, guarantee shield
10. Add social proof: "326 alunos já faturaram R$ 10k+ após o curso"
11. Create main offer: R$ 497, 12x, active
12. Add bonuses: Template pack (R$ 197) + WhatsApp group (R$ 97/mês)
13. Calculate anchor: "Valor total R$ 1.488, Hoje R$ 497"

**Day 4: Recovery & Testing**
14. Configure cart abandonment: 3-email sequence (1h, 24h, 48h)
15. Configure boleto recovery: Reminder 24h before expiration
16. Create test coupon: TESTE100 (100% off, 5 uses, expires today)
17. Run test purchase:
    - Desktop Chrome: ✅ Works
    - Mobile Safari: ✅ Works
    - Email received: ✅ Within 2 min
    - Club access: ✅ Login successful
18. Deactivate test coupon

**Day 5: Launch**
19. Generate checkout link with UTM:
    `https://pay.hotmart.com/X12345678Y?off=abc123&utm_source=instagram&utm_medium=cpc&utm_campaign=lancamento_jan2025`
20. Shorten URL: curso.com.br/comprar (redirect to Hotmart)
21. Launch Instagram ads → Traffic to checkout
22. Monitor first 10 sales:
    - Conversion rate: 18% (good!)
    - Payment method: 70% card, 20% PIX, 10% boleto
    - Avg time to purchase: 4 min (fast = good copy)

**Week 2: Optimize**
23. A/B test headline:
    - Version A (current): "Domine IA para E-Commerce em 30 Dias..."
    - Version B (new): "Fature R$ 15k/mês com IA para E-Commerce (Sem Programar)"
24. Run test for 7 days, 50 conversions per version
25. Result: Version B wins (22% conversion vs. 18%)
26. Implement Version B, archive Version A

**Month 1 Results:**
- 127 sales (exceeded goal of 100)
- R$ 63,119 gross revenue
- R$ 56,807 net (after Hotmart fees + refunds)
- Refund rate: 4% (excellent, below 8% target)
- Avg checkout time: 3.5 min (fast decision)
- Recovery flows recovered 18 sales (14% recovery rate)

**Output**: High-converting checkout generating R$ 56k+ net in first month ✅

---

## 🎯 SUCCESS CHECKLIST

Before going live:

- [ ] Checkout visual customized (logo, colors, header)
- [ ] Payment methods enabled (card, PIX, boleto)
- [ ] Installments configured (max 12x, min R$ 30-50)
- [ ] Checkout copy written (headline, bullets, CTA, FAQ)
- [ ] Trust elements added (badges, social proof, guarantee)
- [ ] Main offer created and activated
- [ ] Bonuses added (if applicable)
- [ ] Recovery flows configured (cart abandonment, boleto)
- [ ] Test purchase completed successfully
- [ ] Mobile experience verified
- [ ] Analytics tracking confirmed (FB Pixel, GA)
- [ ] Checkout link generated and shortened

---

## 🚨 TROUBLESHOOTING

**Problem 1: Low conversion rate (<5%)**
- **Cause**: Weak copy, no trust elements, hidden guarantee
- **Solution**: Add social proof, move guarantee above fold, simplify CTA

**Problem 2: High cart abandonment (>70%)**
- **Cause**: Too many form fields, slow load time, no payment options
- **Solution**: Remove optional fields, compress images, enable PIX

**Problem 3: High refund rate (>15%)**
- **Cause**: Misleading checkout copy, product doesn't match promise
- **Solution**: Align copy with actual product, improve onboarding (Aula 0)

**Problem 4: Payments not processing**
- **Cause**: Payment gateway issue, card declined, CPF invalid
- **Solution**: Verify Hotmart payment settings, test with valid test card, check error logs

**Problem 5: Checkout link not working**
- **Cause**: Offer not activated, product not approved
- **Solution**: Verify offer status = "Ativa", product status = "Aprovado"

---

## 📚 REFERENCES

**Official Hotmart Guides:**
- Checkout Config: https://help.hotmart.com/pt-br/article/360038937471
- Custom Checkout: https://help.hotmart.com/pt-br/article/115003134331
- Payment Methods: https://help.hotmart.com/pt-br/article/25588460435085
- Offers: https://help.hotmart.com/pt-br/article/215827788
- Coupons: https://help.hotmart.com/pt-br/article/360015325411
- Recovery Flows: https://help.hotmart.com/pt-br/article/360062099252

**Tools:**
- **Hotmart Checkout Simulator**: Test checkout before launch
- **UTM Builder**: ga-dev-tools.google/campaign-url-builder
- **Image Compression**: tinypng.com (optimize header images)
- **CPF Generator**: geradorcpf.com (test CPFs only!)

**Conversion Benchmarks (Hotmart):**
- Excellent: >20% checkout conversion
- Good: 10-20%
- Average: 5-10%
- Poor: <5% (requires optimization)

---

**Version**: 1.0.0
**Created**: 2025-11-20
**TAC-7**: ✅ Compliant
**Integration-Ready**: ✅ Yes
**Tested**: ✅ Production-Ready

**💳 Checkout Optimized | 📈 Conversion-Focused | 🔄 Recovery Enabled**
