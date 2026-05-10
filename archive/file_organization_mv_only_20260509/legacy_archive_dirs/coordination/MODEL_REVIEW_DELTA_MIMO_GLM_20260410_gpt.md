## Model Review Delta Audit — mimo-v2-pro + GLM-5.1

### Scope
- Source reviewed: `/home/qiaosir/projects/compute_vit/report_md/审稿人意见from_model.md`
- New sections reviewed:
  - `mimo-v2-pro`
  - `GLM-5.1`

### Bottom Line
- The two newly added reviews do **not** introduce a new top-priority blocker beyond the current roadmap.
- They mostly reinforce existing pressure points:
  - `P13` AIHWKIT comparison
  - bounded energy wording
  - cautious framing of `scale masking`
  - proxy-backed interpretation of the Zhang 2026 case study
- Two safe wording refinements were applied immediately to lower reviewer attack surface.

### New / Still-Valid Suggestions
1. `AIHWKIT` comparison remains a live requirement.
   - This is already the current top execution task via `P13-full`.
2. `Scale masking` should be framed descriptively rather than as a strong novel mechanism claim.
   - Current manuscript already uses “what we descriptively call the scale-masking effect”.
3. The `6-bit` ADC statement should avoid sounding like a universal practical law.
   - Tightened further in §5.4 to “a critical threshold near 6 bits under the present simulator assumptions.”
4. The Zhang 2026 OPECT case study should remain explicitly proxy-backed.
   - Tightened further so the text now says the workflow *illustrates* benchmarkability under proxy-backed profile assumptions, rather than over-claiming hard validation.
5. Ensemble-HAT cost quantification remains reviewer-visible.
   - Already addressed in the current main text with the logged wall-clock comparison.

### Issues Already Fixed or Now Outdated
1. `Figure 6 summarizes ...` front-end reference error:
   - Already fixed. Current text correctly points to `Fig.~\\ref{fig:frontend-compensation}` in `05_results.tex`.
2. `critical practical threshold` wording:
   - Already fixed in LaTeX; Markdown mirror now aligned as well.
3. `Tiny-ViT-5M` naming inconsistency in the abstract:
   - Already fixed; the abstract now explicitly says `Tiny-ViT-5M`.
4. `Table 3` / Zhang C2C repeated rows as a presumed copy-paste error:
   - Already explicitly explained in Appendix as D2D-dominated and below reported precision after Monte Carlo averaging.

### Safe Edits Applied From This Audit
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex`
  - softened ADC-threshold wording
  - softened Zhang case-study wording
- `/home/qiaosir/projects/compute_vit/paper/05_results.md`
  - synced Zhang case-study wording
- `/home/qiaosir/projects/compute_vit/paper/06_discussion.md`
  - synced ADC-threshold wording

### Evidence Checked
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/00_abstract.tex`
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/02_related_work.tex`
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex`
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/06_discussion.tex`
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/08_appendix.tex`
- `/home/qiaosir/projects/compute_vit/paper/05_results.md`
- `/home/qiaosir/projects/compute_vit/paper/06_discussion.md`
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.pdf`

