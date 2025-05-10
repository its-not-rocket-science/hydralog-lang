def generate_digital_c_code(ir):
    lines = []
    lines.append("#include <stdio.h>")
    lines.append("")

    for name, dtype in ir.inputs.items():
        lines.append(f"{dtype} {name}; // input")
    for name, dtype in ir.outputs.items():
        lines.append(f"{dtype} {name}; // output")
    lines.append("")

    for task in ir.tasks.values():
        lines.append(f"void {task.name}() {{")
        for stmt in task.statements:
            lines.append(f"    {stmt}")
        lines.append("}")
        lines.append("")

    lines.append("int main() {")
    for task in ir.tasks.values():
        lines.append(f"    {task.name}();")
    lines.append("    return 0;")
    lines.append("}")

    return '\n'.join(lines)