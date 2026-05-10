# K-S3: Notation & Glossary Audit

**Scope:** All `.tex` sources in `compute_vit/paper/latex_gpt/` (main body compiled in `main.tex` input order, plus `supplementary.tex` and `sections/08_appendix.tex`).

---

## PASS — Defined at first use

### Acronyms
- **CIM**: `01_introduction.tex:5` — "Compute-in-memory (CIM)"
- **HAT**: `00_abstract.tex:5` — "hardware-aware training (HAT)"
- **D2D**: `00_abstract.tex:5` — "device-to-device (D2D)"
- **ADC**: `00_abstract.tex:5` — "analog-to-digital converter (ADC)"
- **MLP**: `01_introduction.tex:17` — "multi-layer perceptron (MLP)"
- **QKV**: `02_related_work.tex:22` — "query-key-value, or QKV"
- **OPECT**: `00_abstract.tex:5` — "organic photoelectrochemical transistor (OPECT)"
- **STE**: `03_methodology.tex:15` — "straight-through estimator (STE)"
- **MC**: `05_results.tex:18` — "Monte Carlo (MC)"
- **IR**: `01_introduction.tex:19` — "current--resistance, or IR, drop"
- **SNR**: `supplementary.tex:526` — "signal-to-noise ratio (SNR)"
- **RRAM**: `05_results.tex:82` — "resistive random-access memory (RRAM)"
- **SRAM**: `01_introduction.tex:5` — "static random-access memory (SRAM)"
- **PCM**: `05_results.tex:82` — "phase-change memory (PCM)"
- **LSB**: `supplementary.tex:298` — "least significant bit (LSB)"
- **DNTT**: `03_methodology.tex:52` — "dinaphtho-thieno-thiophene (DNTT)"
- **NL**: `00_abstract.tex:5` — "nonlinear write (NL=2.0)" (implicit expansion)
- **JSON**: `03_methodology.tex:85` — common knowledge (JavaScript Object Notation)
- **GPU**: `02_related_work.tex:20` — common knowledge
- **RNG**: `supplementary.tex:792` — common knowledge
- **AdamW**: `03_methodology.tex:50` — common optimizer name
- **PyTorch**: `02_related_work.tex:20` — common framework name
- **HuggingFace**: `07_conclusion.tex:12` — common library name
- **CrossSim**: `01_introduction.tex:11` — proper noun (simulator)
- **AIHWKIT**: `01_introduction.tex:11` — proper noun
- **MemTorch**: `01_introduction.tex:11` — proper noun
- **ReLU**: `06_discussion.tex:26` — common activation function
- **softmax**: `02_related_work.tex:22` — common function
- **CIFAR**: `02_related_work.tex:15` — dataset name
- **Flowers-102**: `05_results.tex:29` — dataset name
- **ImageNet**: `06_discussion.tex:47` — dataset name
- **ViT**: `01_introduction.tex:7` — "Vision Transformer (ViT)"
- **CNN**: `01_introduction.tex:7` — "convolutional neural network (CNN)"
- **Q/K/V**: `03_methodology.tex:8` — "query/key/value (Q/K/V)"

