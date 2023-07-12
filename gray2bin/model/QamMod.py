# %%
import matplotlib.pyplot as plt
import numpy as np


class QamMod:
    def __init__(self, order: int = 16, distance: float = 1.0):
        self.order = order
        self.distance = distance
        self.format = '0' + str(int(np.log2(order))) + 'b'
        self.center_offset = (np.sqrt(self.order)-1)/2

    def _split(self, x: int, order: int) -> tuple[int, int]:
        return int(x // np.sqrt(order)), int(x % np.sqrt(order))

    def _gray2bin(self, gray: int) -> int:
        binary = 0
        while (gray > 0):
            binary ^= gray
            gray = gray >> 1
        return binary

    def _map(self, x):
        return self.distance * (self._gray2bin(x) - self.center_offset)

    def modulate(self, x):
        i, q = self._split(x, self.order)
        return self._map(i) - 1j*self._map(q)

    def show_constellation(self):
        x = np.arange(self.order)
        points = [self.modulate(x_i) for x_i in x]

        for i, point in enumerate(points):
            plt.scatter(point.real, point.imag, color='blue')
            plt.annotate(format(x[i], self.format), (point.real, point.imag))

        plt.show()



# %%
order = 64
distance = 1
qammod = QamMod(order, distance)
qammod.show_constellation()
symbols = [qammod.modulate(x_i) for x_i in np.arange(order)]

# %%
