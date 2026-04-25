# DISPATCH KIMI R9A — Length Surgery on Paper-1
**Date:** 2026-04-25 22:30 CST
**Issued by:** Claude
**Assignee:** Kimi
**Authority:** CLAUDE_ROUND9_PAPER1_HARDENING_PLAN_20260425 §3 Track A
**Priority:** HIGH (presentation quality fix)
**Time budget:** 3-4 days
**Constraint:** NO new content. Only cuts + light reordering.

---

## 0. Mission

Cut paper-1 main body from **7,332 words → ≤ 5,500 words** (-25 to -28%). Target: Nat Electronics typical full-paper length. Surgical cuts only — preserve every numerical claim, every figure reference, every cite. Aim for **same scientific content, half the prose**.

---

## 1. Per-section cut targets (line-level)

### 1.1 `00_abstract.tex` — KEEP (137 words)
No change. Within Nat Electronics 150-word limit.

### 1.2 `01_introduction.tex` — 784 → 450 words (cut **334 words / -43%**)

**Specific deletions:**

- **Delete §3 (HAT/QAT/domain-randomization paragraph)** entirely. Currently 4 sentences. **Reason**: this content is duplicated in §2.1 Related Work `Hardware-Aware Training and Robustness`. Keep ONE place.
- **Delete §4 (CIM simulators paragraph)** entirely. Currently lists DNN+NeuroSim, MemTorch, AIHWKIT, CrossSim. **Reason**: these are listed identically in §2.3 Related Work. Keep ONE place (Related Work).
- **Delete §5 (organic devices + hybrid mapping paragraph)** entirely. **Reason**: this is the literature setup that belongs in §2.2 Related Work. Currently appears in BOTH places.
- **Compress §6 + §7 (contribution paragraphs)** into ONE paragraph. Currently they say the same 4 contributions twice (once narrative, once enumerated). Keep enumerated form (cleaner). Target: ~120 words for the contribution list.
- **Keep §1, §2, §6 (compressed), §8** = motivation + gap statement + contributions + scope-of-framework caveat.

**Final intro structure** (4 paragraphs, ~450 words):
1. CIM motivation + organic optoelectronic opportunity (~120 words, current §1)
2. Methodological gap: device-centric literature, no system-level framework for modern backbones (~110 words, current §2)
3. Our framework + 4 enumerated contributions (~120 words, compressed §6+§7)
4. Scope (behavioral, not circuit-accurate) + section preview (~100 words, current §8)

### 1.3 `02_related_work.tex` — 696 → 350 words (cut **346 words / -50%**)

**Specific deletions:**

- **§2.1 Hardware-Aware Training**: delete the sentence "Standard HAT usually keeps one random D2D mask fixed throughout training. Section~\ref{subsec:hardware-transferability} shows that this choice causes the model to fit a particular hardware instance rather than the deployment distribution." — this is repeated in Methodology §3. Keep only one. Cut: ~40 words.
- **§2.1**: delete the AIHWKIT comparison sentence "Existing open-source analog-training stacks are closer to i.i.d. perturbation injection..." — this belongs in Methods/Limitations. Cut: ~50 words.
- **§2.2 Organic devices**: delete "At the same time, most of this literature remains device-centric..." second paragraph — duplicates intro §2 gap statement. Cut: ~80 words.
- **§2.3 CIM Simulators**: delete the "In the CIM context, dense linear operators..." sentence + the "Recent heterogeneous CIM accelerators..." sentence. These get duplicated in §3 Methodology. Keep ONE place (Methodology). Cut: ~120 words.
- **§2.3 last paragraph**: delete "Unlike prior ViT-on-PIM studies, we jointly model..." — this is a contribution-statement, belongs in Intro §6. Cut: ~50 words.

**Final structure** (3 subsections, ~350 words total):
- §2.1 HAT history (3-4 sentences, ~80 words)
- §2.2 Organic neuromorphic / optoelectronic devices (4-5 sentences, ~120 words)
- §2.3 CIM frameworks (4-5 sentences, ~150 words)

### 1.4 `03_methodology.tex` — 1,164 → ~1,000 words (cut **164 words / -14%**)

**Light cuts only**:
- Remove repeated subsection headers like "We now describe..." (purely transition language). ~30 words across 4 subsections.
- Tighten Eq. ref language ("Equation~\ref{eq:foo} states that..." → just cite the equation). ~50 words.
- Remove parenthetical "(see Section~\ref{...} for details)" that points forward to Results — these are unnecessary when forward-references are obvious from layout. ~80 words.

**Do NOT cut**: equations, the Ensemble HAT formal definition, the noise composition order spec, scale-recovery formula. These are load-bearing.

### 1.5 `04_experimental_setup.tex` — KEEP (325 words)
Already tight. No change.

### 1.6 `05_results.tex` — 1,542 → 1,100 words (cut **442 words / -29%**)

**Specific deletions:**

- **§5.1-5.7 opening sentences**: every subsection currently begins with "We now show..." / "In this section..." / "To probe X, we...". Delete all. ~100 words across 7 subsections.
- **§5.5 Hardware Transferability**: the no-AMP confirmation paragraph "The collapse was independently confirmed under FP32 inference with autocast disabled..." reads as defensive footnote. Move to Supp Note S-Verification, leave a 1-sentence pointer. ~80 words.
- **§5.6 Iso-Accuracy Operating Envelope**: the Sobol second-order interpretation paragraph ("This two-phase structure has a direct hardware implication...") repeats Discussion §6.1. Cut from Results, keep in Discussion. ~70 words.
- **§5.7 Severe-NL** (post-fix Stage-2): the static-vs-per-instance ADC explanation paragraph is too long. Compress to 2 sentences: "Per-instance ADC range recalibration confirms the static-cal protocol does not bias the headline." Cut: ~100 words.
- **§5.8 OPECT zero-shot**: the "stark contrast between standard and Ensemble HAT" interpretation belongs in Discussion. Cut from Results. ~90 words.

