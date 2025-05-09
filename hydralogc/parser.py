def parse(code):
    lines = code.strip().splitlines()
    return {"type": "Module", "lines": len(lines), "content": lines}