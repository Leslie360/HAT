# G-BB2: IR-drop preliminary modeling spec

## Goal
Define the smallest circuit-aware extension that can answer the reviewer question: “What happens if line resistance introduces spatial IR drop beyond the current first-order proxy?”

## Minimal model
- Tile granularity: start with **16x16** and **32x32** effective analog tiles.
- Represent each MVM by a row/column conductance matrix plus a deterministic line-resistance field.
- Compute an effective per-cell attenuation map from source line to sink line and apply it before ADC quantization.

## Parameterization
Because the manuscript explicitly states that measured organic-array sheet resistance is not yet available, use a **drop-targeted parameterization** rather than claim exact physical ohms:
- target worst-case line-drop envelopes: `1%`, `3%`, `5%`, `10%`, `15%`;
- fit the internal line-resistance scalar to reproduce those envelopes under a representative conductance load.

## Integration path
- Reuse the existing fresh-instance evaluation harness.
- Insert a deterministic `apply_ir_drop_map()` stage between analog MVM output and digital rescaling.
- Keep D2D and C2C active so the experiment measures interaction rather than a clean-room IR-only effect.

## Compute plan
- Screening pass: one checkpoint, one dataset, `5 fresh arrays × 3 MC`.
- Full pass only if a reviewer explicitly asks or the screening result shows a non-negligible interaction.

## Output
- one contour or line plot: accuracy vs effective IR-drop envelope;
- one rebuttal-ready statement that current first-order conclusions are robust only up to mild IR-drop, and stronger spatial drops require this circuit-aware layer.
