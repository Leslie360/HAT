# Supplementary Table Scaffold: Group-Wise Nonlinearity Ablation

**Target location:** Supplementary Information, new section SX.N (after retention / ADC sections)
**Status:** Updated through the stopped-at-ep54 attn-proj collapse snapshot.
**Framing:** CLAUDE-A Option B (supplementary ablation, not main-paper contribution).

---

## Table SX.N: Group-wise linearization ablation under global NL=2.0 (Tiny-ViT V4, CIFAR-10)

| Variant | Protected group | Global NL | Best test acc | Δ vs NL=2.0 baseline | Epoch | Notes |
|:--|:--|:--:|:--:|:--:|:--:|:--|
| (a) NL=1.0 global | — | 1.0 | **91.94%** | +64.22 pp | — | Upper bound (no nonlinearity) |
| (b) NL=2.0 global (baseline) | — | 2.0 | **27.72 ± 0.82%** | — | — | Unmitigated severe nonlinearity |
| (c) MLP-only linear | fc1, fc2 | 2.0 | **87.79%** | **+60.07 pp** | 73 | Primary recovery path |
| (d) QKV-only linear | attn.qkv | 2.0 | **18.72%** | **−9.00 pp** | 2 | Structural failure — attention nonlinearity is required |
| (e) attn_proj-only linear | attn.proj | 2.0 | **18.86%** | **−8.86 pp** | 0 | ✅ Stopped at ep54 after sustained collapse; final acc \(\sim\)10.25% |
| (f) all-linear | all analog linear | 2.0 | **87.49%** | **+59.77 pp** | 59 | ✅ Complete (final 84.81%) |

---

## Narrative paragraph (to place below table)

> The group-wise ablation isolates the MLP channel-mixing path as the dominant recoverable failure site under the present NL=2.0 gradient-scaling surrogate. Linearizing only the MLP layers (fc1, fc2) recovers 87.79% test accuracy — within ~4 pp of the NL=1.0 upper bound — whereas linearizing either attention-side linear operator degrades to near-chance performance (QKV 18.72%, attention projection 18.86% best and \(\sim\)10.25% by ep54). This dual collapse indicates that the attention nonlinearity is structurally required for representation learning, while the MLP nonlinearity can be approximated or compensated in situ. The all-linear result remains MLP-dominated rather than materially exceeding the MLP-only rescue.

---

## .tex stub (for `supplementary_main.tex` or a new `sections/sx_nl_ablation.tex`)

```latex
\subsection{Group-wise nonlinearity ablation}\label{sec:nl-ablation}

Table~\ref{tab:nl-ablation} decomposes the severe-NL failure mode by
protecting individual analog-layer groups under a fixed global
$\mathrm{NL}=2.0$ gradient-scaling surrogate.

\begin{table}[htbp]
\centering
\caption{Group-wise linearization ablation under global $\mathrm{NL}=2.0$
(Tiny-ViT V4, CIFAR-10).}
\label{tab:nl-ablation}
\begin{tabular}{@{}clcccl@{}}
\toprule
Row & Protected group & Global NL & Best test acc & $\Delta$ vs baseline & Epoch \\
\midrule
(a) & --- (NL=1.0 upper bound) & 1.0 & 91.94\% & +64.22 pp & --- \\
(b) & --- (baseline) & 2.0 & 27.72$\pm$0.82\% & --- & --- \\
(c) & MLP (fc1, fc2) & 2.0 & 87.79\% & +60.07 pp & 73 \\
(d) & QKV projection & 2.0 & 18.72\% & $-$9.00 pp & 2 \\
(e) & attn\_proj & 2.0 & 18.86\% & $-$8.86 pp & 0 \\
(f) & all linear layers & 2.0 & 87.49\% & +59.77 pp & 59 \\
\bottomrule
\end{tabular}
\end{table}

The MLP-only result (row~c) isolates the channel-mixing nonlinearity as the
dominant recoverable bottleneck: linearizing only the MLP layers recovers
$\sim$60~percentage points, placing the model within $\sim$4~pp of the
$\mathrm{NL}=1.0$ upper bound. In contrast, both attention-side linearizations
(rows~d and~e) degrade below the unmitigated baseline, indicating that the
attention nonlinearity is structurally required and cannot be simply removed.
```

---

## Action items

1. **Optional clean-up:** replace this scaffold with the fully compiled `supplementary.tex` table if the manuscript becomes the sole source of truth.
2. **Add 3-seed error bars** for rows (c) and (d) if time permits (thesis defense).
3. **Compile `supplementary_main.tex`** with the final table and verify page count.
