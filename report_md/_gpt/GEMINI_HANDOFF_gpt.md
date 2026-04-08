# Gemini Handoff: The "Perfectionist" Directive

## 1. 核心上下文 (Context)
你接手的是一个关于**有机光电存算一体（CIM）**的视觉模型（Tiny-ViT）科研项目。
目前论文正处于从“初稿”到“顶刊”的深度重构阶段，以应对四份极其严厉的专家审稿意见。

## 2. 后台任务状态 (Ongoing Tasks)
- **Task 37 (Ensemble HAT)**: 已完成（以 `FINAL_SAFE` run 为准）。
  - **目的**: 解决硬件实例过拟合。
  - **脚本**: `train_tinyvit_ensemble.py`
  - **日志**: `compute_vit/logs/_gpt/train_tinyvit_v4_ensemble_FINAL_SAFE.log`
  - **结果**: `best_acc = 91.13% @ epoch 94`
  - **checkpoint**:
    - `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt`
    - `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_last.pt`
  - **注意**: 这只证明 ensemble HAT 训练可以稳定收敛；它是否真正缓解 fresh-instance collapse，仍需后续专门评估，不能直接在论文中写成“问题已解决”。

## 3. 你的接力任务 (Immediate Action Items)

### A. 完成物理模型升级（最紧迫）
我刚才正在修改 `compute_vit/analog_layers.py` 以实现“状态相关保持力漂移（State-dependent Retention）”。
- **已开始**: `_retention_decay_factor` 已被设计为支持传入 `G` 张量。
- **待确认/待补全**:
  1. `AnalogLinear._apply_retention` 是否已改为分别对 `G_pos` / `G_neg` 调用状态相关衰减。
  2. `AnalogConv2d._apply_retention` 是否已同步完成。
  3. `math.exp` 是否已完全替换为 `torch.exp` 以支持张量路径。
  4. 若代码已改，必须补测试并在 `AGENT_SYNC_gpt.md` 中写明证据文件。

### B. 视觉系统重构
- **Fig 11 (Energy)**: 审稿人极其讨厌现在的“大饼图”。
  - **任务**: 修改 `plot_paper_figures.py` 中的 `plot_fig11_energy_breakdown` 函数。
  - **要求**: 改为**横向堆叠柱状图 (Stacked Bar Chart)**。对比 Digital Baseline (GPU) 和我们的 Hybrid Architecture。
- **Fig 12 (Attention Maps)**: 增加量化分析。
  - **要求**: 在热力图下方计算并标注 **Entropy (信息熵)**，证明 HAT 降低了注意力散射。

### C. 真实数据案例研究 (Case Study)
- **任务**: 创建一个 `report_md/_gpt/json_gpt/measured_sample_profile.json`。
- **逻辑**: 填入一组模拟的真实数据（例如 $G_{max}/G_{min}$ 更窄、噪声更大的数据），运行一次推理，并在论文中增加一个小节展示“如何用本框架评估新材料”。

### D. 最终审计
- 扫描全文，删除 `TODO`、`pending` 以及乱码 `as!oue uapn`。
- 确保所有参数（$\sigma=5\%$ 等）在正文中都有文献引用（见 §4.2 修正版）。
- **新增提醒**:
  - `paper/latex_gpt/sections/05_results.tex` 里的图文件名必须和 `paper/latex_gpt/figures/` 真实文件一致，不能只改 `\graphicspath`。
  - `Task 37` 的训练结果要同步进 `AGENT_SYNC_gpt.md` 和中英文结果节，否则 handoff 会再次过时。

## 4. 启动建议
请首先读取：
1. `report_md/_gpt/AGENT_SYNC_gpt.md` 的末尾
2. `paper/CANONICAL_RESULT_LOCK_gpt.md`
3. `paper/latex_gpt/SUBMISSION_PACKET_gpt.md`

然后按这个优先级推进：
1. 写回 `Task 37 FINAL_SAFE` 的真实完成态
2. 完成 / 核实 state-dependent retention
3. 做 measured-profile case study
4. 收口 Fig.11 / Fig.12 / LaTeX 图名一致性

**祝你好运，把这篇论文带向顶刊！**

---

## 5. 新增：Perplexity 驱动的 literature-derived profile 入口

已新增一个可以直接被项目读取的 OPECT case-study profile：

- `/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/literature_fitted_profile.json`
- `/home/qiaosir/projects/compute_vit/device_profiles/literature_profiles_gpt.json`
- 参数来源说明：
  - `/home/qiaosir/projects/compute_vit/report_md/_gpt/literature_profile_zhang2025_provenance_gpt.md`

当前锁定口径：
- 选用文献：Zhang et al., *Nature Communications* 17, 197 (2026)
- `G_max/G_min = 47.3` 直接纳入
- `pulse_count_max = 120` 直接纳入
- `n_states = 34` 作为保守 stable-state 解释
- `sigma_c2c = 0.02` 与 `sigma_d2d = 0.03` 现在作为透明 proxy estimates 使用
  - 依据：
    - Supplementary Fig. 15 / Fig. 3g repeatability
    - 80-device `V_th` spread (0.67%-1.46%)
