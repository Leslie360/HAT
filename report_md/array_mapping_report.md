## Table 2: Tiny-ViT-5M Layer Mapping and Crossbar Array Requirements

| Layer | Type | Dimensions (M×N) | Params | Domain | Arrays (diff pair) |
|:------|:-----|:-----------------:|-------:|:------:|-------------------:|
| patch_embed.conv1.conv | Conv2d(k=(3, 3),s=(2, 2)) | 32×27 | 864 | analog | 2 |
| patch_embed.conv2.conv | Conv2d(k=(3, 3),s=(2, 2)) | 64×288 | 18,432 | analog | 6 |
| **Patch Embedding subtotal** | | | **19,296** | | **8** |
| stages.0.blocks.0.conv1.conv | Conv2d(k=(1, 1),s=(1, 1)) | 256×64 | 16,384 | digital | — |
| stages.0.blocks.0.conv2.conv | DWConv2d(g=256,k=(3, 3)) | 256×9 | 2,304 | digital | — |
| stages.0.blocks.0.conv3.conv | Conv2d(k=(1, 1),s=(1, 1)) | 64×256 | 16,384 | digital | — |
| stages.0.blocks.1.conv1.conv | Conv2d(k=(1, 1),s=(1, 1)) | 256×64 | 16,384 | digital | — |
| stages.0.blocks.1.conv2.conv | DWConv2d(g=256,k=(3, 3)) | 256×9 | 2,304 | digital | — |
| stages.0.blocks.1.conv3.conv | Conv2d(k=(1, 1),s=(1, 1)) | 64×256 | 16,384 | digital | — |
| **Stage 0 (MBConv) subtotal** | | | **70,144** | | **—** |
| stages.1.downsample.conv1.conv | Conv2d(k=(1, 1),s=(1, 1)) | 128×64 | 8,192 | digital | — |
| stages.1.downsample.conv2.conv | DWConv2d(g=128,k=(3, 3)) | 128×9 | 1,152 | digital | — |
| stages.1.downsample.conv3.conv | Conv2d(k=(1, 1),s=(1, 1)) | 128×128 | 16,384 | digital | — |
| **Stage 1 Downsample subtotal** | | | **25,728** | | **—** |
| stages.1.blocks.0.attn.qkv | Linear | 384×128 | 49,536 | analog | 6 |
| stages.1.blocks.0.attn.proj | Linear | 128×128 | 16,512 | analog | 2 |
| stages.1.blocks.0.mlp.fc1 | Linear | 512×128 | 66,048 | analog | 8 |
| stages.1.blocks.0.mlp.fc2 | Linear | 128×512 | 65,664 | analog | 8 |
| stages.1.blocks.0.local_conv.conv | DWConv2d(g=128,k=(3, 3)) | 128×9 | 1,152 | digital | — |
| stages.1.blocks.1.attn.qkv | Linear | 384×128 | 49,536 | analog | 6 |
| stages.1.blocks.1.attn.proj | Linear | 128×128 | 16,512 | analog | 2 |
| stages.1.blocks.1.mlp.fc1 | Linear | 512×128 | 66,048 | analog | 8 |
| stages.1.blocks.1.mlp.fc2 | Linear | 128×512 | 65,664 | analog | 8 |
| stages.1.blocks.1.local_conv.conv | DWConv2d(g=128,k=(3, 3)) | 128×9 | 1,152 | digital | — |
| **Stage 1 (Attention) subtotal** | | | **397,824** | | **48** |
| stages.2.downsample.conv1.conv | Conv2d(k=(1, 1),s=(1, 1)) | 160×128 | 20,480 | digital | — |
| stages.2.downsample.conv2.conv | DWConv2d(g=160,k=(3, 3)) | 160×9 | 1,440 | digital | — |
| stages.2.downsample.conv3.conv | Conv2d(k=(1, 1),s=(1, 1)) | 160×160 | 25,600 | digital | — |
| **Stage 2 Downsample subtotal** | | | **47,520** | | **—** |
| stages.2.blocks.0.attn.qkv | Linear | 480×160 | 77,280 | analog | 16 |
| stages.2.blocks.0.attn.proj | Linear | 160×160 | 25,760 | analog | 8 |
| stages.2.blocks.0.mlp.fc1 | Linear | 640×160 | 103,040 | analog | 20 |
| stages.2.blocks.0.mlp.fc2 | Linear | 160×640 | 102,560 | analog | 20 |
| stages.2.blocks.0.local_conv.conv | DWConv2d(g=160,k=(3, 3)) | 160×9 | 1,440 | digital | — |
| stages.2.blocks.1.attn.qkv | Linear | 480×160 | 77,280 | analog | 16 |
| stages.2.blocks.1.attn.proj | Linear | 160×160 | 25,760 | analog | 8 |
| stages.2.blocks.1.mlp.fc1 | Linear | 640×160 | 103,040 | analog | 20 |
| stages.2.blocks.1.mlp.fc2 | Linear | 160×640 | 102,560 | analog | 20 |
| stages.2.blocks.1.local_conv.conv | DWConv2d(g=160,k=(3, 3)) | 160×9 | 1,440 | digital | — |
| stages.2.blocks.2.attn.qkv | Linear | 480×160 | 77,280 | analog | 16 |
| stages.2.blocks.2.attn.proj | Linear | 160×160 | 25,760 | analog | 8 |
| stages.2.blocks.2.mlp.fc1 | Linear | 640×160 | 103,040 | analog | 20 |
| stages.2.blocks.2.mlp.fc2 | Linear | 160×640 | 102,560 | analog | 20 |
| stages.2.blocks.2.local_conv.conv | DWConv2d(g=160,k=(3, 3)) | 160×9 | 1,440 | digital | — |
| stages.2.blocks.3.attn.qkv | Linear | 480×160 | 77,280 | analog | 16 |
| stages.2.blocks.3.attn.proj | Linear | 160×160 | 25,760 | analog | 8 |
| stages.2.blocks.3.mlp.fc1 | Linear | 640×160 | 103,040 | analog | 20 |
| stages.2.blocks.3.mlp.fc2 | Linear | 160×640 | 102,560 | analog | 20 |
| stages.2.blocks.3.local_conv.conv | DWConv2d(g=160,k=(3, 3)) | 160×9 | 1,440 | digital | — |
| stages.2.blocks.4.attn.qkv | Linear | 480×160 | 77,280 | analog | 16 |
| stages.2.blocks.4.attn.proj | Linear | 160×160 | 25,760 | analog | 8 |
| stages.2.blocks.4.mlp.fc1 | Linear | 640×160 | 103,040 | analog | 20 |
| stages.2.blocks.4.mlp.fc2 | Linear | 160×640 | 102,560 | analog | 20 |
| stages.2.blocks.4.local_conv.conv | DWConv2d(g=160,k=(3, 3)) | 160×9 | 1,440 | digital | — |
| stages.2.blocks.5.attn.qkv | Linear | 480×160 | 77,280 | analog | 16 |
| stages.2.blocks.5.attn.proj | Linear | 160×160 | 25,760 | analog | 8 |
| stages.2.blocks.5.mlp.fc1 | Linear | 640×160 | 103,040 | analog | 20 |
| stages.2.blocks.5.mlp.fc2 | Linear | 160×640 | 102,560 | analog | 20 |
| stages.2.blocks.5.local_conv.conv | DWConv2d(g=160,k=(3, 3)) | 160×9 | 1,440 | digital | — |
| **Stage 2 (Attention) subtotal** | | | **1,860,480** | | **384** |
| stages.3.downsample.conv1.conv | Conv2d(k=(1, 1),s=(1, 1)) | 320×160 | 51,200 | digital | — |
| stages.3.downsample.conv2.conv | DWConv2d(g=320,k=(3, 3)) | 320×9 | 2,880 | digital | — |
| stages.3.downsample.conv3.conv | Conv2d(k=(1, 1),s=(1, 1)) | 320×320 | 102,400 | digital | — |
| **Stage 3 Downsample subtotal** | | | **156,480** | | **—** |
| stages.3.blocks.0.attn.qkv | Linear | 960×320 | 308,160 | analog | 48 |
| stages.3.blocks.0.attn.proj | Linear | 320×320 | 102,720 | analog | 18 |
| stages.3.blocks.0.mlp.fc1 | Linear | 1280×320 | 410,880 | analog | 60 |
| stages.3.blocks.0.mlp.fc2 | Linear | 320×1280 | 409,920 | analog | 60 |
| stages.3.blocks.0.local_conv.conv | DWConv2d(g=320,k=(3, 3)) | 320×9 | 2,880 | digital | — |
| stages.3.blocks.1.attn.qkv | Linear | 960×320 | 308,160 | analog | 48 |
| stages.3.blocks.1.attn.proj | Linear | 320×320 | 102,720 | analog | 18 |
| stages.3.blocks.1.mlp.fc1 | Linear | 1280×320 | 410,880 | analog | 60 |
| stages.3.blocks.1.mlp.fc2 | Linear | 320×1280 | 409,920 | analog | 60 |
| stages.3.blocks.1.local_conv.conv | DWConv2d(g=320,k=(3, 3)) | 320×9 | 2,880 | digital | — |
| **Stage 3 (Attention) subtotal** | | | **2,469,120** | | **372** |
| head.fc | Linear | 1000×320 | 321,000 | digital | — |
| **Classification Head subtotal** | | | **321,000** | | **—** |
| Other parameters (attn biases, etc.) | — | — | 25,172 | digital | — |

**Total parameters:** 5,392,764  
**Analog-mapped:** 4,730,016 (87.7%)  
**Digital:** 662,748 (12.3%)  
**Total 128×128 crossbar arrays (differential pair):** 812  
**Total devices:** 13,303,808  