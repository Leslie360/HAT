# Kimi P8 Track F: Remote 105 Ingestion Ready Packet

Date: 2026-05-09
Scope: Remote 105 TinyImageNet multi-dataset validation lane
Status: COMPLETE — ready packet prepared; not a Paper-1 blocker

## 1. Task file status

Remote task file exists and is clear:

`report_md/_gpt/REMOTE_105_PHASE_P8_FINAL_INGESTION_TASKLIST_20260509.md`

It requires git SHA, git status, environment, exact commands, seed table, fresh protocol, source definition, JSON/log paths, and failure logs.

## 2. Current local 105 state

| Item | Status |
|---|---|
| Review clone | `/home/qiaosir/projects/remote_reviews/105/` |
| P6 closure package | `report_md/_gpt/KIMI_P6_TRACK_E_REMOTE105_CLOSURE_PACKAGE_20260509.md` |
| P7 closure gate | `report_md/_gpt/KIMI_P7_TRACK_D_REMOTE105_CLOSURE_GATE_20260509.md` |
| Branch/commit from P6 | `105-remote-results`, freeze commit `ccf1cf7` |
| Paper-1 blocker? | No |

## 3. Accepted data classification

| Dataset/arch | Data | Classification | Paper-1 route |
|---|---|---|---|
| TinyImageNet, DeiT-Small | Digital vs proportional, seeds 123/456/789 | `paper1-supplement-candidate` | Supplement/defense only, not main claim |
| TinyImageNet, ViT-Small | Digital vs proportional, seeds 123/456/789 with seed456 outlier | `defense-support` | Reviewer response/defense only |
| Standard HAT collapse on TinyImageNet | strong collapse evidence | `paper1-supplement-candidate` | Supplement if needed |
| Any new 105 reruns beyond this packet | provisional until metadata passes | Not accepted until audited |

## 4. Locked summary from P6/P7

| Arch | Digital fresh mean | Proportional fresh mean | Advantage | Verdict |
|---|---:|---:|---:|---|
| DeiT-Small | 51.80% | 53.61% | +1.77 to +1.81 pp depending rounding table | Supplement candidate |
| ViT-Small | 51.42% | 52.69% | +1.27 to +1.35 pp depending rounding table | Defense-support; seed456 outlier documented |

The rounding difference between P6 and P7 tables is reporting precision, not a scientific conflict. Do not update Paper-1 locked main-text values from 105.

## 5. Paste-ready message for 105

```text
请在 105 上执行 P8 final ingestion return，不要 push，不要发 checkpoint。

读取任务文件：report_md/_gpt/REMOTE_105_PHASE_P8_FINAL_INGESTION_TASKLIST_20260509.md

返回一个 Markdown 报告 + compact CSV/JSON summary，必须包含：
1. exact git SHA 和 git status --short；
2. Python/PyTorch/CUDA/timm/GPU/dataset path；
3. 每个 final run 的 train/fresh-eval exact command；
4. DeiT/ViT × digital/proportional × seed123/456/789 的 source test_acc、fresh mean/std、checkpoint path、JSON/log path；
5. fresh protocol：10 fresh instances × 5 MC，D2D/C2C seed 语义；
6. 明确 source 是 best-epoch test_acc，不是 train_acc；
7. server crash 或缺失 run 必须单独列出，不要平均进结果。

分类边界：DeiT proportional 只能作为 Paper-1 supplement/defense candidate；ViT proportional 只能 defense-support；105 不是 Paper-1 submission blocker，不得改 Paper-1 locked values。
```

## 6. Acceptance gate

Accept into supplement/defense only if:

- same-architecture digital baseline exists;
- 3 seeds complete for supplement-level claim;
- source/test/train definitions unambiguous;
- exact commands and git SHA included;
- JSON/log paths exist;
- no checkpoint upload required;
- no Paper-1 main-value mutation requested.

## 7. Verdict

Track F COMPLETE. 105 packet is ready to send, and current 105 evidence remains supplement/defense only.
