# Remote 107 Core Math / Code Repro Packet Template

**Purpose:** Every corrected 107 result must include this packet so local agents can audit and reproduce the analog KV-cache algorithm. This is mandatory after the reported noise-algorithm bug.

## 1. Run Identity

```text
run_id:
git_sha:
git_status_short:
git_diff_stat:
python:
torch:
transformers:
timm_or_other:
cuda:
gpu:
model_id_or_local_path:
tokenizer:
dataset_name:
dataset_split_train_for_hat:
dataset_split_eval_for_ppl:
context_length:
stride:
batch_size:
dtype:
seed:
```

## 2. Core Tensor Shape Contract

State the exact shape at each point:

```text
raw key shape:
raw value shape:
internal analog KV shape: [B, L, H, D] or other
conductance shape:
quantized conductance shape:
noise tensors shape:
returned key/value shape:
```

## 3. Conductance Mapping Formula

Fill with exact equation and code location.

```text
input tensor x:
normalization axis:
min/max or scale definition:
conductance_min:
conductance_max:
G = ...
file:function:line:
```

Include code snippet under 40 lines.

## 4. Quantization Formula

```text
n_states:
bit_width:
rounding rule:
clip rule:
q = ...
G_q = ...
file:function:line:
```

Questions to answer:

- Is quantization per sample, per token, per head, per layer, or global?
- Is zero represented exactly?
- Are K and V quantized identically?

## 5. D2D Noise Algorithm

```text
sigma_d2d:
distribution:
additive_or_multiplicative:
noise shape:
sampled when:
persisted across what: token / sequence / batch / eval run / seed / layer
seed policy:
formula:
file:function:line:
```

Required unit test:

- Same D2D instance gives identical noise across repeated reads.
- Different D2D instance seed changes noise.
- D2D tensor shape matches intended physical assumption.

## 6. C2C Noise Algorithm

```text
sigma_c2c:
distribution:
additive_or_multiplicative:
noise shape:
sampled when:
formula:
file:function:line:
```

Required unit test:

- Same D2D instance but two forward passes produce different C2C noise.
- C2C disabled gives deterministic repeated reads.

## 7. Retention Algorithm

```text
time variable:
retention parameter(s):
formula:
applied before or after C2C:
applied before or after quantization:
file:function:line:
```

Required unit test:

- Accuracy/PPL-free tensor metric changes monotonically with retention time for a fixed cache.
- Retention=0 exactly recovers no-retention path.

## 8. Dequantization / Return Path

```text
x_hat = ...
scale restoration:
clip restoration:
dtype cast:
file:function:line:
```

Required unit test:

- quantize->dequantize with zero noise has expected MSE for 8-bit and 6-bit.
- no-quantize/no-noise path has relative MSE < 1e-6.

## 9. Selective Layer Mask Semantics

```text
analog_layers argument examples:
layer numbering convention: 0-indexed or 1-indexed
all-layer set:
last1 set:
last2 set:
last4 set:
file:function:line:
```

Required unit test:

- `--analog_layers 23` patches exactly one layer for Pythia-410m.
- `--analog_layers all` patches exactly 24 layers.
- JSON output records the exact list actually patched.

## 10. Attention Patch / SDPA Contract

```text
transformers version:
attention class patched:
cache object class:
SDPA/eager path:
mask handling:
position id handling:
file:function:line:
```

Required unit test:

- Patched clean/no-analog path PPL is close to unpatched baseline.
- Attention mask shape matches SDPA requirement for batch, heads, query length, key length.

## 11. HAT Training Objective

```text
trainable parameters:
frozen parameters:
loss function:
optimizer:
lr:
steps:
train split:
eval split:
noise config during HAT:
noise config during final eval:
file:function:line:
```

Required anti-leak statement:

```text
HAT training/calibration uses split: ____
Final PPL uses split: ____
No final-eval token appears in HAT training/calibration: yes/no + explanation
```

## 12. Baseline Reconciliation Table

Every report must include:

| Value | Meaning | Model | Context | Scope | Bit/states | Noise | Retention | Patch state | Split |
|---:|---|---|---:|---|---|---|---|---|---|
| 15.68 | | | | | | | | | |
| 22.18 | | | | | | | | | |
| 23.86 | | | | | | | | | |
| 32.41 | | | | | | | | | |
| 107.27 or replacement | | | | | | | | | |

## 13. Minimal Corrected Rerun Manifest

```text
run_id, seed, context, steps, analog_layers, bit_width/n_states,
train_noise_d2d, train_noise_c2c, eval_noise_d2d, eval_noise_c2c,
retention, pre_hat_ppl, post_hat_ppl, eval_split, command
```

## 14. Attachments To Return

Return Markdown and small JSON only:

```text
ENV.md
BASELINE_RECONCILIATION.md
CORE_MATH_PACKET.md
corrected_p0_results.json
unit_test_summary.txt
```

Do not return large checkpoints or model files.
