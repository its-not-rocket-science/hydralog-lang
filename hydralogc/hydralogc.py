import argparse
from hydralogc.lexer import tokenize
from hydralogc.parser import parse
from hydralogc.ir.analog_ir import AnalogIR
from hydralogc.ir.digital_ir import DigitalIR
from hydralogc.codegen.spice_backend import generate_spice_netlist
from hydralogc.codegen.digital_codegen import generate_digital_c_code


def main():
    parser = argparse.ArgumentParser(description="Hydralog Compiler")
    parser.add_argument("command", choices=[
                        "tokenize", "parse", "compile", "deploy"])
    parser.add_argument("source", help="Hydralog source file")
    parser.add_argument("--target", default="spice",
                        help="Target backend (spice | c)")
    parser.add_argument("-o", "--output", default="output", help="Output file")
    args = parser.parse_args()

    with open(args.source, encoding="utf-8") as f:
        code = f.read()

    if args.command == "tokenize":
        tokens = tokenize(code)
        for t in tokens:
            print(t)
        return tokens

    if args.command == "parse":
        ast = parse(code)
        print(ast)
        return ast

    if args.command == "compile":
        if args.target == "spice":
            analog_ir = AnalogIR()
            analog_ir.add_component("filter", "LPF", {"fc": 1000})
            analog_ir.connect("in", "LPF.in")
            analog_ir.connect("LPF.out", "out")
            netlist = generate_spice_netlist(analog_ir)
            with open(args.output, "w", encoding="utf-8") as out:
                out.write(netlist)
            print(f"Wrote SPICE netlist to {args.output}")
            return netlist

        if args.target == "c":
            digital_ir = DigitalIR()
            digital_ir.add_task("log_temperature", [
                                "printf(\"Temp: %d\\n\", sensor_read());"])
            c_code = generate_digital_c_code(digital_ir)
            with open(args.output, "w", encoding="utf-8") as out:
                out.write(c_code)
            print(f"Wrote C code to {args.output}")
            return c_code

        print(f"Unknown compile target: {args.target}")
        return "error"

    if args.command == "deploy":
        if args.target == "fpaa":
            from hydralogc.deploy import deploy_to_fpaa
            return deploy_to_fpaa(args.source)

        print("Unsupported deployment target")
        return "error"


if __name__ == "__main__":
    main()
