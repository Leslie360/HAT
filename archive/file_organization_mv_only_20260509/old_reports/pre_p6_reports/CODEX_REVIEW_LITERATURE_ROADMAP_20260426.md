# Codex Review — Literature Survey + Experiment Roadmap
**Date:** 2026-04-26 23:50 CST
**Reviewer:** Codex
**Inputs:**
- `report_md/_gpt/LITERATURE_SURVEY_CLAUDE_20260426.md`
- `report_md/_gpt/EXPERIMENT_ROADMAP_CLAUDE_20260426.md`
- local R11D JSON/logs under `paper2_aihwkit_baseline/checkpoints/`
- spot web verification of key references

## 0. Bottom Line

The two documents are directionally useful, but should be tightened before Claude integrates them into paper claims.

My verdict:

1. **Experiment roadmap:** mostly reasonable after clean R11D-2/3 verification, but the headline **"Path B confirmed" is too strong unless Claude confirms the precision semantics.** In our current AIHWKit script, `--inp-res/--out-res=1/16` changes AIHWKit forward input/output discretization, not necessarily stored weight/conductance precision. If our Ensemble HAT "4-bit" means conductance-state weight quantization, the comparison is not automatically apples-to-apples.
2. **Literature survey:** good as a source map for sensitivity knobs, but too aggressive when it says P0 gaps can be "closed with literature data". The safer framing is: **literature supports sensitivity/stress-test parameters, not calibrated organic-array ground truth.**
3. **Most important immediate fix:** distinguish `direct evidence`, `proxy evidence`, and `stress-test evidence` in both text and simulator tasks.
4. **Ask Claude before manuscript integration:** whether AIHWKit 4-bit should be called "4-bit forward I/O precision", "4-bit ADC/DAC", or "4-bit deployment precision". Avoid "4-bit weight precision" unless proven.

---

## 1. Experiment Roadmap Review

### 1.1 R11D numerical status is now verified

Clean local artifacts support the roadmap's R11D-1/2/3 table, with one caveat about the contaminated old R11D-2 directory.

| Track | Clean artifact | Source best | Fresh mean | Status |
|:--|:--|--:|--:|:--|
| R11D-1 4-bit | `checkpoints/r11d_1_4bit/` | 15.01% | 14.6368 ± 0.1059% | valid |
| R11D-2 sigma0.20 | `checkpoints/r11d_2_sigma020_clean/` | 87.60% | 87.5166 ± 0.0500% | valid |
| R11D-3 sigma0.30 | `checkpoints/r11d_3_sigma030_clean/` | 87.57% | 87.4036 ± 0.0483% | valid |

Do **not** use:

```text
paper2_aihwkit_baseline/checkpoints/r11d_2_sigma020/
```

That directory was marked contaminated because two processes wrote the same `best.pt`.

### 1.2 Main interpretation is plausible but needs one semantic guard

The roadmap says:

> Precision, not noise, is the lever. Path B confirmed.

I agree with the **empirical pattern**:

- AIHWKit survives ADD_NORMAL sigma0.20 and sigma0.30 at 8-bit forward precision.
- AIHWKit collapses under the current 4-bit stress setting.

But the phrase **"4-bit weight precision" is not safe yet**. Our R11D-1 command set:

```bash
--inp-res 0.0625
--out-res 0.0625
```

Those are AIHWKit `InferenceRPUConfig.forward.inp_res/out_res` parameters. In AIHWKit terminology, this is forward path discretization, i.e. input/output resolution. It is not automatically the same as 16 stored conductance levels for weights.

Safer wording:

> AIHWKit collapses under 4-bit forward-path discretization (`inp_res=out_res=1/16`) while remaining robust to higher ADD_NORMAL inference noise at 8-bit forward precision. This identifies precision/discretization, rather than Gaussian weight-noise magnitude alone, as the stress axis in the current AIHWKit setup.

Only after Claude confirms exact mapping may we write:

> 4-bit deployment precision method-superiority confirmed.

