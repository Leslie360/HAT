# Tiny-ViT Retention Diagnostic (GPT)

- Generated: `2026-04-05T14:27:03`
- Device: `cuda`
- Eval runs: `10`
- Time point: `1s`

## Condition Summary

| Condition | Recalibrate Scale | D2D Decays | Accuracy |
|:----------|:------------------|:-----------|:---------|
| current | False | False | 10.50 +/- 0.23% |
| recalibrate_scale | True | False | 54.54 +/- 0.54% |
| recalibrate_scale_and_decay_d2d | True | True | 82.61 +/- 0.60% |

## Representative Layers

### current

| Layer | Decay | Original Scale | Recal Scale | Effective Scale | retained |D| max | D2D std(G) |
|:------|------:|---------------:|------------:|----------------:|----------------:|-----------:|
| patch_embed.conv1.conv | 0.6390 | 0.078133 | 0.122277 | 0.078133 | 5.750816 | 0.882724 |
| stages.1.blocks.0.attn.qkv | 0.6390 | 0.099828 | 0.156230 | 0.099828 | 5.750816 | 0.904621 |
| stages.3.blocks.1.mlp.fc2 | 0.6390 | 0.173856 | 0.272083 | 0.173856 | 5.750816 | 0.898736 |

### recalibrate_scale

| Layer | Decay | Original Scale | Recal Scale | Effective Scale | retained |D| max | D2D std(G) |
|:------|------:|---------------:|------------:|----------------:|----------------:|-----------:|
| patch_embed.conv1.conv | 0.6390 | 0.078133 | 0.122277 | 0.122277 | 5.750816 | 0.882724 |
| stages.1.blocks.0.attn.qkv | 0.6390 | 0.099828 | 0.156230 | 0.156230 | 5.750816 | 0.904621 |
| stages.3.blocks.1.mlp.fc2 | 0.6390 | 0.173856 | 0.272083 | 0.272083 | 5.750816 | 0.898736 |

### recalibrate_scale_and_decay_d2d

| Layer | Decay | Original Scale | Recal Scale | Effective Scale | retained |D| max | D2D std(G) |
|:------|------:|---------------:|------------:|----------------:|----------------:|-----------:|
| patch_embed.conv1.conv | 0.6390 | 0.078133 | 0.122277 | 0.122277 | 5.750816 | 0.564042 |
| stages.1.blocks.0.attn.qkv | 0.6390 | 0.099828 | 0.156230 | 0.156230 | 5.750816 | 0.578034 |
| stages.3.blocks.1.mlp.fc2 | 0.6390 | 0.173856 | 0.272083 | 0.272083 | 5.750816 | 0.574274 |
