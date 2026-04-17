#!/usr/bin/env python3
"""
Finalize P13 full-result artifacts from the latest shared-regime JSON export.

The live benchmark script writes to the shared-regime staging paths. This helper
copies the final numeric payload into the reviewer-facing `full_result` files
required by the Codex dispatch once the long run completes.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path("/home/qiaosir/projects/compute_vit")
SRC_JSON = ROOT / "report_md" / "_gpt" / "json_gpt" / "p13_aihwkit_shared_regime_result.json"
DEST_JSON = ROOT / "report_md" / "_gpt" / "json_gpt" / "p13_aihwkit_full_result.json"
DEST_MD = ROOT / "report_md" / "_gpt" / "P13_aihwkit_full_result.md"


def main() -> None:
    if not SRC_JSON.exists():
        raise SystemExit(f"Missing source JSON: {SRC_JSON}")

    data = json.loads(SRC_JSON.read_text())
    effective_test_samples = int(data.get("subset_size", data.get("test_samples", 0)))
    requested_test_samples = int(data.get("test_samples", 0))
    if effective_test_samples <= 0:
        raise SystemExit("Source JSON does not contain a valid evaluation result.")
    if effective_test_samples < 10000 and requested_test_samples not in (10000,):
        raise SystemExit(
            f"Source JSON is not a full CIFAR-10 result yet "
            f"(effective_test_samples={effective_test_samples}, requested_test_samples={requested_test_samples})."
        )

    DEST_JSON.parent.mkdir(parents=True, exist_ok=True)
    DEST_MD.parent.mkdir(parents=True, exist_ok=True)
    DEST_JSON.write_text(json.dumps(data, indent=2))

    md = "\n".join(
        [
            "# P13 AIHWKIT Full CIFAR-10 Benchmark",
            "",
            "| Framework | Regime | Accuracy |",
            "|:--|:--|:--|",
            f"| PyTorch digital | FP32 baseline ({data['digital_device']}) | `{data['digital_acc']:.2f}%` |",
            (
                f"| AIHWKIT | shared regime ({data['analog_device']}, {data['eval_runs']} runs, "
                f"quant={data['quant_bits']}, adc={data['adc_bits']}, "
                f"σ_C2C={data['sigma_c2c']}, σ_D2D={data['sigma_d2d']}) | "
                f"`{data['analog_mean_acc']:.2f} ± {data['analog_std_acc']:.2f}%` |"
            ),
            "",
            "| Item | Value |",
            "|:--|:--|",
            f"| Checkpoint | `{data['checkpoint']}` |",
            f"| Checkpoint epoch | `{data['checkpoint_epoch']}` |",
            f"| Checkpoint best acc | `{data['checkpoint_best_acc']:.2f}%` |",
            f"| Effective test samples | `{effective_test_samples}` |",
            f"| Requested test-samples arg | `{requested_test_samples}` |",
            f"| Batch size | `{data['batch_size']}` |",
            f"| Wall clock | `{data['wall_clock_s']:.1f}s` |",
            f"| Delta (analog - digital) | `{data['delta_acc']:+.2f}%` |",
        ]
    )
    DEST_MD.write_text(md + "\n")
    print(f"Wrote {DEST_MD}")
    print(f"Wrote {DEST_JSON}")


if __name__ == "__main__":
    main()
