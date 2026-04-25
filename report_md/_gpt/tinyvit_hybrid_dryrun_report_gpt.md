# Tiny-ViT Hybrid Dry-Run Report (GPT)

- Model: `tiny_vit_5m_224`
- Dataset target: `cifar10`
- Reference experiment for dry-run: `V4` / `V4_hybrid_standard_noise_hat`
- Scope: static dry-run only, no training launched

## Summary

- Analog layers tracked: 42
- Digital layers tracked: 57
- Total 128×128 crossbar arrays (diff pair): 812
- Total crossbar devices: 13,303,808
- Estimated hybrid energy: 273.9383 µJ / inference
- Estimated FP32 GPU energy: 3137.1448 µJ / inference
- Estimated energy reduction ratio: 11.45×

## Layer Allocation

| Layer | Kind | Domain | Input | Output | Arrays | Energy Config |
|:------|:-----|:------:|:------|:-------|-------:|:--------------|
| patch_embed.conv1.conv | conv2d | analog | `(1, 3, 224, 224)` | `(1, 32, 112, 112)` | 2 | analog MACs=10838016, ADC=401408, DAC=338688 |
| patch_embed.conv2.conv | conv2d | analog | `(1, 32, 112, 112)` | `(1, 64, 56, 56)` | 6 | analog MACs=57802752, ADC=200704, DAC=903168 |
| stages.0.blocks.0.conv1.conv | conv2d | digital | `(1, 64, 56, 56)` | `(1, 256, 56, 56)` | 0 | digital MACs=51380224 |
| stages.0.blocks.0.conv2.conv | conv2d | digital | `(1, 256, 56, 56)` | `(1, 256, 56, 56)` | 0 | digital MACs=7225344 |
| stages.0.blocks.0.conv3.conv | conv2d | digital | `(1, 256, 56, 56)` | `(1, 64, 56, 56)` | 0 | digital MACs=51380224 |
| stages.0.blocks.1.conv1.conv | conv2d | digital | `(1, 64, 56, 56)` | `(1, 256, 56, 56)` | 0 | digital MACs=51380224 |
| stages.0.blocks.1.conv2.conv | conv2d | digital | `(1, 256, 56, 56)` | `(1, 256, 56, 56)` | 0 | digital MACs=7225344 |
| stages.0.blocks.1.conv3.conv | conv2d | digital | `(1, 256, 56, 56)` | `(1, 64, 56, 56)` | 0 | digital MACs=51380224 |
| stages.1.downsample.conv1.conv | conv2d | digital | `(1, 64, 56, 56)` | `(1, 128, 56, 56)` | 0 | digital MACs=25690112 |
| stages.1.downsample.conv2.conv | conv2d | digital | `(1, 128, 56, 56)` | `(1, 128, 28, 28)` | 0 | digital MACs=903168 |
| stages.1.downsample.conv3.conv | conv2d | digital | `(1, 128, 28, 28)` | `(1, 128, 28, 28)` | 0 | digital MACs=12845056 |
| stages.1.blocks.0.attn | attention_special | digital | `(16, 49, 128)` | `(16, 49, 128)` | 0 | QK digital MACs=4917248, AV digital MACs=4917248, softmax elements=153664 |
| stages.1.blocks.0.attn.norm | layernorm | digital | `(16, 49, 128)` | `(16, 49, 128)` | 0 | layernorm elements=100352 |
| stages.1.blocks.0.attn.qkv | linear | analog | `(16, 49, 128)` | `(16, 49, 384)` | 6 | analog MACs=38535168, ADC=301056, DAC=100352 |
| stages.1.blocks.0.attn.proj | linear | analog | `(16, 49, 128)` | `(16, 49, 128)` | 2 | analog MACs=12845056, ADC=100352, DAC=100352 |
| stages.1.blocks.0.mlp.norm | layernorm | digital | `(1, 784, 128)` | `(1, 784, 128)` | 0 | layernorm elements=100352 |
| stages.1.blocks.0.mlp.fc1 | linear | analog | `(1, 784, 128)` | `(1, 784, 512)` | 8 | analog MACs=51380224, ADC=401408, DAC=100352 |
| stages.1.blocks.0.mlp.fc2 | linear | analog | `(1, 784, 512)` | `(1, 784, 128)` | 8 | analog MACs=51380224, ADC=100352, DAC=401408 |
| stages.1.blocks.0.local_conv.conv | conv2d | digital | `(1, 128, 28, 28)` | `(1, 128, 28, 28)` | 0 | digital MACs=903168 |
| stages.1.blocks.1.attn | attention_special | digital | `(16, 49, 128)` | `(16, 49, 128)` | 0 | QK digital MACs=4917248, AV digital MACs=4917248, softmax elements=153664 |
| stages.1.blocks.1.attn.norm | layernorm | digital | `(16, 49, 128)` | `(16, 49, 128)` | 0 | layernorm elements=100352 |
| stages.1.blocks.1.attn.qkv | linear | analog | `(16, 49, 128)` | `(16, 49, 384)` | 6 | analog MACs=38535168, ADC=301056, DAC=100352 |
| stages.1.blocks.1.attn.proj | linear | analog | `(16, 49, 128)` | `(16, 49, 128)` | 2 | analog MACs=12845056, ADC=100352, DAC=100352 |
| stages.1.blocks.1.mlp.norm | layernorm | digital | `(1, 784, 128)` | `(1, 784, 128)` | 0 | layernorm elements=100352 |
| stages.1.blocks.1.mlp.fc1 | linear | analog | `(1, 784, 128)` | `(1, 784, 512)` | 8 | analog MACs=51380224, ADC=401408, DAC=100352 |
| stages.1.blocks.1.mlp.fc2 | linear | analog | `(1, 784, 512)` | `(1, 784, 128)` | 8 | analog MACs=51380224, ADC=100352, DAC=401408 |
| stages.1.blocks.1.local_conv.conv | conv2d | digital | `(1, 128, 28, 28)` | `(1, 128, 28, 28)` | 0 | digital MACs=903168 |
| stages.2.downsample.conv1.conv | conv2d | digital | `(1, 128, 28, 28)` | `(1, 160, 28, 28)` | 0 | digital MACs=16056320 |
| stages.2.downsample.conv2.conv | conv2d | digital | `(1, 160, 28, 28)` | `(1, 160, 14, 14)` | 0 | digital MACs=282240 |
| stages.2.downsample.conv3.conv | conv2d | digital | `(1, 160, 14, 14)` | `(1, 160, 14, 14)` | 0 | digital MACs=5017600 |
| stages.2.blocks.0.attn | attention_special | digital | `(1, 196, 160)` | `(1, 196, 160)` | 0 | QK digital MACs=6146560, AV digital MACs=6146560, softmax elements=192080 |
| stages.2.blocks.0.attn.norm | layernorm | digital | `(1, 196, 160)` | `(1, 196, 160)` | 0 | layernorm elements=31360 |
| stages.2.blocks.0.attn.qkv | linear | analog | `(1, 196, 160)` | `(1, 196, 480)` | 16 | analog MACs=15052800, ADC=94080, DAC=31360 |
| stages.2.blocks.0.attn.proj | linear | analog | `(1, 196, 160)` | `(1, 196, 160)` | 8 | analog MACs=5017600, ADC=31360, DAC=31360 |
| stages.2.blocks.0.mlp.norm | layernorm | digital | `(1, 196, 160)` | `(1, 196, 160)` | 0 | layernorm elements=31360 |
| stages.2.blocks.0.mlp.fc1 | linear | analog | `(1, 196, 160)` | `(1, 196, 640)` | 20 | analog MACs=20070400, ADC=125440, DAC=31360 |
| stages.2.blocks.0.mlp.fc2 | linear | analog | `(1, 196, 640)` | `(1, 196, 160)` | 20 | analog MACs=20070400, ADC=31360, DAC=125440 |
| stages.2.blocks.0.local_conv.conv | conv2d | digital | `(1, 160, 14, 14)` | `(1, 160, 14, 14)` | 0 | digital MACs=282240 |
| stages.2.blocks.1.attn | attention_special | digital | `(1, 196, 160)` | `(1, 196, 160)` | 0 | QK digital MACs=6146560, AV digital MACs=6146560, softmax elements=192080 |
| stages.2.blocks.1.attn.norm | layernorm | digital | `(1, 196, 160)` | `(1, 196, 160)` | 0 | layernorm elements=31360 |
| stages.2.blocks.1.attn.qkv | linear | analog | `(1, 196, 160)` | `(1, 196, 480)` | 16 | analog MACs=15052800, ADC=94080, DAC=31360 |
| stages.2.blocks.1.attn.proj | linear | analog | `(1, 196, 160)` | `(1, 196, 160)` | 8 | analog MACs=5017600, ADC=31360, DAC=31360 |
| stages.2.blocks.1.mlp.norm | layernorm | digital | `(1, 196, 160)` | `(1, 196, 160)` | 0 | layernorm elements=31360 |
| stages.2.blocks.1.mlp.fc1 | linear | analog | `(1, 196, 160)` | `(1, 196, 640)` | 20 | analog MACs=20070400, ADC=125440, DAC=31360 |
| stages.2.blocks.1.mlp.fc2 | linear | analog | `(1, 196, 640)` | `(1, 196, 160)` | 20 | analog MACs=20070400, ADC=31360, DAC=125440 |
| stages.2.blocks.1.local_conv.conv | conv2d | digital | `(1, 160, 14, 14)` | `(1, 160, 14, 14)` | 0 | digital MACs=282240 |
| stages.2.blocks.2.attn | attention_special | digital | `(1, 196, 160)` | `(1, 196, 160)` | 0 | QK digital MACs=6146560, AV digital MACs=6146560, softmax elements=192080 |
| stages.2.blocks.2.attn.norm | layernorm | digital | `(1, 196, 160)` | `(1, 196, 160)` | 0 | layernorm elements=31360 |
| stages.2.blocks.2.attn.qkv | linear | analog | `(1, 196, 160)` | `(1, 196, 480)` | 16 | analog MACs=15052800, ADC=94080, DAC=31360 |
| stages.2.blocks.2.attn.proj | linear | analog | `(1, 196, 160)` | `(1, 196, 160)` | 8 | analog MACs=5017600, ADC=31360, DAC=31360 |
| stages.2.blocks.2.mlp.norm | layernorm | digital | `(1, 196, 160)` | `(1, 196, 160)` | 0 | layernorm elements=31360 |
| stages.2.blocks.2.mlp.fc1 | linear | analog | `(1, 196, 160)` | `(1, 196, 640)` | 20 | analog MACs=20070400, ADC=125440, DAC=31360 |
| stages.2.blocks.2.mlp.fc2 | linear | analog | `(1, 196, 640)` | `(1, 196, 160)` | 20 | analog MACs=20070400, ADC=31360, DAC=125440 |
| stages.2.blocks.2.local_conv.conv | conv2d | digital | `(1, 160, 14, 14)` | `(1, 160, 14, 14)` | 0 | digital MACs=282240 |
| stages.2.blocks.3.attn | attention_special | digital | `(1, 196, 160)` | `(1, 196, 160)` | 0 | QK digital MACs=6146560, AV digital MACs=6146560, softmax elements=192080 |
| stages.2.blocks.3.attn.norm | layernorm | digital | `(1, 196, 160)` | `(1, 196, 160)` | 0 | layernorm elements=31360 |
| stages.2.blocks.3.attn.qkv | linear | analog | `(1, 196, 160)` | `(1, 196, 480)` | 16 | analog MACs=15052800, ADC=94080, DAC=31360 |
| stages.2.blocks.3.attn.proj | linear | analog | `(1, 196, 160)` | `(1, 196, 160)` | 8 | analog MACs=5017600, ADC=31360, DAC=31360 |
| stages.2.blocks.3.mlp.norm | layernorm | digital | `(1, 196, 160)` | `(1, 196, 160)` | 0 | layernorm elements=31360 |
| stages.2.blocks.3.mlp.fc1 | linear | analog | `(1, 196, 160)` | `(1, 196, 640)` | 20 | analog MACs=20070400, ADC=125440, DAC=31360 |
| stages.2.blocks.3.mlp.fc2 | linear | analog | `(1, 196, 640)` | `(1, 196, 160)` | 20 | analog MACs=20070400, ADC=31360, DAC=125440 |
| stages.2.blocks.3.local_conv.conv | conv2d | digital | `(1, 160, 14, 14)` | `(1, 160, 14, 14)` | 0 | digital MACs=282240 |
| stages.2.blocks.4.attn | attention_special | digital | `(1, 196, 160)` | `(1, 196, 160)` | 0 | QK digital MACs=6146560, AV digital MACs=6146560, softmax elements=192080 |
| stages.2.blocks.4.attn.norm | layernorm | digital | `(1, 196, 160)` | `(1, 196, 160)` | 0 | layernorm elements=31360 |
| stages.2.blocks.4.attn.qkv | linear | analog | `(1, 196, 160)` | `(1, 196, 480)` | 16 | analog MACs=15052800, ADC=94080, DAC=31360 |
| stages.2.blocks.4.attn.proj | linear | analog | `(1, 196, 160)` | `(1, 196, 160)` | 8 | analog MACs=5017600, ADC=31360, DAC=31360 |
| stages.2.blocks.4.mlp.norm | layernorm | digital | `(1, 196, 160)` | `(1, 196, 160)` | 0 | layernorm elements=31360 |
| stages.2.blocks.4.mlp.fc1 | linear | analog | `(1, 196, 160)` | `(1, 196, 640)` | 20 | analog MACs=20070400, ADC=125440, DAC=31360 |
| stages.2.blocks.4.mlp.fc2 | linear | analog | `(1, 196, 640)` | `(1, 196, 160)` | 20 | analog MACs=20070400, ADC=31360, DAC=125440 |
| stages.2.blocks.4.local_conv.conv | conv2d | digital | `(1, 160, 14, 14)` | `(1, 160, 14, 14)` | 0 | digital MACs=282240 |
| stages.2.blocks.5.attn | attention_special | digital | `(1, 196, 160)` | `(1, 196, 160)` | 0 | QK digital MACs=6146560, AV digital MACs=6146560, softmax elements=192080 |
| stages.2.blocks.5.attn.norm | layernorm | digital | `(1, 196, 160)` | `(1, 196, 160)` | 0 | layernorm elements=31360 |
| stages.2.blocks.5.attn.qkv | linear | analog | `(1, 196, 160)` | `(1, 196, 480)` | 16 | analog MACs=15052800, ADC=94080, DAC=31360 |
| stages.2.blocks.5.attn.proj | linear | analog | `(1, 196, 160)` | `(1, 196, 160)` | 8 | analog MACs=5017600, ADC=31360, DAC=31360 |
| stages.2.blocks.5.mlp.norm | layernorm | digital | `(1, 196, 160)` | `(1, 196, 160)` | 0 | layernorm elements=31360 |
| stages.2.blocks.5.mlp.fc1 | linear | analog | `(1, 196, 160)` | `(1, 196, 640)` | 20 | analog MACs=20070400, ADC=125440, DAC=31360 |
| stages.2.blocks.5.mlp.fc2 | linear | analog | `(1, 196, 640)` | `(1, 196, 160)` | 20 | analog MACs=20070400, ADC=31360, DAC=125440 |
| stages.2.blocks.5.local_conv.conv | conv2d | digital | `(1, 160, 14, 14)` | `(1, 160, 14, 14)` | 0 | digital MACs=282240 |
| stages.3.downsample.conv1.conv | conv2d | digital | `(1, 160, 14, 14)` | `(1, 320, 14, 14)` | 0 | digital MACs=10035200 |
| stages.3.downsample.conv2.conv | conv2d | digital | `(1, 320, 14, 14)` | `(1, 320, 7, 7)` | 0 | digital MACs=141120 |
| stages.3.downsample.conv3.conv | conv2d | digital | `(1, 320, 7, 7)` | `(1, 320, 7, 7)` | 0 | digital MACs=5017600 |
| stages.3.blocks.0.attn | attention_special | digital | `(1, 49, 320)` | `(1, 49, 320)` | 0 | QK digital MACs=768320, AV digital MACs=768320, softmax elements=24010 |
| stages.3.blocks.0.attn.norm | layernorm | digital | `(1, 49, 320)` | `(1, 49, 320)` | 0 | layernorm elements=15680 |
| stages.3.blocks.0.attn.qkv | linear | analog | `(1, 49, 320)` | `(1, 49, 960)` | 48 | analog MACs=15052800, ADC=47040, DAC=15680 |
| stages.3.blocks.0.attn.proj | linear | analog | `(1, 49, 320)` | `(1, 49, 320)` | 18 | analog MACs=5017600, ADC=15680, DAC=15680 |
| stages.3.blocks.0.mlp.norm | layernorm | digital | `(1, 49, 320)` | `(1, 49, 320)` | 0 | layernorm elements=15680 |
| stages.3.blocks.0.mlp.fc1 | linear | analog | `(1, 49, 320)` | `(1, 49, 1280)` | 60 | analog MACs=20070400, ADC=62720, DAC=15680 |
| stages.3.blocks.0.mlp.fc2 | linear | analog | `(1, 49, 1280)` | `(1, 49, 320)` | 60 | analog MACs=20070400, ADC=15680, DAC=62720 |
| stages.3.blocks.0.local_conv.conv | conv2d | digital | `(1, 320, 7, 7)` | `(1, 320, 7, 7)` | 0 | digital MACs=141120 |
| stages.3.blocks.1.attn | attention_special | digital | `(1, 49, 320)` | `(1, 49, 320)` | 0 | QK digital MACs=768320, AV digital MACs=768320, softmax elements=24010 |
| stages.3.blocks.1.attn.norm | layernorm | digital | `(1, 49, 320)` | `(1, 49, 320)` | 0 | layernorm elements=15680 |
| stages.3.blocks.1.attn.qkv | linear | analog | `(1, 49, 320)` | `(1, 49, 960)` | 48 | analog MACs=15052800, ADC=47040, DAC=15680 |
| stages.3.blocks.1.attn.proj | linear | analog | `(1, 49, 320)` | `(1, 49, 320)` | 18 | analog MACs=5017600, ADC=15680, DAC=15680 |
| stages.3.blocks.1.mlp.norm | layernorm | digital | `(1, 49, 320)` | `(1, 49, 320)` | 0 | layernorm elements=15680 |
| stages.3.blocks.1.mlp.fc1 | linear | analog | `(1, 49, 320)` | `(1, 49, 1280)` | 60 | analog MACs=20070400, ADC=62720, DAC=15680 |
| stages.3.blocks.1.mlp.fc2 | linear | analog | `(1, 49, 1280)` | `(1, 49, 320)` | 60 | analog MACs=20070400, ADC=15680, DAC=62720 |
| stages.3.blocks.1.local_conv.conv | conv2d | digital | `(1, 320, 7, 7)` | `(1, 320, 7, 7)` | 0 | digital MACs=141120 |
| head.norm | layernorm | digital | `(1, 320, 1, 1)` | `(1, 320, 1, 1)` | 0 | layernorm elements=320 |
| head.fc | linear | digital | `(1, 320)` | `(1, 10)` | 0 | digital MACs=3200 |

