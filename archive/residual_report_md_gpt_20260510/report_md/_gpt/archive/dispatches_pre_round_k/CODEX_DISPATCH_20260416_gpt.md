# Codex Dispatch #2 — 2026-04-16

> **发布人**: Claude (项目负责人)
> **背景**: CX-1/CX-2/CX-3 全部完成。CX-4 CrossSim 数据质量不足，需要重做。新增 P3-1 Sobol。
> **GPU 状态**: 空闲

---

## 任务完成确认

| 任务 | 状态 | 说明 |
|:--|:--:|:--|
| CX-1 Contour Map | ✅ | 63/63 points, 审计通过 |
| CX-2 ConvNeXt ADC | ✅ | 5 bit-widths × 10 runs |
| CX-3 ResNet-18 Bug | ✅ | restore_weight_scale fix |
| CX-4 CrossSim | ⚠️ 需重做 | 见下方 |

---

## CX-4 REDO: CrossSim 对比 [HIGH — 重新定义]

### 问题诊断

上一轮结果不可用:
- 只用了 64 samples, 1 run
- Our framework: 54.69% (太少样本，variance 太大)
- CrossSim: 4.69% ≈ random (noise mapping 完全失效)
- 10K 样本的 run 在 CrossSim 转换阶段 crash/timeout (35min 无输出)

### 根本问题

CrossSim 处理 ConvNeXt-Tiny 59 层太慢 (~285s/64-samples)。全 test set 不现实 (~12h/run)。

### 新方案: 分层比较

**Phase 1: 无噪声基线** (验证权重转换路径)

```bash
cd /home/qiaosir/projects/compute_vit

/home/qiaosir/miniconda3/envs/LLM/bin/python run_crosssim_convnext.py \
  --sigma-c2c 0.0 --sigma-d2d 0.0 \
  --crosssim-alpha-noise 0.0 --crosssim-alpha-error 0.0 \
  --max-samples 1000 --runs 1 \
  --output report_md/_gpt/crosssim_clean_baseline.json \
  --log-file logs/_gpt/crosssim_clean.log \
  --num-workers 0 \
  2>&1 | tee -a logs/_gpt/crosssim_clean.log
```

**预期**: 两个框架都应该接近 89-90%。如果 CrossSim clean 也崩，说明权重转换有 bug，不是 noise mapping 的问题。

**Phase 2: 低噪声** (如果 Phase 1 通过)

```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python run_crosssim_convnext.py \
  --sigma-c2c 0.01 --sigma-d2d 0.01 \
  --crosssim-alpha-noise 0.01 --crosssim-alpha-error 0.01 \
  --max-samples 1000 --runs 3 \
  --output report_md/_gpt/crosssim_low_noise.json \
  --log-file logs/_gpt/crosssim_low_noise.log \
  --num-workers 0 \
  2>&1 | tee -a logs/_gpt/crosssim_low_noise.log
```

**Phase 3: 标准噪声** (如果 Phase 2 合理)

```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python run_crosssim_convnext.py \
  --sigma-c2c 0.05 --sigma-d2d 0.05 \
  --crosssim-alpha-noise 0.05 --crosssim-alpha-error 0.05 \
  --max-samples 1000 --runs 3 \
  --output report_md/_gpt/crosssim_standard_noise.json \
  --log-file logs/_gpt/crosssim_standard.log \
  --num-workers 0 \
  2>&1 | tee -a logs/_gpt/crosssim_standard.log
```

**如果 Phase 1 就崩了** (CrossSim clean ≠ 我们的 clean):
- 不要继续 Phase 2/3
- 记录 CrossSim clean accuracy 和 our framework clean accuracy
- 报告给 Claude — 这说明 `from_torch` 转换本身有问题，需要 debug 权重映射

### 交付

3 个 JSON files (或至少 Phase 1)。每个 accuracy != null。

---

## CX-5 NEW: Sobol 参数敏感度分析 [MED — CX-4 之后]

### 目的

论文需要量化 "D2D vs ADC 谁对精度影响更大"。用 Sobol first-order indices。

### 输入数据

已有完整 7×9 = 63 点 contour grid:
```
report_md/_gpt/iso_accuracy_contour_data.json
```

### 脚本

需要新写一个分析脚本。不需要 GPU，纯 Python 计算:

