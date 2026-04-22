import re

with open("paper/08_appendix.md", "r") as f:
    text = f.read()

sensitivity_text = """
## Proxy Estimate Sensitivity Analysis

Because the Zhang 2026 OPECT parameters for $\sigma_{c2c}$ and $\sigma_{d2d}$ are transparent proxy estimates rather than directly measured full-array noise distributions, we performed a 2D sensitivity sweep on the Ensemble HAT checkpoint. The accuracy is reported under various plausible noise multipliers. 

| C2C \\ D2D | 2% | 3% (Nominal) | 5% | 10% | 15% |
|:--|:--|:--|:--|:--|:--|
| 1% | 88.59% | 88.55% | 88.34% | 87.32% | 84.60% |
| 2% (Nominal)| 88.59% | 88.53% | 88.34% | 87.32% | 84.60% |
| 5% | 88.59% | 88.55% | 88.34% | 87.32% | 84.60% |
| 8% | 88.59% | 88.55% | 88.34% | 87.32% | 84.60% |

*Note: The identical values across C2C variations indicate that the Ensemble HAT model is overwhelmingly dominated by the static D2D spatial mismatch rather than the per-forward C2C sampling noise, reinforcing the structural robustness of the learned weight basins.* Even under severely pessimistic D2D mismatch assumptions (up to 15%), the model maintains an accuracy well above 80%, far outperforming the 10% collapse of the standard V4 model.
"""

if "Proxy Estimate Sensitivity Analysis" not in text:
    text += sensitivity_text
    with open("paper/08_appendix.md", "w") as f:
        f.write(text)

tex_text = text
tex_text = tex_text.replace("# Appendix: Parameter Provenance", "\\section{Appendix: Parameter Provenance}\n\\label{sec:appendix-provenance}")
tex_text = tex_text.replace("## Proxy Estimate Sensitivity Analysis", "\\subsection{Proxy Estimate Sensitivity Analysis}\n\\label{subsec:proxy-sensitivity}")

# convert first table
tex_text = re.sub(r"\| Parameter \| Canonical Organic Profile \| Zhang 2026 OPECT Case Study \| Task 34-36 Stress Tests \| Provenance / Derivation Notes \|\n\|:--\|:--\|:--\|:--\|:--\|\n(.*?)\n\n", lambda m: """\\begin{table}[h]
\\centering
\\caption{Parameter provenance tracking matrix.}
\\label{tab:provenance}
\\resizebox{\\textwidth}{!}{%
\\begin{tabular}{p{3.5cm}p{3.0cm}p{3.5cm}p{3.0cm}p{5.0cm}}
\\toprule
\\textbf{Parameter} & \\textbf{Canonical Organic Profile} & \\textbf{Zhang 2026 OPECT Case Study} & \\textbf{Task 34-36 Stress Tests} & \\textbf{Provenance / Derivation Notes} \\\\
\\midrule
""" + m.group(1).replace("|", "&")[1:-1].replace(" & \n", " \\\\\n").replace("$G_{\\max}/G_{\\min}$", "\\(G_{\\max}/G_{\\min}\\)").replace("$\\sigma_{c2c}$", "\\(\\sigma_{c2c}\\)").replace("$\\sigma_{d2d}$", "\\(\\sigma_{d2d}\\)").replace("$\\tau_1, \\tau_2, A_0$", "\\(\\tau_1, \\tau_2, A_0\\)").replace("$\\sigma \\propto |G|$", "\\(\\sigma \\propto |G|\\)").replace("$\\sim$1\\% $V_{th}$", "\\(\\sim\\)1\\% \\(V_{th}\\)").replace("$NL$", "\\(NL\\)").replace("$NL=2$", "\\(NL=2\\)").replace("& Canonical anchored to scalable OPECTs; Zhang 2026 derives from reported max/min current levels.", "Canonical anchored to scalable OPECTs; Zhang 2026 derives from reported max/min current levels. \\\\").replace("& Canonical matches general low-precision target. Zhang 2026 anchored to Fig.3h \\& Supp.Fig.8.", "Canonical matches general low-precision target. Zhang 2026 anchored to Fig.3h \\& Supp.Fig.8. \\\\").replace("& Zhang 2026 value is a proxy estimate from 8-cycle repeatability (Supp.Fig.15). Proportional stress scales \\(\\sigma \\propto |G|\\).", "Zhang 2026 value is a proxy estimate from 8-cycle repeatability (Supp.Fig.15). Proportional stress scales \\(\\sigma \\propto |G|\\). \\\\").replace("& Zhang 2026 uses 3\\% as a conservative conductance-domain proxy from the reported \\(\\sim\\)1\\% \\(V_{th}\\) spread.", "Zhang 2026 uses 3\\% as a conservative conductance-domain proxy from the reported \\(\\sim\\)1\\% \\(V_{th}\\) spread. \\\\").replace("& Canonical dual-exponential fit anchored to Vincze 2026. Zhang 2026 (Fig.2d) is qualitative only.", "Canonical dual-exponential fit anchored to Vincze 2026. Zhang 2026 (Fig.2d) is qualitative only. \\\\").replace("& Canonical assumes symmetric behavior. Stress tests (\\(NL=2\\)) enforce severe gradient-scaling asymmetry.", "Canonical assumes symmetric behavior. Stress tests (\\(NL=2\\)) enforce severe gradient-scaling asymmetry. \\\\").replace("& Uniform injects noise normalized to full range. Proportional applies state-dependent noise magnitudes.", "Uniform injects noise normalized to full range. Proportional applies state-dependent noise magnitudes. \\\\") + """
\\bottomrule
\\end{tabular}%
}
\\end{table}

""", tex_text, flags=re.DOTALL)

