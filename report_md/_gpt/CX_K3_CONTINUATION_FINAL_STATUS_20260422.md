# CX-K3 Continuation Final Status

- Timestamp: 2026-04-22 10:13:02 CST
- Target PID: 1735310
- Aggregate JSON present: yes
- Aggregate MD present: yes

## Driver Tail

```text
[2026-04-22 04:46:52]   hybrid=True, noise=True, C2C=0.05, D2D=0.1, HAT=True
[2026-04-22 04:46:52]   amp=on
[2026-04-22 04:46:52] ======================================================================
[2026-04-22 04:46:52]   Ensemble HAT active: Resampled D2D mismatch for 42 analog modules.
[2026-04-22 04:48:33]   Epoch   0/100: train_loss=0.0519, train_acc=98.27%, test_acc=85.80% (best=85.80%), lr=0.000500
[2026-04-22 04:54:33]   Epoch   4/100: train_loss=0.0618, train_acc=97.84%, test_acc=84.53% (best=87.68%), lr=0.000498
[2026-04-22 05:02:05]   Epoch   9/100: train_loss=0.0541, train_acc=98.13%, test_acc=87.70% (best=88.28%), lr=0.000490
[2026-04-22 05:09:40]   Epoch  14/100: train_loss=0.0482, train_acc=98.34%, test_acc=88.43% (best=88.43%), lr=0.000476
[2026-04-22 05:17:12]   Epoch  19/100: train_loss=0.0447, train_acc=98.49%, test_acc=85.01% (best=88.97%), lr=0.000457
[2026-04-22 05:24:45]   Epoch  24/100: train_loss=0.0429, train_acc=98.52%, test_acc=88.41% (best=88.97%), lr=0.000432
[2026-04-22 05:32:19]   Epoch  29/100: train_loss=0.0376, train_acc=98.71%, test_acc=86.34% (best=88.97%), lr=0.000403
[2026-04-22 05:39:50]   Epoch  34/100: train_loss=0.0329, train_acc=98.89%, test_acc=87.91% (best=89.11%), lr=0.000370
[2026-04-22 05:47:27]   Epoch  39/100: train_loss=0.0263, train_acc=99.07%, test_acc=89.78% (best=90.22%), lr=0.000335
[2026-04-22 05:55:00]   Epoch  44/100: train_loss=0.0230, train_acc=99.22%, test_acc=87.06% (best=90.22%), lr=0.000297
[2026-04-22 06:02:33]   Epoch  49/100: train_loss=0.0181, train_acc=99.39%, test_acc=89.67% (best=90.22%), lr=0.000258
[2026-04-22 06:10:03]   Epoch  54/100: train_loss=0.0136, train_acc=99.54%, test_acc=89.63% (best=90.22%), lr=0.000219
[2026-04-22 06:17:34]   Epoch  59/100: train_loss=0.0094, train_acc=99.70%, test_acc=89.83% (best=90.63%), lr=0.000180
[2026-04-22 06:25:10]   Epoch  64/100: train_loss=0.0068, train_acc=99.75%, test_acc=90.43% (best=90.63%), lr=0.000144
[2026-04-22 06:32:49]   Epoch  69/100: train_loss=0.0053, train_acc=99.83%, test_acc=89.81% (best=91.04%), lr=0.000109
[2026-04-22 06:40:25]   Epoch  74/100: train_loss=0.0036, train_acc=99.88%, test_acc=90.81% (best=91.22%), lr=0.000079
[2026-04-22 06:47:56]   Epoch  79/100: train_loss=0.0019, train_acc=99.95%, test_acc=90.88% (best=91.22%), lr=0.000052
[2026-04-22 06:55:29]   Epoch  84/100: train_loss=0.0014, train_acc=99.95%, test_acc=90.67% (best=91.33%), lr=0.000031
[2026-04-22 07:03:03]   Epoch  89/100: train_loss=0.0011, train_acc=99.97%, test_acc=91.43% (best=91.43%), lr=0.000015
[2026-04-22 07:10:33]   Epoch  94/100: train_loss=0.0013, train_acc=99.95%, test_acc=91.15% (best=91.50%), lr=0.000004
[2026-04-22 07:18:08]   Epoch  99/100: train_loss=0.0010, train_acc=99.97%, test_acc=91.24% (best=91.50%), lr=0.000000
[2026-04-22 07:18:08]   Finished. Best accuracy: 91.50% at epoch 93; checkpoint=/home/qiaosir/projects/compute_vit/checkpoints/_gpt/cx_k3_dgeff/k3_dgeff_0p20/V4_hybrid_standard_noise_hat_k3_dgeff_0p20_best.pt
[2026-04-22 07:18:08] Training finished for 1 experiment(s).
[2026-04-22 07:18:08] Result markdown: /home/qiaosir/projects/compute_vit/report_md/_gpt/cx_k3_train_k3_dgeff_0p20.md

Evaluating fresh-instance transfer for: /home/qiaosir/projects/compute_vit/checkpoints/_gpt/cx_k3_dgeff/k3_dgeff_0p20/V4_hybrid_standard_noise_hat_k3_dgeff_0p20_best.pt
/home/qiaosir/miniconda3/envs/LLM/lib/python3.11/site-packages/torchvision/datasets/cifar.py:83: VisibleDeprecationWarning: dtype(): align should be passed as Python or NumPy boolean but got `align=0`. Did you mean to pass a tuple to create a subarray type? (Deprecated NumPy 2.4)
  entry = pickle.load(f, encoding="latin1")
  instance 01/10: mean_acc=26.76% eval_runs=5
  instance 02/10: mean_acc=19.07% eval_runs=5
  instance 03/10: mean_acc=36.30% eval_runs=5
  instance 04/10: mean_acc=19.93% eval_runs=5
  instance 05/10: mean_acc=41.21% eval_runs=5
  instance 06/10: mean_acc=43.45% eval_runs=5
  instance 07/10: mean_acc=31.79% eval_runs=5
  instance 08/10: mean_acc=47.75% eval_runs=5
  instance 09/10: mean_acc=24.62% eval_runs=5
  instance 10/10: mean_acc=41.60% eval_runs=5
Completed: 33.25% +/- 10.29% across 10 fresh instances
JSON saved to: /home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/cx_k3_eval_k3_dgeff_0p20.json
Group-wise NL mitigation wrapper active: group=mlp, protected_nl=(1.0, -1.0), name_suffix=_k3_dgeff_0p25, 2nd_order_ste=True, delta_g_eff=0.25
[2026-04-22 07:28:58] Device: cuda
[2026-04-22 07:28:58] Mode: train
[2026-04-22 07:28:58] Experiments: ['V4']
[2026-04-22 07:28:58] AMP requested: True, active: True
/home/qiaosir/miniconda3/envs/LLM/lib/python3.11/site-packages/torchvision/datasets/cifar.py:83: VisibleDeprecationWarning: dtype(): align should be passed as Python or NumPy boolean but got `align=0`. Did you mean to pass a tuple to create a subarray type? (Deprecated NumPy 2.4)
  entry = pickle.load(f, encoding="latin1")
[2026-04-22 07:29:04] Warm-start mode: weights only from checkpoints/_gpt/second_order_ste/V4_hybrid_standard_noise_hat_second_order_ste_best.pt; epoch/best/optimizer/scheduler state reset.

[2026-04-22 07:29:04] ======================================================================
[2026-04-22 07:29:04] Experiment V4: V4_hybrid_standard_noise_hat_k3_dgeff_0p25
[2026-04-22 07:29:04]   hybrid=True, noise=True, C2C=0.05, D2D=0.1, HAT=True
[2026-04-22 07:29:04]   amp=on
[2026-04-22 07:29:04] ======================================================================
[2026-04-22 07:29:04]   Ensemble HAT active: Resampled D2D mismatch for 42 analog modules.
[2026-04-22 07:30:41]   Epoch   0/100: train_loss=0.0516, train_acc=98.29%, test_acc=85.53% (best=85.53%), lr=0.000500
[2026-04-22 07:36:43]   Epoch   4/100: train_loss=0.0620, train_acc=97.86%, test_acc=88.57% (best=88.57%), lr=0.000498
[2026-04-22 07:44:15]   Epoch   9/100: train_loss=0.0576, train_acc=97.98%, test_acc=87.77% (best=88.84%), lr=0.000490
[2026-04-22 07:51:52]   Epoch  14/100: train_loss=0.0516, train_acc=98.21%, test_acc=84.12% (best=89.15%), lr=0.000476
[2026-04-22 07:59:32]   Epoch  19/100: train_loss=0.0476, train_acc=98.38%, test_acc=88.22% (best=89.15%), lr=0.000457
[2026-04-22 08:07:12]   Epoch  24/100: train_loss=0.0381, train_acc=98.66%, test_acc=87.91% (best=89.36%), lr=0.000432
[2026-04-22 08:14:51]   Epoch  29/100: train_loss=0.0400, train_acc=98.64%, test_acc=87.85% (best=89.36%), lr=0.000403
[2026-04-22 08:22:26]   Epoch  34/100: train_loss=0.0289, train_acc=99.01%, test_acc=88.09% (best=89.66%), lr=0.000370
[2026-04-22 08:30:01]   Epoch  39/100: train_loss=0.0268, train_acc=99.05%, test_acc=88.25% (best=89.97%), lr=0.000335
[2026-04-22 08:37:40]   Epoch  44/100: train_loss=0.0202, train_acc=99.30%, test_acc=88.26% (best=89.97%), lr=0.000297
[2026-04-22 08:45:21]   Epoch  49/100: train_loss=0.0152, train_acc=99.52%, test_acc=89.71% (best=89.97%), lr=0.000258
[2026-04-22 08:52:59]   Epoch  54/100: train_loss=0.0144, train_acc=99.50%, test_acc=89.11% (best=89.97%), lr=0.000219
[2026-04-22 09:00:32]   Epoch  59/100: train_loss=0.0131, train_acc=99.56%, test_acc=89.09% (best=90.32%), lr=0.000180
[2026-04-22 09:08:18]   Epoch  64/100: train_loss=0.0061, train_acc=99.81%, test_acc=90.04% (best=90.80%), lr=0.000144
[2026-04-22 09:15:56]   Epoch  69/100: train_loss=0.0049, train_acc=99.85%, test_acc=89.86% (best=90.80%), lr=0.000109
[2026-04-22 09:23:31]   Epoch  74/100: train_loss=0.0037, train_acc=99.88%, test_acc=90.64% (best=91.01%), lr=0.000079
[2026-04-22 09:31:12]   Epoch  79/100: train_loss=0.0021, train_acc=99.94%, test_acc=90.60% (best=91.24%), lr=0.000052
[2026-04-22 09:38:54]   Epoch  84/100: train_loss=0.0017, train_acc=99.95%, test_acc=89.97% (best=91.24%), lr=0.000031
[2026-04-22 09:46:26]   Epoch  89/100: train_loss=0.0010, train_acc=99.97%, test_acc=90.86% (best=91.24%), lr=0.000015
[2026-04-22 09:54:05]   Epoch  94/100: train_loss=0.0012, train_acc=99.96%, test_acc=90.81% (best=91.24%), lr=0.000004
[2026-04-22 10:01:51]   Epoch  99/100: train_loss=0.0010, train_acc=99.97%, test_acc=89.55% (best=91.24%), lr=0.000000
[2026-04-22 10:01:51]   Finished. Best accuracy: 91.24% at epoch 76; checkpoint=/home/qiaosir/projects/compute_vit/checkpoints/_gpt/cx_k3_dgeff/k3_dgeff_0p25/V4_hybrid_standard_noise_hat_k3_dgeff_0p25_best.pt
[2026-04-22 10:01:51] Training finished for 1 experiment(s).
[2026-04-22 10:01:51] Result markdown: /home/qiaosir/projects/compute_vit/report_md/_gpt/cx_k3_train_k3_dgeff_0p25.md

Evaluating fresh-instance transfer for: /home/qiaosir/projects/compute_vit/checkpoints/_gpt/cx_k3_dgeff/k3_dgeff_0p25/V4_hybrid_standard_noise_hat_k3_dgeff_0p25_best.pt
/home/qiaosir/miniconda3/envs/LLM/lib/python3.11/site-packages/torchvision/datasets/cifar.py:83: VisibleDeprecationWarning: dtype(): align should be passed as Python or NumPy boolean but got `align=0`. Did you mean to pass a tuple to create a subarray type? (Deprecated NumPy 2.4)
  entry = pickle.load(f, encoding="latin1")
  instance 01/10: mean_acc=23.91% eval_runs=5
  instance 02/10: mean_acc=29.85% eval_runs=5
  instance 03/10: mean_acc=27.49% eval_runs=5
  instance 04/10: mean_acc=27.38% eval_runs=5
  instance 05/10: mean_acc=41.31% eval_runs=5
  instance 06/10: mean_acc=30.02% eval_runs=5
  instance 07/10: mean_acc=15.75% eval_runs=5
  instance 08/10: mean_acc=25.60% eval_runs=5
  instance 09/10: mean_acc=31.06% eval_runs=5
  instance 10/10: mean_acc=48.39% eval_runs=5
Completed: 30.08% +/- 9.07% across 10 fresh instances
JSON saved to: /home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/cx_k3_eval_k3_dgeff_0p25.json
K3 continuation complete. Summary written to /home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/cx_k3_dgeff_continuation.json
```

