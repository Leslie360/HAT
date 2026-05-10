# External Reviewer Prompt — take the PDF + this prompt to any strong reviewer

**Instruction to the user:** attach `main.pdf` (+ `supplementary_main.pdf` if possible) along with this prompt. The prompt is designed so a senior reviewer without project context can produce maximally useful feedback in a single pass.

---

## Prompt (paste this to the external reviewer)

> I'm finalizing a manuscript for submission to **Nature Communications** and would value your honest, senior-level assessment before I click submit. The topic sits at the intersection of **analog in-memory computing hardware** and **Vision Transformers under non-ideal device noise**. The central contribution is a hardware-aware training ("HAT") protocol that converts fresh-instance collapse (near-chance accuracy on a newly-programmed analog array) back to ≥86% on CIFAR-10, plus a diagnostic framework that ranks which device non-idealities dominate the ViT accuracy budget.
>
> I'm attaching the main text (≤18 pp) and supplementary. I'm explicitly **not** asking you to proof-read — I'm asking for the kind of critical reading a Nature Communications reviewer would do. Specifically:
>
> 1. **Central claim stress test.** The headline is "Ensemble HAT raises fresh-instance accuracy from ~10% to 86.37±1.54%." Is this claim defensibly scoped? Are the baselines comparable? Is the ~10% baseline presented with sufficient honesty about its meaning (class-balanced chance or collapsed-predictor)? If a reviewer asked "show me the raw per-instance outputs," would the framing survive?
>
> 2. **Generality vs. over-reach.** The paper targets edge-scale datasets (CIFAR-10/100, Flowers-102) and explicitly scopes out ImageNet. Is that scoping honest or suspiciously convenient? What's the first ImageNet-scale failure mode you'd predict? Does the paper's framing acknowledge it?
>
> 3. **Methodological holes.** Are there glaring omissions a hardware-ML reviewer would catch? Examples I'm worried about:
>    - Fixed Gaussian D2D + C2C vs. real spatially-correlated / heavy-tailed device statistics
>    - CrossSim cross-framework comparison disclosed as 1-run clean / 3-run noise on a 1,000-image subset — is that caveat sufficient, or does the conclusion still over-reach?
>    - Energy estimates are labeled "first-order upper bounds under placeholder constants" — is the manuscript's hedging consistent, or does the marketing creep back in?
>
> 4. **Severe-NL supplementary ablation.** In the supplement there is a group-wise linearization ablation under NL=2.0 showing MLP-only linearization recovers (87.79%), QKV-only and attn-proj-only both collapse (~18%). The current framing calls this a **bottleneck diagnostic**, NOT a solved mitigation — because the MLP-linearized model's fresh-instance transfer is only ~32% (much worse than standard Ensemble HAT's 86%). Does the supplement communicate this limitation honestly, or will reviewers think we're smuggling it in as a 5th contribution?
>
> 5. **Rebuttal risk.** Independent of scientific content: which *three* reviewer objections would hit hardest? For each, rate (a) how likely it is to trigger major revision, (b) what extra experiment or caveat would disarm it fastest.
>
> 6. **Figures.** Figures 4 (cross-dataset accuracy) mixes deterministic and MC-derived error bars in a single panel. Caption discloses this. Is the disclosure enough, or does the figure need splitting/re-drawing?
>
> 7. **Structure.** Section order runs abstract → intro → related work → results → discussion → methodology → supplementary. NC allows this narrative-first order. Does it hurt readability in practice?
>
> 8. **One-liner verdict.** If this arrived on your desk as an NC reviewer today, your gut call: (a) accept with minor revision, (b) major revision needed, (c) fundamentally not NC-caliber. And the single most load-bearing reason for that call.
>
> Please be direct. I would rather absorb sharp criticism now than in a reviewer letter. If something is unclear because the PDF alone doesn't give you enough context, flag what context you'd want — that's itself a useful signal.

---

## Supporting context (include if the reviewer asks for project background)

- **Two-arm deliverable**: this manuscript is paired with the author's PhD thesis; some results that are "open questions" here are followed up in thesis chapters, not in the manuscript itself. Reviewer does not need to accept that separation, but they should know it exists.
- **Submission target**: Nature Communications, not Nature — scope is broad but not headline-general.
- **Locked numbers guard**: the project maintains `scripts/_gpt/check_locked_numbers.py`, which verifies 16 headline values against their raw JSON. Currently passing 16/16. So if the reviewer spot-checks a number, it is traceable.
- **Known late edits since first draft**: (a) CrossSim statistics were recently corrected from "5-seed means" to explicit n=1/n=3 on 1,000-image subset with disclosure, (b) hyperparameter subsection added to §3, (c) rebuttal-supporting language added for R1/R5/R8.
- **Known open item**: standard-HAT fresh-instance baseline is being re-evaluated with `--no-amp` to confirm the 10.00% value is a genuine collapsed-predictor and not a numerical artifact. Result lands before submission; if numbers shift, headline language will update.

---

## What to do with the returned feedback

1. Save the reviewer's reply as `EXTERNAL_REVIEW_<REVIEWER_INITIALS>_20260419.md` in `report_md/_gpt/`.
2. Hand it back to the internal loop (Claude) for triage.
3. The coordinator will classify each point as: pre-submit-fix, rebuttal-only-prep, or out-of-scope.
