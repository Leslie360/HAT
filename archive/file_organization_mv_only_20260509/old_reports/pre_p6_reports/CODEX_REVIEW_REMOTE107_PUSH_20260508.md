# Codex Review — Remote107 Push `origin/107-clean@d8e3b17`

Date: 2026-05-07 16:55 +08
Reviewer: Codex
Scope: fetch-only review; no merge into dirty Paper-1 worktree

## 1. Repository Handling

Remote update detected:

- Previous reviewed commit: `cc0a3ab`
- New remote head: `d8e3b17`
- Branch: `origin/107-clean`

Local `paper1-release-20260501` worktree is heavily dirty due to Kimi/Gemini/Codex manuscript and figure work. I did **not** pull or merge.

A detached review worktree was created instead:

```text
/home/qiaosir/projects/HAT_107_clean_review
```

This keeps Remote107 artifacts accessible without contaminating Paper-1 manuscript work.

## 2. New Remote107 Deliverables

Key new files reviewed:

- `coordination/REMOTE107_BASELINE_EPSC_RETURN_20260508.md`
- `coordination/REMOTE107_P0A_BASELINE_VERDICT.md`
- `coordination/REMOTE107_P0B_ABLATION_RETURN_20260508.md`
- `coordination/REMOTE107_P1_EPSC_RETURN_20260508.md`
- `coordination/REMOTE107_P2_P1B_RETURN_20260508.md`
- `coordination/REMOTE107_P3_P2D8B_RETURN_20260508.md`
- `deliverable/results_v3/p0b_ablation/summary.csv`
- `deliverable/results_v3/epsc_stress/summary.csv`
- `deliverable/results_v3/p1b_1b/*.json`
- `deliverable/results_v3/p2d8b_2d8b/*.json`
- `deliverable/results_v3/train_meta/*.json`

## 3. Locked Numerical Updates

### 3.1 Baseline Reconciliation

Remote107 explicitly resolves the old baseline mismatch:

| Evaluator | Context / stride / batch | PPL | Status |
|---|---:|---:|---|
| Current K107 evaluator | 512 / 256 / 1 | 22.18 | canonical |
| Old vectorized evaluator | 1024 / 512 / 8 | 15.62 | deprecated / not comparable |

Ruling:

- K107 comparisons must use `22.18` as the raw digital baseline.
- The old `15.68`-style number is evaluator-dependent and must not be mixed into K107 tables.

### 3.2 P0-B Paired Ablation Means

Computed directly from `deliverable/results_v3/p0b_ablation/summary.csv`:

| Mode | Meaning | n | Mean PPL | Range |
|---|---|---:|---:|---:|
| B1 | HAT checkpoint, digital/no analog patch | 3 | 19.0430 | 18.9929-19.0854 |
| B2 | analog patch, no noise | 3 | 19.0597 | 19.0103-19.1010 |
| B3 | D2D=0.02 | 9 | 19.4829 | 19.4265-19.5597 |
| B4 | D2D=0.05 | 9 | 19.6437 | 19.5837-19.7373 |

Interpretation:

- HAT fine-tuning gain vs raw digital baseline is approximately `22.18 -> 19.04`, i.e. about `-3.14 PPL`.
- Analog patch overhead without noise is negligible: `B2-B1 ~= +0.017 PPL`.
- D2D=0.02 adds about `+0.44 PPL` over patch-no-noise.
- D2D=0.05 adds about `+0.58 PPL` over patch-no-noise.

Important correction:

- Earlier local notes using `patch-no-noise ~=18.38` and `gain ~=3.80 PPL` should be treated as superseded unless their evaluator/checkpoint protocol is proven identical. The new Remote107 return is better documented and should become canonical for K107.

### 3.3 EPSC Proxy Stress

Computed from `deliverable/results_v3/epsc_stress/summary.csv`:

