# Testing

This package uses the pytest framework.

## Installation

The installation steps are similar to those described in [`README.md`](../README.md), but the `[dev]` extra is required to install pytest as well.

```bash
$ git clone https://github.com/MingMinNa/Python-LightsOut.git
$ cd Python-LightsOut
$ pip install -e ".[dev]"
```

## Run tests
```bash
# Run all tests with code coverage
$ pytest tests/ --cov --cov-report=term-missing

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
testpaths: tests
plugins: cov-7.1.0
collected 146 items

tests\test_board.py .................................................... [ 35%]
.......................                                                  [ 51%]
tests\test_generator.py ......................................           [ 77%]
tests\test_solver.py .................................                   [100%]

=============================== tests coverage ================================
______________ coverage: platform win32, python 3.13.15-final-0 _______________

Name                         Stmts   Miss  Cover   Missing
----------------------------------------------------------
src\lightsout\__init__.py       11      2    82%   22-23
src\lightsout\board.py         102      0   100%
src\lightsout\consts.py         12      0   100%
src\lightsout\exception.py       2      0   100%
src\lightsout\generator.py      35      0   100%
src\lightsout\solver.py         74      0   100%
----------------------------------------------------------
TOTAL                          236      2    99%
============================= 146 passed in 0.81s =============================
```