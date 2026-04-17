# Doctor Measured Profile Audit

- Generated: `2026-04-16T23:43:00`
- Source root: `Doctoral PPT raw TXT export (pages 3, 4, 20)`
- Output JSON: `/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/doctor_measured_profiles.json`

## Fitted Profiles

| Profile | G_min | G_max | Range | n_states | sigma_c2c | sigma_d2d | tau_1 | tau_2 | A_0 | gamma |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Doctor OECT Nonvolatile RC-16 | 3.636e-09 | 2.089e-08 | 5.75 | 16 | 0.0027 | 0.0000 | 10.829 | 192686549.203 | 0.965 | 0.877 |
| Doctor OECT Nonvolatile RC-64 | 2.457e-09 | 1.519e-08 | 6.18 | 64 | 0.0037 | 0.0000 | 10.829 | 192686549.203 | 0.965 | 0.877 |

## Raw-data Mapping

- `第20页/16.txt`, `第20页/64.txt`: extracted stable readout ladders and emitted as `inl_table`.
- `第四页/d/256次线性作图.txt`: used for programming residual noise and `pulse_count_max=262`.
- `第四页/e/s0-s5.txt`: used for duplicate-trace repeatability and retention fitting.
- `第四页/i/pot.txt`: used to fit `I_dark`, `responsivity_alpha`, and `gamma_phys`.
- `第三页/a/小图.txt`: retained as the auxiliary `Origin ExpDec1 fit of G` diagnostic sheet for panel `(a)`.
- `第三页/a/小图_raw_ppf_points.txt`: direct raw `PPF index vs ΔT` points supplied manually after inspecting the inset source.
- `第三页/g/图.txt`, `第三页/h/100sID.txt`, `第三页/b/5-20paule.txt`, `第三页/c/300-800.txt`: parsed and summarized as auxiliary volatile/RC evidence, but not injected into the nonvolatile weight-storage profile.

## Limitations

- `sigma_d2d` is set to `0.0` because no explicit multi-device mismatch distribution was present in the supplied PPT raw export.
- Third-page panel `(a)` inset now has both raw points and fit diagnostics archived, but the current nonvolatile profile schema still has no direct short-term facilitation / PPF field.
- Fourth-page panel `(m)` was image-only; the available `(l)` raw file was not forced into the JSON profile without a clean mapping.

## Photoresponse Fit

- points: `4`
- R^2: `0.9970`

