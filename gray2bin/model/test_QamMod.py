import numpy as np
from scipy.spatial.distance import hamming
from numpy.linalg import norm
from QamMod import QamMod


class TestQamMod:
    """
    The basic class that inherits unittest.TestCase
    """
    distance = 1.4                    # Constellation minimum distance
    order = 16                        # Number of modulation symbols
    k = int(np.log2(order))           # Number of bits to represent order
    qammod = QamMod(order, distance)  # Instantiate QamMod
    qammod.show_constellation()       # Save constellation plot
    m = qammod.get_constellation()    # Get signal constellation

    modulus = int(np.sqrt(order))

    def test_grayness(self):
        """
        Test that signal constellation satisfy "grayness" propery.

        Property: nearby points differ in one position.

        Note: two points are nearby if only one coordinate differs by
        "distance"
        """
        print(self.m)

        def do_format(m_i):
            return list(format(m_i, '0' + str(self.k) + 'b'))

        def get_point(m, row, col):
            return do_format(m[row % self.modulus, col % self.modulus])

        for row, col in np.ndindex(self.m.shape):
            current = get_point(self.m, row, col)

            top = get_point(self.m, row - 1, col)
            left = get_point(self.m, row, col-1)
            bottom = get_point(self.m, row + 1, col)
            right = get_point(self.m, row, col + 1)

            assert hamming(current, top) * self.k == 1
            assert hamming(current, left) * self.k == 1
            assert hamming(current, bottom) * self.k == 1
            assert hamming(current, right) * self.k == 1

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

            assert norm(current - top) == self.distance
            assert norm(current - left) == self.distance
            assert norm(current - bottom) == self.distance
            assert norm(current - right) == self.distance
