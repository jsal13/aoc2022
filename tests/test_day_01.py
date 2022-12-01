import pytest
from hypothesis import assume, given, strategies

from aoc2022.day_01 import get_total_calories_per_elf, get_total_calories_top_n


@pytest.fixture(name="sample_raw_data")
def sample_raw_data_fixture():
    with open("./tests/data/day_01.txt", encoding="utf-8") as test_file:
        return test_file.read()


def test_get_total_calories_per_elf(sample_raw_data):
    test_value = get_total_calories_per_elf(sample_raw_data)
    assert sum(get_total_calories_top_n(test_value, n=1)) == 24000


test_total_cal_lists = [
    ([1, 2, 3, 4, 5, 6], 1, [6]),
    ([1, 2, 3, 4, 5, 6], 3, [6, 5, 4]),
]


@pytest.mark.parametrize("x,n,expected", test_total_cal_lists)
def test_get_total_calories_top_n(x, n, expected):
    assert get_total_calories_top_n(total_calorie_list=x, n=n) == expected


@given(total_cal_list=strategies.lists(strategies.integers()))
def test_get_total_calories_top_n_with_hypothesis(total_cal_list):
    assume(len(total_cal_list) > 0)
    assert get_total_calories_top_n(total_calorie_list=total_cal_list, n=1)[0] == max(
        total_cal_list
    )


def test_day_01_part_1_runs_end_to_end(sample_raw_data):
    cals_per_elf = get_total_calories_per_elf(sample_raw_data)
    max_cal = get_total_calories_top_n(cals_per_elf, n=1)[0]
    assert max_cal == 24000


def test_day_01_part_2_runs_end_to_end(sample_raw_data):
    cals_per_elf = get_total_calories_per_elf(sample_raw_data)
    max_cal = sum(get_total_calories_top_n(cals_per_elf, n=3))
    assert max_cal == 45000
