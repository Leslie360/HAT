import os
import subprocess

tex_content = r"""% fig2_weight_mapping.tex
\documentclass[tikz,border=12pt]{standalone}
\usepackage{amsmath}
\renewcommand{\familydefault}{\sfdefault}
\usepackage{tikz}
\usetikzlibrary{positioning,arrows.meta,shapes.geometric,fit,backgrounds,calc,decorations.pathreplacing}

% Professional, muted color palette (Nature/Science style)
\definecolor{lineColor}{RGB}{50,50,50}
\definecolor{boxBg}{RGB}{248,248,248}
\definecolor{accentBlue}{RGB}{0,114,178}
\definecolor{accentRed}{RGB}{213,94,0}

\begin{document}
\begin{tikzpicture}[
  scale=1.0, transform shape,
  font=\sffamily,
  stagebox/.style={draw=lineColor, fill=white, thick, rounded corners=4pt, inner sep=8pt, align=center, minimum width=2.8cm, minimum height=3.8cm},
  arrowstyle/.style={->, >=Stealth, line width=1.2pt, draw=lineColor},
  steplabel/.style={font=\normalsize\bfseries, text=lineColor},
  mathlabel/.style={font=\normalsize, text=lineColor},
]

\def\sx{1.2} % Horizontal spacing

% ================= ROW 1 (Left to Right) =================

% 1. Input
\node[stagebox] (S1) at (0, 0) {
  \textbf{Software Weight}\\[8pt]
  \begin{tikzpicture}[scale=0.45]
    \foreach \r in {0,1,2,3} {
      \foreach \c in {0,1,2,3} {
        \pgfmathsetmacro{\pct}{int(min(100, 30 + 15*\r + 12*\c))}
        \fill[black!\pct] (\c*0.7, -\r*0.7) rectangle + (0.6, 0.6);
      }
    }
  \end{tikzpicture}\\[8pt]
  \normalsize $W$ (FP32)
};
\node[steplabel, above=0.3cm] at (S1.north) {1. Input};

% 2. Quantize
\node[stagebox, right=\sx of S1] (S2) {
  \textbf{Quantization}\\[8pt]
  \begin{tikzpicture}[scale=0.45]
    \foreach \r in {0,1,2,3} {
      \foreach \c in {0,1,2,3} {
        \pgfmathsetmacro{\val}{int(2+1.5*\r+1.2*\c)}
        \pgfmathsetmacro{\pct}{int(100*min(1,\val/15))}
        \fill[black!\pct] (\c*0.7, -\r*0.7) rectangle + (0.6, 0.6);
      }
    }
  \end{tikzpicture}\\[8pt]
  \normalsize $W_q$ (4-bit)
};
\node[steplabel, above=0.3cm] at (S2.north) {2. Quantize};
\draw[arrowstyle] (S1.east) -- (S2.west) node[midway, above, mathlabel] {4-bit};

% 3. Map
\node[stagebox, right=\sx of S2] (S3) {
  \textbf{Diff.\ Pair}\\[8pt]
  \normalsize $G^+_{ij} = g_0 + \alpha q_{ij}$\\[4pt]
  \normalsize $G^-_{ij} = g_0 - \alpha q_{ij}$\\[8pt]
  \normalsize $G^+ \!- G^- \propto W_q$
};
\node[steplabel, above=0.3cm] at (S3.north) {3. Map};
\draw[arrowstyle] (S2.east) -- (S3.west) node[midway, above, mathlabel] {encode};

% 4. Noise
\node[stagebox, draw=accentRed, right=\sx of S3] (S4) {
  \textbf{Device Noise}\\[8pt]
  \normalsize $W_{\text{eff}} = W_q \!\cdot\! G$\\[4pt]
  \normalsize $\odot(1 \!+\! M_{\text{D2D}})$\\[4pt]
  \normalsize $+ \,\xi_{\text{C2C}}$\\[8pt]
  \textcolor{accentRed}{\normalsize $\sigma_{\text{D2D}}\!=\!0.10$}\\[2pt]
  \textcolor{accentRed}{\normalsize $\sigma_{\text{C2C}}\!=\!0.05$}
};
\node[steplabel, above=0.3cm] at (S4.north) {4. Noise};
\draw[arrowstyle] (S3.east) -- (S4.west) node[midway, above, mathlabel] {D2D+C2C};

% ================= ROW 2 (Right to Left) =================

% 5. Compute
\node[stagebox, below=2.5cm of S4] (S5) {
  \textbf{Analog MAC}\\[8pt]
  \normalsize $I_{\text{out}} = W_{\text{eff}} \cdot x$\\[8pt]
  \normalsize Crossbar\\[4pt]
  \textcolor{accentBlue}{\normalsize $\mathcal{O}(n^2)$ in $\mathcal{O}(1)$}
};
\node[steplabel, below=0.3cm] at (S5.south) {5. Compute};
\draw[arrowstyle] (S4.south) -- (S5.north) node[midway, right, mathlabel] {$V_{\text{in}}$};

% 6. Digitize
\node[stagebox, left=\sx of S5] (S6) {
  \textbf{ADC}\\[8pt]
  \normalsize $I_{\text{out}} \!\rightarrow\! d_{\text{out}}$\\[8pt]
  \normalsize 6-bit\\[4pt]
  \normalsize DNL $\approx$ 0.5 LSB
};
\node[steplabel, below=0.3cm] at (S6.south) {6. Digitize};
\draw[arrowstyle] (S5.west) -- (S6.east) node[midway, above, mathlabel] {$I_{\text{out}}$};

% 7. Recover
\node[stagebox, left=\sx of S6] (S7) {
  \textbf{Scale Recovery}\\[8pt]
  \normalsize $y = \frac{d_{\text{out}}}{G_{\text{ref}}} \cdot s$\\[8pt]
  \normalsize Calibrated\\[4pt]
  \normalsize Activation
};
\node[steplabel, below=0.3cm] at (S7.south) {7. Recover};
\draw[arrowstyle] (S6.west) -- (S7.east) node[midway, above, mathlabel] {$d_{\text{out}}$};

% 8. Output (Symmetry anchor)
\node[stagebox, draw=none, fill=none, left=\sx of S7] (S8) {
  \textbf{Output Activation}\\[8pt]
  \normalsize $y$\\[8pt]
  \normalsize (Digital Domain)
};
\node[steplabel, below=0.3cm, text=white] at (S8.south) {8. Output}; % Invisible alignment anchor
\draw[arrowstyle] (S7.west) -- (S8.east) node[midway, above, mathlabel] {$y$};

\end{tikzpicture}
\end{document}
"""
with open("figures/tikz/fig2_weight_mapping.tex", "w") as f:
    f.write(tex_content)

subprocess.run(["tectonic", "figures/tikz/fig2_weight_mapping.tex"])
