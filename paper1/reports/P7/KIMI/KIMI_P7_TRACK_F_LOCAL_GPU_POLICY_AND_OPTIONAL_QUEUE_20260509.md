# Kimi P7 Track F: Local GPU Policy and Optional Queue

**Date:** 2026-05-09
**Scope:** Local GPU usage rules post-P6 freeze

---

## 1. Principle

**Paper-1 does not need more local GPU training.** All numerical claims are frozen. No training run may mutate frozen claims without explicit Codex acceptance.

---

## 2. Allowed GPU Work

| Category | Allowed Activity | Condition | Output Path |
|----------|-----------------|-----------|-------------|
| Reproducibility smoke eval | Run `check_local_pcm_precision_ladder.py` | Must be read-only on canonical data | Terminal / temp log |
| Guard validation | Run stale-value scans on bundle | Must not overwrite source data | Terminal / temp log |
| Work-2 dry run | Run 107 `eval_llm_kv_cache.py` smoke test | Must be isolated from Paper-1 paths | `work2_sandbox/` |
| Figure regeneration | Re-run `plot_paper1_spine.py` | Only if user explicitly requests visual fix | `paper/figures/` |

---

## 3. Disallowed GPU Work

| Category | Disallowed Activity | Reason |
|----------|--------------------|--------|
| Paper-1 retraining | Any new training of PCM/HAT models | Frozen claims become unstable |
| Silent canonical overwrite | Any eval that writes to `paper/latex_gpt/source_data/canonical_json/` without Codex approval | Breaks submission traceability |
| Open-ended experiments | "Let's try X and see" runs | Not useful for paper defense |
| Multi-job parallel training | Multiple training jobs simultaneously | Risk of GPU freeze; violates sequential rule |
| Large-context LLM eval | ctx > 512 on local 16GB card | OOM risk |

---

## 4. Required Pre-Run Checklist

Before ANY GPU job:

| Step | Command | Pass Criteria |
|------|---------|---------------|
| 1. GPU memory check | `nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader` | Used < 90% of total |
| 2. Single job check | `nvidia-smi` process list | Only 1 Python process |
| 3. GPU temperature | `nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits` | < 80°C |
| 4. Output path isolation | Verify `--save-dir` or `--output` | Not in `paper/latex_gpt/source_data/` unless Codex-approved |
| 5. Command logging | `tee logs/_gpt/$(date +%Y%m%d_%H%M%S)_gpu_run.log` | All output logged |

---

## 5. Optional Queue (If User Requests)

| Priority | Job | Condition | ETA | Risk |
|----------|-----|-----------|-----|------|
| P1 | PCM guard re-run | If canonical data changes | 5 min | None |
| P2 | 107 smoke eval | If Work-2 planning needs verification | 10 min | Low (isolated) |
| P3 | Thesis figure regeneration | If user requests visual update | 30 min | Low (no claims) |
| — | Any new training | **Never unless Codex reopens** | — | High |

---

## 6. Emergency Stop Criteria

Stop immediately if:

| Condition | Action |
|-----------|--------|
| GPU memory > 90% | Kill process, check for leaks |
| GPU temp > 85°C | Pause, cool down |
| nvidia-smi shows >1 Python job | Kill all but intended job |
| Script writes to canonical JSON unexpectedly | Ctrl-C immediately, verify integrity |
| Loss diverges or accuracy drops >10pp | Stop, report to Codex |

---

## 7. Verdict

| Check | Result |
|-------|--------|
| Allowed work defined | ✅ 4 categories |
| Disallowed work defined | ✅ 5 categories |
| Pre-run checklist | ✅ 5 steps |
| Optional queue | ✅ 3 items + emergency stops |
| No open-ended Paper-1 mutation | ✅ Explicitly forbidden |

**Track F Status: COMPLETE**

---

*Report by kimi. 2026-05-09.*
