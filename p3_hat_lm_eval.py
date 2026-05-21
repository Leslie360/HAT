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


def _tasks_slug(tasks_str: str, num_fewshot: int = 0) -> str:
    """Return a short slug for a comma-separated task list to disambiguate output filenames."""
    parts = sorted(tasks_str.split(","))
    if parts == ["arc_easy", "hellaswag", "lambada_openai"]:
        base = "standard3"
    elif parts == ["boolq", "mmlu", "piqa", "winogrande"]:
        base = "extended"
    elif parts == ["boolq", "piqa", "winogrande"]:
        base = "ext3"
    elif parts == ["mmlu"]:
        base = "mmlu"
    elif parts == ["gsm8k"]:
        base = "gsm8k"
    elif parts == ["truthfulqa"] or parts == ["truthfulqa_mc1"]:
        base = "truthfulqa"
    elif parts == ["ai2_arc"]:
        base = "ai2_arc"
    else:
        abbr = "_".join(p.split("_")[0] for p in parts)
        base = abbr[:40] + f"_{len(parts)}tasks" if len(abbr) > 40 else abbr
    if num_fewshot > 0:
        base = f"{base}_{num_fewshot}fs"
    return base


def run_lm_eval(model, tokenizer, tasks: list, device: str = "cuda", batch_size: int = 1, num_fewshot: int = 0):
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
        num_fewshot=num_fewshot,
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
    parser.add_argument("--num_fewshot", type=int, default=0,
                        help="Number of few-shot examples (0 = zero-shot)")
    parser.add_argument("--batch_size", type=int, default=1)
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--output_dir", type=str, default=None)
    parser.add_argument("--output_suffix", type=str, default=None,
                        help="Optional suffix appended to output filename to disambiguate sweeps")
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
    results = run_lm_eval(model, tokenizer, tasks, device=args.device, batch_size=args.batch_size, num_fewshot=args.num_fewshot)
    wall_time = time.time() - start

    # Summarize key metrics
    summary = {}
    for task_name in tasks:
        task_res = results.get("results", {}).get(task_name, {})
        for metric_name, value in task_res.items():
            if hasattr(value, 'item'):
                value = value.item()
            if isinstance(value, (int, float)):
                summary[f"{task_name}:{metric_name}"] = round(float(value), 4)

    def _sanitize(obj):
        """Remove non-JSON-serializable items (functions, dtypes, tensors, etc.)."""
        if isinstance(obj, dict):
            return {k: _sanitize(v) for k, v in obj.items() if not callable(v)}
        elif isinstance(obj, list):
            return [_sanitize(v) for v in obj if not callable(v)]
        elif isinstance(obj, tuple):
            return tuple(_sanitize(v) for v in obj if not callable(v))
        elif isinstance(obj, set):
            return [_sanitize(v) for v in obj if not callable(v)]
        elif isinstance(obj, bytes):
            return obj.decode('utf-8', errors='replace')
        elif type(obj).__name__ in ('dtype', 'DType') or 'dtype' in type(obj).__name__.lower():
            return str(obj)
        elif hasattr(obj, 'item'):   # scalar tensor / numpy scalar
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
    tasks_slug = _tasks_slug(args.tasks, args.num_fewshot)
    extra = f"_{args.output_suffix}" if args.output_suffix else ""
    out_file = os.path.join(
        args.output_dir,
        f"lm_eval_{args.checkpoint_dir.rstrip('/').split('/')[-1]}_{suffix}{extra}_{tasks_slug}.json"
    )
    os.makedirs(args.output_dir, exist_ok=True)
    with open(out_file, "w") as f:
        json.dump(result_record, f, indent=2, default=str)
    print(f"\nSaved: {out_file}")
    print("Summary:", summary)


if __name__ == "__main__":
    main()
