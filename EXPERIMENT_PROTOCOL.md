# Immediate Experiment Protocol (No Collaboration)

**Date:** 2026-04-15  
**Status:** Ready to execute  
**Priority:** P0 experiments (Reviewer #4 W1, W2, W3, W7)

---

## Experiment 1: Framework Comparison Matrix (W1)

### Goal
Compare against 2+ frameworks on canonical + organic-specific configurations

### Configurations to Test

| Config | Our Framework | AIHWKIT | CrossSim | Target |
|:--|:--:|:--:|:--:|:--|
| **Canonical (inorganic-like)** |
| ResNet-18, CIFAR-10, 4-bit, σ=0.05 | 86.57% | 90.08% | TBD | ✅ Done |
| Tiny-ViT, CIFAR-10, 4-bit, σ=0.05 | Run | Run | N/A | New |
| **Organic-specific** |
| + Photoresponse (γ=0.8) | Run | ❌ N/A | ❌ N/A | Demonstrate capability |
| + Retention (τ=1h) | 82.31% | ❌ N/A | ❌ N/A | ✅ Done |
| + NL=2.0 | 27.72% | ❌ N/A | ❌ N/A | ✅ Done |

### Protocol
```bash
# Run on GPU, log all results
python run_framework_comparison.py \
  --configs canonical organic_features \
  --frameworks ours aihwkit \
  --output report_md/_gpt/framework_comparison.json
```

### Expected Output
- JSON with accuracy, runtime, memory for each config
- Feature matrix table for paper
- Runtime comparison: "Ours: 45min, AIHWKIT: 4h"

### Timeline: 3-5 days

---

## Experiment 2: Ensemble HAT Mechanism Ablations (W2)

### 2A: Resampling Frequency Ablation

**Question:** Is per-epoch optimal vs per-batch or per-N-epochs?

**Design:**
| Method | D2D Update | Expected | Rationale |
|:--|:--|:--|:--|
| Standard HAT | Fixed at init | 10.00% | Baseline (overfits) |
| Per-batch | Every batch | ~75% | Too much noise, underfits |
| Per-5-epochs | Every 5 epochs | ~80% | Medium frequency |
| **Per-epoch** | **Every epoch** | **86.57%** | **Optimal balance** |
| Per-20-epochs | Every 20 epochs | ~70% | Too infrequent |

**Protocol:**
```python
# Modify train_tinyvit_ensemble.py
def train_with_frequency(freq='epoch', N=1):
    # freq: 'batch', 'epoch', 'N_epochs'
    # N: number of epochs/batches between resamples
    for epoch in range(epochs):
        for batch in batches:
            if should_resample(freq, N, epoch, batch):
                resample_all_d2d_noise(model)
            train_step()
```

**Metric:** Zero-shot accuracy on fresh hardware instance

**Timeline: 2-3 days** (5 frequencies × 3 seeds = 15 runs)

---

### 2B: Spatial Correlation Ablation

**Question:** Is spatially-correlated D2D necessary vs i.i.d. noise?

**Design:**
| Method | D2D Pattern | Expected |
|:--|:--|:--|
| Standard HAT | Fixed spatial | 10.00% |
| **Ensemble HAT** | **Resampled spatial** | **86.57%** |
| i.i.d. per-epoch | Independent per layer | ~75% |
| i.i.d. per-batch | Independent per forward | ~70% |

**Protocol:**
```python
# Modify analog_layers.py
def resample_d2d_noise(mode='spatial'):
    if mode == 'spatial':
        # Current: spatially correlated mask
        noise = correlated_noise(shape)
    elif mode == 'iid':
        # New: independent per element
        noise = torch.randn(shape) * sigma
    self.d2d_noise.copy_(noise)
```

**Timeline: 2 days** (4 modes × 3 seeds = 12 runs)

---

### 2C: Literature Baseline Comparison

**Question:** How does Ensemble HAT compare to published HAT variants?

**Baselines to Implement:**
| Method | Source | Description |
|:--|:--|:--|
| Standard HAT | Original | Fixed D2D |
| Multi-instance HAT | [Ref needed] | Train on K fixed instances |
| Domain Randomization | [Ref needed] | Extreme noise augmentation |
| Noise Adversarial | [Ref needed] | Adversarial D2D training |

**Protocol:**
```bash
# Implement each variant
python run_baseline_comparison.py \
  --methods standard_hat ensemble_hat multi_instance domain_rand adversarial \
  --model tinyvit \
  --dataset cifar10 \
  --seeds 42 123 456
```

**Timeline: 3-4 days** (research + implementation + runs)

---

### 2D: C2C Robustness Trade-off

**Question:** Does Ensemble HAT sacrifice C2C robustness?

**Design:**
- Train: All methods with σ_d2d = 0.1
- Test: Vary σ_c2c from 0.0 to 0.2
- Hypothesis: No free lunch violation

**Expected:**
| Training | σ_c2c=0.0 | 0.05 | 0.1 | 0.2 |
|:--|:--|:--|:--|:--|
| Standard HAT | 10% | 10% | 9% | 8% |
| Ensemble HAT | 92% | 87% | 74% | 51% |

**Interpretation:** Ensemble HAT maintains expected C2C degradation

**Timeline: 2 days**

---

## Experiment 3: NL=2.0 Mechanism Analysis (W3)

### 3A: Layer-wise Sensitivity

**Question:** Which ViT layers are most affected by NL=2.0?

**Design:**
- Freeze all layers except one
- Train with NL=2.0 on unfrozen layer
- Measure accuracy contribution

**Protocol:**
```python
for layer_name in ['patch_embed', 'blocks.0', 'blocks.5', 'head']:
    model = load_model()
    freeze_all_except(model, layer_name)
    acc = train_with_nl(model, nl_ltp=2.0, nl_ltd=-2.0)
    print(f"{layer_name}: {acc:.2f}%")
```

**Expected:**
```
patch_embed:  XX%  (input embedding sensitive)
blocks.0-2:   XX%  (early features)
blocks.3-5:   XX%  (deep features)  
head:         XX%  (classification)
```

**Timeline: 3-4 days** (6 layers × 3 seeds = 18 runs)

---

### 3B: Weight Distribution Analysis

**Question:** How does NL=2.0 affect weight distributions?

**Metrics:**
- Weight magnitude distribution per layer
- Gradient norm distribution
- Effective learning rate per layer

**Protocol:**
```python
def analyze_nl_impact(model, epoch=50):
    for name, param in model.named_parameters():
        if 'weight' in name:
            print(f"{name}:")
            print(f"  Mean: {param.mean():.4f}")
            print(f"  Std: {param.std():.4f}")
            print(f"  % near zero: {(param.abs() < 0.01).float().mean():.2%}")
```

**Timeline: 1-2 days**

---

### 3C: Mitigation Strategy (Proposed Solution)

**Proposal:** Piecewise STE with NL-aware gradient correction

**Algorithm:**
```python
def nl_aware_ste(weight, grad, nl_ltp, nl_ltd):
    # Detect weight quadrant (LTP vs LTD)
    is_ltp = weight > 0
    
    # Apply NL-dependent scaling
    scale = torch.where(is_ltp, 
                       1.0 + nl_ltp * torch.abs(weight),
                       1.0 + nl_ltd * torch.abs(weight))
    
    # Corrected gradient
    corrected_grad = grad / scale
    return corrected_grad
```

**Validation:**
- Baseline NL=2.0: 27.72%
- With mitigation: Target >40% (any improvement validates concept)

**Timeline: 3-4 days** (implementation + tuning)

---

## Experiment 4: Statistical Standardization (W7)

### Protocol

All core experiments must use:
- **Seeds:** 42, 123, 456, 789, 1024 (n=5)
- **MC inference:** 10 runs per checkpoint
- **Stats:** Mean ± std, 95% CI, t-test vs baseline

### Experiments to Re-run

| Experiment | Current | Target | Effort |
|:--|:--|:--|:--|
| Tiny-ViT HAT (main) | 10 runs | ✅ Already good | None |
| ADC bit-width sweep | 1 seed | 5 seeds | 3-4 days |
| Retention time sweep | 1 seed | 5 seeds | 2-3 days |
| ConvNeXt proportional | 3 seeds | 5 seeds | 1-2 days |
| ResNet-18 CIFAR-10 | 1 seed | 5 seeds | 3-4 days |

### Automation Script
```bash
# run_statistical_protocol.py
for seed in 42 123 456 789 1024; do
  python train_tinyvit.py --experiment V4 --seed $seed
done

# Evaluate all with 10 MC runs
python evaluate_mc.py --checkpoints V4_seed*.pt --runs 10

# Generate statistics report
python generate_stats_report.py --results V4_results.json
```

**Timeline: 1-2 weeks** (mostly compute time)

---

## Experiment 5: ResNet-18 Controlled Study (W6)

### 5A: Root Cause Confirmation

**Hypothesis:** BN statistics corruption during `convert_resnet_to_analog()`

**Test:**
```python
# Before conversion
bn_mean_before = model.bn1.running_mean.clone()

# Convert
model = convert_resnet_to_analog(model)

# After conversion
bn_mean_after = model.bn1.running_mean

print(f"BN drift: {(bn_mean_after - bn_mean_before).abs().mean()}")
```

**Timeline: 1 day**

---

### 5B: Noise Intensity Sweep

**Question:** Does ResNet-18 fail at all noise levels or only high noise?

**Design:**
| σ_d2d | σ_c2c | Tiny-ViT | ResNet-18 | Interpretation |
|:--|:--|:--|:--|:--|
| 0.00 | 0.00 | 95% | 78% | Baseline |
| 0.05 | 0.05 | 87% | ??? | Low noise |
| 0.10 | 0.05 | 87% | ??? | Medium D2D |
| 0.10 | 0.10 | 82% | 1% | High noise |

**Timeline: 2-3 days**

---

### 5C: Architecture Comparison

**Question:** Why does Tiny-ViT work but ResNet-18 fail?

**Analysis:**
```python
# Compare weight distributions
compare_distributions(tinyvit, resnet18)

# Compare gradient flow
track_gradient_norms(tinyvit, resnet18)

# Compare BN statistics evolution
track_bn_stats(tinyvit, resnet18, epochs=50)
```

**Timeline: 2-3 days**

---

## Execution Priority Queue

### Week 1: Immediate (P0)
| Day | Experiment | Rationale |
|:--|:--|:--|
| 1-2 | Exp 1: Framework comparison | Establishes necessity |
| 3-4 | Exp 2A: Frequency ablation | Core mechanism |
| 5-7 | Exp 3A: Layer-wise NL | Core finding depth |

### Week 2: Core (P0)
| Day | Experiment | Rationale |
|:--|:--|:--|
| 1-2 | Exp 2B: Spatial correlation | Mechanism validation |
| 3-4 | Exp 2C: Literature baselines | Innovation verification |
| 5-7 | Exp 3C: NL mitigation | Completeness |

### Week 3: Rigor (P1)
| Day | Experiment | Rationale |
|:--|:--|:--|
| 1-7 | Exp 4: Statistical re-runs | Reviewer #4 W7 |

### Week 4: Consistency (P1)
| Day | Experiment | Rationale |
|:--|:--|:--|
| 1-4 | Exp 5: ResNet-18 study | Reviewer #4 W6 |
| 5-7 | Exp 2D: C2C robustness | Trade-off analysis |

---

## Resource Requirements

| Resource | Quantity | Notes |
|:--|:--|:--|
| GPU hours | ~500 | 4 weeks × ~125 hrs/week |
| Storage | ~50GB | Checkpoints, logs |
| Manual analysis | ~40 hrs | Result interpretation |

---

## Success Criteria

| Experiment | Success Metric |
|:--|:--|
| Framework comparison | Feature matrix with ≥3 clear advantages |
| Ensemble HAT ablations | Statistical significance (p<0.05) for per-epoch optimal |
| NL=2.0 mechanism | Layer-wise sensitivity map + mitigation >40% |
| Statistical standardization | n=5 for all key claims with error bars |
| ResNet-18 study | Root cause confirmed + controlled experiments |

---

## Output Deliverables

| Deliverable | Location | Format |
|:--|:--|:--|
| Framework comparison results | `report_md/_gpt/framework_comparison.json` | JSON |
| Ensemble HAT ablation data | `report_md/_gpt/ensemble_hat_ablation.json` | JSON |
| NL=2.0 mechanism analysis | `report_md/_gpt/nl_mechanism.json` | JSON + Figures |
| Statistical report | `report_md/_gpt/statistical_report.json` | JSON + Tables |
| ResNet-18 diagnosis | `report_md/_gpt/resnet18_analysis.json` | JSON + Explanation |

---

**END PROTOCOL**

Ready to execute. Start with Experiment 1 (Framework comparison) or prioritize differently?
