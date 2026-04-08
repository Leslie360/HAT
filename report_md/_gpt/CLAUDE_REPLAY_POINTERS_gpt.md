# Claude Replay Pointers (GPT)

更新日期：`2026-04-07 16:55`

这份文件是给 Claude 回来后的一屏复盘入口。当前项目已经不再处于“训练排队中”，而是处于：

- 结果基本锁定
- reviewer-style 风险收敛
- 论文收稿与 rebuttal 防御准备

## 1. 先看什么

建议按这个顺序读，不要先翻旧聊天或旧日志：

1. `/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md`
2. `/home/qiaosir/projects/compute_vit/report_md/_gpt/EXTERNAL_REVIEW_SYNTHESIS_gpt.md`
3. `/home/qiaosir/projects/compute_vit/paper/CANONICAL_RESULT_LOCK_gpt.md`
4. `/home/qiaosir/projects/compute_vit/report_md/_gpt/GEMINI_HANDOFF_gpt.md`
5. `/home/qiaosir/projects/compute_vit/paper/05_results.md`
6. `/home/qiaosir/projects/compute_vit/paper/06_discussion.md`
7. `/home/qiaosir/projects/compute_vit/paper/07_conclusion.md`

## 2. 当前最关键的新事实

### Task 37 已从“训练成功”升级为“有 fresh-instance 证据的成功”

- 训练成功日志：
  - `/home/qiaosir/projects/compute_vit/logs/_gpt/train_tinyvit_v4_ensemble_FINAL_SAFE.log`
- fresh-instance 评估脚本：
  - `/home/qiaosir/projects/compute_vit/eval_fresh_instances.py`
- 结果文件：
  - `/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/fresh_instance_eval.json`

锁定数值：
- 标准 `V4` on fresh instances = `10.00 ± 0.00%`
- `Task 37 Ensemble HAT` on fresh instances = `86.37 ± 1.54%`

安全表述：
- 这证明 **multi-instance-aware training can mitigate hardware-instance overfitting in this setting**
- 不要写成“已经解决普适 hardware transferability”

### Gemini 15:15 更新中，真正已核实的部分

已核实：
- `analog_layers.py` 增加了 state-dependent retention 分支
- `plot_paper_figures.py` 的 Fig.11 已改成 horizontal stacked bar
- `visualize_attention.py` 增加了 attention entropy
- `paper/05_results.md` 增加了 `§5.11 Case Study: Evaluating New Materials`
- synthetic measured-like profile 已存在：
  - `/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/measured_sample_profile.json`

仍需保守表述：
- `§5.11` 目前是 **synthetic interface demonstration**
- 还不是“真实 measured-device validation 闭环”

## 3. 当前 reviewer 风险已经收敛到哪里

不是“结果不够多”，而是“说得太满”和“复现信息不够集中”。

### 现在已被 reviewer-style feedback 反复击中的点

完整汇总已在：
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/EXTERNAL_REVIEW_SYNTHESIS_gpt.md`

来源已吸收：
- Hunyuan
- DeepSeek
- Kimi
- Doubao
- Qwen
- Perplexity-style review
- NVIDIA-style review

共同主线：
- 这篇稿子更接近 `first-order behavioral / parameter-sensitivity framework`
- 不是已验证的 predictive hardware emulator

### 当前最值钱的补强项

1. literature-derived fitted-profile case study
2. centralized parameter provenance table / appendix
3. explicit limitations subsection
4. submission-facing reproducibility block

## 4. 当前锁定语义

这些在中英文稿里都不要再改口：

- Tiny-ViT corrected retention:
  - `rapid early drop followed by a broad plateau near 79%`
- `Flowers-102`：
  - `low-data boundary`
  - 不是“方法彻底失败”
- `Task 34`：
  - `distribution-matched recovery`
- `Task 35`：
  - `major remaining failure mode`
- `Task 36`：
  - `architecture-gap evidence under richer physics`
  - 不是普适 CNN superiority
- `Task 37`：
  - `fresh-instance mitigation evidence`
  - 不是 universal transfer solved

## 5. 结果归档入口

### 核心锁定结果
- `/home/qiaosir/projects/compute_vit/paper/CANONICAL_RESULT_LOCK_gpt.md`

### 图注锁定
- `/home/qiaosir/projects/compute_vit/paper/FIGURE_CAPTION_LOCK_gpt.md`
- `/home/qiaosir/projects/compute_vit/paper/FIGURE_CAPTION_DRAFTS_gpt.md`

### Reviewer 风险汇总
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/EXTERNAL_REVIEW_SYNTHESIS_gpt.md`

### Gemini 接手与最新同步
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/GEMINI_HANDOFF_gpt.md`
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md`

### 新增 literature-derived case-study 入口
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/literature_fitted_profile.json`
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/literature_profile_zhang2025_provenance_gpt.md`
- `/home/qiaosir/projects/compute_vit/device_profiles/literature_profiles_gpt.json`
- `/home/qiaosir/projects/compute_vit/report_md/我已经选定 Zhang et al., Nature Communications 16, 197.md`
- `/home/qiaosir/projects/compute_vit/report_md/s41467-025-66891-6.pdf`

### Zhang 2025 OPECT case-study: latest lock

- canonical citation is now PDF-backed:
  - `Zhang et al., Nature Communications 17:197 (2026), doi:10.1038/s41467-025-66891-6`
- older prompt/file names may still carry the shorthand `16, 197 (2025)`:
  - treat that as legacy labeling, not the canonical bibliographic form
