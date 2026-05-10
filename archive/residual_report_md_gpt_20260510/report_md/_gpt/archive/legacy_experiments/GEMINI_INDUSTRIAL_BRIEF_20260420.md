# Compute-ViT Industrial Positioning Brief
**NVIDIA Apamayo — Organic CIM Readiness Assessment**
*Date: 2026-04-20 | Classification: Internal Use*

---

## 1. Executive Summary

- **What it is.** Compute-ViT is a simulation-first framework that quantifies how vision-transformer inference accuracy degrades under analog compute-in-memory (CIM) non-idealities — specifically device-to-device (D2D) mismatch in organic/printable crossbar arrays.
- **Why NVIDIA cares.** Organic CIM promises ultra-low-cost, large-area inference for edge and sensor-near applications, but D2D variance has been the primary blocker to productization. This work provides the first yield-accuracy map for ViT workloads on emerging analog fabrics.
- **Bottom line.** We now have a go/no-go decision framework and a proven mitigation strategy (ensemble hardware-aware training) that recovers the majority of accuracy loss without re-fabricating chips.

---

## 2. Key Claims & Industrial Translation

| Academic Claim | Industrial Translation |
|---|---|
| **Ensemble HAT recovers 86% fresh-instance accuracy.** | **Yield tolerance:** Chips with up to 10% D2D variance still ship with <2 pp accuracy loss. Product-grade inference without binning or rework. |
| **Correlated D2D causes bounded, not catastrophic, degradation.** | **Spatial correlation (e.g., from wafer-level processing) does not catastrophically kill model performance.** Degradation is predictable and stays within recoverable margins. |
| **MLP-linear diagnostic isolates dominant error source.** | **Pinpoint yield loss:** We can tell whether accuracy drops come from MLP blocks or attention blocks, directly guiding redundancy and repair strategy. |
| **Deployment envelope defines accuracy-variance trade-offs.** | **Go/no-go framework for product managers:** Clear maturity tiers let teams decide when organic CIM is ready for a given SKU, reducing speculation. |

---

## 3. TCO Impact

- **Fewer retraining cycles.** Ensemble HAT trains once and generalizes across D2D distributions; no per-chip or per-wafer retraining required.
- **Higher effective yield.** 10% D2D tolerance expands the shippable device population, cutting scrap and improving wafer economics.
- **Faster time-to-market.** Pre-silicon accuracy envelope eliminates months of post-fabrication model tuning and re-spin risk.

---

## 4. NRE Savings

- **Simulation-first validation** replaces expensive mask iterations and test-chip runs for early process nodes.
- **Architecture-technology co-design** happens in Python, not in silicon — enabling rapid exploration of redundancy schemes, bit-widths, and array sizes before any layout effort.
- **Reduced characterization burden:** The diagnostic separates MLP-dominated from attention-dominated error regimes, so teams invest metrology only where it matters.

---

## 5. Collaboration Model

- **Integrate into existing analog-CIM toolchain.** Compute-ViT plugs in as a statistical mismatch generator and accuracy estimator alongside SPICE-based array models.
- **Use as a pre-silicon validation layer.** Run during PDK development to set D2D specs before tape-out; run during product planning to validate SKU feasibility.
- **Recommended path:** Pilot with one edge-ViT SKU, align ensemble HAT training with the current PyTorch analog training stack, and feed measured organic-array statistics back to refine the simulation envelope.

---

## 6. Caution Flags — What Is NOT Ready

- **No SPICE-level validation.** Array models are behavioral; transistor-level non-idealities (line resistance, sneak paths) are not included.
- **No temperature model.** All results assume nominal temperature; thermal drift in organic semiconductors remains uncharacterized.
- **No foundry PDK.** Organic processes lack standardized design kits; absolute numbers (e.g., 10% D2D) are representative, not node-specific.
- **Single workload scope.** Claims are proven on CIFAR-10 ViT only; larger datasets and different architectures require extension.

---

*For questions, contact the Compute-ViT team at NVIDIA Apamayo.*
