# KX51: Doctor-Friendly Measured-Data Crosswalk

> **Date**: 2026-04-13  
> **Status**: COMPLETED  
> **Scope**: Bridge simulator needs to exact raw data types PhD students likely have

---

## Source Basis

This crosswalk is based on:
- `MEASURED_DATA_REQUEST_DOCTOR_FRIENDLY.md` (priority list)
- `report_md/WQY-基于缺陷工程的易失性和非易失性...docx` (WQY paper)
- `report_md/d5mh00948k.pdf` (second group paper)
- `report_md/审稿意见0412.md` (Sonar: "what measured data would help most")

---

## Crosswalk Table: Raw Data → Simulator Parameters

### Priority P0 (Critical Path)

| Raw Data Family | Which Paper Figure(s) | What Student Likely Calls It | Acceptable Formats | Simulator Quantity Extracted |
|:----------------|:----------------------|:-----------------------------|:-------------------|:-----------------------------|
| **Multi-state storage raw data** | WQY Fig S14 / d5mh Fig S14 | "多状态存储测试" / "16-state or 64-state conductance levels" | Excel (.xlsx), CSV (.csv), Origin (.opj), instrument text export | `G_min`, `G_max`, `n_states`, state spacing uniformity |
| **Retention/decay raw data** | WQY Fig S13 / d5mh Fig S13, S14 | "保持性测试" / "电导-时间曲线" / "retention measurement" | Excel, CSV, Origin, Keithley/Agilent log files | `tau_1` (fast), `tau_2` (slow), `A_0` (amplitude ratio) via dual-exponential fit |
| **Wavelength/illumination transfer curves** | WQY Fig S11 / d5mh Fig 3(h) | "不同波长转移曲线" / "254/365/425 nm transfer" | Excel, CSV, Origin, semiconductor parameter analyzer export | `gamma_phys` (photoresponse nonlinearity), `alpha` (wavelength response), programming threshold shifts |
| **Program/erase state transfer curves** | d5mh Fig 3(i) | "初始态/写入态/擦除态" / "P/E states transfer" | Excel, CSV, Origin | `G_min` (erased), `G_max` (programmed), memory window, threshold voltage shift |

### Priority P1 (High Value)

| Raw Data Family | Which Paper Figure(s) | What Student Likely Calls It | Acceptable Formats | Simulator Quantity Extracted |
|:----------------|:----------------------|:-----------------------------|:-------------------|:-----------------------------|
| **EPSC pulse response** | WQY Fig S9, S10 | "EPSC响应" / "脉冲光电导" / "pulse photoconductivity" | Excel, CSV, oscilloscope CSV, Keithley log | Transient response times, volatility timescales, pulse-to-pulse variation |
| **Dark/light output characteristics** | WQY Fig S4, S5 | "暗态/光照输出曲线" / "output characteristics" | Excel, CSV, semiconductor analyzer export | Dark current level, photocurrent ratio, operating regime boundaries |
| **State-switching curves** | d5mh Fig 5(k) / Fig S17 | "状态切换曲线" / "reconfiguration before/after" | Excel, CSV, Origin | Reversibility confirmation, mechanism identification (threshold shift vs. conductance change) |

### Priority P2 (Statistical Value)

| Raw Data Family | Which Paper Figure(s) | What Student Likely Calls It | Acceptable Formats | Simulator Quantity Extracted |
|:----------------|:----------------------|:-----------------------------|:-------------------|:-----------------------------|
| **Same-state repeated measurements** | (Not explicitly shown) | "重复测试" / "多次读写" / "endurance-like cycling" | Excel, CSV | `sigma_C2C` (cycle-to-cycle variation) |
| **Multi-device same-condition measurements** | (Not explicitly shown) | "批次器件测试" / "同条件多器件" / "uniformity check" | Excel, CSV | `sigma_D2D` (device-to-device variation) |
| **LTP/LTD pulse update curves** | (May be in raw data) | "LTP/LTD曲线" / "脉冲更新" / "potentiation/depression" | Excel, CSV | `NL_LTP`, `NL_LTD` (write nonlinearity) via conductance update vs. pulse number |

---

## Detailed Crosswalk by Simulator Parameter

### 1. G_min / G_max (Conductance Window)

**What to ask for**: 
> "多状态存储测试的原始数据，每个state的读数" (Fig S14)

**What we extract**:
- Minimum conductance (erased state) → `G_min`
- Maximum conductance (programmed state) → `G_max`
- Ratio → `G_max/G_min` window

**From papers**:
- WQY: Fig S14 shows 16-state and 64-state storage
- d5mh: Fig 3(i) shows initial/programmed/erased states

---

### 2. n_states (Stable Levels)

**What to ask for**: 
> "多状态存储里真正稳定的state数" (Fig S14)

**What we extract**:
- Count distinguishable, stable conductance levels
- Not just programmed states, but states that survive retention time

**From papers**:
- WQY: "16-state / 64-state" mentioned in Fig S14 caption

---

### 3. sigma_D2D (Device-to-Device Variation)

