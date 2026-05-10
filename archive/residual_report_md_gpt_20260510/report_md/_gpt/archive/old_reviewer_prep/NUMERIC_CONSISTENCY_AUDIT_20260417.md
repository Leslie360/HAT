# Numeric Consistency Audit — 2026-04-17

## Scope

Audited against the locked sources requested in `CODEX_DISPATCH_20260417_gpt.md`:

- `crosssim_clean_baseline.json`
- `crosssim_low_noise.json`
- `crosssim_standard_noise.json`
- `sobol_sensitivity.json`
- `convnext_adc_sweep_results.json`
- `CLAUDE_TASK_gpt.md`
- `paper/CANONICAL_RESULT_LOCK_gpt.md`
- `report_md/json/resnet18_results.json`
- `report_md/_gpt/RESNET_CHECKPOINT_AUDIT_20260416.md`

Files checked:

- [00_abstract.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/00_abstract.tex)
- [01_introduction.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/01_introduction.tex)
- [05_results.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex)
- [06_discussion.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/06_discussion.tex)
- [07_conclusion.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/07_conclusion.tex)
- [supplementary.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex)

## Verified As Correct

| Metric | Locked value | Manuscript state |
|:--|:--|:--|
| Ensemble HAT fresh transfer | `86.37 ± 1.54%` | Verified in abstract, introduction, results, discussion, conclusion, supplement |
| OPECT zero-shot | `88.53%` | Verified in abstract, results, conclusion, supplement |
| NL=2.0 boundary | `27.72 ± 0.82%` | Verified in abstract, introduction, results, discussion, conclusion |
| ConvNeXt proportional-noise 3-seed | `84.75 ± 0.72%` | Verified in results and supplement |
| ConvNeXt ADC sweep | `48.4 ± 16.2%` at 4-bit; `88.6 ± 0.3%` at 6-bit | Verified in results |
| Proportional-noise Tiny-ViT recovery | `97.37 ± 0.05%` | Verified in results |
| Frequency ablation best | `88.41%` | Verified in results and supplement |
| Sobol summary | `S_ADC≈0.976 -> 0.98`, `S_D2D≈0.922 -> 0.92` | Verified in discussion, results, conclusion, supplement |

## Corrected In This Pass

| File | Previous text | Corrected text | Source |
|:--|:--|:--|:--|
| [06_discussion.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/06_discussion.tex) | `82.3% vs. 67.9%` | `81.6% vs. 67.2%` | `crosssim_standard_noise.json` |
| [05_results.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex) baseline table | `ResNet-18 CIFAR-10 = 94.98%` | `95.46%` | `RESNET_CHECKPOINT_AUDIT_20260416.md` |
| [05_results.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex) summary table | mixed MC/best values for `R3/R4`, `V3/V4`, incomplete `C3/C4` cross-dataset rows | normalized to locked best-checkpoint values for cross-dataset rows and retained `±` only for stochastic physical-extension rows | `CANONICAL_RESULT_LOCK_gpt.md`, `resnet18_results.json` |

## Result-Summary Table Lock After Correction

Cross-dataset rows in `Table~\\ref{tab:result-summary}` now use:

- ResNet-18: `95.46 / 16.48 / 90.37` on CIFAR-10 and `78.64 / 1.00 / 1.00` on CIFAR-100
- Tiny-ViT-5M: `98.06 / 89.54 / 91.94` on CIFAR-10 and `86.94 / 44.06 / 65.48` on CIFAR-100
- ConvNeXt-Tiny: `90.74 / 70.48 / 89.91` on CIFAR-10 and `64.12 / 23.86 / 60.54` on CIFAR-100

This matches the canonical rule that grouped cross-dataset narrative/table values use locked best-checkpoint numbers rather than Monte Carlo means.
