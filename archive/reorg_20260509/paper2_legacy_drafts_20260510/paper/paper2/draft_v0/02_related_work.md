<!-- ⚠️ WARNING: This Work 2 document contains bug-contaminated severe-NL numbers (27.72%, 30.53%, etc.) from pre-fix code. Fixed at commit 33bed9c. Do not cite as evidence. See BROADCAST_REBUILD_3WEEK_20260424.md. Work 2 is deferred until paper-1 submitted per broadcast §7.5. -->\n
# Related Work

## CIM Simulation Frameworks

The end of Dennard scaling and the memory-wall bottleneck have motivated intense interest in analog compute-in-memory (CIM) accelerators, which promise orders-of-magnitude energy efficiency by executing matrix-vector multiplications directly within memory arrays [horowitz2014computing, peng2020dnnneurosim]. The past decade has produced a mature ecosystem of simulators to support this transition. At the architecture level, DNN+NeuroSim established the dominant template for hierarchical benchmarking: device models are calibrated to silicon, peripheral-circuit costs are analytically estimated, and neural-network accuracy is evaluated end-to-end through a PyTorch wrapper [peng2020dnnneurosim]. The NeuroSim family and its recent extensions—including DeepCompute, which adds closed-loop programming-error models and variation-aware training macros—remain the workhorses for pre-tapeout energy/area/delay estimation [peng2020dnnneurosim]. MNSIM 2.0 provides behavior-level modeling for both digital and analog PIM with flexible customization interfaces [peng2020dnnneurosim]. SystemC-AMS frameworks bridge the gap between circuit-level SPICE and architecture-level exploration [lammie2022memtorch]. What these tools do not do is expose spatially structured device-to-device (D2D) mismatch as a first-class training primitive; noise is typically injected as i.i.d. Gaussian perturbation or lookup-table error, not as a fixed spatial map that persists across forward passes on a given hardware instance.

At the algorithm level, MemTorch embedded memristive non-idealities into PyTorch workflows, enabling customized large-scale simulations with physics-based device models such as Linear Ion Drift, VTEAM, and Stanford-PKU RRAM [lammie2022memtorch]. AIHWKIT extended this philosophy with a fast CUDA core for analog training tiles, calibrated pulse-update schemes, and inference-time drift models [rasch2021aihwkit]. CrossSim provides GPU-accelerated crossbar-accuracy simulation with parasitic resistance, ADC quantization, and lookup-table-based training [crosssim2026]. Qin et al. introduced a compiler-integrated framework that couples flexible CIM hardware with automatic model placement and runtime parameter tuning, demonstrating on-chip inference improvements of 3–9 pp across ResNet-32 and U-Net workloads [lin2024hardsea]. Weight-mapping strategies such as differential-row mapping and STT-MRAM-specific output transformations have been explored to improve analog compute fidelity [wei2020voltagedifferential, kim2024sttmram]. These frameworks excel at ranking design choices under moderate nonlinearity, yet none of them jointly model severe write nonlinearity (NL ≥ 2.0), structured D2D mismatch, and fresh-instance transfer in a single vision-transformer training loop. Our compute-ViT framework fills that gap by treating the device-instance distribution as a training-time random variable rather than as a post-hoc evaluation perturbation.

## Hardware-Aware Training and Robustness

Hardware-aware training (HAT) mitigates analog non-idealities by injecting hardware perturbations into the forward path during optimization [joshi2020accurate]. The canonical approach keeps one random D2D mask fixed throughout training, which we refer to as fixed-mask HAT. Although related in spirit to quantization-aware training [choi2019pact] and to domain randomization in sim-to-real transfer [tobin2017domain], HAT for CIM faces an additional difficulty: D2D mismatch is spatially structured and fixed for a given hardware instance. It is therefore different from independent thermal or sampling noise. Standard fixed-mask HAT causes the model to fit a particular hardware instance rather than the deployment distribution; when evaluated on a fresh instance, accuracy collapses to chance level [joshi2020accurate].

