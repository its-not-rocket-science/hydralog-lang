class SymbolTable:
    def __init__(self):
        self.stack = [{}]

    def enter_scope(self):
        self.stack.append({})

    def exit_scope(self):
        self.stack.pop()

    def define(self, name, symbol_type, attributes):
        current = self.stack[-1]
        if name in current:
            return False
        current[name] = {"type": symbol_type, "attributes": attributes}
        return True

    def lookup(self, name):
        for scope in reversed(self.stack):
            if name in scope:
                return scope[name]
        return None