### 1.3 AIHWKit fresh-instance semantics need confirmation

Our eval protocol calls `eval_aihwkit_fresh.py` with `modifier.enable_during_test=True` and different seeds. This likely samples test-time analog noise, but Claude should confirm whether this represents:

1. a fixed hardware instance held constant across all test batches,
2. fresh noise per forward pass/batch,
3. fresh noise per layer/tile with AIHWKit-internal sampling semantics.

If it is per-forward stochastic noise rather than a fixed D2D instance, then it is not identical to our HAT fresh-instance protocol. The result remains useful, but the claim should be **"AIHWKit stochastic inference robustness"**, not necessarily **"fresh hardware-instance robustness"**.

### 1.4 Required follow-up before final paper wording

I recommend these minimal checks before Claude finalizes Path B language:

| Priority | Check | Why |
|:--|:--|:--|
| P0 | Ask Claude/DS to confirm AIHWKit `inp_res/out_res` semantics | Prevent false "weight precision" claim |
| P0 | Confirm `enable_during_test=True` sampling cadence | Prevent false "fresh-instance" equivalence |
| P0 | Run 2×2 train/eval precision matrix if cheap | Distinguish training failure vs inference quantization failure |
| P1 | One replicate seed for R11D-1 or short 20-epoch collapse replicate | The collapse is huge, but publication headline benefits from replicate |
| P1 | Continue R11D-4 PCM only after semantics are fixed | PCM result is valuable, but only if protocol wording is clean |

Suggested 2×2 matrix:

| Train precision | Eval precision | Purpose |
|:--|:--|:--|
| 8-bit | 8-bit | existing R10E/R11D baseline |
| 8-bit | 4-bit | isolate inference discretization cliff |
| 4-bit | 8-bit | test whether 4-bit training destroyed learned weights |
| 4-bit | 4-bit | existing R11D-1 |

---

## 2. Literature Survey Review

### 2.1 Overall assessment

The literature survey is useful, but its conclusion should be weakened from:

> Three P0 gaps can be closed with literature data.

To:

> Literature supports adding sensitivity knobs and bounded stress tests for three P0 gaps; it does not fully calibrate an organic OPECT/OECT deployment profile without measured device data.

This distinction matters for Nature Electronics reviewers. They will accept transparent sensitivity studies; they will attack overclaiming proxy parameters as calibration.

### 2.2 Evidence grading

| Topic | Kimi/Claude claim | My assessment | Safe use |
|:--|:--|:--|:--|
| Temperature dependence | DATA AVAILABLE | Partly true. Direct OPECT thermal stability exists; temperature-dependent plasticity source is a different organic synaptic transistor stack. | Add `temperature_c` sensitivity knob, but label source-specific proxy. |
| Endurance/cycling | DATA AVAILABLE | True at OECT level, but cycle counts differ by operating regime. Full-range OECT cycling can degrade in 100 cycles; saturation/pulse regimes can be stable. | Add `cycle_count` stress model with operating-regime dependence, not one universal 1000-cycle benchmark. |
| Read disturb | LITERATURE GAP | Reasonable. Organic-specific read-disturb evidence appears weak. | Text-only limitation. |
| Heavy-tailed noise | STRONG DATA AVAILABLE | True for memristors/RRAM; not direct organic OPECT/OECT conductance-domain D2D. | Add `noise_distribution` as stress-test option, not organic calibration. |
| Spatial IR drop | partial | Already in paper as lower-bound behavioral probe; okay. | Keep first-order proxy language. |
| Sneak/hysteresis | needs data | Correct. | P2/future measured-device validation. |

### 2.3 Source-specific notes

#### Temperature

- The Nature Communications OPECT paper is strong direct evidence for a NIR OPECT platform and reports stability below 80 °C over 1000 s, but it is a 2026 volume article with acceptance/publication spanning late 2025/early 2026. The survey label "2024/2025" should be corrected.
- The Materials & Design temperature-dependent plasticity paper is useful but not the same OPECT substrate as the manuscript's target. Treat it as mechanism/proxy evidence for ion-migration temperature sensitivity.

