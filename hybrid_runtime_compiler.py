"""Hybrid Deployment Runtime Compiler for Organic CIM.

Based on selective D2D resampling experiments, this compiler assigns
layers to {CIM, digital, hybrid} based on their vulnerability to
instance-to-instance analog variation.

Key insight from selective fresh eval:
  - MLP layers: HIGH vulnerability (91% -> 39% when D2D resampled)
  - Attention (QKV, proj): LOW vulnerability (91% -> 88-90%)
  - Embedding: LOW vulnerability (not explicitly tested, assumed robust)

The compiler generates a deployment policy that:
  1. Keeps robust layers on CIM for energy efficiency
  2. Falls back vulnerable layers to digital for accuracy stability
  3. Optionally calibrates CIM layers at runtime
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple


@dataclass
class LayerHealthProfile:
    """Health metrics for a single layer."""
    layer_name: str
    layer_type: str  # 'mlp', 'attn_qkv', 'attn_proj', 'patch_embed', 'head', 'other'
    vulnerability_score: float = 0.0  # 0=robust, 1=fragile
    current_accuracy_drop: float = 0.0  # pp drop from baseline
    drift_rate: float = 0.0  # conductance drift per second
    last_calibration_time: float = 0.0


@dataclass
class DeploymentPolicy:
    """Output of the compiler: what to do with each layer."""
    layer_name: str
    action: str  # 'cim_keep', 'cim_calibrate', 'digital_fallback', 'hybrid_split'
    cim_ratio: float = 1.0  # 1.0 = full CIM, 0.0 = full digital
    calibration_interval: Optional[float] = None  # seconds, None = no calibration


@dataclass
class CompilerConfig:
    """Configuration for the hybrid deployment compiler."""
    # Vulnerability thresholds (from selective eval data)
    mlp_vulnerability: float = 0.93  # MLP accounts for 93% of collapse
    qkv_vulnerability: float = 0.04
    attn_proj_vulnerability: float = 0.02
    
    # Decision thresholds
    accuracy_budget_pp: float = 1.0  # max allowed accuracy drop in pp
    digital_overhead_energy: float = 2.86  # vs INT8 CIM (from T1)
    calibration_cost_energy: float = 0.05  # fraction of inference energy
    
    # Policy rules
    auto_fallback_mlp: bool = True
    auto_calibrate_attention: bool = False  # attention is robust, skip calibration
    mlp_default_digital: bool = False  # if True, all MLP starts on digital


class HybridRuntimeCompiler:
    """Compiles a Tiny-ViT model into a hybrid CIM/digital deployment plan."""
    
    def __init__(self, config: CompilerConfig = None):
        self.config = config or CompilerConfig()
        self._layer_type_detector = self._build_type_detector()
    
    def _build_type_detector(self) -> Callable[[str], str]:
        """Build a name-based layer type classifier."""
        def detector(name: str) -> str:
            if ".mlp.fc" in name:
                return "mlp"
            elif ".attn.qkv" in name:
                return "attn_qkv"
            elif ".attn.proj" in name:
                return "attn_proj"
            elif name.startswith("patch_embed") and ".conv" in name:
                return "patch_embed"
            elif "head.fc" in name:
                return "head"
            else:
                return "other"
        return detector
    
    def compile(self, model_state_dict: Dict[str, any]) -> List[DeploymentPolicy]:
        """Generate deployment policy for each layer in the model."""
        policies = []
        
        for name, param in model_state_dict.items():
            if not name.endswith(".weight"):
                continue  # skip biases, norms, etc.
            
            layer_type = self._layer_type_detector(name)
            policy = self._decide_layer_policy(name, layer_type)
            policies.append(policy)
        
        return policies
    
    def _decide_layer_policy(self, name: str, layer_type: str) -> DeploymentPolicy:
        """Decide deployment action for a single layer."""
        cfg = self.config
        
        if layer_type == "mlp":
            if cfg.mlp_default_digital or cfg.auto_fallback_mlp:
                return DeploymentPolicy(
                    layer_name=name,
                    action="digital_fallback",
                    cim_ratio=0.0,
                    calibration_interval=None,
                )
            else:
                return DeploymentPolicy(
                    layer_name=name,
                    action="cim_calibrate",
                    cim_ratio=1.0,
                    calibration_interval=10.0,  # calibrate every 10s
                )
        
        elif layer_type in ("attn_qkv", "attn_proj"):
            # Attention layers are robust per selective eval
            return DeploymentPolicy(
                layer_name=name,
                action="cim_keep",
                cim_ratio=1.0,
                calibration_interval=None,
            )
        
        elif layer_type == "patch_embed":
            # Patch embed is typically robust (large spatial averaging)
            return DeploymentPolicy(
                layer_name=name,
                action="cim_keep",
                cim_ratio=1.0,
                calibration_interval=None,
            )
        
        elif layer_type == "head":
            # Classifier head is critical — use digital for stability
            return DeploymentPolicy(
                layer_name=name,
                action="digital_fallback",
                cim_ratio=0.0,
                calibration_interval=None,
            )
        
        else:
            # Default: keep on CIM
            return DeploymentPolicy(
                layer_name=name,
                action="cim_keep",
                cim_ratio=1.0,
                calibration_interval=None,
            )
    
    def export_policy_json(self, policies: List[DeploymentPolicy], path: str):
        """Export policy to JSON for runtime consumption."""
        data = {
            "compiler_config": {
                "mlp_vulnerability": self.config.mlp_vulnerability,
                "qkv_vulnerability": self.config.qkv_vulnerability,
                "attn_proj_vulnerability": self.config.attn_proj_vulnerability,
                "accuracy_budget_pp": self.config.accuracy_budget_pp,
            },
            "policies": [
                {
                    "layer_name": p.layer_name,
                    "action": p.action,
                    "cim_ratio": p.cim_ratio,
                    "calibration_interval": p.calibration_interval,
                }
                for p in policies
            ],
        }
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    
    def summarize_policy(self, policies: List[DeploymentPolicy]) -> Dict[str, any]:
        """Generate human-readable summary of the policy."""
        total = len(policies)
        cim_keep = sum(1 for p in policies if p.action == "cim_keep")
        cim_calibrate = sum(1 for p in policies if p.action == "cim_calibrate")
        digital_fallback = sum(1 for p in policies if p.action == "digital_fallback")
        
        return {
            "total_layers": total,
            "cim_keep": cim_keep,
            "cim_calibrate": cim_calibrate,
            "digital_fallback": digital_fallback,
            "cim_keep_ratio": cim_keep / total if total else 0,
            "digital_fallback_ratio": digital_fallback / total if total else 0,
        }


def main():
    """CLI: compile a checkpoint into a deployment policy."""
    import argparse
    import torch
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", required=True, help="Path to model checkpoint")
    parser.add_argument("--mlp-default-digital", action="store_true", help="Put all MLP on digital")
    parser.add_argument("--json-out", default="report_md/_gpt/json_gpt/hybrid_deployment_policy.json")
    args = parser.parse_args()
    
    ckpt = torch.load(args.checkpoint, map_location="cpu", weights_only=False)
    state_dict = ckpt.get("model_state_dict", ckpt)
    
    cfg = CompilerConfig(mlp_default_digital=args.mlp_default_digital)
    compiler = HybridRuntimeCompiler(cfg)
    policies = compiler.compile(state_dict)
    
    compiler.export_policy_json(policies, args.json_out)
    summary = compiler.summarize_policy(policies)
    
    print("Hybrid Deployment Policy Summary:")
    print(f"  Total layers: {summary['total_layers']}")
    print(f"  CIM keep: {summary['cim_keep']} ({summary['cim_keep_ratio']*100:.1f}%)")
    print(f"  CIM calibrate: {summary['cim_calibrate']}")
    print(f"  Digital fallback: {summary['digital_fallback']} ({summary['digital_fallback_ratio']*100:.1f}%)")
    print(f"\nPolicy saved to: {args.json_out}")


if __name__ == "__main__":
    main()
