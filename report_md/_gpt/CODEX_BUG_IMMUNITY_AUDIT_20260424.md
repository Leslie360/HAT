# Codex Bug-Immunity Audit
Date: 2026-04-24
Task: `CX-AUDIT-1`
Source: `BROADCAST_REBUILD_3WEEK_20260424.md`

## Verdict

The scope claim is correct at the code/math level:

- The STE branch-swap bug is a no-op at canonical `NL_LTP=1.0 / NL_LTD=-1.0`.
- Canonical paper results whose training used default `NL=1.0/-1.0` are bug-immune with respect to this specific STE branch mapping bug.
- Severe-NL experiments using `NL=2.0/-2.0` or second-order STE are contaminated unless rerun after commit `9cdbe77`.

Current live paper text still contains contaminated severe-NL / structural-ceiling paragraphs in `paper/latex_gpt/sections/05_results.tex` and `paper/latex_gpt/sections/06_discussion.tex`. Per Rule B, Codex did not edit those live files; Kimi should draft replacements and Claude integrates later.

## Symbolic Check

The first-order STE scale terms are:

```text
ltp_scale = ((Gmax - G) / (Gmax - Gmin)) ** (NL_LTP - 1)
ltd_scale = ((G - Gmin) / (Gmax - Gmin)) ** (abs(NL_LTD) - 1)
```

At canonical `NL_LTP=1.0` and `NL_LTD=-1.0`:

```text
NL_LTP - 1 = 0
abs(NL_LTD) - 1 = 0
ratio ** 0 = 1
```

Therefore both branches multiply `grad_output` by `1`. Swapping LTP/LTD branches cannot change gradients in this limit.

Second-order STE is not active in canonical V-series / Ensemble-HAT paper checkpoints. The contaminated CX-J/CX-K severe-NL line did activate non-canonical NL and/or second-order logic, so it must remain deprecated.

## Checkpoint Metadata Spot-Check

| Checkpoint | Role | Recorded NL | Inferred training NL | Bug status |
|---|---|---:|---:|---|
| `checkpoints/V1_fp32_digital_baseline_best.pt` | digital baseline | not analog | n/a | immune |
| `checkpoints/V3_hybrid_standard_noise_standard_train_best.pt` | canonical standard HAT / fixed-mask baseline | absent in old metadata | default `1.0/-1.0` | immune to branch swap |
| `checkpoints/V4_hybrid_standard_noise_hat_best.pt` | canonical V4 standard HAT | absent in old metadata | default `1.0/-1.0` | immune to branch swap |
| `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` | canonical Ensemble HAT | `1.0/-1.0` | `1.0/-1.0` | immune |
| `checkpoints/V8_hybrid_hat_with_retention_aware_training_best.pt` | retention-aware follow-up | `1.0/-1.0` | `1.0/-1.0` | immune |
| `checkpoints/_gpt/postfix_standard_hat/V3_hybrid_standard_noise_standard_train_best.pt` | post-fix true severe-NL anchor | `2.0/-2.0` | `2.0/-2.0` | valid post-fix, needs M1 replication |
| `checkpoints/_gpt/postfix_reruns/V4_hybrid_standard_noise_hat_best.pt` | post-fix Ensemble HAT severe-NL anchor | `2.0/-2.0` | `2.0/-2.0` | valid post-fix, needs M2 replication |
| `checkpoints/_gpt/postfix_proportional/V4_hybrid_standard_noise_hat_best.pt` | proportional HAT headline risk | `1.0/-1.0`, proportional | `1.0/-1.0` | not a true NL=2 training result |

Note: older canonical checkpoints omit explicit `nl_ltp/nl_ltd` in `exp_cfg`; this is an old-metadata limitation. The training code defaults are `nl_ltp=1.0`, `nl_ltd=-1.0`, and those checkpoints predate the explicit severe-NL override path.

## Paper Figure / Claim Crosswalk

| Paper item | Source / checkpoint family | Training NL | Bug-immunity status | Action |
|---|---|---:|---|---|
| Fig. 4 accuracy comparison | canonical V/R/C checkpoints, e.g. `checkpoints/V*.pt`, `checkpoints/C*.pt`, `checkpoints/R*.pt` | default `1.0/-1.0` or digital | immune | keep, but Kimi final audit should re-check number provenance |
| Fig. 5 HAT recovery | canonical standard HAT + Ensemble HAT | `1.0/-1.0` | immune | keep |
| Fig. 7 / retention curve | V7/V8 retention checkpoints | `1.0/-1.0` | immune | keep |
| Fig. 10 zero-shot transfer | Ensemble HAT checkpoint under literature profile | checkpoint `1.0/-1.0`; profile uses canonical write defaults | immune to branch swap | keep, but avoid calling it severe-NL training |
| Fig. 11 energy | energy model, no STE training | n/a | immune | keep |
| `fig_contour_map` / iso-accuracy | Ensemble HAT sweep, caption states `NL=1.0` | `1.0/-1.0` | immune | keep |
| `figS3_ensemble_hat` | canonical Ensemble HAT fresh-instance transfer | `1.0/-1.0` | immune | keep |
| `fig_structural_limit_signature` | CX-K2 N=30 severe-NL data | contaminated | invalid | already moved to `paper/figures/deprecated_20260424/` |
| §5.x severe-NL structural ceiling paragraphs | CX-J/CX-K severe-NL line | `2.0/-2.0` / second-order | contaminated | replace in K-DRAFT/Claude integration |
| §6 mechanistic structural-limit paragraph | CX-K2/N=30 narrative | contaminated | invalid | replace in K-DRAFT/Claude integration |
| Supplementary NL ablation table S16 | pre-fix severe-NL mitigation line | `2.0/-2.0` | contaminated unless rerun | deprecate or rerun |

## Numeric Check Status

Existing canonical fresh-instance evidence:

- `report_md/_gpt/json_gpt/fresh_instance_eval.json`
  - standard V4 fresh: `10.00 +/- 0.00%`
  - Ensemble HAT fresh: `86.365 +/- 1.535%`
- `report_md/_gpt/json_gpt/fresh_instance_eval_v4_ensemble_correlated_d2d.json`
  - iid row: `86.3288 +/- 1.6093%`

These were generated before the severe-NL bug fix, but they are expected to be unaffected because the checkpoint/training path is canonical `NL=1.0/-1.0`. A fresh post-fix GPU re-evaluation is still useful as `CX-CANONICAL-RECHECK`; it is not launched now because `CX-M1` owns the GPU and the rebuild plan forbids GPU contention.

## Immediate Risk List

1. `paper/latex_gpt/sections/05_results.tex` still says the severe-NL ceiling is structural and cites `30.53 +/- 7.07%`; this is contaminated.
2. `paper/latex_gpt/sections/06_discussion.tex` still contains the `N=30` / structural-limit mechanism paragraph; this is contaminated.
3. `paper/latex_gpt/supplementary.tex` still contains group-wise NL ablation text and tables from the pre-fix severe-NL line; Kimi's `K-DRAFT-5` supplementary audit must flag these.
4. Any memo citing `38.95%`, `Hartigan p=0.98`, or `~30% structural ceiling` as evidence must receive an Erratum tag.

## Conclusion

The canonical NL=1.0 paper backbone is safe with respect to the STE branch-swap bug. The severe-NL story is not safe and must be rebuilt from M-series post-fix results.
