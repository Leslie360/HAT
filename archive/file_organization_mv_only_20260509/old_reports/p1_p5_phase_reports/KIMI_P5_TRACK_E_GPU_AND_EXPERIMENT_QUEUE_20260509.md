# Kimi P5 Track E Report: GPU and Experiment Governance Queue

**Date:** 2026-05-09
**Dispatch:** `DISPATCH_SUPERPHASE_P5_POST_AUDIT_REMOTE_AND_EXPERIMENT_GOVERNANCE_20260509.md`
**Executor:** kimi

---

## 1. Current GPU Status

| GPU | Model | Memory Used | Memory Total | Utilization | Active Jobs |
|-----|-------|-------------|--------------|-------------|-------------|
| 0 | NVIDIA GeForce RTX 5070 Ti | 346 MiB | 16303 MiB | 1% | None |

**Status:** Idle and available.

---

## 2. Candidate Tasks

### Paper-1 Verification (Ready)

| Task | Command | Duration | Status |
|------|---------|----------|--------|
| PCM precision ladder guard | `python scripts/_gpt/check_local_pcm_precision_ladder.py` | < 10s | Ready |

### Work-2 KV-Cache Exploratory (Ready)

| Task | Command | Duration | Status |
|------|---------|----------|--------|
| AnalogKVCache unit test | `python -m pytest tests/test_w2_analog_kv_cache.py` | < 5s | Ready (pytest needed) |
| KV-cache smoke test (manual) | `python -c "from paper2.src.analog_kv_cache import ..."` | < 5s | **Already passed today** |

### 105/107 Result Ingestion (Blocked — Remote)

| Task | Status | Blocker |
|------|--------|---------|
| 105 seed789 completion | Remote-only | Server crashed |
| 107 corrected-noise rerun | Remote-only | Waiting for server |

### Thesis-Only Experiments (Ready)

| Task | Command | Duration | Status |
|------|---------|----------|--------|
| Nonideality sweep | `python scripts/experiment_nonideality_sweep.py` | Hours | Needs config review |
| Proportional HAT fresh eval | `bash scripts/run_proportional_hat_fresh_eval.sh` | Hours | Needs config review |

---

## 3. Prioritized Queue

| Priority | Task | Command Readiness | Est. Duration | Kill Criterion |
|----------|------|-------------------|---------------|----------------|
| P1 | PCM guard sanity | Ready | 10s | Any assertion failure |
| P2 | KV-cache unit test | Ready (no pytest env) | 5s | Any assertion failure |
| P3 | Nonideality sweep | Needs config review | 2-4h | No improvement after 50 epochs |
| P4 | Proportional HAT eval | Needs config review | 1-2h | Divergence or NaN |
| P5 | 105/107 ingestion | Remote-only | N/A | N/A |

---

## 4. Safety Constraints

- **No Paper-1-changing training** without Codex approval.
- **No long GPU jobs** (> 30 min) without explicit user or Codex approval.
- **GPU memory must stay below 90%** to avoid remote freeze risk.
- **Sequential > parallel** unless capacity explicitly approved.

---

## 5. Verdict

GPU is idle. One low-risk Work-2 smoke test already passed today. No immediate local GPU work is required; queue is ready for when user or Codex requests experiments.

---

*Report by kimi. GPU queue assessed on 2026-05-09.*
