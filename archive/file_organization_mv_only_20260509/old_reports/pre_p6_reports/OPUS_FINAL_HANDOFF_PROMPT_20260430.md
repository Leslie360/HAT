# Claude Opus Final Handoff Prompt — 2026-04-30

Use this after reading:

```text
report_md/_gpt/OPUS_FINAL_COUNCIL_PACKET_20260430.md
```

## Current Consensus

All filled model sections agree: ask Claude Opus now. Do not wait five days for Remote 105 seed789.

Reason: Remote 105 is validation/SI/thesis material, not the core paper-1 spine. The local paper-1 evidence is sufficient for architectural direction.

## What Changed Since The Previous Opus Brief

1. Remote 105 crashed; seed789/new-seed results are delayed about five days.
2. Local 6-bit PCM was corrected: the old weak seed456 was an early-stop artifact.
3. Corrected 6-bit PCM is strong:
   - source best: 77.8767 ± 0.5829%
   - fresh: 77.8611 ± 0.5639%
   - 1d drift drop: 0.1033pp
4. This changes the PCM story from a binary 4-bit vs 8-bit contrast into a 4/6/8-bit precision ladder.
5. DeepSeek found a drift-eval preset bug for PCMPresetDevice; Codex verified and fixed it in:
   - `paper2_aihwkit_baseline/eval_aihwkit_drift.py`
   - `paper2_aihwkit_baseline/eval_aihwkit_drift_extended.py`
   The fix strictly resolves checkpoint `pcm_preset` and no longer falls back to UnitCell for Device drift eval. Both files pass `py_compile`.
6. Remote 107 has updated `origin/107-clean` to `aca7dd5`, but selective last1/last2 fresh-D2D eval is still incomplete. Treat 107 as Work-2.

## Model Opinions Summary

### Codex

- Ask Opus now.
- Paper-1 remains local: pure 4-bit failure + Ensemble HAT rescue + PCM precision ladder.
- 105 is conditional SI/thesis validation.
- 107 is separate Work-2.
- Kill universal superiority wording.

### Kimi

- Strongly supports precision-ladder framing.
- 6-bit is Pareto midpoint, not failed.
- Show 6-bit late recovery transparently, preferably SI figure + one honest main-text sentence.
- Do not put 105 in main text.
- Do not revive R11D-T1 or progressive quantization pre-submission.

### Gemini

- Hostile reviewers will attack physical-measurement absence, arbitrary noise distributions, missing 105 seed789, and 6-bit p-hacking risk.
- Avoid phrases like "PCM physical properties act as natural regularizers" and "proportional HAT outperforms digital baselines".
- No new local experiments unless a code bug demands rerun.
- Prioritize audit and wording discipline.

### DeepSeek

- Ask Opus now.
- Identified drift eval preset bug; Codex fixed it.
- Early-stop patience=10 is unsafe for canonical PCM precision-ladder runs.
- Canonical PCM precision runs should use `--early-stop-patience 0` or no early stop before epoch 90.
- Progressive quantization, DOREFA, lr sweeps, more UnitCell repeats should be killed/deferred.

## Final Questions For Claude Opus

Please write the final arbitration into Section 8 of:

```text
report_md/_gpt/OPUS_FINAL_COUNCIL_PACKET_20260430.md
```

Answer explicitly:

1. Confirm whether we proceed now without Remote 105 seed789.
2. Confirm paper-1 spine after corrected 6-bit result.
3. Decide final PCM framing: 4-bit feasibility vs 4/6/8-bit precision ladder.
4. Decide whether 6-bit late-recovery curve goes in main text or SI.
5. Decide whether 105 appears in main text, SI, thesis, or future work.
6. Decide whether 107 is mentioned in paper-1 at all.
7. Give exact next 7-day task list for Kimi / Gemini / DeepSeek / Codex.
8. Give kill/freeze list.
9. Give safe / unsafe / forbidden wording table.
10. Give final instruction to the user if Claude is unavailable afterward.

## Recommended Claude Opening

```text
I have read OPUS_FINAL_COUNCIL_PACKET_20260430.md and the post-fill handoff. I will now write the final arbitration into §8. My ruling treats Remote 105 as non-blocking, Remote 107 as Work-2, and the corrected local 6-bit PCM result as the key update that shifts paper-1 toward a 4/6/8-bit precision-ladder narrative.
```
