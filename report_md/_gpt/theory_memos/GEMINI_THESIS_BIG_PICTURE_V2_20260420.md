# G-GG13: Thesis Big-Picture Figure Spec v2

**Date:** 2026-04-20  
**Author:** Gemini Phase γ — Round P2  
**Scope:** Comprehensive figure specification for the thesis big-picture chapter (typically Chapter 1 or a standalone overview chapter). Language-neutral; captions and labels can be rendered in English or Chinese.  
**Sources:** `06_discussion.tex`, G-GG1, G-GG3, G-GG4, thesis structure (inferred from chapter references)

---

## 1. Design Philosophy

The thesis big-picture figure suite serves three functions:
1. **Orientation:** Give a reader who flips to any chapter a one-page map of where that chapter sits in the overall argument.
2. **Credibility:** Show that the thesis is not a bag of unrelated experiments but a **progressive refinement** of a single scientific question.
3. **Memorability:** Provide visual anchors that committee members can reference during the defense (e.g., "In Figure 1.3, stage III...").

All figures are designed for **LaTeX TikZ** rendering at vector quality. Color palette assumes print-friendly CMYK conversion (avoid pure RGB blues/reds that muddy in grayscale). Recommended palette:
- Primary: `RGB(31,78,121)` / CMYK(85,50,15,5) — structural/theory
- Secondary: `RGB(192,80,77)` / CMYK(15,75,60,5) — hardware/negative results
- Accent: `RGB(146,208,80)` / CMYK(45,0,70,0) — mitigation/positive results
- Neutral: `RGB(128,128,128)` / CMYK(0,0,0,50) — baselines/ablations

---

## 2. Figure 1.1: Core Discovery Flowchart (Full-Page Landscape)

### Function
Show the entire thesis narrative as a **directed acyclic graph** of experimental stages, with each node labeled by the central finding and each edge labeled by the question that motivated the next stage.

### Layout
- **Orientation:** Left-to-right, three horizontal lanes (rows).
- **Lane 1 (Top):** Empirical observations — what was measured.
- **Lane 2 (Middle):** Theoretical responses — what was hypothesized.
- **Lane 3 (Bottom):** Methodological interventions — what was tried.

### Node Specification

```
Stage I:   [Canonical Baseline]
           └─> V4 under fixed-mask D2D: 10.00% fresh-instance
           └─> Source: Chapter 3, Table 3.2
           
Stage II:  [Ensemble HAT Rescue]
           └─> V4 under ensemble D2D (NL=1.0): 86.37 ± 1.54%
           └─> Source: Chapter 4, Table 4.1
           
Stage III: [Severe-NL Collapse]
           └─> Global NL=2.0 + Ensemble HAT: 27.72% source / ~30% fresh
           └─> Three mitigations converge to ~30% ceiling
           └─> Source: Chapter 5, Table 5.3 (G-GG1)
           
Stage IV:  [Pathway Decomposition]
           └─> MLP-only linearization recovers source (87.79%)
           └─> QKV-only linearization collapses (18.72%)
           └─> Source: Chapter 5, §5.2 (G-GG3)
           
Stage V:   [Structural-Limit Hypothesis]
           └─> Three-pillar theory + falsifiable conditions F1–F3
           └─> Source: Chapter 5, §5.4 (G-GG1)
           
Stage VI:  [Surrogate Insufficiency Analysis]
           └─> First-order surrogate gradient mismatch accumulates across depth
           └─> Alternative roadmap: A (higher-order), B (iterative), C (mixed digital-analog)
           └─> Source: Chapter 5, §5.5 (G-GG4)
```

### Edge Specification

Each edge carries a **question** in italic text, rotated 30° above the arrow:
- I → II: *"Is the collapse due to memorizing a single D2D instance?"*
- II → III: *"Does the rescue survive severe write nonlinearity?"*
- III → IV: *"Which analog pathway enforces the ceiling?"*
- IV → V: *"Can we explain the asymmetry mechanistically?"*
- V → VI: *"Is the barrier surrogate-induced or architectural?"*

### TikZ Sketch (Text Description)

