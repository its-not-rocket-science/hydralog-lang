import argparse
from hydralogc.lexer import tokenize
from hydralogc.parser import parse
from hydralogc.ir.analog_ir import AnalogIR
from hydralogc.codegen.spice_backend import generate_spice_netlist
from hydralogc.deploy import deploy_to_fpaa

def main():
    parser = argparse.ArgumentParser(description="Hydralog Compiler")
    parser.add_argument("command", choices=["tokenize", "parse", "compile", "deploy"])
    parser.add_argument("source", help="Hydralog source file")
    parser.add_argument("--target", default="spice", help="Target backend")
    parser.add_argument("-o", "--output", default="output", help="Output file")
    args = parser.parse_args()

    with open(args.source, "r", encoding="utf-8") as f:
        code = f.read()

    if args.command == "tokenize":
        tokens = tokenize(code)
        for t in tokens:
            print(t)
        return tokens

    elif args.command == "parse":
        ast = parse(code)
        print(ast)
        return ast

    elif args.command == "compile":
        analog_ir = AnalogIR()
        analog_ir.add_component("filter", "LPF", {"fc": 1000})
        analog_ir.connect("in", "LPF.in")
        analog_ir.connect("LPF.out", "out")
        netlist = generate_spice_netlist(analog_ir)
        with open(args.output, "w", encoding="utf-8") as out:
            out.write(netlist)
        print(f"Wrote {args.target} netlist to {args.output}")
        return netlist

    elif args.command == "deploy":
        if args.target == "fpaa":
            return deploy_to_fpaa(args.source)
        else:
            print("Unsupported deployment target")
            return "error"

if __name__ == "__main__":
    main()