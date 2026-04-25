# REMOTE DISPATCH — 8×40GB Cross-Architecture + Cross-Dataset Validation
**Date:** 2026-04-24
**Issued by:** Claude (Architect)
**Target:** New 8×40GB GPU server (persistent)
**Trigger:** User has access to a new server; code at GitHub `remote-exploration` branch post commit `c727a43` (dual-bug fix merged from main commit `33bed9c`).
**Replaces:** REMOTE_DISPATCH_A100_POSTFIX_20260424.md (A100 retired)

---

## 0. One-line mission

**Validate the Ensemble HAT diagnostic-treatment narrative on ViT-Small and DeiT-Small at TinyImageNet scale, replacing the "CIFAR-only + Tiny-ViT-only" limitation that currently caps paper-1's venue ceiling.**

This is the single biggest breadth gap in paper-1. Closing it justifies Nature Electronics submission.

---

## 1. Why this direction (rationale for the remote agent)

Paper-1 current status:
- Canonical Ensemble HAT Tiny-ViT @ NL=1.0 fresh-instance: 86.37±1.54% ✅ (bug-immune, core evidence)
- OPECT zero-shot Ensemble HAT: 88.53±0.08% ✅
- Post-fix severe-NL NL=2.0 Standard/Proportional HAT fresh (remote A100): 83-85% ✅ (post-fix verified)
- All CIFAR-10 (with small Tiny-ViT-5M).

The reviewer objection we cannot currently counter: "how do we know your Ensemble HAT diagnostic/treatment generalizes beyond a small 5M-parameter CIFAR model?"

Your mission on the 8×40GB server is to kill that objection with:
- **2 architectures**: ViT-Small/16 (22M params) + DeiT-Small/16 (22M params, different distillation/init heritage)
- **1 larger dataset**: TinyImageNet (200 classes, 64×64 → resized to 224×224, 100K train + 10K val)
- **3 HAT types** per arch: Standard, Ensemble, Proportional
- **3 seeds** per config for CI
- Full 3×2×3 = 18 training runs → parallelizable 8-way on this server

Deliverable = one 3-arch × 3-HAT matrix table replicating the 10% / 86% / ~88% diagnostic+treatment signature on TinyImageNet at larger-model scale.

If this reproduces, Ensemble HAT is no longer a "Tiny-ViT-specific trick" — it is a general diagnostic+treatment for transformer analog CIM deployment.

---

## 2. Hardware budget

- 8×40GB GPUs, ~320GB total VRAM
- ViT-Small/16 at 224×224 batch=128 fits on one 40GB card comfortably (~12-15 GB usage with AMP)
- 8-way parallelism: 8 different training configs simultaneously, one per card
- Not A100 speed — budget ~15-20h per full training run (100 epochs, TinyImageNet)
- 18 configs / 8 GPUs = 2.25 rounds ≈ 2-3 days for training
- Fresh-eval batch: another ~12h

Total wall-clock: ~4-5 days.

---

## 3. Experiment matrix (18 configs)

| Arch | HAT Type | Seeds | Configs |
|:--|:--|:--|:--:|
| ViT-Small/16 | Standard | 123, 456, 789 | 3 |
| ViT-Small/16 | Ensemble | 123, 456, 789 | 3 |
| ViT-Small/16 | Proportional | 123, 456, 789 | 3 |
| DeiT-Small/16 | Standard | 123, 456, 789 | 3 |
| DeiT-Small/16 | Ensemble | 123, 456, 789 | 3 |
| DeiT-Small/16 | Proportional | 123, 456, 789 | 3 |
| **Total** | | | **18** |

All configs share:
- NL=1.0 canonical (not severe-NL — we want bug-immune + paper-quality primary evidence)
- σ_D2D = 10%, σ_C2C = 5% (canonical literature priors, matches paper-1)
- 4-bit hybrid quantization
- Batch=128 per GPU, AMP on
- Epochs=100, AdamW lr=5e-4, cosine schedule, warmup=5 epochs
- TinyImageNet 224×224 resize (not native 64×64 — matches pretrained ImageNet weights if used)

