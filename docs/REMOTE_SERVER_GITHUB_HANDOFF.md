# Remote Server GitHub Handoff

This document is the entrypoint for an external GPU server that will pull this repository from GitHub and run **exploratory** experiments only.

## Mission

The remote server is **not** the source of record for final paper numbers.

Its job is to:
- use faster GPUs to identify the most informative experimental direction;
- tell us which narrative branch is most defensible;
- return only compact markdown summaries and small text artifacts;
- leave final manuscript-grade reruns and locked numbers to the local machine.

## What the remote agent should optimize for

Prioritize:
- fast branch discrimination;
- high-information experiments;
- small, interpretable outputs;
- minimal code changes;
- explicit recommendation of what we should reproduce locally.

Do **not** optimize for:
- publication-ready figures;
- full artifact packaging;
- large checkpoint transfers;
- editing the manuscript text.

## Current project question

The active scientific question is:

> Under severe write nonlinearity, is the current performance ceiling structural, or is it mainly a limitation of the first-order surrogate/training recipe?

The most important unresolved experiment is:
- `CX-J1d-2`: second-order STE / higher-order surrogate diagnostic

## First files the remote agent should read

1. `report_md/_gpt/GPU_REMOTE_EXPLORATION_BRIEF_20260421.md`
2. `report_md/_gpt/GPU_EXTERNAL_TASKLIST_20260421.md`
3. `report_md/_gpt/INDEX.md`
4. `report_md/_gpt/AGENT_SYNC_gpt.md`

Then inspect:
- `scripts/_gpt/run_tinyvit_groupwise_nl_comp.py`
- `train_tinyvit_ensemble.py`
- `analog_layers.py`

## How to run

Environment:
- Prefer the repo `environment.yml`
- Or `requirements.txt` if the server uses pip

Minimal install:
```bash
conda env create -f environment.yml
conda activate LLM
```

Sanity check:
```bash
python scripts/_gpt/check_locked_numbers.py
```

## What counts as a successful remote output

For each exploration wave, return one markdown file containing:
- exact command lines;
- short description of any code edits;
- compact result table;
- narrative implication;
- recommended local reproduction target.

Suggested naming:
- `REMOTE_GPU_EXPLORATION_WAVE1_YYYYMMDD.md`
- `REMOTE_GPU_EXPLORATION_WAVE2_YYYYMMDD.md`

## Hard constraints

While the live GPU loop is open, do **not** edit:
- `paper/00_abstract.md`
- `paper/05_results.md`
- `paper/06_discussion.md`
- `paper/cover_letter*.md`
- `report_md/_gpt/KIMI_REBUTTAL_MASTER_20260420.md`
- `paper/thesis/chapter_5_*.tex`

Allowed:
- new files under `scripts/_gpt/`
- new markdown reports under `report_md/_gpt/`
- exploratory code patches in simulator/training utilities

## Baseline facts the remote agent should assume

Known local results:
- `QKV-only linearization`: fails badly
- `full-attention linearization`: fails badly
- `joint MLP-linear + Ensemble HAT`: improves source-domain behavior but fresh-instance remains near `~30%`

Interpretation:
- attention-side fixes alone are not currently convincing;
- the remote search should focus on whether a **surrogate-fidelity upgrade** changes the conclusion.

## Checkpoint policy for the remote server

Do **not** ask for TIMM/TinyViT pretrained weights as a separate artifact.

For route-finding, the preferred minimal artifact is a single local baseline checkpoint:
- `checkpoints/V4_hybrid_standard_noise_hat_best.pt`

Why:
- it is enough to warm-start the key severe-NL follow-up experiments;
- it avoids depending on outbound model-weight downloads;
- it is more directly comparable to the current local results than restarting from ImageNet-pretrained weights alone.

Important:
- when using `--warm-start-from checkpoints/V4_hybrid_standard_noise_hat_best.pt`, do **not** require `--pretrained`;
- if the current wrapper still assumes `pretrained=True`, patch it locally so that warm-started runs build the model with `pretrained=False` and then load only `model_state_dict`.

## Deliverable style

Every remote report should answer:
1. Which experiment was most informative?
2. Did anything clearly move beyond `<35%`, `35-50%`, or `>50%`?
3. Which single experiment should be reproduced locally first?
4. Does the evidence currently favor:
   - structural limit
   - surrogate-limited story
   - ambiguous hybrid story

## Minimal human explanation

If someone on the remote side asks for the plain-language objective:

> We already know several obvious mitigation tricks do not rescue severe nonlinearity. We are now using faster GPUs to determine whether a better surrogate/training approximation changes the story enough to alter the paper’s core claim. The remote machine is for route-finding, not for final locked manuscript numbers.
