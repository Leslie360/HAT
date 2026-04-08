import re

with open("paper/05_results.md", "r") as f:
    md_text = f.read()

# Define the figure blocks
figs = {
    "fig4_accuracy_comparison": r"""\begin{figure}[t]
    \centering
    \includegraphics[width=0.85\textwidth]{fig4_accuracy_comparison}
    \caption{Cross-dataset accuracy comparison for ConvNeXt-Tiny and Tiny-ViT-5M across three complexity tiers (CIFAR-10, CIFAR-100, and Flowers-102). Tiny-ViT benefits from pre-training but exhibits higher noise sensitivity on complex tasks.}
    \label{fig:accuracy-comparison}
\end{figure}""",
    "fig5_hat_recovery": r"""\begin{figure}[t]
    \centering
    \includegraphics[width=0.85\textwidth]{fig5_hat_recovery}
    \caption{Degradation and recovery summary. Left: Accuracy drop from FP32 to standard noisy evaluation. Right: Recovery gained via Hardware-Aware Training (HAT). Absolute FP32 baselines are indicated to ensure transparency in low-performing regimes like Flowers-102.}
    \label{fig:hat-recovery}
\end{figure}""",
    "fig9_noise_sensitivity": r"""\begin{figure}[t]
    \centering
    \includegraphics[width=0.85\textwidth]{fig9_noise_sensitivity}
    \caption{Continuous noise sensitivity and ADC threshold analysis. The \(6\)-bit ADC knee is a dominant structural bottleneck for Transformer-based CIM architectures.}
    \label{fig:noise-sensitivity}
\end{figure}""",
    "fig7_retention_curve": r"""\begin{figure}[t]
    \centering
    \includegraphics[width=0.8\textwidth]{fig7_retention_curve}
    \caption{Retention decay for the corrected Tiny-ViT V4 model. The model exhibits a two-phase behavior: a rapid early drop followed by a stable plateau near 79\% accuracy extending out to \(10{,}000\) s.}
    \label{fig:retention-curve}
\end{figure}""",
    "fig10_zero_shot_transferability": r"""\begin{figure}[t]
    \centering
    \includegraphics[width=0.85\textwidth]{fig10_zero_shot_transferability}
    \caption{Zero-shot hardware transferability across different device profiles. Tiny-ViT exhibits severe instance overfitting, while ConvNeXt-Tiny maintains structural robustness across fresh D2D realizations.}
    \label{fig:zero-shot-transfer}
\end{figure}""",
    "fig6_physical_compensation": r"""\begin{figure}[t]
    \centering
    \includegraphics[width=0.8\textwidth]{fig6_physical_compensation}
    \caption{Impact of organic phototransistor non-linearity and dark current. Inverse-gamma compensation provides signal recovery in dark regimes but amplifies shot noise elsewhere.}
    \label{fig:frontend-compensation}
\end{figure}""",
    "fig11_energy_breakdown": r"""\begin{figure}[t]
    \centering
    \includegraphics[width=0.8\textwidth]{fig11_energy_breakdown}
    \caption{Inference energy breakdown for the Tiny-ViT hybrid architecture. Despite analog acceleration of linear layers, digital attention operations remain the dominant energy consumer.}
    \label{fig:energy-breakdown}
\end{figure}""",
    "fig8_pareto_energy_accuracy": r"""\begin{figure}[t]
    \centering
    \includegraphics[width=0.8\textwidth]{fig8_pareto_energy_accuracy}
    \caption{Pareto-style energy/accuracy summary across various hardware and training configurations.}
    \label{fig:pareto}
\end{figure}""",
    "fig_attention_maps": r"""\begin{figure}[t]
    \centering
    \includegraphics[width=0.9\textwidth]{fig_attention_maps}
    \caption{Qualitative attention map comparison across V1, V3, V4, and V6 configurations. HAT effectively restores the spatial attention patterns disrupted by hardware non-idealities.}
    \label{fig:attention-maps}
\end{figure}"""
}

# Markdown to LaTeX conversions
tex_text = md_text
tex_text = re.sub(r"^# 5\. Results\n+", r"\\section{Results}\n\\label{sec:results}\n\n", tex_text)
tex_text = re.sub(r"## 5\.1 Baseline Digital Performance", r"\\subsection{Baseline Digital Performance}\n\\label{subsec:baseline-digital}", tex_text)
tex_text = re.sub(r"## 5\.2 Quantization and the \"Scale Masking\" Effect", r"\\subsection{Quantization and the ``Scale Masking'' Effect}\n\\label{subsec:scale-masking}", tex_text)
tex_text = re.sub(r"## 5\.3 Task Complexity Scaling", r"\\subsection{Task Complexity Scaling}\n\\label{subsec:complexity-scaling}", tex_text)
tex_text = re.sub(r"## 5\.4 ADC and Quantization Thresholds", r"\\subsection{ADC and Quantization Thresholds}\n\\label{subsec:adc-thresholds}", tex_text)
tex_text = re.sub(r"## 5\.5 Retention and Temporal Drift", r"\\subsection{Retention and Temporal Drift}\n\\label{subsec:retention-drift}", tex_text)
tex_text = re.sub(r"## 5\.6 Hardware-Instance Transferability", r"\\subsection{Hardware-Instance Transferability}\n\\label{subsec:hardware-transferability}", tex_text)
tex_text = re.sub(r"## 5\.7 Physical Front-end Compensation", r"\\subsection{Physical Front-end Compensation}\n\\label{subsec:frontend-compensation}", tex_text)
tex_text = re.sub(r"## 5\.8 Physical Non-Idealities \(Tasks 23 & 24 Evaluation\)", r"\\subsection{Physical Non-Idealities}\n\\label{subsec:non-idealities}", tex_text)
tex_text = re.sub(r"## 5\.9 HAT Recovery under Physical Stress \(Tasks 34, 35 & 36\)", r"\\subsection{HAT Recovery under Physical Stress}\n\\label{subsec:hat-recovery-stress}", tex_text)
tex_text = re.sub(r"## 5\.10 Energy Efficiency Profile", r"\\subsection{Energy Efficiency Profile}\n\\label{subsec:energy-profile}", tex_text)
tex_text = re.sub(r"## 5\.11 Case Study: Zero-Shot Transfer to a Literature-Calibrated Device", r"\\subsection{Case Study: Zero-Shot Transfer to a Literature-Calibrated Device}\n\\label{subsec:case-study}", tex_text)

