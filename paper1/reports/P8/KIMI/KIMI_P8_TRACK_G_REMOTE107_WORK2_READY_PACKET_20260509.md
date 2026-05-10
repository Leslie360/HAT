# Kimi P8 Track G: Remote 107 Work-2 Ready Packet

Date: 2026-05-09
Scope: Remote 107 corrected-noise analog KV-cache Work-2 lane
Status: COMPLETE — Work-2 packet ready; not Paper-1

## 1. Local 107 status

| Item | Value |
|---|---|
| Review clone | `/home/qiaosir/projects/remote_reviews/107/` |
| Remote branch | `107-clean` |
| Freeze commit | `cc0a3ab` canonical freeze; `c154392` with core math packet; latest noted `a0e7f92` |
| Local P6 package | `report_md/_gpt/KIMI_P6_TRACK_F_REMOTE107_KV_CLOSURE_PACKAGE_20260509.md` |
| Local P7 gate | `report_md/_gpt/KIMI_P7_TRACK_E_REMOTE107_WORK2_GATE_20260509.md` |
| P8 remote task file | `report_md/_gpt/REMOTE_107_PHASE_P8_CORRECTED_NOISE_WORK2_TASKLIST_20260509.md` |

## 2. Corrected-noise vs old data

| Data class | Status | Route |
|---|---|---|
| Corrected-noise P0B/K107-A/B/C/EPSC/scale results | Accepted as Work-2 candidate | Work-2 only |
| Legacy v1 baseline ctx=1024/stride=512/bs=8 PPL 15.62 | Deprecated | Do not compare as current baseline |
| Canonical baseline ctx=512/stride=256/bs=1 PPL 22.1849 | Active | Work-2 canonical |
| All-layer analog KV | Catastrophic | Exclude / stress-control only |

## 3. Core corrected results

| Experiment | Result | Interpretation |
|---|---|---|
| HAT digital baseline | 19.043 PPL | HAT training improves clean PPL by ~3.1 vs 22.18 baseline |
| Patch-on no-noise | 19.060 PPL | patch overhead ~+0.02 PPL |
| last1 D2D=0.02 | 19.451 ± 0.065 | viable terminal-layer route |
| last2 D2D=0.02 | 20.142 ± 0.052 | viable but worse than last1 |
| all layers D2D=0.02 | 37.132 ± 0.878 | all-layer route abandoned |
| EPSC σ=0.15 | 20.762 ± 0.073 | stress still below PPL 25 kill criterion |
| Pythia-2.8B D2D=0.02 | 13.34 PPL | scale trend improves |

## 4. Missing / rerun matrix for P8 task file

The P8 remote task file asks for a stricter corrected-noise final return. Based on current local reports:

| Run | Current status | P8 action |
|---|---|---|
| Last1 D2D=0.02/0.04/0.05 | Available in K107-A | Return exact SHA/commands/JSON/seed metadata again |
| Last2 D2D=0.02/0.04/0.05 | Available in K107-A | Return exact SHA/commands/JSON/seed metadata again |
| Last4 | Not present in P6/P7 summary | Run if feasible or explicitly mark missing |
| All24 D2D=0.02/0.04 | All-layer available for D2D=0.02/0.04/0.05 in K107-A | Return as stress-control with metadata |
| C2C / combined last1/last2 | Some EPSC/2.8B C2C exists; exact P8 combined matrix not fully summarized locally | Return exact available data or rerun if cheap |
| No-HAT pre-eval | Not in local summary | Optional P2 ablation |
| 200/500/1000 steps | Not in local summary | Optional P2 ablation |
| ctx=512 vs 1024 | Canonical ctx=512 active; old ctx=1024 deprecated | Only rerun ctx=1024 if Work-2 needs context sensitivity |

## 5. Core math code locations to quote, not dump

| Region | Purpose |
|---|---|
| `p3_hat_train.py:67-78` | differential conductance mapping |
| `p3_hat_train.py:80-88` | quantization / STE write path |
| `analog_layers.py:170-289` | NL scaling backward path |
| `p3_hat_train.py::inject_c2c_noise` | C2C injection |
| `p3_hat_train.py::inject_d2d_noise` | D2D injection |
| `p3_hat_train.py::apply_retention_drift` | retention equation |
| `eval_llm_kv_cache.py` | sliding-window PPL scoring |

## 6. Paste-ready message for 107

```text
请在 107-clean 上执行 P8 corrected-noise Work-2 return，不要 push，不要发 checkpoint。

读取任务文件：report_md/_gpt/REMOTE_107_PHASE_P8_CORRECTED_NOISE_WORK2_TASKLIST_20260509.md

返回 REMOTE_107_PHASE_P8_CORRECTED_NOISE_REPORT_YYYYMMDD.md，必须包含：
1. exact git SHA、branch、git status --short；
2. 修复 corrected-noise bug 的 exact file/function/commit；
3. 最小 core math snippets/line ranges：quantization、C2C、D2D、retention、layer injection、sliding-window PPL；
4. 每个 result table 的 exact command、ctx/stride/bs、analog layer list、train/eval seeds、dataset split；
5. Last1/Last2/Last4/All24 corrected-noise matrix：D2D=0.02/0.04/0.05（All24 至少 0.02/0.04）；
6. C2C 和 combined robustness：Last1 C2C=0.01/0.02，Last1/Last2 D2D=0.02+C2C=0.01；
7. comparison to old bugged/deprecated data，明确 legacy ctx=1024 baseline 不再作为 canonical；
8. JSON metadata completeness table：commit、command、config、seed、checkpoint path/hash、JSON path。

分类边界：所有 107 结论只进入 Work-2，不进入 Paper-1。last1/last2 是候选主路线；all-layer 是 stress/exclude control。
```

## 7. Work-2 gates

| Gate | Current status |
|---|---|
| Selective terminal route | OPEN: last1 19.45 PPL at D2D=0.02 |
| All-layer stress route | CLOSED/Exclude: all-layer catastrophic |
| HAT effect | PASS: 22.18 → 19.04 clean digital |
| Metadata completeness | Needs P8 final return to re-assert exact JSON/commands/seed table |
| Paper-1 separation | PASS: no 107 content routed into Paper-1 |

## 8. Verdict

Track G COMPLETE. 107 is ready as Work-2 packet; missing strict P8 items are clearly listed for remote return, and no 107 claim is injected into Paper-1.
