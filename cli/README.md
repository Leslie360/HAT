# cli/

Thin user-facing wrappers around train/eval commands.

The implementation modules live in `../src/compute_vit/`. Wrappers preserve command-line entry points without keeping implementation files in the repository root.

## Current wrappers

- `train_tinyvit.py`
- `train_tinyvit_ensemble.py`
- `train_convnext.py`
- `train_resnet18.py`
- `eval_fresh_instances.py`
- `eval_fresh_instances_postfix.py`
- `eval_imagenet_analog.py`
- `eval_literature_profile.py`
- `eval_measured_profile.py`
- `eval_resnet18_checkpoints.py`
- `model_profiling.py`
- `physical_noise_pipeline.py`
- `hybrid_runtime_compiler.py`

## Rule

Run wrappers from the project root, e.g. `python cli/eval_fresh_instances.py --help`.
