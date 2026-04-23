from typing import Union
#!/usr/bin/env python3
"""
Phase A1.2: Physical-Aware Analog Layers for Crossbar Array Simulation

Implements AnalogLinear (replacement for nn.Linear) with:
  - Weight quantization to discrete conductance states (differential pair)
  - Cycle-to-cycle (C2C) noise: re-sampled every forward pass
  - Device-to-device (D2D) noise: fixed at initialization
  - Double-exponential retention decay
  - Straight-Through Estimator (STE) for gradient through quantization

All default parameters from: claude全栈参考手册.md Chapter 2

Reference:
  - Quantization & mapping: §1.3 (differential pair scheme)
  - Device physics: §2.1 (n_states, G range, NL, noise, retention)
  - Noise model: §2.1 W_noisy = W + N(0, σ_D2D²), W_inference = W_noisy + N(0, σ_C2C²)
  - Retention: §2.1 G(t) = G₀ × [A₁·exp(-t/τ₁) + A₂·exp(-t/τ₂) + A₀]

These layers are the building blocks for the hybrid models evaluated in Fig. 4.
"""

import copy
import math
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

import torch
import torch.nn as nn
import torch.nn.functional as F

from amp_utils import autocast_disabled_context
from tinyvit_hybrid_utils import classify_tinyvit_layer


# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────

@dataclass
class AnalogLinearConfig:
    """Device physics parameters for organic optoelectronic synaptic transistor.

    All defaults from claude全栈参考手册.md §2.1 (标准值 column).
    """
    # Quantization
    n_states: int = 16          # 4-bit, 16 discrete conductance levels
    G_min: float = 1.0          # minimum conductance (a.u.)
    G_max: float = 10.0         # maximum conductance (a.u.), dynamic range 10×

    # Non-linearity (for future HAT weight update modeling)
    NL_LTP: float = 1.0         # Long-term potentiation non-linearity
    NL_LTD: float = -1.0        # Long-term depression non-linearity

    # Higher-order surrogate (CX-J1d)
    use_second_order_ste: bool = False  # Enable 2nd-order Taylor-corrected STE
    delta_g_eff: float = 0.0            # Effective perturbation scale for curvature correction
    second_order_alpha: float = 1.0     # Scalar multiplier on the 2nd-order correction term

    # Noise
    sigma_c2c: float = 0.05     # 5% cycle-to-cycle noise (re-sampled per forward)
    sigma_d2d: float = 0.10     # 10% device-to-device noise (fixed at init)
    noise_mode: str = "uniform"  # uniform: sigma*G_range, proportional: sigma*|G_current|

    # Retention (double exponential decay)
    retention_enabled: bool = False
    tau_1: float = 0.14         # seconds (short-term component)
    tau_2: float = 0.61         # seconds (long-term component)
    A_0: float = 0.6            # persistent fraction
    inference_time: float = 0.0  # seconds since programming
    retention_recalibrate_scale: bool = False  # recompute digital scale after retention decay
    retention_scales_d2d: bool = False  # decay stored D2D conductance mismatch with the same factor
    retention_state_dependent: bool = False  # high-conductance states decay faster

    # Control flags
    noise_enabled: bool = True   # Master switch for noise injection
    restore_weight_scale: bool = False  # Recover digital weight scale after conductance-domain ops
    asymmetry_factor: float = 0.0  # Asymmetry between G_pos and G_neg (0.0 to 1.0)
    ir_drop_factor: float = 0.0    # IR drop factor (0.0 to 0.03)
    sneak_factor: float = 0.0      # Sneak path factor (0.0 to 0.02)
    inl_table: Optional[torch.Tensor] = None  # Non-uniform conductance lookup table

    def __post_init__(self):
        self.noise_mode = str(self.noise_mode).lower().strip()
        if not (-1.0 < self.asymmetry_factor < 1.0):
             raise ValueError(f"AnalogLinearConfig.asymmetry_factor must be in (-1, 1), got {self.asymmetry_factor}")
        if not (0.0 <= self.ir_drop_factor <= 1.0):
             raise ValueError(f"AnalogLinearConfig.ir_drop_factor must be in [0, 1], got {self.ir_drop_factor}")
        if not (0.0 <= self.sneak_factor <= 1.0):
             raise ValueError(f"AnalogLinearConfig.sneak_factor must be in [0, 1], got {self.sneak_factor}")
        if self.n_states < 2:
            raise ValueError(f"AnalogLinearConfig.n_states must be >= 2, got {self.n_states}")
        if self.G_min <= 0:
            raise ValueError(f"AnalogLinearConfig.G_min must be > 0, got {self.G_min}")
        if self.G_max <= self.G_min:
            raise ValueError(
                f"AnalogLinearConfig.G_max must be > G_min ({self.G_min}), got {self.G_max}"
            )
        if self.sigma_c2c < 0 or self.sigma_d2d < 0:
            raise ValueError("AnalogLinearConfig sigma_c2c and sigma_d2d must be non-negative")
        if self.second_order_alpha < 0:
            raise ValueError(
                f"AnalogLinearConfig.second_order_alpha must be >= 0, got {self.second_order_alpha}"
            )
        # Warn if second-order STE is requested but delta_g_eff is non-positive,
        # because backward() silently skips the correction when delta_g_eff <= 0.
        if self.use_second_order_ste and self.delta_g_eff <= 0.0:
            import warnings
            warnings.warn(
                f"AnalogLinearConfig: use_second_order_ste=True but delta_g_eff={self.delta_g_eff} "
                f"(must be > 0 for the second-order correction to activate).",
                RuntimeWarning,
                stacklevel=2,
            )
        if self.noise_mode not in {"uniform", "proportional"}:
            raise ValueError(
                f"AnalogLinearConfig.noise_mode must be 'uniform' or 'proportional', got {self.noise_mode}"
            )
        if self.tau_1 <= 0 or self.tau_2 <= 0:
            raise ValueError(
                f"AnalogLinearConfig.tau_1 and tau_2 must be > 0, got {self.tau_1}, {self.tau_2}"
            )
        if not (0.0 <= self.A_0 <= 1.0):
            raise ValueError(f"AnalogLinearConfig.A_0 must be in [0, 1], got {self.A_0}")
        if self.inference_time < 0:
            raise ValueError(
                f"AnalogLinearConfig.inference_time must be >= 0, got {self.inference_time}"
            )
        if self.inl_table is not None:
            table = torch.as_tensor(self.inl_table, dtype=torch.float32)
            if table.ndim != 1 or table.numel() < 2:
                raise ValueError("AnalogLinearConfig.inl_table must be a 1D tensor/list with >= 2 entries")
            if not torch.isfinite(table).all():
                raise ValueError("AnalogLinearConfig.inl_table must contain only finite values")
            if not bool(torch.all(table[1:] > table[:-1]).item()):
                raise ValueError("AnalogLinearConfig.inl_table must be strictly increasing")
            self.inl_table = table.clone()


def _require_positive_int(name: str, value: int):
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{name} must be a positive integer, got {value!r}")


def _normalize_positive_2tuple(name: str, value, allow_zero: bool = False):
    if isinstance(value, tuple):
        items = value
    else:
        items = (value, value)
    if len(items) != 2:
        raise ValueError(f"{name} must be an int or 2-tuple, got {value!r}")
    normalized = []
    for item in items:
        if not isinstance(item, int):
            raise ValueError(f"{name} entries must be integers, got {value!r}")
        if allow_zero:
            if item < 0:
                raise ValueError(f"{name} entries must be >= 0, got {value!r}")
        elif item <= 0:
            raise ValueError(f"{name} entries must be > 0, got {value!r}")
        normalized.append(item)
    return tuple(normalized)


# ─────────────────────────────────────────────
# Straight-Through Estimator for quantization
# ─────────────────────────────────────────────

