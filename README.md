# Hexabyte - Commandline Hex Editor

[![python version](https://img.shields.io/pypi/v/hexabyte)](https://pypi.org/project/hexabyte/)
[![python implementation](https://img.shields.io/pypi/implementation/hexabyte)](https://pypi.org/project/hexabyte/)
[![python version](https://img.shields.io/pypi/pyversions/hexabyte)](https://pypi.org/project/hexabyte/)
[![python wheel](https://img.shields.io/pypi/wheel/hexabyte)](https://pypi.org/project/hexabyte/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![version](https://img.shields.io/pypi/v/hexabyte.svg)](https://pypi.python.org/pypi/hexabyte)
[![license](https://img.shields.io/pypi/l/hexabyte.svg)](https://pypi.python.org/pypi/hexabyte)
[![python versions](https://img.shields.io/pypi/pyversions/hexabyte.svg)](https://pypi.python.org/pypi/hexabyte)
[![Actions status](https://github.com/thetacom/hexabyte/workflows/CI/badge.svg)](https://github.com/thetacom/hexabyte/actions)
A modern, robust, and extensible commandline hex editor.

## User

### Build

```bash
hexabyte/$ pip install poetry
...
hexabyte/$ poetry build
...
hexabyte/$ pip install pip install dist/hexabyte-0.1.0-py3-none-any.whl
...
```

### Run

```bash
hexabyte/$ hexabyte --help
Usage: hexabyte [OPTIONS] FILENAME1 [FILENAME2]

  Start the hexabyte application.

Options:
  -c, --config PATH  [default: ~/.config/hexabyte/config.toml]
  --help             Show this message and exit.
```

```bash
hexabyte/$
```

### Install

## Developer

```bash
hexabyte/$ poetry install
...
```
