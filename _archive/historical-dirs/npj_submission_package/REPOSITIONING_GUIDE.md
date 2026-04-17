# npj Computational Materials: Manuscript Repositioning Guide

> **Goal**: Adapt NC-targeted manuscript for npj Computational Materials  
> **Focus**: Materials methodology over ML systems novelty  
> **Key Shift**: "Algorithm enabling materials evaluation" → "Materials framework using ML"

---

## 1. Title Revision

### Current (NC-style)
> Profile-Driven Hardware Simulation for Organic Optoelectronic Vision Transformers

### Recommended (npj-style)
> **Option A**: Profile-Driven Behavioral Simulation for Organic Optoelectronic Compute-in-Memory: A Materials-to-System Methodology

> **Option B**: Bridging Reported Device Metrics and Deployment Risk: A Simulation Framework for Organic Optoelectronic Arrays

> **Option C**: Materials-Aware Simulation of Vision Transformer Inference on Organic Optoelectronic Synaptic Arrays

**Selection Rationale**: Option A emphasizes "methodology" and "materials-to-system", aligning with npj's scope.

---

## 2. Abstract Restructuring

### Current Structure (NC)
1. Motivation (organic devices)
2. Gap (no simulator)
3. Solution (framework)
4. Key findings (HAT, ADC, NL)
5. Positioning (decision bridge)

### New Structure (npj)
1. **Materials Context**: Organic optoelectronic devices for edge computing
2. **Characterization Gap**: Literature metrics → deployment risk translation
3. **Methodology**: Profile-driven simulation interface
4. **Device Physics Insights**: Parameter sensitivity, ADC requirements
5. **Validation Path**: Framework verified against established tools
6. **Positioning**: Transparent evaluation methodology for materials researchers

### Revised Abstract Draft

```latex
\begin{abstract}
Organic optoelectronic synaptic devices offer compelling characteristics for 
edge computing—multilevel conductance tuning, low static power, and optical 
programmability—yet reported device-level metrics leave a critical question 
unanswered: are these characteristics sufficient for modern vision tasks? 
Existing characterization flows focus on single-device properties, lacking 
a systematic bridge to system-level deployment risk.

To address this gap, we present a profile-driven behavioral simulation 
methodology that translates literature-derived or measured device parameters 
into task-level accuracy and energy bounds for compute-in-memory inference. 
The framework explicitly models organic-specific physics: photoresponse 
non-linearity, dual-exponential retention drift, and write non-linearity. 

Systematic sensitivity analysis reveals that analog-to-digital converter 
resolution (not nominal conductance quantization) dominates deployment 
bottlenecks, with a sharp 6-bit accuracy cliff observed across architectures. 
Device-to-device variation emerges as the critical training challenge; 
standard hardware-aware training collapses to 10\% on fresh hardware instances, 
while an ensemble training strategy resampling device masks recovers 
86.37$\\pm$1.54\% accuracy. 

All experiments are conducted at the behavioral simulation level using 
literature-derived proxy parameters; fabricated-array validation represents 
a natural extension enabled by the profile-driven interface. We position 
the framework as a transparent materials-to-system evaluation methodology, 
providing materials researchers with actionable feedback on which device 
characteristics most strongly constrain edge-vision deployment.
\end{abstract}
```

---

## 3. Introduction Reordering

### Current (NC)
1. Organic device promise
2. CIM motivation
3. Existing simulators (inorganic focus)
4. Our framework (4 contributions)
5. Key findings preview

### Revised (npj)
1. **Organic materials for computing** (device properties)
2. **Characterization-to-deployment gap** (materials science problem)
3. **Simulation methodology precedent** (computational materials)
4. **Our methodology** (4 contributions, reordered):
   - Profile-driven device-to-system interface
   - Device physics sensitivity analysis
   - Training methodology for D2D robustness
   - Literature case study
5. **Findings preview** (materials-relevant)

---

## 4. Contribution Reordering

### For NC (Algorithm-first)
1. Ensemble HAT algorithm
2. Profile-driven framework
3. ADC cliff insight
4. Case study validation

### For npj (Materials-first)
1. **Profile-driven materials-to-system interface**
   - JSON parameter injection
   - Device physics abstraction
   - Future measured-data path
   
2. **Device parameter sensitivity methodology**
   - C2C/D2D sweep framework
   - Retention time constant analysis
   - Frontend non-linearity compensation
   
3. **Training methodology for deployment robustness**
   - Hardware-instance overfitting discovery
   - Ensemble HAT as solution
   
4. **Literature-profile validation**
   - Zhang 2025 case study
   - Cross-paper comparison capability

---

## 5. Related Work Additions

### Must Add Section: "Computational Materials Tools"