class StraightThroughQuantize(torch.autograd.Function):
    """Uniform quantization with STE gradient passthrough.

    Forward: clamp → normalize to [0,1] → round to n_levels → denormalize
    Backward: scaled STE (Branch A semantics).

    Branch A note:
      The first-order gradient scaling uses (ratio)^(NL-1) **without** an NL
      multiplier. This matches paper Equation S2 (paper/latex_gpt/supplementary.tex).
      The absence of the NL prefactor is intentional: the surrogate scales the
      STE by the normalized conductance position, modeling state-dependent update
      difficulty, rather than by the strict derivative of a power-law f(G)=G^NL.
    """

    @staticmethod
    def forward(ctx, x: torch.Tensor, n_levels: int,
                x_min: float, x_max: float,
                nl_ltp: float = 1.0, nl_ltd: float = -1.0,
                inl_table: Optional[torch.Tensor] = None,
                use_second_order_ste: bool = False,
                delta_g_eff: float = 0.0,
                second_order_alpha: float = 1.0) -> torch.Tensor:
        eps = 1e-8
        scale = x_max - x_min + eps
        # Clamp to valid range
        x_clamped = torch.clamp(x, x_min, x_max)
        ctx.save_for_backward(x_clamped)
        ctx.x_min = float(x_min)
        ctx.x_max = float(x_max)
        ctx.nl_ltp = float(nl_ltp)
        ctx.nl_ltd = float(nl_ltd)
        ctx.use_second_order_ste = bool(use_second_order_ste)
        ctx.delta_g_eff = float(delta_g_eff)
        ctx.second_order_alpha = float(second_order_alpha)

        if inl_table is not None:
            # Nearest-neighbor lookup in the INL table.
            # Assume inl_table is a 1D tensor of shape [n_levels].
            # We must find the index that minimizes |x_clamped - inl_table[i]|.
            # Reshape for broadcasting
            # x_clamped: [*, 1], inl_table: [1, n_levels]
            x_flat = x_clamped.flatten()
            # This can be memory-intensive for large tensors.
            # Using torch.bucketize or similar might be better if inl_table is sorted.
            # If not sorted, we can use:
            dist = torch.abs(x_flat.unsqueeze(1) - inl_table.unsqueeze(0))
            indices = torch.argmin(dist, dim=1)
            x_quant_flat = inl_table[indices]
            return x_quant_flat.view_as(x_clamped)
        else:
            # Normalize to [0, 1]
            x_norm = (x_clamped - x_min) / scale
            # Quantize to n_levels discrete values
            x_quant = torch.round(x_norm * (n_levels - 1)) / (n_levels - 1)
            # Denormalize back to [x_min, x_max]
            return x_quant * scale + x_min

    @staticmethod
    def backward(ctx, grad_output: torch.Tensor):
        (x_clamped,) = ctx.saved_tensors
        x_min = ctx.x_min
        x_max = ctx.x_max
        nl_ltp = abs(ctx.nl_ltp)
        nl_ltd = abs(ctx.nl_ltd)

        grad_input = grad_output
        eps = 1e-8
        conductance_span = max(x_max - x_min, eps)

        # Branch A first-order STE scaling (paper/latex_gpt/supplementary.tex Equation S2):
        #   The surrogate scales the STE by the normalized conductance position
        #   (ratio)^(NL-1), modeling state-dependent update difficulty.  There is
        #   **no** NL prefactor — this is an intentional behavioral proxy, not the
        #   strict derivative of f(G)=G^NL.
        #
        # Backward compatibility:
        #   NL=1.0 is identity;
        #   NL=0.0 is also treated as "no nonlinearity requested" for idealized profiles.
        if not (math.isclose(nl_ltp, 1.0, rel_tol=0.0, abs_tol=1e-8) or math.isclose(nl_ltp, 0.0, rel_tol=0.0, abs_tol=1e-8)):
            ltp_ratio = ((x_max - x_clamped) / conductance_span).clamp_min(eps)
            ltp_scale = torch.pow(ltp_ratio, nl_ltp - 1.0)
        else:
            ltp_scale = torch.ones_like(grad_output)

        if not (math.isclose(nl_ltd, 1.0, rel_tol=0.0, abs_tol=1e-8) or math.isclose(nl_ltd, 0.0, rel_tol=0.0, abs_tol=1e-8)):
            ltd_ratio = ((x_clamped - x_min) / conductance_span).clamp_min(eps)
            ltd_scale = torch.pow(ltd_ratio, nl_ltd - 1.0)
        else:
            ltd_scale = torch.ones_like(grad_output)

        grad_input = torch.where(grad_output >= 0, grad_output * ltd_scale, grad_output * ltp_scale)

        # Second-order Taylor correction (CX-J1d)
        if getattr(ctx, 'use_second_order_ste', False) and getattr(ctx, 'delta_g_eff', 0.0) > 0.0:
            delta_g = ctx.delta_g_eff
            alpha = getattr(ctx, 'second_order_alpha', 1.0)
            # Second-order "brake" correction (CX-J1d):
            #   This term applies a negative correction based on the first derivative
            #   of the scaling factor S(u), not the second derivative of a power-law.
            #   The negative sign acts as a brake, preventing the optimizer from
            #   driving weights into the conductance bounds.
            if not (math.isclose(nl_ltp, 1.0, rel_tol=0.0, abs_tol=1e-8) or math.isclose(nl_ltp, 0.0, rel_tol=0.0, abs_tol=1e-8)):
                ltp_corr = -0.5 * (nl_ltp - 1.0) * torch.pow(ltp_ratio.clamp_min(eps), nl_ltp - 2.0) * delta_g
            else:
                ltp_corr = torch.zeros_like(grad_output)

            if not (math.isclose(nl_ltd, 1.0, rel_tol=0.0, abs_tol=1e-8) or math.isclose(nl_ltd, 0.0, rel_tol=0.0, abs_tol=1e-8)):
                ltd_corr = -0.5 * (nl_ltd - 1.0) * torch.pow(ltd_ratio.clamp_min(eps), nl_ltd - 2.0) * delta_g
            else:
                ltd_corr = torch.zeros_like(grad_output)

            # Map the second-order correction to the same physical update
            # direction as the first-order branch: positive gradient -> LTD,
            # negative gradient -> LTP.
            correction = alpha * torch.where(grad_output >= 0, grad_output * ltd_corr, grad_output * ltp_corr)
            grad_input = grad_input + correction

        # No gradient for quantizer hyperparameters.
        return grad_input, None, None, None, None, None, None, None, None, None


def ste_quantize(x: torch.Tensor, n_levels: int,
                 x_min: float, x_max: float,
                 nl_ltp: float = 1.0, nl_ltd: float = -1.0,
                 inl_table: Optional[torch.Tensor] = None,
                 use_second_order_ste: bool = False,
                 delta_g_eff: float = 0.0,
                 second_order_alpha: float = 1.0) -> torch.Tensor:
    """Convenience wrapper for StraightThroughQuantize."""
    return StraightThroughQuantize.apply(x, n_levels, x_min, x_max, nl_ltp, nl_ltd, inl_table,
                                         use_second_order_ste, delta_g_eff, second_order_alpha)


def _init_sparsity_state(module: nn.Module):
    module.track_sparsity = False
    module._sparsity_relative_accum = 0.0
    module._sparsity_absolute_accum = 0.0
    module._sparsity_count = 0
    module._sparsity_last_relative = 0.0
    module._sparsity_last_absolute = 0.0
    module._sparsity_relative_scale = 0.01
    module._sparsity_absolute_threshold = 0.01


def _record_input_sparsity(module: nn.Module, x: torch.Tensor):
    if not getattr(module, "track_sparsity", False):
        return
    x_abs = x.detach().abs()
    max_val = float(x_abs.max().item()) if x_abs.numel() > 0 else 0.0
    relative_threshold = (
        getattr(module, "_sparsity_relative_scale", 0.01) * max_val if max_val > 0.0 else 1e-6
    )
    absolute_threshold = getattr(module, "_sparsity_absolute_threshold", 0.01)

    relative_zero_frac = (x_abs < relative_threshold).float().mean().item()
    absolute_zero_frac = (x_abs < absolute_threshold).float().mean().item()

    module._sparsity_relative_accum += relative_zero_frac
    module._sparsity_absolute_accum += absolute_zero_frac
    module._sparsity_count += 1
    module._sparsity_last_relative = relative_zero_frac
    module._sparsity_last_absolute = absolute_zero_frac


