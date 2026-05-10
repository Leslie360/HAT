# T1 Draft: Distinguishing Inverse-Gamma Frontend Compensation from ISP Gamma Correction

## Target Insertion Point
Discussion section, after "Transformer Sensitivity to Non-Idealities" or as a new subsection under Discussion.

## Rationale
The most likely reviewer attack on the inverse-gamma frontend is: "This is just standard gamma correction from digital image processing."

The rebuttal must be crisp, technical, and placed where reviewers will see it.

---

## Proposed LaTeX Paragraph

```latex
\subsection{Frontend Compensation as a System-Level Design Primitive}

The inverse-gamma preprocessor in Eq.~\ref{eq:inverse-gamma} is superficially similar to gamma correction in digital image processing (ISP), but the two serve different physical purposes and operate in different noise regimes. In ISP, gamma encoding ($\gamma_{\text{ISP}} \approx 2.2$) compresses high-intensity pixel values to match the nonlinear response of the human visual system, while its inverse (gamma decoding) expands the signal before display. The goal is perceptual uniformity, not physical linearization, and the noise model is typically signal-independent (e.g., thermal noise in the digital domain or Poisson noise in the sensor that is already quantized).

In the organic phototransistor frontend modeled here, the nonlinearity is a physical transduction property: photocurrent follows $I_{\text{photo}} \propto P^{\gamma_{\text{phys}}}$ with $\gamma_{\text{phys}}$ typically between 0.5 and 2.0, depending on material and illumination regime. The inverse-gamma preprocessor $P_{\text{in}} = X^{1/\gamma_{\text{phys}}}$ is therefore applied \emph{before} the physical transduction step, not after sensor readout. Consequently, the shot noise $\varepsilon_{\text{shot}}$ is injected \emph{after} the compensation and scales with the compensated photocurrent. This ordering is critical: ISP gamma decoding operates on already-noisy quantized pixels, whereas the frontend compensation reshapes the signal that subsequently acquires noise. The result is a regime-dependent trade-off that has no analogue in ISP: for $\gamma_{\text{phys}} > 1$, compensation linearizes the signal and improves accuracy; for $\gamma_{\text{phys}} < 1$, it amplifies shot-noise variance across the entire intensity range, yielding marginal or negative benefit (Table~\SuppTableFrontend). This signal-to-noise coupling is intrinsic to the phototransistor transduction chain and is captured explicitly by the compensated photocurrent model in Eq.~\ref{eq:frontend-photoresponse}.

Because the preprocessor is parameterized by $\gamma_{\text{phys}}$ and exposed through the same JSON device profile as conductance window, retention, and variability, it functions as a \emph{replaceable system-level design primitive} rather than as a fixed preprocessing step. A device team can evaluate, directly in the simulator, whether their measured photoresponse exponent warrants compensation or whether the associated noise amplification outweighs the linearization benefit for their specific vision task. This bridging of device characterization to task-level accuracy prediction is the distinguishing feature of the present approach.
```

## Key Distinctions Tabulated (for reviewer response if needed)

| Aspect | ISP Gamma Correction | Frontend Inverse-Gamma Compensation |
|--------|---------------------|-------------------------------------|
| **Purpose** | Perceptual uniformity for human vision | Physical linearization of photocurrent |
| **Nonlinearity location** | Display/sensor characteristic | Phototransistor transduction ($I_{\text{photo}} \propto P^{\gamma_{\text{phys}}}$) |
| **Noise model** | Signal-independent or post-quantization | Shot noise $\propto I_{\text{photo}}$ (signal-dependent) |
| **Ordering** | Applied to already-quantized/noisy pixels | Applied before physical transduction |
| **Trade-off** | None (deterministic lookup) | Signal-to-noise trade-off: dark-region recovery vs bright-region amplification |
| **Parameterization** | Fixed standard ($\gamma_{\text{ISP}}=2.2$) | Device-specific ($\gamma_{\text{phys}}$ from measurement) |
| **Task-level evaluation** | Not typically performed | Central: accuracy vs $\gamma_{\text{phys}}$ matrix (Table~\SuppTableFrontend) |

## Defense Line (if reviewer asks)

> "We do not claim invention of inverse-gamma transformation (known in ISP and optics). We claim its systematic evaluation as a \textbf{task-level design primitive} in an organic optoelectronic CIM context, where the shot-noise coupling and the profile-driven parameterization create a regime-dependent trade-off that is absent from digital ISP pipelines."
