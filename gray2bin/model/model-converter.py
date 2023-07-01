# %%
import matplotlib.pyplot as plt
import numpy as np
from toolz.functoolz import compose
from scipy.spatial.distance import hamming
import unittest


class QamMod:
    def __init__(self, order: int = 16, distance: float = 1.0):
        self.order = order
        self.distance = distance

    def _split(self, x: int, order: int) -> tuple[int, int]:
        return (int(x // np.sqrt(order)), int(x % np.sqrt(order)))

    def _geti(self, x: int) -> int:
        return self._split(x, self.order)[0]

    def _getq(self, x: int) -> int:
        return self._split(x, self.order)[1]

    def _gray2bin(self, x: int) -> int:
        """
        Transform vector of gray encoded values into vector of binary encoded
        values.
        """

        def node(x): return x[0] >> 1, x[1] ^ (x[0] >> 1)

        """
        Compose node() (log2(order) - 1) times and apply composite func to
        each element of x taking only second return value ([1]) from the
        output tuple.
        """
        return compose(*(node,)*int(np.log2(self.order) - 1))((x,)*2)[1]

    def _map(self, x):
        return self.distance * (self._gray2bin(x) - (np.sqrt(self.order)-1)/2)

    def modulate(self, x):
        """Transforms array of integers to QAM symbols.

        Constraints:
            - x is integer from the interval [0, order - 1]
            - order is integer which should be a perfect square and power of 2
            - distance is non-negative real which is a minimum distance
              between modulation symbols
        """
        return self._map(self._geti(x)) - 1j*self._map(self._getq(x))

    def get_constellation(self, dtype=int):
        """
        Returns matrix showing how input data would be mapped onto
        constellation points.
        """
        x = np.arange(self.order)
        m = [QamMod(self.order, self.distance).modulate(x_i) for x_i in x]

        y = np.zeros(
                shape=(
                    int(np.sqrt(self.order)),
                    int(np.sqrt(self.order))),
                dtype=dtype)

        for i, x_i in enumerate(m):
            edge = (self.distance-np.sqrt(self.order))/2

            if dtype == int:
                y[int(-(x_i.imag + edge)), int(x_i.real - edge)] = int(x[i])
            elif dtype == complex:
                y[int(-(x_i.imag + edge)), int(x_i.real - edge)] = x_i

        return y

    def show_constellation(self):
        x = np.arange(self.order)
        points = [self.modulate(x_i) for x_i in x]

        for i, point in enumerate(points):
            plt.plot(point.real, point.imag, '.', color='blue')
            plt.annotate(format(x[i], '06b'), (point.real, point.imag))

        plt.show()
        plt.savefig('./gray2bin/model/constellation.png')

# %%


class Testing(unittest.TestCase):
    """
    The basic class that inherits unittest.TestCase
    """
    distance = 1  # Set constellation minimum distance
    order = 4   # Set modulation order (number of modulation symbols)

    k = int(np.log2(order))  # Number of bits required to represent order
    bin_format = '0' + str(k) + 'b'

    qammod = QamMod(order, distance)  # Instantiate the QamMod class
    qammod.show_constellation()  # Save constellation plot

    modulus = int(np.sqrt(order))

    def test_grayness(self):
        """
        Neighbour constellation points should differ only in one position.
        """
        y = self.qammod.get_constellation()

        def my_format(y):
            return list(format(y, self.bin_format))

        def take_neighbour(y, q, i):
            return my_format(y[q % self.modulus, i % self.modulus])

        for q, i in np.ndindex(y.shape):
            current = take_neighbour(y, q, i)

            # top = list(format(int(y[(q-1) % np.sqrt(self.order), i % np.sqrt(self.order)]), bin_format))
            # left = list(format(int(y[q % np.sqrt(self.order), (i-1) % np.sqrt(self.order)]), bin_format))
            # bottom = list(format(int(y[(q+1) % np.sqrt(self.order), i % np.sqrt(self.order)]), bin_format))
            # right = list(format(int(y[q % np.sqrt(self.order), (i+1) % np.sqrt(self.order)]), bin_format))

            top = take_neighbour(y, q-1, i)
            left = take_neighbour(y, q, i-1)
            bottom = take_neighbour(y, q+1, i)
            right = take_neighbour(y, q, i+1)

            self.assertEqual(hamming(current, top) * self.k, 1)
            self.assertEqual(hamming(current, left) * self.k, 1)
            self.assertEqual(hamming(current, bottom) * self.k, 1)
            self.assertEqual(hamming(current, right) * self.k, 1)

    def test_distance(self):
        """
        Neighbour constellation points should differ only in one position.
        """
        y = self.qammod.get_constellation(dtype=complex)

        for q, i in np.ndindex(y.shape):
            current = y[q,   i]

            top = y[(q-1) % 8,  i % 8]
            left = y[q % 8, (i-1) % 8]
            bottom = y[(q+1) % 8, i % 8]
            right = y[q % 8, (i+1) % 8]

            self.assertEqual(
                np.linalg.norm(current - top), self.distance)
            self.assertEqual(
                np.linalg.norm(current - left), self.distance)
            self.assertEqual(
                np.linalg.norm(current - bottom), self.distance)
            self.assertEqual(
                np.linalg.norm(current - right), self.distance)


# %%


if __name__ == '__main__':
    unittest.main()

# %%
