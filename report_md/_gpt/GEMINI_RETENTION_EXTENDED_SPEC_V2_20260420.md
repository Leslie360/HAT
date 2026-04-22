# G-DD2: Retention-Extended Experimental Spec v2

## 1. Current State
TinyViT V4 + Ensemble HAT on CIFAR-10 shows a characteristic two-phase retention decay under the canonical double-exponential model (τ₁≈140 ms, τ₂≈10 s, A₀=0.6):

| Time (s) | Accuracy |
|---|---|
| 0 | 91.63% |
| 1 | 82.66% |
| 10 | 79.13% |
| 100 | 79.05% |
| 1 000 | 79.35% |
| 10 000 | 79.51% |

A **stable plateau at 79.13–79.51%** is reached by t=10 s and persists through 10 000 s (~2.8 h). Existing measurements cover 0–10⁴ s. The residual conductance fraction A₀=0.6 sets a hard asymptotic floor in the present model.

## 2. Extended Protocol
### Direct timepoints
Extend the inference-time sweep to:
- **1 h** (3 600 s)
- **1 d** (86 400 s)
- **1 wk** (604 800 s)
- **1 mo** (~2.6×10⁶ s)

Retain 10 Monte-Carlo runs per point; increase to 30 MC for t≥1 d to tighten variance on the flat tail.

### Accelerated-aging proxy
Direct 1-month measurement is impractical. Propose a **temperature-stress protocol**:
- Stress arrays at 60 °C and 85 °C.
- Assume Arrhenius acceleration with Eₐ≈0.3–0.5 eV (typical for organic phototransistors).
- Back-calculate equivalent room-temperature time: τ_room = τ_stress × exp[Eₐ/k_B (1/T_room − 1/T_stress)].
- Validate by comparing the 60 °C/1 h stressed point against the already-measured 3 600 s room-temperature datum.

### Profile parameter
Add `retention_hours: float` to `DeviceProfile` as a user-facing target. Internally map it to the existing `(tau_1, tau_2, A_0)` triple, or to a fitted third-order decay when extended data becomes available.

## 3. Success Criterion
Under the current double-exponential model, **no ranking collapse is predicted**—the 79% plateau is the asymptotic limit. The Ensemble HAT margin over the standard-HAT retention baseline (~19%) remains >60 pp.

If an unmodeled slow mode τ₃ exists, a practical bound can be set: **ranking collapse occurs if accuracy drops below ~60%**, the approximate floor where the analog–digital gap becomes deployment-unviable. The observed 10 s–10⁴ s flatness argues against a 9 pp drop on the one-month horizon.

## 4. Compute Estimate
| Phase | Config | GPU-hr (1×A100) |
|---|---|---|
| Direct sweep (4 points, 30 MC each) | 1 checkpoint, CIFAR-10 | ~0.2 |
| Accelerated-aging validation (3 T × 2 t) | Same checkpoint | ~0.1 |
| **Total screening** | — | **≤0.3** |

## 5. Open Question
Is the 79% plateau a **fundamental device+architecture limit**, or can a stronger HAT variant push through it? Candidates to test:
- **Higher ensemble frequency** (currently capped by programming overhead).
- **Joint MLP–attention training** (CODEX G-JT1 pilot shows fresh-instance gains; retention translation is untested).
- **State-dependent recalibration** (§6.6 deferred adaptive calibration).

If any candidate shifts the asymptote above ~82%, the retention narrative changes from "acceptable floor" to "near-clean recovery."
