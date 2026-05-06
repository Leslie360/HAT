# Remote 105 - HAT Cross-Architecture Validation

## Branch: 105-remote-results

### Environment
- Python: 3.11.15
- PyTorch: 2.4.1+cu121
- CUDA: 12.1
- timm: 1.0.26
- GPU: 8x NVIDIA PH402 SKU 200

### Key Scripts
- `train_vit_tinyimagenet.py` - Training script
- `eval_fresh_instances_vit.py` - Fresh instance evaluation
- `eval_t105e_noise_off.py` - T105-E ablation (noise-off eval)
- `auto_fill_queue.sh` - Auto queue filler

### Results Location
- `report_md/_gpt/json_gpt/` - All JSON evaluation results
- `handoff_local/` - Communication logs with local team

### Key Findings
- DeiT: proportional > digital (+1.28pt average)
- ViT: Inconsistent results between seeds (requires seed 789 verification)
- Fresh degradation ≈ 0 for proportional mode
- Standard mode collapses (-34pt)

### Running Experiments
- Seed 789 training in progress (4 configs on GPUs 4,5,6,7)
- Expected completion: ~21 hours
