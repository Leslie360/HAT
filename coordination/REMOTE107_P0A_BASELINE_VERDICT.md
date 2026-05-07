# P0-A Baseline Reconciliation Verdict

**Date:** 2026-05-08
**Branch:** `107-clean`

---

## 1. Evaluators Tested

### A1. Current K107 evaluator

- **Script:** `p3_hat_train.evaluate_ppl` / `p3_hat_eval.py`
- **Parameters:** `ctx_len=512`, `stride=256`, `batch_size=1`
- **Result:** PPL = **22.1849**
- **Command:**
  ```bash
  /home/lisq753/miniconda3/envs/LLM/bin/python baseline_eval_digital.py
  ```
- **JSON:** `deliverable/results_v3/baseline_digital_current.json`

### A2. Old/vectorized evaluator

- **Script:** `p3_e2e_eval.py` / `eval_llm_analog.py` style
- **Parameters:** `max_length=1024`, `stride=512`, `batch_size=8`
- **Result:** PPL = **15.6175**
- **Command:**
  ```bash
  /home/lisq753/miniconda3/envs/LLM/bin/python baseline_eval_old.py
  ```
- **JSON:** `deliverable/results_v3/baseline_digital_old.json`

---

## 2. Root Cause

The **15.68** figure cited in older notes (`RESULTS_SUMMARY.md`) was produced by the old evaluator with:
- 2× longer context window (1024 vs 512)
- 2× larger stride (512 vs 256)
- 8× larger batch size (8 vs 1)

Longer context and larger batch reduce perplexity because the model sees more tokens for each prediction. This is a well-known evaluator artifact, not a model difference.

---

## 3. Verdict

**The canonical digital baseline for K107 comparisons is 22.18 PPL.**

All K107-A/B/C/P0-B/P1 results must be compared against **22.18**, not 15.68.

Reasoning:
1. **Consistency:** Every K107 train/eval run uses `p3_hat_train.evaluate_ppl` with `ctx_len=512, stride=256, batch_size=1`.
2. **Fairness:** Analog overhead must be measured against the same evaluator configuration as the digital baseline. Mixing evaluators would conflate setup differences with analog noise effects.
3. **Reproducibility:** The 15.68 evaluator path (`p3_e2e_eval.py`) is deprecated and not used for K107 canonical runs.

---

## 4. Recommended Action

- Update `RESULTS_SUMMARY.md` to note that 15.68 was from the old `max_length=1024` evaluator and is **not** comparable to K107 results.
- For manuscript, report both numbers with explicit evaluator parameters, or standardize on the 512/256/1 setup.

---

## 5. Files

- `deliverable/results_v3/baseline_digital_current.json`
- `deliverable/results_v3/baseline_digital_old.json`
