# GEMINI P1/P2 THESIS CHAPTER OUTLINE: IR DROP & SNEAK PATHS

**Reread of canonical state:** This design builds upon the context established in `GEMINI_CONTEXT_REREAD_20260418.md`.

## 1. Background
Organic optoelectronic devices frequently exhibit high on-state conductances to maximize dynamic range and operating speed. However, in dense crossbar arrays, this high conductance dramatically increases the row currents, exacerbating Ohmic voltage drops (IR drop) along the interconnect wires. Furthermore, finite off-state resistances in these organic materials lead to unintended parallel conduction routes (sneak paths) through unselected devices. Unlike traditional silicon CMOS or inorganic RRAM where these parasitics might be secondary at small scales, the specific material properties of organic semiconductors make spatial IR drop and sneak-path interference primary bottlenecks \citep{[TBD_Organic_CIM_IR_Drop], [TBD_Sneak_Path_Arrays], [TBD_OPECT_Scaling_Limits]}. This chapter introduces first-class spatial models to replace the ad-hoc 1% placeholder penalty currently utilized in the compound stress tests.

## 2. Mathematical Model
### Spatial IR Drop
The effective voltage applied to a device at crossbar coordinate $(i, j)$ is dynamically reduced by the cumulative voltage drop along the row and column interconnects.
Let $V_{\text{in}}$ be the ideal input vector, $R_w$ the interconnect wire resistance per cell, and $I(k, j)$ the current drawn by cell $(k, j)$. The effective column-wise drop is formulated recursively or approximated as:
$$ V_{\text{eff}}(i,j) = V_{\text{in}, i} - R_w \sum_{k=1}^{i} I(k, j) $$
This creates a deterministic spatial gradient where devices furthest from the source/sink experience the most severe attenuation.

### Sneak-Path Currents
Due to the absence of perfect selector devices (1T1R/1T1O), unselected cells conduct leakage currents. We model this via a cross-coupling interference matrix $M_{\text{sneak}} \in \mathbb{R}^{N \times N}$, where the observed current $I_{\text{out}, j}$ aggregates legitimate cross-point current and parasitic leakage:
$$ I_{\text{out}, j} = \sum_i \left[ V_{\text{eff}}(i,j) \cdot G(i,j) + V_{\text{leak}} \cdot G_{\text{off}}(i,j) \right] $$
This formulation captures the data-dependent nature of sneak paths.

## 3. Simulator Integration Plan
These models will be integrated directly into `compute_vit/analog_layers.py`.
- **Hook Location:** The spatial IR drop requires input-dependent and weight-dependent dynamic calculation. It must hook into the `forward()` pass of `AnalogLinear` and `AnalogConv2d` *before* the MAC accumulation.
- **Pre-Pass Approximation:** To avoid prohibitive $O(N^3)$ circuit-solving during training, a fast iterative pre-pass will estimate $I(k,j)$ using the ideal $V_{\text{in}}$, which then computes $V_{\text{eff}}$ for the actual forward pass.
- **Profile Interface:** The JSON profile schema will be extended to include:
  - `"R_wire_ohms": 0.5`
  - `"G_off_siemens": 1e-9`
  - `"selector_nonlinearity": 10`

## 4. Experiments to Run
1. **IR-Drop Magnitude Sweep (V4 CIFAR-10):** Evaluate accuracy degradation by varying $R_w \in \{0.1, 0.5, 1.0, 5.0\} \Omega$.
2. **Array-Size Scaling:** Compare the vulnerability of $16 \times 16$ vs $64 \times 64$ vs $256 \times 256$ crossbar partitions under a fixed $R_w$, identifying the maximum safe array size for organic CIM.
3. **Interaction with HAT:** Conduct HAT retraining with the IR-drop model enabled in the forward pass. Test whether the network learns to map critical weights to safer (low IR-drop) spatial coordinates.

## 5. Expected Outcomes & Risks
**Expected Outcomes:** This chapter resolves reviewer pressure P1 and P2 by replacing the 1% arbitrary penalty with a rigorous, physically grounded simulation. We expect accuracy to precipitously drop for $256 \times 256$ arrays unless HAT can actively compensate, establishing a clear array-size ceiling for organic edge-vision.
**Risks:** Simulating spatial IR drop dynamically in PyTorch breaks standard GEMM parallelization. Training times may increase by $5\times - 10\times$.

## 6. Estimated Cost
- **Implementation & Testing (Wall-clock):** 3-5 days.
- **Execution (GPU-hours):** ~120 GPU-hours for the combined sweep and HAT retraining.