# Codex 任务单 — 2026-04-11 09:30 (Claude 休眠前最终版)

> **Claude 即将休眠。以下任务按优先级排列，请依次执行。**
> **完成每个任务后在 `AGENT_SYNC_gpt.md` 末尾追加 `[Codex]` block。**

---

## 当前状态

- P13-full 正在运行（PID 145616，CPU-only analog fallback）
- CX4 (C4 三种子写入论文) ✅ 已完成
- Coverage: ✅45/104 (43%)

---

## CX1: P13-full 收尾 [⚡ 等进程结束]

P13 跑的是 AIHWKIT 全量 CIFAR-10（10K samples × 10 eval runs，CPU analog）。

**进程结束后要做的事：**

1. 如果进程 stdout 有输出，记录 digital accuracy / AIHWKIT mean±std / wall-clock
2. 如果 stdout 丢失（之前 tee 只捕获了 crash），重新跑一次并 tee：
   ```bash
   /home/qiaosir/miniconda3/envs/LLM/bin/python -u /home/qiaosir/projects/compute_vit/scripts/_gpt/aihwkit_shared_regime_benchmark_gpt.py \
     --device cuda --test-samples 0 --eval-runs 10 --batch-size 128 --train-samples 0 \
     2>&1 | tee logs/_gpt/p13_aihwkit_full_cifar10_gpu.log
   ```
3. 将结果写入：
   - `report_md/_gpt/P13_aihwkit_full_result.md`（reviewer-facing 表格）
   - `report_md/_gpt/json_gpt/p13_aihwkit_full_result.json`
4. 更新 `CLAUDE_TASK_gpt.md` Locked Numbers 中的 "AIHWKIT full" 行
5. 在 AGENT_SYNC 追加 `[Codex]` block

**预期结果格式：**

| Framework | Regime | Accuracy (full 10K) |
|:--|:--|:--|
| PyTorch digital | FP32 baseline | ~96.xx% |
| AIHWKIT | shared regime (CPU analog) | xx.xx ± x.xx% |

---

## CX2: P14-A Flowers-102 V2 Ablation [等 CX1 完成]

**目的：** V2 (σ→0, 仅量化无噪声) 作为 Flowers-102 的控制实验，对照已有 V3(4.81%) / V4(22.48%) / V1(97.97%)。

**执行：**
- 参考 `report_md/_gpt/P14_FLOWERS_ABLATION_PLAN_gpt.md` 中的详细命令
- 核心：Flowers-102 上 train + eval V2, seed=42
- 日志 tee 到 `logs/_gpt/p14_flowers_v2_ablation.log`

**交付：**
- V2 accuracy (eval mean ± std, 10-run)
- 写入 AGENT_SYNC

---

## CX3: P14-B CIFAR-10 Data Ablation [等 CX2 完成]

**目的：** 验证 "HAT data-floor hypothesis" — 小数据量下 HAT 是否也失效。Reviewer #12 明确要求。

**Step 1 — 检查/添加 CLI 参数：**
```python
# 在 train_tinyvit.py argparse 中加（如果还没有的话）：
parser.add_argument("--data-fraction", type=float, default=1.0,
                    help="Fraction of training data to use (0.0-1.0)")
# 在 dataset loading 处：
if args.data_fraction < 1.0:
    n = int(len(train_dataset) * args.data_fraction)
    train_dataset = torch.utils.data.Subset(train_dataset, range(n))
```

**Step 2 — 运行：**
```bash
for FRAC in 0.10 0.25 0.50 1.00; do
  /home/qiaosir/miniconda3/envs/LLM/bin/python -u /home/qiaosir/projects/compute_vit/train_tinyvit.py \
    --dataset cifar10 --seed 42 --batch-size 128 \
    --save-dir checkpoints/_gpt/p14_data_ablation/V4_frac${FRAC} \
    --mode train --experiments V4 --data-fraction $FRAC --epochs 100 --num-workers 0 \
    2>&1 | tee logs/_gpt/p14_data_ablation_V4_frac${FRAC}.log
done
```

**交付：**

| Data Fraction | V4 HAT Accuracy |
|:--:|:--:|
| 10% | ? |
| 25% | ? |
| 50% | ? |
| 100% | ? (should be ~87.95%) |

---

## 注意事项

- 所有 log 必须 tee 到 `logs/_gpt/` 下
- 不要同时跑多个 GPU 任务
- 如果遇到 OOM，减 batch-size 到 64
- 如果遇到 AIHWKIT CUDA 报错，继续用 CPU fallback
- Gemini 和 Kimi 也在并行工作，不要动他们的 .tex 文件（除了 CX4 已完成的改动）
