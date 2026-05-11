"""
Eval a HAT checkpoint in purely digital mode (no analog patch).
For P0-B paired ablation B1.
"""
import os, sys, json, argparse, subprocess, time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

sys.path.insert(0, '/home/lisq753/projects/HAT/HAT')
from p3_hat_train import evaluate_ppl

def _git_info():
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=os.path.dirname(__file__),
                                         stderr=subprocess.DEVNULL, timeout=5).decode().strip()
        status = subprocess.check_output(["git", "status", "--short"], cwd=os.path.dirname(__file__),
                                         stderr=subprocess.DEVNULL, timeout=5).decode().strip()
    except Exception:
        commit, status = None, None
    return commit, status

def main():
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint_dir", type=str, required=True)
    parser.add_argument("--max_length", type=int, default=512)
    parser.add_argument("--output_dir", type=str, default=None)
    parser.add_argument("--device", type=str, default="cuda")
    args = parser.parse_args()

    if args.output_dir is None:
        args.output_dir = os.path.dirname(args.checkpoint_dir.rstrip('/'))

    print(f"Loading checkpoint from {args.checkpoint_dir} (digital mode, NO analog patch)...")
    model = AutoModelForCausalLM.from_pretrained(args.checkpoint_dir, torch_dtype=torch.float32)
    tokenizer = AutoTokenizer.from_pretrained(args.checkpoint_dir)
    tokenizer.pad_token = tokenizer.eos_token
    model = model.to(args.device)

    print("Evaluating PPL (digital)...")
    ppl = evaluate_ppl(model, tokenizer, args.device, max_length=args.max_length)
    print(f"PPL: {ppl:.2f}")

    git_commit, git_status_short = _git_info()
    gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "cpu"
    gpu_id = os.environ.get("CUDA_VISIBLE_DEVICES", "unknown")
    result = {
        "git_commit": git_commit,
        "git_status_short": git_status_short,
        "script": os.path.basename(__file__),
        "command": " ".join(sys.argv),
        "mode": "eval",
        "model": args.checkpoint_dir,
        "dataset_eval": "wikitext-2-raw-v1 (test)",
        "analog_patch": False,
        "n_states": None,
        "sigma_c2c": 0.0,
        "sigma_d2d": 0.0,
        "ctx_len": args.max_length,
        "stride": args.max_length,
        "batch_size": 1,
        "ppl": ppl,
        "wall_clock_time": time.time() - start_time,
        "gpu_id": gpu_id,
        "gpu_name": gpu_name,
    }

    out_file = os.path.join(args.output_dir, f"eval_{args.checkpoint_dir.rstrip('/').split('/')[-1]}_digital_noanalog.json")
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"Saved: {out_file}")

if __name__ == "__main__":
    main()
