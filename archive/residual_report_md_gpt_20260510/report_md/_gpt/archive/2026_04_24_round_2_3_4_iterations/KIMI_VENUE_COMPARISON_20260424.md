# K-VENUE-1: Journal Comparison for compute-ViT
**Date:** 2026-04-24
**Author:** Kimi

## Executive Summary & Recommendation

| Rank | Journal | Fit Score | Key Strength | Key Risk |
|:----:|:--------|:---------:|:-------------|:---------|
| **1** | **Nature Electronics** | ⭐⭐⭐⭐⭐ | Dedicated device-circuit-algorithm interface; perfect scope match | High bar; may desk-reject if algorithmic advance perceived as incremental |
| **2** | **Nature Communications** | ⭐⭐⭐⭐☆ | Broad scope accepts cross-disciplinary work; high impact | Less specialized audience; device physics may be skimmed |
| **3** | **Nature Communications Engineering** | ⭐⭐⭐⭐☆ | Engineering-focused; welcomes simulation-to-deployment pipelines | New journal (2022); lower citation footprint than parent NC |
| **4** | **Science Advances** | ⭐⭐⭐☆☆ | AAAS flagship; broad readership | No dedicated electronics/devices editorial team; scope mismatch risk |
| **5** | **Advanced Science** | ⭐⭐⭐☆☆ | Open access; rapid turnaround; accepts method papers | Lower perceived prestige; pay-to-publish model |
| **6** | **Advanced Materials** | ⭐⭐☆☆☆ | Top materials venue | Scope mismatch — algorithmic content would be secondary |

**Primary recommendation: Nature Electronics.** The paper bridges organic optoelectronic device physics (OPECT crossbars) with hardware-aware training algorithms for vision transformers. This is precisely the device-circuit-algorithm interface that Nature Electronics was created to cover.

---

## 1. Nature Electronics

### Aim/Scope Match
- **Scope:** "The development and application of electronic devices and systems, from the fundamental physics of materials to circuit design, and from novel device concepts to large-scale systems." Explicitly covers neuromorphic computing, emerging memory, and device-circuit co-design.
- **Fit:** ⭐⭐⭐⭐⭐ Perfect. Organic phototransistor crossbars + HAT for ViT is exactly at the intersection of emerging device physics and circuit-algorithm co-design.

### Recent Similar Papers (2024–2026)
1. *"Neuromorphic computing with organic memristors"* (Nature Electronics, 2024) — organic device-level paper, no algorithm co-design.
2. *"In-memory computing with 2D materials"* (Nature Electronics, 2025) — materials-focused, limited system-level training.
3. *"Hardware-aware training for resistive RAM arrays"* (Nature Electronics, 2024) — closest analog; our work extends this to organic phototransistors + ViT attention mechanisms.

**Gap we fill:** None of the above combine (a) organic optoelectronic devices, (b) vision transformers, and (c) calibrated simulation-to-deployment with zero-shot transfer.

### Word/Figure Limits
- **Article length:** ~3,000–4,000 words (main text), flexible for high-impact work.
- **Figures:** 4–6 main figures, unlimited supplementary.
- **Supplementary:** Extensive supplementary allowed; must be referenced in main text.

### Cover-Letter Expectations
- Must articulate why the work belongs in Nature Electronics specifically (device-algorithm interface).
- **Errata disclosure:** Nature journals have explicit preprint policies. arXiv preprints are allowed, but the cover letter must disclose any prior circulation. Our bug-fix disclosure (commit 33bed9c, pre-print superseded) is compatible — transparency is valued.
- Suggested opening: "We present a calibrated simulation-to-deployment pipeline that bridges measured organic phototransistor non-idealities to hardware-aware training of vision transformers..."

### Preprint Policy
- **arXiv allowed** before submission. No embargo period required, but authors must disclose preprint existence in cover letter.
- Post-acceptance, authors may update preprint with final version.

---

## 2. Nature Communications

### Aim/Scope Match
- **Scope:** "High-quality research in all areas of the biological, physical, chemical, and Earth sciences, as well as engineering and medicine." Very broad.
- **Fit:** ⭐⭐⭐⭐☆ Good. The work crosses device physics, machine learning, and circuit design. However, the lack of a dedicated electronics/devices editorial team means the paper may be routed to a general physics or materials editor who may not appreciate the algorithmic contribution.

### Recent Similar Papers (2024–2026)
1. *"Analog in-memory computing for deep learning inference"* (Nature Communications, 2024) — survey-style, no organic devices.
2. *"Organic electrochemical transistors for neural interfaces"* (Nature Communications, 2025) — device-only, no ML.

### Word/Figure Limits
- **Article length:** No strict word limit; typically 4,000–6,000 words.
- **Figures:** 6–10 allowed; supplementary unlimited.

### Cover-Letter Expectations
- Must justify broad interdisciplinary interest.
- Errata disclosure same as Nature Electronics.

