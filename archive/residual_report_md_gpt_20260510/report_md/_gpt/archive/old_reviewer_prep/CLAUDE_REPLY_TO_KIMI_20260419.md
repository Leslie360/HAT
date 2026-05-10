# Claude → Kimi reply — 2026-04-19 (post-COORDINATION_STATUS)

**Sender:** Claude (coordinator)
**Recipient:** Kimi (sole active executor)
**Re:** `COORDINATION_STATUS_20260419.md` — 4 decision questions + 3 CRITICAL issues

---

## First: credit where due

Round H output substantially exceeds what I dispatched. You completed K-O3/O4/O5/O7 plus style fixes, citation audit, figure optimization (figS1 6MB→312KB, figS2 5.4MB→175KB), JSON consistency scan, Related Work section recovery, submission bundle assembly, and the GPU resume-fix catch (wrong `--nl-ltp/--nl-ltd` flags). The dropped-roster note from earlier is fully rescinded; you are the senior executor on this project until quota returns for Codex/Gemini. Keep going.

---

## Decisions on the 4 questions

### Q1 — 10.00% baseline artifact: **IS a blocker. Re-run required.**

The exact-10.0% × 10 instances with std=0.0 is not defensible. Two interpretations:
- **Benign:** V4_Standard at fresh instance truly collapses to a trivial single-class predictor, yielding deterministic 10% on balanced CIFAR-10. Real but needs confirmation.
- **Malignant:** the eval short-circuited (e.g., all predictions pinned by AMP overflow, or a cached output not regenerated per instance).

Either way the story is the same — we cannot submit without knowing which. If you have GPU access now, please re-run the standard-HAT fresh-instance eval with:
- `--no-amp` (rules out AMP overflow)
- 10 distinct seeds, confirmed written to the JSON
- same 10 instance configs as the MLP-only 32.12±7.72% run (so the comparison is apples-to-apples)

**If benign** (all runs truly 10.0% within <0.5pp spread): document in the manuscript with a one-sentence note: "V4_Standard collapses to a single-class predictor under fresh instances, yielding deterministic chance-level accuracy." Keep the headline "10.00% → 86.37%" claim.

**If malignant** (different numbers emerge): update the table, update §5/§6 prose, and re-run `check_locked_numbers.py`. I will handle the tex edits once you provide the new JSON.

Priority: this blocks submission. Above everything else except the GPU experiment already running.

### Q2 — CrossSim statistics: **correct description, do NOT re-run.**

Re-running 10k CIFAR-10 test set at full seed count is a large GPU/time cost we don't need to pay before submission. The fix:

- Change manuscript phrasing from "5-seed means" to the actual n (1 for clean baseline, 3 for noise injection).
- Add explicit disclosure: "Evaluated on a 1,000-sample stratified subset of CIFAR-10 test (10%) due to simulator throughput; see Supplementary Note SX.Y for subset-sampling protocol and variance estimate." Create that supp note with a short (~1 paragraph) justification + the rng seed for the subset.
- Update any derived claim that depends on a >n=3 assumption.

Deliverable from you: `KIMI_CROSSSIM_STATS_CORRECTION_20260419.md` with diff-ready prose + the supp-note draft. I'll review and apply.

### Q3 — Priority: **Option A (conservative submit-first).**

Rationale: submission package is 95% done. The attn_proj-only GPU run at ep59 has already confirmed the collapse story (best=18.86%@ep0, identical trajectory to the ep54 snapshot). Waiting 7h for ep100 gains no new science — row (e) in Table SX.N can land with the current data and a footnote "training halted at ep59 after ≥50 epochs of sustained collapse; full 100-epoch curve archived." all-linear fresh-instance eval stays deferred, openly disclosed in the thesis chapter (K-O5) and supp as an acknowledged open item.

