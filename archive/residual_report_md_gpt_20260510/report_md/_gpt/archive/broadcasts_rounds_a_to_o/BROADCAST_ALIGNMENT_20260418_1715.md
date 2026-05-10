# Broadcast Alignment — 2026-04-18 17:15

## Purpose

This memo reconciles the current authoritative state after the interrupted turn. It supersedes any stale live-status statements embedded inside earlier broadcasts, but does **not** rewrite those historical dispatch files.

## Authoritative current state

### 1. Round-D bookkeeping

- `CX-J` is complete.
  - file exists: `CLAUDE_A_DECISION_PRELIM_20260418.md`
- `CX-K` is complete.
  - file exists: `R1_R4_LANDING_AUDIT_20260418.md`

### 2. R1–R4 landing truth

- `R1` abbreviation hardening: landed in source
- `R2` methodology-clarity pass: landed in source
- `R4` limitations / outlook framing: landed in source
- `R3` data-rigor pass: **partial only**

The two live `R3` gaps are:

1. `88.53` OPECT result carries uncertainty in `05_results.tex`, but **not** yet in the abstract.
2. the inverse-gamma `+5.8 pp` claim is now scoped as a single-seed deterministic result, but still lacks a proper uncertainty estimate.

### 3. Canonical fresh-instance cadence numbers are already locked

Do **not** treat cadence as still incomplete. The completed artifact is:

- `report_md/_gpt/json_gpt/fresh_instance_cadence_control.json`

Locked values:

- fixed: `10.00 ± 0.00%`
- epoch: `86.33 ± 1.61%`
- batch: `89.48 ± 0.36%`

### 4. Severe-NL lane truth

#### Source-domain lanes

- baseline severe `NL=2.0`: `27.72 ± 0.82%`
- `MLP-only`: `87.79%` best, `86.22%` final
- `QKV-only`: `18.72%` best, `10.15%` final
- `all-linear`: `87.49%` best, `84.81%` final

#### Fresh-instance lanes currently known

- `MLP-only`: `32.12 ± 7.72%`
- `QKV-only`: `10.01 ± 0.10%`
- `all-linear`: **still pending**

Editorial implication remains the same as the preliminary decision memo:

- keep the severe-`NL` mitigation story in the supplement / response package,
- do not promote it to a new main-text contribution on current evidence.

### 5. GPU ownership

The active GPU lane is:

- `attn_proj-only` severe-NL training
  - log: `logs/_gpt/train_tinyvit_v4_nl2_attn_proj_linear_comp_20260418_1700.log`

The earlier raw `wsl.exe` attempt to launch `all-linear` fresh-instance should **not** be treated as a confirmed active run.

Reason:

- the outer wrapper appeared,
- but no inner WSL Python child was confirmed,
- and no output artifact was created.

### 6. Kimi coordination

Kimi has been re-briefed using:

- `KIMI_DISPATCH_20260418_nl_fresh_transfer_gpt.md`

Required next Kimi output:

- `KIMI_NL_FRESH_TRANSFER_INTERPRETATION_20260418.md`

## Which files now define the current truth

Use these in this order:

1. `report_md/_gpt/AGENT_SYNC_gpt.md`
2. `report_md/_gpt/BROADCAST_ALIGNMENT_20260418_1715.md`
3. `report_md/_gpt/CLAUDE_TASK_gpt.md`
4. `report_md/_gpt/CLAUDE_A_DECISION_PRELIM_20260418.md`
5. `report_md/_gpt/R1_R4_LANDING_AUDIT_20260418.md`
6. `report_md/_gpt/NL_LANE_RESULTS_20260418.md`

## Do not claim the following anymore

- that `all-linear` fresh-instance is currently running
- that `R1–R4` are all fully landed
- that cadence control is still unfinished
