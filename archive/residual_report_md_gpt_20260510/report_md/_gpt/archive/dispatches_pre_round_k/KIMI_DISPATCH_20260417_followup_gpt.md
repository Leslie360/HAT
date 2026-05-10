# Codex Dispatch — Kimi Follow-up (2026-04-17)

**From:** Codex
**To:** Kimi
**Scope:** Literature verification, bibliography hardening, reviewer-facing positioning only. **No code edits, no figure regeneration, no private-data use, no fabricated baselines.**

## Why this follow-up exists

The manuscript is now much tighter technically. The remaining high-value work is editorial and literature-facing:
- verify which “missing comparison” suggestions are actually real prior art versus model-invented labels,
- harden weak bibliography entries,
- give drop-in wording that is defensible under review.

Work only under:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/`

Do **not** use or quote:
- `数据_博士/`
- unpublished doctor-owned figures
- private PPT screenshots
- any local raw data not already exposed in the paper or supplementary files

---

## KM-F1 — Reality check on proposed comparison baselines [HIGHEST]

### Task
Audit whether the following comparison requests correspond to **real, citable prior art** in CIM / analog-HAT literature, or whether they are just plausible-sounding labels produced by LLM review text:
- “MI-HAT” / “Multi-Instance HAT”
- “SDR-HAT” / “Spatial Domain Randomization HAT”
- any claimed analog-CIM training method that explicitly varies spatial hardware instances during training

### Deliverable
Write:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/KIMI_COMPARISON_REALITY_CHECK_20260417.md`

### Required output structure
For each requested baseline family:
1. `Is this an actual named method?` → yes / no / unclear
2. If yes:
   - canonical paper title
   - authors
   - venue
   - year
   - DOI / URL
   - 1-sentence relevance to this manuscript
3. If no:
   - state clearly that the label appears non-canonical or unverifiable
   - provide the **closest real literature** instead
4. End with one section:
   - `What comparisons are actually defensible to mention in response to reviewers?`
   - keep this practical and conservative

**Important:** If those names are not real literature, say so explicitly. Do not “repair” them into invented citations.

---

## KM-F2 — Bibliography hardening with exact replacement blocks [HIGH]

### Task
Produce exact publication-grade replacement metadata for the weakest live bib entries.

### Priority entries
- `wang2025oectarray`
- `liu2025optoelectronic`
- `kim2025hemlet`
- `olizaman2023dmm`
- `bettayeb2024memristorattention`

### Deliverable
Write:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/KIMI_BIB_REPLACEMENTS_20260417.md`

### Required output structure
For each entry:
1. `Current problem`
   - e.g. placeholder authors, weak venue string, arXiv formatting, contradictory use
2. `Verified canonical metadata`
   - title
   - authors
   - venue
   - year
   - volume/issue/pages if available
   - DOI
   - URL
3. `Drop-in BibTeX block`
   - full replacement block ready to paste
4. `Citation-use guidance`
   - keep as-is / weaken wording / remove from manuscript / move to related-work-only

### Extra requirement
If `bettayeb2024memristorattention` is indeed a poor or contradictory citation for “keep attention digital”, give one sentence on how to reframe that citation safely instead of deleting it blindly.

---

## KM-F3 — Drop-in prose for intro / discussion / reviewer response [HIGH]

### Task
Convert the validated literature positioning into short prose blocks that can be pasted directly into the manuscript or reviewer response.

### Deliverable
Write:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/KIMI_DROPIN_PROSE_20260417.md`

### Required contents
Provide 6 compact blocks:
1. `Introduction paragraph` on why existing simulators (AIHWKIT / CrossSim / MemTorch / DNN+NeuroSim) are useful but not sufficient for organic optoelectronic profiling
2. `Related-work paragraph` positioning Ensemble HAT against fixed-mask HAT, generic i.i.d. perturbation, and domain randomization
3. `Contribution bullets` — 3 bullets only, Nature-style, no hype
4. `Response-to-reviewers paragraph` for “why no MI-HAT / SDR-HAT comparison?”
5. `Response-to-reviewers paragraph` for “simulation-only without fabricated-array validation”
6. `Response-to-reviewers paragraph` for “why the CrossSim / AIHWKIT shared-regime checks are still meaningful`

### Constraints
- Each block must be conservative and citation-aware
- No invented methods
- No fake certainty
- Prefer wording that survives hostile review rather than sounding impressive

---

## Existing local context you may rely on

You may use these already-generated local notes as input:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/KIMI_REFERENCE_RECOVERY_20260417.md`
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/KIMI_REFERENCE_STYLE_AUDIT_20260417.md`
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/KIMI_ENSEMBLE_HAT_POSITIONING_20260417.md`
- `/home/qiaosir/projects/compute_vit/report_md/bibliography_structured.csv`

Do not just restate those files. Improve and resolve them.

---

## Reporting rule

When finished, append a short block to:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md`

Include exact output paths and a one-line verdict for each deliverable.
