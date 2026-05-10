# Defense Wild-Card Q&A Prep — Negative-Result Pivot

*10 questions that cut to the pivot. Each answer: exactly 3 sentences.*

---

## 1. Negative-Result Philosophy

**Isn't it risky to build your thesis on a negative result?**

Ignoring the ceiling would be riskier: every mitigation converged to the same ~30% basin. The thesis shows the barrier is structural, redirecting the field toward higher-order surrogates and attention-free architectures. A falsifiable negative result is still a contribution when the alternative is sixty points of source-domain overfitting.

**What if a reviewer says you just didn't try hard enough?**

Source-domain joint optimization reached 91.36%, yet fresh-instance transfer collapsed to 30.89 ± 5.76%, matching the 32.12% MLP-only and 32.60% all-linear baselines. If three interventions land in the same 30–32% band, the bottleneck is not optimizer effort but the interaction between first-order NL and softmax attention. I welcome that skepticism: every checkpoint is released so someone with a better idea can falsify the claim.

## 2. Career Strategy

**Will this negative result hurt your job prospects?**

A candidate who can articulate why a hypothesis failed is more valuable than one who only reports victories, because hardware teams need people who spot dead ends. The 30% ceiling is a risk-ranking result: it tells industry where not to invest transistor budget. I frame it as signal, not noise—interviews stress the diagnostic toolkit, not the raw number.

**How do you spin this in industry interviews?**

I say we identified a deployment boundary hidden by simulation-only benchmarking, and built a protocol to measure it before silicon. The narrative is not "we got 30%," but "we stopped a team from shipping a chip that scores 91% in the lab and 30% in the fleet." ML-systems interviewers recognize that catching a sixty-point generalization gap is exactly what pre-silicon validation is for.

## 3. Meta-Science

**Did you pre-register the joint-training hypothesis?**

We did not pre-register formally, but the hypothesis was documented in timestamped group slides from March 2026, so the 30% result surprised the group rather than serving a retroactive narrative. The CX-J1 experiment was designed to break the 32% ceiling, and its failure was recorded in the lab notebook before any post-hoc storytelling. Pre-registration would have been ideal, and I now treat it as standard practice; the best I can offer is dated documentation.

**How do we know you didn't cherry-pick the 30% number?**

The 30.89% figure is the mean across ten fresh D2D instances, and the 5.76 pp standard deviation captures variance without selective reporting. Every alternative lands in the same 30–32% band, so cherry-picking one would require suppressing three others that tell the same story. Raw JSON logs and evaluation scripts are in the reproducibility bundle for independent aggregation.

## 4. Future Vision

**If you had unlimited compute, what's the first experiment you'd run to break the ceiling?**

I would train a second-order surrogate capturing curvature in the conductance-response surface, because the first-order STE may flatten basins that hide better solutions. A second-order proxy would let gradients see how programming errors propagate through dot products, potentially escaping the 30% basin without architectural change. The compute cost is prohibitive now—roughly 5–10× per pass—but unlimited resources make it the first shot.

**What would convince you the ceiling is real?**

If five independent groups, using different architectures and surrogates, report fresh-instance accuracy below 35% under severe NL, I would accept the ceiling as a fundamental limit of the current abstraction. Conversely, a single reproducible result above 50% with the same NL=2.0 profile would immediately reopen the question. Science advances by betting against its own conclusions, and I structured the release so others can take that bet.

## 5. Personal

**What was your emotional reaction when CX-J1 came back at 30%?**

I felt sick for two hours: six weeks of joint-training work and a 91% source-domain number had felt like vindication, and the fresh-instance collapse turned that triumph into proof of precise overfitting. Then I remembered that the best science begins with unwanted results, and I designed CX-J1b to isolate whether the barrier lives in QKV or in the attention block as a functional unit. That emotional arc—from denial to autopsy—is now how I mentor juniors: never trust a victory until it survives a fresh instance.

**How did your advisor react to the pivot?**

He insisted we test on fresh instances before celebrating the 91%, so when the number cratered he said, "Good, now we know," and asked me to write down the falsification conditions that could reopen the ceiling. His calm reframed the failure from a personal setback into a community boundary, the intellectual generosity a PhD advisor should provide. Our only tension came later, when I wanted to bury the result in a footnote and he pushed me to make it a chapter centerpiece.

---

*End of document — 10 questions, ~780 words.*
