class ErrorCollector:
    def __init__(self):
        self.errors = []

    def report_error(self, code, message, line, column):
        self.errors.append({
            "code": code,
            "message": message,
            "line": line,
            "column": column
        })

    def has_errors(self):
        return len(self.errors) > 0

    def print_errors(self):
        for error in self.errors:
            print(
                f"[{error['code']}] {error['message']} at line {error['line']}, column {error['column']}")