## Aggregate JSON Head

```json
{
  "stage": "K3_continuation",
  "warm_start_from": "checkpoints/_gpt/second_order_ste/V4_hybrid_standard_noise_hat_second_order_ste_best.pt",
  "epochs": 100,
  "batch_size": 128,
  "num_workers": 0,
  "fresh_instances": 10,
  "eval_runs": 5,
  "results": {
    "k3_dgeff_0p05": {
      "delta_g_eff": 0.05,
      "train_best_acc": 91.52,
      "train_best_epoch": 72,
      "fresh_mean": 36.2118,
      "fresh_std": 9.613163218559572,
      "fresh_instances": 10,
      "mc_runs_per_instance": 5,
      "checkpoint_path": "/home/qiaosir/projects/compute_vit/checkpoints/_gpt/cx_k3_dgeff/k3_dgeff_0p05/V4_hybrid_standard_noise_hat_k3_dgeff_0p05_best.pt"
    },
    "k3_dgeff_0p10": {
      "delta_g_eff": 0.1,
      "train_best_acc": 90.97,
      "train_best_epoch": 92,
      "fresh_mean": 30.7934,
      "fresh_std": 11.5895997074005,
      "fresh_instances": 10,
      "mc_runs_per_instance": 5,
      "checkpoint_path": "/home/qiaosir/projects/compute_vit/checkpoints/_gpt/cx_k3_dgeff/k3_dgeff_0p10/V4_hybrid_standard_noise_hat_k3_dgeff_0p10_best.pt"
    },
    "k3_dgeff_0p15": {
      "delta_g_eff": 0.15,
      "train_best_acc": 91.27,
      "train_best_epoch": 82,
      "fresh_mean": 27.8508,
      "fresh_std": 7.365293639767527,
      "fresh_instances": 10,
      "mc_runs_per_instance": 5,
      "checkpoint_path": "/home/qiaosir/projects/compute_vit/checkpoints/_gpt/cx_k3_dgeff/k3_dgeff_0p15/V4_hybrid_standard_noise_hat_k3_dgeff_0p15_best.pt"
    },
    "k3_dgeff_0p20": {
      "delta_g_eff": 0.2,
      "train_best_acc": 91.5,
      "train_best_epoch": 93,
      "fresh_mean": 33.248400000000004,
      "fresh_std": 10.2938015782962,
      "fresh_instances": 10,
      "mc_runs_per_instance": 5,
      "checkpoint_path": "/home/qiaosir/projects/compute_vit/checkpoints/_gpt/cx_k3_dgeff/k3_dgeff_0p20/V4_hybrid_standard_noise_hat_k3_dgeff_0p20_best.pt"
    },
    "k3_dgeff_0p25": {
      "delta_g_eff": 0.25,
      "train_best_acc": 91.24,
      "train_best_epoch": 76,
      "fresh_mean": 30.0756,
      "fresh_std": 9.067994892906468,
      "fresh_instances": 10,
      "mc_runs_per_instance": 5,
      "checkpoint_path": "/home/qiaosir/projects/compute_vit/checkpoints/_gpt/cx_k3_dgeff/k3_dgeff_0p25/V4_hybrid_standard_noise_hat_k3_dgeff_0p25_best.pt"
    }
  },
  "best_tag": "k3_dgeff_0p05",
  "mean_of_means": 31.636
}
```
