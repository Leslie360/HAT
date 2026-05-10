# Gemini Joint Training Spec — 2026-04-20

Goal: thesis-only experiment combining MLP-linear protection with Ensemble HAT to recover fresh-instance transfer beyond the current ~32% ceiling.

## Proposal
- Start from the canonical Ensemble HAT checkpoint rather than cold-start training.
- Apply the MLP-linear severe-NL protection while retaining epoch-level D2D resampling.
- Primary target metric: recover >=80% fresh-instance accuracy under the same `10 arrays × 5 MC` protocol.

## Ablation matrix
1. Ensemble HAT only
2. MLP-linear only
3. Joint MLP-linear + Ensemble HAT warm-start
4. Joint MLP-linear + Ensemble HAT cold-start

## Budget
- Treat this as a thesis experiment, not a submission-path task.
- Only launch after the current manuscript is submitted and metadata no longer blocks the archive.
