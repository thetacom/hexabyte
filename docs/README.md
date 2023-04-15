# Hexabyte - Commandline Hex Editor

A modern, robust, and extensible commandline hex editor.

## Usage

```bash
~/$ pip install hexabyte
...
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
