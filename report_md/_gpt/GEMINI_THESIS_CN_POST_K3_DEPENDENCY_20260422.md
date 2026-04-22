# G-DR2: Thesis CN Dependency Map for Post-K3 Landing
**Date:** 2026-04-22

Map of Chinese thesis chapters requiring updates when `K3 delta_g_eff=0.25` final lands.

| Target File | Section Topic | Can Update Now? | Depends on `K3-0p25`? | Replacement Style |
| :--- | :--- | :--- | :--- | :--- |
| `chapter_1_introduction.tex` | Core Contribution Summary | yes | no | interpretation swap (bimodal basin) |
| `chapter_2_related_work.tex` | Analog Training Frameworks | yes | no | no change needed |
| `chapter_3_methodology.tex` | Higher-Order STE Math | yes | no | no change needed |
| `chapter_4_benchmarks.tex` | NLP=1.0 and FP32 Baselines | yes | no | no change needed |
| `chapter_5_failure_modes.tex` | J1b/c/d/K2 Bimodal Basin | yes | no | interpretation swap (incorporate 38.95%) |
| `chapter_5_failure_modes.tex` | K3 dg_eff Sweep Analysis | no | yes | number swap & interpretation swap |
| `chapter_5_failure_modes.tex` | K4/K5 Surrogate Fidelity | yes | no | interpretation swap |
| `chapter_6_physical_realism.tex` | Tier-2 mitigations (J2/J3/J4) | yes | no | interpretation swap (ablation context) |
| `chapter_7_deployment.tex` | Deployment Envelopes | yes | no | no change needed |
| `chapter_8_outlook.tex` | Future Work (HA-SAM) | yes | no | footnote/paragraph addition |
| `abstract_cn.tex` | Final conclusion & abstract | no | yes | interpretation swap |
