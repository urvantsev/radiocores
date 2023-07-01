# %%
import matplotlib.pyplot as plt
import numpy as np
from toolz import map
from toolz.functoolz import compose


class QamMod:
    def __init__(self, order: int=16, distance: float=1.0):
        self.order = order
        self.distance = distance


    def _split(self, x: int, order: int) -> tuple[int, int]:
        return (int(x // np.sqrt(order)), int(x % np.sqrt(order)))


    def _geti(self, x: int) -> int:
        return self._split(x, self.order)[0]


    def _getq(self, x: int) -> int:
        return self._split(x, self.order)[1]


    def _gray2bin(self, x: int) -> int:
        """Transform vector of gray encoded values into vector of binary encoded values."""

        def node(x): return x[0] >> 1, x[1] ^ (x[0] >> 1)

        # Compose node() (log2(order) - 1) times and apply composite func to each element of x taking
        # only second return value ([1]) from the output tuple.
        return compose(*(node,)*int(np.log2(self.order) - 1)) ((x,)*2) [1]


    def _map(self, x):
        return self.distance * (self._gray2bin(x) - (np.sqrt(self.order) - 1) / 2)

    def show_constellation(self):
        x = np.arange(order)
        y = [self.modulate(x_i) for x_i in x]

        for i, y_i in enumerate(y):
            plt.plot(y_i.real, y_i.imag, '.', color='blue')
            plt.annotate(format(x[i], '06b'), (y_i.real, y_i.imag))
        plt.show()

    def modulate(self, x):
        """Transforms array of integers to QAM symbols.
        Constraints:
            - x is integer from the interval [0, order - 1]
            - order is integer which should be a perfect square and power of 2
            - distance is non-negative real which is a minimum distance between modulation symbols
        """
        return self._map(self._geti(x)) - 1j*self._map(self._getq(x))



distance = 1
order = 64
# x = np.random.randint(order, size=1024)
QamMod(order, distance).show_constellation()


# %%
from scipy.spatial.distance import hamming

def test_qammod(order, distance):
    x = np.arange(order)
    modulated = [QamMod(order, distance).modulate(x_i) for x_i in x]

    y = np.zeros( shape=( int( np.sqrt(order) ), int( np.sqrt(order) ) ) )

    for i, x_i in enumerate(modulated):
        edge = -np.sqrt(order) / 2 + distance/2
        y[int(x_i.real - edge), int(-(x_i.imag + edge))] = int(x[i])

    return y

distance = 1
order = 64
y = test_qammod(order, distance)
print(y)

for q, i in np.ndindex(y.shape):
    assert hamming( list(format(int(y[q, i]), '06b')), list(format(int(y[q-1, i]), '06b') ) ) * 6 == 1


# %%
