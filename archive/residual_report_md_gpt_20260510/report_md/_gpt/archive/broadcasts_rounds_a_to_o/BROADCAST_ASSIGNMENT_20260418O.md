> Canonical coordination: `AGENT_SYNC_gpt.md` | Task ledger: `CLAUDE_TASK_gpt.md`
> **Multi-day program.** This broadcast is explicitly designed to run Kimi/Gemini for ~3 days of parallel work without needing a new dispatch. Tasks are organized into **three phases** with explicit triggers; agents may re-order within a phase and pivot to next-phase tasks once their phase-α queue is empty.

# Round O Broadcast — 2026-04-19 11:45 (multi-day program; thesis completion + artifact generation + defense prep)

**Author:** Claude (Chief Architect)
**Trigger:** Round N closed: Kimi delivered thesis ch.2/3/4 (~98 KB actual LaTeX prose) + rebuttal arsenal v2 (15 extra objections) + literature landscape + repo hygiene. Codex closed CX-GA (warm-start resume fixed; 1-epoch CUDA smoke PASS @ 81.71%). Round-N Gemini deliverables didn't land to disk — Kimi will absorb that scope in Round O.
**Quota:** Kimi ✅ **deep saturation** (~18 tasks) · Gemini 🟡 **medium-heavy** (~12 tasks) · Codex 🔴 **minimal** (CX-GB gated + 1 optional smoke).
**Round O theme:** Thesis completion (Chapters 5–8) + community-artifact generation (tutorial notebook, blog draft, talk script, defense slides outline) + paper-2 scoping + final NC rebuttal preparedness. This is intentionally the largest single broadcast so far; agents can chew on it for days.

---

## Long-horizon reminder

```
Round N: thesis ch.2–4 drafted + rebuttal v2 + repo hygiene        [DONE]
Round O: thesis ch.5–8 + artifacts + paper-2 scoping + defense     [THIS BROADCAST — multi-day]
Round P: 2nd-paper prototype + Zenodo/GitHub release + press kit   [forward]
```

---

## PHASE STRUCTURE

Tasks are grouped into **three phases** so the work can unfold naturally over multiple days:

- **Phase α (Day 1)** — Thesis completion + rebuttal master consolidation + Round-N Gemini backfill
- **Phase β (Day 2)** — Community artifacts (tutorial / blog / talk / slides) + paper-2 deep scoping
- **Phase γ (Day 3)** — Defense materials + final QA + pre-flight for Round P

**Rules for agents:**
1. Start with Phase-α tasks in your track; complete as many as possible before moving on.
2. When your phase-α queue is empty, self-promote to phase-β tasks in the same track.
3. When phase-β is empty, proceed to phase-γ.
4. Tasks within a phase are **independent** — you may re-order by your own judgment.
5. Do **not** wait on cross-agent handoffs within the same phase unless explicitly gated (marked ⛓️).
6. If a task is blocked or over-scoped, drop a 2-line note in `AGENT_SYNC_gpt.md` and move to the next.

---

## State on disk (pinned at t0)

- NC bundle ready; only user metadata gates `CX-GB`.
- Thesis chapters 1–4 exist (ch.1 skeleton, ch.2–4 ~30 KB each actual prose).
- Rebuttal arsenal v1 (10 objections) + v2 (15 objections, 3 files).
- Codex warm-start fix validated on CUDA.
- Round-N Gemini files (G-CC1–CC7) **not on disk** — Kimi absorbs G-CC4/CC5/CC6/CC7 this round; G-CC1/CC2/CC3 specs become their Gemini re-try.

---

## KIMI — Round O (deep saturation; ~18 tasks across 3 phases)

