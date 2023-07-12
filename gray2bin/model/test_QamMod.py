import numpy as np
from scipy.spatial.distance import hamming
from QamMod import QamMod


class TestQamMod:
    DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    @classmethod
    def setup_class(cls):
        cls.order = 64
        cls.distance = 1.4
        cls.size = int(np.sqrt(cls.order))
        cls.k = int(np.log2(cls.order))
        cls.qam_mod = QamMod(cls.order, cls.distance)

    def get_constellation(self, dtype=int):
        x = np.arange(self.order)
        m = [self.qam_mod.modulate(x_i) for x_i in x]

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

    def get_point(self, constellation, row, col):
        m_i = constellation[row % self.size, col % self.size]
        return list(format(m_i, f'0{self.k}b'))

    def test_grayness(self):
        constellation = self.get_constellation()

        for row, col in np.ndindex(constellation.shape):
            current = self.get_point(constellation, row, col)
            surrounding = [self.get_point(constellation, row + dr, col + dc)
                           for dr, dc in self.DIRECTIONS]

            assert all(hamming(current, point) * self.k == 1
                       for point in surrounding)
