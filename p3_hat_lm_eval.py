"""
HAT Downstream Evaluation via lm-evaluation-harness.

Loads a HAT-trained checkpoint (clean or analog), monkey-patches attention
for analog KV if requested, and runs lm-eval tasks.

Usage:
    python p3_hat_lm_eval.py --checkpoint_dir <path> --tasks lambada_openai,hellaswag,arc_easy
    python p3_hat_lm_eval.py --checkpoint_dir <path> --tasks lambada_openai --analog
"""

import os
import sys
import json
import argparse
import time

if not os.environ.get("HF_ENDPOINT"):
    os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

sys.path.insert(0, '/home/lisq753/projects/HAT/HAT')
from analog_layers import AnalogLinearConfig
from p3_hat_train import patch_model_for_hat


def run_lm_eval(model, tokenizer, tasks: list, device: str = "cuda", batch_size: int = 1):
    """Run lm-evaluation-harness on the given model."""
    from lm_eval import evaluator
    from lm_eval.models.huggingface import HFLM

    # Wrap model for lm-eval
    lm = HFLM(
        pretrained=model,
        tokenizer=tokenizer,
        batch_size=batch_size,
        device=device,
    )

    results = evaluator.simple_evaluate(
        model=lm,
        tasks=tasks,
        batch_size=batch_size,
        device=device,
    )
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint_dir", type=str, required=True)
    parser.add_argument("--tasks", type=str, default="lambada_openai,hellaswag,arc_easy",
                        help="Comma-separated lm-eval task names")
    parser.add_argument("--analog", action="store_true",
                        help="Enable analog KV noise during eval")
    parser.add_argument("--n_states", type=int, default=256)
    parser.add_argument("--sigma_c2c", type=float, default=0.01)
    parser.add_argument("--sigma_d2d", type=float, default=0.02)
    parser.add_argument("--analog_layers", type=str, default=None,
                        help="Override analog layers (auto-load from hat_config.json if not set)")
    parser.add_argument("--d2d-seed", type=int, default=None, dest="d2d_seed")
    parser.add_argument("--max_length", type=int, default=512)
    parser.add_argument("--batch_size", type=int, default=1)
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--output_dir", type=str, default=None)
    parser.add_argument("--fp16", action="store_true")
    args = parser.parse_args()

    if args.output_dir is None:
        args.output_dir = os.path.dirname(args.checkpoint_dir.rstrip('/'))

    # Auto-load hat_config.json for analog_layers + d2d_seed
    hat_config_path = os.path.join(args.checkpoint_dir, "hat_config.json")
    d2d_seed = args.d2d_seed
    analog_layers = set(int(x) for x in args.analog_layers.split(",")) if args.analog_layers else None
    if os.path.isfile(hat_config_path):
        with open(hat_config_path) as f:
            hat_cfg = json.load(f)
        if analog_layers is None and "analog_layers" in hat_cfg:
            analog_layers = set(hat_cfg["analog_layers"])
            print(f"Auto-loaded analog_layers: {analog_layers}")
        if d2d_seed is None and "d2d_seed" in hat_cfg:
            d2d_seed = hat_cfg["d2d_seed"]
            print(f"Auto-loaded d2d_seed: {d2d_seed}")
    if d2d_seed is None:
        d2d_seed = 0xD2D

    dtype = torch.bfloat16 if args.fp16 else torch.float32
    print(f"Loading checkpoint from {args.checkpoint_dir}...")
    model = AutoModelForCausalLM.from_pretrained(
        args.checkpoint_dir,
        torch_dtype=dtype,
        use_safetensors=True,
        local_files_only=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(args.checkpoint_dir, local_files_only=True)
    tokenizer.pad_token = tokenizer.eos_token
    model = model.to(args.device)

    if args.analog:
        analog_cfg = AnalogLinearConfig(
            n_states=args.n_states,
            sigma_c2c=args.sigma_c2c,
            sigma_d2d=args.sigma_d2d,
        )
        print("Patching attention for analog KV...")
        patch_model_for_hat(model, analog_cfg, analog_layers,
                            max_length=args.max_length,
                            d2d_seed=d2d_seed)
    else:
        print("Evaluating CLEAN checkpoint (no analog noise)")

    tasks = [t.strip() for t in args.tasks.split(",")]
    print(f"\nRunning lm-eval tasks: {tasks}")
    start = time.time()
    results = run_lm_eval(model, tokenizer, tasks, device=args.device, batch_size=args.batch_size)
    wall_time = time.time() - start

    # Summarize key metrics
    summary = {}
    for task_name in tasks:
        task_res = results.get("results", {}).get(task_name, {})
        for metric_name, value in task_res.items():
            if isinstance(value, float):
                summary[f"{task_name}:{metric_name}"] = round(value, 4)

    def _sanitize(obj):
        """Remove non-JSON-serializable items (functions, dtypes, tensors, etc.)."""
        if isinstance(obj, dict):
            return {k: _sanitize(v) for k, v in obj.items() if not callable(v)}
        elif isinstance(obj, list):
            return [_sanitize(v) for v in obj if not callable(v)]
        elif isinstance(obj, type) and hasattr(obj, '__name__') and obj.__name__.endswith('dtype'):
            # torch.dtype / numpy.dtype (torch.bfloat16 has no 'dtype' attr)
            return str(obj)
        elif hasattr(obj, 'item'):   # scalar tensor
            return obj.item()
        return obj

    result_record = {
        "script": os.path.basename(__file__),
        "command": " ".join(sys.argv),
        "checkpoint_dir": args.checkpoint_dir,
        "analog": args.analog,
        "n_states": args.n_states,
        "sigma_c2c": args.sigma_c2c,
        "sigma_d2d": args.sigma_d2d,
        "analog_layers": sorted(analog_layers) if analog_layers else None,
        "tasks": tasks,
        "summary": summary,
        "full_results": _sanitize(results),
        "wall_clock_time": wall_time,
    }

    suffix = "analog" if args.analog else "clean"
    out_file = os.path.join(
        args.output_dir,
        f"lm_eval_{args.checkpoint_dir.rstrip('/').split('/')[-1]}_{suffix}.json"
    )
    os.makedirs(args.output_dir, exist_ok=True)
    with open(out_file, "w") as f:
        json.dump(result_record, f, indent=2)
    print(f"\nSaved: {out_file}")
    print("Summary:", summary)


if __name__ == "__main__":
    main()
