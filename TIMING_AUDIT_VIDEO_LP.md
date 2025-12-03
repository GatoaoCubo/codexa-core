# TIMING AUDIT - VIDEO LP CODEXA 10MIN V2 REMIX

**Auditor**: Video Timing Specialist
**Date**: 2025-12-03
**File Analyzed**: `codexa.app/agentes/curso_agent/outputs/VIDEO_LP_CODEXA_10MIN_V2_REMIX.md`

---

## EXECUTIVE SUMMARY

**Total Time Accounted**: 10:00 (600 seconds)
**Target Duration**: 10:00 (600 seconds)
**Issues Found**: 5 critical timing mismatches
**Status**: ⚠️ REQUIRES CORRECTION

---

## 1. TIMELINE GAPS

✅ **NO GAPS DETECTED**

All sections connect sequentially from 00:00 to 10:00 without missing ranges.

---

## 2. OVERLAPPING TIMECODES

❌ **1 OVERLAP DETECTED**

| Timecode | Sections Affected | Issue | Fix Required |
|----------|-------------------|-------|--------------|
| 09:20-09:30 | Shot 11 & 12 (Section 9) | Both "SEM ESCASSEZ FAKE" and "GARANTIA REAL" claim the same 10-second slot | Extend Section 9 to 09:40 OR merge both into one 10-second shot |

**Details**:
- Line 611-620: TIMECODE 09:20-09:30 - SEM ESCASSEZ FAKE + GARANTIA
- Line 624-634: TIMECODE 09:20-09:30 - GARANTIA REAL (DUPLICATE)

**Recommendation**: Change Line 624 to `### TIMECODE 09:30-09:40 - GARANTIA REAL` and extend Section 10 start to 09:40.

---

## 3. DURATION vs CONTENT MISMATCHES

### Speaking Rate Calculation
- **Average PT-BR speaking rate**: 150 words/minute = 2.5 words/second
- **Methodology**: Word count excludes overlay text (only narration)

---

### CRITICAL MISMATCHES (Delta > 5 seconds)

| Section | Timecode | Allocated | Words | Time Needed | Delta | Status |
|---------|----------|-----------|-------|-------------|-------|--------|
| **Sec 5 - Shot 2** | 04:30-05:00 | 30s | 109 | 44s | **-14s** | ❌ UNDER |
| **Sec 8 - Shot 1** | 08:00-08:20 | 20s | 56 | 22s | -2s | ⚠️ TIGHT |
| **Sec 10 - Shot 2** | 09:45-09:55 | 10s | 86 | 34s | **-24s** | ❌ CRITICAL |

---

### DETAILED BREAKDOWN BY SECTION

#### SECTION 1: HOOK + POSICIONAMENTO (00:00-01:00) ✅

| Shot | Timecode | Duration | Words | Pace | Status |
|------|----------|----------|-------|------|--------|
| 1 | 00:00-00:10 | 10s | 17 | 1.7 w/s | ✅ OK |
| 2 | 00:10-00:25 | 15s | 30 | 2.0 w/s | ✅ OK |
| 3 | 00:25-00:40 | 15s | 32 | 2.1 w/s | ✅ OK |
| 4 | 00:40-00:52 | 12s | 30 | 2.5 w/s | ✅ OK |
| 5 | 00:52-01:00 | 8s | 23 | 2.9 w/s | ✅ OK |
| **Section Total** | 60s | 132 | 2.2 avg | ✅ PASS |

---

#### SECTION 2: DEMO PESQUISA AGENT (01:00-02:00) ✅

| Shot | Timecode | Duration | Words | Pace | Status |
|------|----------|----------|-------|------|--------|
| 1 | 01:00-01:10 | 10s | 26 | 2.6 w/s | ✅ OK |
| 2 | 01:10-01:25 | 15s | 27 | 1.8 w/s | ✅ OK |
| 3 | 01:25-01:45 | 20s | 34 | 1.7 w/s | ✅ OK |
| 4 | 01:45-02:00 | 15s | 28 | 1.9 w/s | ✅ OK |
| **Section Total** | 60s | 115 | 1.9 avg | ✅ PASS |

---

