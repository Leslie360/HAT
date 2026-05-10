# paper2_aihwkit_baseline/

Work-2 AIHWKit/PCM baseline area. This belongs to the Paper2 / 107 lane, not Paper1 release evidence.

## Current contents

| Path | Purpose |
|:--|:--|
| `PCM_PROTOCOL.md` | Current PCM protocol notes. |
| `train_aihwkit_baseline.py`, `r11d*_train*.py` | Training scripts for AIHWKit/PCM baselines. |
| `eval_aihwkit_*.py` | Evaluation scripts for fresh/drift/extended checks. |
| `checkpoints/` | Local Work-2 checkpoint/results payloads, including valid, superseded, and invalid marked runs. See `checkpoints/INDEX_20260510.tsv`. |
| `r10e_tex_paragraph.tex` | Compatibility symlink to `../paper2/manuscript/snippets/r10e_tex_paragraph.tex`. |
| `data/` | Local Work-2 data payloads. |

## Rules

- Keep Work-2/107 evidence separate from Paper1 source data.
- Preserve invalid/contaminated markers; do not delete them silently.
- Before moving checkpoint payloads, create a size/provenance report and get explicit approval.
- Future ideal home is `paper2_107/aihwkit_pcm/`, but this directory remains active until a planned migration is executed.

## Related files

- `../paper2/README.md`
- `../coordination/remote_tasks/107/REMOTE_107_PHASE_P8_CORRECTED_NOISE_WORK2_TASKLIST_20260509.md`
- `../WORKSPACE_LAYOUT.md`
