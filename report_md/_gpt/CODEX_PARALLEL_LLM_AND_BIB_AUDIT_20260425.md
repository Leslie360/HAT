# Codex Parallel LLM + Bibliography Authenticity Audit

Date: 2026-04-25 22:25 CST
Owner: Codex
Scope: user requested parallel execution: keep LLM GPU work moving while verifying bibliography authenticity.

## Executive Verdict

1. Bibliography authenticity pass is now complete for `paper/latex_gpt/refs_gpt.bib`.
2. The current BibTeX database has 58 entries; all DOI/arXiv/URL-bearing entries resolved through machine checks.
3. DOI-title mismatch check found 0 low-similarity DOI/title pairs, which specifically guards against the earlier wrong-DOI failure mode.
4. `main.tex` and `supplementary_main.tex` both compile with `latexmk` RC 0 after the bibliography changes.
5. LLM Work 2 GPU smoke was run in parallel with three 200-step Pythia 410M hybrid last-block training jobs. No-noise remains stable; noisy all-analog paths remain unstable or high-variance and should not be promoted to paper claims.

## Files Changed Or Produced

### Edited

- `paper/latex_gpt/refs_gpt.bib`

### Produced

- `report_md/_gpt/refs_gpt_validation_20260425.json`
- `paper2/results/run_llm_parallel_wait_20260425_220737.sh`
- `logs/_gpt/w2_llm_hp_nonnoise_lb200_20260425_220737.log`
- `logs/_gpt/w2_llm_hp_noise005002_r10_lr5e6_lb200_20260425_220737.log`
- `logs/_gpt/w2_llm_hp_noise010005_r10_lr1e6_lb200_20260425_220737.log`

## Bibliography Validation Method

Checks performed:

1. Parsed `paper/latex_gpt/refs_gpt.bib`: 58 entries.
2. Parsed all LaTeX citation keys under `paper/latex_gpt/*.tex`, `paper/latex_gpt/sections/*.tex`, and `paper/latex_gpt/supplementary/*.tex`: 54 cited keys.
3. Missing cited keys: 0.
4. Uncited but real entries retained: `fastirdrop2025`, `iconniv2026`, `kirkpatrick2017overcoming`, `wager2013dropout`.
5. DOI validation: Crossref API for DOI entries, arXiv API for arXiv eprints, URL HEAD/GET fallback for URL-only entries.
6. DOI-title similarity validation: 0 low-similarity pairs.
7. Brace balance: balanced.
8. Non-ASCII scan: none remaining in `refs_gpt.bib`.

Validation output:

```text
entries 58
bad_or_needs_attention 0
low_title_similarity 0
cited_keys 54
bib_entries 58
missing []
uncited_entries 4 ['fastirdrop2025', 'iconniv2026', 'kirkpatrick2017overcoming', 'wager2013dropout']
```

## Key Bibliography Corrections

These were the highest-risk corrections because prior entries either had wrong DOI metadata, incomplete metadata, or pseudo-DOIs.

| Key | Action | Verified source |
|---|---|---|
| `kim2024sttmram` | Replaced unrelated ICCD metadata with the actual IEEE JXCDC paper metadata | https://doi.org/10.1109/JXCDC.2024.3478360 |
| `lin2024hardsea` | Replaced unrelated ASP-DAC metadata with IEEE TVLSI HARDSEA metadata | https://doi.org/10.1109/TVLSI.2023.3337777 |
| `lin2023vitptq` | Corrected FQ-ViT to IJCAI-22 proceedings metadata | https://www.ijcai.org/proceedings/2022/164 |
| `liu2021ptqvit` | Removed non-resolving pseudo-DOI, retained NeurIPS URL | https://proceedings.neurips.cc/paper/2021/hash/ec8956637a99787bd197eacd77acce5e-Abstract.html |
| `li2022qvit` | Removed non-resolving pseudo-DOI, retained OpenReview URL | https://openreview.net/forum?id=fU-m9kQe0ke |
| `cui2025multimode` | Corrected Nature Nanotechnology DOI, authors, volume, issue, pages | https://doi.org/10.1038/s41565-024-01794-z |
| `jang2023insensor` | Corrected Advanced Materials metadata and DOI | https://doi.org/10.1002/adma.202203830 |
| `beller2024organicneurons` | Corrected Nature Communications metadata and DOI | https://doi.org/10.1038/s41467-024-49668-1 |
| `ji2025singleoectneuron` | Completed authors and URL | https://doi.org/10.1038/s41467-025-59587-4 |
| `harikesh2024oeneurons` | Corrected Nature Electronics DOI | https://doi.org/10.1038/s41928-024-01200-5 |
| `ando2025transfer` | Updated to IEEE IEDM DOI metadata after Hume re-audit; prior IBM-only record was incomplete | https://doi.org/10.1109/IEDM50572.2025.11353900 |
| `qiu2025m3dattention` | Updated to IEEE IEDM DOI metadata after Hume re-audit; prior "DOI not yet public" statement was incorrect | https://doi.org/10.1109/IEDM50572.2025.11353844 |
| `yan2025learningaware` | Added IEEE DOI and complete author list | https://doi.org/10.1109/IEDM50572.2025.11353856 |
| `analogfm2025` | Added arXiv authors and URL | https://arxiv.org/abs/2505.09663 |
| `roberts2022principles` | Corrected to Cambridge University Press book metadata | https://doi.org/10.1017/9781009023405 |
| `wager2013dropout` | Corrected to NeurIPS 2013 proceedings entry and arXiv metadata | https://papers.nips.cc/paper/4882-dropout-training-as-adaptive-regularization |
| `kirkpatrick2017overcoming` | Corrected to PNAS article metadata and DOI | https://doi.org/10.1073/pnas.1611835114 |