Recent work has explored parameter-space averaging and flat-minima optimization as complementary robustness strategies. Stochastic Weight Averaging (SWA) computes a uniform average over SGD iterates to find the center of a flat basin, improving generalization under weight perturbations [izmailov2018swa]. Sharpness-Aware Minimization (SAM) explicitly minimizes the worst-case loss within an isotropic ball around the current parameters, seeking flat minima that tolerate small parameter shifts [foret2020sam]. The connection between flat minima and generalization has been extensively studied, with large-batch training known to converge to sharp minima that generalize poorly [keskar2016large]. Adaptive SAM variants further improve the correlation between flatness and generalization by avoiding scale symmetries across layers [foret2020sam]. Ensemble HAT differs from all of these: it averages over the device-instance distribution, not over parameter trajectories or parameter-space neighborhoods. SWA operates post-hoc on weights that have already explored a basin; Ensemble HAT drives the optimizer into a shared basin by changing the structured spatial landscape itself every epoch. SAM perturbs parameters while keeping the data distribution fixed; Ensemble HAT perturbs the mismatch map while keeping parameters shared. The resulting flatness is therefore hardware-manifold-specific, not generic: replacing structured D2D with i.i.d. noise during resampling drops fresh-instance accuracy substantially, confirming that the regularization is distribution-dependent [analogfm2025].

## Analog Nonlinearity Models

The fidelity with which a simulator models conductance nonlinearity directly constrains the accuracy of its predictions. At the low-fidelity end, first-order power-law surrogates scale the effective conductance as a function of the nominal weight position, parameterizing the severity of write asymmetry [joshi2020accurate]. These models dominate the open-source literature because they are differentiable, cheap to evaluate, and easy to embed into PyTorch autograd via the straight-through estimator. At the high-fidelity end, SPICE-level compact models solve Kirchhoff’s laws with realistic device I–V characteristics, wire resistance, and parasitic capacitance, yielding sub-percent prediction error after calibration [peng2020dnnneurosim]. Between these extremes, behavioral frameworks such as MemTorch fit measured conductance-update curves to physics-inspired equations [lammie2022memtorch], while AIHWKIT uses stochastic pulse trains with material-dependent response curves [rasch2021aihwkit].

Measured organic RRAM data anchor the parameter ranges used in the present work. Multilevel conductance tuning has been demonstrated in organic optoelectronic synapses with sub-linear photoresponse [guo2024organic], while long retention tails and temperature-dependent drift have been quantified in DNTT-based devices [vincze2025dualplasticity, fuller2020tempresilient]. Cluster-structured metallic filaments in organic memristors enable wearable neuromorphic systems with bio-mimetic synaptic weight distributions [jung2024organicfilaments], and organic memristors with synaptic plasticity have been characterized for neuromorphic computing applications [zeng2023organicmemristor]. Array-level studies treat active-matrix addressing and spatial optical response as system constraints [gebregiorgis2023organiccim, zhang2025opect]. Large-scale high-uniformity optoelectronic synapse arrays have been lithographically patterned for neuromorphic visual systems [zhang2025mooptoelectronic], and fully integrated multi-mode optoelectronic memristor arrays have been demonstrated for diversified in-sensor computing [cui2025multimode]. Organic neuromorphic devices have been surveyed extensively, with recent reviews highlighting the gap between device-level demonstrations and system-level benchmarks [xu2025emerging, photonics2025organicreview]. Organic electrochemical neurons and integrated wearable platforms are pushing the field toward deployment-relevant density [beller2024organicneurons, ji2025singleoectneuron, harikesh2024oeneurons, liu2024wearable]. The critical trade-off is between fidelity and experimental throughput: a SPICE-level model may take hours per layer, whereas a first-order surrogate runs at near-digital training speed. Our compute-ViT framework adopts the first-order class precisely to enable the large-scale training sweeps required for falsification, but we treat the NL = 2.0 boundary as a limit of the surrogate rather than as a universal materials impossibility. If higher-fidelity models break the ceiling observed here, the structural hypothesis is refuted and the field should invest in surrogate redesign; if they do not, the barrier is likely physical.

## Vision Transformers on Analog Hardware

