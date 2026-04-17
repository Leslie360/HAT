# Codex Artifact Destination Ruling (2026-04-13)

This memo decides where the latest GPU/exploratory artifacts belong:

- `main manuscript`
- `supplementary`
- `revision-only evidence`
- `paper-2 / framework backlog`

The rule is conservative: an artifact is promoted only if it is both source-grounded and narratively stable.

---

## 1. `ablation_ensemble_results.json`

- **Destination:** `supplementary` + optional one-sentence pointer in main text
- **Why:** This is the clearest evidence that Ensemble HAT is not interchangeable with generic i.i.d. perturbation augmentation.
- **Safe main-text use:** one sentence reinforcing the cross-instance transfer point
- **Do not do:** add a full new main-text subsection unless the figure/table is already visually integrated

## 2. `pure_digital_adc_sweep.json`

- **Destination:** `supplementary` + keep current main-text pointer
- **Why:** It cleanly separates the digital quantization cliff from hybrid analog-digital degradation.
- **Safe main-text use:** retain the current sentence that a pure-digital control confirms the 6-bit cliff is not solely a digital-Transformer artifact
- **Do not do:** over-expand the digital control beyond a concise causal clarification

## 3. `retention_sensitivity_results.json`

- **Destination:** `supplementary`
- **Why:** Useful for defending proxy-parameter robustness, but too detailed and parameterized for the current main-text narrative.
- **Best use:** parameter-robustness table or mini-matrix in supplementary
- **Do not do:** elevate to abstract/conclusion

## 4. `combined_stress_results.json`

- **Destination:** `supplementary` or `revision-only evidence`
- **Why:** It is scientifically useful, but the combined-stress setting is a constructed bundle rather than a canonical deployment point.
- **Best use:** robustness appendix / reviewer-response support
- **Do not do:** present it as a new central headline result

## 5. `tiny_imagenet_eval_results.json`

- **Destination:** `paper-2 / framework backlog`
- **Current status:** exploratory failure / protocol-debug asset
- **Why:** The present artifact is non-degenerate in the sense that it records a real run, but all reported accuracies are `0.00%`, and the current metadata indicates a likely class-space / evaluation mismatch (`dataset = imagenet1k` with `tiny-imagenet-200/val`).
- **Do not do:** cite this as evidence of completed large-scale validation

## 6. ImageNet-1K preparation / download scripts

- **Destination:** `paper-2 / framework scale-readiness backlog`
- **Why:** Valuable infrastructure, but not manuscript evidence until a valid evaluation protocol and non-degenerate result exist.

---

## Summary Table

| Artifact | Destination | Main-text eligible? | Notes |
|:--|:--|:--:|:--|
| `ablation_ensemble_results.json` | supplementary | Yes, brief pointer only | Strong novelty-defense asset |
| `pure_digital_adc_sweep.json` | supplementary | Yes, brief pointer only | Supports ADC-cliff causality |
| `retention_sensitivity_results.json` | supplementary | No | Parameter-robustness evidence |
| `combined_stress_results.json` | supplementary / revision-only | No | Good reviewer-defense support |
| `tiny_imagenet_eval_results.json` | paper-2 backlog | No | Current output is exploratory/debug-grade |

---

## Practical Rule

If an artifact:

1. sharpens an already central claim, and
2. has a stable protocol, and
3. does not force a new narrative branch,

then it may enter `main text` as a short pointer.

Otherwise it should live in `supplementary` or the long-horizon backlog.
