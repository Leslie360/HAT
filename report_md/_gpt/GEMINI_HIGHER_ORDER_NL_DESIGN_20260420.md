# G-GG2: Higher-Order NL Surrogate Design
**Date**: 2026-04-20
**Target**: Informs CX-J1d

## Design
Current surrogate uses a first-order approximation (gradient scaling). To test if the failure is an artifact of this surrogate, we propose a higher-order Taylor expansion:
$G(V) = G_0 + G_1 V + G_2 V^2 + G_3 V^3$
Where $G_2$ and $G_3$ capture asymmetric and saturating nonlinearities typical of organic RRAM. 
Implementation: Modify `analog_layers.py` to accept polynomial coefficients from the JSON device profiles.
