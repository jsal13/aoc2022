from unittest.mock import patch

import pytest
from hypothesis import example, given, strategies

from aoc2022.function_sample import (
    add_two_positive_numbers,
    call_expensive_function,
    square_int_and_add_one,
    strip_numbers_bad_function,
    sum_up_integers,
)

input_and_expected = [(1, 1, 2), (1, 2, 3), (2, 1, 3), (2, 2, 4)]

# ======
# PYTEST
# ======

# PARAMETERIZATION


@pytest.mark.parametrize("x,y,expected", input_and_expected)
def test_add_two_positive_numbers_valid_cases_1(x: int, y: int, expected: int):
    assert add_two_positive_numbers(x, y) == expected


@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [1, 2])
def test_add_two_positive_numbers_valid_cases_2(x: int, y: int):
    assert add_two_positive_numbers(x, y) == x + y


@pytest.mark.parametrize("x", [-1, 0])
@pytest.mark.parametrize("y", [-1, 0, 1])
def test_add_two_positive_numbers_exception_cases(x: int, y: int):
    with pytest.raises(ValueError, match=r"[xy] must be positive.$"):
        add_two_positive_numbers(x, y)


# MOCKING FUNCTIONS


@patch("aoc2022.function_sample.add_one")
def test_square_int_and_add_one_with_mocked_add_one(mock_add_one):
    mock_add_one.return_value = 3
    assert square_int_and_add_one(4) == 3


data = [(1, 1), (2, 2), (3, 3)]


@pytest.mark.parametrize("x,expected", data)
@patch("aoc2022.function_sample.add_one")
@patch("aoc2022.function_sample.square_int")
def test_square_int_and_add_one_with_mocked_inner_functions(
    mock_add_one, mock_square_int, x, expected
):
    mock_add_one.return_value = x
    mock_square_int.return_value = x
    assert square_int_and_add_one(x) == expected


@patch("aoc2022.function_sample.expensive_function")
def test_call_expensive_function(mock_expensive_function):
    resp = call_expensive_function()

    assert resp
    # mock_expensive_function.assert_not_called()
    mock_expensive_function.assert_called_once()


# ==========
# HYPOTHESIS
# ==========


@given(s=strategies.text())
@example("")
@example("9")
def test_strip_numbers_bad_function(s):
    val = strip_numbers_bad_function(s)
    if val != "":
        assert val.isalpha()


@given(nums=strategies.lists(strategies.integers()))
def test_sum_up_integers(nums):
    assert sum_up_integers(nums) == sum(nums)


@given(x=strategies.integers())
@patch("aoc2022.function_sample.add_one")
@patch("aoc2022.function_sample.square_int")
def test_square_int_and_add_one_with_mocked_inner_functions_fuzzing(
    mock_add_one, mock_square_int, x
):
    mock_add_one.return_value = x
    mock_square_int.return_value = x
    assert square_int_and_add_one(x) == x
