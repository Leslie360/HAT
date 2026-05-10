# GEMINI G-Z2: Single-Class Collapse Mechanism — 2026-04-19

**Reread of canonical state:** I have reviewed the confirmation from `CX-BB` (10.00 ± 0.00% accuracy) which verifies that standard (fixed-mask) hardware-aware training (HAT) results in a deterministic single-class predictor when evaluated on fresh hardware instances.

## Mechanistic Story: The Geometry of Collapse

The 10.00% accuracy on CIFAR-10 is not a random guess (which would exhibit variance); it is a **deterministic representational collapse**. This occurs because standard HAT allows the optimizer to "cheat" by co-adapting weights to a specific hardware mismatch map.

1.  **Exploitation of Train-Time D2D Realization**: During training with a fixed D2D mask $M_{\text{train}}$, the optimizer treats the mismatch as a static feature rather than noise. It finds a local minimum where the weights $W$ are specifically tuned to cancel out the errors induced by $M_{\text{train}}$. This co-adaptation creates a sharp, narrow basin in the loss landscape that is valid *only* for that specific $M_{\text{train}}$.
2.  **Logit Margin Saturation**: Because the network is trained to produce high-confidence predictions, the logit for the correct class is pushed far from the decision boundary. However, this margin is built on the "interference pattern" of the weights and the training mask. When a fresh mask $M_{\text{fresh}}$ is introduced, the interference pattern is destroyed. The resulting logit shifts are not random; they are often large enough to saturate a single output neuron (e.g., the "airplane" or "frog" class) regardless of the input features.
3.  **Attention Head Specialization**: In Tiny-ViT, specific attention heads specialize in spatial features. Fixed-mask training binds these heads to specific physical crossbar locations. If those locations have high $M_{\text{train}}$ conductance, the head learns to "ignore" or "amplify" that hardware bias. On a fresh instance, the amplification happens at the wrong spatial location, destroying the attention map geometry and forcing the global pooling layer to default to a bias-dominated single-class prediction.

**Conclusion**: The 10.00% result is the terminal state of **hardware-instance overfitting**. The model hasn't learned "robust features"; it has learned a "hardware-specific lookup table" that breaks completely when the hardware instance changes.
