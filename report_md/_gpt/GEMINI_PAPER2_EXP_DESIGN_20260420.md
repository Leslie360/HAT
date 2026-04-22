# G-GG6: Paper-2 Experimental Design
**Date**: 2026-04-20

## Proposed Experiments (Anchor Set)
1. **QKV vs MLP Isolation**: Train models with varying degrees of protected linear execution (CX-J1b/c).
2. **Surrogate Fidelity Sweep**: Compare 1st, 2nd, and 3rd order NL surrogates (CX-J1d extension).
3. **Softmax Temperature Scaling**: Test if artificially lowering the softmax temperature recovers robustness by smoothing the exponential amplification of analog noise.
4. **Attention Head Specialization**: Analyze if certain heads (e.g., local vs global) collapse faster under NL.
