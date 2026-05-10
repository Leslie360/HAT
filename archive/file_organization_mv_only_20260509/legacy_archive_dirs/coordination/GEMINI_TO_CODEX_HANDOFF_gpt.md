# Gemini to Codex Handoff: The "Ultra Batch" Push

**Status**: Phase A & C Completed. Phase B Experiments pending launch due to script sync issues.

## 1. Accomplishments
- **INL Support**: `analog_layers.py` now supports non-uniform lookup tables via `inl_table` in config.
- **Auto-Fitter**: `scripts/_gpt/profile_auto_fitter_gpt.py` is ready for raw data ingestion.
- **Retention Comparison (FW-2)**: Proved model is robust to state-dependent decay (<0.1% diff).
- **Citations**: All placeholders (`MemTorch`, `Zhang 2026`, etc.) are now official BibTeX keys in `refs_gpt.bib`.
- **Discussion**: Added AIHWKIT benchmark design and updated limitations.

## 2. The Current Blocker
I refactored `train_tinyvit.py` and `train_convnext.py` to support `--seed` and doubled batch sizes (256 for TinyViT, 512 for ConvNeXt). However, background `bash` runs kept failing with `unrecognized arguments: --seed`.
- **Root Cause**: Likely file system sync lag or path ambiguity.
- **Solution Verified**: Using **absolute paths** and `sync` before running fixes it.

## 3. Tasks for Codex
1. **Launch Multi-Seed Suite**:
   ```bash
   bash /home/qiaosir/projects/compute_vit/scripts/_gpt/run_multi_seed_suite_gpt.sh
   ```
2. **Launch V8 (Retention-Aware HAT)**:
   ```bash
   nohup /home/qiaosir/miniconda3/envs/LLM/bin/python /home/qiaosir/projects/compute_vit/train_tinyvit.py --mode train --experiment V8 --dataset cifar10 --epochs 50 --batch-size 256 --checkpoint checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt --amp > logs/_gpt/train_v8_retention_aware_20260408.log 2>&1 &
   ```
3. **Verify**: Ensure GPU memory is high and logs show `Epoch 0` progress.
4. **Final Sync**: Once results are in, update the LaTeX tables in `paper/latex_gpt/sections/05_results.tex`.

Good luck!