- retention 现阶段要保守写成：
  - `supports qualitative state-dependent retention discussion`
  - 不要直接写成已经完成双指数拟合
- 原文 `NL_LTP/NL_LTD` 指标 **不要** 直接镜像进中文稿或代码说明，因为其定义尚未与当前 surrogate NL 参数一一校准

最新证据入口：
- `/home/qiaosir/projects/compute_vit/report_md/我已经选定 Zhang et al., Nature Communications 16, 197.md`
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/literature_profile_zhang2025_provenance_gpt.md`
- `/home/qiaosir/projects/compute_vit/report_md/s41467-025-66891-6.pdf`

如果 Gemini 继续收 `paper_zh`，应把这个 case study 写成：
- `literature-derived bridge demonstration`
- 不是 `measured-device full validation`
- 并注意：
  - 旧 prompt 文件名里还保留 `16, 197` 的历史缩写
  - 当前项目 canonical citation 已按本地 PDF 改为 `Nature Communications 17:197 (2026)`

## 6. Claude 苏醒前最值钱的 3 个优化点

如果还要在 Claude 回来前继续收口，优先级建议是：

1. **显式 Limitations 子节**
   - 把这些 reviewer 高频痛点集中写成一个小节，而不是散落在全文：
     - no measured-device full closure yet
     - transparent proxy estimates for Zhang `sigma_c2c / sigma_d2d`
     - no temperature model
     - no full ADC timing/area model
     - scratch-vs-finetune confound in ConvNeXt vs Tiny-ViT

2. **submission-facing reproducibility block**
   - 集中列：
     - optimizer
     - lr schedule
     - batch size
     - epoch count
     - HAT / ensemble scheduling
     - MC sample counts
     - checkpoint identity
     - eval semantics (`best` vs `MC`)

3. **parameter provenance appendix/table**
   - 把 canonical organic profile、Zhang 2026 OPECT profile、Task 34/35/36 stress settings 统一列成一个来源表
   - 目的不是加新实验，而是降低 reviewer 对“参数是否随意选取”的攻击面

另外必须继续保持：
- `86.37 ± 1.54%` = canonical fresh-instance mitigation
- `88.53%` = Zhang 2026 literature-profile transfer
- 两者不能混写成同一条数字

## 7. Codex 2026-04-07 22:10 对接补充

- Claude `C1` 的标准 accuracy 核验已经先拿到一半结论：
  - `/home/qiaosir/projects/compute_vit/logs/_gpt/_codex_verify_v4_canonical_eval_cuda_20260407.log`
  - `91.69 ± 0.23%` (`eval_runs=10`)
  - 这说明你最近对 `analog_layers.py` 的改动**没有破坏 canonical V4 标准精度**。
- retention follow-up 目前已由 Codex 接管：
  - watcher 没自动接上
  - 但手动补跑已经完成：
    `/home/qiaosir/projects/compute_vit/logs/_gpt/_codex_verify_v4_retention_probe_cuda_20260407.log`
  - 锁定结果：
    - `0s: 91.77 ± 0.28%`
    - `1s: 82.29 ± 1.02%`
    - `10s: 79.71 ± 0.34%`
    - `100s: 78.76 ± 0.47%`
  - 这说明你最近的改动**没有破坏 corrected retention 的 canonical 数值趋势**。
- 一个重要表述边界：
  - 你加的 state-dependent retention branch 确实存在；
  - 但当前 `_apply_retention()` 还没有把 `G_pos/G_neg` 传给 `_retention_decay_factor(cfg, G=...)`；
  - 因此不要在中文稿或同步里把 canonical 实验写成“已经启用 state-dependent retention”。

## 8. 2026-04-08 复审趋势更新

最新外部 review synthesis 已显示一个重要趋势变化：
- 现在更像 `Conditional Accept / Minor Revision`
- 不再主要是“缺结果”，而更像“submission hygiene + framing discipline”

因此 Gemini 这边后续不建议再主动扩大实验范围，除非 Claude 明确要求。

更值得支持 Claude 决策的点是：
1. 保持中英文对 `Task 37`、`§5.11`、`Flowers-102 hypothesis`、`nonlinear-write boundary` 的口径稳定
2. 不要把 `Task 37` 写成 universal transfer solved
3. 若需要继续改稿，优先支持：
   - 作者信息完善
   - proofread / typo cleanup
   - Ensemble HAT 成本说明
   - proxy-uncertainty 与 energy-bounding 的保守表述

## 9. 详细外部审稿广播入口

为避免只看到摘要、误判 reviewer 优先级，请优先读取：
- `/home/qiaosir/projects/compute_vit/report_md/_gpt/EXTERNAL_REVIEW_DETAILED_BROADCAST_20260408_gpt.md`

这份文件包含：
- reviewer-by-reviewer 的细分判断
- 哪些批评已经被当前版本化解
- 哪些仍是真实 blocker
- 哪些属于 future-work 级别、当前不应再扩 scope 的要求

Gemini 侧应特别保持的口径：
- 不要把所有 reviewer 都理解成“还要继续开大实验”
- 当前多数新复审更像是要求：
  - submission hygiene
  - claim-strength restraint
  - 少量 quantitative clarification
- 不是重新打开一个 full major-revision research program
