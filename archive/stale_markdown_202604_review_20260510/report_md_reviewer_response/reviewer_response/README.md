# Reviewer Response Package

**Complete experimental validation for Nature Communications major revision**

---

## Generated Files

### Analysis Documents
| File | Description |
|:--|:--|
| `REVIEWER_REPORT_ANALYSIS.md` | Detailed breakdown of all reviewer concerns |
| `POINT_BY_POINT_RESPONSE.md` | Draft response letter with experiment results |

### Experimental Results
| File | Description | Key Finding |
|:--|:--|:--|
| `ir_drop_sensitivity_final.json` | IR drop 0-20% sweep | 10% IR drop → -3.12% accuracy |
| `adc_nonideality_final.json` | ADC offset/gain/INL analysis | Realistic errors → -0.75% accuracy |

### Logs
| File | Description |
|:--|:--|
| `logs/ir_drop_sensitivity_final.log` | Full IR drop experiment output |
| `logs/adc_nonideality_final.log` | Full ADC non-ideality experiment output |

---

## Quick Reference: Key Results

### Q1: IR Drop Validity
```
ReRAM proxy (1-3%):    -0.17% to +0.07%  ✅ Valid
Organic typical (10%):  -3.12%            ⚠️ Moderate impact
Organic extreme (20%):  -20.47%          ❌ Significant impact
```
**Response:** 1-3% is valid lower bound; add sensitivity analysis for 5-15% organic range

### Q2: Scale-Masking Robustness
```
Ideal calibration:      63.04%            Baseline
±0.5 LSB offset:        63.02%            -0.02%
±5% gain error:         62.27%            -0.77%
Combined realistic:     62.29%            -0.75%
```
**Response:** Scale-masking is robust to realistic ADC errors (<1% degradation)

### Q3: ConvNeXt Baseline
**Issue:** 33.22% on Flowers-102 was experimental error  
**Action:** Remove erroneous result; re-train with corrected config

### Q4: Figure S2 Placement
**Action:** Move S2 to main Figure 3

---

## Manuscript Revision Checklist

- [ ] Add IR drop sensitivity section (Section X.Y)
- [ ] Add ADC non-ideality section (Section X.Z)
- [ ] Add Figure X: IR drop sensitivity curve
- [ ] Add Figure Y: ADC robustness analysis
- [ ] Move S2 to main Figure 3
- [ ] Downgrade energy claim (abstract + text)
- [ ] Add ResNet-18 limitation discussion
- [ ] Fix ConvNeXt Flowers-102 baseline
- [ ] Add scale-masking caveats to Section 1.3.3

---

## Experimental Scripts

To reproduce:

```bash
# IR drop sensitivity
cd /home/qiaosir/projects/compute_vit
python run_ir_drop_sensitivity_v3.py

# ADC non-ideality
python run_adc_nonideality_v2.py
```

---

## Status

| Reviewer Priority | Status | Evidence |
|:--|:--|:--|
| Q1 (IR drop) | ✅ Complete | `ir_drop_sensitivity_final.json` |
| Q2 (Scale-masking) | ✅ Complete | `adc_nonideality_final.json` |
| Q3 (Baseline) | ⏳ Pending | Re-training needed |
| Q4 (Figure S2) | ✅ Text change | Move to main figure |

**Ready for manuscript revision:** Yes (pending Q3 re-training)
