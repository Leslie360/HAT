# Bibliography Last-Pass Audit Report (K-O3)
**Date:** 2026-04-19
**Auditor:** Subagent (Kimi Code CLI)
**Input files:**
- Bib file: `compute_vit/paper/latex_gpt/refs_gpt.bib` *(Note: `main.bib` does not exist at the specified path; the project uses `refs_gpt.bib`.)*
- Tex files: `sections/00_abstract.tex`, `sections/01_introduction.tex`, `sections/06_discussion.tex`

---

## 1. Citation-Frequency Tally
All citations in the three sections are issued with `\citep{...}`; no `\cite` or `\citet` calls were found.

| Rank | Bib key | Count | Selection note |
|------|---------|-------|----------------|
| 1 | `peng2020dnnneurosim` | 2 | Tied for most-cited |
| 2 | `guo2024organic` | 2 | Tied for most-cited |
| 3 | `jung2024organicfilaments` | 2 | Tied for most-cited |
| 4 | `zeng2023organicmemristor` | 2 | Tied for most-cited |
| 5 | `gebregiorgis2023organiccim` | 2 | Tied for most-cited |
| 6 | `zhang2026opect` | 2 | Tied for most-cited |
| 7 | `horowitz2014computing` | 1 | First appearance order (tie-break) |
| 8 | `xu2025emerging` | 1 | Second appearance order (tie-break) |

*All remaining 24 references appear exactly once. The seventh and eighth slots were filled by the first two singletons encountered in reading order.*

---

## 2. Top-8 Reference Audit

### 2.1 `peng2020dnnneurosim`
- **DOI:** `10.1109/TCAD.2020.3043731` — **PASS** (present, well-formed IEEE DOI).
- **Journal:** *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems* — **PASS** (fully spelled out).
- **Year:** `2021` — **PASS** (no explicit year in the `.tex` context; the compiled citation will read 2021, matching the journal publication year).
  *N.B. The bib key contains “2020” (likely reflecting the arXiv preprint year), but the `year` field itself is correct.*
- **Author list:** Xiaochen Peng, Shanshi Huang, Hongwu Jiang, Anni Lu, Shimeng Yu — **PASS** (complete; verified against publisher record).

### 2.2 `guo2024organic`
- **DOI:** `10.1021/acsami.3c19624` — **PASS** (present, well-formed ACS DOI).
- **Journal:** *ACS Applied Materials \& Interfaces* — **PASS** (full official title).
- **Year:** `2024` — **PASS** (no explicit year in the `.tex` context).
- **Author list:** Haotian Guo, Jing Guo, Yujing Wang, Hezhen Wang, Simin Cheng, Zehao Wang, Qian Miao, Xiaomin Xu — **PASS** (complete; verified against PubMed / ACS record).

### 2.3 `jung2024organicfilaments`
- **DOI:** `10.1002/advs.202307494` — **PASS** (present, well-formed Wiley DOI).
- **Journal:** *Advanced Science* — **PASS** (fully spelled out).
- **Year:** `2024` — **PASS** (no explicit year in the `.tex` context).
- **Author list:** Uihoon Jung, Miseong Kim, Jaewon Jang, Jin-Hyuk Bae, In Man Kang, Sin-Hyung Lee — **PASS** (complete; verified against publisher PDF and PubMed record).

### 2.4 `zeng2023organicmemristor`
- **DOI:** `10.3390/nano13050803` — **PASS** (present, well-formed MDPI DOI).
- **Journal:** *Nanomaterials* — **PASS** (fully spelled out).
- **Year:** `2023` — **PASS** (no explicit year in the `.tex` context).
- **Author list:** Jianmin Zeng, Xinhui Chen, Shuzhi Liu, Qilai Chen, Gang Liu — **PASS** (complete; verified against MDPI article page).

### 2.5 `gebregiorgis2023organiccim`
- **DOI:** `10.1109/TED.2023.3327947` — **PASS** (present, well-formed IEEE DOI).
- **Journal:** *IEEE Transactions on Electron Devices* — **PASS** (fully spelled out).
- **Year:** `2023` — **PASS** (no explicit year in the `.tex` context).
- **Author list:** Lan Shen Hu, Marco Fattori, Winston Schilp, Roy Verbeek, Setareh Kazemzadeh, Yoeri van de Burgt, Auke Jisk Kronemeijer, Gerwin Gelinck, Eugenio Cantatore — **PASS** (complete; verified against TU/e repository and IEEE Xplore).

### 2.6 `zhang2026opect`
- **DOI:** `10.1038/s41467-025-66891-6` — **PASS** (present, well-formed Nature DOI).
- **Journal:** *Nature Communications* — **PASS** (fully spelled out).
- **Year:** `2025` — **PASS** (the `.tex` text reads “…a literature-anchored **2025** organic photoelectrochemical transistor (OPECT) case study… \citep{zhang2026opect}”; the rendered year will be 2025, matching the textual context).
  *N.B. The bib key contains “2026”, which is inconsistent with the `year` field. The article’s version-of-record date is January 2026, but the publication/PubMed date is December 2025; the `year = 2025` choice is defensible given the text context.*
