# pylint: disable=protected-access
from textwrap import dedent

import pytest

from aoc2022.day_02 import (
    Game,
    Round,
    parse_input,
    part_1_rps_conversion,
    part_2_rps_conversion,
    rps_rules,
)

# from hypothesis import assume, given, strategies


@pytest.fixture(name="test_data_raw")
def test_data_raw_fixture():
    data = dedent(
        """
        A Y
        B X
        C Z
        """
    ).strip()
    return data


TEST_ROUNDS = [["R", "Y"], ["P", "X"], ["S", "Z"]]

TEST_ROUNDS_PART_1 = [["R", "P"], ["P", "R"], ["S", "S"]]
TEST_ROUNDS_PART_1_EXPECTED_POINTS = [8, 1, 6]
TEST_ROUNDS_PART_1_WLD = ["Lose", "Win", "Draw"]

TEST_ROUNDS_PART_2 = [["R", "R"], ["P", "R"], ["S", "R"]]
TEST_ROUNDS_PART_2_EXPECTED_POINTS = [4, 1, 7]


def test_parse_input(test_data_raw):
    assert parse_input(test_data_raw) == TEST_ROUNDS


def test_part_1_rps_conversion():
    assert part_1_rps_conversion(TEST_ROUNDS) == TEST_ROUNDS_PART_1


def test_part_2_rps_conversion():
    assert part_2_rps_conversion(TEST_ROUNDS) == TEST_ROUNDS_PART_2


@pytest.mark.parametrize(
    "test_round,expected", list(zip(TEST_ROUNDS_PART_1, TEST_ROUNDS_PART_1_WLD))
)
def test_rps_rules(test_round, expected):
    assert rps_rules(test_round[0], test_round[1]) == expected


@pytest.mark.parametrize("test_round,expected", list(zip(TEST_ROUNDS_PART_1, [6, 0, 3])))
def test_round_method_calculate_round_score(test_round, expected):
    assert Round(row=test_round)._calculate_wld_score() == expected


@pytest.mark.parametrize("test_round,expected", list(zip(TEST_ROUNDS_PART_1, [2, 1, 3])))
def test_round_method_calculate_shape_score(test_round, expected):
    assert Round(row=test_round)._calculate_shape_score() == expected


@pytest.mark.parametrize(
    "test_round,expected",
    list(zip(TEST_ROUNDS_PART_1, TEST_ROUNDS_PART_1_EXPECTED_POINTS)),
)
def test_round_method_round_score_part_1(test_round, expected):
    assert Round(row=test_round).round_score() == expected


@pytest.mark.parametrize(
    "test_rounds,expected",
    [(TEST_ROUNDS_PART_1, sum(TEST_ROUNDS_PART_1_EXPECTED_POINTS))],
)
def test_rounds_attribute_total_part_1(test_rounds, expected):
    assert Game(rows=test_rounds).total == expected


@pytest.mark.parametrize(
    "test_round,expected",
    list(zip(TEST_ROUNDS_PART_2, TEST_ROUNDS_PART_2_EXPECTED_POINTS)),
)
def test_round_method_round_score_part_2(test_round, expected):
    assert Round(row=test_round).round_score() == expected


@pytest.mark.parametrize(
    "test_rounds,expected",
    [(TEST_ROUNDS_PART_2, sum(TEST_ROUNDS_PART_2_EXPECTED_POINTS))],
)
def test_rounds_attribute_total_part_2(test_rounds, expected):
    assert Game(rows=test_rounds).total == expected
