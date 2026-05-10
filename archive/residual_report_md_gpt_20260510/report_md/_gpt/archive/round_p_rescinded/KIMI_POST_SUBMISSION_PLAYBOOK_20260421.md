<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Post-Submission Contingency Playbook

> **Paper:** *Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision*
> **Target:** Nature Communications (NC)
> **Submitted:** 2026-04-21
> **Author / Incident Commander:** Songqiao Li
> **Playbook version:** 1.0

---

## Global Decision Tree

```
DECISION RECEIVED
│
├─► ACCEPT (no revision) ───────► SCENARIO A
│
├─► MINOR REVISION ─────────────► SCENARIO B
│   └─► Can fixes be done in ≤3 weeks?
│       ├─► YES ────────────────► Execute B.1–B.5
│       └─► NO ────────────────► Renegotiate deadline or escalate to Scenario C
│
└─► MAJOR REVISION / REJECT ────► SCENARIO C
    ├─► MAJOR REVISION ─────────► Execute C.1–C.7, resubmit to NC
    └─► REJECT ─────────────────► Execute C.1–C.7, pivot venue (C.8)
```

---

## SCENARIO A — Accept (No Revision)

**Trigger:** Editor email contains "accepted," "accept as is," or no revision request.

### A.1 Celebration Checklist (do first; 30 min)

- [ ] **Notify inner circle.** Text/call advisor + 2 closest collaborators within 1 hour. No Slack DMs to half the lab — keep the circle tight until public.
- [ ] **Log the win.** Add NC acceptance date to CV, website, and ORCID record. Screenshot the editor email; archive in `internal/milestones/`.
- [ ] **Sleep on it.** Do not touch the manuscript, arXiv source, or press kit for 12 hours. Acceptance euphoria breeds typos.

### A.2 Immediate Actions (0–24 hours)

| Action | Owner | Deliverable | ETA |
|--------|-------|-------------|-----|
| arXiv posting | Author | `arxiv_submission_2026042X.tar.gz` + announced ID | T+4h |
| Press release | Author / Lab Comms | `KIMI_PRESS_RELEASE_V2_20260421.md` → institutional PIO | T+8h |
| Code release | Author | GitHub public repo + Zenodo DOI | T+24h |

**arXiv posting — detailed:**
- Use existing `KIMI_ARXIV_CHECKLIST_20260421.md`.
- Flatten `main.tex`, inline `.bbl`, strip cover letter, append supplementary as `\appendix`.
- Tarball under 10 MB; category `cs.LG` + `cs.AR` + `eess.SP`.
- **Do not** add NC DOI yet (not assigned). Add it in v2 after publication.

**Press release — detailed:**
- Send `KIMI_PRESS_RELEASE_V2_20260421.md` to institutional public-information office.
- Emphasize: *"first profile-driven framework to quantify pathway-specific analog limits in vision transformers."*
- Embargo until arXiv announcement hits (usually 24–72 h after upload).

**Code release — detailed:**
- Execute `RELEASE_CHECKLIST.md` preflight commands (install, smoke test, unit tests, syntax compile, leak scan).
- Create public-release branch; remove `_archive/`, `logs/`, `report_md/`, `internal/`, `数据_博士/`.
- Tag `v1.0.0-nc`. Push to GitHub.
- Zenodo: upload release tarball; acquire DOI; add DOI badge to `README.md`.

### A.3 48-Hour Action Plan

**Hour 0–12:** Celebration + sleep.

**Hour 12–24:**
- [ ] arXiv uploaded and processed. Verify PDF preview has no missing figures.
- [ ] Press release sent to PIO with embargo note.
- [ ] GitHub repo switched from private → public. Verify `README.md` renders correctly.
- [ ] Social shortforms queued: `KIMI_SOCIAL_SHORTFORM_20260420.md` → schedule on X/Twitter + LinkedIn for arXiv announcement day.