# Convert bold and italic
tex_text = re.sub(r"\*\*(.*?)\*\*", r"\\textbf{\1}", tex_text)
tex_text = re.sub(r"\*(.*?)\*", r"\\textit{\1}", tex_text)

# Fix percent signs and math
tex_text = re.sub(r"(\d+(?:\.\d+)?)\\%", r"\1\\%", tex_text)  # Make sure % is escaped, but don't double escape
tex_text = re.sub(r"(\d+(?:\.\d+)?)%", r"\1\\%", tex_text)
tex_text = tex_text.replace("QK^T", "\\(QK^{\\top}\\)")

# Handle lists
tex_text = re.sub(r"1\. \\textbf{(.*?)}:(.*?)\n", r"\\begin{enumerate}\n    \\item \\textbf{\1}:\2\n", tex_text, count=1)
tex_text = re.sub(r"2\. \\textbf{(.*?)}:(.*?)\n", r"    \\item \\textbf{\1}:\2\n", tex_text)
tex_text = re.sub(r"3\. \\textbf{(.*?)}:(.*?)\n\n", r"    \\item \\textbf{\1}:\2\n\\end{enumerate}\n\n", tex_text)

tex_text = re.sub(r"1\. \\textbf{(.*?)}: When a model(.*?)\n", r"\\begin{enumerate}\n    \\item \\textbf{\1}: When a model\2\n", tex_text, count=1)
tex_text = re.sub(r"2\. \\textbf{(.*?)}: Similarly,(.*?)\n\n", r"    \\item \\textbf{\1}: Similarly,\2\n\\end{enumerate}\n\n", tex_text)


# Table
table_md = """| Architecture | Dataset | FP32 Accuracy (\\%) |
|:--|:--|--:|
| ResNet-18 | CIFAR-10 | 94.98 |
| ConvNeXt-Tiny | CIFAR-10 | 90.74 |
| Tiny-ViT-5M | CIFAR-10 | 97.48 |
| ConvNeXt-Tiny | CIFAR-100 | 64.12 |
| Tiny-ViT-5M | CIFAR-100 | 86.94 |
| ConvNeXt-Tiny | Flowers-102 | 33.22 |
| Tiny-ViT-5M | Flowers-102 | 97.97 |"""

table_tex = r"""\begin{table}[h]
\centering
\caption{Baseline digital (FP32) performance across architectures and datasets.}
\label{tab:fp32-baselines}
\begin{tabular}{llc}
\toprule
\textbf{Architecture} & \textbf{Dataset} & \textbf{FP32 Accuracy (\%)} \\
\midrule
ResNet-18 & CIFAR-10 & 94.98 \\
ConvNeXt-Tiny & CIFAR-10 & 90.74 \\
Tiny-ViT-5M & CIFAR-10 & 97.48 \\
ConvNeXt-Tiny & CIFAR-100 & 64.12 \\
Tiny-ViT-5M & CIFAR-100 & 86.94 \\
ConvNeXt-Tiny & Flowers-102 & 33.22 \\
Tiny-ViT-5M & Flowers-102 & 97.97 \\
\bottomrule
\end{tabular}
\end{table}"""

tex_text = tex_text.replace(table_md, table_tex)

# Insert Figures
tex_text = tex_text.replace("\\label{subsec:complexity-scaling}\n\nFigures 4 and 5", "\\label{subsec:complexity-scaling}\n\n" + figs["fig4_accuracy_comparison"] + "\n\n" + figs["fig5_hat_recovery"] + "\n\nFigures~\\ref{fig:accuracy-comparison} and~\\ref{fig:hat-recovery}")
tex_text = tex_text.replace("\\label{subsec:adc-thresholds}\n\nThe ADC", "\\label{subsec:adc-thresholds}\n\n" + figs["fig9_noise_sensitivity"] + "\n\nThe ADC")
tex_text = tex_text.replace("\\label{subsec:retention-drift}\n\nFig. 7", "\\label{subsec:retention-drift}\n\n" + figs["fig7_retention_curve"] + "\n\nFig.~\\ref{fig:retention-curve}")
tex_text = tex_text.replace("\\label{subsec:hardware-transferability}\n\nExperiments", "\\label{subsec:hardware-transferability}\n\n" + figs["fig10_zero_shot_transferability"] + "\n\nExperiments")
tex_text = tex_text.replace("\\label{subsec:frontend-compensation}\n\nWe evaluate", "\\label{subsec:frontend-compensation}\n\n" + figs["fig6_physical_compensation"] + "\n\nWe evaluate")
tex_text = tex_text.replace("\\label{subsec:energy-profile}\n\nThe analytical", "\\label{subsec:energy-profile}\n\n" + figs["fig11_energy_breakdown"] + "\n\n" + figs["fig8_pareto_energy_accuracy"] + "\n\n" + figs["fig_attention_maps"] + "\n\nThe analytical")

with open("paper/latex_gpt/sections/05_results.tex", "w") as f:
    f.write(tex_text)

print("Updated 05_results.tex")
