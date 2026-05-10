# Comparison Baseline Reality Check — 2026-04-17

**Scope:** Audit whether the comparison labels "MI-HAT", "SDR-HAT", and related multi-instance analog-HAT baselines correspond to real, citable prior art, or to plausible-sounding LLM-invented labels.

---

## 1. "MI-HAT" / "Multi-Instance HAT"

### Is this an actual named method?
**No.**

### Evidence
- A web search for `"MI-HAT"` together with `"hardware-aware training"`, `"analog crossbar"`, or `"CIM"` returns **zero** hits in the neuromorphic / analog-AI literature.
- The only academic occurrence of `"MULTI_HAT"` found is a French hardware-engineering thesis describing a **multi-channel Hardware Address Translator** for DMA peripherals (unrelated to neural networks or memristors).

### Closest real literature instead
1. **Zhu et al. (2020)** — *Statistical training for neuromorphic computing using memristor-based crossbars considering process variations and noise* (DATE).
   This work samples device parameters statistically during training, but it treats variation as a per-weight parameter distribution rather than as fixed spatial mismatch maps per hardware instance.

2. **Liu et al. (2015)** — *Vortex: Variation-aware training for memristor X-bar* (DAC).
   A variation-aware training framework that models device non-idealities, but again without the epoch-level resampling of full spatial D2D maps.

3. **IBM variation-aware training** (Krishnan et al., 2021/2022) — Uses measured RRAM variation data to inject noise during training and proposes "model stability" as a metric.
   No multi-instance HAT label is used, and the training does not resample spatial instance maps.

---

## 2. "SDR-HAT" / "Spatial Domain Randomization HAT"

### Is this an actual named method?
**No.**

### Evidence
- No publication, preprint, or conference abstract uses the acronym `"SDR-HAT"` or the phrase `"Spatial Domain Randomization HAT"` in the context of analog CIM or neuromorphic computing.
- `"Domain Randomization"` itself is a well-known robotics concept (Tobin et al., IROS 2017), but no literature fuses it with `"HAT"` to form a named analog-training method.

### Closest real literature instead
1. **Tobin et al. (2017)** — *Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World* (IROS).
   The source of the domain-randomization concept; applied to rendering/robotics, not to spatial hardware-instance mismatch.

2. **Rasch et al. (2021)** — AIHWKIT.
   Offers optional per-batch i.i.d. noise resampling, which is the nearest existing open-source implementation, but the noise lacks spatial structure.

---

## 3. "Any claimed analog-CIM training method that explicitly varies spatial hardware instances during training"

### Is there a canonical named method fitting this exact description?
**No.**

### What exists in the literature
| Paper | What it actually does | Why it is not the same |
|:------|:----------------------|:-----------------------|
| **Zhu et al., DATE 2020** | Statistical sampling of device parameters during training | Per-weight sampling, not full spatial instance maps |
| **Liu et al., DAC 2015 (Vortex)** | Variation-aware training with device noise injection | No epoch-level resampling of fixed spatial mismatch maps |
| **IBM variation-aware training** | Noise injection based on measured chip statistics | Optimizes a single model against a variation distribution, not against a sequence of distinct instance maps |
| **AIHWKIT (Rasch 2021)** | Optional per-batch i.i.d. Gaussian noise | No spatial correlation; noise is independent per weight |

None of these papers introduce a named method equivalent to "resample the full spatial D2D mismatch map at each training epoch."

---

## 4. What Comparisons Are Actually Defensible to Mention in Response to Reviewers?

**Conservative, reviewer-safe wording:**

> We are not aware of a prior open-source baseline that implements exactly the same epoch-level resampling of full spatial D2D mismatch maps. The closest available analog-training toolkits (AIHWKIT) support only i.i.d. noise injection, which our ablation shows is insufficient for fresh-instance transfer. Variation-aware training methods in the literature (Zhu et al., DATE 2020; Liu et al., DAC 2015) model device variability statistically, but they typically sample parameters per weight or per layer rather than resampling complete spatial instance maps. Because no external apples-to-apples baseline exists, we rely on internal controls—fixed-mask standard HAT, per-batch i.i.d. perturbation, and per-epoch structured D2D resampling—to isolate the causal contribution of the mismatch-map exposure schedule.

**Why this is defensible:**
- It does not invent method names.
- It acknowledges real prior work without overstating overlap.
- It explains why an internal ablation is the strongest available evidence.
- It avoids implying that the reviewers' suggested baselines are real but missing.

---

## Bottom line

| Label | Verdict |
|:------|:--------|
| MI-HAT / Multi-Instance HAT | **Invented / non-canonical** |
| SDR-HAT / Spatial Domain Randomization HAT | **Invented / non-canonical** |
| "Explicit spatial instance resampling for analog HAT" as a named prior method | **Does not exist in citable literature** |

The fairest response to any reviewer requesting these comparisons is to state clearly that the labels do not correspond to known prior art and to point to the closest real literature instead.
