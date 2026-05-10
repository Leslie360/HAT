# Draft: Training Hyperparameters Paragraph for §3 Methodology

## Suggested Insertion Location

**File:** `paper/latex_gpt/sections/03_methodology.tex`
**Position:** After \subsection{Hardware-Aware Training} (currently ends around line 101) and before \subsection{Physical Frontend Compensation} (starts at line 103).
**Form:** Insert as a new subsection `\subsection{Training Protocol}` (or as a `\subsubsection{Training hyperparameters}` inside `\subsection{Hardware-Aware Training}` if space is tight).

**Surrounding text for context:**
```latex
Inference under variability is evaluated by Monte Carlo sampling. For a fixed checkpoint, the model is run repeatedly with fresh C2C draws, and accuracy is reported as mean $\pm$ standard deviation across $N$ stochastic forward passes. This allows us to separate the accuracy of a single trained set of weights from the uncertainty induced by hardware variability at deployment time.

% <<< INSERT NEW SUBSECTION HERE >>>

\subsection{Physical Frontend Compensation}
```

---

## Draft Paragraph (~150 words)

```latex
\subsection{Training Protocol}
\label{subsec:training-protocol}

All Tiny-ViT experiments are trained with AdamW ($lr = 5\times10^{-4}$, weight decay $0.05$) for 100 epochs using a batch size of 64 and a cosine annealing learning-rate schedule ($T_{\max} = 100$). Images are resized to $224\times224$, augmented with random horizontal flips, and normalized by dataset statistics. The default analog programming resolution is $n_{\text{states}} = 16$ conductance levels. Experiment V1 uses standard digital training; V2 uses hybrid layers without noise; V3 uses hybrid layers with fixed D2D mismatch ($\sigma_{\text{D2D}}=10\%$) active during training but no per-forward C2C resampling; V4--V7 employ full hardware-aware training in which fixed D2D mismatch is resampled at the start of every epoch and C2C noise ($\sigma_{\text{C2C}}=5\%$ or $10\%$) is drawn on each forward pass. V6 additionally enables the physical photoresponse front-end, and V7 evaluates post-training retention decay. Complete hyperparameter specifications and the experiment matrix are available in the open-source training scaffold (see Code Availability).
```

---

## Key Numerical Values Extracted from Source

| Parameter | Value | Source location |
|-----------|-------|-----------------|
| Optimizer | AdamW | `train_tinyvit_ensemble.py:617` |
| Learning rate | $5\times10^{-4}$ | `train_tinyvit_ensemble.py:105` |
| Weight decay | $0.05$ | `train_tinyvit_ensemble.py:106` |
| Batch size | 64 | `train_tinyvit_ensemble.py:104` |
| Epochs | 100 | `train_tinyvit_ensemble.py:103` |
| LR schedule | CosineAnnealingLR ($T_{\max}=100$) | `train_tinyvit_ensemble.py:618` |
| Image size | $224\times224$ | `train_tinyvit_ensemble.py:355` |
| Augmentation | RandomHorizontalFlip | `train_tinyvit_ensemble.py:356` |
| Conductance states ($n_{\text{states}}$) | 16 | `train_tinyvit_ensemble.py:89` |
| D2D resampling frequency | Start of every epoch (HAT only) | `train_tinyvit_ensemble.py:651--655` |
| V3 training mode | Fixed D2D on, C2C off | `train_tinyvit_ensemble.py:294--304` |
| V4--V7 training mode | Full HAT (D2D + C2C) | `train_tinyvit_ensemble.py:291--293` |

---

## Notes for Review

- **Citation placeholder:** The draft uses "(see Code Availability)" because no BibTeX label for the code repository was found in the current `paper/latex_gpt/` tree. Replace with the appropriate `\citep{}` or footnote command once the code-availability statement is added to the main manuscript.
- **Subsection vs. subsubsection:** If the Methodology section is already long, this material can be demoted to a `\subsubsection{Training hyperparameters}` inside `\subsection{Hardware-Aware Training}` without changing the paragraph text.
- **Datasets:** The training script supports CIFAR-10, CIFAR-100, and Flowers-102. The paragraph omits an explicit dataset list to stay concise; add it if the manuscript requires.