### Greek symbols & subscripted variables
- **$s_{\ell}$**: `03_methodology.tex:17` — scale factor introduced in Eq. (1)
- **$G_{\min}$, $G_{\max}$**: `03_methodology.tex:15` — "conductance window $[G_{\min}, G_{\max}]$"
- **$n_{\mathrm{states}}$**: `03_methodology.tex:15` — "quantized to $n_{\mathrm{states}}$ levels"
- **$Q_{n}(\cdot)$**: `03_methodology.tex:15` — "STE quantizer $Q_{n}(\cdot)$"
- **$G_{\mathrm{eff}}$**: `03_methodology.tex:15` — "Differential readout recovers $G_{\mathrm{eff}}=\tilde{G}^{+}-\tilde{G}^{-}$"
- **$\tilde{G}^{+}$, $\tilde{G}^{-}$**: `03_methodology.tex:15` — positive/negative branch conductances
- **$M_{0}$**: `03_methodology.tex:28` — "one D2D mismatch field $M_{0}$"
- **$M^{(e)}$**: `03_methodology.tex:33` — "resamples $M^{(e)}\sim p(M)$ at each epoch"
- **$\theta_{\mathrm{std}}^{\star}$**: `03_methodology.tex:30` — standard-HAT optimum (Eq. 2)
- **$\theta_{\mathrm{ens}}^{\star}$**: `03_methodology.tex:35` — ensemble-HAT optimum (Eq. 3)
- **$x_{n}$, $y_{n}$**: `03_methodology.tex:30` — input/label pair (standard notation)
- **$T_{\max}$**: `03_methodology.tex:50` — cosine-annealing hyperparameter (common knowledge)
- **$P_{\mathrm{in}}$**: `03_methodology.tex:54` — preprocessed optical power (Eq. 4 context)
- **$I_{\mathrm{photo}}$**: `01_introduction.tex:15` — photocurrent (context: "sublinear photoresponse ($I_{\text{photo}} \propto P^{\gamma_{\text{phys}}}$)")
- **$X_{\mathrm{norm}}$**: `03_methodology.tex:72` — renormalized input (Eq. 6 context)
- **$\beta$**: `supplementary.tex:565` — substitution variable $\beta = \gamma_c \gamma_{\text{phys}}$
- **$\gamma_c$**: `supplementary.tex:554` — "physical inverse $\gamma_c = 1/\gamma_{\text{phys}}$"
- **$\rho$**: `06_discussion.tex:43` — correlation coefficient
- **$E_{\text{MAC}}$, $E_{\text{cell}}$, $E_{\text{ADC},8b}$, $E_{\text{DAC},8b}$, $t_{\text{ADC},8b}$, $N_{\text{ops}}$**: `supplementary.tex:440–441` — energy-model parameters defined inline
- **$\sigma_{\text{pop}}$**: `supplementary.tex:792` — "run-to-run spread ($\sigma_{\text{pop}} = 2.67\%$)"
- **$\delta_{\mathrm{IR}}^{\max}$**: `supplementary.tex:662` — maximum IR-drop fraction
- **$\Delta_{\hat{W}}$**: `03_methodology.tex:26` — "recovered weight step $\Delta_{\hat{W}}$"
- **$\epsilon$**: `03_methodology.tex:17` — small constant (common notation)
- **$N$**: `03_methodology.tex:30` — number of samples (common notation)
- **$M'$**: `03_methodology.tex:39` — unseen mismatch draw
- **$\mathrm{Acc}_{\mathrm{fresh}}$**: `03_methodology.tex:40` — fresh-instance accuracy
- **$G_{\mathrm{eff},ij}$**: `03_methodology.tex:17` — element-wise effective conductance
- **$\Delta G$**: `supplementary.tex:385` — defined as $G_{\max}-G_{\min}$
- **$s_{\ell}^{\mathrm{ret}}$**: `supplementary.tex:389` — retention recalibration scale
- **$\delta G_{\mathrm{eff},ij}$**: `supplementary.tex:395` — conductance perturbation
- **$\delta g_{\mathrm{D2D}}$**: `supplementary.tex:401` — D2D perturbation
- **$\delta g_{\mathrm{C2C}}$**: `supplementary.tex:406` — C2C perturbation
- **$G(t)$**: `supplementary.tex:426` — time-dependent conductance
- **$G_{\mathrm{prog}}$**: `supplementary.tex:426` — programmed conductance
- **$f_{\mathrm{ret}}(t)$**: `supplementary.tex:430` — retention decay factor
- **$A_1$, $A_2$**: `supplementary.tex:432` — retention amplitudes
- **$\epsilon_{\mathrm{sneak}}$**: `supplementary.tex:664` — sneak-path noise
- **$E_{\mathrm{total}}$, $E_{\mathrm{ADC}}$, $E_{\mathrm{DAC}}$**: `supplementary.tex:447–461` — energy totals
- **$t_{0.975}$, $df$**: `supplementary.tex:792` — statistical constants
- **$n$**: sample size (common notation)
- **$S_i$**: `03_methodology.tex:90` — Sobol index (Eq. 6)
- **$X_i$, $Y$**: `03_methodology.tex:95` — Sobol factors/output
- **$\sigma^2$**: `supplementary.tex:560` — variance
- **$A$**: `supplementary.tex:520` — attention map
- **$\gamma_{\text{ISP}}$**: `supplementary.tex:511` — ISP gamma
- **$X$**: `03_methodology.tex:52` — normalized input $X \in [0,1]$
- **$P$**: `01_introduction.tex:15` — optical power
- **$\Delta_{\max}$**: `supplementary.tex:96` — table header defines it
- **$\alpha$ (asymmetry)**: `08_appendix.tex:624` — asymmetry factor

