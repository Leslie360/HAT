# G-GG1: Structural-Limit Hypothesis Formal Statement
**Date**: 2026-04-20
**Scope**: Number-agnostic theoretical framing

## Formal Statement
Let the attention matrix be $A = \text{softmax}(Q K^T / \sqrt{d})$. Under ideal conditions, $Q = X W_Q$ and $K = X W_K$. 
Under severe nonlinearity (NL), the effective weights become a function of the input: $\tilde{W}(X)$. 
Because the softmax function amplifies absolute differences exponentially, small input-dependent distortions $\delta(X)$ in the pre-softmax logits induce catastrophic rank-order swapping in the attention probabilities.
This is a structural limit: it is not a failure of the optimizer to find a robust minimum, but rather that the hypothesis class of the analog-mapped attention block under severe NL no longer contains the target function.
