# Consolidated User Decision & Metadata Request
## Nature Communications Submission — Round M (2026-04-20)

> **Purpose:** This form consolidates all remaining user decisions into a single ask. Your responses will unblock both the final Nature Communications submission bundle and the next phase of experimental work (Round N).
>
> **How to use:** Please fill out the brackets `[...]` and return this file.

---

## PART 1: Manuscript Metadata (Required for Submission)

### 1.1 Corresponding Author Information
- **Full Name:** `[First Name Middle Initial Last Name]`
- **Email:** `[institutional_email@domain.edu]`
- **Affiliation:** `[Department, University/Institute, City, Postal Code, Country]`

### 1.2 Acknowledgements Text
> Please provide funding sources (with grant numbers), equipment support, and computing resources.
```
[Replace this block with your acknowledgements text.]
```

### 1.3 CRediT Author Contributions
> Please map author initials to their roles. (e.g., Conceptualization: X.Y., Z.W.)
- **Conceptualization:** `[...]`
- **Methodology:** `[...]`
- **Software:** `[...]`
- **Validation:** `[...]`
- **Formal Analysis:** `[...]`
- **Investigation:** `[...]`
- **Resources:** `[...]`
- **Data Curation:** `[...]`
- **Writing - Original Draft:** `[...]`
- **Writing - Review & Editing:** `[...]`
- **Visualization:** `[...]`
- **Supervision:** `[...]`
- **Project Administration:** `[...]`
- **Funding Acquisition:** `[...]`

---

## PART 2: Submission Logistics

### 2.1 Suggested Reviewers (Need 3-5)
> Based on our analysis, we need experts in:
> 1. Organic-RRAM device physics
> 2. ViT-quantization/Efficient deep learning
> 3. CIM (Compute-in-Memory) hardware-aware-training
> 4. Simulation-framework methodology
> 5. Edge-AI systems

Please provide 3-5 specific names that fit these profiles (ensure no conflicts of interest):
**Reviewer 1:** `[Name, Affiliation, Email, Expertise, Why suitable]`
**Reviewer 2:** `[Name, Affiliation, Email, Expertise, Why suitable]`
**Reviewer 3:** `[Name, Affiliation, Email, Expertise, Why suitable]`
**Reviewer 4 (Opt):** `[Name, Affiliation, Email, Expertise, Why suitable]`
**Reviewer 5 (Opt):** `[Name, Affiliation, Email, Expertise, Why suitable]`

### 2.2 Excluded Reviewers (Optional)
**Excluded 1:** `[Name, Reason]`

---

## PART 3: Code & Data Availability Decisions

### 3.1 GitHub Repository URL
> Provide the intended public GitHub repository URL for the codebase.
- **Repository URL:** `[https://github.com/username/compute_vit]`

### 3.2 Open Source License
> Choose a license for the released code.
- **License Choice (e.g., MIT, Apache-2.0, BSD-3):** `[MIT]`

---

## PART 4: GPU-Window Strategy (Round N Kickoff)

> The main GPU is currently idle. We have two competing priorities for the next training window.
> **Option A:** Joint MLP-Linear + Ensemble HAT pilot (~60 GPU-h). Highest thesis priority.
> **Option B:** ImageNet-100 pilot (~120 GPU-h). Fulfills cover letter promise and defends against reviewer scalability questions.

- **GPU Window Decision (A or B):** `[Option A / Option B]`

---
*Once this form is completed, Claude will trigger the final bundle rebuild and authorize the selected GPU pilot run.*
