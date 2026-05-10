# Direction D: Optical-Electronic Co-Design Frontend for Organic CIM

## Literature Sweep Summary (2021–2026)
**Date:** 2026-04-23
**Scope:** Optoelectronic CIM systems, photodiode nonlinearity, joint optical/electronic optimization, illumination robustness, organic photodetectors + neural computation.

---

## 1. Motivation
Real-world deployment of optical-input CIM accelerators (e.g., near-sensor or in-sensor analog arrays) must operate under **varying ambient illumination**, temperature drift, and photodetector non-ideality. Current CIM literature largely assumes a calibrated, linear optical frontend or relies on a fixed inverse-gamma correction. In practice, photodiode responsivity is **nonlinear with incident flux, bias voltage, and wavelength**, and organic photodetectors (OPDs) exhibit additional trap-state-limited dark current and process variation. Ignoring these frontend non-idealities when training the electronic backend leads to a **domain-shift gap** between laboratory conditions and field deployment. Direction D therefore targets **joint optimization of the optical frontend (photodiode / illumination) and the electronic CIM backend** to maximize end-to-end task accuracy and illumination robustness.

---

## 2. SOTA Landscape

### 2.1 In-Sensor / Near-Sensor Optoelectronic Computing
- **Jang et al., *Nature Electronics* 2022** – Demonstrated in-sensor analog convolution using an electrostatically doped silicon photodiode array (3×3) programmed into seven different kernels. Shows that photocurrent modulation via gate bias can fuse sensing and linear compute, but assumes ideal illumination and does not co-optimize with a downstream neural network.
  *Key number:* 3×3 programmable kernel, compatible with CMOS foundry flow.
- **Vasileiadis et al., *Materials* 2021** – Proposed a 1D1M (one-photodiode–one-memristor) vision sensor crossbar and used SPICE to show mean-filtering via in-memory computing. Eight discrete illumination levels were used, but the photodiode was modeled as an ideal current source in series with a diode; no joint training with CIM weights.
  *Key number:* 28×28 array, 8-level gray-scale capture + mean-filter READ.
- **Yang et al., *Nature Electronics* 2024** – “In-sensor dynamic computing for intelligent machine vision.” Introduced reconfigurable phototransistor arrays that perform adaptive in-sensor preprocessing. Focus is on device-level dynamic computing, not system-level co-design with a CIM macro.
  *Key number:* Reconfigurable kernels for edge enhancement under varying contrast.
- **Huang et al., *Nature Nanotechnology* 2025** – Fully integrated multi-mode optoelectronic membrane array for diversified in-sensor computing. Achieves multimodal sensing (pressure, temperature, light) with integrated processing, but the optical pathway is not explicitly co-optimized with algorithmic weights.
  *Key number:* Membrane-array format, multimodal fusion.

### 2.2 Photodiode Response Models & Nonlinearity
- **Sandberg et al., *Nature Photonics* 2023** – Showed that the dark saturation current in organic photodiodes (OPDs) is fundamentally limited by **mid-gap trap states**, establishing an upper bound for specific detectivity. This directly impacts the signal-to-noise ratio and linear dynamic range of an OPD-CIM frontend.
  *Key number:* Detectivity bound set by trap-mediated dark current.
- **Teledyne COSMOS sensor characterization (2024)** – Documented severe photodiode nonlinearity at low signal levels caused by charge-trapping potential barriers. A calibration ramp was required to map raw values back to linear illumination.
  *Key number:* >10% deviation below 5% saturation; trap-model calibration required.
- **InGaAs / Si photodiode linearity studies (2022–2023)** – Supralinearity under over-filled illumination can reach **0.14–20%** depending on device geometry and wavelength. Voltage-dependent responsivity has been identified as a dominant low-frequency nonlinearity source.

### 2.3 Joint Optimization of Optical Frontend + Electronic Processor
- **Klinghoffer et al., *ICCV* 2023 (DISeR)** – Used reinforcement learning to jointly optimize illumination sources, optics, sensors, and downstream algorithms over a **non-differentiable simulator**. Demonstrates that end-to-end co-design of the imaging pipeline outperforms modular design for classification and detection tasks.
  *Key number:* RL-based search over optics + sensor + algorithm parameters.
- **Bian et al., *Light: Science & Applications* 2025** – Review on “Physical twinning for joint encoding-decoding optimization in computational optics.” Highlights the **digital-twin** approach: optical modulation elements are represented as differentiable neural-network layers and co-trained with the decoder. The reverse physical twinning (optimized parameters → real hardware) remains the key challenge.
  *Key number:* End-to-end differentiable optical-electronic co-optimization framework.
- **“Physics vs. Learned Priors” (2022)** – Survey of deep optics / end-to-end camera design. Joint optimization has been applied to HDR, depth estimation, classification, and object detection by parameterizing optics, sensor, and ISP as learnable layers.

