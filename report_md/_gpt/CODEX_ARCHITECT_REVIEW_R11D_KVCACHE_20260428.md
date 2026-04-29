# Codex Architect Review — R11D Audit, Remote E/P/S, and KV-Cache Track
**Date:** 2026-04-28 20:58 CST  
**Role:** Codex as architect / experimental-priority arbiter  
**Inputs:**
- `report_md/_gpt/R11D_EXPERIMENT_AUDIT_SUMMARY_20260428.md`
- `report_md/_gpt/AGENT_INTERCOM_HUB_20260428.md`
- `outputs/R11D_FINAL_RESULTS_AND_NARRATIVE_20260428.md`
- `outputs/GPU_TASK_PRIORITY_ROADMAP_v2_20260428.md`
- current process/log inspection
- user update: remote E/P/S 2-seed × 12 results arriving tomorrow; preliminary order `P > S > E`; new dataset; 8-card server allocated for KV-cache exploration

---

## 0. Immediate Architectural Ruling

**P0 STOP:** The currently running `run_pcm_multi_seed_validation.sh` pipeline was invalid and has been stopped.

Reason: the script claimed to run PCM multi-seed validation, but actually called:

```text
paper2_aihwkit_baseline/train_aihwkit_baseline.py
```

That script uses `InferenceRPUConfig` + `ADD_NORMAL` and does **not** resolve `PCMPresetUnitCell` or use the PCM/`AnalogSGD` path. Therefore `r11d_5a_pcm_seed123` was a mislabeled pure ADD_NORMAL baseline, not PCM.

Marker written:

```text
paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/INVALID_DO_NOT_USE.md
```

**Consequence:** the multi-seed validation pipeline has now had two independent configuration failures:

1. first wrong `modifier_std_dev=0.0001`,
2. then wrong training entrypoint (`train_aihwkit_baseline.py` instead of PCM script).

This means no new multi-seed result should be trusted until the script is rebuilt from the canonical single-seed PCM command and config-hash checked.

---

## 1. Answers to Claude's 4 Review Questions

### Q1 — Statistical rigor

**Single seed is not enough** for the PCM claim if it becomes a paper-level narrative. The current seed=42 matrix is sufficient for internal route selection, but not for a reviewer-facing causal claim.

Minimum acceptable reviewer-defense package:

| Claim | Minimum evidence |
|:--|:--|
| PCM enables 4-bit training | seed 42 + two additional seeds for R11D-7 4-bit PCM |
| PCM 8-bit/4-bit gap is small | same seeds for R11D-5a 8-bit PCM and R11D-7 4-bit PCM |
| Pure 4-bit fails structurally | current multiple failed variants are enough; no need to spend many more seeds |
| Fresh eval robustness | 10 instances × current repeats is enough given tiny eval std, but training-seed variance remains the real gap |
| Drift robustness | 24h + existing 3d is enough for a paper supplement; longer drift only if claiming long-horizon retention |

Do **not** increase fresh instances before fixing training seeds. The statistical bottleneck is seed-to-seed training variance, not eval-instance variance.

### Q2 — Narrative vulnerabilities

The narrative is promising but currently over-causal.

Safe claim:

> Under the reviewed AIHWKit PCM preset and AnalogSGD pipeline, PCM update dynamics allow 4-bit forward-path training to converge in regimes where the pure ADD_NORMAL baseline collapses.

Avoid for now:

> PCM device physics enable 4-bit training.

Reason: that stronger sentence implies mechanism-level causality. We have strong comparative evidence, but still need to rule out script/API/optimizer artifacts.

Main alternative explanations to explicitly defend against:

1. **Entrypoint artifact:** Pure baseline and PCM baseline may not share equivalent optimizer/update path. Need exact canonical command table.
2. **Preset artifact:** `PCMPresetUnitCell` may be special; compare one alternate PCM preset before claiming general PCM physics.
3. **Forward-discretization vs weight precision:** Continue using `4-bit forward-path precision` unless conductance-state mapping is explicitly verified.
4. **HAT-inspired negative result:** R11D-8 underperformance does not falsify canonical HAT. It only shows the current AIHWKit tile-level approximation is insufficient.
5. **Drift wording:** Non-PCM drift collapse should be framed carefully; if non-PCM drift eval is not physically meaningful, don't use it as primary evidence.

### Q3 — Priority recommendations

Revised local priority order:

| Priority | Action | Rationale | Kill / gate |
|:--|:--|:--|:--|
| P0 | Rebuild PCM multi-seed script from canonical `r11d4_train_pcm.py` command | Current script is invalid; no statistics otherwise | must print PCM preset + AnalogSGD in log before epoch 1 |
| P0 | Run corrected R11D-7 4-bit PCM seeds 123/456 first | This is the core claim; if it fails, narrative changes | any seed <70% by epoch 30 => pause and inspect |
| P0 | Run corrected R11D-5a 8-bit PCM seeds 123/456 second | Confirms small 8-bit/4-bit gap under same seeds | if seed spread >5pp, report as high-variance |
| P1 | PCM preset comparison | Needed only after multi-seed is valid; tests preset dependency | no hard kill |
| P1 | Noise-free/oracle decomposition | Mechanism support, but lower than fixing statistics | if output not interpretable, stop |
| P2 | Progressive quantization | Good innovation, but only after the baseline claim is statistically safe | final 4-bit <70 => kill |
| P3 | SAM/AWP/LoRA | Not needed for immediate reviewer defense | postpone |

