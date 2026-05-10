# Local GPU Fresh-Instance Protection Sharded Report — 20260510

## Evidence grade

- `fresh-instance/full-test/sharded-n10-mc3`: full CIFAR-10 test split, 10 held-out D2D instances, 3 C2C MC passes per instance.
- Batch size was reduced to 64 and instances were run sequentially to avoid GPU freezes.

## Summary

| Strategy | Mean acc. | Std | Min | Max | Gain vs fresh | Runs |
|---|---:|---:|---:|---:|---:|---:|
| `fresh_all_analog` | 10.00% | 0.01 | 10.00% | 10.03% | +0.00 pp | 30 |
| `freeze_top20_d2d` | 67.65% | 3.21 | 61.17% | 71.70% | +57.65 pp | 30 |
| `freeze_top30_d2d` | 86.04% | 0.95 | 84.18% | 87.96% | +76.04 pp | 30 |
| `freeze_top42_d2d` | 91.66% | 0.19 | 91.27% | 92.10% | +81.66 pp | 30 |

## Interpretation

- `fresh_all_analog` remains at chance level across the full 10×3 protocol.
- Protecting the top 20 layers gives partial rescue but remains instance-sensitive.
- Protecting the top 30 layers is stable around 86%, close to the top42/source-domain ceiling around 91.7%.
- The 10×3 result is suitable as the current thesis-level fresh-instance evidence for sensitivity-ranked protection, while still representing an inference-time protection diagnosis rather than a fabricated hardware implementation.

## Artifacts

- Rows: `thesis/results/mixed_precision/fresh_instance_protection_maps_sharded_20260510.tsv`
- Summary: `thesis/results/mixed_precision/fresh_instance_protection_maps_sharded_summary_20260510.tsv`
- Figure: `thesis/figures/mixed_precision/fig_fresh_instance_protection_maps_sharded_20260510.png`
