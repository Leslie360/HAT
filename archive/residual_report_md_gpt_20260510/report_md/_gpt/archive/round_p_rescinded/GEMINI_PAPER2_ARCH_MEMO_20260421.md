# Paper-2 Architectural Design Memo
*Date: 2026-04-21 | Story: Structural Limits of Analog CIM for ViT*

---

## 1. Narrative Arc
The paper opens by reframing the conversation: instead of asking whether analog compute-in-memory (CIM) can run vision transformers (ViTs), we ask *where* it fundamentally breaks. **Section 1** (Introduction) establishes the tension—ViTs’ dynamic attention maps and high weight reuse are kryptonite for static, noise-prone analog arrays. **Section 2** (Preliminaries) recaps the joint-training framework from Paper-1, but only as a chassis. **Section 3** introduces the diagnostic taxonomy: three mitigations (source-aware training, fresh-weight injection, noise-aware attention scaling) and three diagnostic axes (capacity, pathway sensitivity, deployment envelope). **Section 4** presents the three-mitigation convergence study, proving that no combination fully closes the accuracy gap. **Section 5** dissects the attention pathway via mechanism analysis, isolating the softmax/QK-dot-product bottleneck. **Section 6** runs the full diagnostic sweep (CX-J1b/c/d), quantifying the ceiling. **Section 7** synthesizes the structural limits into a deployment envelope. **Section 8** concludes with a hard directive: analog CIM for ViTs requires architectural co-design, not just circuit-level fixes. The arc is a tightening spiral: from broad hypothesis → targeted mechanism → irreducible limit.

---

## 2. Figure Plan

| Fig | Title | Visual Directive |
|-----|-------|------------------|
| **1** | **Framework Schematic** *(Reuse Paper-1)* | **DO NOT REDRAW.** Use the exact Paper-1 schematic but gray-out the training loop and highlight the inference diagnostic probe in **red**. Signals continuity without rewriting history. |
| **2** | **Three-Mitigation Convergence** | Grouped bar chart (y: ImageNet-1k top-1; x: mitigation combos) capped by a horizontal “FP32 ceiling” line. **Color rule:** desaturated blues for individual mitigations, warning-orange for the combined stack, dashed red line for the ceiling. *Story:* the gap that refuses to close. |
| **3** | **Attention-Pathway Mechanism** *(from G-FF1)* | Sankey-style flow: Q/K/V projection → analog array → noise injection → softmax → output. Annotate three breakpoints with **lightning-bolt** icons: (i) QK-dot noise amplification, (ii) softmax dynamic-range collapse, (iii) post-softmax weight corruption. **Severity color-code:** red > orange > yellow. |
| **4** | **Diagnostic Sweep CX-J1b/c/d** *(Placeholder)* | 2×2 matrix of mini-plots. Rows: capacity (J1b) vs. pathway (J1c). Columns: accuracy degradation vs. energy-delay product. **LOCK AXIS RANGES NOW**—y-acc 0–100%, y-EDP log scale. Leave data panels blank; prevents scope creep. |
| **5** | **Deployment Envelope / Decision Diagram** | Ternary-threshold diagram. Axes: device noise (%), array size (kb), attention-head count. Contours: “Viable,” “Marginal,” “Prohibited.” **Visual rule:** “Prohibited” must occupy ≥60% of the plot. Call-out boxes: “Today’s RRAM” (Marginal) and “Projected PCM” (Viable). |

---

## 3. Table Plan

| Table | Title | Directive |
|-------|-------|-----------|
| **1** | **Device Profile Parameters** | 4-column compact table: Device (RRAM, PCM, FeFET, SRAM-CIM), Noise σ (%), Endurance (cycles), Array Size (kb). **Rule:** Source every cell from CrossSim physical models; no speculative numbers. |
| **2** | **Mitigation Comparison (Source vs. Fresh)** | 3 rows × 4 cols. Rows: Source-Aware Training, Fresh-Weight Injection, Noise-Aware Attention Scaling. Columns: Accuracy Gain (Δ%), Hardware Overhead (relative), Scalability (Yes/No). **Use binary heatmap (green/red) for Scalability.** Argument: gains are isolated, overheads are cumulative. |
| **3** | **Statistical Summary (SEM, CI, Power)** | Final results for CX-J1b/c/d. Columns: Diagnostic, n (runs), Mean Acc (%), SEM, 95% CI, Statistical Power (1−β). **Pre-format now; populate after final sweep.** Power must be ≥0.80 for all claims. |

---

## 4. Venue-Fit Argument
This story belongs in **Nature Electronics**, not NeurIPS-Hardware or *Nature Communications*. NeurIPS-Hardware rewards algorithmic novelty and training recipes; our pivot to *structural limits* is fundamentally a device-circuit-system co-design argument that lives downstream of algorithm invention. *Nature Communications* demands breadth across disciplines, but our narrative is laser-focused on one hardware paradigm (analog CIM) and one workload (ViT), which risks seeming narrow. *Nature Electronics* occupies the exact intersection: it publishes the physics of frustration—where device non-idealities meet system architecture and force a hard boundary. The mechanism-level diagnosis (Fig. 3) and the deployment envelope (Fig. 5) are native idioms for that audience.

---

## 5. Risk Assessment
If CX-J1b/c/d *breaks the ceiling*—i.e., a mitigation combination unexpectedly pushes accuracy within 1% of FP32—the paper survives by morphing from a *limit* study into a *conditional viability* study. The diagnostic framework itself (the taxonomy, the mechanism diagram, the envelope) becomes the contribution, while the results shift from “impossible” to “requires these exact conditions.” We retain the narrative arc by reframing Section 7: instead of a “Prohibited” zone, we draw a “Goldilocks” zone. The risk is not existential; it is tonal. **Directive:** Pre-write two concluding paragraphs now—one for the ceiling, one for the breakthrough—and lock them as alternatives. The paper’s survival clause is that the framework is agnostic to the sign of the result.

---
*End of memo. Word count target: ≤800. Lock figure axis ranges and table schemas before any data collection begins.*