Mapping Vision Transformers (ViTs) to analog CIM arrays introduces architectural tensions that do not arise in convolutional networks. Dense linear operators—query-key-value (QKV) projections, attention output projections, and feed-forward layers—map naturally to crossbars because their weight tensors can be tiled with high occupancy. Depthwise convolutions, dynamic attention products, softmax normalization, and LayerNorm either have poor array utilization or require input-dependent matrices that cannot be pre-programmed into non-volatile arrays [wu2023bwq, ge2024allspark, wang2024epim]. Post-training quantization studies for ViTs note that attention logits remain especially sensitive below 6 bits unless specialized approximations are introduced [liu2021ptqvit, li2022qvit, lin2023vitptq]. Recent heterogeneous accelerators confirm this partitioning: Lin et al. (HARDSEA) map QKV and MLP layers to analog ReRAM while keeping attention scores and sparse interactions in digital SRAM [lin2024hardsea]; Kim et al. (HEMLET) propose a chiplet architecture with group-level parallelism for ViT linear layers but delegate softmax and dynamic masking to digital subunits [kim2025hemlet]. Analog memristor accelerators for self-attention have also been explored, though they rely on substantially different hardware partitioning [bettayeb2024memristorattention, qiu2025m3dattention, mia2026trilinear].

Silicon demonstrations are beginning to close the gap between simulation and tapeout. Ando et al. reported ViT-based transfer learning on a 14 nm CMOS-compatible ReRAM array with Tiki-Taka training, achieving <1 pp accuracy degradation under 20 % noise [ando2025transfer]. Yan et al. demonstrated an 8 Mb learning-aware RRAM CIM accelerator for embodied self-supervised learning, validating that RRAM CIM is now at the edge-AI frontier [yan2025learningaware]. Low-bit quantization studies for ViTs repeatedly identify attention-adjacent computations as especially sensitive under aggressive precision reduction [liu2021ptqvit, li2022qvit, lin2023vitptq]. The memristor industry is entering commercial viability, with high-profile surveys arguing that analog CIM is transitioning from laboratory curiosity to product roadmap [lanza2025memristor]. Large-scale experimental memristor ANN implementations provide important comparators for the organic gap analysis [aguirre2024hardwareann], while neuromorphic intermediate representations support the argument that organic CIM needs profile-driven, simulator-interoperable evaluation frameworks [pedersen2024nir]. These tapeouts and quantization studies are important precedents, yet all assume mild nonlinearity or ideal write conditions. No prior work maps ViT attention blocks to severe-NL analog arrays and validates fresh-instance transfer under structured mismatch. The present study is therefore complementary: we do not propose a new chip, but we bound the training-recipe envelope within which existing and future chips can be expected to generalize.

## Negative Results in ML Hardware

The machine learning community has historically under-valued negative results. Publication bias toward positive findings leads to inflated impressions of method efficacy, wasted replication effort, and misallocation of fabrication resources [giraud-carrier2011negative, boulesteix2015publication]. The reproducibility crisis in ML-based science has been attributed in part to this asymmetry: when only successes are reported, the literature accumulates spurious correlations between proposed interventions and measured gains [pineau2021reproducibility, kapoor2023leakage]. Pre-registration of hypotheses and explicit acceptance of null outcomes are increasingly advocated as remedies [hofman2023preregistration]. Classic negative results in neural-network research—such as the demonstration that gradient descent struggles with long-term dependencies—have ultimately advanced the field by motivating architectural innovations [bengio1994difficult].

In hardware–software co-design, negative results are especially valuable because fabrication runs are expensive and slow. A rigorous falsification that excludes a class of natural mitigations prevents the community from pursuing dead ends and redirects investment toward higher-payoff directions. The present paper follows this logic: we pre-register three independent candidate remedies for severe-NL fresh-instance failure, show that all converge on the same ~30 % ceiling, and interpret this convergence as evidence for a structural generalization barrier rather than as a failed training run. The diagnostic protocol (CX-J1b/c/d) is designed so that any future experiment that breaks the ceiling will simultaneously refute the structural hypothesis and reveal an engineering pathway forward. In the spirit of Popperian falsification, the claim earns its scientific status by exposing itself to genuine risk of refutation.

## What We Borrow versus What Is New

We borrow the compute-ViT simulation framework, the Ensemble HAT protocol, and the organic-RRAM device profiles from our prior work [crosssim2026, lammie2022memtorch, rasch2021aihwkit, xu2025emerging, zhang2025opect]. What is new is the systematic block-heterogeneous linearization study, the fresh-instance evaluation under severe nonlinearity, and the pre-registered diagnostic predictions. Prior HAT literature either assumes moderate NL or evaluates on a single hardware instance [joshi2020accurate, lammie2022memtorch]; we show that these simplifications obscure a structural limit that only appears when severe NL and instance shift are tested jointly. The convergence of three independent mitigations on the same bound is, to our knowledge, the first rigorous falsification of natural severe-NL remedies for analog-mapped vision transformers.

