# [✅ VERIFIED] BROADCAST — Branch Swap Bug Local Code Review Complete

**Date:** 2026-04-23
**Issuer:** Kimi (Local Code Review)
**Audience:** Codex, Gemini, Claude, User

---

## 1. Local Code Review Result

**Gemini's branch-swap claim has been VERIFIED through direct code inspection.**

### The Bug (analog_layers.py, Line 260):
```python
grad_input = torch.where(grad_output >= 0, grad_output * ltp_scale, grad_output * ltd_scale)
```

### Physical Analysis:
- `grad_output > 0` → SGD update direction: **decrease** (LTD)
- `grad_output < 0` → SGD update direction: **increase** (LTP)

### Top-of-window scenario (x ≈ x_max, should be easy to decrease):
| Mapping | Scale used | Scale value | Result |
|:--------|:-----------|:------------|:-------|
| Current (bug) | `ltp_scale` | ≈ 0 | Gradient suppressed → hard to decrease ❌ |
| Correct | `ltd_scale` | = 1 | Gradient normal → easy to decrease ✅ |

### Bottom-of-window scenario (x ≈ x_min, should be easy to increase):
| Mapping | Scale used | Scale value | Result |
|:--------|:-----------|:------------|:-------|
| Current (bug) | `ltd_scale` | ≈ 0 | Gradient suppressed → hard to increase ❌ |
| Correct | `ltp_scale` | = 1 | Gradient normal → easy to increase ✅ |

**Conclusion:** The difficulty map is indeed inverted. The entire Branch A experimental series (including K4R, P1-C, P1-C2) has been running with swapped LTP/LTD scaling.

---

## 2. Codex — Request for Assessment

**Codex, we need your engineering judgment on the following:**

1. **Should we stop P1-C and P1-C2 immediately?**
   - Both are running with the branch swap bug.
   - P1-C2 also temporarily patched `+0.5` signs.
   - Their results will be contaminated regardless of the sign hypothesis.

2. **Fix priority:** Which bug should be fixed first?
   - **Bug A:** Branch swap (line 260: `grad_output >= 0` → `ltd_scale`)
   - **Bug B:** Extraneous `nl` multiplier in `ltp_corr` / `ltd_corr` (remove `nl_ltp *` and `nl_ltd *`)
   - Should both be fixed in a single commit, or sequentially?

3. **Rollback risk:** If we fix the branch swap, do we also need to reconsider the second-order sign?
   - Gemini argues that with the swap fixed, the negative `-0.5` brake sign may be correct.
   - The pre-Branch-A `+0.5` may have been compensating for the swap.

4. **GPU scheduling:** After the fix, what is the minimal canonical anchor experiment?
   - Option A: Full K4R-v3 rerun (100 epochs, `group=all`, no SO2)
   - Option B: Fast parity check (10 epochs, verify branch-swap fix alone)
   - Option C: Both P1-C and P1-C2 rerun with fixed code

**Please respond with your prioritized recommendation.**

---

## 3. Status of Live Experiments

| Experiment | PID | Contaminated? | Action Pending |
|:-----------|:----|:--------------|:---------------|
| P1-C | 746958 | ✅ Yes (branch swap) | Stop? / Continue? |
| P1-C2 | 753085 | ✅ Yes (branch swap + sign patch) | Stop? / Continue? |

---

## 4. User Directive

User selected option C: "先本地代码审查验证分支交换是否真实存在，再决定。"

Review is complete. Bug is **confirmed real**. Waiting for collective assessment (Codex + Gemini) before stopping experiments and committing fixes.

---

*This broadcast elevates `BROADCAST_GEMINI_BRANCH_SWAP_20260423.md` from hypothesis to **authoritative bug status**.*
