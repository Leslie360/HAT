# Bibliography Key Mapping 2026-04-17

Purpose: map the Perplexity export in `report_md/bibliography_structured.csv` onto the current manuscript bibliography in `paper/latex_gpt/refs_gpt.bib` without rewriting citation keys inside the LaTeX sources.

## Safe direct mappings

These rows match the current bibliography either by exact key or by exact title/year identity and can be used to patch metadata only.

| CSV key | Current bib key | Mapping basis | Action |
|---|---|---|---|
| `peng2020dnnneurosim` | `peng2020dnnneurosim` | exact key | kept, added DOI URL |
| `rasch2021aihwkit` | `rasch2021aihwkit` | exact key | kept manuscript key, retained arXiv DOI style |
| `crosssim2024` | `crosssim2026` | exact title/year | keep manuscript key, no citation-key rewrite |
| `lammie2022memtorch` | `lammie2022memtorch` | exact key | added DOI URL |
| `choi2018pact` | `choi2019pact` | exact title/year | keep manuscript key, added stable URL |
| `jacob2018quantization` | `jacob2018quantization` | exact key | manuscript DOI already stronger than CSV |
| `bengio2013estimating` | `bengio2013estimating` | exact key | added DOI URL |
| `tobin2017domain` | `tobin2017domain` | exact key | added DOI URL |
| `xu2025emerging` | `xu2025emerging` | exact key | added DOI URL |
| `guo2024organic` | `guo2024organic` | exact key | added DOI URL |
| `zhang2025optoelectronic` | `photonics2025organicreview` | exact title/year | keep manuscript key |
| `liu2025opect` | `zhang2026opect` | exact title/year | keep manuscript key |
| `vincze2025dualplasticity` | `vincze2026dualplasticity` | exact title/year | keep manuscript key |
| `zhang2025largescale` | `zhang2025mooptoelectronic` | exact title/year | keep manuscript key |
| `cui2025integrated` | `cui2025multimode` | exact title/year | keep manuscript key |
| `liu2023artificial` | `visionarch2023crosstalk` | exact title/year | keep manuscript key |
| `li2024activematrix` | `amspa2024insensor` | exact title/year | keep manuscript key |
| `melianas2020temperature` | `fuller2020tempresilient` | exact title/year | keep manuscript key |
| `guo2024hightemperature` | `guo2024hightemp` | exact title/year | keep manuscript key |
| `wu2024blockwise` | `wu2023bwq` | title identity | keep manuscript key |
| `ge2025allspark` | `ge2024allspark` | exact title/year | keep manuscript key |
| `bettayeb2024efficient` | `bettayeb2024memristorattention` | exact title/year | keep manuscript key |
| `yang2025fastir` | `fastirdrop2025` | exact title/year | keep manuscript key |
| `liu2026iconniv` | `iconniv2025` | exact title/year | keep manuscript key |
| `wei2020voltage` | `wei2020voltagedifferential` | title identity | keep manuscript key |
| `kim2024accuracy` | `kim2024sttmram` | title identity | keep manuscript key |

## Key drifts worth keeping as-is

These are not errors. The current manuscript keys are already referenced in the `.tex` sources and changing them would create unnecessary churn.

- `crosssim2024` vs `crosssim2026`
- `choi2018pact` vs `choi2019pact`
- `liu2025opect` vs `zhang2026opect`
- `vincze2025dualplasticity` vs `vincze2026dualplasticity`
- `zhang2025optoelectronic` vs `photonics2025organicreview`

## One row that still needs external confirmation

- CSV key: `lin2023fqvit`
- Current likely match: `lin2023vitptq`
- Why not patched automatically:
  - the current bib already contains the title `FQ-ViT: Post-Training Quantization for Fully Quantized Vision Transformer`
  - the CSV export did not align on key naming
  - this looks like a naming mismatch, not a content mismatch
- Practical conclusion:
  - no blocker for current manuscript build
  - only ask Perplexity if we want a cleaned canonical citation-key policy for future releases

## Metadata policy used in this pass

- patched:
  - DOI when absent
  - URL when absent
  - stable bibliographic fields when unambiguous
- not patched:
  - manuscript citation keys
  - fields where the manuscript already had a stronger canonical form
  - rows where the CSV only offered weaker metadata, such as plain arXiv strings in the DOI column
