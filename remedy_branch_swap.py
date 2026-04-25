import os
import re

def fix_logic(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, "r") as f:
        content = f.read()

    # 1. Fix the Branch Swap (The most critical fix)
    # Target: grad_input = torch.where(grad_output >= 0, grad_output * ltp_scale, grad_output * ltd_scale)
    # Correct: grad_output >= 0 (Decrease) -> ltd_scale; grad_output < 0 (Increase) -> ltp_scale
    old_swap = r"grad_input = torch\.where\(grad_output >= 0, grad_output \* ltp_scale, grad_output \* ltd_scale\)"
    new_swap = r"grad_input = torch.where(grad_output >= 0, grad_output * ltd_scale, grad_output * ltp_scale)"
    
    if re.search(old_swap, content):
        content = re.sub(old_swap, new_swap, content)
        print(f"Fixed branch swap in {filepath}")
    else:
        print(f"Branch swap not found or already fixed in {filepath}")

    # 2. Fix the Second-Order Coefficient (Removing redundant nl_ltp/nl_ltd multipliers)
    # The derivative of S(u) = u^(nl-1) is (nl-1)*u^(nl-2), NOT nl*(nl-1)*u^(nl-2)
    # Matches Gemini Ruling 2026-04-23
    
    # LTP Correction
    old_ltp_corr = r"ltp_corr = -0\.5 \* nl_ltp \* \(nl_ltp - 1\.0\) \* torch\.pow\(ltp_ratio\.clamp_min\(eps\), nl_ltp - 2\.0\) \* delta_g"
    new_ltp_corr = r"ltp_corr = -0.5 * (nl_ltp - 1.0) * torch.pow(ltp_ratio.clamp_min(eps), nl_ltp - 2.0) * delta_g"
    
    # LTD Correction
    old_ltd_corr = r"ltd_corr = -0\.5 \* nl_ltd \* \(nl_ltd - 1\.0\) \* torch\.pow\(ltd_ratio\.clamp_min\(eps\), nl_ltd - 2\.0\) \* delta_g"
    new_ltd_corr = r"ltd_corr = -0.5 * (nl_ltd - 1.0) * torch.pow(ltd_ratio.clamp_min(eps), nl_ltd - 2.0) * delta_g"

    content = re.sub(old_ltp_corr, new_ltp_corr, content)
    content = re.sub(old_ltd_corr, new_ltd_corr, content)
    
    # Also handle the logic for the second order correction in the torch.where
    # If branches were swapped in grad_input, they must be swapped in the correction too
    old_corr_apply = r"correction = alpha \* torch\.where\(grad_output >= 0, grad_output \* ltp_corr, grad_output \* ltd_corr\)"
    new_corr_apply = r"correction = alpha * torch.where(grad_output >= 0, grad_output * ltd_corr, grad_output * ltp_corr)"
    
    if re.search(old_corr_apply, content):
        content = re.sub(old_corr_apply, new_corr_apply, content)
        print(f"Fixed correction branch swap in {filepath}")

    with open(filepath, "w") as f:
        f.write(content)

fix_logic("compute_vit/analog_layers.py")
fix_logic("compute_vit/analog_layers_ensemble.py")

print("Remediation complete.")
