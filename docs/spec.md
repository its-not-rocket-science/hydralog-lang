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
        return tokens

    elif args.command == "parse":
        ast = parse(code)
        print(ast)
        return ast

    elif args.command == "compile":
        if args.target == "spice":
            analog_ir = AnalogIR()
            analog_ir.add_component("filter", "LPF", {"fc": 1000})
            analog_ir.connect("in", "LPF.in")
            analog_ir.connect("LPF.out", "out")
            netlist = generate_spice_netlist(analog_ir)
            with open(args.output, "w") as out:
                out.write(netlist)
            print(f"Wrote SPICE netlist to {args.output}")
            return netlist

        elif args.target == "c":
            from ir.digital_ir import DigitalIR
            from codegen.digital_codegen import generate_digital_c_code
            digital_ir = DigitalIR()
            digital_ir.add_task("log_temperature", ["printf(\"Temp: %d\n\", sensor_read());"])
            c_code = generate_digital_c_code(digital_ir)
            with open(args.output, "w") as out:
                out.write(c_code)
            print(f"Wrote C code to {args.output}")
            return c_code

    elif args.command == "deploy":
        if args.target == "fpaa":
            return deploy_to_fpaa(args.source)
        else:
            print("Unsupported deployment target")
            return "error"

if __name__ == "__main__":
    main()
```

---

## Compiler Architecture (Sketch)

Hydralog's compiler is designed to support hybrid analog-digital targets using a modular, multi-stage pipeline. The compiler architecture includes:

### 1. Frontend
- **Lexer**: Tokenizes the source `.hyd` files.
- **Parser**: Builds an abstract syntax tree (AST).
- **Semantic Analyzer**: Performs deep validation and annotation of the AST.

- **Semantic Analyzer**:
  - Verifies module names, ports, parameters, and signal types
  - Ensures legal connections between analog and digital domains
  - Detects duplicate task names and invalid references
  - Builds a symbol table and performs static type checking
  - Reports all errors and warnings before IR generation

### 1a. Semantic Analysis Data Structures

- **Symbol Table**: Maps names to declarations (modules, ports, parameters, signals).
- **Type Table**: Tracks data types of signals, ports, and parameters.
- **Scope Stack**: Maintains current parsing context (module, task, etc.).
- **Error Collector**: Aggregates semantic warnings and errors for reporting.

### 1b. Semantic Error Model and Diagnostics

- **Error Codes**: Each error has a unique identifier (e.g., E001 for undefined signal, E002 for type mismatch).
- **Error Messages**: Clear and human-readable descriptions of the issue.
- **Locations**: Errors include source file, line, and column information.
- **Severity Levels**: Classify issues as error, warning, or info.
- **Reporting**: All collected errors are reported together to the user before halting compilation.

### 1c. Symbol Table and Scope Model API

The semantic analyzer maintains a hierarchical symbol table to support nested scopes:

- **Global Scope**: Contains module and top-level declarations.
- **Module Scope**: Contains ports, parameters, and signal names for each module.
- **Task Scope**: Contains local variables and signals within digital tasks.
- **Scope Entry/Exit**: Scopes are pushed/popped as modules and tasks are entered/exited.
- **Symbol Lookup**: Supports local lookup first, then parent scopes (lexical scoping).
- **Symbol Table Operations**:
  - `define(name, symbol_type, attributes)` — Adds a symbol to current scope.
  - `lookup(name)` — Finds the nearest visible declaration.
  - `enter_scope()` / `exit_scope()` — Manages nesting.
  - `report_error()` — Adds semantic errors to the error collector.

### 1d. AST Node Types and Structure

The parser constructs a typed AST for semantic analysis and IR generation. Proposed core node types:

- `ProgramNode`: Root container for all modules.
- `ModuleNode`: Represents a module; holds ports, parameters, components, tasks.
- `PortNode`: Defines an input or output port.
- `ParameterNode`: Defines a parameter with optional default value.
- `ComponentNode`: Analog component instantiation.
- `ConnectionNode`: Connects signals between components.
- `TaskNode`: Digital task block with statements.
- `StatementNode`: Abstract base for task statements (assignments, calls).
- `ExpressionNode`: Abstract base for arithmetic or logic expressions.

Each node includes attributes like `line`, `column`, `name`, `type`, and `children` for traversal and diagnostics.

### 1e. AST Traversal and Visitor Model

The compiler uses a visitor pattern to traverse the AST for analysis and IR generation.

- **Visitor Interface**: Defines `visit_<NodeType>` methods for all AST node types.
- **Traversal Mechanism**: The `accept(visitor)` method is implemented by all AST nodes to dispatch to the correct visitor method.
- **Separation of Concerns**:
  - Semantic analysis visitor validates structure and types.
  - IR generation visitor emits analog IR, digital IR, or event graph.
- **Extensibility**: Additional passes (e.g., optimization, code formatting) can be added by implementing new visitors.

### 1f. Semantic Analyzer Visitor Design

The semantic analyzer is implemented as a visitor that walks the AST:

- **visit_ProgramNode**: Initializes global symbol table.
- **visit_ModuleNode**: Defines module in symbol table; creates new scope.
- **visit_PortNode / visit_ParameterNode**: Defines port or parameter symbols.
- **visit_ComponentNode**: Validates component type and parameters.
- **visit_ConnectionNode**: Verifies connected signals exist and are compatible.
- **visit_TaskNode**: Creates task scope; validates task name and statements.
- **visit_StatementNode / visit_ExpressionNode**: Validates local variable references and expression types.
- All validation errors are collected into the error collector with locations and codes.
- Upon completion, the AST is annotated and ready for IR generation.

### 1g. IR Generation Visitor Design

The IR generation visitor transforms the validated AST into intermediate representations:

- **visit_ProgramNode**: Initializes IR containers for analog, digital, and event graphs.
- **visit_ModuleNode**: Defines module context and emits IR blocks.
- **visit_PortNode / visit_ParameterNode**: Adds inputs, outputs, and parameters to the IR model.
- **visit_ComponentNode**: Creates analog IR components and connections.
- **visit_ConnectionNode**: Adds signal flow edges to the analog IR graph.
- **visit_TaskNode**: Generates digital IR tasks with associated statements.
- **visit_StatementNode / visit_ExpressionNode**: Converts statements to IR-level operations.

This visitor ensures a consistent mapping from semantic-validated AST to Hydralog IR.

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

---

## What's Been Implemented

- 🚧 Digital IR infrastructure and backend codegen (next phase)
- 🔍 Semantic analysis planning and AST refactoring roadmap

- 🧠 Language spec and analog instruction abstraction
- 🧾 CLI interface (`hydralogc`) with tokenize, parse, compile, deploy
- 🛠 Analog IR builder and SPICE backend generator
- 🧪 Unit tests for core components with `pytest`
- ✅ GitHub Actions CI pipeline scaffold
- 🧰 Package structure with `setup.py` and proper `__init__.py` modules
- 📊 Code coverage enabled with `pytest-cov`

This modular structure enables experimentation, automated testing, and future support for additional backends or analog compute models.
