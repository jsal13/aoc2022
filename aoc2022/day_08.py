from math import prod
from typing import List

from aoc2022.utils import read_aoc_day_data_file


def parse_input(data: str) -> List[List[int]]:
    """Parse input for Day 8."""
    grid = []
    for line in data.splitlines():
        row = []
        for elt in line:
            row.append(int(elt))
        grid.append(row)
    return grid


class TreeGrid:
    """Represent a grid of tree heights."""

    def __init__(self, grid: List[List[int]]):
        self.grid = grid
        self.size = len(self.grid)

    def is_visible(self, row: int, col: int) -> bool:
        """Return if a tree at ``[row, col]`` is visible from any direction."""
        val = self.grid[row][col]

        if (row == 0) or (row == self.size - 1) or (col == 0) or (col == self.size - 1):
            return True

        return any(
            [
                all(self.grid[i][col] < val for i in range(0, row)),  # top
                all(self.grid[i][col] < val for i in range(row + 1, self.size)),  # bottom
                all(self.grid[row][i] < val for i in range(0, col)),  # left
                all(self.grid[row][i] < val for i in range(col + 1, self.size)),  #  right
            ]
        )

    def count_visible(self) -> int:
        """Count the number of ``is_visible`` trees in the grid."""
        return sum(
            self.is_visible(row=row, col=col)
            for row in range(self.size)
            for col in range(self.size)
        )

    def num_trees_visible(self, row: int, col: int) -> List[int]:
        """
        Count how many trees are visible from the vantage point of ``[row, col]``.

        Notes
        -----
        The return value is of the form ``[upward, left, down, right]``.

        """
        if (row == 0) or (row == self.size - 1) or (col == 0) or (col == self.size - 1):
            return [0, 0, 0, 0]

        value = self.grid[row][col]

        # left
        left = 0
        while col - left > 0:
            left += 1
            if self.grid[row][col - left] >= value:
                break

        # right
        right = 0
        while col + right < self.size - 1:
            right += 1
            if self.grid[row][col + right] >= value:
                break

        # up
        upward = 0
        while row - upward > 0:
            upward += 1
            if self.grid[row - upward][col] >= value:
                break

        # down
        down = 0
        while row + down < self.size - 1:
            down += 1
            if self.grid[row + down][col] >= value:
                break

        return [upward, left, down, right]

    def calculate_scenic_score(self, row: int, col: int):
        """Calculate the 'Scenic Score' of the tree."""
        return prod(self.num_trees_visible(row=row, col=col))


if __name__ == "__main__":
    raw_data = read_aoc_day_data_file(8)
    treegrid = TreeGrid(parse_input(raw_data))

    # Part 1
    print(f"Part 1: {treegrid.count_visible()}")

    # Part 2
    max_score: int = 0
    for _row in range(1, treegrid.size - 1):
        for _col in range(1, treegrid.size - 1):
            score = treegrid.calculate_scenic_score(row=_row, col=_col)
            if score > max_score:
                max_score = score

    print(f"Part 2: {max_score}")
