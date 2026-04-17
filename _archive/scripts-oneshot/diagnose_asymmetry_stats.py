
import torch
import torch.nn as nn
from analog_layers import AnalogLinear, AnalogLinearConfig

def diagnose():
    device = "cpu"
    cfg_clean = AnalogLinearConfig(asymmetry_factor=0.0)
    cfg_asym = AnalogLinearConfig(asymmetry_factor=0.05)
    
    # Test a layer
    layer_clean = AnalogLinear(512, 512, config=cfg_clean)
    layer_asym = AnalogLinear(512, 512, config=cfg_asym)
    
    # Initialize with zeros (to see the bias)
    with torch.no_grad():
        nn.init.zeros_(layer_clean.weight)
        nn.init.zeros_(layer_asym.weight)
        
        # Get effective weights
        G_pos_c, G_neg_c = layer_clean._weight_to_conductance(layer_clean.weight)
        W_eff_c = G_pos_c - G_neg_c
        
        G_pos_a, G_neg_a = layer_asym._weight_to_conductance(layer_asym.weight)
        W_eff_a = G_pos_a - G_neg_a
        
        print(f"Clean (0% asym) W_eff mean: {W_eff_c.mean().item():.6f}")
        print(f"Asym (5% asym) W_eff mean: {W_eff_a.mean().item():.6f}")
        print(f"Asym (5% asym) W_eff std: {W_eff_a.std().item():.6f}")
        
        # Let's see what happens to a real weight range
        nn.init.normal_(layer_clean.weight, 0, 0.1)
        layer_asym.weight.data.copy_(layer_clean.weight.data)
        
        G_pos_a, G_neg_a = layer_asym._weight_to_conductance(layer_asym.weight)
        W_eff_a = G_pos_a - G_neg_a
        print(f"Asym (5% asym) with real weights W_eff mean: {W_eff_a.mean().item():.6f}")

if __name__ == "__main__":
    diagnose()
