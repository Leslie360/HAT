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

## 2026-04-08 23:15 Figure / Reference / Story Decision Pointer

## 2026-04-09 18:36 C4 / AIHWKIT Addendum

- The recovered historical training audit now strongly indicates that we had been mixing:
  - the historical canonical `C4` checkpoint (`89.91%`, `batch_size=256`)
  - and the later Task 36 proportional-noise extension (`91.98%`, `batch_size=128`, `noise_mode=proportional`, `AMP off`)
- read the current `C4` discrepancy primarily through that lens, not through a hidden-AMP hypothesis.

### Current `C4-fix-v2` live state

- queue:
  - `/home/qiaosir/projects/compute_vit/scripts/_gpt/run_c4_fix256_queue_20260409_gpt.sh`
  - `/home/qiaosir/projects/compute_vit/logs/_gpt/c4_fix256_queue_20260409.log`
- `seed=42` is fully closed:
  - train log:
    - `/home/qiaosir/projects/compute_vit/logs/_gpt/multi_seed/multi_seed_C4_fix256_s42.log`
  - eval log:
    - `/home/qiaosir/projects/compute_vit/logs/_gpt/multi_seed/multi_seed_C4_fix256_s42_eval.log`
  - locked result:
    - best checkpoint = `83.02% @ epoch 195`
    - `10-run eval = 82.64 ± 0.15%`
- `seed=123` is now also fully closed:
  - train log:
    - `/home/qiaosir/projects/compute_vit/logs/_gpt/multi_seed/multi_seed_C4_fix256_s123.log`
  - eval log:
    - `/home/qiaosir/projects/compute_vit/logs/_gpt/multi_seed/multi_seed_C4_fix256_s123_eval.log`
  - locked result:
    - best checkpoint = `82.51% @ epoch 195`
    - `10-run eval = 82.19 ± 0.10%`
- `seed=2026` is currently live and finite:
  - `/home/qiaosir/projects/compute_vit/logs/_gpt/multi_seed/multi_seed_C4_fix256_s2026.log`
  - latest visible status at sync time:
    - `Epoch 82`
    - `best = 77.27%`

Interpretation:
- `BS=256 + AMP off` confirms that the training chain is healthy and closer to the historical recipe than the earlier `BS=128` rescue run.
- It still does **not** recover the historical canonical `89.91%` on the first two completed seeds, so the paper should not treat the older single-run number as trivially reproducible.

### `P13` AIHWKIT status has advanced

- this is no longer just a design note
- minimal CPU shared-regime benchmark exists:
  - `/home/qiaosir/projects/compute_vit/report_md/_gpt/P13_aihwkit_shared_regime_result_256.md`
  - `/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/p13_aihwkit_shared_regime_result_256.json`
- locked reviewer-facing result:
  - digital subset = `96.88%`
  - AIHWKIT subset = `91.80 ± 1.02%`
  - subset size = `256`
  - eval runs = `5`
  - wall clock = `151.1s`

Safe claim:
- this is a **bounded shared-regime sanity check**
- it is sufficient to rebut "no numeric cross-check at all"
- it is **not** a full AIHWKIT equivalence study for retention, photoresponse, or organic write nonlinearity

Manuscript status:
- the bounded AIHWKIT result has now been folded into:
  - `/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/06_discussion.tex`
  - `/home/qiaosir/projects/compute_vit/paper/06_discussion.md`

If you only read one new sync block before deciding what to keep from the user's new assets, read:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md`
  - section: `[Codex] 2026-04-08 23:15`

What that block contains:
- direct assessment of the user's new Banana figures `figA`-`figD`
- which ones should become manuscript figures vs. which ones should stay as optional concept assets
- exact manual crop guidance for the user
- which reference groups from `参考文献2.md` are actually worth integrating
- the current best story spine for the paper

Shortest actionable summary:
- use `figA` for `Fig.1`, but only after manually removing the broken top title and bottom footnote strip
- use `figB` for `Fig.2`, but only after removing the duplicated bottom ribbon text
- keep `figC` as an optional concept / bridge figure, not a forced main-text replacement
- do not use `figD` as a main paper figure in its current form
- no new broad Perplexity search is needed right now; the current targeted citation harvest is sufficient for the next citation pass

## 2026-04-08 23:28 FW-1 Quick Pointer

