# BROADCAST FINAL PUSH — Depth Phase, PhD-Graduation-Gated
**Date:** 2026-04-24
**From:** Claude (Chief Architect)
**To:** Kimi, Codex, Gemini
**Supersedes:** BROADCAST_REBUILD_3WEEK_20260424.md (rebuild plan absorbed here; hard-dates dropped)
**Status:** ACTIVE

---

## 0. Headline

- Paper-1 submission gated by PhD student's graduation clearance. **Several months of buffer.**
- Real D2D/C2C device data incoming (pre-graduation internal delivery possible).
- **Shift from "rebuild within 3 weeks" to "deepen until ready"**.
- Remote A100 retired. Local GPU + new 8×40GB persistent server. No urgent compute.
- All agents work against `NARRATIVE_PIVOT_20260424.md` as single source of truth.

---

## 1. What changed vs previous broadcasts

| Previous mode | Current mode |
|:--|:--|
| Rebuild in 3 weeks with hard checkpoints FA/FB/FC | Months of depth-accumulation, no hard dates |
| Replicate post-fix results urgently | Replicate opportunistically, prioritize theory+audit |
| Work 2 deferred as paper-2 only | Work 2 upgraded to "medium scope" preliminary section in paper-1 |
| Literature-prior D2D/C2C forever | Literature-prior NOW, measured-calibrated post-data-landing |
| Remote A100 active | Retired; all compute local |

---

## 2. Task matrix

Dispatch files are live in `report_md/_gpt/DISPATCH_*.md`. Read them; do not re-ask.

| Dispatch ID | Owner | Priority | File | Time budget |
|:--|:--|:--:|:--|:--|
| KIMI-THEORY-1 | Kimi | HIGHEST | `DISPATCH_KIMI_THEORY_1_20260424.md` | unconstrained |
| KIMI-W2-OUTLOOK | Kimi | MEDIUM (after THEORY-1) | `DISPATCH_KIMI_W2_OUTLOOK_20260424.md` | unconstrained |
| KIMI-K-DRAFT-V3 | Kimi | HIGH (after THEORY-1 Methods paragraph) | `DISPATCH_KIMI_K_DRAFT_V3_20260424.md` | unconstrained |
| GEMINI-G-AUDIT-CODE | Gemini | HIGH | `DISPATCH_GEMINI_G_AUDIT_CODE_20260424.md` | unconstrained |
| CODEX-CX-FRESH-EVAL-MSERIES | Codex | HIGH | `DISPATCH_CODEX_FRESH_EVAL_MSERIES_20260424.md` | ~3-6 GPU-h |
| CODEX-CX-PLOT-REFRESH | Codex | MEDIUM (after fresh-eval) | `DISPATCH_CODEX_PLOT_REFRESH_20260424.md` | no GPU |
| REMOTE-8X40GB-CROSS-ARCH | 8×40GB server | HIGH (active) | `REMOTE_DISPATCH_8X40GB_CROSS_ARCH_20260424.md` | ~5-7 days wall-clock |
| CLAUDE-DATA-INGEST | Claude | STANDING | `DATA_INGEST_PROTOCOL_20260424.md` | activate on data arrival |

---

## 3. Role boundaries (reaffirm)

- **Kimi**: theory derivation, paper text rewrites, Work 2 outlook, narrative polish. No experiments, no code.
- **Codex**: all GPU execution (local only now), plot regeneration, regression-guard maintenance. No paper text.
- **Gemini**: error-finding ONLY — code audit (G-AUDIT-CODE), hostile review, consistency checks. No design, no theory, no drafts.
- **Claude**: architecture, integration, AGENT_SYNC curation, user-facing briefings, data-ingest readiness, final integration.

---

## 4. Infrastructure tasks (Claude-owned, standing)

- Monitor AGENT_SYNC for any drift toward old severe-NL narrative
- Monthly ping on PhD team data status
- On real data landing: run R-D0 QQ plot within 24 hours, brief user
- Integration gates: every K-DRAFT-v3 file requires Claude read + zone check before `.tex` swap

---

## 5. What we are NOT doing

- No new A100 dispatches (remote retired)
- No paper text edits by anyone but Claude at integration (Kimi produces `.kimi_draft_v3` sidecars)
- No arxiv preprint before Gemini G-AUDIT-CODE clean
- No NC submission — target is Nature Electronics after PhD defense
- No new experiments until real D2D/C2C data arrives (exception: CX-FRESH-EVAL-MSERIES which is just evaluation, no training)
- No bug retrospection in paper body

---

## 6. Failure modes to prevent

- **Narrative drift**: if a draft reintroduces severe-NL ceiling language, flag immediately
- **Zone violation**: number cited without 3A/3B/3C placement — halt the draft
- **Bug reappearance**: Gemini G-AUDIT-CODE + CX-REGRESSION guard are the two layers; run CX-REGRESSION before any new checkpoint is accepted
- **Data leakage**: measured D2D/C2C is under embargo until PhD defense — do NOT include raw data in any arxiv/GitHub commit until clearance

---

## 7. Open questions for the user (no action required now)

1. When real D2D/C2C lands, do we want to run cross-architecture validation (ViT-Small / DeiT-Small on TinyImageNet)? Not needed for paper-1 core, but would add breadth. ~2 GPU-weeks local.
2. Work 2 scope escalation: should Codex start preliminary KV-cache mapping experiment during the wait, aiming for "maximum scope" paper-1 Outlook? Not urgent.
3. Arxiv preprint strategy: submit preprint without measured-D2D once theory+audit land, or hold everything for post-defense simultaneous release?

Claude awaits user signal on these; no default action taken.

---

## 8. One-liner

**We have months. Build it right. NARRATIVE_PIVOT is the spec. No one edits .tex except Claude at integration.**
