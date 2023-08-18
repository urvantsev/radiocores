import numpy as np
import pytest
from radiocores.bin2gray import bin2gray
from radiocores.gray2bin import gray2bin


@pytest.mark.parametrize("order", [4, 16, 64, 256])  # Add more orders if needed
def test_gray2bin(order):
    vec = np.arange(order)  # generate a vector of values
    vec_gray = np.vectorize(bin2gray)(vec)  # convert to Gray code
    vec_bin = np.vectorize(gray2bin)(vec_gray)  # convert back to binary
    assert np.all(vec == vec_bin)  # compare with initial vector


if __name__ == "__main__":
    pytest.main()
