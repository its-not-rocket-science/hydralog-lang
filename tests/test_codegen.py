from hydralogc.ir.analog_ir import AnalogIR
from hydralogc.codegen.spice_backend import generate_spice_netlist

def test_spice_output():
    ir = AnalogIR()
    ir.add_component("filter", "LPF", {"fc": 1234})
    ir.connect("a", "LPF.in")
    ir.connect("LPF.out", "b")
    output = generate_spice_netlist(ir)
    assert ".title" in output
    assert "LPF" in output