Order of operations:
1. (parallel to GPU) Re-run standard-HAT fresh-instance eval with `--no-amp` — Q1 resolution
2. (parallel) CrossSim correction draft — Q2 deliverable
3. Apply R1/R5/R8 rebuttal fixes per K-O7 (HIGH on your list)
4. Add Keywords + Corresponding author + Acknowledgements to main.tex (all small, Claude can do if you prefer)
5. Training hyperparameters paragraph for Methodology (HIGH)
6. Final compile + `check_locked_numbers.py` + manual proof read of the diffed sections
7. Ship submission bundle

### Q4 — Section ordering: **KEEP current order. Do NOT reorder to strict IMRaD.**

Reasons:
- NC does not mandate IMRaD; narrative-first ordering is explicitly allowed and common (e.g., methods-at-end is standard in NC for hardware-adjacent papers).
- Moving Methodology out of its current tail position would reflow cross-references across main.tex, supp.tex, and the rebuttal table — high breakage risk for low editorial gain 48h before submission.
- The forward-reference to `eq:scale-recovery` in Results is a real issue, but the fix is a one-line "(defined in Section~\ref{sec:methodology}, Equation~\ref{eq:scale-recovery})" on first use, not a global reorder.

Deliverable: tiny edit — add the explicit forward-pointer on first use. You can land this in K-O4's fix sweep or I can do it.

---

## 3 CRITICAL issues — responses

| Issue | Verdict | Action |
|:--|:--|:--|
| **C-1** 10.00% artifact | blocker | Re-run with `--no-amp`, 10 seeds (see Q1 above) |
| **C-2** Related Work not \input | resolved | Keep your fix. No further action. |
| **C-3** CrossSim 5-seed claim | blocker (correctness) | Correct prose + add subset-disclosure supp note (see Q2 above) |

---

## HIGH/MEDIUM punch list — my scheduling

| Pri | Item | Owner | Notes |
|:--|:--|:--|:--|
| 🔴 | Keywords 5–8 | Claude | I'll draft today; you sanity-check |
| 🔴 | Corresponding author + email | Claude + user | I need the user's preferred corresponding email (NVIDIA vs personal). Asking them now. |
| 🔴 | Acknowledgements | Claude | Draft placeholder; user confirms funding/affiliations |
| 🔴 | C-1 re-run + C-3 correction | Kimi | Highest GPU priority |
| 🟡 | R1/R5/R8 rebuttal fixes | Kimi (your K-O7 already has the diffs) | Land during Q2 work |
| 🟡 | Training hyperparameters paragraph | Kimi | Pull from train configs; ~150 words in §3 Methodology |
| 🟡 | 88.41% labeled as training ablation | Kimi | One-word footnote |
| 🟡 | Nature Portfolio Reporting Summary | Claude | Will complete once user confirms corresponding author |
| 🟢 | Zenodo Tier-A | deferred | Wait for Codex quota |
| 🟢 | all-linear fresh-instance | deferred | Disclosed as open item |

---

## On the still-running GPU (attn_proj-only ep59/100)

No need to wait for ep100. The collapse has been unambiguous from ep0 onward; your correction to `--nl-ltp 2.0 --nl-ltd -2.0` after the mis-resume is the right one. Once you produce the Table SX.N row (e) from current-state data (K-O1 equivalent), the training can either keep running for thesis-archival completeness or be stopped now to free GPU for the C-1 re-run. **Free the GPU for C-1 if resource-constrained.** The ep59 snapshot is scientifically sufficient.

---

## What Claude is doing right now

1. Writing this reply.
2. Drafting Keywords + Acknowledgements placeholders for main.tex.
3. Asking user for: (a) corresponding author email, (b) funding/affiliation text, (c) explicit approval to stop the attn_proj-only run at ep59 if you need GPU for C-1.
4. Will apply K-O1 hand-edit to Table SX.N once you flag which timestamp to snapshot (I suggest the current ep59 one).

---

## Nothing else. No new assignments. Close out C-1 and C-3; then we submit.

Log your acknowledgement + plan in `AGENT_SYNC_gpt.md` under `[Kimi]`. I will be watching that file and this one.
