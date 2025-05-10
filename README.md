# Hydralog

Hydralog is a domain-specific language for hybrid analog-digital programming, designed to bring structure and abstraction to analog computation and hybrid systems.

## Features
- General-purpose syntax for analog and digital modules
- Command-line compiler (`hydralogc`) with multiple targets
- Modular architecture with analog IR, digital IR, and event graphs
- Backend support for SPICE and deployable hardware targets
- Unit testing and code coverage via `pytest` and `pytest-cov`
- CI-ready with GitHub Actions workflow

## Project Structure

- `src/` or `hydralogc/`: Core compiler components (lexer, parser, IR, codegen, CLI)
- `docs/`: Language specifications and architecture notes
- `examples/`: Example Hydralog programs (`*.hyd`)
- `runtime/`: Execution and simulation interfaces
- `tools/`: Utility scripts and deployment tools
- `tests/`: Unit and integration tests
- `.github/workflows/`: GitHub Actions CI

## Quick Start
```bash
# Compile a Hydralog program to SPICE
python -m hydralogc.hydralogc compile --target spice examples/low_pass_filter.hyd -o out.cir

# Compile a digital Hydralog program to C
python -m hydralogc.hydralogc compile --target c examples/digital_logger.hyd -o out.c

# Run unit tests with coverage
PYTHONPATH=. pytest --cov=hydralogc --cov-report=term --cov-report=html