### 🟦 PHASE α (Day 1) — Thesis completion core + Round-N Gemini backfill

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **K-V1** | **Thesis Chapter 5: Mitigation case studies** | `paper/thesis/chapter_5_mitigation.tex` (~25 pp) | Anchor case studies: (a) Ensemble HAT as the 10%→86% lift; (b) MLP-linear as the severe-NL diagnostic (source 87%, fresh-instance 32% honest cap); (c) all-linear upper-bound as the ceiling-is-not-the-roof result; (d) per-batch vs per-epoch HAT (86.16% vs 86.37%); (e) ensemble-frequency plateau. Each case study: problem → intervention → outcome → residual open question. |
| **K-V2** | **Thesis Chapter 6: Physical-realism extensions** | `paper/thesis/chapter_6_physical_realism.tex` (~25 pp) | What the NC paper deferred but thesis can re-open: (a) correlated-D2D full result (already harvested in CX-CA); (b) heavy-tailed conductance extension (using the stub script + G-CC1-style theory); (c) IR-drop preliminary modeling (G-CC-style outline); (d) temperature drift (G-CC-style outline); (e) retention beyond 79% (G-CC-style outline). For each: what we did / what we only spec'd / what remains open. |
| **K-V3** | **Thesis Chapter 7: Deployment envelope** | `paper/thesis/chapter_7_deployment.tex` (~20 pp) | The "so what" chapter. Convert all our data into a deployment envelope: (a) which combinations of D2D σ × NL × ADC bits × retention time × temperature preserve the Ensemble HAT ranking; (b) which combinations collapse it; (c) decision diagram for "should this architecture ship on organic RRAM?"; (d) implications for CNN vs ViT choice at different device maturity tiers. Reuse NC Fig 4/5 data; do not duplicate. |
| **K-V4** | **Thesis Chapter 8: Outlook + conclusion** | `paper/thesis/chapter_8_outlook.tex` (~15 pp) | Outlook: (a) joint MLP-linear + Ensemble HAT (post-CX-FA cold-start, pre-warm-start run); (b) ImageNet-100 pilot (G-AA2 spec); (c) language-model CIM direction; (d) hardware-in-the-loop roadmap. Conclusion: integrative paragraphs that land the thesis as one story, not 8 disjoint chapters. |
| **K-V5** | **Gemini-backfill: HAT-as-implicit-regularizer theory note** (was G-CC4) | `KIMI_HAT_AS_REGULARIZER_NOTE_20260420.md` (≤800 words) | Math framing: fixed-mask training minimizes a single empirical risk L(θ; D̂), while Ensemble HAT minimizes expected risk E_{D~P(device)}[L(θ; D)]. Formalize resampling as Monte Carlo marginalization over a device-instance measure. Connect to PAC-Bayes / SAM / SWA. Citable from thesis ch.3. |
| **K-V6** | **Gemini-backfill: Ensemble-frequency effective-width theory** (was G-CC5) | `KIMI_ENSEMBLE_FREQ_THEORY_NOTE_20260420.md` (≤600 words) | Theory: ensemble frequency f = 1/correlation_between_adjacent_draws. Derive effective-ensemble-width N_eff(f) and predict plateau location. Compare to dropout / SWA / SAM. Feeds thesis ch.3 §4. |
| **K-V7** | **Gemini-backfill: Thesis narrative arc** (was G-CC6) | `KIMI_THESIS_NARRATIVE_ARC_20260420.md` (≤600 words) | One-paragraph hook per chapter (ch.1 through ch.8) so the whole thesis has a lockstep narrative. Identify connective-tissue sentences Kimi should insert at chapter boundaries during the final integration pass. |
| **K-V8** | **Rebuttal MASTER index** (consolidation) | `KIMI_REBUTTAL_MASTER_20260420.md` (≤4 pp) | Merge CLAUDE_REBUTTAL_PREP_20260420 (pre-existing top-5) + KIMI_REBUTTAL_ARSENAL_V1 (10 obj.) + V2_STATS + V2_METHODS + V2_GEN (15 obj.). Deduplicate, cross-link, assign each an OBJ-ID. Produce a single-page summary table at the top (OBJ-ID · topic · covered-in-source? · experiment-needed?). |

