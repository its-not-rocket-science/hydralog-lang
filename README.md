# Hydralog

Hydralog is a domain-specific language for hybrid analog-digital programming, designed to bring structure and abstraction to analog computation and hybrid systems.

## Features
- Analog + digital instruction abstraction
- Command-line compiler (`hydralogc`)
- Simulation and backend code generation (SPICE, C, etc.)

## Getting Started
```bash
./hydralogc compile --target spice examples/low_pass_filter.hyd -o out.cir

## Project Structure

- `src/`: Core compiler components (lexer, parser, IR, codegen)
- `docs/`: Language specifications and architecture notes
- `examples/`: Example Hydralog programs (*.hyd)
- `runtime/`: Execution and simulation interfaces
- `tools/`: Utility scripts and deployment tools
- `tests/`: Unit and integration tests
