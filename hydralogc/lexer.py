def tokenize(source_code):
    tokens = []
    for line in source_code.splitlines():
        line = line.strip()
        if line.startswith('module'):
            tokens.append(('MODULE', line))
        elif 'input' in line or 'output' in line:
            tokens.append(('PORT', line))
        elif line.startswith('parameter'):
            tokens.append(('PARAM', line))
        elif line.startswith('configure'):
            tokens.append(('CONFIGURE', line))
        elif 'connect' in line:
            tokens.append(('CONNECT', line))
        else:
            tokens.append(('UNKNOWN', line))
    return tokens