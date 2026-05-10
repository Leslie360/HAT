## CX-W: Dual-Attention-Collapse Tightening Note

Status: draft only, do not land automatically.

### Context

- `MLP-only` NL=2.0 mitigation recovered source-domain accuracy to `87.79%`.
- `QKV-only` collapsed to `18.72%` best and `10.15%` final.
- `attn_proj-only` is following the same pattern in live training, with best `18.86%` at epoch 0 and sustained `~10-11%` thereafter.

### Proposed one-sentence main-text tightening for `sections/06_discussion.tex`

Under the present gradient-scaling surrogate, nonlinear-write mitigation remains confined to the MLP analog path: both attention-side linearizations, targeting either QKV generation or the output projection, collapse to near-chance accuracy under `NL=2.0`, so we treat the mitigation result as a supplementary mechanism study rather than as a new main-text recovery claim.

### Rationale

- This sentence is narrower than a generic "MLP is most sensitive" claim.
- It explicitly encodes the two confirmed negative controls on the attention side.
- It preserves Option B: supplementary placement, not promotion to a fifth core manuscript contribution.
