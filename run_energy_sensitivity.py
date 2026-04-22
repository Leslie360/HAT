"""
Energy Model Sensitivity Analysis (Lightweight, can run in parallel)

Analyzes how energy conclusions change with parameter variations.
This is CPU-light and GPU-light, can run alongside training.
"""

import numpy as np
import json
import sys
from datetime import datetime

from repo_bootstrap import ensure_repo_root

ensure_repo_root()
sys.stdout.reconfigure(line_buffering=True)

print("="*70)
print("Energy Model Sensitivity Analysis")
print("="*70)
print("Note: This is a lightweight analysis, runs alongside training")
print("="*70)

# Baseline energy model parameters (from paper)
BASELINE = {
    'E_ADC_8b': 25e-15,      # 25 fJ per conversion
    'E_DAC_8b': 30e-15,      # 30 fJ per conversion  
    'E_cell': 100e-15,       # 100 fJ per array access
    'E_digital': 1e-12,      # 1 pJ per MAC (digital baseline)
    'n_arrays': 100,         # number of arrays
    'n_conversions': 1000,   # ADC conversions per inference
}

def calculate_energy(params):
    """Calculate total energy per inference"""
    E_total = (
        params['E_ADC_8b'] * params['n_conversions'] +
        params['E_DAC_8b'] * params['n_conversions'] +
        params['E_cell'] * params['n_arrays']
    )
    return E_total

def calculate_speedup(analog_energy, digital_energy):
    """Calculate speedup vs digital"""
    return digital_energy / analog_energy

def sensitivity_analysis():
    """Run sensitivity analysis on key parameters"""
    
    baseline_energy = calculate_energy(BASELINE)
    baseline_speedup = calculate_speedup(baseline_energy, BASELINE['E_digital'])
    
    print(f"\nBaseline Configuration:")
    print(f"  E_ADC_8b: {BASELINE['E_ADC_8b']*1e15:.1f} fJ")
    print(f"  E_DAC_8b: {BASELINE['E_DAC_8b']*1e15:.1f} fJ")
    print(f"  E_cell: {BASELINE['E_cell']*1e15:.1f} fJ")
    print(f"  Total: {baseline_energy*1e12:.3f} pJ")
    print(f"  Speedup vs digital: {baseline_speedup:.2f}×")
    
    # Sensitivity ranges
    variations = {
        'E_ADC_8b': [0.5, 0.75, 1.0, 1.5, 2.0, 5.0, 10.0],  # multiples of baseline
        'E_DAC_8b': [0.5, 0.75, 1.0, 1.5, 2.0, 5.0, 10.0],
        'E_cell': [0.5, 0.75, 1.0, 1.5, 2.0, 5.0, 10.0],
    }
    
    results = {}
    
    for param_name, multipliers in variations.items():
        print(f"\n{param_name} Sensitivity:")
        print("-" * 50)
        
        param_results = []
        for mult in multipliers:
            test_params = BASELINE.copy()
            test_params[param_name] = BASELINE[param_name] * mult
            
            energy = calculate_energy(test_params)
            speedup = calculate_speedup(energy, BASELINE['E_digital'])
            
            param_results.append({
                'multiplier': mult,
                'energy_pJ': energy * 1e12,
                'speedup': speedup
            })
            
            marker = " <-- baseline" if mult == 1.0 else ""
            print(f"  {mult:5.2f}×: {energy*1e12:6.2f} pJ, {speedup:5.2f}× speedup{marker}")
        
        results[param_name] = param_results
    
    # Combined variation (all params vary together)
    print(f"\nCombined Variation (all parameters together):")
    print("-" * 50)
    combined_results = []
    for mult in [0.5, 0.75, 1.0, 2.0, 5.0, 10.0]:
        test_params = BASELINE.copy()
        test_params['E_ADC_8b'] *= mult
        test_params['E_DAC_8b'] *= mult
        test_params['E_cell'] *= mult
        
        energy = calculate_energy(test_params)
        speedup = calculate_speedup(energy, BASELINE['E_digital'])
        
        combined_results.append({
            'multiplier': mult,
            'energy_pJ': energy * 1e12,
            'speedup': speedup
        })
        
        marker = " <-- baseline" if mult == 1.0 else ""
        print(f"  {mult:5.2f}×: {energy*1e12:6.2f} pJ, {speedup:5.2f}× speedup{marker}")
    
    results['combined'] = combined_results
    
    # Key findings
    print(f"\n" + "="*70)
    print("KEY FINDINGS")
    print("="*70)
    
    # Most sensitive parameter
    adc_range = (results['E_ADC_8b'][0]['speedup'], results['E_ADC_8b'][-1]['speedup'])
    dac_range = (results['E_DAC_8b'][0]['speedup'], results['E_DAC_8b'][-1]['speedup'])
    cell_range = (results['E_cell'][0]['speedup'], results['E_cell'][-1]['speedup'])
    
    print(f"\nSensitivity Ranking (speedup variation range):")
    print(f"  1. E_ADC_8b: {adc_range[0]:.2f}× to {adc_range[1]:.2f}× (range: {adc_range[1]-adc_range[0]:.2f})")
    print(f"  2. E_DAC_8b: {dac_range[0]:.2f}× to {dac_range[1]:.2f}× (range: {dac_range[1]-dac_range[0]:.2f})")
    print(f"  3. E_cell:   {cell_range[0]:.2f}× to {cell_range[1]:.2f}× (range: {cell_range[1]-cell_range[0]:.2f})")
    
    # Conservative bounds
    print(f"\nConservative Bounds (2× all parameters):")
    conservative = next(r for r in combined_results if r['multiplier'] == 2.0)
    print(f"  Energy: {conservative['energy_pJ']:.2f} pJ")
    print(f"  Speedup: {conservative['speedup']:.2f}×")
    print(f"  (vs baseline {baseline_speedup:.2f}×)")
    
    # Pessimistic bounds
    print(f"\nPessimistic Bounds (5× all parameters):")
    pessimistic = next(r for r in combined_results if r['multiplier'] == 5.0)
    print(f"  Energy: {pessimistic['energy_pJ']:.2f} pJ")
    print(f"  Speedup: {pessimistic['speedup']:.2f}×")
    
    # Recommended claim
    print(f"\n" + "="*70)
    print("RECOMMENDED ENERGY CLAIM")
    print("="*70)
    print(f"Current headline: '11.45× lower than FP32'")
    print(f"Recommended: '{baseline_speedup:.1f}× (baseline) to {conservative['speedup']:.1f}× (conservative)'")
    print(f"Or: 'up to {baseline_speedup:.1f}× under first-order assumptions'")
    
    return results

def main():
    results = sensitivity_analysis()
    
    # Save results
    output = {
        'experiment': 'Energy Model Sensitivity Analysis',
        'date': datetime.now().isoformat(),
        'baseline': BASELINE,
        'baseline_speedup': calculate_speedup(calculate_energy(BASELINE), BASELINE['E_digital']),
        'sensitivity_results': results,
        'recommendation': {
            'current_claim': '11.45× lower than FP32',
            'conservative_claim': f"{results['combined'][2]['speedup']:.1f}× (2× parameters)",
            'recommended_wording': f"up to {calculate_speedup(calculate_energy(BASELINE), BASELINE['E_digital']):.1f}× under first-order analytical assumptions"
        }
    }
    
    with open('report_md/_gpt/energy_sensitivity_analysis.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults saved: report_md/_gpt/energy_sensitivity_analysis.json")
    print("="*70)

if __name__ == '__main__':
    main()
