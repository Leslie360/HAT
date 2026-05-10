# CC Paper1 Author Review — 2026-05-10

## Verdict

minor_edits

## Blocking Findings

| Severity | File/page | Issue | Recommended fix |
|---|---|---|---|
| Minor | `paper1/manuscript/sections/04_experimental_setup.tex:8` | Table caption still uses the stiff phrase “Data establish the ideal software performance...”. This is not a scientific blocker, but it survived Codex's stale-wording pass and reads less polished than the surrounding prose. | Replace with smoother wording such as “These baselines define the ideal software reference before analog non-ideality injection.” |
| Minor | `paper1/manuscript/supplementary_main.tex:33` and `paper1/manuscript/supplementary.tex:269,283,287,691,805,806` | Supplement still exposes the `\notrun{}` macro and “n.e.” entries. The caption explains that it means not evaluated, not failed, so this is defensible, but it may distract reviewers because the main-text stale scan explicitly removed `notrun`-style wording. | Prefer spelling these table entries as “not evaluated” or “n.e. (not evaluated)” directly in the Supplement, then remove the macro if unused. |
| Minor | `paper1/release/paper1_submission_bundle_20260509_final/RELEASE_README.md:2-5` and `SHA256SUMS.txt:47-58` | The final release bundle is still the 2026-05-09 accepted bundle and has not been refreshed after Codex Paper1 narrative polish pass 2. Active manuscript is therefore ahead of the submission bundle. | After the minor text edits are accepted, Codex should sync active `main.tex`, `sections/`, and `main.pdf` into the final bundle, then refresh `SHA256SUMS.txt` and rebuild the tarball. |

## Nonblocking Polish Notes

| File/page | Note | Suggested wording or action |
|---|---|---|
| `paper1/manuscript/sections/01_introduction.tex:9` | “The paper makes three contributions” is acceptable but slightly mechanical. | Optional: “We make three contributions.” |
| `paper1/manuscript/sections/05_results.tex:44` | “Ensemble HAT finds a broad plateau” is supported by the figure narrative, but “finds” can sound causal/visual rather than quantitative. | Optional: “is associated with a broader plateau” if Codex wants extra caution. |
| `paper1/manuscript/sections/05_results.tex:71-76` | The ADC/D2D Sobol statement is concise and useful. Caption avoids overclaiming, but the hard-cliff language is strong. | Keep if source data supports it; otherwise soften “hard cliff” to “operational cliff” in text/caption. |
| `paper1/manuscript/sections/06_discussion.tex:42` | Analog KV-cache is mentioned only as a future memory-bound inference component, not as Paper1 evidence. | Keep; it is properly framed as future work and does not import Paper2/107 claims. |
| `paper1/manuscript/sections/08_availability.tex:4` | Availability mentions the public GitHub URL and MIT licence. | Looks consistent with the prior license correction; no action unless release packaging changes the public URL. |

## Claim Consistency Checks

| Check | Status | Evidence |
|---|---|---|
| IdealDevice algorithmic ablation is separated from PCM deployment frontier | PASS | Abstract explicitly says “the algorithmic result is not itself a PCM deployment claim” at `sections/00_abstract.tex:2`; Results labels the IdealDevice section as an algorithmic ablation at `sections/05_results.tex:6-14`; PCM frontier starts separately at `sections/05_results.tex:46-66`. |
| Main PCM numbers are internally consistent | PASS | 8-bit 77.60%, 6-bit 68.44% with std 6.03%, and 4-bit 76.68% / 4.01 pp drift appear consistently in Abstract, Introduction, Results Table, Discussion, and Conclusion. Grep found no active `68.55` or `0.07 pp` stale values in the reviewed manuscript paths. |
| Claims avoid absolute hardware prediction | PASS | Experimental Setup warns that parameters are literature-derived/proxy-calibrated and should be read as comparative risk rankings, not absolute hardware predictions (`sections/04_experimental_setup.tex:23`). Discussion repeats the limitation for circuit parasitics and energy estimates (`sections/06_discussion.tex:21-24`). |
| Paper2/107 not promoted into Paper1 | PASS | Main text mentions analog KV-cache only as a future study direction (`sections/06_discussion.tex:42`; `sections/07_conclusion.tex:8`), with no 107 numeric claims. |
| Figure/table captions avoid major overclaiming | PASS with minor polish | Main captions generally mark algorithmic vs PCM roles correctly. Only `sections/04_experimental_setup.tex:8` should be smoothed. |
| Release bundle matches active polished manuscript | NOT YET | Codex report says release bundle was intentionally untouched; `RELEASE_README.md` and `SHA256SUMS.txt` still correspond to the pre-polish 2026-05-09 bundle. |

## Supplement/Main Consistency

| Check | Status | Evidence |
|---|---|---|
| Supplement supports the main algorithmic/physical separation | PASS | Supplementary PCM vs IdealDevice comparison repeats the IdealDevice 8-bit/4-bit and Ensemble HAT values (`supplementary.tex:718-741`) and the main text keeps PCM claims separate. |
| Supplement flags retired/invalid diagnostics | PASS | Severe-NL/Task35 diagnostics are explicitly marked invalid or historical at `supplementary.tex:797-815`, avoiding the old MLP-localization overclaim. |
| Supplement limitations are candid | PASS | PAC-Bayes slack is explicitly described as directional rather than predictive (`supplementary/S_theory_ensemble_hat.tex:186`), CrossSim comparison avoids superiority claims (`supplementary/S_tooling_comparison.tex:18`), and OPECT distribution limits are stated (`supplementary/S_opect_distribution.tex:56-74`). |
| Supplement notation/stale markers | MINOR EDIT | `\notrun{}` / `n.e.` entries remain in Supplement tables. They are explained, but replacing them with explicit “not evaluated” wording would reduce reviewer friction. |
| Supplement contradicts main PCM conclusion | PASS | The 6-bit transition-zone conclusion is consistent with the supplement's four-seed closure and late-recovery retirement note (`supplementary.tex:908-940`). |

## Release Recommendation

I recommend `minor_edits`: the active Paper1 manuscript is scientifically coherent after Codex polish pass 2, and I found no major claim, number, Paper2-contamination, or Supplement/Main contradiction blocker. Before release-bundle refresh, Codex should apply the two small prose/notation fixes above, rebuild `main.pdf` and the Supplement if the macro/table wording changes, then sync the accepted active manuscript into `paper1/release/paper1_submission_bundle_20260509_final/`, refresh `SHA256SUMS.txt`, and rebuild the final tarball.
