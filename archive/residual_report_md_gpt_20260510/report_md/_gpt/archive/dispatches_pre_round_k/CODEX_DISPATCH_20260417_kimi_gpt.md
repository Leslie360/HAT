# Codex Dispatch — Kimi Support Pack (2026-04-17)

**From:** Codex
**To:** Kimi
**Scope:** Literature / reference / reviewer-facing manuscript support only. **No code edits, no figure regeneration, no data fabrication, no unpublished-source disclosure.**
**Goal:** Offload the highest-value non-GPU work while Codex handles experiments and manuscript implementation.

---

## Hard constraints

1. **Do not use or quote unpublished raw materials** from `数据_博士/`, private PPT screenshots, or doctor-owned original figures.
2. **Do not invent references.** Every citation claim must include a verifiable DOI, URL, or canonical bibliographic record.
3. **Do not rewrite results numerically.** If you cite a manuscript number, point to the exact local file/section where it appears.
4. Work only on:
   - literature discovery
   - reference normalization audit
   - reviewer-facing positioning language
   - figure/caption/publication-style audit
5. Output only markdown files under:
   - `/home/qiaosir/projects/compute_vit/report_md/_gpt/`

---

## KX-1 — DOI / metadata recovery for live manuscript references [HIGH]

**Why:** The manuscript is now technically stronger, but the bibliography still risks looking under-curated. We need a clean external anchor set for review and final submission.

### Task
Build a reviewer-facing citation table for the papers most likely to be challenged or explicitly discussed in review.

### Priority topics
- analog / HAT / CIM training baselines
- domain randomization / sim-to-real framing
- inorganic simulators used for positioning
- recent organic optoelectronic / OECT / OPECT / photonic-memory array papers
- any reference used to justify ADC, retention, or nonlinear-write framing

### Minimum target paper set
Please verify or replace with exact canonical entries where needed:
- `peng2020dnnneurosim`
- `rasch2021aihwkit`
- `crosssim2026`
- `lammie2022memtorch`
- `tobin2017domain`
- `joshi2020accurate`
- `choi2019pact`
- `bengio2013estimating`
- `xu2025emerging`
- `guo2024organic`
- `zhang2026opect`
- `vincze2026dualplasticity`
- any missing 2024–2025 organic-array/system papers that materially strengthen the intro/discussion

### Deliverable
Write:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/KIMI_REFERENCE_RECOVERY_20260417.md`

### Required format
For each paper, include:
- Bib key in current manuscript
- Full title
- Full author list or standard abbreviated form
- Journal / conference
- Year
- Volume / issue / pages if available
- DOI
- URL
- 1-line note: why this paper matters to this manuscript
- 1-line note: where it should be cited or strengthened in the current draft

Also include a short section:
- `Likely weak or placeholder references`
- `Likely duplicate / inconsistent entries`

---

## KX-2 — Ensemble HAT novelty boundary audit [HIGH]

**Why:** The main remaining reviewer attack is not “does Ensemble HAT work?” but “is it just stronger noise regularization / domain randomization?”

### Task
Produce a tight literature-and-positioning memo on how to frame Ensemble HAT against:
- fixed-mask HAT
- i.i.d. noise augmentation
- sim-to-real domain randomization
- any analog-CIM training method that varies device instances across training

### Deliverable
Write:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/KIMI_ENSEMBLE_HAT_POSITIONING_20260417.md`

### Required contents
1. `Closest prior ideas`
   - list the 3–6 closest concepts or papers
2. `What is genuinely new here`
   - in 3–5 bullets
3. `What should not be claimed`
   - e.g. do not overclaim first-ever if prior art overlaps conceptually
4. `Safe wording for Introduction`
   - give 2–3 sentence versions usable in manuscript prose
5. `Safe wording for Discussion / Response to Reviewers`
   - explicitly distinguish structured fixed spatial mismatch maps from generic i.i.d. perturbation
6. `If reviewers ask for MI-HAT / SDR-HAT comparisons`
   - state what the fairest narrative response would be if exact apples-to-apples external baselines are unavailable

Important: this memo must be grounded in real literature, not generic ML analogies.

---

## KX-3 — Figure / caption publication audit [MED]

**Why:** The figures are now much cleaner, but NC-level polish still depends on captions being self-contained and style being publication-safe.

### Task
Audit the current manuscript figures and captions from a reviewer/editor perspective.

### Targets
Use the current built assets and LaTeX sources:
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.pdf`
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary_main.pdf`
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex`
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex`

### Deliverable
Write:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/KIMI_FIGURE_CAPTION_AUDIT_20260417.md`

### Required contents
For each main-text figure and each high-value supplementary figure:
- whether caption is self-contained
- whether axes/legend labels are publication-safe
- whether any experimental condition is missing from caption
- whether any panel still reads like slideware instead of paper artwork
- whether any claim in text is stronger than what the figure visibly supports

End with:
- `Top 5 figure/caption fixes still worth doing`
- ordered by impact / effort ratio

---

## KX-4 — Reference-format and style audit [MED]

**Why:** Even with the right papers, sloppy reference formatting lowers trust fast.

### Task
Audit reference formatting consistency against Nature-family expectations.

### Deliverable
Write:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/KIMI_REFERENCE_STYLE_AUDIT_20260417.md`

### Check for
- missing DOI
- missing volume/issue/pages where available
- inconsistent capitalization
- broken or likely placeholder venues
- duplicated concepts under different bib keys
- references cited in text but weakly tied to actual claims

Output a concrete fix list, not general advice.

---

## KX-5 — Perplexity-ready literature query block [LOW, but useful]

**Why:** We may still want a single external-search paragraph for DOI recovery via Perplexity.

### Task
Draft one dense, no-fluff paragraph that can be pasted into Perplexity to recover:
- canonical metadata
- DOI
- venue
- year
- exact relevance to this manuscript
for the citation clusters above.

### Deliverable
Write:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/KIMI_PERPLEXITY_PROMPT_20260417.md`

Constraint:
- one paragraph only
- no bullets
- optimized for retrieval, not explanation

---

## What Codex is doing in parallel

Codex is **not** waiting on these outputs to continue. In parallel, Codex is handling:
- GPU-side experiment execution
- manuscript-side implementation of accepted fixes
- code/release closure

That means your outputs should optimize for **precision and editorial usefulness**, not speculative roadmap ideas.

---

## Reporting rule

When finished, append one block to:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md`

Use the house format already in that file and include exact output paths.
