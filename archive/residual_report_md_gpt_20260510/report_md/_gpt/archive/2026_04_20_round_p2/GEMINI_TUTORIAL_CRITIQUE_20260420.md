# G-GG16: Pedagogical Critique of K-Y17
**Date**: 2026-04-20

## Critique
The tutorial notebook currently focuses too much on *how* to run the code, and not enough on *why* the failure happens.
**Recommendation**: Add a specific cell that extracts the pre-softmax logits from a clean model vs. an NL=2.0 model, and plots the histograms side-by-side. Showing the user visually how the logits get crushed by NL makes the "structural limit" concept instantly intuitive.
