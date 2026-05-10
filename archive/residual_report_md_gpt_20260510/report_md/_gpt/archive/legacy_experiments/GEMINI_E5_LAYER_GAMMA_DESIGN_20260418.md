# GEMINI E5 LAYER-WISE GAMMA DESIGN — 2026-04-18

**Reread of canonical state:** This design satisfies the E5 experiment placeholder. It assumes an architecture where the optical sublinear photoresponse ($\gamma_{\text{phys}}$) is either applied at the sensor input or distributed across optical interconnects between specific transformer blocks.

## 1. Goal & Hypothesis
**Goal:** Identify which structural depths of the Tiny-ViT V4 architecture are most sensitive to sublinear photoresponse ($\gamma_{\text{phys}}$) when uncompensated.
**Hypothesis:** If the optical frontend is applied to activations at each block boundary (cascaded optical array), the early layers (Patch Embedding and Blocks 0-1) will dominate the sensitivity. Sublinear distortion at these early stages irreversibly compresses the dynamic range of the token embeddings, stripping high-frequency spatial features before they reach the deeper attention heads.

## 2. Experimental Matrix
- **Architecture:** Tiny-ViT-5M (CIFAR-10).
- **$\gamma_{\text{phys}}$ values:** $\{0.5, 1.0, 1.5, 2.0\}$.
- **Layer Target Groups (where uncompensated $\gamma$ is applied; all other layers use ideal $\gamma=1.0$):**
  1. Patch Embedding only.
  2. Blocks 0 and 1 only (early features).
  3. Blocks 2 and 3 only (deep features).
  4. Classification Head only.
  5. All Layers (Baseline Canonical).
- **Total Cells:** $4 \times 5 = 20$ cells.

## 3. Required Code Modifications
To enable per-block $\gamma$ injection, `compute_vit/analog_layers.py` must expose layer indexing to the `PhysicalFrontEnd`.
**Pseudo-code implementation:**
```python
class PhysicalFrontEnd(nn.Module):
    def __init__(self, gamma_phys=1.0, layer_name=None, target_layers=None):
        super().__init__()
        self.layer_name = layer_name
        self.target_layers = target_layers or []

        # If this layer is in the target group, apply the specified gamma,
        # otherwise default to ideal 1.0
        if any(target in self.layer_name for target in self.target_layers):
            self.active_gamma = gamma_phys
        else:
            self.active_gamma = 1.0

    def forward(self, x):
        # Apply sublinear photoresponse
        return torch.pow(x.clamp(min=1e-8), self.active_gamma)
```
The model builder (`tinyvit.py`) will be patched to pass a string identifier (e.g., `"patch_embed"`, `"blocks.0"`) to the frontend instantiation.

## 4. Estimated GPU-Hours
- **Execution Type:** Inference-only evaluations using the existing HAT-trained V4 checkpoints.
- **Scale:** 20 cells $\times$ 3 MC seeds = 60 evaluations.
- **Cost:** ~2 GPU-hours.

## 5. Decision Criteria for Rebuttal vs Thesis
- **Promote to NC Rebuttal/Supplement:** If a single layer group (e.g., Patch Embed) accounts for $> 80\%$ of the accuracy drop seen in the "All Layers" baseline, it justifies a short rebuttal supplement arguing for a targeted heterogeneous architecture (e.g., keeping Patch Embed digital while running deep blocks analog).
- **Keep Thesis-Only:** If the degradation is evenly distributed across all block depths, it simply confirms compounding error, which is less novel for the journal submission but fits perfectly into the thesis architectural analysis chapter.