**Hour 24–36:**
- [ ] Advisor signs off on press-release quote.
- [ ] Update personal website with arXiv link + 1-paragraph plain-language summary.
- [ ] Email 3–5 key collaborators (not co-authors) with personal note + arXiv link.

**Hour 36–48:**
- [ ] Monitor arXiv moderation queue. If flagged, respond immediately with scope justification (`cs.LG` + `cs.AR`).
- [ ] Post blog draft: `KIMI_BLOG_DRAFT_V2_20260421.md` → personal site or Medium.
- [ ] Prepare 5-minute "elevator" talk from `KIMI_TALK_SCRIPT_5MIN_20260420.md`.

**Deliverables:**
1. arXiv ID logged in `internal/milestones/`
2. Zenodo DOI badge live on GitHub
3. Press release published by institutional channels
4. Personal website + socials updated

---

## SCENARIO B — Minor Revision

**Trigger:** Editor email contains "minor revisions," "revise," or "accept with minor changes."
**Typical NC minor-rev horizon:** 2–4 weeks.

### B.1 Decision Tree

```
MINOR REVISION RECEIVED
│
├─► Count reviewer asks.
│   └─► ≤5 discrete items ──────► Proceed to B.2
│   └─► >5 or any feels major ──► Re-read asks; if any demand new experiments
│                                   beyond 1 GPU run, escalate to Scenario C
│
├─► Check feasibility matrix (B.3).
│   └─► All asks = text / stats / existing-data replot ──► 2-week timeline
│   └─► Any ask = 1 lightweight experiment ──────────────► 3-week timeline
│   └─► Any ask = >1 experiment or hardware request ─────► Escalate to C
│
└─► Draft response letter skeleton within 48 h (B.4).
```

### B.2 Typical Minor-Rev Requests for This Paper (Likely Items)

| # | Likely Request | Response Strategy | Experiment? |
|---|----------------|-------------------|-------------|
| 1 | **Tighten abstract to ≤150 words.** | Trim parenthetical physical-effects list; move details to body. | No |
| 2 | **Add multi-seed training robustness.** | Run seeds 42, 123, 456 for canonical Ensemble HAT (already planned). Report grand mean ± between-seed SD. | Yes — 3 GPU runs (~36 h) |
| 3 | **Clarify statistical hierarchy (SEM vs. SD).** | Add supplementary table: raw SD, hierarchical SEM, 95 % CI, Cohen's d, power. | No — existing JSON |
| 4 | **Strengthen related-work distinction from HWA-QAT.** | Add 1 paragraph in §2 citing 2–3 HWA-QAT papers; contrast quantization-aware vs. profile-driven organic stack. | No |
| 5 | **Soften "structural limit" language.** | Replace with "surrogate-bound ceiling" or "first-order ceiling" in abstract + 3 main-text instances. Add Discussion sentence that higher-order models may shift the bound. | No |
| 6 | **Batch-level vs. epoch-level Ensemble HAT ablation.** | Run 1 seed with batch-level D2D resampling; compare convergence curves. | Yes — 1 GPU run (~12 h) |
| 7 | **Figure-caption edits / resolution.** | Re-export figures at 600 dpi; ensure all error bars are visible. | No |
| 8 | **Add ORCID + suggested reviewers.** | Add `orcidlink` package; create `SUGGESTED_REVIEWERS.md` with 3 names + emails. | No |

### B.3 What to Add vs. What to Push Back On

**Add willingly (no negotiation):**
- Language hedging ("structural" → "surrogate-bound").
- Statistical supplement tables (existing JSON).
- ORCID, suggested reviewers, formatting fixes.
- Multi-seed campaign (already budgeted).

**Add conditionally (negotiate if timeline compressed):**
- Batch-level ablation — offer supplementary figure instead of main-text panel.
- Related-work paragraph — 1 paragraph max; do not rewrite §2.