def _sample_d2d_noise(reference: torch.Tensor, sigma_d2d: float, G_range: float) -> torch.Tensor:
    if sigma_d2d <= 0.0 or G_range <= 0.0:
        return torch.zeros_like(reference)
    return torch.randn_like(reference) * sigma_d2d * G_range


def _scaled_noise_from_reference(noise_source: torch.Tensor,
                                 reference: torch.Tensor,
                                 sigma: float,
                                 G_range: float,
                                 noise_mode: str,
                                 is_fixed_pattern: bool = False) -> torch.Tensor:
    if sigma <= 0.0:
        return torch.zeros_like(reference)

    mode = str(noise_mode or "uniform").lower()
    if mode == "uniform":
        base = noise_source if is_fixed_pattern else torch.randn_like(reference)
        return base if is_fixed_pattern else base * sigma * G_range

    if mode == "proportional":
        eps = 1e-8
        magnitude = reference.abs().clamp_min(eps)
        if is_fixed_pattern:
            pattern = noise_source / max(G_range, eps)
            return pattern * magnitude
        return torch.randn_like(reference) * sigma * magnitude

    raise ValueError(f"Unsupported noise_mode='{noise_mode}'. Expected 'uniform' or 'proportional'.")


def _retention_decay_factor(cfg: AnalogLinearConfig, G: Optional[torch.Tensor] = None) -> Union[float, torch.Tensor]:
    if not cfg.retention_enabled or cfg.inference_time <= 0:
        return 1.0
    A_0 = cfg.A_0
    A_1 = (1.0 - A_0) / 2.0
    A_2 = A_1
    t = cfg.inference_time
    
    if G is not None:
        # State-dependent acceleration: High G states decay up to 20% faster
        G_norm = (G - cfg.G_min) / (cfg.G_max - cfg.G_min + 1e-9)
        state_factor = 1.0 + 0.2 * G_norm.clamp(0, 1)
        # We use torch.exp for tensor operations
        return (
            A_1 * torch.exp(-t / (cfg.tau_1 / state_factor))
            + A_2 * torch.exp(-t / (cfg.tau_2 / state_factor))
            + A_0
        )

    t_tensor = torch.as_tensor(t)
    return (
        A_1 * torch.exp(-t_tensor / cfg.tau_1)
        + A_2 * torch.exp(-t_tensor / cfg.tau_2)
        + A_0
    ).item() if not isinstance(t, torch.Tensor) else (
        A_1 * torch.exp(-t / cfg.tau_1)
        + A_2 * torch.exp(-t / cfg.tau_2)
        + A_0
    )


# ─────────────────────────────────────────────
# AnalogLinear Module
# ─────────────────────────────────────────────

