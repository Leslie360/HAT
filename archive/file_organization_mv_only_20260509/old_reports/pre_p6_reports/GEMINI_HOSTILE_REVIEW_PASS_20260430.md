# Gemini Day 3-4 Tasks: Hostile Review Pass & Wording Verification

## 1. Attack Vectors and Replacement Phrasing

| Vulnerable Wording (Target for Reviewers) | Attack Vector | Safe Replacement Phrasing |
| :--- | :--- | :--- |
| "PCM naturally regularizes training." | **Attack:** "You did not prove physical regularization, you just used an `ADD_NORMAL` modifier in a software simulator." | "Under the tested PCM UnitCell simulation regime, the implicit noise and update characteristics enable 4-bit and 6-bit convergence where pure quantization baselines collapse." |
| "6-bit is universally better than 8-bit." | **Attack:** "Your mean is slightly higher, but the standard deviation overlaps. You cannot claim statistical superiority." | "6-bit is the best tested Pareto midpoint in our PCM UnitCell experiments, maintaining 8-bit-like drift stability with comparable fresh accuracy." |
| "Proportional HAT outperforms digital baselines across architectures." | **Attack:** "Your own ViT seed 456 data shows digital beating proportional HAT. This claim is demonstrably false." | "Remote 105 preliminary results suggest robustness across transformer backbones, pending full multi-seed validation." |
| "The method is tape-out ready." | **Attack:** "You ran simulations with uniform spatial noise. Real chips have IR drop and massive spatial variance." | "The results reveal a precision-retention deployment frontier for the tested PCM simulation regime." |
| "Analog KV-cache solves the memory wall." | **Attack:** "This is unsupported speculation in this paper's context." | *(Delete. 107 is independent Work-2. Mention only briefly as future direction: "Extending the same hardware-aware training principles to memory-bound inference components such as analog KV-cache is an important future direction.")* |
| "Ensemble HAT is universally superior to AIHWKit." | **Attack:** "Your 8-bit AIHWKit baseline reached ~87%, matching Ensemble HAT. It is not universally superior." | "Ensemble HAT rescues the tested 4-bit pure-quantization regime where the AIHWKit IdealDevice baseline collapses." |

## 2. Locked Number Verification

I have audited the canonical numbers against the text:
*   IdealDevice 8-bit (87.28%): **Verified.**
*   IdealDevice 4-bit (14.64%): **Verified.**
*   Ensemble HAT 4-bit (86.16%): **Verified.**
*   PCM UnitCell Precision Ladder (4/6/8-bit): **Verified** against the locked 3-seed means.

The replacement phrasings above avoid the forbidden claims. After Codex's line-level cleanup, the companion Results/SI drafts are acceptable as integration inputs, subject to normal LaTeX editing and final locked-number checks.
