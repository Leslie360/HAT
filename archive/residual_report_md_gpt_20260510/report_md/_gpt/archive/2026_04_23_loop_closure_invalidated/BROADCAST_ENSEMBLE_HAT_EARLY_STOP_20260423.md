# Broadcast: Ensemble HAT Post-Fix Early Stop + Fresh Eval Launch

**Date:** 2026-04-23 23:36 CST
**Authority:** User (qiaosir) — methodology paper, no need to chase SOTA numbers
**Executed by:** Kimi Code CLI

---

## Decision: Early Stop Ensemble HAT

**Rationale:** Methodology paper. Patience=10 principle agreed with user. Ensemble HAT reached best same-instance accuracy at epoch 10 (81.72%) and showed zero improvement for 30 subsequent epochs (test_acc oscillated 79-81%). Continuing wastes GPU time.

**Final same-instance stats (post-fix, clean code):**
- Best checkpoint: `checkpoints/_gpt/postfix_reruns/V4_hybrid_standard_noise_hat_best.pt`
- Best epoch: 10
- Best test_acc: **81.72%**
- Training config: NL_LTP=2.0, NL_LTD=-2.0, epoch-resampled D2D, AMP on
- Total epochs trained: 40 (early stopped)
- Git HEAD: 33bed9c

---

## Immediate Action: Fresh-Instance Eval Launched

Command:
```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python eval_fresh_instances_postfix.py \
  --checkpoint checkpoints/_gpt/postfix_reruns/V4_hybrid_standard_noise_hat_best.pt \
  --exp-id V4 --model-type tinyvit \
  --num-instances 10 --mc-runs 5 \
  --nl-ltp 2.0 --nl-ltd -2.0 --noise-mode uniform \
  --output report_md/_gpt/json_gpt/postfix_ensemble_hat_v4_nl20_fresh_eval.json
```

Protocol:
- 10 fresh D2D instances, seed convention 42 + 100*i
- 5 Monte Carlo eval runs per instance (C2C resampled per forward)
- Evaluator NL override: 2.0 / -2.0 (verified by Kimi+Codex cross-review)
- Evaluator pushes NL into model.config (CRITICAL FIX applied)

---

## Current Parallel Experiments

| Experiment | Status | Best Same-Instance | Notes |
|:---|:---|:---|:---|
| Ensemble HAT NL=2.0 | ✅ **STOPPED** (epoch 40) | **81.72%** | Fresh eval in progress |
| Standard HAT NL=2.0 | 🔄 **RUNNING** (epoch ~2-3) | 61.68% (epoch 0) | Monitoring for patience=10 |

---

## Next Steps After Fresh Eval Completes

1. Codex cross-review of fresh eval results
2. Compare post-fix Ensemble HAT fresh transfer vs pre-fix invalid 86.37%
3. Compare vs R1 standard HAT (NL=1.0, 34.56% fresh)
4. Decide next rerun priority based on numbers

---

*Cross-review and final fresh-instance numbers to follow.*
