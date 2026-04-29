# Task: R11D-1 4-bit Path B Narrative Integration

**task_id:** r11d_4bit_pathb_narrative
**priority:** HIGHEST (substantive paper finding; Path B revival)
**target output:** `outputs/r11d_4bit_pathb_narrative.md`

---

## Background (read before planning)

R11D-1 just landed. AIHWKit baseline at **4-bit precision** (matched to our paper's canonical 4-bit weights):
- Train collapsed: best 15.01% at epoch 21 (early stopped)
- **Fresh-instance eval: 14.64 ± 0.11% across 10 instances**
- Source: `paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/fresh_eval.json`

Compare to existing paper-1 numbers (all CIFAR-10 Tiny-ViT-5M, fresh-instance):
- Standard HAT (fixed mask, 4-bit): 10.00% — collapses
- AIHWKit baseline 8-bit (R10E): 87.34 ± 0.14% — robust at canonical
- **AIHWKit baseline 4-bit (R11D-1): 14.64 ± 0.11% — collapses**
- Ensemble HAT 4-bit canonical: 86.16 ± 0.19% (Round-10 R10A 3-seed) — robust

**Key narrative finding:** AIHWKit's per-batch noise injection achieves cross-instance robustness at 8-bit but collapses at 4-bit precision. Ensemble HAT survives both. This is **Path B revival**: method-superiority restored in the realistic-deployment-precision regime (4-bit is paper-1's canonical setting).

---

## Goal

Integrate R11D-1 finding into manuscript without breaking existing zone discipline / wording bans / numerical claims. Specifically:

1. **Discussion §6.x** — write a 4-6-sentence paragraph framing the 4-bit AIHWKit collapse vs Ensemble HAT survival. Place near existing AIHWKit literature mention or create new subsection "Comparison to established analog HAT primitives".
2. **Cover letter** — add 1 sentence highlighting this differentiating evidence.
3. **Supplementary** — add a comparison table (Standard HAT / AIHWKit @ 8-bit / AIHWKit @ 4-bit / Ensemble HAT @ 4-bit) for completeness.

The text should:
- Cite Rasch et al. 2021 (`rasch2021aihwkit`) for AIHWKit
- Frame finding as method-superiority IN THE 4-BIT REGIME, not blanket superiority (be honest about 8-bit parity)
- Use neutral protocol language (no "post-fix"/"deployment-fidelity" without the hook qualifier)
- Maintain "structural analogue" wording for theory connections
- Word budget ≤ +200 words main + 100 words cover letter + small table

---

## Decision rule (for reviewer/critic phase)

**Approve** if the paragraph:
- States both numbers (AIHWKit 4-bit 14.64±0.11% vs Ensemble 86.16±0.19%) with proper provenance
- Honestly notes 8-bit parity (AIHWKit 87.34% ≈ Ensemble 86.16%)
- Frames 4-bit as "realistic deployment precision" (it is — paper §5.6 iso-accuracy operating envelope)
- Avoids overclaim of universal superiority
- Cites Rasch 2021 properly
- Stays within word budget

**Reject** if it:
- Hides the 8-bit parity result
- Claims general superiority over AIHWKit
- Uses banned wording
- Breaks paper compile

---

## Specific output expected

The pipeline should produce in `outputs/r11d_4bit_pathb_narrative.md`:

1. **Discussion paragraph** (~150 words) — placement target: `paper/latex_gpt/sections/06_discussion.tex` near existing AIHWKit citation if any, otherwise end of comparison subsection
2. **Cover letter sentence** (~30 words) — placement target: `paper/latex_gpt/cover_letter.tex` in the contribution-summary paragraph
3. **Comparison table** (LaTeX) — placement target: `paper/latex_gpt/supplementary.tex` near existing method-comparison section
4. **Diff summary** showing exactly what changed in each file
5. **Compile verification**: confirm `latexmk -pdf main.tex` succeeds RC 0 zero undefined refs

---

## Files the pipeline should read

- `paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/fresh_eval.json` — R11D-1 raw data
- `paper2_aihwkit_baseline/checkpoints/fresh_eval.json` — R10E AIHWKit 8-bit canonical (87.34%)
- `report_md/_gpt/CODEX_R10E_AIHWKIT_BASELINE_REPORT_20260425.md` — R10E setup details
- `report_md/_gpt/CODEX_R10A_FINAL_INTEGRATION_REPORT_20260426.md` — Ensemble HAT 3-seed (86.16%)
- `paper/latex_gpt/sections/06_discussion.tex` — Discussion file to edit
- `paper/latex_gpt/cover_letter.tex` — cover letter to edit
- `paper/latex_gpt/supplementary.tex` — supplementary to edit

---

## Constraints

- **No new science** — only synthesis of existing R10E + R11D-1 + R10A numbers
- **No new figures in this task** — figure work is a separate task (pipeline can hand off to Gemini critic for visual review only)
- **Compile must pass** — pipeline doc step verifies via `latexmk`
- **Keep word count discipline** — main body ≤ 5,700 words after this task
- **Zone tagging** — these AIHWKit numbers form a new zone (call it "AIHWKit comparison" zone) with explicit citation provenance

---

## Done definition

- 3 files edited (discussion, cover letter, supplementary)
- Diff summary in output
- main.tex + supplementary_main.tex compile clean
- Final paragraph reads naturally from a senior reviewer's perspective
