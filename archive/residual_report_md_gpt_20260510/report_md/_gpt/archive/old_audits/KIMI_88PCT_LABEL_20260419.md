# 88.41% Training-Ablation Label — Draft Options

**Date:** 2026-04-19
**Source:** `JSON_INVESTIGATION_20260419.md` §2, `FINAL_CONTENT_REVIEW_20260419.md` §M2
**Task:** Explicitly label the 88.41% cadence-scan value as a **50-epoch training ablation**, not an evaluation of the canonical 100-epoch ensemble checkpoint (locked number: 86.37 ± 1.54%).

---

## Status Check

A grep of `paper/latex_gpt/sections/*.tex` for `88.41` **returns no matches** as of this writing. The cadence-scan paragraph has not yet been landed in `05_results.tex`.
The intended sentence (per `CODEX_DISPATCH_20260416_tex_gpt.md` and `FINAL_CONTENT_REVIEW_20260419.md`) is:

> **Current intended text:**
> ```latex
> An exploratory single-run cadence scan (Supplementary Fig.~\SuppFigZeroShot) shows epoch-level resampling reaches 88.41\%, versus 87.18\% (fixed) and 86.16\% (per-batch).
> ```
> *(Alternative longer variant in dispatch: adds 87.76% and 87.31% cadences; same issue applies.)*

The supplementary figure caption already notes this is a **"50-epoch scan"** and that the panel is **"intended to show that cadence matters, rather than to serve as the final paper-locked estimate."** The main text lacks that qualifier.

---

## Option A: Footnote on first mention of 88.41%

**Revision:**
```latex
An exploratory single-run cadence scan (Supplementary Fig.~\SuppFigZeroShot) shows epoch-level resampling reaches 88.41\%\footnote{50-epoch training ablation; not directly comparable to the 100-epoch canonical ensemble checkpoint.}, versus 87.18\% (fixed) and 86.16\% (per-batch).
```

| Pros | Cons |
|:--|:--|
| Keeps sentence flow intact. | Adds a footnote to a sentence that already has a parenthetical; slightly cluttered. |
| Reader who cares can check the footnote; casual reader is not interrupted. | Footnote text is longish; may wrap on narrow columns. |
| Most "Nature-style" way to flag a protocol caveat. | |

---

## Option B: Parenthetical in the same sentence

**Revision:**
```latex
An exploratory single-run cadence scan (Supplementary Fig.~\SuppFigZeroShot) shows epoch-level resampling reaches 88.41\% (50-epoch training ablation), versus 87.18\% (fixed) and 86.16\% (per-batch).
```

| Pros | Cons |
|:--|:--|
| Zero vertical space cost. | Four parentheticals in one sentence makes it dense. |
| Explicit and impossible to miss. | Slightly breaks reading rhythm. |
| Fastest to implement; no footnote numbering needed. | |

---

## Option C: Add one clause in the next sentence

**Revision:**
```latex
An exploratory single-run cadence scan (Supplementary Fig.~\SuppFigZeroShot) shows epoch-level resampling reaches 88.41\%, versus 87.18\% (fixed) and 86.16\% (per-batch). These values were obtained from separate 50-epoch training ablations and are therefore not directly comparable to the 100-epoch ensemble-HAT checkpoint evaluation.
```

| Pros | Cons |
|:--|:--|
| Cleanest sentence structure; no inline parenthetical overload. | Adds an extra sentence that partly repeats the supplementary caption. |
| Explicitly states the incomparability, which is the key scientific point. | Slightly more verbose than a one-line fix. |
| Works well if the dispatch variant with five cadences is used (more numbers = more need for a disclaimer sentence). | |

---

## Recommendation

**Use Option B (parenthetical) if the sentence stays short** (three cadences only). It is the most minimal change, costs nothing in layout, and satisfies the audit requirement in a single breath.

**Use Option A (footnote) if the sentence uses the longer dispatch variant** (five cadences: 88.41, 87.76, 87.31, 87.18, 86.16). With that many numbers already inline, a footnote keeps the main clause readable while still making the caveat discoverable.

**Avoid Option C** unless the paragraph is already being rewritten for other reasons; it is overkill for a one-line fix.

---

*Rationale:* The core risk identified in `JSON_INVESTIGATION_20260419.md` is that readers may compare 88.41% to 86.37 ± 1.54% as if they were the same experiment. Any of the three options above breaks that implicit comparison. The footnote (A) is the most formally correct for a scientific manuscript; the parenthetical (B) is the most pragmatic for a late-stage edit.
