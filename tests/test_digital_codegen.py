from hydralogc.ir.digital_ir import DigitalIR
from hydralogc.codegen.digital_codegen import generate_digital_c_code

def test_generate_digital_c_code_output():
    ir = DigitalIR()
    ir.add_input("sensor_value")
    ir.add_output("temperature")
    ir.add_task("log_temp", ["temperature = sensor_value;"])

    code = generate_digital_c_code(ir)
    assert "int main()" in code
    assert "temperature = sensor_value;" in code
