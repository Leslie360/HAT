# Paper-2 Candidate Selection (CLAUDE-BQ)

**Date:** 2026-04-20
**Source:** K-V13 deep scope + G-DD8 venue fit + G-DD9 industrial brief

## Decision: Route R-A — Joint MLP-linear + Ensemble HAT deployment-grade result

### Rationale (1 page)

**1. Risk/reward is optimal.** R-A requires ~95 GPU-hours (verified on RTX 5070 Ti in <1 week) and has a clear binary success criterion: ≥80% fresh-instance accuracy under severe NL (NL=2.0). Success means breaking the 32% ceiling that has defined the hardest open boundary in the thesis. Failure is also publishable: it would establish a fundamental incompatibility between first-order NL surrogates and distributional training, which is itself a significant negative result for the field.

**2. No external dependencies.** Unlike R-B (needs LLM infrastructure, KV-cache redesign, 2,500+ GPU-hours) or R-C (needs theoretical collaborator for formal proofs), R-A uses only existing compute_vit code + the CX-GA warm-start fix. It can begin the day after the NC submission ships.

**3. Venue fit is strong.** Nature Electronics (5/5 fit per G-DD8) is the ideal target: device-aware training with deployment-grade validation is squarely in their scope. NeurIPS-Hardware is a co-lead fallback. Either venue is higher-impact than a second NC, and both are distinct enough from NC #1 to avoid self-plagiarism concerns.

**4. Industrial relevance is immediate.** Per G-DD9, the ≥80% target directly translates to "yield tolerance under severe process nonlinearity" — a question every analog-CIM product manager asks. NVIDIA-internal adoption of the protocol becomes plausible if we can demonstrate joint mitigation.

**5. Thesis integration is seamless.** R-A is literally the thesis punchline (Chapter 8, §1). Elevating it to Paper-2 requires only a results section + revised introduction, not a new research program.

### Fallback: Route R-C

If R-A fails to reach ≥50% (confirming fundamental incompatibility), pivot to R-C (theory-only HAT-as-regularizer + ensemble-frequency effective width). This uses the failure data as evidence for the theoretical bound and requires ≤20 GPU-hours for validation. Target: COLT or NeurIPS Theory track.

### Deferred: Route R-B

R-B (organic-RRAM LLM CIM scaling) is explicitly deferred to Round P or a future grant cycle (Aim 2 of G-DD7). It requires infrastructure we don't have (LLM checkpoint compatibility, KV-cache analog mapping) and 25× the compute of R-A. Revisit once R-A succeeds and R-C is either published or rejected.

### Next action

Stage R-A experimental protocol as the first task of Round P. Trigger: NC submission accepted or revision cycle begins.
