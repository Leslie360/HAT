# NC Compression Plan (2026-04-09)

## Goal

- Current compiled main paper: `25 pages`
- Target for `Nature Communications`-style main text: roughly `10-12 pages` main paper
- Strategy: keep the deployment-decision narrative and the strongest quantitative results in the main paper; move implementation-heavy details, large parameter tables, and secondary robustness diagnostics into Supplementary Information (SI)

## Current Section Load

Based on the current LaTeX section files:

| Section | File | Lines | Compression Priority |
|:--|:--|--:|:--|
| Abstract | `00_abstract.tex` | 7 | low |
| Introduction | `01_introduction.tex` | 16 | low |
| Related Work | `02_related_work.tex` | 27 | medium |
| Methodology | `03_methodology.tex` | 43 | high |
| Experimental Setup | `04_experimental_setup.tex` | 33 | high |
| Results | `05_results.tex` | 172 | very high |
| Discussion | `06_discussion.tex` | 63 | very high |
| Conclusion | `07_conclusion.tex` | 10 | low |
| Appendix | `08_appendix.tex` | 144 | move to SI |

## Main-Paper Story That Must Survive

The compressed main text should keep exactly this spine:

1. Organic device metrics alone do not answer deployment viability.
2. Existing simulators are valuable, but not centered on organic optoelectronic profile substitution and hybrid deployment decisions.
3. We contribute a profile-driven, first-order behavioral bridge from device characterization to task-level deployment risk.
4. We answer four concrete deployment questions:
   - Is quantization really the main bottleneck?
   - What fails first as task complexity rises?
   - Is same-instance robustness enough?
   - Which richer physical regimes can be retrained around?
5. The strongest positive and negative results:
   - `10.00% -> 86.37 ± 1.54%` fresh-instance recovery with Ensemble HAT
   - `88.53%` literature-derived Zhang 2026 OPECT transfer
   - `97.37 ± 0.05%` proportional-noise matched recovery
   - `27.72 ± 0.82%` nonlinear-write hard boundary
   - corrected retention plateau near `~79%`

Anything that does not directly support that spine should be compressed or moved to SI.

## Proposed Main-Text Structure

### 1. Introduction

Keep in main text:
- deployment-decision gap
- why organic optoelectronic CIM needs a dedicated bridge
- four deployment questions
- headline quantitative outcomes

Trim:
- repetitive roadmap sentences
- duplicated limitations language

Target:
- `~1.0-1.2 pages`

### 2. Related Work

Keep in main text:
- one concise paragraph on organic neuromorphic / optoelectronic devices
- one concise paragraph on CIM simulators: NeuroSim, MemTorch, AIHWKIT, CrossSim
- one concise paragraph on HAT / quantization-aware deployment

Move or cut:
- extended simulator-by-simulator nuance that does not affect the paper's positioning
- repeated “not a chip-accurate emulator” caveats

Target:
- `~0.8-1.0 page`

### 3. Methodology

Keep in main text:
- hybrid analog/digital mapping concept
- differential-pair conductance abstraction
- one compact paragraph on noise / retention / nonlinear-write profile injection
- one compact paragraph on energy-model scope

Move to SI:
- extended formulas and derivations
- full measurement-to-parameter table
- detailed energy-constant table
- long explanation of optical frontend equations
- retention-equation details

Target:
- `~1.5-2.0 pages`

### 4. Experimental Setup

Keep in main text:
- model suite
- datasets
- one short paragraph defining canonical vs stress-test regimes
- reproducibility statement

Move to SI:
- full V1-V8 / C1-C8 matrix
- seed / eval-run / checkpoint lineage table
- detailed hardware profile tables

Target:
- `~0.8-1.0 page`

### 5. Results

This is the main compression site.

Current problem:
- too many subsections
- too many local conclusions that repeat the same high-level message
- some diagnostics belong in SI

#### Proposed merge plan

**5.1 Canonical accuracy and complexity scaling**
- merge current `5.1 + 5.2 + 5.3`
- keep:
  - FP32 baseline table
  - one canonical degradation/recovery figure
  - key message: quantization alone is not the main bottleneck; complexity amplifies fragility
- move:
  - extra wording around every model/dataset pair

**5.2 ADC and retention bottlenecks**
- merge current `5.4 + 5.5`
- keep:
  - 6-bit threshold discussion
  - corrected retention plateau result
- move:
  - long step-by-step retention semantics explanation

**5.3 Fresh-instance transfer and physical stress**
- merge current `5.6 + 5.8 + 5.9`
- keep:
  - fresh-instance collapse
  - Ensemble HAT recovery
  - proportional-noise recovery
  - nonlinear-write failure boundary
- move:
  - secondary ConvNeXt nuance
  - extended wall-clock commentary beyond one sentence

**5.4 Frontend and literature-derived case study**
- merge current `5.7 + 5.11`
- keep:
  - frontend compensation is beneficial but trade-off-laden
  - Zhang 2026 case study as the bridge proof
- move:
  - detailed parameter provenance to SI
  - sensitivity table to SI

**5.5 Energy profile**
- keep as standalone but short
- emphasize upper-bound nature and digital-attention ceiling
- keep only one compact paragraph plus figure reference

Target:
- `~4.0-4.5 pages`

### 6. Discussion

Keep in main text:
- one subsection on dominant bottlenecks
- one subsection on architectural implications
- one subsection on what the framework can and cannot claim

Move to SI or cut:
- long future-work lists
- repeated inorganic-comparison caveats
- repeated limitations already visible in methods/results

Target:
- `~1.5-2.0 pages`

### 7. Conclusion

Keep:
- one short recap of the deployment bridge
- three strongest conclusions
- one bounded closing statement

Target:
- `~0.5 page`

## What Should Move to Supplementary Information

Move almost all of current Appendix plus setup-heavy tables:

1. Full V1-V8 / C1-C8 / stress-test matrix
2. Full parameter provenance tables
3. Zhang proxy sensitivity sweep
4. C2C CI table
5. detailed energy constants and component assumptions
6. state-dependent retention sanity-check details
7. extra reproducibility tables
8. auto-fitter details
9. additional figure-level diagnostics

## Figure Strategy for Compression

### Keep in main paper

- system architecture schematic
- weight mapping schematic
- one canonical accuracy figure
- one HAT/fresh-instance figure
- one retention figure
- one energy figure
- one optional frontend/case-study figure if space allows

### Move to SI if page pressure remains high

- attention map figure
- standalone zero-shot bar chart if same message is already in text/table
- secondary noise-sensitivity panels

## Concrete Editing Order

1. Freeze GPU-dependent numbers first:
   - `P1-fix-v3`
   - `P13`
   - `P14`
2. Then compress in this order:
   - `08_appendix.tex` -> SI content bucket
   - `04_experimental_setup.tex` -> trim and move experiment matrix
   - `05_results.tex` -> merge subsections
   - `06_discussion.tex` -> collapse repeated caveats
   - `02_related_work.tex` -> tighten simulator comparison
3. Recompile and inspect page count after each stage

## Reviewer Benefit

This compression plan directly addresses:

- `#44` manuscript too long
- `#67` results fragmented
- `#70` Section 2 overlap
- `#71` Section 4 verbose

It also indirectly improves readability for the broader reviewer set by making the paper read as one coherent deployment-decision story rather than as a sequence of loosely connected experiment reports.
