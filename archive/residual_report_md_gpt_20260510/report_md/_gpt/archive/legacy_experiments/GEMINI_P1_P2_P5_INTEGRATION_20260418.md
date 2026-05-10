# GEMINI P1/P2/P5 INTEGRATION — 2026-04-18

**Reread of canonical state:** I have re-read the three newly drafted thesis outlines (`GEMINI_P1_P2_IRDROP_SNEAK_THESIS_OUTLINE_20260418.md`, `GEMINI_P5_THERMAL_THESIS_OUTLINE_20260418.md`, and `GEMINI_E6_THESIS_CHAPTER_OUTLINE_20260418.md`). These cover spatial IR drop/sneak paths, temperature coefficients, and the $\gamma \times \text{NL}$ interaction sweep.

## 1. Recommended Structure
**Recommendation:** A single, integrated chapter titled *"Toward Circuit-Aware Simulation: Co-Optimizing Spatial, Thermal, and Optical Non-Idealities."*

**Argument for Single Chapter:** The power of these models lies in their interaction. High temperatures (P5) worsen wire resistance, which directly exacerbates spatial IR drop (P1). Furthermore, thermal shifts in $\gamma_{\text{phys}}$ interact directly with the $\gamma$ compensation sweep in E6. Treating them as three independent chapters forces redundant explanations of the simulator's forward-pass hooks and hides the compound stress limits that matter most to systems engineers.

**Argument for Independent Chapters:** It allows for deeper, isolated analytical focus without the confounding variables of multi-physics interactions. However, this reads more like a catalog of features than a cohesive scientific narrative.

## 2. Shared Mathematical Scaffolding
An integrated chapter allows us to define a unified "Circuit-Aware Forward Pass" early on:
- **Unified Profile Interface:** Extending the JSON schema once with `"R_wire_ohms"`, `"G_off_siemens"`, `"T_op"`, and thermal coefficients (`"T_coeff_gamma"`, etc.).
- **Coupled Variables:** Defining $R_w(T) = R_{w, 300\text{K}} \cdot (1 + \alpha_R (T - 300))$ so that the IR-drop equations automatically inherit thermal state.
- **Combined Forward Hook:** The simulator applies sublinear photoresponse $P_{\text{in}}^{\gamma(T)}$, calculates the spatial $V_{\text{eff}}(i, j)$ pre-pass, injects thermal $\sigma_{\text{D2D}}(T)$, and accumulates sneak leakage, culminating in a single highly realistic `AnalogLinear` projection.

## 3. Cross-Experiment Dependencies
To build the narrative logically, the execution order must be strict:
1. **Isolated Thermal Sweep (P5):** Establish the baseline temperature sensitivity of the array assuming perfect interconnects.
2. **Isolated Spatial Sweep (P1/P2):** Establish the array-size ceiling ($16 \times 16$ vs $256 \times 256$) assuming a stable $300\text{K}$ environment.
3. **Coupled Thermal-Spatial Stress:** Run the $256 \times 256$ array at $350\text{K}$. This reveals the compound failure mode where elevated resistance destroys the spatial voltage distribution.
4. **$\gamma \times \text{NL}$ Interaction (E6):** Finally, apply the inverse-gamma and MLP-linear mitigations on top of the newly established circuit-aware baseline to see if software mitigations can rescue a physically hostile crossbar.

## 4. Total Cost Estimate
- **Implementation (Wall-clock):** ~1 week to unify the hooks and validate the coupled physics.
- **Compute (GPU-hours):**
  - P5 (Thermal): ~15 h
  - P1/P2 (Spatial): ~120 h
  - Coupled Stress: ~30 h
  - E6 (Joint Sweep): ~200 h
  - **Total:** ~365 GPU-hours (Requires ~2-3 weeks of background queuing on the RTX 5070 Ti).

## 5. Risk Register
1. **Risk:** *Forward-pass Simulation Bottleneck.* Spatial IR drop breaks $O(1)$ matrix multiplications, slowing training dramatically.
   - **Mitigation:** Use a fast 1-iteration Jacobi approximation for $V_{\text{eff}}$ during training, reserving the precise solver for inference-only evaluation.
2. **Risk:** *Parameter Space Explosion.* Tuning $T$, $R_w$, $\gamma$, and NL simultaneously makes it impossible to pinpoint why a model collapsed.
   - **Mitigation:** Adhere strictly to the execution dependency order (Section 3), isolating single variables before running compound cells.
3. **Risk:** *Reviewer Backlash on Unverified Models.* Coupling unmeasured placeholders (like arbitrary $R_w$ thermal coefficients) might invite criticism that the simulator has become disconnected from physical reality.
   - **Mitigation:** Strictly bound the parameter ranges using the literature citations collected in the Chapter 2 background review, and heavily caveat that these are "worst-case limit" explorations.