```latex
\subsection{Simulation Methodology in Materials Science}

Computational materials science has developed robust methodologies for 
bridging atomistic parameters to macroscopic properties. Density functional 
theory (DFT) enables band structure prediction from atomic configurations; 
molecular dynamics connects interatomic potentials to transport phenomena. 
However, a analogous methodology bridging device-level non-idealities to 
system-level deployment metrics remains underdeveloped for emerging 
computational materials.

Existing device simulation tools (TCAD, SPICE) focus on circuit-level 
verification rather than machine learning workload evaluation. Recent 
neuromorphic computing frameworks (AIHWKIT, NeuroSim, CrossSim) provide 
system-level simulation but target inorganic resistive memories, lacking 
organic-specific physics: photoresponse, retention drift, and optical 
programming dynamics.

Our work complements these approaches by providing a methodology explicitly 
designed for organic optoelectronic devices, with profile-driven parameter 
substitution enabling seamless transition from literature values to future 
measured characterization.
```

---

## 6. Results Emphasis Shifts

### Maintain (Core Findings)
- 6-bit ADC cliff
- D2D dominance over C2C
- Ensemble HAT recovery

### Enhance (Materials Relevance)
- **Parameter sensitivity analysis** foreground
- **Device physics interaction** discussion
- **Literature parameter provenance** transparency

### Reduce (ML Systems Focus)
- Algorithm novelty claims
- Comparison to ML robustness methods
- Transformer architecture details

---

## 7. Discussion Expansions

### Add: "Implications for Materials Characterization"

```latex
\subsection{Guidance for Device Engineering Priorities}

The sensitivity analysis provides actionable guidance for organic device 
researchers prioritizing engineering efforts:

\begin{enumerate}
    \item \textbf{ADC precision over state count}: Increasing conductance 
    states beyond 6-bit ADC resolution provides diminishing returns. 
    Materials effort should prioritize consistent programming over 
    maximizing distinguishable levels.
    
    \item \textbf{D2D uniformity over C2C reduction}: Within-batch 
    variation dominates deployment accuracy; process control should 
    emphasize spatial uniformity over single-device programming precision.
    
    \item \textbf{Retention time constants}: The double-exponential model 
    parameters ($\tau_1$, $\tau_2$) can be extracted from standard 
    conductance decay measurements; we provide the extraction methodology 
    in Supplementary Section S1.3.
\end{enumerate}
```

---

## 8. Supplementary Enhancements

### Must Add

1. **Parameter Risk Matrix** (already prepared)
   - Table S5 with robustness ratings
   
2. **Device Physics Comparison**
   - Organic vs. inorganic non-idealities
   - Why standard RRAM models fail for organics
   
3. **Profile Fitting Methodology**
   - How to extract parameters from literature
   - Example: Zhang 2025 extraction walkthrough

### Can Remove (or Deprioritize)

1. ML training hyperparameter details
2. Architecture comparison deep-dive
3. Energy model circuit-level discussion

---

## 9. Cover Letter Adaptation

### Key Changes

**Opening**:
> "We submit a methodology paper bridging organic device characterization 
> and system-level deployment evaluation..."

**Why npj**:
> "npj Computational Materials' explicit welcome of methodology papers 
> bridging materials characterization and application contexts makes it 
> the ideal venue for this work. The framework provides materials 
> researchers with systematic tools to evaluate how reported device 
> properties translate to real-world deployment constraints."

**Contribution Framing**:
> "The core contribution is a reusable simulation methodology enabling 
> computational exploration of device-design tradeoffs before full 
> hardware validation..."

---

## 10. Anticipated Reviewer Concerns (npj-specific)

### Concern 1: "Where is the new materials science?"
**Defense**: Methodology papers advance the field by enabling new 
computational experiments. DFT didn't require new atoms; it enabled 
new predictions.

### Concern 2: "Why not wait for measured devices?"
**Defense**: Simulation methodology must precede validation. This 
framework establishes the evaluation infrastructure for future 
measured-device studies.

### Concern 3: "Is this just curve fitting?"
**Defense**: The framework embeds physical device models (retention, 
photoresponse, non-linearity) within an executable simulation. 
Predictions are mechanistic, not phenomenological.

---

## Implementation Checklist

- [ ] Update title (Option A)
- [ ] Rewrite abstract (npj structure)
- [ ] Reorder introduction contributions
- [ ] Add "Computational Materials Tools" section
- [ ] Expand "Implications for Materials Characterization" discussion
- [ ] Add Parameter Risk Matrix to supplementary
- [ ] Create npj-specific cover letter
- [ ] Verify all materials terminology consistent
- [ ] Check supplementary device physics content

---

**Estimated Effort**: 1-2 days of focused editing  
**Expected Outcome**: Manuscript repositioned for high-confidence npj acceptance
