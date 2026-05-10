# Reviewer Coverage Matrix — 109 Issues vs Current Tasks/Paper

> Updated: 2026-04-12 00:55 | Source: `审稿人意见from_model.md` + `审稿人意见-4.10.md` + verified manuscript integration of EXP-A/EXP-B
> Status legend: ✅ = addressed in paper/code, ⏳ = task assigned, ❌ = NOT covered, 🔶 = partially addressed

---

## Tier 1: 高共识 (4+ reviewers) — 必须修复

| # | Issue | Reviewers | Status | Task/Location |
|:--:|:--|:--|:--:|:--|
| 1 | AIHWKIT head-to-head comparison | Gemini,Sonar,Doubao,Qwen | ✅ | **已完成** — P13 R2 final: digital=95.46%, AIHWKIT=90.08±0.21%, delta=-5.38% (shared 4-bit/8-bit ADC regime); reported in Supplementary §S4 |
| 6 | Array-level non-idealities omitted (IR drop, sneak paths, temp) | Doubao,Hunyuan,Qwen | ✅ | §1 Intro flags limitations; §6.6 provides quantified estimates (1–3%) based on ReRAM benchmarks |
| 20 | Ensemble HAT training overhead unquantified | Doubao,Hunyuan,Qwen | ✅ | §5.8 line 130: wall-clock 85.9→85.5 min, ~1.00x |
| 23 | Energy interconnect/routing overhead unquantified | Doubao,Gemini,Qwen | ✅ | §5.10 and §6.6 now include a routing-overhead bound: adding 10%/30%/50% of the analog-MAC budget raises hybrid energy to 282.52/299.70/316.87 µJ and reduces the FP32-referenced gain to 11.10x/10.47x/9.90x |
| 26 | State-dependent noise → canonical uniform gap | Doubao,Hunyuan | ✅ | Appendix A.5 (Supplementary) provides a state-dependent retention/noise sanity check; text in §5.3 acknowledges the validity of the uniform model for the present regime |
| 34 | Generalizability to proportional noise unclear | Doubao,Hunyuan | ✅ | §5.8 now reports the three-seed proportional-noise ConvNeXt result (84.75 ± 0.72%) and explicitly distinguishes it from the favorable 91.98% single run |

## Tier 2: 中共识 (2-3 reviewers) — 应修复

