# Pre-Submission Red-Team v2 (Post-Pivot)

**Date:** 2026-04-21
**Scope:** Hostile review of the post-pivot manuscript. Maximally critical.

---

## Attack 1: The Negative Result Is Convenient

**Attack:** You just didn't train long enough—try 500 epochs and that ~30% ceiling will vanish.

**Severity:** MAJOR

**Defense:** The manuscript reports ~30% fresh-instance plateaus across MLP-linear, all-linear, and joint recipes, with curves flatlining before epoch 100; the 32.12% MLP-only result never climbs even as source accuracy hits 87.79%. This is an optimization barrier, not a budget shortage.

**Action item:** Add a supplementary figure showing epoch-wise curves for severe-NL ablations and state the epoch count at which each run stopped improving.

---

## Attack 2: The Simulator Is Wrong

**Attack:** Your first-order surrogate is too crude to claim anything about a "structural limit."

**Severity:** CRITICAL

**Defense:** §4.5 already calls the first-order surrogate a gradient-scaling approximation and lists higher-fidelity modeling as future work; the ceiling is scoped as a bound contingent on surrogate fidelity, not a hardware law. Still, the abstract and title risk overclaiming by using "structural" without this caveat.

**Action item:** Weaken abstract language from "structural limit" to "surrogate-bound ceiling" and add a Discussion sentence stating the ~30% threshold is an upper bound that may shift under higher-order write dynamics.

---

## Attack 3: The Attention Argument Is Post-Hoc

**Attack:** You didn't predict the attention pathway would dominate before running CX-J1—you made it up after seeing the data.

**Severity:** MAJOR

**Defense:** The manuscript frames the attention bottleneck as a diagnosis from the CX-J1 ablation suite, and the falsification subsection states testable predictions before higher-order experiments. However, the main text blurs the line between post-hoc explanation and pre-registered hypothesis.

**Action item:** Add a "Pre-registered Predictions" paragraph to §3.8 or Supplementary Methods timestamping which attention-pathway hypothesis was formed before versus after CX-J1b/c results.

---

## Attack 4: The ~30% Ceiling Is Meaningless

**Attack:** CIFAR-10 is too easy—on ImageNet this would be 0.1%, so your ceiling has no predictive value.

**Severity:** MAJOR

**Defense:** The manuscript deliberately scopes to edge-scale datasets and uses CIFAR-10/100 scaling to show HAT recovery grows with task grain; the severe-NL ceiling is a relative collapse on the same benchmark where Ensemble HAT achieves 86%, not an ImageNet claim. No large-scale validation leaves generality unsupported.

**Action item:** Add one sentence to §4.5 Limitations predicting that ImageNet-scale deployment would likely fall below the CIFAR-10 ceiling due to deeper attention stacks, and cite this as thesis-follow-up work.

---

## Attack 5: No Silicon Validation

**Attack:** You claim "structural" but you've never touched a real chip, so this is all fantasy.

**Severity:** CRITICAL

**Defense:** The manuscript never claims silicon validation; it is framed as a behavioral simulation study and the Discussion labels conclusions as "first-order upper-bound-like estimates." Yet "structural" may be read as a physical claim about fabricated hardware.

**Action item:** Replace every instance of "structural limit" in the main text with "surrogate-bound limit" or "first-order ceiling," and add a Limitations bullet stating silicon validation is required before transferring the bound to real arrays.

---

## Attack 6: The Paper Is Two Papers

**Attack:** Ensemble HAT (positive) and the structural limit (negative) don't belong together—you're stitching unrelated findings.

**Severity:** MINOR

**Defense:** Both results share the same simulator and training framework; the limit narrative explains why Ensemble HAT works (it bypasses instance overfitting) and why it stops working (the NL=2.0 barrier), creating a coherent accuracy-regime map. The tension is more narrative than scientific.

**Action item:** Redraw Figure 1 or the graphical abstract as a two-axis diagram (noise severity × mitigation strategy) showing positive and negative results as complementary quadrants of the same design space.

---

## Attack 7: Not Novel Enough

**Attack:** Everyone already knows analog nonlinearity destroys accuracy—what's actually new here?

**Severity:** MAJOR

**Defense:** The novelty is quantifying the *pathway-specific* failure geometry—attention-side linearizations collapse while MLP-side linearizations recover, and ensemble training on D2D masks rescues fresh-instance transfer—rather than merely saying nonlinearity hurts accuracy. The Related Work section must make this distinction razor-sharp for skimming reviewers.

**Action item:** Sharpen the Related Work contrast paragraph to cite at least one prior work that reported analog-nonlinearity loss without pathway decomposition, and explicitly state that this paper is the first to isolate the attention mechanism as the rate-limiting factor in a ViT-CIM system.

---

## Final Verdict

**Major revisions needed before submission.**

The CRITICAL attacks on simulator fidelity (2) and silicon absence (5) are addressable by language-level hedging, but not as written. Until "structural" is systematically defanged to "surrogate-bound," a hostile reviewer will treat the ceiling claim as overreach. The MAJOR attacks on training duration (1), post-hoc reasoning (3), dataset scale (4), and novelty (7) each require one paragraph or figure to disarm. Attack 6 is MINOR and fixable with a single conceptual diagram. None require new experiments. Once language is tightened and the graphical abstract reframed, the manuscript becomes submission-ready.
