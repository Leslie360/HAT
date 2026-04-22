#!/usr/bin/env python3
"""Lightweight unittest coverage for Tiny-ViT training helpers."""

import json
import tempfile
import unittest
from pathlib import Path

import torch

from analog_layers import AnalogLinear, AnalogLinearConfig
from train_tinyvit import (
    RunLogger,
    build_retention_metadata,
    build_dataset_pair,
    build_training_checkpoint_payload,
    build_results_markdown,
    export_result_rows,
    get_num_classes,
    get_training_checkpoint_paths,
    get_v_experiment_configs,
    init_training_history,
    maybe_resume_experiment,
    resolve_experiment_ids,
    set_noise_for_eval,
    set_noise_for_train,
    summarize_eval_runs,
)


class TinyViTHelperTests(unittest.TestCase):
    def test_resolve_experiment_ids_single_and_multi(self):
        configs = get_v_experiment_configs()

        self.assertEqual(resolve_experiment_ids("V4", None, configs), ["V4"])
        self.assertEqual(resolve_experiment_ids("V4", ["V3", "V5"], configs), ["V3", "V5"])
        self.assertEqual(resolve_experiment_ids("V4", ["V3,V5", "V5"], configs), ["V3", "V5"])

    def test_resolve_experiment_ids_all_keyword(self):
        configs = get_v_experiment_configs()
        self.assertEqual(resolve_experiment_ids("V4", ["ALL"], configs), list(configs.keys()))

    def test_summarize_eval_runs_single_and_multi(self):
        single = summarize_eval_runs([1.0], [88.5])
        self.assertEqual(single["eval_runs"], 1)
        self.assertEqual(single["test_acc_mean"], 88.5)
        self.assertEqual(single["test_acc_std"], 0.0)

        multi = summarize_eval_runs([1.0, 2.0, 3.0], [80.0, 82.0, 84.0])
        self.assertEqual(multi["eval_runs"], 3)
        self.assertEqual(multi["test_acc_mean"], 82.0)
        self.assertEqual(multi["test_acc_min"], 80.0)
        self.assertEqual(multi["test_acc_max"], 84.0)
        self.assertGreater(multi["test_acc_std"], 0.0)

    def test_export_result_rows_writes_json_csv_and_markdown(self):
        rows = [
            {
                "mode": "eval",
                "experiment": "V4",
                "experiment_name": "V4_hybrid_standard_noise_hat",
                "dataset": "cifar10",
                "checkpoint_path": "checkpoints/V4_hybrid_standard_noise_hat_best.pt",
                "eval_runs": 3,
                "test_acc_mean": 81.25,
                "test_acc_std": 1.5,
            }
        ]

        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            json_path = base / "json_gpt" / "tinyvit_results_gpt.json"
            csv_path = base / "csv_gpt" / "tinyvit_results_gpt.csv"
            md_path = base / "tinyvit_results_gpt.md"

            export_result_rows(rows, str(json_path), str(csv_path), str(md_path))

            self.assertTrue(json_path.exists())
            self.assertTrue(csv_path.exists())
            self.assertTrue(md_path.exists())

            loaded = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertEqual(loaded[0]["experiment"], "V4")
            self.assertIn("Tiny-ViT Results (GPT)", md_path.read_text(encoding="utf-8"))
            self.assertIn("acc=81.25%", build_results_markdown(rows))

    def test_export_result_rows_supports_retention_payload(self):
        retention_rows = [
            {
                "experiment": "V4",
                "experiment_name": "V4_hybrid_standard_noise_hat",
                "dataset": "cifar10",
                "time_s": 1000,
                "test_acc_mean": 84.2,
                "test_acc_std": 0.3,
                "mc_runs": 10,
                "checkpoint_path": "checkpoints/V4_hybrid_standard_noise_hat_best.pt",
            }
        ]
        retention_metadata = {
            "source_experiment": "V4_hybrid_standard_noise_hat",
            "checkpoint_path": "checkpoints/V4_hybrid_standard_noise_hat_best.pt",
            "epoch": 99,
            "best_acc": 95.1,
            "mc_runs": 10,
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            json_path = base / "json_gpt" / "tinyvit_retention_gpt.json"
            md_path = base / "tinyvit_retention_gpt.md"

            export_result_rows([], str(json_path), None, str(md_path), retention_rows, retention_metadata)

            loaded = json.loads(json_path.read_text(encoding="utf-8"))
            self.assertIn("retention", loaded)
            self.assertEqual(loaded["retention"][0]["time_s"], 1000)
            self.assertIn("Retention Sweep", md_path.read_text(encoding="utf-8"))

    def test_get_training_checkpoint_paths(self):
        exp_cfg = get_v_experiment_configs()["V4"]
        best_path, last_path = get_training_checkpoint_paths(exp_cfg, "checkpoints")
        self.assertTrue(best_path.endswith("V4_hybrid_standard_noise_hat_best.pt"))
        self.assertTrue(last_path.endswith("V4_hybrid_standard_noise_hat_last.pt"))

    def test_maybe_resume_experiment_prefers_last_checkpoint(self):
        exp_cfg = get_v_experiment_configs()["V2"]

        with tempfile.TemporaryDirectory() as tmpdir:
            save_dir = Path(tmpdir)
            best_path, last_path = get_training_checkpoint_paths(exp_cfg, str(save_dir))

            model = torch.nn.Linear(4, 2)
            optimizer = torch.optim.AdamW(model.parameters(), lr=exp_cfg.lr, weight_decay=exp_cfg.weight_decay)
            scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=exp_cfg.epochs)
            history = init_training_history()
            history["train_loss"] = [1.2, 0.9]
            history["test_acc"] = [80.0, 82.5]

            with torch.no_grad():
                model.weight.fill_(0.25)
                model.bias.fill_(0.5)

            payload = build_training_checkpoint_payload(
                model, optimizer, scheduler, None, exp_cfg, "cifar10", 10,
                epoch=7, best_acc=82.5, best_epoch=6, history=history, amp_enabled=False
            )
            torch.save(payload, best_path)

            with torch.no_grad():
                model.weight.fill_(1.5)
                model.bias.fill_(1.0)
            payload = build_training_checkpoint_payload(
                model, optimizer, scheduler, None, exp_cfg, "cifar10", 10,
                epoch=9, best_acc=84.0, best_epoch=9, history=history, amp_enabled=False
            )
            torch.save(payload, last_path)

            new_model = torch.nn.Linear(4, 2)
            new_optimizer = torch.optim.AdamW(new_model.parameters(), lr=exp_cfg.lr, weight_decay=exp_cfg.weight_decay)
            new_scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(new_optimizer, T_max=exp_cfg.epochs)

            start_epoch, best_acc, best_epoch, resumed_best_path, resumed_last_path, resumed_history, resume_path = (
                maybe_resume_experiment(
                    new_model, new_optimizer, new_scheduler, None, exp_cfg,
                    str(save_dir), device="cpu", dataset="cifar10", num_classes=10,
                    resume_existing=True
                )
            )

            self.assertEqual(start_epoch, 10)
            self.assertEqual(best_acc, 84.0)
            self.assertEqual(best_epoch, 9)
            self.assertEqual(resumed_best_path, best_path)
            self.assertEqual(resumed_last_path, last_path)
            self.assertEqual(resume_path, last_path)
            self.assertEqual(resumed_history["test_acc"], [80.0, 82.5])
            self.assertTrue(torch.allclose(new_model.weight, torch.full_like(new_model.weight, 1.5)))
            self.assertTrue(torch.allclose(new_model.bias, torch.full_like(new_model.bias, 1.0)))

    def test_maybe_resume_experiment_skips_incompatible_dataset_checkpoint(self):
        exp_cfg = get_v_experiment_configs()["V1"]

        with tempfile.TemporaryDirectory() as tmpdir:
            save_dir = Path(tmpdir)
            best_path, _ = get_training_checkpoint_paths(exp_cfg, str(save_dir))

            model = torch.nn.Linear(4, 10)
            optimizer = torch.optim.AdamW(model.parameters(), lr=exp_cfg.lr, weight_decay=exp_cfg.weight_decay)
            scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=exp_cfg.epochs)
            payload = build_training_checkpoint_payload(
                model, optimizer, scheduler, None, exp_cfg, "cifar10", 10,
                epoch=3, best_acc=70.0, best_epoch=3, history=init_training_history(), amp_enabled=False
            )
            torch.save(payload, best_path)

            new_model = torch.nn.Linear(4, 100)
            new_optimizer = torch.optim.AdamW(new_model.parameters(), lr=exp_cfg.lr, weight_decay=exp_cfg.weight_decay)
            new_scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(new_optimizer, T_max=exp_cfg.epochs)

            start_epoch, best_acc, best_epoch, _, _, history, resume_path = maybe_resume_experiment(
                new_model, new_optimizer, new_scheduler, None, exp_cfg,
                str(save_dir), device="cpu", dataset="cifar100", num_classes=100,
                resume_existing=True
            )

            self.assertEqual(start_epoch, 0)
            self.assertEqual(best_acc, 0.0)
            self.assertEqual(best_epoch, -1)
            self.assertEqual(history, init_training_history())
            self.assertIsNone(resume_path)

    def test_get_num_classes_supports_cifar100(self):
        self.assertEqual(get_num_classes("cifar10"), 10)
        self.assertEqual(get_num_classes("cifar100"), 100)
        self.assertEqual(get_num_classes("flowers102"), 102)

    def test_noise_routing_propagates_nl_and_noise_mode(self):
        model = torch.nn.Sequential(
            AnalogLinear(4, 3, config=AnalogLinearConfig()),
            AnalogLinear(3, 2, config=AnalogLinearConfig()),
        )
        cfg = get_v_experiment_configs()["V4"]
        cfg.nl_ltp = 2.0
        cfg.nl_ltd = -2.5
        cfg.noise_mode = "proportional"

        set_noise_for_train(model, cfg)
        set_noise_for_eval(model, cfg)

        for module in model.modules():
            if isinstance(module, AnalogLinear):
                self.assertEqual(module.config.noise_mode, "proportional")
                self.assertAlmostEqual(module.config.NL_LTP, 2.0)
                self.assertAlmostEqual(module.config.NL_LTD, -2.5)

    def test_build_dataset_pair_uses_train_flag_for_cifar_style_datasets(self):
        created = []

        class FakeDataset(torch.utils.data.Dataset):
            def __init__(self, root, train, download, transform):
                created.append({"root": root, "train": train, "download": download, "transform": transform})

            def __len__(self):
                return 1

            def __getitem__(self, index):
                return torch.zeros(3, 4, 4), 0

        trainset, testset = build_dataset_pair(
            dataset="cifar10",
            data_root="/tmp/fake",
            transform_train="train_tf",
            transform_test="test_tf",
            download=False,
            dataset_cls=FakeDataset,
        )

        self.assertEqual(len(created), 2)
        self.assertTrue(created[0]["train"])
        self.assertFalse(created[1]["train"])
        self.assertEqual(created[0]["transform"], "train_tf")
        self.assertEqual(created[1]["transform"], "test_tf")
        self.assertIsInstance(trainset, FakeDataset)
        self.assertIsInstance(testset, FakeDataset)

    def test_build_dataset_pair_combines_flowers_train_and_val(self):
        created = []

        class FakeFlowers(torch.utils.data.Dataset):
            def __init__(self, root, split, download, transform):
                created.append({"root": root, "split": split, "download": download, "transform": transform})
                self.split = split

            def __len__(self):
                return 1

            def __getitem__(self, index):
                return torch.zeros(3, 4, 4), 0

        trainset, testset = build_dataset_pair(
            dataset="flowers102",
            data_root="/tmp/flowers",
            transform_train="train_tf",
            transform_test="test_tf",
            download=False,
            dataset_cls=FakeFlowers,
        )

        self.assertEqual([entry["split"] for entry in created], ["train", "val", "test"])
        self.assertIsInstance(trainset, torch.utils.data.ConcatDataset)
        self.assertEqual(len(trainset.datasets), 2)
        self.assertIsInstance(testset, FakeFlowers)
        self.assertEqual(testset.split, "test")

    def test_build_retention_metadata_tracks_checkpoint_context(self):
        exp_cfg = get_v_experiment_configs()["V4"]
        ckpt = {
            "epoch": 12,
            "best_acc": 94.5,
            "dataset": "cifar10",
            "exp_cfg": {"epochs": 100},
        }
        metadata = build_retention_metadata("V4", exp_cfg, "checkpoints/V4_best.pt", ckpt, eval_runs=10)
        self.assertEqual(metadata["experiment"], "V4")
        self.assertEqual(metadata["mc_runs"], 10)
        self.assertEqual(metadata["trained_epochs"], 100)

    def test_standard_noise_train_enables_d2d_but_disables_c2c(self):
        exp_cfg = get_v_experiment_configs()["V3"]
        from analog_layers import AnalogLinear, AnalogLinearConfig
        analog = AnalogLinear(4, 2, config=AnalogLinearConfig(sigma_d2d=exp_cfg.sigma_d2d))
        model = torch.nn.Sequential(analog)

        set_noise_for_train(model, exp_cfg)

        self.assertTrue(analog.config.noise_enabled)
        self.assertEqual(analog.config.sigma_c2c, 0.0)
        self.assertEqual(analog.config.sigma_d2d, exp_cfg.sigma_d2d)

    def test_run_logger_prefixes_timestamps(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "logger.log"
            logger = RunLogger(str(log_path))
            try:
                logger.log("hello")
                logger.log("")
            finally:
                logger.close()
            text = log_path.read_text(encoding="utf-8").splitlines()
            self.assertRegex(text[0], r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] hello$")
            self.assertEqual(text[1], "")


if __name__ == "__main__":
    unittest.main()
