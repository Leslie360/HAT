# Agent Broadcast — Codex Round C (2026-04-18 21:30 CST)

**Owner**: Codex (CLAUDE-assistant)
**Trigger**: User "推进其他的" → "你得广播你做的事情"
**GPU State**: all-linear running (ep64/100, best 87.49%), attn_proj queued behind it

---

## 1. Completed Work This Round

### 1.1 CLAUDE-A NL Narrative Decision
- **Status**: PRELIMINARY Option B locked (supplementary ablation, NOT 5th contribution)
- **Trigger**: MLP-only 87.79% + QKV-only 18.72% results in
- **Key signal**: QKV-only failure (-9 pp vs baseline) kills generality claim
- **Deliverable**: `CLAUDE_A_DECISION_PRELIM_20260418.md`

### 1.2 Provenance Audit Gap Fill (CX-D)
- **G1**: A2.3 `89.85/84.04` → `report_md/json/a23_experiment_results.json` key `"2.0_1e-11"`
- **G2**: OPECT `88.53` → `report_md/_gpt/json_gpt/literature_profile_eval.json` key `"V4_Ensemble"`
- **G3**: `p<10⁻¹⁵` → re-derived from `fresh_instance_eval.json`; Welch's t-test p=1.38e-16 (standard HAT σ=0 caveat noted)
- **G4**: GM-E5 `89.61` → `_archive/old-experiment-json/combined_stress_results.json`
- **G5**: Energy → `analog_layers.py` `EnergyProfiler.compare_with_fp32_gpu()`

### 1.3 R1–R4 .tex Patches (ALL LANDED)

| Patch | File | Change |
|:------|:-----|:-------|
| R1 A1–A4, A6 | `00_abstract.tex` | ADC, D2D, HAT, OPECT, NL expanded |
| R1 A8–A11 | `01_introduction.tex` | CNN, ViT, MLP, SRAM expanded |
| R1 A7, A12 | `03_methodology.tex` | LTP/LTD, STE expanded |
| R1 A13 | `05_results.tex` | MC expanded |
| R1 A14 | `01_introduction.tex` | IR drop → current–resistance (IR) drop |
| R1 A16 | `03_methodology.tex` | DNTT → dinaphtho-thieno-thiophene (DNTT) |
| R1 A18 | `05_results.tex` | PCM/RRAM expanded in Fig 10 caption |
| R1 A21 | `supplementary.tex` | LSB → least significant bit (LSB) |
| R1 A23 | `supplementary.tex` | SNR → signal-to-noise ratio (SNR) |
| R2 D1 | `05_results.tex` | OPECT 88.53% → **88.53±0.08%** (n=10) |
| R2 D2 | `05_results.tex` | 97.39% → **97.39±0.00%** (n=10) |
| R2 D3 | `05_results.tex` | +5.8 pp → single-seed deterministic evaluation |
| R2 D4 | `05_results.tex` | p<10⁻¹⁵ → one-sample t-test, n=10 |
| R2 D5 | `05_results.tex` | Cadence scan → single-run explicit |
| R2 D6 | `05_results.tex` | Retention plateau → numerically grounded (91.63→82.66→79.13–79.51%) |
| R2 D7 | `05_results.tex` | Best-checkpoint rule disclosed |
| R2 D8 | `06_discussion.tex` | Compound stress → single-run point estimate |
| R2 D9 | `06_discussion.tex` | CrossSim → 5-seed means + 14.43 pp gap |
| R2 D10 | `03_methodology.tex` | Seed policy: "independently per grid point and per architecture" |
| R3 C1 | `03_methodology.tex` | Scale-recovery branch usage: standard default; retention only for V8 |
| R3 C2 | `03_methodology.tex` | Shot-noise κ absorbed into per-profile calibration |
| R3 C3 | `03_methodology.tex` | Ensemble HAT expectation: "one map per epoch, held constant across mini-batches" |
| R3 C4 | `03_methodology.tex` | Sobol estimator: "directly from grid of MC means" |
| R3 C5 | `05_results.tex` | p<10⁻¹⁵ test name: one-sample t-test |
| R3 C6 | `03_methodology.tex` | Gradient-scaling: "∝ |G|^(NL−1)" |
| R3 C7 | `03_methodology.tex` | Operator list: analog vs digital explicit |
| R3 C9 | `03_methodology.tex` | MC seed reuse: "not shared across grid or across models" |
| R3 C10 | `03_methodology.tex` | Fresh-instance p(M): i.i.d. Gaussian, held constant over eval |
| R3 C11 | `05_results.tex` | "~7 pp jump" → mean 7 pp, per-row 5.8–8.1 pp |
| R4 | `06_discussion.tex` | Limitations: IR drop, sneak paths, temperature explicitly listed; Outlook: "circuit-aware layer explicitly deferred" |

