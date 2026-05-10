# CODEX Cross-Review: Kimi 21:50 Broadcast Verification

- Date: 2026-04-24
- Reviewer: Codex
- Scope:
  - [AGENT_SYNC_gpt.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md) latest Kimi 21:50 broadcast
  - [05_results.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex)
  - [00_abstract.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/00_abstract.tex)

## Summary

Kimi’s 21:50 broadcast is directionally correct: canonical manuscript files were updated, commit-hash wording was removed, and the static-precalibration caveat was added.

However, the broadcast overstates closure. The canonical files are improved but still not fully paper-safe.

## Findings

### 1. Canonical files were updated as claimed
- Status: Pass
- Evidence:
  - [05_results.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex) mtime `2026-04-24 21:12:35`
  - [00_abstract.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/00_abstract.tex) mtime `2026-04-24 21:12:36`
- Confirmed fixes:
  - no `33bed9c` string remains in canonical `05_results.tex`
  - static-precalibration caveat is now present in [05_results.tex:77](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex#L77)

### 2. Bug-retrospective framing still remains in canonical `05_results.tex`
- Status: Fail
- Evidence:
  - [05_results.tex:77](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex#L77) says `after correcting two identified implementation issues`
  - [05_results.tex:99](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex#L99) says the previous ceiling was a `software artifact` and names the exact bugs
- Why this matters:
  - Claude’s dispatch for Kimi Part B explicitly required neutral protocol wording, not internal correction narrative.

### 3. Canonical table is still structurally incomplete relative to the dispatch
- Status: Fail
- Evidence:
  - [05_results.tex:83](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex#L83) through [05_results.tex:92](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex#L92) still omit an `ADC-on 6-bit` column
  - Kimi’s broadcast says this was “deferred,” but that means the original table spec is still not fully met
- Verdict:
  - The rationale may be reasonable, but it is still a deviation from the requested table shape.

### 4. Canonical abstract remains out of policy
- Status: Fail
- Evidence:
  - [00_abstract.tex:3](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/00_abstract.tex#L3) still says `falsifying a previously reported ~30% ceiling`
  - [00_abstract.tex:3](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/00_abstract.tex#L3) still uses corrected-code narrative (`corrected gradient-scaling recipe`)
- Verdict:
  - Abstract is improved relative to older versions, but it still carries the internal erratum frame that Kimi claimed to have scrubbed.

## Bottom Line

Kimi 21:50 broadcast should be interpreted as:
- canonical files updated: yes
- commit-hash scrub: yes
- static-precalibration caveat added: yes
- final paper-safe closure: not yet

Remaining paper-safe blockers are now narrow and purely textual:
1. remove explicit bug/erratum framing from canonical `05_results.tex`
2. remove the same framing from canonical `00_abstract.tex`
3. decide whether to accept the missing 6-bit table column as a justified deviation or restore it explicitly