**Push back on (politely, with evidence):**
- *"Add ImageNet-1K results."* → Out of scope for edge-vision claim; cite §6.6 and offer as thesis follow-up.
- *"Add silicon validation."* → Explicitly simulation-only study; framework designed for iterative calibration post-fabrication.
- *"Add SPICE deck."* → Future work; current results are upper bounds under idealized interconnect.
- *"Rewrite as two separate papers."* → Narrative coherence argument (see GEMINI_REDTEAM_V2 §Attack 6).

### B.4 Timeline: 2–4 Weeks

| Week | Milestone | Deliverable |
|------|-----------|-------------|
| Week 1, Day 1–2 | Read reviews; triage asks; draft response skeleton | `RESPONSE_LETTER_v2_DRAFT.md` |
| Week 1, Day 3–5 | Execute text/stats fixes; language tightening | Revised `.tex` sections |
| Week 1, Weekend | Run lightweight experiments (multi-seed, batch ablation) | New JSON results |
| Week 2, Day 1–3 | Integrate new results; update figures/tables | Revised `.tex` + supplementary |
| Week 2, Day 4–5 | Full recompile; proofread; advisor sign-off | `main.pdf` + `supplementary.pdf` |
| Week 2, Weekend | Final response letter; highlight every change | `RESPONSE_LETTER_v2_FINAL.md` |
| Week 3 (if needed) | Buffer for experiment overrun or figure re-rendering | — |
| Week 4 (hard stop) | Submit revision via NC portal | Confirmation email + tracking ID |

### B.5 Deliverables

1. **Response letter:** Point-by-point rebuttal. Every ask → "We thank the reviewer…" + change summary + line numbers.
2. **Revised manuscript:** Track changes or colored text for editor quick-scan.
3. **Updated supplementary:** New tables/figures appended; old labels preserved for cross-reference stability.
4. **Experiment audit:** `MINOR_REVISION_EXP_AUDIT.md` — what was run, what was not, why.

---

## SCENARIO C — Major Revision / Reject

**Trigger:** Editor email contains "major revisions," "reject but encourage resubmission," or "reject."
**Psychological state:** Expect shock. This playbook is designed to run on autopilot while emotions recalibrate.

### C.1 Emotional Resilience Checklist (Do This First — Seriously)

- [ ] **Step away from the screen.** 30-minute walk. No exceptions. Do not draft a response while cortisol is high.
- [ ] **Read the reviews twice.** First read = emotional; second read = analytical. Highlight factual asks in yellow, opinionated language in grey.
- [ ] **Call advisor.** Schedule a 30-min debrief within 24 h. Do not email collaborators the raw reviews.
- [ ] **Reframe:** Major revision is a *second chance*. Reject + encourage resubmission is a *soft reject with a roadmap*. Hard reject = the paper found the wrong venue, not that the science is worthless.
- [ ] **Sleep rule:** No decisions on experiments, venues, or rebuttal tone after 22:00.
- [ ] **Buddy system:** Text one labmate: "Got major revisions / reject. Need a sanity check on Saturday." Accountability prevents spiraling.
- [ ] **One-week blackout on social media.** Do not tweet about reviews. Do not subtweet. Do not read threads about acceptance rates.

### C.2 Typical Major-Rev Requests for This Paper (5–7 Likely Items)