Safe sentence:

> Published organic synaptic transistor and OPECT studies demonstrate that temperature can substantially alter ionic/plasticity dynamics in some stacks, while at least one NIR OPECT platform remains conductance-stable below 80 °C over 1000 s. We therefore include temperature as a sensitivity axis rather than a calibrated universal correction.

#### Endurance

- Regionally controlled ion-doping OECTs support 1000-pulse stability and memory retention on the order of tens to 1000 s, depending on device regime.
- Stable-operating-window OECT literature shows the opposite lesson under full-range cycling: degradation can appear within 100 cycles. This is actually valuable because it tells us endurance is operating-window dependent.

Safe model:

```text
G_max(cycle) = G_max(0) * (1 - a * log1p(cycle / N0))
```

or a bounded decay parameterized by operating regime:

```text
endurance_mode ∈ {saturation, pulse, full_sweep}
```

#### Heavy-tailed noise

Memristive RRAM/lognormal evidence supports non-Gaussian stress testing. It does not prove the organic OPECT D2D law is lognormal.

Safe sentence:

> Because measured organic conductance-domain D2D histograms are not yet available, we include lognormal/Laplace/Student-t options as robustness stress tests motivated by broader memristive-device literature, not as default organic priors.

---

## 3. Additions I Recommend

### 3.1 Add a "citation strength" column to the literature table

Suggested categories:

| Strength | Meaning |
|:--|:--|
| A | Same device class and same measured quantity |
| B | Same organic family, adjacent quantity |
| C | Inorganic/memristive analogue, useful only for stress test |
| D | Theory/engineering approximation |

Apply this to the simulator-upgrade table:

| Feature | Current priority | Citation strength | Revised claim |
|:--|:--|:--|:--|
| `temperature_c` | P0 | A/B mixed | sensitivity axis |
| `cycle_count` | P0 | A/B mixed | operating-window-dependent decay |
| `noise_distribution` | P0 | C | stress-test distribution |
| read disturb | P1 | gap | explicit limitation |
| IR drop | P1 | D | first-order array proxy |

### 3.2 Add a protocol-integrity note to R11D table

In `EXPERIMENT_ROADMAP_CLAUDE_20260426.md`, add footnotes:

1. R11D-2/3 numbers come from `_clean` directories only.
2. Old `r11d_2_sigma020/` is contaminated and excluded.
3. AIHWKit 4-bit means `forward.inp_res=forward.out_res=1/16` unless further confirmed.
4. Fresh eval uses AIHWKit test-time modifier noise; semantics to be confirmed against fixed-instance D2D.

### 3.3 Fix stale manuscript/tooling text

Current `paper/latex_gpt/supplementary/S_tooling_comparison.tex` still says Tiny-ViT AIHWKit conversion failed. That is now stale because R10E/R11D produced actual Tiny-ViT AIHWKit numbers.

Action for Claude/Kimi:

- Replace S-T.3 with the actual AIHWKit head-to-head table and semantics caveat.
- Ensure `supplementary.tex`, `S_tooling_comparison.tex`, and `cover_letter.tex` do not contradict each other.

### 3.4 Fix AIHWKit citation naming

Current text alternates between `Rasch 2021` and `Rasch 2023`. The IBM GitHub page asks users to cite the AICAS 2021 toolkit paper and also points to a 2023 APL Machine Learning tutorial.

Suggested policy:

- Cite `rasch2021aihwkit` for the toolkit lineage.
- Optionally add the 2023 APL ML tutorial as usage/tutorial reference.
- Do not call the 2021 arXiv/BibTeX entry "Rasch et al. 2023" unless the bibliography entry is changed.

### 3.5 Check CrossSim BibTeX DOI

Local `crosssim2024` BibTeX uses:

```text
10.2172/2585829
```

The Sandia page I checked shows:

```text
10.2172/2563881
```

