# DISPATCH: Codex — R11D-HAT-PCM Code Review

**Date:** 2026-04-27
**From:** Claude (Chief Architect)
**To:** Codex (GPU/代码 Agent)
**Priority:** HIGH
**Deadline:** Before R11D-5a/5b complete (~2h)
**Status:** DISPATCHED

---

## 1. Mission

Review `paper2_aihwkit_baseline/r11d_hat_pcm.py` for logic correctness,
aihwkit API misuse, and edge cases. This is a NEW script (written by Claude)
that implements per-epoch D2D mismatch resampling on aihwkit `AnalogLinear`
tile weights while keeping `AnalogSGD` + `PCMPresetUnitCell` for real PCM
pulse-update physics.

---

## 2. Files to Review

| File | Purpose |
|------|---------|
| `paper2_aihwkit_baseline/r11d_hat_pcm.py` | **Main target** — NEW hybrid script |
| `paper2_aihwkit_baseline/r11d4_train_pcm.py` | Baseline PCM script (for diff) |
| `paper2_aihwkit_baseline/run_r11d_hat_pcm.sh` | Launch script |

---

## 3. Specific Questions (answer each)

### Q1 — `set_weights()` correctness
`resample_all_d2d_noise()` calls `module.set_weights(w_new, b)` on every
`AnalogLinear` layer, every epoch. Does this correctly propagate through
`analog_module.set_weights()` for `InferenceTile`? Any edge case with `bias=None`?

### Q2 — `AnalogSGD` + `post_update_step()` interaction
`AnalogSGD.step()` calls `tile.post_update_step()` which applies PCM pulse-update.
We call `set_weights()` at the START of each epoch (before `train_epoch()`).
Is there any risk that `post_update_step()` from the previous epoch's last batch
could conflict with our `set_weights()`? Should we call `model.eval()` before
`set_weights()`?

### Q3 — `state_dict()` / checkpoint safety
`torch.save({"model_state_dict": model.state_dict()})` is used.
`AnalogLinear.state_dict()` returns `analog_module.shared_weights`.
Claude verified that `set_weights()` updates `shared_weights` (test script
in `/tmp/test_analog_state_dict3.py`). But is this always true after
`AnalogSGD.step()` + `post_update_step()`? Should we snapshot `get_weights()`
into checkpoint explicitly?

### Q4 — OOM fallback path
The script inherits OOM fallback from `r11d4_train_pcm.py`:
```python
try:
    model = build_model(...)
except RuntimeError as e:
    if "out of memory" in str(e).lower():
        args.batch_size = 32
        model = build_model(...)
```
Does `build_model()` get called twice correctly? Does `noise_buffers`
initialization (which happens AFTER `build_model()`) handle the fallback path?

### Q5 — Scaled vs additive mode
Run a **10-epoch quick test** with `--hat-mode additive` (same settings as
smoke test: bs=32, lr=5e-4, epochs=10). Compare to `scaled` mode results.
Which mode converges better? Document in report.

---

## 4. Deliverables

1. **Code review report** — answer Q1-Q5 above
2. **Quick test result** — `additive` mode 10-epoch run (if GPU available)
3. **BROADCAST file** — `BROADCAST_CODEX_R11D_HAT_PCM_REVIEW_20260427.md`
   with `Status: COMPLETE` and summary

---

## 5. Context

- Smoke test passed: `scaled` mode, 3 epochs, 29.27%
- R11D-5a running (ep43, 67.43%, lr=1e-3)
- R11D-5b running (ep1, lr=5e-3)
- GPU shared but ~10GB free; if OOM, use bs=32 or queue after 5a/5b

**End of dispatch.**
