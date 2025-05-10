from hydralogc.ir.digital_ir import DigitalIR

def test_digital_ir_adds_io_and_tasks():
    ir = DigitalIR()
    ir.add_input("sensor_value")
    ir.add_output("temperature")
    ir.add_task("log_temp", ["temperature = sensor_value;"])

    assert "sensor_value" in ir.inputs
    assert "temperature" in ir.outputs
    assert "log_temp" in ir.tasks