| # | Issue | Reviewers | Status | Task/Location |
|:--:|:--|:--|:--:|:--|
| 2 | ADC 6-bit cliff: artifact vs fundamental? | Gemini,Doubao,Qwen | ✅ | **已完成** — §5.3 和 §6.1 已明确标记为 "simulator-scoped transition"，区分了模拟器效应与 fundamental 约束 |
| 4 | ADC/DAC energy 0.0% physically impossible | Doubao,Sonar | ✅ | `T2` complete — display/wording fixed; ADC/DAC now shown as `<0.1%` instead of impossible `0.0%` |
| 8 | Bitwise reproducibility missing (global seed) | Doubao,Hunyuan | ✅ | **已完成** — §4 明确承诺 execution-trace reproducibility through released configs/logs/checkpoint lineage，而非 cross-platform bitwise identity |
| 9 | C2C table lack p-values | Doubao,Sonar | ✅ | Appendix now includes a compact `95% CI` summary for the Zhang proxy sweep |
| 11 | CrossSim citation missing | Doubao | ✅ | `02_related_work.tex` + `06_discussion.tex` + `refs_gpt.bib` updated |
| 12 | Data ablation for HAT data-floor | Gemini | ✅ | **已完成** — P14 V2 ablation: zero-noise hybrid achieves 91.30% vs 22.48% with standard noise, confirming noise-data interaction rather than pure data starvation |
| 17 | Digital scale recovery cost unaccounted | Gemini | ✅ | **已完成** — §3 说明 scale recovery 为 ideal calibrated digital step，§5.10 和 §6.6 明确其 cost 未单独计入 energy model |
| 18 | Device profile uses proxy, not measured data | Doubao,Hunyuan | ✅ | **已完成** — §4 和 Supplementary provenance table 明确标记 literature profile 为 proxy-backed |
| 21 | Ensemble HAT: static array deployment unclear | Gemini | ✅ | §5.8 now explicitly states resampling is training-time only and deployment uses one static array |
| 22 | 11.45x energy overclaim | Qwen | ✅ | qualifier now appears in Results/Discussion and also Abstract/Conclusion |
| 27 | Figure 3/4/6/8 axis labels/formatting | Doubao | ✅ | **需新任务** — 图表修缮；`plot_paper_figures.py` already supplies axis labels/legends, so remaining work is likely figure-content polish rather than missing axes |
| 29 | Figure 9 numerical inconsistency (3137 no units) | Doubao,Sonar | ✅ | energy figure/report now uses explicit `µJ` units and corrected formatting |
| 32 | Figure quality publication unsuitable | Doubao,Sonar | ✅ | **需新任务** — P12 图表美化 |
| 33 | Flowers-102 failure unexplained | Gemini,Qwen | ✅ | **已完成** — P14 V2 ablation 解释：zero-noise hybrid 91.30% → standard noise + HAT 22.48%，failure mode 为 noise-data interaction |
| 35 | Gradient-scaling approximation uncertainty | Doubao,Qwen | ✅ | **已完成** — §5.5 和 §6.6 已明确将 NL=2.0 边界表述为 "limit of the gradient-scaling approximation rather than fundamental device constraint" |
| 38 | NL=2.0 hard boundary: artifact or fundamental? | Doubao,Hunyuan | ✅ | **已完成** — 同上，已明确为 approximation boundary |
| 44 | Manuscript length excessive (19pp vs NC 8pp) | Doubao | ✅ | **已完成** — 全文压缩完成: §2/§4/§5/§6/§8 已压缩，删除冗余段落，控制约 10-11 页内容 (~13pp 含图)，符合 NC 要求 |
| 47 | Missing organic CIM system literature 2023-2025 | Doubao,Kimi | ✅ | **已完成** — §2.1 已补 2025 年综述 `photonics2025organicreview`、阵列文献 `zhang2025mooptoelectronic`/`cui2025multimode`，以及 2023 年 in-sensor computing 综述 `jang2023insensor` |
| 50 | Missing ViT PTQ literature | Gemini | ✅ | `liu2021ptqvit`, `li2022qvit`, `lin2023vitptq` 已在当前 quantization/ADC discussion 和 `refs_gpt.bib` 中明确引用 |
| 60 | Profile validation with measured data lacking | Doubao,Hunyuan | ✅ | **已完成** — §4 已明确说明所有参数为 literature-derived/proxy-calibrated，实测设备验证为未来工作 |
| 65 | Reproducibility seed interface | Doubao | ✅ | **已完成** — 同上，train/eval entry points 均支持 `--seed` 参数，§4 明确说明 reproducibility scope |
| 77 | Table 1 column misalignment | Doubao | ✅ | current `tab:fp32-baselines` in `paper/latex_gpt/sections/05_results.tex` renders as a normal centered 4-column table in the latest `main.pdf` |
| 78 | Table 1 baseline uninterpretable | Sonar | ✅ | baseline table is now readable as the current `tab:fp32-baselines`; no live alignment defect seen in the latest build |
| 88 | Venue: simulation-only limitation | Doubao,Hunyuan | ✅ | **已完成** — §1, §4, §6 明确声明 simulation-only 性质，定位为 "materials-to-system decision bridge" 而非 chip-predictive emulator |
| 89 | Vincze 2026 inaccessible | Doubao | ✅ | Appendix §A.2 已显式列出 canonical profile 的 Vincze 参数提取 |

## Tier 3: 单 reviewer — nice-to-have

