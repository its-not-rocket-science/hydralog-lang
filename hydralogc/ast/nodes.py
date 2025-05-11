from hydralogc.ast.base import ASTNode


class ProgramNode(ASTNode):
    def __init__(self, modules, line=0, column=0):
        super().__init__(line, column)
        self.children = modules


class ModuleNode(ASTNode):
    def __init__(self, name, ports, parameters, components, tasks, line=0, column=0):
        super().__init__(line, column)
        self.name = name
        self.children = ports + parameters + components + tasks


class PortNode(ASTNode):
    def __init__(self, name, type_, line=0, column=0):
        super().__init__(line, column)
        self.name = name
        self.type = type_


class ParameterNode(ASTNode):
    def __init__(self, name, default=None, line=0, column=0):
        super().__init__(line, column)
        self.name = name
        self.default = default


class ComponentNode(ASTNode):
    def __init__(self, type_, name, parameters, line=0, column=0):
        super().__init__(line, column)
        self.type = type_
        self.name = name
        self.parameters = parameters


class ConnectionNode(ASTNode):
    def __init__(self, from_, to, line=0, column=0):
        super().__init__(line, column)
        self.from_ = from_
        self.to = to


class TaskNode(ASTNode):
    def __init__(self, name, statements, line=0, column=0):
        super().__init__(line, column)
        self.name = name
        self.statements = statements


class StatementNode(ASTNode):
    def __init__(self, text, line=0, column=0):
        super().__init__(line, column)
        self.text = text


class ExpressionNode(ASTNode):
    def __init__(self, expression, line=0, column=0):
        super().__init__(line, column)
        self.expression = expression
