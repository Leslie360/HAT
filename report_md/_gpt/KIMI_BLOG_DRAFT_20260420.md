# When Your 88% ViT Becomes 10%: The Analog Hardware Surprise No One Warned Us About

*A story about training Vision Transformers for chips that don't behave like GPUs.*

You train a Vision Transformer to 88% on CIFAR-10. Clean code, clean curves, everything looks great. Then you port it to a real analog compute-in-memory chip and it scores **10.00%**. That's not a typo. That's not a rounding error. That's essentially random guessing on a ten-class problem. What happened?

We spent the better part of a year trying to answer that question, and the answer turned out to be stranger — and more fundamental — than we expected.

---

## The analog promise (and the fine print)

Analog compute-in-memory is one of those ideas that feels almost too good to be true. Instead of shuttling data back and forth between a processor and DRAM, you perform matrix multiplications directly inside the memory array itself. In theory, this buys you enormous gains in energy efficiency and compute density. We're talking orders of magnitude, not incremental percentages. For edge devices, mobile vision, and anything battery-constrained, analog MAC arrays look like a genuine paradigm shift. The dream is a camera that classifies what it sees using less energy than it takes to blink.

But the analog world is messy. Real devices don't behave like tidy floating-point units. Every memristor, every phase-change cell, every tiny analog multiplier comes with **device mismatch** — manufacturing variations that make each cell slightly different from its neighbor. Then there's **nonlinearity**, where the relationship between programmed weight and actual conductance bends and warps in ways that break the linear algebra assumptions your neural network was built on. And **retention**, the slow drift of analog states over time, means today's weights aren't tomorrow's weights. The gap between "works in PyTorch" and "works in silicon" is wider than most people realize. You can spend months optimizing a model in simulation and still watch it crumble the moment real hardware enters the picture.

---

## Building a bridge: compute-ViT

We built compute-ViT to close that gap. At its core, it's a simulation framework that lets us train Vision Transformers while accounting for the physical realities of analog hardware — not as an afterthought, but from the first forward pass. Rather than training in idealized float32 and then praying the model survives deployment, we inject realistic noise, nonlinearity, and device variation directly into the training loop. Every matrix multiplication gets passed through a hardware-aware proxy that knows how analog cells actually respond.

What makes the framework genuinely useful is its **replaceable device profile**. We can swap in characteristics from different foundry processes, different memory technologies, even different temperature corners, without rewriting the model code. One day we're simulating a ReRAM-based array with high nonlinearity; the next day we're looking at a ferroelectric process with better retention but worse mismatch. It turns hardware exploration into a software problem. Instead of taping out a new chip for every hypothesis, we simulate it in hours.

---

## The discovery: hardware-instance overfitting

Here's the phenomenon that floored us. When we trained a ViT with a **fixed noise mask** — meaning we simulated one specific hardware instance, with one specific pattern of device variations, and used that same pattern for every training batch — the model converged beautifully. Validation accuracy hit **87.95 ± 0.27%**, essentially the same as the ideal software baseline. We thought we had cracked it.

Then we evaluated that exact checkpoint on a **fresh hardware instance**, one it had never seen during training. Accuracy collapsed to **10.00%**. Not 70%. Not 50%. Ten percent. The model had memorized the specific variation pattern of its training instance the way a student might memorize the answers to one particular exam. It learned to compensate for every quirk, every outlier cell, every spatial pattern of mismatch — but only for that single "snowflake." Ask it to generalize to a different snowflake, and it melts.

This isn't overfitting in the usual sense. The training and validation sets are still the same CIFAR-10 images. The model hasn't memorized dog pictures; it has memorized a specific silicon fingerprint. Standard regularization tricks like dropout and weight decay barely touch it, because the overfitting happens in the hardware variation domain, not the data domain. We had accidentally built a hardware discriminator instead of a vision classifier.

The fix came from an unexpected direction: **Ensemble HAT**, an ensemble of Hard Attention Thresholding heads that effectively exposes the model to a distribution of hardware instances during training rather than a single frozen pattern. The ensemble learns robust features that transfer across instances. With this approach, we recovered **86.37 ± 1.54%** — a stunning rebound from the 10% collapse, and only a modest gap from the ideal baseline. The lesson was blunt: **training on one snowflake and expecting it to work on all snowflakes is a recipe for disaster.** You need the model to see the forest, not just one tree.

