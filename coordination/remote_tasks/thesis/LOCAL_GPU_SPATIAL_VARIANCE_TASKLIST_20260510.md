# Local GPU Spatial Variance / IR-Drop Tasklist — 2026-05-10

## Objective

Move beyond uniform device noise by testing layer-to-tile mapping under spatially non-uniform analog hardware profiles: IR drop, thermal gradient, and tile-specific D2D/nonlinearity severity.

## Thesis/Paper value

This work turns Paper1's algorithm-device frontier into a floorplan-aware deployment story:

> robust training is necessary but not sufficient; physical tile placement and non-uniform chip conditions determine deployment margins.

## Start condition

Start after mixed-precision P0 or if P0 is blocked by missing training hooks.

## Output paths

- `thesis/results/spatial_variance/`
- `thesis/figures/spatial_variance/`
- `logs/local_gpu_spatial_variance_*_20260510.log`
- `coordination/agent_reports/Codex/LOCAL_GPU_SPATIAL_VARIANCE_REPORT_20260510.md`

## Tasks

### S0 GPU/provenance preflight

- Run `nvidia-smi`.
- Confirm no active local training.
- Locate current device-profile interfaces.
- Tee logs.

### S1 Define tile profiles

Create a profile grid such as:

| Tile class | D2D | C2C | NL | Role |
|---|---:|---:|---:|---|
| good | 0.05 | nominal | 1.0 | high-quality center tile |
| nominal | 0.10 | nominal | 1.0 | baseline |
| weak | 0.15 | elevated | 1.2 | edge tile |
| bad | 0.20 | elevated | 1.5 or stress | corner/hot tile |

Output:

`thesis/results/spatial_variance/tile_profiles_20260510.json`

### S2 Define mapping strategies

Evaluate:

1. sequential layer-to-tile mapping.
2. random mapping.
3. sensitivity-aware mapping using mixed-precision P0 ranking.
4. worst-case mapping.

Output:

`thesis/results/spatial_variance/mapping_specs_20260510.tsv`

### S3 Evaluation matrix

Run inference/probe first, training only if needed.

For each mapping:

- baseline metric.
- fresh-instance metric.
- D2D seed variance.
- optional retention/drift after scale recalibration.

### S4 Figures

Create:

- `fig_tile_mapping_sensitivity_20260510.png/.pdf`
- `fig_floorplan_accuracy_tradeoff_20260510.png/.pdf`

## Success criteria

Strong success:

- sensitivity-aware mapping beats random and worst-case mapping by >=2-3 pp.

Moderate success:

- identifies which layer groups must avoid bad tiles.

Negative result still useful if:

- mapping has little effect after Ensemble HAT, implying training dominates floorplan variation under tested regimes.

## Stop conditions

- model-to-tile mapping requires invasive code changes.
- evaluation cannot reproduce nominal baseline.
- GPU capacity unsafe.

## Evidence labels

- Single-seed floorplan probe: pilot.
- Multiseed floorplan matrix: thesis candidate claim.
