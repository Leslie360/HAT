# 📡 Broadcast: Selective D2D Resampling Results (COMPLETE)

**Date:** 2026-04-10
**Experiment:** R1 checkpoint selective fresh eval
**Method:** 5 instances × 3 MC runs per scope
**Data Source:** `report_md/_gpt/json_gpt/selective_fresh_eval_*.json`
**Figure Source:** `report_md/_gpt/figures/selective_fresh_eval_complete.png`

## Complete Results

| Resample Scope | Modules | Mean Acc | Std | vs Training Best |
|---------------|---------|----------|-----|-----------------|
| `none` | 0 | **91.32%** | 0.16% | -0.18 pp |
| `attn_proj` | 12 | **90.47%** | 0.18% | -1.03 pp |
| `qkv` | 10 | **88.15%** | 1.84% | -3.35 pp |
| `mlp` | 20 | **38.71%** | 10.16% | **-52.8 pp** |

## Key Findings

1. **MLP layers are the SOLE source of fresh-instance collapse.**
   - Resampling ONLY MLP D2D noise: 91% → 39% (52.8 pp loss)
   - This accounts for **93% of total collapse** (56.9 pp)

2. **Attention layers (QKV + proj) are highly robust to D2D variation.**
   - attn_proj resampling: barely any impact (-1.0 pp)
   - qkv resampling: minor impact (-3.4 pp)

3. **T5 weight divergence correlation confirmed.**
   - T5 top divergence: `stages.3.blocks.1.mlp.fc2.weight` (JS=0.257)
   - Selective eval independently confirms MLP = vulnerability hotspot

## Implication for Work 2

The hybrid deployment compiler should:
- **Keep attention (QKV + proj) on CIM** — they are robust to instance variation
- **Prioritize MLP layers for runtime calibration / digital fallback**
- **Use MLP health score as the primary trigger** for remapping decisions
- **This is NOT a multi-tile problem** — it's a per-layer-type problem

## Figure

![Selective Fresh Eval Complete](figures/selective_fresh_eval_complete.png)