| # | Likely Request | Severity | Response Strategy |
|---|----------------|----------|-------------------|
| 1 | **Hardware-in-the-loop validation.** Fabricated-array data or SPICE-calibrated netlist. | CRITICAL | Scope hedge: "simulation-first baseline designed for iterative calibration." Offer collaboration letter from foundry contact if available. |
| 2 | **ImageNet-scale or ViT-Base validation.** | MAJOR | Acknowledge scale limitation. Run Tiny-ViT on ImageNet-100 pilot (if feasible) or commit to thesis follow-up. If demanded: run ViT-Base CIFAR-10 ablation as config-only change. |
| 3 | **Higher-order surrogate (pulse-level KMC or SPICE write model).** | MAJOR | Explicitly scope as future work. Run CX-J1b/c (QKV-only / full-attention linearization) to isolate pathway without new physics. |
| 4 | **Full factorial experiment (2³ attention–MLP perturbation design).** | MAJOR | CX-J1 (joint MLP-linear + Ensemble HAT) already provides the 2³ corner. Add CX-J1b/c for remaining factorial corners if compute allows. |
| 5 | **Temperature-drift + retention combined sweep.** | MAJOR | Add JSON profile fields for temp coefficients; run retention sweep at 2–3 temperature setpoints (~48 GPU-hours). Push back if >3 setpoints requested. |
| 6 | **Novel algorithm requirement.** "If Ensemble HAT fails at severe NL, propose something that works." | CRITICAL | Reframe: contribution is *bounding* the design space, not infinite recipes. Offer second-order surrogate theory (GEMINI_STRUCTURAL_LIMIT_THEORY) as conceptual next step, not experiment. |
| 7 | **Chip demo / FPGA emulation / energy-measured baseline.** | CRITICAL | Out of scope for behavioral-simulation paper. Cite `RELEASE_CHECKLIST.md` energy-latency JSON; offer as industrial-collaboration output. |

### C.3 Feasibility Matrix: Which Experiments Are Doable

| Experiment Code | Description | Compute | Feasibility | Timeline |
|-----------------|-------------|---------|-------------|----------|
| **CX-J1b** | QKV-only linearization (NL=1.0), rest at NL=2.0 | ~15–20 GPU-h | ✅ FEASIBLE | 2–3 days |
| **CX-J1c** | Full-attention linearization (QKV+proj NL=1.0), MLP at NL=2.0 | ~15–20 GPU-h | ✅ FEASIBLE | 2–3 days |
| **CX-J1d** | Reverse configuration: MLP at NL=2.0, attention fully linear | ~15–20 GPU-h | ✅ FEASIBLE | 2–3 days |
| **Multi-seed campaign** | Seeds 42, 123, 456 for canonical + severe-NL conditions | ~36 GPU-h | ✅ FEASIBLE | 3–4 days |
| **Batch-level HAT ablation** | Batch vs. epoch D2D resampling | ~12 GPU-h | ✅ FEASIBLE | 1–2 days |
| **ViT-Base CIFAR-10** | Scale validation, config-only | ~24 GPU-h | ✅ FEASIBLE | 2–3 days |
| **ImageNet-100 pilot** | Tiny-ViT fine-tuned on 100-class subset | ~48 GPU-h | ⚠️ CONDITIONAL | 5–7 days |
| **Temp-dependent retention sweep** | 2–3 temperature setpoints | ~48 GPU-h | ⚠️ CONDITIONAL | 5–7 days |
| **Log-normal D2D stress test** | Heavy-tailed distribution injection | ~12 GPU-h | ⚠️ CONDITIONAL | 2–3 days |
| **Per-head ablation + energy** | Attention-head sensitivity | ~24 GPU-h | ❌ DIFFICULT | 1–2 weeks |
| **SPICE-calibrated array models** | Requires foundry/PDK access | N/A | ❌ INFEASIBLE | Months |
| **Pulse-level KMC write model** | Device-physics simulation | N/A | ❌ INFEASIBLE | Months |
| **Full ImageNet-1K** | 224×224, 1000 classes | ~200+ GPU-h | ❌ INFEASIBLE | 3–4 weeks |
| **Silicon tape-out / FPGA demo** | Physical fabrication | N/A | ❌ INFEASIBLE | 6–12 months |
| **LLM workload benchmark** | GPT-style autoregressive inference | ~100+ GPU-h | ❌ INFEASIBLE | 2–4 weeks |

**Rule of thumb:** If the requested experiment is not in the feasible table, the response strategy is *language + scope hedge + future-work commitment*, not execution.

