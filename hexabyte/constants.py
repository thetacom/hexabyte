"""Hexabyte Constants."""

from pathlib import Path

DEFAULT_CONFIG_PATH = Path("~/.config/hexabyte/")
CONFIG_FILENAME = "config.toml"
DIFF_MODEL_COUNT = 2

# Generic Sizes
BYTE = 8
KB = 1024
MB = KB * 1024

# 32-bit Sizes
WORD_32BIT = BYTE * 2  # 2 bytes
DWORD_32BIT = WORD_32BIT * 2  # 4 bytes
QWORD_32BIT = DWORD_32BIT * 2  # 8 bytes
PTR_32BIT = DWORD_32BIT  # 4 bytes
# 64-bit Sizes
WORD_64BIT = BYTE * 4  # 4 bytes
DWORD_64BIT = WORD_64BIT * 2  # 8 bytes
QWORD_64BIT = DWORD_64BIT * 2  # 16 bytes
PTR_64BIT = DWORD_64BIT  # 8 bytes
