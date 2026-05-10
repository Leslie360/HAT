# 0411 外审意见接受声明与任务广播

> Date: 2026-04-11
> Owner: Codex
> Source review pack: `report_md/审稿意见model_0411.md`
> This document does **not** change the `106/109` reviewer-closure count by itself.
> It records which new suggestions are accepted for **hardening / polish / scope-defense** and how they are delegated.

---

## 1. Codex 对 Kimi / Gemini 广播的正式接受结论

### Accepted from Kimi

The following Kimi-broadcast points are accepted and promoted to active closeout work:

1. **前置 simulation-only / behavioral-simulation 定位**
   - accepted
   - reason: this is now a reviewer-expectation management issue, not a weakness admission issue

2. **统一软化 NL=2.0 相关措辞**
   - accepted
   - target wording family:
     - `approximation-limit boundary`
     - `simulator-scoped boundary`
     - `under the present gradient-scaling approximation`

3. **Ensemble HAT 与普通 noise augmentation / domain randomization 区分**
   - accepted
   - reason: this is the most reviewer-visible novelty-defense gap in the current draft

4. **C2C invariance 表格加入机制解释**
   - accepted
   - preferred mechanism wording:
     - scale masking
     - same quantization bucket / below-LSB perturbation

5. **把差分对不对称敏感度阈值从 supplementary 明示到主文**
   - accepted
   - reason: this is an actionable engineering constraint and deserves main-text visibility

### Accepted from Gemini

The following Gemini strategic points are accepted:

1. **主线仍然是 simulation-first methodology paper**
   - accepted
   - Codex canonical stance remains `A+B`:
     - submit now as simulation-first methodology paper
     - keep the manuscript collaboration-ready rather than anti-measurement

2. **向合作方索要少量高价值实测参数具有极高收益**
   - accepted as strategy
   - not a pre-submission blocker

3. **不要为了等待真实数据而打乱已经锁定的实验与投稿链**
   - accepted

---

## 2. Codex 自己新增的建议

These are Codex-added recommendations after reading the full `0411` review pack:

1. **Ensemble HAT 应上升为第一贡献位**
   - the paper should read as:
     - new failure mode discovered
     - new mitigation strategy proposed
     - simulator/profile system is the enabling infrastructure
   - not:
     - simulator first
     - everything else as applications

2. **Profile interface 的贡献权重应适度下调**
   - keep it as a real contribution
   - do not let it become the lead novelty claim unless `profile_auto_fitter` is demonstrated more concretely

3. **`profile_auto_fitter_gpt.py` 必须二选一**
   - either:
     - add one minimal toy / synthetic demonstration in supplementary
   - or:
     - demote it from “core contribution” to “supporting utility”

4. **摘要、结论、cover letter、discussion 的语气必须完全一致**
   - current risk is not lack of work
   - current risk is cross-section inconsistency

5. **这轮更值得投入文字与结构修补，而不是新 GPU 实验**
   - unless a zero-cost text fix truly requires a tiny supplementary control

---

## 3. Immediate Codex Task Plan

### CX-0411-1 [HIGH]
**Global wording sync for simulation-only / approximation-boundary**

Scope:
- `paper/latex_gpt/sections/00_abstract.tex`
- `paper/latex_gpt/sections/01_introduction.tex`
- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/sections/06_discussion.tex`
- `paper/latex_gpt/sections/07_conclusion.tex`
- `paper/latex_gpt/cover_letter.tex`

Goal:
- remove any residual mismatch between limitations and headline claims

### CX-0411-2 [HIGH]
**Contribution-order rewrite**

Goal:
- make `Ensemble HAT + fresh-instance collapse` the lead contribution
- move simulator/profile interface to enabling infrastructure position

### CX-0411-3 [MED]
**C2C mechanism + asymmetry-threshold integration**

Goal:
- add scale-masking explanation where reviewers will actually see it
- surface the differential-pair asymmetry threshold in main text

### CX-0411-4 [MED]
**Profile-auto-fitter triage**

Decision:
- either add a minimal supporting demo
- or reduce the contribution weight in the manuscript

### CX-0411-5 [HIGH]
**Accept only source-grounded Kimi/Gemini fixes, then compile and sync**

Goal:
- patch
- compile
- update task boards
- keep the repo on a single truth state

---

## 4. Delegation Plan

### Kimi gets

- reviewer-defense wording
- novelty differentiation language
- rebuttal / cover-letter defense text
- profile-auto-fitter contribution triage memo

### Gemini gets

- main-text line edits
- contribution-order rewrite suggestions
- C2C explanation placement edits
- asymmetry-threshold surfacing edits
- global overclaim scrub

### Codex keeps

- final acceptance / rejection of suggestions
- source patching
- LaTeX compile
- board synchronization

---

## 5. What does NOT change

The following are unchanged by this acceptance round:

- no new GPU-heavy experiments are opened
- locked numbers remain locked
- current reviewer-coverage count stays `106/109` until manuscript/source changes actually land
- current venue strategy remains:
  - **submit now as simulation-first NC paper**
  - **do not wait for measured-device collaboration before submission**

---

## 6. Short canonical summary

The 0411 review pack does **not** tell us to rebuild the paper.
It tells us to:

1. make the paper more honest upfront
2. make Ensemble HAT the real protagonist
3. stop letting reviewers mistake simulator-boundary results for physical-law claims

That is now the active closeout strategy.