### C.4 Response Strategy by Request Type

**Hardware validation asks:**
- Do not promise silicon data you do not have.
- Response template: *"We agree that hardware validation is the critical next step. The framework's JSON profile interface (§3.5) is designed so that measured array statistics can replace literature proxies without code changes. We have added a Limitations paragraph clarifying that the current ceiling is a surrogate-bound estimate pending foundry calibration."*

**Scale asks (ImageNet, ViT-Base, LLM):**
- Response template: *"We scoped the study to edge-scale vision tasks where organic CIM is most competitive on energy density. We have added a ViT-Base CIFAR-10 ablation (Supplementary Fig. SX) and a Discussion sentence predicting that deeper attention stacks would likely fall below the reported ceiling, making the current result an optimistic upper bound."*

**Novel-algorithm asks:**
- Response template: *"The reviewer's intuition that a better algorithm might break the ceiling is exactly the falsifiable prediction this paper enables. We do not claim the ceiling is immutable; we claim it is the bound under first-order surrogates. We have added §6.X outlining three candidate second-order extensions (curvature-aware STE, state-dependent retention tracking, attention-free architecture search) as direct follow-ups."*

### C.5 Timeline: 2–3 Months

| Phase | Weeks | Focus | Deliverable |
|-------|-------|-------|-------------|
| **Triage & Grieving** | W1 | Emotional resilience; advisor debrief; read reviews analytically | `REVIEW_TRIAGE_2026MMDD.md` |
| **Experiment Sprint** | W2–W4 | Execute all feasible experiments (CX-J1b/c/d, multi-seed, ViT-Base, ImageNet-100 if authorized) | New JSON + figures |
| **Manuscript Rewrite** | W5–W7 | Rewrite abstract, §1, §6; add new results; soften overclaim language; update supplementary | `main.tex` v2 + `supplementary.tex` v2 |
| **Response Letter** | W8–W9 | Point-by-point major-revision response; highlight every textual and experimental change | `RESPONSE_LETTER_MAJOR_v2.md` |
| **Advisor / Co-author Review** | W10 | Internal review cycle; figure-resolution check; reference update | Signed-off PDFs |
| **Submission** | W10–W12 | NC resubmit (if major revision) or new-venue package (if reject) | Portal confirmation |

### C.6 If NC Rejects — Resubmission Target Venue

| Priority | Venue | Fit | Rationale | Lead Time |
|----------|-------|-----|-----------|-----------|
| 1 | **Nature Electronics** | 5/5 | Fundamental limits and negative results are first-class contributions. Cross-disciplinary impact. | Fresh submission; ~8–12 % acceptance |
| 2 | **NeurIPS (Main Track)** | 4/5 | ML theory track welcomes impossibility results and scaling-limit proofs. Strong reproducibility culture. | Sept deadline; ~20–25 % acceptance |
| 3 | **ICML (Theory Track)** | 3/5 | Similar to NeurIPS but more optimization-success oriented; harder sell for negative result. | Jan deadline; ~22–27 % acceptance |
| 4 | **DATE** | 3/5 | Design-automation community tolerates methodology papers that redefine feasibility regions. | Sept deadline; ~22–26 % acceptance |
| 5 | **DAC** | 3/5 | Methodology-heavy limit studies fit EDA-relevance track. | June deadline; ~20–24 % acceptance |

**Pivot checklist:**
- [ ] Reformat to venue template (NeurIPS/DATE/DAC have strict page limits).
- [ ] Rewrite abstract to venue conventions (NeurIPS likes "We prove/show" statements).
- [ ] Check novelty window: if NC rejection took >3 months, verify no competing preprint scooped the result.
- [ ] Update cover letter to venue-specific fit argument.
- [ ] arXiv v2 with updated abstract and venue-agnostic framing (if not already posted).

### C.7 Deliverables

