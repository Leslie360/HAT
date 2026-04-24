#!/usr/bin/env python3
"""Unit tests for dual-bug fix (branch swap + extraneous nl multiplier + second-order branch mapping)."""
import sys
import torch

sys.path.insert(0, ".")
from analog_layers import StraightThroughQuantize
from eval_fresh_instances_postfix import resolve_eval_overrides


def test_branch_swap_ltp():
    """grad_output < 0 (LTP update) must use ltp_scale."""
    x = torch.tensor([0.9], requires_grad=True)  # near top
    q = StraightThroughQuantize.apply(x, 16, 0.0, 1.0, 2.0, -2.0)
    
    grad_input = torch.autograd.grad(q, x, grad_outputs=torch.tensor([-1.0]), retain_graph=False)[0]
    
    assert abs(grad_input.item()) < 0.5, f"LTP at top should be suppressed, got {grad_input.item()}"
    print("✅ test_branch_swap_ltp passed")


def test_branch_swap_ltd():
    """grad_output > 0 (LTD update) must use ltd_scale."""
    x = torch.tensor([0.9], requires_grad=True)  # near top
    q = StraightThroughQuantize.apply(x, 16, 0.0, 1.0, 2.0, -2.0)
    
    grad_input = torch.autograd.grad(q, x, grad_outputs=torch.tensor([1.0]), retain_graph=False)[0]
    
    assert abs(grad_input.item() - 0.9) < 0.1, f"LTD at top should be ~0.9, got {grad_input.item()}"
    print("✅ test_branch_swap_ltd passed")


def test_no_extraneous_nl_multiplier():
    """Second-order coefficient must be -0.5 * (nl - 1), not nl * (nl - 1)."""
    with open("analog_layers.py") as f:
        src = f.read()
    
    assert "-0.5 * (nl_ltp - 1.0)" in src, "ltp_corr missing correct coefficient"
    assert "-0.5 * (nl_ltd - 1.0)" in src, "ltd_corr missing correct coefficient"
    assert "-0.5 * nl_ltp * (nl_ltp - 1.0)" not in src, "ltp_corr still has extraneous nl multiplier"
    assert "-0.5 * nl_ltd * (nl_ltd - 1.0)" not in src, "ltd_corr still has extraneous nl multiplier"
    print("✅ test_no_extraneous_nl_multiplier passed")


def test_first_order_no_multiplier():
    """First-order must remain no-multiplier: pow(ratio, nl-1)."""
    with open("analog_layers.py") as f:
        src = f.read()
    
    assert "torch.pow(ltp_ratio, nl_ltp - 1.0)" in src, "first-order LTP missing correct form"
    assert "torch.pow(ltd_ratio, nl_ltd - 1.0)" in src, "first-order LTD missing correct form"
    print("✅ test_first_order_no_multiplier passed")


def test_second_order_branch_matches_first_order():
    """
    TERTIARY BUG FIX VERIFICATION (commit 9cdbe77).
    
    The second-order correction must map gradients to the SAME physical
    direction as the first-order term:
      - grad_output >= 0  -> LTD (weight decrease) -> ltd_corr
      - grad_output < 0   -> LTP (weight increase) -> ltp_corr
    
    49cacef fixed first-order but left second-order inverted.
    """
    with open("analog_layers.py") as f:
        src = f.read()
    
    # Find the second-order correction line
    # It must map positive gradients to ltd_corr, not ltp_corr
    lines = src.split('\n')
    corr_line = None
    for i, line in enumerate(lines):
        if 'correction = alpha * torch.where(grad_output >= 0' in line:
            corr_line = line.strip()
            break
    
    assert corr_line is not None, "Could not find second-order correction line"
    
    # Verify the mapping: grad_output >= 0 -> ltd_corr, grad_output < 0 -> ltp_corr
    # The line should be: correction = alpha * torch.where(grad_output >= 0, grad_output * ltd_corr, grad_output * ltp_corr)
    assert "ltd_corr" in corr_line and "ltp_corr" in corr_line, "Missing ltd_corr or ltp_corr in correction"
    
    # Check order: the first branch (grad_output >= 0) must use ltd_corr
    # Split by comma to find the three parts of torch.where
    where_start = corr_line.find('torch.where(')
    where_args = corr_line[where_start + len('torch.where('):].rstrip(')')
    
    # Find which corr appears first in the arguments
    ltd_pos = where_args.find('ltd_corr')
    ltp_pos = where_args.find('ltp_corr')
    
    assert ltd_pos < ltp_pos, \
        f"Second-order branch mapping inverted: ltd_corr at {ltd_pos}, ltp_corr at {ltp_pos}. " \
        f"Positive gradients (LTD) must map to ltd_corr. Line: {corr_line}"
    
    print("✅ test_second_order_branch_matches_first_order passed")


def test_eval_provenance_rejects_silent_nl_mismatch():
    """Fresh eval must not silently reinterpret a checkpoint under different NL."""
    provenance = {
        "checkpoint_nl_ltp": 1.0,
        "checkpoint_nl_ltd": -1.0,
        "checkpoint_noise_mode": "proportional",
    }

    try:
        resolve_eval_overrides(
            provenance,
            nl_ltp=2.0,
            nl_ltd=-2.0,
            noise_mode="proportional",
            allow_eval_nl_override=False,
        )
    except ValueError as exc:
        assert "NL_LTP checkpoint=1.0 eval=2.0" in str(exc)
        assert "NL_LTD checkpoint=-1.0 eval=-2.0" in str(exc)
    else:
        raise AssertionError("Expected NL mismatch to be rejected")

    resolved = resolve_eval_overrides(
        provenance,
        nl_ltp=2.0,
        nl_ltd=-2.0,
        noise_mode="proportional",
        allow_eval_nl_override=True,
    )
    assert resolved[0] == 2.0 and resolved[1] == -2.0
    assert len(resolved[3]) == 2
    print("✅ test_eval_provenance_rejects_silent_nl_mismatch passed")


if __name__ == "__main__":
    test_branch_swap_ltp()
    test_branch_swap_ltd()
    test_no_extraneous_nl_multiplier()
    test_first_order_no_multiplier()
    test_second_order_branch_matches_first_order()
    test_eval_provenance_rejects_silent_nl_mismatch()
    print("\n🎉 All 6 tests passed!")
