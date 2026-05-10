# Source Code Audit Report — Kimi
**Date:** 2026-04-22
**Scope:** Core training/eval pipeline and continuation drivers
**Trigger:** Prevent recurrence of Codex-discovered bugs (0-byte file corruption, delta_g_eff auto-fill mis-semantics, hardcoded CIFAR-10)

---

## 1. Files Audited

| File | Lines | Purpose |
|:-----|------:|:--------|
| `train_tinyvit_ensemble.py` | 1647 | Core Tiny-ViT training loop, CLI, checkpoint I/O |
| `analog_layers.py` | ~1493 | AnalogLinear, AnalogConv2d, STE, convert_to_hybrid |
| `analog_layers_ensemble.py` | ~1260 | **Deprecated** old snapshot of analog_layers |
| `scripts/_gpt/run_tinyvit_groupwise_nl_comp.py` | 162 | Groupwise NL wrapper |
| `scripts/_gpt/eval_joint_fresh_instance.py` | 196 | Fresh-instance evaluator |
| `scripts/_gpt/run_cx_k4_alpha_continuation.py` | 189 | K4 continuation driver |
| `run_ensemble_hat_fixed.py` | 157 | **Deprecated** eval script using old analog_layers |

---

## 2. Bugs Found & Fixed

### 2.1 `%%` in CLI help string (train_tinyvit_ensemble.py:1473)
**Severity:** Low (cosmetic)
**Before:** `help="Enable torch.compile(model) for ~15-30%% training speedup ..."`
**After:** `help="Enable torch.compile(model) for ~15-30% training speedup ..."`
**Fix applied:** ✅

### 2.2 `analog_layers_ensemble.py` lacks second-order STE support
**Severity:** High (silent behavioral divergence)
**Issue:** `analog_layers_ensemble.py` is an old snapshot. Its `StraightThroughQuantize.forward/backward` signatures have **only 6 parameters** (no `use_second_order_ste`, `delta_g_eff`, `second_order_alpha`). `run_ensemble_hat_fixed.py` imports from it. Any accidental execution would produce first-order-only results while logs claim SO2 is active.
**Fix applied:** Added prominent `DEPRECATED` header comments to both files. ✅

### 2.3 `AnalogLinearConfig` silently ignores `use_second_order_ste=True` when `delta_g_eff <= 0`
**Severity:** Medium (silent failure)
**Issue:** `StraightThroughQuantize.backward` gates the second-order term on `ctx.delta_g_eff > 0.0`. If a user sets `use_second_order_ste=True` but forgets to set a positive `delta_g_eff`, the correction is silently skipped. No warning is emitted.
**Fix applied:** Added `RuntimeWarning` in `AnalogLinearConfig.__post_init__` when `use_second_order_ste=True and delta_g_eff <= 0.0`. ✅

---

## 3. Codex Bugs Re-verified

| Bug | Codex Fix Status | Kimi Verification |
|:----|:----------------:|:------------------|
| `delta_g_eff <= 0` treated as auto-fill | Fixed to `delta_g_eff < 0` | ✅ Confirmed correct. `0.0` is now literal zero; `-1.0` triggers auto-fill. |
| SO2-off path did not clear higher-order state | Fixed: explicit reset of `use_second_order_ste`, `delta_g_eff`, `second_order_alpha` | ✅ Confirmed correct in `make_groupwise_setter`. |
| `eval_joint_fresh_instance.py` hardcoded CIFAR-10 | Fixed: derives `dataset`/`num_classes` from checkpoint | ✅ Confirmed correct. CLI override flags still available. |
| `train_tinyvit_ensemble.py` corrupted to 0 bytes | Restored from `git show HEAD` | ✅ File is now 1647 lines, syntax valid. **Root cause of corruption remains unknown** — see §5.1. |

---

## 4. Architecture Risks (No Immediate Fix Required)

### 4.1 `analog_layers.py` vs `analog_layers_ensemble.py` code drift
The two files have diverged. `analog_layers_ensemble.py` is missing:
- `use_second_order_ste`, `delta_g_eff`, `second_order_alpha` fields
- `second_order_alpha` scaling in `StraightThroughQuantize.backward`
- `retention_state_dependent` support in `_retention_decay_factor`
- `AnalogLinearConfig.__post_init__` validation improvements

**Recommendation:** Delete `analog_layers_ensemble.py` and `run_ensemble_hat_fixed.py` after Round Q loop closure (not before, to preserve provenance).

### 4.2 Non-atomic file writes across the codebase
At least 15 Python files use `open(path, "w")` to overwrite JSON/CSV/MD/log outputs. If the Python process is killed mid-write (OOM, SIGKILL, power loss), the file can be truncated to 0 bytes or left in a partially-written corrupt state. This is the **most likely root cause** of the `train_tinyvit_ensemble.py` 0-byte incident (if an agent or script attempted to overwrite it).

**Mitigation:**
- For critical source files: **never** write to `.py` files programmatically without atomic rename (`write to .tmp`, then `os.replace`).
- For JSON/CSV artifacts: acceptable risk for experiment outputs; not acceptable for source code.

### 4.3 `make_groupwise_setter` monkey-patches global functions
```python
base.set_noise_for_train = make_groupwise_setter(...)
base.set_noise_for_eval = make_groupwise_setter(...)
```
This modifies module-level globals. If two different wrappers are imported in the same process, the second import overwrites the first. Currently safe because each run is a separate subprocess.

### 4.4 `RunLogger` file handle leak
`RunLogger.__init__` opens a file handle but lacks `__del__` or context-manager protocol. If `RunLogger` is instantiated outside `main()` and not explicitly closed, the handle leaks. Currently safe because `main()` has `try/finally: logger.close()`.

---

## 5. Outstanding Mysteries

### 5.1 Root cause of `train_tinyvit_ensemble.py` → 0 bytes
No script in `scripts/_gpt/` writes to `.py` source files. Possible causes:
- IDE auto-save conflict (VS Code remote + local sync)
- Agent tool call that targeted the wrong file path
- Filesystem race condition during git operation

**Preventive measure:** Add a pre-flight checksum verification before any future agent attempts to modify `train_tinyvit_ensemble.py`.

---

## 6. Syntax Verification Post-Fix

All audited files pass `ast.parse()`:
```
train_tinyvit_ensemble.py                OK
analog_layers.py                         OK
analog_layers_ensemble.py                OK
run_ensemble_hat_fixed.py                OK
scripts/_gpt/run_tinyvit_groupwise_nl_comp.py     OK
scripts/_gpt/eval_joint_fresh_instance.py         OK
scripts/_gpt/run_cx_k4_alpha_continuation.py      OK
```

---

## 7. Sign-off

- **K3 continuation driver:** Reviewed. No additional bugs found beyond Codex fixes.
- **K4 continuation driver:** Reviewed. Eval command correctly passes `--second-order-alpha`.
- **J1d parity fix watcher:** Reviewed. Command uses `--delta-g-eff -1.0` (auto-fill semantics).
- **Source integrity:** All critical files syntax-valid; deprecated files clearly marked.

---

**⚠️ DEPRECATED 2026-04-24** — This memo references bug-contaminated data (STE branch swap + extraneous nl multiplier in analog_layers.py, fixed at commit 33bed9c). The "structural ceiling / bimodal basin / Hartigan p=0.98" narrative is invalidated. Do not cite as evidence. See BROADCAST_HALT_AND_REPLICATE_20260424.md and BROADCAST_REBUILD_3WEEK_20260424.md for current status.