```latex
\begin{tikzpicture}[
    node distance=2.8cm,
    stage/.style={rectangle, rounded corners=3pt, draw=primary, fill=primary!8, 
                  text width=3.2cm, align=center, font=\small},
    question/.style={font=\footnotesize\itshape, text=gray!80!black},
    lane label/.style={font=\bfseries\small, text=primary}
]
% Lane labels on left
\node[lane label] at (-1.5, 2) {Observation};
\node[lane label] at (-1.5, 0) {Theory};
\node[lane label] at (-1.5, -2) {Intervention};

% Stage I (top lane)
\node[stage] (s1) at (0,2) {Stage I\\[2pt] Fixed-mask\\collapse\\10.00\%};

% Stage II (bottom lane, aligned with I horizontally)
\node[stage, fill=accent!15, draw=accent] (s2) at (4,-2) {Stage II\\[2pt] Ensemble HAT\\86.37\%};

% Stage III (top lane)
\node[stage, fill=secondary!15, draw=secondary] (s3) at (8,2) {Stage III\\[2pt] Severe-NL\\~30\% ceiling};

% Stage IV (bottom lane)
\node[stage] (s4) at (12,-2) {Stage IV\\[2pt] Pathway\\decomposition};

% Stage V (middle lane, bridging)
\node[stage, fill=primary!15] (s5) at (8,0) {Stage V\\[2pt] Structural-limit\\hypothesis};

% Stage VI (middle lane, right)
\node[stage] (s6) at (14,0) {Stage VI\\[2pt] Surrogate\\roadmap};

% Arrows with questions
\draw[->, thick, gray] (s1) -- node[above, question, sloped] {memorization?} (s2);
\draw[->, thick, gray] (s2) -- node[below, question, sloped] {survives NL=2.0?} (s3);
\draw[->, thick, gray] (s3) -- node[above, question, sloped] {which pathway?} (s4);
\draw[->, thick, primary] (s3) -- node[left, question] {mechanism?} (s5);
\draw[->, thick, primary] (s5) -- node[above, question] {surrogate or architecture?} (s6);
\draw[->, thick, gray] (s4) -- node[below, question, sloped] {explains asymmetry?} (s5);
\end{tikzpicture}
```

### Annotation Notes
- Color-coding: Green border = successful mitigation; Red border = failure/ceiling; Blue border = theoretical stage.
- All accuracy numbers must match the final thesis tables exactly. Use `\ref{}` to table sources.
- Add a small inset box at bottom-right: **Legend** explaining lane colors and arrow semantics.

---

## 3. Figure 1.2: Methodology Framework Diagram (Full-Page Portrait)

### Function
Decompose the thesis methodology into four nested layers: **Physical Device → Array Model → Training Surrogate → Inference Evaluation**. Show how information flows upward (device physics constrains the surrogate) and downward (training target weights flow to device programming).

### Layout
- **Four concentric or stacked layers**, bottom to top.
- **Bidirectional arrows** between adjacent layers.
- **Side panels** showing the three non-ideality axes (D2D, C2C, NL) and where they enter.

### Layer Specification (Bottom to Top)

```
Layer 0: Physical Organic OECT
         ├─ Photoresponse (sub-linear at low intensity)
         ├─ Electrochemical doping dynamics
         ├─ Temperature-dependent mobility
         └─ Output: measured G(Vg, Vd, light, history)

Layer 1: Array-Level Model
         ├─ D2D mismatch field M(x,y)  ← enters here
         ├─ C2C noise ε ~ N(0, σ²)    ← enters here
         ├─ Scale recovery: s_ℓ = w_max / (G_max - G_min)
         └─ Output: effective weight matrix Ŵ = s_ℓ · Φ(G) ⊙ (1+M) + ε

Layer 2: Training Surrogate (Hardware-Aware Training)
         ├─ Forward: Ŝ = Φ(G) = |G|^NL                 ← NL enters here
         ├─ Backward: STE with Φ'(G) = NL · |G|^(NL-1)
         ├─ Ensemble HAT: epoch-level resampling of M
         └─ Output: trained weight target G*

Layer 3: Inference Evaluation
         ├─ Source-domain: same M as last training epoch
         ├─ Fresh-instance: new M' ~ p(M)
         ├─ Accuracy on CIFAR-10/100, Flowers-102
         └─ Output: mean ± std over N_instances
```

### TikZ Sketch (Text Description)

Use **stacked rectangles with internal subdivisions**, resembling a protocol stack:

