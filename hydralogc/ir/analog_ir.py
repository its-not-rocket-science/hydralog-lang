class AnalogIR:
    def __init__(self):
        self.components = []
        self.connections = []

    def add_component(self, comp_type, name, params):
        self.components.append((comp_type, name, params))

    def connect(self, src, dst):
        self.connections.append((src, dst))