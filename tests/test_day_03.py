# pylint: disable=protected-access
from string import ascii_letters

import pytest
from hypothesis import given
from hypothesis import strategies as st

from aoc2022.day_03 import Rucksack, Rucksacks, alpha_mapping, input_parser


@pytest.fixture(name="test_data_raw")
def test_data_raw_fixture():
    return """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""".strip()


@pytest.fixture(name="test_data")
def test_data_fixture():
    return [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
        "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
        "ttgJtRGJQctTZtZT",
        "CrZsJsPPZsGzwwsLwLmpwMDw",
    ]


def test_data_parser(test_data_raw, test_data):
    assert input_parser(test_data_raw) == test_data


TEST_ITEM_SPLIT = [
    ("vJrwpWtwJgWrhcsFMMfFFhFp", ("vJrwpWtwJgWr", "hcsFMMfFFhFp")),
    ("jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL", ("jqHRNqRjqzjGDLGL", "rsFMfFZSrLrFZsSL")),
    ("wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn", ("wMqvLMZHhHMvwLH", "jbvcjnnSBnvTQFn")),
    ("PmmdzqPrVvPwwTWBwg", ("PmmdzqPrV", "vPwwTWBwg")),
    ("ttgJtRGJQctTZtZT", ("ttgJtRGJ", "QctTZtZT")),
    ("CrZsJsPPZsGzwwsLwLmpwMDw", ("CrZsJsPPZsGz", "wwsLwLmpwMDw")),
]


@pytest.mark.parametrize("letters,expected", TEST_ITEM_SPLIT)
def test_rucksack_method_split_into_compartments(letters, expected):
    rucksack = Rucksack(letters)
    assert rucksack._split_into_compartments() == expected


@given(letter=st.text(min_size=1, max_size=1, alphabet=ascii_letters))
def test_alpha_mapping(letter):
    assert alpha_mapping(letter) == ascii_letters.index(letter) + 1


TEST_ITEM_COMMON_ELT = [
    ("vJrwpWtwJgWrhcsFMMfFFhFp", "p"),
    ("jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL", "L"),
    ("PmmdzqPrVvPwwTWBwg", "P"),
    ("wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn", "v"),
    ("ttgJtRGJQctTZtZT", "t"),
    ("CrZsJsPPZsGzwwsLwLmpwMDw", "s"),
]


@pytest.mark.parametrize("letters,expected", TEST_ITEM_COMMON_ELT)
def test_rucksack_method_find_common_item(letters, expected):
    rucksack = Rucksack(letters)
    assert rucksack._find_common_item() == expected


@given(letter=st.text(min_size=1, max_size=1, alphabet=ascii_letters))
def test_rucksack_method_convert_item_to_priority(letter):
    rucksack = Rucksack(letters=[])
    assert rucksack._convert_item_to_priority(letter) == alpha_mapping(letter)


TEST_RUCKSACK_COMMON_ITEM_VALUES = [
    ("vJrwpWtwJgWrhcsFMMfFFhFp", 16),
    ("jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL", 38),
    ("PmmdzqPrVvPwwTWBwg", 42),
    ("wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn", 22),
    ("ttgJtRGJQctTZtZT", 20),
    ("CrZsJsPPZsGzwwsLwLmpwMDw", 19),
]


@pytest.mark.parametrize("letters,expected", TEST_RUCKSACK_COMMON_ITEM_VALUES)
def test_rucksack_method_get_common_item_priority(letters, expected):
    rucksack = Rucksack(letters=letters)
    assert rucksack.get_common_item_priority() == expected


def test_rucksacks_method_get_total_priority(test_data):
    rucksacks = Rucksacks(letters_list=test_data)
    assert rucksacks.get_total_priority() == 157


TEST_RUCKSACK_PART_2_THREE_SACKS_COMMON_LETTER = [
    (
        [
            "vJrwpWtwJgWrhcsFMMfFFhFp",
            "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
            "PmmdzqPrVvPwwTWBwg",
        ],
        "r",
    ),
    (
        [
            "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
            "ttgJtRGJQctTZtZT",
            "CrZsJsPPZsGzwwsLwLmpwMDw",
        ],
        "Z",
    ),
]


@pytest.mark.parametrize(
    "letters_list,expected", TEST_RUCKSACK_PART_2_THREE_SACKS_COMMON_LETTER
)
def test_rucksacks_method_get_common_letter(letters_list, expected):
    assert Rucksacks(letters_list=letters_list).get_common_letter() == expected


TEST_RUCKSACK_PART_2_THREE_SACKS_COMMON_LETTER_PRIORITY = [
    (
        [
            "vJrwpWtwJgWrhcsFMMfFFhFp",
            "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
            "PmmdzqPrVvPwwTWBwg",
        ],
        18,
    ),
    (
        [
            "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
            "ttgJtRGJQctTZtZT",
            "CrZsJsPPZsGzwwsLwLmpwMDw",
        ],
        52,
    ),
]


@pytest.mark.parametrize(
    "letters_list,expected", TEST_RUCKSACK_PART_2_THREE_SACKS_COMMON_LETTER_PRIORITY
)
def test_rucksacks_method_get_common_letter_priority(letters_list, expected):
    assert Rucksacks(letters_list=letters_list).get_common_letter_priority() == expected