If you only need the latest training-state fact:
- `V1 seed=2026` has now finished cleanly and its missing eval has been completed
- the Tiny-ViT digital-baseline `V1` three-seed set is now fully closed:
  - `42  -> 98.18%`
  - `123 -> 97.87%`
  - `2026 -> 98.14%`
  - aggregate:
    - `98.06% mean`
    - `0.14 pp population std`

Source of truth:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md`
  - section: `[Codex] 2026-04-08 23:28`

Interpretation:
- useful reproducibility evidence
- should live in appendix / reproducibility framing
- should **not** displace the main scientific story about:
  - fresh-instance transfer
  - Ensemble HAT
  - literature-profile transfer
  - nonlinear-write boundary

## 2026-04-08 23:56 Overnight Queue Pointer

If you only need the current compute status before making the next decision, read:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md`
  - section: `[Codex] 2026-04-08 23:56`

What changed:
- Codex re-read the latest `CLAUDE_TASK_gpt.md` and `MASTER_PLAN.md`
- verified that:
  - `V1` three-seed is complete
  - `V4/C1/C4` nine remaining seed logs are stale CLI failures
  - `V8` is resumable from `epoch 23`
- then launched a detached tmux queue that should keep the GPU busy overnight:
  1. `V4` three seeds train + eval
  2. `C1` three seeds train + eval
  3. `C4` three seeds train + eval
  4. `V8` resume to 50 epochs + eval

Operational handles:
- tmux session:
  - `fw1_p2_overnight_gpt`
- driver log:
  - `/home/qiaosir/projects/compute_vit/logs/_gpt/fw1_p2_overnight_queue_20260409.log`

Shortest factual status at launch:
- queue boot confirmed
- first live job is `V4 seed=42 train`

## 2026-04-09 00:08 Story Rewrite Pointer

If you only need the latest non-GPU manuscript improvement:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md`
  - section: `[Codex] 2026-04-09 00:08`

What changed:
- `00_abstract.tex`, `01_introduction.tex`, and `07_conclusion.tex` were rewritten around the stronger narrative spine:
  - unmet deployment-decision problem
  - gap against existing device papers and inorganic-oriented simulators
  - profile-driven bridge as the method
  - four system questions answered
  - quantified headline results
  - bounded final claim

Practical meaning:
- the manuscript should now read less like a catalog of experiments
- and more like a targeted answer to:
  - which measured organic-device characteristics actually matter first for deployment

## 2026-04-09 00:19 Citation Strengthening Pointer

If you only need the latest literature-facing upgrade:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md`
  - section: `[Codex] 2026-04-09 00:19`

What changed:
- targeted references from `参考文献2.md` were added to support:
  - optical non-uniformity / crosstalk
  - IR drop / sneak path
  - temperature sensitivity

Why it matters:
- these were three of the most reviewer-visible limitation claims
- they now have stronger primary-source backing in `§2` and `§6.6`

## 2026-04-09 00:08 Markdown Sync Pointer

If you only need the latest non-GPU cleanup:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md`
  - section: `[Codex] 2026-04-09 00:08`

What changed:
- the English markdown side now matches the revised LaTeX side for:
  - `01_introduction`
  - `02_related_work`
  - `06_discussion`
  - `07_conclusion`

Why it matters:
- there is no longer a stale `.md` vs `.tex` story split
- tomorrow-morning review should be lower-friction because both manuscript paths now tell the same bounded deployment-bridge story

Concurrent GPU note:
- overnight queue still alive
- latest visible training state:
  - `V4 seed=42`
  - `Epoch 14`
  - `best=69.66%`

## 2026-04-09 01:02 Reviewer-Facing Delta

If Claude only checks one new manuscript-facing improvement from this round:
- the attention-map section in `§5` is no longer purely qualitative

What changed:
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex`
- `/home/qiaosir/projects/compute_vit/paper/05_results.md`

New quantitative supplement:
- mean head-averaged attention entropy across the three representative samples:
  - `V1 = 3.38`
  - `V3 = 3.61`
  - `V4 = 3.07`
- `V4` restores the correct class on all three displayed examples, while `V3` is correct on only one

Why it matters:
- this directly answers a recurring reviewer complaint that the attention figure was "qualitative only"
- the new phrasing stays modest:
  - not a full attention-geometry benchmark
  - but no longer just a visual anecdote

