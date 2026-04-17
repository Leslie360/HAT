# GM-X35: Supplement-Only Insertion Drafts for Optional Experiments

以下 LaTeX 片段旨在将 GM-E1 (消融对照) 和 GM-E2 (纯数字对照) 的结果正式编入 Supplementary Information。

---

## 1. 针对 Ensemble HAT 的消融对比 (Ablation Study)
**插入点**: `supplementary.tex` 中关于 Ensemble HAT 的章节或 Table S1 附近。

```latex
\textit{Ablation Study: Ensemble HAT vs. i.i.d. Noise Augmentation.} 
To justify the structural necessity of Ensemble HAT, we conducted an ablation study using standard hardware-aware training (fixed D2D mask) and an i.i.d. noise-augmented control (resampling D2D per-forward pass). While generic i.i.d. noise-injection improves stochastic robustness, it fails to capture the fixed spatial correlation of crossbar mismatch. Our results show that standard V4 models collapse to ~10.00\% on fresh hardware instances, whereas Ensemble HAT consistently recovers $86.37 \pm 1.54\%$ accuracy across 10 unseen D2D realizations. This confirms that resampling the \textit{static} mismatch map each epoch is the critical mechanism for preventing hardware-instance overfitting.
```

---

## 2. 针对 6-bit ADC 悬崖的因果性分析 (ADC Control)
**插入点**: `supplementary.tex` 中 `fig:supp-noise-sensitivity` (Fig S5) 的说明文字处。

```latex
\textit{Pure Digital Control.} 
A pure-digital ADC sweep (no analog noise) was performed to isolate the impact of quantization from physical stochasticity. While a digital 4-bit ADC penalty exists (44.96\% accuracy), the introduction of analog noise exacerbates this cliff, dropping performance to ~27\%. This demonstrates a non-linear coupling between ADC quantization and analog noise, confirming that 6-bit resolution is a fundamental requirement for maintaining Transformer decision boundaries in mixed-signal CIM architectures.
```

---

## 3. 参数风险矩阵 (Parameter Risk Matrix - 引用 GM-X24)
**插入点**: `supplementary.tex` 的末尾，新增一个 Subsection。

*(内容即为 `PARAMETER_RISK_MATRIX_gpt.md` 的翻译版本)*
