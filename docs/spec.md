# Hydralog: Specification for a Hybrid Analog-Digital Programming Language

## Overview
**Hydralog** is a high-level, strongly-typed domain-specific language (DSL) designed to program hybrid analog-digital systems. It abstracts away hardware-specific details and offers a general-purpose model for configuring, simulating, and compiling analog instructions alongside digital logic.

---

## Language Design Goals
- Enable structured analog computation through composable modules
- Provide analog instruction set abstraction
- Allow seamless analog-digital interaction
- Support simulation, compilation, and deployment on FPAAs, hybrid SoCs, and neuromorphic hardware

---

## CLI Interface (hydralogc)

Hydralog provides a command-line interface (`hydralogc`) to run the full compilation pipeline from source code to simulation or deployment.

### CLI Structure
```text
hydralogc [COMMAND] [OPTIONS] <source_file>
```

### Supported Commands
- `tokenize` – Print token stream
- `parse` – Print parsed AST
- `ir` – Generate and display IR (analog, digital, events)
- `compile` – Generate backend code (SPICE, C, etc.)
- `simulate` – Run analog/digital/event simulation
- `deploy` – Send compiled code to hardware targets

### Example Usage
```bash
hydralogc tokenize examples/low_pass_filter.hyd
hydralogc parse examples/low_pass_filter.hyd
hydralogc compile --target spice examples/low_pass_filter.hyd -o out.cir
hydralogc deploy --target fpaa out.cfg
```

### CLI Implementation (Python)
```python
import argparse
from lexer import tokenize
from parser import parse
from ir.analog_ir import AnalogIR
from codegen.spice_backend import generate_spice_netlist
from deploy import deploy_to_fpaa

def main():
    parser = argparse.ArgumentParser(description="Hydralog Compiler")
    parser.add_argument("command", choices=["tokenize", "parse", "compile", "deploy"])
    parser.add_argument("source", help="Hydralog source file")
    parser.add_argument("--target", default="spice", help="Target backend")
    parser.add_argument("-o", "--output", default="output", help="Output file")
    args = parser.parse_args()

    with open(args.source) as f:
        code = f.read()

    if args.command == "tokenize":
        tokens = tokenize(code)
        for t in tokens:
            print(t)

    elif args.command == "parse":
        ast = parse(code)
        print(ast)

    elif args.command == "compile":
        analog_ir = AnalogIR()  # Normally filled from parsed AST
        netlist = generate_spice_netlist(analog_ir)
        with open(args.output, "w") as out:
            out.write(netlist)
        print(f"Wrote {args.target} netlist to {args.output}")

    elif args.command == "deploy":
        if args.target == "fpaa":
            deploy_to_fpaa(args.source)
        else:
            print("Unsupported deployment target")

if __name__ == "__main__":
    main()
```

---

## Compiler Architecture (Sketch)

Hydralog's compiler is designed to support hybrid analog-digital targets using a modular, multi-stage pipeline. The compiler architecture includes:

### 1. Frontend
- **Lexer**: Tokenizes the source `.hyd` files.
- **Parser**: Builds an abstract syntax tree (AST).
- **Semantic Analyzer**: Checks type consistency, parameter validity, and analog-digital boundaries.

### 2. Intermediate Representations
- **Analog IR**: DAG of components (e.g., amplifiers, filters) and signal flow.
- **Digital IR**: Representation of digital control logic and discrete tasks.
- **Event Graph**: Maps analog signal conditions to digital task triggers.

### 3. Code Generators
- **Analog Backend**: Emits SPICE netlists or FPAA configuration code.
- **Digital Backend**: Generates C/C++ code for microcontroller-based logic.

### 4. Simulation and Deployment
- **Simulator**: Optional modules to simulate analog circuits or hybrid event response.
- **Deployer**: Sends output files to hardware (e.g., via USB/JTAG to FPAAs).

### 5. CLI Integration
The entire pipeline is wrapped in a command-line interface (`hydralogc`) that allows users to invoke individual stages or full compilation/deployment flows.

This modular structure enables experimentation, modular replacement of parts, and future support for additional analog or digital backends.
