> Canonical coordination: `AGENT_SYNC_gpt.md` | Task ledger: `CLAUDE_TASK_gpt.md`
> Long-horizon: this broadcast declares Round N in full plus the **shape** of Rounds O–P so Kimi/Gemini can pre-plan.

# Round N Broadcast — 2026-04-19 11:25 (long-horizon program; Kimi/Gemini sustained saturation)

**Author:** Claude (Chief Architect)
**Trigger:** Round M closed. Everything submission-facing is done; only user metadata gates the final bundle. Codex `CX-FA` 3-epoch smoke confirmed joint-training wiring is valid but surfaced a real bug: the resume semantics inherit stale epoch counters, making naïve checkpoint reuse unsafe for warm-start. GPU remains idle but all *long* runs are user-gated (pending `CLAUDE_USER_DECISION_REQUEST_20260420.md`).
**Quota policy (user-directed):** Kimi ✅ **saturated** · Gemini 🟡 medium-heavy · Codex 🔴 **minimal** (1 bug-fix + CX-FD gated).
**Round N theme:** Since submission is metadata-gated and long GPU runs are user-gated, we saturate Kimi/Gemini on **long-horizon capital** that makes the NC paper, the thesis, and the next-paper pipeline all stronger at the same time.

---

## Long-horizon program (Rounds N → O → P)

| Round | Goal | Kimi shape | Gemini shape | Codex shape |
|:-:|:--|:--|:--|:--|
| **N** | Thesis Ch.2–4 drafting · rebuttal arsenal v2 (beyond top-10) · literature landscape deep-dive · repo hygiene · housekeeping completion | 10+ writing tasks | 7 design briefs (forward-experiment specs + theory framing) | 1 bug-fix (warm-start resume) + CX-FD gated |
| **O** *(forward shape)* | Thesis Ch.5–7 + community artifacts (blog, talk figures, tutorial notebook) + reviewer-drill rehearsal + RESPONSE_LETTER v2 pre-emptive refactor | 10+ writing tasks | 6–8 design/narrative tasks | nothing unless a bug lands |
| **P** *(forward shape)* | 2nd-paper scoping (organic-RRAM CIM beyond ViT) · post-accept press kit · final thesis integration pass | 6–8 strategy/prose tasks | 5–6 strategy/positioning tasks | Zenodo push + GitHub public release when user authorizes |

Agents: you are welcome to look ahead at Round O/P shapes and queue internal planning, but only execute Round N tasks explicitly listed below.

---

## State on disk (pinned)

- Bundle: main 17pp / supp 23pp / cover 2pp · 16/16 locked-numbers PASS · pre-flight v2 PASS
- Joint-training smoke: wiring valid (28.44% best @ ep1 cold-start, not evidence) · warm-start resume bug identified
- Rebuttal arsenal v1: 10 anticipated objections staged
- Thesis Chapter 1: LaTeX skeleton exists at `paper/thesis/chapter_1_hat_instance_overfitting.tex`
- Pending user decisions: metadata + GitHub URL + license + GPU-window priority

---

## KIMI — Round N (SATURATED; 11 tasks across 4 tracks)

