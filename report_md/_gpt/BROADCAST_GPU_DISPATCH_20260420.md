# BROADCAST GPU DISPATCH — 2026-04-20
## Multi-Tier GPU Execution Queue & Round P Initialization

**Author:** Claude (Chief Architect)
**Trigger:** User metadata form completed and user authorized GPU Option A (Joint MLP-Linear + Ensemble HAT pilot). 
**Theme:** Saturated GPU execution with strict tiering, while Kimi/Gemini pivot to artifact refinement and Paper-2 groundwork.

---

## 1. Dispatch Rationale

With the user's metadata form completed and **Option A** (Joint MLP-Linear + Ensemble HAT) explicitly authorized, we are now transitioning from artifact generation to deep execution. The GPU is the primary bottleneck, so we have established a strict **Multi-Tier Execution Queue** for Codex. Kimi and Gemini will perform asynchronous refinement of thesis chapters and community artifacts as new data trickles in from the GPU.

This broadcast serves as the canonical spec for the GPU queue and the corresponding Kimi/Gemini Round P tracking tasks.

---

## 2. Multi-Tier GPU Execution Queue (Codex)

The GPU is exclusively allocated to Codex. Execution must strictly follow these tier rules. Codex must drop a JSON payload and a 1-paragraph summary into `report_md/_gpt/` upon completion of each tier before advancing.

### Tier 1 (Critical)
- **Task:** `CX-J1` (Joint MLP-Linear + Ensemble HAT full run)
- **Compute:** ~60 GPU-hours
- **Goal:** Elevate the thesis punchline. Target ≥80% fresh-instance accuracy via joint training. 
- **Rule:** Must complete and validate before any other GPU tasks. If this fails or NaNs, halt the queue and trigger a new broadcast.

### Tier 2 (High Priority)
- **Tasks:** `CX-J2` (Heavy-tailed D2D full sweep), `CX-J3` (Temperature-drift stress-test full run)
- **Compute:** ~24 GPU-hours combined
- **Goal:** Directly support the physical-realism extension chapters (Thesis Ch. 6) and pre-empt NC reviewer physics objections.
- **Rule:** Execute only after CX-J1 is secured and checkpointed.

### Tier 3 (Medium Priority)
- **Tasks:** `CX-J4` (Retention-beyond-79% evaluation), `CX-J5` (IR-drop circuit-aware simulation)
- **Compute:** ~16 GPU-hours combined
- **Goal:** Expand the deployment envelope (Thesis Ch. 7) for industrial relevance.
- **Rule:** Execute sequentially after Tier 2.

### Tier 4 (Low Priority/Opportunistic)
- **Tasks:** `CX-J6` (ImageNet-100 pilot), `CX-J7` (ADC precision sweep ablation)
- **Compute:** ~130 GPU-hours combined
- **Goal:** Fulfill cover letter promises and defend against scalability questions.
- **Rule:** Only execute if GPU idle time exceeds 48 hours and Tiers 1-3 are verified and signed off by Claude.

---

## 3. Asynchronous Refinement (Kimi & Gemini)

While Codex manages the GPU, Kimi and Gemini will execute their respective tracking tasks (`K-W1`–`W8` and `G-EE1`–`EE4`). 

**Rule:** Do not wait for Codex. Proceed with artifact refinement using placeholder metrics if necessary, and patch them when Codex drops the JSON results.

### Kimi (Artifact & Thesis Refinement)
- Update Thesis Ch. 5–7 with incoming GPU data (`K-W1`–`W3`).
- Refine public artifacts: Tutorial notebook, Blog draft, Talk scripts, and FAQ (`K-W4`–`W8`).

### Gemini (Strategy & Positioning)
- Adjust Paper-2 strategy based on early CX-J1 metrics (`G-EE1`).
- Refine the grant proposal and industrial briefs (`G-EE2`–`EE3`).
- Produce visual asset specs for the press kit (`G-EE4`).

---

## 4. Claude Oversight

Claude will monitor the GPU queue execution (`CLAUDE-BW`), audit Kimi/Gemini's artifact refinement (`CLAUDE-BX`, `CLAUDE-BY`), and ultimately declare Round P closed to prepare the final Zenodo push (`CLAUDE-BZ`).

*End of GPU Dispatch Broadcast.*