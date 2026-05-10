# G-BB4: Ethics + reproducibility statement draft

## Ethics statement
This work does not involve human participants, patient data, animal experiments, or dual-use biological materials. The study is computational and simulation-based, and therefore no institutional ethics approval or participant consent was required.

## Reproducibility statement
All manuscript-quoted numerical values are locked against the underlying JSON artifacts via `scripts/_gpt/check_locked_numbers.py`. The live package includes the compiled manuscript PDFs, source-data archive, code snapshot, figure-generation inputs, and a Zenodo-ready reproducibility bundle. Training and evaluation scripts record the experiment identity, checkpoint path, Monte Carlo protocol, and device settings used for each reported result. Hardware/software versions and hyperparameter details are documented in the manuscript and supplementary materials; the remaining user-owned fields are corresponding-author metadata and funding acknowledgements.
