# Testing

This package uses the pytest framework.

## Installation

The installation steps are similar to those described in [`README.md`](../README.md), but the `[test]` extra is required to install pytest as well.

### Install from the repository
```bash
$ git clone https://github.com/MingMinNa/Python-LightsOut.git
$ cd Python-LightsOut
$ pip install .[test]
```

### Install via PyPI
```bash
$ pip install python-lightsout[test]
```

## Run tests
```bash
# Run all tests
$ pytest tests/

# Run tests in a specific file
$ pytest tests/test_board.py

# Run a specific test class
$ pytest tests/test_board.py::TestConstruction

# Run a specific test
$ pytest tests/test_board.py::TestConstruction::test_default_grid_is_all_off
```

## Output
```bash
============================= test session starts =============================
platform win32 -- Python 3.13.15, pytest-9.1.1, pluggy-1.6.0
rootdir: ...\Python-LightsOut
configfile: pyproject.toml
collected 95 items

tests\test_board.py ..................................................   [ 52%]
tests\test_generator.py .....................                            [ 74%]
tests\test_solver.py ........................                            [100%]

============================= 95 passed in 0.28s ==============================
```