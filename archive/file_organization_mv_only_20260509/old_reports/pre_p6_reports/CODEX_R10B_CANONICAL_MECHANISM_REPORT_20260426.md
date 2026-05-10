# Codex R10B Canonical Collapse-Mechanism Report

Date: 2026-04-26  
Owner: Codex  
Status: COMPLETE, manuscript text patched and compiled

## Executive Verdict

The earlier R10B proxy output evaluated post-fix M-series checkpoints and was not valid evidence for the canonical Standard-HAT 10% fresh-instance collapse. Codex reran the diagnostic on the canonical checkpoints and replaced the manuscript wording.

Canonical fixed-mask Standard HAT does not merely lose calibration under fresh D2D instances. It degenerates into a deterministic single-class predictor:

- Accuracy: `10.00 +/- 0.00%` over 5 fresh D2D instances.
- Prediction entropy: approximately `0`.
- Maximum-class frequency: `100%`.
- Instance-0 prediction counts: `[0, 0, 0, 0, 0, 0, 0, 10000, 0, 0]`.

Canonical Ensemble HAT under the same 5-instance diagnostic remains healthy:

- Accuracy: `85.97 +/- 1.98%`.
- Prediction entropy: `2.28` vs `ln(10)=2.3026`.
- Maximum-class frequency: `15.27 +/- 2.27%`.

Therefore the paper should describe the canonical V4 failure mode as **deterministic single-class fresh-instance collapse**, not as the post-fix M-series recovery case.

## Source Artifacts

- JSON: `report_md/_gpt/json_gpt/r10b_standard_hat_class_distribution.json`
- Figure PDF: `paper/latex_gpt/figures/figS_standard_hat_collapse_mechanism.pdf`
- Figure PNG: `paper/latex_gpt/figures/figS_standard_hat_collapse_mechanism.png`
- Script: `scripts/_gpt/run_r10b.py`

## Manuscript Changes

Patched:

- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/supplementary.tex`

Removed from the manuscript narrative:

- The stale post-fix M-series statement: `82.31 +/- 0.37%` Standard HAT and `80.25 +/- 0.51%` Ensemble HAT.
- The claim that this M-series diagnostic confirms the canonical V4 collapse mechanism.

Inserted:

- Standard HAT canonical collapse: `10.00 +/- 0.00%`, entropy approximately `0`, max-class frequency `100%`.
- Ensemble HAT canonical control: `85.97 +/- 1.98%`, entropy `2.28`, max-class frequency `15.27 +/- 2.27%`.

## Verification

Commands run:

```bash
cd /home/qiaosir/projects/compute_vit/paper/latex_gpt
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex
grep -i "warning\|undefined\|error" main.log supplementary_main.log | grep -v infwarerr || true
```

Results:

- `main.tex`: compile RC 0.
- `supplementary_main.tex`: compile RC 0.
- Warning/undefined/error grep: empty.

Locked-number guard also remains clean:

- `scripts/_gpt/check_locked_numbers.py`: `16/16 passed`.

## Coordination Notes

- Kimi/Gemini/DeepSeek should treat the old post-fix M-series R10B wording as superseded for manuscript use.
- Post-fix M-series remains useful as a separate diagnostic/control family, but it is not the canonical collapse-mechanism evidence.
- R10A seed456 has completed training and is now under fresh-instance evaluation. R10A seed789 continues training.
