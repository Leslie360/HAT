# Kimi P8 Track E: Final Bundle Refresh If Needed

Date: 2026-05-09
Scope: final Paper-1 submission bundle
Status: COMPLETE — refreshed and verified

## 1. Trigger

Track A/B changed LaTeX text in manuscript/SI, so the final submission bundle was refreshed.

## 2. Rebuilds

| Artifact | Status | Evidence |
|---|---|---|
| `paper/latex_gpt/main.pdf` | Up to date | `logs/p8_latex_rebuild_after_final_text_20260509_222917.log` |
| `paper/latex_gpt/supplementary_main.pdf` | Rebuilt | 39 pages, 2,826,721 bytes |
| `paper/latex_gpt/cover_letter.pdf` | Up to date | same log |

## 3. Bundle refresh actions

| Step | Result |
|---|---|
| Resynced changed PDFs and source files | PASS |
| Refreshed `MANIFEST_FILES.txt` | PASS |
| Refreshed `SHA256SUMS.txt` | PASS |
| Recreated tarball | PASS |
| Cold unpacked tarball | PASS |
| Ran `sha256sum -c SHA256SUMS.txt` in cold unpack | PASS, 133/133 OK after self-audit repair |
| Self-audit bundle stray removal | PASS: removed `sections/06_discussion.tex.bak_20260425` from final bundle and moved it to quarantine |

## 4. Final paths

| Artifact | Path | Size / hash |
|---|---|---|
| Final bundle directory | `paper1/release/paper1_submission_bundle_20260509_final/` | 133 SHA-verified entries |
| Final tarball | `paper1/release/paper1_submission_bundle_20260509_final.tar.gz` | 9.9M |
| Tarball SHA256 | same path | `32959fac881ad1659d2da0a4ebeba30846dac72986e032dc411ea6e916c6f4a4` |
| Main PDF | `paper/latex_gpt/main.pdf` | 260K |
| Supplement PDF | `paper/latex_gpt/supplementary_main.pdf` | 2.7M |
| Cover letter PDF | `paper/latex_gpt/cover_letter.pdf` | 64K |

## 5. Verification logs

- Final bundle SHA/cold-unpack log: `logs/p8_trackE_final_bundle_refresh_20260509_223000.log`
- Self-audit bundle repair log: `logs/p8_self_audit_bundle_repair_20260509_224103.log`
- Final LaTeX rebuild log: `logs/p8_latex_rebuild_after_final_text_20260509_222917.log`
- PCM guard log: `logs/p8_pcm_guard_20260509_223000.log`

## 6. Stale scans

Final active-source scan excluding explicitly deprecated old-protocol archive returned no hits for:

- `68.55`
- `0.07 pp` / `0.07~pp`
- stale 6-bit `\notrun{}` context
- stale `86.37 ± 0.19` aggregate pattern

## 7. Verdict

Track E COMPLETE. Final bundle has been refreshed, tarred, cold-unpacked, and SHA-verified.
