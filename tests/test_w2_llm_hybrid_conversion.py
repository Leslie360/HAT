import sys

import pytest

sys.path.insert(0, ".")

from paper2.src.llm_hybrid import (
    classify_pythia_linear,
    convert_pythia_to_hybrid,
    discover_pythia_linear_modules,
)


def test_classify_pythia_linear_names():
    assert classify_pythia_linear("gpt_neox.layers.0.attention.query_key_value") == "qkv"
    assert classify_pythia_linear("gpt_neox.layers.0.attention.dense") == "attention_output"
    assert classify_pythia_linear("gpt_neox.layers.0.mlp.dense_h_to_4h") == "mlp"
    assert classify_pythia_linear("gpt_neox.embed_out") == "digital"


def test_discover_pythia_linear_modules_skips_lm_head():
    torch = pytest.importorskip("torch")

    class TinyPythiaLike(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.gpt_neox = torch.nn.Module()
            self.gpt_neox.layers = torch.nn.ModuleList([torch.nn.Module()])
            layer = self.gpt_neox.layers[0]
            layer.attention = torch.nn.Module()
            layer.attention.query_key_value = torch.nn.Linear(4, 12)
            layer.attention.dense = torch.nn.Linear(4, 4)
            layer.mlp = torch.nn.Module()
            layer.mlp.dense_h_to_4h = torch.nn.Linear(4, 16)
            layer.mlp.dense_4h_to_h = torch.nn.Linear(16, 4)
            self.embed_out = torch.nn.Linear(4, 10)

    summary = discover_pythia_linear_modules(TinyPythiaLike())
    assert summary.qkv == ("gpt_neox.layers.0.attention.query_key_value",)
    assert summary.attention_output == ("gpt_neox.layers.0.attention.dense",)
    assert set(summary.mlp) == {
        "gpt_neox.layers.0.mlp.dense_h_to_4h",
        "gpt_neox.layers.0.mlp.dense_4h_to_h",
    }
    assert "embed_out" in summary.skipped


def test_convert_pythia_to_hybrid_skips_lm_head():
    torch = pytest.importorskip("torch")
    from analog_layers import AnalogLinear

    class TinyPythiaLike(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.gpt_neox = torch.nn.Module()
            self.gpt_neox.layers = torch.nn.ModuleList([torch.nn.Module()])
            layer = self.gpt_neox.layers[0]
            layer.attention = torch.nn.Module()
            layer.attention.query_key_value = torch.nn.Linear(4, 12)
            layer.attention.dense = torch.nn.Linear(4, 4)
            layer.mlp = torch.nn.Module()
            layer.mlp.dense_h_to_4h = torch.nn.Linear(4, 16)
            layer.mlp.dense_4h_to_h = torch.nn.Linear(16, 4)
            self.embed_out = torch.nn.Linear(4, 10)

    model, summary = convert_pythia_to_hybrid(TinyPythiaLike())
    converted = {name for name, module in model.named_modules() if isinstance(module, AnalogLinear)}
    assert converted == set(summary.analog_names)
    assert not isinstance(model.embed_out, AnalogLinear)


def test_convert_pythia_to_hybrid_can_scope_to_mlp_only():
    torch = pytest.importorskip("torch")
    from analog_layers import AnalogLinear

    class TinyPythiaLike(torch.nn.Module):
        def __init__(self):
            super().__init__()
            self.gpt_neox = torch.nn.Module()
            self.gpt_neox.layers = torch.nn.ModuleList([torch.nn.Module()])
            layer = self.gpt_neox.layers[0]
            layer.attention = torch.nn.Module()
            layer.attention.query_key_value = torch.nn.Linear(4, 12)
            layer.attention.dense = torch.nn.Linear(4, 4)
            layer.mlp = torch.nn.Module()
            layer.mlp.dense_h_to_4h = torch.nn.Linear(4, 16)
            layer.mlp.dense_4h_to_h = torch.nn.Linear(16, 4)
            self.embed_out = torch.nn.Linear(4, 10)

    model, _ = convert_pythia_to_hybrid(
        TinyPythiaLike(),
        include_qkv=False,
        include_attention_output=False,
        include_mlp=True,
    )
    converted = {name for name, module in model.named_modules() if isinstance(module, AnalogLinear)}
    assert converted == {
        "gpt_neox.layers.0.mlp.dense_h_to_4h",
        "gpt_neox.layers.0.mlp.dense_4h_to_h",
    }
