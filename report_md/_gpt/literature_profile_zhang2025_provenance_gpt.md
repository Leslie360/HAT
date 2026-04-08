# Literature Profile Provenance (GPT)

## Candidate

- Paper: Zhang et al., *Nature Communications* 17, 197 (2026)
- DOI: `10.1038/s41467-025-66891-6`
- Device: near-infrared organic photoelectrochemical transistor (OPECT)

## Runtime Artifacts

- Runnable case-study JSON:
  - `/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/literature_fitted_profile.json`
- Library profile entry:
  - `/home/qiaosir/projects/compute_vit/device_profiles/literature_profiles_gpt.json`
- Perplexity extraction sources:
  - `/home/qiaosir/projects/compute_vit/report_md/查找数据.md`
  - `/home/qiaosir/projects/compute_vit/report_md/最佳json.md`
- Local article PDF:
  - `/home/qiaosir/projects/compute_vit/report_md/s41467-025-66891-6.pdf`

## Exact Literature Anchors

### 34 states

Per Perplexity's figure-level extraction, the `34 states` claim is supported by all of:

- Abstract:
  - `non-volatile multi-level storage memories (34 states, 60 s)`
- Main text, Results, `Synaptic behaviors of OPECT arrays`:
  - `34 distinguishable conductance states with retention more than 60 s were realized in OPECTs array owing to decent photo-induced ion doping (Fig. 3h)`
- Fig. 3h caption:
  - `Retention characteristics of OPECTs at 34 conductance states, with Gmax/Gmin ≈ 65.8`
- Supplementary Fig. 8 (as quoted by the extraction note):
  - `34 discrete conductance states can be easily identified with retention more than 60 s`

Local PDF check:

- first-page publisher line:
  - `Nature Communications | (2026)17:197`
- this is now the canonical bibliographic form for the project assets, even though some older prompt files still carry the shorthand `16, 197 (2025)`

### 120 optical pulses

Per the same extraction, the `120 optical pulses` claim is supported by:

- Main text, Results, `Synaptic behaviors of single OPECT`:
  - `By applying 120 consecutive NIR light pulses, the conductance state of a device increased quasi-linearly from 1.54 μS to 361.15 μS, realizing a 234-fold improvement (Fig. 2c)`
- Fig. 2c caption:
  - `Conductance update by continuously applying 120 optical pulses (1000 nm, 3 mW/cm², 0.5 s)`

### Variability evidence

- `sigma_c2c` evidence path:
  - Supplementary Fig. 15: 8-cycle LTP/LTD repeatability
  - Fig. 3g: three reproducible LTP/D curves
- `sigma_c2c` extraction note:
  - Supplementary Fig. 15 is sufficient for an approximate conductance-domain `sigma_c2c` workflow because the same pulse index can be read across 8 repeated cycles
  - safest pulse indices are interior points rather than boundary pulses
  - the current runtime value (`0.02`) remains a transparent proxy until explicit digitization is done
- `sigma_d2d` evidence path:
  - Fig. 3b / Fig. 3c: 80-device uniformity study
  - main-text direct value for threshold-voltage spread:
    - dark: mean `-1.50 V`, std `0.01 V`
    - light: mean `-1.37 V`, std `0.02 V`
  - this corresponds to about `0.67%` and `1.46%` relative spread in `V_th`
  - no direct conductance-uniformity histogram has been identified from the current main-paper extraction package

### Retention fitting evidence

- Fig. 2d:
  - `Retention time of three conductance states`
  - suitable for qualitative state-dependent retention discussion and later digitization if needed
- Fig. 2e and Fig. 3h:
  - useful as supporting multi-state retention/discriminability evidence
- current conservative interpretation:
  - the paper does **not** provide a fitted retention model
  - the safest manuscript wording is that Fig. 2d supports qualitative state-dependent retention discussion
  - if a future quantitative fit is attempted after digitization, a stretched-exponential baseline is safer than directly claiming a double-exponential fit

