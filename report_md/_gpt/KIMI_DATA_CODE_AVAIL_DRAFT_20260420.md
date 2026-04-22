# K-T4: Data Availability + Code Availability — Draft

**Paper:** Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision  
**Venue:** Nature Communications  
**Date:** 2026-04-20  
**Status:** Draft — awaiting URL, DOI, and license confirmation

---

## Ready-to-insert LaTeX paragraphs

Paste the two blocks below into the manuscript in the locations prescribed by the Nature Communications template (typically immediately before or within the References section, or in a dedicated ``Data and Code Availability'' paragraph at the end of the Methods).

### Data Availability

```latex
\section*{Data availability}

All datasets used in this study are publicly available and were accessed through standard machine-learning libraries.
CIFAR-10 and CIFAR-100 were downloaded via \texttt{torchvision} (\url{https://www.cs.toronto.edu/~kriz/cifar.html}) and are released under the MIT licence.
Flowers-102 was downloaded via \texttt{torchvision} (\url{https://www.robots.ox.ac.uk/~vgg/data/flowers/102/}); the dataset is made available for academic research.
ImageNet ILSVRC2012 (\url{https://image-net.org/}) was used only for pre-training the Tiny-ViT-5M backbone; users must supply their own copy subject to the ImageNet terms of use.

The source data underlying all figures and tables in the main text and Supplementary Information are provided as part of this submission.
They consist of 73 JSON files and 2 CSV files (total uncompressed size $\sim$732~KiB), catalogued in \texttt{source\_data\_v1/MANIFEST.md}.
Key files include the iso-accuracy contour JSONs, retention time-series, ADC-layerwise nonideality sweeps, fresh-instance evaluation records, inverse-gamma frontend sweeps, and nonlinear-write ablation lanes.
Raw doctoral measurement exports that underlie the fitted device profiles are available from the corresponding author upon reasonable request.
```

### Code Availability

```latex
\section*{Code availability}

The complete simulation framework, training scripts, evaluation pipelines, and figure-generation code are available at [\url{https://github.com/...}] (to be released upon acceptance).
A snapshot of the codebase has been deposited on Zenodo and will receive a permanent DOI at acceptance [DOI: Zenodo placeholder].
The repository is released under the [License placeholder] licence.

Key scripts included in the release are:
\begin{itemize}[noitemsep,topsep=3pt]
    \item \texttt{train\_tinyvit.py}, \texttt{train\_convnext.py}, \texttt{train\_resnet18.py} — training loops for the three backbone architectures;
    \item \texttt{train\_tinyvit\_ensemble.py} — Ensemble HAT training with epoch-level D2D resampling;
    \item \texttt{eval\_measured\_profile.py}, \texttt{eval\_literature\_profile.py}, \texttt{eval\_fresh\_instances.py} — evaluation and zero-shot transfer pipelines;
    \item \texttt{run\_a23\_experiments.py} — inverse-gamma frontend compensation sweep driver;
    \item \texttt{analog\_layers.py}, \texttt{analog\_layers\_ensemble.py} — mixed analog--digital layer implementations with noise injection, ADC quantization, and energy profiling;
    \item \texttt{physical\_noise\_pipeline.py} — frontend photoresponse and shot-noise model;
    \item \texttt{plot\_paper\_figures.py}, \texttt{plot\_convnext\_results.py}, \texttt{plot\_resnet18\_results.py} — figure generation;
    \item \texttt{scripts/\_gpt/check\_locked\_numbers.py} — reproducibility sanity check that re-reads every JSON cited in the manuscript and asserts numerical consistency.
\end{itemize}
```

---

## Checklist for finalisation

| Item | Status | Notes |
|:---|:---|:---|
| GitHub repository URL | **Placeholder** | Replace `[https://github.com/...]` with the actual public repository URL. |
| Zenodo DOI | **Placeholder** | Replace `[DOI: Zenodo placeholder]` with the assigned Zenodo DOI after deposition. |
| Software licence | **Placeholder** | Choose and confirm: MIT / Apache-2.0 / BSD-3-Clause. The repository currently contains an Apache-2.0 reference in `README.md`; verify this is the authors' final choice. |
| Source-data bundle completeness | Ready | `release_artifacts/source_data_v1/` contains 73 JSON + 2 CSV + README + MANIFEST (see `source_data_v1_MANIFEST.md`). |
| Raw measurement data access | Ready | Statement notes availability from corresponding author upon reasonable request. |
| Dataset licence accuracy | Ready | CIFAR-10/100 (MIT), Flowers-102 (academic use), ImageNet (user-supplied, terms of use). |

---

## One-sentence summary for cover page / abstract metadata

> All data are publicly available or provided with this submission; code and pre-trained checkpoints will be released on GitHub and Zenodo upon acceptance.
