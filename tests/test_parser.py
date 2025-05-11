from hydralogc.parser import parse
from hydralogc.ast.nodes import ProgramNode, ModuleNode


def test_parse_returns_ast():
    code = "module M {\ninput signal a;\n}"
    result = parse(code)
    assert isinstance(result, ProgramNode)
    assert len(result.children) > 0
    assert isinstance(result.children[0], ModuleNode)
    assert result.children[0].name == "ExampleModule"