class AnalogLinear(nn.Module):
    """Drop-in replacement for nn.Linear with analog crossbar simulation.

    Simulates the full physical pipeline:
      float weight → differential pair (G⁺, G⁻) → quantize → D2D noise → C2C noise
      → optional retention decay → VMM → output

    During HAT training:
      - Quantization uses STE for gradient flow
      - D2D noise is fixed for entire training run
      - C2C noise is re-sampled every forward (stochastic regularization)
      - Retention is OFF

    During inference:
      - Same pipeline; C2C can be toggled for Monte Carlo evaluation
      - Retention can be enabled to simulate post-programming degradation
    """

    def __init__(self, in_features: int, out_features: int,
                 bias: bool = True, config: Optional[AnalogLinearConfig] = None):
        super().__init__()
        _require_positive_int("in_features", in_features)
        _require_positive_int("out_features", out_features)
        self.in_features = in_features
        self.out_features = out_features
        self.config = copy.copy(config) if config is not None else AnalogLinearConfig()

        # Learnable weight (same as nn.Linear)
        self.weight = nn.Parameter(torch.empty(out_features, in_features))
        if bias:
            self.bias = nn.Parameter(torch.empty(out_features))
        else:
            self.register_parameter('bias', None)

        # D2D noise: sampled once, fixed forever (σ relative to G_range)
        # Physical meaning: manufacturing variation between devices on the crossbar
        G_range = self.config.G_max - self.config.G_min
        self.register_buffer(
            'd2d_noise',
            torch.randn(out_features, in_features) * self.config.sigma_d2d * G_range
        )
        _init_sparsity_state(self)

        # Initialize weights (Kaiming uniform, same as nn.Linear)
        self._reset_parameters()

    def _reset_parameters(self):
        nn.init.kaiming_uniform_(self.weight, a=math.sqrt(5))
        if self.bias is not None:
            fan_in = self.in_features
            bound = 1 / math.sqrt(fan_in)
            nn.init.uniform_(self.bias, -bound, bound)

    def resample_d2d_noise(self):
        """Draw a new fixed D2D noise pattern for this layer."""
        with torch.no_grad():
            G_range = self.config.G_max - self.config.G_min
            self.d2d_noise.copy_(_sample_d2d_noise(self.d2d_noise, self.config.sigma_d2d, G_range))

    def _weight_to_conductance(self, W: torch.Tensor):
        """Map float weights to quantized differential conductance pair.

        Flow (per handbook §1.3):
          1. Split W into W⁺ = max(W, 0) and W⁻ = max(-W, 0)
          2. Normalize each to [0, 1] using detached max(|W|)
          3. Map to [G_min, G_max]
          4. Quantize to n_states discrete levels via STE
        """
        cfg = self.config
        eps = 1e-8

        # Quantization-sensitive mapping stays in float32 under AMP.
        with autocast_disabled_context(W.device.type):
            W_fp32 = W.float()

            # Split into positive and negative parts
            W_pos = torch.clamp(W_fp32, min=0.0)
            W_neg = torch.clamp(-W_fp32, min=0.0)

            # Normalize by max absolute weight (detached to avoid gradient through normalizer)
            w_abs_max = W_fp32.abs().max().detach() + eps
            W_pos_norm = W_pos / w_abs_max  # in [0, 1]
            W_neg_norm = W_neg / w_abs_max  # in [0, 1]

            # Map to conductance range [G_min, G_max]
            G_range = cfg.G_max - cfg.G_min
            G_pos = cfg.G_min + W_pos_norm * G_range
            G_neg = cfg.G_min + W_neg_norm * G_range

            # Quantize to discrete conductance levels
            G_pos = ste_quantize(G_pos, cfg.n_states, cfg.G_min, cfg.G_max, cfg.NL_LTP, cfg.NL_LTD, cfg.inl_table, cfg.use_second_order_ste, cfg.delta_g_eff, cfg.second_order_alpha)
            G_neg = ste_quantize(G_neg, cfg.n_states, cfg.G_min, cfg.G_max, cfg.NL_LTP, cfg.NL_LTD, cfg.inl_table, cfg.use_second_order_ste, cfg.delta_g_eff, cfg.second_order_alpha)

            # Apply asymmetry (if any) with offset correction
            if cfg.asymmetry_factor != 0.0:
                G_pos = G_pos * (1.0 + cfg.asymmetry_factor)
                G_neg = G_neg * (1.0 - cfg.asymmetry_factor)
                # Subtract the constant DC bias: G_min*(1+alpha) - G_min*(1-alpha) = 2*G_min*alpha
                offset = 2.0 * cfg.G_min * cfg.asymmetry_factor
                G_pos = G_pos - offset

            # Apply IR drop (position-dependent conductance reduction)
            if cfg.ir_drop_factor > 0.0:
                # Simplified model: random drop per device based on distance
                # In a real array, this would be a function of (row, col)
                ir_drop_pos = torch.rand_like(G_pos) * cfg.ir_drop_factor
                ir_drop_neg = torch.rand_like(G_neg) * cfg.ir_drop_factor
                G_pos = G_pos * (1.0 - ir_drop_pos)
                G_neg = G_neg * (1.0 - ir_drop_neg)

            # Apply Sneak path (leakage current)
            if cfg.sneak_factor > 0.0:
                # Model as random additive noise relative to G_max
                sneak_noise_pos = torch.randn_like(G_pos) * cfg.sneak_factor * cfg.G_max
                sneak_noise_neg = torch.randn_like(G_neg) * cfg.sneak_factor * cfg.G_max
                # Clamp to 10% of G_max to keep it realistic
                limit = cfg.G_max * 0.1
                G_pos = G_pos + sneak_noise_pos.clamp(-limit, limit)
                G_neg = G_neg + sneak_noise_neg.clamp(-limit, limit)

        return G_pos, G_neg

    def _conductance_to_weight_scale(self, W: torch.Tensor,
                                     effective_conductance: Optional[torch.Tensor] = None) -> torch.Tensor:
        cfg = self.config
        if not cfg.restore_weight_scale:
            return W.new_tensor(1.0)

        with autocast_disabled_context(W.device.type):
            W_fp32 = W.float()
            eps = 1e-8
            w_abs_max = W_fp32.abs().max().detach() + eps
            if cfg.retention_recalibrate_scale and effective_conductance is not None:
                effective_range = effective_conductance.float().abs().max().detach() + eps
                return w_abs_max / effective_range
            G_range = cfg.G_max - cfg.G_min
            return w_abs_max / G_range

    def _apply_retention(self, G_pos: torch.Tensor, G_neg: torch.Tensor):
        """Apply double-exponential retention decay (handbook §2.1).

        G(t) = G_min + (G_programmed - G_min) × [A₁·exp(-t/τ₁) + A₂·exp(-t/τ₂) + A₀]
        where A₁ + A₂ + A₀ = 1, A₁ = A₂ = (1 - A₀) / 2
        """
        cfg = self.config
        if not cfg.retention_enabled or cfg.inference_time <= 0:
            return G_pos, G_neg

        if cfg.retention_state_dependent:
            decay_pos = _retention_decay_factor(cfg, G_pos)
            decay_neg = _retention_decay_factor(cfg, G_neg)
            G_pos_decayed = cfg.G_min + (G_pos - cfg.G_min) * decay_pos
            G_neg_decayed = cfg.G_min + (G_neg - cfg.G_min) * decay_neg
        else:
            decay_factor = _retention_decay_factor(cfg)
            G_pos_decayed = cfg.G_min + (G_pos - cfg.G_min) * decay_factor
            G_neg_decayed = cfg.G_min + (G_neg - cfg.G_min) * decay_factor

        return G_pos_decayed, G_neg_decayed

    def _apply_noise(self, G_pos: torch.Tensor, G_neg: torch.Tensor):
        """Apply D2D (fixed) and C2C (re-sampled) noise to effective weight.

        Noise model (handbook §2.1):
          W_noisy = W_eff + d2d_noise        (fixed at init)
          W_inference = W_noisy + N(0, σ_c2c² × G_range²)  (per forward)
        """
        cfg = self.config
        W_eff = G_pos - G_neg  # differential output

        if not cfg.noise_enabled:
            return W_eff

        # D2D noise: fixed buffer, optionally decays with retention to match
        # the shrinking programmed conductance contrast.
        d2d_noise = self.d2d_noise
        if cfg.noise_mode == "uniform" and cfg.retention_scales_d2d and cfg.retention_enabled and cfg.inference_time > 0:
            d2d_noise = d2d_noise * _retention_decay_factor(cfg)
        W_eff = W_eff + _scaled_noise_from_reference(
            d2d_noise,
            W_eff,
            cfg.sigma_d2d,
            cfg.G_max - cfg.G_min,
            cfg.noise_mode,
            is_fixed_pattern=True,
        )

        # C2C noise: re-sampled every forward pass
        if cfg.sigma_c2c > 0:
            W_eff = W_eff + _scaled_noise_from_reference(
                torch.empty_like(W_eff),
                W_eff,
                cfg.sigma_c2c,
                cfg.G_max - cfg.G_min,
                cfg.noise_mode,
                is_fixed_pattern=False,
            )

        return W_eff

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Full analog inference pipeline.

        x: (..., in_features)
        returns: (..., out_features)
        """
        _record_input_sparsity(self, x)
        # Step 1: Float weight → quantized differential conductance pair
        G_pos, G_neg = self._weight_to_conductance(self.weight)

        # Step 2: Optional retention decay
        G_pos, G_neg = self._apply_retention(G_pos, G_neg)
        retained_diff = G_pos - G_neg

        # Step 3: Apply noise (D2D fixed + C2C re-sampled)
        W_eff = self._apply_noise(G_pos, G_neg)
        W_eff = W_eff * self._conductance_to_weight_scale(self.weight, retained_diff)

        # Step 4: Vector-Matrix Multiplication
        return F.linear(x, W_eff, self.bias)

    def extra_repr(self) -> str:
        cfg = self.config
        return (
            f"in_features={self.in_features}, out_features={self.out_features}, "
            f"bias={self.bias is not None}, "
            f"n_states={cfg.n_states}, G=[{cfg.G_min},{cfg.G_max}], "
            f"σ_c2c={cfg.sigma_c2c}, σ_d2d={cfg.sigma_d2d}, "
            f"noise={cfg.noise_enabled}, noise_mode={cfg.noise_mode}, "
            f"retention={cfg.retention_enabled}, "
            f"scale_recovery={cfg.restore_weight_scale}"
        )


# ─────────────────────────────────────────────
# AnalogConv2d Module
# ─────────────────────────────────────────────

class AnalogConv2d(nn.Module):
    """Drop-in replacement for nn.Conv2d with analog crossbar simulation.

    Same physical pipeline as AnalogLinear:
      float weight → differential pair (G⁺, G⁻) → quantize → D2D noise → C2C noise
      → optional retention decay → Conv2d → output

    Weight shape: (C_out, C_in, kH, kW) — unrolled to (C_out, C_in*kH*kW) for
    crossbar mapping, but simulation operates on the full tensor.
    """

    def __init__(self, in_channels: int, out_channels: int,
                 kernel_size, stride=1, padding=0, dilation=1,
                 groups: int = 1, bias: bool = True,
                 config: Optional[AnalogLinearConfig] = None):
        super().__init__()
        _require_positive_int("in_channels", in_channels)
        _require_positive_int("out_channels", out_channels)
        _require_positive_int("groups", groups)
        self.kernel_size = _normalize_positive_2tuple("kernel_size", kernel_size)
        self.stride = _normalize_positive_2tuple("stride", stride)
        self.padding = _normalize_positive_2tuple("padding", padding, allow_zero=True)
        self.dilation = _normalize_positive_2tuple("dilation", dilation)
        if in_channels % groups != 0:
            raise ValueError(
                f"in_channels ({in_channels}) must be divisible by groups ({groups})"
            )
        if out_channels % groups != 0:
            raise ValueError(
                f"out_channels ({out_channels}) must be divisible by groups ({groups})"
            )
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.groups = groups
        self.config = copy.copy(config) if config is not None else AnalogLinearConfig()

        # Learnable weight (same as nn.Conv2d)
        self.weight = nn.Parameter(
            torch.empty(out_channels, in_channels // groups, *self.kernel_size)
        )
        if bias:
            self.bias = nn.Parameter(torch.empty(out_channels))
        else:
            self.register_parameter('bias', None)

        # D2D noise: same shape as weight, fixed at init
        G_range = self.config.G_max - self.config.G_min
        self.register_buffer(
            'd2d_noise',
            torch.randn_like(self.weight) * self.config.sigma_d2d * G_range
        )
        _init_sparsity_state(self)

        self._reset_parameters()

    def _reset_parameters(self):
        nn.init.kaiming_uniform_(self.weight, a=math.sqrt(5))
        if self.bias is not None:
            fan_in = self.in_channels // self.groups
            for k in self.kernel_size:
                fan_in *= k
            bound = 1 / math.sqrt(fan_in)
            nn.init.uniform_(self.bias, -bound, bound)

    def resample_d2d_noise(self):
        """Draw a new fixed D2D noise pattern for this layer."""
        with torch.no_grad():
            G_range = self.config.G_max - self.config.G_min
            self.d2d_noise.copy_(_sample_d2d_noise(self.d2d_noise, self.config.sigma_d2d, G_range))

    def _weight_to_conductance(self, W: torch.Tensor):
        """Same mapping as AnalogLinear but works on any-shape weight tensor."""
        cfg = self.config
        eps = 1e-8
        with autocast_disabled_context(W.device.type):
            W_fp32 = W.float()
            W_pos = torch.clamp(W_fp32, min=0.0)
            W_neg = torch.clamp(-W_fp32, min=0.0)
            w_abs_max = W_fp32.abs().max().detach() + eps
            W_pos_norm = W_pos / w_abs_max
            W_neg_norm = W_neg / w_abs_max
            G_range = cfg.G_max - cfg.G_min
            G_pos = cfg.G_min + W_pos_norm * G_range
            G_neg = cfg.G_min + W_neg_norm * G_range
            G_pos = ste_quantize(G_pos, cfg.n_states, cfg.G_min, cfg.G_max, cfg.NL_LTP, cfg.NL_LTD, cfg.inl_table, cfg.use_second_order_ste, cfg.delta_g_eff, cfg.second_order_alpha)
            G_neg = ste_quantize(G_neg, cfg.n_states, cfg.G_min, cfg.G_max, cfg.NL_LTP, cfg.NL_LTD, cfg.inl_table, cfg.use_second_order_ste, cfg.delta_g_eff, cfg.second_order_alpha)

            # Apply asymmetry (if any) with offset correction
            if cfg.asymmetry_factor != 0.0:
                G_pos = G_pos * (1.0 + cfg.asymmetry_factor)
                G_neg = G_neg * (1.0 - cfg.asymmetry_factor)
                # Subtract the constant DC bias: G_min*(1+alpha) - G_min*(1-alpha) = 2*G_min*alpha
                offset = 2.0 * cfg.G_min * cfg.asymmetry_factor
                G_pos = G_pos - offset

            # Apply IR drop (position-dependent conductance reduction)
            if cfg.ir_drop_factor > 0.0:
                # Simplified model: random drop per device based on distance
                # In a real array, this would be a function of (row, col)
                ir_drop_pos = torch.rand_like(G_pos) * cfg.ir_drop_factor
                ir_drop_neg = torch.rand_like(G_neg) * cfg.ir_drop_factor
                G_pos = G_pos * (1.0 - ir_drop_pos)
                G_neg = G_neg * (1.0 - ir_drop_neg)

            # Apply Sneak path (leakage current)
            if cfg.sneak_factor > 0.0:
                # Model as random additive noise relative to G_max
                sneak_noise_pos = torch.randn_like(G_pos) * cfg.sneak_factor * cfg.G_max
                sneak_noise_neg = torch.randn_like(G_neg) * cfg.sneak_factor * cfg.G_max
                # Clamp to 10% of G_max to keep it realistic
                limit = cfg.G_max * 0.1
                G_pos = G_pos + sneak_noise_pos.clamp(-limit, limit)
                G_neg = G_neg + sneak_noise_neg.clamp(-limit, limit)

        return G_pos, G_neg

    def _conductance_to_weight_scale(self, W: torch.Tensor,
                                     effective_conductance: Optional[torch.Tensor] = None) -> torch.Tensor:
        cfg = self.config
        if not cfg.restore_weight_scale:
            return W.new_tensor(1.0)

        with autocast_disabled_context(W.device.type):
            W_fp32 = W.float()
            eps = 1e-8
            w_abs_max = W_fp32.abs().max().detach() + eps
            if cfg.retention_recalibrate_scale and effective_conductance is not None:
                effective_range = effective_conductance.float().abs().max().detach() + eps
                return w_abs_max / effective_range
            G_range = cfg.G_max - cfg.G_min
            return w_abs_max / G_range

    def _apply_retention(self, G_pos, G_neg):
        cfg = self.config
        if not cfg.retention_enabled or cfg.inference_time <= 0:
            return G_pos, G_neg

        if cfg.retention_state_dependent:
            decay_pos = _retention_decay_factor(cfg, G_pos)
            decay_neg = _retention_decay_factor(cfg, G_neg)
            G_pos_d = cfg.G_min + (G_pos - cfg.G_min) * decay_pos
            G_neg_d = cfg.G_min + (G_neg - cfg.G_min) * decay_neg
        else:
            decay_factor = _retention_decay_factor(cfg)
            G_pos_d = cfg.G_min + (G_pos - cfg.G_min) * decay_factor
            G_neg_d = cfg.G_min + (G_neg - cfg.G_min) * decay_factor

        return G_pos_d, G_neg_d

    def _apply_noise(self, G_pos, G_neg):
        cfg = self.config
        W_eff = G_pos - G_neg
        if not cfg.noise_enabled:
            return W_eff
        d2d_noise = self.d2d_noise
        if cfg.noise_mode == "uniform" and cfg.retention_scales_d2d and cfg.retention_enabled and cfg.inference_time > 0:
            d2d_noise = d2d_noise * _retention_decay_factor(cfg)
        W_eff = W_eff + _scaled_noise_from_reference(
            d2d_noise,
            W_eff,
            cfg.sigma_d2d,
            cfg.G_max - cfg.G_min,
            cfg.noise_mode,
            is_fixed_pattern=True,
        )
        if cfg.sigma_c2c > 0:
            W_eff = W_eff + _scaled_noise_from_reference(
                torch.empty_like(W_eff),
                W_eff,
                cfg.sigma_c2c,
                cfg.G_max - cfg.G_min,
                cfg.noise_mode,
                is_fixed_pattern=False,
            )
        return W_eff

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Analog Conv2d forward: quantize, apply noise, and convolve."""
        _record_input_sparsity(self, x)
        G_pos, G_neg = self._weight_to_conductance(self.weight)
        G_pos, G_neg = self._apply_retention(G_pos, G_neg)
        retained_diff = G_pos - G_neg
        W_eff = self._apply_noise(G_pos, G_neg)
        W_eff = W_eff * self._conductance_to_weight_scale(self.weight, retained_diff)
        return F.conv2d(x, W_eff, self.bias, self.stride, self.padding,
                        self.dilation, self.groups)

    def extra_repr(self) -> str:
        """Return a string with layer configuration details."""
        cfg = self.config
        return (
            f"in_channels={self.in_channels}, out_channels={self.out_channels}, "
            f"kernel_size={self.kernel_size}, stride={self.stride}, padding={self.padding}, "
            f"groups={self.groups}, bias={self.bias is not None}, "
            f"n_states={cfg.n_states}, noise={cfg.noise_enabled}"
        )


