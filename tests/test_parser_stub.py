from hydralogc.parser import parse
from hydralogc.ast.nodes import ProgramNode, ModuleNode


def test_parser_returns_program_node():
    source_code = """
    module ExampleModule {
        input analog sig_in;
    }
    """
    ast = parse(source_code)
    assert isinstance(ast, ProgramNode)
    assert len(ast.children) > 0
    assert isinstance(ast.children[0], ModuleNode)
    assert ast.children[0].name == "ExampleModule"
