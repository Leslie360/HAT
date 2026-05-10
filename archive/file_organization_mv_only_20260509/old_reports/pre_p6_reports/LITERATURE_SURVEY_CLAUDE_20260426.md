# Literature Survey: Missing Parameter Data Sources for Organic Optoelectronic CIM Simulator
**Date:** 2026-04-26
**Auditor:** Claude (Chief Architect)
**Method:** Web search across 2020-2025 organic device literature
**Scope:** 13 missing simulation parameters/physical effects identified in behavioral simulator audit

---

## 1. Temperature Dependence — DATA AVAILABLE

### 1.1 Materials & Design (2025)
- **Title:** "Temperature-dependent plasticity in organic synaptic transistors"
- **Device:** PMMA/TaOx/pentacene bottom-gate synaptic transistor
- **Quantified:** 25°C → 65°C gives >175% channel current increase, ~2.5x memory window widening, PPF tau from 68ms → 245ms
- **Mechanism:** thermally enhanced ion migration
- **Source:** https://www.sciencedirect.com/science/article/pii/S0264127525005726

### 1.2 Nature Communications (2024/2025)
- **Title:** "Near-infrared organic photoelectrochemical synaptic transistor"
- **Quantified:** Below 80°C, no obvious conductance change within 1,000 s
- **Implication:** Practical temperature stability boundary for organic photoelectrochemical synapses
- **Source:** https://www.nature.com/articles/s41467-025-66891-6

### 1.3 KAUST / ECME 2025 (Wentao Shan & Sahika Inal)
- **Device:** Solid-state OECT with semi-solid ionic liquid gel
- **Quantified:** Thermal annealing tunes microstructure; 82% conductance retention over 1,000 s across 5 multilevel states
- **Source:** ECME 2025 abstracts

**Actionable:** Add `temperature_c` to AnalogLinearConfig; model sigma_d2d(T), tau(T) with polynomial or Arrhenius scaling using ~2.5x window widening (25→65°C) as surrogate.

---

## 2. Endurance / Cycling Degradation — DATA AVAILABLE

### 2.1 Science Advances (March 2025)
- **Title:** "Monolithically integrated solid-state vertical OECTs"
- **Quantified:** >1,000 stable switching cycles at 1 Hz with negligible degradation; 225 days air storage without encapsulation
- **Source:** https://www.science.org/doi/10.1126/sciadv.adt5186

### 2.2 npj Flexible Electronics (Dec 2025)
- **Title:** "Regionally controlled ion-doping of OECTs"
- **Quantified:** 1,000 pulse cycles stable (VGS = ±1.5V, 150ms width); write time 0.40s, erase time 1.16s, >60% retention for >60s
- **Source:** https://www.nature.com/articles/s41528-025-00511-7

### 2.3 Cambridge / Springer (2024)
- **Title:** "Stable operating windows for polythiophene OECTs"
- **Quantified:** Repeated full-voltage cycling degrades performance; best stability from limiting operating range
- **Source:** https://link.springer.com/content/pdf/10.1557/s43579-023-00511-6.pdf

**Actionable:** 1,000 cycles is emerging benchmark. Add `max_cycles` or `cycle_count` decay factor (G_max narrowing with cycle number) to simulator.

---

## 3. Read Disturb — LITERATURE GAP

- General memristor read-disturb mitigation papers exist (e.g., TU Delft 2024 dissertation)
- **No dedicated organic device read-disturb characterization** found in accessible literature 2020-2025
- This is a genuine gap; cannot be filled from literature alone without measured data

**Actionable:** List as "explicitly not modeled" in Discussion. No code change possible without data.

---

## 4. Heavy-Tailed / Non-Gaussian Noise — STRONG DATA AVAILABLE

### 4.1 Nature Communications (2022)
- **Title:** "Experimentally validated memristive memory augmented neural network"
- **Key finding:** *"The intrinsic stochastic behavior in memristor devices results in a lognormal-like distribution near 0 μS"*
- **Model:** Device-to-device variation uses lognormal dependence (Eq. 5)
- **Source:** https://www.nature.com/articles/s41467-022-33629-7

### 4.2 IEEE JXCDC (Dec 2022)
- **Title:** "Memristive Devices for Time Domain Compute-in-Memory"
- **Key finding:** *"The programmed high resistive state shows a log-normal distribution, the programmed low resistive state shows a normal distribution"*
- **Typical for:** Filamentary VCM cells; linked to stochastic electroforming
- **Source:** https://d-nb.info/1282375474/34

### 4.3 Supporting Theory Literature
- **J. Stat. Mech. (2020)** — Agudov et al.: Nonstationary distributions in stochastic memristor model (DOI: 10.1088/1742-5468/ab684a)
- **Chaos, Solitons & Fractals (2021)** — Alonso et al.: Multivariate time-series modeling of memristor variability (DOI: 10.1016/j.chaos.2020.110461)
- **Mathematics (2021)** — Ruiz-Castro et al.: Phase-type distributions as non-Gaussian alternative for RRAM variability (DOI: 10.3390/math9040390)

**Actionable:** Add `noise_distribution` option to AnalogLinearConfig ("gaussian", "lognormal", "laplace", "student_t"). Code change: replace `torch.randn_like` with `torch.distributions.LogNormal` sampling. No new measured data needed.

---

## 5. Summary: Can We Model It?

| Missing Parameter | Literature Data? | Actionable Tonight? | Priority |
|:------------------|:-----------------|:--------------------|:---------|
| Temperature dependence | **Yes** (quantified 25→65°C effects) | Yes — add `temperature_c` proxy | P0 |
| Endurance/cycling | **Yes** (~1,000 cycle benchmark) | Yes — add cycle-decay factor | P0 |
| Heavy-tailed noise | **Yes** (lognormal HRS confirmed) | Yes — add `noise_distribution` option | P0 |
| Read disturb | **No** (organic-specific gap) | No — text-only acknowledgment | P1 |
| Spatial IR drop | Partial (scalar placeholder exists) | Yes — upgrade to position-dependent | P1 |
| Sneak path network | No (coupled network model missing) | Medium effort | P2 |
| Hysteresis | Needs measured P-E loop | No — text-only | P2 |

---

## 6. Bottom Line

Three of the four P0 gaps (temperature, endurance, heavy-tailed noise) can be closed **with literature data only**, no lab measurement required. The code changes are additive config fields. Read disturb is the only true dead end — but framing it as an explicit limitation with "future measured-device validation" is reviewer-defensible.

---

*Extracted from AGENT_SYNC_gpt.md §"[LITERATURE SURVEY] Claude: Missing Parameter Data Sources"*
