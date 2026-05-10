# G-BB5: GPU-window strategy brief

## Recommendation
Run the **joint MLP-linear + Ensemble HAT smoke** first, and defer the ImageNet-100 pilot to Round N.

## Rationale
1. The joint-training formulation is the highest-value thesis experiment because it directly targets the fresh-instance gap exposed by the severe-NL study.
2. A 3-epoch smoke is cheap and immediately de-risks the implementation path for the real thesis run.
3. The ImageNet-100 pilot is valuable, but it is a larger compute commitment and does not answer the most acute open mechanistic question.

## Sequencing
- Step 1: complete the 3-epoch smoke and confirm the loss/optimizer path is NaN-free.
- Step 2: if stable, choose between a full joint-training run and the ImageNet pilot based on user priorities and rebuttal timing.
- Step 3: keep ImageNet-100 as the next window once the joint-training path is proven executable.
