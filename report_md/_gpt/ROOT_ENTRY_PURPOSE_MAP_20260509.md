# Root Entry Purpose Map

Date: 2026-05-09
Status: updated after R3 report/coordination migration.

| Entry | Purpose | Future target / action |
|---|---|---|
| `.git` | Git repository metadata | keep root |
| `.gitignore` | Git ignore rules | keep root |
| `EXPERIMENT_PROTOCOL.md` | project documentation entrypoint | keep root or move to docs/ later |
| `LICENSE` | license | keep root |
| `MASTER_PLAN.md` | project documentation entrypoint | keep root or move to docs/ later |
| `PROJECT_INDEX.md` | project documentation entrypoint | keep root or move to docs/ later |
| `README.md` | repository overview | keep root |
| `README_REPRODUCIBILITY_PAPER1.md` | project documentation entrypoint | keep root or move to docs/ later |
| `RELEASE_CHECKLIST.md` | project documentation entrypoint | keep root or move to docs/ later |
| `REPRODUCIBILITY.md` | project documentation entrypoint | keep root or move to docs/ later |
| `ROOT_REORG_PLAN_20260509.md` | root reorganization execution plan | keep root until reorg complete |
| `WORKSPACE_LAYOUT.md` | workspace layout documentation | merge into canonical WORKSPACE_LAYOUT.md later |
| `WORKSPACE_LAYOUT_V2_20260509.md` | workspace layout documentation | merge into canonical WORKSPACE_LAYOUT.md later |
| `amp_utils.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
| `analog_layers.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
| `analog_layers_ensemble.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
| `archive` | restorable archive and reorg outputs | keep root; do not stage blindly |
| `auto_fitted_profile.json` | source/resource or local entry | review |
| `broadcast.md` | active multi-agent broadcast | move/copy to coordination/active later |
| `checkpoints` | large local checkpoints | data_local/checkpoints, no broad commit |
| `coordination` | new dispatch/audit/remote-task organization root | active R3 target |
| `data` | datasets | data_local/datasets, no broad commit |
| `device_profile_utils.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
| `device_profiles` | supporting project resources | review for tools/data_local placement |
| `download_data.sh` | source/resource or local entry | review |
| `environment.yml` | environment/dependency definition | keep root |
| `eval_fresh_instances.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
| `eval_fresh_instances_postfix.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
| `eval_imagenet_analog.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
| `eval_literature_profile.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
| `eval_measured_profile.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
| `eval_resnet18_checkpoints.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
| `experiments` | new experiment execution root | fill during R7 |
| `hybrid_calibration.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
| `hybrid_runtime_compiler.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
| `inference_analysis_utils.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
| `internal` | supporting project resources | review for tools/data_local placement |
| `logs` | current execution logs | keep root or experiments/logs later |
| `model_profiling.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
| `notebooks` | supporting project resources | review for tools/data_local placement |
| `paper` | current Paper-1 manuscript plus thesis legacy tree | split into paper1/ and thesis/ after acceptance |
| `paper1` | new Paper-1 reports/layout root | continue filling with manuscript/release after acceptance |
| `paper2` | Work-2 KV-cache project | move to work2/kv_cache later |
| `paper2_aihwkit_baseline` | Work-2 AIHWKit/PCM experiments | move to work2/aihwkit_pcm later |
| `physical_noise_pipeline.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
| `release_artifacts` | final submission and provenance artifacts | split into paper1/release and paper1/provenance later |
| `report_asset_paths.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
| `report_md` | compatibility report hub with active index/sync only | keep minimal entrypoint |
| `requirements-optional.txt` | environment/dependency definition | keep root |
| `requirements.txt` | environment/dependency definition | keep root |
| `scripts` | scripts and validation/plotting tools | split into tools/ and experiments/scripts later |
| `tasks` | task definitions | coordination/tasks later |
| `tests` | test suite | keep root |
| `tinyvit_hybrid_utils.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
| `tools` | new reusable tool root | fill during R7 |
| `train_convnext.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
| `train_resnet18.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
| `train_tinyvit.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
| `train_tinyvit_ensemble.py` | top-level training/eval/source script | keep until import/path audit, then tools/experiments |
