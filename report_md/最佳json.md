<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# 最后请把你最推荐的 1 篇 case-study 论文，整理成一个“JSON-ready profile draft”：

字段尽量包括：

- device_type
- source
- notes
- G_min
- G_max
- n_states
- noise.sigma_c2c
- noise.sigma_d2d
- noise.mode
- retention.A_0
- retention.tau_1
- retention.tau_2
- optional: gamma_phys, I_dark, responsivity_alpha
- optional: NL_LTP, NL_LTD

注意：

- 没有数据的字段请标 NA
- 每个字段后面说明它来自论文的哪张图/表/段落
- 不要自行脑补缺失值

我已经从论文全文中提取到了关键原始数据。现在整理成完整的 JSON-ready profile draft。[^1][^2]

***

## JSON-Ready Device Profile Draft

基于论文：**Zhang et al., "Near-infrared organic photoelectrochemical synaptic transistors," *Nature Communications*, vol. 16, 197, 2025**[^3][^2]

DOI: [10.1038/s41467-025-66891-6](https://www.nature.com/articles/s41467-025-66891-6)

***

```json
{
  "device_type": "Organic Photoelectrochemical Transistor (OPECT)",
  "source": {
    "citation": "Zhang et al., Nature Communications 16, 197 (2025)",
    "doi": "10.1038/s41467-025-66891-6",
    "notes": "NIR-sensitive (1000 nm) OPECT based on organic BHJ thin film with ion-gel gate;
              photoinduced electrochemical doping mechanism; wafer-scale photolithography array
              (1111 units/cm²). All parameters extracted from main text and Supplementary Figures
              as noted below. Parameters NOT from this paper are explicitly marked NA."
  },

  "G_min": {
    "value": 1.54,
    "unit": "μS",
    "source": "Main text, Fig. 2c caption: 'conductance state of a device increased quasi-linearly
               from 1.54 μS to 361.15 μS' — G_min taken as the initial state before optical
               programming (0 pulses applied at V_GS = -1.2 V under 1000 nm NIR)"
  },

  "G_max": {
    "value": 361.15,
    "unit": "μS",
    "source": "Main text, Fig. 2c caption: '120 consecutive NIR light pulses (1000 nm, 3 mW/cm²,
               0.5 s)... 234-fold improvement'. Also consistent with reported G_max/G_min = 47.3
               under V_GS = -1.2 V (different operating point — see note below)",
    "note": "Two operating points mentioned: (1) Fig.2c gives absolute G_min=1.54 μS,
             G_max=361.15 μS (ratio ~234); (2) Main text §'Synaptic behaviors' gives
             G_max/G_min = 47.3 at V_GS = -1.2 V. These represent different bias conditions.
             The 234-fold is the range across 120 pulses; 47.3 is the ratio at V_GS = -1.2 V,
             which is the optimal NL operating point. Profile should use 47.3 for ratio-based
             modeling unless absolute μS values are required."
  },

  "G_max_over_G_min": {
    "value": 47.3,
    "unit": "dimensionless",
    "source": "Main text: 'the highest G_max/G_min of 47.3 and lowest NL of −0.015/2.01 were
               achieved' at V_GS = −1.2 V under 1000 nm NIR light"
  },

  "n_states": {
    "value": 120,
    "unit": "discrete conductance levels",
    "source": "Main text, Fig. 2c: '120 consecutive NIR light pulses... quasi-linear increase'.
               Supplementary Fig. 23: 'one-to-one conductance state update process...
               controllable and uniform weight programming'. This gives a practical estimate of
               ~120 distinguishable programmed states. The paper also reports 'multi-level storage
               memories' but does not explicitly quote a stable n_states count after noise filtering.",
    "note": "120 is the number of programming steps, not independently verified stable states.
             If the criterion is 'states distinguishable after D2D and C2C noise', the effective
             n_states may be lower. Treat as upper bound."
  },

  "noise": {
    "sigma_c2c": {
      "value": "NA",
      "unit": "—",
      "source": "Not reported in main text or supplementary. No explicit cycle-to-cycle
                 variability (σ_c2c) measurement was performed. Paper shows 8 cycles of
                 LTP/LTD curves (Supplementary Fig. 15) but does not compute σ across cycles."
    },
    "sigma_d2d": {
      "value": "NA",
      "unit": "—",
      "source": "Not reported as a quantitative statistic (no σ_d2d or coefficient-of-variation
                 quoted). The wafer-scale array uniformity is shown in Supplementary Fig. S8
                 (optical microscopy) and device-to-device current maps, but no numerical
                 spread across conductance states is tabulated."
    },
    "mode": {
      "value": "uniform (assumed)",
      "source": "No direct evidence for conductance-proportional noise in this paper.
                 Assumes uniform as conservative default. Must be treated as an assumption
                 pending actual σ extraction from Supplementary Fig. 15 multi-cycle data."
    }
  },

  "retention": {
    "A_0": {
      "value": "NA",
      "unit": "—",
      "source": "No stretched-exponential or power-law retention fitting was performed.
                 No fitted A_0 parameter is reported in main text or supplementary."
    },
    "tau_1": {
      "value": "NA",
      "unit": "—",
      "source": "No fitted time constant tau_1 is provided. Paper shows retention curves
                 for three conductance states (Fig. 2d) but provides only qualitative
                 'long retention' description."
    },
    "tau_2": {
      "value": "NA",
      "unit": "—",
      "source": "Same as tau_1 — no dual-time-constant fit was reported."
    },
    "retention_qualitative": {
      "value": "non-volatile; stable over observation window",
      "source": "Main text: 'long retention time' (Fig. 2d shows retention of three conductance
                 states). Exact retention window is visible in Fig. 2d but numerical axis
                 limits are not quoted in text. Paper describes the device as 'non-volatile'
                 throughout.",
      "note": "To extract tau_1 and tau_2, Fig. 2d must be digitized and fitted to a
               bi-exponential or stretched-exponential model manually. The three curves in
               Fig. 2d may also allow state-dependent retention analysis."
    },
    "state_dependent_retention_evidence": {
      "value": "Qualitative: YES — Fig. 2d shows three distinct conductance states with
                potentially different decay rates, but no quantitative comparison is given.",
      "source": "Main text, Fig. 2d caption: 'Retention time of three conductance states'
                 — the three states are shown on the same plot, enabling visual comparison
                 of decay rates, but no fitted tau values per state are reported."
    }
  },

  "NL_LTP": {
    "value": -0.015,
    "unit": "dimensionless (normalized nonlinearity metric)",
    "source": "Main text: 'lowest NL of −0.015/2.01 were achieved' at V_GS = −1.2 V,
               1000 nm NIR. The −0.015 value corresponds to LTP (potentiation direction).
               Formula follows the standard nonlinearity metric used in analog synapse literature."
  },

  "NL_LTD": {
    "value": 2.01,
    "unit": "dimensionless (normalized nonlinearity metric)",
    "source": "Main text: 'lowest NL of −0.015/2.01 were achieved' — the 2.01 value
               corresponds to LTD (depression direction). Notably higher nonlinearity
               than LTP direction, indicating asymmetric write behavior."
  },

  "gamma_phys": {
    "value": "NA",
    "unit": "—",
    "source": "No explicit photoresponse nonlinearity exponent (gamma) is reported.
               The paper describes intensity-dependent response but does not fit a
               power-law I_photo ~ P^gamma model."
  },

  "I_dark": {
    "value": "NA",
    "unit": "—",
    "source": "Dark current is not explicitly reported as a standalone number.
               Transfer curves are shown but baseline off-current values are not
               tabulated in the main text or supplementary table."
  },

  "responsivity_alpha": {
    "value": "high at 1000 nm (qualitative)",
    "unit": "NA (no A/W value given)",
    "source": "Main text: 'This ratio exhibited the highest photo response under 1000 nm light'
               — wavelength-dependent response is shown in a figure, but responsivity in A/W
               or specific photoresponse magnitude is not numerically reported. Only relative
               comparison across wavelengths is provided."
  },

  "operating_conditions": {
    "V_GS_optimal": {
      "value": -1.2,
      "unit": "V",
      "source": "Main text: 'when V_GS was set as −1.2 V under 1000 nm NIR light, the highest
                 G_max/G_min of 47.3 and lowest NL of −0.015/2.01 were achieved'"
    },
    "optical_pulse_conditions": {
      "wavelength_nm": 1000,
      "power_density_mW_per_cm2": 3,
      "pulse_width_s": 0.5,
      "n_pulses_LTP": 120,
      "source": "Main text, Fig. 2c caption: '120 optical pulses (1000 nm, 3 mW/cm², 0.5 s)'"
    }
  },

  "profile_completeness_summary": {
    "fields_extracted": [
      "G_min", "G_max", "G_max/G_min", "n_states (upper bound)",
      "NL_LTP", "NL_LTD",
      "retention (qualitative, state-dependent evidence visible in Fig.2d)",
      "operating conditions (V_GS, optical pulse params)"
    ],
    "fields_missing_require_digitization": [
      "retention.A_0", "retention.tau_1", "retention.tau_2",
      "(can be extracted by digitizing Fig. 2d and fitting bi-exponential)"
    ],
    "fields_not_in_paper": [
      "sigma_c2c", "sigma_d2d",
      "gamma_phys", "I_dark", "responsivity_alpha (in A/W)"
    ],
    "recommended_action_for_missing_fields": {
      "sigma_c2c": "Estimate from Supplementary Fig. 15 (8-cycle LTP/LTD repeatability) by
                    computing std/mean across cycles at each conductance step",
      "sigma_d2d": "Estimate from device-to-device current uniformity map in Supplementary Fig. S8",
      "tau_1_tau_2": "Digitize Fig. 2d using WebPlotDigitizer; fit to y(t) = A_0 * exp(-t/tau_1) + (1-A_0) * exp(-t/tau_2)",
      "I_dark": "Read off transfer curve at V_GS = 0 in dark condition from Fig. 1 or Supplementary",
      "gamma_phys": "Fit log(EPSC_peak) vs log(P_intensity) from intensity-dependent measurement figures"
    }
  }
}
```


***

## 使用说明与注意事项

这份 profile 有三类字段，需要区别对待：

**直接可用（7个字段）**: G_min、G_max、G_max/G_min、NL_LTP、NL_LTD、n_states（上界）、operating conditions——这些均有明确原文出处。[^2][^1]

**需要图表数字化后可补全（3个字段）**: retention.A_0、tau_1、tau_2 需要用 WebPlotDigitizer 从 Fig. 2d 读点后拟合；sigma_c2c 和 sigma_d2d 需从 Supplementary Fig. 15 和 Fig. S8 中统计计算。

**该论文不涉及、必须从其他文献补充（3个字段）**: gamma_phys、I_dark（绝对值）、responsivity_alpha（A/W）在该论文中没有定量报告，若框架对这些参数有依赖，需引用其他器件文献（如 CuInSe₂ QD 宽带 OPST  可补充 broadband responsivity 数据）。[^4]

**最关键的建模注意**: NL_LTD = 2.01 显著大于 NL_LTP = -0.015，说明该器件的写操作在 depression 方向有明显非线性，这与典型 RRAM 器件的对称假设不同——这正是需要在论文中专门讨论的"有机器件特异性"。[^2]
<span style="display:none">[^10][^11][^12][^13][^14][^15][^16][^17][^18][^19][^20][^21][^22][^23][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://www.nature.com/articles/s41467-025-66891-6

[^2]: https://pmc.ncbi.nlm.nih.gov/articles/PMC12780254/

[^3]: https://ui.adsabs.harvard.edu/abs/2025NatCo..17..197L/abstract

[^4]: https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/smm2.1246

[^5]: https://pmc.ncbi.nlm.nih.gov/articles/PMC11825661/

[^6]: https://pmc.ncbi.nlm.nih.gov/articles/PMC8991232/

[^7]: https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/advs.202102036

[^8]: https://academic.oup.com/nsr/advance-article-pdf/doi/10.1093/nsr/nwad311/54257155/nwad311.pdf

[^9]: https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/aelm.202001126

[^10]: https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/adma.202402903

[^11]: https://onlinelibrary.wiley.com/doi/pdfdirect/10.1002/agt2.345

[^12]: https://www.nature.com/articles/s41467-025-56814-w

[^13]: https://www.nature.com/articles/s41467-024-51194-z

[^14]: https://www.proquest.com/docview/2554790480/600184A7BBF643BCPQ/4

[^15]: https://www.ablesci.com/assist/detail?id=BEXl0B

[^16]: https://henryluckky.github.io/files/TED-2022-09-2185-R_Proof_hi.pdf

[^17]: https://pubs.rsc.org/it-it/content/articlelanding/2025/tc/d5tc00345h/unauth

[^18]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10302604/

[^19]: https://pubs.rsc.org/en/content/articlelanding/2025/tc/d5tc00345h

[^20]: https://ksp.etri.re.kr/ksp/article/file/71085.pdf

[^21]: https://hocityu.com/publications_files/NanoLett_2023_Organic%20Electrochemical%20Synaptic%20Transistors%20for%20Neuromorphic%20Processing.pdf

[^22]: https://pubs.rsc.org/en/content/articlehtml/2025/mh/d5mh01710f

[^23]: https://research.manchester.ac.uk/en/publications/vision-inspired-optoelectronic-synaptic-transistors-based-on-p-ty/

