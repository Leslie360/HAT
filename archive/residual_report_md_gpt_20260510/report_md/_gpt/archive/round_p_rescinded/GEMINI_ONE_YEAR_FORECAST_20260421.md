# One-Year Forward Memo — compute-ViT Post-NC

**Date:** 2026-04-21
**Horizon:** 12 months after Nature Communications acceptance

This memo defines what success looks like for the compute-ViT framework one year after NC acceptance, and what we must execute today to shift probability toward Scenario A.

---

## Scenario A — Optimistic

**Metrics.** 50+ citations; 100+ GitHub stars and 3 external contributors; 2+ external groups publish extensions (e.g., LLM attention blocks on RRAM or printed-CIFAR-100); 1 invited talk at a major venue (NeurIPS/ISSCC/VLSI). Personal: PhD defended, postdoc or industry lab secured.

**Hindsight.** We should have released the fresh-instance evaluation protocol as a standalone pip-installable package immediately upon acceptance, rather than burying it in the thesis repo. The organic-device JSON schema and a 5-minute Colab notebook should have shipped on day one.

**Action items NOW.** (1) Freeze `compute-vit-core` with a minimal API before thesis submission. (2) Draft a 15-minute conference talk abstract for ISSCC/IEDM and submit to industry sessions. (3) Label “good first issues” for D2D-map visualization and ADC-floor sweep wrappers to seed external contributors.

---

## Scenario B — Moderate

**Metrics.** 20–30 citations; 50+ GitHub stars with occasional issues/PRs; cited by 2–3 review papers on analog-CIM or neuromorphic computing; small but engaged community on Twitter/X. Personal: PhD defended, applications pending.

**Hindsight.** We over-invested in perfecting the CrossSim comparison figure and under-invested in a one-page “Quick Start” that runs without an OPECT JSON file. The barrier to first run was too high for most visitors.

**Action items NOW.** (1) Ship a default `standard_noise.json` profile so the repo trains CIFAR-10 in <10 min on a single GPU with no hardware knowledge required. (2) Publish a 1,000-word blog post, “Why ViT attention collapses under analog mismatch,” the week the paper goes live. (3) List the repo on Papers with Code and submit to Awesome-Analog-Computing.

---

## Scenario C — Pessimistic

**Metrics.** <10 citations; minimal GitHub engagement (<20 stars, no external PRs). The paper is correct, but the field pivots to digital near-memory compute or standard-cell accelerators, and organic CIM funding dries up. Personal: PhD defended, career pivot required.

**Hindsight.** We treated the organic angle as a differentiator rather than a risk. Without a measured-device validation paper to back the literature-derived calibration, the community files the work under “simulator-only.” The lack of SPICE co-simulation becomes the excuse to ignore it.

**Action items NOW.** (1) Secure a collaboration letter or data-sharing agreement with an experimental group *before* the NC decision arrives, so a validation follow-up is already in motion. (2) Build a “Plan B” narrative: frame ensemble-HAT + fresh-instance evaluation as a general analog-training protocol portable to RRAM/PCM, not only organic. (3) Set a hard 6-month checkpoint: if stars <30 and citations <5, redirect energy to a systems/EDA paper to maintain publication velocity.

---

*End of memo.*