Additional theory entries completed with official venue URLs/DOIs: `hochreiter1997flat`, `dziugaite2017computing`, `perez2021tighter`, `foret2021sharpness`, `keskar2017large`, `andriushchenko2022understanding`, `mcallester1999some`, `mcallester1999pac`.

## Compile Verification

Commands:

```bash
cd /home/qiaosir/projects/compute_vit/paper/latex_gpt
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex
```

Results:

- `main.pdf`: built successfully, 19 pages, RC 0.
- `supplementary_main.pdf`: built successfully, 39 pages, RC 0.
- No undefined citation warnings detected in logs.
- Remaining notable warning is layout-only: long IBM URL creates an overfull hbox in the bibliography.

## LLM Parallel GPU Smoke

Launcher:

```bash
paper2/results/run_llm_parallel_wait_20260425_220737.sh
```

All three jobs used:

```text
model: EleutherAI/pythia-410m-deduped
backend: /home/qiaosir/miniconda3/envs/LLM/bin/python
mode: hybrid high-precision analog
scope: last_block only
steps: 200
max_length: 64
dtype: float32
local_files_only: true
trainable_params: 12,596,224
modules wrapped: 24 QKV, 24 attention output, 48 MLP
peak CUDA per job: 3.76 GB
```

| Run | Noise | LR | Resample | Initial loss | Final loss | Min loss | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| `w2_llm_hp_nonnoise_lb200_20260425_220737` | none | 1e-5 | none | 6.4882 | 6.0010 | 6.0010 | Stable positive control |
| `w2_llm_hp_noise005002_r10_lr5e6_lb200_20260425_220737` | d2d 0.05, c2c 0.02 | 5e-6 | every 10 steps | 12.0682 | 13.8240 | 11.4106 | Unstable, not usable as canonical path |
| `w2_llm_hp_noise010005_r10_lr1e6_lb200_20260425_220737` | d2d 0.10, c2c 0.05 | 1e-6 | every 10 steps | 13.9156 | 12.5371 | 11.9847 | High variance, weak improvement, still not paper-safe |

Interpretation:

1. The Work 2 Pythia conversion and high-precision analog training path are operational.
2. The no-noise positive control is healthy and monotonic on the small smoke batch.
3. Naively enabling analog noise across all wrapped last-block modules remains damaging for Pythia, consistent with the earlier W1 risk signal.
4. Next W2 experiments should be staged and narrower: isolate MLP-only, output-projection-only, QKV-only, and KV-cache-only effects before claiming HAT-style recovery.

## Boundary Conditions

- The bibliography audit verifies metadata authenticity and citation-key integrity. It does not prove that every cited work is the best rhetorical support for each sentence.
- The LLM numbers are smoke-test numbers only. They are not WikiText, not long-context generation, and not paper claims.
- Correction on 2026-04-26: Hume found that `qiu2025m3dattention` and `ando2025transfer` both already have IEEE/Crossref DOI records. `refs_gpt.bib` has been updated accordingly; treat the older "DOI not yet public" statement as superseded.