## Energy Breakdown

- analog_MAC: 85.8612 µJ (31.3%)
- ADC: 0.1096 µJ (<0.1%)
- DAC: 0.1255 µJ (<0.1%)
- digital_MAC: 158.4985 µJ (57.9%)
- special_ops: 29.3436 µJ (10.7%)
- buffer: 0.0000 µJ (not separately modeled)

## Latency Estimate

- Estimated total latency: 403367.4040 µs / inference
| Component | Latency |
|:----------|--------:|
| analog_pipeline | 4772.6000 µs |
| digital_compute | 396246.2080 µs |
| special_ops | 2348.5960 µs |
| buffer | 0.0000 µs |

## Experiment Matrix V1-V7

| Exp | Hybrid | Noise | C2C | D2D | HAT | Physical FE | Retention |
|:---:|:------:|:-----:|:---:|:---:|:---:|:-----------:|:---------:|
| V1 | no | off | 0.0 | 0.0 | no | no | off |
| V2 | yes | off | 0.0 | 0.0 | no | no | off |
| V3 | yes | on | 0.05 | 0.1 | no | no | off |
| V4 | yes | on | 0.05 | 0.1 | yes | no | off |
| V5 | yes | on | 0.1 | 0.2 | yes | no | off |
| V6 | yes | on | 0.05 | 0.1 | yes | yes | off |
| V7 | yes | on | 0.05 | 0.1 | yes | no | 1000s |

## Notes / TODO

- Attention energy uses a hook-based estimate for QK^T, softmax, and A·V.
- Buffer/SRAM/DRAM terms are not yet separately itemized in this dry-run and should not be interpreted as physically zero.
- Physical front-end min-max normalization remains a Claude-review item.
