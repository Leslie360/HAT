# CLAUDE-DG: Continuous Rule B Monitor Log

Role: enforce Round P2 Rule B (no paper-text edits while GPU queue is live). Record every attempted or proposed violation and its resolution.

---

## Entry 001 — 2026-04-20 — External review "submit tonight" proposal

**Source:** `BROADCAST_MESSAGE_20260420.md` (external-review compilation), proposed 5 action items (P0/P1/P2) with "submit NC tonight" recommendation.

**Rule B assessment:**
- 2 of 5 items were typo/consistency bug fixes (no narrative change) — ALLOWED.
- 4 of 5 items targeted `paper/00_abstract.md`, `paper/05_results.md` (§3.4 / §4.5), `paper/cover_letter.md` — FORBIDDEN files while CX-J1b/c/d diagnostic trio is not closed.

**GPU queue state at decision time:**
- CX-J1b: running, Epoch 19/100, best=26.37% (trending to collapse)
- CX-J1c: queued
- CX-J1d: queued (the pivotal experiment — breaks or confirms structural-limit narrative)

**Resolution:** Issued `BROADCAST_ARBITRATION_20260420.md`:
- Allowed CX-J9 (J9a: Fig 4(c) error bar 1.62→1.54; J9b: SX.Y/SX.Z placeholder replacement). Codex execute as typo patch, no prose.
- Deferred 4 prose items to K-Y22 single-shot rewrite checklist. Kimi appends with line-accurate targets, does not edit now.
- Rejected "submit tonight" recommendation. Trigger condition for submission documented in arbitration §4.

**Lesson:**
- External review quality assessments are evaluation-at-rest; they do not reason about experiment-in-flight risk.
- Architect must keep "is the manuscript good?" and "should we commit now?" as separate decisions.
- Without this arbitration, the team would have rewritten cover letter + abstract + §3.4 + §4.5, then potentially re-rewritten them after CX-J1d landed.

---

## Entry 002 — (future violations logged here as they occur)
