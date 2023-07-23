import numpy as np
from typing import List
import radiocores.qammod.model.qammod as qm


class TestQamMod:
    DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    @classmethod
    def setup_class(cls):
        """
        Setting up testing parameters.
        """
        cls.order = 64
        cls.distance = 1.4
        cls.size = int(np.sqrt(cls.order))
        cls.k = int(np.log2(cls.order))

        cls.constellation_int = cls.generate_constellation(dtype=int)
        cls.constellation_complex = cls.generate_constellation(dtype=complex)

    @classmethod
    def generate_constellation(cls, dtype=int) -> np.ndarray:
        """
        Generate a QAM constellation array.
        """
        decimal_data = np.arange(cls.order)
        modulated_symbols = [qm.qammod(data, cls.order, cls.distance) for data in decimal_data]

        constellation = np.zeros((cls.size, cls.size), dtype=dtype)
        offset = (cls.size - 1) / 2

        for data, symbol in zip(decimal_data, modulated_symbols):
            row = int(offset - symbol.imag / cls.distance)
            col = int(symbol.real / cls.distance + offset)

            constellation[row, col] = int(data) if dtype == int else symbol

        return constellation

    def get_binary_representation(
        self, constellation: np.ndarray, row: int, col: int
    ) -> List[str]:
        """
        Get binary representation of a point in the constellation array.
        """
        point = constellation[row % self.size, col % self.size]
        return list(format(point, f"0{self.k}b"))

    def test_grayness(self):
        """
        Check that each point in the constellation differs by one bit from its
        neighbors.
        """
        for row, col in np.ndindex(self.constellation_int.shape):
            current_point = self.get_binary_representation(
                self.constellation_int, row, col
            )
            surrounding_points = [
                self.get_binary_representation(
                    self.constellation_int, row + dr, col + dc
                )
                for dr, dc in self.DIRECTIONS
            ]

            assert all(
                sum(a != b for a, b in zip(current_point, point)) == 1
                for point in surrounding_points
            )

    def test_distance(self):
        """
        Verify that the distances between all adjacent elements are equal to
        the constellation distance set.
        """
        row_differences = self.calculate_differences(axis=0)
        column_differences = self.calculate_differences(axis=1)

        assert np.allclose(
            row_differences, self.distance
        ), f"Row distances not approximately {self.distance}"
        assert np.allclose(
            column_differences, self.distance
        ), f"Column distances not approximately {self.distance}"

    def calculate_differences(self, axis: int) -> np.ndarray:
        """
        Calculate differences along specified axis.
        """
        return np.abs(np.diff(self.constellation_complex, axis=axis))
