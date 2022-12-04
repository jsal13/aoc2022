from typing import List, Set

from aoc2022.utils import read_aoc_day_data_file


def input_parser(data: str) -> List[List[Set[int]]]:
    """Parse input for Day 4."""

    def _dashes_to_range(s: str) -> Set[int]:
        """Convert 'n-m' to ``list(range(n, m+1))``."""
        min_val, max_val = map(int, s.split("-"))
        return set(range(min_val, max_val + 1))

    rows = [row.split(",") for row in data.splitlines()]
    return [[_dashes_to_range(row[0]), _dashes_to_range(row[1])] for row in rows]


class Pairing:
    """Represent a pairing of Elves."""

    def __init__(self, pairing: List[Set[int]]):
        self.pairing = pairing

    def find_common_elts(self) -> Set[int]:
        """Find common elements in the pairing."""
        return set.intersection(*self.pairing)

    def pair_contains_subset(self) -> bool:
        """Return True if one pair is a subset of the other."""
        return self.pairing[0].issubset(self.pairing[1]) or self.pairing[1].issubset(
            self.pairing[0]
        )


class Pairings:
    """Represent a collection of ``Pairing`` objects."""

    def __init__(self, pairing_list: List[List[Set[int]]]):
        self.pairing_list = [Pairing(pairing=pairing_row) for pairing_row in pairing_list]

    def count_number_of_subset_pairs(self) -> int:
        """Count the number of pairs containing a subset."""
        return sum(pairing.pair_contains_subset() for pairing in self.pairing_list)

    def count_overlapping_pairs(self) -> int:
        """Count the number of pairs containing a common element."""
        # Note: We could have made a "intersects_nontrivially" above in ``Pairing``.
        return sum(len(pairing.find_common_elts()) > 0 for pairing in self.pairing_list)


if __name__ == "__main__":
    raw_data = read_aoc_day_data_file(4)
    problem_assignment_pairs_list = input_parser(raw_data)
    pairings = Pairings(pairing_list=problem_assignment_pairs_list)

    # Part 1.
    print(f"Part 1: {pairings.count_number_of_subset_pairs()}")

    # Part 2.
    print(f"Part 2: {pairings.count_overlapping_pairs()}")
