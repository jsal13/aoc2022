from typing import Dict, List

import numpy as np

from aoc2022.utils import read_aoc_day_data_file


def parse_cmds(data: str) -> List[tuple[str, int]]:
    split_lines = [line.split() for line in data.splitlines()]
    return [(elt[0], int(elt[1])) for elt in split_lines]


class RopeGrid:
    def __init__(self, start_loc, num_knots: int, grid_size: int = 1000):
        self.start_loc = start_loc
        self.grid_size = grid_size

        # "0" is the head knot, or the head.
        self.knots = list(range(num_knots))

        self.knots_locs: Dict[int, List[int]] = {k: self.start_loc for k in self.knots}

        self.points_visited_by_knots = {k: [self.start_loc] for k in self.knots}
        self.grid = self._create_grid()

    def _create_grid(self):
        return np.full(shape=(self.grid_size, self.grid_size), fill_value=".", dtype=str)

    def move(self, head_direction: str):
        """Iterate movement for all knots, head first."""
        for knot in self.knots:
            if knot == 0:
                self._move_head(direction=head_direction)
            else:
                self._move_knot(knot=knot)

    def _move_head(self, direction: str):
        """Move the head knot by ``direction``."""
        if direction == "L":
            self.knots_locs[0] = [self.knots_locs[0][0], self.knots_locs[0][1] - 1]
        elif direction == "R":
            self.knots_locs[0] = [self.knots_locs[0][0], self.knots_locs[0][1] + 1]
        elif direction == "U":
            self.knots_locs[0] = [self.knots_locs[0][0] - 1, self.knots_locs[0][1]]
        elif direction == "D":
            self.knots_locs[0] = [self.knots_locs[0][0] + 1, self.knots_locs[0][1]]
        else:
            raise ValueError("`direction` must be in one of: 'L','R','U','D'.")

    def _move_knot(self, knot: int):
        """
        Move the knot ("1", "2", ..., "9") according to where the head is.

        If the head is ever two steps directly up, down, left, or right from the tail,
        the tail must also move one step in that direction so it remains close enough.

        Otherwise, if the head and tail aren't touching and aren't in the same row
        or column, the tail always moves one step diagonally to keep up.
        """
        head_row_coord = self.knots_locs[knot - 1][0]
        head_col_coord = self.knots_locs[knot - 1][1]
        knot_row_coord = self.knots_locs[knot][0]
        knot_col_coord = self.knots_locs[knot][1]

        # TODO: Clean this up, it's a nightmare.

        # The following are places to check...
        # Note the head must be at least 2 away in some direction.
        #
        # 1 a . b 3
        # g . . . c
        # . . T . .
        # h . . . d
        # 2 e . f 4

        if head_col_coord == knot_col_coord:
            if head_row_coord - 2 == knot_row_coord:  # Due South
                self.knots_locs[knot] = [
                    self.knots_locs[knot][0] + 1,
                    self.knots_locs[knot][1],
                ]
            elif head_row_coord + 2 == knot_row_coord:  # Due North
                self.knots_locs[knot] = [
                    self.knots_locs[knot][0] - 1,
                    self.knots_locs[knot][1],
                ]
        elif head_row_coord == knot_row_coord:
            if head_col_coord - 2 == knot_col_coord:  # Due East
                self.knots_locs[knot] = [
                    self.knots_locs[knot][0],
                    self.knots_locs[knot][1] + 1,
                ]
            elif head_col_coord + 2 == knot_col_coord:  # Due West
                self.knots_locs[knot] = [
                    self.knots_locs[knot][0],
                    self.knots_locs[knot][1] - 1,
                ]

        # 1
        if (
            head_col_coord + 2 == knot_col_coord and head_row_coord + 2 == knot_row_coord
        ):  # 1
            self.knots_locs[knot] = [
                self.knots_locs[knot][0] - 1,
                self.knots_locs[knot][1] - 1,
            ]

        elif (
            head_col_coord + 2 == knot_col_coord and head_row_coord - 2 == knot_row_coord
        ):  # '2'
            self.knots_locs[knot] = [
                self.knots_locs[knot][0] + 1,
                self.knots_locs[knot][1] - 1,
            ]

        elif (
            head_col_coord - 2 == knot_col_coord and head_row_coord + 2 == knot_row_coord
        ):  # '3'
            self.knots_locs[knot] = [
                self.knots_locs[knot][0] - 1,
                self.knots_locs[knot][1] + 1,
            ]
        elif (
            head_col_coord - 2 == knot_col_coord and head_row_coord - 2 == knot_row_coord
        ):  # '4'
            self.knots_locs[knot] = [
                self.knots_locs[knot][0] + 1,
                self.knots_locs[knot][1] + 1,
            ]

        # Position 'a'/'b'
        if head_row_coord + 2 == knot_row_coord:
            if head_col_coord + 1 == knot_col_coord:  # 'a'
                self.knots_locs[knot] = [
                    self.knots_locs[knot][0] - 1,
                    self.knots_locs[knot][1] - 1,
                ]
            elif head_col_coord - 1 == knot_col_coord:  # 'b'
                self.knots_locs[knot] = [
                    self.knots_locs[knot][0] - 1,
                    self.knots_locs[knot][1] + 1,
                ]

        # Position 'c'/'d'
        elif head_col_coord - 2 == knot_col_coord:
            if head_row_coord + 1 == knot_row_coord:  # 'c'
                self.knots_locs[knot] = [
                    self.knots_locs[knot][0] - 1,
                    self.knots_locs[knot][1] + 1,
                ]
            elif head_row_coord - 1 == knot_row_coord:  # 'd'
                self.knots_locs[knot] = [
                    self.knots_locs[knot][0] + 1,
                    self.knots_locs[knot][1] + 1,
                ]

        # Position 'e'/'f'
        elif head_row_coord - 2 == knot_row_coord:
            if head_col_coord + 1 == knot_col_coord:  # 'e'
                self.knots_locs[knot] = [
                    self.knots_locs[knot][0] + 1,
                    self.knots_locs[knot][1] - 1,
                ]
            elif head_col_coord - 1 == knot_col_coord:  # 'f'
                self.knots_locs[knot] = [
                    self.knots_locs[knot][0] + 1,
                    self.knots_locs[knot][1] + 1,
                ]

        # Position 'g'/'h'
        elif head_col_coord + 2 == knot_col_coord:
            if head_row_coord + 1 == knot_row_coord:  # 'g'
                self.knots_locs[knot] = [
                    self.knots_locs[knot][0] - 1,
                    self.knots_locs[knot][1] - 1,
                ]
            elif head_row_coord - 1 == knot_row_coord:  # 'h'
                self.knots_locs[knot] = [
                    self.knots_locs[knot][0] + 1,
                    self.knots_locs[knot][1] - 1,
                ]

        if self.knots_locs[knot] not in self.points_visited_by_knots[knot]:
            self.points_visited_by_knots[knot].append(self.knots_locs[knot])

    def plot_rope_grid(self):
        """Make a plot of the rope grid."""
        # TODO: Does this work correctly for test input?
        self.grid.fill(".")
        self.grid[self.start_loc[0], self.start_loc[1]] = "s"
        for knot in self.knots:
            if knot > 0:
                self.grid[self.knots_locs[knot][0], self.knots_locs[knot][1]] = knot
            else:
                self.grid[self.knots_locs[0][0], self.knots_locs[0][1]] = "H"
        return self.grid


if __name__ == "__main__":
    raw_data = read_aoc_day_data_file(9)

    cmds = parse_cmds(raw_data)
    GRID_SIZE = 1000

    # Part 1
    ropegrid = RopeGrid(
        start_loc=[int(GRID_SIZE / 2), int(GRID_SIZE / 2)],
        num_knots=2,
        grid_size=GRID_SIZE,
    )

    for cmd in cmds:
        for _ in range(cmd[1]):
            ropegrid.move(cmd[0])

    print(f"Part 1: {len(ropegrid.points_visited_by_knots[1])}")

    # Part 2
    ropegrid = RopeGrid(
        start_loc=[int(GRID_SIZE / 2), int(GRID_SIZE / 2)],
        num_knots=10,
        grid_size=GRID_SIZE,
    )

    for cmd in cmds:
        for _ in range(cmd[1]):
            ropegrid.move(cmd[0])

    print(f"Part 2: {len(ropegrid.points_visited_by_knots[9])}")
