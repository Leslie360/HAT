# R10H Energy Provenance Report

**Date:** 2026-04-25  
**Agent:** Kimi (R10H dispatch from Claude Round-10)  
**Task:** Find literature sources for the energy placeholder constants, or honestly label them as estimates.

---

## 1. Executive Summary

| Constant | Value | Verdict |
|:---|:---|:---|
| `E_analog_MAC` | 100 fJ | **Literature proxy** — anchored to Gebregiorgis et al. (2023) \cite{gebregiorgis2023organiccim}, but used generically |
| `E_ADC_8bit` | 25 fJ/conv | **Order-of-magnitude estimate** — median of CIM SAR-ADC range (10–30 fJ); no single bib entry |
| `E_DAC_8bit` | 30 fJ/conv | **Order-of-magnitude estimate** — referenced in internal notes to Li et al. (2022, TCAS-I), but that paper is **not in `refs_gpt.bib`** |

**Bottom line:** As expected, these are largely first-order analytical placeholders. Only `E_analog_MAC` has a direct literature anchor in the bibliography; the converter energies are median/proxy estimates without corresponding bib entries.

---

## 2. Search Methodology

1. **Code search:** Grepped `compute_vit/` for `100 fJ`, `25 fJ`, `30 fJ`, `E_analog_MAC`, `E_ADC_8bit`, `E_DAC_8bit`.
2. **Internal documentation:** Read `report_md/claude全栈参考手册.md` §2.2, §3.2 and `_archive/paper-drafts/参考文献库.md`.
3. **Bibliography audit:** Searched `paper/latex_gpt/refs_gpt.bib` (67 entries) for Gebregiorgis, Yoon, Zhang 2022, Li 2022.
4. **Review corpus:** Cross-checked hostile-review summaries and editorial advisories for prior complaints about these constants.

---

## 3. Per-Parameter Findings

### 3.1 `E_analog_MAC` = 100 fJ

- **Code location:** `compute_vit/analog_layers_ensemble.py:791`
- **Code comment:** `# 100 fJ (organic device)`
- **Internal doc (`claude全栈参考手册.md` §3.2):** "模拟MAC（有机器件） 100 fJ/MAC | Gebregiorgis 2023, 三端有机器件"
- **Bib entry:** `gebregiorgis2023organiccim` **exists** in `refs_gpt.bib` (IEEE TETC, 2023).
- **Provenance:** Gebregiorgis et al. report 100 fJ/MAC for a three-terminal organic device array, decomposed as 70 fJ (device) + 20 fJ (readout) + 10 fJ (digital).
- **Assessment:** This is a **literature proxy** — a real measured number from a specific organic technology, but applied generically as a placeholder for the target device in this framework. Prior review comments (hostile review, editorial advisory) correctly flagged it as a "placeholder constant without physical basis" in the sense that it is not calibrated to the authors' own fabricated devices.

### 3.2 `E_ADC_8bit` = 25 fJ/conversion

- **Code location:** `compute_vit/analog_layers_ensemble.py:793`
- **Code comment:** `# 25 fJ/conversion` (no further attribution)
- **Internal doc (`claude全栈参考手册.md` §2.2):** "Yoon 2025: 24.8fJ; Zhang 2022: 10.2fJ" → "多篇CIM论文中位数" (median of multiple CIM papers)
- **Bib entries:** **NO entries** for Yoon 2025 or Zhang 2022 in `refs_gpt.bib`.
- **Assessment:** This is an **order-of-magnitude estimate** — a rounded median drawn from a literature range. It is not anchored to a single citable source in the current bibliography. The value is plausible (falls within the 10–30 fJ range for 8-bit SAR ADCs in CIM contexts), but it is an engineering estimate, not a direct citation.

### 3.3 `E_DAC_8bit` = 30 fJ/conversion