1. **Triage document:** Reviewer asks ranked by feasibility + emotional temperature.
2. **Experiment audit:** What was run, what was skipped, why (with compute logs).
3. **Revised manuscript v2:** Track-changes or `latexdiff` against v1.
4. **Major-response letter:** Typically 8–15 pages. Every reviewer paragraph → response paragraph.
5. **Fallback package:** Reformatted manuscript for Venue #1 (Nature Electronics) ready to submit within 1 week of NC reject.

### C.8 Emotional Resilience — Extended Protocol

**Week 1:**
- Daily 30-min physical activity (run, gym, walk). Non-negotiable.
- One social event unrelated to academia.
- Journal entry: "What is the worst-case interpretation of these reviews? What is the most generous?" Both are usually wrong; truth is in the middle.

**Week 2–4 (Experiment sprint):**
- Celebrate small wins: first training curve plotted, first JSON result logged.
- Maintain normal sleep schedule. All-nighters degrade experiment quality.
- If a rerun fails (GPU OOM, NaN loss), do not catastrophize. Treat it as a debugging task, not a personal failure.

**Week 8+ (Response-letter grind):**
- Write response letter in 45-min Pomodoro blocks. Longer sessions produce hostile prose.
- Read every response aloud before submission. If it sounds defensive, rewrite.
- Advisor red-line on tone, not just science.

**Mantra (print and tape to monitor):**
> *"A major revision is a second chance. A reject is a venue mismatch. The 30 % ceiling is still true. The code still runs. The science is still sound."*

---

## Appendix: Quick-Reference Contact Sheet

| Role | Contact | When to Ping |
|------|---------|--------------|
| Advisor | — | Within 24 h of any decision; before final response submit |
| Lab IT / GPU scheduler | — | If experiment queue exceeds 72 h during revision sprint |
| Institutional PIO | — | After arXiv announcement (Scenario A) or embargo lift |
| NC Editorial Office | — | Only for technical submission issues; never to argue reviews |
| Zenodo support | — | If DOI minting fails during code release |
| arXiv moderation | — | If submission is flagged or category-challenged |

---

## Appendix: File Manifest for All Scenarios

| File | Location | Purpose |
|------|----------|---------|
| This playbook | `report_md/_gpt/KIMI_POST_SUBMISSION_PLAYBOOK_20260421.md` | Master reference |
| arXiv checklist | `report_md/_gpt/KIMI_ARXIV_CHECKLIST_20260421.md` | Scenario A posting |
| Press release | `report_md/_gpt/KIMI_PRESS_RELEASE_V2_20260421.md` | Scenario A publicity |
| Blog draft | `report_md/_gpt/KIMI_BLOG_DRAFT_V2_20260421.md` | Scenario A outreach |
| Rebuttal master | `report_md/_gpt/KIMI_REBUTTAL_MASTER_20260421.md` | Scenarios B & C objection index |
| Rebuttal v3 anticipation | `report_md/_gpt/KIMI_REBUTTAL_V3_ANTICIPATION_20260421.md` | Scenarios B & C deep defense |
| Hostile reviews | `report_md/_gpt/GEMINI_HOSTILE_REVIEWS_20260421.md` | Scenario C rehearsal |
| Red-team v2 | `report_md/_gpt/GEMINI_REDTEAM_V2_20260421.md` | Scenario C language fixes |
| Conference fit | `report_md/_gpt/GEMINI_CONFERENCE_FIT_V2_20260421.md` | Scenario C fallback venues |
| Paper-2 design | `report_md/_gpt/GEMINI_PAPER2_EXPERIMENTAL_DESIGN_20260421.md` | Scenario C experiment specs |
| Release checklist | `RELEASE_CHECKLIST.md` | Scenario A code release |
| NC submission checklist | `report_md/_gpt/KIMI_NC_SUBMISSION_CHECKLIST_20260420.md` | Formatting compliance |

---

*Playbook compiled 2026-04-21. Revise after each decision received.*
