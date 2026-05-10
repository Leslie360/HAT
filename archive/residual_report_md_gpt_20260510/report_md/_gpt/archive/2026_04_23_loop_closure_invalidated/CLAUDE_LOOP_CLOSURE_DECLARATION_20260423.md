# CLAUDE — Work 1 Loop Closure Declaration
**Date:** 2026-04-23
**Authority:** `BROADCAST_LOOP_CLOSURE_DISPATCH_20260423.md`, `CLAUDE_SLIM_COMPLETION_STATUS_20260423.md`, `CLAUDE_HANDOFF_FOR_LOOP_CLOSURE_20260423.md`
**Status:** 🔓 **LOOP CLOSED.** Frozen files unfrozen. Single-shot rewrite applied. Paper-1 is submit-ready pending PDF rebuild.

---

## 1. Verification summary

| Check | Result |
|:--|:--|
| Kimi K-PATCH-1 diff landed | ✅ `KIMI_PAPER1_REWRITE_DIFF_20260423.md` + loop-closure analysis patched |
| Codex CX-FIG figure rendered | ✅ PNG 300 dpi + PDF vector, Hartigan p=0.98 annotation visible, single broad KDE peak |
| Figure quality | ✅ Publication-grade; Viridis continuous (no clustering), red mean + σ band, clear marginal KDE |
| Canonical numbers | ✅ N=30 mean 38.95 ± 9.85%, range 22.03-61.69%, dip statistic 0.0415, p=0.9796 |
| Narrative consistency | ✅ "wide unimodal structural limit" throughout; no "bimodal" / "two attractors" in paper text |

## 2. Relocations performed

- `compute_vit/images_gpt/fig_structural_limit_signature.{png,pdf}` → `paper/figures/fig_structural_limit_signature.{png,pdf}` (Codex wrote to project root; moved to canonical paper-figure path).
- `compute_vit/CODEX_CX_FIG_SUMMARY_20260423.md` → `report_md/_gpt/CODEX_CX_FIG_SUMMARY_20260423.md`.
- Empty `compute_vit/images_gpt/` directory removed.

## 3. Frozen files edited (single-shot rewrite applied)

### `paper/latex_gpt/sections/00_abstract.tex`
Appended sentence after existing closing claim:
> An extended N=30 fresh-instance sample (38.95±9.85%; Hartigan's dip test, p=0.98) does not reject the unimodal null hypothesis, supporting the structural-limit interpretation over alternative two-basin hypotheses.

### `paper/latex_gpt/sections/05_results.tex`
After the "three independent mitigations" paragraph (existing line 76), inserted:
- One new paragraph summarizing the N=30 evaluation and the softmax-Lipschitz interpretation.
- New `\begin{figure}` block referencing `figures/fig_structural_limit_signature.pdf`, labeled `fig:structural-limit-signature`, with full caption.

### `paper/latex_gpt/sections/06_discussion.tex`
Inside Limitations subsection (§43), after the existing `$NL=2.0$ limit reflects ... structurally` sentence, appended:
> An $N=30$ fresh-instance evaluation of the best second-order-surrogate recipe (Hartigan's dip test, $p=0.98$; Fig.~\ref{fig:structural-limit-signature}) does not reject the unimodal null hypothesis, indicating that the apparent visual clustering observed in smaller samples (N=10) was a small-sample artifact rather than evidence of two distinct failure modes.

### `paper/latex_gpt/cover_letter_v3.tex`
After the "three intuitive strategies" paragraph (existing line 24):
1. Appended one sentence on the N=30 Hartigan test.
2. Inserted a new `\textbf{Ablation Coverage Note}` paragraph with the three disclosure items (K4 α=0.75/1.0 gap; J2-J4 memo-level; δg_eff=0.0 eval-chain consistency).

## 4. Remaining manual steps (not automatable here)

The following must be done by the user or by Codex at build time:

1. **Rebuild PDF**: `cd paper/latex_gpt && latexmk -pdf main.tex && latexmk -pdf cover_letter_v3.tex` (or equivalent build path). Inspect:
   - Fig. `fig:structural-limit-signature` appears in §5 around the three-mitigations discussion.
   - New abstract sentence flows naturally.
   - Cover letter Ablation Coverage Note reads cleanly.
2. **Run `check_locked_numbers.py`** (if present in `scripts/`) to verify no drift in any other locked number.
3. **Spot-check main.tex** for any `\input{sections/...}` ordering or a `\listoffigures` that needs a regeneration pass.
4. **Submit paper-1 NC package** (manuscript PDF + cover letter + supplementary + figures zip).

## 5. Round Q closed

All SLIM tasks + all loop-closure dispatch tasks complete:

| Agent | Tasks | Status |
|:--|:--|:--|
| Codex | CX-K1 + CX-K2 + CX-FIG | ✅ Complete |
| Kimi | K-SLIM-1 + K-SLIM-2 + K-SLIM-3 + K-PATCH-1 | ✅ Complete (12/20 archive is the only residual gap — non-blocking) |
| Gemini | G-SLIM-1 + G-SLIM-2 + G-SLIM-3 | ✅ Complete |
| Claude | CLAUDE-EH (this memo) | ✅ Complete |

## 6. Round R opens on user signal

Round R scope (pre-staged, awaiting user green-light):
- **Work 2 CX-L1**: TinyLlama-1.1B bring-up + KV-cache instrumentation + WikiText-103 FP16 baseline.
- **Work 2 skeleton_v1 rewrite**: from falsification-study to KV-cache pitch (per `CLAUDE_WORK2_DIRECTION_LOCK_20260423.md`).
- **Chinese thesis Ch.6-7**: KV-cache chapters (new files in `paper/thesis_cn/`).

No Round R task executes until paper-1 is submitted AND user signals Round R open. This is a hard gate.

## 7. Standing rules post-closure

- The 5 frozen paper-1 files (`paper/00_abstract.md`, `05_results.md`, `06_discussion.md`, `cover_letter*.md`, `paper/thesis/chapter_5_*.tex`) are **unfrozen** as of this declaration. Further edits are normal editing, subject only to standard version control.
- If NC rebuttal cycle arrives, Rule B re-activates on a per-cycle basis at that time — not retroactively.
- `KIMI_REBUTTAL_MASTER_20260420.md` remains usable as base; rebuttal updates fold in via standard edit, no special protocol.

## 8. One-line summary

Work 1 is done. Paper-1 is submit-ready. Work 2 waits for submission + user green-light.
