def bin2gray(binary: int) -> int:
    gray = binary ^ (binary >> 1)
    return gray
