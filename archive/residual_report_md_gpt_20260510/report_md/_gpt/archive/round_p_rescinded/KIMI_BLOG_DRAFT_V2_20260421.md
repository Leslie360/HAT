<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# We Thought Joint Training Would Fix Everything. It Didn't.

We thought joint training would fix everything. Train the network weights and the analog programming pulses together, let the model learn the hardware's quirks from the inside out, and watch the accuracy gap vanish. It was a beautiful hypothesis. We had the simulator, the surrogate models, and the Ensemble HAT trick that had already rescued us from the 10% hardware-instance collapse. What could go wrong? As it turns out, plenty. The ceiling didn't budge. And that failure turned out to be **the most useful result of the entire project.**

---

## The setup: this had to work

Our reasoning was simple. We already knew that a naive MLP head — one that saw fresh hardware instances at test time but was trained without any hardware-aware regularization — hit a hard ceiling around **32%** on CIFAR-10. That wasn't a soft floor; it was a wall. The diagnostic was brutal: strip out self-attention, keep only the MLP, and the feature space collapses into something barely separable once analog noise enters the picture. So we did the obvious thing. We threw **everything** at it. We linearized the MLP with a differentiable surrogate. We wrapped the whole thing in Ensemble HAT, which had previously dragged us back from 10% to 86%. We trained jointly: network weights and programming targets optimized in a single loop, no more train-then-pray. The model saw the hardware model at every step. It learned to compensate. It had to break the 32% barrier. It just had to.

The simulator was ready. Replaceable device profiles, correlated variation, retention drift — the whole physics kitchen sink. We ran sweeps across nonlinearity levels, correlation coefficients, even temperature corners. Each run took hours, but the pipeline was humming. We were so sure the 32% ceiling was a **training artifact** that better joint optimization would vaporize. We were wrong.

---

## The result: the ceiling held

On the **source domain** — the exact hardware instance distribution the model trained on — we hit **91%**. That's better than our previous Ensemble HAT best, and it felt like vindication. The joint training was doing something real. The surrogate was tracking the hardware. The ensemble was stabilizing. For a few hours, we let ourselves believe we had cracked it.

Then we tested on a **fresh hardware instance**, one drawn from the same statistical distribution but never seen during training. Accuracy collapsed to **30%**. Not 70%. Not 50%. Thirty. After all that engineering — the linearized surrogates, the ensemble heads, the joint optimization loop — we had improved on the naive 32% ceiling by a whopping **negative two percentage points.** The model hadn't learned to generalize across hardware instances. It had learned to overfit the source distribution with exquisite precision. All that extra capacity went into memorizing the training noise, not mastering the physics.

---

## The deeper lesson: three mitigations, one ceiling

We tried three distinct mitigation strategies, and every single one bounced off the same wall. The linearized MLP surrogate gave us clean gradients through the hardware model, but clean gradients through a noisy forward pass still produce a noisy solution. The Ensemble HAT ensemble exposed the model to a *distribution* of instances during training, yet the learned features still crumbled when the test instance lay outside the convex hull of the training cloud. Joint training co-optimized weights and programming targets, but the optimization landscape appears to have a **structural basin** around 30% that no local search escapes. Each fix addressed a symptom. None touched the disease.

The disease, we now believe, is **structural, not algorithmic.** There is a fundamental information-theoretic limit to how much a vision model can compensate for instance-specific analog variation when the only source of diversity during training is a finite ensemble of simulated masks. The 30-32% region isn't a training artifact. It's a **hard boundary** set by the mismatch between the dimensionality of the hardware variation space and the representational capacity we allocate to absorbing it. You can dress up the optimizer, but you can't negotiate with the geometry.

What this means for the field is uncomfortable and important. If you're building analog accelerators and your accuracy claims are based on source-domain evaluation — the same noise instance the model trained on — **you are measuring the wrong thing.** The relevant metric is fresh-instance generalization, and the gap between the two can be sixty points. We need a collective recalibration of what "works on analog hardware" actually means. Source-domain accuracy is a mirage. Fresh-instance accuracy is the oasis, and right now it's dry.

---

## The path forward: higher-order, attention-free, and silicon

So where do we go from here? Three directions feel genuinely promising, and none of them are tweaks to the training loop.

First, **higher-order surrogates.** Our current hardware proxy is a first-order approximation: differentiable, but local. A second-order surrogate that captures curvature in the device response — how small programming errors propagate through a dot product — could reshape the optimization basin entirely. The math is messier. The compute cost is higher. But if the 30% wall is geometric, we need to change the geometry, not just climb the same hill faster.

Second, **attention-free architectures.** The irony is that attention *helps* in the analog regime — our earlier work showed that without it, the ceiling drops to 32%. But attention is also expensive, noisy, and hard to deploy on tiny edge arrays. If we can find a **linear-attention** or **state-space** architecture that preserves the analog-friendly mixing properties while shedding quadratic cost, we might buy ourselves enough parameter budget to properly absorb hardware variation. The architecture itself becomes the mitigation.

Third, and most critically, **hardware-in-the-loop.** Simulation is a wonderful filter, but at some point the map is not the territory. We need training pipelines that interleave simulated batches with real-device batches, letting the model feel the true distribution of mismatch rather than our Gaussian approximation of it. The outliers — the heavy-tailed cells that simulation smooths over — might be exactly what the model needs to see to learn true robustness. Simulation got us to 91% on paper. Only silicon can teach 91% in reality.

---

## Call to action

The compute-ViT codebase drops soon: device profiles, Ensemble HAT, joint-training harness, and the full diagnostic suite that led us to this wall. **Try it.** Break it. Falsify our 30% claim with an architecture we didn't think of, or a surrogate we didn't build, or a dataset where the geometry is kinder. Nothing would make us happier than being wrong about the ceiling. That's the point of doing this in the open.

See Fig. 4 from the paper for the visual autopsy: accuracy versus mitigation strategy, source-domain on the left, fresh-instance on the right, the gap between them staring back like a verdict. If you're building analog accelerators and you've never plotted that second column, now is the time.

Analog hardware is already here. The only question left is whether we have the honesty to measure it properly.
