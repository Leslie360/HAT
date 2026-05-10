# 📊 Post-fix Rerun Campaign — Status Dashboard (CORRECTED)

**Last updated:** 2026-04-24 09:55 CST
**Correction:** Proportional HAT 90.88% retracted (NL=1.0 train / NL=2.0 eval mismatch).

---

## ⚠️ Critical Erratum

| Claim | Status | Reason |
|-------|--------|--------|
| Proportional HAT 90.88% fresh eval | ❌ **RETRACTED** | Trained at NL=1.0, eval forced NL=2.0. Not a legitimate NL=2.0 result. |

**Verified:** `checkpoints/_gpt/postfix_proportional/V4_hybrid_standard_noise_hat_best.pt` has `exp_cfg.nl_ltp=1.0`, `exp_cfg.nl_ltd=-1.0`.

---

## ✅ Legitimate Results (NL=2.0 train & eval)

| # | Experiment | Same-Inst | Fresh-Eval | Std | Noise Mode | Status |
|---|------------|-----------|------------|-----|------------|--------|
| 1 | Ensemble HAT (V4) | 81.72% | **81.69%** | 0.64% | uniform | ✅ Verified |
| 2 | Standard HAT (V3) | 83.27% | **82.63%** | 0.56% | uniform | ✅ Verified |
| 3 | Proportional HAT (V4) | N/A | **INVALID** | N/A | proportional | ❌ NL mismatch |
| 4 | V1 Digital Baseline | 91.00% | N/A | N/A | none | ✅ Done |

---

## 🔑 Key Findings (Post-Retraction)

1. **Bug fix alone recovers ~52 pp**: Pre-fix ~30% → Post-fix ~82% under NL=2.0
2. **"Structural ceiling" was a software artifact**: The ~30% limit was caused by STE branch swap + extraneous nl multiplier
3. **Proportional noise story is UNVERIFIED**: True NL=2.0 proportional HAT requires CX-M3 replication
4. **Single-run results need replication**: M-series (CX-M1/M2/M3/M4) ordered per BROADCAST_HALT_AND_REPLICATE_20260424.md

---

## 📁 Artifacts

### Fresh Eval JSONs (Legitimate only)
- `report_md/_gpt/json_gpt/postfix_ensemble_hat_v4_nl20_fresh_eval.json` ✅
- `report_md/_gpt/json_gpt/V3_hybrid_standard_noise_standard_train_best_fresh_eval.json` ✅
- ~~`report_md/_gpt/json_gpt/V4_hybrid_standard_noise_hat_best_fresh_eval.json`~~ ❌ NL mismatch — do not cite

### Cross-Reviews
- `KIMI_FULL_REPORT_20260424.md` ✅ Erratum added (K-RETRACT complete)
- `CODEX_CROSS_REVIEW_RERUN_20260423.md` ✅ (code audit)
- `CODEX_CROSS_REVIEW_FRESH_EVAL_20260423.md` ✅ (Ensemble HAT eval)

### Broadcasts
- `BROADCAST_HALT_AND_REPLICATE_20260424.md` 🛑 Active — supersedes all prior
- `BROADCAST_PROPORTIONAL_HAT_HISTORIC_20260424.md` ❌ RETRACTED

---

## 🚀 Next Steps (Non-Kimi)

### Codex-controlled
- [ ] **CX-M1** — Standard HAT NL=2.0 seed B replication
- [ ] **CX-M2** — Ensemble HAT NL=2.0 seed B replication
- [ ] **CX-M3** — Proportional HAT NL=2.0 from scratch (true test)
- [ ] **CX-M4** — Proportional HAT NL=2.0 seed B (if M3 lands)

### Claude-controlled
- [x] **EJ-1** — Revert 5 paper-1 edits + move signature figure

---

## ✅ Kimi Task Completion

| Task | ID | Status |
|------|-----|--------|
| K-RETRACT — Erratum in `KIMI_FULL_REPORT_20260424.md` | K-RETRACT | ✅ DONE |
| Broadcast retraction — `BROADCAST_PROPORTIONAL_HAT_HISTORIC_20260424.md` | — | ✅ DONE |
| Dashboard correction — `STATUS_DASHBOARD_20260424.md` | — | ✅ DONE |
| README correction — `TOMORNING_README.md` | — | ✅ DONE |