### 2.4 Organic Photodetectors + Neuromorphic Computation
- **Chen et al., *Nature Photonics* 2023** – Organic optoelectronic synapse based on photon-modulated electrochemical doping. Mimics retina-like adaptation and demonstrates neural-network-compatible weight update, but does not address array-level CIM inference or illumination variation.
- **Wu et al., *Nature Communications* 2023** – Wearable in-sensor reservoir computing using optoelectronic polymers. Achieves multi-task learning with polymer photodetectors; nonlinearity is exploited as a feature, not compensated.
- **Zhou et al., *Nature Communications* 2023** – Full hardware implementation of neuromorphic visual systems based on multimodal optoelectronic resistive memory arrays. Integrates sensing + memory + computing in one crossbar, yet the photoresponse is treated as a fixed synaptic weight modulation, not a jointly optimizable frontend.
- **Chang et al., *Nature Communications* 2024** – Birdlike broadband neuromorphic visual sensor arrays for fusion imaging. Uses organic/inorganic heterostructures for UV–visible-NIR fusion imaging; demonstrates in-sensor preprocessing but no co-optimization with external CIM.

### 2.5 Illumination Robustness in Vision Systems
- **Chuquimarca et al., *Smart Agricultural Technology* 2025** – Systematic study of deep-learning robustness under gamma-based illumination augmentation. Baseline accuracy (~92.5%) dropped by up to **11.8 percentage points** under moderate gamma shift (Γ=0.4); augmentation training recovered ~8.3 pp on average.
  *Key number:* 11.8 pp accuracy drop under moderate illumination change.
- **SRM-based ADS (*Nature Communications* 2025)** – Memristor YOLO models outperformed software baselines under fluctuating illumination because analog tuning enabled dynamic feature refinement. Suggests that **hardware-algorithm co-design** can intrinsically improve illumination robustness.

---

## 3. Research Gap
1. **Missing joint optimization loop:** Existing optoelectronic CIM works either (a) fix the photodiode model and only optimize the memory array, or (b) treat the optical frontend as a separate sensor with no gradient flow to the CIM weights. No prior work has demonstrated **end-to-end gradient-based co-optimization of an organic-photodetector frontend and a CIM backend** for image classification.
2. **Illumination robustness ignored:** Most neuromorphic vision sensors are characterized under a single calibrated light intensity. The impact of **varying illumination on analog MAC accuracy** (photocurrent → CIM bit-line current) has not been quantified in the context of OPD-CIM arrays.
3. **Organic-specific nonlinearity unaddressed:** OPDs exhibit trap-limited dark current and bias-dependent responsivity that differ from silicon CMOS image sensors. Simple inverse-gamma compensation is insufficient; a **physics-informed or learnable frontend model** is needed.
4. **No benchmark protocol:** There is no standardized evaluation protocol (dataset + illumination augmentation + metric) for comparing optical-electronic co-design strategies in CIM systems.

---

## 4. Feasibility Assessment
- **Technical leverage:** Work 1 already contains a simplified optical frontend model (inverse-gamma compensation) and a CIM simulation pipeline. Extending it to a **differentiable photodiode response block** (e.g., parametric I–V model or a shallow MLP) and connecting it to the CIM simulator is a natural next step.
- **Tooling:** CrossSim (existing project dependency) supports analog CIM simulation with programmable non-idealities. PyTorch/TensorFlow can wrap the frontend model and allow end-to-end backpropagation.
- **Data cost:** Standard vision datasets (CIFAR-10/100, Tiny ImageNet) plus synthetic illumination augmentation (gamma, brightness, contrast) require no new physical fabrication.
- **Risk:** Medium. The main risk is modeling the OPD accurately without access to fabricated devices. Mitigation: use published OPD compact models (Sandberg et al.) and perform sensitivity analysis on trap-state density and responsivity slope.

---

## 5. Preliminary Experiment Design

### 5.1 Objective
Demonstrate that **jointly optimizing photodiode frontend parameters together with CIM array weights** improves classification accuracy and illumination robustness compared to a fixed frontend + standalone CIM backend.

### 5.2 Setup
| Component | Specification |
|-----------|---------------|
| **Dataset** | CIFAR-10 (graduation baseline) + illumination augmentation: γ ∈ [0.3, 3.0], brightness ±50%, contrast ±50% |
| **Optical Frontend** | Parametric photodiode model:
  `I_ph = R(λ,V_bias) · P_opt^γ + I_dark(V_bias,T)`
  where `R` = responsivity, `γ` = sublinearity factor (~0.8–1.2), `I_dark` derived from trap-state model (Sandberg). Frontend parameters are learnable or part of a hyper-parameter search. |
