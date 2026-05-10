# CLAUDE GPU Window Decision — Round M (2026-04-20)

**Decision:** AUTHORIZE `CX-FA` (Joint MLP-Linear + Ensemble HAT pilot smoke test).
**Rationale:**
1. The joint training formulation (G-AA3) is the primary novel contribution for the thesis fork (K-T6), making it the highest strategic priority.
2. The ImageNet-100 pilot (120 GPU-h) is a defensive measure for reviewers, but since we are pre-submission, we should prioritize the thesis-critical path while the GPU is idle.
3. The 3-epoch smoke test (`CX-FA`) is computationally cheap and will de-risk the full run for Round N without committing the full window yet.

**Status:** Codex (`CX-FA`) is authorized to proceed with the 3-epoch smoke test.