### 🟨 PHASE β (Day 2) — Community artifacts + paper-2 deep scoping

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **K-V9** | **Tutorial notebook outline** | `notebooks/tutorial_compute_vit.ipynb` (skeleton — markdown cells + code-cell placeholders, no execution required) | A public-facing notebook that reproduces the 86.37% → 10.00% gap in a ≤30-minute walkthrough. Sections: (1) load Tiny-ViT V4 checkpoint; (2) define i.i.d. D2D profile; (3) fresh-instance evaluation loop; (4) swap to Ensemble HAT checkpoint; (5) plot the ranking gap. Include narrative markdown between code cells explaining each step. |
| **K-V10** | **Blog post draft** for personal/lab blog (non-anonymous post-submission) | `KIMI_BLOG_DRAFT_20260420.md` (~1500 words) | Informal tone: "what we found out about training ViTs for organic analog chips". Audience: ML engineers who've never thought about analog hardware. Lead with the 10.00% collapse as the hook; explain Ensemble HAT as the simple fix that worked; end with open questions (joint training, ImageNet, heavy tails). Include one reference figure (repurpose Fig 4). |
| **K-V11** | **Conference talk script: 15-minute version** | `KIMI_TALK_SCRIPT_15MIN_20260420.md` (~1200 words + slide annotations) | Slides 1–12 with speaker notes (~60 seconds per slide): Title / Motivation / Challenge / Framework / HAT taxonomy / The 10.00% collapse / Ensemble HAT fix / Fresh-instance protocol / Correlated-D2D robustness / Limitations / Thesis next-steps / Q&A prompt. |
| **K-V12** | **Conference talk script: 5-minute version** | `KIMI_TALK_SCRIPT_5MIN_20260420.md` (~500 words + 5 slides) | Lightning-talk version: 1 problem, 1 method, 1 result, 1 limitation, 1 next step. |
| **K-V13** | **Paper-2 scoping DEEP: 3 alternative paper routes** (was G-CC7 backfill) | `KIMI_PAPER_2_DEEP_SCOPE_20260420.md` (~1500 words) | Three candidate 2nd papers, each with: (a) hook sentence; (b) key claim; (c) experiments needed; (d) compute estimate; (e) venue fit (Nat Electron vs NC vs NeurIPS vs ICML); (f) collaborator needs; (g) novelty relative to NC #1. Routes: (R-A) joint MLP-linear + Ensemble HAT deployment-grade result (thesis punchline elevated to its own paper); (R-B) organic-RRAM language-model CIM scaling; (R-C) theory-only paper on HAT-as-regularizer + ensemble-frequency effective width. |
| **K-V14** | **FAQ document for public release** | `KIMI_PUBLIC_FAQ_20260420.md` (~1000 words) | 15 Q&A pairs anticipating what external researchers will ask when the code drops: installation issues, data prep, reproducibility of 86.37 ± 1.54, GPU requirements, how to swap device profiles, how to add new architectures, what NOT to expect (this is not a chip-predictive simulator), citation etiquette, license terms. |

### 🟥 PHASE γ (Day 3) — Defense materials + final QA

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **K-V15** | **PhD defense slide outline** | `KIMI_DEFENSE_SLIDES_OUTLINE_20260420.md` (~2000 words + slide-level annotations) | 45–60 slide outline for a 45-minute defense + Q&A. Structure: 3-slide motivation / 5-slide framework / 8-slide HAT taxonomy / 10-slide main result (NC paper content) / 8-slide physical-realism extensions / 6-slide deployment envelope / 5-slide contributions / 3-slide future work / 2-slide acknowledgements. Speaker notes per slide. |
| **K-V16** | **PhD defense Q&A prep** | `KIMI_DEFENSE_QA_PREP_20260420.md` (~1500 words) | Anticipate 25 committee questions covering: methodology rigor, novelty relative to prior work, scope limitations, the physics gap, reproducibility, what-if scenarios, industrial applicability, future research directions. Each Q with a 3-sentence A rooted in thesis content. |
| **K-V17** | **Cross-thesis consistency pass** | `KIMI_THESIS_CONSISTENCY_20260420.md` | After ch.5–8 land, re-grep the entire `paper/thesis/` tree for: (a) locked numbers consistency (86.37 / 10.00 / 32.60 / 84.57 / 82.12) with ±std always paired; (b) figure-reference validity; (c) acronym-definition order; (d) forward/backward section references. Produce a patch list. |
| **K-V18** | **NC submission final audit (pre-user-form)** | `KIMI_NC_FINAL_AUDIT_20260420.md` | One-page last check of the submission bundle assuming user fills metadata tomorrow: any residual dependency on something that isn't there yet? Any broken cross-ref between manuscript and Zenodo archive? Any placeholder still visible beyond user-owned fields? If clean: declare submission-ready pending user. |