### Specialized terms
- **photoresponse**, **retention**, **write nonlinearity**: contextual/descriptive
- **mixed-signal**, **crossbar**, **differential-pair**: standard hardware terms
- **zero-shot transfer**, **canonical regime**, **iso-accuracy**, **operating envelope**, **contour map**: descriptive
- **Sobol analysis**: known sensitivity-analysis method
- **two-phase structure**, **proportional-noise**, **state-dependent**, **gradient-scaling approximation**, **group-wise ablation**, **bottleneck**, **attention-side linearizations**, **fresh-instance transfer**, **spatial mismatch map overfitting**: descriptive
- **profile interface**, **digital backbone**, **training recipe**, **scale recovery**, **scale-masking**, **front-end compensation**, **sublinear photoresponse**, **signal-to-noise trade-off**, **hardware-instance overfitting**, **MLP path**, **analog ceiling**, **energy model**, **spatial IR drop**, **sneak-path currents**, **temperature-dependent shifts**, **heavy-tailed conductance distributions**, **spatially correlated D2D**: descriptive or defined by context

---

## FAIL — First use lacks definition

### Acronyms
- **C2C**: `05_results.tex:18` — "5% C2C" used without expansion (expanded later in `03_methodology.tex:15` as "cycle-to-cycle (C2C)")
  - Patch: "cycle-to-cycle (C2C)"
- **DAC**: `supplementary.tex:96` — "ADC / DAC" without expansion
  - Patch: "digital-to-analog converter (DAC)"
- **LTP**: `03_methodology.tex:52` — "$NL_{\mathrm{LTP}}=1$ (long-term potentiation)"; acronym precedes expansion
  - Patch: "long-term potentiation (LTP)" before first use
- **LTD**: `03_methodology.tex:52` — "$|NL_{\mathrm{LTD}}|=1$ (long-term depression)"; acronym precedes expansion
  - Patch: "long-term depression (LTD)" before first use
- **ISP**: `supplementary.tex:510` — "ISP gamma correction" without expansion
  - Patch: "image signal processor (ISP)"
- **INL**: `supplementary.tex:302` — "Offset, gain, and INL are injected..." without expansion
  - Patch: "integral nonlinearity (INL)"
- **DNL**: `supplementary.tex:441` — "behavioral DNL/INL modeling" without expansion
  - Patch: "differential nonlinearity (DNL)"
- **SAR**: `supplementary.tex:441` — "SAR-like 8-bit readout proxy" without expansion
  - Patch: "successive-approximation register (SAR)"
- **MAC**: `supplementary.tex:440` — "Analog MAC" without expansion
  - Patch: "multiply-accumulate (MAC)"
- **MSE**: `supplementary.tex:560` — "expected MSE is" without expansion
  - Patch: "mean-squared error (MSE)"
- **PIM**: `02_related_work.tex:24` — "ViT-on-PIM studies" without expansion
  - Patch: "processor-in-memory (PIM)"
- **GELU**: `03_methodology.tex:8` — "GELU activation" without expansion
  - Patch: "Gaussian Error Linear Unit (GELU)"
- **LN**: `supplementary.tex:92` — "softmax, LN, head" without expansion
  - Patch: "layer normalization (LN)"
- **AR(1)**: `06_discussion.tex:43` — "separable AR(1) perturbation" without expansion
  - Patch: "autoregressive AR(1)"
- **AMP**: `05_results.tex:41` — "no-AMP recovery run" without expansion
  - Patch: "automatic mixed precision (AMP)"
- **FP32**: `05_results.tex:8` — "Digital FP32 baselines" without expansion
  - Patch: "32-bit floating point (FP32)"
- **i.i.d.**: `03_methodology.tex:44` — "i.i.d. Gaussian draw" without expansion
  - Patch: "independent and identically distributed (i.i.d.)"
- **MVM**: `supplementary.tex:27` — "crossbar MVM" without expansion
  - Patch: "matrix-vector multiplication (MVM)"

### Specialized terms
- **inverse-gamma**: `00_abstract.tex:3` — "inverse-gamma compensation" used without definition
  - Patch: "inverse-gamma (power-law) compensation"
