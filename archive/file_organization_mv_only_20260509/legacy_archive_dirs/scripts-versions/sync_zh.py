import os

# 1. Update 06_discussion.md
with open("paper_zh/06_discussion.md", "r") as f:
    text = f.read()

limitations_text = """## 6.6 局限性

虽然本框架提供了结构化的系统级见解，但必须明确承认以下物理理想化假设是当前行为模型的局限性：
- **一阶能量模型**：阵列到数字互连的能量被吸收在 SRAM 读写成本项中。专用的布线开销（包括模拟输出总线和数字协处理器之间的数据编组）未单独列出。
- **硬件阵列非理想特性**：未建模沿交叉阵列字线和位线的位置相关 IR 压降（IR drop），以及无源阵列中的潜影电流（sneak-path currents）。这些效应会引入与随机 C2C/D2D 变异不同的、依赖于输入模式的系统性权重失真。
- **非线性写入**：我们的 `NL_LTP/NL_LTD` 实现是一种梯度缩放近似。在实际的脉冲编程中，离子/电子迁移的随机性可能会进一步降低 HAT 的恢复效果。
- **状态相关漂移**：均匀的保持力衰减是一种理想化假设。如果高电导状态的漂移速度明显快于低电导状态，那么在没有更频繁的重新校准的情况下，79% 的“稳定平台期”可能会进一步下降。
- **INL/DNL 复杂性**：现实世界中非线性的电导分布可能会引入系统性偏差，这些偏差比本文建模的高斯噪声更难克服。
- **温度敏感性**：温度相关的迁移率和阈值电压漂移在实际部署环境中对有机半导体至关重要，但在当前框架中尚未建模，代表了一个优先的扩展方向。

## 6.7 未来方向

未来最重要的工作是闭环实验室测量与仿真器。目前框架已支持 JSON 配置文件，但将原始测量数据转化为分布参数仍需手动。未来的工作应该自动提取 $G_{\\max}/G_{\\min}$、状态数、变异性和保持力常数。
此外，应探索**多实例 HAT**以应对硬件过拟合；并在外设层面探索**混合精度 ADC**分配，以在脆弱的注意力层分配更高精度，从而进一步推高能效边界。
"""

start_idx = text.find("## 6.5 物理建模局限性说明")
if start_idx != -1:
    text = text[:start_idx] + limitations_text
    with open("paper_zh/06_discussion.md", "w") as f:
        f.write(text)

# 2. Update 04_experimental_setup.md
with open("paper_zh/04_experimental_setup.md", "r") as f:
    text2 = f.read()

repro_text = """

## 4.4 可复现性与透明度

为了确保计算的可复现性，所有训练运行均在固定的随机种子和确定的 PyTorch 操作下进行。以下是实验执行的集中元数据：
- **优化器**：ResNet-18 (SGD, LR=$0.1$)，ConvNeXt-Tiny (AdamW, LR=$4\\times 10^{-3}$)，和 Tiny-ViT-5M (AdamW, LR=$5\\times 10^{-4}$)。均使用余弦退火学习率调度。ResNet-18 的权重衰减设为 $5\\times 10^{-4}$，ConvNeXt/Tiny-ViT 设为 $0.05$。
- **硬件感知训练 (HAT)**：HAT 损失函数采用直通估计器 (STE)，并在训练循环期间原生注入附加的每次前向标准高斯噪声。
- **Epochs 和 Batch Size**：ResNet-18 (200 epochs, batch 128); ConvNeXt-Tiny (200 epochs, batch 256); Tiny-ViT-5M (100 epochs, batch 64)。
- **评估语义**：所有噪声推理评估均源自多遍蒙特卡洛 (MC) 采样（例如，每个检查点评估设置 10 次运行，特定的保持力扫描为 20 次运行）。报告的指标专门是这些重复随机传递的平均值和标准差。
- **检查点选择**：跨数据集比较报告最佳 epoch 检查点，而蒙特卡洛测试指标报告围绕这些锁定检查点的分布。
- **代码与数据**：仿真框架、器件配置文件模式和训练脚本将在发表时开源发布。附录中提供了器件参数推导和来源文献的摘要，以保证参数出处的透明度。
"""

if "## 4.4 可复现性与透明度" not in text2:
    text2 += repro_text

with open("paper_zh/04_experimental_setup.md", "w") as f:
    f.write(text2)
