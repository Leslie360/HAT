import os

base_dir = "compute_vit/report_md/_gpt"
files_to_deprecate = [
    "GEMINI_PAPER2_CROSSWALK_20260421.md",
    "GEMINI_PAPER2_LOCKED_NUMBER_SCRUB_20260421.md",
    "GEMINI_PAPER2_ROUTE_FINAL_20260425.md",
    "GEMINI_CONFERENCE_FIT_V3_20260501.md"
]

for fname in files_to_deprecate:
    path = os.path.join(base_dir, fname)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        
        header = f"> **⚠️ SUPERSEDED (2026-04-23):** This memo was written under the Round Q assumption that Paper-2 would be a continuation of the ViT Bimodal Basin theory (Route R-A). Claude's `CLAUDE_WORK2_DIRECTION_LOCK_20260423.md` has since explicitly re-routed Paper-2 to **LLM KV-Cache Mapping (Direction C)**. This document is retained for archival purposes but its conclusions are officially VOID. See G-HH21 through G-HH25 for the correct Paper-2 theory.\n\n"
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(header + content)

sync_file = os.path.join(base_dir, "AGENT_SYNC_gpt.md")
task_file = os.path.join(base_dir, "CLAUDE_TASK_gpt.md")

sync_msg = """
## [Gemini] 2026-04-23 15:30 — Work 2 Reconciliation (Self-Correction)
### Topic
- Resolving contradictions between Round Q (Paper 2 = Bimodal Basin) and Claude's Work 2 Lock (Paper 2 = LLM KV-Cache).

### Status
- **OMISSION CAUGHT:** I previously generated G-HH21~25 for the new KV-Cache direction without explicitly deprecating my older G-HH memos that mapped Paper-2 to the ViT structural limit/bimodal basin theory.
- **ACTION TAKEN:** I have applied `SUPERSEDED` headers to:
  - `G-HH2 (GEMINI_PAPER2_CROSSWALK_20260421.md)`
  - `G-HH6 (GEMINI_PAPER2_LOCKED_NUMBER_SCRUB_20260421.md)`
  - `G-HH10 (GEMINI_PAPER2_ROUTE_FINAL_20260425.md)`
  - `G-HH18 (GEMINI_CONFERENCE_FIT_V3_20260501.md)`
- **CLARIFICATION:** Work 1 (Thesis Ch.3-5 / Paper 1 NC) is strictly the ViT Bimodal Basin. Work 2 (Thesis Ch.6-7 / Paper 2 MICRO/ASPLOS) is strictly the LLM KV-Cache mapping. The theoretical separation is now watertight.

### Evidence
- Superseded headers applied to the 4 affected files in `report_md/_gpt/`.
"""

for fpath in [sync_file, task_file]:
    if os.path.exists(fpath):
        with open(fpath, "a", encoding="utf-8") as f:
            f.write(sync_msg)

print("Gemini Work 2 reconciliation complete.")
