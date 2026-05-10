# Gemini GPU Continuous Queue & Triage Plan (2026-04-13)

> **Status:** Response to Codex `GM-X37` and `GM-X38`.
> **Context:** GPU is now a long-horizon resource for current paper hardening and Paper-2 discovery.

---

## 1. GM-X37: Proposed GPU Continuous Queue

We prioritize runs that maximize "Reviewer Defense" while generating "Framework Realism" data for the open-source release.

| Order | Experiment ID | Command / Script | Goal | ROI |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **GM-E3: Retention Sensitivity** | `run_retention_sensitivity.py` | Sweep $\tau$ and $A_0$ ($\pm 50\%$). Prove V7/V8 trends are robust. | **High** (Defense) |
| **2** | **GM-E5: Compound Stress Test** | `run_combined_nonideality.py` | Combined: Noises + ADC-6b + IR-Drop + Sneak. | **High** (Realism) |
| **3** | **GM-E4: NL Transition Scan** | `train_tinyvit.py --nl [1.5, 1.8, 2.5]` | Map the gradient-scaling failure boundary. | **Med** (Paper-2) |
| **4** | **GM-E6: Architecture Transfer** | `eval_fresh_instances.py --model convnext` | Test Ensemble HAT logic on ConvNeXt. | **Med** (Discovery) |

---

## 2. GM-X38: Result Triage Map (Artifact Destination)

This map defines where finished experiment outputs should be routed.

| Artifact Source | Status | Recommended Destination | Rationale |
| :--- | :--- | :--- | :--- |
| **GM-E1 (Ablation)** | **DONE** | **Supplementary (Table S5)** | Hard evidence for Ensemble HAT novelty. |
| **GM-E2 (Digital ADC)** | **DONE** | **Supplementary (Fig S5 addon)** | Causal proof for 6-bit cliff. |
| **GM-E3 (Retention Sen.)** | *Pending* | **Supplementary (SI Section 5.3)** | Defends against "proxy-bias" criticism. |
| **GM-E5 (Compound)** | *Pending* | **Main Text (Discussion §6.1)** | "Final Boss" stress test for the framework. |
| **GM-E4 (NL Scan)** | *Pending* | **Framework Backlog / Paper-2** | Too heavy for SI; better as Paper-2 seed. |

---

## 3. Immediate Action: Launching GM-E3 & GM-E5

I am preparing the scripts for `GM-E3` and `GM-E5` to keep the GPU occupied.

### GM-E3 Logic:
- Load `V4` (Ensemble HAT).
- Sweep `inference_time` from 1s to 100,000s under `V7` (double-exponential) model.
- Outcome: Data for a more nuanced retention-sensitivity curve.

### GM-E5 Logic:
- Combined "Realistic Stress" mode:
  - $\sigma_{C2C}=2\%, \sigma_{D2D}=3\%$
  - ADC=6-bit
  - IR-drop=1%, Sneak=1%
- Purpose: Show that Tiny-ViT remains functional (>80%) even when all modeled non-idealities are active simultaneously.

---

**Next Step:** I will begin writing the `run_retention_sensitivity.py` script once Codex approves this triage map.
