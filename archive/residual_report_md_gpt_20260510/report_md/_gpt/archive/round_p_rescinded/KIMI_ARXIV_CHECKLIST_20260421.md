<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# ArXiv Preprint Formatting & Posting Checklist

> **Task:** K-X21 — Post the NC manuscript to arXiv.
> **Manuscript:** *Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision*
> **Author:** Songqiao Li
> **Date:** 2026-04-21

---

## 1. Pre-formatting (TeX → arXiv-ready)

The goal is a single self-contained `.tex` source tree that compiles with arXiv’s AutoTeX (TeX Live 2023+).

1. **Create a clean staging directory** (`arxiv_submission_YYYYMMMDD/`).
2. **Copy the main manuscript** (`paper/latex_gpt/main.tex`) into the staging directory as `main.tex`.
3. **Flatten includes:** Replace all `\input{sections/XX_...}` directives with the literal content of each section file, concatenated in order:
   - `00_abstract`
   - `01_introduction`
   - `02_related_work`
   - `05_results`
   - `06_discussion`
   - `03_methodology`
   - `04_experimental_setup`
   - `07_conclusion`
4. **Remove cover letter:** Do **not** include `cover_letter.tex` or `cover_letter_v3.tex`.
5. **Inline the `.bbl`:**
   - Delete the `\bibliography{refs_gpt}` and `\bibliographystyle{unsrtnat}` lines.
   - Paste the **entire** contents of `paper/latex_gpt/main.bbl` at the end of the document, just before `\end{document}`.
   - Verify that `main.bbl` contains all cited entries (check against the in-text `\citep`/\citet` calls).
6. **Convert supplementary material to appendix:**
   - Append the contents of `paper/latex_gpt/supplementary.tex` (or `supplementary_main.tex`) after the bibliography as an `\appendix` block.
   - Re-label appendix figures/tables with standard arXiv conventions (A, B, C…) or keep the `S*` prefix if already cross-referenced in the main text.
7. **Audit packages for arXiv compatibility:**
   - Remove non-standard packages not in TeX Live 2023 (e.g., custom university thesis styles).
   - Ensure `hyperref`, `graphicx`, `amsmath`, `booktabs`, `natbib` (or inline bbl), `microtype`, `tikz`, `subcaption`, `caption`, `enumitem`, `placeins` are used — these are all standard.
   - If using `cleveref`, keep it; arXiv supports it.
8. **Figure cleanup:**
   - Ensure all figures referenced by `\includegraphics` exist in the staging `figures/` subdirectory.
   - arXiv accepts `.pdf`, `.png`, `.jpg`, `.eps`. Prefer `.pdf` for vector graphics and `.png` for raster images.
   - Remove unused large raster files (e.g., `figA.png` through `figD.png` if not referenced) to keep the tarball under 10 MB.
9. **Comment removal:** Strip all `% TODO`, `% FIXME`, or developer comments that should not appear in the public source.
10. **Local compile test:** Run `pdflatex main.tex` (or `tectonic main.tex`) **three times** and verify:
    - No missing references (`?`).
    - No overfull `\hbox` warnings in the bibliography.
    - All figures render.
    - PDF is under 25 MB.

---

## 2. File Manifest

Upload exactly these files via the arXiv web uploader or tarball (`tar czvf submission.tar.gz …`).

| File / Dir | Purpose | Notes |
|------------|---------|-------|
| `main.tex` | Master source | Flattened, no external `\input` dependencies |
| `main.bbl` *(inlined)* | Bibliography | Already pasted into `main.tex`; do **not** upload separately if inlined |
| `figures/` | Figure assets | Only referenced figures; prefer PDF > PNG |
| `*.sty` | Custom style files | Only if absolutely required; otherwise omit |
| `arxiv_metadata.txt` *(optional)* | Draft metadata | Not uploaded; use for copy-paste into web form |
| **Do NOT upload** | | |
| `cover_letter*.tex` | Editorial correspondence | arXiv is not a journal submission portal |
| `refs_gpt.bib` | Raw BibTeX | arXiv will not process `.bib`; `.bbl` must be inlined |
| `*.aux`, `*.log`, `*.out` | Build artifacts | AutoTeX regenerates these |
| `README.md`, build scripts | Ancillary | Only if you intend an `anc/` directory |

11. **Create the tarball:**
    ```bash
    tar czvf arxiv_submission_20260421.tar.gz \
      main.tex figures/ --exclude="*.aux" --exclude="*.log"
    ```
12. **Verify tarball contents:**
    ```bash
    tar tzvf arxiv_submission_20260421.tar.gz | less
    ```
    Ensure no hidden system files (`.DS_Store`, `._*`) are included.

---

## 3. Metadata

Copy-paste the following into the arXiv submission form. Field limits: Title ≤ 300 chars, Abstract ≤ 1,920 chars.

13. **Title:**
    ```
    Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision
    ```
14. **Authors:**
    ```
    Songqiao Li
    ```
    *(If co-authors are added later, they must be included at initial submission; arXiv does not allow author additions after announcement without a new version.)*
15. **Abstract:** *(Use the exact abstract from `00_abstract.tex`, lightly proofread for TeX escapes.)*
    ```
    We present a behavioral simulation framework for organic optoelectronic inference mapping literature metrics to task-level accuracy. Across three datasets, ADC resolution dominates under the canonical regime: below 6 bits causes abrupt collapse, while above 6 bits device-to-device variability becomes binding. Standard hardware-aware training overfits a single fixed mismatch and collapses to 10.00% on fresh hardware, whereas Ensemble HAT---resampling mismatch masks each epoch---recovers 86.37+/-1.54%. A literature-anchored OPECT case study reaches 88.53+/-0.08% zero-shot transfer. Under severe nonlinear write (NL=2.0), we systematically test and falsify three candidate mitigation strategies, including joint training, which remains pinned at ~30% fresh-instance accuracy. Our findings establish a ~30% fresh-instance ceiling under severe nonlinearity, indicating that first-order behavioral surrogates impose a structural generalization barrier in the attention pathway.
    ```
    > **Note:** Replace `+/-` with `±` (Unicode) or keep ASCII `+/-`; arXiv accepts both but Unicode renders cleaner. Replace em-dashes `---` with plain double-hyphens `--` or leave as LaTeX source if the abstract field is raw text.
16. **Keywords / Comments:**
    - **Comments:** *(optional but recommended)*
      ```
      12 pages, 11 figures, 3 tables. Supplementary material included as appendix.
      ```
    - **Report number:** *(if applicable)* Leave blank unless your institution assigns one.
17. **ACM class / MSC class:** Leave blank (optional for cs.LG).
18. **Journal reference:** Leave blank for preprint; fill in only after formal publication.

---

## 4. License

19. **Select the arXiv license** on the submission form:
    - **Recommended:** *"arXiv.org perpetual, non-exclusive license to distribute this article"* (standard arXiv license).
    - This license is **non-exclusive**, **perpetual**, and **irrevocable**. It grants arXiv the right to host and distribute the work indefinitely. You retain full copyright and may publish the same work in a journal (Nature Communications) without conflict.
20. **Do NOT select** the CC0 (public domain dedication) unless explicitly required by your institution.
21. **If submitting a preprint of a work later published in NC:** The standard arXiv license is fully compatible with Nature’s preprint policy. No additional steps are required.

---

## 5. Primary Category

22. **Primary category:** `cs.LG` (Machine Learning)
    - Justification: Core contribution is a learning-system methodology (Ensemble HAT, profile-driven simulation, generalization analysis) evaluated on vision benchmarks.

---

## 6. Secondary Categories (Cross-listing)

23. **Select cross-listings:**
    - `cs.AR` — Hardware Architecture
      *(Justification: organic optoelectronic CIM, ADC-resolution trade-offs, mixed-signal inference mapping)*
    - `eess.SP` — Signal Processing
      *(Justification: noise modeling, SNR analysis, device variability as a signal-degradation problem)*
24. **Optional additional cross-listings to consider:**
    - `cs.CV` — Computer Vision and Pattern Recognition
      *(if you want stronger visibility in the vision community; justified by ViT experiments on CIFAR / Tiny-ImageNet)*
    - `cs.ET` — Emerging Technologies
      *(if available; organic electronics is an emerging substrate)*
25. **Limit:** arXiv allows up to 6 secondary categories; stay focused. `cs.LG` + `cs.AR` + `eess.SP` is the minimal correct set.

---

## 7. Post-submission Workflow

26. **Upload & process:**
    - Upload the tarball via the **Submit** form.
    - Click **Process files**. AutoTeX compiles the source.
    - Review the generated PDF preview. If compilation fails, fix the error, re-upload, and re-process.
27. **Metadata verification:**
    - Double-check title, author order, abstract, and categories on the preview page.
    - Verify that the PDF metadata (title/author) is populated correctly (check `Document Properties` in your PDF reader).
28. **Moderation queue:**
    - After submission, the paper enters the **moderation queue** for the primary category (`cs.LG`).
    - Typical turnaround: **24–72 hours** (can be faster on weekdays).
    - Moderators check for basic scope fit and policy compliance; this is **not** peer review.
29. **Announcement schedule:**
    - Once moderated, the paper is **announced** at the next daily mailing (usually ~20:00 UTC).
    - You will receive an email with the **arXiv identifier** (e.g., `arXiv:2604.01234`).
30. **Post-announcement actions:**
    - Update your CV, website, and any grant reports with the arXiv ID.
    - Share the link on social media / academic networks.
    - If submitting to NC simultaneously or subsequently, cite the arXiv ID in the cover letter as a preprint reference.

---

## 8. Versioning (NC Revision Updates)

arXiv uses a simple version numbering scheme (`v1`, `v2`, `v3`, …). Each version is immutable once announced.

31. **When to create a new version:**
    - After receiving the NC decision (accept / minor revision / major revision).
    - To fix typos, update figures, or add acknowledgements post-acceptance.
    - **Not** for trivial punctuation fixes unless they materially affect correctness.
32. **Versioning steps:**
    1. Log in to arXiv → **My Articles** → select the paper.
    2. Click **Add a new version**.
    3. Upload the revised source tarball (follow Sections 1–2 above).
    4. Update the **Comments** field to reflect changes, e.g.:
       ```
       v2: Revised for Nature Communications. Added Section X, updated Figure 4.
       ```
    5. Submit. The new version enters moderation again (usually faster for updates).
33. **Preserving old versions:**
    - All prior versions remain publicly accessible at `https://arxiv.org/abs/XXXX.XXXXXvN`.
    - The default landing page always redirects to the **latest** version.
34. **Post-acceptance finalization:**
    - Once the NC DOI is assigned, submit a final arXiv version.
    - Add the **Journal reference** field:
      ```
      Nature Communications, Vol. X, Article YYYY (2026).
      ```
    - Add the **DOI** field.
35. **No retractions for routine updates:** Use the versioning system; retractions are reserved for serious issues (plagiarism, errors that invalidate conclusions).

---

## Quick-Reference Summary

| Step | Action | Owner | Status |
|------|--------|-------|--------|
| 1–2 | Flatten `main.tex`, inline `.bbl` | — | ☐ |
| 3 | Append supplementary as appendix | — | ☐ |
| 4 | Strip cover letter & comments | — | ☐ |
| 5 | Local compile test (3×) | — | ☐ |
| 6 | Build tarball, verify manifest | — | ☐ |
| 7 | Fill arXiv metadata form | — | ☐ |
| 8 | Choose license (standard) | — | ☐ |
| 9 | Set `cs.LG` primary + `cs.AR`, `eess.SP` secondaries | — | ☐ |
| 10 | Upload, process, verify PDF preview | — | ☐ |
| 11 | Submit → moderation → announcement | — | ☐ |
| 12 | Post-announcement sharing & citation | — | ☐ |

---

*End of checklist.*
