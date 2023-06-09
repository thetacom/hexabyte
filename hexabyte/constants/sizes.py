"""Size Related Constants.

References
----------
https://en.wikipedia.org/wiki/Word_(computer_architecture)
"""

# Bit Based Sizes and Constants
BIT = 1

NIBBLE_ALIGN_BITS = 2
NIBBLE_BITS = 4  #  2**NIBBLE_ALIGN_BITS

BYTE_ALIGN_BITS = 3
BYTE_BITS = 8  # 2**BYTE_ALIGN_BITS

BYTE_MAX = 255  # 2**BYTE_BITS - 1

# Byte Based Sizes
BYTE_SZ = 1

WORD_ALIGN_BITS = 1
WORD_SZ = 2  # 2**WORD_ALIGN_BITS
WORD_BITS = 16  # BYTE_BITS * WORD_SZ  # 2 bytes

DWORD_ALIGN_BITS = 2
DWORD_SZ = 4  # 2**DWORD_ALIGN_BITS
DWORD_BITS = 32  # BYTE_BITS * DWORD_SZ  # 4 bytes

QWORD_ALIGN_BITS = 3
QWORD_SZ = 8  # 2**QWORD_ALIGN_BITS
QWORD_BITS = 64  # BYTE_BITS * QWORD_SZ  # 8 bytes

PTR32_BITS = DWORD_BITS  # 4 bytes

WORD64_ALIGN_BITS = 2
WORD64_SZ = 4  # 2**WORD_ALIGN_BITS
WORD64_BITS = 32  # BYTE_BITS * WORD_SZ  # 2 bytes

DWORD64_ALIGN_BITS = 3
DWORD64_SZ = 8  # 2**DWORD_ALIGN_BITS
DWORD64_BITS = 64  # BYTE_BITS * DWORD_SZ  # 4 bytes

QWORD64_ALIGN_BITS = 4
QWORD64_SZ = 16  # 2**QWORD_ALIGN_BITS
QWORD64_BITS = 128  # BYTE_BITS * QWORD_SZ  # 8 bytes

PTR64_BITS = QWORD64_BITS  # 4 bytes

KB_ALIGN_BITS = 10
KB = 1024  # 2**KB_ALIGN_BITS
MB_ALIGN_BITS = 20
MB = 1048576  # 2**MB_ALIGN_BITS
GB_ALIGN_BITS = 30
GB = 1073741824  # 2**GB_ALIGN_BITS

# Data Source Constants
DEFAULT_BLOCK_SIZE = 4096  # 2**12