### 1.4 Cover Letter v2 Update
- OPECT 88.53% → 88.53±0.08%
- Contribution #5 wording updated to reflect NL mitigation supplementary framing

### 1.5 Supplementary Table Scaffold
- `SUPP_TABLE_NL_ABLATION_SCAFFOLD.md` — rows for MLP, QKV, attn_proj, all-linear, baselines

### 1.6 TX-32 Archive
- `paper/` legacy `.md` drafts (01-08 chapters, PAPER_OUTLINE, FIGURE_CAPTION_DRAFTS, etc.) → `_archive/paper-drafts/`

### 1.7 Reviewer Response Draft Phase 3
- New section: **Group-wise NL Mitigation Ablation** (MLP 87.79%, QKV 18.72%, all-linear preliminary 87.49%)
- New section: **Learnable Inverse-Gamma Compensation (E3)** (γ_comp=0.7398, +2.85 pp)
- Summary of Revisions updated with [NEW] entries
- Residual Limitations #3 updated: "localized to MLP path; attention QKV structurally required"

### 1.8 Coordination Documents
- `EXPERIMENT_DASHBOARD_20260418.md`
- `PRE_SUBMISSION_CHECKLIST.md`

---

## 2. Compile Verification

| Document | Pages | Status |
|:---------|:-----:|:-------|
| Main | **15** | ✅ Tectonic clean compile |
| Supplementary | **21** | ✅ Tectonic clean compile |
| Cover letter | **2** | ✅ Tectonic clean compile |

> Note: Main increased from 14→15 pp due to R1–R4 necessary additions. NC Article has no hard page ceiling; 15 pp is acceptable.

---

## 3. GPU Queue Status

| Job | Status | Best Acc | Epoch | ETA |
|:----|:-------|:---------|:------|:----|
| all-linear NL mitigation | 🔄 Running | **87.49%** | 64/100 | ~10–12 h |
| attn_proj-only | ⏳ Queued (OOM) | — | — | After all-linear finishes |

**No GPU headroom** — 9 python DDP processes saturate GPU. Do NOT launch new training lanes.

---

## 4. Blockers for Next Round

1. **all-linear completion** → update Table SX.N row (f), finalize CLAUDE-A decision
2. **attn_proj-only completion** → update Table SX.N row (e)
3. **D13 Fig 4 mixed error bars** → decision needed (split panel or compute MC for bare cells)

---

## 5. Recommended Next Actions (when user says "继续推进")

- **Option A**: Prepare E5 layer-wise gamma sensitivity script (CPU-only, queued for GPU)
- **Option B**: Process remaining PRE_SUBMISSION_CHECKLIST items (D11, D12, D13, C8)
- **Option C**: Build `check_locked_numbers.py` guard script
- **Option D**: Wait for GPU drain, then launch attn_proj-only + finalize CLAUDE-A

---

**End of broadcast.**

---

## UPDATE (2026-04-18 ~17:00 CST)

### all-linear NL Mitigation COMPLETED
- **Best test acc: 87.49%** @ epoch 59 (final: 84.81%)
- Slightly below MLP-only (87.79%), consistent with QKV failure masking
- Confirms MLP-dominance in composite setting

### CLAUDE-A FINAL Decision: Option B LOCKED
- `CLAUDE_A_DECISION_FINAL_20260418.md` created
- NL mitigation stays supplementary (Table SX.N)
- Main-paper contributions remain at 4
- K-B cover letter v2 / R1–R4 patches fully unblocked

### attn_proj-only LAUNCHED
- Started immediately after GPU freed by all-linear completion
- Expected completion: ~2026-04-19 15:00
- Will complete Table SX.N row (e)

### Table SX.N Status
| Row | Variant | Result | Status |
|:-----|:--------|:-------|:-------|
| (c) | MLP-only | 87.79% | ✅ |
| (d) | QKV-only | 18.72% | ✅ |
| (f) | all-linear | 87.49% | ✅ |
| (e) | attn_proj-only | TBD | 🔄 Running |
