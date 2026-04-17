# KX54: Second-Paper Opportunity Memo

> **Date**: 2026-04-13  
> **Status**: COMPLETED  
> **Scope**: Identify high-value follow-up contributions enabled by current infrastructure

---

## Strategic Context

**User decision**: Wait for measured data (Option 3) before first-paper submission.  
**Opportunity**: Use interval to discover and prepare second-paper contributions.

---

## Second-Paper Opportunity Matrix

### Opportunity A: ImageNet-Scale Validation

**Core Idea**: Demonstrate Ensemble HAT and framework at ImageNet-1K scale

**Gap in Current Paper**: 
- Current: CIFAR-10/100, Flowers-102 (reviewer criticism: "toy datasets")
- Missing: ImageNet-scale validation for real-world edge deployment

**Contribution**:
- First organic-CIM simulation at ImageNet scale
- Scale-dependent accuracy degradation analysis
- Computational cost benchmarking (training wall-clock)

**Required GPU**: ~40-60 GPU-hours per architecture (Tiny-ViT, ConvNeXt)

**Target Venues**:
- **NeurIPS Systems Track** (if breakthrough results)
- **IEEE TPDS** (solid systems contribution)
- **ACM TECS** (embedded systems focus)

**Risk**: May show catastrophic failure (manageable with honest analysis)

---

### Opportunity B: Full Measured-Device Closure

**Core Idea**: Complete validation loop with in-house measured organic arrays

**Gap in Current Paper**:
- Current: Literature-proxy parameters
- Missing: Measured-device calibration and validation

**Contribution**:
- First end-to-end organic optoelectronic CIM with measured-device simulation
- Profile auto-fitter validation against real G-V curves
- Quantitative prediction accuracy assessment

**Required**: Measured data (6 parameters) + ~10 GPU-hours for validation runs

**Target Venues**:
- **Nature Electronics** (measured-device closure highly valued)
- **npj Computational Materials** (natural extension)
- **Advanced Materials** (device-focused)

**Risk**: Low (follow-up to current methodology)

---

### Opportunity C: Cross-Device Transferability

**Core Idea**: Train on one device profile, deploy on another

**Gap in Current Paper**:
- Current: Single canonical profile + Zhang case study
- Missing: Systematic cross-device transfer analysis

**Contribution**:
- Device-agnostic training methodology
- Transfer learning for CIM deployment
- Domain adaptation metrics for analog arrays

**Required**: Multiple device profiles (could use literature + measured)

**Target Venues**:
- **ICML** (domain adaptation angle)
- **IEEE TCAD** (design automation focus)
- **DATE** (embedded systems)

**Risk**: Medium (algorithmic contribution may overlap with existing ML literature)

---

### Opportunity D: Open-Source Framework Release

**Core Idea**: Productionize and release simulation framework

**Gap in Current Paper**:
- Current: Research codebase
- Missing: Community-ready tool with documentation

**Contribution**:
- pip-installable package
- Interactive tutorials (Jupyter notebooks)
- Pre-trained model zoo
- Community contribution guidelines

**Required**: Engineering effort (minimal GPU)

**Target Venues**:
- **JOSS** (Journal of Open Source Software)
- **SoftwareX** (Elsevier)
- **NeurIPS Datasets/Benchmarks Track**

**Risk**: Low; high community value

---

### Opportunity E: Temporal Dynamics Deep-Dive

**Core Idea**: Comprehensive retention and drift analysis

**Gap in Current Paper**:
- Current: Simplified uniform retention model
- Missing: State-dependent, time-varying dynamics

**Contribution**:
- Physics-informed retention modeling
- Temporal training strategies
- Drift-aware inference scheduling

**Required**: Retention parameter sweeps (~10 GPU-hours) + theoretical analysis

**Target Venues**:
- **IEDM** (device-focused)
- **IEEE TED** (device physics)
- **npj Computational Materials**

**Risk**: Low; builds on current framework

---

## Prioritized Recommendation

| Priority | Opportunity | Rationale | Preparation |
|:---------|:------------|:----------|:------------|
| **P0** | B: Measured-device closure | Natural extension; leverages in-house data; highest acceptance confidence | Prepare profile auto-fitter; queue validation experiments |
| **P1** | A: ImageNet validation | Highest impact if successful; addresses key reviewer criticism | Pre-run scaling analysis; prepare checkpoint resume strategy |
| **P2** | D: Open-source release | Force multiplier for all other work; community building | Package structure; documentation skeleton |
| **P3** | E: Temporal dynamics | Deepens technical contribution; device physics angle | Literature review on retention models |
| **P4** | C: Cross-device transfer | Interesting but may overlap with existing ML methods | Survey domain adaptation literature |

---

## Timeline Integration

### Current Paper Submission (Option 3)
- **T+0 to T+2 months**: Wait for measured data
- **T+2 to T+3 months**: Integrate data; submit to NC

### Second-Paper Parallel Track
```
Month 1-2 (while waiting for data):
├── ImageNet baseline setup (Opportunity A)
├── Open-source packaging (Opportunity D)
└── Measured-data integration prep (Opportunity B)

Month 3 (after first-paper submission):
├── ImageNet full runs (if promising)
├── Measured-device validation paper (Opportunity B)
└── Open-source release

Month 4-6:
├── Submit second paper (measured-device focus)
└── Continue ImageNet if results strong
```

---

## Resource Allocation

### GPU Priority
1. **First**: Current-paper strengthening (GM-E1, GM-E2)
2. **Second**: ImageNet exploration (Opportunity A)
3. **Third**: Measured-data validation (Opportunity B, when data arrives)

### Engineering Priority
1. **First**: Profile auto-fitter refinement (measured-data readiness)
2. **Second**: Open-source packaging (Opportunity D)
3. **Third**: Documentation and tutorials

---

## Success Metrics

### Opportunity A (ImageNet)
- [ ] Successfully train V1 baseline on ImageNet-1K
- [ ] Demonstrate Ensemble HAT recovery at scale
- [ ] Wall-clock time <10x CIFAR-100 (efficiency claim)

### Opportunity B (Measured-device)
- [ ] Auto-fitter achieves R² > 0.9 on measured G-V curves
- [ ] Simulation predicts measured-device accuracy within ±5pp
- [ ] End-to-end validation paper submitted

### Opportunity D (Open-source)
- [ ] pip install orgoptedge-sim
- [ ] 3+ tutorial notebooks
- [ ] Community issue tracking active

---

## Conclusion

**Highest-value second-paper opportunity**: Measured-device closure (Opportunity B)
- Leverages in-house data already planned
- Natural extension of current methodology
- High acceptance confidence at strong venue

**Highest-risk/high-reward**: ImageNet validation (Opportunity A)
- Could enable top-tier ML venue targeting
- Requires substantial GPU investment
- Unclear if Ensemble HAT scales

**Immediate action**: Begin ImageNet setup while waiting for measured data.

---

**GPU Status**: `nvidia-smi` available. Recommend launching ImageNet V1 baseline as continuous background job while waiting for measured data.
