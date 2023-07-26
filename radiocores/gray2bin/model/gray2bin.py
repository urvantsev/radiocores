def gray2bin(gray: int) -> int:
    binary = 0
    while gray > 0:
        binary ^= gray
        gray = gray >> 1
    return binary
