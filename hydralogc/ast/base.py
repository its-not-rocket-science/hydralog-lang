class ASTNode:
    def __init__(self, line=0, column=0):
        self.line = line
        self.column = column
        self.children = []

    def accept(self, visitor):
        method_name = f'visit_{self.__class__.__name__}'
        visit = getattr(visitor, method_name, visitor.generic_visit)
        return visit(self)
