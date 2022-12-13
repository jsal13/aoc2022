import math
import re
from dataclasses import dataclass
from functools import partial
from typing import Callable, List

from aoc2022.utils import read_aoc_day_data_file


@dataclass
class Monkey:
    """Represent Monkey in Day 11."""

    starting_items: List[int]
    operation: Callable[[int], int]
    test_value: int  # Divisible by int.
    test_result_actions: tuple[int, int]  # false, true.


def _operation_callable_base(x: int, value: str, operation: str) -> int:
    """Use to create a partial for ``operation_callable`` in ``parse_input()``."""
    if operation == "+":
        return x + int(value)

    if operation == "*":
        if value == "old":
            return x**2
        return x * int(value)

    raise ValueError(f"Cannot parse {x}, {value}, {operation}")


def parse_input(data: str) -> dict[int, Monkey]:
    """Parse input data for Day 11."""
    # NOTE: This can be broken down to smaller functions to unit test.
    monkeys = [[row.strip() for row in line.split("\n")] for line in data.split("\n\n")]

    monkey_dict: dict[int, Monkey] = {}
    for monkey in monkeys:
        monkey_key = int(re.findall(r"Monkey (\d+)?:", monkey[0])[0])

        # Get the numeric values in "Starting items: ..." line.
        starting_items = list(map(int, re.findall(": (.*)", monkey[1])[0].split(", ")))

        # This is always + or *, so we parse and create a callable.
        operation_str = re.findall(r": new = old (.*)", monkey[2])[0].strip()
        operation_list = operation_str.split(" ")

        operation_callable = partial(
            _operation_callable_base, value=operation_list[1], operation=operation_list[0]
        )

        # Parse this out to a number as it is always "divisible by some number."
        test_value = int(re.findall(r"Test: divisible by (\d+)", monkey[3])[0])

        # (false_value, true_value), and these are ints representing the monkey thrown to.
        true_val = int(re.findall(r"If true: throw to monkey (\d+)", monkey[4])[0])
        false_val = int(re.findall(r"If false: throw to monkey (\d+)", monkey[5])[0])
        test_result_actions = (false_val, true_val)

        monkey_dict[monkey_key] = Monkey(
            starting_items=starting_items,
            operation=operation_callable,
            test_value=test_value,
            test_result_actions=test_result_actions,
        )

    return monkey_dict


class Round:
    """Represent a round in Day 11 of Monkeys doing things."""

    def __init__(self, monkey_data: dict[int, Monkey]):
        self.monkey_data = monkey_data

        self.modulo_value = math.prod(
            monkey.test_value for monkey in self.monkey_data.values()
        )

        self.monkey_num_times_inspected = {idx: 0 for idx in range(len(self.monkey_data))}
        self.current_items = [
            self.monkey_data[i].starting_items for i in range(len(self.monkey_data))
        ]
        self.current_round = 1

    def do_a_round(self, divide_worry_level: bool = True):
        """Run an entire round with all monkeys."""
        # print(f"Round {self.current_round}")
        for idx in range(len(self.monkey_data)):
            # print(f"  Monkey {idx}:")
            self.individual_monkey_round(
                monkey_index=idx, divide_worry_level=divide_worry_level
            )
        self.current_round += 1

        # Update current values for items
        self.current_items = [
            self.monkey_data[i].starting_items for i in range(len(self.monkey_data))
        ]

    def individual_monkey_round(self, monkey_index: int, divide_worry_level: bool):
        """Run a single monkey's portion of the round."""
        current_monkey_data = self.monkey_data[monkey_index]
        for item in current_monkey_data.starting_items:
            self.monkey_num_times_inspected[monkey_index] += 1

            output_log = []
            output_log.append(f"Monkey inspects an item with a worry level of {item}.")

            worry_level = current_monkey_data.operation(item)
            output_log.append(f"Worry level is now {worry_level}")

            if divide_worry_level:
                worry_level = int(math.floor(worry_level / 3))
                output_log.append(
                    "Monkey gets bored with item.  "
                    f"Worry level is divided by 3 to {worry_level}."
                )

            if worry_level % current_monkey_data.test_value == 0:
                output_log.append(
                    f"Current worry level is divisible by {current_monkey_data.test_value}."
                )
                self.monkey_data[
                    current_monkey_data.test_result_actions[1]
                ].starting_items.append(worry_level % self.modulo_value)
                output_log.append(
                    f"Item with worry level {worry_level}"
                    f"is thrown to monkey {current_monkey_data.test_result_actions[1]}."
                )
            else:
                output_log.append("Current worry level is not divisible by 23.")
                self.monkey_data[
                    current_monkey_data.test_result_actions[0]
                ].starting_items.append(worry_level % self.modulo_value)
                output_log.append(
                    f"Item with worry level {worry_level}"
                    f" is thrown to monkey {current_monkey_data.test_result_actions[0]}."
                )

            # print("\n".join(output_log))
            # print()

        # Remove the current items.
        current_monkey_data.starting_items = []


if __name__ == "__main__":
    raw_data = read_aoc_day_data_file(11)

    test_data_parsed = parse_input(raw_data)

    # Part 1.
    rnd = Round(monkey_data=test_data_parsed)
    for _ in range(20):
        rnd.do_a_round()

    inspected_num_values = rnd.monkey_num_times_inspected.values()
    sorted_inspected_num_values = sorted(inspected_num_values, reverse=True)
    print(f"Part 1: {sorted_inspected_num_values[0] * sorted_inspected_num_values[1]}")

    # Part 2.
    rnd = Round(monkey_data=test_data_parsed)
    for _ in range(10_000):
        rnd.do_a_round(divide_worry_level=False)

    inspected_num_values = rnd.monkey_num_times_inspected.values()
    sorted_inspected_num_values = sorted(inspected_num_values, reverse=True)
    print(f"Part 2: {sorted_inspected_num_values[0] * sorted_inspected_num_values[1]}")