Start from ImageNet-1K pretrained weights (timm has these — `timm.create_model('vit_small_patch16_224', pretrained=True)` and `timm.create_model('deit_small_patch16_224', pretrained=True)`). This matches paper-1's Tiny-ViT fine-tuning protocol.

---

## 4. Code you need (all on GitHub `remote-exploration` branch)

You already have from previous handoff:
- `analog_layers.py` — MLP path analog CIM primitive (33bed9c fixed, LTP/LTD branch + second-order correction)
- `analog_layers_ensemble.py` — Ensemble HAT wrapper with per-epoch D2D resampling
- `train_tinyvit.py` — reference training script (uses timm + analog layers, has `build_model`, `train_one_epoch`, `evaluate` helpers)
- `train_tinyvit_ensemble.py` — Ensemble HAT variant
- `eval_fresh_instances.py` — fresh-instance eval (10 instances × 5 MC)
- `eval_fresh_instances_postfix.py` — post-fix-aware version with explicit NL flag handling (PUSHED WITH THIS DISPATCH)
- `inference_analysis_utils.py`, `amp_utils.py`, `tinyvit_hybrid_utils.py` — utility modules
- `test_dual_bug_fix.py`, `test_groupwise_nl_wrapper.py` — verification suite (must pass before any real training)

You need to write (no equivalent exists yet):
- `train_vit_tinyimagenet.py` — adapted from `train_tinyvit.py`, supports:
  - `--model {vit_small_patch16_224, deit_small_patch16_224}` via timm
  - `--dataset tiny_imagenet` with your own dataloader (see §6)
  - Preserves the hybrid-analog classify-and-convert path: MLP layers → analog CIM, attention softmax + norm → digital, QKV/O projections → analog
  - Exports checkpoint with `exp_cfg` metadata (arch, hat_type, seed, nl_ltp, nl_ltd, noise_mode, batch_size, epochs, amp_enabled)
- `eval_fresh_instances_vit.py` — adapted from `eval_fresh_instances_postfix.py`, architecture-aware

Use `train_tinyvit.py` as your template. The analog conversion logic in `convert_to_hybrid()` from `analog_layers.py` is architecture-agnostic — you classify layers by name pattern and convert the MLP/QKV ones.

---

## 5. Hybrid-analog mapping rule for ViT-Small / DeiT-Small

Match paper-1 Tiny-ViT's rule: MLP-path + QKV projections go analog, attention softmax + LayerNorm stay digital.

Concretely, for each `TransformerEncoderBlock`:
- `mlp.fc1` → analog
- `mlp.fc2` → analog  
- `attn.qkv` → analog (stacked Q, K, V projection)
- `attn.proj` → analog (output projection)
- `norm1`, `norm2` → digital (kept fp32 for numerical stability)
- softmax, scaling → digital

`patch_embed` (conv or linear): analog
Classification head `head` (final Linear): analog

This preserves paper-1's "analog where MAC-heavy, digital where numerically sensitive" discipline.

---

## 6. TinyImageNet dataloader

Standard TinyImageNet layout:
```
tiny-imagenet-200/
├── train/
│   ├── n01443537/images/*.JPEG
│   └── .../
├── val/
│   ├── images/*.JPEG
│   └── val_annotations.txt
└── wnids.txt (200 classes)
```

Download: `wget http://cs231n.stanford.edu/tiny-imagenet-200.zip` (standard source, no auth needed).

