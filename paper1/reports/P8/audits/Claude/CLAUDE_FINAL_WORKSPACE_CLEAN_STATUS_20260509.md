# Claude Final Workspace Clean Status

Date: 2026-05-09
Policy: mv-only organization; no deletion; no commit/push.

## 1. Final verification

| Check | Result |
|---|---|
| Final submission tarball SHA | `32959fac881ad1659d2da0a4ebeba30846dac72986e032dc411ea6e916c6f4a4  paper1/release/paper1_submission_bundle_20260509_final.tar.gz` |
| Bundle manifest entries | `133 paper1/release/paper1_submission_bundle_20260509_final/MANIFEST_FILES.txt` |
| Archive root | `archive/file_organization_mv_only_20260509` |
| Files in mv-only archive | `4514` |
| Restore script | `archive/file_organization_mv_only_20260509/restore/RESTORE_COMMANDS.sh` |
| Restore lines | `498 archive/file_organization_mv_only_20260509/restore/RESTORE_COMMANDS.sh` |

## 2. Current git status classes

```text
    676  D
     91  M
     78 ??
```

Interpretation: the many `D` entries are tracked historical/build files moved into the archive. They are not deleted from disk; restore commands exist.

## 3. Remaining untracked active roots

```text
?? archive/cleanup_candidates_20260509/
?? archive/file_organization_mv_only_20260509/
?? broadcast.md
?? paper/latex_gpt/sections/08_availability.tex
?? paper/latex_gpt/source_data/canonical_json/deprecated_20260501_old_protocol/
?? paper/latex_gpt/source_data/canonical_json/manifest_canonical_json_20260509.csv
?? paper/latex_gpt/source_data/canonical_json/manifest_canonical_json_20260509.json
?? paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed456/
?? paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed457/
?? paper/latex_gpt/supplementary/figS5_proxy_sensitivity_tikz.tex
?? thesis/en/ (compat: paper/thesis/)XJTU-thesis/
?? thesis/cn/ (compat: paper/thesis_cn/)chapter_8_outlook.tex
?? thesis/cn/ (compat: paper/thesis_cn/)main.bbl
?? thesis/cn/ (compat: paper/thesis_cn/)main.pdf
?? thesis/cn/ (compat: paper/thesis_cn/)main.tex
?? paper1/provenance/paper1_provenance_archive_20260509.tar.gz
?? paper1/provenance/paper1_provenance_archive_20260509/
?? paper1/release/paper1_submission_bundle_20260509_final.tar.gz
?? paper1/release/paper1_submission_bundle_20260509_final/
?? report_md/_gpt/BROADCAST_CLAUDE_PAPER1_MAIN_APPENDIX_REVIEW_20260509.md
?? report_md/_gpt/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md
?? report_md/_gpt/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md
?? report_md/_gpt/CLAUDE_P8_SELF_AUDIT_20260509.md
?? report_md/_gpt/CODEX_APPENDIX_CONTENT_REPAIR_20260509.md
?? report_md/_gpt/CODEX_FINAL_ACCEPTANCE_PCM_FREEZE_20260509.md
?? report_md/_gpt/CODEX_PHASED_WORKFLOW_PROTOCOL_20260509.md
?? report_md/_gpt/CODEX_PHASE_P6_FINAL_ACCEPTANCE_20260509.md
?? report_md/_gpt/CODEX_PHASE_P7_FINAL_ACCEPTANCE_20260509.md
?? report_md/_gpt/CODEX_REVIEW_CLAUDE_BROADCAST_AND_GPU_STATUS_20260509.md
?? report_md/_gpt/DISPATCH_KIMI_PCM_CORRECTED_EVAL_20260509.md
?? report_md/_gpt/DISPATCH_PCM_6BIT_DRIFT_AND_APPENDIX_REPAIR_20260509.md
?? report_md/_gpt/DISPATCH_SUPERPHASE_P6_EXPERIMENT_COMPLETION_AND_EVIDENCE_GAP_CLOSURE_20260509.md
?? report_md/_gpt/DISPATCH_SUPERPHASE_P7_FINAL_FREEZE_REPO_AND_WORK2_BRIDGE_20260509.md
?? report_md/_gpt/DISPATCH_SUPERPHASE_P8_ULTRA_LONG_MANUSCRIPT_REPO_REMOTE_WORK2_20260509.md
?? report_md/_gpt/DS_IDEALDEVICE_AND_PCM_PROTOCOL_AUDIT_20260509.md
?? report_md/_gpt/DS_PCM_CORRECTED_EVAL_AUDIT_20260509.md
?? report_md/_gpt/DS_PHASE_P6_HOSTILE_EXPERIMENT_AUDIT_20260509.md
?? report_md/_gpt/DS_PHASE_P7_FINAL_FREEZE_CLEANUP_AUDIT_20260509.md
?? report_md/_gpt/KIMI_6BIT_DRIFT_CLOSURE_20260509.md
?? report_md/_gpt/KIMI_6BIT_RECONCILIATION_REPORT_20260509.md
?? report_md/_gpt/KIMI_P6_DEEP_VERIFICATION_20260509.md
?? report_md/_gpt/KIMI_P6_FINAL_DELIVERY_20260509.md
?? report_md/_gpt/KIMI_P6_SELF_AUDIT_20260509.md
?? report_md/_gpt/KIMI_P6_TRACK_A_EVIDENCE_GAP_LEDGER_20260509.md
?? report_md/_gpt/KIMI_P6_TRACK_B_LOCAL_PCM_GAP_CLOSURE_20260509.md
?? report_md/_gpt/KIMI_P6_TRACK_C_LOCAL_GPU_EXECUTION_REPORT_20260509.md
?? report_md/_gpt/KIMI_P6_TRACK_D_STATISTICAL_COMPLETION_PACK_20260509.md
?? report_md/_gpt/KIMI_P6_TRACK_E_REMOTE105_CLOSURE_PACKAGE_20260509.md
?? report_md/_gpt/KIMI_P6_TRACK_F_REMOTE107_KV_CLOSURE_PACKAGE_20260509.md
?? report_md/_gpt/KIMI_P6_TRACK_G_REPO_HYGIENE_EXECUTION_PLAN_20260509.md
?? report_md/_gpt/KIMI_P6_TRACK_H_FINAL_EXPERIMENT_COMPLETENESS_VERDICT_20260509.md
?? report_md/_gpt/KIMI_P7_SELF_AUDIT_20260509.md
?? report_md/_gpt/KIMI_P7_TRACK_A_FINAL_FREEZE_CERTIFICATE_20260509.md
?? report_md/_gpt/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md
?? report_md/_gpt/KIMI_P7_TRACK_C_CANONICAL_DATA_MAP_V2_20260509.md
?? report_md/_gpt/KIMI_P7_TRACK_D_REMOTE105_CLOSURE_GATE_20260509.md
?? report_md/_gpt/KIMI_P7_TRACK_E_REMOTE107_WORK2_GATE_20260509.md
?? report_md/_gpt/KIMI_P7_TRACK_F_LOCAL_GPU_POLICY_AND_OPTIONAL_QUEUE_20260509.md
?? report_md/_gpt/KIMI_P7_TRACK_G_APPENDIX_VISUAL_QA_HANDOFF_20260509.md
?? report_md/_gpt/KIMI_P7_TRACK_H_SUBMISSION_CHECKLIST_AND_DEFENSE_PACK_20260509.md
?? report_md/_gpt/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md
?? report_md/_gpt/KIMI_P8_SELF_AUDIT_20260509.md
?? report_md/_gpt/KIMI_P8_TRACK_A_NARRATIVE_DESLOP_REWRITE_20260509.md
?? report_md/_gpt/KIMI_P8_TRACK_B_APPENDIX_TEXT_AND_TABLE_CONSISTENCY_20260509.md
?? report_md/_gpt/KIMI_P8_TRACK_C_CLEANUP_EXECUTION_OR_DRYRUN_20260509.md
?? report_md/_gpt/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md
?? report_md/_gpt/KIMI_P8_TRACK_E_FINAL_BUNDLE_REFRESH_IF_NEEDED_20260509.md
?? report_md/_gpt/KIMI_P8_TRACK_F_REMOTE105_INGESTION_READY_PACKET_20260509.md
?? report_md/_gpt/KIMI_P8_TRACK_G_REMOTE107_WORK2_READY_PACKET_20260509.md
?? report_md/_gpt/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md
?? report_md/_gpt/KIMI_P8_TRACK_I_LOCAL_GPU_AND_WORK2_OPTIONAL_QUEUE_20260509.md
?? report_md/_gpt/KIMI_P8_TRACK_J_FINAL_USER_HANDOFF_MAP_20260509.md
?? report_md/_gpt/MIMO_APPENDIX_REVIEWER_RISK_AUDIT_20260509.md
?? report_md/_gpt/MIMO_PCM_NARRATIVE_REPAIR_20260509.md
?? report_md/_gpt/MIMO_PHASE_P6_DEFENSE_READINESS_AUDIT_20260509.md
?? report_md/_gpt/MIMO_PHASE_P7_RELEASE_READINESS_AUDIT_20260509.md
?? report_md/_gpt/REMOTE_105_PHASE_P8_FINAL_INGESTION_TASKLIST_20260509.md
?? report_md/_gpt/REMOTE_107_PHASE_P8_CORRECTED_NOISE_WORK2_TASKLIST_20260509.md
```

## 4. If you want to keep the clean organization in Git

Do not use `git add -A` blindly. Preferred conservative staging:

```bash
git add report_md/_gpt/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md report_md/_gpt/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md report_md/_gpt/AGENT_SYNC_gpt.md broadcast.md
# Then explicitly decide whether to stage archive/file_organization_mv_only_20260509/ as a committed archive.
# If committing the move itself, stage the moved-from historical paths and the archive path together after review.
git status --short
```

## 5. If you want to restore the pre-organization layout

```bash
bash archive/file_organization_mv_only_20260509/restore/RESTORE_COMMANDS.sh
```

## 6. Recommendation

For immediate Paper-1 submission, ignore git cleanliness and use the final tarball. For GitHub, first decide whether the archive should be committed or kept local; otherwise stage only Paper-1 active files plus P6/P7/P8 reports.
