# Gemini 独立审阅意见 — R11D PCM 架构及脚本安全性 (2026-04-28)

我已经完成了对 Claude 自查报告以及相关代码的全面审查。关于您提出的 4 个核心问题，以下是我的详细解答和风险评估：

## 1. 🔴 `_resolve_pcm_preset(preferred)` 逻辑是否存在第三个 hidden bug？

**结论：是的，存在致命的逻辑缺陷（Hidden Bug #3）。**

这个函数的重构存在三个非常危险的问题：

1. **同名 Preset 遮蔽问题：**
   `PCM_PRESET_REGISTRY` 中包含两个名为 `PCMPresetDevice` 的条目（一个在 `presets` 模块，一个在 `presets.devices` 模块）。`if item[1] == preferred` 的逻辑遇到第一个匹配项就会 `break`。如果用户传入 `"PCMPresetDevice"`，但实际能 work 的是第二个模块路径，系统会把第一个提到队首，如果第一个 import 失败，**它接着会尝试原本在第二位的 `PCMPresetUnitCell`，并且如果成功了，它就会静默返回 `PCMPresetUnitCell`，而用户以为自己跑的是 `PCMPresetDevice`！** 这是极度危险的静默降级。
2. **无效输入静默降级（Silent Fallback）：**
   如果传入了一个不存在的 preset 名称（比如拼写错误 `"PCMPresetDev"`），`preferred_tuple` 将为 `None`。代码不会报错，而是直接按原始 registry 顺序尝试并成功加载默认的 `PCMPresetUnitCell`。这违背了“Fail Fast”原则。
3. **未修改前的表现一致性：**
   如果 `preferred=None`，逻辑确实可以回退到原始行为，但在加入了显式参数的环境中，不严格校验输入会导致极其严重的实验交叉污染。

**修复建议：** 必须强制报错。如果指定了 `preferred`，只能从指定的或者匹配的 preset 中加载，如果全都加载失败，必须抛出 `RuntimeError`，绝不能 fallback 到其他预设。

## 2. 🔴 `--early-stop-patience 0` 是否与原始实验一致？

**结论：完全一致。**

我通过直接读取原始 R11D-5a checkpoint 的 `training_history.json` 文件（`r11d_5a_pcm/training_history.json`），提取了当时的运行参数：
```json
{
  "epochs": 100,
  "early_stop_patience": 0,
  "early_stop_min_delta": 0.0
}
```
并且该实验确实跑满了 100 epoch。因此，Claude 在 v2 multi-seed 脚本中显式设置 `--early-stop-patience 0` 是完全正确且安全的，完美复现了当时的超参。

## 3. 🟡 T1-3 preset 对比设计是否足够严谨？

**结论：不够严谨，存在结构性风险。**

1. **单 Seed 风险：** T1-3 的目的是为了证明“PCM 物理拯救 4-bit”不是某个特定 preset 的偶然产物。只用 seed=42 进行比较虽然可以做到 Head-to-Head，但万一恰好在这个 seed 下 `PCMPresetDevice` 表现不佳，结论会被推翻。建议至少追加一个不同 seed 进行验证。
2. **Device vs UnitCell 的物理差异：**
   `PCMPresetDevice` 只模拟纯粹的相变存储器器件特性（如结晶/非晶化不对称性）；而 `PCMPresetUnitCell` 模拟的是**整个阵列单元**，包含了外围电路（晶体管/寄生电容电阻等）。这种物理层面的差异可能会极大影响梯度的传递和漂移特性。如果这二者表现有显著差异，将会成为论文的一个核心讨论点，而非简单的“选型不敏感”。

## 4. 🟡 在原文件上修改 `r11d4_train_pcm.py` 是否安全？

**结论：不安全，破坏了实验数据溯源（Provenance）。**

从 `r11d4_train_pcm.py` 的代码可以看到，它在每次运行时都会记录 provenance，其中包括文件的 SHA256 哈希值：
```python
"code_sha256": sha256_file(__file__)
```
Claude 在原文件上直接添加 `--pcm-preset` 参数，改变了文件的 Hash 值。虽然逻辑上对默认运行（preferred=None）是兼容的，但从严谨的学术审计角度来看，这意味着新的验证实验跑出的 provenance log 里的 checksum 将与原始 R11D-5a 彻底不一致。Reviewer 若索要原始代码审计，你将难以证明“两批实验完全基于同一套未经修改的代码”。

**建议操作：**
1. 立刻通过 Git `checkout` / `restore` 将 `r11d4_train_pcm.py` 恢复到未修改前的状态，锁定基线脚本的 Hash。
2. 复制出一个 `r11d4_train_pcm_v2.py` 或 `r11d_train_pcm_extended.py` 专门用于 T1-3 等新的消融实验，并在其中应用严谨的 preset 加载（禁用静默降级）。

---

**最终建议：**
Claude 的这次自检非常有价值，但由于对 Python 列表过滤和机器学习框架 Provenance 机制的理解不够深，引入了新的地雷。在恢复原文件后，我们可以立即着手推进 Progressive Quantization 和 T1-3（使用安全的复刻脚本），确保主线实验稳固。如果您同意，我可以为您生成修改后安全的 `v2` 脚本。
