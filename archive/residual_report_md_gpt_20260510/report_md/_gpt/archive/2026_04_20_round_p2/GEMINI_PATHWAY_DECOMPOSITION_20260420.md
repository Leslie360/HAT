# G-GG3: Pathway Decomposition Theory
**Date**: 2026-04-20
**Target**: Informs CX-J1b/c

## Analysis: QKV vs MLP
The ViT architecture contains two primary computational pathways mapped to crossbars:
1. **MLP blocks**: Feed-forward, pointwise. Errors are additive and propagate linearly before the GeLU activation.
2. **QKV blocks**: Token-mixing. Errors inside $Q$ and $K$ are multiplied, then exponentiated by the Softmax.
Theoretical prediction: The QKV pathway has an exponentially higher condition number with respect to weight perturbations compared to the MLP pathway. Thus, linearizing QKV (CX-J1b) should yield significantly higher accuracy recovery than linearizing the MLP.
