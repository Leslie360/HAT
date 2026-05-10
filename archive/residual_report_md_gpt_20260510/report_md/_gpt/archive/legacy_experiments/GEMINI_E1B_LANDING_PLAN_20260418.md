# GEMINI E1B LANDING PLAN — 2026-04-18

**Reread of canonical state:** I have re-read `GEMINI_E1B_EXECUTION_REFINEMENT_20260418.md` (the runbook containing CLI invocations, the 9-run $3 \times 3$ grid, and the $\sim 15$ GPU-hour estimate for cross-architecture HAT + inverse-gamma joint retraining).

## 1. Pre-Launch Smoke Test Sequence
Before committing the 15-hour batch, Codex must run these three 1-epoch dry runs and assert pass/fail criteria:

- **Smoke 1 (ResNet-18):**
  - *Command:* `python train_resnet18.py --experiment R_Smoke_E1b --epochs 1 --batch_size 16 --apply_inverse_gamma True --gamma_phys 2.0`
  - *Pass Criteria:* Completes 1 epoch; logs show `gamma_comp=0.5000` initialized; validation accuracy $> 10.0\%$.
- **Smoke 2 (ConvNeXt-Tiny):**
  - *Command:* `python train_convnext.py --experiment C_Smoke_E1b --epochs 1 --batch_size 16 --apply_inverse_gamma True --gamma_phys 2.0`
  - *Pass Criteria:* No tensor dimension mismatch during the `InverseGammaPreprocessor` injection; model successfully saves `best.pt`.
- **Smoke 3 (Tiny-ViT):**
  - *Command:* `python train_tinyvit_ensemble.py --experiment V_Smoke_E1b --epochs 1 --batch_size 16 --apply_inverse_gamma True --gamma_phys 2.0`
  - *Pass Criteria:* Completes without CUDA OOM; `test_acc` is printed in logs.

## 2. Failure-Mode Catalog

| Failure Mode | Diagnostic | Recovery Action |
|:--|:--|:--|
| **F1: `apply_inverse_gamma` Unrecognized** | `argparse` throws unrecognized argument error on ResNet/ConvNeXt. | Codex must patch `train_resnet18.py`/`train_convnext.py` to accept the frontend args and instantiate `PhysicalFrontEnd`, mirroring Tiny-ViT. |
| **F2: CUDA Out-Of-Memory (OOM)** | Script crashes mid-epoch with `CUDA out of memory`. | Reduce `--batch_size` from 128 to 64; double `--update_freq` (gradient accumulation) to maintain effective batch size. |
| **F3: Accuracy stuck at 10.00%** | Validation accuracy flatlines near chance level for $> 5$ epochs. | Indicates frontend saturation. Verify inputs are clamped to $[1e-8, 1.0]$ before applying the $\gamma$ exponent. |
| **F4: NaN Loss** | Loss explodes to `NaN` during AMP mixed-precision scaling. | The $X^{0.5}$ operation generates NaNs if inputs are exactly 0. Ensure `eps` clamping is strictly applied in the preprocessor. |
| **F5: Missing D2D Resampling** | Train accuracy is high ($>95\%$), but test accuracy collapses to chance. | Ensemble HAT mask resampling is missing in the training loop. Port `resample_d2d_noise()` logic into the specific architecture's loop. |

## 3. Mid-Run Check-in Cadence
Codex should pause and report status to `AGENT_SYNC_gpt.md` at two distinct points:
1. **Checkpoint 1 (After Architecture 1):** Once the $3$ ResNet-18 seeds complete ($\sim 3$ hours). Report the mean accuracy to ensure the joint retraining is actually yielding expected benefits before burning the ConvNeXt/ViT budget.
2. **Checkpoint 2 (After Architecture 2):** Once ConvNeXt completes ($\sim 9$ hours total elapsed). Confirm the JSON summary file has correctly aggregated the first two architectures.

## 4. Output Schema
The tracking script (or post-processing analyzer) should aggregate the results into a JSON schema like this for downstream Sobol/robustness plotting:
```json
{
  "E1b_joint_retraining": {
    "ResNet-18": {
      "gamma_phys": 2.0,
      "I_dark": 1e-11,
      "seeds": [42, 123, 456],
      "best_acc_runs": [84.1, 84.5, 83.9],
      "mean_acc": 84.17,
      "std_acc": 0.31
    },
    "ConvNeXt-Tiny": { ... },
    "Tiny-ViT": { ... }
  }
}
```

## 5. Hand-off Checklist
Before Codex declares E1b complete, they must verify:
- [ ] 9 total `.pt` checkpoint files exist in `checkpoints/E1b/` (or equivalent directory).
- [ ] 9 separate log files are preserved in `logs/E1b/`.
- [ ] A consolidated JSON summary matching the schema above is saved to `report_md/_gpt/json_gpt/E1b_results.json`.
- [ ] No `NaN` losses or $10.0\%$ flatlines occurred in the final reported metrics.