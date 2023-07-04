# %%
import matplotlib.pyplot as plt
import numpy as np
from toolz.functoolz import compose


class QamMod:
    def __init__(self, order: int = 16, distance: float = 1.0):
        self.order = order
        self.distance = distance
        self.format = '0' + str(int(np.log2(order))) + 'b'

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

        for i, m_i in enumerate(m):
            edge = (np.sqrt(self.order) - 1) / 2
            row = int((edge - m_i.imag/self.distance))  # Get row
            col = int((m_i.real/self.distance + edge))  # Get column

            if dtype == int:
                y[row, col] = int(x[i])
            elif dtype == complex:
                y[row, col] = m_i

        return y

    def show_constellation(self):
        x = np.arange(self.order)
        points = [self.modulate(x_i) for x_i in x]

        for i, point in enumerate(points):
            plt.plot(point.real, point.imag, '.', color='blue')
            plt.annotate(format(x[i], self.format), (point.real, point.imag))

        plt.show()
        plt.savefig('./gray2bin/model/constellation.png')