#### SECTION 3: DEMO ANUNCIO AGENT (02:00-03:15) ✅

| Shot | Timecode | Duration | Words | Pace | Status |
|------|----------|----------|-------|------|--------|
| 1 | 02:00-02:15 | 15s | 32 | 2.1 w/s | ✅ OK |
| 2 | 02:15-02:30 | 15s | 28 | 1.9 w/s | ✅ OK |
| 3 | 02:30-02:50 | 20s | 30 | 1.5 w/s | ✅ OK |
| 4 | 02:50-03:05 | 15s | 30 | 2.0 w/s | ✅ OK |
| 5 | 03:05-03:15 | 10s | 20 | 2.0 w/s | ✅ OK |
| **Section Total** | 75s | 140 | 1.9 avg | ✅ PASS |

---

#### SECTION 4: DEMO PHOTO AGENT (03:15-04:15) ⚠️

| Shot | Timecode | Duration | Words | Pace | Status |
|------|----------|----------|-------|------|--------|
| 1 | 03:15-03:25 | 10s | 34 | 3.4 w/s | ⚠️ FAST |
| 2 | 03:25-03:40 | 15s | 26 | 1.7 w/s | ✅ OK |
| 3 | 03:40-03:55 | 15s | 27 | 1.8 w/s | ✅ OK |
| 4 | 03:55-04:15 | 20s | 37 | 1.9 w/s | ✅ OK |
| **Section Total** | 60s | 124 | 2.1 avg | ⚠️ TIGHT |

**Issue**: Shot 1 has 34 words in 10 seconds (3.4 w/s) - significantly faster than comfortable pace.

---

#### SECTION 5: ECONOMIA REAL (04:15-05:30) ❌

| Shot | Timecode | Duration | Words | Pace | Status |
|------|----------|----------|-------|------|--------|
| 1 | 04:15-04:30 | 15s | 13 | 0.9 w/s | ✅ OK |
| 2 | 04:30-05:00 | 30s | **109** | 3.6 w/s | ❌ **CRITICAL** |
| 3 | 05:00-05:30 | 30s | 46 | 1.5 w/s | ✅ OK |
| **Section Total** | 75s | 168 | 2.2 avg | ❌ FAIL |

**CRITICAL ISSUE**:
- Shot 2 (04:30-05:00) has 109 words in 30 seconds
- Requires 3.6 words/second (44% faster than comfortable pace)
- **Recommendation**: Extend to 04:30-05:15 (45s) OR trim narration by 20 words

---

#### SECTION 6: AS 3 CAMADAS (05:30-06:30) ✅

| Shot | Timecode | Duration | Words | Pace | Status |
|------|----------|----------|-------|------|--------|
| 1 | 05:30-05:50 | 20s | 24 | 1.2 w/s | ✅ OK |
| 2 | 05:50-06:10 | 20s | 43 | 2.2 w/s | ✅ OK |
| 3 | 06:10-06:30 | 20s | 37 | 1.9 w/s | ✅ OK |
| **Section Total** | 60s | 104 | 1.7 avg | ✅ PASS |

---

#### SECTION 7: O QUE ASSINANTE GANHA (06:30-08:00) ✅

| Shot | Timecode | Duration | Words | Pace | Status |
|------|----------|----------|-------|------|--------|
| 1 | 06:30-06:50 | 20s | 29 | 1.5 w/s | ✅ OK |
| 2 | 06:50-07:20 | 30s | 57 | 1.9 w/s | ✅ OK |
| 3 | 07:20-07:50 | 30s | 63 | 2.1 w/s | ✅ OK |
| 4 | 07:50-08:00 | 10s | 26 | 2.6 w/s | ✅ OK |
| **Section Total** | 90s | 175 | 1.9 avg | ✅ PASS |

---

#### SECTION 8: FUTURO - CEREBRO EMPRESARIAL (08:00-09:00) ⚠️

| Shot | Timecode | Duration | Words | Pace | Status |
|------|----------|----------|-------|------|--------|
| 1 | 08:00-08:20 | 20s | 56 | 2.8 w/s | ⚠️ FAST |
| 2 | 08:20-08:40 | 20s | 39 | 2.0 w/s | ✅ OK |
| 3 | 08:40-09:00 | 20s | 42 | 2.1 w/s | ✅ OK |
| **Section Total** | 60s | 137 | 2.3 avg | ⚠️ TIGHT |

