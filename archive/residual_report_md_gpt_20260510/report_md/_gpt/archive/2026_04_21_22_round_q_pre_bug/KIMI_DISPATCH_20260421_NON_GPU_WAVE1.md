<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Kimi Dispatch — Non-GPU Wave 1 (2026-04-21)

Objective:
- Use the live GPU window to finish missing non-GPU deliverables that are explicitly allowed under Rule B.
- Do not edit frozen paper text.

Hard constraints:
- No edits to:
  - `paper/00_abstract.md`
  - `paper/05_results.md`
  - `paper/06_discussion.md`
  - `paper/cover_letter*.md`
  - `KIMI_REBUTTAL_MASTER_20260420.md`
  - `paper/thesis/chapter_5_*.tex`
- Thesis outputs stay in Simplified Chinese.
- Packaging / community / paper-2 support docs stay in English unless the filename clearly implies Chinese.

Please deliver these files:

1. `report_md/_gpt/KIMI_CREDIT_V3_20260420.md`
- Author contribution matrix.
- Must be language-neutral and ready to fold into submission metadata later.

2. `report_md/_gpt/KIMI_ARXIV_CHECKLIST_V2_20260420.md`
- Process checklist only.
- Cover: source-data, code snapshot, PDF sanity, ancillary files, reproducibility notes.

3. `report_md/_gpt/KIMI_CONFERENCE_TEMPLATES_20260420.md`
- Compare NeurIPS-W / MLSys / ICML-W / DATE style packaging needs.
- Keep it operational, not rhetorical.

4. `report_md/_gpt/KIMI_POST_SUBMISSION_PLAYBOOK_20260420.md`
- Time-ordered post-submission actions.
- Include: monitoring, rebuttal prep, artifact release, and metadata freeze points.

5. `paper/thesis_cn/chapter_8_outlook.tex`
- Chinese thesis outlook chapter.
- Must be forward-looking only.
- No dependence on unresolved `J1d` numbers.
- Safe themes:
  - higher-fidelity surrogates
  - physical-realism extensions
  - mixed-signal partitioning
  - broader task families
  - measured-array closure

6. `report_md/_gpt/KIMI_DEFENSE_SLIDES_CN_20260420.md`
- 50–60 slide outline.
- Chinese.
- Should reflect the current negative-result / falsification framing without rewriting the paper.

7. `report_md/_gpt/KIMI_DEFENSE_QA_CN_20260420.md`
- 40-question defense bank.
- Chinese.
- Prioritize hostile questions on:
  - simulation-only scope
  - why no submission during live loop
  - why MLP succeeds and attention collapses
  - how to interpret negative mitigation results

8. `report_md/_gpt/KIMI_PAPER2_GAP_ANALYSIS_20260420.md`
- Compare current `paper/paper2/skeleton_v0/` against what is still missing for a viable theory-first paper-2 draft.
- Must be number-agnostic.

9. `report_md/_gpt/KIMI_ROUND_Q_ADVANCE_BRIEF_20260420.md`
- One-page brief for Friday synthesis.
- Structure:
  - if `J1d < 35%`
  - if `35–50%`
  - if `>50%`
- Only planning guidance. No prose rewrites.

Quality bar:
- Concrete, line-item useful, and integration-ready.
- No invented experiment results.
- No silent edits to frozen files.

Logging:
- Append one compact block to `AGENT_SYNC_gpt.md` after this wave lands.
