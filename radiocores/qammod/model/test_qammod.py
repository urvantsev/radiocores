import numpy as np
from typing import List
import radiocores.qammod.model.qammod as qm
import pytest


class TestQamMod:
    DIRECTIONS = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    @staticmethod
    def generate_constellation(order, distance, dtype=int) -> np.ndarray:
        """
        Generate a QAM constellation array.
        """
        size = int(np.sqrt(order))
        decimal_data = np.arange(order)
        modulated_symbols = [qm.qammod(data, order, distance) for data in decimal_data]

        constellation = np.zeros((size, size), dtype=dtype)
        offset = (size - 1) / 2

        for data, symbol in zip(decimal_data, modulated_symbols):
            row = int(offset - symbol.imag / distance)
            col = int(symbol.real / distance + offset)

            constellation[row, col] = int(data) if dtype == int else symbol

        return constellation

    @staticmethod
    def get_binary_representation(constellation, size, k, row, col) -> List[str]:
        """
        Get binary representation of a point in the constellation array.
        """
        point = constellation[row % size, col % size]
        return list(format(point, f"0{k}b"))

    @pytest.mark.parametrize(
        "order, distance", [(4, 0.3), (16, 1), (64, 1.41), (256, 10.5)]
    )  # add more parameter tuples if needed
    def test_grayness(self, order, distance):
        """
        Check that each point in the constellation differs by one bit from its
        neighbors.
        """
        size = int(np.sqrt(order))
        k = int(np.log2(order))
        constellation_int = self.generate_constellation(order, distance, dtype=int)

        for row, col in np.ndindex(constellation_int.shape):
            current_point = self.get_binary_representation(
                constellation_int, size, k, row, col
            )
            surrounding_points = [
                self.get_binary_representation(
                    constellation_int, size, k, row + dr, col + dc
                )
                for dr, dc in self.DIRECTIONS
            ]

            assert all(
                sum(a != b for a, b in zip(current_point, point)) == 1
                for point in surrounding_points
            )

    @pytest.mark.parametrize(
        "order, distance", [(4, 0.3), (16, 1), (64, 1.41), (256, 10.5)]
    )  # add more parameter tuples if needed
    def test_distance(self, order, distance):
        """
        Verify that the distances between all adjacent elements are equal to
        the constellation distance set.
        """
        constellation_complex = self.generate_constellation(
            order, distance, dtype=complex
        )

        row_differences = np.abs(np.diff(constellation_complex, axis=0))
        column_differences = np.abs(np.diff(constellation_complex, axis=1))

        assert np.allclose(
            row_differences, distance
        ), f"Row distances not approximately {distance}"
        assert np.allclose(
            column_differences, distance
        ), f"Column distances not approximately {distance}"
