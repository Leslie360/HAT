# Compute-ViT Industrial Partnership Brief v2
**NVIDIA Apamayo — Organic CIM Pre-Silicon Risk Assessment**
*Date: 2026-04-21 | Classification: Internal Use*

---

## 1. Executive Summary

- **What it is.** Compute-ViT is a pre-silicon risk-assessment framework that prevents wasted NRE by quantifying how vision-transformer inference accuracy degrades under analog compute-in-memory (CIM) non-idealities — specifically device-to-device (D2D) mismatch in organic/printable crossbar arrays.
- **Why NVIDIA cares.** Organic CIM promises ultra-low-cost, large-area inference for edge and sensor-near applications, but D2D variance has been the primary blocker to productization. This work provides the first yield-accuracy map for ViT workloads on emerging analog fabrics.
- **Bottom line.** We now have a maturity-zone classifier that tells you whether your process node is in the production-viable band, the marginal band, or the do-not-ship zone — before you spend a dollar on masks.

---

## 2. Key Claims & Industrial Translation

| Claim | Industrial Translation |
|---|---|
| **Ensemble HAT at NL=1.0 → 86% fresh-instance accuracy.** | **Production-viable zone.** Chips with moderate D2D variance ship with <2 pp accuracy loss. Product-grade inference without binning or rework. |
| **Severe NL (NL≥2.0) → ~30% accuracy ceiling.** | **Do-not-ship zone.** Process nodes exhibiting severe mismatch cannot be rescued by training tricks alone. Hard no-go decision before tapeout. |
| **The framework classifies your process maturity zone before tapeout.** | **Pre-silicon risk gate.** Run compute-ViT against your PDK mismatch specs to determine viability, avoiding late-stage kills. |

---

## 3. TCO Impact

1. **Avoid one failed tapeout = save $2–5M NRE.** Compute-ViT kills unviable SKUs during PDK review, not after first silicon.
2. **Fewer retraining cycles.** Ensemble HAT trains once and generalizes across D2D distributions; no per-chip or per-wafer retraining required.
3. **Higher effective yield.** 10% D2D tolerance expands the shippable device population, cutting scrap and improving wafer economics.
4. **Faster time-to-market.** Pre-silicon accuracy envelope eliminates months of post-fabrication model tuning and re-spin risk.

---

## 4. NRE Savings

- **Simulation-first decision making.** Compute-ViT replaces expensive mask iterations and test-chip runs for early process nodes by establishing a viability gate before any layout effort.
- **Architecture-technology co-design** happens in Python, not in silicon — enabling rapid exploration of redundancy schemes, bit-widths, and array sizes before committing to tapeout.
- **Reduced characterization burden.** The diagnostic separates MLP-dominated from attention-dominated error regimes, so teams invest metrology only where it matters.

---

## 5. Collaboration Model

- **Integrate compute-ViT into NVIDIA's pre-silicon validation pipeline.** Use the framework as a statistical mismatch generator and accuracy estimator alongside SPICE-based array models during PDK development.
- **Use as a pre-silicon risk gate.** Run during PDK development to set D2D specs before tape-out; run during product planning to validate SKU feasibility.
- **Recommended path.** Pilot with one edge-ViT SKU, align ensemble HAT training with the current PyTorch analog training stack, and feed measured organic-array statistics back to refine the simulation envelope.

---

## 6. Caution Flags — What This Is (and Is Not)

- **Not a chip predictor.** Compute-ViT does not predict the exact accuracy of any individual die. It tells you whether your device specs fall in the viable, marginal, or do-not-ship zone.
- **No SPICE-level validation.** Array models are behavioral; transistor-level non-idealities (line resistance, sneak paths) are not included.
- **No temperature model.** All results assume nominal temperature; thermal drift in organic semiconductors remains uncharacterized.
- **No foundry PDK.** Organic processes lack standardized design kits; absolute numbers (e.g., 10% D2D) are representative, not node-specific.
- **Single workload scope.** Claims are proven on CIFAR-10 ViT only; larger datasets and different architectures require extension.

---

*For questions, contact the Compute-ViT team at NVIDIA Apamayo.*
