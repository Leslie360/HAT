# Local GPU Fresh-Instance Protection Sharded Report — 20260510

## Evidence grade

- `fresh-instance/full-test/sharded-n10-mc1`: full CIFAR-10 test split, 10 held-out D2D instances, one C2C MC pass per instance.
- This reaches the canonical instance count, but still uses one MC pass per instance rather than the multi-MC final protocol.
- Batch size was reduced to 64 and instances were run sequentially to avoid GPU freezes.

## Summary

| Strategy | Mean acc. | Std | Min | Max | Gain vs fresh |
|---|---:|---:|---:|---:|---:|
| `fresh_all_analog` | 10.00% | 0.00 | 10.00% | 10.01% | +0.00 pp |
| `freeze_top20_d2d` | 67.63% | 3.32 | 61.17% | 71.46% | +57.63 pp |
| `freeze_top30_d2d` | 85.97% | 1.02 | 84.18% | 87.72% | +75.97 pp |
| `freeze_top42_d2d` | 91.71% | 0.22 | 91.44% | 92.10% | +81.71 pp |

## Interpretation

- `fresh_all_analog` remains at chance level across 10 held-out instances.
- Protecting the top 20 layers gives a partial but more variable rescue.
- Protecting the top 30 layers is stable around 86%, close to the top42/source-domain ceiling around 91.7%.
- This supports sensitivity-ranked protection as a deployment-design candidate; final claim-bearing validation still needs multi-MC replication per instance.

## Artifacts

- Rows: `thesis/results/mixed_precision/fresh_instance_protection_maps_sharded_20260510.tsv`
- Summary: `thesis/results/mixed_precision/fresh_instance_protection_maps_sharded_summary_20260510.tsv`
- Figure: `thesis/figures/mixed_precision/fig_fresh_instance_protection_maps_sharded_20260510.png`
