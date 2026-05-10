# User Metadata Request Form
## Nature Communications Submission — 2026-04-20

> **Purpose:** This one-page form collects the final pieces of author-side metadata required for submission. Once completed, Kimi/Codex will insert these values into the LaTeX source, recompile the manuscript, and run the final locked-numbers guard.
>
> **How to use:** Replace the placeholder text or `[...]` brackets with your information, then return this file.

---

## Corresponding Author Information

### 1. Corresponding Author Full Name *(REQUIRED)*
```
[First Name] [Middle Initial(s)] [Last Name]
```
*Example:* `Wei Zhang`

---

### 2. Corresponding Author Email *(REQUIRED)*
> **Note:** Please use an institutional email address (e.g., `@university.edu`, `@institute.ac.cn`) rather than a personal email provider (Gmail, Yahoo, etc.) if possible. Nature Communications and many journals prefer institutional addresses for verification.

```
[corresponding.author@institution.edu]
```
*Example:* `wei.zhang@mit.edu`

---

### 3. Corresponding Author Affiliation *(REQUIRED)*
> **Format:** Department + University/Institute + City + Country (as it should appear on the manuscript title page).

```
[Department of X], [University/Institute Name], [City], [Postal Code], [Country]
```
*Example:* `Department of Electrical Engineering and Computer Science, Massachusetts Institute of Technology, Cambridge, MA 02139, USA`

---

## Manuscript Metadata

### 4. Acknowledgements Text *(REQUIRED)*
> **What to include:** Funding sources (with full grant numbers), equipment support, computing resources, fellowships, or any other acknowledgements required by your funders/institution.
>
> **Tip:** Check your grant agreements for exact wording requirements (e.g., "This work was supported by..." vs. "W.Z. acknowledges support from...").

```
[Replace this block with your acknowledgements text.]
```
*Example:*
```
This work was supported by the National Science Foundation under Grant No. ECCS-1234567
and the Office of Naval Research under Grant No. N00014-23-1-XXXX. W.Z. acknowledges
support from the MIT Presidential Fellowship. The authors thank the MIT.nano facilities
for device fabrication support.
```

---

## Reviewer Information

### 5. Suggested Reviewers *(REQUIRED: 3–5 reviewers)*
> For each suggested reviewer, please provide:
> - **Full Name**
> - **Affiliation**
> - **Email address**
> - **Area of expertise** (2–3 keywords)
> - **Why suitable & non-conflicting:** Briefly explain why this person is well-qualified to review this work and why there is no conflict of interest (no recent co-authorship, no advisor/advisee relationship, no direct competition, no financial interest, etc.).

#### Reviewer 1
```
Name:          [Full Name]
Affiliation:   [University/Institute, Department]
Email:         [reviewer1@institution.edu]
Expertise:     [e.g., neuromorphic computing, analog AI accelerators, memristive devices]
Why suitable:  [e.g., Leading expert in compute-in-memory architectures; no overlap in
               co-authorship or funding in the past 4 years.]
```

#### Reviewer 2
```
Name:          [Full Name]
Affiliation:   [University/Institute, Department]
Email:         [reviewer2@institution.edu]
Expertise:     [e.g., optical neural networks, silicon photonics, AI hardware]
Why suitable:  [e.g., Pioneered optical MAC arrays; no personal or professional conflict
               with any author.]
```

#### Reviewer 3
```
Name:          [Full Name]
Affiliation:   [University/Institute, Department]
Email:         [reviewer3@institution.edu]
Expertise:     [e.g., vision transformers, efficient deep learning, edge AI]
Why suitable:  [e.g., Published extensively on ViT compression and hardware-software
               co-design; no shared projects or funding.]
```

#### Reviewer 4 *(optional, but recommended if available)*
```
Name:          [Full Name]
Affiliation:   [University/Institute, Department]
Email:         [reviewer4@institution.edu]
Expertise:     [keywords]
Why suitable:  [conflict-free rationale]
```

#### Reviewer 5 *(optional)*
```
Name:          [Full Name]
Affiliation:   [University/Institute, Department]
Email:         [reviewer5@institution.edu]
Expertise:     [keywords]
Why suitable:  [conflict-free rationale]
```

---

### 6. Excluded Reviewers *(OPTIONAL)*
> List any individuals who should **not** be asked to review this manuscript due to a conflict of interest. For each, provide the name and a brief reason for exclusion.

```
Name:   [Full Name]
Reason: [e.g., Recent co-author on related work published 2024; advisor of co-author X.]
```

```
Name:   [Full Name]
Reason: [e.g., Direct financial interest in competing technology; ongoing grant collaboration.]
```

*(Add more entries as needed, or delete this section if none apply.)*

---

## What Happens After You Fill This In

Once you return this completed form, the automated pipeline will execute the following steps:

1. **Metadata Injection** — Kimi/Codex will parse this form and insert the corresponding values into the manuscript LaTeX source (e.g., `\author`, `\email`, `\affiliation`, `\acknowledgements`, and the cover letter / submission system notes).

2. **Recompilation** — The LaTeX source will be recompiled to produce an updated PDF with all metadata correctly rendered.

3. **Bundle Refresh** — The submission bundle (manuscript PDF, source files, figures, supplementary materials, etc.) will be refreshed to reflect the updated source.

4. **Locked-Numbers Guard (Final Run)** — The pipeline will run the locked-numbers guard one final time to ensure that no numerical values, citations, or cross-references were inadvertently altered during the metadata injection process.

5. **Ready for Submission** — If all checks pass, the bundle will be marked as submission-ready.

> **Expected turnaround:** Automated steps 1–4 typically complete within a few minutes after the form is returned.

---

*Form compiled: 2026-04-20*
