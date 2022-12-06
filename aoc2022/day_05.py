import copy
import re
from typing import List

import numpy as np

from aoc2022.utils import read_aoc_day_data_file


class InputParser:
    """Parser for the Input to Day 5."""

    def __init__(self, data: str):
        self.data = data
        self.queue_raw, self.instructions_raw = self._split_queue_and_instructions()
        self.queue = self._parse_queue()
        self.instructions = self._parse_instructions()

    def _split_queue_and_instructions(self) -> tuple[str, str]:
        """Split the queue and instruction portion of the data."""
        queues_raw, instructions_raw = self.data.split("\n\n")
        return queues_raw, instructions_raw

    def _parse_queue(self) -> List[List[str]]:
        """
        Parse queue portion of the data.

        Notes
        -----
        Omg, make this better.
        """
        queue_lines = self.queue_raw.splitlines()
        queue_lines = queue_lines[:-1]  # Removes numbers line.
        queue_lines = [
            line for line in queue_lines if line.strip()
        ]  # Removes blank lines.

        queue_letters = []
        for line in queue_lines:
            new_line = []
            for idx in range(0, len(line), 4):
                new_line.append(line[idx : idx + 4])

            # Remove extra spaces and brackets.
            new_line = [re.sub(r"[ \[\]]", "", item) for item in new_line]
            queue_letters.append(new_line)

        # Find the largest row, extend all other rows to match that length.
        max_row_length = len(max(queue_letters, key=len))

        queue_letters_matrix = []
        for row in queue_letters:
            empty_space = [""] * (max_row_length - len(row))
            queue_letters_matrix.append([*row, *empty_space])

        queue_letters_matrix = np.transpose(np.array(queue_letters_matrix)).tolist()

        queue = []
        for row in queue_letters_matrix:
            queue.append([letter for letter in row[::-1] if letter != ""])

        return queue

    def _parse_instructions(self) -> List[List[int]]:
        """Parse instructions portion of the data."""
        return [
            list(map(int, val))
            for line in self.instructions_raw.splitlines()
            for val in re.findall(r"move (\d+) from (\d+) to (\d+)", line)
        ]


def execute_instructions_on_queue(
    queue: List[List[str]], instructions: List[List[int]], bulk_move: bool = False
) -> List[List[str]]:
    """
    Execute instructions on ``queue``.

    ``bulk_move`` implies each are moved at once, instead of one at a time.

    Notes
    -----
    The instruction is of the form (a, b, c) where this corresponds to:
    "Move ``a`` elements, one at a time, from queue ``b-1`` to queue ``c-1``",
    adjusting for counting starting at 0.

    """
    tmp_queue = copy.deepcopy(queue)  # To prevent overwriting queue.
    for instruction in instructions:
        iter_number = instruction[0]
        column_from = instruction[1] - 1
        column_to = instruction[2] - 1

        if bulk_move:
            vals = tmp_queue[column_from][-1 * iter_number :]
            for _ in range(iter_number):
                tmp_queue[column_from].pop()
            tmp_queue[column_to] = [*tmp_queue[column_to], *vals]
        else:
            for _ in range(iter_number):
                val = tmp_queue[column_from].pop()
                tmp_queue[column_to].append(val)

    return tmp_queue


def get_top_values_in_queue(queue: List[List[str]]) -> List[str]:
    """Get top values from the queue."""
    return [row[-1] for row in queue]


if __name__ == "__main__":
    raw_data = read_aoc_day_data_file(5)

    # Part 1:
    parsed_data = InputParser(raw_data)
    problem_queue = parsed_data.queue
    problem_instructions = parsed_data.instructions
    result = execute_instructions_on_queue(
        queue=problem_queue, instructions=problem_instructions, bulk_move=False
    )

    print(f"Part 1: {''.join(i[-1] for i in result)}")

    # Part 2:
    result = execute_instructions_on_queue(
        queue=problem_queue, instructions=problem_instructions, bulk_move=True
    )
    print(f"Part 2: {''.join(i[-1] for i in result)}")