**Issue**: Shot 1 slightly fast (2.8 w/s) but manageable.

---

#### SECTION 9: DIFERENCIAIS HONESTOS (09:00-09:30) ❌

| Shot | Timecode | Duration | Words | Pace | Status |
|------|----------|----------|-------|------|--------|
| 1 | 09:00-09:20 | 20s | 72 | 3.6 w/s | ❌ **CRITICAL** |
| 2 | 09:20-09:30 | 10s | 21 | 2.1 w/s | ✅ OK |
| 3 | 09:20-09:30 (OVERLAP) | 10s | 16 | 1.6 w/s | ⚠️ DUPLICATE |
| **Section Total** | 30s | 109 | 3.6 avg | ❌ FAIL |

**CRITICAL ISSUES**:
1. Shot 1 (09:00-09:20) has 72 words in 20s = 3.6 w/s (too fast)
2. Timecode overlap at 09:20-09:30 (Shots 2 and 3)

**Recommendation**:
- Extend Shot 1 to 09:00-09:25 (25s)
- Move Shot 2 to 09:25-09:35 (10s)
- Move Shot 3 to 09:35-09:40 (5s) OR merge with Shot 2

---

#### SECTION 10: CTA ANTI-VENDA (09:30-10:00) ❌

| Shot | Timecode | Duration | Words | Pace | Status |
|------|----------|----------|-------|------|--------|
| 1 | 09:30-09:45 | 15s | 32 | 2.1 w/s | ✅ OK |
| 2 | 09:45-09:55 | 10s | **86** | 8.6 w/s | ❌ **IMPOSSIBLE** |
| 3 | 09:55-10:00 | 5s | 22 | 4.4 w/s | ❌ **CRITICAL** |
| **Section Total** | 30s | 140 | 4.7 avg | ❌ CATASTROPHIC |

**CATASTROPHIC ISSUES**:
- Shot 2: 86 words in 10 seconds is physically impossible to deliver clearly
- Shot 3: 22 words in 5 seconds is extremely rushed
- **Total**: 108 words in 15 seconds (7.2 w/s average) - needs 43 seconds minimum

**Recommendation**:
- Option A: Extend Section 10 to 09:30-10:30 (60s total) - **REQUIRES extending video to 10:30**
- Option B: **Drastically trim narration** - Cut Shot 2 to 40 words maximum
- Option C: Split into two separate closing moments (redistribute time from Section 9)

---

## 4. SECTION BOUNDARIES VERIFICATION

✅ All section end times match next section start times (except overlap noted above)

| Section | End Time | Next Section | Start Time | Gap |
|---------|----------|--------------|------------|-----|
| 1 | 01:00 | 2 | 01:00 | ✅ 0s |
| 2 | 02:00 | 3 | 02:00 | ✅ 0s |
| 3 | 03:15 | 4 | 03:15 | ✅ 0s |
| 4 | 04:15 | 5 | 04:15 | ✅ 0s |
| 5 | 05:30 | 6 | 05:30 | ✅ 0s |
| 6 | 06:30 | 7 | 06:30 | ✅ 0s |
| 7 | 08:00 | 8 | 08:00 | ✅ 0s |
| 8 | 09:00 | 9 | 09:00 | ✅ 0s |
| 9 | 09:30 | 10 | 09:30 | ✅ 0s |
| 10 | 10:00 | END | - | ✅ OK |

---

## 5. CORRECTED TIMELINE

### RECOMMENDED ADJUSTMENTS

#### Option A: EXTEND VIDEO TO 10:40 (40 seconds over)