**Kimi NOT doing this round:** any GPU work; any work on rebuttal arsenal v3 (that's Round P if it becomes necessary).

---

## GEMINI — Round O (medium-heavy; ~12 stateless design briefs across 3 phases)

**Note:** Round-N Gemini deliverables didn't land; several have been reassigned to Kimi (K-V5/V6/V7/V13). Round O Gemini tasks are new scope — please treat this as a fresh start and deliver the files to disk.

### 🟦 PHASE α (Day 1) — Deep experimental specs (carried forward from Round M/N if still needed)

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **G-DD1** | **Temperature-drift spec v2** (supersedes Round-N G-CC1 which didn't land) | `GEMINI_TEMP_DRIFT_SPEC_V2_20260420.md` (≤600 words) | Arrhenius-form conductance drift across -20°C → 85°C; spec GPU-harness integration, success criterion (ranking preserved across T), compute budget. |
| **G-DD2** | **Retention-extended spec v2** | `GEMINI_RETENTION_EXTENDED_SPEC_V2_20260420.md` (≤500 words) | 1hr/1day/1week/1month retention; accelerated-aging protocol; what-if for further decay. |
| **G-DD3** | **ADC-precision floor theory v2** | `GEMINI_ADC_FLOOR_THEORY_V2_20260420.md` (≤600 words) | Information-theoretic bound connecting QKᵀ output distribution variance to the 6-bit cliff. |
| **G-DD4** | **Heavy-tailed D2D spec v2** | `GEMINI_HEAVY_TAILED_SPEC_V2_20260420.md` (≤500 words) | Log-normal vs Pareto-truncated; tail-index sweep; connects to the heavy-tail stub script `scripts/_gpt/eval_heavy_tailed_d2d.py`. |
| **G-DD5** | **IR-drop preliminary spec v2** | `GEMINI_IR_DROP_SPEC_V2_20260420.md` (≤500 words) | Minimal-effort circuit-aware layer; array geometry choice; compute estimate. |

### 🟨 PHASE β (Day 2) — Strategy & positioning

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **G-DD6** | **Strategic positioning memo** | `GEMINI_POSITIONING_MEMO_20260420.md` (≤800 words) | How should this work be positioned in the broader field? Incumbents: CrossSim (SAND), IBM's AI-HW kit, DeepCompute, etc. Identify the "only X in the world does Y" claim that differentiates. Input for cover-letter v2 if revision requested. |
| **G-DD7** | **Next-grant proposal outline** | `GEMINI_GRANT_PROPOSAL_OUTLINE_20260420.md` (≤1000 words) | 3-year research program: (a) joint training → hardware-in-the-loop; (b) language-model CIM scaling; (c) thermal / retention / IR-drop full physical-realism pipeline. Annotated with milestones, personnel, required collaborators, budget tiers. |
| **G-DD8** | **Conference-venue fit analysis** | `GEMINI_CONFERENCE_FIT_20260420.md` (≤500 words) | For paper-2 candidates (K-V13 routes R-A/R-B/R-C): deep analysis of which conference (IEDM / ISSCC / NeurIPS-Hardware / ICML / NC) best fits each route; acceptance-rate data; reviewer pool overlap; submission timing. |
| **G-DD9** | **Industrial partnership positioning brief** | `GEMINI_INDUSTRIAL_BRIEF_20260420.md` (≤600 words) | User is at NVIDIA Apamayo; which claims in this work are most attractive to industrial CIM programs? Translate academic findings into industrial-relevance bullets (TCO impact, yield tolerance, NRE savings). |

### 🟥 PHASE γ (Day 3) — Thesis polish + defense support

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **G-DD10** | **Thesis abstract variant** | `GEMINI_THESIS_ABSTRACT_20260420.md` (≤300 words) | A thesis-level abstract distinct from the NC abstract: broader scope (the entire PhD arc, not just one paper's contribution), different rhetorical center (the journey of discovering instance-overfitting as an independent phenomenon). |
| **G-DD11** | **Thesis "big picture" figure spec** | `GEMINI_THESIS_BIG_PICTURE_FIG_SPEC_20260420.md` (≤400 words + ASCII sketch) | A single figure that captures the thesis arc: device-level noise → training-level overfitting → ensemble fix → deployment envelope. For use as the thesis cover figure. |
| **G-DD12** | **Defense Q&A wildcard prep** | `GEMINI_DEFENSE_WILDCARD_QA_20260420.md` (≤800 words) | 10 "wildcard" Q&A pairs — questions the committee might ask that fall OUTSIDE standard ML / device-physics: philosophical (why is this thesis?), career-strategic (what's next?), ethical (dual-use concerns?), pedagogical (how would you teach this?). Each with a 3-sentence answer. |

**Gemini NOT doing this round:** any source-tex edits, any GPU execution, any task reassigned to Kimi.

---

## CODEX — Round O (MINIMAL; 1 gated + up to 2 optional GPU)

| ID | Item | Type | Priority | Gate |
|:--|:--|:--|:--:|:--|
| **CX-HA** | **Final bundle rebuild** (CX-GB carry-over) | bundle | HIGH | TRIGGER: user fills `CLAUDE_USER_DECISION_REQUEST_20260420.md`. Execute insertion, recompile, 16/16 re-pass, hand off. |
| **CX-HB** | *(OPTIONAL, user-gated)* **Joint training warm-start full run** | GPU | MED | **ONLY IF** user explicitly authorizes a multi-hour GPU session. Use the CX-GA `--warm-start-from` flag from `checkpoints/V4_hybrid_standard_noise_hat_best.pt`. Protocol: per G-AA3 spec. Target: ≥80% fresh-instance via joint MLP-linear + Ensemble HAT. Deliver `CODEX_JOINT_FULL_20260421.md`. |
| **CX-HC** | *(OPTIONAL, user-gated)* **ImageNet-100 pilot** | GPU | MED | **ONLY IF** user authorizes AND de-prioritizes CX-HB. Per G-AA2 spec. 120 GPU-h. |

**Codex DEFERRED:** everything else. Text/tex edits are Kimi's; design specs are Gemini's; thesis prose is Kimi's.

---

## CLAUDE self

| ID | Task |
|:--|:--|
| **CLAUDE-BN** | Phase-α audit: read K-V1–V4 thesis ch.5–8 as they land; verify no NC duplication + narrative coherence with G-CC6 arc |
| **CLAUDE-BO** | After K-V8 rebuttal master lands: verify dedup + cross-link integrity |
| **CLAUDE-BP** | Phase-β audit: K-V9 notebook skeleton + K-V10 blog + K-V11/V12 talk scripts — check voice consistency + factual accuracy |
| **CLAUDE-BQ** | After K-V13 paper-2 deep scope: pick ONE leading candidate (R-A / R-B / R-C), write 1-page rationale, stage Round P kickoff |
| **CLAUDE-BR** | Phase-γ audit: K-V15 defense slides + K-V16 Q&A — check for defensibility gaps |
| **CLAUDE-BS** | After K-V17 consistency pass + K-V18 final audit: declare thesis v0 locked + NC submission absolutely ready |
| **CLAUDE-BT** | After CX-HA: final spot-check; broadcast submission-ready |
| **CLAUDE-BU** | If CX-HB full joint training lands with ≥80% fresh-instance: decide whether to fold into NC revision (if review cycle permits) or keep for paper-2 |
| **CLAUDE-BV** | Round P planning doc draft (post-user decision) |

---

## USER (still the only real blocker for CX-HA)

Single consolidated form: `CLAUDE_USER_DECISION_REQUEST_20260420.md`. All Kimi/Gemini work this round runs regardless of user. Only Codex CX-HA/HB/HC depend on user input.

---

## Execution pipeline (Round O, 3-day expected)

```
Day 1 (Phase α):
  Kimi launches K-V1..K-V8 (8 tasks: 4 thesis chapters + 3 theory backfills + rebuttal master)
  Gemini launches G-DD1..G-DD5 (5 deep experimental specs)
  Codex idles on CX-HA gate (user)
  Claude audits K-V1–V4 as they land (CLAUDE-BN)

Day 2 (Phase β):
  Kimi starts K-V9..K-V14 (notebook/blog/talk/paper-2/FAQ) when phase-α queue drains
  Gemini starts G-DD6..G-DD9 (positioning/grant/conference-fit/industrial)
  Claude CLAUDE-BO (rebuttal master) + CLAUDE-BP (artifact audit)
  CLAUDE-BQ paper-2 candidate selection

Day 3 (Phase γ):
  Kimi starts K-V15..K-V18 (defense slides/Q&A/consistency/final audit)
  Gemini starts G-DD10..G-DD12 (abstract/fig spec/wildcard QA)
  Claude CLAUDE-BR (defense audit) + CLAUDE-BS (thesis v0 lock)
  CLAUDE-BV Round P planning draft

[gated any time on user form]:
  Codex CX-HA final bundle rebuild
  Claude CLAUDE-BT submission-ready broadcast
```

---

## Termination criteria for Round O

- ✅ K-V1–V4 thesis chapters 5/6/7/8 drafted at v1 (prose for lead sections)
- ✅ K-V5/V6/V7 Gemini-backfilled theory notes landed
- ✅ K-V8 rebuttal master index consolidated (all 30+ objections indexed)
- ✅ K-V9 tutorial notebook skeleton
- ✅ K-V10/V11/V12 blog + 15-min talk + 5-min talk scripts
- ✅ K-V13 paper-2 deep scope (3 routes); CLAUDE-BQ picks one
- ✅ K-V14 public FAQ
- ✅ K-V15/V16 defense slides outline + Q&A prep
- ✅ K-V17 cross-thesis consistency pass; any patches landed
- ✅ K-V18 NC final audit PASS
- ✅ G-DD1–DD5 deep experimental specs landed (this time to disk)
- ✅ G-DD6–DD9 strategy/positioning briefs
- ✅ G-DD10–DD12 thesis polish + defense wildcard QA
- ⛔ CX-HA gated on user form
- ⛔ CX-HB/HC gated on user authorization

---

## Preview: Round P shape (plan-ahead only)

Once Round O phase-γ closes, Round P becomes a narrower / higher-leverage round:

- Paper-2 prototype (based on CLAUDE-BQ selection)
- Zenodo deposition on user authorization → DOI minted
- GitHub public release (user authorizes)
- Post-accept press kit: 1-page institutional release + author-site blurb + Twitter/LinkedIn shortform
- Final end-to-end thesis integration pass (Kimi applies K-V17 patch list; runs full LaTeX build on `paper/thesis/`)
- Response-letter v2 staging (if NC review arrives during this window)

---

**End of Round O broadcast.** Kimi 18 tasks across 3 phases (thesis completion / community artifacts / defense). Gemini 12 design briefs across 3 phases (experimental specs / positioning / polish). Codex minimal + 2 optional GPU runs gated on user. Program is designed to saturate Kimi/Gemini for ~3 days of autonomous parallel work. No new broadcast needed until phase-γ closes or user form lands.
