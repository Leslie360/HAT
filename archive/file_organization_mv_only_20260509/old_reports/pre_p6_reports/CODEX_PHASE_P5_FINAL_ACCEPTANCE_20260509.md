# Codex Phase P5 Final Acceptance

**Date:** 2026-05-09
**Owner:** Codex
**Scope:** Post-audit lock, cold-unpack reproducibility, data map, remote tasks, repo hygiene

## Verdict

**P5 accepted.** Kimi completed all Tracks A-F, DS and Mimo both audited PASS, and no blocker remains.

## What P5 Proved

| Area | Verdict | Notes |
|---|---|---|
| Post-audit scientific drift | PASS | Table 5 locked at `0.04/0.07/4.01 pp`; Gemini Fresh-minus-24h mutation removed |
| Cold-unpack reproducibility | PASS | Tarball unpacks, SHA passes, all PDFs rebuild |
| Data location map | PASS | User-facing lookup exists |
| Remote 105/107 task refresh | PASS | Task file is ready for server/GitHub copy |
| GPU queue | PASS | GPU idle; queue exists but was conservative |
| Repo hygiene plan | PASS | Conservative; no push without user approval |

## Codex Position On Experiment Completeness

The Paper-1 main claim is submission-ready, but the broader experiment program is **not fully saturated**.

Use this distinction:

1. **Paper-1 main submission:** sufficient and frozen.
2. **Paper-1 supplement / defense strength:** useful gaps remain.
3. **105 cross-architecture validation:** incomplete until seed789 and same-architecture digital comparisons close.
4. **107 analog KV-cache Work-2:** promising but still pending corrected-noise rerun and core math/code packet.
5. **Local GPU:** idle; should be used for bounded, non-contaminating补强 experiments.

Therefore P6 is required: not because Paper-1 is broken, but because the project can still become stronger and better defended.

## Immediate Gaps To Close

| Gap | Importance | Current Status |
|---|---|---|
| 6-bit PCM source count mismatch | Medium | Fresh n=4, source_best n=3 because seed123 training history is missing |
| 105 seed789 closure | Medium/High | Server-dependent; needed for cross-architecture validation |
| 107 corrected-noise rerun | High for Work-2 | Remote pending; trend must survive bug fix |
| Existing data statistical CIs/effect sizes | Medium | Can be done locally, no GPU |
| Local GPU safe补强 queue | Medium | GPU idle; needs controlled launch criteria |
| Draft residue / repo hygiene | Low/Medium | Needs final cleanup before any push |

## Acceptance Conditions

P5 is accepted, and P6 is authorized.
