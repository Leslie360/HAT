# Kimi Dispatch — NL Follow-up (2026-04-17)

You are helping finalize the `compute_vit` manuscript. Focus only on nonlinear write (`NL`) and do not invent baselines.

## Deliverables
Create these 3 files under `report_md/_gpt/`:

1. `KIMI_NL_PRIOR_ART_20260417.md`
- Find real primary-source prior art relevant to:
  - non-linear write / programming asymmetry in analog CIM training
  - optimizer / STE / write-aware mitigation ideas
  - any paper that localizes sensitivity to MLP / FC blocks vs attention/QKV in transformers or analog ViTs
- For each item provide:
  - full citation
  - DOI / stable URL
  - 2-3 sentence relevance note
  - whether it is safe to cite in the main manuscript vs rebuttal only
- Do **not** fabricate labels like `MI-HAT` or `SDR-HAT` unless they are real published names.

2. `KIMI_NL_WORDING_20260417.md`
- Write drop-in prose for:
  - main-text discussion of `NL=2.0` as a training-surrogate limit rather than a device law
  - rebuttal-side wording for the broader `NL` sweep (`1.2/1.5/1.8/2.0/2.2/2.5/3.0`)
  - a short paragraph on why `MLP-localized mitigation` is a logical next experiment
- Keep tone conservative and reviewer-facing.

3. `KIMI_NL_METHOD_COMPARISON_20260417.md`
- Identify the nearest real method families for comparing our `MLP-only mitigation` idea.
- We need real names only, such as:
  - write-aware training
  - update-aware / program-aware training
  - custom STE / surrogate-gradient methods for analog nonlinearity
- For each family give:
  - canonical reference(s)
  - exact method name
  - what comparison claim is safe
  - what claim would be overreach

## Constraints
- Prefer primary sources and official publisher pages.
- Do not rely on blog posts or secondary summaries unless there is no primary source.
- If you cannot verify a citation, say so explicitly.
- The output should be directly usable for `refs_gpt.bib`, related work, and reviewer response.
