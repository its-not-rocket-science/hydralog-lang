from hydralogc.parser import parse

def test_parse_lines():
    code = "module M {\ninput signal a;\n}"
    result = parse(code)
    assert result['type'] == 'Module'
    assert result['lines'] == 3