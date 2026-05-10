# CLAUDE DIRECTION RESOLUTION (2026-04-24)

## Analysis of the Direction Request

The core conflict is between the latest `remote` results and the newest `local` post-fix reruns.
- **Remote:** Proposes "domain randomization" (uniform NL=1.0 + D2D resample) based on an `r40 replica` yielding 54.69% fresh accuracy.
- **Local:** Demonstrates much stronger HAT recovery under the corrected code:
  - Uniform Ensemble HAT: ~81.7%
  - Uniform Standard HAT: ~82.6%
  - Proportional HAT: ~90.9%

**The local results definitively supersede the remote `r40` domain randomization route.** The remote route was based on a pre-fix codebase that conflated the bugs. Now that the code is fixed (LTP/LTD swap + config copying), the local M-series clearly shows that true HAT training (or even standard training) under the correct severe-NL dynamics recovers performance far better than the 54% achieved by domain randomization.

## Rulings

1. **Main Route:** The **local post-fix HAT route** (both Uniform and Proportional, pending the proportional config-consistency review) is the main scientific path. The remote `r40` domain randomization is relegated to a secondary/diagnostic baseline. It proves that simply resampling D2D without modeling the true NL dynamics is insufficient.

2. **Narrative Shift:** The canonical Work 1 paper story shifts from the "structural limit" (which was an artifact of the STE bug) to **"HAT recovery under corrected code"**. The core message is that the organic device's severe non-linearity is *not* an insurmountable structural limit, but a mapping challenge that can be overcome by proper Hardware-Aware Training (and potentially modulated by the noise law).

3. **Remote Node Action:** The remote node must **not** continue exploring the old `r40` family. Instead, the remote node should be used to accelerate the local M-series validation. The remote node must run the **M-Series Fast Exploration** queue (`REMOTE_TASK_QUEUE_20260424_M_SERIES_EXPLORATION.md`) using the exact local post-fix code (`33bed9c`).

4. **Minimum Evidence Threshold:** Before rewriting the results section, we need the cross-host validation of the M-series to land. Specifically, we need `R-M1`, `R-M2`, and `R-M3` from the remote queue to confirm the local ~82% and ~91% figures. We must also resolve the config-metadata discrepancy on the local proportional run (did it actually train at NL=2.0, or just eval?).

## Directives

1. **To User/Codex:** Push the `33bed9c` commit to the remote node.
2. **To Remote:** Execute the `REMOTE_TASK_QUEUE_20260424_M_SERIES_EXPLORATION.md` queue immediately to provide cross-host validation of the local M-series.
3. **To Kimi:** The narrative is now "HAT recovery". Do not use the `30.53%` structural ceiling numbers. Drafts should anticipate replacing the structural limit discussion with the ~82% (Uniform) and ~91% (Proportional) recovery figures, once validated by the remote node.