- case-study profile currently locks:
  - `G_max/G_min = 47.3`
  - `pulse_count_max = 120`
  - `n_states = 34`
  - `sigma_c2c = 0.02` as transparent proxy from Supplementary Fig. 15 / Fig. 3g repeatability evidence
  - `sigma_d2d = 0.03` as transparent proxy from the reported 80-device `V_th` spread
- retention wording should stay conservative:
  - current evidence supports qualitative state-dependent retention discussion
  - do not state that a Zhang-specific double-exponential fit has already been established
  - if later digitized, a stretched-exponential baseline is safer than assuming two timescales by default

## 6. 不要再从哪些地方反推当前状态

这些文件现在只能当历史痕迹，不应当作为当前状态入口：

- 旧版 `CLAUDE_REPLAY_POINTERS_gpt.md`（已重写）
- 早期 watcher / driver logs
- 旧的 stage-2 / stage-3 autolaunch 描述
- 旧聊天里关于 `Task 37` “仅到 epoch 0” 的说法

## 7. Claude 回来后的最合理动作

如果 Claude 现在回到项目，最值得直接审阅的是：

1. `Task 37` 是否值得升格为正文主正结果之一
2. `§5.11` synthetic case study 是否需要降调，还是继续补 literature-derived fitted profile
3. 是否立即在正文加入：
   - explicit limitations subsection
   - reproducibility / parameter provenance block
4. 是否把新的 Zhang 2025 OPECT literature profile 升格为正文 / 附录里的桥梁 case-study 主证据
5. 是否接受当前的 transparent proxy estimates:
   - `sigma_c2c = 0.02`
   - `sigma_d2d = 0.03`
   作为文献 case-study runtime 值，直到进一步 digitization 完成

一句话总结：
- 现在项目的主线实验基本锁定了
- 最关键的新强项是 `Task 37 fresh-instance recovery`
- 最大残余风险已经从“实验空白”转成“claim strength / reproducibility / bridge validation framing”

## 2026-04-07 22:10 Addendum

- Claude `C1` verification is partly closed:
  - canonical `V4` CUDA MC eval completed at
    `/home/qiaosir/projects/compute_vit/logs/_gpt/_codex_verify_v4_canonical_eval_cuda_20260407.log`
  - summary:
    - `91.69 ± 0.23%`
    - `min=91.23`, `max=91.88`, `eval_runs=10`
  - interpretation:
    - Gemini's recent `analog_layers.py` changes did **not** break canonical `V4` standard accuracy.
- Retention follow-up:
  - CUDA watcher did **not** auto-chain correctly.
  - Manual handoff was required, but the retention probe is now complete:
    `/home/qiaosir/projects/compute_vit/logs/_gpt/_codex_verify_v4_retention_probe_cuda_20260407.log`
  - summary:
    - `0s:   91.77 ± 0.28%`
    - `1s:   82.29 ± 1.02%`
    - `10s:  79.71 ± 0.34%`
    - `100s: 78.76 ± 0.47%`
  - interpretation:
    - corrected retention trend remains intact (`rapid drop` then `~79% plateau`)
    - Gemini's recent changes did **not** break the canonical retention curve
- Important code-audit nuance:
  - `analog_layers.py` contains a state-dependent retention branch, but current `_apply_retention()` still calls `_retention_decay_factor(cfg)` without passing `G`.
  - Read this as:
    - interface added
    - canonical path likely still uses scalar retention
    - do **not** over-claim that state-dependent retention is already active in canonical experiments

## 2026-04-08 00:20 Re-review Addendum

The newest reviewer-style re-evaluations have shifted the external decision boundary upward:

- old trend:
  - `Reject / Major Revision`
- current trend:
  - `Conditional Accept`
  - `Minor Revision`
  - or `Minor Revision bordering on Major`

Why the shift happened:
- `Task 37 Ensemble HAT` is now repeatedly identified as the strongest revision
- the Zhang 2026 OPECT case study is being accepted as a meaningful bridge demonstration
- the strengthened `Limitations` and `Reproducibility` framing is being read as genuine scientific maturity rather than defensive hedging

What now looks like the top remaining blockers:
1. `paper/latex_gpt/main.tex` still has `Author list TBD`
2. the manuscript still needs one submission-level proofread / typo / figure-reference sweep
3. `Ensemble HAT` needs one explicit paragraph about training-cost overhead

High-value but second-tier quantitative clarifications:
- Zhang proxy-estimate uncertainty / sensitivity note
- interconnect / routing overhead bounding analysis
- continued restraint on Flowers-102 causality
- continued explicit treatment of the `27.72%` nonlinear-write failure as a hard boundary
- continued caveat about scratch-vs-finetune confound in ConvNeXt vs Tiny-ViT comparisons

Interpretation for Claude:
- the paper no longer appears primarily blocked by missing results
- it now appears primarily blocked by
  - submission hygiene
  - quantitative framing discipline
  - and a few concise but high-leverage clarifications

## 2026-04-08 00:35 Detailed Reviewer Broadcast Pointer

If you only read one new file before making decisions, read:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/EXTERNAL_REVIEW_DETAILED_BROADCAST_20260408_gpt.md`

That file contains:
- reviewer-by-reviewer breakdown
- what each reviewer explicitly praised
- what each reviewer still treats as a blocker
- which criticisms are already outdated under the current repo state
- which remaining items are true submission blockers vs. future-work asks

Recommended decision order after reading it:
1. decide whether to prioritize `submission hygiene` immediately
   - author metadata
   - proofread / typo sweep
   - ensemble-cost paragraph
2. then decide whether to add
   - Zhang proxy-uncertainty note
   - interconnect / routing energy bounding note
