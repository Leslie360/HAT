# R10I — Scenarios Reframing Change Log

**Date:** 2026-04-25  
**Mission:** Replace misleading "three independent scenarios" framing with honest language that correctly distinguishes canonical evaluation + zero-shot transfer (same training) from severe-NL retraining (independent training arm).

---

## Files Edited

### 1. `compute_vit/paper/latex_gpt/cover_letter.tex` (line 28)

**OLD:**
```latex
The framework is validated across three scenario pillars: (i) canonical uniform noise (10\% D2D, 5\% C2C, $NL=1.0$), where Ensemble HAT recovers 86.37$\pm$1.54\%; (ii) a literature-anchored OPECT organic-phototransistor proxy ($\sigma_{\mathrm{D2D}}=3\%$, $\sigma_{\mathrm{C2C}}=2\%$), where zero-shot transfer reaches 88.53$\pm$0.08\% without retraining; and (iii) severe nonlinear write ($NL=2.0$), where hardware-aware training with a revised gradient-scaling recipe recovers to the $\sim$80--82\% band.
```

**NEW:**
```latex
The framework is demonstrated under canonical evaluation, literature-anchored zero-shot transfer, and severe-NL stress: (i) canonical uniform noise (10\% D2D, 5\% C2C, $NL=1.0$), where Ensemble HAT recovers 86.37$\pm$1.54\%; (ii) a literature-anchored OPECT organic-phototransistor proxy ($\sigma_{\mathrm{D2D}}=3\%$, $\sigma_{\mathrm{C2C}}=2\%$), where zero-shot transfer reaches 88.53$\pm$0.08\% without retraining; and (iii) severe nonlinear write ($NL=2.0$), where hardware-aware training with a revised gradient-scaling recipe recovers to the $\sim$80--82\% band.
```

**Rationale:** "Validated across three scenario pillars" falsely implies three independent trainings/validations. The new wording (Option B) states the three pieces of evidence honestly without implying independence: (i) and (ii) are two evaluations of the same canonical training, while (iii) is a separate severe-NL retraining arm. All numerical claims (86.37 / 88.53 / 80--82) are preserved.

---

### 2. `compute_vit/paper/latex_gpt/sections/06_discussion.tex` (line 21)

**OLD:**
```latex
\subsection{Treatment: Ensemble HAT mitigation across scenarios}
```

**NEW:**
```latex
\subsection{Treatment: Ensemble HAT mitigation under varied evaluation conditions}
```

**Rationale:** The title "across scenarios" is semantically adjacent to the problematic framing and could be read as implicitly endorsing the "three independent scenarios" narrative. "Under varied evaluation conditions" is more precise and avoids that implication while keeping the subsection scope intact.

---

## Files Scanned but Unchanged

| File | Finding |
|------|---------|
| `sections/00_abstract.tex` | No "three scenario" or related framing language found. Abstract already presents the evidence honestly without independence claims. |
| `sections/01_introduction.tex` | No target phrases found. Para 6 (contributions) frames literature-profile substitution and severe-NL as "two frequently qualitative concerns," which is accurate. |

---

## Constraints Checklist

- [x] Did NOT delete the three pieces of evidence  
- [x] Did NOT change numerical claims (86.37 / 88.53 / 80--82 preserved)  
- [x] ONLY changed framing language  
- [x] Used Option B for compactness as instructed  

## Notes

- A draft file `cover_letter_v6.tex.kimi_draft_v3` contains the same old phrasing but was **not** edited because it is an archived draft, not an active manuscript file.
- No other `.tex` files in the `latex_gpt` tree contain the target phrases.
