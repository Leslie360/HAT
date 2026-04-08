## 2026-04-05 Codex
### Goal
- Prioritize experiment-framework development with literature profiles and synthetic placeholder profiles before in-house device data are ready.

### Available Profile Libraries
- Literature-anchored:
  - `/home/qiaosir/projects/compute_vit/device_profiles/literature_profiles_gpt.json`
- Synthetic stress-test:
  - `/home/qiaosir/projects/compute_vit/device_profiles/synthetic_profiles_gpt.json`
- Measured-profile schema example:
  - `/home/qiaosir/projects/compute_vit/device_profiles/example_measured_device_profile_gpt.json`

### Recommended Development Order
1. Run zero-shot device comparison with the literature library.
2. Run Tiny-ViT V4 noise sweep with one selected synthetic profile.
3. Run ADC sweep under the same selected synthetic profile.
4. Later replace the selected profile JSON entry with measured device statistics.

### Ready-to-Run Commands
- Literature profile comparison:
```bash
cd /home/qiaosir/projects/compute_vit && /home/qiaosir/miniconda3/envs/LLM/bin/python run_device_comparison.py --device-profile-json device_profiles/literature_profiles_gpt.json --log-path logs/_gpt/device_comparison_literature_gpt.log --json-name device_comparison_literature_results_gpt.json --csv-name device_comparison_literature_results_gpt.csv --report-name device_comparison_literature_report_gpt.md
```

- Synthetic V4 noise sweep:
```bash
cd /home/qiaosir/projects/compute_vit && /home/qiaosir/miniconda3/envs/LLM/bin/python run_noise_sweep.py --model-type tinyvit --experiment V4 --sweep-type noise --device-profile-json device_profiles/synthetic_profiles_gpt.json --profile-name "Synthetic High-Noise" --log-path logs/_gpt/noise_sweep_synthetic_high_noise_gpt.log --json-name noise_sweep_synthetic_high_noise_gpt.json --csv-name noise_sweep_synthetic_high_noise_gpt.csv --report-name noise_sweep_synthetic_high_noise_gpt.md
```

- Synthetic V4 ADC sweep:
```bash
cd /home/qiaosir/projects/compute_vit && /home/qiaosir/miniconda3/envs/LLM/bin/python run_noise_sweep.py --model-type tinyvit --experiment V4 --sweep-type adc --device-profile-json device_profiles/synthetic_profiles_gpt.json --profile-name "Synthetic High-Noise" --log-path logs/_gpt/adc_sweep_synthetic_high_noise_gpt.log --json-name adc_sweep_synthetic_high_noise_gpt.json --csv-name adc_sweep_synthetic_high_noise_gpt.csv --report-name adc_sweep_synthetic_high_noise_gpt.md
```

- Generate a larger fake profile grid:
```bash
cd /home/qiaosir/projects/compute_vit && /home/qiaosir/miniconda3/envs/LLM/bin/python generate_synthetic_device_profiles_gpt.py --base-profile-json device_profiles/literature_profiles_gpt.json --base-profile-name "Organic OPECT Standard" --dynamic-ranges 5 10 20 --n-states 8 16 32 64 --sigma-c2c 0.01 0.05 0.10 --sigma-d2d 0.03 0.10 0.20 --output device_profiles/generated_synthetic_profiles_gpt.json
```

### Interpretation Guidance
- These runs are for framework development and stress characterization.
- Do not present them as in-house measured-device validation.
- For the paper, describe them as:
  - literature-anchored priors
  - synthetic sensitivity envelopes
  - measured-profile-ready pipeline