| **Electronic Backend** | Analog CIM macro (SRAM or RRAM-based) simulated in CrossSim or the internal CIM model from Work 1; weights stored as conductance states, ADC quantization included. |
| **Baselines** | (B1) Ideal linear frontend; (B2) Work 1 fixed inverse-gamma compensation; (B3) Fixed frontend + data augmentation only. |
| **Proposed** | (P1) **Co-train:** frontend parameters (γ, V_bias set-points, exposure time) jointly with CIM weights via task loss; (P2) **Adaptive frontend:** a lightweight calibration network (1–2 FC layers) inserted between photodiode and CIM, trained end-to-end. |

### 5.3 Evaluation Metrics
- **Task accuracy** (top-1 %) under nominal illumination.
- **Robustness margin:** accuracy degradation Δacc when illumination γ shifts from 1.0 → 0.4 and 1.0 → 2.5.
- **Energy efficiency:** normalized MAC energy including frontend photocurrent integration time.
- **Physical plausibility:** final learned γ and R values must lie within reported OPD ranges (e.g., γ ∈ [0.85, 1.15], R ∈ [0.1, 0.6] A/W for visible OPDs).

### 5.4 Milestones (tentative)
1. **M1 (Weeks 1–2):** Implement differentiable photodiode response block and integrate with existing CIM simulator. Validate against published I–V curves.
2. **M2 (Weeks 3–4):** Train baselines (B1–B3) on CIFAR-10 with illumination augmentation; record accuracy vs. γ curves.
3. **M3 (Weeks 5–6):** Train proposed co-design variants (P1, P2); quantify robustness margin improvement and energy trade-offs.
4. **M4 (Weeks 7–8):** Ablation study—impact of trap-state dark current, responsivity voltage dependence, and ADC resolution on co-design gains.
5. **M5 (Weeks 9–10):** Draft thesis chapter + one conference paper target (e.g., *IEEE International Electron Devices Meeting* or *Nature Electronics* supplementary letter).

---

## 6. Citation List

1. Jang, H. et al. “In-sensor optoelectronic computing using electrostatically doped silicon.” *Nature Electronics* 5, 519–525 (2022).
2. Vasileiadis, N. et al. “In-Memory-Computing Realization with a Photodiode/Memristor Based Vision Sensor.” *Materials* 14, 5223 (2021).
3. Yang, Y. et al. “In-sensor dynamic computing for intelligent machine vision.” *Nature Electronics* 7, 225–233 (2024).
4. Huang, H. Y. et al. “Fully integrated multi-mode optoelectronic membrane array for diversified in-sensor computing.” *Nature Nanotechnology* 20, 93–103 (2025).
5. Sandberg, O. J. et al. “Mid-gap trap state-mediated dark current in organic photodiodes.” *Nature Photonics* 17, 380–386 (2023).
6. Klinghoffer, T. et al. “DISeR: Designing Imaging Systems with Reinforcement Learning.” *ICCV* (2023).
7. Bian, L. et al. “Physical twinning for joint encoding-decoding optimization in computational optics: a review.” *Light: Science & Applications* 14, 18 (2025).
8. Chen, K. et al. “Organic optoelectronic synapse based on photon-modulated electrochemical doping.” *Nature Photonics* 17, 629–637 (2023).
9. Wu, X. et al. “Wearable in-sensor reservoir computing using optoelectronic polymers with through-space charge-transport characteristics for multi-task learning.” *Nature Communications* 14, 468 (2023).
10. Zhou, G. et al. “Full hardware implementation of neuromorphic visual systems based on multimodal optoelectronic resistive memory array for versatile image processing.” *Nature Communications* 14, 8489 (2023).
11. Chang, C. et al. “Birdlike broadband neuromorphic visual sensor arrays for fusion imaging.” *Nature Communications* 15, 5256 (2024).
12. Chuquimarca, L. E. et al. “Assessing deep learning model robustness for banana ripeness classification under varying illumination conditions.” *Smart Agricultural Technology* 12, 101333 (2025).
13. “Low-power scalable multilayer optoelectronic neural networks enabled with incoherent light.” *Nature Communications* 15, 55139 (2024).
14. Oh, S. W. et al. “Progress of Materials and Devices for Neuromorphic Vision Sensors.” *Nano-Micro Letters* 14, 203 (2022).
15. Li, L. et al. “Spectral nonlinearity of an inverse-layer-type silicon photodiode under over-filled illumination.” *Optics & Laser Technology* 155, 108254 (2022).
16. Teledyne COSMOS team. “Characterization of the Teledyne COSMOS Camera: A Large Format CMOS Image Sensor for Astronomy.” arXiv:2502.00101 (2024).
17. Becker, M. et al. “A surface-normal photodetector as nonlinear activation function in diffractive optical neural networks.” *Optics Express* (2021).
18. Ansari, S. et al. “From material to cameras: low-dimensional photodetector arrays on CMOS.” *Small Methods* (2023).

---

*End of survey. Ready for integration into thesis proposal and Work 2 planning documents.*
