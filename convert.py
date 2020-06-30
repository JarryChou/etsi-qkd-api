from baseconv import base64


def int_to_32_bin(x: int) -> str:
    return '{:032b}'.format(x)


def bin_to_int(x: str) -> int:
    return int(x, 2)


def concat_two_int(x: int, y: int) -> int:
    x_bin = int_to_32_bin(x)
    y_bin = int_to_32_bin(y)
    concat = x_bin + y_bin
    return bin_to_int(concat)


def int_to_base64(x: int) -> str:
    return base64.encode(x)
