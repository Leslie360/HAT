# Local GPU CNN-vs-ViT Fresh-Instance Ensemble HAT Tasklist — 2026-05-10

## Objective

Test whether Ensemble HAT's fresh-instance robustness is architecture-specific to Tiny-ViT or also holds for a CNN baseline under comparable analog device variation.

## Thesis/Paper value

This closes the architecture-generality gap:

> if ViT benefits more than CNN, the thesis can argue attention/patch-mixing interacts with hardware-instance overfitting; if both benefit, HAT is a general training principle.

## Start condition

Start only when:

- mixed-precision P0 is complete or paused, and
- `nvidia-smi` confirms no active local training conflict.

Do not launch concurrently with another local GPU training job unless the user explicitly approves capacity.

## Output paths

- `thesis/results/cnn_vs_vit_hat/`
- `thesis/figures/cnn_vs_vit_hat/`
- `logs/local_gpu_cnn_vs_vit_hat_*_20260510.log`
- `coordination/agent_reports/Codex/LOCAL_GPU_CNN_VS_VIT_HAT_REPORT_20260510.md`

## Tasks

### H0 GPU and provenance preflight

- Run `nvidia-smi` and record GPU, utilization, VRAM used/free.
- Confirm no ongoing local GPU training.
- Locate existing ViT/HAT checkpoint and eval scripts.
- Locate existing CNN baseline, if present.
- Tee all command output to `logs/` with timestamped log files.

### H1 Choose comparable models

Prefer minimal new engineering:

1. Existing Tiny-ViT / ViT Paper1 model.
2. Existing ConvNeXt/CNN baseline if already present.
3. If no valid CNN baseline exists, use the smallest already-supported CNN training/eval path rather than adding a new architecture.

Record parameter counts, dataset, checkpoint identity, and analog-layer mapping.

### H2 Define evaluation matrix

Minimum pilot matrix:

| Model | Training | Fresh instance eval | D2D seeds | Status |
|---|---|---|---:|---|
| ViT | baseline/no HAT | yes | >=3 | required if checkpoint exists |
| ViT | Ensemble HAT | yes | >=3 | required |
| CNN | baseline/no HAT | yes | >=3 | required |
| CNN | Ensemble HAT | yes | >=3 | required if training path exists |

If full CNN HAT training is too expensive, run inference-only perturbation first and mark results as pilot.

### H3 Metrics

Record:

- clean/fresh accuracy.
- mean fresh-instance accuracy across D2D seeds.
- standard deviation across D2D seeds.
- worst-seed accuracy.
- retention/drift metric if available in the same eval path.
- compute cost and peak VRAM.

Output TSV:

`thesis/results/cnn_vs_vit_hat/cnn_vs_vit_hat_summary_20260510.tsv`

### H4 Figures

Create:

- `thesis/figures/cnn_vs_vit_hat/fig_architecture_hardware_overfitting_20260510.png`
- optional PDF version.

Figure should show baseline vs Ensemble HAT robustness for ViT and CNN side by side.

## Success criteria

Strong success:

- Ensemble HAT improves fresh-instance robustness for both architectures, or
- ViT and CNN diverge clearly enough to support an architecture-specific thesis discussion.

Moderate success:

- Inference-only probe identifies whether CNN is less/more sensitive than ViT.

Negative result still useful if:

- CNN does not benefit from Ensemble HAT, showing Paper1's mechanism is more architecture-dependent than originally framed.

## Stop conditions

- No comparable CNN path exists without invasive code changes.
- Baseline eval cannot reproduce known locked metrics.
- GPU capacity would saturate VRAM.
- Any required change touches Paper1 release files or protected checkpoints/data.

## Evidence labels

- Inference-only comparison: pilot/protocol evidence.
- Multiseed training + fresh-instance eval: thesis candidate claim.