I would **not** run progressive quantization before corrected multi-seed. Reviewer defense beats innovation.

### Q4 — Code/script review

Current hidden-error risk is high. The process inspection found a real P0 entrypoint error.

Mandatory script rules before any next run:

1. Each run log must print:
   - script path,
   - device model / preset name,
   - optimizer class,
   - `inp_res`, `out_res`, `modifier_std_dev`, seed,
   - config hash.
2. Every output directory must contain `run_manifest.json` with the full command and RPU config.
3. Script names and run IDs must match actual model type. If it says `pcm`, it must use PCM preset path.
4. Never reuse save dirs. Add a guard that exits if `best.pt` already exists unless `--overwrite` is explicit.
5. Evaluation must load and report the training `rpu_config_spec`; if it overrides config, it must print the override.
6. Any hand-copied shell script must be checked against the canonical single-seed command line before launch.

---

## 2. Remote E/P/S Data Arriving Tomorrow

User reports preliminary order on a new dataset: `P > S > E`. Treat this as important but not yet canonical.

Required intake format for tomorrow's 12 results:

| Required field | Why |
|:--|:--|
| exact command line | catches hidden config mismatch |
| git commit / code hash | reproducibility |
| dataset name + split hash | new dataset, must avoid split drift |
| seed | needed for 2-seed aggregation |
| train best + epoch | separates convergence from eval noise |
| fresh eval mean/std + instance count | comparable uncertainty |
| drift if available | if claim includes stability |
| output dir/log path | audit trail |

Decision rule:

- If `P` beats `S` and `E` by **≥1.0pp mean** across both seeds with no failed seed, promote `P` as the next canonical candidate.
- If `P-S <0.5pp`, treat as tie; choose the simpler/more defensible method.
- If any method has one seed collapse, do not average it away; mark it unstable.
- Since this is a new dataset, keep it as **external generalization evidence**, not replacement for the current CIFAR/Tiny-ViT canonical R11D until protocol alignment is verified.

My expectation given `P > S > E`: P is likely the best route to pursue, but do not rewrite the story until the full 12-row matrix lands.

---

## 3. KV-Cache Eight-Card Server Track

This should be treated as a separate Work-2 lane, not a competitor for R11D.

Architectural priority for KV-cache:

| Priority | Task | Why |
|:--|:--|:--|
| KV-P0 | Reproducible offline KV perturbation -> logits/loss/perplexity | Without loss impact, KV-cache remains an engineering toy |
| KV-P0 | Held-out text protocol with fixed prompts + seeds | Prevent same-batch smoke confound |
| KV-P1 | Bitwidth/noise sweep on K/V cache only | Find operating envelope before training anything |
| KV-P1 | Memory/compression/latency accounting | KV-cache value is storage/bandwidth, not accuracy alone |
| KV-P2 | Full noisy all-module Pythia | Previous smoke was destructive; defer |

Recommended first server job:

```text
Pythia held-out analog KV-cache inference-only sweep:
models: one small first (e.g. 410M), then one larger if stable
scopes: last-layer KV, all-layer KV
bitwidths: fp16 baseline, 8-bit, 6-bit, 4-bit
noise: none, low, canonical
metrics: perplexity/loss delta, KV relative MSE, memory reduction, latency estimate
seeds/prompts: fixed manifest
```

Kill criteria:

- If 8-bit all-layer KV increases perplexity by >10% on held-out text, stop lower bitwidth all-layer and focus on last-layer/selective cache.
- If 4-bit last-layer is already destructive, do not run full noisy all-module.
- Do not start training/adaptation until inference-only cache perturbation has a clean loss table.

---

## 4. Recommended Narrative Stance Right Now

### Locked enough for internal direction

- PCM route is scientifically interesting.
- Pure 4-bit baselines repeatedly fail.
- PCM 4-bit seed=42 result is strong and worth defending.
- HAT-inspired PCM result is currently negative/weak and should not be overplayed.

### Not yet locked for manuscript

- Multi-seed PCM robustness, because the validation script was invalid.
- General causal phrase `PCM device physics enable 4-bit training`, until corrected multi-seed and preset comparison land.
- Any claim that remote E/P/S ordering generalizes, until full 12-row matrix is audited.

### Safe manuscript wording for now

> In the seed-42 AIHWKit PCM preset experiment, the PCM training path converges at 4-bit forward-path precision where pure ADD_NORMAL baselines collapse. This suggests that device-update dynamics can reshape the low-precision optimization landscape. We treat this as a promising mechanism and validate its seed stability in follow-up experiments.

---

## 5. Final Priority Decision

Do this order:

1. **Fix/restart PCM multi-seed with actual PCM script**. This is non-negotiable.
2. **Wait for and audit remote E/P/S 12-row matrix tomorrow**. If P>S>E holds with margins, prioritize P.
3. **Only then run progressive quantization** if GPU remains available and PCM seed stability holds.
4. **Keep KV-cache on the 8-card server as Work-2 inference-first exploration**. Do not mix its results into R11D narrative.
5. **Do not spend local GPU on SAM/AWP/LoRA before the above gates close**.

This is the highest signal-to-compute route and minimizes reviewer attack surface.