```python
#!/usr/bin/env python3
"""Sobol first-order sensitivity indices from contour sweep data."""

import json
import numpy as np
from pathlib import Path

DATA_PATH = "report_md/_gpt/iso_accuracy_contour_data.json"
OUTPUT_PATH = "report_md/_gpt/sobol_sensitivity.json"

def main():
    with open(DATA_PATH) as f:
        data = json.load(f)

    d2d_vals = sorted(set(r["d2d_pct"] for r in data))
    adc_vals = sorted(set(r["adc_bits"] for r in data))

    # Build mean accuracy matrix
    grid = np.zeros((len(d2d_vals), len(adc_vals)))
    for r in data:
        i = d2d_vals.index(r["d2d_pct"])
        j = adc_vals.index(r["adc_bits"])
        grid[i, j] = r["mean"]

    total_var = np.var(grid)

    # First-order: variance of conditional means
    # S_d2d: fix D2D, average over ADC
    mean_over_adc = grid.mean(axis=1)  # shape (7,)
    var_d2d = np.var(mean_over_adc)
    S_d2d = var_d2d / total_var

    # S_adc: fix ADC, average over D2D
    mean_over_d2d = grid.mean(axis=0)  # shape (9,)
    var_adc = np.var(mean_over_d2d)
    S_adc = var_adc / total_var

    # Also compute for the "operational" region only (6-bit+, D2D<=15%)
    mask_d2d = [i for i, d in enumerate(d2d_vals) if d <= 15]
    mask_adc = [j for j, a in enumerate(adc_vals) if a >= 6]
    sub = grid[np.ix_(mask_d2d, mask_adc)]
    sub_total_var = np.var(sub)

    sub_mean_adc = sub.mean(axis=1)
    sub_mean_d2d = sub.mean(axis=0)
    S_d2d_op = np.var(sub_mean_adc) / sub_total_var if sub_total_var > 0 else 0
    S_adc_op = np.var(sub_mean_d2d) / sub_total_var if sub_total_var > 0 else 0

    result = {
        "full_grid": {
            "total_variance": float(total_var),
            "S_d2d": float(S_d2d),
            "S_adc": float(S_adc),
            "S_interaction": float(1 - S_d2d - S_adc),
            "interpretation": "S_d2d + S_adc + S_interaction = 1.0"
        },
        "operational_region": {
            "filter": "D2D <= 15%, ADC >= 6-bit",
            "total_variance": float(sub_total_var),
            "S_d2d": float(S_d2d_op),
            "S_adc": float(S_adc_op),
            "S_interaction": float(1 - S_d2d_op - S_adc_op),
        },
        "conditional_means": {
            "d2d_values": d2d_vals,
            "mean_acc_by_d2d": [float(v) for v in mean_over_adc],
            "adc_values": adc_vals,
            "mean_acc_by_adc": [float(v) for v in mean_over_d2d],
        }
    }

    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Full grid: S_d2d={S_d2d:.3f}, S_adc={S_adc:.3f}, S_interaction={1-S_d2d-S_adc:.3f}")
    print(f"Operational: S_d2d={S_d2d_op:.3f}, S_adc={S_adc_op:.3f}")
    print(f"Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
```

**直接运行即可:**

```bash
cd /home/qiaosir/projects/compute_vit
/home/qiaosir/miniconda3/envs/LLM/bin/python -c "上面的脚本"
```

或者如果你想保存为文件再运行:

```bash
# 写入脚本
cat > run_sobol_analysis.py << 'SCRIPT_EOF'
(上面的完整脚本)
SCRIPT_EOF

# 运行
/home/qiaosir/miniconda3/envs/LLM/bin/python run_sobol_analysis.py
```

**交付**: `report_md/_gpt/sobol_sensitivity.json`

---

## 执行顺序

```
1. CX-4 Phase 1 (CrossSim clean baseline) — ~10-15min
2. CX-4 Phase 2/3 (如果 Phase 1 通过) — ~30min each
3. CX-5 Sobol analysis — ~10 秒, 无 GPU
```

---

## 关键文件路径

| 文件 | 用途 |
|:--|:--|
| `run_crosssim_convnext.py` | CX-4 CrossSim 脚本 (直接运行) |
| `report_md/_gpt/iso_accuracy_contour_data.json` | CX-1 完成数据 (Sobol 输入) |
| `report_md/_gpt/crosssim_comparison_results.json` | CX-4 旧输出 (不可用) |
| `checkpoints/C4_4bit_noise_HAT_best.pt` | ConvNeXt checkpoint |
| Python: `/home/qiaosir/miniconda3/envs/LLM/bin/python` | |

