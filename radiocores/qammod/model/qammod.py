# %%
import numpy as np
from radiocores.gray2bin import gray2bin


def qammod(x: int, order: int, distance: float) -> complex:
    # create the vector [i, q]
    vec = np.array([x // np.sqrt(order), x % np.sqrt(order)], dtype=int)

    # transform from gray to bin and apply offset to each element
    vec_transformed = np.vectorize(gray2bin)(vec) - (np.sqrt(order) - 1) / 2

    # calculate the scalar product with [1, -1j]
    result = np.dot(distance * vec_transformed, [1, -1j])

    return result