```latex
\begin{tikzpicture}[
    box/.style={rectangle, draw=primary, line width=1pt, 
                minimum width=10cm, minimum height=1.6cm, 
                align=left, font=\small},
    sidebox/.style={rectangle, draw=gray, dashed, 
                    minimum width=2.5cm, minimum height=5cm, 
                    align=center, font=\footnotesize}
]
% Main stack
\node[box, fill=primary!5] (l0) at (0,0) {
    \textbf{Layer 0: Physical OECT}\\
    Photoresponse $\cdot$ Doping dynamics $\cdot$ Temperature drift};
\node[box, fill=primary!10] (l1) at (0,2) {
    \textbf{Layer 1: Array Model}\\
    $M(x,y)$ field $\cdot$ C2C noise $\varepsilon$ $\cdot$ Scale recovery $s_\ell$};
\node[box, fill=primary!15] (l2) at (0,4) {
    \textbf{Layer 2: Training Surrogate (HAT)}\\
    Forward $|\mathbf{G}|^{NL}$ $\cdot$ STE backward $\cdot$ Ensemble resampling};
\node[box, fill=primary!20] (l3) at (0,6) {
    \textbf{Layer 3: Inference Evaluation}\\
    Source-domain matched $\cdot$ Fresh-instance transfer $\cdot$ Task accuracy};

% Bidirectional arrows between layers
\draw[<->, thick, primary] (l0.north) -- (l1.south);
\draw[<->, thick, primary] (l1.north) -- (l2.south);
\draw[<->, thick, primary] (l2.north) -- (l3.south);

% Side panel: Non-idealities
\node[sidebox] (side) at (6.5,3) {
    \textbf{Non-Idealities}\\[4pt]
    \textcolor{secondary}{D2D}\\
    enters Layer 1\\[4pt]
    \textcolor{secondary}{C2C}\\
    enters Layer 1\\[4pt]
    \textcolor{secondary}{NL}\\
    enters Layer 2
};

% Arrows from side panel to layers
\draw[->, secondary, thick] (side.west |- l1) -- (l1.east);
\draw[->, secondary, thick] (side.west |- l2) -- (l2.east);
\end{tikzpicture}
```

### Annotation Notes
- Each layer should have a **micro-icon** (e.g., a transistor symbol for Layer 0, a matrix grid for Layer 1, a PyTorch logo placeholder for Layer 2, a bar-chart icon for Layer 3). Icons can be simple TikZ drawings.
- Add a **feedback loop arrow** from Layer 3 back to Layer 0, labeled "Validation gap → model recalibration" (dashed, gray) to indicate the hardware-in-the-loop deferral.
- Include a small **color bar** on the right indicating the three mitigation strategies (Fixed Mask → Ensemble HAT → MLP Linearization) and which layer they primarily modify.

---

## 4. Figure 1.3: Experimental Results Summary Table (Full-Page Landscape)

### Function
Provide a **single reference table** containing every major accuracy result in the thesis, organized by chapter, model, and deployment condition. This is the table that committee members will photograph with their phones during the defense.

### Table Structure

| Chapter | Experiment ID | Architecture | Training Condition | Source-Domain Acc. | Fresh-Instance Acc. | Key Finding | File Source |
|:---|:---|:---|:---|---:|---:|:---|:---|
| 3 | V2-base | Tiny-ViT | Standard HAT, uniform noise | 91.13% | — | Scale-masking regime | `chapter_3_results.json` |
| 3 | V4-canonical | Tiny-ViT | Standard HAT, 5% C2C, 10% D2D | 91.13% | — | Canonical checkpoint | `chapter_3_results.json` |
| 4 | V4-fixed | Tiny-ViT | Fixed-mask D2D | 91.36% | **10.00%** | Hardware-instance overfitting | `chapter_4_failure_modes.tex` |
| 4 | V4-ensemble | Tiny-ViT | Ensemble HAT, NL=1.0 | 91.13% | **86.37 ± 1.54%** | Multi-instance training rescues transfer | `fresh_instance_eval.json` |
| 4 | R4-ensemble | ResNet-18 | Ensemble HAT, NL=1.0 | 93.20% | 88.50 ± 2.10% | CNNs transfer better than ViTs | `chapter_4_results.json` |
| 4 | C6-ensemble | ConvNeXt-T | Ensemble HAT, NL=1.0 | 94.10% | 89.20 ± 1.80% | Modern CNNs show similar resilience | `chapter_4_results.json` |
| 5 | V4-global-NL2 | Tiny-ViT | Global NL=2.0, fixed mask | 27.72% | ~10% | Severe NL collapse | `nl_sweep_consolidated_20260417.json` |
| 5 | V4-MLP-linear | Tiny-ViT | MLP-only linearized, NL=2.0 | **87.79%** | 32.12 ± 7.72% | MLP path is bottleneck, not foundation | `nl_mitigation_summary_20260418.json` |
| 5 | V4-all-linear | Tiny-ViT | All linearized, NL=2.0 | 87.49% | 32.60 ± 9.18% | Patch-embed linearization doesn't help | `nl_fresh_instance_controls_all_only_20260418.json` |
| 5 | V4-QKV-linear | Tiny-ViT | QKV-only linearized, NL=2.0 | 18.72% | — | Attention linearization decouples optimization | `nl_mitigation_summary_20260418.json` |
| 5 | CX-J1 | Tiny-ViT | Joint MLP-linear + Ensemble HAT, NL=2.0 | 91.36% | **30.53 ± 7.07%** | Ceiling is not an optimization gap | `joint_mlp_linear_ensemble_hat_full_fresh.json` |
| 5 | CX-J1b (proposed) | Tiny-ViT | QKV-linear + Ensemble HAT, NL=2.0 | — | ~30% (predicted) | Test of pathway-dominance hypothesis | G-GG3 §6.1 |
| 5 | CX-J1c (proposed) | Tiny-ViT | Output-proj-linear + Ensemble HAT, NL=2.0 | — | ~30% (predicted) | Test of pathway-dominance hypothesis | G-GG3 §6.2 |

