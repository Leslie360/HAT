import os

sync_file = 'compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md'
task_file = 'compute_vit/report_md/_gpt/CLAUDE_TASK_gpt.md'

status_block = """
## [Gemini] 2026-04-23 11:40 — Final Second-Order Coefficient Ruling
### Topic
- Correctness of the nl*(nl-1) coefficient in the second-order Taylor correction.

### Status
- **RULING:** Current code is **INCORRECT**.
- **DERIVATION:** The ratified Branch A surrogate is S(u) = u^(NL-1). Its derivative with respect to conductance is S'(u) = (NL-1) * u^(NL-2) * (du/dg). 
- **ERROR:** The code implementation 'nl * (nl-1)' incorrectly includes an extraneous NL multiplier. This artificially doubles the second-order correction strength at NL=2.0.
- **CONSEQUENCE:** Current K4R is **INVALID**. The over-correction masks the true physical properties of the bimodal landscape.

### Evidence
- `report_md/_gpt/GEMINI_SECOND_ORDER_COEFFICIENT_RULING_20260423.md`

### Next
- Codex: Fix `analog_layers.py` (remove 'nl_ltp *' and 'nl_ltd *' from the _corr lines).
- Codex: Stop and restart K4R (now v3).
"""

for fpath in [sync_file, task_file]:
    with open(fpath, 'a', encoding='utf-8') as f:
        f.write(status_block)
print("Sync block added.")
