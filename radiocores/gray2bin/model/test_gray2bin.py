import numpy as np
import pytest
from radiocores.gray2bin import gray2bin


def bin2gray(binary: int) -> int:
    gray = binary ^ (binary >> 1)
    return gray

@pytest.mark.parametrize('order', [4, 16, 64, 256])  # Add more orders if needed
def test_gray2bin(order):
    vec = np.arange(order)  # generate a vector of values
    vec_gray = np.vectorize(bin2gray)(vec)  # convert to Gray code
    vec_bin = np.vectorize(gray2bin)(vec_gray)  # convert back to binary
    assert np.all(vec == vec_bin)  # compare with initial vector


if __name__ == "__main__":
    pytest.main()