## 信任规则

1. accuracy != null
2. Phase 1 clean baseline 必须先通过 (>85%)
3. 如果 CrossSim clean 也崩 → 停止, 报告
4. 每个 phase 都 tee 到 logs/
5. 不填假数据

---

*Claude (项目负责人) — 2026-04-16*

---

## CX-6 NEW: 论文 Figure 生成 [HIGH — CX-4 完成后]

### 目的

用 contour 数据和 ADC 数据生成论文插图。Claude 统一审核。

### Fig 1: Contour Heatmap

输入: `report_md/_gpt/iso_accuracy_contour_data.json`
输出: `paper/latex_gpt/figures/fig_contour_map.pdf`

要求:
- matplotlib heatmap, X轴=ADC bits, Y轴=σ_D2D (%)
- 颜色: 蓝(低) → 红(高), 用 `RdYlBu_r` 或 `coolwarm`
- 在每个格子里标注 mean accuracy 值 (%.1f)
- 等高线叠加 (80%, 85%, 88%)
- 字体大小适合单栏论文 (~10pt)
- Title: 不要 title (论文图表用 caption)
- X label: "ADC Resolution (bits)"
- Y label: "σ_D2D (%)"
- Colorbar label: "Accuracy (%)"

```python
#!/usr/bin/env python3
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

with open('report_md/_gpt/iso_accuracy_contour_data.json') as f:
    data = json.load(f)

d2d_vals = sorted(set(r['d2d_pct'] for r in data))
adc_vals = sorted(set(r['adc_bits'] for r in data))

grid = np.zeros((len(d2d_vals), len(adc_vals)))
for r in data:
    i = d2d_vals.index(r['d2d_pct'])
    j = adc_vals.index(r['adc_bits'])
    grid[i, j] = r['mean']

fig, ax = plt.subplots(figsize=(8, 5))
norm = Normalize(vmin=10, vmax=90)
im = ax.imshow(grid, cmap='RdYlBu_r', norm=norm, aspect='auto', origin='lower')

# Annotate
for i in range(len(d2d_vals)):
    for j in range(len(adc_vals)):
        color = 'white' if grid[i,j] < 50 else 'black'
        ax.text(j, i, f'{grid[i,j]:.0f}', ha='center', va='center', fontsize=8, color=color)

# Contour overlay
cs = ax.contour(grid, levels=[80, 85, 88], colors='black', linewidths=0.8, origin='lower')
ax.clabel(cs, inline=True, fontsize=7, fmt='%.0f%%')

ax.set_xticks(range(len(adc_vals)))
ax.set_xticklabels(adc_vals)
ax.set_yticks(range(len(d2d_vals)))
ax.set_yticklabels([f'{d:.0f}' for d in d2d_vals])
ax.set_xlabel('ADC Resolution (bits)', fontsize=11)
ax.set_ylabel('σ_D2D (%)', fontsize=11)

cbar = fig.colorbar(im, ax=ax, shrink=0.85)
cbar.set_label('Accuracy (%)', fontsize=10)

plt.tight_layout()
plt.savefig('paper/latex_gpt/figures/fig_contour_map.pdf', dpi=300, bbox_inches='tight')
plt.savefig('paper/latex_gpt/figures/fig_contour_map.png', dpi=200, bbox_inches='tight')
print('Saved fig_contour_map.pdf and .png')
```

**运行:**
```bash
cd /home/qiaosir/projects/compute_vit
/home/qiaosir/miniconda3/envs/LLM/bin/python -c "上面的脚本"
```

### Fig 2: Sobol Bar Chart (可选)

如果时间允许，画一个简单的双组 bar chart:
- 左组: Full grid (S_adc=0.976, S_d2d=0.018)
- 右组: Operational region (S_d2d=0.922, S_adc=0.041)
- 输出: `paper/latex_gpt/figures/fig_sobol_sensitivity.pdf`

### 交付

- `paper/latex_gpt/figures/fig_contour_map.pdf`
- `paper/latex_gpt/figures/fig_contour_map.png` (预览用)
- (可选) `paper/latex_gpt/figures/fig_sobol_sensitivity.pdf`

---

*Claude (项目负责人) — 2026-04-16 追加*
