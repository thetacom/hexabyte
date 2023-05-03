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

![Hexabyte](imgs/logo/hexabyte.png)

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
usage: hexabyte [-h] [-c CONFIG_FILEPATH] [-s] [files ...]

Hexabyte can operate in three distinct modes. Single file mode opens a single file with a single editor. Split screen mode opens a single file with a split screen view. Diff
mode opens two files side by side.

positional arguments:
  files                 Specify 1 or 2 filenames

options:
  -h, --help            show this help message and exit
  -c CONFIG_FILEPATH, --config CONFIG_FILEPATH
                        Specify config location. Default: ~/.config/hexabyte/config.toml
  -s, --split           Display a single file in two split screen editors.
```

![hello_world ELF hex view](imgs/hello_world_hex.png)

![hello_world ELF utf8 view](imgs/hello_world_utf8.png)

![hello_world ELF binary view](imgs/hello_world_binary.png)

![hello_world ELF command view](imgs/hello_world_cmd.png)

![hello_world ELF entropy panel](imgs/hello_world_entropy.png)

![Mach-O Diff with entropy panel](imgs/bin_bash_diff_entropy.png)

![Help Screen](imgs/help_screen.png)

## Developer

```bash
~/$ git clone https://github.com/thetacom/hexabyte
...
~/$ cd hexabyte
hexabyte/$ poetry install
...
```

### Test

```bash
hexabyte/$ make test
...
```
