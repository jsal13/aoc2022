from typing import List

from aoc2022.utils import read_aoc_day_data_file

OPPONENT_TO_RPS_MAPPING = {"A": "R", "B": "P", "C": "S"}
PLAYER_TO_RPS_PART_1_MAPPING = {"X": "R", "Y": "P", "Z": "S"}
WIN_LOSE_DRAW_MAPPING = {"Win": 6, "Lose": 0, "Draw": 3}
SHAPE_POINT_MAPPING = {"R": 1, "P": 2, "S": 3}
XYZ_WLD_MAPPING = {"X": "Lose", "Y": "Draw", "Z": "Win"}
WLD_PLAYER_OPPONENT_PLAY_MAPPING = {
    "R": {"S": "Win", "P": "Lose", "R": "Draw"},
    "P": {"R": "Win", "S": "Lose", "P": "Draw"},
    "S": {"P": "Win", "R": "Lose", "S": "Draw"},
}
WLD_OPPONENT_PLAY_MAPPING = {
    "R": {"Win": "P", "Lose": "S", "Draw": "R"},
    "P": {"Win": "S", "Lose": "R", "Draw": "P"},
    "S": {"Win": "R", "Lose": "P", "Draw": "S"},
}


def parse_input(data: str) -> List[List[str]]:
    """Return a list of [R/P/S, X/Y/Z] for each line in the data."""
    split_rows = [row.split(" ") for row in data.splitlines()]
    return [[OPPONENT_TO_RPS_MAPPING[row[0]], row[1]] for row in split_rows]


def part_1_rps_conversion(data: List[List[str]]) -> List[List[str]]:
    """Parse input if doing Part 1 of Day 2."""
    return [[row[0], PLAYER_TO_RPS_PART_1_MAPPING[row[1]]] for row in data]


def part_2_rps_conversion(data: List[List[str]]) -> List[List[str]]:
    """
    Parse input if doing Part 2 of Day 2.

    Note: X means the player needs to lose, Y means the player needs to end the round
    in a draw, and Z means the player needs to win.
    """
    return [
        [row[0], WLD_OPPONENT_PLAY_MAPPING[row[0]][XYZ_WLD_MAPPING[row[1]]]]
        for row in data
    ]


def rps_rules(player: str, opponent: str) -> str:
    """Return 'Lose/Draw/Win' for the player depending on the player/opponent inputs."""
    return WLD_PLAYER_OPPONENT_PLAY_MAPPING[player][opponent]


class Round:
    """
    Represent a single round of RPS.

    Example:
    -------
    rnd = Round(row=["R", "P"])

    """

    def __init__(self, row: List[str]):

        self.row = row
        self.player = self.row[1]
        self.opponent = self.row[0]

    def round_score(self) -> int:
        """Return appropriate player score for the round."""
        return self._calculate_wld_score() + self._calculate_shape_score()

    def _calculate_wld_score(self) -> int:
        """Calculate the player score of one row if they won, lose, drew."""
        return WIN_LOSE_DRAW_MAPPING[rps_rules(self.player, self.opponent)]

    def _calculate_shape_score(self) -> int:
        """Calculate the shape score of the player."""
        return SHAPE_POINT_MAPPING[self.player]


class Game:
    """
    Represent a ``Game`` consisting of multiple ``Round``s.

    Example:
    -------
    game = Game(rows=[["R", "P"], ["P", "P"]])

    """

    def __init__(self, rows: List[List[str]]):
        self.rnds = [Round(row=row) for row in rows]
        self.points = [r.round_score() for r in self.rnds]
        self.total = sum(self.points)


if __name__ == "__main__":
    data_raw = read_aoc_day_data_file(2)
    input_rows = parse_input(data_raw)

    # Part 1
    input_rows_part_1 = part_1_rps_conversion(input_rows)
    game = Game(rows=input_rows_part_1)
    print(f"Part 1: {game.total}")

    # Part 2
    input_rows_part_2 = part_2_rps_conversion(input_rows)
    game = Game(rows=input_rows_part_2)
    print(f"Part 2: {game.total}")
