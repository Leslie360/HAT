# Gemini ImageNet Pilot Scope — 2026-04-20

- Recommended first stage: ImageNet-100 rather than full ImageNet-1k.
- Model: Tiny-ViT family, smallest variant that preserves the current mixed-signal mapping logic.
- Training protocol: start with canonical Ensemble HAT cadence (per-epoch D2D resampling), then test whether a shorter schedule preserves ranking.
- Decision points:
  1. If training instability appears before useful convergence, reduce resolution / model size before changing the hardware protocol.
  2. If the 6-bit threshold shifts materially upward, keep that as the main pilot finding rather than forcing full performance recovery.
- Success criterion: preserve the ranking logic (ADC cliff, instance-overfitting mitigation, bounded spatial-correlation degradation), not necessarily absolute SOTA accuracy.
