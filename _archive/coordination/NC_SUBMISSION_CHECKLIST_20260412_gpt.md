# Nature Communications Submission Checklist (Codex, 2026-04-12)

> Source: `report_md/How to submit _ Nature Communications.pdf` + current manuscript/package state.

## Official requirements distilled

1. Online submission package should include:
   - cover letter
   - manuscript text file
   - figure files
   - optional Supplementary Information file
2. First submission may use a single manuscript PDF/LaTeX file with figures embedded, up to **30 MB**.
3. Supplementary Information should be uploaded separately.
4. Custom code central to the main claims must be available to **editors and reviewers at submission**.
5. Related or overlapping manuscripts must be disclosed if relevant.
6. Permissions are required for personal communications, if any.
7. Source data for graphs/charts may be requested and should be ready in spreadsheet or zipped form.

## Current package status

| Item | Current state | Status | Notes |
|:--|:--|:--:|:--|
| Main manuscript PDF | `paper/latex_gpt/main.pdf` = 4.8 MB, 16 pages | ✅ | Well below 30 MB |
| Supplementary PDF | `paper/latex_gpt/supplementary_main.pdf` = 9.1 MB, 13 pages | ✅ | Separate file ready |
| Cover letter | `paper/latex_gpt/cover_letter.pdf` = 63 KB, 2 pages | ✅ | Ready |
| Manuscript compile state | clean compile, no undefined refs/citations | ✅ | Verified locally |
| Reviewer-accessible code archive | wording updated in manuscript and cover letter | 🔄 | Still needs actual private link/archive at submission |
| Source-data package | wording updated in manuscript and cover letter | 🔄 | Should still be assembled as reviewer-facing spreadsheet/zip |
| Related-manuscript disclosure | no overlap currently stated | 🔄 | Manual author confirmation required in submission form |
| Reviewer suggestions/exclusions | cover letter points to submission system | 🔄 | Manual submission-form step |
| Author affiliations / metadata | manuscript front matter exists, but submission-system metadata must still be checked | 🔄 | Manual submission-form step |

## Concrete closeout actions

### Must do before pressing submit

- Generate a reviewer-accessible code package or private repository link matching the submitted manuscript.
- Assemble source-data tables for all plotted figures and summary tables into a single spreadsheet or zipped folder.
- Confirm no overlapping manuscript needs disclosure.
- Fill author affiliations, current addresses, and reviewer suggestions/exclusions in the submission system.

### Already satisfied

- Main manuscript and supplementary are separate, upload-ready PDFs.
- Combined file sizes are comfortably within NC first-submission limits.
- Cover letter exists and now aligns with reviewer-accessible code wording.
- Manuscript text already contains `Data Availability`, `Code Availability`, `Competing Interests`, and `Author Contributions`.

## Recommended division of labor

- **Codex:** manuscript/package truth maintenance, compile checks, final submission hygiene.
- **Kimi:** submission-form checklist audit, release bundle audit, rebuttal/cover-letter stress test.
- **Gemini:** NC-style compression, caption coherence, bibliography integrity, submission wording polish.
