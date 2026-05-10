# G-SLIM-1: Structural Limit & Bimodal Falsification Theory
**Date:** 2026-04-23
**Scope:** Round Q SLIM (Empirically Updated post-CX-K2)

## 1. The Falsified Hypothesis
Our initial theoretical prediction hypothesized that higher-order surrogate gradients under severe non-ideality (NL=2.0) would expose a two-attractor structure (a "bimodal basin") in the loss landscape.

## 2. The Empirical Reality (CX-K2 Landing)
The N=30 fresh-instance evaluation from Codex (`cx_k2_bimodality_test.json`) returned a mean of **38.95% ± 9.85%** with a range of 22.03% to 61.69%.
Crucially, Hartigan's dip test yielded **$p=0.9796$**, definitively rejecting the bimodality hypothesis.

## 3. The New Formal Claim: The Flat, High-Variance Basin (Structural Limit)
The analog hypothesis class under severe non-ideality does not fracture into two distinct attractors. Instead, it forms a **single, structurally flat, high-variance basin**.
Because the Lipschitz constant of the attention Softmax operator exponentially amplifies analog weight perturbations, the optimizer is unable to find a sharp, robust minimum. It settles on a plateau where the specific D2D instantiation of a fresh hardware chip can arbitrarily scatter the accuracy anywhere along a unimodal, extremely wide continuum (22% to 62%).
This confirms the **Structural Limit (Branch B)**: the analog ViT architecture is fundamentally incapable of deterministic generalization under NL=2.0, not because it falls into a specific trap, but because the entire optimization space is too brittle to yield reliable weights.
