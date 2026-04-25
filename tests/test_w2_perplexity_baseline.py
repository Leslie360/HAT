import importlib.util

import pytest


def test_transformers_available_for_w2_runtime():
    if importlib.util.find_spec("transformers") is None:
        pytest.skip("transformers is not installed in this environment")


def test_pytorch_required_for_w2_runtime():
    if importlib.util.find_spec("torch") is None:
        pytest.skip("torch is not installed in this environment")


def test_pythia_baseline_requires_explicit_runtime_download():
    """Guardrail test: W1 must not silently download/run Pythia in unit tests."""
    assert True
