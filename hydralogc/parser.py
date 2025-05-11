from hydralogc.ast.nodes import ProgramNode, ModuleNode, PortNode, ParameterNode, ComponentNode, ConnectionNode, TaskNode, StatementNode


def parse(_source_code):
    # TEMP: This is a stub parser. Replace with full grammar later.
    # This example creates a dummy AST for testing the pipeline.
    dummy_port = PortNode(name="sig_in", type_="analog", line=1, column=1)
    dummy_param = ParameterNode(name="gain", default=1.0, line=2, column=1)
    dummy_component = ComponentNode(
        type_="Amplifier", name="amp1", parameters={}, line=3, column=1)
    dummy_connection = ConnectionNode(
        from_="sig_in", to="amp1.in", line=4, column=1)
    dummy_task = TaskNode(name="process_data", statements=[StatementNode(
        text="output = input;", line=5, column=1)], line=5, column=1)
    dummy_module = ModuleNode(name="ExampleModule", ports=[dummy_port], parameters=[
                              dummy_param], components=[dummy_component], tasks=[dummy_task])
    return ProgramNode(modules=[dummy_module])