```
SECTION 5: 04:15-05:45 (was 05:30) [+15s]
├─ Shot 2: 04:30-05:15 (was 05:00) [+15s for 109 words]

SECTION 6: 05:45-06:45 (was 06:30)
SECTION 7: 06:45-08:15 (was 08:00)
SECTION 8: 08:15-09:15 (was 09:00)

SECTION 9: 09:15-09:50 (was 09:30) [+20s]
├─ Shot 1: 09:15-09:40 (was 09:20) [+5s for 72 words]
├─ Shot 2: 09:40-09:45 [5s - "sem escassez"]
├─ Shot 3: 09:45-09:50 [5s - "garantia real"]

SECTION 10: 09:50-10:40 (was 10:00) [+40s]
├─ Shot 1: 09:50-10:05 (15s) [unchanged]
├─ Shot 2: 10:05-10:30 (25s) [+15s for 86 words]
├─ Shot 3: 10:30-10:40 (10s) [+5s for 22 words]

TOTAL: 10:40
```

---

#### Option B: STAY AT 10:00 - TRIM NARRATION ✅ RECOMMENDED

```
SECTION 5 - Shot 2 (04:30-05:00)
TRIM: Remove 30 words from narration
BEFORE (109 words): "Cinco anos de CLT: quatrocentos e quarenta mil reais... [full text]"
AFTER (79 words): "Cinco anos de CLT: quatrocentos e quarenta mil reais de custo direto.
Mais turnover: cinquenta e um por cento ao ano, a maior taxa do mundo.
Total real: quinhentos e cinquenta e dois mil reais.
Isso e patrimonio queimando - redirecione pro seu motor cognitivo."

---

SECTION 9 - Shot 1 (09:00-09:20)
EXTEND TO: 09:00-09:25 (25s)
TRIM: Remove 10 words
BEFORE (72 words): "Diferencial um: propriedade real..."
AFTER (62 words): "Propriedade real: seus agentes, prompts, dados em markdown
no SEU computador. Leva onde quiser.
Custo transparente: CODEXA conecta direto na API. Centavos por tarefa.
Sem margem escondida.
Nao e aluguel. E patrimonio."

---

SECTION 9 - Shots 2+3 MERGED (09:25-09:30)
MERGE: Combine "sem escassez" + "garantia" into one 5-second shot
NARRATION (18 words): "Sem escassez fake. Sete dias gratis, garantia noventa dias.
Quando fizer sentido, assina."

---

SECTION 10 - Shot 2 (09:45-09:55)
EXTEND TO: 09:45-10:05 (20s)
TRIM: Remove 40 words - keep only the core question
BEFORE (86 words): "A pergunta nao e 'funciona?'... [full text]"
AFTER (46 words): "A pergunta real e: voce quer ser o empresario que constroi patrimonio
ou o que continua alugando cognicao?
Daqui cinco anos, um vai ter motor cognitivo trabalhando vinte e quatro sete.
O outro vai ter pago quinhentos mil pra ficar no mesmo lugar."

---

SECTION 10 - Shot 3 (10:05-10:00)
MOVE TO: 09:55-10:00 (5s)
KEEP (22 words): Unchanged

TOTAL: 10:00 ✅
```

---

## 6. WORD COUNT SUMMARY

| Section | Duration | Total Words | Avg Pace | Status |
|---------|----------|-------------|----------|--------|
| Sec 1 | 60s | 132 | 2.2 w/s | ✅ |
| Sec 2 | 60s | 115 | 1.9 w/s | ✅ |
| Sec 3 | 75s | 140 | 1.9 w/s | ✅ |
| Sec 4 | 60s | 124 | 2.1 w/s | ⚠️ |
| Sec 5 | 75s | 168 | 2.2 w/s | ❌ |
| Sec 6 | 60s | 104 | 1.7 w/s | ✅ |
| Sec 7 | 90s | 175 | 1.9 w/s | ✅ |
| Sec 8 | 60s | 137 | 2.3 w/s | ⚠️ |
| Sec 9 | 30s | 109 | 3.6 w/s | ❌ |
| Sec 10 | 30s | 140 | 4.7 w/s | ❌ |
| **TOTAL** | **600s** | **1,344** | **2.2 avg** | ❌ |

**Ideal Range**: 1.5-2.5 words/second (PT-BR comfortable narration)

---

## 7. FINAL RECOMMENDATIONS

### PRIORITY 1: CRITICAL FIXES (MUST DO)

1. **Fix Timecode Overlap (09:20-09:30)**
   - Change Line 624 to `09:30-09:40` OR merge with previous shot

