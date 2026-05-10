# Remote Evidence Package Spec

日期：2026-04-22
用途：规范远端每次回传的最小证据包，保证本地可以核对、留存、决定是否正式复现。

## 原则
远端当前定位是：
- **exploration engine**（探索引擎）
- 不是 paper-grade authoritative evidence machine

因此，远端不需要回传大权重文件，但必须回传**足够让本地判断可信度和复现价值的证据**。

## 必须回传的内容
每个实验至少回传下面 8 类信息。

### 1. 实验身份信息
- experiment name
- branch / commit hash
- launch date
- operator / agent name
- machine info（4xA100 / driver / CUDA / PyTorch）

### 2. 完整命令
必须逐字给出实际运行命令。
不要只写“same as before”。

至少包括：
- model / experiment id
- protected group
- surrogate order
- `delta_g_eff`
- `alpha`
- `resample_interval`
- batch size
- epochs
- num_workers
- amp / tf32
- warm-start checkpoint path
- fresh-eval protocol

### 3. 代码差异
如果改了代码，必须回：
- 受影响文件路径
- 最小 diff 片段
- 一句话解释为什么改

不要只写“fixed conv bug”或“optimized dataloader”。

### 4. Source-domain 结果
至少回：
- epoch 0 train acc
- epoch 0 test acc
- best source-domain acc
- best epoch
- final source-domain acc

如果是 no-train parity probe，也要明确写：
- no-train source eval = xx%

### 5. Fresh-instance 结果
至少回：
- number of fresh instances
- eval runs per instance
- fresh mean ± std
- peak instance
- 每个 instance 的 mean 列表

推荐表格格式：

| instance | mean_acc |
|---|---:|
| 1 | ... |
| 2 | ... |

### 6. Parity 核对项
如果实验声称和本地 parity，必须额外回：
- baseline checkpoint md5/sha256
- protected analog module count
- 前 10 个 module 名称
- `delta_g_eff` 的 auto-fill 语义
- DataLoader 配置：
  - num_workers
  - persistent_workers
  - pin_memory
- resize 路径：CPU 还是 GPU

### 7. 训练曲线/关键点
不要求大图，但必须至少回其中一种：
- markdown 表格
- csv 小表

最少要有：
- epoch 0
- epoch 4 or 5
- epoch 9 or 10
- best epoch
- final epoch

### 8. 结论标签
每个实验必须给一个明确 verdict：
- `worth local reproduction`
- `not worth local reproduction`
- `parity unresolved`
- `exploration only`

## 推荐附加内容
如果方便，再附：
- per-epoch source curve csv
- per-instance fresh csv
- runtime summary
- GPU memory / throughput summary

## 不要求回传的内容
当前阶段默认**不要**回传：
- 大 checkpoint
- 完整日志包
- 大型 tensor dump
- 原始数据集

除非本地明确要求。

## 命名建议
远端每次回传建议至少给两份 markdown：
1. `REMOTE_<tag>_RESULTS.md`
2. `REMOTE_<tag>_EVIDENCE.md`

其中：
- `RESULTS` 放结果表和结论
- `EVIDENCE` 放命令、diff、parity 核对项、per-instance 明细

## 本地使用规则
本地收到远端结果后，按三档处理：
1. **authoritative-ready**
   - 命令、配置、per-instance、parity 核对齐全
2. **memo-level only**
   - 只有摘要，没有原始支撑
3. **exploration hint**
   - 只有方向信息，不能直接引用

如果缺少：
- exact command
- per-instance 明细
- code diff
- parity md5
则默认降级为 `memo-level only`。

## 一句话要求
远端不要只回“最好结果是多少”，必须回“这个结果是怎么来的、是否真和本地同实验、值不值得本地正式复现”。
