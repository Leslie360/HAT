# Kimi P8 Track J: Final User Handoff Map

Date: 2026-05-09
Status: COMPLETE

## 1. Submission package

| Artifact | Path | Status |
|---|---|---|
| Final bundle dir | `paper1/release/paper1_submission_bundle_20260509_final/` | SHA verified, 133/133 OK after self-audit repair |
| Final tarball | `paper1/release/paper1_submission_bundle_20260509_final.tar.gz` | SHA256 `32959fac881ad1659d2da0a4ebeba30846dac72986e032dc411ea6e916c6f4a4`, size 9.9M |
| Main manuscript PDF | `paper/latex_gpt/main.pdf` | 260K |
| Supplement PDF | `paper/latex_gpt/supplementary_main.pdf` | 2.7M |
| Cover letter PDF | `paper/latex_gpt/cover_letter.pdf` | 64K |
| Final bundle verification log | `logs/p8_self_audit_bundle_repair_20260509_224103.log` | PASS |
| PCM guard log | `logs/p8_pcm_guard_20260509_223000.log` | PASS |

## 2. If user wants to submit

Upload these files from `paper1/release/paper1_submission_bundle_20260509_final/`:

1. `main.pdf`
2. `supplementary_main.pdf`
3. `cover_letter.pdf`
4. Any required LaTeX source archive from the same bundle if the portal requests source files.

If the portal allows one archive, upload:

`paper1/release/paper1_submission_bundle_20260509_final.tar.gz`

## 3. If user wants to push GitHub

Do not broad-stage. Use Track D:

`report_md/_gpt/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md`

Recommended branch:

`paper1-final-freeze-p8-20260509`

Before pushing, Codex/user should approve whether to commit the final tarball and whether thesis edits belong in this branch.

## 4. If user wants to clean files

Cleanup already executed conservatively.

Quarantine root:

`archive/cleanup_candidates_20260509/`

Restore examples:

```bash
mv archive/cleanup_candidates_20260509/old_remote_files/* .
mv archive/cleanup_candidates_20260509/old_drafts/deprecated paper/latex_gpt/
mv archive/cleanup_candidates_20260509/old_drafts/deprecated_20260424 paper/latex_gpt/figures/
mv archive/cleanup_candidates_20260509/test_renderings/* paper/latex_gpt/
mv archive/cleanup_candidates_20260509/chatgpt_images/* paper/latex_gpt/
```

User-decision item still retained:

`report_md/记忆类型可调的光电突触和存储器用于储备池计算-第8稿(1).pptx`

## 5. If user wants to ask 105

Paste this to 105:

```text
请在 105 上执行 P8 final ingestion return，不要 push，不要发 checkpoint。

读取任务文件：report_md/_gpt/REMOTE_105_PHASE_P8_FINAL_INGESTION_TASKLIST_20260509.md

返回一个 Markdown 报告 + compact CSV/JSON summary，必须包含：exact git SHA、git status --short、Python/PyTorch/CUDA/timm/GPU/dataset path、每个 final run 的 exact train/fresh-eval command、DeiT/ViT × digital/proportional × seed123/456/789 的 source test_acc/fresh mean/std/checkpoint path/JSON/log path、fresh protocol=10 fresh instances × 5 MC、D2D/C2C seed 语义，并明确 source 是 best-epoch test_acc 不是 train_acc。

分类边界：DeiT proportional 只能 supplement/defense candidate；ViT proportional 只能 defense-support；105 不是 Paper-1 submission blocker，不得改 Paper-1 locked values。
```

## 6. If user wants to ask 107

Paste this to 107:

```text
请在 107-clean 上执行 P8 corrected-noise Work-2 return，不要 push，不要发 checkpoint。

读取任务文件：report_md/_gpt/REMOTE_107_PHASE_P8_CORRECTED_NOISE_WORK2_TASKLIST_20260509.md

返回 REMOTE_107_PHASE_P8_CORRECTED_NOISE_REPORT_YYYYMMDD.md，必须包含 exact git SHA/branch/status、corrected-noise bug 修复 file/function/commit、core math line ranges、每个结果的 exact command、ctx/stride/bs、analog layers、train/eval seeds、dataset split、Last1/Last2/Last4/All24 corrected-noise matrix、C2C/combined robustness、old bugged/deprecated data comparison、JSON metadata completeness。

分类边界：所有 107 结论只进入 Work-2，不进入 Paper-1。last1/last2 是候选主路线；all-layer 是 stress/exclude control。
```

## 7. If user wants Gemini to continue figures

Gemini should stay in visual/user-directed lane only:

- inspect appendix figure aesthetics;
- legend density, panel spacing, font consistency;
- page balance in `supplementary_main.pdf`;
- no source CSV/JSON edits;
- no numerical/caption claim changes without Codex acceptance.

## 8. If user wants Codex final check

Ask Codex:

```text
请做 P8 final acceptance：检查 KIMI_P8_TRACK_A-J 和 KIMI_P8_SELF_AUDIT，确认 narrative edits 未改数值/claim，bundle SHA/cold-unpack 通过，cleanup 未动 protected paths，git scope 保守，105/107 scope 分离，thesis map 标签诚实，Paper-1 GPU 未重开。
```

## 9. P8 deliverables

- `KIMI_P8_TRACK_A_NARRATIVE_DESLOP_REWRITE_20260509.md`
- `KIMI_P8_TRACK_B_APPENDIX_TEXT_AND_TABLE_CONSISTENCY_20260509.md`
- `KIMI_P8_TRACK_C_CLEANUP_EXECUTION_OR_DRYRUN_20260509.md`
- `KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md`
- `KIMI_P8_TRACK_E_FINAL_BUNDLE_REFRESH_IF_NEEDED_20260509.md`
- `KIMI_P8_TRACK_F_REMOTE105_INGESTION_READY_PACKET_20260509.md`
- `KIMI_P8_TRACK_G_REMOTE107_WORK2_READY_PACKET_20260509.md`
- `KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md`
- `KIMI_P8_TRACK_I_LOCAL_GPU_AND_WORK2_OPTIONAL_QUEUE_20260509.md`
- `KIMI_P8_TRACK_J_FINAL_USER_HANDOFF_MAP_20260509.md`
- `KIMI_P8_SELF_AUDIT_20260509.md`

## 10. Verdict

Track J COMPLETE. User can submit, push after approval, restore quarantined files, or dispatch 105/107 without asking where artifacts are.
