# KX45: Venue Diversification Memo

> **Date**: 2026-04-13  
> **Status**: COMPLETED  
> **Scope**: 3-5个合理投稿venue的定位比较与最小改稿路线

---

## Venue Comparison Matrix

| Venue | Why Fit | Main Risk | Minimum Change | Timeline |
|:------|:--------|:----------|:---------------|:---------|
| **Nature Communications** | Cross-disciplinary (materials+ML+architecture); precedent for simulation frameworks (AIHWKIT) | 8/10 reviewers expect Major Revision; proxy parameter skepticism from materials reviewers | Add Parameter Risk Matrix; strengthen Ensemble HAT baseline comparison text | Immediate |
| **npj Computational Materials** | Nature portfolio; method-friendly; lower hardware validation bar | Lower impact factor; less ML systems audience | Emphasize materials-to-system bridge narrative; reduce algorithm novelty emphasis | 1 week |
| **Advanced Intelligent Systems** (Wiley) | Emerging venues; accepts simulation; IF ~7 | Less prestigious than NC; smaller readership | Minor reformatting; emphasize system intelligence angle | 1 week |
| **IEEE TCAD** | Top EDA venue; strong simulation tradition | Long review cycle (6-9 months); less materials science crossover | Expand methodology detail; add formal verification of analog models | 2-3 months |
| **NeurIPS Systems Track** | ML systems audience; appreciates algorithmic contribution | No materials science readership; expects ImageNet-scale results | Remove device physics; emphasize Ensemble HAT as ML systems contribution | 1-2 months |

---

## Detailed Analysis

### 1. Nature Communications (Current Target)

**Fit Score**: 4/5  
**Acceptance Probability**: Moderate (Major Revision likely)

**Strengths**:
- Cross-disciplinary sweet spot (organic materials + ML systems)
- AIHWKIT precedent (2020) establishes simulation-framework acceptability
- "6-bit ADC cliff" and "fresh-instance collapse" are NC-style actionable insights
- Profile-driven interface provides reusable community tool

**Risks**:
- 8/10 0412 reviewers expect Major Revision
- Proxy parameters will trigger materials-side skepticism
- CIFAR-scale validation deemed insufficient by some ML reviewers

**Required Changes**:
1. Add Parameter Risk Matrix (KX41 Defense 8)
2. Strengthen Ensemble HAT vs. domain randomization distinction textually
3. Add explicit "simulation-only" claim scope in abstract/conclusion
4. Prepare Major Revision response strategy (measured data pipeline)

**Decision Trigger**: Submit if willing to undergo Major Revision cycle; otherwise consider alternatives.

---

### 2. npj Computational Materials (Recommended Alternative)

**Fit Score**: 4.5/5  
**Acceptance Probability**: High (Minor Revision likely)

**Strengths**:
- Nature portfolio maintains credibility
- Explicitly welcomes methodology papers
- Lower expectation for hardware validation
- Materials science audience appreciates device-parameter sensitivity analysis

**Risks**:
- Lower impact factor than NC
- Less visibility in ML/AI community
- May be perceived as "downgrade" despite quality fit

**Required Changes**:
1. Reorder contributions: foreground materials-to-system bridge
2. Reduce emphasis on Ensemble HAT algorithm novelty
3. Expand device physics discussion (retention, photoresponse)
4. Add explicit comparison to other materials simulation tools

**Decision Trigger**: Choose if priority is acceptance confidence over maximum impact.

---

### 3. Advanced Intelligent Systems (Wiley)

**Fit Score**: 4/5  
**Acceptance Probability**: High

**Strengths**:
- Growing venue for neuromorphic/AI hardware
- Welcomes simulation studies
- Faster review cycle than Nature portfolio
- Good fit for "intelligent edge systems" angle

**Risks**:
- IF ~7 (vs NC ~16)
- Smaller readership
- Less recognition in academic evaluation

**Required Changes**:
1. Reformat to Wiley template
2. Emphasize "intelligent systems" aspects (edge deployment, efficiency)
3. Maintain current content with minor scope adjustments

**Decision Trigger**: Choose if speed-to-publication is priority.

---

### 4. IEEE TCAD (IEEE Transactions on Computer-Aided Design)

**Fit Score**: 3.5/5  
**Acceptance Probability**: Moderate (long cycle)

**Strengths**:
- Premier EDA venue
- Strong tradition of simulation/validation papers
- Rigorous methodology review
- Good for framework/tool contributions

**Risks**:
- 6-9 month review cycle
- Expects formal model verification
- Minimal materials science readership
- May require substantial methodology expansion

**Required Changes**:
1. Add formal verification of analog behavior models
2. Expand AIHWKIT comparison to full numerical equivalence study
3. Add circuit-level validation (SPICE co-simulation)
4. Restructure for EDA audience (less ML background assumed)

**Decision Trigger**: Choose if long-term credibility in EDA community is priority.

---

### 5. NeurIPS Systems Track

**Fit Score**: 3/5  
**Acceptance Probability**: Low (scope mismatch)

**Strengths**:
- Top ML venue
- Ensemble HAT algorithm contribution valued
- Large systems community

**Risks**:
- No materials science audience
- Expects ImageNet-scale results
- Device physics section irrelevant to reviewers
- High rejection rate for non-standard ML contributions

**Required Changes**:
1. Remove all device physics (retention, photoresponse, NL write)
2. Frame as "robust training for deployment variation"
3. Add ImageNet experiments (substantial new work)
4. Compare to modern robustness methods ( adversarial training, etc.)

**Decision Trigger**: Only if willing to do substantial new experiments and reposition as pure ML systems paper.

---

## Strategic Recommendation

### Tier 1 (Immediate Action)

**Option A**: Submit to NC now, prepare for Major Revision
- 60% probability of Major Revision → eventual acceptance
- Highest impact if successful
- Requires measured data for revision (user has in-house data coming)

**Option B**: Pivot to npj Computational Materials
- 80% probability of Minor Revision → acceptance
- Maintains Nature portfolio credibility
- Faster path to publication

### Tier 2 (Contingency)

**Option C**: Simultaneous preparation
- Submit NC first
- If rejected without review, immediately pivot to npj
- Requires minimal dual-track preparation

### Tier 3 (Not Recommended)

**Option D**: Wait for measured data before any submission
- Loses first-mover advantage
- Risk of being scooped
- Current package is defensible as-is

---

## Decision Matrix

| Your Priority | Recommended Venue | Action |
|:--------------|:------------------|:-------|
| Maximum impact | NC | Submit now; prepare Major Revision response |
| Acceptance confidence | npj Computational Materials | Reposition emphasis; submit within 1 week |
| Speed to publication | Advanced Intelligent Systems | Reformat; submit immediately |
| EDA community credibility | IEEE TCAD | Expand methodology; accept long cycle |
| ML systems recognition | NeurIPS (not recommended without ImageNet) | Major repositioning required |

---

## Next Steps

1. **Decide on primary target** (NC vs npj)
2. **If NC**: Execute KX41-KX44 defense packs; submit within 1 week
3. **If npj**: Reposition contributions (KX41 adjustments); submit within 1 week
4. **Either case**: Prepare Parameter Risk Matrix as defensive asset

*No change to locked numbers; no new GPU experiments required for any option.*
