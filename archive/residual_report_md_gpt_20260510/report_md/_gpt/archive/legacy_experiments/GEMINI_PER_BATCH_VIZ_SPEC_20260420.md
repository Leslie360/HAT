# G-BB3: Per-batch vs per-epoch HAT visualization spec

## Figure purpose
Answer the reviewer question “Why epoch-level D2D resampling instead of per-batch resampling?” with one compact trade-off figure.

## Proposed layout
- **Panel A:** accuracy vs cadence
  - x-axis: `fixed`, `every 20 epochs`, `every 5 epochs`, `per-epoch`, `per-batch`
  - y-axis: fresh-instance accuracy
  - marker + error bar for mean ± std
- **Panel B:** training cost vs cadence
  - y-axis: relative wall-clock or epochs-to-best
- **Panel C:** optional variance bar
  - y-axis: standard deviation across fresh instances

## Visual encoding
- Use the same color for all cadences, with `per-epoch` highlighted in a darker tone.
- Use a dashed vertical reference line or shaded band to call out the selected paper cadence.
- Keep a single sentence takeaway above the panels: “Per-epoch resampling is the best accuracy/stability compromise; per-batch increases stochasticity without improving final transfer.”

## Matplotlib notes
- category plot (`errorbar` on integer x positions)
- one shared legend only if Panel B/C require it
- no more than 5 categories; no nested annotations
