# Codex Manuscript/Figure Patch — 2026-05-01

## Verdict
Local Paper-1 is now in a coherent submission-shaping state for the locked spine:

- Algorithmic failure/rescue: IdealDevice 8-bit stable, 4-bit pure quantization collapses, Ensemble HAT rescues 4-bit.
- Physical substrate: PCM UnitCell 4/6/8-bit precision ladder now uses raw-artifact-verified 3-seed data.
- Deployment narrative: 6-bit PCM is the best tested precision-retention midpoint; 4-bit is trainable but drift-limited.

No mandatory local GPU experiments remain for Paper-1 before draft polishing. Remaining experiments are optional strengthening or future-work validation.

## Files changed or generated

### Manuscript integration
- `paper/latex_gpt/main.tex`: retitled away from stale organic/optoelectronic framing; keywords aligned to analog CIM/HAT/PCM/precision-retention.
- `paper/latex_gpt/supplementary_main.tex`: supplementary title aligned to main title.
- `paper/latex_gpt/sections/01_introduction.tex`: reframed opening around analog CIM deployment risk, PCM, and separation of algorithmic vs physical limits.
- `paper/latex_gpt/sections/02_related_work.tex`: changed simulator positioning from organic-specific replacement to profile-level extension/risk-ranking layer.
- `paper/latex_gpt/sections/05_results.tex`: inserted main spine figure and softened causal PCM wording to tested-regime observation.
- `paper/latex_gpt/sections/06_discussion.tex`: filled previously empty treatment subsection with sequential design rule: first cross-instance HAT, then precision-retention choice.
- `paper/latex_gpt/sections/07_conclusion.tex`: corrected public release URL to `https://github.com/Leslie360/HAT`.
- `paper/latex_gpt/supplementary/design_rules_box.tex`: retitled design-rule box to analog CIM transformer deployment.

### Figure/source data
- `paper/latex_gpt/figures/fig1_paper1_spine.pdf`
- `paper/latex_gpt/figures/fig1_paper1_spine.png`
- `paper/latex_gpt/source_data/fig1_paper1_spine.csv`
- `paper/latex_gpt/source_data/tab_pcm_precision_ladder.csv`
- `paper/latex_gpt/source_data/manifest_paper1_spine.json`
- `scripts/_gpt/plot_paper1_spine.py`

### Guard/provenance
- `scripts/_gpt/check_local_pcm_precision_ladder.py`
- `report_md/_gpt/CODEX_LOCAL_EXPERIMENT_AUDIT_20260501.md`
- `report_md/_gpt/CODEX_NEXT_STEPS_AFTER_LOCAL_AUDIT_20260501.md`

## Verification

Commands run:

```bash
/home/qiaosir/miniconda3/bin/python scripts/_gpt/plot_paper1_spine.py
python scripts/_gpt/check_locked_numbers.py
python scripts/_gpt/check_local_pcm_precision_ladder.py
cd paper/latex_gpt && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cd paper/latex_gpt && latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex
rg -n "undefined references|undefined citations|Reference .* undefined|Citation .* undefined|Label .* multiply defined|! LaTeX Error|Emergency stop|Fatal error|Overfull|Placeholder|PLACEHOLDER|TODO|FIXME|TBD" ...
```

Results:

- Locked number guard: 22/22 PASS.
- Local PCM precision-ladder guard: PASS.
- `main.pdf`: builds successfully, 14 pages.
- `supplementary_main.pdf`: builds successfully, 41 pages.
- Final log/source scan: no undefined refs/citations, fatal LaTeX errors, Overfull boxes, placeholders, TODO/FIXME/TBD.

## Current answer to user questions

### Are the figures acceptable?
Yes for draft/submission-shaping. Main text now has a compact two-panel spine figure plus a PCM precision table. SI late-recovery figure is no longer a placeholder. Source data and manifest exist.

Remaining figure polish, if time allows:

1. Harmonize all SI figure visual style; not blocking.
2. Add a small schematic for the sequential rule: HAT first, precision-retention second; optional.
3. Ensure final journal-specific figure sizing after target venue is chosen.

### Do we need more local experiments?
No mandatory local GPU experiments for Paper-1. The local data support the locked spine.

Optional only:

1. PCMPresetDevice 3-seed sensitivity: useful for SI/thesis, not blocking Paper-1.
2. 105 cross-architecture TinyImageNet seeds: useful validation, not needed for current main claim.
3. 107 analog KV-cache: separate Work-2, should not enter Paper-1 except as future work.

### What must the paper still change?
P0 manuscript work now shifts from experiments to polish/package:

1. Clean source-data archive and manifest for all main/SI figures, not only Fig. 1.
2. Decide target venue and adjust formatting/length accordingly.
3. Do one hostile read focused on claim strength: every causal verb must be either supported or softened to tested-regime observation.
4. Do reference audit for all retained organic/optoelectronic SI claims; they are supplementary now, not the main spine.
5. Prepare reviewer-accessible code/data archive around the guarded scripts and raw JSONs.
