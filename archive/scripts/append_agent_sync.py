import os

base_dir = "compute_vit/report_md/_gpt"
sync_file = os.path.join(base_dir, "AGENT_SYNC_gpt.md")

blocks = """
## [Gemini] 2026-04-22 (G-DR1 Scrub)
### Topic
- Round-Q memo consistency scrub completed.
### Status
- Deprecated stale Branch-A and ceiling-broken files.
- `CODEX_CX_K2_SUMMARY.md` (38.95%) established as core bimodal evidence.
### Evidence
- `report_md/_gpt/GEMINI_ROUND_Q_MEMO_CONSISTENCY_20260422.md`

## [Gemini] 2026-04-22 (G-DR2 Thesis Map)
### Topic
- Thesis CN dependency map for post-K3 landing created.
### Status
- Mapped 11 target sections across Ch.1 to Ch.8 and abstract.
- Blocked items identified with strictly "yes/no" dependency on `K3-0p25`.
### Evidence
- `report_md/_gpt/GEMINI_THESIS_CN_POST_K3_DEPENDENCY_20260422.md`

## [Gemini] 2026-04-22 (G-DR3 Skeleton Audit)
### Topic
- Paper-2 skeleton_v1 placeholder audit triggered stop condition.
### Status
- **STOP CONDITION TRIGGERED.** `paper/paper2/skeleton_v1/` directory does not exist yet.
- Audit halted to strictly prevent hallucination per Drudge Wave rules.
### Evidence
- `report_md/_gpt/GEMINI_PAPER2_SKELETON_V1_PLACEHOLDER_AUDIT_20260422.md`

## [Gemini] 2026-04-22 (G-DR4 Fig Crosswalk)
### Topic
- Figure/source-data crosswalk v2 completed.
### Status
- Mapped 9 figure intents to their authoritative JSON/CSV sources.
- Checked Zenodo-readiness; Fig 7/8 flagged as not ready (provisional/pending).
### Evidence
- `report_md/_gpt/GEMINI_FIGURE_SOURCE_CROSSWALK_V2_20260422.md`

## [Gemini] 2026-04-22 (G-DR5 Objection Bank)
### Topic
- Reviewer objection bank for ambiguous-branch generated.
### Status
- 12 concise objections mapped with 'danger' and 'response' paths.
- Explicitly maintained `[K3-0p25 pending]` for missing evidence items.
### Evidence
- `report_md/_gpt/GEMINI_AMBIGUOUS_BRANCH_OBJECTION_BANK_20260422.md`

## [Gemini] 2026-04-22 (G-DR6 Attack Surface)
### Topic
- Defense attack surface v2 updated.
### Status
- 15 hostile questions generated specifically for the K2/K3 weak-drift context.
- Short/long answers provided with exact `[yes/no]` dependency on `K3-0p25`.
### Evidence
- `report_md/_gpt/GEMINI_DEFENSE_ATTACK_SURFACE_V2_20260422.md`

## [Gemini] 2026-04-22 (G-DR7 Backlog Map)
### Topic
- Submission/release housekeeping backlog map completed.
### Status
- Categorized exactly into: can do now, blocked on user metadata, blocked on K3 final, optional.
- Excluded user-owned metadata tasks from the map to follow constraints.
### Evidence
- `report_md/_gpt/GEMINI_RELEASE_BACKLOG_MAP_20260422.md`

## [Gemini] 2026-04-22 (G-DR8 Decision Aid)
### Topic
- One-page branch decision aid generated.
### Status
- 3 scenarios mapped (lifts above, matches, worse than K2) for K3-0.25 landing.
- Provided scientific interpretation and paper-2 route changes for each scenario.
### Evidence
- `report_md/_gpt/GEMINI_BRANCH_DECISION_AID_20260422.md`
"""

try:
    with open(sync_file, "a", encoding="utf-8") as f:
        f.write(blocks)
except Exception as e:
    print(f"Error appending to sync file: {e}")

print("Added per-task 5-line blocks to AGENT_SYNC_gpt.md.")
