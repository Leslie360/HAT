# Public FAQ — Profile-Driven Behavioral Simulation for Organic Optoelectronic CIM

Welcome! This FAQ covers the most common questions we receive about installing, running, and extending our simulation framework. If you don't find what you need, see Question 15 for how to reach us.

> **1. I hit an installation error. What Python and PyTorch versions do I need?**

We target Python 3.11 and PyTorch ≥2.1 compiled against CUDA 12.1. The recommended path is `conda env create -f environment.yml && conda activate LLM`, because conda handles the CUDA toolkit for you. If you prefer pip, `pip install -r requirements.txt` works, but you must install the NVIDIA driver and CUDA toolkit separately.

> **2. How do I prepare datasets? Will CIFAR-10 download automatically?**

CIFAR-10, CIFAR-100, and Flowers-102 are downloaded automatically by `torchvision` into `./data/` on first use. ImageNet ILSVRC2012 must be supplied manually; see `download_data.sh` for the expected folder layout. Custom datasets are supported as long as they follow the standard PyTorch `Dataset` interface and are registered in the `DATASET_STATS` dictionary of the training script.

> **3. What is the exact command to reproduce the Ensemble HAT result (86.37 ± 1.54%)?**

Run the following from the repository root:

```bash
python train_tinyvit_ensemble.py --experiment V4 --mode train --dataset cifar10 --epochs 100
```

On a modern NVIDIA GPU, the full 100-epoch run completes in roughly 90 minutes, with the best accuracy typically reached between epochs 40 and 60. After training, evaluate the saved checkpoint with `python run_ensemble_hat_fixed.py` to obtain the ensemble mean and standard deviation across 10 fresh D2D instances.

> **4. What are the GPU requirements? Is there a minimum VRAM?**

Any NVIDIA GPU with ≥4 GB VRAM is sufficient for Tiny-ViT training and evaluation. We develop and test on RTX-series desktop cards and A100 datacenter GPUs. A CPU-only fallback exists—PyTorch automatically falls back to `device="cpu"` when CUDA is absent—but it is impractical for training (see Question 13).

> **5. How do I swap in a custom device profile? What is the JSON format?**

Device profiles are JSON files that map literature or measured metrics to simulation parameters. The schema is documented in `device_profile_utils.py`; key fields include `G_min`, `G_max`, `n_states`, `sigma_c2c`, `sigma_d2d`, `noise_mode`, `tau_1`, `tau_2`, `A_0`, `gamma_phys`, `I_dark`, `responsivity_alpha`, `NL_LTP`, `NL_LTD`, and `pulse_count_max`. Place your JSON under `device_profiles/` and load it with `load_device_profiles_json()`; an annotated example is provided in `device_profiles/example_measured_device_profile_gpt.json`.

> **6. How do I add a new architecture, such as a custom CNN or transformer?**

You only need to tell the framework which layers should map to analog crossbars. Create a `classify_layer(name, module)` function that returns `"analog"` or `"digital"` for each `nn.Linear` and `nn.Conv2d` in your model (see `tinyvit_hybrid_utils.py` for a worked example), then pass it to `convert_to_hybrid(model, config=analog_cfg, classify_fn=your_fn)`. No changes to the core noise or quantization kernels are required.

> **7. What is this simulator *not*?**

It is not a SPICE simulator—there are no transistor netlists, parasitic extractions, or circuit-level transient analyses. It is not chip-predictive—floorplan, routing congestion, and packaging effects are explicitly out of scope. It is not a foundry PDK—we do not provide design rules, DRC decks, or tape-out kits.

> **8. Can I use this framework for my own RRAM or CIM technology?**

Yes, with caveats. Write a JSON profile that captures your device's conductance range, cycle-to-cycle and device-to-device variability, retention decay, and programming non-linearity. The framework is validated against organic optoelectronic data; if your technology operates in a very different conductance or voltage regime, you should benchmark against a calibrated hardware reference before treating the absolute accuracy numbers as predictive.

> **9. How do I cite the paper?**

Please use the following BibTeX entry:

```bibtex
@article{li2026organic,
  title={Profile-Driven Behavioral Simulation of Organic Optoelectronic Compute-in-Memory for Edge Vision},
  author={Li, Songqiao and ...},
  journal={Nature Communications},
  year={2026}
}
```

> **10. What license covers the code?**

MIT unless otherwise specified by user.

> **11. Why CIFAR-10 and not ImageNet?**

Three reasons. First, scope isolation: CIFAR-10 lets us study physics-to-task accuracy mapping without confounding factors from complex augmentation pipelines and billion-parameter backbones. Second, compute budget: a full ImageNet training run would consume roughly two orders of magnitude more GPU time, slowing the research iteration loop. Third, physics-first: the non-idealities we target—retention drift, photoresponse nonlinearity, and device-to-device mismatch—are already accuracy-limiting at the CIFAR-10 scale, so the smaller dataset is sufficient to demonstrate and benchmark the framework.

> **12. How long does training take?**

On a modern GPU, one epoch of Tiny-ViT Hardware-Aware Training takes roughly 50–55 seconds. A full 50-epoch HAT run finishes in about 45 minutes, while the default 100-epoch schedule takes roughly 90 minutes. Ensemble evaluation—resampling D2D noise across 10 fresh hardware instances—adds another 2–3 minutes after the checkpoint is loaded.

> **13. Can I run this without a GPU?**

Technically yes: when CUDA is unavailable, PyTorch falls back to the CPU automatically. Practically, training is 10–20× slower, turning a 90-minute GPU run into an overnight CPU job. We strongly recommend a CUDA-capable GPU for any interactive development or ablation studies.

> **14. What if my results don't match exactly?**

Small deviations are expected and normal. PyTorch seeding is sensitive to GPU driver version, CUDA toolkit build, and even the number of CPU cores used for data loading, so identical seeds on different machines can produce slightly different weight trajectories. The reported standard deviations—86.37 ± 1.54% for Ensemble HAT and 87.95 ± 0.27% for the V4 canonical configuration—capture this run-to-run variation; if your mean falls inside the reported interval, your reproduction is successful.

> **15. How do I report bugs or request features?**

Open a GitHub issue with the `bug` or `enhancement` label, and include the exact command you ran, your environment (`python -c "import torch; print(torch.__version__)"`), and the observed versus expected behavior. For sensitive or embargoed questions, email the corresponding author directly.

---

*Last updated: 2026-04-20*