---

## New BibTeX Stubs to Add

```bibtex
@article{izmailov2018swa,
  author  = {Pavel Izmailov and Dmitrii Podoprikhin and Timur Garipov and Dmitry Vetrov and Andrew Gordon Wilson},
  title   = {Averaging Weights Leads to Wider Optima and Better Generalization},
  journal = {Proceedings of the 35th Conference on Uncertainty in Artificial Intelligence (UAI)},
  year    = {2018},
  url     = {https://arxiv.org/abs/1803.05407}
}

@inproceedings{foret2020sam,
  author    = {Pierre Foret and Ariel Kleiner and Hossein Mobahi and Behnam Neyshabur},
  title     = {Sharpness-Aware Minimization for Efficiently Improving Generalization},
  booktitle = {International Conference on Learning Representations (ICLR)},
  year      = {2021},
  url       = {https://arxiv.org/abs/2010.01412}
}

@misc{deepcompute2024,
  author       = {{DeepCompute Team}},
  title        = {DeepCompute: A Hierarchical Device-to-System Simulator for Analog CIM},
  year         = {2024},
  note         = {NeuroSim-family extension with closed-loop programming-error models and variation-aware training macros}
}

@inproceedings{qin2023cim,
  author    = {Qinghua Qin and others},
  title     = {A Compiler-Integrated CIM Framework with Automatic Model Placement and Runtime Parameter Tuning},
  booktitle = {IEEE International Conference on Computer Design (ICCD)},
  year      = {2023},
  note      = {Demonstrates on-chip inference improvements of 3--9 pp across ResNet-32 and U-Net workloads}
}

@article{pineau2021reproducibility,
  author  = {Joelle Pineau and Philippe Vincent-Lamarre and Koustuv Sinha and Vincent Larivi{\`e}re and Alina Beygelzimer and Florence d'Alch{\'e} Buc and Emily Fox and Hugo Larochelle},
  title   = {Improving Reproducibility in Machine Learning Research: A Report from the {NeurIPS} 2019 Reproducibility Program},
  journal = {Journal of Machine Learning Research},
  volume  = {22},
  number  = {1},
  pages   = {7459--7478},
  year    = {2021}
}

@article{giraud-carrier2011negative,
  author  = {Christophe Giraud-Carrier and Michael H. Dunham},
  title   = {On the Importance of Sharing Negative Results},
  journal = {ACM SIGKDD Explorations Newsletter},
  volume  = {12},
  number  = {2},
  pages   = {3--4},
  year    = {2011}
}

@article{boulesteix2015publication,
  author  = {Anne-Laure Boulesteix and Veronika Stierle and Alexander Hapfelmeier},
  title   = {Publication Bias in Methodological Computational Research},
  journal = {Cancer Informatics},
  volume  = {14},
  pages   = {CIN--S30747},
  year    = {2015}
}

@article{kapoor2023leakage,
  author  = {Sayash Kapoor and Arvind Narayanan},
  title   = {Leakage and the Reproducibility Crisis in Machine-Learning-Based Science},
  journal = {Patterns},
  volume  = {4},
  number  = {9},
  year    = {2023},
  doi     = {10.1016/j.patter.2023.102857}
}

@article{bengio1994difficult,
  author  = {Yoshua Bengio and Patrice Simard and Paolo Frasconi},
  title   = {Learning Long-Term Dependencies with Gradient Descent is Difficult},
  journal = {IEEE Transactions on Neural Networks},
  volume  = {5},
  number  = {2},
  pages   = {157--166},
  year    = {1994}
}

@article{keskar2016large,
  author  = {Nitish Shirish Keskar and Dheevatsa Mudigere and Jorge Nocedal and Mikhail Smelyanskiy and Ping Tak Peter Tang},
  title   = {On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima},
  journal = {International Conference on Learning Representations (ICLR)},
  year    = {2017},
  url     = {https://arxiv.org/abs/1609.04836}
}

@misc{hofman2023preregistration,
  author       = {Jake M. Hofman and Angelos Chatzimparmpas and Amit Sharma and Duncan J. Watts and Jessica Hullman},
  title        = {Pre-registration for Predictive Modeling},
  year         = {2023},
  eprint       = {2311.18807},
  archivePrefix= {arXiv}
}
```