Concurrent GPU note:
- overnight queue still alive
- latest visible training state:
  - `V4 seed=42`
  - `Epoch 46`
  - `best=85.68%`

## 2026-04-09 01:18 Model-Review Distillate

If Claude only wants the shortest readout from:
- `/home/qiaosir/projects/compute_vit/report_md/审稿人意见from_model.md`

Use this interpretation:

### What the new bundle really says

- it does **not** change the current strategic picture
- it mainly reinforces:
  - keep the paper framed as a `profile-driven deployment-decision bridge`
  - do not let it sound like a predictive hardware emulator
  - expect continued pressure for AIHWKIT/inorganic-tool comparison
  - keep Flowers-102 at hypothesis-level
  - keep energy claims bounded

### What is still truly active

1. bibliography placeholders remain real
   - `refs_gpt.bib` still contains many `and others` / `Author and others`
2. a likely front-end figure cross-reference bug still exists
   - current `05_results.tex` says:
     - `Figure 6 summarizes ... frontend configurations`
3. the visible `11.45x` sentence in `§5.10` is still a likely reviewer attack surface if not further bounded

### What now looks stale

1. `Author list TBD`
   - outdated
   - current `main.tex` has `Songqiao Li`
2. "attention maps are purely qualitative"
   - only partly true now
   - entropy supplement has been added
3. some broad formatting complaints likely target older exported PDFs

### Best practical next step if Claude wants one small, high-leverage cleanup

Choose one of:
1. bibliography placeholder cleanup
2. front-end figure-reference fix
3. slightly stronger caveat in the `11.45x` sentence

## 2026-04-09 01:46 Hygiene Pass Closed

The three small reviewer-visible cleanup items from the previous pointer have now been partly or fully addressed:

1. **Front-end figure-reference bug**
   - fixed
   - `05_results.tex` now points to `Fig.~\\ref{fig:frontend-compensation}` instead of a stale hard-coded `Figure 6`

2. **Visible `11.45x` sentence**
   - tightened
   - `05_results.tex` / `05_results.md` now explicitly say the number is a first-order, upper-bound-like estimate under current operation-count assumptions
   - they also explicitly note that interconnect / data-marshaling overhead is still absorbed into memory-access terms

3. **Placeholder bibliography entries**
   - the worst class is fixed:
     - no remaining `Author and others` entries
   - DOI-backed metadata now fills:
     - `visionarch2023crosstalk`
     - `amspa2024insensor`
     - `fastirdrop2025`
     - `iconniv2025`
     - `zhang2026opect`
   - remaining note:
     - broader `and others` cleanup is still unfinished

Concurrent GPU note:
- overnight queue still alive
- latest visible training state:
  - `V4 seed=42`
  - `Epoch 85`
  - `best=88.07%`

## 2026-04-09 02:08 Queue Reality Check

The previous `Epoch 85 / best 88.07` note is now stale.

### Current true state

- `V4 seed=42` has fully completed:
  - training: `best=88.45% @ epoch 98`
  - 10-run eval: `87.64 ± 0.48%`
- queue then advanced as expected:
  - `START | V4 seed=123 train`

### Important log-reading caveat

- `multi_seed_V4_s123.log` still contains an old stale CLI error banner at the top
- that banner belongs to an earlier failed invocation
- the live run **does** start below it:
  - `Starting train for V4 on cifar10 (Seed: 123, BS: 256, AMP: True, pretrained=True)`

### Small manuscript cleanup also landed

- `refs_gpt.bib` now additionally has full DOI-backed authors for:
  - `fuller2020tempresilient`
  - `guo2024hightemp`

## 2026-04-09 02:28 Reproducibility Layer Strengthened

Two more paper-facing upgrades landed without interrupting the queue:

### 1. `V4 seed=42` is now encoded in the manuscript as a sanity-check result

- reproducibility block (`04_experimental_setup.tex/.md`) now states that a fresh rerun of the canonical V4 regime reached:
  - `88.45% @ epoch 98` best checkpoint
  - `87.64 ± 0.48%` over a 10-run noisy checkpoint evaluation
- appendix (`08_appendix.tex/.md`) now contains a compact table for this rerun sanity check
- framing is deliberately conservative:
  - this is a representative rerun anchor
  - not yet the final full V4 three-seed aggregate