# ─────────────────────────────────────────────
# InverseGammaPreprocessor
# ─────────────────────────────────────────────

class InverseGammaPreprocessor(nn.Module):
    """Inverse-gamma front-end preprocessing for photocurrent linearization.

    Applies: P_in = X^(1/gamma_phys)
    Also computes shot noise variance map: var = alpha * X^(1/gamma_phys)

    Reference: claude全栈参考手册.md §4.1
      - Dark region (X→0): noise variance compressed  ✓
      - Bright region (X→1): noise variance amplified when 1/γ > 1 (γ < 1)
    """

    def __init__(self, gamma_phys: float = 1.0, alpha: float = 1.0):
        super().__init__()
        self.gamma_phys = gamma_phys
        self.alpha = alpha

    def forward(self, x: torch.Tensor):
        """
        Args:
            x: Normalized image tensor in [0, 1], shape (..., H, W) or (..., C, H, W)
        Returns:
            P_in: Inverse-gamma compensated signal
            noise_var: Shot noise variance map (same shape)
        """
        eps = 1e-8
        x_clamped = torch.clamp(x, min=eps, max=1.0)

        if self.gamma_phys == 1.0:
            P_in = x_clamped
        else:
            P_in = torch.pow(x_clamped, 1.0 / self.gamma_phys)

        # Shot noise variance: σ² = α × P_in
        noise_var = self.alpha * P_in

        return P_in, noise_var

    def extra_repr(self) -> str:
        return f"gamma_phys={self.gamma_phys}, alpha={self.alpha}"


# ─────────────────────────────────────────────
# PhotocurrentSimulator
# ─────────────────────────────────────────────

