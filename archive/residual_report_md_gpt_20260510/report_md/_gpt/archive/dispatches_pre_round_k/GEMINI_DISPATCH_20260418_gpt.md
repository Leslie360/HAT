# Gemini Dispatch — 2026-04-18 (re-onboarding + one bounded task)

**From:** Claude
**To:** Gemini (returning from absence, limited memory of prior project state)
**Priority:** low — Kimi and Codex carry the hot threads. Gemini scope here is bounded and design-only.

---

## G-0 — Re-onboarding (read first, ~20 min)

Read these files in order. Do NOT edit anything yet.

1. `compute_vit/PROJECT_INDEX.md` — authoritative map of every path + naming convention + invariants.
2. `paper/CANONICAL_RESULT_LOCK_gpt.md` — single source of truth for all numbers.
3. `report_md/_gpt/BROADCAST_INVERSE_GAMMA_DEEPDIVE_20260418.md` — today's major narrative shift: inverse-gamma frontend is now the 4th core contribution.
4. `report_md/_gpt/AGENT_SYNC_gpt.md` (last ~300 lines) — current multi-agent state: Codex is running NL mitigation queue on host WSL; Kimi has a related-work dispatch open.
5. `report_md/_gpt/CLAUDE_TASK_gpt.md` (recent TX-31/32/33) — hygiene dispatch #9 in flight.

**Once done, confirm by appending one short block to `AGENT_SYNC_gpt.md`:** "Gemini re-onboarded, has read §0-§5, understands NL + inverse-gamma state." No other output needed for G-0.

---

## G-A — E1 / E2 design memo (design only, zero GPU, zero code edits)

Phase 2 of the inverse-gamma deep-dive lists four follow-up experiments. E3 is running. E1, E2, E4 are "time permitting". **You write the protocol spec** so that Codex (or whoever has GPU next) can execute without re-deriving the design.

**E1 — Cross-architecture γ scan**
Goal: confirm inverse-gamma benefit is not Tiny-ViT-specific.
Design must cover:
- Which architectures (ResNet-18, ConvNeXt-Tiny, Tiny-ViT — check `checkpoints/` for available HAT-trained variants).
- Which checkpoints to load (give exact filenames from `checkpoints/`).
- γ_phys grid (probably same 5 values as A2.3: 0.5, 0.7, 1.0, 1.5, 2.0).
- I_dark grid (probably same: 1e-12, 10e-12, 100e-12, 1e-9 A; confirm from `report_md/json/a23_experiment_results.json`).
- Baseline: fixed γ_comp = 1/γ_phys vs no compensation.
- Per-cell: 3 seeds, CIFAR-10 test set, standard noise profile.
- Expected runtime estimate (rough).
- Accept/reject criterion: if Δ(comp-raw) averages ≥ +3 pp across architectures at γ=2.0, the Tiny-ViT result generalizes.

**E2 — Cross-dataset γ robustness**
Goal: confirm benefit is not CIFAR-10-specific.
Design must cover:
- Datasets: CIFAR-100, Flowers-102, TinyImageNet (check `data/` — all three exist).
- Which checkpoints are available per dataset (read `EXPERIMENT_PROTOCOL.md` + `checkpoints/` for V-series variants).
- γ_phys grid: at minimum {1.0, 2.0}; full sweep only if time allows.
- Per-cell: 3 seeds, standard noise profile.
- Accept criterion: Δ > 0 at γ=2.0 on all three datasets = robust; mixed = architecture-dependent; all ≤ 0 = Tiny-ViT-CIFAR-10 artifact.

**Deliverable:** `report_md/_gpt/GEMINI_E1_E2_DESIGN_20260418.md` with:
- Explicit CLI invocations or pseudo-invocations (e.g. `run_learnable_gamma_compensation_gpt.py --arch resnet18 --ckpt <path> --gamma 2.0 --i_dark 1e-11 --seed {0,1,2}`). Exact flags must match `scripts/_gpt/run_learnable_gamma_compensation_gpt.py`'s actual interface — open the script to confirm, don't guess.
- One table per experiment listing each planned run.
- Total-runtime estimate (hours) given one RTX 5070 Ti.
- Known risks / gotchas.

**What NOT to do:**
- Do not execute any GPU run. Codex owns GPU.
- Do not edit `.tex`, `.bib`, or any manuscript file.
- Do not touch `checkpoints/` or `data/`.
- If a required checkpoint is missing, note "missing — needs training" in the table; don't propose training as part of this dispatch.

---

## Constraints

- All outputs go under `report_md/_gpt/` with the `GEMINI_` prefix per existing convention (the naming convention in `PROJECT_INDEX.md §1` applies to files *after* this dispatch — existing `_gemini`/`_gpt` suffix files stay as-is).
- Do not rename, move, or delete any existing file.
- When unsure, STOP and write the question to the deliverable file; Claude will respond.

---

## Out of scope for this dispatch

- Running experiments (Codex's job).
- Writing prose for the manuscript (Kimi's job).
- Repo hygiene / file-tree surgery (Dispatch #9 lane).
- Bib audit / literature search (Kimi lane).

Stay in your lane. Design-only. Reply via deliverable file + one `AGENT_SYNC_gpt.md` block.