### 2. Bibliography hygiene improved again

Additional cited entries now have DOI-backed full metadata:
- `peng2020dnnneurosim`
- `wu2023bwq`
- `ge2024allspark`
- `yoon2025adc`

### Current live queue note

- `V4 seed=123` is genuinely running
- latest visible point: `Epoch 5`, `best=48.78%`

## 2026-04-09 09:35 C4 Fix Has Been Relaunched Cleanly

The old overnight queue is no longer the active GPU path. The current critical action is the corrected `C4` rerun that Claude requested.

### Live status

- detached tmux session: `c4_fix_20260409_gpt`
- driver log:
  - `/home/qiaosir/projects/compute_vit/logs/_gpt/c4_fix_queue_20260409.log`
- queue script:
  - `/home/qiaosir/projects/compute_vit/scripts/_gpt/run_c4_fix_queue_20260409_gpt.sh`
- first train log:
  - `/home/qiaosir/projects/compute_vit/logs/_gpt/multi_seed/multi_seed_C4_fix_s42.log`

### Settings

- `batch-size = 128`
- `AMP = off`
- fresh save dirs under:
  - `/home/qiaosir/projects/compute_vit/checkpoints/_gpt/multi_seed_fix/`

### Why this matters

This intentionally avoids the stale failed checkpoints from the overnight queue and follows the Claude-audited safe recipe for `C4`.

### Parallel Gemini support

Gemini has been split onto the non-blocking preparation tasks:

- `P13`: AIHWKIT shared-regime benchmark prep — still pending final return
- `P14`: Flowers-102 ablation prep — completed

P14 deliverables now exist at:
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/P14_FLOWERS_ABLATION_PLAN_gpt.md`
- `/home/qiaosir/projects/compute_vit/scripts/_gpt/run_flowers102_noise_ablation_gpt.sh`

### New reality check

- `C4-fix` has now advanced beyond startup without reproducing the overnight NaN failure:
  - `Epoch 0: train_loss=47.2612`
  - `Epoch 1: train_loss=2.5736`
  - `Epoch 2: train_loss=2.4664`

- `P13` is no longer just a vague future-work placeholder; the refreshed note at
  - `/home/qiaosir/projects/compute_vit/report_md/_gpt/AIHWKIT_COMPARISON_DESIGN_gpt.md`
  now explicitly locks the reviewer-facing minimal benchmark to:
  - `ResNet-18 + CIFAR-10 + shared regime`
  and clearly records the current blocker:
  - local environment still lacks `aihwkit`

## 2026-04-09 17:21 C4 Third Pass Is Now the Live GPU Path

The `BS=128` C4-fix run is no longer the only active interpretation target.

### Why a third pass was launched

- Claude's latest audit correctly identified that the historical successful C4 checkpoint stored:
  - `batch_size = 256`
- The `BS=128` three-seed rerun was stable but materially lower:
  - `82.97%` mean over seeds
- A closer recipe match is therefore required before freezing the paper narrative.

### Important correction

Claude's audit suggested optionally adding AMP back, but the original successful training log shows:
- `AMP requested: False, active: False`
- `AMP: off`

So the best-matched replay recipe is:
- `BS=256`
- `AMP=off`

### Current live queue

- detached tmux session:
  - `c4_fix256_20260409_gpt`
- queue script:
  - `/home/qiaosir/projects/compute_vit/scripts/_gpt/run_c4_fix256_queue_20260409_gpt.sh`
- driver log:
  - `/home/qiaosir/projects/compute_vit/logs/_gpt/c4_fix256_queue_20260409.log`
- fresh save root:
  - `/home/qiaosir/projects/compute_vit/checkpoints/_gpt/multi_seed_fix256`

### Parallel side work

- `P13` AIHWKIT has also been delegated again in parallel so the CPU-side benchmark work can progress while GPU is occupied.

## 2026-04-09 23:08 Kimi Follow-up Corrections

- `#93` is no longer silent:
  - `§5.5` and `Appendix A.5` now explicitly state that the retention sanity check is scoped to the retained V4 Ensemble-HAT path and was **not** repeated on standard-HAT or non-HAT checkpoints.
