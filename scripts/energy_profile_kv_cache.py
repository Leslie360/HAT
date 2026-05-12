#!/usr/bin/env python3
"""Energy/area/latency profiling for analog vs digital KV cache."""
import json
import os

OUT_DIR = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107"

# ---------------------------------------------------------------------------
# Model configs (Pythia family, MHA — no GQA)
# ---------------------------------------------------------------------------
MODELS = {
    "pythia-410m":  {"layers": 24, "hidden": 1024, "heads": 16, "head_dim": 64,  "params": 0.41},
    "pythia-1b":    {"layers": 24, "hidden": 2048, "heads": 16, "head_dim": 128, "params": 1.0},
    "pythia-2.8b":  {"layers": 32, "hidden": 2560, "heads": 32, "head_dim": 80,  "params": 2.8},
    "pythia-6.9b":  {"layers": 32, "hidden": 4096, "heads": 32, "head_dim": 128, "params": 6.9},
}

# ---------------------------------------------------------------------------
# Technology parameters (representative literature values)
# ---------------------------------------------------------------------------
TECH = {
    "digital_fp16": {
        "bits_per_param": 16,
        "cell_area_f2": 140,           # 6T SRAM ~ 140 F^2
        "mac_energy_pj": 0.4,          # NVIDIA A100-ish digital MAC
        "read_energy_pj_per_bit": 1.0, # SRAM read
    },
    "analog_rram": {
        "bits_per_param": 8,           # HAT uses 256 states ≈ 8-bit effective
        "cell_area_f2": 10,            # 1T1R RRAM ~ 10 F^2
        "mac_energy_pj": 0.1,          # RRAM CIM ~ 100 fJ = 0.1 pJ
        "read_energy_pj_per_bit": 0.1, # RRAM read
        "adc_energy_pj_per_conversion": 0.5,  # SAR ADC estimate
    },
    "analog_pcm": {
        "bits_per_param": 8,
        "cell_area_f2": 12,
        "mac_energy_pj": 0.15,
        "read_energy_pj_per_bit": 0.15,
        "adc_energy_pj_per_conversion": 0.5,
    },
    "analog_fefet": {
        "bits_per_param": 8,
        "cell_area_f2": 8,
        "mac_energy_pj": 0.08,
        "read_energy_pj_per_bit": 0.08,
        "adc_energy_pj_per_conversion": 0.5,
    },
}

F_NM = 14  # representative process node (14 nm)


def kv_cache_size(model_cfg, seq_len):
    """KV cache size in MB for a single sequence."""
    l = model_cfg["layers"]
    h = model_cfg["heads"]
    d = model_cfg["head_dim"]
    params = l * h * 2 * d  # K + V
    bytes_fp16 = params * 2
    return bytes_fp16 * seq_len / (1024 ** 2)


def area_mm2(model_cfg, tech_key):
    """Array area for storing full KV cache of one token."""
    l = model_cfg["layers"]
    h = model_cfg["heads"]
    d = model_cfg["head_dim"]
    params_per_token = l * h * 2 * d
    bits = params_per_token * TECH[tech_key]["bits_per_param"]
    area_f2 = bits * TECH[tech_key]["cell_area_f2"]
    area_nm2 = area_f2 * (F_NM ** 2)
    return area_nm2 / 1e12  # mm^2


def attention_macs(model_cfg, seq_len):
    """MAC ops for one attention layer (QK^T + softmax-weighted V)."""
    h = model_cfg["heads"]
    d = model_cfg["head_dim"]
    # QK^T:  h × L × D  dot  h × D × L  →  h × L × L  =  h*L*L*D MACs
    # Softmax-weighted V: h × L × L  ×  h × L × D  →  h × L × D  =  h*L*L*D MACs
    return 2 * h * (seq_len ** 2) * d


def profile():
    results = []
    seq_lens = [512, 2048]

    for mname, mcfg in MODELS.items():
        for seq_len in seq_lens:
            kv_mb = kv_cache_size(mcfg, seq_len)

            # Digital baseline
            dig_area = area_mm2(mcfg, "digital_fp16")
            dig_macs = attention_macs(mcfg, seq_len)
            dig_mac_nj = dig_macs * TECH["digital_fp16"]["mac_energy_pj"]
            dig_read_nj = kv_mb * 1024 * 1024 * 8 * TECH["digital_fp16"]["read_energy_pj_per_bit"]

            row = {
                "model": mname,
                "seq_len": seq_len,
                "kv_cache_mb": round(kv_mb, 2),
                "digital": {
                    "area_mm2": round(dig_area, 4),
                    "attention_mac_ops": dig_macs,
                    "attention_energy_nj": round(dig_mac_nj, 2),
                    "kv_read_energy_nj": round(dig_read_nj, 2),
                    "total_energy_nj": round(dig_mac_nj + dig_read_nj, 2),
                },
            }

            for tech in ["analog_rram", "analog_pcm", "analog_fefet"]:
                tname = tech.replace("analog_", "")
                ana_area = area_mm2(mcfg, tech)
                ana_macs = dig_macs  # same op count, different energy
                ana_mac_nj = ana_macs * TECH[tech]["mac_energy_pj"]
                # Analog CIM avoids explicit KV read; energy dominated by MAC + ADC
                # One ADC per attention score (L scores per head) + one per output vector
                adc_ops = seq_len * mcfg["heads"] * 2  # QK^T scores + weighted-V outputs
                adc_nj = adc_ops * TECH[tech]["adc_energy_pj_per_conversion"]
                ana_total_nj = ana_mac_nj + adc_nj

                row[tname] = {
                    "area_mm2": round(ana_area, 4),
                    "attention_mac_ops": ana_macs,
                    "attention_energy_nj": round(ana_mac_nj, 2),
                    "adc_energy_nj": round(adc_nj, 2),
                    "total_energy_nj": round(ana_total_nj, 2),
                    "energy_reduction_vs_digital": round((dig_mac_nj + dig_read_nj) / ana_total_nj, 2),
                    "area_reduction_vs_digital": round(dig_area / ana_area, 2),
                }

            results.append(row)

    # Summary table
    print("# Energy / Area Profiling: Analog vs Digital KV Cache\n")
    print("| Model | Seq Len | KV Cache (MB) | Digital Area (mm²) | RRAM Area (mm²) | RRAM Energy Reduction | FeFET Energy Reduction |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    for r in results:
        print(f"| {r['model']} | {r['seq_len']} | {r['kv_cache_mb']} | {r['digital']['area_mm2']} | {r['rram']['area_mm2']} | {r['rram']['energy_reduction_vs_digital']}× | {r['fefet']['energy_reduction_vs_digital']}× |")

    print("\n## Key Assumptions")
    print(f"- Process node: {F_NM} nm")
    print("- Digital MAC energy: 0.4 pJ (A100-class GPU)")
    print("- RRAM CIM MAC energy: 0.1 pJ (100 fJ)")
    print("- FeFET CIM MAC energy: 0.08 pJ (80 fJ)")
    print("- ADC energy: 0.5 pJ/conversion (8-bit SAR ADC)")
    print("- Analog effective precision: 8-bit (256 states)")
    print("- Digital storage: FP16 (16-bit) in SRAM")

    out_path = os.path.join(OUT_DIR, "energy_profile_kv_cache.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {out_path}")


if __name__ == "__main__":
    profile()
