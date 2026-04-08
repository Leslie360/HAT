# Gemini Takeover Brief (GPT)

This file is the shortest handoff for Gemini to continue from the current Codex state.

## Scope Split

- Gemini owns:
  - `/home/qiaosir/projects/compute_vit/paper_zh/*`
- Codex-completed English assets to mirror against:
  - `/home/qiaosir/projects/compute_vit/paper/*.md`
  - `/home/qiaosir/projects/compute_vit/paper/latex_gpt/*`

## Locked Scientific Boundaries

- Tiny-ViT corrected retention:
  - `rapid early drop followed by a broad plateau near 79%`
  - do not reuse the obsolete `84.28%` wording for Tiny-ViT
- ConvNeXt corrected retention:
  - keep distinct from Tiny-ViT; ConvNeXt long-time plateau is around `84.3%`
- `Flowers-102`:
  - write as `low-data boundary` / `data-volume floor`
  - do not write as universal method failure
- `Task 34`:
  - write as `distribution-matched recovery`
  - not universal robustness
- `Task 35`:
  - write as `major remaining failure mode`
- `Task 36`:
  - write as `architecture-gap evidence under richer physics`
  - not proof that CNNs are universally robust
- manuscript-wide downgrade:
  - `first-order behavioral simulation framework`

## Locked Result References

- `/home/qiaosir/projects/compute_vit/paper/CANONICAL_RESULT_LOCK_gpt.md`
- `/home/qiaosir/projects/compute_vit/paper/FIGURE_CAPTION_LOCK_gpt.md`
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/SUBMISSION_PACKET_gpt.md`

## Most Important English Updates Already Landed

- `§2` now explicitly contrasts:
  - NeuroSim
  - MemTorch
  - AIHWKIT
- `§4` now explicitly defines:
  - `V4_proportional_HAT`
  - `V4_NL2_HAT`
  - `C4_proportional_HAT`
- `§5/§6/§7` wording has been softened to submission-ready claim strength
- LaTeX `sections/05-07` are no longer short placeholders; they now carry near-submission prose

## What Gemini Should Do Next

1. Keep `paper_zh/*` aligned with the files above, not with old logs or chat memory.
2. Preserve the `best vs MC` distinction, especially for `ConvNeXt / Flowers-102`.
3. Mirror the new simulator-tool differentiation in Chinese `§2`.
4. Mirror the physical-extension setup paragraph in Chinese `§4`.
5. Mirror the `~79%` Tiny-ViT retention wording and the `Flowers-102` low-data framing.

## What Gemini Does Not Need to Redo

- rerun experiments
- reinterpret `Task 34/35/36`
- rebuild figures from scratch
- infer numbers from logs

Use the locked English-side artifacts instead.
