# Supplementary Information (SI)

## S1. Full Local PCM Precision-Ladder Per-Seed Tables

The following tables detail the raw performance metrics across all three random seeds used to calculate the canonical means in the main text.

**Table S1: 8-bit PCM UnitCell**
| Seed | Best Test | Fresh Mean ± Std | Drift 1d | 0s→1d Drop |
|---:|---:|---:|---:|---:|
| 123 | 77.00% | 77.00 ± 0.05% | 77.01% | -0.15pp |
| 456 | 78.36% | 78.27 ± 0.05% | 78.22% | 0.24pp |
| 789 | 77.56% | 77.52 ± 0.04% | 77.49% | 0.03pp |
*(Note: 3-seed Mean: 77.64%, Fresh: 77.60%, Drop: 0.04pp)*

**Table S2: 6-bit PCM UnitCell**
| Seed | Best Test | Fresh Mean ± Std | Drift 1d | 0s→1d Drop |
|---:|---:|---:|---:|---:|
| 123 | 77.33% | 77.36 ± 0.04% | 77.19% | 0.16pp |
| 456 | 78.49% | 78.47 ± 0.05% | 78.39% | 0.11pp |
| 789 | 77.81% | 77.75 ± 0.04% | 77.65% | 0.04pp |
*(Note: 3-seed Mean: 77.88%, Fresh: 77.86%, Drop: 0.10pp)*

**Table S3: 4-bit PCM UnitCell**
| Seed | Best Test | Fresh Mean ± Std | Drift 1d | 0s→1d Drop |
|---:|---:|---:|---:|---:|
| 123 | 76.74% | 76.65 ± 0.04% | 72.28% | 4.40pp |
| 456 | 77.15% | 77.07 ± 0.06% | 72.18% | 4.84pp |
| 789 | 76.23% | 76.33 ± 0.04% | 73.45% | 2.78pp |
*(Note: 3-seed Mean: 76.71%, Fresh: 76.68%, Drop: 4.01pp)*

## S2. 6-bit PCM Late-Recovery Training Curve

**Figure S1: Training trajectory of 6-bit PCM (seed 456).**
*(Insert plot of test accuracy vs. epoch here)*

Initial experiments utilizing a `patience=10` early-stopping criterion falsely terminated in a poor local minimum (~69% at epoch 56). Complete 100-epoch training shows late recovery in this 6-bit seed, reaching 78.49%. All canonical precision-ladder results therefore use the matched full 100-epoch schedule to avoid early-stop artifacts being mistaken for physical instability.

## S3. Provenance and Checkpoint Tracking

To ensure rigorous reproducibility, all canonical results are mapped to their generating scripts and deterministic seeds. All PCM precision-ladder runs enforced `--early-stop-patience 0`.

| Configuration | Precision | Seed | Checkpoint Directory | Early-Stop |
| :--- | :--- | :--- | :--- | :--- |
| PCM UnitCell | 8-bit | 123 | `r11d_5a_pcm_seed123` | `patience=0` |
| PCM UnitCell | 8-bit | 456 | `r11d_5a_pcm_seed456` | `patience=0` |
| PCM UnitCell | 8-bit | 789 | `r11d_5a_pcm_seed789` | `patience=0` |
| PCM UnitCell | 6-bit | 123 | `r11d_6bit_pcm_seed123` | `patience=0` |
| PCM UnitCell | 6-bit | 456 | `r11d_6bit_pcm_seed456_full100` | `patience=0` |
| PCM UnitCell | 6-bit | 789 | `r11d_6bit_pcm_seed789` | `patience=0` |
| PCM UnitCell | 4-bit | 123 | `r11d_7_pcm_4bit_seed123` | `patience=0` |
| PCM UnitCell | 4-bit | 456 | `r11d_7_pcm_4bit_seed456_clean` | `patience=0` |
| PCM UnitCell | 4-bit | 789 | `r11d_7_pcm_4bit_seed789` | `patience=0` |

## S4. Preliminary Remote Validation

Preliminary remote validation on DeiT/ViT suggests proportional noise-aware training preserves fresh-instance accuracy across transformer backbones, pending full multi-seed validation.
