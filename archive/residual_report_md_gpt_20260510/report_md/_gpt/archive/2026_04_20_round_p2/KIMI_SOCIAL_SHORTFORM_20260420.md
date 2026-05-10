# Social Shortforms — Post-Submission Announcement

*Date: 2026-04-20*
*Paper: Profile-Driven Behavioral Simulation of Organic Optoelectronic Compute-in-Memory for Edge Vision (submitted)*

---

## Thread A — Twitter/X (5–7 tweets)

> **Tweet 1 / Hook**
>
> You train a Vision Transformer to 88% on CIFAR-10. You put it on a real analog chip. It scores 10%. What happened?

---

> **Tweet 2 / The Answer**
>
> You trained on one fixed noise mask. The model memorized that chip's exact fingerprint — not the dataset. We call it hardware-instance overfitting. Standard regularization can't touch it because the overfitting lives in the physics domain, not the data domain.

---

> **Tweet 3 / The Fix**
>
> The fix is almost embarrassingly simple: Ensemble HAT. Resample the device noise every single epoch. Instead of memorizing one snowflake, the model learns to generalize across thousands of hardware instances. No extra inference cost. No architecture change.

---

> **Tweet 4 / The Number**
>
> Result: 86.37 ± 1.54% accuracy on fresh chip instances. That's a recovery from 10% (random guessing) to within ~1.5 points of the ideal software baseline. The gap isn't physics. It was the training recipe all along.

---

> **Tweet 5 / The Limitation**
>
> Caveat: this is a first-order behavioral model. Real chips have correlated D2D variation, retention drift, heavy-tailed outliers, and temperature dependence. We model some of it, but silicon always has more physics than simulation.

---

> **Tweet 6 / The Next Step**
>
> What's next? Joint training (co-optimizing weights and programming pulses), scaling to ImageNet-100, and stress-testing whether analog compute can ever work for LLMs. The 10%→86% jump was step one. The hard physics is still ahead.

---

> **Tweet 7 / CTA**
>
> 📄 Paper: "Profile-Driven Behavioral Simulation of Organic Optoelectronic CIM" (submitted)
> 💻 Code & checkpoints: GitHub release upon acceptance
> Questions welcome — DMs open.

---

## Thread B — LinkedIn (1 long post)

As edge AI moves from the cloud to sensor nodes, energy efficiency has become the defining constraint. Analog compute-in-memory promises orders-of-magnitude gains by performing matrix multiplications inside the memory array itself — but until now, a catastrophic accuracy collapse has blocked deployment. Our work, supported by NVIDIA through the Apamayo program, identifies the root cause as hardware-instance overfitting and demonstrates that resampling device noise during training recovers 86.37% accuracy on organic optoelectronic arrays. This turns a training artifact into a solvable software problem, opening a credible path to low-power vision accelerators. We are now scaling this framework toward ImageNet and joint weight-programming co-optimization. If you work on emerging memory devices, analog circuit design, or robust training theory, we are actively looking for collaborators and prospective postdocs to close the gap between simulation and silicon. Please reach out.

---

*End of document.*