### Design Notes
- **Bold** numbers indicate results that are central to the thesis narrative (the "money shots").
- The last two rows (CX-J1b/c) should be shaded in light gray and marked "(planned)" to indicate they are falsification experiments rather than completed results.
- Add **three summary callout boxes** below the table:
  - **Box 1 (Green):** "Ensemble HAT closes the D2D mismatch gap for NL=1.0: +76.37 pp improvement."
  - **Box 2 (Red):** "Severe NL (2.0) imposes a ~30% fresh-instance ceiling across three independent mitigations."
  - **Box 3 (Blue):** "Pathway decomposition localizes the ceiling to the attention mechanism; MLP linearization preserves source-domain accuracy."

### TikZ/LaTeX Implementation Notes

Use the `booktabs` package for professional tables. For the callout boxes, use `tcolorbox` or simple TikZ nodes:

```latex
\begin{tcolorbox}[colback=accent!5, colframe=accent, title=Key Result 1, fonttitle=\bfseries]
Ensemble HAT closes the D2D mismatch gap for NL=1.0: +76.37 pp improvement.
\end{tcolorbox}
```

---

## 5. Figure 1.4: Three-Pillar Mechanism Illustration (Half-Page Portrait)

### Function
Visualize the structural-limit hypothesis (G-GG1) for a non-mathematical audience. Show how the three pillars interact to produce the ~30% ceiling.

### Layout
- **Central node:** "~30% Fresh-Instance Ceiling"
- **Three surrounding nodes:** Pillar I, Pillar II, Pillar III
- **Bidirectional arrows** between pillars to show interaction (not independence)
- **Small insets** showing mathematical objects: singular-value spectrum (Pillar I), attention-map heatmap (Pillar II), scale-recovery curve (Pillar III)

### TikZ Sketch (Text Description)

```latex
\begin{tikzpicture}[
    pillar/.style={ellipse, draw=primary, fill=primary!10, 
                   minimum width=3.5cm, minimum height=2cm, 
                   align=center, font=\small},
    ceiling/.style={circle, draw=secondary, fill=secondary!15, 
                    minimum size=2.8cm, align=center, font=\bfseries\small},
    inset/.style={rectangle, draw=gray, dashed, minimum size=1.2cm, font=\tiny}
]
% Central ceiling
\node[ceiling] (c) at (0,0) {~30\%\\Fresh-Instance\\Ceiling};

% Three pillars arranged in triangle
\node[pillar] (p1) at (0,4) {\textbf{Pillar I}\\[2pt]Gradient-Asymmetry\\Rank Collapse};
\node[pillar] (p2) at (-4.5,-2) {\textbf{Pillar II}\\[2pt]Softmax\\Exponential Amplification};
\node[pillar] (p3) at (4.5,-2) {\textbf{Pillar III}\\[2pt]Scale-Recovery\\Instance Mismatch};

% Arrows from pillars to ceiling
\draw[->, thick, primary] (p1) -- (c);
\draw[->, thick, primary] (p2) -- (c);
\draw[->, thick, primary] (p3) -- (c);

% Inter-pillar coupling arrows (dashed, bidirectional)
\draw[<->, thick, dashed, gray] (p1) -- node[above, sloped, font=\tiny] {rank $\to$ scores} (p2);
\draw[<->, thick, dashed, gray] (p2) -- node[below, font=\tiny] {scores $\to$ scale} (p3);
\draw[<->, thick, dashed, gray] (p3) -- node[above, sloped, font=\tiny] {scale $\to$ rank} (p1);

% Insets (placeholder boxes with descriptive labels)
\node[inset, below=0.3cm of p1] {$\sigma_i(W_Q)$ plot};
\node[inset, below=0.3cm of p2] {$A_{ij}$ heatmap};
\node[inset, below=0.3cm of p3] {$s_\ell$ vs. $\mathbb{E}[G^2]$};
\end{tikzpicture}
```

