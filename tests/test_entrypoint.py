import importlib


def test_main_entrypoint_exists():
    module = importlib.import_module("main")
    assert callable(module.main)
