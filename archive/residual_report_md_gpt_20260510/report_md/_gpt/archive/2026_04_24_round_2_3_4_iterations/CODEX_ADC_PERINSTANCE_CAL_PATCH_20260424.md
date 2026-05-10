# Codex ADC Per-Instance Calibration Patch

Date: 2026-04-24
Task: R3-3 Stage 1 from `DISPATCH_CODEX_ROUND3_PATCHES_20260424.md`
Owner: Codex

## Verdict

R3-3 Stage 1 is complete: code patch + unit test only.

No M-series ADC re-evaluation was launched. Stage 2 remains gated on Claude/user signal or 8x40GB remote return.

## Patch

Files changed:

| File | Change |
|:--|:--|
| `inference_analysis_utils.py` | `calibrate_adc_ranges(...)` now accepts `use_current_noise` and `disable_c2c` flags. Default behavior is unchanged. |
| `scripts/_gpt/eval_fresh_instances_adc_ablation.py` | ADC range calibration moved inside the fresh-instance loop, after D2D resampling. |
| `scripts/_gpt/eval_fresh_instances_adc_ablation.py` | Output JSON now records `adc_calibration_scope=\"per_instance\"`, `adc_calibration_noise=\"current_d2d_with_c2c_disabled\"`, and calibrated module counts per instance. |
| `inference_analysis_utils.py` | ConvNeXt imports are now optional so TinyViT-only ADC evaluation does not fail in environments without `torchvision`. |
| `test_adc_perinstance_calibration.py` | New regression test confirming ADC ranges differ across synthetic D2D realizations. |

Key code locations:

| Location | Purpose |
|:--|:--|
| `inference_analysis_utils.py:531` | Extended `calibrate_adc_ranges(...)` signature |
| `inference_analysis_utils.py:556` | Optional calibration on current D2D state |
| `scripts/_gpt/eval_fresh_instances_adc_ablation.py:122` | Per-instance calibration call after D2D resampling |
| `scripts/_gpt/eval_fresh_instances_adc_ablation.py:164` | JSON provenance marks per-instance calibration |
| `test_adc_perinstance_calibration.py:60` | Range-difference sanity test across 3 D2D draws |

## Protocol Semantics

For each fresh instance:

1. Seed RNG for the instance.
2. Resample D2D buffers with the target `sigma_d2d` and `noise_mode`.
3. Calibrate ADC output ranges on the current D2D instance.
4. Disable C2C during calibration to avoid mixing cycle-to-cycle randomness into the static ADC range estimate.
5. Attach `ADCQuantHookManager` and run the requested MC evals.

The old static calibration path remains available through the default `calibrate_adc_ranges(bundle, max_batches=N)` call.

## Validation

Commands run:

```bash
/home/qiaosir/miniconda3/bin/python test_adc_perinstance_calibration.py
/home/qiaosir/miniconda3/bin/python test_dual_bug_fix.py
/home/qiaosir/miniconda3/bin/python test_groupwise_nl_wrapper.py
/home/qiaosir/miniconda3/bin/python scripts/_gpt/eval_fresh_instances_adc_ablation.py --help
```

Results:

| Test | Result |
|:--|:--|
| `test_adc_perinstance_calibration.py` | passed |
| `test_dual_bug_fix.py` | `All 7 tests passed` |
| `test_groupwise_nl_wrapper.py` | `Ran 9 tests ... OK` |
| ADC ablation CLI import/help | passed |

## Impact

- No training launched.
- No fresh-eval launched.
- Existing static-calibration ADC report remains the locked Round-2 result until Stage 2 is explicitly fired.
- This patch only prepares the corrected per-instance calibration path for the future gated rerun.

## Stage 2 Gate

Do not run Stage 2 until explicitly signaled.

When fired, rerun ADC-on 8-bit for M1..M6 and compare against the static-calibration dual report:

- expected recovery: `+0.2` to `+0.8` pp;
- escalation threshold: `> 2 pp` recovery, per Claude Round-3 trigger.