- `#104` is now directly addressed with the exact references Kimi asked for:
  - `liu2021ptqvit` = *Post-Training Quantization for Vision Transformer* (NeurIPS 2021)
  - `li2022qvit` = *Q-ViT: Accurate and Fully Quantized Low-Bit Vision Transformer* (NeurIPS 2022)
- important truth correction on figure quality:
  - quantitative plots (`fig4`--`fig11`, attention maps) compile from PDF assets
  - `Fig.1` and `Fig.2` still compile from Banana PNG schematics
  - so vector-figure coverage is only **partial**, not complete
- ligature/rendering note:
  - source text is clean, but the TeX environment still emits a `pdftex.map` font warning
  - an attempted `fontenc`/`lmodern` fix was reverted because it broke compilation on this machine
- live GPU status:
  - `P1-fix-v3` seed=123 is the current run
  - latest visible checkpoint: `Epoch 14`, `best=66.47%`
  - log: `/home/qiaosir/projects/compute_vit/logs/_gpt/multi_seed/multi_seed_C4_v3_s123.log`

### Additional audit clarifications

- `Table 1` is not a live formatting blocker anymore:
  - the current baseline table (`tab:fp32-baselines`) renders normally in the latest `main.pdf`
- `Fig.10` still lacks input-image context:
  - fixed in the latest build: `fig10_zero_shot_transferability` now includes a top strip of representative CIFAR-10 inputs with sample IDs above the transferability panels
- the ligature/rendering complaint appears to be a PDF font-path issue rather than a source-text typo:
  - `main.pdf` still embeds mostly Type 3 fonts without Unicode maps
  - `main.log` still shows `pdftex.map` warnings

### Latest follow-up

- `Fig.10` was upgraded to a context-aware layout:
  - top strip: representative CIFAR-10 input images (`id 0`, `23`, `37`)
  - bottom: ConvNeXt / Tiny-ViT transferability panels
- `P1-fix-v3` seed=123 is still the live run and is climbing normally:
  - latest visible state: `Epoch 109`, `best=81.39%`
  - log: `/home/qiaosir/projects/compute_vit/logs/_gpt/multi_seed/multi_seed_C4_v3_s123.log`

## 2026-04-10 23:58 Render/Vector Closure Update

- the earlier ligature/render-path diagnosis is now outdated:
  - `updmap --user` restored a valid `pdftex.map`
  - `main.log` now shows `/home/qiaosir/.texlive2021/texmf-var/fonts/map/pdftex/updmap/pdftex.map`
  - the old `pdftex.map` warning is gone
- the remaining `Type 3` fonts were traced to the attention-map PDFs only
- those attention figures were regenerated without embedded text, and their semantics were moved into the caption:
  - `/home/qiaosir/projects/compute_vit/visualize_attention.py`
  - `/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex`
- current hard evidence:
  - `pdffonts fig_attention_maps.pdf` -> no embedded fonts
  - `pdffonts fig_attention_differences.pdf` -> no embedded fonts
  - `pdffonts main.pdf` -> only `Type 1` / `CID TrueType`, no `Type 3`
- consequence for reviewer tracking:
  - `#97` should now be treated as **resolved**
  - `#103` should now be treated as **resolved** for the compiled main manuscript, because Fig.1/2 and the attention figures also compile from PDF assets
- live GPU note:
  - `P1-fix-v3` seed=123 latest visible state is `Epoch 147`, `best=82.59%`
  - log: `/home/qiaosir/projects/compute_vit/logs/_gpt/multi_seed/multi_seed_C4_v3_s123.log`

## 2026-04-11 00:24 C4-v3 Seed123 Result

- `P1-fix-v3` seed=123 has now finished cleanly:
  - best checkpoint: `84.62% @ epoch 197`
  - 10-run eval: `84.58 ± 0.11%`
  - logs:
    - `/home/qiaosir/projects/compute_vit/logs/_gpt/multi_seed/multi_seed_C4_v3_s123.log`
    - `/home/qiaosir/projects/compute_vit/logs/_gpt/multi_seed/multi_seed_C4_v3_s123_eval.log`
- queue progression is healthy:
  - seed=2026 has already started automatically
  - driver log:
    - `/home/qiaosir/projects/compute_vit/logs/_gpt/c4_fixv3_proportional_queue_20260409.log`
