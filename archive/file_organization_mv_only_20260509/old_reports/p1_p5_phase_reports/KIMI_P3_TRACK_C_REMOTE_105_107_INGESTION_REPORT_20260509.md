# Kimi P3 Track C Report: Remote 105/107 Ingestion

**Date:** 2026-05-09
**Dispatch:** `DISPATCH_SUPERPHASE_P3_LONG_AUTONOMOUS_20260509.md`
**Executor:** kimi
**Verdict:** NO NEW REMOTE DATA — EXISTING DATA CLASSIFIED AND INDEXED

---

## 1. Remote Data Status

No new remote deliverables received since the 2026-05-07 acquisition snapshot.

| Server | Last Data | New Data Today | Status |
|--------|-----------|----------------|--------|
| Remote 105 | 2026-05-07 | None | Indexed, classified as future-only/supplement |
| Remote 107 | 2026-05-07 | None | Indexed, classified as Work-2 only |

---

## 2. Remote 105 Classification

**Acquired data:** TinyImageNet-200 cross-architecture validation (deit_small, vit_small) × 4 HAT modes × 2 seeds.

| Result Slice | Classification | Reason |
|-------------|----------------|--------|
| DeiT proportional vs digital (both seeds beat digital) | **Paper-1 supplement candidate** | Strong validation of proportional HAT generalization beyond local TinyViT |
| ViT proportional vs digital (mixed: seed123 -0.03pp, seed456 -0.16pp) | **Future-only** | Not consistently above digital; needs seed789 or more seeds |
| Ensemble HAT fresh collapse (~-3 to -4.8pp) | **Paper-1 supplement** | Confirms main-text ensemble pathology on alternate architectures |
| Standard HAT catastrophic collapse (~-30 to -34pp) | **Paper-1 supplement** | Confirms main-text standard HAT pathology |
| Noise-off ablation (54.52% vs fresh 54.19% vs digital 53.61%) | **Future-only / thesis** | Interesting but single-seed, single-architecture; not main-claim ready |

**Kill criteria applied:**
- Seed 789 missing due to server crash → flagged as incomplete 3-seed table
- Same-architecture comparisons controlled → valid
- No cross-architecture proportional-beat-digital claims made (only per-architecture)

---

## 3. Remote 107 Classification

**Acquired data:** Analog KV-cache v2 results, selective terminal-layer, Pythia-410m.

| Result Slice | Classification | Reason |
|-------------|----------------|--------|
| Selective last1 D2D=0.02 PPL=18.42 (baseline 15.68, +2.74 PPL) | **Work-2 only** | KV-cache is separate from Paper-1 PCM vision focus |
| Selective last1 D2D=0.04 PPL=18.55 | **Work-2 only** | Companion evidence, not Paper-1 claim |
| Selective last1 D2D=0.05 PPL=18.60 | **Work-2 only** | Companion evidence, not Paper-1 claim |
| All-layer results (worse than selective) | **Work-2 control data** | Stress test, not deployment claim |
| v2 noise-algorithm bug fix | **Work-2 provenance** | Documents corrected methodology |

**Work-2 notes:**
- Last1 selective terminal-layer is the strongest KV route in acquired data.
- All-layer results preserved as stress/control data.
- JSON metadata incomplete in places; use branch commit + README + generated tables as provenance.
- No Paper-1 main or supplement contamination.

---

## 4. Data Index Maintenance

Existing index is current:
`report_md/_gpt/REMOTE_105_107_DATA_ACQUISITION_INDEX_20260507.md`

Stable snapshot paths:
- 105: `/home/qiaosir/projects/docs/data/remote_snapshots_20260507/hat_105_results`
- 107: `/home/qiaosir/projects/docs/data/remote_snapshots_20260507/hat_107_clean`

No index updates required today.

---

## 5. Cross-Contamination Check

| Check | Result |
|-------|--------|
| Paper-1 LaTeX references 105/107? | No (verified via grep) |
| Paper-1 source data contains 105/107 values? | No |
| 105/107 data in release bundle? | No |
| PCM canonical numbers affected by remote? | No |

**No cross-contamination.**

---

## 6. Verdict

Track C complete. No new remote data to ingest. Existing data classified and separated. Ready for Codex review if remote servers return new deliverables.

---

*Report by kimi. Ingestion status checked on 2026-05-09.*
