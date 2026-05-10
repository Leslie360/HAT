# GEMINI E1b EXECUTION REFINEMENT — 2026-04-18

**Reread of canonical state:** Context established via `GEMINI_CONTEXT_REREAD_20260418.md` and the previously drafted E1/E2 Design memo.

## 1. Concrete CLI Invocation
To execute the E1b cross-architecture HAT + inverse-gamma joint retraining, we will utilize the existing training infrastructure with the frontend compensation flags activated.

**ResNet-18 (CIFAR-10):**
```bash
python train_resnet18.py --experiment R_E1b_HAT_Gamma --seed 42 --epochs 100 --batch_size 128 --lr 1e-4 --weight_decay 0.05 --sigma_c2c 0.05 --sigma_d2d 0.10 --hat_training True --gamma_phys 2.0 --I_dark 1e-11 --apply_inverse_gamma True
```

**ConvNeXt-Tiny (CIFAR-10):**
```bash
python train_convnext.py --experiment C_E1b_HAT_Gamma --seed 42 --epochs 100 --batch_size 128 --lr 1e-4 --weight_decay 0.05 --sigma_c2c 0.05 --sigma_d2d 0.10 --hat_training True --gamma_phys 2.0 --I_dark 1e-11 --apply_inverse_gamma True
```

**Tiny-ViT (CIFAR-10):**
*(Note: Already partially covered by `run_learnable_gamma_compensation_gpt.py`, but for a strict 1/γ fixed compensation parity, use the standard ensemble script).*
```bash
python train_tinyvit_ensemble.py --experiment V_E1b_HAT_Gamma --seed 42 --epochs 100 --batch_size 128 --lr 1e-4 --weight_decay 0.05 --sigma_c2c 0.05 --sigma_d2d 0.10 --hat_training True --gamma_phys 2.0 --I_dark 1e-11 --apply_inverse_gamma True
```

## 2. Hyperparameter Table

| Architecture | Dataset | $\gamma_{\text{phys}}$ | LR | WD | Epochs | Batch | Noise ($\sigma_{\text{C2C}}$/$\sigma_{\text{D2D}}$) | Status |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| ResNet-18 | CIFAR-10 | 2.0 | `1e-4` | 0.05 | 100 | 128 | 0.05 / 0.10 | Known (Standard HAT) |
| ConvNeXt | CIFAR-10 | 2.0 | `1e-4` | 0.05 | 100 | 128 | 0.05 / 0.10 | Known (Standard HAT) |
| Tiny-ViT | CIFAR-10 | 2.0 | `1e-4` | 0.05 | 100 | 128 | 0.05 / 0.10 | Known (Standard HAT) |

## 3. Seed & MC Policy
- **Training Seeds:** 3 independent seeds (`42`, `123`, `456`) per architecture.
- **Evaluation:** During validation, the same seed controls the fresh D2D evaluation mask (consistent with canonical reporting). No seeds are shared across different $\gamma_{\text{phys}}$ cells.
- Total runs: $3 \text{ architectures} \times 1 \text{ cell } (\gamma=2.0) \times 3 \text{ seeds} = 9$ training runs.

## 4. Wall-Clock & GPU-Hour Estimate
- ResNet-18: ~1 hour per run $\times 3 = 3$ hours.
- ConvNeXt-Tiny: ~2 hours per run $\times 3 = 6$ hours.
- Tiny-ViT: ~2 hours per run $\times 3 = 6$ hours.
- **Total Estimate:** ~15 GPU-hours.

## 5. Pre-flight Checks (Codex Runbook)
Before launching the 9-run grid, Codex must verify:
1. **Smoke Test 1 (CLI Args):** Run `python train_resnet18.py --help` to verify `--apply_inverse_gamma` (or equivalent flag) is exposed and correctly routes to the `InverseGammaPreprocessor`.
2. **Smoke Test 2 (Integration):** Launch ResNet-18 with `--epochs 1 --batch_size 16`. Verify it completes the epoch without CUDA OOM or dimension mismatches in the photoresponse frontend.
3. **Smoke Test 3 (Baseline Check):** Ensure the initial untrained accuracy matches digital random-init ($\sim 10\%$), confirming the frontend hasn't saturated the inputs to a single class prior to training.