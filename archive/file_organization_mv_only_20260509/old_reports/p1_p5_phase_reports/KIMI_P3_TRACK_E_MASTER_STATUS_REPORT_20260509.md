# Kimi P3 Track E Report: Master Status and Data Map

**Date:** 2026-05-09
**Dispatch:** `DISPATCH_SUPERPHASE_P3_LONG_AUTONOMOUS_20260509.md`
**Executor:** kimi

---

## 1. Paper-1 Current State

| Item | Status | Path |
|------|--------|------|
| Main text | Frozen | `paper/latex_gpt/main.tex` |
| Supplementary | Frozen | `paper/latex_gpt/supplementary.tex` |
| Clean release bundle | **Ready** | `release_artifacts/paper1_release_candidate_20260509_clean/` |
| Pre-built PDFs | Valid | `main.pdf` (202.61 KiB), `supplementary_main.pdf` (2.71 MiB) |

**Frozen items (do not edit without Codex acceptance):**
- PCM precision ladder canonical numbers
- 6-bit narrative framing ("seed-sensitive transition zone", not "Pareto midpoint")
- All scientific numbers in tables and figures
- Figure semantics and visual design

---

## 2. Locked Canonical PCM Numbers

| Precision | Fresh Mean | Fresh Std | 1h Drift | 1d Drift | 24h Drop | Role |
|-----------|-----------|-----------|----------|----------|----------|------|
| 8-bit PCM | **77.60%** | 0.64 pp | 77.49% | 77.57% | ~0 pp | Deployment-stable practical point |
| 6-bit PCM | **68.55%** | 6.03 pp | 68.57% | 68.46% | ~0 pp | D2D-sensitive transition zone |
| 4-bit PCM | **76.68%** | 0.37 pp | 74.04% | 72.64% | -4.0 pp | Quantization-dominated, drift-costly |

**Source:** `source_data/tab_pcm_precision_ladder.csv`
**Guard:** `scripts/_gpt/check_local_pcm_precision_ladder.py` → PASS

---

## 3. Clean Bundle Location

```
release_artifacts/paper1_release_candidate_20260509_clean/
├── main.pdf
├── supplementary_main.pdf
├── cover_letter.tex
├── main.tex
├── supplementary_main.tex
├── supplementary.tex          ← recovered missing file
├── refs_gpt.bib
├── sections/                  ← 9 section files
├── supplementary/             ← 11 tex files (sections + TikZ)
├── figures/                   ← ~90 files (active + legacy orphans)
│   └── deprecated_20260424/   ← old plotrefresh figures
├── source_data/
│   ├── tab_pcm_precision_ladder.csv
│   ├── manifest_paper1_spine.json
│   └── canonical_json/
│       ├── manifest_canonical_json_20260509.json
│       └── deprecated_20260501_old_protocol/
├── MANIFEST_FILES.txt         ← 207 files
├── SHA256SUMS.txt             ← 206 checksums
└── RELEASE_README.md
```

---

## 4. Local GPU Status

| GPU | Model | Memory | Utilization | Active Jobs |
|-----|-------|--------|-------------|-------------|
| 0 | RTX 5070 Ti | 346/16303 MiB | 1% | None |

**Queue:** Empty.
**Last completed:** Work-2 KV smoke test (PASSED, 2026-05-09).

---

## 5. Remote 105 Status

| Item | Detail |
|------|--------|
| Last data | 2026-05-07 |
| New data today | None |
| Stable snapshot | `docs/data/remote_snapshots_20260507/hat_105_results` |
| Seeds completed | 123, 456 (789 crashed) |
| Classification | Supplement candidate (DeiT proportional), future-only (ViT proportional, noise-off) |

---

## 6. Remote 107 Status

| Item | Detail |
|------|--------|
| Last data | 2026-05-07 |
| New data today | None |
| Stable snapshot | `docs/data/remote_snapshots_20260507/hat_107_clean` |
| Strongest route | Selective last1, D2D=0.02, PPL=18.42 |
| Classification | **Work-2 only** — no Paper-1 contamination |

---

## 7. Frozen vs Experimental

| Category | Frozen | Still Experimental |
|----------|--------|-------------------|
| Paper-1 main text | Yes | No |
| Paper-1 supplement | Yes | No |
| PCM precision ladder | Yes | No |
| 6-bit narrative | Yes | No |
| 105 cross-architecture | No (awaiting seed789) | Yes |
| 107 KV-cache | No | Yes (Work-2) |
| 5-bit PCM | No | KILL/non-frontier (completed) |
| Figure regeneration | No | Deferred post-submission |
| Thesis compilation | No | Yes (ongoing) |

---

## 8. Data Location Index

| What | Where |
|------|-------|
| Paper-1 LaTeX source | `paper/latex_gpt/` |
| Paper-1 clean bundle | `release_artifacts/paper1_release_candidate_20260509_clean/` |
| Paper-1 source data | `paper/latex_gpt/source_data/` |
| PCM canonical JSON | `paper/latex_gpt/source_data/canonical_json/` |
| Deprecated 6-bit old protocol | `.../canonical_json/deprecated_20260501_old_protocol/` |
| 105 remote snapshot | `docs/data/remote_snapshots_20260507/hat_105_results` |
| 107 remote snapshot | `docs/data/remote_snapshots_20260507/hat_107_clean` |
| 105/107 index | `report_md/_gpt/REMOTE_105_107_DATA_ACQUISITION_INDEX_20260507.md` |
| P1 report | `report_md/_gpt/KIMI_PHASE_P1_SOURCE_DATA_CANONICALIZATION_REPORT_20260509.md` |
| P2 report | `report_md/_gpt/KIMI_PHASE_P2_RELEASE_CANDIDATE_BUNDLE_REPORT_20260509.md` |
| P3 Track A report | `report_md/_gpt/KIMI_P3_TRACK_A_P2R_CLEAN_BUNDLE_REPORT_20260509.md` |
| P3 Track B report | `report_md/_gpt/KIMI_P3_TRACK_B_CLEANROOM_REPRO_REPORT_20260509.md` |
| P3 Track C report | `report_md/_gpt/KIMI_P3_TRACK_C_REMOTE_105_107_INGESTION_REPORT_20260509.md` |
| P3 Track D report | `report_md/_gpt/KIMI_P3_TRACK_D_GPU_BACKLOG_STATUS_20260509.md` |
| P3 Track E report | `report_md/_gpt/KIMI_P3_TRACK_E_MASTER_STATUS_REPORT_20260509.md` |
| P3 Final delivery | `report_md/_gpt/KIMI_SUPERPHASE_P3_FINAL_DELIVERY_20260509.md` |
| BROADCAST log | `BROADCAST.md` |

---

## 9. Action Required

| Action | Owner | Urgency |
|--------|-------|---------|
| DS reproducibility audit on clean bundle | DS | Medium |
| Mimo reviewer-facing completeness audit | Mimo | Medium |
| Codex final acceptance | Codex | Medium |
| Fix 19 undefined citations in supplementary | Kimi/Codex | Low (cosmetic) |
| Fix ~18 unresolved cross-references in supplementary | Kimi/Codex | Low (cosmetic) |
| Remove orphan figures from release bundle (optional) | User/Codex | Low |
| Await 105 seed789 completion | Remote 105 | Unknown (server crashed) |
| Await 107 full metadata/env packet | Remote 107 | Low |

---

## 10. One-Line Summary

Paper-1 is frozen, clean bundle is valid, clean-room builds pass, GPU is idle, remote data is indexed and separated. Ready for DS/Mimo audit and Codex final acceptance.

---

*Report by kimi. Master status consolidated on 2026-05-09.*
