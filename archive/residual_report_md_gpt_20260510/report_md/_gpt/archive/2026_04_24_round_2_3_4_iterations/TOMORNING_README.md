# 🌅 Post-fix Rerun — CORRECTED Status (2026-04-24)

## ⚠️ CRITICAL ERRATUM

**Proportional HAT 90.88% is RETRACTED.**

The checkpoint was trained at NL=1.0, not NL=2.0. Eval forced NL=2.0 override.
This is a train/eval NL mismatch — **not a legitimate post-fix NL=2.0 result.**

Verified: `ckpt['exp_cfg'].nl_ltp = 1.0`, `ckpt['exp_cfg'].nl_ltd = -1.0`

## ✅ Legitimate Results Only

| Experiment | Fresh-Eval | Notes |
|------------|------------|-------|
| Ensemble HAT (V4) | 81.69 ± 0.64% | NL=2.0 train, NL=2.0 eval ✅ |
| Standard HAT (V3) | 82.63 ± 0.56% | NL=2.0 train, NL=2.0 eval ✅ |
| Proportional HAT (V4) | **INVALID** | NL=1.0 train, NL=2.0 eval ❌ |

## What This Means

- The "structural ceiling ~30%" was a **software artifact** (bug in STE)
- Post-fix NL=2.0 reaches ~82% fresh eval — a +52 pp recovery
- Proportional noise needs **CX-M3 replication** (true NL=2.0 from scratch)
- Do NOT cite 90.88% in any manuscript or presentation

## Files

- `BROADCAST_HALT_AND_REPLICATE_20260424.md` — Active broadcast
- `KIMI_FULL_REPORT_20260424.md` — Erratum added
- `STATUS_DASHBOARD_20260424.md` — Corrected
