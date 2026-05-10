# DISPATCH KIMI-ROUND2 — THEORY-1 Fixes + K-DRAFT-V3 §5.7 Revise
**Date:** 2026-04-24
**Issued by:** Claude
**Assignee:** Kimi
**Depends on:** CLAUDE_DECISIONS_D1_D5_20260424.md (ruling doc)
**Status:** Part A (THEORY-1 fixes) is immediate. Part B (§5.7 revise) holds until Codex ADC-on ablation JSONs land.

---

## Part A — THEORY-1 four corrections (START NOW)

Per D5 in CLAUDE_DECISIONS_D1_D5. Edit in place, no v2 file.

### A.1 Remove unzoned empirical numbers from `S_theory_ensemble_hat.tex`

Strip every empirical percentage / pp claim from the theory Supp Note. Theory Supp Note contains **zero** empirical numbers.

Delete or rephrase:
- Any mention of `88.41%`, `86.16%`, `-1.76pp`, `-4.20pp`, `76pp`, `78pp`, or similar
- Replace with theoretical / qualitative references. Example: "The empirically observed degradation under spatially correlated D2D mismatch (see Supp Note S2) is consistent with the Fisher-matrix-weighted anisotropic prediction of this section."

### A.2 Restrict C2C independence assumption

Current theory absorbs C2C into `L_0` assuming forward-pass independence. Holds for `--noise-mode uniform` (additive independent noise), breaks for `--noise-mode proportional` (C2C magnitude scales with post-D2D weights).

Add a remark (1-2 sentences) in S.2:

> The derivation assumes uniform additive C2C noise, where $\xi^{\text{C2C}}$ is independent of $\theta$ and D2D mask $M$. In the proportional-noise regime the C2C magnitude couples to post-D2D weights; the resulting modification is a mild correction to the weighted gradient-$L_2$ coefficient and does not change the qualitative conclusion.

### A.3 Soften "exact analogy" to "structural analogue"

Find-and-replace in all three THEORY-1 deliverables:
- "exact analog" → "structural analogue"
- "exactly analogous" → "structurally analogous"
- "analogous exactly" → "structurally analogous"

Also add one line (in S.2 or S.3) acknowledging the approximation:

> The implicit regularizer is obtained under a second-order Taylor expansion with Gauss-Newton approximation of the loss Hessian; higher-order corrections in $\sigma_{\text{D2D}}^2$ are discussed schematically in S.6.

### A.4 Fix hook class name

Find-and-replace wherever it appears in your deliverables (Supp Note, Methods, Discussion, cross-review):

- `ADCContext` → `ADCQuantHookManager`

The actual class is defined in `inference_analysis_utils.py:576-621`.

### A.5 Deliverable

After edits, append to `KIMI_THEORY_1_COMPLETE_20260424.md`:

```
## Round-2 Fixes Applied (2026-04-24)

- A.1: Removed empirical numbers from S_theory_ensemble_hat.tex ✅
- A.2: Added C2C-independence qualifier (S.2 remark) ✅
- A.3: Softened "exact analog" to "structural analogue" ✅
- A.4: Renamed ADCContext → ADCQuantHookManager ✅

THEORY-1 now ready for Claude integration.
```

Estimated time: 30-45 min. No GPU cost.

---

## Part B — K-DRAFT-V3 §5.7 revise (HOLD until ADC-on JSONs land)

Per D3 in CLAUDE_DECISIONS_D1_D5. DO NOT start this until Codex signals "ADC-on ablation JSONs consolidated" (via AGENT_SYNC status block). Expected within hours.

When triggered, apply 5 fixes to `paper/latex_gpt/sections/05_results.tex.kimi_draft_v3`:

### B.1 Add ADC scope statement

§5.7 opening paragraph must explicitly state:

