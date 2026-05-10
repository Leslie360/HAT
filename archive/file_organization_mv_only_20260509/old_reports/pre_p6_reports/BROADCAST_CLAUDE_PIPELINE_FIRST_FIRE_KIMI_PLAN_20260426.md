# BROADCAST — Pipeline First-Fire + Kimi Plan Review + Number Correction
**Date:** 2026-04-26 21:40 CST
**From:** Claude
**To:** User / DS / Gemini / Kimi / Codex
**Status:** Pipeline auto-fired on `tasks/r11d_4bit_pathb_narrative_integration.md`. Kimi (planner) → ds_flash (coder) handoff already in `broadcast.md`.

---

## 1. Pipeline first fire confirmed

User invoked `agents-do tasks/r11d_4bit_pathb_narrative_integration.md` after Claude wrote the first pipeline task file. Result in project-root `broadcast.md`:

- 13:33:33Z `user → kimi` — task spec verbatim
- 13:35:37Z `kimi → ds_flash` — full implementation plan

Pipeline working as advertised. Claude's role going forward: write `tasks/<task_id>.md`, do not write per-role dispatches.

---

## 2. Kimi's plan — 4 substantive additions over Claude's spec

Claude's task spec was good but Kimi tightened it on 4 axes:

### 2.1 NUMBER CORRECTION — AIHWKit 8-bit
- **Claude spec said:** AIHWKit 8-bit = 87.34 ± 0.14%
- **Kimi pulled from `paper2_aihwkit_baseline/checkpoints/fresh_eval.json`:** mean = 87.2820, std = 0.1286 → **87.28 ± 0.13%**
- Claude verified: Kimi is correct. The 87.34±0.14 figure that propagated through earlier reports was from a CODEX_R10E summary, not the actual JSON.
- **Going forward, locked number is 87.28 ± 0.13%** (not 87.34 ± 0.14%).
- This is a 0.06pp difference; story unchanged (still robust at 8-bit) but every paper edit must use 87.28.

### 2.2 Discussion subsection placement specified
- Kimi: insert new subsection `\subsection{Comparison to established analog HAT primitives}` between `\subsecref{implications}` and `\subsecref{limitations}` in `06_discussion.tex`.
- Cleaner than Claude's "near existing AIHWKit citation" — gives a deterministic anchor.

### 2.3 Supplementary table anchor specified
- Kimi: place the 4-row comparison table inside existing `\subsection{Comparison with Inorganic RRAM Baselines}` (~L638), AFTER existing AIHWKit prose paragraph.
- Reuses an existing zone instead of creating a new one.

### 2.4 Locked-number guard update — NEW STEP
- Kimi added Step 4: update `scripts/_gpt/check_locked_numbers.py` to pin 14.64 and 87.28 so future edits can't silently drift them.
- This is defensive scaffolding Claude did NOT request. Good catch.

---

## 3. Compile gate (Kimi's spec)

Both must return RC 0 with zero undefined refs:
```
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex
```
Plus locked-number guard:
```
/home/qiaosir/miniconda3/envs/LLM/bin/python scripts/_gpt/check_locked_numbers.py
```

Output target:
```
outputs/r11d_4bit_pathb_narrative_integration_20260426-213333.md
```

---

## 4. R11D-2 σ=0.20 clean — final result

Background fact relevant to Discussion §6 framing (does NOT enter this task; stored for next round):

- **Best test:** 87.60% (epoch 99 of 100)
- **Fresh-eval (10 inst × 5 MC):** **87.52% ± 0.05%**
- File: `paper2_aihwkit_baseline/checkpoints/r11d_2_sigma020_clean/fresh_eval.json`
- Versus contaminated original (85.04% ± 0.11%): +2.48pp gain — **contamination call by Codex validated**.
- **Implication:** AIHWKit @ 8-bit handles σ=0.20 stress fine (87.52 ≈ 87.28 canonical). High-noise stress at 8-bit does NOT break AIHWKit. Path B revival rests entirely on the **4-bit precision regime**.

R11D-3 σ=0.30 auto-launched after R11D-2 cleared 80% threshold; epoch 7/100, ETA ~1.7h.

---

## 5. Tasks ready in pipeline format

| File | Status |
|:--|:--|
| `tasks/r11d_4bit_pathb_narrative_integration.md` | **FIRED** — Kimi planning done; ds_flash coding in progress |
| `tasks/r11c_paper_integrity_fixit.md` | READY — 11-issue bundled fix-it; not yet fired |

---

## 6. Required action

- @User — DS will be writing edits next. Do not interleave manual paper edits during pipeline run.
- @DS — execute Kimi plan from `broadcast.md` 13:35:37Z. Use **87.28 ± 0.13%** (not 87.34 ± 0.14%).
- @Codex — when DS hands back, you are reviewer. Apply decision rule from task spec.
- @Gemini — on standby for critic phase + later figure work; no immediate action.
- @All — V6 PHANTOM fix at `paper/latex_gpt/supplementary.tex:132` (82.58 single-seed) is in working tree; do not regress.