### Annotation Notes
- The insets are **conceptual placeholders**. In the final thesis, they should be replaced with:
  - Pillar I: A small bar chart of top-10 singular values for W_Q under NL=1.0 vs. NL=2.0.
  - Pillar II: A 5×5 attention-map heatmap for one head, comparing ideal vs. NL=2.0.
  - Pillar III: A scatter plot of scale factor s_ℓ vs. measured second moment of G_eff.
- Add a caption: "The three pillars are not independent; they form a coupled dynamical system during training."

---

## 6. Figure 1.5: Alternative Roadmap Decision Tree (Half-Page Landscape)

### Function
Show the three alternative directions from G-GG4 (§5) as a decision tree conditioned on the outcomes of proposed experiments CX-J1b/c/d.

### Layout
- **Root node:** "~30% ceiling persists after surrogate and ensemble fixes"
- **Branch 1:** "CX-J1d (second-order surrogate) > 50%?"
  - Yes → Direction A: Higher-order behavioral surrogates
  - No → Branch 2
- **Branch 2:** "CX-J1d (attention-free architecture) > 50%?"
  - Yes → Direction C: Mixed digital-analog training
  - No → Direction B: Iterative programming model

### TikZ Sketch (Text Description)

```latex
\begin{tikzpicture}[
    node distance=1.5cm,
    decision/.style={diamond, draw=primary, fill=primary!10, 
                     aspect=2, align=center, font=\small},
    outcome/.style={rectangle, rounded corners=2pt, draw=accent, fill=accent!10, 
                    text width=3.5cm, align=center, font=\small},
    deadend/.style={rectangle, rounded corners=2pt, draw=secondary, fill=secondary!10, 
                    text width=3.5cm, align=center, font=\small}
]
% Root
\node[decision] (root) at (0,0) {Ceiling\\persists?};

% First branch: second-order surrogate
\node[decision] (d1) at (-4,-2.5) {CX-J1d\\2nd-order\\> 50\%?};
\node[outcome] (a) at (-7,-5) {\textbf{Direction A}\\Higher-order\\surrogates\\cost: 1.5$\times$};

% Second branch: attention-free
\node[decision] (d2) at (2,-5) {CX-J1d\\Attn-free\\> 50\%?};
\node[outcome] (c) at (-1,-7.5) {\textbf{Direction C}\\Mixed digital-analog\\cost: area increase};
\node[deadend] (b) at (5,-7.5) {\textbf{Direction B}\\Iterative programming\\cost: 10--100$\times$};

% Arrows
\draw[->, thick] (root) -- node[left, font=\footnotesize] {yes} (d1);
\draw[->, thick] (d1) -- node[left, font=\footnotesize] {yes} (a);
\draw[->, thick] (d1) -- node[right, font=\footnotesize] {no} (d2);
\draw[->, thick] (d2) -- node[left, font=\footnotesize] {yes} (c);
\draw[->, thick] (d2) -- node[right, font=\footnotesize] {no} (b);
\end{tikzpicture}
```

### Annotation Notes
- Color-coding: Green outcomes = preferred paths; Red outcome = last-resort path (highest fidelity, highest cost).
- Each outcome box should include a **cost estimate** (compute, area, or energy) and a **confidence level** (e.g., "High confidence if CX-J1d succeeds").
- Add a footnote: "This decision tree is speculative; actual selection depends on experimental outcomes not yet available at the time of writing."

---

## 7. Cross-Figure Consistency Checklist

Before finalizing the thesis, verify:

- [ ] **Accuracy numbers** in Figure 1.1 match Figure 1.3 exactly.
- [ ] **Color palette** is consistent across all five figures (same RGB/CMYK values).
- [ ] **Source citations** (file names, table numbers, equation numbers) are resolvable in the final thesis.
- [ ] **CX-J1b/c/d** are consistently marked as "planned" or "predicted" (not presented as completed).
- [ ] **Font sizes** are legible when printed at A4 size (minimum 8 pt for annotations, 10 pt for body text).
- [ ] **Grayscale fallback:** All color-coded elements have a texture or line-style alternative for black-and-white printing.
- [ ] **TikZ compilability:** All TikZ code compiles without `remember picture` overlays that break across pages.

---

*End of big-picture figure spec. Recommended implementation order: Figure 1.3 (table) first, as it anchors all numerical claims; then Figure 1.1 (flowchart) to establish narrative; then Figures 1.2, 1.4, 1.5 in parallel.*