| Config | Noise | n | Mean PPL | Max PPL | Verdict |
|---|---|---:|---:|---:|---|
| EPSC-e1 | C2C=0.05, D2D=0.05 | 9 | 19.7176 | 19.8131 | pass |
| EPSC-e2 | C2C=0.10, D2D=0.10 | 9 | 20.1161 | 20.2306 | pass |
| EPSC-e3 | C2C=0.15, D2D=0.15 | 9 | 20.7624 | 20.8688 | pass |
| EPSC-e4 | C2C=0.00, D2D=0.20 | 9 | 20.6040 | 20.7536 | pass |
| EPSC-e5 | C2C=0.01, D2D=0.10 | 9 | 19.8614 | 19.9741 | pass |

Ruling:

- EPSC proxy compatibility is strong under this proxy model.
- Central EPSC stress `0.10/0.10` maxes at `20.23`, safely below the `25 PPL` kill line.
- D2D remains the stronger degradation channel, but terminal-layer KV is robust.

### 3.4 Model Scale Check

Computed from committed eval JSONs:

| Model | Eval D2D | n | Mean PPL | Std | Range |
|---|---:|---:|---:|---:|---:|
| Pythia-1B | 0.02 | 6 | 14.6021 | 0.0190 | 14.5785-14.6378 |
| Pythia-1B | 0.05 | 6 | 14.8193 | 0.0265 | 14.7916-14.8711 |
| Pythia-2.8B | 0.02 | 6 | 13.3345 | 0.0117 | 13.3090-13.3443 |
| Pythia-2.8B | 0.05 | 6 | 13.4307 | 0.0121 | 13.4121-13.4479 |

Ruling:

- K107 selective terminal-layer analog KV improves with scale in these tests: 410M -> 1B -> 2.8B.
- Pythia-2.8B is very stable across train/eval seeds.
- `D2D=0.05` overhead at 2.8B is only about `+0.10 PPL` over `D2D=0.02`.

## 4. Code Review Notes

Remote107 added an OOM fix in `p3_hat_train.py`:

- For selective analog layers, only optimize patched attention layer parameters instead of all model parameters.
- Falls back to full-model optimization if target params cannot be found.

This is pragmatic and explains why 2.8B could run. However, manuscript/provenance should state that Pythia-2.8B HAT used selective-layer optimization, not full-model fine-tuning. This is not a blocker because the method is terminal-layer analog KV, but it must be explicit.

## 5. Impact on Current Local Work

### Paper-1

No direct change. Paper-1 is the analog vision / PCM precision-retention manuscript. K107 is a Paper-2 or companion direction. Do not mix K107 PPL results into Paper-1 main claims.

### Kimi Local GPU Queue

Do **not** interrupt Kimi's local PCM frontier queue. The current Kimi assignment remains correct:

1. Inventory local 4/5/6/8-bit PCM frontier artifacts.
2. Close missing 5-bit PCM cells if needed.
3. Re-eval canonical 4/6/8-bit only if provenance is weak.

Remote107 results do not reduce the value of this local queue because it addresses Paper-1's central PCM frontier claim, not K107.

### Gemini Figure Work

Gemini can continue Paper-1 appendix/main figure polish. If Gemini touches K107 figures later, use only the locked values above, not older 15.68/18.38-era notes.

## 6. Recommended Next Actions

1. Keep `origin/107-clean` isolated in `/home/qiaosir/projects/HAT_107_clean_review` for data extraction.
2. Broadcast that K107 canonical baseline is `22.18` and that `15.62/15.68` is deprecated for K107 comparisons.
3. For any K107 manuscript/figure draft, use three panels:
   - P0-B paired ablation: raw digital baseline -> HAT digital -> no-noise patch -> D2D noise.
   - EPSC proxy stress: e1-e5 curve with kill line at 25 PPL.
   - scale trend: 410M / 1B / 2.8B terminal-layer KV PPL.
4. Do not merge `107-clean` into the dirty Paper-1 branch. Later integration should be a clean PR/branch or a curated data copy.

## 7. Current Verdict

Remote107 has produced a strong, well-documented K107 result package. The most important correction is baseline discipline:

> Use 22.18 as raw canonical K107 digital baseline; use ~19.04 as HAT-trained digital/no-analog checkpoint PPL; report HAT gain as ~3.1 PPL under the current evaluator.

Kimi/Gemini can continue their current local tasks without conflict.
