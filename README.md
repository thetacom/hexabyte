# Hexabyte - Commandline Hex Editor

[![Version](https://img.shields.io/pypi/v/hexabyte.svg)](https://pypi.python.org/pypi/hexabyte)
[![Status](https://img.shields.io/pypi/status/hexabyte)](https://pypi.python.org/pypi/hexabyte)
[![Wheel](https://img.shields.io/pypi/wheel/hexabyte)](https://pypi.org/project/hexabyte/)
[![Downloads](https://img.shields.io/pypi/dm/hexabyte)](https://pypi.python.org/pypi/hexabyte)
[![License](https://img.shields.io/pypi/l/hexabyte.svg)](https://pypi.python.org/pypi/hexabyte)
[![Python Implementation](https://img.shields.io/pypi/implementation/hexabyte)](https://pypi.org/project/hexabyte/)
[![Python Version](https://img.shields.io/pypi/pyversions/hexabyte)](https://pypi.org/project/hexabyte/)

[![Lint](https://github.com/thetacom/hexabyte/actions/workflows/lint.yml/badge.svg)](https://github.com/thetacom/hexabyte/actions/)
[![Test](https://github.com/thetacom/hexabyte/actions/workflows/test.yml/badge.svg)](https://github.com/thetacom/hexabyte/actions/)
[![Release](https://github.com/thetacom/hexabyte/actions/workflows/release.yml/badge.svg)](https://github.com/thetacom/hexabyte/actions/)
[![Publish](https://github.com/thetacom/hexabyte/actions/workflows/publish.yml/badge.svg)](https://github.com/thetacom/hexabyte/actions/)

[![Pre-Commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)

A modern, robust, and extensible commandline hex editor.

## User

### Install

```bash
~/$ pip install hexabyte
...
```

### Run

```bash
~/$ hexabyte --help
Usage: hexabyte [OPTIONS] FILENAME1 [FILENAME2]

  Start the hexabyte application.

Options:
  -c, --config PATH  [default: ~/.config/hexabyte/config.toml]
  --help             Show this message and exit.
```

## Developer

```bash
~/$ git clone https://github.com/thetacom/hexabyte
...
~/$ cd hexabyte
hexabyte/$ poetry install
...
```