**Keep**: every numerical claim, every table, every figure ref.

### 1.7 `06_discussion.tex` — 1,089 → 750 words (cut **339 words / -31%**)

**Specific deletions:**

- **§6.1 Principal Bottlenecks**: the variance-decomposition recap (Sobol numbers ADC=0.98, D2D=0.92) is duplicated from Results §5.6. Discussion should INTERPRET, not RECAP. Cut: ~120 words.
- **§6.2 Transformer Sensitivity**: the "Why the transformer amplifies front-end distortion" paragraph is mechanistic content that belongs in Methodology or Supp Note S-Frontend-Theory. Cut from main body. ~150 words.
- **§6.3 Task Complexity / Data Starvation**: this entire subsection is one paragraph. Compress to 1 sentence in §6.5 Limitations. Cut: ~60 words.
- **§6.5 Limitations**: tighten — currently has 2 paragraphs that overlap. Merge to 1 paragraph. ~60 words.

**Keep**: Mechanism subsection (linking E2 D2D landscape to SAM analogy), Design Rules callout box, Outlook subsection.

### 1.8 `07_conclusion.tex` — KEEP (395 words)
Already concise.

### 1.9 `08_appendix.tex` — 1,200 → 800 words (cut **400 words / -33%**)

**Specific deletions:**

- Per-experiment narrative paragraphs that describe what tables already show. Replace each with a single sentence + table. ~200 words.
- Repetitive method recaps (already in §3 Methodology). ~150 words.
- "We additionally..." intro phrases for every appendix subsection. ~50 words.

**Keep**: data tables, raw provenance, hyperparameter listings.

---

## 2. Cut list summary

| File | Current | Target | Cut | Method |
|:--|--:|--:|--:|:--|
| 00_abstract | 137 | 137 | 0 | — |
| 01_introduction | 784 | 450 | -334 | Delete intro §3-§5 (duplicated in Related Work); compress §6+§7 |
| 02_related_work | 696 | 350 | -346 | Remove inline contribution restatements; remove cross-section duplicates |
| 03_methodology | 1,164 | 1,000 | -164 | Remove transition language + redundant cross-refs |
| 04_experimental_setup | 325 | 325 | 0 | — |
| 05_results | 1,542 | 1,100 | -442 | Remove every "We now show..." opener + 4 subsection-internal interpretation paragraphs |
| 06_discussion | 1,089 | 750 | -339 | Remove duplicated Sobol recap; move mechanism para to Supp Note; tighten Limitations |
| 07_conclusion | 395 | 395 | 0 | — |
| 08_appendix | 1,200 | 800 | -400 | Remove narrative paragraphs that duplicate tables |
| **TOTAL** | **7,332** | **5,307** | **-2,025 (-28%)** | |

---

## 3. Constraints (HARD)

- **No content changes.** Only cuts + minor reorders. Every number, every figure ref, every cite stays.
- **No silent narrative shifts.** If a sentence does scientific work (claim, evidence, mechanism), keep it.
- **No new content.** This dispatch is for cutting, not adding.
- **Verify after each section**: `wc -w` on the file after editing to confirm target met.
- **No bug-retrospective language reintroduction.** Maintain Round-7 scrub discipline.
- **Zone discipline preserved**: every claim still maps to 3A/3B/3C.

---

## 4. Workflow

For each section:
1. Read current `.tex` carefully
2. Identify duplications + filler
3. Make cuts inline (NOT new draft files — directly edit canonical `.tex`)
4. `wc -w` verify hit target
5. Append progress to AGENT_SYNC

After all 9 files done:
1. Compile full manuscript: `cd paper/latex_gpt && latexmk -pdf main.tex`
2. Verify RC 0, zero undefined refs
3. Verify total `wc -w sections/*.tex` ≤ 5,500
4. Hand off to Claude for integration review

---

## 5. Deliverables

| File | Status |
|:--|:--|
| `paper/latex_gpt/sections/01_introduction.tex` | EDITED in place |
| `paper/latex_gpt/sections/02_related_work.tex` | EDITED in place |
| `paper/latex_gpt/sections/03_methodology.tex` | EDITED in place (light) |
| `paper/latex_gpt/sections/05_results.tex` | EDITED in place |
| `paper/latex_gpt/sections/06_discussion.tex` | EDITED in place |
| `paper/latex_gpt/sections/08_appendix.tex` | EDITED in place |
| `paper/latex_gpt/main.pdf` | Recompiled |
| `KIMI_R9A_LENGTH_SURGERY_REPORT_20260425.md` | Per-section before/after word count + cut log |

---

## 6. Success criteria

- Body word count: ≤ 5,500 (currently 7,332)
- Manuscript compiles RC 0, zero warnings, zero undefined refs
- Reviewer reading the trimmed paper still gets every key claim
- Zero scientific content lost (all numbers, figures, cites preserved)
- No bug-retrospective phrasing introduced

---

## 7. Coordination

- Track B (Codex TikZ) runs parallel — your text cuts don't conflict
- Track C (Defense paragraphs) is your second task — start AFTER Track A finishes
- 8×40GB and Round-8 Work 2 are independent — ignore
- Gemini will hostile-review the trimmed paper after Tracks A+B+C all land

**No deadline.** 3-4 days expected.