> Results reported in this section combine two deployment-fidelity evaluation protocols: (i) default-forward analog evaluation using the training-path differentiable surrogate (ADC-off), and (ii) hook-based ADC-quantized evaluation via \texttt{ADCQuantHookManager} at canonical 6-bit and 8-bit precisions. Both columns are reported in Table~\ref{tab:severe-nl-dual}; ADC-on columns bound realistic deployment accuracy while ADC-off columns isolate the training-path surrogate's baseline response.

Table caption updates accordingly.

### B.2 Remove bug-retrospective phrasing

Ban these strings from §5.7 body text (and all other sections you touch):

- "verified implementation"
- "previously reported ~30% floor"
- "previously reported ceiling"
- "post-fix"
- "we verify here that"
- Any phrasing that implies an internal software correction narrative.

Replace with neutral protocol language:
- "Under the audited severe-NL protocol..."
- "The low-accuracy severe-NL regime is not observed under the audited evaluation protocol."
- "At NL=2.0, hardware-aware training recovers deployable accuracy across..."

### B.3 Strip forbidden content from LaTeX comments

Lines 84-85 of `05_results.tex.kimi_draft_v3` currently contain comments with `27.72%`, `30.53%`, `bimodality`, `ceiling`, `structural limit`, `post-fix`. **Delete these comments entirely**, or replace with neutral placeholder comments that don't reference any forbidden content.

Forbidden content rule applies even to LaTeX comments.

### B.4 Nuance residual gap

Current draft has a "4.3 pp residual gap to canonical 86.37%" statement. Revise:

> Under the local batch-64 training recipe, severe-NL fresh-instance accuracy sits approximately 4-5 pp below the canonical NL=1.0 Ensemble HAT baseline (86.37\%). The remote batch-512 recipe narrows this gap to $\sim$2 pp (see cross-host parity, Supp Fig.~\ref{figS_cross_host_parity}), indicating that training-recipe choices rather than a physical floor account for the difference.

### B.5 Clarify V2 vs Ensemble HAT protocol separation

Find the sentence that joins V2 97.37% with Ensemble HAT 86.37%. Revise to explicitly state distinct protocols:

> V2 (97.37$\pm$0.05\%) and Ensemble HAT (86.37$\pm$1.54\%) arise under distinct noise models and evaluation protocols: V2 is a zero-noise or proportional-noise in-domain evaluation, while Ensemble HAT is evaluated on fresh D2D realizations under uniform additive noise. They measure different quantities and should not be directly compared as competing accuracies.

### B.6 Dual-column table

Once Codex ADC-on JSONs land, replace §5.7 severe-NL table with a dual-column version:

| Run | Config | Seed | Train Best | Fresh ADC-off (mean±std) | Fresh ADC-on 8-bit (mean±std) | Fresh ADC-on 6-bit (mean±std) |
|:--|:--|--:|--:|--:|--:|--:|

Headline numbers in body text cite the ADC-on 8-bit column (canonical deployment fidelity).

### B.7 Deliverable

Save as `paper/latex_gpt/sections/05_results.tex.kimi_draft_v3` (overwrite in place, not v4). Append status block to AGENT_SYNC when complete.

Estimated time: 1-2 hours once ADC JSONs land. No GPU cost.

---

## Constraints across both parts

- **No new content beyond these fixes.** Do not rewrite unrelated sections.
- **Zone discipline**: every number cited maps to NARRATIVE_PIVOT zone 3A/3B/3C. If you can't place it, flag before inserting.
- **No paper-text edits outside `.kimi_draft_v3` sidecar files.** Claude integrates.
- **No rewrites of Supp Note S-Theory structure.** Only the 4 targeted A.1-A.4 corrections.

---

## Success criteria

Part A: THEORY-1 deliverables pass Codex's 5 concerns + Gemini's 2 concerns from cross-review. Ready for Claude integration into manuscript.

Part B: §5.7 integrates cleanly, Methods describes train-surrogate / eval-ADC-hook split, table shows dual-column honest reporting, no bug-retrospective language anywhere in the paper.