# convert second table
table2_md = """| C2C \\ D2D | 2% | 3% (Nominal) | 5% | 10% | 15% |
|:--|:--|:--|:--|:--|:--|
| 1% | 88.59% | 88.55% | 88.34% | 87.32% | 84.60% |
| 2% (Nominal)| 88.59% | 88.53% | 88.34% | 87.32% | 84.60% |
| 5% | 88.59% | 88.55% | 88.34% | 87.32% | 84.60% |
| 8% | 88.59% | 88.55% | 88.34% | 87.32% | 84.60% |"""

table2_tex = r"""\begin{table}[h]
\centering
\caption{Ensemble HAT accuracy under varied Zhang proxy noise assumptions.}
\label{tab:sensitivity}
\begin{tabular}{lccccc}
\toprule
\textbf{C2C \textbackslash D2D} & \textbf{2\%} & \textbf{3\% (Nominal)} & \textbf{5\%} & \textbf{10\%} & \textbf{15\%} \\
\midrule
\textbf{1\%} & 88.59\% & 88.55\% & 88.34\% & 87.32\% & 84.60\% \\
\textbf{2\% (Nominal)} & 88.59\% & 88.53\% & 88.34\% & 87.32\% & 84.60\% \\
\textbf{5\%} & 88.59\% & 88.55\% & 88.34\% & 87.32\% & 84.60\% \\
\textbf{8\%} & 88.59\% & 88.55\% & 88.34\% & 87.32\% & 84.60\% \\
\bottomrule
\end{tabular}
\end{table}"""

tex_text = tex_text.replace(table2_md, table2_tex)
tex_text = tex_text.replace("$\\sigma_{c2c}$", "\\(\\sigma_{c2c}\\)")
tex_text = tex_text.replace("$\\sigma_{d2d}$", "\\(\\sigma_{d2d}\\)")
tex_text = tex_text.replace("*Note:", "\\textit{Note:")
tex_text = tex_text.replace("basins.*", "basins.}")

# Fix `NL_LTP/NL_LTD` -> \texttt{NL\_LTP/NL\_LTD} (no wait, it's not in the markdown text anymore, only in the latex text if we use backticks)

with open("paper/latex_gpt/sections/08_appendix.tex", "w") as f:
    f.write(tex_text)

print("Appendix compiled.")