class PhotocurrentSimulator(nn.Module):
    """Simulates organic optoelectronic phototransistor response.

    Physical model:
      I_photo = alpha * P_in^gamma_phys + I_dark + Poisson_noise

    Two modes:
      - 'compensated': input has been inverse-gamma preprocessed
        → I_photo = alpha * (X^(1/γ))^γ + I_dark ≈ alpha * X + I_dark (linearized)
      - 'raw': direct physical response without compensation
        → I_photo = alpha * X^γ + I_dark

    Reference: claude全栈参考手册.md §2.1
      - I_dark ~100 pA (TIPS-Pen off-state)
      - alpha: responsivity (a.u., normalized in simulation)
    """

    def __init__(self, alpha: float = 1.0, I_dark: float = 1e-10,
                 gamma_phys: float = 0.7, shot_noise: bool = True):
        super().__init__()
        self.alpha = alpha
        self.I_dark = I_dark
        self.gamma_phys = gamma_phys
        self.shot_noise = shot_noise

    def forward(self, x: torch.Tensor, mode: str = 'raw'):
        """
        Args:
            x: Input signal in [0, 1]. If mode='compensated', this is P_in from
               InverseGammaPreprocessor; if mode='raw', this is the raw pixel value.
            mode: 'compensated' or 'raw'
        Returns:
            I_photo: Simulated photocurrent (same shape as x)
        """
        eps = 1e-8
        x_clamped = torch.clamp(x, min=eps, max=1.0)

        if mode == 'compensated':
            # Input already inverse-gamma'd: P_in = X^(1/γ)
            # Physical response: I = α × P_in^γ = α × X  (linearized)
            I_signal = self.alpha * torch.pow(x_clamped, self.gamma_phys)
        elif mode == 'raw':
            # No compensation: I = α × X^γ
            I_signal = self.alpha * torch.pow(x_clamped, self.gamma_phys)
        else:
            raise ValueError(f"Unknown mode '{mode}', expected 'compensated' or 'raw'")

        I_photo = I_signal + self.I_dark

        # Poisson-like shot noise: σ² ∝ I_photo
        if self.shot_noise and self.training or (self.shot_noise and not self.training):
            noise_std = torch.sqrt(torch.clamp(I_photo * self.alpha, min=eps))
            I_photo = I_photo + torch.randn_like(I_photo) * noise_std * 0.01  # scaled

        return I_photo

    def extra_repr(self) -> str:
        return (f"alpha={self.alpha}, I_dark={self.I_dark}, "
                f"gamma_phys={self.gamma_phys}, shot_noise={self.shot_noise}")


# ─────────────────────────────────────────────
# ADCQuantizer
# ─────────────────────────────────────────────

@dataclass
class ADCConfig:
    """ADC parameters from claude全栈参考手册.md §2.2."""
    adc_bits: int = 8
    dnl_sigma: float = 0.5   # DNL non-linearity in LSB units
    I_min: float = 0.0       # minimum output current (a.u.)
    I_max: float = 1.0       # maximum output current (a.u.)


