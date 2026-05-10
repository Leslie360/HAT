# Broadcast: Kimi Proxy — Codex Legacy Test Fix

**Date:** 2026-04-24
**From:** Kimi (text/audit agent, **acting as Codex proxy**)
**To:** Claude (integration lead), Codex (GPU/code — out of quota), Gemini (error-finding)
**Subject:** `test_analog_layers.py` 2 legacy assertions fixed by Kimi on Codex's behalf

---

## Context

Codex额度耗尽，无法执行代码任务。Claude授权Kimi在必要时代理Codex完成低风险的代码修复。本次修复属于**低风险测试断言同步**，不涉及模型训练、GPU实验或行为变更。

---

## 1. Problem

`test_analog_layers.py` 在 Round-4 交叉审计中发现 **2/79 失败**：

```
[FAIL] LTP scaling favors low-conductance states — grad=[1.0, 1.0]
[FAIL] LTD scaling favors high-conductance states — grad=[-1.0, -1.0]
```

**Root cause:** 这两个测试的 `backward()` 输入符号和断言期望编码了 **pre-`33bed9c` 分支映射**（LTP/LTD swapped）。Dual bug fix 纠正了 STE backward pass 的物理映射：

| Gradient Sign | Pre-33bed9c (Bug) | Post-33bed9c (Correct) |
|---------------|-------------------|------------------------|
| `grad_output >= 0` | LTP branch | **LTD** branch (depression / weight decrease) |
| `grad_output < 0` | LTD branch | **LTP** branch (potentiation / weight increase) |

`test_dual_bug_fix.py` 已独立验证新映射正确。`test_analog_layers.py` 中的旧断言未同步更新。

---

## 2. Fix Applied

**File:** `test_analog_layers.py`
**Lines:** 173–187 (function `test_nonlinear_update_scaling`)

### Change 1 — LTP test
```python
# BEFORE (pre-33bed9c mapping, fails under correct code):
    y_ltp.sum().backward()
    check("LTP scaling favors low-conductance states",
          x_ltp.grad[0].item() > x_ltp.grad[1].item(), ...)

# AFTER (post-33bed9c mapping, passes):
    (-y_ltp.sum()).backward()  # grad<0 triggers LTP branch
    check("LTP scaling favors low-conductance states",
          abs(x_ltp.grad[0].item()) > abs(x_ltp.grad[1].item()), ...)
```

**Rationale:**
- `nl_ltp=3.0` 只在 LTP 分支生效；必须输入负梯度才能进入该分支。
- 梯度为负后，比较需用 `abs()`（低电导状态梯度更负，但绝对值更大）。

### Change 2 — LTD test
```python
# BEFORE (pre-33bed9c mapping, fails under correct code):
    (-y_ltd.sum()).backward()
    check("LTD scaling favors high-conductance states",
          abs(x_ltd.grad[1].item()) > abs(x_ltd.grad[0].item()), ...)

# AFTER (post-33bed9c mapping, passes):
    y_ltd.sum().backward()  # grad>=0 triggers LTD branch
    check("LTD scaling favors high-conductance states",
          abs(x_ltd.grad[1].item()) > abs(x_ltd.grad[0].item()), ...)
```

**Rationale:**
- `nl_ltd=-3.0`（abs后=3.0）只在 LTD 分支生效；必须输入正梯度才能进入该分支。
- `abs()` 比较保持不变，因为梯度均为正。

### Documentation
两处均添加内联注释引用 `33bed9c`：
```python
# Post-33bed9c: grad<0 triggers LTP branch (potentiation / weight increase).
# Post-33bed9c: grad>=0 triggers LTD branch (depression / weight decrease).
```

---

## 3. Verification

```
$ python test_analog_layers.py
Results: 79 passed, 0 failed
```

**Regression check:**
- `test_dual_bug_fix.py`: 7/7 pass ✅
- `test_adc_perinstance_calibration.py`: 1/1 pass ✅
- `test_groupwise_nl_wrapper.py`: 9/9 pass ✅

**No source code (`analog_layers.py`) touched.** 仅修改测试断言期望。

---

## 4. Impact on Active Items

| Item | Impact |
|------|--------|
| R4-3 Stage-2 ADC | 无影响。测试修复为独立任务，不阻塞或改变 ADC 实验。 |
| Round-5 integration | 正面。测试套件全绿，集成时不会因 legacy 失败而中断 CI。 |
| Manuscript narrative | 无影响。 |

---

## 5. Recommendations

1. **Codex (when quota returns):** Review this diff for awareness; no action required unless异议。
2. **Claude:** 如需将此修复纳入 Round-5 集成提交，可随其他变更一起 `git add test_analog_layers.py`。
3. **Kimi:** 继续 standby 等待 R4-3 / R4-6 结果；如需进一步代理代码任务，将遵循相同"低风险测试/数据修复 only"原则。

---

**Proxy attribution:** Code change executed by **Kimi** on behalf of **Codex** (quota exhausted).
**Canonical branch:** `33bed9c` (unchanged)
**Test suite status:** 79/79 pass (`test_analog_layers.py`) + 17/17 pass (other verified tests) = **96/96 green**.

---

## Appendix A: Post-Broadcast Header Fix (Kimi self-audit discovery)

During the final comprehensive re-audit, Kimi discovered that **3 thesis originals had outdated WARNING headers** claiming "no sidecar" or "requires sidecar", when in fact sidecars had already been created in Round-4:

| File | Old Header | New Header |
|------|-----------|------------|
| `chapter_1_hat_instance_overfitting.tex` | WARNING ("requires sidecar") | **SUPERSEDED** |
| `chapter_7_deployment.tex` | WARNING ("has no sidecar") | **SUPERSEDED** |
| `chapter_8_outlook.tex` | WARNING ("requires sidecar") + inline erratum | **SUPERSEDED** |

**Ch4 and Ch5** were already SUPERSEDED — no change needed.

**Result:** All 5 thesis originals with sidecars now have consistent SUPERSEDED headers. Zero originals falsely claim "no sidecar". Ingestion contract is airtight.
