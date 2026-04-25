import os
import re

def fix_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # Revert 1st order LTP (remove nl_ltp *)
    content = re.sub(
        r"ltp_scale = nl_ltp \* torch\.pow\(ltp_ratio, nl_ltp - 1\.0\)",
        r"ltp_scale = torch.pow(ltp_ratio, nl_ltp - 1.0)",
        content
    )
    
    # Revert 1st order LTD (remove nl_ltd *)
    content = re.sub(
        r"ltd_scale = nl_ltd \* torch\.pow\(ltd_ratio, nl_ltd - 1\.0\)",
        r"ltd_scale = torch.pow(ltd_ratio, nl_ltd - 1.0)",
        content
    )

    # Fix 2nd order LTP (remove nl_ltp * and ensure minus sign)
    # Match both the original positive one and my recent negative one just in case
    content = re.sub(
        r"ltp_corr = -?0\.5 \* nl_ltp \* \(nl_ltp - 1\.0\) \* torch\.pow\(ltp_ratio\.clamp_min\(eps\), nl_ltp - 2\.0\) \* delta_g",
        r"ltp_corr = -0.5 * (nl_ltp - 1.0) * torch.pow(ltp_ratio.clamp_min(eps), nl_ltp - 2.0) * delta_g",
        content
    )
    # Also handle if it was already positive without minus
    content = re.sub(
        r"ltp_corr = 0\.5 \* nl_ltp \* \(nl_ltp - 1\.0\) \* torch\.pow\(ltp_ratio\.clamp_min\(eps\), nl_ltp - 2\.0\) \* delta_g",
        r"ltp_corr = -0.5 * (nl_ltp - 1.0) * torch.pow(ltp_ratio.clamp_min(eps), nl_ltp - 2.0) * delta_g",
        content
    )

    # Fix 2nd order LTD (remove nl_ltd * but keep positive sign)
    content = re.sub(
        r"ltd_corr = 0\.5 \* nl_ltd \* \(nl_ltd - 1\.0\) \* torch\.pow\(ltd_ratio\.clamp_min\(eps\), nl_ltd - 2\.0\) \* delta_g",
        r"ltd_corr = 0.5 * (nl_ltd - 1.0) * torch.pow(ltd_ratio.clamp_min(eps), nl_ltd - 2.0) * delta_g",
        content
    )

    with open(filepath, "w") as f:
        f.write(content)

fix_file("compute_vit/analog_layers.py")
if os.path.exists("compute_vit/analog_layers_ensemble.py"):
    fix_file("compute_vit/analog_layers_ensemble.py")

print("Math fixed in source files.")
