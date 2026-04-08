# Citation Map (GPT)

This file maps the narrative citation placeholders still present in `paper/*.md` to the current BibTeX keys in `paper/latex_gpt/refs_gpt.bib`.

It is the shared normalization reference for:
- English LaTeX closeout
- Gemini's `paper_zh/` cross-checking
- later venue-template migration

## Locked Mappings

| Narrative placeholder | BibTeX key |
|:--|:--|
| `Horowitz 2014` | `horowitz2014computing` |
| `Peng et al. 2020` | `peng2020dnnneurosim` |
| `Alibart 2016` | `alibart2016physical` |
| `Xu et al. 2025` | `xu2025emerging` |
| `Guo et al. 2024` | `guo2024organic` |
| `Zeng et al. 2023` | `zeng2023organicmemristor` |
| `Jung et al. 2024` | `jung2024organicfilaments` |
| `Vincze et al. 2026` | `vincze2026dualplasticity` |
| `MemTorch` | `memtorch` |
| `Wu et al. 2023` | `wu2023bwq` |
| `Wang et al. 2024` | `wang2024epim` |
| `Ge et al. 2024` | `ge2024allspark` |
| `Jacob et al. 2018` | `jacob2018quantization` |
| `Bengio et al. 2013` | `bengio2013estimating` |
| `Yoon et al. 2025` | `yoon2025adc` |
| `Li et al. 2022` | `li2022timemultiplexing` |
| `Gebregiorgis et al. 2023` | `gebregiorgis2023organiccim` |

## Still Unresolved

These placeholders should not be silently fabricated into final journal citations until the exact target reference is chosen.

| Placeholder | Current handling |
|:--|:--|
| `Fault-Aware Training Survey` | keep as narrative placeholder in markdown; do not force a BibTeX key yet |
| `MemTorch` final bibliographic form | current `memtorch` entry is usable for draft LaTeX, but the exact venue/source should be finalized later |

## Usage Rule

- If `paper/*.md` and `paper_zh/*.md` need wording updates, keep the scientific claim aligned first.
- If LaTeX needs a cite key immediately, prefer the mapping above.
- If a placeholder is unresolved, keep it explicit rather than inventing a polished but uncertain reference.
