class DigitalTask:
    def __init__(self, name, statements):
        self.name = name
        self.statements = statements

class DigitalIR:
    def __init__(self):
        self.inputs = {}
        self.outputs = {}
        self.tasks = {}

    def add_input(self, name, dtype='int'):
        self.inputs[name] = dtype

    def add_output(self, name, dtype='int'):
        self.outputs[name] = dtype

    def add_task(self, name, statements):
        self.tasks[name] = DigitalTask(name, statements)