# GM-X34: Optional Experiment Gate Memo

根据 2026-04-13 战略重置要求，本项目对当前处于 "expansion mode" 的可选实验进行高收益 (ROI) 评估。

## 1. 实验候选列表与 Payoff 评估

| 实验 ID | 描述 | 回应的 Reviewer 质疑 | 科学 Payoff | 成本 (GPU-hrs) | 优先级 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **GM-E1** | **i.i.d. D2D 消融对照** | Ensemble HAT 是否只是通用噪声增强？ | **极高**。确立算法核心新颖性。 | < 1 hr | **P0 (Must do)** |
| **GM-E2** | **纯数字 ADC 扫描** | 6-bit 悬崖是模拟特有还是算法通用？ | **高**。分离噪声与量化贡献。 | < 1 hr | **P0 (Must do)** |
| **GM-E3** | **$\tau$ 敏感性矩阵** | 代理参数 $\tau$ 的选择是否具有循环论证嫌疑？ | **中**。增强参数稳健性证明。 | ~2 hrs | **P1** |
| **GM-E4** | **轻量级 NL 扫描 (1.5-2.5)** | NL=2.0 边界是否具有普适性？ | **高**。软化边界论述的数据支撑。 | ~10 hrs | **P1 (Wait for measured data)** |

## 2. 决策建议 (Gate Decision)

### ✅ 批准执行: GM-E1 & GM-E2
- **理由**: 成本极低（均为推理端评估，无需重训），且能直接填补 `05_results.tex` 中预留的 "Control experiment confirms..." 论证空白。
- **状态**: 
  - GM-E1 已成功在 `ablation_ensemble_hat_vs_iid.py` 中跑出 10 实例均值 86.5% 的数据。
  - GM-E2 正在通过修正后的 `run_pure_digital_adc_sweep.py`（加入动态范围校准）重新执行。

### ⏸️ 暂缓执行: GM-E4
- **理由**: 重训练 Checkpoint 成本较高。建议等待材料博士回传实测 $NL$ 参数后，针对性地跑一组实测 $NL$ 的 Baseline，而不是盲目扫参。

## 3. 实验插入路径 (GM-X35 预览)
所有结果将仅作为 **"Methodological Robustness Checks"** 插入 Supplementary Information，并在主文 Results 相应段落各增加一句 takeaway 引用。