- **Author list:** **FAIL** — **INCOMPLETE**.
  - *Current bib entry lists:* Xu Liu, Shilei Dai, Yiyang Jin, Junyao Zhang, Ziyi Guo, Tongrui Sun, Li Li, Pu Guo, Huaiyu Gao, Haixia Liang.
  - *Missing authors (confirmed from Nature Communications author list):* **Shiqi Zhang, Lize Xiong, Yanmin Zhou, Jia Huang**.
  - **Suggested correction:** Append the four missing authors to the `author` field:
    ```bib
    author = {Xu Liu and Shilei Dai and Yiyang Jin and Junyao Zhang and Ziyi Guo and Tongrui Sun and Li Li and Pu Guo and Huaiyu Gao and Haixia Liang and Shiqi Zhang and Lize Xiong and Yanmin Zhou and Jia Huang},
    ```

### 2.7 `horowitz2014computing`
- **DOI:** `10.1109/ISSCC.2014.6757323` — **PASS** (present, well-formed IEEE DOI).
- **Journal/Booktitle:** *IEEE International Solid-State Circuits Conference (ISSCC)* — **PASS** (spelled out with acronym in parentheses, standard for proceedings).
- **Year:** `2014` — **PASS** (no explicit year in the `.tex` context).
- **Author list:** Mark Horowitz — **PASS** (complete; single-author paper).

### 2.8 `xu2025emerging`
- **DOI:** `10.1021/acsami.4c17455` — **PASS** (present, well-formed ACS DOI).
- **Journal:** *ACS Applied Materials \& Interfaces* — **PASS** (full official title).
- **Year:** `2025` — **PASS** (no explicit year in the `.tex` context).
- **Author list:** Yunchao Xu, Yuan He, Dongyong Shan, Biao Zeng, Qian-Xi Ni — **PASS** (complete; verified against ACS / PubMed record).

---

## 3. Spot-Check: Three Less-Cited References

### 3.1 `alibart2016physical` (1 citation)
- **DOI:** `10.1038/srep31932` — **PASS** (present, well-formed Nature DOI).
- **Journal:** *Scientific Reports* — **PASS** (fully spelled out).
- **Year:** `2016` — **PASS** (no explicit year in the `.tex` context).
- **Author list:** Yu-Pu Lin, Christopher H. Bennett, Théo Cabaret, Damir Vodenicarevic, Djaafar Chabi, Damien Querlioz, Bruno Jousselme, Vincent Derycke, Jacques-Olivier Klein — **PASS** (complete; all nine authors listed, no “et al.” in the bib entry).
- **Text–Bib attribution:** **FAIL** — **MISMATCH**.
  The `.tex` text reads: “…the Monte Carlo study of **Alibart \emph{et al.}**, which sampled device parameters for a simple organic-memristive perceptron \citep{alibart2016physical}.”
  The bib entry, however, corresponds to **Lin \emph{et al.}** (2016), not Alibart. There is no author named Alibart in this reference.
  - **Suggested correction:** Verify the intended paper. If the Lin *et al.* supervised-learning demonstrator is meant, update the prose to “Lin *et al.*”; if a 2016 Monte Carlo study by Alibart is intended, replace the bib entry with the correct Alibart reference and update the key name accordingly.

### 3.2 `choi2019pact` (1 citation)
- **DOI:** — **FAIL** — **MISSING**. The entry lacks a `doi` field entirely.
- **Journal/Booktitle:** *Proceedings of the 35th International Conference on Machine Learning* — **PASS** (fully spelled out).
- **Year:** `2018` — **PASS** (no explicit year in the `.tex` context).
  *N.B. The bib key contains “2019”, but the conference year is 2018 (PMLR v80).*
- **Author list:** Jungwook Choi, Zhuo Wang, Swagath Venkataramani, Pierce I-Jen Chuang, Vijayalakshmi Srinivasan, Kailash Gopalakrishnan — **PASS** (complete).
- **Suggested correction:** Add the DOI:
  ```bib
  doi = {10.48550/arXiv.1805.06085},
  ```
  *(The PMLR proceedings volume does not issue a CrossRef DOI; the arXiv DOI `10.48550/arXiv.1805.06085` is the standard fallback used elsewhere in this bib file.)*

### 3.3 `iconniv2025` (1 citation)
- **DOI:** `10.1145/3777381` — **PASS** (present, well-formed ACM DOI).
- **Journal:** *ACM Transactions on Architecture and Code Optimization* — **PASS** (fully spelled out).
- **Year:** `2026` — **PASS** (no explicit year in the `.tex` context).
  *N.B. The bib key contains “2025”, but the `year` field is 2026, matching the ACM citation. The article appears to have been accepted in 2025 with a 2026 volume date.*
- **Author list:** Jinpeng Liu, Wei Tong, Bing Wu, Huan Cheng, Heng Zhou, Xueliang Wei, Dan Feng — **PASS** (complete; verified against ACM Digital Library).

---

## 4. Summary of Action Items

| Priority | Reference | Issue | Recommended Fix |
|----------|-----------|-------|-----------------|
| **High** | `zhang2026opect` | Author list truncated (4 authors missing) | Add Shiqi Zhang, Lize Xiong, Yanmin Zhou, Jia Huang to `author` field. |
| **High** | `alibart2016physical` | Text attributes citation to “Alibart et al.” but bib entry is Lin et al. | Reconcile text and bib: either change prose to “Lin et al.” or swap in the correct Alibart reference. |
| **Medium** | `choi2019pact` | DOI missing | Insert `doi = {10.48550/arXiv.1805.06085},` (or the PMLR DOI if available). |
| **Low** | `peng2020dnnneurosim`, `choi2019pact`, `zhang2026opect`, `iconniv2025` | Bib key year ≠ `year` field | Cosmetic: consider renaming keys for internal consistency (does not affect rendered output). |

---

*End of audit.*
