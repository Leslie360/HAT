# Bib Tail Fixes — 2026-04-18

**Scope:** Three entries flagged as weak in `KIMI_DISPATCH_20260418_related_work_finish_gpt.md`.

---

## 1. `wei2020voltagedifferential` → FIXED ✅

**Current `refs_gpt.bib` entry:**
```bibtex
@inproceedings{wei2020voltagedifferential,
  author    = {Wan, W. and Kubendran, R. and Gao, B. and Joshi, S. and Raina, P. and Wu, H. and Cauwenberghs, G. and Wong, H.-S. P.},
  title     = {A Voltage-Mode Sensing Scheme with Differential-Row Weight Mapping for Energy-Efficient {RRAM}-Based In-Memory Computing},
  booktitle = {2020 IEEE Symposium on {VLSI} Technology},
  pages     = {1--2},
  year      = {2020},
  doi       = {10.1109/VLSITechnology18217.2020.9265066},
  url       = {https://doi.org/10.1109/VLSITechnology18217.2020.9265066}
}
```

**Verification:**
- DOI `10.1109/VLSITechnology18217.2020.9265066` resolves to IEEE VLSI Technology 2020.
- Title matches: "A Voltage-Mode Sensing Scheme with Differential-Row Weight Mapping for Energy-Efficient RRAM-Based In-Memory Computing"
- Authors match published author list (Wan et al.).
- **Note:** The citation key `wei2020voltagedifferential` is slightly mismatched with the first author "Wan", but this is a legacy key. No functional issue; BibTeX resolves by key, not by author surname.

**Verdict:** No action needed. Entry is clean.

---

## 2. `joshi2020accurate` → FIXED ✅

**Current `refs_gpt.bib` entry:**
```bibtex
@article{joshi2020accurate,
  author  = {Vinay Joshi and Manuel Le Gallo and Simon Haefeli and Irem Boybat and S. R. Nandakumar and Christophe Piveteau and Martino Dazzi and Bipin Rajendran and Abu Sebastian and Evangelos Eleftheriou},
  title   = {Accurate Deep Neural Network Inference Using Computational Phase-Change Memory},
  journal = {Nature Communications},
  volume  = {11},
  pages   = {2473},
  year    = {2020},
  doi     = {10.1038/s41467-020-16108-9},
  url     = {https://doi.org/10.1038/s41467-020-16108-9}
}
```

**Verification:**
- DOI `10.1038/s41467-020-16108-9` resolves to Nature Communications 11, 2473 (2020).
- Title exact match.
- Author list exact match with published article (10 authors).
- **Note:** `bibliography_structured.csv` abbreviates as "V. Joshi et al."; the full author list in `.bib` is preferable for BibTeX processing.

**Verdict:** No action needed. Entry is clean.

---

## 3. `choi2019pact` → KEY/YEAR MISMATCH ⚠️

**Current `refs_gpt.bib` entry:**
```bibtex
@inproceedings{choi2019pact,
  author  = {Jungwook Choi and Zhuo Wang and Swagath Venkataramani and Pierce I-Jen Chuang and Vijayalakshmi Srinivasan and Kailash Gopalakrishnan},
  title   = {{PACT}: Parameterized Clipping Activation for Quantized Neural Networks},
  booktitle = {Proceedings of the 35th International Conference on Machine Learning},
  series    = {Proceedings of Machine Learning Research},
  volume    = {80},
  pages     = {1028--1037},
  year    = {2018},
  url     = {http://proceedings.mlr.press/v80/choi18a.html}
}
```

**Verification:**
- PACT was presented at ICML 2018 (Stockholm), PMLR vol. 80.
- The arXiv preprint is `arXiv:1805.06085` (May 2018).
- URL `http://proceedings.mlr.press/v80/choi18a.html` is valid.
- **Problem:** The citation key is `choi2019pact` but `year = 2018`. `bibliography_structured.csv` uses key `choi2018pact` (year-correct).

**Impact:** The key/year mismatch is cosmetic—BibTeX compiles correctly because the key is just a label. However, it may confuse readers who search the `.bib` file by year pattern.

**Recommended action:**
- **Option A (preferred):** Rename key to `choi2018pact` and update all `\citep{choi2019pact}` → `\citep{choi2018pact}` across `.tex` files. Clean but touches multiple files.
- **Option B:** Leave as-is; add a comment in `.bib` noting the key is legacy. Minimal churn.

**Given current manuscript freeze for submission:** Option B is safer unless the user explicitly wants a global key rename.

---

## Summary

| Entry | Status | Action |
|-------|--------|--------|
| `wei2020voltagedifferential` | ✅ Clean | None |
| `joshi2020accurate` | ✅ Clean | None |
| `choi2019pact` | ⚠️ Key/year mismatch (2018 paper, 2019 key) | Optional: rename to `choi2018pact` globally, or leave legacy |
