# Round P Plan — Post-Submission / Post-Defense Pipeline

**Author:** Claude (Chief Architect)
**Trigger:** Round O closed. Thesis v0 drafted (8 chapters, 120 pp compiled). NC bundle refreshed.
**Theme:** Paper-2 prototype + Zenodo/GitHub release + press kit + thesis final integration.

---

## State on disk (pinned at t0)

- NC bundle: `outputs/submission_bundle_20260419/` — refreshed with current .tex + .bbl
- Thesis: `paper/thesis/` — 8 chapters + `main.tex` compiling to 120 pp
- Rebuttal: `KIMI_REBUTTAL_MASTER_20260420.md` — 27 OBJs indexed
- Paper-2 scope: `KIMI_PAPER_2_DEEP_SCOPE_20260420.md` — Route R-A selected
- Community artifacts: tutorial notebook, blog draft, talk scripts, FAQ — all on disk
- GPU: idle; warm-start bug fixed (CX-GA)

---

## KIMI — Round P (~10 tasks)

| ID | Item | Deliverable | Priority |
|:---|:-----|:------------|:--------:|
| K-W1 | Thesis final integration pass | Apply K-V17 patch list; insert K-V7 boundary sentences; rebuild `main.pdf` | HIGH |
| K-W2 | Paper-2 manuscript skeleton | `paper/paper_2/skeleton.tex` — Introduction + Methods + anticipated Results structure | HIGH |
| K-W3 | Paper-2 results section (preliminary) | `paper/paper_2/prelim_results.md` — Placeholder prose for ≥80% target; actual numbers to be inserted post-GPU | MED |
| K-W4 | Press kit: 1-page institutional release | `report_md/_gpt/KIMI_PRESS_RELEASE_20260420.md` | MED |
| K-W5 | Press kit: author-site blurb | `report_md/_gpt/KIMI_AUTHOR_BLURB_20260420.md` (~200 words) | MED |
| K-W6 | Press kit: social shortforms | `report_md/_gpt/KIMI_SOCIAL_SHORTFORM_20260420.md` — Twitter/X + LinkedIn threads | LOW |
| K-W7 | Zenodo README final | `release_artifacts/zenodo_archive_v0/README.md` — polished, with DOI placeholder | MED |
| K-W8 | Thesis dedication + acknowledgements draft | `paper/thesis/acknowledgements.tex` | LOW |
| K-W9 | Response-letter v2 staging (if reviews arrive) | `report_md/_gpt/KIMI_RESPONSE_V2_STAGING_20260420.md` | ON-DEMAND |
| K-W10 | Full thesis bibliography consistency | Reconcile thesis-only cites with NC refs; ensure no duplicates | MED |

---

## GEMINI — Round P (~6 tasks)

| ID | Item | Deliverable | Priority |
|:---|:-----|:------------|:--------:|
| G-EE1 | Zenodo deposition checklist | `GEMINI_ZENODO_CHECKLIST_20260420.md` — file manifest, metadata fields, license compatibility | HIGH |
| G-EE2 | GitHub release checklist | `GEMINI_GITHUB_RELEASE_CHECKLIST_20260420.md` — release notes, tag strategy, CI/actions | MED |
| G-EE3 | Open-source governance brief | `GEMINI_OSS_GOVERNANCE_20260420.md` — contribution guidelines, code of conduct, issue templates | LOW |
| G-EE4 | Industrial pilot proposal | `GEMINI_INDUSTRIAL_PILOT_20260420.md` — 6-month engagement plan for NVIDIA-internal CIM team | MED |
| G-EE5 | Conference submission calendar | `GEMINI_CONF_CALENDAR_20260420.md` — IEDM/ISSCC/NeurIPS/ICML deadlines for R-A and R-B | MED |
| G-EE6 | Collaborator outreach template | `GEMINI_COLLAB_OUTREACH_20260420.md` — cold-email templates for 3 target groups (device fab, FPGA emulation, theory) | LOW |

---

## CODEX — Round P (user-gated)

| ID | Item | Type | Gate |
|:---|:-----|:-----|:-----|
| CX-IA | Final bundle rebuild (CX-HA carry-over) | bundle | **TRIGGER:** user metadata form submitted |
| CX-IB | Paper-2 GPU run: Joint MLP-linear + Ensemble HAT | GPU | **ONLY IF** user authorizes. Target: ≥80% fresh-instance. Protocol: per K-V13 R-A spec + G-AA3. |
| CX-IC | Paper-2 GPU run: ImageNet-100 pilot (if deprioritized in Round O) | GPU | **ONLY IF** user authorizes AND de-prioritizes CX-IB. |

---

## CLAUDE self — Round P

| ID | Task |
|:---|:-----|
| CLAUDE-BW | After K-W1: declare thesis v1.0 locked |
| CLAUDE-BX | After CX-IB: decide whether ≥80% result folds into NC revision or stays for paper-2 |
| CLAUDE-BY | After Zenodo README + G-EE1: trigger deposition on user authorization |
| CLAUDE-BZ | After GitHub release: public-announcement coordination (blog + social + press) |
| CLAUDE-CA | Round Q planning (if needed) |

---

## Termination criteria for Round P

- ✅ Thesis v1.0 compiled clean (K-W1)
- ✅ Paper-2 skeleton on disk (K-W2)
- ✅ Zenodo archive finalized (G-EE1 + K-W7)
- ✅ GitHub release checklist ready (G-EE2)
- ✅ Press kit complete (K-W4/K-W5/K-W6)
- ⛔ CX-IB/CX-IC gated on user GPU authorization
- ⛔ Zenodo deposition DOI gated on user authorization
- ⛔ GitHub public release gated on user authorization

---

## Preview: Round Q shape (plan-ahead only)

- Paper-2 full manuscript (if CX-IB succeeds)
- Thesis defense rehearsal (slide deck built from K-V15 outline)
- NC revision response (if reviews arrive)
- ImageNet-100 pilot (if not done in Round P)
- Collaborator meetings + grant submission (G-DD7)