This needs Claude/Gemini verification before final references. It is not central to the roadmap, but reference accuracy matters.

---

## 4. Questions to Send Claude

I would ask Claude these exact questions:

1. **AIHWKit precision semantics:** In R11D-1, does `cfg.forward.inp_res=cfg.forward.out_res=1/16` justify saying "4-bit weight precision", or should we say "4-bit forward ADC/DAC precision"?
2. **Fresh-instance semantics:** Does AIHWKit `WeightModifierType.ADD_NORMAL` with `enable_during_test=True` instantiate a fixed hardware-noise map per eval instance, or does it resample per forward pass/batch? If the latter, should the table label be changed from "fresh-instance" to "test-time stochastic analog robustness"?
3. **Path B wording:** Given the above, should "Path B confirmed" be weakened to "Path B supported in the tested 4-bit forward-discretization regime"?
4. **R11D-4 priority:** Should PCM run now, or should the AIHWKit precision/fresh semantics be corrected first?
5. **Literature framing:** Do you agree to change "P0 gaps closed by literature data" to "P0 sensitivity axes supported by literature proxies"?
6. **Manuscript consistency:** Should Kimi immediately replace stale `S_tooling_comparison.tex` AIHWKit failure text with the actual R10E/R11D results?
7. **References:** Should we add the 2023 APL Machine Learning AIHWKit tutorial citation and correct/check the CrossSim DOI?

---

## 5. My Recommended Claude Decision

My recommended decision is a hybrid:

1. Keep the R11D conclusion that **AIHWKit is robust to high ADD_NORMAL noise at 8-bit but collapses under the current 4-bit forward-discretization stress**.
2. Do **not** yet call it "4-bit weight precision" or unconditional "method-superiority confirmed".
3. Present literature upgrades as **sensitivity/stress axes**, not fully calibrated device physics.
4. Prioritize a short semantic/protocol correction pass before R11D-4 PCM.
5. Use R11D-4 PCM only after the table labels are scientifically precise.

This keeps the strong story while avoiding overclaiming.

---

## 6. Spot-Verified Sources

- AIHWKit GitHub/README: toolkit supports PyTorch analog modules, inference/training workflows, hardware-aware training, ADC/DAC discretization, device variations, and asks users to cite the 2021 AICAS paper. Source: https://github.com/IBM/aihwkit
- AIHWKit tutorial page exists as 2023 APL Machine Learning article, but AIP page was access-restricted during fetch. Source DOI page: https://doi.org/10.1063/5.0142944
- Wager et al. 2013 NeurIPS: dropout/noising as adaptive regularization and first-order L2-style regularizer. Source: https://papers.nips.cc/paper/4882-dropout-training-as-adaptive-regularization
- Foret et al. 2021 ICLR: SAM minimizes loss value and sharpness; useful for the flat-minima analogy. Source: https://openreview.net/forum?id=6Tm1mposlrM
- NIR OPECT Nature Communications article: 1000 nm NIR OPECT, temperature/humidity retention and stability statements, 32/34 conductance states and array uniformity. Source: https://www.nature.com/articles/s41467-025-66891-6
- Regionally controlled ion-doping OECT: 1000-pulse cycling and >60% retention over >60 s. Source: https://www.nature.com/articles/s41528-025-00511-7
- Stable operating windows for polythiophene OECTs: full-range cycling degrades within 100 cycles; saturation operation much more stable. Source: https://link.springer.com/article/10.1557/s43579-023-00511-6
- Nature Communications 2022 memristive memory: reports lognormal-like conductance behavior near 0 uS in memristive devices; useful for non-Gaussian stress tests, not direct organic calibration. Source: https://www.nature.com/articles/s41467-022-33629-7
- CrossSim Sandia publication page: confirms CrossSim 2024 page and DOI shown as `10.2172/2563881`; local BibTeX should be checked. Source: https://www.sandia.gov/research/publications/details/crosssim-a-hardware-software-co-design-tool-for-analog-in-memory-computing-2024-04-01/
