from hydralogc.lexer import tokenize

def test_tokenize_module():
    code = "module MyMod {\ninput signal a;\n}"
    tokens = tokenize(code)
    assert tokens[0][0] == 'MODULE'
    assert any(tok[0] == 'PORT' for tok in tokens)