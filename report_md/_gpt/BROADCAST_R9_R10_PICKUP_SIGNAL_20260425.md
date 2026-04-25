# BROADCAST — Round-9 + Round-10 PICKUP SIGNAL
**Date:** 2026-04-25 23:30 CST
**From:** Claude (Chief Architect)
**Status:** All dispatches live + on GitHub master @ commit `844b0f7d`. Agents pick up immediately.

---

## 0. What this is

Single consolidated **PICKUP SIGNAL** for both Round-9 (presentation hardening) and Round-10 (substantive completion). Read your dispatch + start working.

---

## 1. @ Codex — START NOW

**Priority order (ABSOLUTE)**: R10A → R10D → R10E → R9B TikZ → R8 W2 Phase 2

**Round-10 (highest priority)** — `DISPATCH_CODEX_R10_EXPERIMENTS_20260425.md`:
1. **R10A** multi-seed canonical Ensemble HAT — kick off NOW (3 seeds × 100 epochs). This replaces the single-seed 86.37% headline. ~25 GPU-h.
2. **R10B** Standard HAT 10% mechanism class-distribution analysis — 4h, no new training.
3. **R10D** intermediate NL sweep (NL=1.2/1.5/1.8) — ~30 GPU-h.
4. **R10E** AIHWKit head-to-head baseline — ~10 GPU-h. Install AIHWKit in separate conda env.

**Round-9** — `DISPATCH_CODEX_R9B_TIKZ_SCHEMATICS_20260425.md`:
- TikZ rebuild fig1/fig2/figS3 (CPU only, parallel-friendly).

**Round-8 Work 2 Phase 2** continues at reduced bandwidth (30%). Pythia 410M Ensemble HAT training. If GPU contention with R10: paper-1 R10 wins (W2 has buffer; paper-1 doesn't).

**Your bandwidth split**: 50% R10 + 20% R9B + 30% W2 P2. Document provenance in every JSON output.

---

## 2. @ Kimi — START NOW

**Priority order**: R10I → R10F → R10C → R10G → R10H → R10B-text → R9A length surgery (last)

**Round-10 framing** (TODAY 1 hour) — `DISPATCH_KIMI_R10_FRAMING_20260425.md`:
- **R10I** "1.5 scenarios" reframing — 1 hour, edits abstract+intro+discussion+cover letter.

**Round-10 characterization** (Days 1-3) — `DISPATCH_KIMI_R10_CHARACTERIZATION_20260425.md`:
- **R10F** literature freshness audit (1 day) — find 2025-2026 prior art for Ensemble HAT.
- **R10C** OPECT distribution stats (1 day, with Codex assist for QQ + AD test).
- **R10H** energy ε literature provenance table (4h).

**Round-10 framing** (Days 2-4) — same framing dispatch:
- **R10G** Tobin/AIHWKit novelty contrast paragraph (4h).
- **R10B-text** integration (30 min after Codex R10B lands).

**Round-9** — `DISPATCH_KIMI_R9A_LENGTH_SURGERY_20260425.md` + `DISPATCH_KIMI_GEMINI_R9C_DEFENSE_20260425.md`:
- **R9A** length surgery — START Day 6+ AFTER R10 finishes. Target shifts to 5,900 words (was 5,500) due to R10 additions.
- **R9C** defense paragraphs — partly superseded by R10D evidence; write the rest.

**Your bandwidth split**: 50% R10 (Days 1-5) → 50% R9A+C (Days 6-10).

---

## 3. @ Gemini — STAND BY

**Days 1-5**: no Round-10 task. Standby.

**Days 6-7**: substantive audit of R10 deliverables (per-concern verification — does R10A actually close A1? does R10E actually close D2?).

**After R9 + R10 all close**: G-HOSTILE-V2 final hostile-reviewer simulation fires. Read `DISPATCH_GEMINI_HOSTILE_REVIEW_V2_SPEC_20260425.md`. Output: paper-1 submission-ready verdict.

---

## 4. Cold-start file order (any agent reading this fresh)

1. `INDEX.md` — file map
2. `BROADCAST_ROUND10_LAUNCH_20260425.md` — most recent broadcast
3. `BROADCAST_ROUND9_HARDENING_20260425.md` — presentation track
4. `CLAUDE_ROUND10_SUBSTANTIVE_COMPLETION_PLAN_20260425.md` — master plan
5. Your specific dispatch file (in §1-§3 above)
6. `NARRATIVE_PIVOT_20260424.md` — narrative source of truth
7. `CLAUDE_FORWARD_ROADMAP_20260425.md` §14 — 1-paragraph cold-start brief

---

## 5. Submission timeline (re-stated)

```
NOW → +5 days:    R9 + R10 parallel (you're working)
+5 → +7 days:     Claude integration pass + Gemini hostile-v2 audit
+7 → +10 days:    Final read-through + cover letter polish
+10 days:         submission-ready, awaiting PhD defense gate
```

After PhD defense clearance: SUBMIT to Nature Electronics.

---

## 6. What does NOT change

- NARRATIVE_PIVOT (zone partition, three-scenario evidence — to be reframed via R10I)
- All numerical claims preserved (R10 augments, doesn't replace, except R10A multi-seed which extends the headline)
- Wording bans unchanged
- Workspace doctrine unchanged
- 8×40GB cross-arch independent
- `paper/` files: only Kimi edits, only after R10 evidence lands

---

## 7. Escalation contact

If any of these hit: append immediately to AGENT_SYNC + tag @Claude:
- R10A any seed mean < 80%
- R10D non-monotonic with NL
- R10E AIHWKit beats Ensemble HAT
- R10B Standard HAT NOT single-class collapse
- R10C OPECT data unavailable in source paper
- R10F finds direct Ensemble HAT prior art

I'll handle each immediately when I see the AGENT_SYNC entry.

---

## 8. State of session (Claude side)

- Round-10 dispatches committed: `844b0f7d`
- GitHub master = local master = synced
- Background processes: all clean (no stale gc/repack/push runs)
- Disk: 17GB+ /tmp reclaimed; main repo `.git/` is 693MB
- No outstanding Claude task except monitoring AGENT_SYNC for incoming reports

Claude monitors. Agents work. PhD-graduation is the only external gate after this round closes.

**One-line**: paper-1 final substantive sprint LIVE; agents pick up dispatches per §1-§3; submission-ready in ~10 days.
