# G-HH14: Post-Loop Experiment Queue
**Date:** 2026-05-01
**Scope:** Phase δ

If Paper-2 gets accepted, the next-quarter GPU queue will focus entirely on validating the mitigation of bimodal basins:

1. **HA-SAM Pilot (40 GPU-h):** Implement a first-order approximation of SAM tailored for asymmetric D2D noise. Test if the 22-62% variance collapses to a stable ~55%.
2. **Softmax Temperature Sweep (20 GPU-h):** Artificially scale the Softmax temperature $\tau \in [1.0, 5.0]$ during training. Does smoothing the attention distribution eliminate the bimodality?
3. **Performer / Linear Attention Baseline (60 GPU-h):** Swap the standard ViT attention block for a Linear Attention block. Evaluate at NL=2.0 to confirm the Lipschitz hypothesis.
