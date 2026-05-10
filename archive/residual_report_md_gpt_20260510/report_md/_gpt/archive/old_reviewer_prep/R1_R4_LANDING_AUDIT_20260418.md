# R1–R4 Landing Audit — 2026-04-18

## Scope

Audit the claimed autonomous landings for the four Claude review bundles:

- `R1` = abbreviation first-use hardening
- `R2` = calculation / methodology one-line clarifications
- `R3` = data-rigor patches (`n`, test name, error-bar language)
- `R4` = limitations / future-physics framing

## Verification method

1. grep the active manuscript sources under `paper/latex_gpt/sections/` and `paper/latex_gpt/supplementary.tex`
2. confirm the compiled artifacts exist:
   - `paper/latex_gpt/main.pdf`
   - `paper/latex_gpt/supplementary_main.pdf`
3. use the latest successful compile state as the PDF-surface proxy

### Limitation

The current shell does not provide `pdftotext`, `mutool`, or a Python PDF-text parser. Therefore this audit verifies:

- source presence,
- compiled-PDF existence,
- absence of compile failures,

but does **not** perform byte-level PDF text extraction in this pass. Any row marked `source landed` should therefore be read as "present in the active compiled source" rather than as a separate OCR/text-extraction proof.

## Build state checked

- `paper/latex_gpt/main.pdf` exists
- `paper/latex_gpt/supplementary_main.pdf` exists
- active manuscript sources are present and non-empty

## Audit table

| Bundle | Claimed landing | Source evidence | Status | Notes |
|:--|:--|:--|:--:|:--|
| R1 | `ADC` expanded on first use | `00_abstract.tex`: `analog-to-digital converter (ADC)` | ✅ | Landed in abstract source. |
| R1 | `D2D` expanded on first use | `00_abstract.tex`: `device-to-device (D2D)` | ✅ | Landed in abstract source. |
| R1 | `HAT` expanded on first use | `00_abstract.tex`: `hardware-aware training (HAT)` | ✅ | Landed in abstract source. |
| R1 | `OPECT` expanded on first use | `00_abstract.tex`: `organic photoelectrochemical transistor (OPECT)` | ✅ | Landed in abstract source. |
| R1 | `CNN` / `ViT` expanded | `01_introduction.tex`: `convolutional neural network (CNN)` / `Vision Transformer (ViT)` | ✅ | Landed in introduction source. |
| R1 | `MLP` expanded | `01_introduction.tex`: `multi-layer perceptron (MLP)` | ✅ | Landed in introduction source. |
| R1 | `SRAM` expanded | `01_introduction.tex`: `static random-access memory (SRAM)` | ✅ | Landed in introduction source. |
| R1 | `IR` expanded | `01_introduction.tex`: `current--resistance, or IR, drop` | ✅ | Landed in introduction source. |
| R1 | `LTP/LTD` expanded | `03_methodology.tex`: `long-term potentiation` / `long-term depression` | ✅ | Landed in methodology source. |
| R1 | `Monte Carlo (MC)` expanded | `05_results.tex` Fig. 4 caption and main text | ✅ | Landed in results source. |
| R2 | operator split explicitly listed | `03_methodology.tex` first paragraph | ✅ | Analog/digital operator lists now explicit. |
| R2 | scale-recovery branch usage clarified | `03_methodology.tex` after Eq. 4 | ✅ | Standard vs retention recalibration use-case is now explicit. |
| R2 | Ensemble HAT expectation estimator clarified | `03_methodology.tex` after Eq. 6 | ✅ | States one mismatch map per epoch, held fixed within epoch. |
| R2 | fresh-instance distribution clarified | `03_methodology.tex` after Eq. 7 | ✅ | Defines fresh arrays as iid Gaussian D2D draws, distinct from C2C. |
| R2 | shot-noise proportionality clarified | `03_methodology.tex` after Eq. 9 | ✅ | States coefficient absorbed into per-profile calibration. |
| R2 | Sobol estimator clarified | `03_methodology.tex` §Sensitivity and Energy Metrics | ✅ | Direct estimator over 7×9 MC grid now stated. |
| R3 | OPECT headline number carries uncertainty in main results | `05_results.tex`: `88.53±0.08%, n=10` | ✅ | Results-section landing is present. |
| R3 | OPECT headline number carries uncertainty in abstract | `00_abstract.tex`: still `88.53%` only | ⛔ | Not fully landed. Abstract still omits `±0.08` and `n=10`. |
| R3 | inverse-gamma `+5.8 pp` claim now scoped | `05_results.tex`: `single-seed deterministic evaluation` | 🔶 | Better than before, but still not a full error-bar landing. |
| R3 | fresh-instance significance names the test and n | `05_results.tex`: `one-sample t-test ... n=10` | ✅ | Test family and sample size are now explicit. |
| R3 | cadence / seed-policy clarity | `03_methodology.tex` Sobol paragraph | ✅ | Independent MC sampling policy now stated. |
| R4 | explicit deferred physical effects in Limitations | `06_discussion.tex` Limitations paragraph | ✅ | IR drop, sneak paths, temperature dependence, spatial correlation, heavy tails are enumerated. |
| R4 | framework positioned as decision aid, not chip emulator | `06_discussion.tex` last sentence | ✅ | Landed in source. |
| R4 | future circuit-aware extension explicitly framed | `06_discussion.tex` Outlook paragraph | ✅ | Landed in source. |
| R4 | appendix-side provenance / sensitivity framing retained | `08_appendix.tex` provenance + Zhang-proxy sections | ✅ | Appendix source present and non-empty. |

## Summary

### Fully landed

- `R1` abbreviation pass: **substantially landed** in the active manuscript source.
- `R2` methodology-clarity pass: **landed**.
- `R4` limitations / outlook framing: **landed**.

### Partially landed

- `R3` data-rigor pass is **not fully complete**.

The largest remaining gaps are:

1. **OPECT 88.53 headline**
   - Results section now carries `88.53±0.08%, n=10`.
   - Abstract still says only `88.53%`.

2. **Inverse-gamma +5.8 pp claim**
   - It is now scoped as a `single-seed deterministic evaluation`.
   - It still does not carry a proper uncertainty estimate.

## Audit conclusion

The Round-D broadcast claim that `R1–R4` were all fully landed is **too strong**.

A defensible refined statement is:

- `R1`, `R2`, and `R4` are landed in the active manuscript source.
- `R3` is only **partially** landed and still needs a small follow-up pass if we want the broadcast to match reality.

That follow-up is editorial, not architectural.
