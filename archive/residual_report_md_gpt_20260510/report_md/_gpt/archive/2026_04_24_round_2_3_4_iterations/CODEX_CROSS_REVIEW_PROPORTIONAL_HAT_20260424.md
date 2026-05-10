You are an independent code auditor reviewing a post-fix experimental rerun for an academic paper on analog in-memory computing (CIM) with TinyViT on CIFAR-10.

EXPERIMENT: Standard HAT (V3), post-fix, NL=2.0
- Configuration: hybrid=True, noise_enabled=True, sigma_c2c=0.05, sigma_d2d=0.10, HAT=False, NL_LTP=2.0, NL_LTD=-2.0
- Training: fixed D2D mismatch during train, C2C off during train, standard noisy training policy
- Checkpoint: checkpoints/_gpt/postfix_standard_hat/V3_hybrid_standard_noise_standard_train_best.pt

FRESH EVAL RESULT (10 instances × 5 MC runs):
- cross_instance_mean: 82.6346%
- cross_instance_std: 0.5624%
- Range: 81.40% -- 83.36%

SAME-INSTANCE BASELINE:
- max_test_acc during training: ~83.3% at epoch 86
- Final epoch 99 test_acc: 53.5% (severe overfitting after plateau)

YOUR TASK:
1. Verify the fresh eval arithmetic (mean, std, range from instance_means)
2. Check for evaluation risks (NL override correctness, noise mode consistency, D2D resampling)
3. Compare train/eval gap: same-instance max 83.3% vs fresh eval mean 82.63% = only 0.67% degradation
4. Write a verdict: Is this result trustworthy? Any caveats?
5. Suggest safe phrasing for the manuscript.

Report your findings in a structured markdown format.

[?2004h[?1004h[6n]10;?\]0;compute_vit]0;⠋ compute_vit[?2026h[39m[49m[0m[?25h[3;3H[?2026l]0;⠹ compute_vit[?2026h[1;0r[1;1H
[39;49m[K[39m[49m[0m
[39;49m[K[1mT[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[K[1mi[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[K[1mp[39m[49m[0m
[39;49m[K [39m[49m[0m
[39;49m[K[1m:[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[K[3mN[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[K[3me[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[K[3mw[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[KU[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ks[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ke[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[K [39m[49m[0m
[39;49m[K[1m/[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[K[1mf[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[K[1ma[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[K[1ms[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[K[1mt[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kt[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ko[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ke[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kn[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ka[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kb[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kl[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ke[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ko[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ku[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kr[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kf[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ka[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ks[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kt[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ke[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ks[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kt[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ki[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kn[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kf[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ke[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kr[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ke[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kn[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kc[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ke[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kw[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ki[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kt[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kh[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ki[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kn[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kc[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kr[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ke[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ka[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ks[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ke[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kd[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kp[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kl[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ka[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kn[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ku[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ks[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ka[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Kg[39m[49m[0m
[39;49m[K[39m[49m[0m
[39;49m[Ke[39m[49m[0m
[39;49m[K [39m[49m[0m
[39;49m[K.[39m[49m[0m[r[3;3H[39m[49m[0m[?25h[3;3H[?2026l[?2026h[39m[49m[0m[?25h[3;3H[?2026l[?2026h[39m[49m[0m[?25h[3;3H[?2026l]0;⠸ compute_vit[?2026h[39m[49m[0m[?25h[3;3H[?2026l]0;⠼ compute_vit[?2026h[39m[49m[0m[?25h[3;3H[?2026l]0;compute_vit[?2026h[39m[49m[0m[?25h[3;3H[?2026l[?2026h[39m[49m[0m[?25h[3;3H[?2026l[?2026h[39m[49m[0m[?25h[3;3H[?2026l[?2026h[39m[49m[0m[?25h[3;3H[?2026l
