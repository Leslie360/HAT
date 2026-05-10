# Reviewer-Suggester Prep Brief

Target: 3–5 anonymous reviewer slots for manuscript on organic-CIM ViT acceleration via mixed-precision Ensemble HAT.

1. **Organic/RRAM Device Physicist** — Validates literature-derived C2C/D2D noise, retention drift, and nonlinearity bounds. *Nature Electronics, IEDM, Advanced Materials.* Would check proxy-calibrated parameters against measured device data and judge whether the uniform-noise approximation is physically justified.

2. **ViT Quantization & Attention Architect** — Validates mixed-precision claims and ADC/softmax sensitivity. *NeurIPS, ICLR, IEEE TVLSI.* Would assess whether the 6-bit ADC cliff and per-layer bit-width assignments are fundamental or artifacts, and whether attention-collapse warnings are contextualized against PTQ4ViT/Q-ViT baselines.

3. **CIM Hardware-Aware Training Methodologist** — Validates Ensemble HAT novelty and training overhead. *ISSCC, ISCA, IEEE Micro.* Would evaluate whether ensemble resampling with static-array deployment is a credible HAT strategy and whether the ~1.00× wall-clock claim is fair.

4. **Simulation Framework & Benchmarking Expert** — Validates CrossSim comparison protocol. *ACM TODAES, DAC, IEEE TCAD.* Would judge head-to-head baseline fairness, analog noise fidelity, and transparent disclosure of simulator-scoped limitations.

5. **Edge-AI Systems & Energy Modeling Researcher** — Validates energy model and deployment framing. *MICRO, HPCA, IEEE JSSC.* Would test whether the energy gain survives routing-overhead bounds and whether ADC/DAC assumptions hold at the system level.