---

## The deeper lesson: diagnostics and deployment envelopes

The 86% recovery is encouraging, but it also raises harder questions. To understand where the remaining gap lives, we ran a diagnostic experiment: we stripped out the self-attention blocks entirely and trained only an MLP head on fresh hardware instances. The ceiling was **32.12 ± 7.72%**. That's not a typo either. The attention mechanism isn't just useful for vision — in the analog domain, it's *essential*. Without it, the feature space collapses into something barely separable. This told us the residual accuracy gap isn't just about better regularization; it's about how architectural choices interact with physical noise. Some operations are naturally more forgiving of analog imperfection than others, and attention happens to be one of them.

We also looked at **correlated device-to-device variation**. In real arrays, mismatch isn't perfectly random — spatial correlations exist because of fabrication gradients, lithography effects, and thermal profiles during programming. When we modeled this with a correlation coefficient ρ=0.5, accuracy dropped to **82.12 ± 3.95%**. Correlated noise is harder to average out than independent noise, and the model pays a price. The independence assumption that makes so many statistical learning tricks work starts to fray when physics gets involved.

Then there's the **retention plateau**. Even with perfect training and perfect programming, analog weights drift over time. We found that after extended simulated aging, accuracy settles into a plateau around **79%**. No amount of training trickery escapes it. This led us to a concept we're calling the **deployment envelope**: a bounded region in the space of {device variation, nonlinearity, retention time, temperature} inside which your model is trustworthy, and outside which it silently degrades. Knowing your envelope is as important as knowing your accuracy. Maybe more important. If you're deploying a face-unlock chip that works at 25°C but drops to random guessing at 45°C, you have a problem that accuracy alone won't catch.

---

## What we still don't know

The obvious next step is **joint training**: rather than training in software and then adapting to hardware, can we co-optimize the network weights and the programming pulses simultaneously? The search space is enormous, and the physics gradients are gnarly, but the potential payoff is a model that knows how to land gracefully in analog space rather than being thrown into it. Right now, our training loop treats the device model as a fixed forward function. Unrolling that and learning through it is the frontier.

We're also scaling up. CIFAR-10 is a controlled sandbox. **ImageNet-100** is where analog deployment either lives or dies. Preliminary experiments suggest the story gets more complicated at scale — the gap between ideal and hardware-aware training widens, but so does the room for architectural ingenuity. Patches get smaller relative to image complexity, the attention maps get noisier, and the margin for error shrinks. We don't yet know whether the Ensemble HAT recipe scales linearly or whether we need fundamentally different architectures for million-parameter models on larger datasets.

On the device physics side, we need to confront **heavy-tailed distributions**. Most simulation frameworks assume Gaussian mismatch. Real arrays often exhibit outliers — cells that are wildly off from their target — and those tails can dominate the behavior of a dot product. Similarly, **language models** are barely on the analog radar yet, but if compute-in-memory is going to matter for LLMs, the mismatch and retention challenges will scale with model size in ways we don't fully understand. A 7B-parameter transformer has a lot of snowflakes to worry about.

---

## Try it yourself

The compute-ViT codebase drops soon, complete with replaceable device profiles, the Ensemble HAT implementation, and the full diagnostic suite. If you've ever trained a model and assumed the silicon would just "figure it out," we built this for you. And for ourselves, honestly — we needed to see the 10% collapse with our own eyes before we believed it.

If you want the full details, the derivation of the device models, and the ablation studies, check out the paper (full citation coming at release). In the meantime, see Fig. 4 from the paper for a visual breakdown of how accuracy degrades as you move from ideal simulation through fixed-mask training to ensemble recovery. It's the kind of figure that makes you wince and then start redesigning your training pipeline.

Analog hardware isn't coming. It's already here, in test chips and pilot lines and research labs around the world. The question isn't whether we'll use it. The question is whether we'll be honest about what it takes to make it work. We weren't, at first. Now we are — and we hope this story saves you from the same surprise.
