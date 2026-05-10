# Config-Sharing Bug Confirmation

Date: 2026-04-22
Author: Codex (local)

## Verdict

Remote's config-sharing diagnosis is valid on the local codebase.

I confirmed locally that:

1. `AnalogLinear` and `AnalogConv2d` used to keep a direct reference to the incoming
   `AnalogLinearConfig` object.
2. `convert_to_hybrid()` passed the same `config` object to every replaced analog
   layer.
3. As a result, any later per-layer mutation of `module.config` could silently
   overwrite the effective settings of all analog layers that shared that object.

This affects any experiment that depends on layer-specific configuration after
model conversion, especially:

- groupwise NL protection (`group=mlp`, `group=qkv`, `group=attn_proj`)
- higher-order surrogate sweeps (`J1d`, `K2`, `K3`, `K4`, `K5`)

It does **not** automatically invalidate experiments where all analog layers are
intentionally assigned the same settings (for example `group=all` with uniform NL),
but it does invalidate the interpretation of historical mixed-NL results.

## Local confirmation

Before the fix:

- `AnalogLinear(…, config=cfg)` twice produced shared `config` references.
- `convert_to_hybrid()` also produced shared `config` references across replaced
  layers.

After the fix:

- constructors now shallow-copy incoming `AnalogLinearConfig`
- conversion helpers also copy the seed config before per-layer construction
- regression tests confirm:
  - direct constructions do not share config
  - converted layers do not share config

## Scope impact

The following local result families should be treated as suspect unless rerun under
the fixed code:

- historical `J1d`
- `K2`
- `K3`
- `K4`
- `K5`

The right next step is **not** a full rerun first. The right next step is a
minimal local parity probe set under the fixed code to see whether the remote
behavior reproduces locally.
