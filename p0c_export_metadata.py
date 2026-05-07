"""
P0-C: Export train metadata for all K107-A and K107-C checkpoints.
Copies hat_config.json and train JSONs to deliverable/results_v3/train_meta/.
"""

import os
import json
import shutil

CKPT_BASE = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints"
OUT_DIR = "/home/lisq753/projects/HAT/HAT/deliverable/results_v3/train_meta"
os.makedirs(OUT_DIR, exist_ok=True)

CHECKPOINTS = [
    # K107-A
    "k107_a1_last1_seed42",
    "k107_a1_last1_seed123",
    "k107_a1_last1_seed456",
    "k107_a2_last2_seed42",
    "k107_a2_last2_seed123",
    "k107_a2_last2_seed456",
    "k107_a3_all_seed42",
    # K107-C
    "k107_c_128states_seed42",
    "k107_c_16states_seed42",
    "k107_c_32states_seed42",
    "k107_c_64states_seed42",
]


def main():
    for name in CHECKPOINTS:
        ckpt_dir = os.path.join(CKPT_BASE, name)
        if not os.path.isdir(ckpt_dir):
            print(f"[WARN] Checkpoint dir missing: {ckpt_dir}")
            continue

        # hat_config.json
        src_hat = os.path.join(ckpt_dir, "hat_config.json")
        dst_hat = os.path.join(OUT_DIR, f"{name}_hat_config.json")
        if os.path.isfile(src_hat):
            shutil.copy2(src_hat, dst_hat)
            print(f"  copied hat_config -> {dst_hat}")
        else:
            print(f"[WARN] Missing hat_config.json for {name}")

        # train JSON
        src_json = os.path.join(CKPT_BASE, f"{name}.json")
        dst_json = os.path.join(OUT_DIR, f"{name}_train.json")
        if os.path.isfile(src_json):
            shutil.copy2(src_json, dst_json)
            print(f"  copied train json -> {dst_json}")
        else:
            print(f"[WARN] Missing train JSON for {name}")

    print(f"[P0C] Metadata export complete. Output: {OUT_DIR}")


if __name__ == "__main__":
    main()
