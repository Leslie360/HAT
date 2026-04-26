# Codex W2 Held-Out Smoke Pilot — Seed 1234

Date: 2026-04-26  
Owner: Codex

## Verdict

The first held-out W2 smoke pilot is much stricter than the same-batch eval and prevents overclaiming:

- `all`: held-out eval delta `-0.0436` (barely positive route; weak generalization signal)
- `mlp`: held-out eval delta `+0.1898` (worse; no generalization signal in this seed)

This means the earlier same-batch/fresh-D2D matrix should remain an infrastructure result only. It does not justify paper-level LLM generalization claims.

## Protocol

Same as W2 low-noise route, but with `--eval-text-set heldout`:

- Model: `EleutherAI/pythia-410m-deduped`
- Seed: `1234`
- Train scope: last block
- Steps: `1000`
- Noise: `d2d=0.005`, `c2c=0.002`
- Scopes: `all`, `mlp`
- Fresh-D2D eval: 10 instances x 5 C2C repeats

## Results

| Scope | Eval Before | Eval After | Eval Delta | Fresh-D2D Mean | Fresh-D2D Std |
|---|---:|---:|---:|---:|---:|
| `all` | `7.3127` | `7.2691` | `-0.0436` | `7.1505` | `0.1707` |
| `mlp` | `6.4877` | `6.6775` | `+0.1898` | `6.4696` | `0.0865` |

Raw logs:

- `logs/_gpt/w2_heldout_freshd2d_all_n005002_lb1000_seed1234_20260426_112604.log`
- `logs/_gpt/w2_heldout_freshd2d_mlp_n005002_lb1000_seed1234_20260426_112604.log`

## Follow-Up

Codex launched seeds `456` and `789` for `all` and `mlp` under the same held-out protocol. Logs: `logs/_gpt/w2_heldout_freshd2d_{all,mlp}_n005002_lb1000_seed{456,789}_20260426_112930.log`.