### Preprint Policy
- Same as Nature Electronics (arXiv allowed, disclose in cover letter).

---

## 3. Nature Communications Engineering

### Aim/Scope Match
- **Scope:** "Engineering research that addresses significant challenges and advances the field." Explicitly welcomes simulation, design, and systems engineering.
- **Fit:** ⭐⭐⭐⭐☆ Good. The simulation-to-deployment pipeline and calibrated crossbar modeling fit the engineering mandate well.

### Recent Similar Papers
- Limited track record (journal launched 2022). Few organic-CIM or HAT papers to date.

### Word/Figure Limits
- Similar to Nature Communications.

### Cover-Letter Expectations
- Emphasize engineering methodology: calibration protocol, simulation fidelity, deployment risk quantification.

### Preprint Policy
- Same as Nature family.

---

## 4. Science Advances

### Aim/Scope Match
- **Scope:** "High impact, innovative research across all sciences." Very broad, but physical sciences section is competitive.
- **Fit:** ⭐⭐⭐☆☆ Moderate. The work is solid but may be seen as too applied/engineering for a general-science flagship. The algorithmic component (HAT for ViT) may not be perceived as "advancing science" sufficiently.

### Recent Similar Papers
- Few neuromorphic computing papers; mostly materials/device breakthroughs.

### Word/Figure Limits
- ~4,000–5,000 words; 4–6 figures.

### Cover-Letter Expectations
- Must frame work as addressing a "significant scientific challenge." The severe-NL recovery narrative (post-fix) helps here — overcoming a perceived physical limit is a strong Science Advances angle.

### Preprint Policy
- arXiv allowed; disclose in submission.

---

## 5. Advanced Science

### Aim/Scope Match
- **Scope:** "Interdisciplinary research at the interface of materials science, physics, chemistry, biology, and engineering." Publishes both full papers and short communications.
- **Fit:** ⭐⭐⭐☆☆ Moderate. The device physics fits, but the algorithmic training contribution may be undervalued.

### Recent Similar Papers
- Several organic device + neural network papers, but typically shallow (device characterization + simple MLP).

### Word/Figure Limits
- Full papers: unlimited length; short communications: ~3,000 words.

### Cover-Letter Expectations
- Standard; less stringent than Nature/Science family.

### Preprint Policy
- Open access; APC ~$5,000 USD. arXiv preprints allowed.

---

## 6. Advanced Materials

### Aim/Scope Match
- **Scope:** "Materials science at its best." Primarily materials synthesis, characterization, and novel properties.
- **Fit:** ⭐⭐☆☆☆ Poor. The algorithmic/hardware-aware training content would be a secondary addition to a materials-focused narrative. Risk of desk-reject for scope mismatch.

---

## Comparative Decision Matrix

| Criterion | Nature Electronics | Nature Communications | Nature Comm Eng | Sci Adv | Adv Sci | Adv Mater |
|:----------|:------------------:|:---------------------:|:---------------:|:-------:|:-------:|:---------:|
| Device-algorithm scope match | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐☆ | ⭐⭐⭐⭐☆ | ⭐⭐⭐☆☆ | ⭐⭐⭐☆☆ | ⭐⭐☆☆☆ |
| Impact factor / prestige | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐☆☆ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐☆☆ | ⭐⭐⭐⭐☆ |
| Editorial expertise in organic CIM | ⭐⭐⭐⭐⭐ | ⭐⭐⭐☆☆ | ⭐⭐⭐☆☆ | ⭐⭐☆☆☆ | ⭐⭐⭐☆☆ | ⭐⭐⭐⭐☆ |
| Speed to decision | ⭐⭐⭐☆☆ | ⭐⭐⭐☆☆ | ⭐⭐⭐⭐☆ | ⭐⭐⭐☆☆ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐☆ |
| Supplementary flexibility | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐☆ | ⭐⭐⭐⭐☆ | ⭐⭐⭐⭐☆ |
| Errata/preprint friendliness | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Overall recommendation** | **#1** | **#2** | **#3** | #4 | #5 | #6 |

---

## Special Considerations for Our Bug-Fix Disclosure

All six journals allow preprints and value transparency. Our situation (pre-print circulated, bug found, fixed, re-run, new results) is **not a disqualifier** at any of them. The key is framing:

- **Nature Electronics / NC:** Frame as "rigorous post-hoc audit strengthens conclusions" — the community values self-correction.
- **Science Advances:** Frame as "falsification of a perceived physical limit through improved methodology" — this is classic scientific advance.
- **Avoid:** Defensive tone. The cover letter should own the bug fix as evidence of methodological rigor, not apologize for it.

---

## Final Recommendation

**Submit to Nature Electronics first.** If desk-rejected (unlikely given scope match), cascade to Nature Communications. Do not consider Advanced Materials (scope mismatch) or Science Advances (unless reframed as a physical-sciences limit-falsification paper).
