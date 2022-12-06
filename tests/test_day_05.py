# pylint: disable=protected-access
from typing import List

import pytest

from aoc2022.day_05 import (
    InputParser,
    execute_instructions_on_queue,
    get_top_values_in_queue,
)


@pytest.fixture(name="test_data_raw")
def test_data_raw_fixture():
    return """
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


@pytest.fixture(name="test_data_queue")
def test_data_queue_fixture():
    return [["Z", "N"], ["M", "C", "D"], ["P"]]


@pytest.fixture(name="test_data_instructions")
def test_data_instructions_fixture() -> List[List[int]]:
    return [[1, 2, 1], [3, 1, 3], [2, 2, 1], [1, 1, 2]]


@pytest.fixture(name="class_input_parser")
def class_input_parser_fixture(test_data_raw) -> InputParser:
    return InputParser(test_data_raw)


# TODO: Why do I need to typehint here, if it's already in fixture?
def test_input_parser_parse_instructions(
    class_input_parser: InputParser, test_data_instructions
):
    assert class_input_parser._parse_instructions() == test_data_instructions


def test_input_parser_parse_queue(class_input_parser: InputParser, test_data_queue):
    assert class_input_parser._parse_queue() == test_data_queue


def test_execute_instructions_on_queue_bulk_move_false(class_input_parser: InputParser):
    queue = class_input_parser.queue
    instructions = class_input_parser.instructions

    assert execute_instructions_on_queue(
        queue=queue, instructions=instructions, bulk_move=False
    ) == [
        ["C"],
        ["M"],
        ["P", "D", "N", "Z"],
    ]


def test_execute_instructions_on_queue_bulk_move_true(class_input_parser: InputParser):
    queue = class_input_parser.queue
    instructions = class_input_parser.instructions

    assert execute_instructions_on_queue(
        queue=queue, instructions=instructions, bulk_move=True
    ) == [
        ["M"],
        ["C"],
        ["P", "Z", "N", "D"],
    ]


def test_get_top_values_in_queue(class_input_parser: InputParser):
    queue = class_input_parser.queue
    instructions = class_input_parser.instructions
    result = execute_instructions_on_queue(queue=queue, instructions=instructions)
    assert get_top_values_in_queue(result) == ["C", "M", "Z"]