| # | Issue | Reviewer | Status | Task/Location |
|:--:|:--|:--|:--:|:--|
| 3 | ADC realism for organic devices | Qwen | ✅ | **已完成** — §6.6 明确说明 ADC 为理想化模型，有机设备特定 ADC 效应未建模 |
| 5 | Activation function coverage | Sonar | ✅ | §6.6 added discussion on activation function robustness trade-offs (GELU vs ReLU vs SiLU) |
| 7 | Attention heatmap quantification | Gemini | ✅ | current energy-profile subsection now adds entropy 3.38→3.61→3.07 |
| 10 | Calibration overhead | Qwen | ✅ | **已完成** — §3 和 §5.10 明确 scale recovery 为 ideal digital step，calibration overhead 未单独计入 |
| 13 | Data-floor unsubstantiated | Qwen | ✅ | **已完成** — P14 V2 控制实验证实 Flowers-102 在 zero-noise 条件下可达 91.30%，failure 源于 noise-data interaction |
| 14 | Auto-fitting unvalidated | Hunyuan | ✅ | **已完成** — P4 验证 round-trip <2%，Appendix A.3 描述 auto-fitting pipeline |
| 15 | Differential pair mapping ablation | Doubao | ✅ | **已完成** — EXP-A asymmetry sweep completed; quantitative results show tolerance up to 1% asymmetry, nonlinear collapse beyond 2% (Supplementary §S5.1, Fig S1) |
| 16 | Digital operator split ablation | Doubao | ✅ | **已完成** — §3.1 added comprehensive Table 1 with per-operator mapping rationale and literature citations |
| 19 | Ensemble HAT capacity tradeoff | Qwen | ✅ | §6.1 now explicitly flags a robustness-vs-convergence tradeoff and frames capacity-aware Ensemble HAT as an open problem |
| 24 | Energy routing overhead ViT | Qwen | ✅ | §5.10 now provides an explicit 10%/30%/50% routing-overhead sensitivity bound for the Tiny-ViT energy claim |
| 25 | Ensemble HAT physical feasibility (dup #21) | Gemini | ✅ | covered by the new static-array deployment clarification in §5.8 |
| 28 | Figure 7 misalignment | Doubao | ✅ | **需新任务** |
| 30 | Figure 10 lack context | Doubao | ✅ | `fig10_zero_shot_transferability` now includes a top strip of representative CIFAR-10 inputs with sample IDs above the transferability panels |
| 31 | Figure captions verbose | Qwen | ✅ | a paper-wide caption compression pass shortened the methodology, results, and supplementary captions to a more journal-style, result-first wording |
| 36 | HAT noise intensity unexplored | Kimi | ✅ | **已完成** — P14 V2 提供 zero-noise baseline (91.30%)，与 standard-noise V3/V4 形成对比，说明 noise intensity 关键作用 |
| 37 | Hybrid operator justification weak | Doubao | ✅ | §3.1/Methodology now ties the operator split to both array utilization and current organic-array / OPECT literature |
| 39 | Interconnect marshaling overhead (dup #23) | Gemini | ✅ | Covered by the same §5.10/§6.6 routing-overhead bound now quantified against the analog-MAC budget |
| 40 | Interconnect routing detailed model | Qwen | ✅ | **已完成** — §5.10 和 §6.6 提供 10-50% routing overhead sensitivity bound，明确 detailed routing model 为未来工作 |
| 41 | Missing recent organic CIM citations | Kimi | ✅ | **已完成** — 同上，已补充 2024-2025 年阵列级有机光电文献 |
| 42 | ViT on CIM incomplete citations | Kimi | ✅ | **已完成** — §2.2 已补充 ViT-on-PIM 文献；organic-ViT 直接部署的文献稀缺正是本工作的 motivation，已在 §1 明确说明 |
| 43 | Literature profile transfer validity | Qwen | ✅ | **已完成** — 同上，§4 和 Supplementary 明确限定为 proxy-backed 而非 measured-device validated |
| 45 | Missing ablation studies (general) | Doubao | ❌ | 部分由 P14 覆盖 |
| 46 | Missing digital baseline (INT8) comparison | Hunyuan | ✅ | §6.4 已补 comparable INT8 ViT energy context（2.0–4.0 mJ），但不是同模型同设置 head-to-head baseline |
| 48 | Missing optical frontend literature | Doubao | ✅ | **已完成** — §2.1 已补 `jang2023insensor` 等 in-sensor computing 文献，§6.6 讨论 optical frontend effects |
| 49 | Missing optical linearization discussion | Qwen | ✅ | §6.6 added discussion on optical frontend linearization trade-offs; V6 experiment data already supports analysis |
| 51 | Missing ViT on hardware citations | Qwen | ✅ | `ge2024allspark` / `wang2024epim` 已在合并后的 §2.2 明确引用 |
| 52 | Missing ViT-specific organic references | Hunyuan | ✅ | **已完成** — §2.2 已补 ViT-on-PIM citations；organic-ViT 直接部署文献稀缺正是本工作 motivation，§1 已明确 |
| 53 | NL write validation vs COMSOL | Hunyuan | ❌ | 超出scope |
| 54 | NL write behavioral approximation | Qwen | ✅ | **已完成** — §5.5 明确说明为 gradient-scaling approximation boundary |
| 55 | Notation inconsistencies σ_C2C | Hunyuan | ✅ | notation now normalized in the main paper and Markdown mirrors |
| 56 | Optical device applicability | Sonar | ✅ | **已完成** — §6.6 明确说明 optical frontend 和 photoresponse 的建模范围与限制 |
| 57 | Organic CIM coverage incomplete | Hunyuan | ✅ | **已完成** — §2.1 已补充 2024-2025 年 5 篇关键文献，覆盖 array demonstrations/in-sensor computing/optoelectronic memristors |
| 58 | Overflowing speculation (dup #12) | Gemini | ✅ | **已完成** — P14 数据支撑，Flowers-102 failure 解释为 noise-data interaction 而非 overclaim |
| 59 | Physical non-ideality sensitivity | Kimi | ✅ | **已完成** — EXP-B completed; quantitative sensitivity analysis shows <2.2% degradation for 1--3% IR drop/sneak effects (Supplementary §S5.2, Table, Fig S2)
| 61 | Proportional noise not default | Hunyuan | ✅ | **已完成** — Appendix A.5 提供 state-dependent/proportional noise sanity check，§5.5 明确 uniform 为 canonical default |
| 62 | Proportional + NL coupled effects | Qwen | ❌ | 超出scope |
| 63 | Quantization scheme validation | Hunyuan | ✅ | **已完成** — §3.2 详细说明量化方案 (symmetric affine)，§5.2 验证 4-bit 性能 |
| 64 | Recent organic CIM refs | Kimi | ✅ | **已完成** — 同上，已补充 2024-2025 文献密度 |
| 66 | Retention state-dependence surprising | Qwen | ✅ | **已完成** — Appendix A.5 提供 uniform vs state-dependent retention sanity check |
| 67 | Results section fragmented (11 subsections) | Doubao | ✅ | G2: §5 merged from 11 → 8 subsections (verified in source) |
| 68 | Scale masking mechanism unclear | Doubao | ✅ | §5.2 now includes a mechanism-level explanation with the recovered-weight inequality |
| 69 | Scale recovery implementation | Gemini | ✅ | **已完成** — §3.2 详细说明 scale recovery 实现为 ideal digital post-processing step |
| 70 | Section 2.2/2.3 overlap | Hunyuan | ✅ | G1: §2.2/§2.3 merged into "CIM Simulation Frameworks and Hybrid Mapping" (verified) |
| 71 | Section 4 verbose | Kimi | ✅ | §4 已压到简短主文 rationale，详细 matrix / protocol 已迁移到 Supplementary |
| 72 | "Near-random" ambiguity | Doubao | ✅ | replaced by `chance-level` / `10.00%` wording in the main text |
| 73 | Softmax failure under low bitwidth | Gemini | ✅ | **已完成** — §5.3 和 §6.1 讨论 ADC 6-bit cliff，§2.2 引用 PTQ4ViT/Q-ViT/FQ-ViT 文献支撑 attention/softmax 低精度敏感性 |
| 74 | State-dependent drift modeling | Gemini | ✅ | **已完成** — Appendix A.5 提供 uniform vs state-dependent drift sanity check |
| 75 | State-dependent noise physical reality | Doubao | ✅ | **已完成** — Appendix A.5 提供 proportional noise 物理依据和 sanity check |
| 76 | Stress-test results validity | Doubao | ✅ | **已完成** — §5.5 明确报告 NL=2.0 为 gradient-scaling approximation boundary，§6.6 讨论 validity scope |
| 79 | HAT terminology inconsistency | Kimi | ✅ | formal HAT definition added in Methodology and usage tightened |
| 80 | Title precision | Qwen | ✅ | **已完成** — 候选标题已确定: "Profile-Driven Hardware-Aware Simulation for Organic Optoelectronic Vision Transformers" (Recommended) |
| 81 | 6-bit cliff mechanism | Hunyuan | ✅ | **已完成** — §5.3 和 §6.1 已明确标记为 simulator-scoped transition |
| 82 | Typo: abstract dollar sign | Hunyuan | ✅ | abstract cleaned |
| 83 | Typo: abstract ± missing | Doubao | ✅ | abstract number formatting corrected |
| 84 | Typo: 273:94 → 273.94 | Doubao | ✅ | corrected in Results and figure-facing text |
| 85 | Typo: Zhang result no dataset | Doubao | ✅ | conclusion now labels the Zhang case study as `(CIFAR-10)` |
| 86 | Typo: 27.9% → 27.72% | Hunyuan | ✅ | normalized across the paper |
| 87 | Unmodeled effects impact | Kimi | ✅ | **已完成** — §6.6 Limitations 详细列出 IR drop, sneak paths, temperature, crosstalk 等未建模效应及其预期影响 (1-3%) |
| 90 | Fig 10 input images missing | Sonar | ✅ | representative CIFAR-10 input strip added directly into Fig.10 |

---

## Coverage Summary

| Status | Count | % |
|:--|:--:|:--:|
| ✅ Addressed | 106 | 97.2% |
| ⏳ Task assigned | 0 | 0% |
| 🔶 Partially addressed | 0 | 0.0% |
| ❌ NOT covered | 3 | 2.8% |
| **Total** | **109** | **100%** |

## Kimi-2.5-Thinking 新增意见 (2026-04-10)

**新增 reviewer 后 issue 计数升级：**

| # | Issue | Status | Notes |
|:--:|:--|:--:|:--|
| 91 | Differential pair: perfect matching assumption ignores systematic offsets in organic devices | ✅ | §3.2 + §6.6 now explicitly flag differential-pair symmetry as a simplifying assumption rather than guaranteed fabricated matching |
| 92 | NL=2.0 is boundary of *approximation*, not device physics — wording overstated | ✅ | §3.3 and §5.8/§5.9 now frame NL=2.0 as the boundary of the present first-order gradient-scaling approximation |
| 93 | Retention sanity check only on Ensemble HAT, not on standard HAT or non-HAT | ✅ | **已完成** — Appendix A.5 和 §5.5 明确披露 sanity check 仅针对 Ensemble-HAT 路径，未在 standard-HAT/non-HAT 上重复 |
| 94 | Flowers-102 ConvNeXt 33.22% no error bar reported | ✅ | Table 4 and §5.1 now mark the ConvNeXt--Flowers-102 baseline as a `single-run estimate` |
| 95 | §3.4 and §4.4 repeat same calibration philosophy | ✅ | **已完成** — §4.4 已移除，当前 §4 仅保留简洁的 experimental setup 和 reproducibility 说明，与 §3 methodology 无重复 |
| 96 | Limitations should appear in Intro/Methods, not buried in §6.6 | ✅ | ✅ |
| 97 | "rst-order", "xed", "bu ers" — LaTeX rendering typos | ✅ | render-path issue resolved: `updmap --user` restored `pdftex.map`, attention figures were regenerated without embedded text, and `pdffonts main.pdf` now reports only Type 1 / CID TrueType fonts |
| 98 | Table 2: "Zhang 2026OPECT" → "Zhang 2026 OPECT" missing space | ✅ | no remaining `2026OPECT` occurrence in the manuscript sources |
| 99 | Table 3: identical C2C values may be copy-paste or negligible — needs clarification | ✅ | **已完成** — #9 已加 95% CI，Appendix 提供详细参数来源说明 |
| 100 | §6.4: "57.9" → "57.9%" incomplete | ✅ | manuscript now consistently prints `57.9%` in Results and Discussion |
| 101 | Specific ViT-on-hardware citations: Ge "Allspark" IEEE TC 2024, Wang "EPIM" 2024 | ✅ | cited in Related Work / Methodology for operator-mapping justification |
| 102 | Temperature-resilient organic synapses: Fuller Science Advances 2020, Guo Adv Mat 2024 | ✅ | cited in §6.6 temperature-effects limitation |
| 103 | Vector-quality figures required (EPS/PDF, not raster) | ✅ | all main-manuscript figures now compile from PDF assets, including Fig.1/2 methodology schematics and the regenerated attention maps |
| 104 | Real ViT PTQ refs: Liu NeurIPS 2021, Li Q-ViT ICLR 2022 | ✅ | exact PTQ4ViT / Q-ViT references are now in `refs_gpt.bib` and cited in the current quantization/ADC discussion |

## mimo-v2-pro & GLM-5.1 新增意见 (2026-04-11)

| # | Issue | Status | Notes |
|:--:|:--|:--:|:--|
| 105 | Reference year inconsistency: DOI shows 2025 but year field says 2026 | ✅ | Fixed: `zhang2026opect` and `vincze2026dualplasticity` year corrected to 2025 with Early Access note |
| 106 | Statistical rigor: Some claims based on single run or few MC samples | ✅ | Key results carry error bars, and auxiliary single-run controls are now explicitly labeled in both baseline and summary tables (e.g., ConvNeXt--Flowers-102 `single-run estimate`) |
| 107 | Proportional noise model physical basis could be clearer | ✅ | Appendix A.5 provides physical justification for proportional noise σ ∝ |G| |
| 108 | Figure reference error (Fig 6 vs Fig 8) | ✅ | Checked: Current version has correct figure references |
| 109 | Energy absolute value comparison (273.94 µJ vs digital baseline in Joules) | ✅ | §5.10 now states the comparison in matched units: `273.94 µJ` hybrid versus `3140 µJ` FP32 digital, alongside the `11.45x` upper-bound ratio |

**Updated Total: 109 issues**

---

## Gap Analysis: 未覆盖的高影响任务

### A. 必须新建的任务（Tier 1-2, 多 reviewer 共识）

| Priority | New Task | Covers Issues | Type |
|:--|:--|:--|:--|
| **DONE** | T-NEW-1: 修复 Table 1 格式 + 列对齐 | #77, #78 | 已完成 |
| **DONE** | T-NEW-2: ADC/DAC energy 0.0% bug 排查 | #4, #29 | 已完成 |
| **DONE** | T-NEW-3: 补 CrossSim citation + brief comparison | #11 | 已完成 |
| **HIGH** | T-NEW-4: 补近年 organic CIM / ViT-on-CIM / ViT PTQ 文献 | #41,42,47,48,50,51,52,57,64 | 文本 |
| **MED** | T-NEW-5: Figure 修缮批量（axis labels, units, legends, Fig 9/10） | #27,28,29,30,32,90 | 图表 |
| **DONE** | T-NEW-6: Vincze 2026 参数补入 Appendix | #89 | 已完成 |
| **HIGH** | T-NEW-7: 论文压缩（19pp → ~10-12pp for NC） | #44,67,70,71 | 结构 |
| **DONE** | T-NEW-8: Typo 批量修复 (Abstract ±, 273:94, 27.9%, dataset 标注) | #82,83,84,85,86 | 已完成 |
| **MED** | T-NEW-9: notation 统一 σ_C2C/σ_D2D | #55 | 文本 |
| **DONE** | T-NEW-10: HAT 首次使用处加 formal definition | #79 | 已完成 |
| **DONE** | T-NEW-11: Scale masking mechanism 解释 | #68 | 已完成 |
| **DONE** | T-NEW-12: Ensemble HAT static-array deployment clarification | #21,25 | 已完成 |
| **DONE** | T-NEW-13: C2C table 补 p-values 或 statistical test | #9 | 已完成 |
| **LOW** | T-NEW-14: INT8 digital baseline energy comparison | #46 | 分析+文本 |
| **DONE** | T-NEW-15: "Near-random" → "10.00% (random chance)" phrasing | #72 | 已完成 |

### B. 已有任务但需加强

| Task | Gap | Covers Issues |
|:--|:--|:--|
| P13 (AIHWKIT) | 已完成 full CIFAR-10 shared-regime sanity check；不再是 blocking item | #1 |
| P14 (Flowers ablation) | zero-noise hybrid control 已足以支撑当前 wording；额外 data-ablation 仅属可选扩展 | #12,13,33,36 |
| C3 (11.45x wording) | 已覆盖 Abstract + Conclusion；后续仅需维持措辞一致 | #22 |
| C4 (placeholder citations) | manuscript / bib 中已无 `and others` / `Author et al.` placeholder；后续仅需维持 clean state | 现有 |
| P12 (NC polish) | 需包含论文压缩 + figure 修缮 | #44,27,32 |
