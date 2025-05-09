import sys
import builtins
import io
from hydralogc.hydralogc import main

def test_cli_compile(monkeypatch):
    # Fake file input
    monkeypatch.setattr(builtins, "open", lambda f, *a, **k: io.StringIO("dummy code"))

    # Replace AnalogIR with mock that has expected structure
    class DummyIR:
        def __init__(self):
            self.components = [("filter", "LPF", {"fc": 1000})]
            self.connections = [("in", "LPF.in"), ("LPF.out", "out")]

        def add_component(self, *a, **k): pass
        def connect(self, *a): pass

    monkeypatch.setattr("hydralogc.hydralogc.AnalogIR", DummyIR)

    # Simulate CLI arguments
    test_args = ["hydralogc", "compile", "examples/test.hyd"]
    monkeypatch.setattr(sys, "argv", test_args)

    result = main()
    assert result is not None