## Field Mapping

| Field | Runtime value | Status | Rationale |
|:--|--:|:--|:--|
| `device_type` | `Organic OPECT Zhang2025 Literature-Fitted` | direct | Named to distinguish the case-study profile from the canonical organic prior. |
| `G_min` | `1.0` | normalized | We intentionally normalize conductance to avoid mixing incompatible absolute operating points mentioned in the literature summary. |
| `G_max` | `47.3` | direct-normalized | Uses the reported optimal `G_max / G_min = 47.3` as the stable dynamic-range anchor. |
| `n_states` | `34` | direct-conservative | Chosen from the explicit `34 distinguishable conductance states` evidence instead of using the 120-pulse programming sweep as guaranteed stable states. |
| `sigma_c2c` | `0.02` | proxy estimate | The paper still does not report an explicit conductance-domain sigma, but Supplementary Fig. 15 / Fig. 3g show strong repeatability. Runtime value is a transparent proxy estimate, not a direct literature number. |
| `sigma_d2d` | `0.03` | proxy estimate | The paper directly reports `V_th` spread across 80 devices (~0.67%-1.46%). Runtime value is a conservative conductance-domain uplift from that evidence, not a directly measured conductance sigma. |
| `noise_mode` | `uniform` | conservative assumption | No explicit proportional-noise law is reported in the current extraction package. |
| `tau_1` | `null` | withheld | Retention figure exists, but no fit has been extracted yet. |
| `tau_2` | `null` | withheld | Same as above. |
| `A_0` | `null` | withheld | Same as above. |
| `NL_LTP` | `null` | intentionally withheld | The raw paper reports `-0.015` as a literature nonlinearity metric; this is not numerically identical to the simulator's surrogate NL parameterization, so it should not be injected directly. |
| `NL_LTD` | `null` | intentionally withheld | Same reason as `NL_LTP`; raw reported value `2.01` should first be mapped to simulator semantics. |
| `pulse_count_max` | `120` | direct | Based on the reported 120 optical programming pulses in the literature summary. |
| `gamma_phys` | `null` | missing | No safe fitted value extracted yet. |
| `I_dark` | `null` | missing | No safe fitted value extracted yet. |
| `responsivity_alpha` | `null` | missing | No safe fitted value extracted yet. |

## Why This Is Still Useful

This profile is already useful for the paper because it demonstrates a reviewer-relevant bridge workflow:

1. pick one concrete organic device paper
2. extract directly usable parameters
3. mark missing fields explicitly
4. keep assumption-filled fields transparent rather than hidden
5. run the same simulator stack with a literature-derived profile identity

This is stronger than a purely synthetic stress profile, even though it is not yet a full measured-device closure.

## What Still Needs Digitization / Follow-Up

The next Perplexity or manual extraction pass should target the exact missing pieces below.

### Highest value

1. digitized conductance traces from Supplementary Fig. 15 to convert the repeatability evidence into an explicit `sigma_c2c`
2. a more defensible mapping from `V_th` spread to conductance-domain `sigma_d2d`, or direct conductance-uniformity statistics if present in supplementary material
3. digitized retention points from Fig. 2d if we later decide to fit a conservative retention model
4. if Fig. 2d is fit later, test stretched-exponential first and only promote a double-exponential form if the digitized curve shape actually supports two timescales

### Also useful

5. whether the paper reports a power-law or other explicit photoresponse nonlinearity
6. whether dark current can be read off safely from any figure or supplementary plot
7. whether the paper gives a responsivity value in physical units

## Safe Manuscript Framing

Use this case-study profile as:

- `literature-derived fitted-profile demonstration`
- `bridge-interface evidence`
- `not yet a full measured-device validation loop`
- `PDF-backed literature case-study with transparent proxy estimates`

Do **not** write:

- that all fields are measured directly
- that the literature NL metric has already been calibrated into our surrogate NL parameter
- that this single case study fully validates the framework
