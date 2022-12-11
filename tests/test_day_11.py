# pylint: disable=protected-access
from functools import partial

import pytest

from aoc2022.day_11 import Monkey, _operation_callable_base, parse_input

INPUT_1_STR = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""".strip()


@pytest.fixture(name="input_1")
def input_1_fixture():
    return {
        0: Monkey(
            starting_items=[79, 98],
            operation=partial(_operation_callable_base, value="19", operation="*"),
            test_value=23,
            test_result_actions=(3, 2),
        ),
        1: Monkey(
            starting_items=[54, 65, 75, 74],
            operation=partial(_operation_callable_base, value="6", operation="+"),
            test_value=19,
            test_result_actions=(0, 2),
        ),
        2: Monkey(
            starting_items=[79, 60, 97],
            operation=partial(_operation_callable_base, value="old", operation="*"),
            test_value=13,
            test_result_actions=(3, 1),
        ),
        3: Monkey(
            starting_items=[74],
            operation=partial(_operation_callable_base, value="3", operation="+"),
            test_value=17,
            test_result_actions=(1, 0),
        ),
    }


# NOTE: Cannot use Hypothesis for this if we also want to use the fixture.
@pytest.mark.parametrize("x", [-10, -5, -1, 0, 1, 5, 10])
def test_parse_input_for_operations(x, input_1):
    monkeys = parse_input(INPUT_1_STR)
    for k, value in monkeys.items():
        assert value.operation(x) == input_1[int(k)].operation(x)