Transform:
- Resize 64×64 → 224×224 (to match pretrained ViT-S weights; bicubic)
- Normalize with ImageNet stats (mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
- Training augmentation: RandomHorizontalFlip, RandomResizedCrop (224, scale=0.7-1.0), TrivialAugmentWide

Validate dataloader before launching training by checking 1 batch has `shape=(128, 3, 224, 224)` and `num_classes=200`.

---

## 7. Verification gates (MUST PASS before any real training)

Before running the 18-config matrix:

### Gate A — Code provenance
```bash
git rev-parse HEAD                      # expect commit at or after c727a43 
                                        # (contains 33bed9c dual-bug fix)
python test_dual_bug_fix.py             # must pass 5/5
python test_groupwise_nl_wrapper.py     # must pass 8/8
```

### Gate B — Hybrid conversion sanity on ViT-Small
Write a 10-line smoke test: load ViT-Small pretrained, call `convert_to_hybrid`, confirm MLP/QKV/proj linears are replaced by `AnalogLinear` and LayerNorm/softmax path is untouched. Forward one random batch, confirm no NaN.

### Gate C — Single-config smoke run (1 epoch, 1 seed, 1 config)
Run 1 epoch of ViT-Small + Standard HAT + seed 123 on TinyImageNet. If training accuracy moves upward and loss decreases, proceed. If stuck at chance (1/200 = 0.5%), debug before launching full matrix.

### Gate D — Fresh-eval smoke on an existing checkpoint
Run `eval_fresh_instances_postfix.py` on one paper-1 Tiny-ViT checkpoint (you have these from A100 handoff) to confirm the fresh-eval pipeline reproduces paper-1 86.37±1.54%. If it doesn't, the eval pipeline on this server is broken and any new numbers are untrustworthy.

Only after Gates A-D all pass, launch the 18-config matrix.

---

## 8. Launch protocol

Parallelize 8-way:
```bash
# Round 1: 8 configs
CUDA_VISIBLE_DEVICES=0 python train_vit_tinyimagenet.py --model vit_small_patch16_224 --hat standard --seed 123 ... &
CUDA_VISIBLE_DEVICES=1 python train_vit_tinyimagenet.py --model vit_small_patch16_224 --hat ensemble --seed 123 ... &
...
CUDA_VISIBLE_DEVICES=7 python train_vit_tinyimagenet.py --model deit_small_patch16_224 --hat proportional --seed 123 ... &
wait
# Round 2: next 8 configs (seeds 456 mostly)
# Round 3: last 2 configs
```

Save checkpoints to:
`checkpoints/_gpt/cross_arch_tinyimagenet/{arch}_{hat}_seed{S}/best.pt`

Save training logs:
`logs/_gpt/cross_arch_{arch}_{hat}_seed{S}_<ts>.log`

---

## 9. Fresh-instance evaluation

After all 18 trainings land:
```bash
# Parallelize 8-way across checkpoints
for ckpt in checkpoints/_gpt/cross_arch_tinyimagenet/*/best.pt; do
    python eval_fresh_instances_vit.py \
        --checkpoint $ckpt \
        --num-instances 10 \
        --mc-runs 5 \
        --nl-ltp 1.0 --nl-ltd -1.0 \
        --sigma-d2d 0.10 --sigma-c2c 0.05 \
        --output-json report_md/_gpt/json_gpt/cross_arch_$(basename $(dirname $ckpt))_fresh.json
done
```

Each fresh eval takes ~30-45 min. 18 evals / 8 cards ≈ 1.5-2 hours.

---

## 10. What you return

**ONE consolidated file** + JSONs. No checkpoint transfer back (~~100GB too heavy).

### 10.1 Per-config JSON
`cross_arch_<arch>_<hat>_seed<S>_fresh.json`:
```json
{
    "arch": "vit_small_patch16_224",
    "hat_type": "ensemble",
    "seed": 123,
    "train_best_acc": 0.XXXX,
    "train_best_epoch": XX,
    "fresh_per_instance_mean": [0.XXXX × 10],
    "fresh_aggregate": {"mean": 0.XXXX, "std": 0.XXXX, "median": 0.XXXX, "range": [low, high]},
    "commit_hash": "c727a43...",
    "exp_cfg": {full training config},
    "cuda_device_name": "...",
    "pytorch_version": "..."
}
```

### 10.2 Master summary report
`CROSS_ARCH_TINYIMAGENET_REPORT_<YYYYMMDD>.md` with:
- 18-row table (arch, hat, seed, train_best, fresh_mean, fresh_std)
- Aggregate per (arch, hat) group: mean ± std across seeds
- Diagnostic-treatment gap: Δ(Ensemble - Standard) per architecture, Δ(Proportional - Standard) per architecture
- Comparison to paper-1 Tiny-ViT canonical (Ensemble 86.37±1.54, Standard 10.00±0.00) — does the same pattern hold at ViT-Small scale?

### 10.3 Anomalies
If any config fails to train (stuck at chance, NaN, etc.), flag in a separate section with the log snippet. Do not silently drop configs.

---

## 11. Decision rule on landing

- **If Ensemble ≥ Standard + 50pp on both arches, on TinyImageNet**: diagnostic-treatment generalizes. This becomes a major paper-1 supplementary finding (possibly main-text if Kimi can fit it). **Flag to Claude for narrative integration.**
- **If Ensemble ≥ Standard + 20-50pp**: generalizes partially. Still a paper-grade result, framed as "Ensemble HAT effect attenuates at larger model/dataset scale but remains positive". Useful signal.
- **If Ensemble ≈ Standard (within 5pp)**: surprising result worth investigating — possibly TinyImageNet's larger class count / pretrained init dilutes the hardware-instance overfitting. Do NOT discard. Write up as a scope-limitation finding. This is still scientifically interesting.
- **If Ensemble < Standard**: flag immediately to Claude. Suggests an implementation issue or a different regime — do not silently publish.

All four outcomes are useful. Honest reporting > cherry-picked positive.

---

## 12. Optional stretch goal (ONLY if time remains)

After the 18-config matrix lands and you have ≥3 spare GPU-days, optionally add:
- **One arch + Ensemble HAT at TinyImageNet + NL=2.0 severe**: 3 seeds. Tests whether post-fix severe-NL recovery also generalizes cross-arch/cross-data.
- **ViT-Small + Ensemble HAT @ measured-D2D distribution**: ONLY if PhD team's real D2D data has landed and is ingested via `data/measured_d2d_distribution.npy` (see DATA_INGEST_PROTOCOL §3). Uses the `--d2d-distribution measured` flag.

Do NOT start the stretch goal before the primary 18-config matrix is complete. Priority discipline.

---

## 13. What you DO NOT do

- No paper text edits
- No narrative inference (you return data, Claude integrates)
- No exploratory hyperparameter sweeps beyond the matrix
- No new architectures (only ViT-Small + DeiT-Small for now)
- No new datasets (only TinyImageNet for now)
- No runs that skip verification gates A-D

---

## 14. Status reporting cadence

- After Gate D passes: one-line confirmation to `report_md/_gpt/AGENT_SYNC_gpt.md` with a timestamp and the 4-gate results.
- After Round 1 training (8 configs) lands: one status block listing per-config best_acc.
- After all 18 trainings land: one status block with full training matrix.
- After all fresh-evals land: the final report.

---

## 15. Cross-reference to NARRATIVE_PIVOT

This dispatch plugs into `NARRATIVE_PIVOT_20260424.md` §6 Landmark L2 ("Deep-work accumulation phase") and implements the "Cross-architecture (ViT-Small / DeiT-Small on TinyImageNet)" work item listed there. Results land directly as a Supplementary Section "Cross-architecture validation" in paper-1.

If results are strong (outcome 1 above), Kimi may promote to main text — subject to Claude's integration judgment.

---

## 16. Success criterion for this dispatch

A publishable-quality 18-row experiment matrix with fresh-instance evaluation, delivered as JSON + one master report, within ~5-7 days wall-clock, on the 8×40GB server, reproducing (or honestly refuting) paper-1's canonical Ensemble HAT diagnostic-treatment signature at transformer+dataset scale.

**Verification-gated.** No numbers reported until gates A-D pass.
