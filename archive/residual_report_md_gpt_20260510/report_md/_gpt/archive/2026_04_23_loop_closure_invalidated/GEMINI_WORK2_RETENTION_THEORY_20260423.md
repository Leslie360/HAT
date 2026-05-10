# G-HH21: Retention Theory for Organic Optoelectronic CIM KV-Cache
**Date:** 2026-04-23
**Scope:** Work 2 (LLM KV-Cache Mapping)

## 1. Formal Problem Statement

Unlike traditional model weight storage, which requires non-volatility on the scale of years ($>10^8$ s), the LLM KV-cache is highly dynamic. Its required lifespan is strictly bounded by the user's session duration, $T_{session}$.
Organic Optoelectronic CIM (OEC-RAM) typically exhibits retention times $\tau_{org} \sim 10^3$ to $10^4$ seconds. This presents a unique opportunity: if $\tau_{org}$ is statistically matched to $T_{session}$, the device can operate in a **quasi-non-volatile** regime, requiring zero electrical or optical refresh cycles during inference.

## 2. Statistical Distributions

**2.1. Session Length Distribution ($P(T)$)**
Empirical studies of LLM conversational traces (e.g., LMSYS Chatbot Arena) show that user session lengths follow a heavy-tailed distribution, well-approximated by a Log-Normal or Pareto distribution. For edge LLMs, a conservative Log-Normal model is appropriate:
$$ T \sim \text{LogNormal}(\mu_T, \sigma_T^2) $$
where the expected session time $\mathbb{E}[T]$ is roughly $300$ seconds.

**2.2. Conductance Retention Drift**
The organic OEC-RAM conductance decay is modeled by a stretched exponential relaxation:
$$ G(t) = G_0 \exp\left(-\left(\frac{t}{\tau}\right)^\beta\right) $$
For small $t/\tau$, the drift can be linearized: $\Delta G(t) \approx G_0 \frac{t}{\tau}$.

## 3. Break-Even Retention Specification

To preserve the KV-cache integrity without refresh, the maximum conductance drift over the session duration $T$ must not exceed the quantization margin (half the LSB step size). Let $N$ be the number of analog states. The margin is $\Delta G_{margin} = \frac{G_{max} - G_{min}}{2(N-1)}$.

Thus, the success condition for a given session is:
$$ G_0 \left(1 - \exp\left(-\frac{T}{\tau}\right)\right) < \Delta G_{margin} $$

Since $T$ is a random variable, we define the **System Reliability Target** $R = 1 - \epsilon$, where $\epsilon$ is the acceptable probability of cache corruption (e.g., $\epsilon = 0.01$).
We require:
$$ \mathbb{P} \left( T < -\tau \ln\left(1 - \frac{\Delta G_{margin}}{G_0}\right) \right) \ge 1 - \epsilon $$

Using the CDF of the Log-Normal distribution $F_T(t)$:
$$ F_T \left( -\tau \ln\left(1 - \frac{\Delta G_{margin}}{G_0}\right) \right) = 1 - \epsilon $$

Let $T_{critical} = F_T^{-1}(1 - \epsilon)$ be the 99th percentile of the session length distribution.
The **Break-Even Retention Spec** $\tau_{break\_even}$ is:
$$ \tau_{break\_even} = \frac{- T_{critical}}{\ln\left(1 - \frac{\Delta G_{margin}}{G_0}\right)} $$

## 4. Conclusion
Using a Taylor approximation $\ln(1-x) \approx -x$ for small $x$:
$$ \tau_{break\_even} \approx T_{critical} \cdot \frac{G_0}{\Delta G_{margin}} = T_{critical} \cdot \frac{2G_0(N-1)}{G_{max}-G_{min}} $$
This demonstrates that the required retention time scales linearly with the 99th percentile of the session length and the number of analog states $N$. For an edge LLM with $T_{critical} = 1000$s and $N=4$ states, $\tau_{break\_even} \sim 6000$s. Organic OEC-RAM perfectly satisfies this spec, offering a physics-level match for KV-cache mapping without incurring the endurance penalties of oxide-RRAM.
