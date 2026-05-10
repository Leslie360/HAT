# K-R4: Round-J Residual Audit

## K-Q4: Abstract framing hedge
- Status: PASS
- File: sections/00_abstract.tex
- Line: 7
- Quote: "Taken together, the framework serves as a simulation-based materials-to-system decision aid for identifying device characteristics that constrain edge-vision deployment."
- Note: Both required hedge terms (`simulation-based` and `decision aid`) are present in the abstract closing sentence.

## K-Q5: CrossSim 14.43 pp softening
- Status: PASS
- File: sections/06_discussion.tex
- Line: 47
- Quote: "...diverges under noise injection ($81.63 \\pm 0.56$\\% vs.\\ $67.20 \\pm 2.67$\\% at $\\sigma=5\\%$, a large qualitative divergence of 14.43~pp at $n=3$, preliminary), highlighting the sensitivity of accuracy predictions to the noise-to-conductance mapping."
- Note: All three required elements are present in the same parenthetical: `large qualitative divergence of 14.43`, `preliminary`, and `$n=3$`.

## K-Q6: ImageNet failure-mode prediction
- Status: PASS
- File: sections/06_discussion.tex
- Line: 47
- Quote: "Extrapolation to ImageNet-scale deployment is also outside the present evidence base: per-epoch D2D resampling would incur substantially higher training overhead, the 6-bit ADC cliff may shift upward for deeper MLP stacks with finer decision boundaries, and the current results do not address fresh large-scale training from random initialization."
- Note: The paragraph explicitly notes (1) higher training overhead, (2) potential ADC cliff shift, and (3) unaddressed random-init large-scale training, located in the Discussion/Outlook subsection.

## K-Q7: Forward pointers Eq.3/Eq.8
- Status: FAIL
- File: sections/05_results.tex
- Line: 41, 51, 63
- Quote:
  - Line 41 (Eq.~3, **no forward pointer**): "This motivates the distribution-matched Ensemble HAT objective (Eq.~\\ref{eq:hat-ensemble}), instantiated in Section~\\ref{subsec:nl-hat-stress}."
  - Line 51 (Eq.~8, **no forward pointer**): "Sobol analysis (Eq.~\\ref{eq:sobol-first-order}) confirms the two-phase structure: $S_{\\mathrm{ADC}}=0.98$ over the full grid, and $S_{\\mathrm{D2D}}=0.92$ in the operational region ($\\geq$6~bits, $\\sigma_{\\mathrm{D2D}} \\leq 15\\%$), with negligible interaction ($<$4\\%)."
  - Line 63 (Eq.~3, **forward pointer present**): "Ensemble HAT (Figure~\\ref{fig:ensemble-hat-concept}; formally defined in Section~\\ref{sec:methodology}, Eq.~\\ref{eq:hat-ensemble}) preserves 86.37$\\pm$1.54\\% across 10 fresh arrays..."
- Missing: Eq.~8 (`eq:sobol-first-order`) is referenced in Results without any forward pointer to Section~\\ref{sec:methodology}. Eq.~3 (`eq:hat-ensemble`) at line 41 also lacks a forward pointer to methodology (only a local Results subsection pointer).

## K-Q9: Per-batch HAT one-liner
- Status: PASS
- File: sections/05_results.tex
- Line: 63
- Quote: "An exploratory single-run training-ablation cadence scan (Supplementary Fig.~\\SuppFigZeroShot) shows epoch-level resampling reaches 88.41\\% (50-epoch training ablation), versus 87.18\\% (fixed) and 86.16\\% (per-batch), confirming that structured epoch-level resampling rather than per-batch perturbation is the load-bearing schedule choice."
- Note: Explicit numerical comparison of all three resampling schedules is present: epoch-level (88.41\\%), fixed (87.18\\%), and per-batch (86.16\\%).

---
**Audit summary:** 4 of 5 items pass. K-Q7 fails because Eq.~8 lacks a forward pointer in Results and the Eq.~3 reference at line 41 also does not point back to methodology.
