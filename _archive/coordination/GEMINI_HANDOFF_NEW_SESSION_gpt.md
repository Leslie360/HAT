# Gemini Handoff: The "Final Fixes" Directive

**Date**: 2026-04-08
**Context**: The previous chat session became too long and lagged severely. I am passing the baton to the next Gemini/Claude session to finish the exact tasks Claude assigned in his `2026-04-08` wake-up assessment.

---

## 1. What Needs to be Done IMMEDIATELY

Claude outlined 5 critical FIXES and 3 SYNC tasks. Here is exactly what you need to do.

### 🔴 FIX-3: S4 敏感性扫描（最紧急，涉及学术诚信）
I wrote the script `scripts/_gpt/proxy_sensitivity_sweep_gpt.py`, but it failed to run because of Python import paths (it couldn't find `inference_analysis_utils`).
**Your Task**: 
1. Fix the script by running it directly from the root using `sys.path` manipulation, or just move the script to the root directory: `mv scripts/_gpt/proxy_sensitivity_sweep_gpt.py .`
2. Run it: `python proxy_sensitivity_sweep_gpt.py`
3. It will generate a log at `logs/_gpt/proxy_sensitivity_sweep_20260408.log` and a JSON.
4. **CRITICAL**: You must manually update `paper/08_appendix.md` and `paper/latex_gpt/sections/08_appendix.tex` with the **true numbers** outputted by this script. Do not leave the old hallucinated numbers there.

### 🔴 FIX-1: 06_discussion.tex 删除重复行
`paper/latex_gpt/sections/06_discussion.tex` 结尾处（大约在第59行左右）有一行重复的碎片代码：
`gether, these steps would preserve the current framework's profile-substitution structure...`
**Your Task**: Delete this broken line using the `replace` tool.

### 🔴 FIX-2: §6.6 光电非均匀性声明
**Your Task**: In both `paper/06_discussion.md` and `paper/latex_gpt/sections/06_discussion.tex` (§6.6 Limitations), add the following bullet point right after Temperature Sensitivity:
> - **Optical Non-Uniformity**: Light-intensity non-uniformity across the array aperture and optical write crosstalk between adjacent synaptic elements are not modeled. For optoelectronic synaptic transistors where programming is optically driven, these effects may introduce spatially correlated weight errors distinct from the stochastic D2D variability considered here.

### 🟡 FIX-4: Flowers-102 措辞强化
**Your Task**: In `paper/05_results.md` and `05_results.tex`, locate the sentence discussing the "data-volume floor" in the Flowers-102 paragraph. Add this exact sentence right after it:
> This interpretation remains a hypothesis rather than a proven causal mechanism; controlled experiments with larger labeled Flowers subsets would be needed to confirm whether the recovery failure is purely data-driven.

### 🟡 FIX-5: enumerate 格式统一
**Your Task**: In `paper/latex_gpt/sections/05_results.tex`, locate the `\begin{enumerate}` block under the Physical Non-Idealities or HAT Recovery sections (around lines 111-118). Ensure all numbered items use `\item` correctly instead of mixing `1.` and `\item`.

---

## 2. SYNC Tasks (.md <-> .tex)

Claude noticed that some of our previous updates didn't sync perfectly between MD and TEX. 
**Your Task**: Use the `replace` tool to ensure the following sentences are present in BOTH the `.md` and `.tex` files:

1. **SYNC-1**: In `06_discussion.md` (§6.6), under "First-Order Energy Model", make sure it contains the sentence: *"Bounding this unmodeled interconnect overhead at 10%, 30%, or even 50% of the MAC cost proportionally reduces the absolute efficiency..."* (This is already in `.tex`, but missing in `.md`).
2. **SYNC-2**: In `05_results.md` (§5.9 Task 37 Ensemble HAT), make sure it contains the training cost discussion: *"While this multi-instance strategy successfully mitigates hardware overfitting, it introduces a measurable training-cost overhead..."* (Already in `.tex`, missing/different in `.md`).
3. **SYNC-3**: In `05_results.md` and `.tex` (§5.9 Task 35 NL Write), make sure the 27.72% result is accompanied by: *"This 27.72% represents a hard physical boundary for the current gradient-scaling approximation, not a stochastic outlier."*

---

## 3. How to Report Back

When you finish these tasks, append a block to `report_md/_gpt/AGENT_SYNC_gpt.md` using a Python script. Do not use `cat << EOF` in bash. 
In the sync log, you **MUST** provide evidence:
- The paths of the files you modified.
- The path of the generated log: `logs/_gpt/proxy_sensitivity_sweep_20260408.log`.

Good luck! Let's get this Nature Communications paper across the finish line!
