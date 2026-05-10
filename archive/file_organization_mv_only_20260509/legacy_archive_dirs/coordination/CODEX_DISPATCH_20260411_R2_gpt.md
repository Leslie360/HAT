# Codex 任务单 — Round 2 (2026-04-11, Claude 审阅后)

> **上一轮 P13-full 进程已死，结果丢失。本轮最高优先级：重跑 P13。**

---

## CX-R1: P13-full 重跑 [⚡ IMMEDIATE]

上一轮 PID 145616 已不在运行，结果文件仍是旧的 256-sample 数据。需要重新运行全量。

**确保 tee 捕获输出：**
```bash
nohup /home/qiaosir/miniconda3/envs/LLM/bin/python -u /home/qiaosir/projects/compute_vit/scripts/_gpt/aihwkit_shared_regime_benchmark_gpt.py \
  --device cuda --test-samples 0 --eval-runs 10 --batch-size 128 --train-samples 0 \
  2>&1 | tee logs/_gpt/p13_aihwkit_full_cifar10_gpu_r2.log &
```

**注意事项：**
- 上次问题是 AIHWKIT 无 CUDA tiles → CPU fallback 很慢（10K×10 在 CPU 上可能需要 1-2 小时）
- 确认脚本已有 CPU fallback patch（上轮 Codex 已修补）
- 如果预计超过 2 小时，考虑减 eval-runs 到 5

**完成后：**
1. 运行 finalizer: `python scripts/_gpt/finalize_p13_aihwkit_full_result_gpt.py`
2. 确认 `report_md/_gpt/P13_aihwkit_full_result.md` 和 JSON 已更新
3. 更新 `CLAUDE_TASK_gpt.md` Locked Numbers
4. AGENT_SYNC 追加 `[Codex]` block

---

## CX-R2: P14-A Flowers-102 V2 [等 P13]

队列脚本已就绪: `scripts/_gpt/run_post_p13_ablation_queue_gpt.sh`

P13 完成后直接运行：
```bash
bash scripts/_gpt/run_post_p13_ablation_queue_gpt.sh 2>&1 | tee logs/_gpt/p14_queue.log
```

**交付：** Flowers V2 accuracy + 数据消融 4 个 fraction

---

## CX-R3: 论文 label 检查 [非 GPU，可并行]

Gemini 大幅重构了 §4/§5/§6 + Supplementary。请检查：
1. `\ref{...}` 是否全部解析（编译 main.tex 看有无 `??`）
2. Figure 编号连续性（Kimi KM7 报告过乱序问题）
3. Supplementary 交叉引用是否正确

```bash
cd /home/qiaosir/projects/compute_vit/paper/latex_gpt && pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex && grep -c "??" main.log
```

---

## 不要做的事

- 不要碰 Gemini 负责的 .tex 文件（§2/§4/supplementary）
- 不要重复做已完成的 CX4
- 不要自行决定 title 修改