# Gemini Day 2-3 Tasks: Tables, Figures, and Provenance

## 1. Main Precision Ladder Table (Accuracy vs Drift Drop)

| Precision | Source Best Mean | Fresh Mean | 1d Drift Drop | Role in Deployment |
| :--- | :--- | :--- | :--- | :--- |
| **8-bit PCM** | 77.64 ± 0.68% | 77.60 ± 0.64% | 0.04pp | Drift-flat reference, maximum stability |
| **6-bit PCM** | 77.88 ± 0.58% | 77.86 ± 0.56% | 0.10pp | **Best tested Pareto midpoint** |
| **4-bit PCM** | 76.71 ± 0.46% | 76.68 ± 0.37% | 4.01pp | Maximum compression, trainable but drift-limited |

*(Note: Data reflects locked canonical numbers for PCM UnitCell across 3 seeds. 6-bit is the best tested Pareto midpoint in this PCM UnitCell matrix, not a claim of global optimality.)*

## 2. SI Figure: 6-bit Seed 456 Late-Recovery Training Curve

**Purpose:** To explicitly preempt p-hacking accusations by showing the necessity of the full 100-epoch schedule.

*   **Artifact Note:** `r11d_6bit_pcm_seed456` originally stopped at Epoch 56 (`patience=10`) with a best test of ~69%.
*   **Corrected Curve:** `r11d_6bit_pcm_seed456_full100` recovers late in the schedule (low LR phase), reaching 78.49% by Epoch 100.
*   **Caption to include in SI:** "Figure S-X: Training trajectory of 6-bit PCM (seed 456). Initial experiments utilizing a patience=10 early-stopping criterion falsely terminated in a poor local minimum (~69%). Complete 100-epoch training shows late recovery in this 6-bit seed, reaching 78.49%. All canonical precision-ladder results therefore use the matched full 100-epoch schedule to avoid early-stop artifacts being mistaken for physical instability."

## 3. SI Provenance Table (Paths and Seeds)

| Configuration | Precision | Seed | Checkpoint Directory | Early-Stop Policy |
| :--- | :--- | :--- | :--- | :--- |
| PCM UnitCell | 8-bit | 123 | `checkpoints/r11d_5a_pcm_seed123` | `patience=0` (100 ep) |
| PCM UnitCell | 8-bit | 456 | `checkpoints/r11d_5a_pcm_seed456` | `patience=0` (100 ep) |
| PCM UnitCell | 8-bit | 789 | `checkpoints/r11d_5a_pcm_seed789` | `patience=0` (100 ep) |
| PCM UnitCell | 6-bit | 123 | `checkpoints/r11d_6bit_pcm_seed123` | `patience=0` (100 ep) |
| PCM UnitCell | 6-bit | 456 | `checkpoints/r11d_6bit_pcm_seed456_full100` | `patience=0` (100 ep) |
| PCM UnitCell | 6-bit | 789 | `checkpoints/r11d_6bit_pcm_seed789` | `patience=10`, not triggered (100 ep) |
| PCM UnitCell | 4-bit | 123 | `checkpoints/r11d_7_pcm_4bit_seed123` | `patience=0` (100 ep) |
| PCM UnitCell | 4-bit | 456 | `checkpoints/r11d_7_pcm_4bit_seed456_clean` | `patience=0` (100 ep) |
| PCM UnitCell | 4-bit | 789 | `checkpoints/r11d_7_pcm_4bit_seed789` | `patience=0` (100 ep) |
