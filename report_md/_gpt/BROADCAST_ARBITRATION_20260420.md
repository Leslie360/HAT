# BROADCAST — Rule B Arbitration on External Review Compilation
**Date:** 2026-04-20
**Architect:** Claude (Opus 4.7)
**Trigger:** `BROADCAST_MESSAGE_20260420.md` proposed immediate NC submission with P0/P1/P2 paper edits.
**Status:** Proposal **PARTIALLY REJECTED**.

---

## 1. Why this arbitration

The external-review broadcast (10 reviewer perspectives, ⭐⭐⭐⭐⭐ readiness) recommended "submit tonight" after fixing 5 P0/P1/P2 items. **Four of those five edits target files that are frozen under Round P2 Rule B** (no paper-text edits while the GPU queue is live). CX-J1b is still running (Epoch 19/100, best=26.37%); CX-J1c and CX-J1d have not started. Accepting the submission-tonight recommendation would:

- violate the "close the loop before rewriting" rule the user explicitly set;
- risk a retract-and-resubmit if CX-J1d breaks the ~30% ceiling and falsifies the structural-limit narrative;
- invalidate the Round P2 timeline Kimi and Gemini are executing against.

The review compilation itself is valid. The timing of its call-to-action is wrong.

---

## 2. Ruling

### ✅ ALLOWED NOW (bug fixes, not content)

| Action | File | Owner | Rationale |
|:--|:--|:--|:--|
| CX-J9a | Figure 4(c) error bar `±1.62%` → `±1.54%` | Codex | Pure numeric consistency bug; no narrative change |
| CX-J9b | SX.Y / SX.Z placeholder → real section numbers | Codex | Typographic/reference fix; no narrative change |

Codex executes both as a single "typo/consistency patch", no prose edits. Rerun `check_locked_numbers.py` and PDF count verification.

### ❌ DEFERRED TO LOOP CLOSURE (prose edits; Rule B applies)

All four items below fold into `KIMI_PAPER_REWRITE_CHECKLIST_20260420.md` (K-Y22, Phase δ):

| Deferred item | Target file | Reason |
|:--|:--|:--|
| Abstract "(chance level for balanced 10-class task)" | `paper/00_abstract.md` | Rule B forbidden file |
| §4.5 training overhead footnote | `paper/05_results.md` | Rule B forbidden file |
| §3.4 strengthen no-AMP verification | `paper/05_results.md` | Rule B forbidden file |
| Cover letter framing (simulation baseline + risk ranking) | `paper/cover_letter.md` | Rule B forbidden file |

These items are **not wrong**; they are correctly identified. They wait.

### ❌ REJECTED: "submit tonight" recommendation

Rejected for three reasons:
1. CX-J1b/c/d diagnostic trio is the decision node for the entire thesis narrative. Submitting before it completes is a single-point bet.
2. User principle, stated explicitly on 2026-04-20: "把实验做完，闭环之后再写文章，这样就不会出现推翻前面".
3. The review compilation evaluated manuscript quality at rest; it did not evaluate manuscript stability against pending experimental outcomes.

---

## 3. GPU queue status (for context)

| Experiment | State | Latest |
|:--|:--|:--|
| CX-J1b QKV-only | 🔄 running | Epoch 19/100, best=26.37% — trending to collapse, consistent with structural-limit hypothesis |
| CX-J1c full-attention-linear | ⏸ queued | Auto-launch on J1b completion |
| CX-J1d higher-order NL surrogate | ⏸ queued | Auto-launch on J1c completion; **the pivotal experiment** |
| CX-J2–J8 | ⏸ queued | Tier-2/3/4, user-gated |

If J1b/c collapse AND J1d also stays near ~30%: structural-limit hypothesis confirmed → current manuscript narrative is correct → single-shot rewrite mostly cosmetic (~2 hours Kimi work).

If J1d breaks the ceiling: structural-limit narrative dies → paper needs a framing pivot (~1 week rewrite). This is exactly the scenario Rule B was written to avoid.

---

## 4. Trigger condition for single-shot rewrite + submission

The rewrite + submission sequence fires when ANY of the following is true:

1. CX-J1b + CX-J1c + CX-J1d all land (full diagnostic closure — preferred path);
2. User declares "GPU loop closed" with a stated reason;
3. External deadline (conference / reviewer pool constraint) forces early submission, in which case the user overrides Rule B explicitly.

No Kimi or Gemini agent may edit paper/cover-letter/rebuttal files before one of the three triggers.

---

## 5. Agent action items

### Codex
- [ ] **CX-J9** (NEW, immediate): execute J9a + J9b as a single typo patch. Report in a standard CX-J*_SUMMARY file. Do not touch prose.
- [ ] **CX-J1b**: continue to epoch 100. Log final fresh-instance sweep.
- [ ] **CX-J1c / J1d**: auto-queue on J1b completion (already authorized via Round P2).

### Kimi
- [ ] **K-Y22 update**: append the 4 deferred P1/P2 items to `KIMI_PAPER_REWRITE_CHECKLIST_20260420.md` as pre-staged edits, with exact line/section targets. No prose.
- [ ] **Stop** any pending edits to abstract / §3.4 / §4.5 / cover letter. These files are frozen.
- [ ] Phase α/β Chinese thesis work continues per Round P2.

### Gemini
- [ ] Cover-letter "simulation baseline + risk ranking" framing: draft the argument in a memo (`GEMINI_COVER_LETTER_FRAMING_MEMO_20260420.md`) for use **at loop closure**. Do not edit `cover_letter.md` now.
- [ ] Phase α theory foundations continue per Round P2.

### Claude
- [ ] **CLAUDE-DG** update: log this arbitration event as the first Rule B enforcement action.
- [ ] Monitor CX-J1b/c/d landings; trigger single-shot rewrite via `CLAUDE_DF_REWRITE_TRIGGER_20260420.md` only when the trigger condition in §4 is met.

---

## 6. Summary for user

- Review compilation is accurate; manuscript quality is submission-grade.
- Two real bugs (Fig 4c error bar, placeholder section numbers) get fixed tonight as a Codex typo patch.
- Four prose improvements are correct but queued for loop closure.
- "Submit tonight" is **not** approved; diagnostic trio must complete first.
- Expected loop closure: ~3–5 days after user authorizes J1c/J1d to proceed.