- **shot-noise**: `00_abstract.tex:3` — "shot-noise trade-off" used without definition
  - Patch: "shot-noise (photon-counting) trade-off"
- **profile-driven**: `00_abstract.tex:3` — "profile-driven first-order behavioral simulation framework" used without definition
  - Patch: "profile-driven (replaceable device-profile) framework"
- **Ensemble HAT**: `00_abstract.tex:5` — used without definition (formally introduced only in `03_methodology.tex:33`)
  - Patch: "Ensemble HAT (epoch-resampled D2D mismatch)"
- **fresh-instance**: `00_abstract.tex:5` — "fresh-instance evaluations" used without definition
  - Patch: "fresh-instance (unseen hardware) evaluations"

### Greek symbols & subscripted variables
- **$\gamma_{\text{phys}}$**: `01_introduction.tex:15` — "$I_{\text{photo}} \propto P^{\gamma_{\text{phys}}}$" without definition
  - Patch: "photoresponse exponent $\gamma_{\text{phys}}$"
- **$\sigma_{\mathrm{D2D}}$**: `05_results.tex:31` — first compiled use ("$\sigma_{\mathrm{D2D}}$ levels") without definition
  - Patch: "D2D standard deviation $\sigma_{\mathrm{D2D}}$"
- **$\sigma_{\mathrm{C2C}}$**: `05_results.tex:56` — first compiled use ("$\sigma_{\mathrm{C2C}}=5\%$") without definition
  - Patch: "C2C standard deviation $\sigma_{\mathrm{C2C}}$"
- **$\varepsilon_{\mathrm{shot}}$**: `03_methodology.tex:65` — used in Eq. (5) without definition
  - Patch: "shot noise $\varepsilon_{\mathrm{shot}}$"
- **$I_{\mathrm{dark}}$**: `03_methodology.tex:63` — used in Eq. (5) without definition
  - Patch: "dark current $I_{\mathrm{dark}}$"
- **$\tau_{1}$, $\tau_{2}$**: `03_methodology.tex:85` — listed in JSON bundle without definition
  - Patch: "retention time constants $\tau_1, \tau_2$"
- **$A_{0}$**: `03_methodology.tex:85` — listed in JSON bundle without definition
  - Patch: "initial amplitude ratio $A_0$"
- **$S_{\text{ADC}}$**: `01_introduction.tex:17` — "$S_{\text{ADC}}=0.98$" without definition
  - Patch: "Sobol index for ADC, $S_{\text{ADC}}$"
- **$S_{\mathrm{D2D}}$**: `05_results.tex:51` — "$S_{\mathrm{D2D}}=0.92$" without definition
  - Patch: "Sobol index for D2D, $S_{\mathrm{D2D}}$"
- **$\alpha$**: `03_methodology.tex:61` — "$\alpha P_{\mathrm{in}}^{\gamma_{\mathrm{phys}}}$" without definition
  - Patch: "photocurrent gain $\alpha$"
- **$w_{\max}$**: `03_methodology.tex:21` — used in Eq. (1) without definition
  - Patch: "maximum weight magnitude $w_{\max}$"
- **$d_k$**: `supplementary.tex:520` — "$QK^{\top}/\sqrt{d_k}$" without definition
  - Patch: "key dimension $d_k$"
- **$\sigma_{\mathrm{sneak}}$**: `supplementary.tex:664` — used without definition
  - Patch: "sneak-path noise standard deviation $\sigma_{\mathrm{sneak}}$"
- **$\delta_{\mathrm{IR}}$**: `supplementary.tex:661` — used without definition
  - Patch: "IR drop fraction $\delta_{\mathrm{IR}}$"

---

**Summary:** 37 items fail the first-use definition check. The majority are supplementary-level acronyms (DAC, INL, DNL, SAR, MAC, MSE, ISP, LN, MVM) and main-body symbols that appear in figures/captions or equations before their textual introduction ($\sigma_{\mathrm{D2D}}$, $\sigma_{\mathrm{C2C}}$, $S_{\text{ADC}}$, $S_{\mathrm{D2D}}$, $\gamma_{\text{phys}}$, $\alpha$, $\varepsilon_{\mathrm{shot}}$, $I_{\mathrm{dark}}$, $\tau_{1,2}$, $A_0$, $w_{\max}$). A handful of abstract-level terms (inverse-gamma, shot-noise, profile-driven, Ensemble HAT, fresh-instance) are introduced without a gloss.
