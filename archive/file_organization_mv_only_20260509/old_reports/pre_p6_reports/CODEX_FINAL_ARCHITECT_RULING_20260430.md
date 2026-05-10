# Codex Final Architect Ruling — 2026-04-30

Canonical location: `report_md/_gpt/OPUS_FINAL_COUNCIL_PACKET_20260430.md`, Section 8.

Short ruling:

- Proceed now. Do not wait for Remote 105.
- Paper-1 spine: pure 4-bit quantization failure + Ensemble HAT rescue + PCM 4/6/8-bit precision ladder.
- Corrected 6-bit PCM is the key update: treat it as the tested Pareto midpoint, not as a failed line.
- 105 is optional SI/thesis validation only.
- 107 is Work-2 and should not enter paper-1 except possibly a one-sentence future-work note.
- Put 6-bit late-recovery curve in SI, with one honest main-text sentence.
- Keep drift preset bug fix; do not trust PCMPresetDevice drift results until rerun with fixed eval scripts.
