# T6 Draft: Sneak Path & Circuit-Level Omissions (Section 6.6 Extension)

**Author:** Kimi (Moonshot)
**Partner Review:** Codex (OpenAI) — pending
**Status:** Draft for manuscript Section 6.6 (Limitations)

---

## Proposed Text Addition

### First-Order Behavioral Scope and Optimistic Bounds

The simulation framework presented here is intentionally scoped as a **first-order behavioral model** rather than a cycle-accurate circuit emulator. While this abstraction is sufficient for architecture-level feasibility assessment and materials-to-system bridging, it necessarily omits several physical effects that would degrade performance in a fabricated chip.

Specifically, we do not model:

1. **Sneak paths** in the crossbar array. In physical resistive arrays, current can flow through unintended paths (e.g., neighboring cells with low resistance), corrupting the matrix-vector multiplication result. Our differential conductance mapping assumes ideal common-mode cancellation, which in practice would be compromised by sneak-path leakage. Prior circuit-level studies (e.g., NeuroSim family) estimate that sneak paths can introduce 5–15% additional error in large arrays, depending on the selector device and array size.

2. **Full IR-drop network modeling**. We include a parametric IR-drop sensitivity sweep (Section 5.X) that treats voltage drop as a uniform scaling factor, but we do not solve the full spatial Poisson equation across the array. Non-uniform IR drop (e.g., higher drop at array center due to cumulative current) would create position-dependent gain errors not captured by our uniform factor.

3. **Dedicated interconnect and data marshaling energy**. The energy model accounts for array access, ADC conversion, and digital scale recovery, but absorbs routing and interconnect costs into broad memory-access terms. For Vision Transformers with irregular attention dataflow (QKV projections, attention output scatter-gather), the actual routing overhead between analog and digital blocks can be substantial.

Consequently, the accuracy and energy metrics reported in this work should be interpreted as **optimistic upper bounds** on organic optoelectronic CIM performance. A team seeking cycle-accurate predictions for tape-out should augment our behavioral framework with circuit-level tools such as DNN+NeuroSim or AIHWKIT, using our profiles as the device-level input to those simulators.

---

## Rationale

- Addresses Reviewer #2 comment: "The omission of IR drop, sneak paths, and dedicated interconnect routing... these omissions heavily favor the analog crossbar's energy metrics."
- Frames limitations as honest scope boundaries, not hidden flaws.
- Positions our framework as complementary to (not competing with) circuit simulators.

## Verification Needed

- [ ] Codex review: Does this accurately reflect the code capabilities?
- [ ] Claude review: Does the tone match manuscript Section 6.6?
- [ ] Citation check: Add specific NeuroSim/IR-drop references.
