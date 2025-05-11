class SemanticAnalyzerVisitor:
    def __init__(self, symbol_table, error_collector):
        self.symbol_table = symbol_table
        self.errors = error_collector

    def visit_ProgramNode(self, node):
        self.symbol_table.enter_scope()
        for child in node.children:
            child.accept(self)
        self.symbol_table.exit_scope()

    def visit_ModuleNode(self, node):
        if not self.symbol_table.define(node.name, "module", {}):
            self.errors.report_error(
                "E001", f"Duplicate module name: {node.name}", node.line, node.column)
        self.symbol_table.enter_scope()
        for child in node.children:
            child.accept(self)
        self.symbol_table.exit_scope()

    def visit_PortNode(self, node):
        if not self.symbol_table.define(node.name, "port", {"type": node.type}):
            self.errors.report_error(
                "E001", f"Duplicate port name: {node.name}", node.line, node.column)

    def visit_ParameterNode(self, node):
        if not self.symbol_table.define(node.name, "parameter", {"default": node.default}):
            self.errors.report_error(
                "E001", f"Duplicate parameter: {node.name}", node.line, node.column)

    def visit_TaskNode(self, node):
        if not self.symbol_table.define(node.name, "task", {}):
            self.errors.report_error(
                "E001", f"Duplicate task name: {node.name}", node.line, node.column)
        self.symbol_table.enter_scope()
        for stmt in node.statements:
            stmt.accept(self)
        self.symbol_table.exit_scope()