class ADCQuantizer(nn.Module):
    """ADC pseudo-quantization layer with DNL non-linearity distortion.

    Simulates analog-to-digital converter at the output of crossbar columns.

    Quantization: uniform quantization to 2^adc_bits levels
    DNL distortion: each quantization step has a Gaussian perturbation
      Δ_actual[i] = Δ_ideal × (1 + N(0, σ_DNL²))

    Reference: claude全栈参考手册.md §2.2
      - Default 8-bit, 25 fJ/conversion
      - σ_DNL = 0.5 LSB
    """

    def __init__(self, config: Optional[ADCConfig] = None):
        super().__init__()
        self.config = config or ADCConfig()
        cfg = self.config
        n_levels = 2 ** cfg.adc_bits

        # DNL perturbation: fixed per ADC instance (like D2D for ADC steps)
        # Each level boundary has a slightly shifted position
        if cfg.dnl_sigma > 0:
            dnl_noise = torch.randn(n_levels) * cfg.dnl_sigma
            # Cumulative effect on level boundaries
            self.register_buffer('dnl_offsets', dnl_noise)
        else:
            self.register_buffer('dnl_offsets', torch.zeros(n_levels))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Quantize continuous signal to discrete ADC levels.

        Args:
            x: Continuous-valued tensor (e.g., crossbar column output)
        Returns:
            x_quantized: Discretized output
        """
        cfg = self.config
        n_levels = 2 ** cfg.adc_bits
        eps = 1e-8

        # Clamp to valid range
        x_clamped = torch.clamp(x, cfg.I_min, cfg.I_max)

        # Normalize to [0, 1]
        scale = cfg.I_max - cfg.I_min + eps
        x_norm = (x_clamped - cfg.I_min) / scale

        # Quantize to integer level index
        level_idx = torch.round(x_norm * (n_levels - 1)).long()
        level_idx = torch.clamp(level_idx, 0, n_levels - 1)

        # Ideal quantized value
        x_quant = level_idx.float() / (n_levels - 1)

        # Apply DNL distortion: shift each level by its DNL offset (in LSB units)
        if cfg.dnl_sigma > 0:
            lsb = 1.0 / (n_levels - 1)
            dnl_shift = self.dnl_offsets[level_idx] * lsb
            x_quant = x_quant + dnl_shift

        # Denormalize back
        x_quant = x_quant * scale + cfg.I_min

        if self.training:
            # STE: pass gradient through quantization
            return x + (x_quant - x).detach()
        else:
            return x_quant

    def extra_repr(self) -> str:
        cfg = self.config
        return (f"bits={cfg.adc_bits}, dnl_sigma={cfg.dnl_sigma}, "
                f"range=[{cfg.I_min}, {cfg.I_max}]")


# ─────────────────────────────────────────────
# EnergyProfiler
# ─────────────────────────────────────────────

@dataclass
class EnergyConstants:
    """Energy constants for 28nm technology node.

    All values from claude全栈参考手册.md §3.2.
    Units: Joules
    """
    E_analog_MAC: float = 100e-15       # 100 fJ (organic device)
    E_analog_MAC_conservative: float = 150e-15  # 150 fJ (RRAM median)
    E_ADC_8bit: float = 25e-15          # 25 fJ/conversion
    E_DAC_8bit: float = 30e-15          # 30 fJ/conversion
    E_digital_INT8_MAC: float = 0.4e-12  # 0.4 pJ
    E_digital_FP32_MAC: float = 2.5e-12  # 2.5 pJ
    E_softmax_per_elem: float = 15e-12  # 15 pJ/element
    E_layernorm_per_elem: float = 8e-12  # 8 pJ/element
    E_SRAM_read: float = 5e-12          # 5 pJ/read (32-bit)
    E_DRAM_read: float = 1300e-12       # 1300 pJ/read (off-chip)
    t_array_settle_ns: float = 50.0     # array RC settle time
    t_adc_8bit_ns: float = 100.0        # 8-bit SAR ADC conversion time
    t_adc_4bit_ns: float = 25.0         # 4-bit ADC conversion time
    digital_mac_throughput_per_s: float = 1e9  # conservative edge throughput


class EnergyProfiler:
    """Energy profiling for hybrid analog/digital inference.

    Accumulates energy consumption for each forward pass, broken down by:
      - Analog MAC energy
      - ADC/DAC conversion energy
      - Digital computation energy (INT8 MACs, special ops)
      - Buffer read/write energy

    Reference: claude全栈参考手册.md §3.1, §3.2
    """

    def __init__(self, constants: Optional[EnergyConstants] = None):
        self.constants = constants or EnergyConstants()
        self.reset()

    def reset(self):
        """Reset all energy accumulators."""
        self.energy = {
            'analog_MAC': 0.0,
            'ADC': 0.0,
            'DAC': 0.0,
            'digital_MAC': 0.0,
            'special_ops': 0.0,
            'buffer': 0.0,
        }
        self.latency_ns = {
            'analog_pipeline': 0.0,
            'digital_compute': 0.0,
            'special_ops': 0.0,
            'buffer': 0.0,
        }
        self.op_counts = {
            'analog_MACs': 0,
            'digital_MACs': 0,
            'ADC_conversions': 0,
            'DAC_conversions': 0,
            'softmax_elements': 0,
            'layernorm_elements': 0,
            'SRAM_reads': 0,
        }
        self._analog_latency_records: List[dict] = []

    def _estimate_adc_latency_ns(self, adc_bits: int) -> float:
        if adc_bits <= 4:
            return self.constants.t_adc_4bit_ns * max(adc_bits, 1) / 4.0
        if adc_bits == 8:
            return self.constants.t_adc_8bit_ns
        return self.constants.t_adc_8bit_ns * (adc_bits / 8.0) ** 2

    def add_analog_layer(self, M: int, N: int, batch_tokens: int,
                         col_tiles: Optional[int] = None, adc_bits: int = 8,
                         array_size: int = 128):
        """Account for one analog Linear layer's energy.

        Args:
            M: output features (rows)
            N: input features (cols)
            batch_tokens: total number of input vectors (batch_size × seq_len)
        """
        c = self.constants
        n_MACs = batch_tokens * M * N
        n_ADC = batch_tokens * M       # one ADC per output element
        n_DAC = batch_tokens * N       # one DAC per input element
        col_tiles = col_tiles or max(1, math.ceil(N / array_size))
        stage_latency_ns = max(c.t_array_settle_ns, self._estimate_adc_latency_ns(adc_bits))
        layer_latency_ns = batch_tokens * col_tiles * stage_latency_ns

        self.energy['analog_MAC'] += n_MACs * c.E_analog_MAC
        self.energy['ADC'] += n_ADC * c.E_ADC_8bit
        self.energy['DAC'] += n_DAC * c.E_DAC_8bit
        self.latency_ns['analog_pipeline'] += layer_latency_ns

        self.op_counts['analog_MACs'] += n_MACs
        self.op_counts['ADC_conversions'] += n_ADC
        self.op_counts['DAC_conversions'] += n_DAC
        self._analog_latency_records.append({
            'M': M,
            'N': N,
            'batch_tokens': batch_tokens,
            'col_tiles': col_tiles,
            'adc_bits': adc_bits,
            'latency_ns': layer_latency_ns,
        })

    def add_digital_layer(self, n_MACs: int, precision: str = 'INT8'):
        """Account for digital computation energy.

        Args:
            n_MACs: number of MAC operations
            precision: 'INT8' or 'FP32'
        """
        c = self.constants
        e_per_mac = c.E_digital_INT8_MAC if precision == 'INT8' else c.E_digital_FP32_MAC
        self.energy['digital_MAC'] += n_MACs * e_per_mac
        self.latency_ns['digital_compute'] += (n_MACs / c.digital_mac_throughput_per_s) * 1e9
        self.op_counts['digital_MACs'] += n_MACs

    def add_softmax(self, n_elements: int):
        """Account for softmax computation."""
        self.energy['special_ops'] += n_elements * self.constants.E_softmax_per_elem
        self.latency_ns['special_ops'] += (n_elements / self.constants.digital_mac_throughput_per_s) * 1e9
        self.op_counts['softmax_elements'] += n_elements

    def add_layernorm(self, n_elements: int):
        """Account for LayerNorm computation."""
        self.energy['special_ops'] += n_elements * self.constants.E_layernorm_per_elem
        self.latency_ns['special_ops'] += (n_elements / self.constants.digital_mac_throughput_per_s) * 1e9
        self.op_counts['layernorm_elements'] += n_elements

    def add_buffer_access(self, n_reads: int, memory_type: str = 'SRAM'):
        """Account for memory access energy."""
        c = self.constants
        e_per_read = c.E_SRAM_read if memory_type == 'SRAM' else c.E_DRAM_read
        self.energy['buffer'] += n_reads * e_per_read
        self.latency_ns['buffer'] += (n_reads / c.digital_mac_throughput_per_s) * 1e9
        self.op_counts['SRAM_reads'] += n_reads

    def total_energy(self) -> float:
        """Total energy in Joules."""
        return sum(self.energy.values())

    def summary(self) -> dict:
        """Return full energy breakdown."""
        total = self.total_energy()
        latency = self.estimate_latency()
        result = {
            'energy_breakdown_J': dict(self.energy),
            'total_energy_J': total,
            'total_energy_uJ': total * 1e6,
            'op_counts': dict(self.op_counts),
            'latency_breakdown_ns': dict(self.latency_ns),
            'total_latency_ns': latency['total_latency_ns'],
            'total_latency_us': latency['total_latency_us'],
        }
        # Percentage breakdown
        if total > 0:
            result['percentage'] = {k: v / total * 100 for k, v in self.energy.items()}
        return result

    def estimate_latency(self) -> dict:
        """Return latency breakdown in nanoseconds and microseconds."""
        total_latency_ns = sum(self.latency_ns.values())
        return {
            'latency_breakdown_ns': dict(self.latency_ns),
            'total_latency_ns': total_latency_ns,
            'total_latency_us': total_latency_ns / 1000.0,
            'analog_layers': list(self._analog_latency_records),
        }

    def compare_with_fp32_gpu(self, total_MACs: int) -> dict:
        """Compare hybrid energy with pure FP32 GPU baseline.

        Args:
            total_MACs: Total MAC operations in the model
        Returns:
            Comparison dict with speedup ratio
        """
        c = self.constants
        gpu_energy = total_MACs * c.E_digital_FP32_MAC
        hybrid_energy = self.total_energy()

        return {
            'gpu_FP32_energy_J': gpu_energy,
            'gpu_FP32_energy_uJ': gpu_energy * 1e6,
            'hybrid_energy_J': hybrid_energy,
            'hybrid_energy_uJ': hybrid_energy * 1e6,
            'energy_reduction_ratio': gpu_energy / (hybrid_energy + 1e-30),
        }

    def print_summary(self):
        """Print formatted energy summary."""
        s = self.summary()
        print("=" * 60)
        print("Energy Profiling Summary")
        print("=" * 60)
        print(f"  Total energy: {s['total_energy_uJ']:.4f} µJ")
        print(f"  Total latency: {s['total_latency_us']:.4f} µs")
        print(f"  ─────────────────────────────────")
        for k, v in s['energy_breakdown_J'].items():
            pct = s.get('percentage', {}).get(k, 0)
            print(f"  {k:20s}: {v*1e6:12.4f} µJ  ({pct:5.1f}%)")
        print(f"  ─────────────────────────────────")
        for k, v in s['latency_breakdown_ns'].items():
            print(f"  {k:20s}: {v/1000.0:12.4f} µs")
        print(f"  ─────────────────────────────────")
        print(f"  Operation counts:")
        for k, v in s['op_counts'].items():
            if v > 0:
                print(f"    {k:24s}: {v:>14,}")
        print()


def enable_sparsity_tracking(model: nn.Module):
    """Enable input-sparsity tracking on all analog layers."""
    for module in model.modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            module.track_sparsity = True


def disable_sparsity_tracking(model: nn.Module):
    """Disable input-sparsity tracking on all analog layers."""
    for module in model.modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            module.track_sparsity = False


def reset_sparsity_tracking(model: nn.Module):
    """Reset sparsity accumulators for all analog layers."""
    for module in model.modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            module._sparsity_relative_accum = 0.0
            module._sparsity_absolute_accum = 0.0
            module._sparsity_count = 0
            module._sparsity_last_relative = 0.0
            module._sparsity_last_absolute = 0.0


def get_sparsity_report(model: nn.Module) -> dict:
    """Return aggregated zero-frac statistics across tracked analog layers."""
    layer_rows = []
    weighted_relative_sum = 0.0
    weighted_absolute_sum = 0.0
    weighted_count = 0

    for name, module in model.named_modules():
        if not isinstance(module, (AnalogLinear, AnalogConv2d)):
            continue
        count = int(getattr(module, "_sparsity_count", 0))
        mean_relative_zero_frac = (
            float(getattr(module, "_sparsity_relative_accum", 0.0)) / count if count > 0 else 0.0
        )
        mean_absolute_zero_frac = (
            float(getattr(module, "_sparsity_absolute_accum", 0.0)) / count if count > 0 else 0.0
        )
        layer_rows.append({
            "layer": name,
            "kind": type(module).__name__,
            "samples": count,
            "relative_scale": float(getattr(module, "_sparsity_relative_scale", 0.01)),
            "absolute_threshold": float(getattr(module, "_sparsity_absolute_threshold", 0.01)),
            "mean_relative_zero_frac": mean_relative_zero_frac,
            "mean_relative_nonzero_frac": 1.0 - mean_relative_zero_frac,
            "last_relative_zero_frac": float(getattr(module, "_sparsity_last_relative", 0.0)),
            "mean_absolute_zero_frac": mean_absolute_zero_frac,
            "mean_absolute_nonzero_frac": 1.0 - mean_absolute_zero_frac,
            "last_absolute_zero_frac": float(getattr(module, "_sparsity_last_absolute", 0.0)),
        })
        weighted_relative_sum += mean_relative_zero_frac * count
        weighted_absolute_sum += mean_absolute_zero_frac * count
        weighted_count += count

    model_mean_relative_zero_frac = (
        weighted_relative_sum / weighted_count if weighted_count > 0 else 0.0
    )
    model_mean_absolute_zero_frac = (
        weighted_absolute_sum / weighted_count if weighted_count > 0 else 0.0
    )
    return {
        "tracked_layers": len(layer_rows),
        "tracked_passes": weighted_count,
        "relative_scale": 0.01,
        "absolute_threshold": 0.01,
        "model_mean_relative_zero_frac": model_mean_relative_zero_frac,
        "model_mean_relative_nonzero_frac": 1.0 - model_mean_relative_zero_frac,
        "model_mean_absolute_zero_frac": model_mean_absolute_zero_frac,
        "model_mean_absolute_nonzero_frac": 1.0 - model_mean_absolute_zero_frac,
        "layers": layer_rows,
    }


def resample_d2d_buffers(model: nn.Module,
                         selector: Optional[Callable[[str, nn.Module], bool]] = None) -> int:
    """Resample fixed D2D mismatch buffers for all (or selected) analog layers."""
    updated = 0
    for name, module in model.named_modules():
        if not isinstance(module, (AnalogLinear, AnalogConv2d)):
            continue
        if selector is not None and not selector(name, module):
            continue
        module.resample_d2d_noise()
        updated += 1
    return updated


# ─────────────────────────────────────────────
# Model conversion utility
# ─────────────────────────────────────────────

def convert_to_hybrid(model: nn.Module,
                      config: Optional[AnalogLinearConfig] = None,
                      analog_layer_names: Optional[list] = None,
                      verbose: bool = False) -> nn.Module:
    """Replace Tiny-ViT analog-mapped layers with analog equivalents.

    Args:
        model: PyTorch model (e.g., Tiny-ViT from timm)
        config: AnalogLinearConfig with device physics parameters
        analog_layer_names: Explicit list of layer name substrings to replace.
            If None, uses the shared Tiny-ViT mapping rules.
        verbose: Print replacement log

    Returns:
        Modified model (in-place) with AnalogLinear / AnalogConv2d layers
    """
    config = copy.copy(config) if config is not None else AnalogLinearConfig()
    replaced_linear = 0
    replaced_conv = 0

    for name, module in list(model.named_modules()):
        if not isinstance(module, (nn.Linear, nn.Conv2d)):
            continue

        if analog_layer_names is not None:
            should_replace = any(p in name for p in analog_layer_names)
        else:
            should_replace = classify_tinyvit_layer(name, module) == "analog"

        if not should_replace:
            continue

        if isinstance(module, nn.Linear):
            analog_layer = AnalogLinear(
                in_features=module.in_features,
                out_features=module.out_features,
                bias=module.bias is not None,
                config=config,
            )
            analog_layer.weight.data.copy_(module.weight.data)
            if module.bias is not None and analog_layer.bias is not None:
                analog_layer.bias.data.copy_(module.bias.data)
            replaced_linear += 1
            if verbose:
                print(
                    f"  Replaced: {name} → "
                    f"AnalogLinear({module.in_features}, {module.out_features})"
                )
        else:
            analog_layer = AnalogConv2d(
                in_channels=module.in_channels,
                out_channels=module.out_channels,
                kernel_size=module.kernel_size,
                stride=module.stride,
                padding=module.padding,
                dilation=module.dilation,
                groups=module.groups,
                bias=module.bias is not None,
                config=config,
            )
            analog_layer.weight.data.copy_(module.weight.data)
            if module.bias is not None and analog_layer.bias is not None:
                analog_layer.bias.data.copy_(module.bias.data)
            replaced_conv += 1
            if verbose:
                print(
                    f"  Replaced: {name} → AnalogConv2d("
                    f"{module.in_channels}, {module.out_channels}, "
                    f"kernel_size={module.kernel_size})"
                )

        parts = name.split('.')
        parent = model
        for p in parts[:-1]:
            parent = getattr(parent, p)
        setattr(parent, parts[-1], analog_layer)

    if verbose:
        print(
            f"\nTotal replaced: {replaced_linear + replaced_conv} layers "
            f"({replaced_linear} linear, {replaced_conv} conv)"
        )

    return model


def convert_resnet_to_analog(model: nn.Module,
                             config: Optional[AnalogLinearConfig] = None,
                             skip_first_conv: bool = True,
                             skip_downsample: bool = False,
                             verbose: bool = False) -> nn.Module:
    """Replace Conv2d and Linear layers in ResNet with analog equivalents.

    For ResNet-18 on CIFAR-10: all standard Conv2d (groups=1) + final FC
    are mapped to analog crossbar arrays.

    Args:
        model: ResNet model
        config: AnalogLinearConfig (shared for all analog layers)
        skip_first_conv: Skip the first conv layer (stem, often kept digital)
        skip_downsample: Skip downsample/shortcut convolutions
        verbose: Print replacement log
    Returns:
        Modified model with AnalogConv2d/AnalogLinear layers
    """
    config = copy.copy(config) if config is not None else AnalogLinearConfig()
    replaced_conv = 0
    replaced_linear = 0

    for name, module in list(model.named_modules()):
        if isinstance(module, nn.Conv2d):
            # Skip depthwise convolutions
            if module.groups > 1 and module.groups == module.in_channels:
                continue
            # Skip first conv if requested
            if skip_first_conv and name == 'conv1':
                continue
            # Skip downsample convolutions if requested
            if skip_downsample and 'downsample' in name:
                continue

            analog_conv = AnalogConv2d(
                in_channels=module.in_channels,
                out_channels=module.out_channels,
                kernel_size=module.kernel_size,
                stride=module.stride,
                padding=module.padding,
                dilation=module.dilation,
                groups=module.groups,
                bias=module.bias is not None,
                config=config,
            )
            analog_conv.weight.data.copy_(module.weight.data)
            if module.bias is not None and analog_conv.bias is not None:
                analog_conv.bias.data.copy_(module.bias.data)

            parts = name.split('.')
            parent = model
            for p in parts[:-1]:
                parent = getattr(parent, p)
            setattr(parent, parts[-1], analog_conv)
            replaced_conv += 1

            if verbose:
                print(f"  Conv2d → AnalogConv2d: {name} "
                      f"({module.in_channels}→{module.out_channels}, k={module.kernel_size})")

        elif isinstance(module, nn.Linear):
            analog_linear = AnalogLinear(
                in_features=module.in_features,
                out_features=module.out_features,
                bias=module.bias is not None,
                config=config,
            )
            analog_linear.weight.data.copy_(module.weight.data)
            if module.bias is not None and analog_linear.bias is not None:
                analog_linear.bias.data.copy_(module.bias.data)

            parts = name.split('.')
            parent = model
            for p in parts[:-1]:
                parent = getattr(parent, p)
            setattr(parent, parts[-1], analog_linear)
            replaced_linear += 1

            if verbose:
                print(f"  Linear → AnalogLinear: {name} "
                      f"({module.in_features}→{module.out_features})")

    if verbose:
        print(f"\nTotal replaced: {replaced_conv} Conv2d + {replaced_linear} Linear "
              f"= {replaced_conv + replaced_linear} layers")

    return model
