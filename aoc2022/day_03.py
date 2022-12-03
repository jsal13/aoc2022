from string import ascii_letters
from typing import List, Tuple

from aoc2022.utils import read_aoc_day_data_file


def input_parser(data: str) -> List[str]:
    """Parse input for Day 3."""
    return data.splitlines()


def alpha_mapping(letter: str) -> int:
    """
    Convert ascii_letters.

    Lowercase item types a through z have priorities 1 through 26.
    Uppercase item types A through Z have priorities 27 through 52.
    """
    return ascii_letters.index(letter) + 1


class Rucksack:
    """Represent the Rucksack with the contents."""

    def __init__(self, letters: str):
        self.letters = letters
        self.compartment_1, self.compartment_2 = self._split_into_compartments()

    def _split_into_compartments(self) -> Tuple[str, str]:
        """Split letters in half, creating two compartments."""
        self.num_letters = len(self.letters)
        self.split_index = int(self.num_letters / 2)
        return (self.letters[: self.split_index], self.letters[self.split_index :])

    def _find_common_item(self) -> str:
        """Find a single element common to both compartments."""
        common = set(self.compartment_1).intersection(set(self.compartment_2))
        if len(common) > 1:
            raise ValueError("More than one common letter in compartments!")

        return list(common)[0]

    def _convert_item_to_priority(self, letter: str) -> int:
        """Convert item to priority value."""
        return alpha_mapping(letter=letter)

    def get_common_item_priority(self):
        """Return common item's priority."""
        return self._convert_item_to_priority(self._find_common_item())


class Rucksacks:
    """Represent all Rucksacks with contents."""

    def __init__(self, letters_list: List[str]):
        self.letters_list = letters_list
        self.rucksack_list = [Rucksack(letters=letters) for letters in self.letters_list]

    def get_total_priority(self):
        """Sum total priority from all Rucksacks."""
        return sum(rucksack.get_common_item_priority() for rucksack in self.rucksack_list)

    def get_common_letter(self):
        """Return letter common to all ``Rucksack``s in ``rucksack_list``."""
        common = set.intersection(
            *[set(rucksack.letters) for rucksack in self.rucksack_list]
        )

        if len(common) == 0:
            raise ValueError(
                f"No common elements found in Rucksacks: {self.rucksack_list}"
            )

        if len(common) > 1:
            raise ValueError("More than one common letter in compartments!")

        return list(common)[0]

    def get_common_letter_priority(self) -> int:
        """Return common item's priority."""
        return alpha_mapping(self.get_common_letter())


if __name__ == "__main__":
    raw_data = read_aoc_day_data_file(3)
    problem_letters_list = input_parser(raw_data)

    # Part 1.
    rucksacks = Rucksacks(letters_list=problem_letters_list)
    print(f"Part 1: {rucksacks.get_total_priority()}")

    # Part 2.
    total: int = 0
    for idx in range(0, len(problem_letters_list), 3):
        rucksacks = Rucksacks(letters_list=problem_letters_list[idx : idx + 3])
        total += rucksacks.get_common_letter_priority()

    print(f"Part 2: {total}")