- **Code location:** `compute_vit/analog_layers_ensemble.py:794`
- **Code comment:** `# 30 fJ/conversion` (no further attribution)
- **Internal doc (`claude全栈参考手册.md` §2.2):** "Li 2022估计" (Li 2022 estimate), "普遍高于ADC" (generally higher than ADC)
- **Internal doc (`参考文献库.md`):** Li et al. (2022, IEEE TCAS-I) report a full CIM breakdown of 136 fJ/MAC with DAC at 10 fJ under heavy sharing. The 30 fJ used here is a higher, architecture-agnostic estimate.
- **Bib entries:** The only `li2022*` entry in `refs_gpt.bib` is `li2022qvit` (Q-ViT, NeurIPS 2022), which is the **wrong paper**. The Li 2022 TCAS-I CIM paper is **NOT in the bibliography**.
- **Assessment:** This is an **order-of-magnitude estimate** without a direct literature citation in the bib. The internal notes reference a real paper, but that paper is absent from the reference list, so the 30 fJ value cannot be validated by a reader from the manuscript alone.

### 3.4 Auxiliary constants (for completeness)

| Parameter | Value | Provenance | Status |
|:---|:---|:---|:---|
| `E_digital_FP32_MAC` | 2.5 pJ | Horowitz 2014 + 28 nm scaling | Literature-derived (in bib) |
| `E_digital_INT8_MAC` | 0.4 pJ | Horowitz 2014 + 28 nm scaling | Literature-derived (in bib) |
| `E_SRAM_read` | 5 pJ | Horowitz 2014 | Literature-derived (in bib) |
| `E_DRAM_read` | 1300 pJ | Horowitz 2014 | Literature-derived (in bib) |
| `E_softmax_per_elem` | 15 pJ | Analytical estimate | Engineering estimate |
| `E_layernorm_per_elem` | 8 pJ | Analytical estimate | Engineering estimate |

---

## 4. Honest Assessment

> **The expected outcome from the dispatch was: "Most likely these are order-of-magnitude estimates without direct literature anchors."**
>
> This is **mostly confirmed**, with one nuance: `E_analog_MAC = 100 fJ` does have a direct literature anchor (Gebregiorgis 2023), but it is used as a generic proxy rather than a device-specific measurement. The converter energies (ADC 25 fJ, DAC 30 fJ) are indeed median/order-of-magnitude estimates without corresponding bibliography entries.

**Reviewer-risk analysis:**
- A hostile reviewer will correctly note that the ADC/DAC values are "not calibrated to any organic device."
- The defense is transparency: label them explicitly as "order-of-magnitude estimates" and frame the energy analysis as "relative comparison / design-space exploration," not "silicon power prediction."
- The existing sensitivity analysis (±30% parameter variation, 10–50% routing overhead) already supports this defense.

---

## 5. Paper-Safe Paragraph for Discussion

> Energy estimates use first-order analytical placeholders: $E_{\text{cell}} = 100~\text{fJ}$ is a literature proxy drawn from measured organic thin-film arrays (Gebregiorgis \textit{et al.}, 2023) and is intended as a generic order-of-magnitude bound rather than a device-specific calibration. $E_{\text{ADC}} = 25~\text{fJ}$ and $E_{\text{DAC}} = 30~\text{fJ}$ are SAR-converter proxies representing the central tendency of reported CIM peripherals; they are not tied to a single fabricated converter. These constants are intended for \emph{relative comparison} and design-space exploration, not routed-circuit prediction. Sensitivity analysis (Supplementary Note S-Energy) confirms that the ranking between analog and digital deployments is robust to $\pm 30\%$ variation in any single parameter and to $10$--$50\%$ unmodeled routing overhead.

---

## 6. Deliverables Produced

1. `compute_vit/paper/latex_gpt/supplementary/S_energy_provenance.tex` — Supplementary Note S-Energy with full provenance table and detailed notes.
2. `compute_vit/report_md/_gpt/KIMI_R10H_ENERGY_PROVENANCE_REPORT_20260425.md` — This report.

---

## 7. Recommendations (optional follow-up)

1. **Do not add fake bib entries** for Yoon 2025 or Zhang 2022 just to legitimize the 25 fJ ADC value. Instead, keep the honest "order-of-magnitude estimate" framing.
2. **If** the Li 2022 TCAS-I paper is deemed essential, add it to `refs_gpt.bib` as `li2022timemux` or similar and update the supplementary note. But this is low priority because the paper already disclaims absolute prediction.
3. The existing `horowitz2014computing` citation is solid and widely accepted; no action needed.
4. Ensure the main-text Discussion and Abstract use the paper-safe paragraph above (or equivalent) to inoculate against reviewer attacks on placeholder constants.
