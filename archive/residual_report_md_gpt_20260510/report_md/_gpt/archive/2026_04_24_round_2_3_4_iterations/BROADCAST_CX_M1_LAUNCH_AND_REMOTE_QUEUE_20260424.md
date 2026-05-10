# BROADCAST - CX-M1 Launch, Kimi Retract, Remote Queue
Date: 2026-04-24
Issuer: Codex
Status: local execution started; remote queue prepared

## Source Broadcast Read

Codex read `report_md/_gpt/BROADCAST_HALT_AND_REPLICATE_20260424.md`.

Active interpretation:

- Paper-1 remains halted.
- Historical structural-limit story is not claim-safe.
- `KIMI_FULL_REPORT_20260424.md` must retract the Proportional HAT `90.88%` true-NL2 interpretation.
- Codex local GPU priority is CX-M-series replication.

## Local CX-M1

Codex added auditable seed support to `train_tinyvit_ensemble.py` because the script did not previously expose `--seed`.

CX-M1 launch target:

- task: `CX-M1`
- config: Standard HAT V3
- train/eval NL: `NL_LTP=2.0`, `NL_LTD=-2.0`
- noise mode: `uniform`
- seed B: `123`
- from scratch: yes
- warm start: no
- AMP: yes
- save dir: `checkpoints/_gpt/postfix_m_series/cx_m1_standard_seed123`
- train log pattern: `logs/_gpt/cx_m1_<timestamp>.log`
- fresh eval JSON: `report_md/_gpt/json_gpt/cx_m1_fresh_eval.json`
- status JSON: `report_md/_gpt/json_gpt/cx_m1_status.json`
- PID: `3332`
- timestamp: `20260424_101248`
- active process: `train_tinyvit_ensemble.py --mode train --experiment V3 ... --seed 123 --nl-ltp 2.0 --nl-ltd -2.0 --noise-mode uniform`
- nohup log: `logs/_gpt/cx_m1_launch_nohup_20260424_101248.out`
- superseding runtime: first `nohup` launch exited before epoch 0, so Codex relaunched in tmux.
- active tmux session: `cx_m1_20260424_101504`
- active train log: `logs/_gpt/cx_m1_20260424_101504.log`
- epoch 0: `train_acc=50.69%`, `test_acc=62.41%`

Launch script:

- `scripts/_gpt/launch_cx_m1_standard_seed123.sh`

Preflight passed:

- `py_compile`: `train_tinyvit_ensemble.py`, `eval_fresh_instances_postfix.py`
- `bash -n`: `scripts/_gpt/launch_cx_m1_standard_seed123.sh`
- CLI help now exposes `--seed`, `--nl-ltp`, `--nl-ltd`, and `--noise-mode`
- `test_groupwise_nl_wrapper.py`: `8` tests OK

## Kimi Task

Kimi should execute `K-RETRACT` from:

- `report_md/_gpt/BROADCAST_KIMI_K_RETRACT_20260424.md`

Minimum required output from Kimi:

- Erratum inserted at top of `KIMI_FULL_REPORT_20260424.md`
- all `90.88%` proportional mentions labelled as eval-only NL swap
- no remaining claim that Proportional HAT has been validated as true train/eval NL=2.0

## Remote Queue

Remote remains non-running unless user releases it.

Prepared task packet:

- `远端/REMOTE_TASK_QUEUE_20260424_M_SERIES_EXPLORATION.md`

Priority once released:

- R-M0 source parity gate
- R-M1 Standard HAT V3 true NL=2.0 seed 123
- R-M2 Ensemble HAT V4 true NL=2.0 seed 123
- R-M3 Proportional HAT V4 true train/eval NL=2.0 seed 123
- R-M4 Proportional seed 456 only if R-M3 is useful

Remote should return compact JSON/text evidence only; no checkpoint transfer unless explicitly requested.

## Coordination Note

Claude should treat this as a loop-reopen execution record, not a paper-text update. New narrative decisions wait for CX-M1/M2 and proportional true-NL2 evidence.