**What to ask for**: 
> "同批次多个器件，同样条件测同一个state的读数分布" (not explicitly shown, but natural extension)

**What we extract**:
- Standard deviation of conductance readings across multiple devices
- Same programming condition, different devices

**From papers**:
- Not explicitly shown; may need to request as "uniformity check" data

---

### 4. sigma_C2C (Cycle-to-Cycle Variation)

**What to ask for**: 
> "同一个state重复写/读30-50次的原始值" (not explicitly shown)

**What we extract**:
- Standard deviation of repeated programming to same target state
- Same device, same target, multiple cycles

**From papers**:
- Zhang 2025 proxy: "8-cycle repeatability" in Supp.Fig.15

---

### 5. tau_1, tau_2, A_0 (Retention Time Constants)

**What to ask for**: 
> "保持性/随时间演化的原始数据，编程态和擦除态" (Fig S13)

**What we extract**:
- Fit G(t) = A_0 * exp(-t/tau_1) + (1-A_0) * exp(-t/tau_2)
- Fast decay (tau_1 ~ 100ms) and slow decay (tau_2 ~ 1s)

**From papers**:
- WQY: Fig S13 "随时间演化的transfer curve"
- d5mh: Fig S13, S14 retention data
- Current manuscript: Vincze values (140ms, 610ms, A_0=0.6)

---

### 6. NL_LTP / NL_LTD (Write Nonlinearity)

**What to ask for**: 
> "LTP/LTD脉冲更新曲线，不同初始态" (not explicitly shown, but standard test)

**What we extract**:
- Conductance update vs. pulse number
- Fit nonlinearity parameter NL from pulse response

**From papers**:
- Not explicitly shown; may need to request as "脉冲更新特性"

---

### 7. gamma_phys (Photoresponse Nonlinearity)

**What to ask for**: 
> "不同光强下的响应曲线" (Fig S11)

**What we extract**:
- Photocurrent vs. illumination intensity
- Fit gamma from I ~ P^gamma relationship

**From papers**:
- WQY: Fig S11 "不同波长/光强 programming"
- Current manuscript: gamma=2.0 tested

---

## Doctor-Friendly Request Templates

### Short Version (WeChat/email)

> 我们现在不是要你帮我们算参数，而是想要你们最近这两篇文章里几组关键图背后的原始数据。
> 
> 最优先想要：
> 1. 多状态存储（16/64 state）原始数据  
> 2. 保持性/随时间演化的原始数据  
> 3. 不同波长、以及编程/擦除前后 transfer curve 原始数据  
> 4. 如果有：重复测试、多器件同条件测试  
> 
> excel、csv、Origin、仪器导出文本都可以，我们自己来提参数。

### Formal Version (Email attachment)

> We are developing a simulation framework to bridge device characterization and system-level deployment evaluation for organic optoelectronic arrays. To calibrate our models against real device behavior, we would greatly appreciate access to the underlying raw data (not just figures) from your recent papers:
> 
> Priority data:
> 1. Multi-state storage raw readouts (16-state / 64-state conductance levels)
> 2. Retention/decay curves (conductance vs. time for programmed/erased states)
> 3. Transfer curves under different wavelengths (254/365/425 nm) and illumination conditions
> 4. Programmed vs. erased state transfer curves
> 
> If available, we would also value:
> - Repeated measurements of the same state (cycle-to-cycle statistics)
> - Multi-device measurements under identical conditions (device-to-device statistics)
> 
> Formats: Excel (.xlsx), CSV (.csv), Origin (.opj), or instrument log files are all acceptable. We will perform parameter extraction internally.

---

## Simulator Integration Path

```
Raw Data (from PhD student)
    │
    ▼
profile_auto_fitter_gpt.py
    │
    ▼
JSON Profile (measured-device-calibrated)
    │
    ▼
Simulation Framework
    │
    ▼
Task-Level Accuracy / Energy Estimates
```

The `profile_auto_fitter_gpt.py` script already exists and is designed for exactly this workflow.

---

## Risk Assessment

| Data Type | Confidence Student Has It | Value to Simulator | Risk of Asking |
|:----------|:--------------------------|:-------------------|:---------------|
| Multi-state storage | **High** (Fig S14 shown) | Critical (G_min/G_max/n_states) | Low |
| Retention decay | **High** (Fig S13 shown) | Critical (tau_1/tau_2/A_0) | Low |
| Wavelength response | **High** (Fig S11 shown) | High (gamma_phys) | Low |
| Program/erase states | **High** (Fig 3(i) shown) | High (memory window) | Low |
| Repeated measurements | **Medium** (not shown but common) | High (sigma_C2C) | Medium |
| Multi-device data | **Medium** (not shown) | High (sigma_D2D) | Medium |
| LTP/LTD curves | **Low** (not shown) | Moderate (NL) | Higher |

---

## Recommendation

**Immediate action**: Request P0 data (multi-state, retention, wavelength, P/E states) using the short WeChat template. These are clearly present in the papers and highest value for simulator calibration.

**Follow-up**: Request P2 statistical data (repeated measurements, multi-device) as a second ask, acknowledging it may require additional testing.