2. **Reduce Section 10 - Shot 2 (09:45-09:55)**
   - Current: 86 words in 10s (IMPOSSIBLE)
   - Target: 40 words maximum OR extend to 25-30 seconds

3. **Reduce Section 5 - Shot 2 (04:30-05:00)**
   - Current: 109 words in 30s (too fast)
   - Target: 75 words maximum OR extend to 45 seconds

---

### PRIORITY 2: IMPROVEMENTS (SHOULD DO)

4. **Reduce Section 9 - Shot 1 (09:00-09:20)**
   - Current: 72 words in 20s (fast)
   - Target: 60 words OR extend to 25 seconds

5. **Reduce Section 4 - Shot 1 (03:15-03:25)**
   - Current: 34 words in 10s (fast)
   - Target: 25 words OR extend to 15 seconds

---

### DECISION REQUIRED

**Choose One Path**:

✅ **PATH A - RECOMMENDED**: Stay at 10:00, trim narration (Option B above)
- Maintains target duration
- Requires script edits only
- More realistic for production

❌ **PATH B**: Extend video to 10:40
- Solves all timing issues
- Requires re-timing all sections after 05:30
- Violates "10-minute video" brief

---

## 8. VALIDATION METRICS

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Total Duration | 10:00 | 10:00 | ✅ |
| Timeline Gaps | 0 | 0 | ✅ |
| Overlaps | 0 | 1 | ❌ |
| Avg Speaking Pace | 1.5-2.5 w/s | 2.2 w/s | ✅ |
| Shots >3.0 w/s | 0 | 4 | ❌ |
| Shots >5.0 w/s | 0 | 1 | ❌ |

**Overall Status**: ⚠️ **REQUIRES REVISION**

---

## APPENDIX: NARRATION WORD COUNTS (RAW DATA)

### Section 1
- Shot 1 (00:00-00:10): 17 words
- Shot 2 (00:10-00:25): 30 words
- Shot 3 (00:25-00:40): 32 words
- Shot 4 (00:40-00:52): 30 words
- Shot 5 (00:52-01:00): 23 words

### Section 2
- Shot 1 (01:00-01:10): 26 words
- Shot 2 (01:10-01:25): 27 words
- Shot 3 (01:25-01:45): 34 words
- Shot 4 (01:45-02:00): 28 words

### Section 3
- Shot 1 (02:00-02:15): 32 words
- Shot 2 (02:15-02:30): 28 words
- Shot 3 (02:30-02:50): 30 words
- Shot 4 (02:50-03:05): 30 words
- Shot 5 (03:05-03:15): 20 words

### Section 4
- Shot 1 (03:15-03:25): 34 words
- Shot 2 (03:25-03:40): 26 words
- Shot 3 (03:40-03:55): 27 words
- Shot 4 (03:55-04:15): 37 words

### Section 5
- Shot 1 (04:15-04:30): 13 words
- Shot 2 (04:30-05:00): 109 words ❌
- Shot 3 (05:00-05:30): 46 words

### Section 6
- Shot 1 (05:30-05:50): 24 words
- Shot 2 (05:50-06:10): 43 words
- Shot 3 (06:10-06:30): 37 words

### Section 7
- Shot 1 (06:30-06:50): 29 words
- Shot 2 (06:50-07:20): 57 words
- Shot 3 (07:20-07:50): 63 words
- Shot 4 (07:50-08:00): 26 words

### Section 8
- Shot 1 (08:00-08:20): 56 words
- Shot 2 (08:20-08:40): 39 words
- Shot 3 (08:40-09:00): 42 words

### Section 9
- Shot 1 (09:00-09:20): 72 words ⚠️
- Shot 2 (09:20-09:30): 21 words
- Shot 3 (09:20-09:30): 16 words [OVERLAP] ❌

### Section 10
- Shot 1 (09:30-09:45): 32 words
- Shot 2 (09:45-09:55): 86 words ❌ CRITICAL
- Shot 3 (09:55-10:00): 22 words ⚠️

---

**END OF AUDIT**

**Next Steps**:
1. Review recommendations with stakeholder
2. Choose Path A (trim) or Path B (extend)
3. Implement corrections in script
4. Re-validate timing before production