### 🟦 Track α: Thesis drafting (Chapters 2–4, actual LaTeX prose)

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **K-U1** | **Thesis Chapter 2: Framework architecture (compute-ViT)** | `paper/thesis/chapter_2_framework.tex` (≤20 pp prose + figure refs) | Lift scope from NC §2–§3 but expand: (a) design rationale (why profile-driven), (b) pluggable interfaces (device model, mismatch, NL), (c) integration with PyTorch autograd, (d) validation against CrossSim as sanity layer. Do not repeat NC content verbatim — cite and extend. |
| **K-U2** | **Thesis Chapter 3: Hardware-aware training taxonomy** | `paper/thesis/chapter_3_hat_taxonomy.tex` (≤20 pp) | Full taxonomy: per-batch vs per-epoch vs fixed-mask; ensemble frequency sweep; noise-profile targeting (proportional vs additive vs mixed); literature comparison (DNN+, Qin et al., others from Kimi's memory). End with: how the choice of resampling cadence implicitly defines the transfer guarantee. |
| **K-U3** | **Thesis Chapter 4: Failure mode atlas** | `paper/thesis/chapter_4_failure_modes.tex` (≤25 pp) | Anchor: the 10.00% collapse story (§5 in NC) + NL=2.0 dual-attention collapse (Table SX.N) + MLP-only diagnostic + correlated-D2D bounded degradation + retention plateau at 79%. Frame each as a *named* failure mode with: trigger condition, observable signature, proposed mitigation, open question. This is the single most thesis-differentiated chapter. |

### 🟨 Track β: Rebuttal arsenal v2 (deeper, beyond top-10)

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **K-U4** | **Rebuttal arsenal v2: statistical rigor objections** | `KIMI_REBUTTAL_ARSENAL_V2_STATS_20260420.md` (≤3 pp) | 5 new objections specifically on statistical methodology: (1) n=10 fresh instances is small — is variance estimate reliable? (2) Two-level MC hierarchy — is the ±1.54 pp a proper standard error of the mean? (3) Did you correct for multiple comparisons across the 4 conditions? (4) Cohen's d / effect size on the 86.37 vs 10.00 gap? (5) Confidence-interval coverage for the correlated-D2D Δ? Each with answer rooted in existing data. |
| **K-U5** | **Rebuttal arsenal v2: method-comparison objections** | `KIMI_REBUTTAL_ARSENAL_V2_METHODS_20260420.md` (≤3 pp) | 5 new objections on method choice: (1) Why Tiny-ViT specifically? ImageNet-trained ViT-Base would be more convincing. (2) Why 4-bit conductance? Commercial targets are 2-bit or 8-bit. (3) Why 6-bit ADC as threshold? Derivation? (4) Why your D2D σ=0.1 as canonical? What range does literature span? (5) Why pairwise rather than joint attention-MLP perturbation? Each with data-rooted answer. |
| **K-U6** | **Rebuttal arsenal v2: generalization objections** | `KIMI_REBUTTAL_ARSENAL_V2_GEN_20260420.md` (≤3 pp) | 5 new objections on external validity: (1) Would this transfer to language-model workloads? (2) Would it transfer to CNNs outside Tiny-ViT class? (3) What about FP8 inference instead of 4-bit analog? (4) What if temperature varies over the inference lifetime? (5) Does fine-tuning-only HAT still work, or is training-from-scratch required? Each with answer. |

### 🟩 Track γ: Literature landscape + citation deepening

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **K-U7** | **Literature landscape review** (NC-scope + thesis-scope) | `KIMI_LIT_LANDSCAPE_20260420.md` (≤8 pp) | Current citation density: how many, which areas light. Add: (a) organic RRAM physics papers from last 3 years we might be missing; (b) analog CIM ViT / Transformer papers; (c) noise-aware training survey landscape; (d) Nature Comms / Science Adv / Nat Electron recent work in adjacent scope. For each, verdict: cite / consider-for-thesis / irrelevant. |
| **K-U8** | **Citation polish pass** | edits to `paper/latex_gpt/refs_gpt.bib` + minor tex inserts if truly missing | From K-U7, add the 5–10 highest-value citations to `refs_gpt.bib` and cite them in the appropriate existing paragraph (1–2 word inserts, no narrative rewrites). Recompile clean. |

### 🟥 Track δ: Repo & documentation hygiene (forward-facing)

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **K-U9** | **Docstring / README pass on `compute_vit/`** core modules | `KIMI_DOCSTRING_PASS_20260420.md` + edits to 3–5 core `.py` files | Identify the 5 most-referenced modules (e.g., training loop, D2D resampler, mismatch injector, profile loader, eval harness). Add 1-paragraph module docstrings + 1-line function docstrings on public API. Goal: someone reading the Zenodo archive could reproduce Fig 4 without a lab walk-through. |
| **K-U10** | **Top-level `README.md` for the public GitHub repo** | `KIMI_REPO_README_DRAFT_20260420.md` | NC-reviewer-facing: installation (conda + pip), reproduction commands for the 3 headline numbers (86.37 / 10.00 / 84.57), dataset prep, hardware requirements, citation block, license note. Placeholder GitHub URL + Zenodo DOI. User will land when ready. |
| **K-U11** | **Post-submission rebuttal-logistics playbook** | `KIMI_REBUTTAL_PLAYBOOK_20260420.md` (≤2 pp) | When reviews arrive, what happens in the first 72 hours: (a) triage protocol (who reads first, what they flag); (b) decision tree for "can we address verbally" vs "need new experiment"; (c) which pre-staged specs map to which expected objection type; (d) rebuttal-letter template structure; (e) timing budget for revised manuscript. |

---

## GEMINI — Round N (medium-heavy; 7 stateless design briefs)

### 🟨 Track β: Forward-experiment specs (rebuttal-defensive, deep)

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **G-CC1** | **Temperature-drift stress-test spec** | `GEMINI_TEMP_DRIFT_SPEC_20260420.md` (≤500 words) | Reviewers will ask about operating-temperature effects on organic-RRAM conductance. Spec: (a) temperature range (-20°C to 85°C automotive-grade?); (b) Arrhenius-form conductance drift model with activation-energy prior from literature; (c) reuse of fresh-instance harness with temperature-indexed profiles; (d) success criterion (ranking preserved across T). |
| **G-CC2** | **Retention-beyond-79% extended spec** | `GEMINI_RETENTION_EXTENDED_SPEC_20260420.md` (≤400 words) | Current retention plateau at 79% is suspicious — we don't know if it's an artifact of our test window or a true asymptote. Spec: (a) extended retention protocol (1 hour / 1 day / 1 week / 1 month projections); (b) forced-stress accelerated-aging method; (c) compute budget; (d) what-if: if we observe further decay, how does it bound the deployment envelope? |
| **G-CC3** | **ADC-precision floor theory** | `GEMINI_ADC_FLOOR_THEORY_20260420.md` (≤500 words) | Why 6-bit ADC is the threshold — theoretical derivation, not empirical fit. Information-theoretic bound on signal/quantization-noise ratio given the QKᵀ output distribution we observe; connect to the empirical 6-bit cliff. This lifts a rebuttal answer from "we measured" to "we predicted". |

### 🟩 Track γ: Theory framing (thesis narrative)

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **G-CC4** | **Theory note: HAT as implicit regularizer** | `GEMINI_HAT_AS_REGULARIZER_20260420.md` (≤600 words) | Frame Ensemble HAT mathematically: resampling D2D per epoch is equivalent to marginalizing the loss over a device-instance distribution. Show that fixed-mask training minimizes a *single* empirical risk, while Ensemble HAT minimizes expected risk over an instance measure. This gives the 10.00%-vs-86.37% gap a generalization-theoretic name. Citable inside thesis Chapter 3. |
| **G-CC5** | **Theory note: ensemble frequency as effective width** | `GEMINI_ENSEMBLE_FREQ_THEORY_20260420.md` (≤500 words) | Our ensemble-frequency sweep showed plateau behavior. Theory: treat frequency as the inverse of between-sample correlation; derive effective-ensemble-width formula; predict the location of the plateau. Connect to dropout / SWA / SAM literature. |

### 🟦 Track α: Thesis framing + forward vision

| ID | Item | Deliverable | Spec |
|:--|:--|:--|:--|
| **G-CC6** | **Thesis narrative arc (ch.1 → ch.N)** | `GEMINI_THESIS_NARRATIVE_ARC_20260420.md` (≤500 words) | Given Kimi is drafting chapters 2–4, lock the narrative ordering across all chapters: framework (ch.2) → HAT taxonomy (ch.3) → failure atlas (ch.4) → mitigation case studies (ch.5) → physical-realism extension (ch.6) → deployment envelope (ch.7) → outlook (ch.8). Write the 1-paragraph hook for each chapter Kimi can absorb into the drafts. |
| **G-CC7** | **Second-paper scoping: what could NC paper #2 be?** | `GEMINI_PAPER_2_SCOPING_20260420.md` (≤600 words) | Strategic thinking ahead: once NC #1 lands, what is the follow-up? Candidates: (a) joint MLP-Linear + Ensemble HAT as a deployment-grade result (if the Round-N/O full run succeeds); (b) organic-RRAM language-model CIM scaling; (c) hardware-in-the-loop paper with a fabrication collaborator; (d) theory paper purely on the HAT-as-regularizer thread. For each: novelty, venue fit (NC vs Nat Electron vs ICML), required compute, required collaborators. |

**Gemini NOT doing this round:** any source-tex edits, any GPU execution.

---

## CODEX — Round N (MINIMAL; 1 bug-fix + 1 gated)

| ID | Item | Type | Priority | Gate |
|:--|:--|:--|:--:|:--|
| **CX-GA** | **Warm-start resume semantics bug-fix** surfaced by CX-FA | code + test | HIGH | Immediate. Add a `--warm-start-from` flag that loads weights only (not epoch counter / optimizer state / scheduler state) from a canonical checkpoint. Verify via a 1-epoch smoke that the epoch counter starts at 0 and best-acc tracking works. No GPU full-run yet. Deliver `CODEX_WARM_START_FIX_20260420.md` + patch. |
| **CX-GB** | **Final bundle rebuild** (CX-FD carry-over) | bundle | HIGH | TRIGGER: when user fills `CLAUDE_USER_DECISION_REQUEST_20260420.md`. Execute metadata insertion, recompile, refresh bundle, 16/16 re-pass, hand off to CLAUDE-BD/BG. |

**Codex DEFERRED (no Round N execution):**
- Full joint MLP-Linear + Ensemble HAT run (gated on CX-GA fix + user authorization → Round O/P)
- ImageNet-100 pilot (gated on user priority → Round O/P)
- Heavy-tailed D2D full sweep (gated on G-BB1 spec approval → Round O)
- Temperature-drift / retention-extended / IR-drop experiments (all Round O/P candidates)
- Any new tex edits beyond K-U8 citations — Kimi owns text layer

---

## CLAUDE self

| ID | Task |
|:--|:--|
| **CLAUDE-BG** | Audit K-U1–U3 thesis chapters as they land — narrative coherence, no NC duplication, figure-ref validity |
| **CLAUDE-BH** | Consolidate K-U4/U5/U6 v2 arsenal + v1 arsenal into `CLAUDE_REBUTTAL_MASTER_20260420.md` (single index) |
| **CLAUDE-BI** | After K-U7 literature landscape: decide which 5 citations are "must-add before submission" vs "thesis-only" |
| **CLAUDE-BJ** | After G-CC6 narrative arc + K-U1–U3: ratify thesis outline; sign off on Round-O chapter targets |
| **CLAUDE-BK** | After G-CC7 paper-2 scoping: pick a leading candidate; frame Round-P as the first scoping round |
| **CLAUDE-BL** | After CX-GA fix: audit the patch; authorize Round-O full-run if user signals green |
| **CLAUDE-BM** | After CX-GB: submission-ready spot-check identical to CLAUDE-AY predecessor |

---

## USER (unblocks everything — still only one form to fill)

`CLAUDE_USER_DECISION_REQUEST_20260420.md` consolidates:
1. Acknowledgements text
2. Corresponding author + email + affiliation
3. Suggested reviewers (names; types per K-T8 brief)
4. GitHub repo URL + license
5. GPU-window priority (joint-training full vs ImageNet pilot) — *decision deferred to post-submission if needed*
6. CRediT author role assignments (initials per K-T3 template)

Once submitted, everything downstream unblocks automatically.

---

## Execution pipeline (Round N)

```
t0 (now):
  Kimi launches 11 tasks in parallel where possible:
    K-U1/U2/U3 thesis chapters (longest; can run concurrently)
    K-U4/U5/U6 rebuttal v2 (independent)
    K-U7 literature landscape (independent)
    K-U9 docstring pass (independent)
    K-U10 repo README draft (independent)
    K-U11 rebuttal playbook (independent)
  Gemini launches G-CC1–CC7 in parallel (all stateless)
  Codex fixes warm-start resume (CX-GA) — single immediate task

t+2-4h:
  K-U7 literature landscape in → K-U8 citation polish starts
  K-U8 lands → Codex recompile quick check
  G-CC4/CC5 theory notes feed back into K-U2/U3 chapter drafting (Kimi can absorb)
  G-CC6 narrative arc sets ordering

t+6-8h:
  K-U1–U3 thesis chapters at v1 (prose for lead sections, skeleton elsewhere)
  K-U4–U6 rebuttal v2 complete → CLAUDE-BH master index
  G-CC7 paper-2 scoping → CLAUDE-BK pick

[gated on USER form]:
  Codex CX-GB final bundle rebuild → CLAUDE-BM submission-ready declaration

[gated on USER GPU authorization]:
  Round O kickoff (full joint training OR ImageNet pilot, under warm-start-fixed launcher)
```

---

## Termination criteria for Round N

- ✅ K-U1/U2/U3 thesis chapters 2/3/4: each has at minimum §1 prose + §2–§5 outlines
- ✅ K-U4/U5/U6 rebuttal v2 covers 15 additional objections (stats, methods, generalization)
- ✅ K-U7 literature landscape reviewed; CLAUDE-BI picks must-add citations
- ✅ K-U8 citations landed; recompile clean
- ✅ K-U9 docstring pass on 5 core modules
- ✅ K-U10 repo README draft ready for user's GitHub URL
- ✅ K-U11 rebuttal logistics playbook staged
- ✅ G-CC1/CC2/CC3 deep experiment specs; G-CC4/CC5 theory notes; G-CC6 thesis arc; G-CC7 paper-2 scope
- ✅ CX-GA warm-start bug-fix landed + validated
- ⛔ CX-GB final bundle gated on user
- ⛔ Round O GPU kickoff gated on user

---

## Preview: Round O shape (no execution yet, plan-ahead only)

- Thesis Chapters 5–7 (mitigation case studies · physical-realism extension · deployment envelope)
- Full joint training OR ImageNet pilot (whichever user selects)
- Response-letter v2 pre-emptive refactor
- Blog post / tutorial notebook draft
- Reviewer-drill rehearsal (Kimi role-plays reviewer; Claude adjudicates)
- Codex may run the user-selected GPU experiment if warm-start fix is validated

## Preview: Round P shape

- Thesis Chapters 8 + conclusion
- Paper #2 scoping → lightweight prototype
- Zenodo push + public GitHub release (user authorizes)
- Post-accept press-kit + institutional announcement draft
- Final end-to-end thesis integration pass

---

**End of Round N broadcast.** Kimi 11 tasks (α thesis · β rebuttal v2 · γ literature · δ repo hygiene). Gemini 7 stateless (β deep specs · γ theory · α thesis arc + paper-2 scope). Codex 2 (warm-start fix + gated bundle). Long-horizon shape declared through Round P. Agents run in parallel; submission still gated only on user form.
