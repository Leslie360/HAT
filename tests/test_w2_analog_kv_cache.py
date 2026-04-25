import sys

import pytest

torch = pytest.importorskip("torch")

sys.path.insert(0, ".")

from paper2.src.analog_kv_cache import AnalogKVCache, AnalogKVCacheConfig


def test_d2d_is_persistent_when_c2c_disabled():
    torch.manual_seed(7)
    cache = AnalogKVCache(
        layer_idx=0,
        num_heads=2,
        head_dim=4,
        max_seq_len=3,
        config=AnalogKVCacheConfig(quantize=False, sigma_d2d=0.10, sigma_c2c=0.0),
    )
    k = torch.ones(1, 2, 4)
    v = torch.full((1, 2, 4), 2.0)
    cache.write(0, k, v)

    k1, v1 = cache.read()
    k2, v2 = cache.read()

    assert torch.allclose(k1, k2)
    assert torch.allclose(v1, v2)
    assert not torch.allclose(k1, k.unsqueeze(2))


def test_c2c_is_fresh_across_reads():
    torch.manual_seed(11)
    cache = AnalogKVCache(
        layer_idx=0,
        num_heads=2,
        head_dim=4,
        max_seq_len=3,
        config=AnalogKVCacheConfig(quantize=False, sigma_d2d=0.0, sigma_c2c=0.20),
    )
    token = torch.ones(1, 2, 4)
    cache.write(0, token, token)

    k1, _ = cache.read()
    k2, _ = cache.read()

    assert not torch.allclose(k1, k2)


def test_read_prefix_and_token_shapes():
    cache = AnalogKVCache(
        layer_idx=1,
        num_heads=2,
        head_dim=3,
        max_seq_len=5,
        config=AnalogKVCacheConfig(quantize=False, noise_enabled=False),
    )
    for idx in range(3):
        token = torch.full((1, 2, 1, 3), float(idx + 1))
        cache.write(idx, token, token + 10)

    k, v = cache.read(end_pos=2)
    assert k.shape == (1, 2, 2, 3)
    assert v.shape == (1, 2, 2, 3)
    assert torch.all(k[:, :, 0, :] == 1)
    assert torch.all(k[:, :, 1, :] == 2)
    assert int(cache.valid_length.item()) == 3


def test_quantizer_respects_bit_width_level_bound():
    cache = AnalogKVCache(
        layer_idx=0,
        num_heads=1,
        head_dim=8,
        max_seq_len=1,
        config=AnalogKVCacheConfig(bit_width=2, quantize=True, noise_enabled=False),
    )
    token = torch.linspace(-1.0, 1.0, steps=8).reshape(1, 1, 8)
    cache.write(0, token, token)
    k, _ = cache.read()

    # Signed 2-bit path uses {-1, 0, +1} after symmetric scaling.
    assert torch.unique(k).numel() <= 3
