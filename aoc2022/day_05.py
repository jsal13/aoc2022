import re
from queue import SimpleQueue
from typing import List

import numpy as np

from aoc2022.utils import read_aoc_day_data_file


class InputParser:
    """Parser for the Input to Day 5."""

    def __init__(self, data: str):
        self.data = data
        self.queue_raw, self.instructions_raw = self._split_queue_and_instructions()

        self.queue_length = self._get_queue_length()
        self.queue = self._parse_queue()

        self.instructions = self._parse_instructions()

    def _split_queue_and_instructions(self) -> tuple[str, str]:
        """Split the queue and instruction portion of the data."""
        queues_raw, instructions_raw = self.data.split("\n\n")
        return queues_raw, instructions_raw

    def _get_queue_length(self) -> int:
        """Get the length of the queue."""
        digits_strs = re.findall(r"([0-9]+) ", self.queue_raw)  # Gets all digits as strs.
        return max(map(int, digits_strs))

    def _parse_queue(self) -> List[List[str]]:
        """
        Parse queue portion of the data.

        Notes
        -----
        The regex does the following:
        - Removes all numbers,
        - Removes all brackets and replaces with spaces,
        - If any letter is preceeded by three spaces, replaces with just that letter.
            - This moves the letters to the left the appropriate amount.
        - Collapses any remaining 3-space intervals.
        - Removes initial space at the beginning of the lines.
        - Truncates each line to match the queue_length.

        """
        queue_letters_only = re.sub(r"[0-9]", "", self.queue_raw)
        queue_letters_only = re.sub(r"[\[\]]", " ", queue_letters_only)
        queue_letters_only = re.sub(r"   ([A-Z])", "\\1", queue_letters_only)
        queue_letters_only = re.sub(r"^ ", "", queue_letters_only)
        queue_letters_only = re.sub(r"   ", "", queue_letters_only)
        queue_letters_only = re.sub(r"\n ", "\n", queue_letters_only)
        queue_letters_list = [
            list(line) for line in queue_letters_only.split("\n") if line.strip()
        ]
        queue_letters_list.reverse()

        queue_list = [[] for _ in range(self.queue_length)]
        for line in queue_letters_list:
            for col, letter in enumerate(line):
                if letter.strip():  # If not a space...
                    queue_list[col].append(letter)

        for q in queue_list:
            print(q)
        return queue_list

    def _parse_instructions(self) -> List[tuple[int, int, int]]:
        """Parse instructions portion of the data."""
        return [
            tuple(map(int, val))
            for line in self.instructions_raw.splitlines()
            for val in re.findall(r"move (\d+) from (\d+) to (\d+)", line)
        ]


def execute_instructions_on_queue(
    queue: List[List[str]], instructions: tuple[int, int, int]
) -> List[List[str]]:
    """
    Execute instructions **in place** on ``queue``.

    Notes
    -----
    The instruction is of the form (a, b, c) where this corresponds to:
    "Move ``a`` elements, one at a time, from queue ``b-1`` to queue ``c-1``",
    adjusting for counting starting at 0.

    """
    for instruction in instructions:
        iter_number = instruction[0]
        column_from = instruction[1] - 1
        column_to = instruction[2] - 1

        for _ in range(iter_number):
            val = queue[column_from].pop()
            queue[column_to].append(val)
        print(queue)

    return queue


def get_top_values_in_queue(queue: List[List[str]]) -> List[str]:
    """Get top values from the queue."""
    return [row[-1] for row in queue]


DATA = """
    [D]
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

parsed_data = InputParser(DATA)
result = execute_instructions_on_queue(
    queue=parsed_data.queue, instructions=parsed_data.instructions
)


# if __name__ == "__main__":
# raw_data = read_aoc_day_data_file(5)
# parsed_data = InputParser(raw_data)
# problem_queue = parsed_data.queue
# problem_instructions = parsed_data.instructions
# result = execute_instructions_on_queue(
#     queue=problem_queue, instructions=problem_instructions
# )

# # Part 1.
# print(f"Part 1: {''.join(result)}")

#     # Part 2.
#     print(f"Part 2: {pairings.count_overlapping_pairs()}")
