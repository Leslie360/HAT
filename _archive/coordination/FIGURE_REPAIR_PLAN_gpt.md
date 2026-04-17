# T5: Figure 批量修缮方案 [Gemini]

## 目标
响应 4 位 Reviewer 对可视化质量的集中反馈 (Issues: #27, 28, 29, 30, 32, 90)，提升论文图表的专业度和完整性。

## 修缮方案清单

所有待修改图形的代码主要位于核心绘图脚本: `paper/plot_paper_figures.py` 和 `visualize_attention.py`。以下是针对各个 Figure 的具体修改策略，供执行阶段（如 Codex）直接应用：

### 1. Fig 3, 4, 6, 8 (Axis labels, Units, Legends)
*   **问题**: 标签不规范，单位可能缺失，图例位置或文字不清晰。
*   **修改脚本**: `paper/plot_paper_figures.py`
*   **执行策略**:
    *   **Fig 3/4 (Accuracy & HAT)**: 检查 `plt.ylabel('Accuracy (%)')` 是否完整，确保 legends 使用简洁且易读的 labels。
    *   **Fig 6 (Frontend Compensation)**: 确保 x-axis `$\gamma_{\text{phys}}$` 和 y-axis `Accuracy (%)` 的单位完备，legend 数学格式严格使用 LaTeX。
    *   **Fig 8 (Pareto Energy-Accuracy)**: 检查 `plt.xlabel('Inference Energy ($\mu$J)')` 和 `plt.ylabel('Accuracy (%)')` 的符号。图例防止遮挡关键数据点。

### 2. Fig 7 (Retention Curve)
*   **问题**: x/y 轴对齐与 panel 一致性。
*   **修改脚本**: `paper/plot_paper_figures.py`
*   **执行策略**:
    *   使用 `plt.subplots()` 统一设定图表外边距 (`plt.tight_layout()`)。
    *   确保 x-axis 时间使用的是对数坐标 (`set_xscale('log')`) 并在 x-label 显式标注单位 `Time (s)`。
    *   限制 y-axis 的 `Accuracy (%)` 范围，使其与论文中其他 panel 的高度视觉一致。

### 3. Fig 9 (Energy Breakdown)
*   **问题**: "Total cost 3137" 无单位；ADC/DAC = 0.0% 视觉误导。
*   **修改脚本**: `paper/plot_paper_figures.py`
*   **执行策略**:
    *   饼图中心或副标题的文本，将从类似 `f"Total: {cost}"` 修改为 `f"Total Cost: {cost:.2f} $\mu$J"`。
    *   配合 T2 任务的结论，将 0.0% 的占比合并或使用明确的记号(如 `*`)，并在图例注释中解释其未建模状态，防止 Reviewer 误解为物理 0 消耗。

### 4. Fig 10 (Attention Maps)
*   **问题**: 缺 input images + color scale + sample ID。
*   **修改脚本**: `visualize_attention.py` 
*   **执行策略**:
    *   增加最左侧一列作为 **Input Reference panel**，绘制原图 (RGB)。
    *   在图表右侧或底部附加一个全局的 `plt.colorbar()` 标量条。
    *   在 y-axis 或 titles 为每行标注样本元数据，例如 `CIFAR-10 (ID: 42)`。

## 下一步 (Handoff)
此计划处于 Design-ready 状态。后续可交由 Codex 或 Python agent 直接按此标准批量调整绘图脚本，重新生成 PDF figures 供 LaTeX 引用。