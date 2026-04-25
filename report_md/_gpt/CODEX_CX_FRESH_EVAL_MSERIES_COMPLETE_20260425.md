# M-Series Fresh Eval Complete Report

**Date:** 2026-04-25  
**Git HEAD:** 33bed9c (dual bug fix)  
**Evaluator:** eval_fresh_instances_postfix.py  
**Hardware:** NVIDIA GeForce RTX 5070 Ti (16GB)

## Complete Results (M1-M9)

| Model | HAT Variant | Noise | Seed | Mean | Std | Range |
|-------|-------------|-------|------|------|-----|-------|
| M1 | Standard (V3) | Uniform | 123 | 81.89% | 1.02% | 80.32--83.51% |
| M5 | Standard (V3) | Uniform | 456 | 80.37% | 0.08% | 80.24--80.49% |
| M7 | Standard (V3) | Uniform | 789 | 81.33% | 0.46% | 80.49--81.79% |
| M2 | Ensemble (V4) | Uniform | 123 | 80.37% | 0.59% | 79.28--81.12% |
| M6 | Ensemble (V4) | Uniform | 456 | 81.04% | 1.73% | 77.71--82.88% |
| M8 | Ensemble (V4) | Uniform | 789 | 80.21% | 0.20% | 79.84--80.65% |
| M3 | Ensemble (V4) | Proportional | 123 | 80.64% | 0.13% | 80.43--80.84% |
| M4 | Ensemble (V4) | Proportional | 456 | 80.67% | 0.41% | 79.95--81.18% |
| M9 | Ensemble (V4) | Proportional | 789 | 81.18% | 0.37% | 80.53--81.63% |

## Cross-Seed Averages (n=3 seeds each)

| HAT Variant | Noise | Cross-Seed Mean | Cross-Seed Std |
|-------------|-------|-----------------|----------------|
| Standard (V3) | Uniform | **81.20%** | 0.84% |
| Ensemble (V4) | Uniform | **80.54%** | 0.43% |
| Ensemble (V4) | Proportional | **80.83%** | 0.30% |

## Key Findings

1. **All routes recover to ~80--82% band**: Confirmed across 9 models (3 seeds × 3 configurations).
2. **Standard vs Ensemble HAT**: No statistically significant separation (81.20% vs 80.54%, well within seed variance).
3. **Proportional vs Uniform noise**: No special advantage under NL=2.0 (80.83% vs 80.54%).
4. **Seed stability**: M8 (Ensemble Uniform seed789) shows exceptionally low std (0.20%), indicating robust Ensemble HAT convergence at this seed.
5. **M7 consistency**: M7 (Standard Uniform seed789) mean=81.33%, consistent with M1 (81.89%) and M5 (80.37%).

## Updated Text

05_results.tex §5.3 "Four observations" paragraph updated to reflect three-seed cross-seed averages:
- Standard uniform: 81.20%
- Ensemble uniform: 80.54%
- Proportional: 80.83%

## Files
- `report_md/_gpt/json_gpt/cx_m*_fresh_eval.json` (M1-M9)
