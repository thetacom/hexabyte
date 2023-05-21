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

> **NOTE:** To reduce the number of dependencies of the core editor. The builtin plugins have been moved into separate packages. They are [hexabyte_extended_info](https://github.com/thetacom/hexabyte_extended_info) and [hexabyte_entropy](https://github.com/thetacom/hexabyte_entropy).

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

Help Screen

![Help Screen](imgs/help_screen.png)

Command Prompt

![hello_world ELF command view](imgs/hello_world_cmd.png)

Single File - Split Screen

![Single File - Split Screen](imgs/hello_world_split.png)

Single File - Hexadecimal View Mode

![hello_world ELF hex view](imgs/hello_world_hex.png)

UTF8 View Mode

![hello_world ELF utf8 view](imgs/hello_world_utf8.png)

Binary View Mode

![hello_world ELF binary view](imgs/hello_world_binary.png)

Two Files - Diff View
![Two Files - Diff View](imgs/diff.png)

### Plugins and Customization

Hexabyte's interface is highly customizable. You can adjust the column size and column count for each view mode.

![Config](imgs/config.png)

Hexabyte functionality can be extended through the use of plugins.

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
